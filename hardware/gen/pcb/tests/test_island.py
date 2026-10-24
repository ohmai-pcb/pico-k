"""D-029 router start bug: a hand-drawn F.Cu track ending on a via must expose the via's B/In2 cells
as terminal cells. Run: $KT hardware/gen/pcb/tests/test_island.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import pcbnew  # noqa: E402
import handroute as HR  # noqa: E402

MM = pcbnew.FromMM


def board():
    b = pcbnew.BOARD()
    b.SetCopperLayerCount(4)
    n = pcbnew.NETINFO_ITEM(b, "/N"); b.Add(n)
    o = pcbnew.NETINFO_ITEM(b, "/O"); b.Add(o)
    t = pcbnew.PCB_TRACK(b); t.SetStart(pcbnew.VECTOR2I(MM(10), MM(10))); t.SetEnd(pcbnew.VECTOR2I(MM(11), MM(10)))
    t.SetWidth(MM(0.15)); t.SetLayer(pcbnew.F_Cu); t.SetNet(n); b.Add(t)
    v = pcbnew.PCB_VIA(b); v.SetPosition(pcbnew.VECTOR2I(MM(11), MM(10))); v.SetWidth(pcbnew.F_Cu, MM(0.45)); v.SetDrill(MM(0.2))
    v.SetLayerPair(pcbnew.F_Cu, pcbnew.B_Cu); v.SetNet(n); b.Add(v)
    far = pcbnew.PCB_VIA(b); far.SetPosition(pcbnew.VECTOR2I(MM(20), MM(10))); far.SetWidth(pcbnew.F_Cu, MM(0.45)); far.SetDrill(MM(0.2))
    far.SetLayerPair(pcbnew.F_Cu, pcbnew.B_Cu); far.SetNet(n); b.Add(far)
    other = pcbnew.PCB_VIA(b); other.SetPosition(pcbnew.VECTOR2I(MM(11), MM(10.2))); other.SetWidth(pcbnew.F_Cu, MM(0.45))
    other.SetDrill(MM(0.2)); other.SetLayerPair(pcbnew.F_Cu, pcbnew.B_Cu); other.SetNet(o); b.Add(other)
    return b, t, v, far, other


def test_track_island_includes_end_via_only():
    b, t, v, far, other = board()
    isl = HR.island(b, t)
    assert v in isl              # via at the track end is a terminal (on B.Cu / In2 too)
    assert far not in isl        # same net but not touching
    assert other not in isl      # touching but another net
    assert any(i.IsOnLayer(pcbnew.B_Cu) for i in isl)


if __name__ == "__main__":
    test_track_island_includes_end_via_only()
    print("ok")
