#!/usr/bin/env python3
"""Autoroute hardware/pico-k.kicad_pcb with Freerouting as a separate process (DSN export -> Freerouting -> SES import).

Order: build_pcb.py -> fanout.py --no-stitch -> route.py -> fanout.py (stitching) -> DRC.
Run with the KiCad Python venv ($KT, see STATUS toolchain): $KT hardware/gen/pcb/route.py [--timeout HH:MM:SS]
Env: FR_JAR = Freerouting jar, FR_JAVA = its Java runtime (default `java`); both must equal toolchain.lock.yaml
(tools.freerouting: version, sha256, java; D-019: 2.2.4 on OpenJDK 25.0.4.1), checked before the run.
- DSN is written by KiCad (pcbnew.ExportSpecctraDSN) and edited in patch_dsn() (see the numbered steps there):
  signals on F.Cu, In2.Cu (D-020, staged: leftovers only; USB D+/D- excluded) and B.Cu; In1 (GND) is a plane; GND/3V3 are not
  autorouted (In2 3V3 pour refilled around the In2 tracks after import).
- Freerouting runs headless (gui.enabled=false), with analytics disabled (usage_and_diagnostic_data.disable_analytics
  and profile.allow_telemetry=false, on the command line and in the user settings file) and inside an empty network
  namespace (unshare -rn): 2.1.0 ... 2.2.4 have no switch for the start-up GitHub version check (VersionChecker is
  started unconditionally in Freerouting.main), so the namespace makes that check (and any other network access) fail.
- SES is read back by KiCad (pcbnew.ImportSpecctraSES), which replaces all tracks and vias: the GND/3V3 fanout copper
  is saved before and added back after; then zones are refilled and the board is saved.
- Freerouting 2.2.4: end runs by --passes, not by --timeout. When the job timeout + 30 s grace passes while the
  router is still in a pass, its monitor sets TIMED_OUT and the job never reaches COMPLETED, so main() waits forever
  and no SES is written (RoutingJobSchedulerActionThread, v2.2.4; seen twice on pico-k). Keep the timeout as a backstop.
- Always load/save the board at its project path: pcbnew rewrites pico-k.kicad_pro with defaults otherwise.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import pcbnew

ROOT = Path(__file__).resolve().parents[3]
PCB = ROOT / "hardware" / "pico-k.kicad_pcb"
WORK = ROOT / "out" / "route"
LOCK = ROOT / "toolchain.lock.yaml"


def pinned_freerouting() -> tuple[Path, str]:
    """(jar, java) after checking both against the tier-1 lock entry."""
    import yaml
    want = yaml.safe_load(LOCK.read_text())["tools"]["freerouting"]
    jar, java = Path(os.environ["FR_JAR"]), os.environ.get("FR_JAVA", "java")
    if hashlib.sha256(jar.read_bytes()).hexdigest() != want["sha256"]:
        raise SystemExit(f"{jar}: sha256 does not match the locked Freerouting {want['version']}")
    r = subprocess.run([java, "-version"], capture_output=True, text=True)
    m = re.search(r'version "([^"]+)"', r.stderr + r.stdout)
    if want.get("java") and (not m or m.group(1) != str(want["java"])):
        raise SystemExit(f"{java}: Java {m.group(1) if m else '?'} != locked {want['java']} for Freerouting")
    return jar, java


def user_settings(d: Path) -> None:
    """Analytics/telemetry off in the settings file too (Freerouting rewrites it with defaults otherwise)."""
    d.mkdir(parents=True, exist_ok=True)
    f = d / "freerouting.json"
    if not f.exists():   # a hand-written partial file crashes 2.2.4 (null profile id): let it write its own first
        return
    s = json.loads(f.read_text())
    s.setdefault("usage_and_diagnostic_data", {})["disable_analytics"] = True
    s.setdefault("profile", {})["allow_telemetry"] = False
    s.setdefault("gui", {})["enabled"] = False
    f.write_text(json.dumps(s, indent=2))


PLANE_NETS = ("GND", "3V3")
# D-020: signals on F.Cu, In2.Cu (3V3 pour flows around them) and B.Cu; In1.Cu (GND) stays a solid plane.
SIGNAL_LAYERS = ("F.Cu", "In2.Cu", "B.Cu")
# nets left open by the F/B-only run (b71be51), small signals only (no power, no USB, no crystal)
IN2_NETS = r"^/GP(8|9|10|18|19|20|21|22|25|26|27|28)$|QSPI|^/ADC_(AVDD|VREF)$|^/BOOTSEL$|^/SMPS_PS$|_SENSE$|D2-A|Q1-D"
USB_NETS = ("Net-(U1-USB_DM)", "Net-(U1-USB_DP)", "/USB_CONN_DM", "/USB_CONN_DP")  # F/B only: not in IN2_NETS


def _poly(coords) -> str:
    return " ".join(f"{x:.0f} {y:.0f}" for x, y in coords)


def subset_nets(s: str, pattern: str | None, exclude: str | None) -> str:
    """Staged routing: keep only the nets matching pattern (and not exclude) in the network section."""
    a = s.index("  (network"); b = s.index("    (class", a)
    blocks = re.findall(r"(\n    \(net (\S+)\n.*?\n    \))", s[a:b], re.S)
    keep = [blk for blk, n in blocks if (not pattern or re.search(pattern, n)) and not (exclude and re.search(exclude, n))]
    return s[:a] + "  (network" + "".join(keep) + "\n" + s[b:]


def patch_dsn(src: Path, dst: Path, signal_layers=SIGNAL_LAYERS, nets=None, exclude=None, in2_nets=None) -> None:
    """Edit KiCad's DSN for this board (units: um). Each step keeps Freerouting inside the KiCad/JLC rules."""
    from shapely.geometry import LineString, Polygon  # noqa: PLC0415
    s = src.read_text()
    # 1. J4 castellation ovals are centred on the outline (half outside the board): Freerouting counts every one as a
    #    violation and routes as if the board were broken there. Drop them (the PTH pin pad on the same pin stays) and
    #    keep 0.8 mm strips along both long edges free of other copper instead.
    ov = re.findall(r"\n\s*\(pin Oval\[A\]Pad_2410\.000000x1600\.000000_um ([\d@]+) [-\d.]+ [-\d.]+\)", s)
    s = re.sub(r"\n\s*\(pin Oval\[A\]Pad_2410\.000000x1600\.000000_um [\d@]+ [-\d.]+ [-\d.]+\)", "", s)
    for n in ov:
        s = re.sub(rf"(?<=[\s(])J4-{re.escape(n)}(?=[\s)])", "", s)
    ko = [f'(keepout "" (polygon signal 0  {_poly([(a, -100000), (b, -100000), (b, -151000), (a, -151000), (a, -100000)])}))'
          for a, b in ((100000, 100800), (120200, 121000))]
    # 2. inner cut-outs (PCC-SMD slots) are exported as keepouts with no margin: grow them by 0.25 (edge clearance 0.2)
    def grow(m):
        n = [float(v) for v in m.group(1).split()]
        g = Polygon(list(zip(n[0::2], n[1::2]))).buffer(250, resolution=4)
        return f'(keepout "" (polygon signal 0  {_poly(g.exterior.coords)}))'
    s = re.sub(r'\(keepout "" \(polygon signal 0\s+([-\d\s.]+)\)\)', grow, s)
    # 3. GND / 3V3 are not autorouted (In1 GND / In2 3V3 planes, KiCad pours, fanout.py vias): remove the nets and
    #    turn their existing fanout copper into keepouts (+0.025 via margin) so the space stays reserved.
    def wire(m):
        g = LineString([(float(m.group(3)), float(m.group(4))), (float(m.group(5)), float(m.group(6)))]).buffer(
            float(m.group(2)) / 2 + 25, resolution=4)
        ko.append(f'(keepout "" (polygon {m.group(1)} 0  {_poly(g.exterior.coords)}))')
        return ""
    s = re.sub(r"\n\s*\(wire \(path (\S+) (\d+)\s+(-?\d+) (-?\d+)\s+(-?\d+) (-?\d+)\)\(net (?:GND|3V3)\)\(type \w+\)\)",
               wire, s)
    def via(m):
        ko.append(f'(keepout "" (circle signal 500 {m.group(1)} {m.group(2)}))')
        return ""
    s = re.sub(r'\n\s*\(via "Via\[0-3\]_450:200_um"\s+(-?\d+) (-?\d+) \(net (?:GND|3V3)\)\(type \w+\)\)', via, s)
    for n in PLANE_NETS:
        s = re.sub(rf"\n\s*\(net {n}\s*\n\s*\(pins[^)]*\)\s*\)", "", s)
        s = re.sub(rf"(\(class Power[^\n]*?) {n}(?=[ \n])", r"\1", s)
    s = re.sub(r"\n\s*\(plane [^\n]*\n[^\n]*\)\)", "", s)
    # 4. layers that carry no signals become Specctra power layers (In1 = unbroken GND reference for USB / TC)
    for lay in ("F.Cu", "In1.Cu", "In2.Cu", "B.Cu"):
        if lay not in signal_layers:
            s, k = re.subn(rf"\(layer {re.escape(lay)}\s*\(type signal\)", f"(layer {lay}\n      (type power)", s)
            assert k == 1, lay
    # 5. pre-placed signal copper (U1 escape vias/stubs from fanout.py) is fixed, Freerouting routes from it
    s = re.sub(r"(\(wire \(path [^\n]*?\)\(net [^)]*\)\(type) route\)", r"\1 fix)", s)
    s = re.sub(r'(\(via "Via\[0-3\]_450:200_um"\s+-?\d+ -?\d+ \(net [^)]*\)\(type) route\)', r"\1 fix)", s)
    s = s.replace('\n    (via "Via[0-3]', "".join("\n    " + k for k in ko) + '\n    (via "Via[0-3]', 1)
    # 6. Power class: Freerouting 2.1.0 does not neck down, and a 0.3 mm track cannot leave a 0.2 mm QFN-60 pad at
    #    0.4 mm pitch with 0.15 clearance. Nets on U1 pins route at 0.2 mm (DVDD ~ 0.1-0.2 A, VREG_LX/PGND short);
    #    the TPS63001 / input nets (VBUS, VSYS, L1, L2; up to ~1 A peak, ESTIMATE) keep 0.3 mm (VSON-10 0.5 pitch).
    hi = ("VBUS", "VSYS", '"Net-(U3-L1)"', '"Net-(U3-L2)"')
    m = re.search(r"\(class Power (.*?)\(circuit", s, re.S)
    if m:
        names = m.group(1).split()
        lo = [n for n in names if n not in hi]
        hin = [n for n in names if n in hi]
        block = s[m.start():s.index("\n    )", m.start()) + 6]
        new = block.replace(m.group(1), " ".join(lo) + "\n      ").replace("(width 300)", "(width 200)")
        new += "\n" + block.replace("(class Power", "(class PowerHi").replace(m.group(1), " ".join(hin) + "\n      ")
        s = s.replace(block, new)
    # 7. PTH holes with a thin ring: JLC PTH-to-track 0.28 (kicad_dru) is a hole rule that Freerouting does not know;
    #    it keeps only the 0.1 copper clearance. The PCC-SMD slots (J2/J3: 0.61 x 3.25 drill in a 0.91 oval, ring
    #    0.15) are widened in the DSN only to drill + 2 x (0.28 - 0.1) + 0.04 = 1.01 so tracks keep 0.28 to the hole.
    s = re.sub(r"(\(padstack Oval\[A\]Pad_910\.000000x3550\.000000_um.*?\(attach off\))",
               lambda m: re.sub(r"(\(path \S+ )910 ", r"\g<1>1010 ", m.group(1)), s, flags=re.S)
    # 8. (no layer costs: any (autoroute_settings ...) scope in the DSN makes Freerouting 2.2.4 start with 0 nets to
    #    route, even a bare "(autoroute on)"; tested 2026-10-16. Short In2 use comes from staging instead: route
    #    F/B first, then only the leftover nets with In2 enabled and the earlier copper fixed.)
    # 9. D-020: In2 only for the nets matching in2_nets (small signals that do not fit on F/B); every other class,
    #    including USB D+/D- and all power nets, gets (use_layer F.Cu B.Cu). Keeps In2 use short and the 3V3 pour
    #    whole (an all-nets In2 run used 333 mm on In2 and split the pour into 10 pieces).
    if "In2.Cu" in signal_layers:
        a = s.index("  (network"); b = s.index("  (wiring", a)
        net_s = s[a:b]
        allowed = []
        if in2_nets:
            i0 = net_s.index("(class kicad_default"); j0 = net_s.index("(circuit", i0)
            head = net_s[i0:j0]
            names = re.findall(r'"[^"]+"|[^\s()"]+', head[len("(class kicad_default"):])
            allowed = [n for n in names if re.search(in2_nets, n.strip('"'))]
            for n in allowed:
                head = re.sub(rf'\s{re.escape(n)}(?=[\s)])', "", head, count=1)
            net_s = net_s[:i0] + head + net_s[j0:]
        net_s = net_s.replace('(use_via "Via[0-3]_450:200_um")\n',
                              '(use_via "Via[0-3]_450:200_um")\n        (use_layer F.Cu B.Cu)\n')
        if allowed:
            cls = ("    (class In2ok " + " ".join(allowed) +
                   '\n      (circuit\n        (use_via "Via[0-3]_450:200_um")\n      )\n'
                   "      (rule\n        (width 150)\n        (clearance 100)\n      )\n    )\n")
            k = net_s.index("    (class kicad_default")
            net_s = net_s[:k] + cls + net_s[k:]
        s = s[:a] + net_s + s[b:]
        print(f"In2 allowed for {len(allowed)} nets: {' '.join(allowed)}")
    if nets or exclude:
        s = subset_nets(s, nets, exclude)
    dst.write_text(s)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--passes", type=int, default=30)
    ap.add_argument("--threads", type=int, default=max(1, (os.cpu_count() or 2) - 1))
    ap.add_argument("--timeout", default="00:10:00", help="Freerouting job timeout HH:MM:SS (2.1.0 ignores max_passes)")
    ap.add_argument("--via-costs", type=int, default=50, help="Freerouting router.scoring.via_costs (2.1.0 default 50)")
    ap.add_argument("--opt-passes", type=int, default=2,
                    help="Freerouting 2.2 optimizer passes after routing (default 100 there, no time limit: it ran past "
                         "the job timeout and wrote no SES)")
    ap.add_argument("--in2-nets", default=IN2_NETS, help="regex: nets that may use In2 (all others F/B only)")
    ap.add_argument("--no-in2", action="store_true", help="signals on F.Cu/B.Cu only (stage 1 of D-020 staging)")
    ap.add_argument("--nets", help="staged routing: only nets matching this regex (others stay unrouted)")
    ap.add_argument("--exclude", help="staged routing: skip nets matching this regex")
    ap.add_argument("--no-route", action="store_true", help="only export/patch the DSN")
    a = ap.parse_args()
    jar, java = pinned_freerouting()
    WORK.mkdir(parents=True, exist_ok=True)
    board = pcbnew.LoadBoard(str(PCB))
    raw, dsn, ses = WORK / "pico-k.raw.dsn", WORK / "pico-k.dsn", WORK / "pico-k.ses"
    if not pcbnew.ExportSpecctraDSN(board, str(raw)):
        raise SystemExit("DSN export failed")
    patch_dsn(raw, dsn, signal_layers=("F.Cu", "B.Cu") if a.no_in2 else SIGNAL_LAYERS, nets=a.nets, exclude=a.exclude, in2_nets=a.in2_nets)
    if a.no_route:
        return 0
    ses.unlink(missing_ok=True)
    user_settings(WORK / "freerouting-user")
    cmd = ["unshare", "-rn", java, "-jar", str(jar), "-de", str(dsn), "-do", str(ses),
           "--gui.enabled=false", "--usage_and_diagnostic_data.disable_analytics=true", "--profile.allow_telemetry=false",
           f"--router.max_passes={a.passes}", f"--router.max_threads={a.threads}",
           f"--router.job_timeout={a.timeout}", f"--router.optimizer.max_passes={a.opt_passes}", f"--router.scoring.via_costs={a.via_costs}",
           f"--user_data_path={WORK / 'freerouting-user'}"]
    with open(WORK / "freerouting.log", "w") as log:
        h, m, sec = (int(v) for v in a.timeout.split(":"))
        try:   # 2.1.0 hung headless after an error: hard stop 5 min after the job timeout
            subprocess.run(cmd, stdout=log, stderr=subprocess.STDOUT, check=False, timeout=h * 3600 + m * 60 + sec + 300)
        except subprocess.TimeoutExpired:
            print("Freerouting did not exit, killed")
    if not ses.exists():
        raise SystemExit("Freerouting wrote no SES, see out/route/freerouting.log")
    board = pcbnew.LoadBoard(str(PCB))
    keep = [t.Duplicate() for t in board.GetTracks()]   # SES has only what Freerouting routed (no fixed copper)
    if not pcbnew.ImportSpecctraSES(board, str(ses)):
        raise SystemExit("SES import failed")
    for t in keep:   # fanout + escape copper (fixed or keepouts in the DSN), not in the SES
        board.Add(t)
    board.BuildConnectivity()
    pcbnew.ZONE_FILLER(board).Fill(board.Zones())
    pcbnew.SaveBoard(str(PCB), board)
    print("routed:", sum(1 for t in board.GetTracks() if t.Type() == pcbnew.PCB_TRACE_T), "tracks,",
          sum(1 for t in board.GetTracks() if t.Type() == pcbnew.PCB_VIA_T), "vias")
    return 0


if __name__ == "__main__":
    sys.exit(main())
