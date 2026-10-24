#!/usr/bin/env python3
"""Generate the project footprints in hardware/pico-k.pretty (phase 8).

Every dimension comes from a cited datasheet figure; the cite is written into each footprint's
descr and into parts/footprints.yaml. Values marked ESTIMATE are derived, not printed.
Run: python3 hardware/gen/pcb/footprints.py   (plain Python, no KiCad needed)
"""
from __future__ import annotations

import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "hardware" / "pico-k.pretty"


_UUID_N = [0]


def u() -> str:
    """Deterministic UUIDs (uuid5 of a running counter) so regenerating the library gives identical files."""
    _UUID_N[0] += 1
    return str(uuid.uuid5(uuid.NAMESPACE_URL, f"pico-k.pretty/{_UUID_N[0]}"))


def fmt(v: float) -> str:
    s = f"{v:.4f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


class FP:
    def __init__(self, name: str, descr: str, tags: str, attr: str = "smd"):
        self.name, self.descr, self.tags, self.attr = name, descr, tags, attr
        self.items: list[str] = []

    def line(self, x1, y1, x2, y2, layer, w=0.1):
        self.items.append(f'(fp_line (start {fmt(x1)} {fmt(y1)}) (end {fmt(x2)} {fmt(y2)}) '
                          f'(stroke (width {fmt(w)}) (type solid)) (layer "{layer}") (uuid "{u()}"))')

    def rect(self, x1, y1, x2, y2, layer, w=0.1):
        for a, b, c, d in ((x1, y1, x2, y1), (x2, y1, x2, y2), (x2, y2, x1, y2), (x1, y2, x1, y1)):
            self.line(a, b, c, d, layer, w)

    def arc(self, sx, sy, mx, my, ex, ey, layer, w=0.1):
        self.items.append(f'(fp_arc (start {fmt(sx)} {fmt(sy)}) (mid {fmt(mx)} {fmt(my)}) (end {fmt(ex)} {fmt(ey)}) '
                          f'(stroke (width {fmt(w)}) (type solid)) (layer "{layer}") (uuid "{u()}"))')

    def rrect_cut(self, x1, y1, x2, y2, r, layer="Edge.Cuts", w=0.05):
        """Rounded-rectangle outline (internal slot cut-out) with corner radius r."""
        import math
        self.line(x1 + r, y1, x2 - r, y1, layer, w)
        self.line(x2, y1 + r, x2, y2 - r, layer, w)
        self.line(x2 - r, y2, x1 + r, y2, layer, w)
        self.line(x1, y2 - r, x1, y1 + r, layer, w)
        k = r * (1 - 1 / math.sqrt(2))
        self.arc(x2 - r, y1, x2 - k, y1 + k, x2, y1 + r, layer, w)
        self.arc(x2, y2 - r, x2 - k, y2 - k, x2 - r, y2, layer, w)
        self.arc(x1 + r, y2, x1 + k, y2 - k, x1, y2 - r, layer, w)
        self.arc(x1, y1 + r, x1 + k, y1 + k, x1 + r, y1, layer, w)

    def text(self, kind, txt, x, y, layer, hide=False, size=1.0):
        h = " (hide yes)" if hide else ""
        self.items.append(f'(property "{kind}" "{txt}" (at {fmt(x)} {fmt(y)} 0) (layer "{layer}"){h} (uuid "{u()}") '
                          f'(effects (font (size {fmt(size)} {fmt(size)}) (thickness {fmt(size * 0.15)}))))')

    def user(self, txt, x, y, layer, size=0.6):
        self.items.append(f'(fp_text user "{txt}" (at {fmt(x)} {fmt(y)} 0) (layer "{layer}") (uuid "{u()}") '
                          f'(effects (font (size {fmt(size)} {fmt(size)}) (thickness {fmt(size * 0.15)}))))')

    def pad(self, num, kind, shape, x, y, sx, sy, layers, drill=None, extra="", rr=None, rot=0):
        d = ""
        if drill is not None:
            if isinstance(drill, tuple):
                d = f" (drill oval {fmt(drill[0])} {fmt(drill[1])})"
            elif isinstance(drill, str):
                d = f" (drill {drill})"
            else:
                d = f" (drill {fmt(drill)})"
        r = f" (roundrect_rratio {fmt(rr)})" if rr is not None else ""
        a = f" {fmt(rot)}" if rot else ""
        self.items.append(f'(pad "{num}" {kind} {shape} (at {fmt(x)} {fmt(y)}{a}) (size {fmt(sx)} {fmt(sy)}){d} '
                          f'(layers {layers}){r}{extra} (uuid "{u()}"))')

    def write(self):
        OUT.mkdir(parents=True, exist_ok=True)
        body = "\n\t".join(self.items)
        s = (f'(footprint "{self.name}"\n\t(version 20241229)\n\t(generator "ohmai-pico-k-footprints")\n'
             f'\t(generator_version "9.0")\n\t(layer "F.Cu")\n\t(descr "{self.descr}")\n\t(tags "{self.tags}")\n'
             f'\t(attr {self.attr})\n\t{body}\n)\n')
        (OUT / f"{self.name}.kicad_mod").write_text(s, encoding="utf-8")
        return self.name


SMD = '"F.Cu" "F.Paste" "F.Mask"'
SMD_NOPASTE = '"F.Cu" "F.Mask"'
PTH = '"*.Cu" "*.Mask"'


# ---------------------------------------------------------------------------------------------------------------
# Omega PCC-SMD clip, "BARE PCB" figure, PCC-SMD.pdf p.2 (all mm; x from the pair centreline, y from the board
# edge, positive into the board). Footprint origin = pair centreline at the board edge; KiCad y = -drawing y.
#   Pad ("PAD DIMENSIONS"):        x 1.60 .. 5.87, y 0.50 .. 9.50
#   Side tab (same copper):        x 5.87 .. 7.21, y 2.84 .. 7.16
#   Side slot ("THROUGH-HOLE SLOT DIMENSIONS", plated, inside the tab copper): x 6.09 .. 6.70, y 3.38 .. 6.63
#   Rear slot (no copper drawn => non-plated cut-out, R0.40 corners "R0.40 ALL"): x 2.09 .. 5.70, y 9.77 .. 11.27
#   Paste ("SOLDER PASTE PROFILE", p.2): 4x 1.95 x 1.65, 2x 1.50 x 2.7, 2x 1.50 x 1.65 (two clips), centre
#     spacing 2.15 (columns), 6.45 (outer rows), 2 (middle rows), 1.60 (column offset). Positions ESTIMATE: grid
#     centred on the pad; the 2.7-wide windows reach into the side tab.
PCC = {
    "pad": (1.60, 5.87, 0.50, 9.50), "tab": (5.87, 7.21, 2.84, 7.16), "slot": (6.09, 6.70, 3.38, 6.63),
    "rear": (2.09, 5.70, 9.77, 11.27, 0.40),
}


def pcc_clip(side: str) -> str:
    s = 1 if side == "R" else -1
    pol = "+" if side == "R" else "-"
    fp = FP(f"Omega_PCC-SMD_Clip_{side}",
            f"Omega PCC-SMD mini thermocouple clip, {('right (+, T+)' if s > 0 else 'left (-, T-)')} of the pair. "
            "Origin = pair centreline at the board edge. Dimensions: Omega PCC-SMD spec sheet p.2 BARE PCB "
            "(pad x 1.60-5.87 y 0.50-9.50; tab x 5.87-7.21 y 2.84-7.16; plated side slot x 6.09-6.70 y 3.38-6.63; "
            "rear slot x 2.09-5.70 y 9.77-11.27 R0.40, non-plated) and SOLDER PASTE PROFILE p.2. "
            "Polarity per D-009: seen from the top with this edge toward the viewer, + is on the right.",
            "thermocouple connector PCC-SMD omega", attr="smd")
    fp.text("Reference", "REF**", s * 3.7, -12.3, "F.SilkS", size=0.8)
    fp.text("Value", f"PCC-SMD {pol}", s * 3.7, -5.0, "F.Fab", size=0.6)
    fp.text("Datasheet", "datasheets/PCC-SMD.pdf p.2", 0, 0, "F.Fab", hide=True)
    x1, x2, y1, y2 = PCC["pad"]
    cx, cy = s * (x1 + x2) / 2, -(y1 + y2) / 2
    fp.pad("1", "smd", "rect", cx, cy, x2 - x1, y2 - y1, SMD_NOPASTE)
    tx1, tx2, ty1, ty2 = PCC["tab"]
    fp.pad("1", "smd", "rect", s * (tx1 + tx2) / 2, -(ty1 + ty2) / 2, tx2 - tx1, ty2 - ty1, SMD_NOPASTE)
    sx1, sx2, sy1, sy2 = PCC["slot"]
    # plated slot: copper ring kept inside the tab copper (0.22 mm / 0.51 mm to the tab edges)
    fp.pad("1", "thru_hole", "oval", s * (sx1 + sx2) / 2, -(sy1 + sy2) / 2, (sx2 - sx1) + 0.3, (sy2 - sy1) + 0.3,
           PTH, drill=(sx2 - sx1, sy2 - sy1))
    # paste windows (ESTIMATE positions, sizes printed p.2)
    pc = (x1 + x2) / 2
    cols = (pc - 2.15 / 2, pc + 2.15 / 2)            # inner, outer column centres
    rows_outer = (5.0 - 6.45 / 2, 5.0 + 6.45 / 2)
    rows_mid = (5.0 - 1.0, 5.0 + 1.0)
    for ry in rows_outer:
        for c in cols:
            fp.pad("", "smd", "rect", s * c, -ry, 1.95, 1.65, '"F.Paste"')
    for ry in rows_mid:
        fp.pad("", "smd", "rect", s * (cols[1] - 0.975 + 1.35), -ry, 2.7, 1.50, '"F.Paste"')
        fp.pad("", "smd", "rect", s * cols[0], -ry, 1.65, 1.50, '"F.Paste"')
    rx1, rx2, ry1, ry2, rr = PCC["rear"]
    a, b = sorted((s * rx1, s * rx2))
    fp.rrect_cut(a, -ry2, b, -ry1, rr)
    # silk polarity mark behind the tab, outside the rear slot (slot ends at x 5.70) and clear of the pad
    fp.user(pol, s * 6.6, -10.5, "F.SilkS", size=1.0)
    a, b = sorted((s * 1.35, s * 7.46))
    fp.rect(a, 2.6, b, -11.52, "F.CrtYd", 0.05)   # clip body overhangs the edge by ~2.4 (11.94 long, p.1)
    a, b = sorted((s * 1.60, s * 7.21))
    fp.rect(a, 2.43, b, -9.51, "F.Fab", 0.1)
    return fp.write()


# ---------------------------------------------------------------------------------------------------------------
# Pico 2 edge: 2 x 20 castellated + 2.54 mm through-holes. Raspberry Pi Pico 2 datasheet Fig. 3 p.7:
# board 21 x 51, rows 17.78 apart (centres x 1.61 / 19.39), pitch 2.54, end pins 1.37 from the short edges
# ((51 - 48.26)/2), hole 1 mm, pad 1.6 mm, castellation hole 1 mm at the long edge. Footprint origin = board
# top-left corner (USB end left, seen from the top); pin 1 top-left, counter-clockwise (Pico 2 Fig. 2 p.8).
# Castellated SMT pads must cover the carrier pads of Pico 2 Fig. 5 p.10 (pad length to x 2.41 = 1.61 + 0.8).
END_PINS = (1, 20, 21, 40)   # D-017: plain edge pads, no half-hole


def pico_edge() -> str:
    fp = FP("RaspberryPi_Pico2_Edge_Castellated_2x20",
            "Pico 2 drop-in edge: 36 castellated half-holes (end pins 1/20/21/40 plain edge pads, D-017) plus 2.54 mm through-holes. Pico 2 datasheet Fig. 3 p.7 "
            "(21 x 51, rows 17.78, x 1.61, pitch 2.54, ends 1.37, hole 1, pad 1.6); pin order Fig. 2 p.8; "
            "SMT footprint Fig. 5 p.10. Origin = board top-left (USB end).",
            "pico castellated module edge", attr="through_hole")
    fp.text("Reference", "REF**", 10.5, -1.5, "F.Fab", hide=True)
    fp.text("Value", "Pico2_Edge", 10.5, 25.5, "F.Fab", hide=True)
    for n in range(1, 41):
        if n <= 20:
            x, y, edge, sgn = 1.61, 1.37 + (n - 1) * 2.54, 0.0, 1
        else:
            x, y, edge, sgn = 19.39, 1.37 + (40 - n) * 2.54, 21.0, -1
        # pin pad: Ø1.6 (pin 1 square) on the Ø1.0 hole at x 1.61 (no drill offset: KiCad 9 DRC checks holes at the pad
        # centre). Castellation: Ø1.0 plated hole centred on the board edge with a 2.41 x 1.6 oval pad that overlaps the
        # pin pad (copper outside the outline is removed by the edge routing), so each pin is one copper island.
        fp.pad(str(n), "thru_hole", "rect" if n == 1 else "circle", x, y, 1.6, 1.6, PTH, drill=1.0,
               extra=" (property pad_prop_castellated)")
        if n in END_PINS:
            # D-017 (P8-2): no half-hole on the 4 end pins. JLC castellation rules (JLC blog "Castellated PCBs",
            # updated 2026-09-08: A. pad edge to board edge >= 1 mm; Table 2: hole to board corner >= 3.0 mm) cannot be
            # met 1.37 mm from the short edge. The pin keeps its PTH and gets top + bottom pads to 0.2 mm from the long
            # edge (JLC copper to routed edge >= 0.2), so the Pico 2 Fig. 5 p.10 carrier pad is still covered.
            a, b = (0.2, 2.41) if edge == 0.0 else (18.59, 20.8)
            for lay in ('"F.Cu" "F.Mask"', '"B.Cu" "B.Mask"'):
                fp.pad(str(n), "smd", "roundrect", (a + b) / 2, y, b - a, 1.6, lay, rr=0.25)
        else:
            fp.pad(str(n), "thru_hole", "oval", edge, y, 2.41, 1.6, PTH, drill=1.0,
                   extra=" (property pad_prop_castellated)")
    fp.rect(0, 0, 21, 51, "F.Fab", 0.1)
    # courtyard: two strips around the pin rows only (the module interior is free for parts)
    fp.rect(-0.25, -0.25, 2.66, 51.25, "F.CrtYd", 0.05)
    fp.rect(18.34, -0.25, 21.25, 51.25, "F.CrtYd", 0.05)
    return fp.write()


# MPS MPL-AT2512-3R3 Rev 1.2 p.3 RECOMMENDED LAND PATTERN: 2 pads 2.30 tall, 2.90 overall, 0.50 gap
# => pad 1.20 x 2.30 at x = +/-0.85. Package 2.50 x 2.0 (p.3 PRODUCT PACKAGE). Dot = start of winding = pad 1.
def mpl_at2512() -> str:
    fp = FP("L_MPS_MPL-AT2512", "MPS MPL-AT2512 2.5 x 2.0 mm molded inductor. Land pattern MPS MPL-AT2512-3R3 Rev 1.2 "
            "p.3 (2.90 overall, 2.30 tall, 0.50 gap: pads 1.20 x 2.30 at +/-0.85); pad 1 = dot (start of winding).",
            "inductor MPS MPL-AT2512")
    fp.text("Reference", "REF**", 0, -2.0, "F.SilkS", size=0.8)
    fp.text("Value", "MPL-AT2512", 0, 2.0, "F.Fab", size=0.6)
    fp.pad("1", "smd", "rect", -0.85, 0, 1.20, 2.30, SMD)
    fp.pad("2", "smd", "rect", 0.85, 0, 1.20, 2.30, SMD)
    fp.rect(-1.25, -1.0, 1.25, 1.0, "F.Fab", 0.1)
    fp.rect(-1.7, -1.4, 1.7, 1.4, "F.CrtYd", 0.05)
    fp.items.append(f'(fp_circle (center -1.6 -1.35) (end -1.5 -1.35) (stroke (width 0.2) (type solid)) '
                    f'(fill yes) (layer "F.SilkS") (uuid "{u()}"))')
    return fp.write()


# Murata DFE201612P-2R2M=P2 spec JE243A-0033-01 (Reference Only): body 2.0 +/-0.2 x 1.6 +/-0.2, T 1.2 max (p.1/9);
# Recommended PCB pattern p.5/9: 2 pads 0.8 wide x 1.8 tall, 0.8 gap, 2.4 overall => pads at x = +/-0.8.
# Note (spec ~p.7): "Do not make any through holes and copper pattern under the coil" => rule area between the pads
# over the body outline (pads themselves allowed): no tracks, vias or pour on any copper layer.
def dfe201612p() -> str:
    fp = FP("L_Murata_DFE201612P", "Murata DFE201612P 2.0 x 1.6 x 1.2 mm metal-alloy inductor. Land pattern Murata spec "
            "JE243A-0033-01 p.5 (pads 0.8 x 1.8, gap 0.8, 2.4 overall: pads at +/-0.8); body p.1 (2.0 x 1.6 +/-0.2). "
            "Keepout (no tracks/vias/pour, all copper layers) between the pads under the coil per the spec notes.",
            "inductor Murata DFE201612P 2016")
    fp.text("Reference", "REF**", 0, -1.7, "F.SilkS", size=0.6)
    fp.text("Value", "DFE201612P", 0, 1.7, "F.Fab", size=0.5)
    fp.pad("1", "smd", "rect", -0.8, 0, 0.8, 1.8, SMD)
    fp.pad("2", "smd", "rect", 0.8, 0, 0.8, 1.8, SMD)
    fp.rect(-1.0, -0.8, 1.0, 0.8, "F.Fab", 0.1)
    fp.rect(-1.45, -1.15, 1.45, 1.15, "F.CrtYd", 0.05)   # max body 2.2 x 1.8 / pads 2.4 x 1.8, +0.25
    fp.items.append(
        '(zone (net 0) (net_name "") (layers "F.Cu" "In1.Cu" "In2.Cu" "B.Cu") (uuid "' + u() + '") (name "under-coil") '
        '(hatch edge 0.5) (connect_pads (clearance 0)) (min_thickness 0.25) (filled_areas_thickness no) '
        '(keepout (tracks not_allowed) (vias not_allowed) (pads allowed) (copperpour not_allowed) '
        '(footprints allowed)) (placement (enabled no) (sheetname "")) (fill (thermal_gap 0.5) (thermal_bridge_width 0.5)) '
        '(polygon (pts (xy -0.4 -0.8) (xy 0.4 -0.8) (xy 0.4 0.8) (xy -0.4 0.8))))')
    return fp.write()


# Pico 2 test point: Pico 2 datasheet Fig. 5 p.10 "TEST POINTS ARE 1.5x1.5mm WITH 0.3mm CORNER RADIUS".
def tp_pico2() -> str:
    fp = FP("TestPoint_Pico2_1.5x1.5mm", "Pico 2 test pad 1.5 x 1.5 mm, 0.3 mm corner radius (Pico 2 datasheet Fig. 5 "
            "p.10). Placed on the bottom side.", "test point pico")
    fp.text("Reference", "REF**", 0, -1.4, "F.SilkS", size=0.6)
    fp.text("Value", "TP", 0, 1.4, "F.Fab", hide=True, size=0.6)
    fp.pad("1", "smd", "roundrect", 0, 0, 1.5, 1.5, SMD_NOPASTE, rr=0.2)
    fp.rect(-1.0, -1.0, 1.0, 1.0, "F.CrtYd", 0.05)
    return fp.write()


# SHOU HAN TYPE-C 16PIN 2MD(073), drawing p.1 RECOMMENDED PCB LAYOUT (TOP VIEW): signal pads 0.30 wide (8x) at
# +/-0.25, +/-0.75, +/-1.25, +/-1.75; 0.60 wide (4x) at +/-2.40 and +/-3.20 (spans 4.80 / 6.40); pegs 0.65 at
# 5.78; shell slots 0.60 wide at 8.64: rear 2.10 / 1.70, front 1.80 / 1.40 (pad / drill). Pad length 1.45 and the
# y positions are taken from the KiCad HRO TYPE-C-31-M-12 footprint (same body, 7.35 deep) - ESTIMATE.
def usb_c_2md073() -> str:
    fp = FP("USB_C_Receptacle_ShouHan_TYPE-C-16PIN-2MD-073",
            "SHOU HAN TYPE-C 16PIN 2MD(073) USB 2.0 receptacle. X dims: drawing p.1 RECOMMENDED PCB LAYOUT (pads 0.30 "
            "at 0.5 pitch, 0.60 at spans 4.80/6.40, pegs 0.65 at 5.78, slots 0.60 at 8.64: rear 2.10/1.70, front "
            "1.80/1.40). Y positions and pad length 1.45 from KiCad HRO TYPE-C-31-M-12 (ESTIMATE).",
            "usb usb-c 2.0 shouhan", attr="smd")
    fp.text("Reference", "REF**", 0, -5.645, "F.SilkS", size=0.8)
    fp.text("Value", "TYPE-C 16PIN 2MD(073)", 0, 5.1, "F.Fab", size=0.6)
    y = -4.045
    sig = {"A5": -1.25, "A6": -0.25, "A7": 0.25, "A8": 1.25, "B5": 1.75, "B6": 0.75, "B7": -0.75, "B8": -1.75}
    wide = {"A1": -3.20, "B12": -3.20, "A4": -2.40, "B9": -2.40, "A9": 2.40, "B4": 2.40, "A12": 3.20, "B1": 3.20}
    for n, x in wide.items():
        fp.pad(n, "smd", "rect", x, y, 0.60, 1.45, SMD)
    for n, x in sig.items():
        fp.pad(n, "smd", "rect", x, y, 0.30, 1.45, SMD)
    for x in (-2.89, 2.89):
        fp.pad("", "np_thru_hole", "circle", x, -2.6, 0.65, 0.65, '"*.Cu" "*.Mask"', drill=0.65)
    for x in (-4.32, 4.32):
        fp.pad("S1", "thru_hole", "oval", x, -3.13, 1.0, 2.10, PTH, drill=(0.6, 1.70))
        fp.pad("S1", "thru_hole", "oval", x, 1.05, 1.0, 1.80, PTH, drill=(0.6, 1.40))
    fp.rect(-4.47, -3.65, 4.47, 3.65, "F.Fab", 0.1)
    fp.rect(-5.32, -5.27, 5.32, 4.15, "F.CrtYd", 0.05)
    fp.line(-5.1, 0.6, -5.1, 2.0, "F.SilkS", 0.12)   # body sides, ending 0.35 behind the board edge (mouth 1.3 beyond it)
    fp.line(5.1, 0.6, 5.1, 2.0, "F.SilkS", 0.12)
    fp.user("PCB edge (front 3.65)", 0, 3.65, "Dwgs.User", size=0.4)
    return fp.write()


def kicad_normalise(names) -> None:
    """Load each generated footprint with KiCad's own parser and save it with KiCad's own writer (pcbnew
    FootprintLoad/FootprintSave), so the library files are KiCad-serialised, not hand-formatted (KiCad assigns fresh
    UUIDs on every save: regenerate only when the geometry changes). Fails loudly if
    KiCad cannot parse a footprint. Run with the KiCad Python (/usr/bin/python3)."""
    import pcbnew  # noqa: PLC0415  (KiCad 9 scripting module)

    lib = str(OUT)
    for n in names:
        fp = pcbnew.FootprintLoad(lib, n)
        if not fp:
            raise SystemExit(f"KiCad could not parse {n}")
        pcbnew.FootprintSave(lib, fp)


GEN = {"Omega_PCC-SMD_Clip_R": lambda: pcc_clip("R"), "Omega_PCC-SMD_Clip_L": lambda: pcc_clip("L"),
       "RaspberryPi_Pico2_Edge_Castellated_2x20": pico_edge, "L_MPS_MPL-AT2512": mpl_at2512,
       "TestPoint_Pico2_1.5x1.5mm": tp_pico2, "USB_C_Receptacle_ShouHan_TYPE-C-16PIN-2MD-073": usb_c_2md073,
       "L_Murata_DFE201612P": dfe201612p}

if __name__ == "__main__":
    import sys
    # optional args: footprint names to (re)generate; default all (fresh UUIDs, so pass names to touch only those)
    names = [GEN[n]() for n in (sys.argv[1:] or GEN)]
    try:
        kicad_normalise(names)
        print("KiCad-normalised:", ", ".join(names))
    except ImportError:
        print("pcbnew not importable: files left as generated (run with /usr/bin/python3)")
