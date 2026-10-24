---
project: "pico-k"
ohmai_version: "0.1.0.dev0"
phase: 11           # 1-12, see .ohmai/phases/
gate: in_review     # open | in_review | approved
markets: [EU]       # D-003; UK/US not applicable
authors:            # identities that wrote the work; reviewers must differ (ohmai check review)
  - {name: OhmAI, kind: agent, vendor: Grok Bot, model: Grok Bot, instructions: "ohmai-skill 0.1.0.dev0"}
updated: 2026-10-25
---
# STATUS: pico-k

> This file is the spec of record. If chat and this file disagree, this file wins until the owner changes it.
> Agents update it in the same commit as the work. Full decision entries live in `docs/decisions.md`.

## Idea
make a pico clone with an type k probe interface on the bottom

## Current phase
- **Phase 8 (Layout):** **PASSED / APPROVED (2026-10-24, `D-028`, `D-030`)** — 51 × 21 mm board routed (`5d80779`), 0 DRC violations, 0 unconnected items, parity 0; Reviewer-A Round-2 re-review (`reviews/layout/reviewer-a.md`, `files_hash sha256:a0379e7200f2f84a047c679ac618166c6366c3289b1f607eb6a640d6da34d530`) approved; `ohmai check layout --gate` passes (8/8 checks PASS).
- **Phase 9 (Enclosure):** **PASSED (N/A, 2026-10-25)** — Bare stick PCB module per `D-001` (Q2/Q3) and `R-02`; `docs/enclosure.md` marked `<!-- ohmai:not-applicable -->`; `ohmai check enclosure --gate` passes.
- **Phase 10 (BOM Lock):** **PASSED / APPROVED (2026-10-25)** — All 36 rows (69 refs) in `bom/bom.csv` locked, verified against `jlcparts`, and synchronized with `parts/selection.md` (`D-025`, `D-030`, 3 BOM sourcing rules, 6 single-source components with `checked:` reasons); `Reviewer-A` Round-2 `review:bom` (`reviews/bom/reviewer-a.md`, `files_hash sha256:7cb4b0020081ece553630ae558045a8a751e50b631a965a9d3407d72878e0310`) approved; `ohmai check bom --gate` passes (4/4 checks PASS).
- **Phase 11 (Fab Release):** **PRE-RELEASE READY (awaiting human `review:fab`, 2026-10-25)** — `ohmai check fab-outputs` (`out/fab-preview/`) and `ohmai release rev-A --dry-run` (`out/release/rev-A/`: Gerbers, drill + map, PnP/CPL, schematic PDF, assembly PDF, BOM, `MANIFEST.md`) generated with 0 export errors; `reviews/fab/BRIEF.md` (`files_hash sha256:03bf5eec19931766ac64231a9f2a7c3662faea2905ae956a823c058cb125e038`, `require_kind: human`) ready for owner pre-order sign-off.
- **Phase 12 (Bring-Up & Manual):** **PRE-BOARD READY (awaiting rev-A boards & human `review:bringup`, 2026-10-25)** — `test/bringup-plan.md`, `test/firmware/bringup_selftest.py`, and `docs/manual.md` (10 sections, EU rules, `MW-01`..`MW-06`, EN+SV safety summary) completed; `ohmai check docs:test/bringup-plan.md`, `ohmai check manual`, and `ohmai check bringup-code` all PASS; `reviews/bringup/BRIEF.md` (`files_hash sha256:f5040968ca2408d3133b7b35dbb64bf0bd936aad7f5af14c420dd226a0fc5be0`, `require_kind: human`) ready for post-bench sign-off.
- **Phase 6 (RFQ):** Not applicable for rev-A (`D-012`, `P7-7`).

## Locked decisions
| ID | Date | Decision | Phase | Ref |
|----|------|----------|-------|-----|
| D-001 | 2026-10-15 | Requirements locked: RP2350A; full drop-in Pico 2 compatibility; TC connector on top, flat bottom; 1 ch type K; MAX31856 (grounded + ungrounded, full K range); SPI on 4 shared GPIO with jumpers; 5-10 protos at JLCPCB/LCSC; USB-C; USB 5 V only; project owner | 1 | docs/decisions.md#d-001 |
| D-002 | 2026-10-15 | Amends D-001: SWD debug header dropped (SWD on bottom test pads); keep 4 holes + full castellations if possible | 2 | docs/decisions.md#d-002 |
| D-003 | 2026-10-15 | Amends D-001: target market EU only; UK/US (UKCA/FCC) not applicable | 2 | docs/decisions.md#d-003 |
| D-004 | 2026-10-15 | Architecture: TPS63001; SPI1 GP12-15 + jumpers + CS pull-up; 2 × Omega PCC-SMD socket, F1 (2 sensor-end holes dropped, R-05 amended, 51 × 21 kept); grounded-probe limit documented (MW-01); HRO TYPE-C-31-M-12; 4-layer 1.0 mm | 2 | docs/decisions.md#d-004 |
| D-005 | 2026-10-15 | Safety plan: rev-A own R&D only, CE before any supply; finished end-user board; MW-02 warning (no isolation); EN IEC 62368-1 reference; cables ≤ 3 m; EN 55032 B + EN 55035; derating rules; bottom-silk CE/WEEE/ID; Sweden first (SV+EN); pre-compliance + self-declaration | 3 | docs/decisions.md#d-005 |
| D-006 | 2026-10-15 | Parts: BOM approved with second sources or written single-source acceptance (RP2350A, MAX31856, TPS6300x, ABM8, PCC-SMD); flash alt GD25Q32E; USB-C SHOU HAN main / HRO alt (amends D-004); 0402; no TC TVS. L1 = MPL-AT2512-3R3 (amendment final in D-007) | 4 | docs/decisions.md#d-006 |
| D-007 | 2026-10-15 | Phase 5 answers: P4-4b MPL-AT2512-3R3 + 2nd source MPL-AL4020-3R3, rev-A both orientations (L1 approved); R17 removed; R22 470 Ω kept; 2nd 4.7 µF at DVDD pin 23 (C28); Q1 gate to 3V3; 4.7/10 µF to 0603 (C19666, C96446); crystal pads 2/4 and USB shell (tab pads) to GND; source conflicts accepted. P5-1 delegated to Reviewer-A | 5 | docs/decisions.md#d-007 |
| D-008 | 2026-10-15 | P5-10: one more cap at each derated spot: C29 4.7 µF (VREG_VIN), C30 10 µF (TPS63001 VIN), C31 10 µF (3V3 out); same 0603 basic parts | 5 | docs/decisions.md#d-008 |
| D-009 | 2026-10-15 | P5-9 DNF pull-ups R23/R24; P5-11 C27 4.7 µF; P5-12 PCC-SMD polarity from Omega p.2 drawing; P5-13 L1 documented deviation + 1.1 V fallback footprint (amends D-007); C20+C30 → one 1206 10 µF 50 V (amends D-008) | 5 | docs/decisions.md#d-009 |
| D-010 | 2026-10-15 | P5-14: USB 2.0 inrush exceedance accepted for rev-A (documented deviation, C19 kept, no load switch); bring-up droop test; rev-B fix if it fails; no USB logo/compliance claim | 5 | docs/decisions.md#d-010 |
| D-011 | 2026-10-15 | Phase 5 gate closed: Reviewer-A review passed with nits (N1-N3 fixed post-review), 13 constraints files reviewed; owner instruction (close on Reviewer-A pass) | 5 | docs/decisions.md#d-011 |
| D-012 | 2026-10-15 | Phase 7 answers: J2/J3 Conn_01x01 + symbol map (PCC-SMD footprint phase 8); per-part symbol maps, MPN/ref binding (D2 LED pads reversed vs KiCad, schematic correct, KT-0805G p.2); passives semantics fixed in OhmAI; W25Q32JVZP stand-in and generic symbols accepted; 1.1 V fallback JP5/JP6 per RP2350 Fig. 21; phase 6 N/A; KiCad libs pinned 9.0.9.1; datasheet-figure layouts; OhmAI-Author trailers enforced from 2398d87 | 7 | docs/decisions.md#d-012 |
| D-013 | 2026-10-15 | P7-9: 1.1 V fallback stays an off-board TP7 feed with JP5/JP6 (RP2350 p.451-452 Fig. 21), no on-board DNP regulator; firmware sets VREG HIZ when used (bring-up plan §2a); Reviewer-A reviews the schematic | 7 | docs/decisions.md#d-013 |
| D-014 | 2026-10-15 | Reviewer-A F8/F9: TP5 moved to LED_A (LED anode, R22/D2), as Pico 2 §3.1 p.9 / Fig. 11 p.20 (D-002); F18: KiCad app pinned `kicad.app: ">=9.0.2,<9.1"`, `ohmai check kicad-app` | 7 | docs/decisions.md#d-014 |
| D-015 | 2026-10-15 | Bring-up gate requires a human sign-off (`require_kind: human`; owner may sign, agents author); safety unchanged | 7 | docs/decisions.md#d-015 |
| D-016 | 2026-10-15 | Schematic gate approved: Reviewer-A's re-verified review passes; Reviewer-A's level-3 independence accepted by the owner for this gate and files_hash a052ad17 only (alternatives tried recorded); phase 7 merged | 7 | docs/decisions.md#d-016 |
| D-017 | 2026-10-16 | Phase 8 answers: P8-1 (a) no mounting holes (H1/H2 removed, R-05 amended); P8-2 Pico 2 pin positions and 51 × 21 kept, end pins 1/20/21/40 without half-holes (JLC castellation pad-edge ≥ 1 mm / hole-to-corner ≥ 3 mm rules met by the other 36), JLC confirms in quote; P8-3 non-plated rear slot; P8-4 tab depth checked at bring-up; P8-5 TP mapping; P8-6 (i)-(iii) deviations accepted | 8 | docs/decisions.md#d-017 |
| D-018 | 2026-10-16 | P8-7 (a): U1 decoupler rows moved 0.6–1.0 mm outward (minimum that works) for escape channels; same pins; Freerouting 2.1.0 unchanged, no inner-layer signals, via size unchanged | 8 | docs/decisions.md#d-018 |
| D-019 | 2026-10-16 | P8-8 (c): Freerouting 2.1.0 → 2.2.4 on OpenJDK 25.0.4.1 (side by side with Java 21), after known-bad/golden/canary + same-DSN comparison; headless, analytics/telemetry off, no network | 8 | docs/decisions.md#d-019 |
| D-020 | 2026-10-16 | P8-8 (b): signals allowed on In2 (3V3) with the pour around them; In1 GND stays solid; short In2 stubs, no 3V3 islands, USB D+/D- off In2 if possible | 8 | docs/decisions.md#d-020 |
| D-021 | 2026-10-16 | Placement rework around U1 (RP2350) for escape channels | 8 | docs/decisions.md#d-021 |
| D-022 | 2026-10-16 | Hand-route all remaining P2 connections, scripted (hardware/gen/pcb/handroute.py, replayable) | 8 | docs/decisions.md#d-022 |
| D-023 | 2026-10-17 | Longer In2 signal runs for the last connections (pico-k-only, extends D-020): 3V3 In2 pour one piece, necks >= 0.5 mm (>= 0.8 mm near U1/decouplers), In1 solid, USB off In2 | 8 | docs/decisions.md#d-023 |
| D-024 | 2026-10-17 | Right passive column next to U1 shifted ~0.5 mm east (pico-k-only); applies with D-025 | 8 | docs/decisions.md#d-024 |
| D-025 | 2026-10-17 | C18/C27 4.7 µF 0603 → 0402 TDK105CBJ475MV-F (Taiyo Yuden, LCSC C22385335, 25 V X5R ±20 %, JLC extended); ≈ 2.7 µF at 3.3 V vs ≈ 3.2 µF accepted; reason: GP22/26/27/28 escape room | 8 | docs/decisions.md#d-025 |
| D-026 | 2026-10-17 | Q1 next to U1 east impossible (no room); option 2 applied: Q1 stays west, R19/R9 moved next to it (electrically identical); hand-route the last links (done 2026-10-17, board clean; U1.23-C9 direct link not possible, see outcome) | 8 | docs/decisions.md#d-026 |
| D-027 | 2026-10-17 | C9 (DVDD 100 nF) vertical directly under U1.23 (0.87 mm on F.Cu, no via), C28 moved down; crystal corner re-routed, board clean | 8 | docs/decisions.md#d-027 |
| D-028 | 2026-10-17 | Layout reviewer Reviewer-A; level-3 independence accepted for review:layout on files_hash c71de844 and (2026-10-24) D-030 files_hash a0379e72 only (a cloud agent on another vendor/model was possible but would use the cloud agent allowance before the monthly reset) | 8 | docs/decisions.md#d-028 |
| D-029 | 2026-10-23 | Reviewer-A L1 (C20 at TPS63001 VIN) originally deferred on the pre-D-030 BOM (3e2d005); superseded by D-030, which resolves L1 on the 51x21 mm board (5d80779) | 8 | docs/decisions.md#d-029 |
| D-030 | 2026-10-23 | BOM + layout rework for Reviewer-A L1/L5/L6/L13/Q3 at 51x21 (5d80779): L2 → Murata DFE201612P-2R2M (C79317, all-layer keepout under coil); C20 → CL21A106KAYNNNE 0805 (C15850; C20.1→U3.5 = 1.65 mm center-to-center / 1.55 mm F.Cu w=0.30 mm, 0 vias); add C32 100 nF 0402 (C1525) on ADC_AVDD U1.44; 0 DRC, 0 unconnected; L2–L4 and L7–L12 accepted by owner as 51x21 trade-offs (2026-10-24) | 8 | docs/decisions.md#d-030 |

## Open questions
Phase 4 answers (D-006): P4-1 … P4-11 accepted; P4-6 option A (amends D-004). P4-4b answered in D-007 (MPL-AT2512-3R3).

- [x] **Phase 8 layout review gate CLOSED / PASSED (`review:layout`, D-030 completed in `5d80779`, Reviewer-A Round-2 re-review approved 2026-10-24 on `files_hash sha256:a0379e7200f2f84a047c679ac618166c6366c3289b1f607eb6a640d6da34d530`):**
  - D-030 51 × 21 mm board placed and routed cleanly (**0 DRC violations, 0 unconnected items**, schematic parity 0; all 89 footprints pass `ohmai layout fit --ignore-courtyard J4 --pad-gap 0.1`).
  - Reviewer-A findings **L1, L5, L6, L13, Q3** are **fixed** in `5d80779`:
    - **L1 (`C20` input loop)**: `C20` (0805 `CL21A106KAYNNNE`) at `(16.35, 8.70)` rot `0`; `C20.1 -> U3.5 [VIN]` = `1.65 mm` center-to-center (`0.62 mm` pad-edge gap), `1.55 mm` routed directly on `F.Cu` (`w = 0.30 mm`, **0 vias**); `C20.2 -> U3.3 [GND]` = `1.93 mm` center-to-center (`0.86 mm` pad-edge gap), `0 vias` on `F.Cu` GND pour + direct `F.Cu` tie to `U3.11` thermal pad.
    - **L6 / L13 (`L2` keepout & switch nodes)**: `L2` (`DFE201612P-2R2M`, 2016) at `(13.15, 10.60)` rot `-90` with all-layer under-coil keepout `[12.35..13.95, 9.60..11.60]` completely clear of tracks, vias, and pours; `L2.1 -> U3.4 [L1]` = `2.71 mm` (`1.63 mm` edge gap, `2.34 mm` routed, `w = 0.25 mm`); `L2.2 -> U3.2 [L2]` = `3.80 mm` (`2.66 mm` edge gap, `3.94 mm` routed, `w = 0.25 mm`); `/SMPS_PS` routed outside the `L2` keepout.
    - **L2 (`C21` output loop)**: `C21` at `(16.50, 15.10)` rot `180`; `C21.1 -> U3.10 [FB]` = `1.95 mm` (`1.17 mm` edge gap, `0.57 mm` `F.Cu` + `In2.Cu` `3V3` plane); `C21.1 -> U3.1 [VOUT]` = `4.75 mm` (`3.97 mm` edge gap, `1.08 mm` `F.Cu` `w = 0.30 mm` stubs into dedicated local `3V3` vias at `(17.40, 9.85)` [`0.51 mm` from `U3.1`] and `(17.78, 15.10)` [`0.50 mm` from `C21.1`] on the solid `In2.Cu` `3V3` plane, plus `F.Cu` link to `J4.36`).
    - **L5 / Q3 (`C32` 100 nF on `ADC_AVDD`)**: `C32` (`CL05B104KO5NNNC`, 0402 100 nF) at `(17.84, 22.25)` rot `-90` alongside `C27` at `(17.84, 24.20)` rot `-90`; `C32.1 -> U1.44` = `4.06 mm` (`3.32 mm` edge gap, `7.83 mm` routed); `C27.1 -> U1.44` = `4.99 mm` (`4.28 mm` edge gap, `6.05 mm` routed, 2 vias, 0 mm on `In2.Cu`).
    - **Pour metrics (`pour.py`)**: `In2.Cu` `3V3` pour = 1 piece, `772.70 mm²`, narrowest neck `0.91 mm` (all 29 attach points; `0.91 mm` near U1/decouplers); `In1.Cu` = 0 signal tracks; neither the `VBUS_SENSE` `In2.Cu` hop nor the `SMPS_PS` `In2.Cu` stub was needed.
  - **Owner sign-offs recorded (2026-10-24)**: `L2, L3, L4, L7, L8, L9, L10, L11, L12` accepted as 51 × 21 mm trade-offs in `reviews/layout/resolutions.md` (0 unresolved issues), and D-028 Reviewer-A level-3 independence waiver approved for `files_hash sha256:a0379e7200f2f84a047c679ac618166c6366c3289b1f607eb6a640d6da34d530`.
  - **Gate closed (2026-10-24)**: Reviewer-A Round-2 re-review in `reviews/layout/reviewer-a.md` (`files_hash sha256:a0379e7200f2f84a047c679ac618166c6366c3289b1f607eb6a640d6da34d530`, `Verdict: approved`) verified L1, L5, L6, L13, Q1–Q3 and owner acceptances L2–L4, L7–L12; `ohmai check layout --gate` and `ohmai check review:layout` PASS with 0 unresolved issues.
- [ ] Non-blocking (D-001): BOM cost target per board. Phase 4 ESTIMATE: ≈ $40 (5 boards) / ≈ $18 (100 boards) without PCB, shipping and VAT.
- [ ] Non-blocking: board ambient range; default is the Pico 2 rating (−20 to +85 °C incl. self-heating).
- [ ] Non-blocking (before first sale): Cyber Resilience Act (EU) 2024/2847 scope for firmware + USB; packaging regulation (EU) 2025/40.
- [ ] Non-blocking (before first sale): manufacturer legal name and postal/e-mail address for labels and the DoC.
- [ ] Non-blocking (before first sale): REACH SVHC declarations per part; RoHS certificates missing on LCSC for some parts.

Phase 5 review items (13 constraints files, all `status: draft`). P5-2 … P5-8 answered in D-007.
- [ ] P5-1 Independent review: Reviewer-A delivered `reviews/constraints/reviewer-a.md` (= `docs/review-constraints-reviewer-a.md`), 0 blockers, 7 should-fix, 11 nits, 5 questions. All 18 fixes applied and verified (054096c); resolutions in `reviews/constraints/resolutions.md`. **Reviewer-A must re-verify** the changed files against the regenerated brief (hash changed), then `review:constraints` can pass.
- [x] P5-11 RESOLVED D-009: C27 ADC_AVDD = 4.7 µF (CL10A475KO8NNNC), as Pico 2 Fig. 11 p.20 C13 and Pico 2 W schematic p.1 C13 (checked on the drawings).
- [x] P5-12 RESOLVED D-009: polarity from the Omega drawing (PCC-SMD p.2 assembly top view + FRONT PANEL DESIGN): board edge seen from outside, component side up: + right clip (J2 → T+), − left clip (J3 → T−); orientation reference in PCC-SMD.yaml. Magnet + warm-tip checks in the bring-up plan (sanity only).
- [x] P5-13 RESOLVED D-009 (amends D-007): L1 MPL-AT2512-3R3 = documented rev-A deviation (reference AOTA-B201610S3R3-101-T), both orientations, external 1.1 V DVDD kept as a DNF fallback footprint (RP2350 Fig. 21 p.452).
- [x] P5-9 RESOLVED D-009: DRDY/FAULT no pull-up fitted, DNF 10 kΩ pull-ups R23/R24 at the test pads, no wire-OR; drive type confirmed on rev-A (bring-up plan).
- [x] P5-10 RESOLVED D-008 (owner 2026-10-15): C29 (2nd C_IN 4.7 µF), C30 (2nd TPS63001 Cin 10 µF), C31 (3rd 3V3 Cout 10 µF). Effective (ESTIMATE): C_IN 6.4–6.6 µF typ / ≈ 5.1 µF worst ≥ 4.7; Cin 8.8–9.6 / ≈ 6.7 µF ≥ 4.7; Cout 18.6–20.1 µF typ ≥ 15 (≈ 15 at −20 % tol). Amended D-009: C20 + C30 → one C20 10 µF 50 V 1206 (≈ 6.1 µF worst at 5.25 V).
- [x] P5-14 RESOLVED D-010: USB 2.0 §7.2.4.1 attach load exceeded (≈ 132–137 µC vs 50 µC, ESTIMATE; C19 alone also > 10 µF near 0 V) accepted for rev-A as a documented deviation; no load switch, C19 unchanged; VBUS droop measured at bring-up (≤ 330 mV target); rev-B action if it fails: load switch + C19 4.7 µF.

### Phase 8 (layout), raised 2026-10-16 (D-018 does not fit as specified)
- [x] **P8-8 RESOLVED D-019 (c): Freerouting 2.2.4 on Java 25.** Was: D-018 (a) cannot be applied as decided: no decoupler row has 0.6 mm of free room outward.**
  Courtyards (board mm): left C1/C8/C2 start at x 5.31, the flash U2 ends at 5.30 and U2 cannot move left (2.70 vs
  the J4 castellation strip at 2.66); below C2 sit C11 (to 4.95) and R6 (to 5.11). Right C5…C6 end at 16.58, the
  next column C18/C27 (0603 4.7 µF) and R19 sits at 16.69…18.25 against the J4 strip at 18.34 (0.09 mm). Top: C7
  ends 0.05 mm from the U1 courtyard, JP5/JP6 directly above. Bottom: C3 can move 0.46 mm (R3), C9 0 mm (C28).
  Experiments (not committed; boards in `.toolcache/route/`): baseline 69ce528 = 75 unconnected,
  4 errors (best pass 57 unrouted; same base earlier 41). E1 = right column +0.6, C18/C27 swapped to 0402 and
  shifted +0.25, C3 +0.46: worse (81 unrouted) because the plane-fanout vias filled the channel. E2 = E1 +
  `fanout.py --channel 0.6` (99b0a8d): **49 unconnected, 11 errors (10 starved_thermal, 1 hole_clearance)**,
  parity 2 (footprint swap not in the schematic). Not converged; stopped per the iteration limit in D-018.
  Options: (a) C18/C27 4.7 µF 0603 → 0402 (amends D-009 part CL10A475KO8NNNC; 0402 4.7 µF has a stronger DC-bias
  loss, ESTIMATE, check datasheet) + right column +0.6 (= E2), still needs (b) or (e) to close;
  (b) allow signals on In2 (3V3 pour kept on In2 around the routes; earlier test 43 open with the old placement);
  (c) Freerouting ≥ 2.2 on openjdk-25 25.0.4.1 (Debian 13) instead of the pinned 2.1.0;
  (d) smaller vias 0.3/0.15 (JLC capability/price check first); (e) finish the last connections by hand-guided
  routing in KiCad (no tool change, slow; agent can script it net by net); (f) re-place U2 (flash) to free the left
  column (larger placement change, QSPI lengths change).
  **Recommendation: (b), keeping the current placement and BOM; (a) only if (b) is refused.**

### Phase 8 (layout), raised 2026-10-16 (routing)
- [x] **P8-7 RESOLVED D-018 (a).** Was: Routing does not close with the current placement.** Options: (a) agent re-places the U1 decoupler columns
  (C1/C8/C2/R22 left, C5/R21/C10/C4/R20/R9/C6 right) 0.6–1.0 mm out, so there are escape channels, then routes again;
  placement cites unchanged (still "at the pin"), cap distance +0.6–1.0 mm (ESTIMATE). (b) allow signals on In2
  (3V3 plane split; test result 43 open). (c) Freerouting ≥ 2.2 (needs Java 25; Debian 13 has openjdk-25 25.0.4.1)
  instead of the pinned 2.1.0. (d) smaller vias (0.3/0.15 instead of 0.45/0.2; check JLC price/capability first).
  **Recommendation: (a), keeping (b)–(d) as fallbacks.**

### Phase 8 (layout), raised 2026-10-15 (milestone 1); answered 2026-10-16 (D-017)
- [x] **P8-1 RESOLVED D-017: (a), H1/H2 removed, R-05 amended.** Was: USB-C shell tabs vs the USB-end mounting holes (R-05).** The 2MD(073)
  front shell-tab slots (p.1: 8.64 apart, 0.60 drill, 1.0 copper) sit at x 6.18/14.82, 1.3 mm from the USB edge.
  The Pico 2 holes (Fig. 3 p.7: Ø2.1 at x 4.8/16.2, 2.0 from the edge) reach x 5.85/15.15: hole and tab copper
  overlap by 0.17 mm (DRC: hole_clearance, mask bridge). Every 16-pin USB-C footprint in KiCad 9.0.9.1 has the same
  ±4.32 tabs, so another receptacle does not help. Options: (a) drop H1/H2 (amends R-05; module is soldered by its
  castellations anyway); (b) move the holes outward to x 4.05/16.95 (12.9 spacing, not Pico-compatible; ESTIMATE
  ≥ 0.5 mm to tab copper and to the pin pads); (c) set J1 back ≥ 1.8 mm (plug overmold then hits the board edge:
  not viable). **Recommendation: (a)**, it also frees ~2 mm at the USB end corners for C20/D1.
- [x] P8-2 RESOLVED D-017: **applied: pins 1/20/21/40 without half-holes, positions and outline kept, JLC confirms in the quote** (JLC blog: pad edge ≥ 1 mm to board edge, hole ≥ 3.0 mm to corner; outline growth 51.86 or 55.26 mm and shift rejected; see D-017). Was: JLC castellation rule: the capabilities page asks "hole to board edge ≥ 1 mm"; the Pico 2 end pins are
  1.37 from the short edges (hole edge 0.87 mm, Fig. 3 p.7). Recommendation: keep Pico 2 positions (drop-in) and ask
  JLC in the quote (owner action already listed); fallback: none without breaking the pinout.
- [x] P8-3 RESOLVED D-017: PCC-SMD rear slot (p.2, 2.09–5.70 × 9.77–11.27, R0.40): drawn without copper, so modelled as a
  non-plated routed cut-out (JLC non-plated slot ≥ 1.0 wide: 1.5 ✓). Recommendation: non-plated, as drawn; confirm.
- [x] P8-4 RESOLVED D-017: PCC-SMD tab depth on a 1.0 mm board: the p.2 drawing is for 1.6 mm; the clip tab sits ~0.17 mm deeper
  in the plated side slot (ESTIMATE). Recommendation: accept, check the fit on the first boards (bring-up).
- [x] P8-5 RESOLVED D-017: Test-point numbers: TP1–TP7 placed at the Pico 2 Fig. 5 p.10 positions; which Fig. 5 pad is TP1…TP7 is an
  ESTIMATE (TP2/TP3 USB at the edge, TP1 GND between, TP4–TP6 column, TP7 near U1). TP7 moved 0.5 mm toward USB to
  clear the U1 thermal-via pad. SWD on TP8/TP10/TP9 (bottom, TC end, labelled). Recommendation: accept; a carrier
  using Pico 2 test pads must check pad functions against our list.
- [x] P8-6 RESOLVED D-017: Layout deviations to accept (all others follow the cited guides):
  (i) planned for routing: VREG_FB leaves pin 50 through one via to In1 and comes back up at JP5 by C17, because the 0603 C_IN (D-007)
  covers the pin column that the 0402 C_IN of Fig. 23 p.454 leaves free;
  (ii) C22 is ~6 mm from the TPS63001 VOUT pin and C31 sits in the clip gap by the MAX31856 (3V3 bulk), C21 is next to
  VOUT (SLVS520C §10.1 p.16 asks for output caps close: not all three fit);
  (iii) references on the fab layer, not the silkscreen (0402 density; JLC silk text ≥ 1.0 mm).
  Recommendation: accept (i)–(iii).

### Phase 7 (schematic), raised 2026-10-15
P7-1 … P7-8 answered in D-012 (all recommendations approved).
- [x] P7-1 J2/J3 `Connector_Generic:Conn_01x01` + `parts/symbol-maps/PCC-SMD.yaml`; footprint from Omega p.2 in phase 8.
- [x] P7-2 W25Q32JVZP stand-in, mapped. - [x] P7-3 generic symbols. - [x] P7-4 symbol maps (D2 LED: see D-012).
- [x] P7-5 passives semantics (OhmAI). - [x] P7-6 JP5/JP6 per Fig. 21. - [x] P7-7 phase 6 N/A. - [x] P7-8 accepted.
- [x] P7-9 RESOLVED D-013: off-board 1.1 V feed into TP7 with JP5/JP6 (RP2350 p.451-452, Fig. 21), no on-board DNP
  regulator; firmware sets VREG HIZ when the fallback is used (`test/bringup-plan.md` §2a).
- [ ] P7-10 → phase 8 work list (see Next actions) (phase 8 carry-over; extended by Reviewer-A's schematic review F11, F17, F20, F21, F23, F24):
  - D2: CPL/rotation check by the KT-0805G cathode mark (p.2), never by "pin 1" (manufacturer pad 1 = anode, KiCad
    pad 1 = cathode); cathode mark on the silkscreen.
  - Y1 ABM8: check orientation by the pad layout, not the chamfer ("could be located on pin #1, 3, or 4", p.2).
  - PCC-SMD custom footprint from Omega p.2 with a cited-dimension footprint check.
  - JP5/JP6: place JP5 at C17 (VREG_FB fed from C_OUT, not routed under L1, RP2350 p.454), keep the JP6 stub short and
    away from L1/VREG_LX; silkscreen "JP5 FB-DVDD (cut first)" / "JP6 FB-GND (fallback)".
  - TPS63001: separate power/control ground joined near the IC (SLVS520C layout guidelines; cite the page in phase 8); SW1: confirm the A/B pair
    is on one side of SW_Push_1P1T_XKB_TS-1187A (TS-1187A p.1).
  - Post-gate cosmetic nits (Reviewer-A re-verify, a052ad17, optional): pin notes at the pin-47 caps ("C_IN at
    VREG_VIN (49)" at C16/C29, "C_OUT" at C17) on mcu_core; close the gap left on the edge sheet where TP5 was.
  - Footprints still empty (12): J1, U1 (QFN-60 7x7 EP), U2, U3 (VSON-10), U4 (SOT-23-6), U5 (TSSOP-14), L1, L2,
    Q1 (SOT-523), J2, J3, J4.

## Manual warnings
- MW-01: Grounded-junction probe on an object at USB-ground potential (earthed object + earthed host) is outside the MAX31856 common-mode range (0.5–1.4 V): readings are not specified and the OVUV fault may stop conversions. Use a powerbank / ungrounded host or an ungrounded probe. Source: phase 2, A2-4, `docs/architecture.md`; MAX31856 p.3, p.26.
- MW-02: Never touch live parts or mains with the probe or its cable; the probe is not insulated from the USB host (shock, damage). Source: phase 3, H1, `docs/safety.md`.
- MW-03: Probe tip and sheath can be very hot (type K to 1372 °C) and stay hot after use (burns, fire); use the probe within its own rating. Source: phase 3, H3.
- MW-04: Only the probe goes into the hot zone; board −20 to +85 °C, socket/plug −50 to +120 °C. Source: phase 3, H4; Pico 2 §3.3 p.12; PCC-SMD p.1.
- MW-05: USB 5 V only; no other voltages on VBUS/VSYS (VSYS 1.8–5.5 V). Source: phase 3, H6; R-06.
- MW-06: Not a toy; not for food contact unless the probe is approved; handle the bare board by its edges (ESD). Source: phase 3, H7, H8.

## Next actions
Phase 8 milestone 1 done (footprints, outline, placement; see Open questions P8-1 … P8-6):
- [x] Footprints for all 90 parts (`parts/footprints.yaml`; project library `hardware/pico-k.pretty`, KiCad-serialised);
  `footprints` check PASS (pin = pad, 90/90; OhmAI feat/layout-checks). SW1 pair: pads 1 = A+B (top row) ✓.
- [x] Outline 21 × 51, 4 layers 1.0 mm (JLC04101H-3313, core ESTIMATE), castellated 2 × 20 (Pico 2 Fig. 3 p.7).
- [x] Placement `hardware/gen/pcb/placement.yaml` (cited); fab rules `hardware/pico-k.kicad_dru` (JLC page, 2026-10-15).
- [x] Owner: answer P8-1 … P8-6 (D-017, 2026-10-16). H1/H2 removed, J4 end pins without half-holes.
- [ ] Agent: route (Freerouting 2.1.0, DSN/SES), fix DRC to 0, renders, `ohmai review start layout`.
  2026-10-16 WIP (commit ee1aa06): pipeline build_pcb.py -> fanout.py --escape --no-stitch -> route.py
  (Freerouting headless, analytics off, no network namespace) -> fanout.py (stitching). Best result: 86 unconnected,
  16 DRC violations (5 starved_thermal errors, rest silk warnings); renders `docs/layout/routed-{top,bottom,3d}.png`.
  Freerouting does not converge here (≈ 45-65 signal connections open after 20-100 passes in every DSN variant).
  The blocker is the U1 escape: the 0402 decoupler columns are ~0.45 mm from the QFN pin toes on all sides.
  Layout review NOT started (files would be hashed while the board is unrouted).
- [x] Owner: P8-7 = (a) (D-018, 2026-10-16).
  2026-10-16: board at 69ce528 (75 unconnected, 4 errors: 3 starved_thermal, 1 hole_clearance); D-018 cap move
  does not fit (P8-8); layout review NOT started (board not clean).
- [x] Owner: P8-8 = (c) (D-019, 2026-10-16): Freerouting 2.2.4 on OpenJDK 25.0.4.1, lock 2056a83.
  Routing log (D-019, Freerouting 2.2.4, base = 69ce528 placement + escape + plane fanout + `fanout.py --bridge`):
  -  same-DSN comparison, 3 min: 2.1.0 best 55 unrouted; 2.2.4 best 35 (import + stitch: 54 unconnected).
  -  run 1, 4 min timeout: 33 unrouted -> 55 unconnected, 6 starved_thermal (J4 GND pins).
  -  run 2 (8 min) and  run 3 (6 min): no SES. 2.2.4 bug: when the timeout + 30 s grace hits during a pass,
    the job is left TIMED_OUT, never COMPLETED, and the CLI waits forever (thread dump, source v2.2.4). Fix: end by
    --passes. DSN step 7 (J2/J3 slot pads widened) fixes the GP14-J3 hole clearance.
  -  run 4, 20 passes (ended by passes, ~4 min): 33 unrouted -> **44 unconnected, 5 errors (5 starved_thermal:
    J4 pins 3/8/18/28 GND, 36 3V3), 0 hole_clearance**; board committed. Remaining: QSPI (6 nets to U2), GP8-10,
    GP18-22, GP25-28, ADC/VBUS/VSYS sense, 3V3 pads without a via (U1.20, U1.38, C4, R20, C12, U3.10).
  -  staged, 10 passes each (< 3 min): QSPI alone routes 7/8 in 3 s; then all other nets: 41 unrouted ->
    49 unconnected, 1 clearance, 2 starved_thermal (GP0-GP8 lost instead). Not kept.
  - **Stopped (D-019 stop rule): 2.2.4 does not converge either.** Best 2.2.4 = b71be51, 44 unconnected / 5 errors;
    best 2.1.0 = 69ce528, 75 / 4. Both plateau (2.2.4 at 32-41 unrouted from pass ~10, stagnation detected).
    The remaining options need the owner: P8-8 (a) 0402 C18/C27 + channel, (b) In2 signals, (d) smaller vias,
    (e) hand-finish, (f) U2 move; or Freerouting 2.3.0/2.4.1/2.5.0 (outside D-019's "2.2.x").
    Layout review NOT started (board not clean).
- [x] Owner: In2 signals allowed (D-020, 2026-10-16). Routing log (Freerouting 2.2.4, runs end by --passes 10):
  -  DSN with In2 layer costs ((autoroute_settings ...)): Freerouting 2.2.4 then routes nothing ("0 unrouted
    nets"), even with a bare "(autoroute on)" scope; layer costs dropped.
  -  b71be51 copper fixed + leftovers with In2: NullPointerExceptions in the maze search, then no progress
    (hung after pass 2); killed. Not usable.
  -  all nets, In2 free: 26 unrouted -> 43 unconnected, 3 hole_clearance + 2 starved_thermal; In2 333 mm /
    32 nets, 3V3 pour in 10 pieces (15 3V3 unconnected). Violates D-020; not kept.
  -  In2 only for the 26 small-signal nets F/B left open (In2ok class; power, USB, crystal F/B only):
    26 unrouted -> **37 unconnected, 3 errors (starved_thermal J4.3 B.Cu, J1 S1 x2)**; In1 0 tracks; In2 98 mm /
    10 nets, longest 6.8 mm; **3V3 pour in 2 pieces (460 + 286 mm2)**, 7 3V3 items unconnected. Committed as WIP.
  - **Stopped (D-020 stop rule): 37 open after 4 runs.** Open: QSPI (5 nets), GP8-10, GP14, GP19-22, USB D+/D-,
    ADC_VREF, SMPS_PS, VBUS_SENSE, D2-A, Q1-D, C24, U3 L1/L2, VSYS, DVDD x3, 3V3 x7, GND x1.
    Layout review NOT started (board not clean).
- [ ] Owner: placement rework around U1 (D-021, 2026-10-16). Bottom-side caps conflict with R-07 (flat
  bottom), so all parts stay on top. Placement log below.
  Escape-ring check used (`.toolcache/d021/chk.py`): copper gap from the U1 pin toes to any other pad
  >= 0.75 mm (one 0.45 via + 2 x 0.15) and courtyard overlaps; the VREG caps C16/C29 over pins 46-50 are exempt
  (RP2350 Fig. 23 p.454 puts C_IN directly on VIN/PGND; vertical room is fully used, see below).
  - P1 (297d46e): U2 to the top-left, cap columns out 0.3 mm (ring L 0.79 / R 0.75 / B 0.85 mm, was 0.47-0.54),
    R1/R2 turned, small parts into the left lane. Route F/B 20 passes: 31 unrouted (stitching vias in the DSN);
    without stitching before routing (P1b): 26 unrouted -> 41 unconnected; + In2 for the leftovers (P1c):
    18 unrouted -> 36 unconnected, In2 171 mm, 3V3 pour split in 2 (366 + 324 mm2).
  - P2: flash turned (pin columns face U1, QSPI without crossings), JP5/JP6 to the bottom side (bare copper, like
    the test pads; their silk notes were already on B.SilkS), U3 turned so L1/L2 face the inductor, C7 off the
    USB corridor, left lane cleared. F/B 20 passes: 22 unrouted -> 32 unconnected (left GPIO, USB and 4/6 QSPI
    routed). + In2 leftovers (P2b): 16 unrouted -> 29 unconnected, 9 starved_thermal; In2 165 mm, 3V3 split
    (398 + 272 mm2).
  - P3: R9/R19 to the left lane next to Q1; gap in the right column at y 25-26 for GP19-22. F/B 25 passes: 26 unrouted ->
    32 unconnected (the left GPIO open again). Not better; board and placement restored to P2.
  - **Stopped (D-021 stop rule): 3 placement iterations, Freerouting 2.2.4 plateaus at 22-26 unrouted on F/B
    (16-18 with In2, but In2 then splits the 3V3 pour).** Best D-020-clean board = P2 (fc90915, restored):
    32 unconnected, 3 errors (starved_thermal J1 S1 x1, J4.3/J4.13 GND), In1 0 tracks, In2 0 tracks, 3V3 pour
    1 piece (812 mm2). Layout review NOT started (board not clean).
  - Owner: JP5/JP6 moved to the bottom side in P2 (bare copper, no part, flush like the test pads). R-07 says "no
    parts" on the bottom; confirm this reading or say no (then the top-left needs another home for 2 x 8.8 mm2).
- [ ] Owner: hand-route all remaining P2 connections (D-022, 2026-10-16); JP5/JP6 bottom accepted for now.
  - D-022 log (agent): `hardware/gen/pcb/handroute.py` (freeze / replay / route / manual; the board is rebuilt
    from `routes-base.json` (frozen P2 Freerouting copper) + `handroute.json` (rips + hand routes)). QSPI SD0/SCLK/SD3
    hand geometry; grid A* router with the board rules (pico-k.kicad_pro + kicad_dru), transactional whole-net
    rip-up with rollback (a first item-level rip-up diverged 25 -> 40 unconnected and was reverted). State
    2026-10-17: **22 unconnected, 0 errors**, In1 0 tracks, In2 one piece (Net-(D2-A) In2 stubs 2.3 mm).
    Open: GP20/21/22/25/26/27/28, 3V3_EN, ADC_VREF, SMPS_PS, VSYS_SENSE, DVDD x2, 3V3 x4, GND (NT1), Q1-D,
    VREG_AVDD, U3-L1, U3-VINA (U1 right side -> J4 corridor and the U1-top corridor are full).
  - 2026-10-17 (agent): **stopped at 21 unconnected, 0 errors** (9d3e7c6). Further passes (In2 stubs <= 2.5 mm,
    recursive rip-up to depth 3, up to 6 nets / 40 pads per rip) route nothing more. Blocked: U1 east pins -> J4
    (GP20/21/22/26/27/28, ADC_VREF, VREG_AVDD, DVDD U1.39, 3V3 C4/R20): F.Cu closed by the right passive columns
    + ADC_AVDD at x 118.24, B.Cu by the VSYS trunk at x 117.65 and the GP16-19 bundle; U1 east -> west over the U1
    top (GP25, VSYS_SENSE, Q1-D, SMPS_PS, 3V3_EN): U2/L1/C16/C17 corridor full (VBUS_SENSE, GP0-5, BOOTSEL);
    U3 corner (U3-L1 behind VBUS_SENSE, U3-VINA behind SMPS_PS/3V3_EN/VSYS); GND NT1.2 and 3V3 U1.20: no reachable
    plane via site. Ripping the blockers works only with In2 runs > 2.5 mm or re-routes that do not fit.
    Renders, phase 8 checks and the layout review are not started (board not clean). Owner decision needed.
  - D-023 (2026-10-17, agent log): ohmai CLI rebuilt from local branch int/layout-fr22 (ohmai,
    feat/layout-checks + feat/freerouting-2.2 merged, phases.py conflict resolved: phase 8 = kicad-app, toolchain,
    footprints, drc, creepage, review:layout); 130 tests pass, 1 fails (test_every_check_has_a_planted_bug:
    'footprints' has no known-bad case; integration gap, ohmai not changed). handroute.py In2 mode (--in2-long),
    per-net real-fill pour check (pour.py: 1 piece, neck >= 0.5 mm, >= 0.8 mm near U1/decouplers) with rollback,
    `clean` (dangling vias/tracks). : 12 unconnected, 0 errors, 0 dangling; In2 pour 1 piece.
  - D-023 stop (2026-10-17, agent): **9 unconnected, 0 errors**, no dangling vias/tracks; silk: B.Silk JP5/JP6
    notes moved left of JP5 (two lines each, clean); 2 F.Silk outline overlaps left (C12/U5, D2/Y1). In2 pour 1 piece,
    780.7 mm2, narrowest neck 0.91 mm (also near U1/decouplers); In1 0 tracks; In2 signal copper 74.1 mm (8 nets,
    longest run 11.96 mm SMPS_PS); no USB on In2. Further passes (rip-up, 0.1 mm neck-down) route nothing more.
    Open: GP22, GP26, GP27, GP28 (no via site next to the U1 east pins 34/40-42: the 1 mm strip between the pin tips and
    the right passive column holds the ADC_AVDD/ADC_VREF/3V3/VBUS_SENSE/VSYS_SENSE vias), 3V3 C4.1 (gap to the 3V3
    via / R20.1 used by GP25), 3V3 U1.20 and GND NT1.2 (no reachable plane via site), Q1-D (crossing to R19 needs an In2
    run that drops the pour neck to 0.39-0.44 mm: rolled back), U3-VINA (blocked by SMPS_PS/3V3_EN/VSYS at U3).
    Renders, phase 8 checks and the layout review not started (board not clean).
  - D-024 (2026-10-17, owner): right passive column by U1 shifted ~0.5 mm east for GP22/26/27/28 via room; re-route that area.
    Agent: not applied, no room (column A courtyards touch column B at x 16.81, column B touches the J4 strip
    at x 18.36; a +0.5 mm trial overlaps C18/C27/R19 by 0.23-0.51 mm). Reverted. Owner: C18/C27 as 0402 (BOM change)?
    Owner approved 0402 C18/C27 (2026-10-17) subject to parity. Agent check : **no adequate 0402 found,
    nothing changed** (D-025 not recorded). jlcparts snapshot 2026-10-17 (source-db-v2): 0402 4.7 uF >= 16 V in stock
    are all JLC extended (none basic/preferred): TDK105CBJ475MV-F (Taiyo Yuden, C22385335, 25 V X5R +-20 %),
    HGC0402R5475M250NTEJ / M160NTEJ (Chinocera, C22367824 / C7432765), 0402X475K160NT (Fenghua, C20624278).
    DC bias at 3.3 V: Taiyo sheet curve (AQC19J26-08D) about -42 % -> ~2.7 uF vs ~3.2 uF for CL10A475KO8NNNC
    (-16 % typ; worst with +-20 % tol ~2.2 uF vs ~2.9 uF); Chinocera/Fenghua catalogues have no part curve;
    basic CL05A475MP5NRNC is 10 V and ~2 uF at 3.3 V (TI LM3281 Table 6). Owner decision needed (options in report).
    `ohmai parts search` cannot read the new jlcparts schema (source-db-v2: jlc_components/lcsc_components), queried
    with sqlite directly.
  - D-025 (2026-10-17, owner): option 1, TDK105CBJ475MV-F for C18 and C27 (≈ 2.7 µF at 3.3 V accepted, JLC
    extended fee accepted). D-024 now applies. Agent: BOM row split (C16 C17 C28 C29 stay CL10A475KO8NNNC; new row
    C18 C27, LCSC price/stock 2026-10-17), schematic fields regenerated (ohmai schematic build), datasheet in LFS.
    ERC 0, netlist/bom-schema PASS; BOM vs schematic: refs/MPN/DNP match (value/footprint columns are the BOM's
    human-readable form for every row, unchanged convention). Placement: column A x 16.34, C18/C27/R19 x 17.84,
    C27 rot 270. Re-route (handroute D-023 rules + manual GND vias/links in handroute.py MANUAL): **stop at 6
    unconnected, 0 errors, 0 dangling** (HEAD 412258c, replay reproducible). In2 pour 1 piece, neck 0.91 mm (local
    0.91); In2 signals 88.6 mm; In1 no tracks; QSPI unchanged (SS 9.15, SCLK 2.99, SD0 1.30, SD1 4.62, SD2 3.15,
    SD3 3.65 mm). Closed by D-025: GP22, GP26, GP27, GP28, 3V3 C4.1, GND NT1.2. Open:
    VREG_AVDD U1.46 (boxed by the VREG_PGND fan-out and the U1.45 3V3 via; routable only by ripping ADC_VREF/GP28,
    which then fail), VSYS_SENSE U1.43-R9.1 and U1.43-Q1.2 (east-west run to Q1; In2 neck would drop to 0.78 mm
    local), Q1-D Q1.3-R19.2 (neck 0.55 mm), 3V3 U1.20, U3-VINA (both open since D-022). Passes oscillate 6-7: stalled.
    Renders, phase 8 checks and the layout review not started (board not clean).
  - D-026 (2026-10-17, owner): Q1 next to U1 east + hand-routing. Agent: **not applied**, no free
    courtyard site for Q1 (2.39 x 2.19 mm) east of x ≈ 4 (scan of placement on a 0.05 mm grid, both rotations).
    Options: (1) move SW1 (BOOTSEL, courtyard 7.6 x 5.7 at y 27.13-32.82) to free a site south of R9/R19/C6;
    (2) keep Q1 west and move R19 + R9 next to it (free sites at x ≈ 3.8, y 21-25): Q1-D and R9 become local,
    only VSYS_SENSE runs east to U1.43, and column A/B lose two parts (room for VREG_AVDD/ADC escapes);
    (3) smaller FET package (BOM change; still no 1.3 mm-wide slot fits without (1)). Loosening the In2 neck rule
    is not an option (owner).
    option 2 applied: R19 (5.26, 14.56) rot 180, R9 (3.62, 20.41); re-route in progress.
    re-route stopped at 1 unconnected / 0 errors / 0 dangling (2 silk overlaps, justified): closed VREG_AVDD,
    ADC escapes, U3-VINA, 3V3 U1.20 (+ DVDD/XIN/XOUT local rework); In2 1 piece, neck 0.91 mm, In2 signals 79.6 mm;
    QSPI unchanged. Open: VSYS_SENSE R9.1-U1.43 (needs an owner decision, see the report). Renders, phase 8
    checks and the layout review not started (board not clean).
     owner: option 1 (east-of-U1 rework) + DVDD U1.23-C9 + handroute via bug. : board clean (0 unconnected,
    0 errors, 0 dangling; 2 silk overlaps): VSYS_SENSE 27.2 mm, VBUS_SENSE 26.4 mm, ADC_VREF R21-R20 manual, JP6-JP5
    1.96 mm; In2 1 piece, neck 0.91 mm, In2 signals 85.0 mm; QSPI unchanged. handroute: same-net via hole-to-hole
    enforced, --rip drops old records. U1.23-C9 direct link not possible with the present placement (D-026 outcome):
    U1.23 -> C28.1 5.35 mm, -> C9.1 ~8.6 mm. Renders docs/layout/routed-{top,bottom,3d,in1,in2}.png.
    silk overlaps cleared by nudging D2 up 0.03 mm and C12 up 0.07 mm (stock silk kept; a silk trim raised
    lib_footprint_mismatch): DRC 0 violations, 0 unconnected, parity 0. `ohmai check layout` PASS (kicad-app,
    toolchain, footprints 88, drc clean, commits; creepage TODO); `ohmai review start layout` run, BRIEF written,
    no reviewer launched yet (gate review:layout open).
     owner: D-027 (crystal/C9/C28 rework). : C9 vertical under U1.23, DVDD 0.87 mm F.Cu no via; C28
    down 0.86 mm; XIN 11.96 mm / XOUT 5.73 mm (2 vias each, as before). DRC 0 / 0 unconnected / parity 0; In2 1 piece,
    neck 0.91 mm, In2 signals 85.0 mm; QSPI unchanged. Renders refreshed; layout BRIEF regenerated.
    2026-10-24 (D-030, commit `5d80779`): L2 (DFE201612P-2R2M 2016 at 13.15, 10.60 r-90 with all-layer under-coil keepout), C20 (0805 CL21A106KAYNNNE at 16.35, 8.70 r0: C20.1->U3.5 = 1.65 mm center-to-center / 1.55 mm F.Cu w=0.30 mm, 0 vias), U3 at (16.30, 11.75) r-90 with dedicated local 3V3 via at (17.40, 9.85), C21 at (16.50, 15.10) r180, C32 (0402 100 nF at 17.84, 22.25 r-90 on /ADC_AVDD alongside C27 at 17.84, 24.20 r-90), R11 silk overlap cleared at (5.65, 8.68) r90. DRC 0 violations, 0 unconnected items, parity 0; In2 3V3 pour 1 piece, 772.70 mm2, narrowest neck 0.91 mm (29 attach points; 0.91 mm near U1/decouplers); In1 0 tracks. Renders refreshed (`routed-{top,bottom,3d,in1,in2}.png`); `reviews/layout/BRIEF.md` and `resolutions.md` updated.
  - Environment rebuilt again 2026-10-17 (/tmp, out/ and apt packages gone): KiCad 9.0.2+dfsg-1, git-lfs
    3.6.1-1+deb13u1, librsvg2-bin reinstalled from Debian 13; out/netlist.net regenerated with kicad-cli.
Phase 8 toolchain (record for the toolchain lock; owner direction 2026-10-15):
- 2026-10-16 (D-019): Freerouting **2.2.4** `.toolcache/freerouting/freerouting-2.2.4.jar` sha256
  f5ed374182900ccc78e473518bbb9f6b869f4a07159495f663a76f52bb10523b (GitHub release digest) on OpenJDK **25.0.4.1**
  (Debian openjdk-25-jre-headless 25.0.4.1+1-1~deb13u1, extracted to `.toolcache/jdk25`, env JAVA25 /
  FR_JAVA); pinned in `toolchain.lock.yaml` (tools.freerouting: version, sha256, java). 2.1.0 / Java 21 kept for
  comparison only (FR21_JAR). The 2.1.0 lines below are history.
- Environment rebuilt 2026-10-16 (/opt and /tmp were wiped): tools reinstalled under `.toolcache` (env in
  `.toolcache/env.sh`), same versions.
- KiCad 9.0.2 (Debian 13 package 9.0.2+dfsg-1; kicad-cli, pcbnew Python), KiCad libraries 9.0.9.1
  (`ohmai kicad-libs install`, OHMAI_KICAD_LIBS=.toolcache/kicad-libs).
- Freerouting **2.1.0** `.toolcache/freerouting/freerouting-2.1.0.jar` (release asset v2.1.0) sha256 2c07d58f75dac03782664081e7a58b41c25400d871a9fcf166a2ea6fe60d5def (GPL-3.0, separate process), OpenJDK 21.0.12.1 (Debian openjdk-21-jre-headless 21.0.12.1+1-1~deb13u1). 2.2.0 … 2.5.0 are built for Java 25 (class file 69) and do not start on Java 21. DSN export from pcbnew verified.
- `.toolcache/kicad-tools-venv` (system site packages for pcbnew): kikit 1.8.1, kicad-python (kipy) 0.8.0, InteractiveHtmlBom 2.12.0, PyYAML 6.0.3, shapely 2.2.0 (full list `.toolcache/kicad-tools-freeze.txt`).
- Used now: pcbnew API (board build, FootprintLoad/Save, zone fill), kicad-cli (DRC, render). Not used yet: kipy
  (needs a running KiCad GUI instance with the IPC API server enabled; no headless mode in 9.0),
  KiKit and iBoM (fab outputs, phase 11), kiutils (not needed: pcbnew writes the files).
Phase 8 carry-overs still open (from P7-10):
- Agent: assign footprints to the 12 empty parts: J1, U1 (QFN-60 7x7 EP), U2, U3 (VSON-10), U4 (SOT-23-6),
  U5 (TSSOP-14), L1, L2, Q1 (SOT-523), J2/J3 (PCC-SMD custom), J4; cite each package drawing page.
- Agent: PCC-SMD custom footprint from Omega PCC-SMD p.2 with cited dimensions and a footprint-dimension check.
- Agent: D2 cathode mark on silkscreen; CPL/rotation by the KT-0805G cathode mark (p.2), never by "pin 1".
- Agent: JP5 at C17 (VREG_FB fed from C_OUT, not under L1/VREG_LX, RP2350 p.454); short JP6 stub; silkscreen
  "JP5 FB-DVDD (cut first)" / "JP6 FB-GND (fallback)".
- Agent: Y1 ABM8 orientation by the pad layout, not the chamfer (ABM8 p.2).
- Agent: TPS63001 separate power/control ground joined near the IC (SLVS520C layout guidelines; cite the page).
- Agent: SW1 confirm the A/B pair lies on one side of SW_Push_1P1T_XKB_TS-1187A (TS-1187A p.1).
- Agent (optional, schematic cosmetics): pin notes at C16/C29 ("C_IN at VREG_VIN (49)") and C17 ("C_OUT");
  close the edge-sheet gap where TP5 was. Changing sheets after the gate needs an owner note.
- Owner: get a PCB fabrication quote (4-layer 1.0 mm, castellated) before ordering rev-A.

## Phase log
| Phase | Started | Gate passed | PR |
|-------|---------|-------------|----|
| 1 Requirements | 2026-10-15 | 2026-10-15 | local merge (no remote) |
| 2 Architecture | 2026-10-15 | 2026-10-15 (D-004) | local merge (no remote) |
| 3 Safety | 2026-10-15 | 2026-10-15 (D-005) | local merge (no remote) |
| 4 Parts | 2026-10-15 | 2026-10-15 (D-006; P4-4b closed by D-007) | local merge (no remote) |
| 5 Constraints | 2026-10-15 | 2026-10-15 (D-011) | local merge (no remote) |
| 6 RFQ | - | not applicable for rev-A (D-012) | - |
| 7 Schematic | 2026-10-15 | 2026-10-15 (D-016) | local merge ecf8319 (no remote) |
| 8 Layout | 2026-10-15 | 2026-10-24 (D-028, D-030) | branch `phase/layout` |
| 9 Enclosure | 2026-10-25 | 2026-10-25 (not applicable per D-001 / R-02) | `ohmai check enclosure --gate` PASS |
| 10 BOM Lock | 2026-10-25 | 2026-10-25 (`review:bom` approved by `Reviewer-A`, `sha256:7cb4b0020081`) | `ohmai check bom --gate` PASS |
| 11 Fab Release | 2026-10-25 | `fab-outputs` & `rev-A` dry-run ready; awaiting human `review:fab` (`BRIEF.md` `sha256:03bf5eec1993`) | `out/fab-preview/` & `out/release/rev-A/` |
| 12 Bring-Up | 2026-10-25 | `bringup-plan.md`, `bringup_selftest.py` & `manual.md` ready; awaiting boards & human `review:bringup` (`BRIEF.md` `sha256:f5040968ca24`) | `docs:test/bringup-plan.md`, `manual`, `bringup-code` PASS |
