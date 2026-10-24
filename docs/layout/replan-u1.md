# U1 east-side placement replan, rev 2 (proposal, NOT executed)

Status: proposal only. It was written after the hop3 SMPS_PS retry with the fixed router (b51493c) still did not close: SMPS_PS routed, but GP28, DVDD and VSYS_SENSE diverged (best state was 9 unconnected; snapshot .toolcache/d029b/wip-hop3-fix_*). The tree is at b51493c. No placement in this doc has been applied.

## Problem
The U1 east pins (31–45) are at x=113.9–114.4 (KiCad mm). The decoupler/divider column (C5, R21, C10, C4, R20, and R8 in the rework) sits at x=116.34, with C18 and C27 at 117.84. That leaves about 1.4 mm of F.Cu between the U1 pad tips and the column's west pads. Every east-column net has to leave through that gap or through a via inside it: SMPS_PS (35), VBUS_SENSE (36), GP25–28 (37, 40–42), DVDD (39), VSYS_SENSE (43) and ADC_AVDD (44). The GP28 via at 114.85,123.73 takes the only via site. The rules allow no In2 except the two approved exceptions.

## Rev 2 (2026-10-23): the shift is +0.10 mm, and C18/C27 stay put
Rev 1 (below, kept for the record) used `fit --ignore J4`. That check dropped J4's pads as well as its courtyard, and its C18/C27 spots shorted J4.31 and J4.32. Rev 2 was checked with the fixed fit (OhmAI 4ec69a8: `--ignore-courtyard J4` keeps J4's pad copper, and pads of other nets within `--pad-gap` now block a spot). It was also checked with a real KiCad DRC on a temporary rebuilt board, and then the board was restored.

### Move
| Ref | role | now (KiCad) | rev 2 (KiCad) | placement.yaml |
|---|---|---|---|---|
| C5 | IOVDD 45 | 116.34,119.37 r0 | 116.44,119.37 r0 | [16.44,19.37] |
| R5 | VREG_AVDD filter | 116.34,120.39 r0 | 116.44,120.39 r0 | [16.44,20.39] |
| R21 | ADC filter | 116.34,121.41 r0 | 116.44,121.41 r0 | [16.44,21.41] |
| C10 | DVDD 39 | 116.34,122.43 r0 | 116.44,122.43 r0 | [16.44,22.43] |
| C4 | IOVDD 38 | 116.34,123.45 r0 | 116.44,123.45 r0 | [16.44,23.45] |
| R20 | VREF divider | 116.34,124.47 r0 | 116.44,124.47 r0 | [16.44,24.47] |
| C18 | AVDD | 117.84,120.41 r90 | **unchanged** | [17.84,20.41] |
| C27 | ADC_AVDD 44 | 117.84,123.47 r270 | **unchanged** | [17.84,23.47] |
| R8 | VBUS_SENSE (rework only) | not in the committed placement | 116.44,125.49 r0 | fit only, no DRC (see below) |

R9, R18, C6 and TP6 do not move. There are no BOM or pinout changes.

### Why +0.10 is the limit
- J4's real east courtyard starts at x=118.345. A C18/C27 courtyard is ±0.455 mm across at r90, so their centre must stay at x ≤ ~117.85. At 117.89, KiCad still flags `courtyards_overlap` with J4.
- The column's courtyards end at 117.245+shift, and C18/C27's begin at centre−0.455. A shift of ≥0.15 with C18/C27 at 117.84 overlaps the column. With s=0.25 at 117.94, the overlap is 0.02–0.04 mm on all 8 parts.
- **+0.5 and +0.75 are infeasible:** C18/C27 would have to sit at ≥118.2–118.45. That is inside J4's courtyard, and at 118.59 (rev 1) it shorts the castellated pads. The fit check found no other combination for those shifts.

### Verification (evidence in .toolcache/d029b/fitcheck_2026-10-23_2149/)
| Candidate | fit (`--ignore-courtyard J4`, pad gap 0.1 / 0.2) | KiCad DRC, bare rebuilt board |
|---|---|---|
| baseline (no move) | – | starved_thermal 4 (pre-existing), nothing else |
| **s=+0.10, C18/C27 117.84 (rev 2)** | all 8 fit | **starved_thermal 4 only: 0 shorts, 0 mask bridges, 0 clearance, 0 courtyard** (`drc_s010.json`, `s010.diff`) |
| s=+0.15, C18/C27 117.89 | all 8 fit | 0 shorts/bridges, but 2× courtyards_overlap C18/C27–J4 (`drc_s015.json`) |
| s=+0.25, C18/C27 118.04 | all 8 fit | 0 shorts/bridges, but 2× courtyards_overlap C18/C27–J4 (`drc_s025.json`); a possible alternative only if a J4 courtyard waiver is accepted |
| s=+0.5 / +0.75 with C18/C27 at 117.84–118.04 | 8 fail (courtyards vs column) | not built |

DRC: `kicad-cli pcb drc --severity-all`, unconnected ignored. The board was built by `build_pcb.py` from the edited placement.yaml, then `git checkout -- hardware` was run and the tree is clean. R8 is only in the uncommitted rework, so its spot has a fit check but no DRC.

### What changes vs rev 1 (the plan the owner saw)
- The shift drops from 0.75 to 0.10 mm. R5 now moves with the column (rev 1 left it behind).
- C18 and C27 stay where they are now; rev 1 moved them by +0.75.
- The U1-to-column gap only grows from about 1.4 to about 1.5 mm (rev 1: about 2.15 mm). **The rev 1 exit plan (two extra lanes plus a via site) is not delivered by rev 2.** The extra 0.1 mm does not open a 0.15/0.15 lane. Whether the east nets close needs a reroute attempt and cannot be assumed.
- Pad-edge distances to U1 pins (now → rev 2, with rev 1 in brackets):

| Pair | now | rev 2 | rev 1 |
|---|---|---|---|
| C5 – pin 45 (3V3) | 1.30 | 1.39 | (2.02) |
| C4 – pin 38 (3V3) | 1.23 | 1.33 | (1.98) |
| C10 – pin 39 (DVDD) | 1.23 | 1.33 | (1.98) |
| C27 – pin 44 (ADC_AVDD) | 3.76 | 3.76 | (4.41) |
| C18 – pin 46 (VREG_AVDD) | 4.18 | 4.18 | (4.92) |
| R5 – pin 46 | 3.18 | 3.28 | (3.18, not moved) |
| R21 – pin 44 | 2.26 | 2.36 | (3.01) |
| R20 – pin 38 | 1.60 | 1.68 | (2.22) |

Rev 2 costs the decouplers about 0.1 mm, against about 0.7 mm in rev 1.

### Plots (rebuilt, unrouted, window 112–122 × 117–127 mm)
- `replan-u1-current.png`: the current placement
- `replan-u1-proposed.png`: rev 2

## Rev 1 (superseded, invalid: shorts J4)
### Move (one rigid shift east by +0.75 mm)
Relative spacing inside the column does not change. All moves were checked jointly on a board rebuilt with every move applied, using `ohmai layout fit REF --ignore J4`. That is the same J4-courtyard convention as the existing placement checks; the J4 pads themselves were not ignored for the R9 attempt below.

| Ref | net role | now (KiCad) | proposed (KiCad) | placement.yaml | fit |
|---|---|---|---|---|---|
| C5 | IOVDD 45 | 116.34,119.37 r0 | 117.09,119.37 r0 | [17.09,19.37] | fits |
| R21 | ADC filter | 116.34,121.41 r0 | 117.09,121.41 r0 | [17.09,21.41] | fits |
| C10 | DVDD 39 | 116.34,122.43 r0 | 117.09,122.43 r0 | [17.09,22.43] | fits |
| C4 | IOVDD 38 | 116.34,123.45 r0 | 117.09,123.45 r0 | [17.09,23.45] | fits |
| R20 | VREF divider | 116.34,124.47 r0 | 117.09,124.47 r0 | [17.09,24.47] | fits |
| R8 | VBUS_SENSE low side | (rework) 116.34,125.49 | 117.09,125.49 r0 | [17.09,25.49] | fits |
| C18 | AVDD | 117.84,120.41 r90 | 118.59,120.41 r90 | [18.59,20.41] | fits |
| C27 | ADC_AVDD 44 | 117.84,123.47 r270 | 118.59,123.47 r270 | [18.59,23.47] | fits |
| R9 | VSYS_SENSE | 103.62,120.41 r0 | unchanged | — | fits |
| R18 | VBUS divider top | 105.5,110.65 r90 | unchanged | — | fits |

A +0.5 mm shift also fits for every part (checked individually). +0.75 is preferred because it opens two 0.15/0.15 lanes plus one via site. Rejected: moving R9 next to U1.43 (118.6,121.9). It overlaps C18 and C27 and the J4.32 pad, and the scan found no free spot within 3 mm.

### Planned exits (after the shift, gap ≈2.15 mm)
- **SMPS_PS (U1.35):** F stub east to a via at about 115.3,124.55, then B.Cu north along the new x≈115.6 lane to U3. The approved short In2 stub stays as a fallback only.
- **VBUS_SENSE (U1.36):** F east to R8.1 (117.09,125.49) in the lane under R20. The divider top R18 connects with the single approved In2 hop.
- **GP25/GP27/GP28 (37, 41, 42):** F fan-out east through lane 1 (x≈115.0) to vias at x≈115.6 (y 121.8 / 123.3 / 124.0). The current GP28 via at 114.85,123.73 moves to that column. Then B.Cu east under the column to J4.31–33.
- **GP26 (40):** F to R21 / J4.31 via lane 2.
- **DVDD (39):** short F stub to C10.1 at 116.6. It crosses the lane at the pad's own row, so it does not consume a lane. To C9 (D-027) on B through the via column.
- **VSYS_SENSE (43):** via at about 115.6,120.9, then B.Cu west under U1 (In1 GND solid, no In2) to R9.
- **ADC_AVDD (44)/C27, AVDD/C18:** F direct; 0.75 mm longer stubs.
- **Decouplers C4/C5/C10:** stub grows by 0.75 mm, to about 2.3 mm. The return goes to In1 GND through the existing GND via at each cap's .2 pad.
- **3V3_EN, VREG_LX/JP5:** unaffected; they exit on the north/U3 side.

Necks: the In2 3V3 pour is untouched, so the ≥0.7 mm neck near U1 is unchanged. Verify with pour.py after execution.

(Rev 1 plots were replaced by the rev 2 plots.)

### Errata (2026-10-23 21:5x, found while executing): C18/C27 spots are invalid
`ohmai layout fit --ignore J4` drops every J4 check, including J4's pad copper, not just its courtyard. I applied the plan exactly as written on a rebuilt board. With C18 and C27 at x=118.59, DRC reports `shorting_items` against the castellated pads: C27.2 GND shorts J4.31 (GP26), and C18.1 VREG_AVDD shorts J4.32 (GP27). There are also solder-mask bridges. `--rules` does not catch it either.

At x=117.84, C18/C27 overlap the shifted column (C5, R21, C10, C4). That leaves no spot east for them, so the +0.75 mm shift cannot be built as written. It was not executed; the snapshot is in .toolcache/d029b/wip-replan_*. Any shift needs a fit check that keeps J4 pads (copper) while ignoring only the J4 courtyard. The replan also leaves R5 (16.34,20.39) in the column unmoved.
