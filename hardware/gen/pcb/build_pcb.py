#!/usr/bin/env python3
"""Build hardware/pico-k.kicad_pcb from the schematic netlist + placement.yaml with KiCad's own pcbnew API.

Run with the KiCad Python venv (system pcbnew + PyYAML): $KT hardware/gen/pcb/build_pcb.py (KT = a venv with system site packages + PyYAML, see STATUS toolchain)
Inputs : out/netlist.net (kicad-cli sch export netlist --format kicadsexpr), hardware/gen/pcb/placement.yaml,
         hardware/fp-lib-table (footprint libraries).
Output : hardware/pico-k.kicad_pcb (outline, 4-layer 1.0 mm stack, net classes, placed footprints with nets,
         zones, silkscreen notes). Routing is done afterwards by Freerouting (route.sh, separate process).
Fab numbers: JLCPCB PCB capabilities page (https://jlcpcb.com/capabilities/pcb-capabilities, read 2026-10-15),
see hardware/pico-k.kicad_dru.
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path

import pcbnew
import yaml

ROOT = Path(__file__).resolve().parents[3]
HW = ROOT / "hardware"
PCB = HW / "pico-k.kicad_pcb"
MM = pcbnew.FromMM
W, H = 21.0, 51.0          # Pico 2 Fig. 3 p.7


def sexp(text: str):
    toks = re.findall(r'"(?:[^"\\]|\\.)*"|\(|\)|[^\s()]+', text)
    stack, cur = [], []
    for t in toks:
        if t == "(":
            stack.append(cur); cur = []
        elif t == ")":
            done = cur; cur = stack.pop(); cur.append(done)
        else:
            cur.append(t[1:-1].replace('\\"', '"') if t.startswith('"') else t)
    return cur[0]


def kids(node, key):
    return [c for c in node if isinstance(c, list) and c and c[0] == key]


def val(node, key, default=""):
    k = kids(node, key)
    return k[0][1] if k and len(k[0]) > 1 else default


def read_netlist(path: Path):
    root = sexp(path.read_text(encoding="utf-8"))
    comps = {}
    for c in kids(kids(root, "components")[0], "comp"):
        flags = {val(pr, "name") for pr in kids(c, "property")}
        comps[val(c, "ref")] = {"value": val(c, "value"), "footprint": val(c, "footprint"),
                                "dnp": "dnp" in flags, "no_bom": "exclude_from_bom" in flags}
    pads = {}
    for n in kids(kids(root, "nets")[0], "net"):
        name = val(n, "name")
        for nd in kids(n, "node"):
            pads[(val(nd, "ref"), val(nd, "pin"))] = name
    return comps, pads


def lib_dirs() -> dict[str, str]:
    env = dict(os.environ, KIPRJMOD=str(HW))
    env.setdefault("OHMAI_KICAD_FOOTPRINTS", str(Path(os.environ.get("OHMAI_KICAD_LIBS") or "~/.cache/ohmai/kicad-libs").expanduser() / "kicad-footprints-9.0.9.1"))
    out = {}
    for name, uri in re.findall(r'\(lib\s+\(name\s+"([^"]+)"\)\s*\(type\s+"[^"]*"\)\s*\(uri\s+"([^"]+)"\)',
                                (HW / "fp-lib-table").read_text()):
        out[name] = re.sub(r"\$\{(\w+)\}", lambda m: env.get(m.group(1), m.group(0)), uri)
    return out


def P(x, y, o):
    return pcbnew.VECTOR2I(MM(o[0] + x), MM(o[1] + y))


def seg(board, layer, a, b, width=0.05):
    s = pcbnew.PCB_SHAPE(board)
    s.SetShape(pcbnew.SHAPE_T_SEGMENT)
    s.SetStart(a); s.SetEnd(b); s.SetLayer(layer); s.SetWidth(MM(width))
    board.Add(s)


def text(board, layer, s, x, y, o, size=1.0, mirror=False):
    t = pcbnew.PCB_TEXT(board)
    t.SetText(s); t.SetPosition(P(x, y, o)); t.SetLayer(layer)
    t.SetTextSize(pcbnew.VECTOR2I(MM(size), MM(size))); t.SetTextThickness(MM(0.15))
    if mirror:
        t.SetMirrored(True)
    board.Add(t)


def zone(board, net, layer, pts, o, prio=0, clearance=0.2, name=""):
    z = pcbnew.ZONE(board)
    z.SetLayer(layer)
    if net is not None:
        z.SetNet(net)
    ol = z.Outline(); ol.NewOutline()
    for x, y in pts:
        ol.Append(MM(o[0] + x), MM(o[1] + y))
    z.SetAssignedPriority(prio)
    z.SetLocalClearance(MM(clearance))
    z.SetMinThickness(MM(0.15))
    z.SetPadConnection(pcbnew.ZONE_CONNECTION_THERMAL)
    z.SetThermalReliefGap(MM(0.2)); z.SetThermalReliefSpokeWidth(MM(0.25))
    z.SetIslandRemovalMode(pcbnew.ISLAND_REMOVAL_MODE_ALWAYS)
    if name:
        z.SetZoneName(name)
    board.Add(z)
    return z


def keepout(board, layers, pts, o, name, tracks=True, vias=True, pours=True):
    z = pcbnew.ZONE(board)
    z.SetIsRuleArea(True)
    ls = pcbnew.LSET()
    for l in layers:
        ls.AddLayer(l)
    z.SetLayerSet(ls)
    ol = z.Outline(); ol.NewOutline()
    for x, y in pts:
        ol.Append(MM(o[0] + x), MM(o[1] + y))
    z.SetDoNotAllowTracks(tracks); z.SetDoNotAllowVias(vias); (z.SetDoNotAllowCopperPour if hasattr(z, "SetDoNotAllowCopperPour") else z.SetDoNotAllowZoneFills)(pours)
    z.SetDoNotAllowPads(False); z.SetDoNotAllowFootprints(False)
    z.SetZoneName(name)
    board.Add(z)


def netclasses(board):
    ds = board.GetDesignSettings()
    ns = ds.m_NetSettings
    d = ns.GetDefaultNetclass()
    d.SetClearance(MM(0.1)); d.SetTrackWidth(MM(0.15)); d.SetViaDiameter(MM(0.45)); d.SetViaDrill(MM(0.2))
    classes = {
        # name: (track, clearance, nets regex)
        "Power": (0.30, 0.15, r"^/?(VBUS|VSYS|3V3|DVDD|VREG_PGND|Net-\(U1-VREG_PGND\)|Net-\(U3-L[12]\)|Net-\(U1-VREG_LX\)|GND)$"),
        "USB": (0.20, 0.15, r"USB"),
        "TC": (0.20, 0.20, r"J2-Pin_1|J3-Pin_1|U5-T[+-]"),
    }
    for name, (tw, cl, rx) in classes.items():
        nc = pcbnew.NETCLASS(name)
        nc.SetTrackWidth(MM(tw)); nc.SetClearance(MM(cl)); nc.SetViaDiameter(MM(0.45)); nc.SetViaDrill(MM(0.2))
        if name == "USB":
            # ESTIMATE 90 ohm differential, top layer over In1 GND, JLC04101H-3313 prepreg h 0.0994 mm, er 4.1,
            # t 0.035: IPC-2141 edge-coupled microstrip, w 0.14 / s 0.15 -> Z0 ~52, Zdiff ~92 ohm. Verify with the
            # JLC impedance calculator (jlcpcb.com/impedance) before ordering. USB FS 12 Mb/s: not critical.
            nc.SetTrackWidth(MM(0.14)); nc.SetDiffPairWidth(MM(0.14)); nc.SetDiffPairGap(MM(0.15))
        ns.SetNetclass(name, nc)
        ns.SetNetclassPatternAssignment(rx, name)
    return classes


def stackup(board):
    board.SetCopperLayerCount(4)
    ds = board.GetDesignSettings()
    ds.SetBoardThickness(MM(1.0))
    # JLC capabilities page: copper to routed edge 0.2; min track/space 0.09 (we use 0.1); via 0.45/0.2;
    # hole to hole 0.5 (different nets); silk 0.15 line / 1.0 text (0.8 notes, ESTIMATE to confirm).
    ds.m_CopperEdgeClearance = MM(0.2)
    ds.m_TrackMinWidth = MM(0.1)
    ds.m_MinClearance = MM(0.1)
    ds.m_ViasMinSize = MM(0.45)
    ds.m_MinThroughDrill = MM(0.2)
    ds.m_HoleToHoleMin = MM(0.25)
    ds.m_HoleClearance = MM(0.2)


STACKUP = """		(stackup
			(layer "F.SilkS" (type "Top Silk Screen"))
			(layer "F.Paste" (type "Top Solder Paste"))
			(layer "F.Mask" (type "Top Solder Mask") (thickness 0.01))
			(layer "F.Cu" (type "copper") (thickness 0.035))
			(layer "dielectric 1" (type "prepreg") (thickness 0.0994) (material "3313") (epsilon_r 4.1) (loss_tangent 0.02))
			(layer "In1.Cu" (type "copper") (thickness 0.0152))
			(layer "dielectric 2" (type "core") (thickness 0.7296) (material "FR4") (epsilon_r 4.6) (loss_tangent 0.02))
			(layer "In2.Cu" (type "copper") (thickness 0.0152))
			(layer "dielectric 3" (type "prepreg") (thickness 0.0994) (material "3313") (epsilon_r 4.1) (loss_tangent 0.02))
			(layer "B.Cu" (type "copper") (thickness 0.035))
			(layer "B.Mask" (type "Bottom Solder Mask") (thickness 0.01))
			(layer "B.Paste" (type "Bottom Solder Paste"))
			(layer "B.SilkS" (type "Bottom Silk Screen"))
			(copper_finish "ENIG")
			(dielectric_constraints yes)
			(castellated_pads yes)
			(edge_plating yes)
		)
"""
# JLC04101H-3313 (jlcpcb.com/impedance, read 2026-10-15): outer Cu 0.035, prepreg 3313 0.0994 er 4.1, inner Cu
# 0.0152. Core 0.7296 is ESTIMATE (total 1.0 mm), er 4.6 ESTIMATE. pcbnew 9.0.2 SWIG does not expose the stackup
# editor, so the (stackup) block is inserted into the KiCad-written (setup) section and the board is then re-loaded
# and re-saved by KiCad so the file stays KiCad-serialised.


def write_stackup(path):
    s = path.read_text(encoding="utf-8")
    s = re.sub(r"\t\t\(stackup.*?\n\t\t\)\n", "", s, flags=re.S)
    s = s.replace("\t(setup\n", "\t(setup\n" + STACKUP, 1)
    path.write_text(s, encoding="utf-8")
    b = pcbnew.LoadBoard(str(path))
    b.BuildConnectivity()
    pcbnew.ZONE_FILLER(b).Fill(b.Zones())   # fill on a loaded board (filling a fresh BOARD() segfaults in 9.0.2)
    pcbnew.SaveBoard(str(path), b)


def main():
    o = (100.0, 100.0)
    comps, pads = read_netlist(ROOT / "out" / "netlist.net")
    place = yaml.safe_load((HW / "gen" / "pcb" / "placement.yaml").read_text())["parts"]
    libs = lib_dirs()
    board = pcbnew.BOARD()
    stackup(board)
    netclasses(board)
    nets = {}
    for name in sorted(set(pads.values())):
        ni = pcbnew.NETINFO_ITEM(board, name)
        board.Add(ni)
        nets[name] = ni
    # outline: Pico 2 Fig. 3 p.7 21 x 51 rectangle
    corners = [(0, 0), (W, 0), (W, H), (0, H)]
    for a, b in zip(corners, corners[1:] + corners[:1]):
        seg(board, pcbnew.Edge_Cuts, P(*a, o), P(*b, o), 0.05)
    missing = []
    for ref in sorted(comps):
        c = comps[ref]
        lib, _, name = c["footprint"].partition(":")
        fp = pcbnew.FootprintLoad(libs[lib], name)
        if fp is None:
            raise SystemExit(f"{ref}: cannot load {c['footprint']}")
        fp.SetReference(ref); fp.SetValue(c["value"])
        fp.Value().SetVisible(False)
        fp.SetDNP(c["dnp"]); fp.SetExcludedFromBOM(c["no_bom"])   # same attributes as the symbol (DRC parity)
        if fp.Reference().GetLayer() in (pcbnew.F_SilkS, pcbnew.B_SilkS):
            # 0402-dense board: references go to the fab layer (assembly drawing), not the silkscreen
            fp.Reference().SetLayer(pcbnew.F_Fab)
            fp.Reference().SetTextSize(pcbnew.VECTOR2I(MM(0.5), MM(0.5)))
            fp.Reference().SetTextThickness(MM(0.08))
        fp.SetFPIDAsString(c["footprint"]) if hasattr(fp, "SetFPIDAsString") else None
        board.Add(fp)
        pl = place.get(ref)
        if pl is None:
            missing.append(ref)
            pl = {"at": [-10, 0]}
        x, y = pl["at"]
        fp.SetPosition(P(x, y, o))
        if pl.get("side", "F") == "B":
            fp.Flip(fp.GetPosition(), pcbnew.FLIP_DIRECTION_TOP_BOTTOM)
        fp.SetOrientationDegrees(float(pl.get("rot", 0)))
        for pad in fp.Pads():
            n = pads.get((ref, pad.GetNumber()))
            if n:
                pad.SetNet(nets[n])
    if missing:
        print("not placed (parked left of the board):", " ".join(missing))
    # --- zones -------------------------------------------------------------------------------------------
    gnd = nets.get("GND")
    full = corners
    zone(board, gnd, pcbnew.In1_Cu, full, o, name="GND In1 (reference plane, USB/TC)")
    zone(board, gnd, pcbnew.B_Cu, full, o, name="GND bottom")
    zone(board, nets.get("3V3"), pcbnew.In2_Cu, full, o, name="3V3 In2")
    zone(board, gnd, pcbnew.F_Cu, full, o, prio=0, clearance=0.25, name="GND top fill")
    # VREG_LX: no copper under L1 / the LX node on layer 2 (RP2350 p.454 + Fig. 24), nor on the top fill
    l1 = place["L1"]["at"]
    keepout(board, [pcbnew.In1_Cu, pcbnew.F_Cu],
            [(l1[0] - 1.8, l1[1] - 1.5), (l1[0] + 1.8, l1[1] - 1.5), (l1[0] + 1.8, l1[1] + 1.5),
             (l1[0] - 1.8, l1[1] + 1.5)], o, "VREG_LX: no pour under L1 (RP2350 p.454)", tracks=False, vias=True)
    # --- silkscreen notes ---------------------------------------------------------------------------------
    jp5, jp6 = place["JP5"]["at"], place["JP6"]["at"]
    # left of JP5 (bottom), two lines each; clear of the JP5/JP6 silk, TP6/TP7 and the J4 mask openings
    for k, line in enumerate(("JP5 FB-DVDD", "(cut first)", "JP6 FB-GND", "(fallback)")):
        text(board, pcbnew.B_SilkS, line, 6.5, 15.0 + k * 1.05 + (0.25 if k >= 2 else 0), o, size=0.8, mirror=True)
    text(board, pcbnew.B_SilkS, "pico-k rev A", 10.5, 25.0, o, size=1.0, mirror=True)
    # read from the bottom (mirrored): TP9 SWDIO x 12.5, TP10 GND x 10.5, TP8 SWCLK x 8.5
    text(board, pcbnew.B_SilkS, "SWDIO GND SWCLK", 10.5, 45.6, o, size=0.8, mirror=True)
    pcbnew.SaveBoard(str(PCB), board)
    write_stackup(PCB)
    print("wrote", PCB.relative_to(ROOT), len(comps), "footprints,", len(nets), "nets")


if __name__ == "__main__":
    sys.exit(main())
