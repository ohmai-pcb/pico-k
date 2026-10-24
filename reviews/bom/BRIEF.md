---
ohmai_review_brief: 1
ohmai_version: 0.1.0.dev0
phase: bom
created: '2026-10-25'
files_hash: sha256:d72c9a74f7936c70b25643fb5a61428d4c77b630e56b1cf8639e3fa4c0f8ff72
required_reviews: 1
min_independence: 3
authors:
- name: OhmAI
  kind: agent
  vendor: Grok Bot
  model: Grok Bot
  instructions: ohmai-skill 0.1.0.dev0
files:
  bom/bom.csv: 2fcff21e8e9a2994865d32f732f20128b6f51e9b318f2e0d8c3d905efa2ff54f
---
# Independent review brief: phase `bom` (pico-k)

This brief is self-contained. You need only this repository and the files listed here.

## Your role
- You are an **independent reviewer**. **Report findings, never edit** the files in scope (or any other
  project file). Write only your own review file (format below).
- Check every line of every file in scope against the cited source page. Do not trust the author's notes.
- Cite the page number printed on the source page (plus section/table), for every issue and question.
- Do not invent values. If a source does not say it, write a `question`.

## Reviewer independence (state which level you are)
Ask for and use the highest feasible level; record the level actually achieved in your header:
1. different vendor's model (e.g. author on vendor A, reviewer on vendor B)
2. different model from the same vendor
3. different agent/bot with different skills or instructions (same model allowed)
4. human reviewer
Not allowed: the same agent session or identity as the author (see Authors). That is not a review.
Required for this gate: level 3 or better (a smaller number; 1 = most independent). A weaker level (larger number) is recorded and WARNs.

## Authors (the reviewer must differ)
- name=OhmAI; kind=agent; vendor=Grok Bot; model=Grok Bot; instructions=ohmai-skill 0.1.0.dev0

## Files in scope (1), content hash `sha256:d72c9a74f7936c70b25643fb5a61428d4c77b630e56b1cf8639e3fa4c0f8ff72`

| File | sha256 |
|---|---|
| `bom/bom.csv` | `2fcff21e8e9a` |

### Changed since the brief last reviewed by Reviewer-A (sha256:1ff04e82ef32...) (verify these first)
- `bom/bom.csv`

## Sources
- `parts/selection.md`

## Locked decisions (do not re-open; flag a conflict as `question`)
- D-001: Requirements locked: RP2350A; full drop-in Pico 2 compatibility; TC connector on top, flat bottom; 1 ch type K; MAX31856 (grounded + ungrounded, full K range); SPI on 4 shared GPIO with jumpers; 5-10 protos at JLCPCB/LCSC; USB-C; USB 5 V only; project owner
- D-002: Amends D-001: SWD debug header dropped (SWD on bottom test pads); keep 4 holes + full castellations if possible
- D-003: Amends D-001: target market EU only; UK/US (UKCA/FCC) not applicable
- D-004: Architecture: TPS63001; SPI1 GP12-15 + jumpers + CS pull-up; 2 × Omega PCC-SMD socket, F1 (2 sensor-end holes dropped, R-05 amended, 51 × 21 kept); grounded-probe limit documented (MW-01); HRO TYPE-C-31-M-12; 4-layer 1.0 mm
- D-005: Safety plan: rev-A own R&D only, CE before any supply; finished end-user board; MW-02 warning (no isolation); EN IEC 62368-1 reference; cables ≤ 3 m; EN 55032 B + EN 55035; derating rules; bottom-silk CE/WEEE/ID; Sweden first (SV+EN); pre-compliance + self-declaration
- D-006: Parts: BOM approved with second sources or written single-source acceptance (RP2350A, MAX31856, TPS6300x, ABM8, PCC-SMD); flash alt GD25Q32E; USB-C SHOU HAN main / HRO alt (amends D-004); 0402; no TC TVS. L1 = MPL-AT2512-3R3 (amendment final in D-007)
- D-007: Phase 5 answers: P4-4b MPL-AT2512-3R3 + 2nd source MPL-AL4020-3R3, rev-A both orientations (L1 approved); R17 removed; R22 470 Ω kept; 2nd 4.7 µF at DVDD pin 23 (C28); Q1 gate to 3V3; 4.7/10 µF to 0603 (C19666, C96446); crystal pads 2/4 and USB shell (tab pads) to GND; source conflicts accepted. P5-1 delegated to Reviewer-A
- D-008: P5-10: one more cap at each derated spot: C29 4.7 µF (VREG_VIN), C30 10 µF (TPS63001 VIN), C31 10 µF (3V3 out); same 0603 basic parts
- D-009: P5-9 DNF pull-ups R23/R24; P5-11 C27 4.7 µF; P5-12 PCC-SMD polarity from Omega p.2 drawing; P5-13 L1 documented deviation + 1.1 V fallback footprint (amends D-007); C20+C30 → one 1206 10 µF 50 V (amends D-008)
- D-010: P5-14: USB 2.0 inrush exceedance accepted for rev-A (documented deviation, C19 kept, no load switch); bring-up droop test; rev-B fix if it fails; no USB logo/compliance claim
- D-011: Phase 5 gate closed: Reviewer-A review passed with nits (N1-N3 fixed post-review), 13 constraints files reviewed; owner instruction (close on Reviewer-A pass)
- D-012: Phase 7 answers: J2/J3 Conn_01x01 + symbol map (PCC-SMD footprint phase 8); per-part symbol maps, MPN/ref binding (D2 LED pads reversed vs KiCad, schematic correct, KT-0805G p.2); passives semantics fixed in OhmAI; W25Q32JVZP stand-in and generic symbols accepted; 1.1 V fallback JP5/JP6 per RP2350 Fig. 21; phase 6 N/A; KiCad libs pinned 9.0.9.1; datasheet-figure layouts; OhmAI-Author trailers enforced from 2398d87
- D-013: P7-9: 1.1 V fallback stays an off-board TP7 feed with JP5/JP6 (RP2350 p.451-452 Fig. 21), no on-board DNP regulator; firmware sets VREG HIZ when used (bring-up plan §2a); Reviewer-A reviews the schematic
- D-014: Reviewer-A F8/F9: TP5 moved to LED_A (LED anode, R22/D2), as Pico 2 §3.1 p.9 / Fig. 11 p.20 (D-002); F18: KiCad app pinned `kicad.app: ">=9.0.2,<9.1"`, `ohmai check kicad-app`
- D-015: Bring-up gate requires a human sign-off (`require_kind: human`; owner may sign, agents author); safety unchanged
- D-016: Schematic gate approved: Reviewer-A's re-verified review passes; Reviewer-A's level-3 independence accepted by the owner for this gate and files_hash a052ad17 only (alternatives tried recorded); phase 7 merged
- D-017: Phase 8 answers: P8-1 (a) no mounting holes (H1/H2 removed, R-05 amended); P8-2 Pico 2 pin positions and 51 × 21 kept, end pins 1/20/21/40 without half-holes (JLC castellation pad-edge ≥ 1 mm / hole-to-corner ≥ 3 mm rules met by the other 36), JLC confirms in quote; P8-3 non-plated rear slot; P8-4 tab depth checked at bring-up; P8-5 TP mapping; P8-6 (i)-(iii) deviations accepted
- D-018: P8-7 (a): U1 decoupler rows moved 0.6–1.0 mm outward (minimum that works) for escape channels; same pins; Freerouting 2.1.0 unchanged, no inner-layer signals, via size unchanged
- D-019: P8-8 (c): Freerouting 2.1.0 → 2.2.4 on OpenJDK 25.0.4.1 (side by side with Java 21), after known-bad/golden/canary + same-DSN comparison; headless, analytics/telemetry off, no network
- D-020: P8-8 (b): signals allowed on In2 (3V3) with the pour around them; In1 GND stays solid; short In2 stubs, no 3V3 islands, USB D+/D- off In2 if possible
- D-021: Placement rework around U1 (RP2350) for escape channels
- D-022: Hand-route all remaining P2 connections, scripted (hardware/gen/pcb/handroute.py, replayable)
- D-023: Longer In2 signal runs for the last connections (pico-k-only, extends D-020): 3V3 In2 pour one piece, necks >= 0.5 mm (>= 0.8 mm near U1/decouplers), In1 solid, USB off In2
- D-024: Right passive column next to U1 shifted ~0.5 mm east (pico-k-only); applies with D-025
- D-025: C18/C27 4.7 µF 0603 → 0402 TDK105CBJ475MV-F (Taiyo Yuden, LCSC C22385335, 25 V X5R ±20 %, JLC extended); ≈ 2.7 µF at 3.3 V vs ≈ 3.2 µF accepted; reason: GP22/26/27/28 escape room
- D-026: Q1 next to U1 east impossible (no room); option 2 applied: Q1 stays west, R19/R9 moved next to it (electrically identical); hand-route the last links (done 2026-10-17, board clean; U1.23-C9 direct link not possible, see outcome)
- D-027: C9 (DVDD 100 nF) vertical directly under U1.23 (0.87 mm on F.Cu, no via), C28 moved down; crystal corner re-routed, board clean
- D-028: Layout reviewer Reviewer-A; level-3 independence accepted for review:layout on files_hash c71de844 and (2026-10-24) D-030 files_hash a0379e72 only (a cloud agent on another vendor/model was possible but would use the cloud agent allowance before the monthly reset)
- D-029: Reviewer-A L1 (C20 at TPS63001 VIN) originally deferred on the pre-D-030 BOM (3e2d005); superseded by D-030, which resolves L1 on the 51x21 mm board (5d80779)
- D-030: BOM + layout rework for Reviewer-A L1/L5/L6/L13/Q3 at 51x21 (5d80779): L2 → Murata DFE201612P-2R2M (C79317, all-layer keepout under coil); C20 → CL21A106KAYNNNE 0805 (C15850; C20.1→U3.5 = 1.65 mm center-to-center / 1.55 mm F.Cu w=0.30 mm, 0 vias); add C32 100 nF 0402 (C1525) on ADC_AVDD U1.44; 0 DRC, 0 unconnected; L2–L4 and L7–L12 accepted by owner as 51x21 trade-offs (2026-10-24)

## Checklist
- [ ] Every row: MPN, footprint, rating, temperature, lifecycle, stock, price source and date.
- [ ] Second source or written single-source acceptance per row; refs match the schematic.

## Required output
Write `reviews/bom/<your-name>.md` exactly in this format:

```markdown
---
reviewer: <your name>            # must differ from every author
kind: agent                      # agent | human
vendor: <model vendor, or 'n/a' for a human>
model: <model name and version, or 'n/a'>
instructions: <skill / system-prompt identity, e.g. 'reviewer-a skill v3'>
independence: <1-4, the level achieved (see above)>
independence_note: <what you asked for and why this level>
files_hash: sha256:d72c9a74f7936c70b25643fb5a61428d4c77b630e56b1cf8639e3fa4c0f8ff72
date: 2026-10-25
---
| ID | File | Verdict | Finding | Cite |
|----|------|---------|---------|------|
| F1 | bom/bom.csv | OK | | |
| F2 | <file> | issue | <what is wrong and the correct value> | p.<n> <section> |
| F3 | <file> | question | <what the source leaves open> | p.<n> |
```

- One row at least per file in scope; `Verdict` is `OK`, `issue` or `question`.
- `files_hash` must be the hash above; if the files change, the author regenerates this brief and you
  re-verify and update your hash.
- The author answers every issue in `reviews/bom/resolutions.md` (`fixed` + commit, or `accepted`
  by the owner with a reason). You do not write resolutions.
