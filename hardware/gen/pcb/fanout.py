#!/usr/bin/env python3
"""Plane fanout for pico-k after the Freerouting import: one via (+ short track) from each top-side GND / 3V3 pad
to its plane (In1 GND, In2 3V3), placed only where it keeps the fab clearances; then GND stitching vias.

Run with the KiCad Python venv ($KT): $KT hardware/gen/pcb/fanout.py
Why not Freerouting: 2.1.0's own fanout (router.fanout.enabled) throws in maze_search on this board and leaves the
plane pins unconnected, so GND/3V3 are taken out of the DSN (route.py) and fanned out here with pcbnew + shapely.
Rules (hardware/pico-k.kicad_dru, JLC capabilities page 2026-10-15/16): via 0.45/0.2, clearance >= 0.1 (Power 0.15),
PTH/via hole to track 0.28 / 0.2, hole to hole 0.25 (via 0.2), copper to edge 0.2. Margins below add 0.02-0.05.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import pcbnew
from shapely.geometry import LineString, Point, Polygon
from shapely.ops import unary_union
from shapely.strtree import STRtree

ROOT = Path(__file__).resolve().parents[3]
PCB = ROOT / "hardware" / "pico-k.kicad_pcb"
MM = pcbnew.FromMM
TO = pcbnew.ToMM
VIA_D, VIA_H = 0.45, 0.2
CL = 0.17          # via copper to other-net copper (Power clearance 0.15 + margin)
HOLE_TRK = 0.30    # via hole edge to other-net track/pad copper (JLC 0.28 for PTH, 0.2 for vias)
HOLE_HOLE = 0.30   # hole edge to hole edge
EDGE = 0.25        # copper to board edge / cut-out
PAD_GAP = 0.12     # via copper to any pad copper (mask bridge between via and pad)
TRK_W = 0.25
PLANES = {"GND": pcbnew.In1_Cu, "3V3": pcbnew.In2_Cu}
CU = [pcbnew.F_Cu, pcbnew.In1_Cu, pcbnew.In2_Cu, pcbnew.B_Cu]


def poly(sps) -> Polygon:
    out = []
    for i in range(sps.OutlineCount()):
        o = sps.Outline(i)
        pts = [(TO(o.CPoint(j).x), TO(o.CPoint(j).y)) for j in range(o.PointCount())]
        if len(pts) >= 3:
            out.append(Polygon(pts).buffer(0))
    return unary_union(out)


def item_poly(it, layer) -> Polygon:
    sps = pcbnew.SHAPE_POLY_SET()
    it.TransformShapeToPolygon(sps, layer, 0, MM(0.005), pcbnew.ERROR_INSIDE)
    return poly(sps)


class Obstacles:
    def __init__(self, board):
        self.b = board
        self.cu = {L: [] for L in CU}      # (geom, netname)
        self.pads = []                      # pad copper on any layer (for the pad gap)
        self.holes = []                     # hole circles
        self.rebuild()

    def rebuild(self):
        b = self.b
        self.cu = {L: [] for L in CU}
        self.pads, self.holes = [], []
        for fp in b.Footprints():
            for p in fp.Pads():
                for L in CU:
                    if p.IsOnLayer(L):
                        g = item_poly(p, L)
                        self.cu[L].append((g, p.GetNetname()))
                        self.pads.append(g)
                if p.HasHole():
                    c = p.GetPosition()
                    sx = TO(p.GetDrillSize().x) / 2
                    self.holes.append(Point(TO(c.x), TO(c.y)).buffer(sx))
        for t in b.GetTracks():
            if t.Type() == pcbnew.PCB_VIA_T:
                for L in CU:
                    self.cu[L].append((Point(TO(t.GetPosition().x), TO(t.GetPosition().y)).buffer(TO(t.GetWidth(L)) / 2),
                                       t.GetNetname()))
                self.holes.append(Point(TO(t.GetPosition().x), TO(t.GetPosition().y)).buffer(TO(t.GetDrillValue()) / 2))
            else:
                L = t.GetLayer()
                if L in self.cu:
                    a, e = t.GetStart(), t.GetEnd()
                    self.cu[L].append((LineString([(TO(a.x), TO(a.y)), (TO(e.x), TO(e.y))]).buffer(TO(t.GetWidth()) / 2),
                                       t.GetNetname()))
        self.trees = {L: STRtree([g for g, _ in v]) for L, v in self.cu.items()}
        self.padtree = STRtree(self.pads)
        self.holetree = STRtree(self.holes)
        # edges: outline and cut-outs as lines
        lines = []
        for d in b.GetDrawings():
            if d.GetLayer() == pcbnew.Edge_Cuts:
                sps = pcbnew.SHAPE_POLY_SET()
                d.TransformShapeToPolygon(sps, pcbnew.Edge_Cuts, 0, MM(0.005), pcbnew.ERROR_INSIDE)
                lines.append(poly(sps))
        for fp in b.Footprints():
            for d in fp.GraphicalItems():
                if d.GetLayer() == pcbnew.Edge_Cuts:
                    sps = pcbnew.SHAPE_POLY_SET()
                    d.TransformShapeToPolygon(sps, pcbnew.Edge_Cuts, 0, MM(0.005), pcbnew.ERROR_INSIDE)
                    lines.append(poly(sps))
        self.edges = unary_union(lines)
        self.keepouts = []
        for z in b.Zones():
            if z.GetIsRuleArea() and z.GetDoNotAllowVias():
                self.keepouts.append(poly(z.Outline()))

    def via_ok(self, x, y, net) -> bool:
        c = Point(x, y)
        r = VIA_D / 2
        for L in CU:
            for i in self.trees[L].query(c.buffer(r + CL)):
                g, n = self.cu[L][i]
                if n != net and g.distance(c) < r + CL:
                    return False
                if n != net and g.distance(c) < VIA_H / 2 + HOLE_TRK:
                    return False
        for i in self.padtree.query(c.buffer(r + PAD_GAP)):
            if self.pads[i].distance(c) < r + PAD_GAP:
                return False
        for i in self.holetree.query(c.buffer(VIA_H / 2 + HOLE_HOLE)):
            if self.holes[i].distance(c) < VIA_H / 2 + HOLE_HOLE:
                return False
        if self.edges.distance(c) < r + EDGE:
            return False
        if any(k.distance(c) < r + 0.05 for k in self.keepouts):
            return False
        return True

    def track_ok(self, a, b, net, layer, w=TRK_W) -> bool:
        ln = LineString([a, b]).buffer(w / 2)
        for i in self.trees[layer].query(ln.buffer(CL)):
            g, n = self.cu[layer][i]
            if n != net and g.distance(ln) < CL:
                return False
        return self.edges.distance(ln) >= EDGE


def add_via(board, net, x, y):
    v = pcbnew.PCB_VIA(board)
    v.SetPosition(pcbnew.VECTOR2I(MM(x), MM(y)))
    v.SetWidth(MM(VIA_D)); v.SetDrill(MM(VIA_H)); v.SetNet(net)
    v.SetLayerPair(pcbnew.F_Cu, pcbnew.B_Cu)
    board.Add(v)


def add_track(board, net, a, b, layer, w=TRK_W):
    t = pcbnew.PCB_TRACK(board)
    t.SetStart(pcbnew.VECTOR2I(MM(a[0]), MM(a[1]))); t.SetEnd(pcbnew.VECTOR2I(MM(b[0]), MM(b[1])))
    t.SetWidth(MM(w)); t.SetLayer(layer); t.SetNet(net)
    board.Add(t)


def channel_poly(board, ref="U1"):
    """D-018: keep plane-fanout vias out of the U1 escape channel (pin toes .. toes + CHANNEL mm)."""
    if "--channel" not in sys.argv:
        return None
    w = float(sys.argv[sys.argv.index("--channel") + 1])
    fp = board.FindFootprintByReference(ref)
    c = fp.GetPosition(); cx, cy = TO(c.x), TO(c.y)
    toe = 3.85  # pad centre 3.45 + half length 0.4 (QFN-60 7x7)
    return Polygon([(cx - toe - w, cy - toe - w), (cx + toe + w, cy - toe - w),
                    (cx + toe + w, cy + toe + w), (cx - toe - w, cy + toe + w)]).difference(
        Polygon([(cx - toe, cy - toe), (cx + toe, cy - toe), (cx + toe, cy + toe), (cx - toe, cy + toe)]))


def fanned(board, p, pg, layer) -> bool:
    """Already fanned out: a same-net via on the pad, or a same-net track starting or ending in the pad."""
    name = p.GetNetname()
    for t in board.GetTracks():
        if t.GetNetname() != name:
            continue
        if t.Type() == pcbnew.PCB_VIA_T:
            if pg.distance(Point(TO(t.GetPosition().x), TO(t.GetPosition().y))) < VIA_D / 2 + 0.05:
                return True
        elif t.GetLayer() == layer and any(pg.contains(Point(TO(q.x), TO(q.y))) for q in (t.GetStart(), t.GetEnd())):
            return True
    return False


def bridge(board, ob, reach=2.6):
    """Plane pads that got no via (no room): a short top-layer track to the nearest same-net pad that has one
    (e.g. an RP2350 IOVDD pin to its own decoupler, which is the decoupling path anyway). QFN pins leave straight
    out of the toe first (0.2 wide = pad width), then turn to the target."""
    placed = 0
    for fp in board.Footprints():
        for p in fp.Pads():
            name = p.GetNetname()
            if name not in PLANES or p.HasHole() or not p.IsOnLayer(pcbnew.F_Cu):
                continue
            layer = pcbnew.F_Cu
            pg = item_poly(p, layer)
            if fanned(board, p, pg, layer):
                continue
            c = p.GetPosition(); cx, cy = TO(c.x), TO(c.y)
            targets = []
            for fp2 in board.Footprints():
                for q in fp2.Pads():
                    if q is p or q.GetNetname() != name or not q.IsOnLayer(layer):
                        continue
                    qg = item_poly(q, layer)
                    if q.HasHole() or fanned(board, q, qg, layer):
                        qc = q.GetPosition(); d = math.hypot(TO(qc.x) - cx, TO(qc.y) - cy)
                        if d <= reach:
                            targets.append((d, (TO(qc.x), TO(qc.y)), f"{fp2.GetReference()}.{q.GetNumber()}"))
            sx, sy = TO(p.GetSize().x), TO(p.GetSize().y)
            w = min(TRK_W, sx, sy)
            path0 = [(cx, cy)]
            if max(sx, sy) > 2 * min(sx, sy):   # long pad (QFN pin): leave through its toe
                fc = fp.GetPosition(); ux, uy = cx - TO(fc.x), cy - TO(fc.y)
                ang = p.GetOrientation().AsRadians()
                ax, ay = (math.cos(ang), -math.sin(ang)) if sx > sy else (math.sin(ang), math.cos(ang))
                if ax * ux + ay * uy < 0:
                    ax, ay = -ax, -ay
                ext = max(sx, sy) / 2 + 0.2
                path0.append((cx + ax * ext, cy + ay * ext))
            done = False
            for d, t, ref in sorted(targets):
                path = path0 + [t]
                if all(ob.track_ok(a, b, name, layer, w) for a, b in zip(path, path[1:])):
                    for a, b in zip(path, path[1:]):
                        add_track(board, p.GetNet(), a, b, layer, w)
                    ob.rebuild(); placed += 1; done = True
                    print(f"bridge {fp.GetReference()}.{p.GetNumber()} [{name}] -> {ref} ({d:.2f} mm)")
                    break
            if not done:
                print(f"no bridge for {fp.GetReference()}.{p.GetNumber()} [{name}]")
    return placed


def fanout(board, ob):
    placed = 0
    chan = channel_poly(board)
    for fp in board.Footprints():
        for p in fp.Pads():
            name = p.GetNetname()
            if name not in PLANES or p.HasHole():
                continue
            layer = pcbnew.F_Cu if p.IsOnLayer(pcbnew.F_Cu) else pcbnew.B_Cu
            c = p.GetPosition(); cx, cy = TO(c.x), TO(c.y)
            pg = item_poly(p, layer)
            ext = math.hypot(TO(p.GetSize().x), TO(p.GetSize().y)) / 2
            if fanned(board, p, pg, layer):
                continue
            done = False
            for d in (ext + 0.30, ext + 0.45, ext + 0.65, ext + 0.9, ext + 1.2):
                for k in range(24):
                    ang = 2 * math.pi * k / 24
                    x, y = cx + d * math.cos(ang), cy + d * math.sin(ang)
                    if chan is not None and fp.GetReference() != "U1" and chan.distance(Point(x, y)) < VIA_D / 2:
                        continue
                    if ob.via_ok(x, y, name) and ob.track_ok((cx, cy), (x, y), name, layer):
                        add_via(board, p.GetNet(), x, y)
                        add_track(board, p.GetNet(), (cx, cy), (x, y), layer)
                        ob.rebuild(); placed += 1; done = True
                        break
                if done:
                    break
            if not done:
                print(f"no fanout for {fp.GetReference()}.{p.GetNumber()} [{name}]")
    return placed


# U1 (RP2350A QFN-60 7x7, EP 3.4) signal escape: the 0402 decouplers sit ~0.45 mm from the pin toes on all sides, so
# pins cannot escape outward. Between the pin heels and the EP there is 1.35 mm (pads 0.8 long at +-3.45, EP +-1.7):
# two staggered via rows under the body (0.45 and 0.90 in from the heel; adjacent pins 0.6 apart, same row 0.8),
# top stub 0.12 mm from the pad to its via, bottom routing by Freerouting. Plane / DVDD / local nets stay on top.
ESC_SKIP = ("GND", "3V3", "DVDD", "Net-(U1-XIN)", "Net-(U1-XOUT)", "/ADC_AVDD")
ESC_W = 0.12


def escape(board, ob, ref="U1"):
    fp = board.FindFootprintByReference(ref)
    c = fp.GetPosition(); cx, cy = TO(c.x), TO(c.y)
    placed, vias = 0, []
    # bottom row (pins 16-30) first: the under-body corners are shared, the side pins next to them lose
    order = lambda q: (0 if 16 <= int(q.GetNumber()) <= 30 else 1, int(q.GetNumber())) if q.GetNumber().isdigit() else (2, 0)
    for p in sorted(fp.Pads(), key=order):
        if not p.GetNumber().isdigit() or int(p.GetNumber()) > 60 or p.GetNetname() in ESC_SKIP:
            continue
        if not p.GetNetname().startswith("/") and "QSPI" in p.GetNetname():
            continue   # flash is next to U1 on top
        if "USB" in p.GetNetname() or "VREG" in p.GetNetname() or "JP5" in p.GetNetname():
            continue   # top-side local nets (USB series R, VREG components)
        q = p.GetPosition(); px, py = TO(q.x), TO(q.y)
        dx, dy = px - cx, py - cy
        inward = (-1 if dx > 0 else 1, 0) if abs(dx) > abs(dy) else (0, -1 if dy > 0 else 1)
        row = 0.45 if int(p.GetNumber()) % 2 == 0 else 0.90   # even pins: row A, odd pins: row B
        d = 0.4 + row   # pad centre -> heel 0.4, then the row offset
        vx, vy = px + inward[0] * d, py + inward[1] * d
        if any(math.hypot(vx - a, vy - b) < 0.6 for a, b in vias) or not ob.via_ok(vx, vy, p.GetNetname()) \
                or not ob.track_ok((px, py), (vx, vy), p.GetNetname(), pcbnew.F_Cu, ESC_W):
            print(f"escape: {ref}.{p.GetNumber()} [{p.GetNetname()}] skipped (no room)")
            continue
        vias.append((vx, vy))
        add_via(board, p.GetNet(), vx, vy)
        t = pcbnew.PCB_TRACK(board)
        t.SetStart(pcbnew.VECTOR2I(MM(px), MM(py))); t.SetEnd(pcbnew.VECTOR2I(MM(vx), MM(vy)))
        t.SetWidth(MM(ESC_W)); t.SetLayer(pcbnew.F_Cu); t.SetNet(p.GetNet())
        board.Add(t)
        placed += 1
    ob.rebuild()
    return placed


def stitch(board, ob, net="GND", pitch=2.0):
    n = board.FindNet(net)
    placed = 0
    y = 1.0
    while y < 51:
        x = 1.0
        while x < 21:
            X, Y = 100 + x, 100 + y
            if ob.via_ok(X, Y, net):
                add_via(board, n, X, Y); placed += 1
                ob.rebuild()
            x += pitch
        y += pitch
    return placed


def main() -> int:
    board = pcbnew.LoadBoard(str(PCB))
    ob = Obstacles(board)
    e = 0
    if "--escape" in sys.argv:
        e = escape(board, ob)
    f = fanout(board, ob)
    f += bridge(board, ob) if "--bridge" in sys.argv else 0
    s = stitch(board, ob) if "--no-stitch" not in sys.argv else 0
    board.BuildConnectivity()
    pcbnew.ZONE_FILLER(board).Fill(board.Zones())
    pcbnew.SaveBoard(str(PCB), board)
    print(f"escape vias {e}, fanout vias {f}, stitching vias {s}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
