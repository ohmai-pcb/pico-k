"""D-029 rip-up bugs. Run: $KT hardware/gen/pcb/tests/test_ripup.py
1. A net ripped in-run was 're-routed' onto its own ripped copper: the pcbnew board still holds it, and
   island() reached it, so the route search ended at once and the saved data had no copper for it.
2. --rip kept manual records but removed their copper from the saved board; the rebuild brought it back.
   Manual copper now survives rip-ups in the model and in the data alike."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import pcbnew  # noqa: E402
import handroute as HR  # noqa: E402
from test_island import board  # noqa: E402


def test_island_skips_ripped_copper():
    b, t, v, far, other = board()
    alive = {tuple(HR.item_key(t))}                    # the via was ripped in the model, the board still has it
    isl = HR.island(b, t, alive)
    assert t in isl and v not in isl
    assert HR.island(b, v, alive) == []                # a ripped item is no terminal at all
    assert v in HR.island(b, t)                        # no model given: board copper as before


def test_manual_records_survive_rips():
    man = {"net": "/N", "why": "manual X", "w": 0.15, "tracks": [{"layer": "F.Cu", "a": [10, 10], "b": [11, 10], "w": 0.15}], "vias": [[11, 10]]}
    auto = {"net": "/N", "why": "a -> b", "w": 0.15, "tracks": [], "vias": [[20, 10]]}
    keep = {"net": "/O", "why": "a -> b", "w": 0.15, "tracks": [], "vias": []}
    assert HR.keep_routes([man, auto, keep], {"/N"}) == [man, keep]
    b, t, v, far, other = board()
    mk = HR.manual_keys([man])
    assert tuple(HR.item_key(t)) in mk and tuple(HR.item_key(v)) in mk and tuple(HR.item_key(far)) not in mk


if __name__ == "__main__":
    test_island_skips_ripped_copper()
    test_manual_records_survive_rips()
    print("ok")
