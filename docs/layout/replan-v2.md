# Replan v2: U1 (RP2350) and TPS63001 (U3) area, with board size options

Status: **DOC ONLY**, written 2026-10-23 (Europe/Stockholm). The board is unchanged: pcb sha256 starts 2d0f674a54a7, and the
probes ran on temporary copies that were restored afterwards. Coordinates are placement.yaml (board origin); KiCad = yaml + 100.
Sources used: public datasheets in `datasheets/` (SLVS520C TPS63001, RP2350, Pico 2, Hardware design with RP2350, MAX31856,
KT-0805G) and pico-k content only.

Plots:
- `docs/layout/replan-v2-current.png`: the current 51 × 21 board, courtyards (grey = J4 castellation strips, red = U3 block).
- `docs/layout/replan-v2-54mm.png`: probe e3, a 54 × 21 board with a +3 mm band at y ≈ 12.2 and a Fig.-20 U3 block. Fit ALL OK, DRC shows 2 silk nits.

## 1. Why tonight's local fixes failed (root cause)

1. **No free area. Every band of the board is close to full.** Courtyard area divided by usable area (x 2.655–18.345, inside the J4 courtyard strips):
   - USB band (y 0–17): 215 / 267 mm², **81 %**.
   - MCU band (y 17–33): 183 / 251 mm², **73 %**.
   - TC band (y 33–51): 270 / 282 mm², **95 %**.

   With 0.1 mm pad gaps and courtyard rules, that leaves only slivers.
2. **A central spine splits the board into two thin channels.** J1, U4, R1/R2, U1, U5 and the clips form a spine about 8 mm wide around x 10.5. The side channels are only about 5.8–7.1 mm wide. A TPS63001 block laid out per SLVS520C Fig. 20 (C20 at VIN, C21 at VOUT, L2 straddling LX1/LX2) needs at least 8.6 mm across and about 8 mm of height. Above L1 (VREG inductor, top edge y ≈ 12.4) there is only about 5.2 mm (y 7.2–12.4), up to the J1 pads and shield.
3. **The U1 east column is also full.** SW1 (7.55 × 7.42), C18/C27 and the JP/NT1 group sit between U1 and the J4 east strip. VREG_AVDD/ADC_AVDD caps cannot move nearer pins 44/46 without displacing these parts (Reviewer-A L4/L5).
4. **The J4 castellations set hard limits.** The castellation pads sit at x 1.61 / 19.39 on a 2.54 mm pitch, and the courtyard strip begins at x 18.345. Nothing can use the edge strips, and the width cannot grow without breaking the Pico footprint. On the east side, pins 35–40 (ADC_VREF … VBUS, y 1.37–14.07) put VSYS/3V3/GND pads right next to the U3 area. In one probe, C20 shorted to J4.35–37.
5. **Moving one part only moved the conflict.** Every local move lost to a neighbour:
   - C20 to the south: J4.
   - L2 to the south: L1 pads.
   - Extra VIN cap: no 0603 spot within 2.5 mm of U3.5. The only 0402 spot is inside the J4 strip.
   - Rerouting at the old spots: failed (corridors blocked by the 3V3 pour necks and the VREG keepout).

Evidence:
- `.toolcache/d029b/reroute-fail_2026-10-23_2205/`
- `.toolcache/d029b/fallback-c20_2026-10-23_2207/`
- `.toolcache/d029c/group-fit_2026-10-23_2214/SUMMARY.md`
- `.toolcache/d029c/group-route-fail_2026-10-23_2220/`
- D-029 in `docs/decisions.md`
- Size probes: `.toolcache/rv2/probes/{e0,e2,e35b,e3}.log`, plus `.kicad_pcb` copies for e35b and e3.

## 2. Placement-first plan (addresses L1–L13 by design)

Order: fixed parts first, then the SMPS block, VREG, U1 decoupling, USB, then the MAX31856. Run `ohmai layout fit` after each step, using `--ignore-courtyard J4 --pad-gap 0.1`, and ignore refs that are not placed yet.

| Finding | Design rule in the replan | Verified spot (probe e3, 54 mm, yaml) |
|---|---|---|
| L1 blocker: C20 far from VIN | SLVS520C Fig. 20: C20 right at VIN/PGND (U3.5/U3.3), same layer, no vias | U3 (12.6, 9.6) r90; C20 (15.7, 11.9) r90. Centre distance C20.1–U3.5 3.17, C20.2–U3.3 3.15 (was a long route) |
| L6: switch node and VOUT loop | L2 straddles LX1/LX2 with short, wide (≥ 0.5 mm) F.Cu pours. C21 at VOUT/PGND with no vias. C15 at VINA | L2 (12.6, 13.3) r180, L2.1–U3.4 2.39, L2.2–U3.2 2.39. C21 (9.6, 12.4) r90, C21.1–U3.1 2.95. C15 (15.6, 8.6), C15.1–U3.8 2.55 |
| L13 + SLVS520C Fig. 20: FB/PS away from LX | In1 cut-out under L2 + LX pours (new keepout) and under L1. FB (U3.10 → 3V3) leaves on the north side, away from LX. SMPS_PS leaves north/west, never inside a cut-out | U3 pins 6–10 face north (y ≈ 8.2). LX is on the south side |
| L2: NT1 at the far end of PGND | NT1 and C29 per RP2350 Fig. 23 / §6.3: NT1 at VREG_PGND (U1.47) under C16/C17, no via in series. C29 parallel to C16 at VREG_VIN | Unchanged VREG cell (C16/C17/L1 per L20). Move NT1 onto the C16.2 pad side |
| L3: In1 cut-out stops at L1 | Extend the cut-out over the VREG_LX trace. Route VREG_FB on F.Cu from C17 (D-021), not under LX | Keepout x 10.7–14.3 widened to cover the LX trace |
| L4: VREG_AVDD long after the filter | R5/C18 move to pin 46. Filtered node ≤ 2 mm, same layer | The +3 mm band frees the U1 north edge (U4/USB move west) |
| L5: ADC_AVDD/C27 far | C27 ≤ 1.5 mm from U1.44, F.Cu, no via. See Q3 | Same; current C27.1–U1.44 is 4.57 (centre). Target ≤ 1.5 |
| L7/L9/L10: USB pair | J1 → U4 → R1/R2 → U1 all on F.Cu over In1 GND. Keep ≥ 2 mm from the SMPS block. R1/R2 (27R) within 2 mm of U1.51/52 (HDG "close to the chip") | U4 (5.6, 10.0) west of U3. The pair runs down the west channel. R1/R2 move to the U1 north-west corner |
| L8/L12: MAX31856 bypass | C12/C13 ≤ 1 mm from U5.5/U5.8, own GND via. C14 across the pins | Re-place the TC band after the shift (it moves +3 mm as a block) |
| L11: crystal | Keep (Reviewer-A: OK). Reroute XIN on F.Cu if the corridor frees | — |

**Exit corridors** (reserve these before routing; each ≥ 0.6 mm wide, or ≥ 1.0 mm for power):
- VSYS: J4.39 → C20 → U3.5, east side, F.Cu.
- 3V3 out: C21 → In2 pour via a ≥ 0.7 mm neck west of U3 (pour rule: In2 3V3 in one piece).
- PGND: U3 EP vias (5 × 0.3, SLVS520C land pattern) straight into In1 GND outside the LX cut-out.
- SMPS_EN/PS: U3 north edge → west, kept out of the cut-outs.
- USB_DP/DM: west channel, F.Cu, x ≈ 4–8.
- VREG_FB: C17 → JP5 on F.Cu.
- ADC_AVDD/VREG_AVDD: U1 north-east edge.
- TC±: unchanged (south band, shifted).

**Pre-route checks** (run after each placement step; fail = stop and re-place):
1. `ohmai layout fit` ALL OK (standing rule).
2. Decoupling pad-edge distance: U3 C20/C21 ≤ 1.5 mm; U1 supply pins ≤ 1.0 mm (L14 values not worse); C27 ≤ 1.5; C12/C13 ≤ 1.0. Measure with `.toolcache/rv2/met.py`.
3. Corridor check: each corridor above is free of courtyards and pads (`ohmai layout fit` scan of a 0.6 mm dummy along the path, or a manual check in the plot).
4. Keepout check: no signal other than LX/VOUT inside the U3 and L1 In1 cut-outs (L3/L13).
5. Bare DRC after placement: 0 non-silk violations.

## 3. Board size options

The J4 castellations (2 × 20, 2.54 mm pitch, x 1.61 / 19.39) fix the **width at 21**. Adding width would move the castellations off the Pico grid or leave them inside the board. Length can only grow by adding a band. Probes put that band at y ≈ 12.2, between the USB entry and VREG/U1. Everything with y ≥ 12.2 moves south (J2/J3/TP7–12 included). J4 and TP1–TP6 stay put (TP6 stays). The 40 pads keep their Pico positions relative to pin 1, so the extra length sticks out past the pin 20/21 end.

| Option | What it buys | Verified? | Constraints / cost |
|---|---|---|---|
| **A. Keep 51 × 21** | Nothing new. Something must give: (a) keep the D-029 compromise (L1 open as a rev-A risk, with bring-up checks: VSYS ripple, U3 load step); or (b) BOM change: smaller L2 (≤ 3 × 3) / 0805 C20 (not allowed under the no-BOM-change rule, owner decision); or (c) remove SW1 and rely on the TP6 BOOTSEL pad (BOM change) | Probe e0: L2 does not fit (overlaps L1 by 3.40 × 2.16, shorts L1 pads) | Meets R-02. L1 blocker not fixed by layout |
| B. +2 mm (53 × 21) | Almost enough | Probe e2: **fails**. L2 overlaps L1 by 3.40 × 0.16 mm | Not recommended |
| **C. +3 mm (54 × 21)** | Full Fig.-20 U3 block; U4/USB move west; room at the U1 north edge for R5/C18/C27/R1/R2 (L4/L5/L10) | **Probe e3: fit ALL OK; bare DRC only 2 silk_overlap (R11/D1, U4/R11)**, `probes/e3.kicad_pcb` | Breaks R-02 (Pico outline, "no overhang", D-004 F1). Castellation pitch and pin order unchanged, but a carrier with a Pico-sized cut-out/socket outline gets a 3 mm overhang at the pin-20/21 end. Probe connector still on top, bottom still flat (R-07). EU marking unaffected |
| C'. +3.5 / +4 mm | +0.5–1 mm routing margin | e35b (54.5): same result as e3 | Same as C. Use +4 only if the routing step needs it |

**JLC cost (public pricing, checked 2026-10-23):** the jlcpcb.com quote page lists "4 L – $2 for 50×50mm PCBs" and $91/m² for batch production. The current 51 × 21 already exceeds 50 mm on one side, so 51 → 54 does not cross a new price tier. At batch rate the area grows 6 % (1071 → 1134 mm²), about +$0.006 per board at $91/m² (ESTIMATE; confirm in JLC's instant quote).

**Recommendation:** Option **C (54 × 21, +3 mm band at the USB end of U1)**, provided the owner amends R-02. It is the only verified way to fix L1 (blocker) and L4–L7/L10 by design. If R-02 must stay at 51 × 21, choose A(a): ship rev A with the documented compromise and bring-up checks, and record it as a known deviation from SLVS520C Fig. 20.

## 4. Effort and step order (for option C; ESTIMATE)

1. Owner: amend R-02 (decision entry) and answer Q1–Q3. About 0.5 h.
2. Update the outline in build_pcb.py (`H = 54`) and the band shift in placement.yaml; re-place the U3 block / U4 / USB per section 2. Run fit after each step. 1–2 h.
3. U1 east/north: R5/C18, C27 (+ 100 nF if Q3 = yes), R1/R2, NT1/C29, JP5/JP6 (per Q1). 1–2 h.
4. TC band re-check (C12/C13/C14). 0.5–1 h.
5. Keepouts / In1 cut-outs, pours (In2 3V3 in one piece, necks ≥ 0.7 mm near U1). 1 h.
6. Route: SMPS and VREG first, then USB, analog, the rest. DRC/ERC clean, `ohmai check footprints`. 4–6 h.
7. Re-review against the Reviewer-A findings (L1–L13 re-measured), plots, commit. 1–2 h.

Total: about 9–14 h of layout work, plus the owner decisions.

## Answers / recommendations for Reviewer-A Q1–Q3

- **Q1 (JP5/JP6 on B.Cu vs flat bottom, R-07):** Recommend moving JP5/JP6 to the **top** in the replan. R-07 asks for a flat bottom so the board can be soldered down by its castellations (requirements R-07). Cutting JP5 and bridging JP6 puts a solder bump there. With the +3 mm band, the U1 north-east area has room for two SolderJumper_2 next to C17, on F.Cu with VREG_FB from C_OUT (RP2350 §6.3 p.451, Fig. 21 p.452; D-013, D-021). D-021 would then be amended (owner). If the owner keeps them on B.Cu, record that the fallback bump is accepted only on a socketed or header build.
- **Q2 (who checks D2 orientation in the JLC preview):** The owner checks it at order time, since that is when JLC's DFM/placement preview is available. The agent prepares a checklist entry beforehand: "D2 green cathode mark on the west (pad 1 = K = GND), KT-0805G pad ① = + (KT-0805G p.2; D-012, D-014)". Add it to the order checklist next to the CPL file.
- **Q3 (100 nF on ADC_AVDD, BOM change):** RP2350 §6.1 p.442 asks for a 100 nF close to ADC_AVDD. Pico 2 Fig. 11 p.20 uses only the 4.7 µF (C13 on Pico 2), and the board copies that (D-009, C27). Recommendation: **add a 100 nF 0402 at U1.44** in the replan, with C27 kept. It costs one basic part and the replan area has room. It is a BOM change, so the owner decides, and no BOM change is made here.
