# Decision log: pico-k

Append-only. One entry per owner decision, written the same day. Add a matching row to the STATUS.md
"Locked decisions" table. To reverse a decision, add a new entry that supersedes the old one. Do not edit
the old entry.

## Template
```
## D-001: <short title>   (YYYY-MM-DD, phase N)
- Decided by: <owner>
- Decision: <what was chosen>
- Options considered: <A, B, C, with one line each>
- Why: <reasons, with links to sources>
- Consequences: <what this locks, what it rules out>
- PR / ref: <PR number or commit>
- Supersedes: <D-xxx or none>
```

## D-000: Use OhmAI 0.1.0.dev0 workflow   (2026-10-15, phase 0)
- Decided by: owner (project created)
- Decision: phases and gates as in `.ohmai/phases/`; main = approved state only; PR = gate.
- Supersedes: none

## D-001: Requirements locked   (2026-10-15, phase 1)
- Decided by: owner
- Decision: `docs/requirements.md` as of this commit is the locked spec. Answers:
  - Use case: general-purpose "probe on a stick", powered and driven by a laptop or powerbank over USB;
    USB 5 V is the only supported source; full Pico pinout kept.
  - Q1 MCU: RP2350A.
  - Q2 Full drop-in Pico 2 compatibility: outline, pin order and functions, castellations + 2.54 mm holes,
    mounting holes, debug header position.
  - Q3 Thermocouple connector on the TOP side; bottom stays flat (answered earlier the same day).
  - Q4 1 channel.
  - Q5 MAX31856; grounded and ungrounded probes; full type K range.
  - Q6 SPI on 4 shared edge GPIO, silkscreen labels, solder jumpers to disconnect.
  - Q7 5-10 prototypes, JLCPCB assembly with LCSC parts. Cost target and certification left open, non-blocking.
  - Q8 USB-C.
  - Admin: owner = project owner.
- Options considered: see `docs/requirements.md` → Research (RP2040 / RP2350A / RP2350B; MAX31855K /
  MAX31856 / MCP9600; GPIO options A/B/C; connector placement readings).
- Why: agent recommendations accepted by the owner; reasons and sources in `docs/requirements.md` → Research.
- Consequences: locks R-01..R-16 and W-01..W-04. Rules out RP2040, RP2350B, MCP9600/MAX31855, micro-USB,
  bottom-side parts, multi-channel.
- PR / ref: local merge of `phase/requirements` into `main` (no remote)
- Supersedes: none

## D-002: SWD debug header dropped (amends D-001)   (2026-10-15, phase 2)
- Decided by: owner, feedback on the phase 2 draft: omit the dedicated debug header and fit an on-board thermocouple connector.
- Decision: R-05 no longer requires the 3-pin SWD debug header. SWCLK/SWDIO/GND go to flat bottom-side
  test pads (as Pico 2 TP1–TP7, Pico 2 datasheet §3.1 p.9). The 4 mounting holes and full castellated rows
  stay required if possible; the connector fit is open question A2-3.
- Why: frees the edge centre for a mini type-K socket on the top side (R-07).
- Consequences: D-001 Q2 "debug header position" no longer applies. Drop-in Pico 2 users who rely on the
  3-pin header use the test pads instead.
- PR / ref: phase/architecture (local)
- Supersedes: D-001 in part (Q2, R-05 debug header only)

## D-003: Target market EU only (amends D-001)   (2026-10-15, phase 2)
- Decided by: owner
- Decision: target market = EU only. EU rules (CE marking, EU declaration of conformity, WEEE, GPSR user
  information) drive phase 3 and the user manual (`docs/manual.md`). UK (UKCA) and US (FCC): not applicable.
- Why: owner decision; OhmAI now asks for target markets in phase 1.
- Consequences: STATUS.md `markets: [EU]`. Certification route still decided in phase 3.
- PR / ref: phase/architecture (local)
- Supersedes: D-001 in part (Q7 "certification left open" → markets fixed; cost target stays open)

## D-004: Architecture (phase 2)   (2026-10-15, phase 2)
- Decided by: owner, phase 2 gate
- Decision (details and sources in `docs/architecture.md`):
  - A2-1: 3.3 V regulator TPS63001DRCR buck-boost (LCSC C28060), PS on GPIO23 as Pico 2.
  - A2-2: SPI1 on GP12 (RX←SDO), GP13 (CS), GP14 (SCK), GP15 (TX→SDI), pins 16/17/19/20; 4 cuttable
    solder jumpers; CS pull-up to 3V3 on the IC side of the jumper. DRDY/FAULT to test pads.
  - A2-3: mini type-K socket = 2 × Omega PCC-SMD clips (option M1) at the edge opposite USB, MAX31856
    directly behind them (cold junction). Fit F1: the 2 mounting holes at that end are dropped; outline
    stays 51 × 21 mm; all 40 castellations kept. **Amends R-05** (4 → 2 holes) and confirms R-02.
  - A2-4: G1, accept the grounded-junction probe common-mode limit and document it (manual warning MW-01).
  - A2-5: USB-C receptacle HRO TYPE-C-31-M-12 (LCSC C165948); phase 4 checks the shell-tab length on a
    1.0 mm board.
  - A2-6: 4-layer, 1.0 mm PCB.
- Options rejected: A2-1 B RT6150B (out of stock at LCSC), C AP2112K (Tj ~157 °C); A2-2 P2/P3; A2-3 F2
  tongue (breaks R-02), F3 through-hole jack (breaks flat bottom), F4 no socket; A2-4 G2 isolation;
  A2-5 U2; A2-6 2-layer. Reasons in `docs/architecture.md`.
- Consequences: R-05 amended; MW-01 is a required manual warning; part numbers become phase 4 inputs
  (second sources still to be named in phase 4).
- PR / ref: local merge of `phase/architecture` into `main` (no remote)
- Supersedes: D-001 in part (R-05 hole count, together with D-002)

## D-005: Safety and compliance plan (phase 3)   (2026-10-15, phase 3)
- Decided by: owner, phase 3 gate: all nine recommendations accepted.
- Decision (details and sources in `docs/safety.md`):
  - S3-1: rev-A (5–10 boards) is the owner's own R&D, supplied to no one; the full CE route runs before
    the first board is supplied to anyone, paid or free.
  - S3-2: D1, finished board for end users (EMC + RoHS CE, GPSR, WEEE, REACH).
  - S3-3: A, mains-probe hazard handled by intended use + warning MW-02; no isolation, no extra series resistors.
  - S3-4: C1, EN IEC 62368-1 as the safety reference for the GPSR risk analysis.
  - S3-5: instructions limit USB and thermocouple cables to ≤ 3 m.
  - S3-6: E1, EN 55032 Class B + EN 55035; performance criterion A = reading change within R-11, no reset or USB drop.
  - S3-7: derating rules: all parts rated −20 to +85 °C; capacitors ≥ 10 V on VBUS/VSYS; resistors ≤ 50 % rated power.
  - S3-8: CE (≥ 5 mm) + WEEE bin (≥ 7 mm) + "pico-k rev-A" + batch code on the bottom silkscreen;
    manufacturer name, postal + e-mail address on packaging and manual; Sweden first, Swedish + English.
  - S3-9: T2, pre-compliance day + self-declaration on the board to be sold; T1 lab if margins are small.
  - Manual warnings MW-01 … MW-06 as listed in STATUS.md.
- Options rejected: S3-2 D2; S3-3 B/C; S3-4 C2; S3-6 E2/E3; S3-9 T1-first, T3 (reasons in `docs/safety.md`).
- Consequences: phase 4 parts need RoHS/REACH declarations and must meet the S3-7 rules; bottom silkscreen
  reserves room for CE + WEEE marks.
- PR / ref: local merge of `phase/safety` into `main` (no remote)
- Supersedes: none

## D-006: Part selection and costed BOM (phase 4)   (2026-10-15, phase 4)
- Decided by: owner, phase 4 gate: recommendations P4-1 … P4-11 accepted; P4-4 then corrected
  by the owner the same day (see "Amendment pending").
- Decision (details, prices and sources in `parts/selection.md`; parts in `bom/bom.csv`):
  - P4-1: single-source risk accepted in writing for RP2350A, MAX31856 (both D-001) and TPS63001/TPS63000 (TI only).
  - P4-2: flash W25Q32RVXHJQ; approved alternate GD25Q32EEIGR with R6 10 kΩ CS pull-up fitted.
  - P4-3: crystal ABM8-272-T3, single source accepted in writing.
  - P4-4: **superseded, see amendment below** (was: AOTA-B201610S3R3-101-T single source, buy from Symmetry).
  - P4-5: Omega PCC-SMD, single source accepted in writing; rev-A hand-soldered from one PCC-SMD-20 strip; consigned to JLC for volume.
  - P4-6: option A. USB-C main part SHOU HAN TYPE-C 16PIN 2MD(073) (−25 … +85 °C, meets S3-7), approved
    alternate Korean Hroparts TYPE-C-31-M-12; shell-tab tips up to 0.2 mm below the 1.0 mm board accepted.
    **Amends D-004** (A2-5 part choice).
  - P4-7: 0402 passives. P4-8: no TVS on T+/T−. P4-9: SW1 and Q1 accepted without a named second source for rev-A.
  - P4-10: LED KT-0805G. P4-11: JLC Economic PCBA if it accepts 4-layer + castellated holes, else Standard.
- Amendment (final, owner 2026-10-15, recorded in D-007): the core-regulator inductor AOTA-B201610S3R3-101-T is
  **replaced**, not bought. P4-4b accepted: L1 = MPS MPL-AT2512-3R3 (LCSC/JLC C3224274), second source MPS
  MPL-AL4020-3R3 (own footprint); rev-A is built with both dot orientations. BOM row L1 `approved`.
  Nothing is purchased by the agent.
- Options rejected: HRO as main USB-C part (temperature rating); YXC X322512MSB4SI crystal (ESR, CL); TVS on T+/T−.
- Consequences: all BOM rows `approved` (L1 since D-007); phase 5 writes constraints for the approved parts and
  for the P4-4b recommendation as draft.
- PR / ref: local merge of `phase/parts` into `main` (no remote)
- Supersedes: D-004 in part (A2-5 USB-C part: HRO → SHOU HAN main, HRO alternate)

## D-007: Phase 5 constraints review answers (phase 5)   (2026-10-15, phase 5)
- Decided by: owner, answers to P4-4b and P5-2 … P5-8 (STATUS.md). Gate stays `in_review`:
  P5-1 (line-by-line review) is delegated to Reviewer-A (`docs/review-constraints-reviewer-a.md`).
- Decision:
  - P4-4b: accept MPL-AT2512-3R3 as L1, second source MPL-AL4020-3R3; rev-A built with both orientations.
    Finalizes the D-006 amendment; L1 `approved` in `bom/bom.csv`.
  - P5-2: R17 560 kΩ removed (no source; Pico 2 W 560K is its RT6154 FB divider).
  - P5-3: R22 470 Ω LED resistor kept.
  - P5-4: second 4.7 µF on DVDD at pin 23 added (RP2350 p.455), provisional ref C28.
  - P5-5: Q1 (ADC3 FET) gate tied to 3V3.
  - P5-6: 4.7 µF and 10 µF moved to 0603, in-stock JLC basic parts: CL10A475KO8NNNC (C19666, 16 V X5R) and
    CL10A106MA8NRNC (C96446, 25 V X5R); derating per S3-7 (see Consequences).
  - P5-7: crystal pads 2/4 to GND; USB-C shell to GND via the 4 tab pads.
  - P5-8: datasheet conflicts accepted as resolved in `parts/constraints/RP2350A.yaml`.
- Options rejected: keep R17; lower LED resistor; gate Q1 from a GPIO; shell via RC; external 1.1 V LDO route as the
  primary DVDD supply.
- Amended by D-009 (P5-13, owner 2026-10-15): L1 MPL-AT2512-3R3 is a documented rev-A deviation (reference part
  AOTA-B201610S3R3-101-T; layout deviates from RP2350 Fig. 23; shielding not stated by MPS), built in both
  orientations; the external 1.1 V DVDD route (RP2350 Fig. 21 p.452) is kept as a DNF fallback footprint, not rejected.
- Consequences: constraints files and `bom/bom.csv` updated; S3-7 voltage/temperature met. DC-bias capacitance
  read from the Samsung curves (ESTIMATE): 4.7 µF ≈ 4.5 µF at 1.1 V (C_OUT, C28 OK), ≈ 3.2 µF at 3.3 V (C_IN,
  below 4.7 µF if effective); 10 µF ≈ 4.8 µF at 5 V (C20 near TPS63001 4.7 µF min), C21+C22 ≈ 13.4 µF at 3.3 V
  (< 15 µF nominal). Raised as open item P5-10; not decided by the agent.
- PR / ref: branch `phase/constraints` (local)
- Supersedes: D-006 in part (amendment finalized; R17 row removed; C16–C22 package)

## D-008: P5-10 DC-bias derating: add one capacitor at each derated spot (phase 5)   (2026-10-15, phase 5)
- Decided by: owner, answer to P5-10 only. P5-9, P5-11, P5-12, P5-13 stay open; gate stays `in_review`.
- Decision: add one capacitor at each of the three spots, same 0603 JLC basic parts as D-007 (provisional refs):
  - RP2350 VREG input: C29 4.7 µF CL10A475KO8NNNC (C19666) in parallel with C16 (C_IN ≥ 4.7 µF, RP2350 p.455).
  - TPS63001 input: C30 10 µF CL10A106MA8NRNC (C96446) in parallel with C20 (≥ 4.7 µF, SLVS520C p.12).
  - TPS63001 3V3 output: C31 10 µF CL10A106MA8NRNC, third Cout with C21/C22 (15 µF nominal, p.12).
- Options rejected: accept the derated values (RPi/TI values read as nominal); upsize to larger packages/values.
- Consequences (ESTIMATE, Samsung DC-bias curves, both reads): C_IN 6.4–6.6 µF typ, ≈ 5.1 µF worst;
  TPS63001 Cin 8.8–9.6 µF typ, ≈ 6.7 µF worst; Cout 18.6–20.1 µF typ (≈ 15 µF at −20 % tolerance). Details in
  `parts/selection.md` § D-008. +≈ $0.095/board at 100. New open item P5-14 (VBUS inrush with C30 behind D1).
  RP2350A.yaml and TPS63001DRCR.yaml changed after Reviewer-A's review: the review gate needs re-verification.
- PR / ref: branch `phase/constraints` (local)
- Supersedes: D-007 in part (C16–C22 group counts)
- Amended by D-009 (P5-14, owner preference for one capacitor): C20 + C30 (2 × 10 µF 0603) replaced by ONE C20
  10 µF 50 V X5R 1206 CL31A106KBHNNNE (LCSC C13585, JLC basic); C30 removed. TPS63001 Cin ≈ 7.5 µF typ at
  5.25 V, ≈ 6.1 µF worst (ESTIMATE). C29 and C31 unchanged.

## D-009: P5-9, P5-11, P5-12, P5-13 answers; P5-14 single TPS63001 input capacitor (phase 5)   (2026-10-15, phase 5)
- Decided by: owner, 2026-10-15. Gate stays `in_review` (Reviewer-A re-verifies the changed constraints files).
- Decision:
  - P5-9: MAX31856 DRDY/FAULT: no pull-up fitted; DNF 10 kΩ pull-up footprints to 3V3 at the test pads (R23, R24,
    provisional refs); no wire-OR; drive type confirmed on rev-A.
  - P5-11: ADC_AVDD capacitor C27 = 4.7 µF (CL10A475KO8NNNC, 0603 16 V), as both RPi schematics, checked by the agent
    on the drawings: Pico 2 datasheet Fig. 11 p.20 C13 4u7, Pico 2 W schematic p.1 C13 4u7 (both on the R9 / ADC_AVDD
    node). The Pico 2 datasheet text p.14 ("201 Ω into 2.2 µF") is not followed.
  - P5-12: PCC-SMD polarity is defined by the Omega drawing (PCC-SMD p.2, assembly top view and FRONT PANEL DESIGN
    view): looking at the board edge from outside, component side up, + is the right clip and − the left clip.
    Recorded with the orientation reference in `parts/constraints/PCC-SMD.yaml`; footprint and silkscreen follow it.
    No question to Omega. Magnet check and warm-tip check stay in the bring-up plan as sanity tests only.
  - P5-13: amends D-007: L1 MPL-AT2512-3R3 is a documented rev-A deviation, both orientations built, external
    1.1 V DVDD supply kept as a DNF fallback footprint (RP2350 Fig. 21 p.452).
  - P5-14 (capacitor part only; the USB inrush question stays open): one larger TPS63001 input capacitor instead of
    C20 + C30: C20 = CL31A106KBHNNNE 10 µF 50 V X5R 1206 (LCSC C13585, JLC basic, JLC stock 2 346 959 on 2026-10-15).
- Options rejected: Omega question for P5-12; two 0603 input capacitors (D-008); 22 µF 0805 (more charge, JLC stock 0
  for CL21A226MAQNNNE on 2026-10-15 via LCSC).
- Consequences (ESTIMATE, Samsung curves): C20 −24.8 % at 5.25 V → 7.5 µF typ, ≈ 6.1 µF worst (−10 % tolerance,
  ≈ −10 % at 85 °C) ≥ 4.7 µF (SLVS520C p.12). USB 2.0 check (spec text in `datasheets/USB-2.0-Spec.pdf`): no single
  input capacitor meets §7.2.4.1, because the 3V3 capacitance charged through the TPS63001 soft start (400 mA
  average start limit, SLVS520C §7.4.1 p.9) alone is ≈ 51–56 µC, more than the 10 µF × 5 V = 50 µC of the
  permitted load; and C19 10 µF ±20 % exceeds C_RPB max 10 µF near 0 V. Open item P5-14 (owner): surge limiting
  and C19 value. Details in `parts/selection.md` § D-009.
- PR / ref: branch `phase/constraints` (local)
- Supersedes: D-007 in part (P5-13 wording), D-008 in part (C20 + C30)

## D-010: P5-14 USB 2.0 inrush: documented rev-A deviation (phase 5)   (2026-10-15, phase 5)
- Decided by: owner, answer to P5-14. Closes the last phase 5 owner item; gate stays `in_review` until
  Reviewer-A's re-verification passes.
- Decision: accept for rev-A that pico-k exceeds the USB 2.0 attach load (§7.2.4.1 p.177: "10 µF in parallel with
  44 Ω", including "capacitive effects visible through the regulator"; C_RPB 1.0–10.0 µF over 0–5.25 V, Table 7-7
  p.179 and Device Capacitance ECN p.2). ESTIMATE ≈ 132–137 µC attach charge vs 50 µC (D-009 analysis,
  `parts/selection.md`). No load switch; C19 stays 10 µF 0603. Also accepted: C19 alone (10 µF ±20 %, up to 12 µF
  near 0 V bias) exceeds the 10 µF C_RPB max by itself.
- Verification: bring-up plan §2a "USB attach VBUS droop": scope on VBUS at the host/hub port, worst-case host
  (bus-powered hub), 10 hot-plugs; pass = droop ≤ 330 mV (§7.2.4.1) and no other hub device disconnects.
- Rev-B action if it fails: slew-rate-controlled load switch between VBUS and VSYS (ramp ≥ 3 ms) and C19 → 4.7 µF
  (CL10A475KO8NNNC).
- CE/EMC/manual: not a CE/EMC/LVD/GPSR requirement; no manual warning. No USB-IF certification and no USB logo or
  "USB compliant" claim while the deviation stands (`docs/safety.md` certification path, item 4).
- Options rejected: load switch on rev-A; C19 → 4.7 µF on rev-A.
- PR / ref: branch `phase/constraints` (local)
- Supersedes: none (closes P5-14 left open by D-008/D-009)

## D-011: Phase 5 gate closed (phase 5)   (2026-10-15, phase 5)
- Decided by: owner, standing rule to close the gate once Reviewer-A passes (2026-10-15).
- Decision: phase 5 approved. Reviewer-A's independent review (owner-delegated, D-007 P5-1) passed with nits at
  25924e5 (files_hash c9a92462...bfd1, independence level 3). Nits N1-N3 fixed post-review (f25334f, recorded as
  `fixed-post-review`); H1 not reproduced, H2/H3 done. All 13 `parts/constraints/*.yaml` set to
  `review.status: reviewed` (reviewer Reviewer-A, owner-delegated). `ohmai check constraints`: PASS (WARN only for the
  recorded post-review nit fixes and review-metadata changes).
- Options rejected: a third full re-verification for the three nits.
- Consequences: phase 6 (RFQ) proposed "not applicable for rev-A" (no open supplier questions), pending owner OK;
  phase 7 (schematic) starts on `phase/schematic`.
- PR / ref: local merge of `phase/constraints` into `main` (no remote)
- Supersedes: none

## D-012: Phase 7 owner answers P7-1 … P7-8, friction fixes, commit trailers (phase 7)   (2026-10-15, phase 7)
- Decided by: owner, approval of all phase 7 recommendations (2026-10-15) plus steering on schematic
  style and commit trailers the same day.
- P7-1: J2 (T+) / J3 (T−) Omega PCC-SMD drawn with the official `Connector_Generic:Conn_01x01`, one per clip, mapped
  in `parts/symbol-maps/PCC-SMD.yaml` (pin 1 `Pin_1` → datasheet CONTACT, PCC-SMD p.1). Polarity per D-009 (P5-12).
  The custom footprint is a phase 8 item, built from the Omega p.2 drawing with a footprint check (no invented
  dimensions; every dimension cited).
- P7-4: per-part symbol maps in `parts/symbol-maps/<constraints stem>.yaml` (OhmAI tool change), separate from the
  reviewed constraints, which stay untouched. Constraints bind by `MPN` field or reference, not value substring.
  **LED finding (checked first, as asked):** KT-0805G datasheet p.2 "2. Package Profile & Soldering PAD Suggested":
  pad ① = + (anode), pad ② = − (cathode), green mark at the cathode end. KiCad `Device:LED` pin 1 = K, pin 2 = A,
  and `LED_SMD:LED_0805_2012Metric` pad 1 = cathode. The schematic has D2.1 (K) on GND and D2.2 (A) on LED_A
  (R22 → GPIO25): **electrically correct**. Only the pad numbering is reversed versus the datasheet, so the symbol
  map is KiCad 1 → datasheet 2 (K), KiCad 2 → datasheet 1 (A). Assembly must orient D2 by the cathode mark:
  phase 8 CPL/rotation check.
- P7-5: OhmAI passives semantics fixed with tests, no constraints edits: rail decoupling counts one cap per supply
  pin on the rail (not the rail sum), `nominal` without `max` is not a maximum (caps: a minimum; R/L: ±5 %),
  required parts on a neighbour net are found through the series part the pin also requires.
- P7-2: W25Q32RVXHJQ drawn with the official `Memory_Flash:W25Q32JVZP` stand-in, mapped in
  `parts/symbol-maps/W25Q32RVXHJQ.yaml` (pins 4 GND→VSS, 7 per §3.3 p.5).
- P7-3: generic official symbols accepted (Y1, D1, D2, L1/L2, SW1, J4, JP1-4, TP, NT1), with symbol maps where names
  or numbers differ (ABM8-272-T3, MPL-AT2512-3R3, TS-1187A-B-A-B, TYPE-C-16PIN-2MD-073, TPS63001DRCR, KT-0805G).
- P7-6: external 1.1 V fallback per RP2350 datasheet §6.3 p.451 text and Fig. 21 p.452 ("Connect VREG_FB directly to
  ground", inductor omitted, VREG_VIN/VREG_AVDD still powered): U1.50 VREG_FB on its own net with JP5
  (SolderJumper_2_Bridged, VREG_FB–DVDD, normal build) and JP6 (SolderJumper_2_Open, VREG_FB–GND, fallback). Fallback
  procedure: remove L1, cut JP5, bridge JP6, feed 1.1 V into TP7 (DVDD); firmware must then set the VREG HIZ bit
  (p.452: the regulator powers on and draws ≈ 400 µA until shut down). No new BOM part (jumpers are copper); an
  on-board DNP 1.1 V LDO footprint is NOT drawn (open question P7-9).
- P7-7: phase 6 (RFQ) not applicable for rev-A.
- P7-8: agent choices accepted; Reviewer-A's schematic review checks them.
- Friction 4: KiCad library version pinned (`ohmai.yaml` `kicad.libraries: "9.0.9.1"`), per-project
  `hardware/sym-lib-table` / `fp-lib-table` (`ohmai kicad-libs tables`), check `kicad-libs`.
- Friction 5: the `review:schematic` gate is reported separately from the work checks.
- Schematic style (steering): datasheet-figure layouts in `hardware/gen/layout/*.yaml`, drawn by
  `ohmai schematic build` with real wires; labels only for inter-block hierarchical ports; new `readability` check.
  The old `hardware/gen/*.py` draft generator is retired.
- Commit trailers (steering): every commit on a phase branch carries a well-formed `OhmAI-Author:` trailer
  (commit-msg hook installed, `ohmai check commits` in every phase and the review gate). Cutoff
  `commits.trailer_required_since` = 2398d87 (phase/schematic HEAD when the rule started); history not rewritten.
- PR / ref: branch `phase/schematic` (local)
- Supersedes: none (answers P7-1 … P7-8)

## D-013: P7-9 1.1 V fallback stays off-board; Reviewer-A reviews the schematic (phase 7)   (2026-10-15, phase 7)
- Decided by: owner (2026-10-15), approving both P7-9 and the reviewer selection.
- Decision 1 (P7-9): the external 1.1 V DVDD fallback stays an off-board feed into TP7 (DVDD) with JP5 (bridged,
  VREG_FB–DVDD) / JP6 (open, VREG_FB–GND), per RP2350 datasheet §6.3 p.451 and Fig. 21 p.452. No on-board DNP
  1.1 V regulator on rev-A. When the fallback is used, firmware must set the VREG HIZ bit (p.452: the regulator
  powers on and draws ≈ 400 µA until shut down). Procedure in `test/bringup-plan.md` §2a.
- Decision 2: Reviewer-A (independent reviewer) reviews the schematic gate; review file `reviews/schematic/reviewer-a.md`
  with the YAML header (vendor, model, independence level), brief `reviews/schematic/BRIEF.md`.
- Options rejected: on-board DNP 1.1 V LDO footprint on rev-A (rev-B option if the fallback is ever needed).
- Consequences: P7-9 closed; P7-10 stays a phase 8 carry-over (D2 orientation by the KT-0805G cathode mark p.2 in
  the CPL check; PCC-SMD footprint from Omega p.2 with cited dimensions; empty footprints J1, U2, L1, L2, J4, J2/J3).
- PR / ref: branch `phase/schematic` (local)
- Supersedes: none (closes P7-9 left open in D-012)

## D-014: TP5 on the LED anode; KiCad application version pinned (phase 7)   (2026-10-15, phase 7)
- Decided by: owner, confirmation to apply both changes (2026-10-15) to Reviewer-A's schematic review questions F8/F9
  and F18 (`reviews/schematic/reviewer-a.md`).
- Decision 1 (F8/F9): TP5 moves from GP25 (U1.37, before R22) to LED_A (LED anode, between R22 and D2), as on
  Pico 2 (Pico 2 datasheet §3.1 p.9: TP5 "GPIO25/LED", "will only swing from 0V to the LED forward voltage";
  Pico 2 Fig. 11 p.20), keeping test pads "as Pico 2" (D-002). TP5 is now drawn on sheet 6 (led_boot_adc) at
  the R22/D2 node; expected_nets.csv updated.
- Decision 2 (F18): the KiCad application (kicad-cli) is pinned to 9.0.x as well as the libraries (9.0.9.1,
  D-012 friction 4): `ohmai.yaml` `kicad.app: ">=9.0.2,<9.1"`, checked by `ohmai check kicad-app` (OhmAI 9f48356;
  FAILs outside the range). Local kicad-cli is 9.0.2.
- Options rejected: TP5 on GP25 (differs from Pico 2); libraries-only pin (a 9.1 app could rewrite the files).
- Consequences: Reviewer-A F8/F9/F18 resolved; Reviewer-A re-checks F1–F3 and the D-014 changes on the new brief.
- PR / ref: branch `phase/schematic` (local)
- Supersedes: none

## D-015: Bring-up gate requires a human sign-off (phase 12 config, set in phase 7)   (2026-10-15, phase 7)
- Decided by: owner, 2026-10-15.
- Decision: the bring-up review gate requires a human reviewer (`ohmai.yaml` `reviews.gates.bringup.require_kind:
  human`, OhmAI e7cca73), since it signs off measurements on a real board. A human who did not author the files in
  scope signs; the owner may sign (agents author the bring-up plan and manual). An agent review alone FAILs the gate.
- Safety gate unchanged: independent agent review + owner approval.
- Consequences: `ohmai check review:bringup` FAILs without a valid `kind: human` review file.
- PR / ref: branch `phase/schematic` (local)
- Supersedes: none

## D-016: Schematic gate approved; Reviewer-A's level-3 independence accepted for this gate only (phase 7)   (2026-10-15, phase 7)
- Decided by: owner, 2026-10-15.
- Decision: accept Reviewer-A's independence level 3 for the phase 7 `review:schematic` gate (configured minimum level 2),
  for Reviewer-A's re-verified review on files_hash sha256:a052ad17...bea only; merge phase 7. Reason: owner decision.
- Alternatives tried (recorded in `reviews/schematic/resolutions.md` `accepted_independence`): level 1 (different
  vendor's model) and level 2 (different model) reviewers are not set up in this environment; a cloud agent on a
  different model was possible, but the owner chose to accept Reviewer-A.
- Scope: this gate and this hash only. OhmAI defaults, the template and pico-k's ohmai.yaml gate config are
  unchanged (schematic still requires level 2); any new hash or other gate needs level 2 again (OhmAI d7b62b3).
- Consequences: `ohmai check review:schematic` PASSes with a WAIVED note; gate approved; phase 8 (layout) opens.
- PR / ref: merge `phase/schematic` into `main` (local, no remote)
- Supersedes: none


## D-017: Phase 8 milestone-1 answers: no mounting holes, end-pin half-holes removed, P8-3..P8-6 accepted   (2026-10-16, phase 8)
- Decided by: owner, 2026-10-16 (P8-1 a, P8-3..P8-6 as recommended; P8-2 "if a compliant option exists
  that keeps drop-in compatibility, apply it"). The P8-2 option below was found and applied by the agent under that
  instruction; the owner can still overrule it in the layout gate.
- Decision:
  - **P8-1 (a):** no mounting holes. H1/H2 removed from the schematic (sheet 5) and the board; R-05 amended. The Pico 2
    USB-end holes (Fig. 3 p.7: Ø2.1 at x 4.8/16.2, 2.0 from the edge) overlapped the USB-C shell-tab copper by 0.17 mm.
  - **P8-2:** keep the Pico 2 pin positions and the 51 × 21 outline; the 4 end pins (1, 20, 21, 40) have **no
    castellated half-hole**. Each keeps its 1.0 mm PTH, Ø1.6 pad, and top and bottom pads out to 0.2 mm from the
    long edge, so a carrier with the Pico 2 Fig. 5 p.10 SMT footprint still lands on them. JLC still confirms in the
    quote.
  - **P8-3:** PCC-SMD rear slot non-plated, as drawn (PCC-SMD p.2).
  - **P8-4:** clip tab depth on 1.0 mm accepted; fit checked on the first boards (bring-up).
  - **P8-5:** test-point mapping TP1–TP7 at the Fig. 5 p.10 positions (pad functions are an ESTIMATE), SWD on TP8–TP10.
  - **P8-6 (i)–(iii):** the layout deviations listed in STATUS (VREG_FB via to JP5; C22/C31 placement; C21 next to VOUT).
- P8-2 finding (sources fetched 2026-10-16):
  - JLC PCB capabilities page (jlcpcb.com/capabilities/pcb-capabilities, "Castellated Holes"): hole Φ ≥ 0.5, "Hole to
    board edge (L): ≥ 1 mm", hole to hole ≥ 0.5. The drawing measures L from the castellation to the board edge at a
    right angle to the castellated edge, i.e. the short edge for our long-edge rows.
  - JLC blog "Castellated PCBs: Introduction and Design Requirements" (updated 2026-09-08), Fig. "design requirements":
    A. castellated **pad edge** to board edge ≥ 1 mm; B. hole ≥ 0.6; C. hole edge to hole edge ≥ 0.6; D. annular ring
    0.25 (≥ 0.18). Table 2: hole to **board corner** ≥ 3.0 mm (5.0 recommended); pad inward extension ≥ 0.5 (0.8
    recommended). So the rule is on the pad edge, and a separate corner rule is on the hole.
  - Pico 2 end pins sit 1.37 from the short edges ((51 − 48.26)/2, Fig. 3 p.7). With pad Ø1.6, the pad edge is 0.57
    (rule A short by 0.43). Hole edge to corner is 0.87 (corner rule short by 2.13).
  - Growing the outline: the Pico 2 datasheet gives 51 × 21 × 1 mm (p.7) with no outline tolerance (the only tolerance
    on Fig. 3 is the Ø2.1 ± 0.05 holes). Rule A needs +0.43 per end (51.86 mm) and the corner rule +2.13 per end
    (55.26 mm). Both are far beyond JLC's own routed-outline tolerance (±0.2 regular / ±0.1 precision,
    capabilities page) and would not drop into a Pico 2 carrier cut-out. Rejected.
  - Shifting the outline: both ends are symmetric (1.37 each), so any shift fixes one end and breaks the other.
    Rejected.
  - Applied option: drop the half-hole on pins 1/20/21/40. The nearest castellations (pins 2/19/22/39) then sit
    3.91 from the short edge. Pad edge 3.11 ≥ 1.0 ✓; hole edge to corner 3.41 ≥ 3.0 ✓ (5.0 recommendation not met);
    hole edge to hole edge 1.54 ≥ 0.6 ✓; annular ring 0.30 ≥ 0.25 ✓; pad reaches 2.41 inward ≥ 0.8 ✓.
  - Trade-off: pins 1 (GP0), 20 (GP15), 21 (GP16) and 40 (VBUS) have no edge fillet. When the board is soldered
    flat onto a carrier, those 4 joints are under the board and cannot be inspected. Pin headers are unaffected.
- Alternatives: keep all 40 half-holes and ask JLC in the quote (milestone-1 recommendation; risk of a rejected order
  or of the routed edge tearing the end pads); a longer outline; a shifted outline (both rejected above).
- Scope: rev A board, layout phase. R-05 amended (requirements.md). The castellation rule is still confirmed with JLC
  in the quote (owner action).
- Consequences: J4 footprint has 36 castellated pads; BOM/requirements unchanged apart from R-05; H1/H2 gone from the
  netlist (88 parts). The USB-end corners are free for C20/D1.
- PR / ref: branch `phase/layout` (local)
- Supersedes: amends D-001 (Q2)/D-002/D-004 on R-05 (mounting holes)

## D-018: Routing plan P8-7 (a): move the U1 decoupler rows outward   (2026-10-16, phase 8)
- Decided by: owner, 2026-10-16.
- Decision: move the U1 decoupling rows 0.6–1.0 mm outward (as little as works) to open escape channels. Each part
  stays as close as possible to the pin it serves and keeps its pin assignment. Then fanout, Freerouting 2.1.0 (pinned,
  GUI off, analytics off, no network), SES import, starved-thermal fixes, DRC 0 errors / 0 unconnected.
- Constraints: no Freerouting upgrade, no signals on inner layers, no via-size change without asking. Stop after a
  couple of placement tweaks if routing does not converge, and report the best result plus the options.
- Alternatives: (b) signals on In2 (3V3 plane split), (c) Freerouting ≥ 2.2 (Java 25), (d) 0.3/0.15 vias. Not chosen.
- Scope: phase 8 placement around U1 (placement.yaml), routing scripts.
- Consequences: decoupler-to-pin distance grows by the move (cited per part in placement.yaml).
- PR / ref: branch `phase/layout` (local)
- Supersedes: none
- Outcome (2026-10-16, agent): not applicable as decided: no row has 0.6 mm free outward (left: flash U2 / J4 strip; right: C18/C27 0603 / J4 strip; top: C7 / JP5-JP6; bottom: C3 0.46 mm max, C9 0). Experiment with C18/C27 as 0402 + channel keepout: 49 unconnected, not closed. Placement left unchanged; question raised as P8-8 (STATUS).

## D-019: P8-8 (c): Freerouting 2.2.x on Java 25, after testing   (2026-10-16, phase 8)
- Decided by: owner, 2026-10-16.
- Decision: move Freerouting from the pinned 2.1.0 to the latest stable 2.2.x after the OhmAI tier-1 update tests,
  with OpenJDK 25 (25.0.4.1) side by side with Java 21. Route from the committed placement (69ce528 base, no D-018 cap
  move), GUI off, analytics off, no network. Fix the starved thermals and the GP14-J3 hole clearance; DRC 0 / 0.
- Constraints: no inner-layer signals, no via-size change, no U2 move without asking. Stop after a few runs if 2.2
  does not converge and report the best result against 2.1.0.
- Applied (agent): Freerouting 2.2.4 (latest 2.2.x; 2.3.0/2.4.1/2.5.0 exist but are outside the decision),
  jar sha256 f5ed374182900ccc78e473518bbb9f6b869f4a07159495f663a76f52bb10523b = GitHub release digest;
  Java: Debian openjdk-25-jre-headless 25.0.4.1+1-1~deb13u1 (deb sha256 3264ef0e…c0b3) extracted to
  .toolcache/jdk25 (no system install). Lock moved by `ohmai upgrade` (2056a83) after known-bad 30/32
  (2 SKiDL cases skipped, SKiDL not installed), golden ldo-led PASS, canary (match-app, libs 9.0.9.1) clean; no
  OhmAI suite exercises Freerouting, so the upgrade is explained by a same-DSN comparison: 2.1.0 best 55 unrouted,
  2.2.4 best 35 (3 min, 7 threads).
- Version check / analytics: 2.2.4 starts `VersionChecker` (api.github.com) unconditionally (Freerouting.java
  v2.2.4, main); analytics have `usage_and_diagnostic_data.disable_analytics` and `profile.allow_telemetry`. Both
  off; runs stay inside `unshare -rn` because the crash path still tried an analytics delivery.
- Alternatives: (a) 0402 C18/C27 + right column move, (b) signals on In2, (d) smaller vias, (e) manual finish,
  (f) U2 move: not chosen (P8-8).
- Scope: toolchain.lock.yaml, hardware/gen/pcb/route.py, routing. PR / ref: branch `phase/layout` (local); OhmAI
  branch `feat/freerouting-2.2` (local, not merged).
- Supersedes: the "Freerouting 2.1.0 unchanged" constraint of D-018.

## D-020: P8-8 (b): signals allowed on In2 (3V3), pour kept around them   (2026-10-16, phase 8)
- Decided by: owner, 2026-10-16.
- Decision: the autorouter may use In2 (3V3 plane layer) for signals; the 3V3 pour stays on In2 and flows around
  them. In1 (GND) stays a solid plane with no signals. Prefer short In2 stubs; the 3V3 pour must stay connected (no
  3V3 islands) and the decouplers and U1/U3 must still reach it with low impedance. Keep USB D+/D- off In2 if
  possible.
- Constraints: start from b71be51 with Freerouting 2.2.4 (pinned, GUI off, analytics off, no network); runs end on
  a pass count; commit after each run. Fix the starved thermals and the GND/3V3 pads without a via; DRC 0 / 0. A few
  open nets may be finished by hand in pcbnew (short, DRC-clean); stop and report if many stay open.
- Alternatives: P8-8 (a) 0402 C18/C27, (d) smaller vias, (e) hand-finish all, (f) U2 move. Not chosen.
- Scope: hardware/gen/pcb/route.py (DSN layers, layer costs, USB layer restriction), routing, In2 zone.
- PR / ref: branch `phase/layout` (local).
- Supersedes: the "no inner-layer signals" constraint of D-018 / D-019.

## D-021: rework the placement around U1 (RP2350) for escape channels   (2026-10-16, phase 8)
- Decided by: owner, 2026-10-16.
- Decision: the routing failures (D-018 … D-020) come from the placement, so the placement around U1 is reworked:
  an escape channel of about 1 via pitch on every side of U1; the flash U2 moved off the left side, with short,
  matched QSPI routes; the decoupler columns spaced out, each cap still as close as possible to its own pin (bottom
  side under U1 allowed if it helps). Keep the 51 x 21 outline, the castellation / pin positions, the connector on
  top and the locked BOM (no part changes without asking).
- Constraints: D-020 In2 exception stays but minimal (3V3 pour one connected piece, In1 GND solid). placement.yaml
  changes through the generator; Freerouting 2.2.4 (pinned, GUI off, analytics off, no network, end on a pass
  count); commit after each step; fix starved thermals and via-less pads; DRC 0 / 0 (a few nets by hand allowed);
  stop and report if it does not converge after a few placement iterations.
- Agent note: "bottom side under U1" conflicts with R-07 (bottom side flat, no parts, so the module can be
  reflowed by its castellations). Not used unless the owner amends R-07.
- Alternatives: P8-8 (a) 0402 C18/C27, (d) smaller vias, (e) hand-finish. Not chosen.
- Scope: hardware/gen/pcb/placement.yaml, fanout/route, routing. PR / ref: branch `phase/layout` (local).
- Supersedes: the U1-area positions of the phase-8 placement (69ce528).
- Outcome (2026-10-17): 3 placement iterations (P1-P3, STATUS) did not converge (Freerouting 2.2.4: 22-26 open on
  F/B, 16-18 with In2 at the cost of a split 3V3 pour). Best D-020-clean board P2 kept. JP5/JP6 on the bottom
  (bare copper) needs the owner's reading of R-07.

## D-022: hand-route all remaining P2 connections (scripted)   (2026-10-16, phase 8)
- Decided by: owner, 2026-10-16.
- Decision: route all connections Freerouting left open on P2 (4b693fc) by hand, as a scripted, reproducible
  pcbnew step (hardware/gen/pcb/handroute.py), using the board design rules and short, direct routes; QSPI lengths
  reasonably matched and reported. Then fix the starved thermals and via-less pads; DRC 0 errors / 0 unconnected,
  only justified warnings.
- Constraints: R-07 kept (bottom flat, no parts); In1 GND solid; In2 3V3 pour one piece (short In2 stubs only if
  the pour stays connected). JP5/JP6 on the bottom (bare copper) accepted for now unless the owner objects.
- Alternatives: P8 options SW1 smaller (BOM), R-07 amendment, wider In2 use, 6 layers. Not chosen.
- Scope: hardware/gen/pcb/handroute.py (+ its route data), hardware/pico-k.kicad_pcb. PR / ref: `phase/layout`.
- Supersedes: the "a few nets by hand" limit of D-020 / D-021.

## D-023: longer In2 signal runs for the last D-022 connections (pico-k-only exception, extends D-020)   (2026-10-17, phase 8)
- Decided by: owner, 2026-10-17 (option (a) of the D-022 stop report, 21 unconnected).
- Decision: the remaining connections may use In2 (3V3 plane layer) for longer signal runs than D-020/D-022's
  "short stubs". Hard rule: the 3V3 In2 pour stays ONE connected piece; checked after every net (planes.py) and any
  net that splits it is rolled back. Pour neck width at least 0.5 mm everywhere, wider near U1 and the decouplers.
- Constraints: In1 (GND) stays solid, no signals. USB D+/D- never on In2. Routes stay scripted and replayable
  (handroute.py In2 mode). Everything else from D-022 stays.
- Exception: **pico-k only**, an exception to the D-020 "prefer short In2 stubs" rule; list it in the README
  exceptions summary. Not a template/skill default.
- Alternatives: placement change around the right passive columns / VSYS trunk (option b); signals on In1 (c, not
  recommended: breaks the solid GND plane). Not chosen.
- Scope: hardware/gen/pcb/handroute.py (+ handroute.json), hardware/pico-k.kicad_pcb. PR / ref: `phase/layout`.
- Supersedes: the D-022 In2 stub length cap (2.5 mm) for these connections.
- Outcome (2026-10-17, agent): 21 -> 9 unconnected with In2 runs (74.1 mm, 8 nets), pour 1 piece, narrowest neck
  0.91 mm; the last 9 do not close without splitting/narrowing the pour or more room at the U1 east pins (STATUS).

## D-024: right passive column next to U1 shifted ~0.5 mm east (pico-k-only placement change)   (2026-10-17, phase 8)
- Decided by: owner, 2026-10-17 (option 1 of the D-023 stop report, 9 unconnected).
- Decision: move the right-hand cap/resistor column next to U1 (column A, x 15.84) about 0.5 mm east (outward) to
  give via room for GP22/26/27/28 at U1 pins 34 and 40-42; rip up and re-route only the affected area.
- Constraints: placement.yaml is the source (replay stays reproducible); courtyards clear, no new DRC errors; R-07
  (bottom flat, no parts); outline 51 x 21; D-023 In2 rules (In1 solid, no signals; In2 3V3 one piece, necks >= 0.5 mm,
  >= 0.8 mm near U1/decouplers; no USB/GND/3V3 on In2); QSPI lengths at or below the current values where possible.
- Exception: **pico-k only** placement change (not a template default).
- Alternatives: In2 necks below 0.5 mm for Q1-D (not chosen).
- Scope: hardware/gen/pcb/placement.yaml, handroute.json, hardware/pico-k.kicad_pcb. PR / ref: `phase/layout`.
- Outcome (2026-10-17, agent): **not applied**. The column has no room to move: column A courtyards end at x 16.81
  exactly where column B (C18, C27 0603 r90; R19) starts, and column B ends at x 18.36, the start of the J4
  castellation strip. A +0.5 mm trial gave new courtyard overlaps C5/R5/R21-C18, C10/C4/R20-C27, R9/C6-R19
  (0.23-0.51 mm), so placement.yaml was reverted (board unchanged at 9 unconnected, 0 errors). Next option: C18/C27
  as 0402 (P8-8 (a) from D-020; BOM change, owner approval needed) frees ~0.53 mm for the shift.
- Outcome update (2026-10-17, owner via D-025): **now applies**. C18/C27 become 0402, which frees the room
  for the shift; placement.yaml and the re-route follow D-025.

## D-025: C18 and C27 4.7 µF 0603 → 0402 TDK105CBJ475MV-F (owner-approved BOM change)   (2026-10-17, phase 8)
- Decided by: owner: 0402 approved 2026-10-17 subject to a parity check; part chosen 2026-10-17
  (option 1 of the agent's  parity report).
- Decision: C18 (VREG_AVDD filter, 3.3 V) and C27 (ADC_AVDD filter, 3.3 V) change from CL10A475KO8NNNC (Samsung,
  0603, 16 V X5R ±10 %, LCSC C19666, JLC basic) to **TDK105CBJ475MV-F** (Taiyo Yuden, 0402 (1005), 4.7 µF 25 V X5R
  ±20 %, LCSC C22385335, JLC extended). Footprint Capacitor_SMD:C_0402_1005Metric. C16/C17/C28/C29 stay 0603.
- Reason: escape room for GP22/26/27/28 at U1 pins 34 and 40-42; the 0402 frees ~0.6 mm in column B so the D-024
  ~0.5 mm east shift of the right passive column fits without courtyard overlaps.
- Derating (curve reads, ESTIMATE): Taiyo Yuden AQC19J26-08D DC-bias curve about −42 % at 3.3 V → ≈ 2.7 µF typ,
  ≈ 2.2 µF at −20 % tolerance; the 0603 gave ≈ 3.2 µF typ (−32 %), ≈ 2.9 µF at −10 %. About −16 % typ effective
  capacitance; still 4.7 µF nominal as the RPi references (Pico 2 Fig. 11 C13, HDG). Owner accepts the lower effective
  capacitance and the JLC extended-part fee.
- Options considered (agent report): Chinocera HGC0402R5475M250NTEJ (C22367824) / M160NTEJ (C7432765) and
  Fenghua 0402X475K160NT (C20624278): no DC-bias curve published; CL05A475MP5NRNC (C23733, basic): 10 V, ≈ 2 µF at
  3.3 V; only C27 to 0402; keep 0603 with In2 necks < 0.5 mm. Not chosen.
- Scope: bom/bom.csv (new C18 C27 row), hardware/gen/layout/mcu_core.yaml + led_boot_adc.yaml (value/fp/MPN →
  regenerated sheets), datasheets/TDK105CBJ475MV-F.pdf (LFS), parts/selection.md, parts/constraints/RP2350A.yaml,
  hardware/gen/pcb/placement.yaml, handroute.json, hardware/pico-k.kicad_pcb. PR / ref: `phase/layout`.
- Amends: D-007 (P5-6) and D-009 (P5-11) part choice for C18 and C27 only. Makes D-024 apply.
- Outcome (2026-10-17, agent): applied. Column A at x 16.34 (+0.5 mm), C18/C27/R19 at x 17.84 (C27 rot 270
  so its GND pad faces south), no new courtyard overlaps, R-07 and the outline unchanged. GP22/26/27/28 now routed.
  Board 9 -> **6 unconnected**, 0 errors, 0 dangling; not yet clean (STATUS).
- Note (2026-10-17, owner): the C27 180° rotation (rot 270, GND pad south) is an ordinary placement tweak, accepted.

## D-026: Q1 (VSYS sense FET) next to U1's east side + hand-routing of the last links   (2026-10-17, phase 8)
- Decided by: owner, 2026-10-17 (option (b) + (c) of the D-025 stop report, 6 unconnected).
- Decision: move Q1 close to U1's east side so VSYS_SENSE (U1.43-R9.1, U1.43-Q1.2) and Q1-D (Q1.3-R19.2) become
  short; then hand-route the rest (move U1.45's 3V3 via, manual VREG_AVDD escape, 3V3 at U1.20, U3-VINA).
- Constraints: placement.yaml only; no courtyard overlaps; R-07; outline 51 x 21; Q1 sense circuit electrically
  identical; D-023 pour rules unchanged; replay rebuilds the board.
- Scope: hardware/gen/pcb/placement.yaml, handroute.py/handroute.json, hardware/pico-k.kicad_pcb. PR / ref: `phase/layout`.
- Outcome (2026-10-17, agent): **not applied**. No free F.Cu spot for Q1's SOT-523 courtyard (2.39 x 2.19 mm)
  anywhere east of x ≈ 4 mm: the band between U1 (courtyard to x 14.64) and the J4 strip (x 18.36) is filled by
  column A, column B, C29, L2, U3 and SW1 (y 27.13-32.82); the only free sites are next to Q1's present place on the
  west edge (x ≈ 3.8, y ≈ 21-25). Placement unchanged, board unchanged (6 unconnected, 0 errors, 0 dangling).
  Options in STATUS (owner decision).
- Outcome update (2026-10-17, owner via the parent session): **option 2 applied** (the Q1-east move was not
  possible): Q1 stays on the west edge (3.9, 16.6); R19 moves to (5.26, 14.56) rot 180 (pad 2 VSYS_DIV next to
  Q1.3) and R9 to (3.62, 20.41) rot 0 (below R4), both on free sites found by a courtyard scan. Electrically
  identical (R19 VSYS-VSYS_DIV, R9 VSYS_SENSE-GND). Only VSYS_SENSE still runs east to U1.43; the freed column
  room is used for the VREG_AVDD / ADC escapes; hand-routing of the rest as approved.
- Outcome update (2026-10-17, agent): hand-routing done except one link. Closed: VREG_AVDD / ADC escapes
  (freed column), U3-VINA (U3.9 GND tied straight into the exposed pad, its via removed; VINA U3.8 -> R14.2 on
  F.Cu), 3V3 U1.20 (F.Cu straight to its decoupler C3.1; the XIN/XOUT vias nudged ~0.1 mm; U1.23 DVDD now leaves on
  B.Cu to the bulk cap C28 with C9.2 GND tied into C28.2; C9/C28 joined to the DVDD trunk by a short In2 hop; the
  GP25 In2 jog moved 0.85 mm). Pour rules unchanged and met: In2 3V3 1 piece, narrowest neck 0.91 mm (0.91 near
  U1/decouplers), In1 no tracks. **Open: VSYS_SENSE R9.1 -> U1.43** (west edge to U1's east side): no path on
  F/B/In2 without rip-up; the rip-up the router needs (GP0-GP3, ADC_VREF, VBUS_SENSE, DVDD, JP5-A; 34 pads) fails
  on GP2, and an In2-cost-1 run splits the pour (D-023). Stopped there (owner instruction); options in STATUS.
- Outcome update (2026-10-17, agent; owner chose option 1): east-of-U1 rework done, board clean.
  VSYS_SENSE, VBUS_SENSE, ADC_VREF and Net-(JP5-A) (VREG_FB) ripped with their old copper removed (handroute
  `--rip` now also drops the nets' earlier records; it used to leave them, which made the earlier trial invalid).
  Kept: the ADC_VREF J4.35 link. New: ADC_VREF R21-R20 as manual `adc_vref_r21_r20` (B east under column A, F beside
  column B, In2 hop over GP26); JP6-JP5 1.96 mm B; VSYS_SENSE R9.1-U1.43 27.2 mm (3 vias, In2 3.6 mm); VBUS_SENSE
  R8-U1.36 26.4 mm. Result: 0 unconnected, 0 errors, 0 dangling (2 silk overlaps, justified); In2 3V3 1 piece, neck
  0.91 mm (0.91 near U1/decouplers), In1 no tracks, In2 signals 85.0 mm; QSPI unchanged.
  handroute fix: A* no longer stacks two vias of one path closer than hole-to-hole (0.45 mm centres), validate
  checks the new vias of a record pairwise (existing holes of every net were already checked).
  U1.23 DVDD decoupling (owner asked for C9 within 1-2 mm): **not possible with this placement**. C9 sits 1.96 mm
  from pin 23 (straight line), but the crystal pins 21/22 lie between pin 23 and C9.1 and C9.2 (GND) is directly
  under pin 23. A direct F.Cu link has to cross the XIN/XOUT stubs. Rotating C9 180 deg (DVDD under pin 23, 0.85 mm
  stub) leaves the XIN and XOUT vias a band of y 127.20-127.36 between the U1 pads and C9 (pad gap 0.12 mm). There
  XOUT has to stay at x <= 110.02 (clear of the DVDD stub) and XIN at sum x+y >= 236.91 (clear of the U1.20 3V3 track).
  That leaves 0.46 mm between them, and they need 0.58 mm (hole-to-hole + clearance). The 3V3 track cannot move
  further west (pad 19), and a U1.20 3V3 via would collide with XIN again. A B/In2 hop into C9.1 has no via site:
  C3.2/C28.2/R3 pads and the GND via at 108.74,128.63 leave none within reach. Moving C9 is not possible either
  (courtyards: C3 west, C28 south, SW1 from x 110.75 east, U1 north; free-area scan). So U1.23 still reaches its
  nearest decoupler C28.1 over 5.35 mm (2 vias), and C9.1 over ~8.6 mm. A real fix needs a placement change around the
  crystal/C9/C28 group (owner decision).
- Outcome update (2026-10-17, agent): the two silk overlaps (D2 bottom line vs the Y1 outline corner, 0.01 mm;
  C12 lower line vs the U5 pin-1 triangle) are cleared by placement nudges, not waived: D2 up 0.03 mm, C12 up
  0.07 mm (track ends stay inside the pads; replay rebuilds the board). Trimming the stock silk in build_pcb.py was
  tried and dropped: it raises lib_footprint_mismatch. DRC 0 violations; phase 8 checks PASS, creepage TODO;
  layout review brief written (no reviewer launched).

## D-027: U1.23 DVDD decoupler C9 directly under the pin (crystal corner placement rework)   (2026-10-17, phase 8)
- Decided by: owner, 2026-10-17: rework the crystal/C9/C28 placement so U1.23 DVDD gets a
  close decoupling cap, then reroute; start from 6b69169.
- Decision: C9 (100 nF 0402) turned vertical directly under U1.23, DVDD on F.Cu without a via; C28 (4.7 uF) moved
  down to make room. Crystal parts (Y1, R3, C23, C24) stay; XIN/XOUT keep their F stub + via + B run, vias moved.
- Constraints: placement.yaml only, no part/BOM change; no courtyard overlap; R-07 (bottom empty); outline unchanged;
  D-023 pour rules; 0 unconnected / 0 errors / 0 dangling; QSPI no longer; replay rebuilds the board.
- Scope: hardware/gen/pcb/placement.yaml, handroute.py (MANUAL) / handroute.json, hardware/pico-k.kicad_pcb.
- Options checked (free-area scan d025/free.py plus clearance arithmetic before routing):
  (1) C9 vertical under pin 23 with the XOUT via under pin 22 and XIN beside the U1.20 3V3 track: fits. With C9, C28,
      C3 and R3 lifted, the scan shows (10.24, 28.21) free for the 1.01 x 1.92 courtyard. SW1 (courtyard from
      x 10.75) caps the centre at x 10.24 and U1 (to y 27.145) sets the top. C9 at y 28.48 gives the XOUT via 0.195 mm
      to C9.1. C28 needs y >= 30.96 below it (bottom row at 32.78). **Chosen.**
  (2) Pin 20 3V3 inward to an In2 via, so that pins 19/21/22 fan out SW on F: needs the GP15 via, the BOOTSEL B run
      and the EP GND via moved, and IOVDD pin 20 would decouple through the plane only. Not taken.
  (3) XIN inward to a via under U1: its B run is boxed in by GP13/14/15 and BOOTSEL (crystal nets F/B only). Not taken.
  (4) SW1 elsewhere (to free the area east of pin 23): no free site for its 7.59 x 5.69 courtyard (scan: 0). Not possible.
- Outcome (2026-10-17, agent): applied. C9 rot 270 at (10.24, 28.48), C28 at (9.95, 30.96).
  - DVDD: U1.23 -> C9.1 0.87 mm pad edge to pad edge (pad centres 1.57 mm), F.Cu 0.15 mm, no via (was 5.35 mm to
    C28 over 2 vias). C9.1 joins the In2 DVDD trunk via west of C28 (manual dvdd_c9_c28), C28.1 the same via. C9.2 goes
    straight to C28.2 with a GND via east of them.
  - Crystal: XIN 11.96 mm, 2 vias (was 11.84); XOUT 5.73 mm, 2 vias (was 5.79); Y1 net from R3 8.12 mm unchanged.
  - Ripped only the corner (data only, d027/rip.py): base XIN/XOUT/DVDD/GND items in 108.9-111.0 x 126.9-132.0 and
    4 hand-route records. The DVDD trunk record keeps its In2 run.
  - Result: DRC 0 violations, 0 unconnected, parity 0. In2 3V3 1 piece, 773.83 mm2, neck 0.91 mm (0.91 near
    U1/decouplers), In2 signals 85.0 mm (no USB/GND/3V3), In1 no tracks. QSPI unchanged.
  - Replay rebuilds the board (reorder-only diff). One replay of five segfaulted inside pcbnew; rerunning was clean.
  - Still open (owner): XIN is long because Y1.1 is the far corner of the crystal. Rotating/moving Y1 is a separate
    placement change.

## D-028: Layout gate reviewer: Reviewer-A, level-3 independence accepted for this gate and hash only   (2026-10-17, phase 8)
- Decided by: owner, 2026-10-17.
- Decision: Reviewer-A reviews the phase 8 `review:layout` gate. The owner accepts Reviewer-A's independence level 3
  (configured minimum level 2) for this gate and for files_hash sha256:c71de844... (reviews/layout/BRIEF.md) only.
- Alternatives considered: a level 1 (other vendor) or level 2 (other model) reviewer through a cloud agent. That
  was possible, but it uses the cloud agent allowance before its monthly reset, so the owner chose Reviewer-A.
- Scope: this gate and this hash only. OhmAI defaults, the template and pico-k's ohmai.yaml gate config are unchanged
  (layout still requires level 2). Any new hash or other gate needs level 2 again, unless the owner decides
  otherwise. Record it in reviews/layout/resolutions.md `accepted_independence` when the review is in.
- Same pattern as D-016 (schematic gate).
- PR / ref: branch `phase/layout` (local).
- Supersedes: none.
- Extended by owner (2026-10-24, with D-030): Reviewer-A level-3 independence waiver also approved for the D-030 board `files_hash sha256:a0379e7200f2f84a047c679ac618166c6366c3289b1f607eb6a640d6da34d530` (recorded in `reviews/layout/resolutions.md` `accepted_independence`).

## D-029: Reviewer-A L1 (TPS63001 input cap C20) deferred; reviewed board kept   (2026-10-23, phase 8)
- Decided by: owner, 2026-10-23 (after the intermediate iterations below).
- Decision: the board stays as Reviewer-A reviewed it (3e2d005, `hardware/pico-k.kicad_pcb` sha256 2d0f674a54a7…,
  files_hash sha256:c71de844…). Reviewer-A L1 (C20 far from U3 VIN) is **deferred**, with the evidence below. The
  237a678 WIP (U3 rot 270, C20 at VIN, 4 unconnected) is dropped from the board (commit 6067908). No BOM, pinout or
  outline change. No In2 exception is used (the VBUS_SENSE In2 hop and SMPS_PS In2 stub approvals were not needed
  on the resulting board).
- Measured on the kept board: C20.1→U3.5 4.23 mm centre to centre (Reviewer-A: 6.68 mm routed, 3 vias); C21.1→U3.1 2.58 mm,
  C21.1→U3.10 2.32 mm; LX pads L2.1→U3.4 2.54 mm, L2.2→U3.2 2.43 mm. DRC 0 violations, 0 unconnected, parity 0.
  In2 3V3 pour 1 piece, 773.83 mm², narrowest neck 0.91 mm (0.91 near U1/decouplers). QSPI as Reviewer-A L15
  (SD0 1.23, SD2 2.32, SCLK 2.51, SD3 3.19, SD1 3.58, SS 7.41 mm). Replay with the fixed router (b51493c, 16be207)
  reproduces this board with 0/0 DRC.
- Attempts (all on scratch working trees, none committed as board changes):
  1. **replan-u1 rev 2 + one reroute** : +0.10 mm U1 east column shift (fit + DRC clean, 79972fe) on top of the
     NT1/C29/R8 WIP, rip/reroute with the fixed router, VBUS_SENSE In2 hop and SMPS_PS stub allowed.
     Result: 7 unconnected (ADC_AVDD, ADC_VREF, SMPS_PS ×2, VBUS_SENSE ×2, JP5-A); both In2 exceptions rejected by the
     router ("In2 stub too long"). Evidence: `.toolcache/d029b/reroute-fail_2026-10-23_2205/`.
  2. **C20-only move** (fallback on the reviewed board): no free spot nearer VIN than the current one
     (scan radius 6 mm, all rotations, `--ignore-courtyard J4`, pad gap 0.1). Evidence:
     `.toolcache/d029b/fallback-c20_2026-10-23_2207/`.
  3. **Group re-place U3/L2/C20/C21** (other parts fixed): no arrangement fits (rot 90/270 at 7 positions,
     rot 0/180). C20 is blocked by R14, C15, U4, L1 and the J4 pads. Evidence:
     `.toolcache/d029c/group-fit_2026-10-23_2214/SUMMARY.md`.
  4. **Group + R14/C15** (237a678 arrangement: U3 rot 270 at (16.3, 14.64), L2 (16.5, 10.4) r0, C20 (13.47,
     10.25) r90, C21 (17.3, 6.6) r90, R14 (15.6, 8.1), C15 (17.7, 17.6) r270): fits (all 6, corrected fit) and bare
     DRC 0 non-thermal. Would give C20.1→U3.5 2.38 mm, but C21.1→U3.1 5.86 mm, LX 2.88/2.96 mm. The one routing
     try (rip VSYS, L1/L2 nodes, VINA, 3V3_EN, SMPS_PS, VSYS_SENSE, VBUS_SENSE, GP28, VREG_AVDD, plus GND/3V3 items in
     the cluster; 9 U3 manual links) ended at 13 unconnected / 115 DRC errors (50 shorts, mostly stale GND/3V3/VSYS
     copper). A manual link (u3_vin_c20) clashed with GND, and the rip step raised a pcbnew SWIG error. Evidence:
     `.toolcache/d029c/group-route-fail_2026-10-23_2220/`.
- Why deferred, not forced: 0 unconnected / 0 DRC and the pour rules hold only on the reviewed board. Closing L1
  needs a larger re-placement of the TPS63001 corner (U3 rot 270 plus R14/C15 moved and a full corner reroute,
  probably with NT1/JP5/JP6, which this round excluded). Classed as rev-A risk: buck-mode input loop through vias and
  In1. Bring-up must check VSYS ripple at U3.5 and the 3V3 noise at the MAX31856 (bring-up plan).
- Scope: docs only, plus the board restore (6067908). Router fixes b51493c/16be207 and OhmAI fit fix 4ec69a8 stay.
- Supersedes: the 237a678 WIP outcome. Reviewer-A's other findings are answered in reviews/layout/resolutions.md.
- Superseded by D-030 (2026-10-24): with L2 changed to DFE201612P-2R2M (2016) and C20 changed to CL21A106KAYNNNE (0805), Reviewer-A L1 (C20 input decoupling loop) is **resolved** on the 51x21 mm board rather than deferred (C20.1 -> U3.5 [VIN] = 1.65 mm center-to-center / 0.62 mm pad-edge gap, 1.55 mm routed on F.Cu w = 0.30 mm, 0 vias; commit 5d80779).

## D-030: BOM changes for Reviewer-A L1 at 51x21: L2 DFE201612P, C20 0805, C32 100 nF on ADC_AVDD   (2026-10-23, phase 8)
- Decided by: owner, 2026-10-23, after docs/layout/bom-options.md (c5d0ad3). The board stays 51 x 21 (R-02), decided .
- Decision:
  1. L2 SWPA3015S2R2MT (C43389) -> Murata **DFE201612P-2R2M** (=P2, LCSC C79317, JLC extended, 7809 stock, $0.1061 qty 1,
     jlcparts 2026-10-15). It has 2.2 uH +/-20 %, a rated current of 2.1 A (inductance change) / 1.5 A (temperature rise) and DCR 144 mOhm max
     (Murata JE243A-0033-01 p.2). It meets SLVS520C (L = 2.2 uH Table 1 p.10; Isat >= 0.95 A per Eq. 3-4 p.11-12 + 20 %).
     Footprint: new project footprint `pico-k:L_Murata_DFE201612P` from spec p.5 (pads 0.8 x 1.8, gap 0.8, 2.4 overall).
     It has a keepout (no tracks, vias or pour on any copper layer) between the pads under the coil, per the spec note.
  2. C20 CL31A106KBHNNNE 1206 (C13585) -> Samsung **CL21A106KAYNNNE** 0805 10 uF 25 V X5R (C15850, JLC basic,
     $0.0692 qty 1). DC bias (Samsung char sheet, graph 3, curve read, ESTIMATE): ~5.8 uF at 5 V, ~5.0 uF worst case at
     -10 %. That is >= 4.7 uF (SLVS520C p.12), with a small margin.
  3. **Add C32** 100 nF 0402 CL05B104KO5NNNC (C1525, basic) on ADC_AVDD at U1.44, alongside C27 (Reviewer-A Q3).
- Rationale: the probes in bom-options.md (f4/f6) showed that the U3 block fits at 51 x 21 with A + B. Cost is about +$0.08 per board
  (A + B); C32 adds about $0.004.
- Alternatives: 54 mm board (replan-v2, rejected); Sunlord WPN201610/WPN252012 (weaker Isat or no readable datasheet);
  R18 0201 (not approved, a further BOM change).
- Supersedes: the L2 part of D-006/D-007, the C20 part of D-009 (C20 stays a single 10 uF input cap), and the L1 deferral in D-029 (L1 is now resolved on the 51x21 mm board).
- Outcome (2026-10-24, agent, commit 5d80779): applied and routed to **0 DRC violations, 0 unconnected items**, parity 0:
  - Placement: U3 at (16.30, 11.75) rot -90 (270 deg); L2 (DFE201612P-2R2M, 2016) at (13.15, 10.60) rot -90 with all-layer under-coil keepout [12.35..13.95, 9.60..11.60]; C20 (CL21A106KAYNNNE, 0805 10 uF) at (16.35, 8.70) rot 0; C21 (CL10A106MA8NRNC, 0603 10 µF) at (16.50, 15.10) rot 180; C32 (CL05B104KO5NNNC, 0402 100 nF) at (17.84, 22.25) rot -90 on /ADC_AVDD alongside C27 at (17.84, 24.20) rot -90. All parts pass `ohmai layout fit --ignore-courtyard J4 --pad-gap 0.1`.
  - L1 resolved (C20 input loop): C20.1 -> U3.5 [VIN] is 1.65 mm center-to-center (0.62 mm pad-edge gap), 1.55 mm routed directly on F.Cu (w = 0.30 mm, 0 vias). C20.2 -> U3.3 [GND] is 1.93 mm center-to-center (0.86 mm pad-edge gap), tied on F.Cu GND pour (0 vias) with U3.3 also tied directly on F.Cu (w = 0.25 mm) to U3.11 exposed thermal pad + 4 in-pad GND vias.
  - L6 / L13 resolved (L2 keepout and switch traces): L2.1 -> U3.4 [L1] is 2.71 mm center-to-center (1.63 mm pad-edge gap, 2.34 mm routed, w = 0.25 mm); L2.2 -> U3.2 [L2] is 3.80 mm center-to-center (2.66 mm pad-edge gap, 3.94 mm routed, w = 0.25 mm). Zero copper on any layer inside L2 under-coil keepout [12.35..13.95, 9.60..11.60]; /SMPS_PS is routed outside the keepout.
  - L2 output loop (C21): C21.1 -> U3.10 [FB] is 1.95 mm center-to-center (1.17 mm pad-edge gap, 0.57 mm F.Cu + In2.Cu 3V3 plane); C21.1 -> U3.1 [VOUT] is 4.75 mm center-to-center (3.97 mm pad-edge gap, 1.08 mm F.Cu w = 0.30 mm stubs into dedicated local 3V3 vias at (17.40, 9.85) [0.51 mm from U3.1] and (17.78, 15.10) [0.50 mm from C21.1] on the solid In2.Cu 3V3 plane, plus F.Cu link to J4.36).
  - L5 / Q3 resolved (C32 100 nF on ADC_AVDD): C32.1 -> U1.44 [/ADC_AVDD] is 4.06 mm center-to-center (3.32 mm pad-edge gap, 7.83 mm routed); C27.1 -> U1.44 is 4.99 mm center-to-center (4.28 mm pad-edge gap, 6.05 mm routed, 2 vias, 0 mm on In2.Cu).
  - Pour metrics (`pour.py`): In2.Cu 3V3 pour is 1 piece, 772.70 mm2, narrowest neck 0.91 mm (all 29 attach points; 0.91 mm near U1/decouplers). In1.Cu has 0 signal tracks. Neither the VBUS_SENSE In2.Cu hop nor the SMPS_PS In2.Cu stub was needed.
  - Owner acceptance of 51 × 21 mm trade-offs and D-028 waiver (2026-10-24, owner): accepted Reviewer-A L2–L4 and L7–L12 as 51 × 21 mm density trade-offs (`reviews/layout/resolutions.md`) and extended the D-028 Reviewer-A level-3 independence waiver to `files_hash sha256:a0379e7200f2f84a047c679ac618166c6366c3289b1f607eb6a640d6da34d530`. Reviewer-A Round-2 re-verification (`reviews/layout/reviewer-a.md`, 2026-10-24) passed (`Verdict: approved`), closing the Phase 8 layout gate (`ohmai check layout --gate` PASS).
