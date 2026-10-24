---
reviewer: Reviewer-A
kind: agent
vendor: Grok Bot
model: Grok Bot
instructions: Reviewer-A CTO/technical-advisor review brief from the owner (independent
  reviewer, no ohmai author skill)
independence: 3
independence_note: Same vendor and model as the author (OhmAI, Grok Bot). A different
  agent with different instructions (the Reviewer-A review brief, not the ohmai author
  skill), working in a separate session. Levels 1 and 2 were not available to this
  run. Level 3 meets the gate minimum.
files_hash: sha256:5deef3c946f0d15514e5c0ecb862d1eca087832be882dcc65abd5b7370d39dd9
date: 2026-10-15
---
# pico-k phase 5: constraints review (P5-1, Reviewer-A): re-verification 2 (D-008 … D-010)

**Reviewed:** branch `phase/constraints` at HEAD `25924e5` (2026-10-15). The local copy was already at that commit, so no fetch was needed. The working tree was clean; my previous `reviewer-a.md` had already been committed by the author in `f3020e2`.

**Hash check:**
- The sha256 values of all 13 files match the regenerated `reviews/constraints/BRIEF.md`; files_hash is `5deef3c9…9dd9`.
- All 13 files validate against `parts/constraints.schema.json` (jsonschema; this is not an `ohmai` run).

**What changed since re-verification 1 (`f3020e2..25924e5`):**
- RP2350A, TPS63001DRCR, MAX31856MUD+T, MPL-AT2512-3R3 and PCC-SMD (D-008 … D-010).
- W25Q32RVXHJQ (my nit R1).
- Seven files are byte-identical to the previous brief: ABM8, DMG1012T, KT-0805G, MBR120, TS-1187A, TYPE-C and USBLC6.

**How I checked:**
- I reviewed all five changed files, not only the one in the brief's "changed since" list.
- I compared the owner decisions with `docs/decisions.md` D-008 … D-010 and with `bom/bom.csv`.
- I re-read the technical values on the source pages.
- I made my own pixel reads of the Samsung curves. These are ESTIMATE values, good to about ±3 points.

I do not rule on the owner decisions themselves. I did not edit any input file and did not commit.

## Gate verdict: PASS WITH NITS

No blocker and no should-fix item. Every owner decision is recorded consistently in the five yaml files, bom.csv, decisions.md and STATUS.md, and the technical values check out against the datasheets. Earlier nits R1 and R2 are fixed. What remains is 3 nits in the reviewed files (N1–N3) and 3 housekeeping notes outside the gate scope (H1–H3).

| ID | File | Verdict | Finding | Cite |
|----|------|---------|---------|------|
| S1 | parts/constraints/RP2350A.yaml | OK | Recorded correctly: C29 parallel to C16 on VREG_VIN (D-008); ADC_AVDD cap 4.7 µF (D-009 P5-11); DNF external 1.1 V fallback (D-009 P5-13). Values check out (see S1 detail). | RP2350 p.451–452 §6.3.7 Fig. 21, p.455; Pico 2 datasheet p.20 Fig. 11 |
| N2 | parts/constraints/RP2350A.yaml | issue | [nit] C29 has no placement rule. Suggest: C16 stays in the Fig. 23 C_IN position; C29 goes right next to it on the same VREG_VIN / VREG_PGND island and shares its GND vias, without enlarging the switching loop or moving C_OUT/L_X. | RP2350 p.454 Fig. 23, p.455 §6.3.8.1 |
| S2 | parts/constraints/TPS63001DRCR.yaml | OK | Recorded correctly: C20 is one CL31A106KBHNNNE 10 µF 50 V X5R 1206; C21 + C22 + C31 are 3 × 10 µF; USB inrush is a documented deviation (D-010). Values and cites check out (see S2 detail). | SLVS520C p.9 §7.4.1, p.12; USB 2.0 p.177 §7.2.4.1; CL31A106KBHNNNE sheet |
| N3 | parts/constraints/TPS63001DRCR.yaml | issue | [nit] The C20 and C_IN worst cases include temperature, but the Cout worst case (≈ 14.9–16.1 µF at −20 % tolerance) does not. The CL10A106MA8NRNC TCC curve shows about −5 % at 85 °C, so Cout is ≈ 14.2–15.3 µF there. TI's 15 µF is a "recommended nominal" value with no upper limit, so this is informational only; state it for consistency. | SLVS520C p.12; Samsung CL10A106MA8NRNC TCC |
| S3 | parts/constraints/MAX31856MUD+T.yaml | OK | DRDY (pin 7) and FAULT (pin 13): DNF 10 kΩ pull-ups R23/R24 to 3V3, no wire-OR (D-009 P5-9). The net is within the pin abs max (−0.3 V to VDVDD + 0.3 V). Pin numbers and directions are unchanged and correct. | MAX31856 p.2, p.10 |
| S4 | parts/constraints/MPL-AT2512-3R3.yaml | OK | The documented rev-A deviation (reference AOTA-B201610S3R3-101-T), both orientations, and the DNF external 1.1 V fallback (D-009 P5-13, amends D-007) are recorded. The Fig. 21 description matches p.451–452. | RP2350 p.451–452; HDG p.6–7 |
| S5 | parts/constraints/PCC-SMD.yaml | OK | The polarity reading of Omega p.2 is correct. Looking at the board edge from outside with the component side up, + is the right clip (J2 → T+) and − the left clip (J3 → T−). This matches MAX31856 Table 1 (type K T+ Chromel, T− Alumel). | PCC-SMD p.2; MAX31856 p.12 |
| N1 | parts/constraints/PCC-SMD.yaml | issue | [nit] The polarity note describes the FRONT PANEL DESIGN view inaccurately; the conclusion is unaffected. The view is a plan view (seen from above), not a view from outside the edge. "1.57" is the PANEL THICKNESS of a front panel drawn edge-on, not the PCB below the clips. The OMEGA label there is rotated 180°, not mirrored. Suggest rewording. | PCC-SMD p.2 FRONT PANEL DESIGN view |
| S6 | parts/constraints/W25Q32RVXHJQ.yaml | OK | R1 fixed: the cite now reads "§5.2 Processor-controlled boot sequence, printed p.369". Verified. | RP2350 p.369 |
| S7 | parts/constraints/ABM8-272-T3.yaml | OK | unchanged since re-verification 1 (hash identical) | n/a |
| S8 | parts/constraints/DMG1012T-7.yaml | OK | unchanged (hash identical) | n/a |
| S9 | parts/constraints/KT-0805G.yaml | OK | unchanged (hash identical) | n/a |
| S10 | parts/constraints/MBR120VLSFT1G.yaml | OK | unchanged (hash identical) | n/a |
| S11 | parts/constraints/TS-1187A-B-A-B.yaml | OK | unchanged (hash identical) | n/a |
| S12 | parts/constraints/TYPE-C-16PIN-2MD-073.yaml | OK | unchanged (hash identical) | n/a |
| S13 | parts/constraints/USBLC6-2SC6.yaml | OK | unchanged (hash identical) | n/a |

## Detail for the five changed files

### S1 RP2350A.yaml

- **C_IN = C16 + C29, 2 × 4.7 µF CL10A475KO8NNNC.**
  - Typical: 6.4–6.6 µF at 3.3 V. My earlier read of the DC-bias curve (−30 %) gives 6.6 µF; the author's −32 % gives 6.4 µF.
  - Worst case: ≈ 5.1 µF, from −10 % tolerance × −12 % at 85 °C. I confirmed the −12 % at 85 °C on the Samsung TCC plot (about −12 % at 85 °C, about +2 % at −20 °C). 6.5 µF × 0.9 × 0.88 ≈ 5.1 µF, which is ≥ 4.7 µF (p.455 §6.3.8.2).
  - The arithmetic is correct. A placement rule is missing (N2).
- **ADC_AVDD cap 4.7 µF (C27).** I re-rendered Pico 2 datasheet Fig. 11 (p.20): 3V3 → R7 200R → ADC_VREF → R9 1R → node with C13 "4u7 M1005 6.3V X5R" to GND, which runs to RP2350 ADC_AVDD.
  - The yaml cite (p.20 Fig. 11, pin 44) and the topology statement are correct.
  - ≈ 3.25 µF at 3.3 V on 0603 16 V (ESTIMATE) is consistent with the earlier curve read.
  - bom.csv C27 has moved into the CL10A475KO8NNNC row.
- **External 1.1 V fallback.**
  - Fig. 21 is on p.452, in §6.3.7 "Application circuit". The supporting text is on p.451: "the inductor can be omitted and only a single input capacitor is required. Connect VREG_FB directly to ground", and VREG_AVDD/VREG_VIN must still be powered. The note is correct.
  - Phase 6 note: the DNF links must make sure L1 and the VREG_FB-to-GND link can never both be fitted.

### S2 TPS63001DRCR.yaml

- **CL31A106KBHNNNE.** The Samsung sheet in `datasheets/` gives 10 µF, ±10 %, 50 V, X5R, 1206/3216, 1.6 mm thick.
  - DC bias (1 kHz, 1 Vrms), my pixel read: −22.8 % at 5.0 V and −24.6 % at 5.25 V. The author has −22.5 % / −24.8 %, which agrees.
  - TCC: ≈ −6.5 % at 85 °C relative to 25 °C; the author's −10 % is conservative.
  - Worst case: 7.5 µF × 0.9 × 0.93 ≈ 6.3 µF (author 6.1 µF). Either way it is ≥ 4.7 µF (SLVS520C p.12 "at least a 4.7-µF input capacitor").
  - 50 V is far above VSYS (≤ 5.25 V).
  - The bom.csv C20 row (1206, C13585, ±10 %, 50 V) matches the sheet.
- **Cout C21 + C22 + C31, 3 × CL10A106MA8NRNC.** 18.6–20.1 µF typical at 3.3 V; 14.9–16.1 µF at −20 % tolerance. The arithmetic is correct. "No upper limit" is verified on p.12 ("There is also no upper limit for the output capacitance value"). Temperature is not included (N3).
- **USB inrush statements.**
  - §7.2.4.1 on printed p.177 says "10 µF in parallel with 44 Ω … plus any capacitive effects visible through the regulator". Verified.
  - The soft start "ramps up from an initial 400 mA" (SLVS520C §7.4.1 p.9). Verified.
  - D-010 itself is an owner decision and I do not rule on it. It is recorded consistently in the yaml, decisions.md D-010, STATUS P5-14 and bom C19.
- C30 is gone from bom.csv and from every yaml. Its history is kept correctly in D-008 (amended by D-009).

### S3 MAX31856MUD+T.yaml

R23/R24 DNF 10 kΩ to 3V3 on DRDY/FAULT appear in the open question, pin 7, pin 13 and the bom.csv R23/R24 row (dnp = yes). A fitted 10 kΩ on a push-pull output costs about 0.33 mA when it is low, which is harmless.

### S4 MPL-AT2512-3R3.yaml

The deviation wording matches D-009 P5-13 and the bom.csv L1 row. Pin 1 (dot) still records the orientation as open, consistent with the both-orientations plan.

### S5 PCC-SMD.yaml: polarity reading

I re-rendered p.2 at 1200 dpi.

**Assembly top view** (the figure labelled "IDEAL COLD JUNCTION COMPENSATION LOCATION"):
- The clips are visible on the PCB, so this is the component side. The board edge is on the right, with the plug entering from the right.
- Rotating the view so that the plug points away from the board, "OMEGA" reads normally (not mirrored). It is therefore a genuine top view.
- The "+" is on the upper clip, the clip spacing is 5.6 mm, and "−" is on the lower clip.
- Seen from outside the board edge with the component side up, the upper clip is on the viewer's right. So **+ is right, − is left**.

**FRONT PANEL DESIGN view:**
- This is the same plan view rotated 180°: the PCB is above, the plug below, and OMEGA is upside down.
- It shows − on the left and + on the right, which with the edge toward the viewer is again + right.

**Conclusion:** the author's polarity reading (J2 = right = T+, J3 = left = T−) is correct, and both views agree. Only the description of the second view is off (N1). The "do not mirror one clip" and silkscreen +/− advice is sound.

### S6 Earlier nits

- **R1, fixed:** the W25Q32RVXHJQ.yaml note now cites §5.2, p.369.
- **R2, fixed:** STATUS.md P5-9 now covers only DRDY/FAULT (closed by D-009).

## Remaining issues

**Nits in the reviewed files (none blocking):**
- **N1:** PCC-SMD.yaml. Reword the FRONT PANEL DESIGN description: it is a plan view, 1.57 mm is the panel thickness, and the label is rotated rather than mirrored.
- **N2:** RP2350A.yaml. Add a C29 placement rule.
- **N3:** TPS63001DRCR.yaml. Optionally state Cout at 85 °C (≈ 14.2–15.3 µF at −20 % tolerance).

**Housekeeping outside the gate scope:**
- **H1:** STATUS.md lists the D-009 row twice in the decisions table.
- **H2:** reviews/constraints/resolutions.md still marks F12, F17, F19, F24, F25 and F28 as `pending`. These are now decided by D-008/D-009, so their resolution should become `accepted`/`answered` with By = owner and the D-ref.
- **H3:** reviews/constraints/BRIEF.md has two problems:
  - The `authors` list has a second entry, "OhmAI (Grok Bot, ohmai skill)", without kind/vendor/model fields.
  - The "Changed since the previous brief" list names only TPS63001DRCR.yaml, although RP2350A, MAX31856MUD+T, MPL-AT2512-3R3, PCC-SMD and W25Q32RVXHJQ also changed against the brief I last reviewed (`41d65780…`). It looks as if it is computed against an intermediate brief.

**Still unverifiable:**
- DC-bias and TCC values remain curve reads (ESTIMATE).
- The MAX31856 DRDY/FAULT drive type is for rev-A to confirm (bring-up plan).
- MPS shielding and field sense: rev-A test.
- Footprint pad numbering: phase 6/7.
- The magnet and warm-tip polarity checks rely on external web sources (TE Connectivity) that I did not check.

---

## Appendix A: re-verification 1 (files_hash 41d65780…c023, HEAD cdf79d7). Its gate table was removed here because it is superseded; finding IDs are kept

**Reviewed:** branch `phase/constraints` at HEAD `cdf79d7` (2026-10-15). The fixes are in commit `054096c`; the resolutions and the regenerated brief are in `cdf79d7`.

**Hash check:** the per-file sha256 values of all 13 files match the regenerated `reviews/constraints/BRIEF.md` (files_hash `41d65780…c023`). All 13 files still validate against `parts/constraints.schema.json` (jsonschema; this is not an `ohmai` run).

**Scope of this pass:**
- I re-checked every changed line in `git diff eabc642..cdf79d7 -- parts/constraints/ bom/bom.csv` against the cited page.
- The first review (files_hash `964bd47e…1122`, HEAD `eabc642`) is kept below as an appendix. Its finding IDs F1–F36 are reused here.
- I did not edit any input file and did not commit.

### Gate verdict: PASS WITH NITS

- **Resolved:** every finding that was the author's to fix. That is 18 fixes, plus the side notes on bom D1 and bom U2.
- **Remaining:** 1 new nit (R1 below) and 1 housekeeping note outside scope (R2).
- **Owner items not ruled on:** F12, F17, F19, F24, F25 and F28 are open owner items (P5-9 … P5-13, including P5-10). The yaml files record them correctly, and I make no ruling on them.
- **Caveat:** F19 (PCC-SMD polarity, P5-12) still has to be answered before the schematic gate. It does not block this constraints gate.


### Re-verification of F1–F36

Status values: **resolved**, **partially**, **not resolved**, **OK** (no action was needed), **owner** (an open owner item that this review does not rule on).

| ID | File | Original finding (short) | Status | Evidence checked in the current file |
|----|------|--------------------------|--------|--------------------------------------|
| F1 | ABM8-272-T3 | OK | OK | unchanged apart from F2/F3 |
| F2 | ABM8-272-T3 | quote cited p.555, is on p.556 | resolved | cite now p.556 §8.2.1.1, plus "same statement in HDG p.14". Matches RP2350 p.556 |
| F3 | ABM8-272-T3 | pin name "case" | resolved | pins 2/4 now "2 (NC/GND)" / "4 (NC/GND)", note cites Abracon p.2 bottom view |
| F4 | DMG1012T-7 | OK | OK | |
| F5 | DMG1012T-7 | ID at 85 °C missing | resolved | 0.45 A at TA 85 °C added, cite p.2 Maximum Ratings. Pin numbering stays a footprint question (agreed) |
| F6 | KT-0805G | OK | OK | |
| F7 | KT-0805G | cite Pico 2, not Pico 2 W | resolved | required_external now cites pico-2-datasheet.pdf p.20 Fig. 11. Re-rendered: GPIO25 → R3 "470R 1% M0603 50mW" → D2 Green. VF remark added |
| F8 | MAX31856MUD+T | OK | OK | |
| F9 | MAX31856MUD+T | CM range, VBIAS/RBIAS, OV/UV, OVUV suspension missing | resolved | Every value checked against the pages; all match. See note 1 below the table |
| F10 | MAX31856MUD+T | BIAS junction point | resolved | layout note and pin 2: BIAS joins T− on the connector side of the T− 100 Ω, caps on the pin side (Fig. 8 p.27). 2 kΩ option cited to p.27 "Input Protection". See note 2 |
| F11 | MAX31856MUD+T | CPHA, SDO high-Z, VPOR, T− + cable R, temp cite | resolved | CPHA note and SDO high-Z (p.15, verified). Table 4 mode 01 for RS < 5 kΩ (p.14, verified). p.28 T− rule added. Operating-temperature cite now names the Abs Max block. VPOR: see F9 |
| F12 | MAX31856MUD+T | DRDY/FAULT drive type | owner (P5-9) | proposal recorded in the open question; no ruling |
| F13 | MBR120VLSFT1G | OK; bom D1 Vf side note | OK / resolved | bom D1 now "Vf max 0.340 V @ 1 A, 25 °C (0.300 V at 85 °C)". Matches onsemi p.2 |
| F14 | MPL-AT2512-3R3 | OK | OK | |
| F15 | MPL-AT2512-3R3 | record Fig. 25 convention | resolved | new layout note: current in at "+", indicator at the "−" (current-out) end; buck DC current flows VREG_LX → L → VOUT, so the indicator is at the VOUT/DVDD end. Builds A/B defined. Consistent with Fig. 25 (p.456) and with Fig. 23 (p.454), where the indicator is drawn at the L_X pad on the C_OUT/VOUT side |
| F16 | MPL-AT2512-3R3 | cut-copper cite | resolved | cite now p.454 (top layer), with layer 2 / Fig. 24 on p.455 |
| F17 | MPL-AT2512-3R3 | shielding / deviation status | owner (P5-13) | marked PENDING OWNER in the shielding open question; no ruling |
| F18 | PCC-SMD | OK | OK | |
| F19 | PCC-SMD | +/− clip position | owner (P5-12) | open question rewritten with a proposal (ask Omega, magnet check, warm-tip check). The external sources it cites (Omega web page, TE page) were not checked by me. No ruling |
| F20 | PCC-SMD | mpn not orderable | resolved | `mpn: PCC-SMD-20`; -500/-1000 noted (p.1 Model No.). `match.mpn` still says "PCC-SMD", which is harmless as a match key |
| F21 | RP2350A | OK | OK | |
| F22 | RP2350A | C_FILT and loop cites | resolved | C_FILT note now p.455. Loops note p.454, with "2 adjacent vias p.455" in the text. Both match the pages |
| F23 | RP2350A | Table 1436 page; C_OUT `to:` | resolved | both Table 1436 entries now p.1340. Pin-50 C_OUT now `to: VREG_PGND` (Fig. 22 p.453) |
| F24 | RP2350A | ADC_AVDD 2.2 vs 4.7 µF | owner (P5-11) | no ruling |
| F25 | RP2350A | C_IN derating | owner (P5-10) | both reads recorded in the open question; no ruling |
| F26 | TPS63001DRCR | OK | OK | |
| F27 | TPS63001DRCR | start-up VIN; RθJA; EP | resolved | "Input voltage range for start-up 1.9–5.5 V" matches p.5. RθJA 46.8 (p.4) vs 48.7 (p.16) recorded as a datasheet inconsistency. EP = 11 left to the footprint check |
| F28 | TPS63001DRCR | 10 µF derating | owner (P5-10) | both reads recorded; no ruling |
| F29 | TS-1187A-B-A-B | OK; storage quirk | OK / resolved | storage note "as printed … drawing quirk" added |
| F30 | TS-1187A-B-A-B | height 1.6 → 1.5 mm | resolved | `package` now "H 1.5 mm (height code A)". Force note gives the order force-height-keystake. See the TS-1187A assessment below |
| F31 | TYPE-C-16PIN-2MD-073 | OK | OK | |
| F32 | TYPE-C-16PIN-2MD-073 | shield contact R | resolved | "Contact resistance SHIELD 50 mΩ max" added, and the 40 mΩ entry now reads "VBUS/GND and other pins". Both match drawing note 4-2. The alternate's signal list is still unchecked (phase 7, agreed) |
| F33 | USBLC6-2SC6 | OK | OK | |
| F34 | W25Q32RVXHJQ | OK; bom HDG page | OK / resolved | bom U2 now cites "Hardware design with RP2350 p.10 §3.1" |
| F35 | W25Q32RVXHJQ | EP `nc: true` vs GND | resolved | pin 9 now `direction: passive`, no `nc`. The note explains the choice is open (p.77 allows both) |
| F36 | W25Q32RVXHJQ | stale R6 question; GD QE default | resolved | R6 question marked RESOLVED (D-006, bom U2/R6). QE note verified, see note 3. Nit R1 on the §5.x section label |

**Notes on the checks:**

1. **F9 values checked against MAX31856 p.3–4 and p.26:**
   - Input common-mode range 0.5–1.4 V (p.3).
   - VBIAS 0.735 V and RBIAS 2 kΩ (p.3).
   - OV rising threshold VAVDD − 0.1 / + 0.17 / + 0.35 V, hysteresis 0.09 V (p.3).
   - UV falling threshold −0.3 / −0.17 / 0 V, hysteresis 0.09 V (p.4).
   - Note 8: the OV/UV limits apply to T+, T− and BIAS.
   - VPOR 2.7 typ / 2.85 max with 0.1 V hysteresis (p.3).
   - Fault Status register: "the presence of the OVUV fault will suspend conversions" (p.26).
2. **F10 citation:** the author is right that the 2 kΩ series text is on p.27 under "Input Protection". Fig. 9 itself is on p.28. Both cites are valid.
3. **F36 QE check:**
   - W25Q32RV: the QE bit is "factory default for … ordering option JQ" (§7.1.10, printed p.15).
   - GD25Q32E: "QE bit … set to 0 (Default)" (p.13), and the initial delivery status register is 00H except DRV0 (p.37). HOLD# is active while QE = 0 (p.9).
   - RP2350 boot ROM: "always using an 03h serial read command" (p.369).

### TS-1187A suffix order: assessment of OhmAI's disagreement

**OhmAI's position:** the drawing's PART NO table lists Operating Force, then Height (Code-X), then Keystake. That row order gives the field order of TS-1187A-X-X-X, so -B-A-B decodes to force B = 160 gf, height A = 1.5 mm, keystake B = brass.

**What I checked:**
- I re-read the drawing (p.1). Under "PAPT NO TS-1187A-X-X-X" the rows are, in order: "Operating Force A:100gf B:160gf C:260gf", "Height Code-X" (pointing to the separate A–J height table), and "Keystake A:PA46 B:Brass".
- The decoding that follows from this order agrees with the distributor data (LCSC C318884 and JLCPCB: 1.6 N, 1.5 mm).
- No other order fits both the drawing's codes and the distributor data. In particular, height first (B = 1.6 mm) contradicts the 1.5 mm listing.

**Conclusion:** I accept OhmAI's reading.
- My original wording, that the drawing "does not state" the order, was too strong. The drawing gives the order by the sequence of the rows, not with an explicit field legend. An explicit legend would be stronger proof, but the row sequence plus the matching distributor listing is enough for a constraints file.
- Nothing further is needed. The yaml now records the decoding and both sources.
- Optional: confirm the height on the delivered reel at incoming inspection, since it affects enclosure clearance.

### New-error scan of the changed lines (eabc642..cdf79d7)

Every changed line in the 12 changed yaml files and in bom.csv (rows U2 and D1) was read against its cited page. Result: one nit (R1) and no new technical errors.

**Lines checked and found correct:**
- **MAX31856:** new recommended entries (values per note 1 above); the junction-point wording; the CPHA/SDO note; Table 4 mode 01; the p.28 rule.
  - The reference to D-006 P4-8 ("no TVS on T+/T−", decisions.md) is consistent with "not planned for pico-k".
  - The CM-range note "grounded probe at USB ground is outside this range" is a correct consequence of p.3 / p.26.
- **MPL-AT2512-3R3:** the orientation derivation is sound for a buck. The average inductor current always flows from the switch node to the output.
- **RP2350A:** the page changes match the source; C_OUT `to: VREG_PGND` matches Fig. 22.
- **TPS63001:** start-up 1.9–5.5 V (p.5). "Use 48.7 (worse)" is a sensible conservative choice.
- **TYPE-C:** the note 4-2 wording matches the drawing.
- **W25Q32RV:** all QE and EP statements verified (note 3). The only nit is the "§5.x" label (R1).
- **KT-0805G, DMG1012T-7, ABM8, PCC-SMD, TS-1187A:** matched their pages as listed in the F-table.
- **bom.csv:** the D1 Vf values match onsemi p.2; the U2 cite p.10 §3.1 matches HDG.

**R2, housekeeping outside scope, not an owner ruling:** in STATUS.md, P5-9 still lists "which PCC-SMD clip position" (now P5-12) and "fit the flash CS 10 kΩ when the GD25Q32E is used" (marked RESOLVED via D-006 in W25Q32RVXHJQ.yaml and resolutions F36). The author may want to trim P5-9 so it carries only DRDY/FAULT.

### Remaining issues

1. **R1 (nit):** W25Q32RVXHJQ.yaml QE note. Change "§5.x" to "§5.2 Processor-controlled boot sequence".
2. **R2 (housekeeping, STATUS.md, outside the gate scope):** remove the two P5-9 sub-items that are now covered by P5-12 and by D-006.
3. **Owner items:** P5-9 (F12), P5-10 (F25, F28), P5-11 (F24), P5-12 (F19) and P5-13 (F17) are open. This review does not rule on them. P5-12 must be answered before the schematic gate.

**Still unverifiable**, carried over from the first review:
- MAX31856 DRDY/FAULT drive type.
- MPS shielding and field sense.
- PCC-SMD +/− position.
- Curve-read DC-bias values (ESTIMATE).
- Footprint pad numbering (phase 6/7).
- The alternates TYPE-C-31-M-12, UMW USBLC6 and the full GD25Q32E map.
- USB 2.0 §7.2.4.1 (spec not in `datasheets/`).
- GD25Q32E QE handling in firmware.

---

### Appendix: original review (files_hash sha256:964bd47e29ab969e62dcaaee23f5aeeba0b91dc074230034fac169f919ee1122, HEAD eabc642)

The original findings table (F1–F36) has been replaced by the re-verification table above, which carries the IDs, the original findings and their status. The narrative sections below are unchanged from the first review, except that their headings are demoted one level.

#### Per-file review

Severity: **blocker** = wrong hardware or damage. **should fix** = fix in the file before the constraints gate, or it will mislead the schematic. **nit** = citation or completeness.

##### ABM8-272-T3.yaml: OK (2 nits)

- **Pins:** 1 X1 / 3 X2 passive; 2/4 ground (D-007). Correct against Abracon p.2 ("#2 and #4 no function"). The 15 pF / 1 kΩ externals match HDG p.13 and Pico 2 Fig. 11.
- **Nit (p.555 vs p.556).** The file cites "Pico 2 has been specifically tuned…" to RP2350 p.555. The datasheet text is on p.556 ("tuned for the specifications of the Abracon ABM8-272-T3 crystal"), also HDG p.14. Fix: change the page.
- **Nit (pin name).** The pin name says "case". Abracon gives no function. Fix: "NC/GND".
- **D-007 consistency:** pads 2/4 to GND are reflected and the open question is marked RESOLVED.

##### DMG1012T-7.yaml: OK (1 nit)

- Ratings match DS31783 Rev 8-2 p.2. Pin numbering is inferred; the open question is legitimate.
- **D-007 P5-5 (gate to 3V3) consequence check.** VSYS ≈ 4.6–5.5 V gives a source of about 1.53–1.83 V and VGS ≈ 1.47–1.77 V, above VGS(th) max 1.0 V. RDS(on) ≤ 0.7 Ω at 1.8 V is negligible against 20 k/10 k.
  - Side effect: the ADC3 node cannot rise above about 3.3 V − VGS(th). This is a useful clamp.
  - With 3V3 off, the FET is off. Leakage into the unpowered RP2350 is blocked, which is the purpose of the Pico 2 W circuit.
  - No negative consequence found.
- **Nit:** ID 0.45 A at 85 °C is not listed.

##### KT-0805G.yaml: OK (1 nit)

- Values verified on p.3/p.4. Pad polarity verified on the p.2 drawing: ① = +, ② = −, green corner mark at ②.
- **D-007 P5-3 (470 Ω):** consistent. The best citation is Pico 2 itself (Pico 2 datasheet p.20, Fig. 11: GPIO25 → R3 470R → D2 Green), not Pico 2 W. The current estimate uses VF at 5 mA. At 0.3–2 mA VF is lower, so the current is somewhat higher than 0.3–1.5 mA. This is harmless.

##### MAX31856MUD+T.yaml: issues (2 should fix, 1 nit, 1 question)

Checks requested:

| Item | File says | Datasheet says | Verdict |
|---|---|---|---|
| Common-mode range | not recorded | 0.5–1.4 V (p.3, Electrical Characteristics) | **should fix**, add as recommended, cite p.3 |
| Abs max T+/T− | ±45 V, ±20 mA (p.2) | ±45 V, ±20 mA (p.2) | OK |
| Input filter | 100 Ω series each input, 100 nF differential, 10 nF to GND each | Fig. 8 p.27: same values. p.27 text: 100 nF "strongly recommended"; the 10 nF caps are for high-noise / RF | OK |
| BIAS pin | analog_out, "connect to T−" | p.10 "nominally 0.735 V, floating when no conversions"; p.27 "Connect the BIAS output to T−"; Fig. 8: BIAS joins T− on the connector side of the 100 Ω | **should fix**, state the junction point; add VBIAS/RBIAS (p.3) |
| DVDD/AVDD decoupling | 0.1 µF each, to AGND/DGND | p.10 pin table and p.27 "0.1 µF … close to the VDD pins"; Typical App p.1 | OK |
| SPI levels | VIL 0.8 / VIH 2.1 V; VOL 0.4 V at 1.6 mA, VOH VDD−0.4 V; ≤ 5 MHz | p.2 / p.5 same | OK. Add CPHA = 1 (p.15) as a nit |
| FAULT/DRDY | `output`, open question on drive type | Datasheet silent; VOH/VOL spec (p.5) applies to outputs | **question**, see F12; recommend no pull-up and an optional DNF |

Other points:
- **Should fix: OV/UV.** Add the rising threshold VAVDD + 0.17 V typ (−0.1..+0.35 V) (p.3) and the falling threshold −0.17 V typ (−0.3..0 V) (p.4). Record that conversions are suspended while OVUV is set (p.14, p.26).

  This is the datasheet basis of MW-01 (grounded-junction probe) and should be in the constraints, not only in architecture.md.
- **Nit:** VPOR 2.7–2.85 V (p.3) is missing.
- **Nit:** "Operating temperature" sits under recommended but cites Abs Max p.2.
- **Nit:** missing p.28 "increase the T− resistor by the cable resistance". Fig. 9 (p.28) uses 2 kΩ in T+, T− and BIAS for > ±45 V faults.
- **Nit (firmware):** open-circuit detection mode depends on source R and time constant (Table 4, p.14). With 100 Ω + 100 nF, mode 01 (RS < 5 kΩ) applies. Note for firmware.
- **Pins:** 1–14 match p.10. DNC is pin 6 with `nc: true`, which the schema allows.

##### MBR120VLSFT1G.yaml: OK

All values match p.2. The p.5 footprint and pin 1 = cathode are consistent.

Side note outside scope: the bom.csv D1 row says "Vf 0.30 V @ 1 A". That is the 85 °C value; at 25 °C it is 0.340 V max (p.2).

##### MPL-AT2512-3R3.yaml: issues (1 should fix, 1 nit, 1 question)

- Values match MPS Rev 1.2, and the RP2350 numeric limits (p.455) are met. Isat ≥ 1.5 A rests on a typical value only.
- **Should fix:** add the RPi orientation reference (Fig. 25 p.456, Fig. 23 p.454). See conflict 5.
- **Nit:** the "cut copper" cite; the top-layer rule is on p.454.
- **Question (D-007 locked):** "fully shielded" and the field sense are unverified.

##### PCC-SMD.yaml: issues (1 should fix as question, 1 nit)

- Temperature, land pattern and CJC notes are correct (Omega p.1–2).
- **Should fix (question):** +/− clip assignment. MAX31856 Table 1 p.12 gives type K T+ = Chromel, T− = Alumel. The asymmetric socket fixes the plug orientation, but which position is − is not on the Omega sheet. Ask Omega or use the matching SMPW/MPJ plug drawing. Unverified by me.
- **Nit:** `mpn` should be an orderable code (PCC-SMD-20 / -500 / -1000).
- The 100 Ω series R cites MAX31856 Fig. 8 p.27 correctly.

##### RP2350A.yaml: issues (3 nits, 2 questions)

- The pin list and table citations were verified, as were the §6.3.8 values (p.455).
- The IOVDD conflict is handled correctly (see conflict 1).
- **Nits:**
  - C_FILT note page;
  - switching-loop page;
  - Table 1436 page;
  - C_OUT `to: GND` should be VREG_PGND (Fig. 22 p.453).
- **Questions:**
  - ADC_AVDD 4.7 µF vs 2.2 µF (conflict 4);
  - C_IN effective capacitance (P5-10).
- **D-007 consistency:** C28 is reflected at pin 23. L1 = MPL-AT2512-3R3 is reflected at pin 48. Conflicts are marked "Accepted, D-007 (P5-8)".
- Pico 2 has only C9 4u7 at pin 23 (Fig. 11 p.20), so requiring 100 nF plus 4.7 µF is conservative and fine.

##### TPS63001DRCR.yaml: OK (1 nit, 1 question)

- Values verified on p.3–5, p.7, p.10, p.12.
- **D-007 P5-6 consequence:** see F28 and conflict notes. My curve read is about 5 points worse than the author's at both 3.3 V and 5 V.
- **D-007 P5-2 consequence:** R16 is the PS/SYNC pull-down and R17 is removed. This is consistent; no remaining reference to R17 in the constraints.

##### TS-1187A-B-A-B.yaml: issues (1 should fix)

- Height is 1.5 mm, not 1.6 mm (F30).
- Everything else matches the drawing.
- Storage −30..80 °C vs operating −30..85 °C is printed that way on the drawing. It is copied correctly but worth a note.

##### TYPE-C-16PIN-2MD-073.yaml: OK (1 nit)

- Pins and spec cites were verified, including Table 3-5 notes 2–5 (p.69) and Table 4-25 (p.236).
- **D-007 P5-7:** the shell is `ground` via the 4 tabs. This is consistent with Pico 2 and Pico 2 W (J1 shell pins to GND).
- **Nit:** the shield 50 mΩ note is not recorded.

##### USBLC6-2SC6.yaml: OK

- All values match.
- The UMW alternate datasheet is not saved; the file already flags this.
- The USB 2.0 §7.2.4.1 reference (VBUS ≤ 10 µF) cannot be checked: the USB 2.0 spec is not in `datasheets/`.

##### W25Q32RVXHJQ.yaml: issues (2 should fix)

- EP `nc` vs GND (F35).
- Stale R6 question, and GD25Q32E QE default (F36).
- Values otherwise verified.
- **Note:** the bom.csv U2 row cites "Hardware design with RP2350 p.8" for the R6 rule; the yaml cites p.10 (§3.1, where R1 10 k DNF and R6 1 k are). p.10 is the right page.

#### The five flagged conflicts: resolution

1. **IOVDD pin list.** Table 1432 (p.1338) lists IOVDD as "11, 20, 30, 38, 45, 54" and QSPI_IOVDD as "54". It contradicts itself and omits pin 1.
   - Fig. 2 (p.15) and Fig. 148 (p.1334) show pin 1 = IOVDD and pin 54 = QSPI_IOVDD.
   - So do Pico 2 Fig. 11 (p.20), the Pico 2 W schematic and HDG Fig. 15 (p.20).
   - The online build 2026-10-01 still has the same table text.
   - **Resolution:** Table 1432 is a datasheet erratum. Follow the figures, as the yaml does. Both pins are on 3V3, so the only risk is a wrong symbol; check the symbol at the ERC gate.
2. **p.455 C_OUT wording.** p.455 says C_OUT "must be placed between VREG_VIN and VREG_PGND". Fig. 22 (p.453) and Fig. 23 (p.454) put C_IN across VREG_VIN–VREG_PGND and C_OUT from VOUT to the same PGND island.
   - p.454 has the mirror slip: it says "C_IN needs its own separate GND via" under the VREG_AVDD bullet, which must mean C_FILT. The C_FILT rule is repeated correctly on p.455.
   - **Resolution:** read p.455 as C_IN and p.454 as C_FILT. Place and route all three exactly as Fig. 23. The text is unchanged in the online build 2026-10-01. Not confirmed by RPi.
3. **VREG_AVDD resistor: 33 Ω vs 27 Ω.** 33 Ω is in RP2350 Fig. 19 (p.451) and Fig. 22 (p.453), HDG p.7 ("RC filter of 33 Ω and 4.7 µF"), and Pico 2 R17 33R (Fig. 11 p.20). Only Pico 2 W uses 27R.
   - **Resolution:** keep 33 Ω (R5), as the yaml and bom.csv do.
   - At about 200 µA the drop is 6.6 mV vs 5.4 mV. The filter corner is about 1.0 kHz nominal.
   - With C18 derated to about 3.3 µF at 3.3 V (ESTIMATE) the corner is about 1.5 kHz. That is still better than RPi's own 0402 part derates to.
4. **ADC_AVDD capacitor: 2.2 µF vs 4.7 µF.** The Pico 2 datasheet text (p.14) says "201 Ω into 2.2 µF". The Pico 2 schematic (Fig. 11 p.20) fits C13 4u7, and Pico 2 W also has C13 4u7.
   - **Resolution:** recommend 4.7 µF. Both built references use it, and the CL10A475KO8NNNC already in the BOM can be reused, saving one line item.
   - D-007 (P5-8) accepted 2.2 µF and is locked, so this is filed as a question (F24). It is low risk either way.
5. **MPL-AT2512-3R3 vs the RPi inductor requirements.**
   - **Numeric limits:** met. 3.3 µH ±20 %; DCR 140 mΩ max ≤ 250 mΩ; Isat 3 A typ ≥ 1.5 A (typical only) (p.455).
   - **Not shown:**
     - "fully shielded": MPS says only "molded". The AOTA sheet says "shielded construction" and "approved for use with Raspberry Pi's RP235x".
     - Field polarity: the MPS dot marks start of winding. RPi needs the field sense (p.456), and HDG p.6 notes the AOTA reel is all aligned the same way.
     - Footprint: the MPL is 2.5 × 2.0 mm against 2.0 × 1.6 mm, so Fig. 23 cannot be copied exactly.
   - HDG p.7 calls deviating "at your own risk".
   - **Resolution:** with D-007 locked, accept it as a documented rev-A R&D deviation, not an equivalent part.
     - Record Fig. 25 in the yaml: current in at "+", indicator at the current-out (VOUT) end.
     - Build both orientations; measure DVDD ripple, load-step and efficiency.
     - Keep the AOTA as the reference part and the Fig. 21 (p.452) external-1V1 fallback.

#### Owner decisions (D-006/D-007): consistency and consequences

| Decision | Reflected in yaml/bom | Consequence found |
|---|---|---|
| R17 removed (P5-2) | bom row gone; DMG1012T and TPS63001 notes updated | none |
| Second 4.7 µF on DVDD, C28 (P5-4) | RP2350A pin 23, bom C28 | Place at the bottom edge near pin 23, away from LX/COUT (p.455). About 4.5 µF at 1.1 V, OK |
| Q1 gate to 3V3 (P5-5) | DMG1012T pin 1 | OK, VGS 1.47–1.77 V. ADC3 node clamped to ≲ 3.3 V − VGS(th) |
| 4.7/10 µF to 0603 (P5-6) | RP2350A, TPS63001, bom | C16 ≈ 3.3 µF at 3.3 V. C20 ≈ 4.4 µF at 5 V and C21 + C22 ≈ 12.4 µF at 3.3 V (my reads, ESTIMATE, a little worse than the author's). Still no worse than the RPi/TI reference parts. Accept under P5-10, or add a DNF third 10 µF on 3V3 |
| 470 Ω LED (P5-3) | KT-0805G, bom R22 | OK; cite Pico 2 p.20 |
| Crystal pads 2/4 and USB shell to GND (P5-7) | ABM8 pins 2/4 `ground`, TYPE-C SH `ground` | Matches Pico 2/Pico 2 W. Pad-1 chamfer ambiguity is harmless with 2/4 both at GND |
| L1 = MPL-AT2512-3R3, both orientations (P4-4b) | MPL yaml, RP2350A pin 48 | see conflict 5 |
| Conflicts accepted (P5-8) | RP2350A open questions | only ADC_AVDD differs from my recommendation (F24) |

#### Items I could not verify

- **MAX31856 DRDY/FAULT output type.** Rev 0 is silent. I could not download a newer ADI revision (curl to analog.com failed); official URL: https://www.analog.com/media/en/technical-documentation/data-sheets/MAX31856.pdf. The push-pull statement comes only from an unverified 2019 forum quote.
- **"Fully shielded" status and field direction of MPL-AT2512-3R3 / MPL-AL4020-3R3.** No MPS statement exists. Needs MPS or rev-A measurement.
- **PCC-SMD +/− clip position.** Not on the Omega sheet.
- **DC-bias values.** These are my pixel reads of the Samsung curves (ESTIMATE, about ±3 points): CL10A475KO8NNNC about −4.6 % at 1.1 V and −30 % at 3.3 V; CL10A106MA8NRNC about −38 % at 3.3 V and −56 % at 5 V. No tabulated data.
- **Pin numbering of footprints:**
  - DMG1012T (1 G / 2 S / 3 D);
  - TPS63001 EP = 11;
  - W25Q32 EP = 9;
  - TS-1187A A–D pad names;
  - USB-C shared A/B pads.

  None of the datasheets define these numbers; check them against the KiCad footprints in phase 6/7.
- **TS-1187A-B-A-B suffix order.** The drawing does not state the order of the X-X-X fields. Height 1.5 mm is taken from the LCSC C318884 / JLCPCB listing, not from the drawing.
- **Alternate parts.** I did not check TYPE-C-31-M-12 (image-only drawing), the UMW USBLC6-2SC6 (datasheet not saved) or the full GD25Q32E pin map beyond the notes cited.
- **Online datasheet builds.** I compared the RP2350 datasheet and HDG against the online builds for the conflict text only. Online URLs: https://datasheets.raspberrypi.com/rp2350/rp2350-datasheet.pdf, https://datasheets.raspberrypi.com/rp2350/hardware-design-with-rp2350.pdf.
- **USB 2.0 §7.2.4.1 (VBUS capacitance limit).** The USB 2.0 spec is not in `datasheets/`.
- **GD25Q32E quad mode.** Whether RP2350 boot2 sets QE on the GD25Q32E is a firmware question and was not verified.