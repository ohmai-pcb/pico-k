---
ohmai_review_brief: 1
ohmai_version: 0.1.0.dev0
phase: constraints
created: '2026-10-15'
files_hash: sha256:5deef3c946f0d15514e5c0ecb862d1eca087832be882dcc65abd5b7370d39dd9
required_reviews: 1
min_independence: 3
authors:
- name: OhmAI
  kind: agent
  vendor: Grok Bot
  model: Grok Bot
  instructions: ohmai-skill 0.1.0.dev0
files:
  parts/constraints/ABM8-272-T3.yaml: 5378bd77f09b494de593b5c83ab25bab4ba1778f634fc014d46a8005f82b436a
  parts/constraints/DMG1012T-7.yaml: e1b19df77a47859043008005080d9fdccd57ba652be552399aacf0025d52f720
  parts/constraints/KT-0805G.yaml: cd129021c98e92a6ea22eb37036beda4d29302a65d89af23517cde6914185812
  parts/constraints/MAX31856MUD+T.yaml: 3c18dd43d12396ad3ff96d24612d1edd3c999605652010466eef0bf64aaf5cda
  parts/constraints/MBR120VLSFT1G.yaml: dbc226b71986e2d78619bc0d98eb3d826f7503e1adf78dc14ce6bf72ba9fc0b4
  parts/constraints/MPL-AT2512-3R3.yaml: 308a5481cf779274445fa3ccb1b28f4dd442b81a69e6948c2aece827815b0cd4
  parts/constraints/PCC-SMD.yaml: f01a3fda54f52446d358c6b5f7985b31bd0bc72d0e2c0265ed7f299846ec47df
  parts/constraints/RP2350A.yaml: 3b704eff515e2a7a692ff9d2083d727738559bb181bc9f2bf0e08091dc5a2e13
  parts/constraints/TPS63001DRCR.yaml: ad65c808e50286663752e43a91a83279a1cfb26fe98d389b61a7baf240746f6c
  parts/constraints/TS-1187A-B-A-B.yaml: 37b618dbccc93b9d00c618ae284aa269ae88d5f33399fc650f7c7695aa4c4204
  parts/constraints/TYPE-C-16PIN-2MD-073.yaml: f8607ae825c0c072484ee47d1214d5a30233cbaedcab3a8e1c99362a89954eaa
  parts/constraints/USBLC6-2SC6.yaml: 2a793cc4a9e1895ecb486d03fe6a4b4afb7e121cd2c5337826b1a70836dc6615
  parts/constraints/W25Q32RVXHJQ.yaml: a2e8e4b5a144da196173e5bc34ebe80fc4ce63561bf656e5b1553d0995e5b28d
---
# Independent review brief: phase `constraints` (pico-k)

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
Minimum configured for this gate: level 3 (a lower level is recorded and WARNs).

## Authors (the reviewer must differ)
- name=OhmAI; kind=agent; vendor=Grok Bot; model=Grok Bot; instructions=ohmai-skill 0.1.0.dev0

## Files in scope (13), content hash `sha256:5deef3c946f0d15514e5c0ecb862d1eca087832be882dcc65abd5b7370d39dd9`

| File | sha256 |
|---|---|
| `parts/constraints/ABM8-272-T3.yaml` | `5378bd77f09b` |
| `parts/constraints/DMG1012T-7.yaml` | `e1b19df77a47` |
| `parts/constraints/KT-0805G.yaml` | `cd129021c98e` |
| `parts/constraints/MAX31856MUD+T.yaml` | `3c18dd43d123` |
| `parts/constraints/MBR120VLSFT1G.yaml` | `dbc226b71986` |
| `parts/constraints/MPL-AT2512-3R3.yaml` | `308a5481cf77` |
| `parts/constraints/PCC-SMD.yaml` | `f01a3fda54f5` |
| `parts/constraints/RP2350A.yaml` | `3b704eff515e` |
| `parts/constraints/TPS63001DRCR.yaml` | `ad65c808e502` |
| `parts/constraints/TS-1187A-B-A-B.yaml` | `37b618dbccc9` |
| `parts/constraints/TYPE-C-16PIN-2MD-073.yaml` | `f8607ae825c0` |
| `parts/constraints/USBLC6-2SC6.yaml` | `2a793cc4a9e1` |
| `parts/constraints/W25Q32RVXHJQ.yaml` | `a2e8e4b5a144` |

### Changed since the brief last reviewed by Reviewer-A (sha256:c9a92462173a...) (verify these first)
- `parts/constraints/ABM8-272-T3.yaml`
- `parts/constraints/DMG1012T-7.yaml`
- `parts/constraints/KT-0805G.yaml`
- `parts/constraints/MAX31856MUD+T.yaml`
- `parts/constraints/MBR120VLSFT1G.yaml`
- `parts/constraints/MPL-AT2512-3R3.yaml`
- `parts/constraints/PCC-SMD.yaml`
- `parts/constraints/RP2350A.yaml`
- `parts/constraints/TPS63001DRCR.yaml`
- `parts/constraints/TS-1187A-B-A-B.yaml`
- `parts/constraints/TYPE-C-16PIN-2MD-073.yaml`
- `parts/constraints/USBLC6-2SC6.yaml`
- `parts/constraints/W25Q32RVXHJQ.yaml`

## Sources
- `datasheets/ABM8-272-T3.pdf`
- `datasheets/DMG1012T-7.pdf`
- `datasheets/KT-0805G.pdf`
- `datasheets/MAX31856MUD+T.pdf`
- `datasheets/MBR120VLSFT1G.pdf`
- `datasheets/MPL-AT2512-3R3.pdf`
- `datasheets/PCC-SMD.pdf`
- `datasheets/RP2350A.pdf`
- `datasheets/TPS63001DRCR.pdf`
- `datasheets/TS-1187A-B-A-B.pdf`
- `datasheets/TYPE-C-16PIN-2MD-073.pdf`
- `datasheets/USBLC6-2SC6.pdf`
- `datasheets/W25Q32RVXHJQ.pdf`
- `bom/bom.csv`
- `datasheets/README.md`
- `docs/decisions.md`

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

## Checklist
- [ ] Every pin of the part is listed; number and name match the datasheet pin table (cite the page).
- [ ] Every direction is right for the pin function; no `unknown` left without an open question.
- [ ] Abs max / recommended values, units and min/max/nominal match the cited page exactly.
- [ ] Required external parts (value, tolerance, `to:` pin or net, total_on_net) match the datasheet or reference design.
- [ ] Every cite points at the page number printed on the page, and the page really says it.
- [ ] Open questions are real questions; resolutions marked in the file match docs/decisions.md.

## Required output
Write `reviews/constraints/<your-name>.md` (also accepted: `docs/review-constraints-reviewer-a.md`) exactly in this format:

```markdown
---
reviewer: <your name>            # must differ from every author
kind: agent                      # agent | human
vendor: <model vendor, or 'n/a' for a human>
model: <model name and version, or 'n/a'>
instructions: <skill / system-prompt identity, e.g. 'reviewer-a skill v3'>
independence: <1-4, the level achieved (see above)>
independence_note: <what you asked for and why this level>
files_hash: sha256:5deef3c946f0d15514e5c0ecb862d1eca087832be882dcc65abd5b7370d39dd9
date: 2026-10-15
---
| ID | File | Verdict | Finding | Cite |
|----|------|---------|---------|------|
| F1 | parts/constraints/ABM8-272-T3.yaml | OK | | |
| F2 | <file> | issue | <what is wrong and the correct value> | p.<n> <section> |
| F3 | <file> | question | <what the source leaves open> | p.<n> |
```

- One row at least per file in scope; `Verdict` is `OK`, `issue` or `question`.
- `files_hash` must be the hash above; if the files change, the author regenerates this brief and you
  re-verify and update your hash.
- The author answers every issue in `reviews/constraints/resolutions.md` (`fixed` + commit, or `accepted`
  by the owner with a reason). You do not write resolutions.

## Note
P5-1 was delegated to Reviewer-A (owner, D-007) with the output path docs/review-constraints-reviewer-a.md. That path is accepted as well as reviews/constraints/reviewer-a.md; either way it needs the header and table format above. Owner decisions D-006/D-007 are locked: flag conflicts as questions, do not reopen. DC-bias values marked ESTIMATE are already tracked as open owner item P5-10; report anything you find on them as usual.
