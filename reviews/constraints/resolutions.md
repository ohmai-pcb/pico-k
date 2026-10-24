---
accepted_changes:
- files_hash: sha256:5deef3c946f0d15514e5c0ecb862d1eca087832be882dcc65abd5b7370d39dd9
  by: owner
  reason: Post-review nits N1-N3 applied in f25334f and review.status set to reviewed
    on all 13 YAML files per D-011
---
# Resolutions: phase `constraints` review findings

Resolution: `fixed` (Ref = commit hash), `accepted` (By = owner, Reason required), `answered` (questions),
`pending` (By = owner: an owner decision, not decided by the author), or `fixed-post-review` (Ref = commit:
a fix the reviewer asked for in their own [nit] issue, applied after the review; the files it touches may differ
from the reviewed hash without a re-verification).
Re-verification: Reviewer-A, HEAD cdf79d7, files_hash 41d65780..., pass with nits (R1 nit, R2 housekeeping).
Review: `reviews/constraints/reviewer-a.md` (= `docs/review-constraints-reviewer-a.md`), Reviewer-A, 2026-10-15, files_hash 964bd47e....
Every fix was checked against the cited page before it was applied (author, 2026-10-15). The fixes change the
files in scope, so Reviewer-A must re-verify against the new brief (`ohmai review start constraints`).

| ID | Reviewer | Resolution | Ref | By | Reason |
|----|----------|------------|-----|----|--------|
| F2 | Reviewer-A | fixed | 054096c | author | Verified: sentence on RP2350 printed p.556 (PDF 557); cite changed to p.556, HDG p.14 added |
| F3 | Reviewer-A | fixed | 054096c | author | Verified Abracon p.2 gives no function; pin names now "2 (NC/GND)", "4 (NC/GND)" |
| F5 | Reviewer-A | fixed | 054096c | author | Verified DS31783 p.2: ID 0.45 A at TA 85 °C added. Pin numbering stays an open question until the footprint check (agreed) |
| F7 | Reviewer-A | fixed | 054096c | author | Verified Pico 2 datasheet p.20 Fig. 11: GPIO25 → R3 470R 1 % → D2 Green; cite moved to Pico 2, VF-below-5 mA remark added |
| F9 | Reviewer-A | fixed | 054096c | author | Verified p.3/p.4: CM 0.5–1.4 V, VBIAS 0.735 V, RBIAS 2 kΩ, OV rising VAVDD−0.1/+0.17/+0.35 V, UV falling −0.3/−0.17/0 V (hyst 0.09 V), Note 8 (T+, T−, BIAS); conversions suspended on OVUV (p.26). VPOR added (F11) |
| F10 | Reviewer-A | fixed | 054096c | author | Verified Fig. 8 p.27 (rendered): BIAS joins T− on the connector side of the T− 100 Ω; caps on the pin side. Recorded in layout note and pin 2. 2 kΩ series option recorded from p.27 "Input Protection" (Reviewer-A cited Fig. 9 p.28; the 2 kΩ text is on p.27) |
| F11 | Reviewer-A | fixed | 054096c | author | Verified: CPHA = 1 (p.15 Table 3 note), SDO high-Z (p.15), VPOR 2.7/2.85 V (p.3), Table 4 mode 01 for RS < 5 kΩ (p.14), "increase the T− resistor by the cable resistance" (p.28). Operating temperature kept under recommended; cite now says it sits in the Abs Max block of p.2 |
| F12 | Reviewer-A | accepted | | owner | Decided D-009 (P5-9): no pull-up fitted, DNF R23/R24 at the test pads, drive type confirmed on rev-A (c30a105) |
| F15 | Reviewer-A | fixed | 054096c | author | Verified RP2350 p.456 Fig. 25: current in at "+", indicator at "−". Added layout note: in the buck, DC current flows VREG_LX → L → VOUT, so the AOTA indicator is at the VOUT/DVDD end; rev-A builds defined as "MPS dot at VREG_LX" / "MPS dot at VOUT". The Fig. 23 placement itself was not re-measured |
| F16 | Reviewer-A | fixed | 054096c | author | Verified: top-layer copper rule printed p.454 (PDF 455); layer-2 rule and Fig. 24 p.455 |
| F17 | Reviewer-A | accepted | | owner | Decided D-009 (P5-13, amends D-007): documented rev-A deviation, AOTA reference, both orientations, DNF external 1.1 V fallback (c30a105) |
| F19 | Reviewer-A | accepted | | owner | Decided D-009 (P5-12): polarity defined from the Omega p.2 drawing; magnet + warm-tip checks as bring-up sanity tests (c30a105) |
| F20 | Reviewer-A | fixed | 054096c | author | Verified p.1 Model No.: mpn now PCC-SMD-20 (strip, matches bom.csv price basis); -500/-1000 listed |
| F22 | Reviewer-A | fixed | 054096c | author | Verified: C_FILT GND rule printed p.455; switching loops p.454, "2 adjacent vias" p.455 |
| F23 | Reviewer-A | fixed | 054096c | author | Verified IIOVDD_MAX / IQSPI_IOVDD_MAX on printed p.1340; C_OUT (pin 50) now to VREG_PGND, as C_IN (Fig. 22 p.453) |
| F24 | Reviewer-A | accepted | | owner | Decided D-009 (P5-11): C27 = 4.7 µF as both RPi schematics (c30a105) |
| F25 | Reviewer-A | accepted | | owner | Decided D-008 (P5-10): C29 added in parallel with C16 (b169d78) |
| F27 | Reviewer-A | fixed | 054096c | author | Verified p.5 start-up VIN 1.9–5.5 V added; RθJA 46.8 (p.4) vs 48.7 °C/W (p.16) recorded as datasheet inconsistency. EP = 11 stays a footprint check |
| F28 | Reviewer-A | accepted | | owner | Decided D-008 (P5-10) + D-009: C31 added (3 × 10 µF Cout); Cin = one C20 1206 10 µF 50 V (b169d78, c30a105) |
| F30 | Reviewer-A | fixed | 054096c | author | Verified drawing p.1 PART NO table (force, height, keystake in that order: B = 160 gf, A = 1.5 mm, B = brass) and LCSC C318884 (1.6 N, 1.5 mm). Height changed to 1.5 mm. Disagree only with "suffix order not stated": the PART NO table order supports it |
| F32 | Reviewer-A | fixed | 054096c | author | Verified drawing note 4-2: SHIELD 50 mΩ max added. Alternate TYPE-C-31-M-12 signal list still unchecked (image-only drawing): stays a phase 7 symbol check |
| F35 | Reviewer-A | fixed | 054096c | author | Verified p.77: floating or GND allowed. Pin 9 now passive without nc; GND-vs-float stays an open schematic choice |
| F36 | Reviewer-A | fixed | 054096c | author | Verified: R6 rule already decided (D-006, bom U2/R6) → marked resolved. W25Q32RV "JQ" ships QE = 1 (p.15); GD25Q32E ships SR 00H exc. DRV0 (§8.2, PDF p.37) → QE = 0, HOLD# active (p.9). Refinement: RP2350 boot ROM uses 03h serial reads (printed p.369), so quad mode is set by the program, which must set QE on the GD part; noted for firmware/bring-up |
| F1 | Reviewer-A | answered | | author | OK, no action |
| F4 | Reviewer-A | answered | | author | OK, no action |
| F6 | Reviewer-A | answered | | author | OK, no action |
| F8 | Reviewer-A | answered | | author | OK, no action |
| F13 | Reviewer-A | answered | | author | OK; side note on bom D1 Vf fixed in 054096c (0.340 V max @ 1 A 25 °C, 0.300 V at 85 °C, onsemi p.2) |
| F14 | Reviewer-A | answered | | author | OK, no action |
| F18 | Reviewer-A | answered | | author | OK, no action |
| F21 | Reviewer-A | answered | | author | OK, no action |
| F26 | Reviewer-A | answered | | author | OK, no action |
| F29 | Reviewer-A | answered | | author | OK; storage-temperature quirk noted in TS-1187A yaml (054096c) |
| F31 | Reviewer-A | answered | | author | OK, no action |
| F33 | Reviewer-A | answered | | author | OK, no action |
| F34 | Reviewer-A | answered | | author | OK; bom U2 HDG page corrected p.8 → p.10 §3.1 (054096c) |

Out-of-table notes from the review, also handled: USB 2.0 spec (VBUS ≤ 10 µF, §7.2.4.1) is not in datasheets/ (open, not
fetched); UMW USBLC6-2SC6 datasheet not saved (already flagged); footprint pin numbering (DMG1012T, TPS63001 EP, W25Q32 EP,
TS-1187A A–D, USB-C A/B) is a phase 6/7 footprint check.

## Re-verification (Reviewer-A, HEAD cdf79d7): R findings

| ID | Reviewer | Resolution | Ref | By | Reason |
|----|----------|------------|-----|----|--------|
| R1 | Reviewer-A | fixed-post-review | 73f5c13 | author | Reviewer-requested nit: W25Q32RVXHJQ.yaml QE note cite "§5.x" → "§5.2 Processor-controlled boot sequence, printed p.369" (heading verified on RP2350 p.369). Only that string changed |
| R2 | Reviewer-A | fixed | 73f5c13 | author | Housekeeping outside scope (STATUS.md, not a reviewed file): P5-9 trimmed to MAX31856 DRDY/FAULT; PCC-SMD polarity is P5-12, flash CS 10 kΩ resolved by D-006. No owner item decided |

## Re-verification 2 (Reviewer-A, HEAD 25924e5, files_hash c9a92462...bfd1): pass with nits

| ID | Reviewer | Resolution | Ref | By | Reason |
|----|----------|------------|-----|----|--------|
| N1 | Reviewer-A | accepted | D-011 | owner | Reviewer-requested nit: PCC-SMD.yaml FRONT PANEL DESIGN view reworded (plan view, 1.57 = panel thickness, label rotated 180°); polarity conclusion unchanged |
| N2 | Reviewer-A | accepted | D-011 | owner | Reviewer-requested nit: RP2350A.yaml C29 placement rule next to C16, shared GND vias (Fig. 23 p.454, §6.3.8.1 p.455) |
| N3 | Reviewer-A | accepted | D-011 | owner | Reviewer-requested nit: TPS63001DRCR.yaml Cout ≈ 14.2–15.3 µF at −20 % and 85 °C stated (informational) |

Housekeeping (outside the gate scope): H1 not reproduced (STATUS.md has one D-009 row at 25924e5 and now);
H2 done above (F12/F17/F19/F24/F25/F28 → accepted, owner decisions D-008/D-009); H3 fixed in ohmai (brief
"Changed since" list vs the reviewed brief, duplicate name-only author entry) and the brief regenerated.
After the review, review.status was set to `reviewed` on all 13 files (a12a64d, owner instruction, D-011); that
is a review-metadata-only change.

