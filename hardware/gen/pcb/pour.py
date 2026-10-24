"""3V3 In2 pour integrity for pico-k (D-020 / D-023): piece count and neck width.

The pour may be the real zone fill (KiCad) or a model (zone outline minus other-net In2 copper grown by the zone
clearance), so routing can test a net before it is committed. A neck of width w survives a morphological opening
by w (erode w/2, dilate w/2). The narrowest neck between a set of 3V3 attach points (3V3 vias and 3V3 PTH pads)
is the largest w for which all of them still lie in one piece of the opened pour.
"""
from __future__ import annotations

from shapely.geometry import MultiPolygon, Point, Polygon
from shapely.ops import unary_union

ZONE_CL = 0.20        # zone clearance of the 3V3 In2 pour (zone setting) / min_hole_clearance
EDGE_CL = 0.20        # copper to edge
ATTACH = 0.25         # an attach point (via / PTH centre) joins a piece within its own copper radius
LOCAL_NECK = 0.8      # D-023: wider necks near U1 and the decouplers
MIN_NECK = 0.5        # D-023: narrowest pour neck anywhere


def pieces(g):
    if g.is_empty:
        return []
    return list(g.geoms) if isinstance(g, MultiPolygon) else [g] if isinstance(g, Polygon) else \
        [p for p in getattr(g, "geoms", []) if isinstance(p, Polygon)]


def model_pour(outline, in2_other, holes_other, edges):
    """outline: zone outline polygon; in2_other: [(geom, clearance)] other-net copper on In2; holes_other: hole
    polygons of other-net items; edges: board edge lines."""
    cut = [g.buffer(cl, 8) for g, cl in in2_other] + [h.buffer(ZONE_CL, 8) for h in holes_other]
    cut.append(edges.buffer(EDGE_CL, 8))
    return outline.difference(unary_union(cut))


def connected(pour, pts, w):
    """all attach points in one piece of the pour opened by w (pieces without a point do not count)."""
    g = pour.buffer(-w / 2, 8).buffer(w / 2, 8) if w > 0 else pour
    ps = pieces(g)
    hit = set()
    for x, y in pts:
        p = Point(x, y)
        k = next((i for i, q in enumerate(ps) if q.distance(p) < ATTACH), None)
        if k is None:
            return False, ps
        hit.add(k)
    return len(hit) == 1, ps


def neck(pour, pts, lo=0.0, hi=2.0, tol=0.02):
    """largest opening width (mm) that keeps all pts in one piece (the narrowest neck between them)."""
    if not connected(pour, pts, lo)[0]:
        return 0.0
    while hi - lo > tol:
        m = (lo + hi) / 2
        if connected(pour, pts, m)[0]:
            lo = m
        else:
            hi = m
    return lo


def piece_count(pour, pts):
    """pieces of the pour that hold at least one attach point (what the fill keeps)."""
    ps = pieces(pour)
    return sum(1 for q in ps if any(q.distance(Point(x, y)) < ATTACH for x, y in pts)), sum(q.area for q in ps)


def board_points(board, pcbnew):
    """3V3 attach points: 3V3 vias and 3V3 PTH pads; local = those near U1 or a 3V3 decoupler pad."""
    TO = pcbnew.ToMM
    pts = [(TO(t.GetPosition().x), TO(t.GetPosition().y)) for t in board.GetTracks()
           if t.Type() == pcbnew.PCB_VIA_T and t.GetNetname() == "3V3"]
    pts += [(TO(p.GetPosition().x), TO(p.GetPosition().y)) for fp in board.Footprints() for p in fp.Pads()
            if p.GetNetname() == "3V3" and p.HasHole()]
    u1 = board.FindFootprintByReference("U1").GetBoundingBox(False)
    ux0, uy0, ux1, uy1 = TO(u1.GetLeft()) - 2, TO(u1.GetTop()) - 2, TO(u1.GetRight()) + 2, TO(u1.GetBottom()) + 2
    caps = [(TO(p.GetPosition().x), TO(p.GetPosition().y)) for fp in board.Footprints()
            if fp.GetReference().startswith("C") for p in fp.Pads() if p.GetNetname() == "3V3"]
    local = [q for q in pts if (ux0 <= q[0] <= ux1 and uy0 <= q[1] <= uy1)
             or any(abs(q[0] - c[0]) + abs(q[1] - c[1]) < 2.0 for c in caps)]
    return pts, local


def fill_geom(board, pcbnew):
    z = [z for z in board.Zones() if z.GetNetname() == "3V3" and z.IsOnLayer(pcbnew.In2_Cu)][0]
    f = z.GetFilledPolysList(pcbnew.In2_Cu)
    TO = pcbnew.ToMM
    polys = []
    for i in range(f.OutlineCount()):
        o = f.Outline(i)
        sh = Polygon([(TO(o.CPoint(k).x), TO(o.CPoint(k).y)) for k in range(o.PointCount())],
                     [[(TO(h.CPoint(k).x), TO(h.CPoint(k).y)) for k in range(h.PointCount())]
                      for h in (f.Hole(i, j) for j in range(f.HoleCount(i)))])
        polys.append(sh.buffer(0))
    return unary_union(polys)


def report(pour, pts, local):
    n, area = piece_count(pour, pts)
    main = max(pieces(pour), key=lambda q: q.area)
    anchor = main.representative_point()
    nk = neck(pour, pts)
    nl = neck(pour, local + [(anchor.x, anchor.y)]) if local else None
    return {"pieces": n, "area": round(area, 2), "neck": round(nk, 2), "neck_local": nl and round(nl, 2)}


def main():
    import sys, pcbnew
    b = pcbnew.LoadBoard(sys.argv[1] if len(sys.argv) > 1 else "hardware/pico-k.kicad_pcb")
    pts, local = board_points(b, pcbnew)
    r = report(fill_geom(b, pcbnew), pts, local)
    ok = r["pieces"] == 1 and r["neck"] >= MIN_NECK and (r["neck_local"] is None or r["neck_local"] >= LOCAL_NECK)
    print(f"In2 3V3 pour: {r['pieces']} piece(s), {r['area']} mm2, narrowest neck {r['neck']} mm "
          f"(all {len(pts)} attach points), near U1/decouplers {r['neck_local']} mm ({len(local)} points): "
          + ("OK" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
