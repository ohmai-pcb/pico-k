#!/usr/bin/env python3
"""Scripted hand routing for pico-k (D-022): the connections Freerouting left open on the P2 placement.

Run with the KiCad Python venv ($KT):
  $KT hardware/gen/pcb/handroute.py freeze          # once: store the routed P2 copper (Freerouting + fanout) as
                                                    #   hardware/gen/pcb/routes-base.json (the SES is not kept)
  $KT hardware/gen/pcb/handroute.py route [--nets RE] [--in2]   # route open connections, append to handroute.json
  $KT hardware/gen/pcb/handroute.py replay          # rebuild: fresh build_pcb.py board + routes-base.json +
                                                    #   handroute.json + finishing (pad zone connections), zone fill
Rebuild chain: build_pcb.py -> handroute.py replay  (identical copper; Freerouting is not deterministic, so its
result is frozen in routes-base.json).

Router: grid A* (0.05 mm, 8 directions, F.Cu / B.Cu, optional In2.Cu stubs) on a raster of the other-net copper
grown by clearance + half the track width; every segment and via is then checked on the exact shapes with the
fanout.py rules (via 0.45/0.2, clearance >= 0.1 (Power/USB 0.15, TC 0.2) + 0.03 margin, hole-to-track 0.30, hole to
hole 0.30, copper to edge 0.25). Plane nets (GND, 3V3) end in a via to In1 / In2 (via-less pads). Rules:
hardware/pico-k.kicad_dru (JLC capabilities page, read 2026-10-15/16).
"""
from __future__ import annotations

import argparse
import os
import subprocess
import tempfile
import heapq
import json
import math
import re
import sys
from pathlib import Path

import numpy as np
import pcbnew
import shapely
from shapely.strtree import STRtree
from shapely.geometry import LineString, Point
from shapely.ops import unary_union

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pour as POUR  # noqa: E402  (3V3 In2 pour pieces / necks, D-023)
import fanout as FO  # noqa: E402  (Obstacles, rules, add_track/add_via)

ROOT = Path(__file__).resolve().parents[3]
HW = ROOT / "hardware"
PCB = HW / "pico-k.kicad_pcb"
BASE = HW / "gen" / "pcb" / "routes-base.json"
DATA = Path(os.environ.get("HANDROUTE_DATA", HW / "gen" / "pcb" / "handroute.json"))
MM, TO = pcbnew.FromMM, pcbnew.ToMM
RES = 0.05
X0, Y0, NX, NY = 100.0, 100.0, 420, 1020
LNAME = {pcbnew.F_Cu: "F.Cu", pcbnew.In1_Cu: "In1.Cu", pcbnew.In2_Cu: "In2.Cu", pcbnew.B_Cu: "B.Cu"}
LID = {v: k for k, v in LNAME.items()}
MARGIN = 0.03
# board rules (pico-k.kicad_pro + pico-k.kicad_dru), used exactly by validate(); the grid search adds a margin
R_VIA_HOLE_CU = 0.20   # min_hole_clearance (via holes)
R_PTH_HOLE_TRK = 0.28  # dru "JLC PTH to track 0.28"
R_HOLE_HOLE = 0.25     # min_hole_to_hole / dru
R_EDGE = 0.20          # min_copper_edge_clearance / dru
VIA_COST = 1.6          # mm-equivalent per via
PLANE_WIN = 80           # cells (4 mm): window for a plane via
NO_IN2 = {"Net-(U1-USB_DP)", "Net-(U1-USB_DM)", "/USB_CONN_DP", "/USB_CONN_DM", "3V3", "GND"}  # never on In2
NECK_W = 0.1            # mm: neck-down width (dru min track width) for Default nets with --neck
WIDE_W = 1.4            # mm: In2 cells inside the pour opened by this width are 'wide'
NARROW_PEN = 0.3        # mm extra per grid step on In2 outside the wide pour
IN2_MAX = 2.5           # mm, longest In2 run of one route
IN2_COST = 4.0          # In2 steps cost x4 (D-022: In2 only as short stubs)
PLANE = {"GND": pcbnew.In1_Cu, "3V3": pcbnew.In2_Cu}
NO_RIP = {"GND", "3V3", "Net-(U1-QSPI_SD0)", "Net-(U1-QSPI_SCLK)", "Net-(U1-QSPI_SD3)",
          "Net-(U1-USB_DP)", "Net-(U1-USB_DM)", "/USB_CONN_DP", "/USB_CONN_DM"}   # never ripped
CLASS_CL = {"Default": 0.1, "Power": 0.15, "USB": 0.15, "TC": 0.2}
CLASS_W = {"Default": 0.15, "Power": 0.25, "USB": 0.14, "TC": 0.2}
# Finishing (D-022): pads whose thermal spokes are starved by the tracks around them are connected solid
# (castellated GND pins J4 and the USB shell tabs: soldered by reflow / hand with the plane, JLC no limit).
SOLID_PADS = {"J4": None, "J1": ("S1",)}
# D-029: SMD GND pads boxed in by the TPS63001 cluster (starved F.Cu thermal spokes)
SOLID_SMD = {"U3": ("3", "9"), "C15": ("2",)}


# Manual geometry (D-022): nets where the shortest grid path would block a neighbour. Polylines in KiCad mm
# (board x + 100, y + 100); "via" points between layer runs. Checked with validate() like router output.
MANUAL = {
    # QSPI right column (U2 pads 5-7, right ends x 109.625) from U1 pins 57 / 56 / 55 nested, no crossings:
    # SD0 straight up, SCLK around pad 5 at x 109.83, SD3 outside it at x 110.11, y 118.9 (0.15 track, >= 0.12 gaps; 0.175 to the 3V3 pin 54).
    "qspi_sd0": [("Net-(U1-QSPI_SD0)", 0.15, [("F.Cu", [(108.9, 119.55), (108.9, 118.25)])])],
    "qspi_sclk": [("Net-(U1-QSPI_SCLK)", 0.15, [("F.Cu", [(109.3, 119.55), (109.3, 118.63), (109.83, 118.63),
                                                          (109.83, 117.75), (109.17, 117.75)])])],
    "qspi_sd3": [("Net-(U1-QSPI_SD3)", 0.15, [("F.Cu", [(109.7, 119.55), (109.7, 118.9), (110.11, 118.9),
                                                        (110.11, 117.25), (109.17, 117.25)])])],
    # D-025: GND for the right passive column after the 0.5 mm shift (F.Cu GND fill islands without a via).
    # Via-only entries sit inside the island fill; tracks join neighbouring GND pads to it.
    "gnd_c27_via": [("GND", 0.25, [("F.Cu", [(118.2, 124.6)]), ("B.Cu", [(118.2, 124.6)])])],
    "gnd_c4_c27": [("GND", 0.15, [("F.Cu", [(116.82, 123.45), (117.32, 123.95), (117.84, 123.95)])])],
    "gnd_r9_c6_via": [("GND", 0.25, [("F.Cu", [(116.7, 127.25)]), ("B.Cu", [(116.7, 127.25)])])],
    "vreg_avdd_r5_c18": [("Net-(U1-VREG_AVDD)", 0.15, [("F.Cu", [(116.85, 120.39), (117.35, 120.39), (117.84, 120.88)])])],
    "adc_avdd_r21_c27": [("/ADC_AVDD", 0.15, [("F.Cu", [(116.85, 121.41), (117.35, 121.41), (117.84, 121.9), (117.84, 122.99)])])],
    # D-026: thermal spokes for C10.2 (to C4.2) and R9.2 (to the C1.2 GND via) - starved_thermal fixes.
    "gnd_c10_c4": [("GND", 0.15, [("F.Cu", [(116.82, 122.43), (116.82, 123.45)])])],
    "gnd_r9_via": [("GND", 0.15, [("F.Cu", [(104.13, 120.41), (104.6, 120.41), (104.928, 120.079)])])],
    # D-026: U3 pin 9 GND straight into the exposed pad (GND, thermal vias) instead of its own via, which frees
    # the pocket north of pins 8-10 for VINA (U3.8 -> R14.2, SLVS520C VINA filter).
    # D-029: TPS63001 turned 270 deg (pins 1-5 face L2 above, VIN west to C20 at pin 5 on F.Cu, SLVS520C 10.1/10.2)
    "u3_vin_c20": [("VSYS", 0.3, [("F.Cu", [(115.3, 113.24), (115.3, 112.95), (114.4, 112.05), (113.9, 112.05)])]),
                   ("VSYS", 0.6, [("F.Cu", [(114.75, 112.4), (114.2, 111.85)])])],
    "u3_lx1": [("Net-(U3-L1)", 0.3, [("F.Cu", [(115.8, 113.24), (115.8, 112.6)])]),
               ("Net-(U3-L1)", 0.6, [("F.Cu", [(115.8, 112.6), (115.8, 112.3), (115.4, 111.9), (115.35, 111.4)])])],
    "u3_lx2": [("Net-(U3-L2)", 0.3, [("F.Cu", [(116.8, 113.24), (116.8, 112.45)])]),
               ("Net-(U3-L2)", 0.6, [("F.Cu", [(116.8, 112.45), (116.8, 112.0), (117.45, 111.6), (117.6, 111.4)])])],
    "u3_pgnd_ep": [("GND", 0.24, [("F.Cu", [(116.3, 113.24), (116.3, 113.9)])])],
    "gnd_u3_9_ep": [("GND", 0.24, [("F.Cu", [(116.8, 116.04), (116.8, 115.3)])])],
    "u3_vout_j4": [("3V3", 0.24, [("F.Cu", [(117.3, 113.24), (117.3, 112.85)])]),
                   ("3V3", 0.3, [("F.Cu", [(117.3, 112.85), (117.7, 112.45), (118.85, 112.45)])])],
    "u3_vina": [("Net-(U3-VINA)", 0.15, [("F.Cu", [(116.3, 116.04), (116.3, 116.5), (116.8, 117.0), (117.55, 117.0)])])],
    # D-029: close the 3V3_EN B stub to the R15-side via after the U3 move
    "en_gap": [("/3V3_EN", 0.15, [("B.Cu", [(109.225, 111.125), (108.775, 111.525)])])],
    "u3_3v3_10": [("3V3", 0.24, [("F.Cu", [(117.3, 116.04), (117.75, 116.04), (118.0, 116.3)])])],
    # D-026: U1.20 (IOVDD) on F straight to its decoupler C3.1 (3V3 via there); the old DVDD F trunk/B link that
    # boxed it in is rerouted, and the XIN/XOUT vias move ~0.1 mm SE so the 3V3 track clears them.
    "v3v3_u1_20": [("3V3", 0.2, [("F.Cu", [(109.3, 126.45), (109.3, 126.9), (108.8, 127.4), (107.75, 127.4), (107.55, 127.6), (107.55, 128.01)])])],
    # D-027: C9 (100 nF) turned vertical directly under U1.23: DVDD 1.0 mm on F.Cu, no via. The XOUT via sits under
    # pin 22 (0.195 mm above C9.1), XIN drops SW of it beside the U1.20 3V3 track; both continue on B as before.
    "xin_u1_21": [("Net-(U1-XIN)", 0.12, [("F.Cu", [(109.7, 126.45), (109.7, 127.0), (109.45, 127.25), (109.45, 127.6)]),
                                         ("B.Cu", [(109.45, 127.6), (109.0, 127.6), (108.259, 128.341), (108.259, 128.809),
                                                   (108.009, 129.059), (107.956, 129.059)])])],
    "xout_u1_22": [("Net-(U1-XOUT)", 0.15, [("F.Cu", [(110.1, 126.45), (110.1, 126.95), (110.0, 127.05), (110.0, 127.3)]),
                                           ("B.Cu", [(110.0, 127.3), (110.0, 128.6), (108.6, 130.0), (108.6, 130.9617)])])],
    "dvdd_u1_23_c9": [("DVDD", 0.15, [("F.Cu", [(110.5, 126.45), (110.5, 128.0), (110.24, 128.0)])])],
    # C9.1 -> DVDD trunk west of C9 (x 109.25, between C28 and R3) into the In2 trunk via, which also takes C28.1;
    # C9.2 -> C28.2 straight, GND via east of them (pads >= 0.345 mm from via centres).
    "dvdd_c9_c28": [("DVDD", 0.12, [("F.Cu", [(110.24, 128.2), (109.25, 128.2), (109.25, 131.2), (109.125, 131.325)])])],
    "dvdd_c28_trunk": [("DVDD", 0.15, [("F.Cu", [(109.95, 131.735), (109.54, 131.325), (109.125, 131.325)])])],
    "gnd_c9_c28": [("GND", 0.25, [("F.Cu", [(110.24, 128.96), (110.24, 129.45), (109.95, 129.74), (109.95, 130.185)])])],
    "gnd_c9_via": [("GND", 0.25, [("F.Cu", [(110.24, 129.45), (110.95, 129.45)]), ("B.Cu", [(110.95, 129.45)])])],
    # D-026 east rework: ADC_VREF R21 -> R20 leaves the J4 link's via eastwards on B (under column A), drops to F
    # beside column B, crosses GP26 on In2 and lands on R20.2; the old run west of the GP27 via blocked U1.43.
    "adc_vref_r21_r20": [("/ADC_VREF", 0.15, [("B.Cu", [(115.275, 120.925), (115.325, 120.975), (118.475, 120.975), (118.525, 120.925)]),
                                             ("F.Cu", [(118.525, 120.925), (118.525, 121.175), (118.375, 121.325), (118.375, 123.075), (118.525, 123.225)]),
                                             ("In2.Cu", [(118.525, 123.225), (117.475, 124.275), (117.475, 124.625)]),
                                             ("F.Cu", [(117.475, 124.625), (117.075, 124.625)])])],
    "gnd_c18_c5": [("GND", 0.15, [("F.Cu", [(117.84, 119.93), (117.84, 119.78), (116.82, 119.78), (116.82, 119.37)])])],
}


# ---------------------------------------------------------------- geometry / raster
def grid_xy(ix, iy):
    return X0 + (ix + 0.5) * RES, Y0 + (iy + 0.5) * RES


def raster(geom, bbox):
    """bool mask NY x NX of the cells whose centre lies in geom (restricted to bbox ix0, iy0, ix1, iy1)."""
    ix0, iy0, ix1, iy1 = bbox
    m = np.zeros((NY, NX), bool)
    if geom.is_empty:
        return m
    xs = X0 + (np.arange(ix0, ix1) + 0.5) * RES
    ys = Y0 + (np.arange(iy0, iy1) + 0.5) * RES
    gx, gy = np.meshgrid(xs, ys)
    shapely.prepare(geom)
    m[iy0:iy1, ix0:ix1] = shapely.contains_xy(geom, gx, gy)
    return m


_PAT = [(re.compile(c["pattern"]), c["netclass"]) for c in
        json.loads((HW / "pico-k.kicad_pro").read_text())["net_settings"].get("netclass_patterns", [])]


def netclass(board, net):
    """net class by the project's netclass_patterns (first match), as KiCad assigns it."""
    for rx, c in _PAT:
        if rx.search(net):
            return c
    return "Default"


def clearance(cls_a, cls_b="Default"):
    return max(CLASS_CL.get(cls_a, 0.1), CLASS_CL.get(cls_b, 0.1)) + MARGIN


RIP_CAP = 4
RIP_PEN = 0.4    # mm of extra path cost per grid cell over rippable copper (rip-up search)


class Env:
    def __init__(self, board, manual=()):
        self.b = board
        self.manual = set(manual)   # item keys of 'manual' records: never ripped (they survive in the data too)
        self.ob = FO.Obstacles(board)
        self.cls = {str(n): netclass(board, str(n)) for n in board.GetNetsByName().keys()}
        self.keep_tracks = [FO.poly(z.Outline()) for z in board.Zones() if z.GetIsRuleArea() and z.GetDoNotAllowTracks()]

        self._index()

    def _index(self):
        """model metadata: for every obstacle entry the item key of its track / via (None for pads)."""
        self.meta = {L: [] for L in self.ob.cu}
        self.hmeta = []
        for fp in self.b.Footprints():
            for p in fp.Pads():
                for L in self.ob.cu:
                    if p.IsOnLayer(L):
                        self.meta[L].append(None)
                if p.HasHole():
                    self.hmeta.append((p.GetNetname(), "padhole"))
        for t in self.b.GetTracks():
            k = tuple(item_key(t))
            if t.Type() == pcbnew.PCB_VIA_T:
                for L in self.ob.cu:
                    self.meta[L].append(k)
                self.hmeta.append(k)
            elif t.GetLayer() in self.ob.cu:
                self.meta[t.GetLayer()].append(k)
        self._reindex()

    def _reindex(self):
        ob = self.ob
        assert all(len(ob.cu[L]) == len(self.meta[L]) for L in ob.cu) and len(ob.holes) == len(self.hmeta)
        self.trackidx = {L: {i for i, m in enumerate(self.meta[L]) if m} for L in ob.cu}
        self.ikey = {(L, i): m for L in ob.cu for i, m in enumerate(self.meta[L]) if m}
        self.viaholes = {i for i, m in enumerate(self.hmeta) if m[1] == "via"}
        ob.trees = {L: STRtree([g for g, _ in v]) for L, v in ob.cu.items()}
        ob.holetree = STRtree(ob.holes)
        self._wide = None     # cached In2 'wide pour' raster (D-023 cost field)
        self._alive = None

    def alive(self):
        if self._alive is None:
            self._alive = set(self.ikey.values()) | {m for m in self.hmeta if m[1] == "via"}
        return self._alive

    # --- in-memory model edits (the board itself is only ever added to; replay rebuilds it)
    def snapshot(self):
        return ({L: list(v) for L, v in self.ob.cu.items()}, list(self.ob.holes),
                {L: list(v) for L, v in self.meta.items()}, list(self.hmeta))

    def restore(self, snap):
        cu, holes, meta, hmeta = snap
        self.ob.cu = {L: list(v) for L, v in cu.items()}; self.ob.holes = list(holes)
        self.meta = {L: list(v) for L, v in meta.items()}; self.hmeta = list(hmeta)
        self._reindex()

    def remove_nets(self, nets):
        """drop all track / via copper of these nets from the model."""
        for L in self.ob.cu:
            keep = [(e, m) for e, m in zip(self.ob.cu[L], self.meta[L]) if not (m and m[0] in nets and m not in self.manual)]
            self.ob.cu[L] = [e for e, _ in keep]; self.meta[L] = [m for _, m in keep]
        keep = [(h, m) for h, m in zip(self.ob.holes, self.hmeta) if not (m[1] == "via" and m[0] in nets and m not in self.manual)]
        self.ob.holes = [h for h, _ in keep]; self.hmeta = [m for _, m in keep]
        self._reindex()

    def add_rec(self, rec):
        net = rec["net"]
        for t in rec["tracks"]:
            L = LID[t["layer"]]
            self.ob.cu[L].append((LineString([tuple(t["a"]), tuple(t["b"])]).buffer(t["w"] / 2), net))
            self.meta[L].append((net, "track", *t["a"], *t["b"]))
        for x, y in rec["vias"]:
            for L in self.ob.cu:
                self.ob.cu[L].append((Point(x, y).buffer(FO.VIA_D / 2), net)); self.meta[L].append((net, "via", x, y))
            self.ob.holes.append(Point(x, y).buffer(FO.VIA_H / 2)); self.hmeta.append((net, "via", x, y))
        self._reindex()

    def refresh(self):
        self.ob.rebuild()
        self._index()

    def pour_report(self):
        """D-023: model of the 3V3 In2 pour with the current model copper -> pieces, area, necks."""
        if not hasattr(self, "_pz"):
            z = [z for z in self.b.Zones() if z.GetNetname() == "3V3" and z.IsOnLayer(pcbnew.In2_Cu)][0]
            self._pz = FO.poly(z.Outline())
            pts, local = POUR.board_points(self.b, pcbnew)
            self._local = local
        L = pcbnew.In2_Cu
        other = [(g, POUR.ZONE_CL) for (g, n) in self.ob.cu[L] if n != "3V3"]
        holes = [h for h, m in zip(self.ob.holes, self.hmeta) if m[0] != "3V3"]
        pour = POUR.model_pour(self._pz, other, holes, self.ob.edges)
        pts = [(m[2], m[3]) for m in self.hmeta if m[0] == "3V3" and m[1] == "via"]
        pts += [(h.centroid.x, h.centroid.y) for h, m in zip(self.ob.holes, self.hmeta) if m == ("3V3", "padhole")]
        return POUR.report(pour, pts, self._local)

    def model_pour(self):
        if not hasattr(self, "_pz"):
            self.pour_report()
        other = [(g, POUR.ZONE_CL) for (g, n) in self.ob.cu[pcbnew.In2_Cu] if n != "3V3"]
        holes = [h for h, m in zip(self.ob.holes, self.hmeta) if m[0] != "3V3"]
        return POUR.model_pour(self._pz, other, holes, self.ob.edges)

    def wide(self):
        """cells where the (model) 3V3 pour is at least WIDE_W wide: In2 runs there leave real necks."""
        if self._wide is None:
            g = self.model_pour().buffer(-WIDE_W / 2, 8).buffer(WIDE_W / 2, 8)
            self._wide = raster(g, (0, 0, NX, NY))
        return self._wide

    def pour_ok(self, base):
        r = self.pour_report()
        ok = (r["pieces"] == 1 and r["neck"] >= min(POUR.MIN_NECK, base["neck"]) and
              (r["neck_local"] is None or r["neck_local"] >= min(POUR.LOCAL_NECK, base["neck_local"] or 9)))
        return ok, r

    def rec_items(self, rec):
        """route-target stand-ins for the copper of a (model-only) route record."""
        out = [("geom", LID[t["layer"]], LineString([tuple(t["a"]), tuple(t["b"])]).buffer(t["w"] / 2)) for t in rec["tracks"]]
        for x, y in rec["vias"]:
            out += [("geom", L, Point(x, y).buffer(FO.VIA_D / 2)) for L in (pcbnew.F_Cu, pcbnew.B_Cu, pcbnew.In2_Cu)]
        return out

    def blocked(self, net, w, layer, bbox, via=False, soft=()):
        """cells where a track centre (or a via centre if via) of net may not be; copper of nets in soft is left
        out (rip-up search)."""
        x0, y0 = X0 + bbox[0] * RES, Y0 + bbox[1] * RES
        x1, y1 = X0 + bbox[2] * RES, Y0 + bbox[3] * RES
        win = shapely.geometry.box(x0 - 1, y0 - 1, x1 + 1, y1 + 1)
        r = (FO.VIA_D / 2) if via else w / 2
        mycls = self.cls.get(net, "Default")
        geoms = []
        for i in self.ob.trees[layer].query(win):
            g, n = self.ob.cu[layer][i]
            if n != net and not (n in soft and i in self.trackidx[layer]):
                cl = clearance(mycls, self.cls.get(n, "Default")) + r
                if via:   # the via hole keeps hole-to-copper from other-net copper too (fanout.via_ok)
                    cl = max(cl, FO.VIA_H / 2 + R_VIA_HOLE_CU + 0.02)
                geoms.append(g.buffer(cl, 8))
        for i in self.ob.holetree.query(win):    # hole to track / via copper
            if soft and i in self.viaholes and self.hmeta[i][0] in soft:
                continue
            if not via and self.hmeta[i][0] == net and self.hmeta[i][1] == "padhole":
                continue      # own PTH pad: the track ends on its ring
            pth = self.hmeta[i][1] == "padhole"
            geoms.append(self.ob.holes[i].buffer((R_HOLE_HOLE + 0.02 + FO.VIA_H / 2) if via else
                                                 ((R_PTH_HOLE_TRK if pth else R_VIA_HOLE_CU) + 0.02 + w / 2), 8))
        geoms.append(self.ob.edges.buffer(R_EDGE + 0.03 + r, 8))
        for k in self.keep_tracks:
            geoms.append(k.buffer(r + 0.05))
        if via:
            for k in self.ob.keepouts:
                geoms.append(k.buffer(r + 0.07))
        m = raster(unary_union(geoms), bbox) if geoms else np.zeros((NY, NX), bool)
        out = np.ones((NY, NX), bool)
        out[bbox[1]:bbox[3], bbox[0]:bbox[2]] = m[bbox[1]:bbox[3], bbox[0]:bbox[2]]
        return out


# ---------------------------------------------------------------- A*
def astar(free, viaok, starts, goals, layers, cost_mult, pen=None, vpen=None):
    """free[l]: NY x NX bool; viaok: bool; starts/goals: sets of (l, iy, ix). Returns list of (l, iy, ix)."""
    goal_l = {}
    for l, y, x in goals:
        goal_l.setdefault(l, set()).add((y, x))
    gy = np.array([g[1] for g in goals]); gx = np.array([g[2] for g in goals])
    cy, cx = gy.mean(), gx.mean()
    def h(y, x):
        dy, dx = abs(y - cy), abs(x - cx)
        return (max(dx, dy) + 0.414 * min(dx, dy)) * RES * 0.9 - spread
    spread = (max(np.ptp(gy), np.ptp(gx)) * RES) if len(goals) > 1 else 0.0
    D = [(0, 1, 1), (1, 0, 1), (0, -1, 1), (-1, 0, 1), (1, 1, 1.4142), (1, -1, 1.4142), (-1, 1, 1.4142), (-1, -1, 1.4142)]
    best = {}
    pq = []
    for s in starts:
        best[s] = 0.0
        heapq.heappush(pq, (h(s[1], s[2]), 0.0, s, None))
    parent = {}
    n = 0
    while pq:
        f, g, s, par = heapq.heappop(pq)
        if g > best.get(s, 1e18) + 1e-9:
            continue
        if s in parent:
            continue
        parent[s] = par
        l, y, x = s
        if (y, x) in goal_l.get(l, ()):
            path = [s]
            while parent[path[-1]] is not None:
                path.append(parent[path[-1]])
            return path[::-1]
        n += 1
        if n > 2_500_000:
            return None
        for dy, dx, c in D:
            yy, xx = y + dy, x + dx
            if 0 <= yy < NY and 0 <= xx < NX and free[l][yy, xx]:
                ng = g + c * RES * cost_mult[l] + (pen[l][yy, xx] if pen is not None else 0.0)
                t = (l, yy, xx)
                if ng < best.get(t, 1e18):
                    best[t] = ng
                    heapq.heappush(pq, (ng + h(yy, xx), ng, t, s))
        if viaok[y, x] and not near_path_via(parent, s, y, x):
            for l2 in layers:
                if l2 != l and free[l2][y, x]:
                    ng = g + VIA_COST + (vpen[y, x] if vpen is not None else 0.0)
                    t = (l2, y, x)
                    if ng < best.get(t, 1e18):
                        best[t] = ng
                        heapq.heappush(pq, (ng + h(y, x), ng, t, s))
    return None


VIA_PITCH_CELLS = (FO.VIA_H + R_HOLE_HOLE) / RES + 1e-9   # same-net via centres: hole_to_hole applies to every pair


def near_path_via(parent, s, y, x):
    """True if the partial path ending in s already changed layer within hole-to-hole reach of (y, x): KiCad's
    hole_to_hole rule holds between any two holes, own net included, so a path must not stack vias closer."""
    cur, steps = s, 0
    while cur is not None and steps < int(VIA_PITCH_CELLS) + 4:
        prev = parent.get(cur)
        if prev is None:
            return False
        if prev[0] != cur[0] and math.hypot(cur[1] - y, cur[2] - x) < VIA_PITCH_CELLS:
            return True
        if prev[1:] != cur[1:]:
            steps += 1
        cur = prev
    return False


def simplify(path):
    """grid path -> [(layer, [(x, y), ...])] polylines, collinear points merged; via points between runs."""
    runs, cur = [], [path[0]]
    for p in path[1:]:
        if p[0] != cur[-1][0]:
            runs.append(cur); cur = [p]
        else:
            cur.append(p)
    runs.append(cur)
    out = []
    for r in runs:
        pts = [r[0]]
        for i in range(1, len(r) - 1):
            a, b, c = pts[-1], r[i], r[i + 1]
            d1 = (np.sign(b[1] - a[1]), np.sign(b[2] - a[2])); d2 = (np.sign(c[1] - b[1]), np.sign(c[2] - b[2]))
            if d1 != d2:
                pts.append(b)
        if len(r) > 1:
            pts.append(r[-1])
        out.append((r[0][0], [grid_xy(p[2], p[1]) for p in pts]))
    return out


# ---------------------------------------------------------------- items
def item_cells(env, it, layers):
    """cells inside the copper of a pad / track / via on the given layers -> set of (l, iy, ix)."""
    cells = set()
    for l in layers:
        if isinstance(it, tuple):
            if it[1] != l:
                continue
            g = it[2]
        elif not it.IsOnLayer(l):
            continue
        else:
            g = FO.item_poly(it, l)
        if g.is_empty:
            continue
        bx = g.bounds
        bb = (max(0, int((bx[0] - X0) / RES) - 1), max(0, int((bx[1] - Y0) / RES) - 1),
              min(NX, int((bx[2] - X0) / RES) + 2), min(NY, int((bx[3] - Y0) / RES) + 2))
        m = raster(g.buffer(-0.02), bb)
        if not m.any():
            m = raster(g, bb)
        for y, x in zip(*np.nonzero(m)):
            cells.add((l, int(y), int(x)))
    return cells


def _cu_layers(t):
    return [l for l in (pcbnew.F_Cu, pcbnew.In1_Cu, pcbnew.In2_Cu, pcbnew.B_Cu) if t.IsOnLayer(l)]


def island(board, it, alive=None):
    """it plus every same-net track/via touching it on a shared layer, transitively.
    alive: item keys still in the router model. The pcbnew board is only ever added to, so after an
    in-run rip-up it still holds the ripped copper; without this filter a re-route 'reached' that phantom
    copper, and the net was saved unrouted (rip-up bug, D-029).
    A hand-drawn via at a track end is then a terminal on all its layers. Before this, an F.Cu-only
    track end was the only goal, and the router gave an instant 'no path' with no rip-up candidates."""
    if isinstance(it, tuple) or not hasattr(it, "GetNetname"):
        return [it]
    ok = (lambda t: True) if alive is None else (lambda t: tuple(item_key(t)) in alive)
    if not isinstance(it, pcbnew.PAD) and not ok(it):
        return []
    net = it.GetNetname()
    cand = [t for t in board.GetTracks() if t.GetNetname() == net and t is not it and ok(t)]
    geo = {}
    def g(t, l):
        k = (id(t), l)
        if k not in geo:
            geo[k] = FO.item_poly(t, l).buffer(0.001)
        return geo[k]
    out, todo, seen = [it], [it], {id(it)}
    while todo:
        a = todo.pop()
        for t in cand:
            if id(t) in seen:
                continue
            if any(t.IsOnLayer(l) and g(t, l).intersects(g(a, l)) for l in _cu_layers(a)):
                seen.add(id(t)); out.append(t); todo.append(t)
    return out


def island_cells(env, it, layers):
    return set().union(set(), *(item_cells(env, i, layers) for i in island(env.b, it, env.alive())))


def find_item(board, desc, pos):
    """board item for a DRC unconnected-item description + position (mm, KiCad coords)."""
    p = pcbnew.VECTOR2I(MM(pos[0]), MM(pos[1]))
    m = re.match(r"(?:PTH )?[Pp]ad (\S+) \[.*\] of (\S+)", desc)
    if m:
        fp = board.FindFootprintByReference(m.group(2))
        cands = [q for q in fp.Pads() if q.GetNumber() == m.group(1)]
        return min(cands, key=lambda q: (q.GetPosition() - p).EuclideanNorm())
    best = None
    for t in board.GetTracks():
        if desc.startswith("Via") != (t.Type() == pcbnew.PCB_VIA_T):
            continue
        if t.HitTest(p, MM(0.01)):
            if best is None or (t.GetPosition() - p).EuclideanNorm() < (best.GetPosition() - p).EuclideanNorm():
                best = t
    return best


def drc_unconnected():
    import subprocess, tempfile
    out = Path(tempfile.gettempdir()) / "handroute-drc.json"
    subprocess.run(["kicad-cli", "pcb", "drc", "--format", "json", "--severity-all", "-o", str(out), str(PCB)],
                   capture_output=True, check=False)
    d = json.loads(out.read_text())
    res = []
    for u in d.get("unconnected_items", []):
        a, b = u["items"][:2]
        net = re.search(r"\[(.*?)\]", a["description"]).group(1)
        res.append((net, (a["description"], (a["pos"]["x"], a["pos"]["y"])), (b["description"], (b["pos"]["x"], b["pos"]["y"]))))
    return res, d


# ---------------------------------------------------------------- apply / record
def apply(board, rec):
    net = board.FindNet(rec["net"])
    for seg in rec.get("tracks", []):
        FO.add_track(board, net, tuple(seg["a"]), tuple(seg["b"]), LID[seg["layer"]], seg["w"])
    for v in rec.get("vias", []):
        FO.add_via(board, net, v[0] - 100 + 100, v[1])


def via_ok(env, x, y, net):
    """exact via check against the board rules (net-class clearance, via hole to copper, hole to hole, edge,
    via-to-pad gap, via keep-outs)."""
    ob, c, r = env.ob, Point(x, y), FO.VIA_D / 2
    mycls = env.cls.get(net, "Default")
    for L in ob.cu:
        for i in ob.trees[L].query(c.buffer(r + 0.3)):
            g, n = ob.cu[L][i]
            if n == net:
                continue
            d = g.distance(c)
            if d < r + clearance(mycls, env.cls.get(n, "Default")) - MARGIN or d < FO.VIA_H / 2 + R_VIA_HOLE_CU:
                return False
    for i in ob.padtree.query(c.buffer(r + FO.PAD_GAP)):
        if ob.pads[i].distance(c) < r + FO.PAD_GAP:
            return False
    for i in ob.holetree.query(c.buffer(FO.VIA_H / 2 + R_HOLE_HOLE)):
        if ob.holes[i].distance(c) < FO.VIA_H / 2 + R_HOLE_HOLE:
            return False
    if ob.edges.distance(c) < r + R_EDGE:
        return False
    return not any(k.distance(c) < r + 0.05 for k in ob.keepouts)


def validate(env, net, w, segs, vias):
    ob = env.ob
    mycls = env.cls.get(net, "Default")
    for layer, a, b in segs:
        ln = LineString([a, b]).buffer(w / 2)
        for i in ob.trees[layer].query(ln.buffer(0.3)):
            g, n = ob.cu[layer][i]
            if n != net and g.distance(ln) < clearance(mycls, env.cls.get(n, "Default")) - MARGIN:
                return f"clearance {n} on {LNAME[layer]}"
        for i in ob.holetree.query(ln.buffer(0.4)):
            if env.hmeta[i][0] == net:   # own pad holes and own vias: same net, no hole clearance (KiCad rule)
                continue
            if ob.holes[i].distance(ln) < (R_PTH_HOLE_TRK if env.hmeta[i][1] == "padhole" else R_VIA_HOLE_CU):
                return "hole clearance"
        if ob.edges.distance(ln) < R_EDGE:
            return "edge"
    for x, y in vias:
        if not via_ok(env, x, y, net):
            return f"via at {x:.2f},{y:.2f}"
    for i, p in enumerate(vias):   # hole_to_hole between the new vias themselves (same net counts too)
        for q in vias[i + 1:]:
            if math.dist(p, q) < FO.VIA_H + R_HOLE_HOLE:
                return f"via hole-to-hole {p[0]:.2f},{p[1]:.2f} / {q[0]:.2f},{q[1]:.2f}"
    return None


def route_one(env, net, src, dst, use_in2=False, w=None, plane=False, soft=()):
    b = env.b
    cls = env.cls.get(net, "Default")
    w = w or CLASS_W.get(cls, 0.15)
    layers = [pcbnew.F_Cu, pcbnew.B_Cu] + ([pcbnew.In2_Cu] if use_in2 and net not in NO_IN2 else [])
    starts = island_cells(env, src, layers)
    goals = (set().union(*(island_cells(env, d, layers) for d in dst)) if isinstance(dst, list) else
             island_cells(env, dst, layers)) if dst is not None else set()
    allc = starts | goals
    ys = [c[1] for c in allc]; xs = [c[2] for c in allc]
    pad = 160 if dst is not None else PLANE_WIN      # search window margin (cells): 8 mm, plane via window
    bbox = (max(0, min(xs) - pad), max(0, min(ys) - pad), min(NX, max(xs) + pad), min(NY, max(ys) + pad))
    free = {l: ~env.blocked(net, w, l, bbox, soft=soft) for l in layers}
    vb = np.zeros((NY, NX), bool)
    for l in (pcbnew.F_Cu, pcbnew.In1_Cu, pcbnew.In2_Cu, pcbnew.B_Cu):
        vb |= env.blocked(net, w, l, bbox, via=True, soft=soft)
    pen = vpen = None
    if soft:   # crossing soft (rippable) copper is allowed at a price: rip as little as possible
        pen = {l: np.where(free[l] & env.blocked(net, w, l, bbox), RIP_PEN, 0.0) for l in layers}
        hv = np.zeros((NY, NX), bool)
        for l in (pcbnew.F_Cu, pcbnew.In1_Cu, pcbnew.In2_Cu, pcbnew.B_Cu):
            hv |= env.blocked(net, w, l, bbox, via=True)
        vpen = np.where(hv & ~vb, 20 * RIP_PEN, 0.0)
    # no via in a pad (own SMD pads included: solder wicking)
    padg = unary_union([g for g in env.ob.pads])
    vb |= raster(padg.buffer(FO.VIA_D / 2 + FO.PAD_GAP), bbox)
    viaok = ~vb
    for l in layers:
        for (ll, y, x) in allc:
            if ll == l:
                free[l][y, x] = True      # own copper
    if plane:
        # goal: any cell where a via can drop to the plane, reached on the pad layer
        goals = {(l, int(y), int(x)) for l in (pcbnew.F_Cu,) for y, x in zip(*np.nonzero(viaok & free[pcbnew.F_Cu]))}
        goals = {g for g in goals if bbox[0] <= g[2] < bbox[2] and bbox[1] <= g[1] < bbox[3]}
        if not goals:
            return None, "no via site"
    starts = {s for s in starts if free[s[0]][s[1], s[2]]}
    cost = {pcbnew.F_Cu: 1.0, pcbnew.B_Cu: 1.0, pcbnew.In2_Cu: IN2_COST}
    if pcbnew.In2_Cu in layers and IN2_MAX > 100:   # D-023: In2 runs prefer wide pour (keeps the necks)
        pen = dict(pen) if pen else {l: np.zeros((NY, NX)) for l in layers}
        pen.setdefault(pcbnew.In2_Cu, np.zeros((NY, NX)))
        pen[pcbnew.In2_Cu] = pen[pcbnew.In2_Cu] + np.where(env.wide(), 0.0, NARROW_PEN)
    path = astar(free, viaok, starts, goals, layers, cost, pen, vpen)
    if not path:
        return None, "no path"
    runs = simplify(path)
    segs, vias = [], []
    for i, (l, pts) in enumerate(runs):
        for a, c in zip(pts, pts[1:]):
            segs.append((l, a, c))
        if i + 1 < len(runs):
            vias.append(pts[-1])
    if plane:
        vias.append(runs[-1][1][-1])
    if soft:   # rip-up search: which soft nets does this path cross?
        hit = set()
        for l, a_, c_ in segs:
            ln = LineString([a_, c_]).buffer(w / 2 + 0.25)
            for i in env.ob.trees[l].query(ln):
                g, n = env.ob.cu[l][i]
                if n in soft and i in env.trackidx[l] and g.buffer(clearance(cls, env.cls.get(n, "Default"))).intersects(LineString([a_, c_]).buffer(w / 2)):
                    hit.add(env.ikey[(l, i)])
        for x, y in vias:
            c = Point(x, y).buffer(FO.VIA_D / 2 + 0.35)
            for l in env.ob.cu:
                for i in env.ob.trees[l].query(c):
                    g, n = env.ob.cu[l][i]
                    if n in soft and i in env.trackidx[l] and g.buffer(clearance(cls, env.cls.get(n, "Default"))).intersects(Point(x, y).buffer(FO.VIA_D / 2)):
                        hit.add(env.ikey[(l, i)])
        return None, ("rip", hit)
    err = validate(env, net, w, segs, vias)
    if err:
        return None, err
    for l, pts in runs:   # D-020/D-022: In2 only as short stubs under a wall
        if l == pcbnew.In2_Cu and sum(math.dist(p, q) for p, q in zip(pts, pts[1:])) > IN2_MAX:
            return None, "In2 stub too long"

    rec = {"net": net, "w": w, "tracks": [{"layer": LNAME[l], "a": [round(a[0], 3), round(a[1], 3)],
                                           "b": [round(c[0], 3), round(c[1], 3)], "w": w} for l, a, c in segs],
           "vias": [[round(x, 3), round(y, 3)] for x, y in vias]}
    return rec, None


def is_manual(r):
    return r.get("why", "").startswith("manual")


def manual_keys(routes):
    """item keys (as item_key gives them) of the copper of 'manual' records."""
    out = set()
    for r in routes:
        if is_manual(r):
            out |= {(r["net"], "track", *map(lambda v: round(v, 3), (*t["a"], *t["b"]))) for t in r["tracks"]}
            out |= {(r["net"], "via", round(x, 3), round(y, 3)) for x, y in r["vias"]}
    return out


def keep_routes(routes, ripped):
    """records that survive ripping these nets: other nets, and manual records (hand-drawn copper is never
    ripped). Used by --rip, the checkpoint, the final save and the pour trial alike, so the saved data and
    the rebuilt board always agree (before, --rip kept manual records but removed their copper from the
    saved board, and the next rebuild brought the 'ripped' copper back)."""
    return [r for r in routes if r["net"] not in ripped or is_manual(r)]


def load_data():
    return json.loads(DATA.read_text()) if DATA.exists() else {"rip": [], "routes": []}


def item_key(t):
    if t.Type() == pcbnew.PCB_VIA_T:
        p = t.GetPosition(); return [t.GetNetname(), "via", round(TO(p.x), 3), round(TO(p.y), 3)]
    a, b = t.GetStart(), t.GetEnd()
    return [t.GetNetname(), "track", round(TO(a.x), 3), round(TO(a.y), 3), round(TO(b.x), 3), round(TO(b.y), 3)]


def real_pour_check(D, ripped, new, recs):
    """rebuild the board with these routes in a scratch run (replay), fill, and run the pour check (D-023)."""
    D2 = dict(D, rip=sorted(set(D["rip"]) | ripped),
              routes=keep_routes(D["routes"], ripped) + keep_routes(new, ripped) + recs)
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(D2, f)
    env_ = dict(os.environ, HANDROUTE_DATA=f.name)
    subprocess.run([sys.executable, __file__, "replay"], env=env_, capture_output=True, check=True)
    r = subprocess.run([sys.executable, str(Path(__file__).with_name("pour.py")), str(PCB)], capture_output=True, text=True)
    os.unlink(f.name)
    line = [x for x in r.stdout.splitlines() if x.startswith("In2 3V3 pour")]
    return r.returncode == 0, (line[0] if line else r.stdout[-300:] + r.stderr[-300:])


def cmd_route(a):
    board = pcbnew.LoadBoard(str(PCB))
    D = load_data()
    data = D["routes"]
    if a.rip:   # rip up the base (Freerouting) copper of these nets; they are then routed here
        names = [str(k) for k in board.GetNetsByName().keys()]
        mk = manual_keys(D["routes"])
        for t in list(board.GetTracks()):
            if re.search(a.rip, t.GetNetname()) and tuple(item_key(t)) not in mk:
                board.Remove(t)
        D["rip"] = sorted(set(D["rip"]) | {n for n in names if re.search(a.rip, n)})
        # their earlier hand routes go too (manual entries stay): otherwise replay keeps the old copper and the
        # next route lands on top of it (shorts, co-located vias)
        n0 = len(D["routes"])
        D["routes"] = keep_routes(D["routes"], {r["net"] for r in D["routes"] if re.search(a.rip, r["net"])})
        print(f"dropped {n0 - len(D['routes'])} hand-route records")
    for spec in (a.rip_at or []):   # NET@x,y: rip the base tracks/vias of NET touching (x, y) (radius 0.3 mm)
        net, xy = spec.rsplit("@", 1)
        P = pcbnew.VECTOR2I(MM(float(xy.split(",")[0])), MM(float(xy.split(",")[1])))
        for t in list(board.GetTracks()):
            if t.GetNetname() == net and t.HitTest(P, MM(0.3)):
                D.setdefault("rip_items", []).append(item_key(t)); board.Remove(t)
    if a.rip or a.rip_at:   # save and stop: routing runs in a fresh process (pcbnew crashed on removed items)
        pcbnew.SaveBoard(str(PCB), board); DATA.write_text(json.dumps(D, indent=1)); print("ripped"); return 0
    unc, _ = drc_unconnected()
    order = a.order.split(",") if a.order else []
    unc.sort(key=lambda u: order.index(u[0]) if u[0] in order else len(order))
    env = Env(board, manual_keys(D["routes"]))
    new, ripped, failed, done = [], set(), [], 0
    pbase = env.pour_report() if a.in2 else None
    if pbase:
        print("pour (model) at start", pbase)
    rc = D.setdefault("ripcount", {})

    def attempt(net, src, dst, plane):
        if plane:   # a short direct link to the other item first (adjacent pins, pad to pad), else a plane via
            if dst is not None and not isinstance(dst, list):
                for w in (None, 0.15):
                    rec, err = route_one(env, net, src, dst, w=w)
                    if rec and sum(math.dist(t["a"], t["b"]) for t in rec["tracks"]) < 3.0 and not rec["vias"]:
                        return rec, err
            return route_one(env, net, src, None, plane=True)
        rec, err = None, None
        for w in ([None, 0.15] if env.cls.get(net) == "Power" else [None]) + ([NECK_W] if a.neck and env.cls.get(net) == "Default" else []):
            rec, err = route_one(env, net, src, dst, use_in2=a.in2, w=w)
            if rec:
                break
        return rec, err

    def soft_hits(net, src, dst, plane, locked):
        soft = {n for n in env.cls if n not in NO_RIP and n not in locked and rc.get(n, 0) < RIP_CAP}
        _, r = (route_one(env, net, src, None, plane=True, soft=soft) if plane else
                route_one(env, net, src, dst, use_in2=a.in2, w=0.15 if env.cls.get(net) == "Power" else None, soft=soft))
        return {k[0] for k in r[1]} if isinstance(r, tuple) else set()

    def route_conn(net, src, dst, plane, depth, tx, why):
        """route one connection in the model; on failure rip the nets in the way (whole nets) and re-route
        them, recursively to depth. tx: shared transaction state {"locked", "ripped", "budget"}.
        Returns the new records or None (the caller rolls the model back)."""
        rec, err = attempt(net, src, dst, plane)
        if rec:
            rec["why"] = why; env.add_rec(rec); return [rec]
        tx["err"] = f"{net}: {err}"
        if depth == 0 or tx["budget"] <= 0:
            return None
        tx["budget"] -= 1
        H = soft_hits(net, src, dst, plane, tx["locked"])
        npads = sum(1 for fp in board.Footprints() for p in fp.Pads() if p.GetNetname() in H)
        if not H or len(H) > a.max_nets or npads > a.max_pads:
            tx["err"] = f"{net}: {err}" + (f"; rip-up would need {sorted(H)} ({npads} pads)" if H else "")
            return None
        tx["locked"] |= H; tx["ripped"] |= H
        env.remove_nets(H)
        rec, err = attempt(net, src, dst, plane)
        if not rec:
            tx["err"] = f"{net}: {err} after rip-up of {sorted(H)}"; return None
        rec["why"] = why + f" (rip-up {sorted(H)})"; env.add_rec(rec); recs = [rec]
        for h in sorted(H):
            rr = reroute_net(h, depth - 1, tx)
            if rr is None:
                return None
            recs += rr
        return recs

    def reroute_net(h, depth, tx):
        """route all pads of net h as a growing tree (nearest pad first) in the model."""
        pads = [p for fp in board.Footprints() for p in fp.Pads() if p.GetNetname() == h]
        if len(pads) < 2:
            return []
        pos = lambda p: (TO(p.GetPosition().x), TO(p.GetPosition().y))
        tree, rest, recs = [pads[0]], pads[1:], []
        tpos = [pos(pads[0])]
        while rest:
            q = min(rest, key=lambda p: min(math.dist(pos(p), t) for t in tpos))
            rest.remove(q)
            rr = route_conn(h, q, list(tree), False, depth, tx, f"reroute {h} (rip-up)")
            if rr is None:
                return None
            recs += rr
            for rec in rr:
                if rec["net"] == h:
                    tree += env.rec_items(rec)
            tree.append(q); tpos.append(pos(q))
        return recs

    for net, (da, pa), (db, pb) in unc:
        if net in ripped or (a.nets and not re.search(a.nets, net)):
            continue
        src, dst = find_item(board, da, pa), find_item(board, db, pb)
        if src is None or dst is None:
            failed.append((net, "item not found")); continue
        it_a, it_b = src, dst
        plane = net in PLANE and not a.no_plane
        if plane:   # pad without a via: route from the pad side (the pad), drop a via
            src = src if isinstance(src, pcbnew.PAD) else dst
            if isinstance(src, pcbnew.PAD) and src.HasHole():
                src = dst
            dst = it_b if src is it_a else it_a
        snap = env.snapshot()
        tx = {"locked": {net}, "ripped": set(), "budget": a.budget, "err": ""}
        recs = route_conn(net, src, dst, plane, a.depth if a.ripup else 0, tx, f"{da} -> {db}")
        if recs is None:
            env.restore(snap)
            failed.append((net, tx["err"], da, db)); print("FAIL", net, "|", tx["err"]); continue
        if a.in2 and (any(t["layer"] == "In2.Cu" for r_ in recs for t in r_["tracks"]) or any(r_["vias"] for r_ in recs)):
            ok, pr = env.pour_ok(pbase)
            if pr["pieces"] == 1:   # the model is conservative: decide on the real zone fill of a trial rebuild
                ok, pr = real_pour_check(D, ripped | tx["ripped"], new, recs)
            if not ok:
                env.restore(snap)
                failed.append((net, f"pour {pr}", da, db)); print("FAIL", net, "| rolled back: In2 pour", pr); continue
            print("   pour", pr)
        R = tx["ripped"]
        ripped |= R
        new = keep_routes(new, R) + recs
        for h in R:
            rc[h] = rc.get(h, 0) + 1
        done += 1
        L = sum(math.dist(t["a"], t["b"]) for t in recs[0]["tracks"])
        print(f"OK {net}: {L:.2f} mm" + (f", rip-up {sorted(R)} ({len(recs) - 1} re-routes)" if R else ""))
        # checkpoint: an interrupted run keeps what it routed (replay rebuilds the board from the data)
        D2 = dict(D, rip=sorted(set(D["rip"]) | ripped), routes=keep_routes(D["routes"], ripped) + new)
        DATA.write_text(json.dumps(D2, indent=1))
    # the board here still holds ripped copper; the next replay builds it from the data
    D["rip"] = sorted(set(D["rip"]) | ripped)
    D["routes"] = keep_routes(D["routes"], ripped) + new
    DATA.write_text(json.dumps(D, indent=1))
    print(f"routed {done}, failed {len(failed)}, ripped nets {sorted(ripped)}")
    return 0


def cmd_clean(a):
    """drop dangling vias (DRC via_dangling): base vias go to rip_items, hand-route vias are removed from their
    record. The next replay rebuilds the board without them."""
    _, d = drc_unconnected()
    D = load_data()
    n = 0
    for v in d.get("violations", []):
        if v["type"] == "track_dangling":
            it = v["items"][0]
            net = re.search(r"\[(.*?)\]", it["description"]).group(1)
            ln = float(re.search(r"length ([0-9.]+)", it["description"]).group(1))
            P = (it["pos"]["x"], it["pos"]["y"])
            ends = lambda t: (math.dist(t["a"], P) < 0.01 or math.dist(t["b"], P) < 0.01) and abs(math.dist(t["a"], t["b"]) - ln) < 0.01
            hit = False
            for r in D["routes"]:
                if r["net"] == net and any(ends(t) for t in r["tracks"]):
                    r["tracks"] = [t for t in r["tracks"] if not ends(t)]; hit = True
            if not hit:
                for t in json.loads(BASE.read_text()):
                    if "via" not in t and t["net"] == net and ends(t):
                        D.setdefault("rip_items", []).append([net, "track", round(t["a"][0], 3), round(t["a"][1], 3),
                                                              round(t["b"][0], 3), round(t["b"][1], 3)]); hit = True
            print(("dropped track" if hit else "NOT FOUND track"), net, P); n += hit
            continue
        if v["type"] != "via_dangling":
            continue
        it = v["items"][0]
        net = re.search(r"\[(.*?)\]", it["description"]).group(1)
        x, y = it["pos"]["x"], it["pos"]["y"]
        hit = False
        for r in D["routes"]:
            if r["net"] == net:
                k = [q for q in r["vias"] if math.dist(q, (x, y)) < 0.01]
                if k:
                    r["vias"] = [q for q in r["vias"] if q not in k]; hit = True
        if not hit:
            for b in json.loads(BASE.read_text()):
                if "via" in b and b["net"] == net and math.dist(b["via"], (x, y)) < 0.01:
                    D.setdefault("rip_items", []).append([net, "via", round(b["via"][0], 3), round(b["via"][1], 3)]); hit = True
        print(("dropped" if hit else "NOT FOUND"), net, x, y); n += hit
    DATA.write_text(json.dumps(D, indent=1))
    print(f"cleaned {n} dangling vias")
    return 0


def cmd_manual(a):
    board = pcbnew.LoadBoard(str(PCB))
    D = load_data()
    env = Env(board)
    for name in a.names:
        for net, w, runs in MANUAL[name]:
            segs, vias = [], []
            for i, (ly, pts) in enumerate(runs):
                segs += [(LID[ly], p, q) for p, q in zip(pts, pts[1:])]
                if i + 1 < len(runs):
                    vias.append(pts[-1])
            err = validate(env, net, w, segs, vias)
            if err:
                print("FAIL", name, net, err); return 1
            rec = {"net": net, "w": w, "why": f"manual {name}",
                   "tracks": [{"layer": LNAME[l], "a": list(p), "b": list(q), "w": w} for l, p, q in segs],
                   "vias": [list(v) for v in vias]}
            apply(board, rec); D["routes"].append(rec); env.refresh()
            print(f"OK {name}: {sum(math.dist(p, q) for _, p, q in segs):.2f} mm")
    board.BuildConnectivity()
    pcbnew.ZONE_FILLER(board).Fill(board.Zones())
    pcbnew.SaveBoard(str(PCB), board)
    DATA.write_text(json.dumps(D, indent=1))
    return 0


def cmd_freeze(a):
    board = pcbnew.LoadBoard(str(PCB))
    out = []
    for t in board.GetTracks():
        p = t.GetPosition()
        if t.Type() == pcbnew.PCB_VIA_T:
            out.append({"via": [TO(p.x), TO(p.y)], "net": t.GetNetname(), "d": TO(t.GetWidth(pcbnew.F_Cu)), "h": TO(t.GetDrillValue())})
        else:
            s, e = t.GetStart(), t.GetEnd()
            out.append({"layer": LNAME.get(t.GetLayer(), t.GetLayerName()), "a": [TO(s.x), TO(s.y)], "b": [TO(e.x), TO(e.y)],
                        "w": TO(t.GetWidth()), "net": t.GetNetname()})
    BASE.write_text(json.dumps(out, indent=0))
    print("froze", len(out), "items")
    return 0


def finish(board):
    """D-022 finishing: solid zone connection for the pads with starved thermal spokes."""
    for ref, pads in SOLID_PADS.items():
        fp = board.FindFootprintByReference(ref)
        for p in fp.Pads():
            if p.GetNetname() in PLANE and (pads is None or p.GetNumber() in pads) and p.HasHole():
                p.SetLocalZoneConnection(pcbnew.ZONE_CONNECTION_FULL)
    for ref, pads in SOLID_SMD.items():
        for p in board.FindFootprintByReference(ref).Pads():
            if p.GetNumber() in pads:
                p.SetLocalZoneConnection(pcbnew.ZONE_CONNECTION_FULL)


def cmd_replay(a):
    import subprocess
    # fresh board from the generator (removing tracks in-process crashes the pcbnew bindings)
    subprocess.run([sys.executable, str(HW / "gen" / "pcb" / "build_pcb.py")], check=True, capture_output=True)
    board = pcbnew.LoadBoard(str(PCB))
    D = load_data()
    for it in json.loads(BASE.read_text()):
        if it["net"] in D["rip"]:
            continue
        key = ([it["net"], "via", round(it["via"][0], 3), round(it["via"][1], 3)] if "via" in it else
               [it["net"], "track", round(it["a"][0], 3), round(it["a"][1], 3), round(it["b"][0], 3), round(it["b"][1], 3)])
        if key in D.get("rip_items", []):
            continue
        net = board.FindNet(it["net"])
        if "via" in it:
            v = pcbnew.PCB_VIA(board); v.SetPosition(pcbnew.VECTOR2I(MM(it["via"][0]), MM(it["via"][1])))
            v.SetWidth(MM(it["d"])); v.SetDrill(MM(it["h"])); v.SetNet(net); v.SetLayerPair(pcbnew.F_Cu, pcbnew.B_Cu)
            board.Add(v)
        else:
            FO.add_track(board, net, tuple(it["a"]), tuple(it["b"]), LID[it["layer"]], it["w"])
    for rec in D["routes"]:
        apply(board, rec)
    finish(board)
    board.BuildConnectivity()
    pcbnew.ZONE_FILLER(board).Fill(board.Zones())
    pcbnew.SaveBoard(str(PCB), board)
    print("replayed")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["route", "freeze", "replay", "finish", "manual", "clean"])
    ap.add_argument("names", nargs="*", help="manual: MANUAL entries to apply")
    ap.add_argument("--nets")
    ap.add_argument("--in2", action="store_true")
    ap.add_argument("--ripup", action="store_true", help="on failure, find the nets in the way and rip them")
    ap.add_argument("--neck", action="store_true", help="allow a 0.1 mm neck-down (dru minimum) for Default nets")
    ap.add_argument("--in2-long", action="store_true", help="D-023: In2 runs of any length (pour checked per net)")
    ap.add_argument("--in2-cost", type=float, default=None, help="cost multiplier of an In2 step")
    ap.add_argument("--depth", type=int, default=2, help="rip-up recursion depth")
    ap.add_argument("--max-nets", type=int, default=4, help="rip-up: most nets ripped for one connection")
    ap.add_argument("--max-pads", type=int, default=20, help="rip-up: most pads of the ripped nets")
    ap.add_argument("--budget", type=int, default=12, help="rip-up searches per transaction")
    ap.add_argument("--no-plane", action="store_true")
    ap.add_argument("--rip", help="regex: rip up these nets' existing copper first (recorded, replay skips it)")
    ap.add_argument("--rip-at", action="append", help="NET@x,y: rip the base copper of NET at that point")
    ap.add_argument("--order", help="comma list of nets to route first, in this order")
    a = ap.parse_args()
    global IN2_MAX, IN2_COST
    if a.in2_long:
        IN2_MAX, a.in2 = 1e9, True
    if a.in2_cost:
        IN2_COST = a.in2_cost
    if a.cmd == "finish":
        b = pcbnew.LoadBoard(str(PCB)); finish(b); pcbnew.ZONE_FILLER(b).Fill(b.Zones()); pcbnew.SaveBoard(str(PCB), b)
        return 0
    return {"route": cmd_route, "freeze": cmd_freeze, "replay": cmd_replay, "manual": cmd_manual, "clean": cmd_clean}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
