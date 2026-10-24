---
ohmai_review_brief: 1
ohmai_version: 0.1.0.dev0
phase: schematic
created: '2026-10-15'
files_hash: sha256:93f6c22fb2fd716cf941dc16c9adbee36ccc1ba8c3aba426abecf72a5afba0af
required_reviews: 1
min_independence: 2
authors:
- name: OhmAI
  kind: agent
  vendor: Grok Bot
  model: Grok Bot
  instructions: ohmai-skill 0.1.0.dev0
files:
  expected_nets.csv: 6ead5861263daa596c0b21d8fbae9cff98f947a04f5b57554ac59af3fe896d9b
  hardware/edge.kicad_sch: 144b9e2b2abcf88831bc5522551438ffb94d4d10cd3825a43b928ce4fffc2d65
  hardware/gen/layout/_root.yaml: 81d7aaa88f28d2bb7ad962d913b34f76d5d581f5430c60b9436fd9fe3f346b37
  hardware/gen/layout/edge.yaml: 16ea68fd24cf5240631a310fd34ef3727e567e1800fdf98f4f43e5e116bcf2a1
  hardware/gen/layout/led_boot_adc.yaml: 59054134add61489498a69d5efa43747aed56c18547101749aed46490d25d885
  hardware/gen/layout/mcu_core.yaml: ae2153c3ed1017cefe0eaa61735d726037c11415e781a1e4773f76522e18ecb7
  hardware/gen/layout/power_usb.yaml: 6602e3d3a22a4d213266f8134196537787d5a537835b3c8d422c4b38bf7b476a
  hardware/gen/layout/regulator.yaml: b3525db8c52c43016c0abdedd003472a632970b490fe59cdcc9f3f5953213137
  hardware/gen/layout/thermocouple.yaml: 708ae4b2a92e5f000d36f1917d90dc126c4e5bec2590dd9d8caa4dd44f7d7435
  hardware/led_boot_adc.kicad_sch: 834622dfda4e966033d4b1da9207360a9175b6aeefe64ce93c163e7f2eafabf7
  hardware/mcu_core.kicad_sch: 53101c22751d57a1f60e2f59ad6c990e4014abb36630794afa4a4d683739fdf8
  hardware/pico-k.kicad_sch: 9dad76d4d8e9b87f192bc0634fd7b523cf4b215718e2c86b49518082beca3b74
  hardware/power_usb.kicad_sch: da1542a9da231aa4b5cc6c10e9232b02a85c387e50cfb68aca0914962fe9767e
  hardware/regulator.kicad_sch: 3b65f2c0d16c75febf6bac2c27d28691805afbe6d8ae44f253f3df913d4b92af
  hardware/thermocouple.kicad_sch: d4328cde69282de92d95b1e71080d1ede7a4268c64e35c56e6b112c51e41c203
  parts/symbol-maps/ABM8-272-T3.yaml: 27dfc9bf9e542c9de64f959de5011a257d6a42ca434932d07497ebf0b55f9550
  parts/symbol-maps/KT-0805G.yaml: ad06c69015412c11c12da1bae6d2d377e0491d3cd480589335126f10c75cb0c1
  parts/symbol-maps/MPL-AT2512-3R3.yaml: 77e0e121e3221b494cf568bc63a458449a15c3987c6835afcef133f169a86d71
  parts/symbol-maps/PCC-SMD.yaml: cb7406a8d2f478c2b4091c8f938d37bbb19753121b4c151cae33eabe7ee52b7f
  parts/symbol-maps/TPS63001DRCR.yaml: 58e552536078d4f00a0170fcdb614b2e77f3e720d6ace41c672720e2b359731e
  parts/symbol-maps/TS-1187A-B-A-B.yaml: da670b3b7dfa89a7497ff309253b77a5795f92d64e352b96970e8593cb757e8d
  parts/symbol-maps/TYPE-C-16PIN-2MD-073.yaml: 6b719910ddf97942a2f755786e36dd268f6f052f1d1bf1de69d7b87bc5090ee7
  parts/symbol-maps/W25Q32RVXHJQ.yaml: 241bd9bb1c6262592783bab4e4acae29a5c4d7c0110d9118e3f6cd21b4b4604a
---
# Independent review brief: phase `schematic` (pico-k)

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
Required for this gate: level 2 or better (a smaller number; 1 = most independent). A weaker level (larger number) is recorded and WARNs.

## Authors (the reviewer must differ)
- name=OhmAI; kind=agent; vendor=Grok Bot; model=Grok Bot; instructions=ohmai-skill 0.1.0.dev0

## Files in scope (23), content hash `sha256:93f6c22fb2fd716cf941dc16c9adbee36ccc1ba8c3aba426abecf72a5afba0af`

| File | sha256 |
|---|---|
| `expected_nets.csv` | `6ead5861263d` |
| `hardware/edge.kicad_sch` | `144b9e2b2abc` |
| `hardware/gen/layout/_root.yaml` | `81d7aaa88f28` |
| `hardware/gen/layout/edge.yaml` | `16ea68fd24cf` |
| `hardware/gen/layout/led_boot_adc.yaml` | `59054134add6` |
| `hardware/gen/layout/mcu_core.yaml` | `ae2153c3ed10` |
| `hardware/gen/layout/power_usb.yaml` | `6602e3d3a22a` |
| `hardware/gen/layout/regulator.yaml` | `b3525db8c52c` |
| `hardware/gen/layout/thermocouple.yaml` | `708ae4b2a92e` |
| `hardware/led_boot_adc.kicad_sch` | `834622dfda4e` |
| `hardware/mcu_core.kicad_sch` | `53101c22751d` |
| `hardware/pico-k.kicad_sch` | `9dad76d4d8e9` |
| `hardware/power_usb.kicad_sch` | `da1542a9da23` |
| `hardware/regulator.kicad_sch` | `3b65f2c0d16c` |
| `hardware/thermocouple.kicad_sch` | `d4328cde6928` |
| `parts/symbol-maps/ABM8-272-T3.yaml` | `27dfc9bf9e54` |
| `parts/symbol-maps/KT-0805G.yaml` | `ad06c6901541` |
| `parts/symbol-maps/MPL-AT2512-3R3.yaml` | `77e0e121e322` |
| `parts/symbol-maps/PCC-SMD.yaml` | `cb7406a8d2f4` |
| `parts/symbol-maps/TPS63001DRCR.yaml` | `58e552536078` |
| `parts/symbol-maps/TS-1187A-B-A-B.yaml` | `da670b3b7dfa` |
| `parts/symbol-maps/TYPE-C-16PIN-2MD-073.yaml` | `6b719910ddf9` |
| `parts/symbol-maps/W25Q32RVXHJQ.yaml` | `241bd9bb1c62` |

### Changed since the brief last reviewed by Reviewer-A (sha256:0616527e6d36...) (verify these first)
- `expected_nets.csv`
- `hardware/edge.kicad_sch`
- `hardware/gen/layout/_root.yaml`
- `hardware/gen/layout/edge.yaml`
- `hardware/gen/layout/led_boot_adc.yaml`
- `hardware/gen/layout/mcu_core.yaml`
- `hardware/gen/layout/power_usb.yaml`
- `hardware/gen/layout/regulator.yaml`
- `hardware/gen/layout/thermocouple.yaml`
- `hardware/led_boot_adc.kicad_sch`
- `hardware/mcu_core.kicad_sch`
- `hardware/pico-k.kicad_sch`
- `hardware/power_usb.kicad_sch`
- `hardware/regulator.kicad_sch`
- `hardware/thermocouple.kicad_sch`

## Sources
- `docs/decisions.md`
- `parts/constraints/ABM8-272-T3.yaml`
- `parts/constraints/DMG1012T-7.yaml`
- `parts/constraints/KT-0805G.yaml`
- `parts/constraints/MAX31856MUD+T.yaml`
- `parts/constraints/MBR120VLSFT1G.yaml`
- `parts/constraints/TPS63001.example.yaml`
- `parts/constraints/MPL-AT2512-3R3.yaml`
- `parts/constraints/PCC-SMD.yaml`
- `parts/constraints/RP2350A.yaml`
- `parts/constraints/TPS63001DRCR.yaml`
- `parts/constraints/TS-1187A-B-A-B.yaml`
- `parts/constraints/TYPE-C-16PIN-2MD-073.yaml`
- `parts/constraints/USBLC6-2SC6.yaml`
- `parts/constraints/W25Q32RVXHJQ.yaml`

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

## Checklist
- [ ] Every pin connection matches parts/constraints/<PART>.yaml and expected_nets.csv.
- [ ] Values, ratings and derating (docs/safety.md) of every passive; pull-ups, strapping, I2C addresses.
- [ ] Power tree, decoupling per pin, reset/boot, ESD and connector pinout (cite pages).

## Required output
Write `reviews/schematic/<your-name>.md` exactly in this format:

```markdown
---
reviewer: <your name>            # must differ from every author
kind: agent                      # agent | human
vendor: <model vendor, or 'n/a' for a human>
model: <model name and version, or 'n/a'>
instructions: <skill / system-prompt identity, e.g. 'reviewer-a skill v3'>
independence: <1-4, the level achieved (see above)>
independence_note: <what you asked for and why this level>
files_hash: sha256:93f6c22fb2fd716cf941dc16c9adbee36ccc1ba8c3aba426abecf72a5afba0af
date: 2026-10-15
---
| ID | File | Verdict | Finding | Cite |
|----|------|---------|---------|------|
| F1 | expected_nets.csv | OK | | |
| F2 | <file> | issue | <what is wrong and the correct value> | p.<n> <section> |
| F3 | <file> | question | <what the source leaves open> | p.<n> |
```

- One row at least per file in scope; `Verdict` is `OK`, `issue` or `question`.
- `files_hash` must be the hash above; if the files change, the author regenerates this brief and you
  re-verify and update your hash.
- The author answers every issue in `reviews/schematic/resolutions.md` (`fixed` + commit, or `accepted`
  by the owner with a reason). You do not write resolutions.

## Note
Reviewer: Reviewer-A (owner, D-013). RE-CHECK ROUND (2026-10-15): your first review (files_hash 0616527e...) is answered in reviews/schematic/resolutions.md (fixes in bcfdc1c, D-014 in the commit after it). Re-verify on this brief and update reviews/schematic/reviewer-a.md (new files_hash): F1/F2 regulator R15 VSYS clear of the VINA node; F3 mcu_core core VREG vs RP2350 Fig. 22 p.453, especially the C16/C29/C17 to VREG_PGND loop drawn at U1 pin 47 (the KiCad RP2350A symbol has VREG_PGND on the bottom edge, opposite VREG_VIN/LX/FB) and the single-point NT1 join (p.454); the nit fixes; D-014: TP5 on LED_A (sheet 6) and kicad.app pin. Then, as before: Write reviews/schematic/reviewer-a.md with the YAML header above (reviewer, vendor, model, instructions, independence level 1-4 with independence_note, files_hash). Do all four: (a) NETS AND PINS: verify every net and pin against the cited datasheet page and against expected_nets.csv (the row comments cite the pin source per part); symbol pins that differ from the datasheet are mapped in parts/symbol-maps/*.yaml (check each mapping and its page; D2 LED pad numbering KT-0805G p.2, D-012). (b) READABILITY: run `ohmai check render` (or `ohmai check schematic`) to create out/render/png/pico-k*.png (out/ is not committed) and judge each sheet against the datasheet application figure it follows: thermocouple vs MAX31856 Fig. 8 (p.27); regulator vs TPS63001 SLVS520C typical application (p.1, Table 1 p.10); mcu_core vs the RP2350 minimal design (datasheets/hardware-design-with-rp2350.pdf) and the Pico 2 schematic (datasheets/pico-2-w-schematic.pdf p.1), VREG per RP2350 §6.3 p.451-455; power_usb vs USBLC6-2SC6 application (Fig. 14 p.8). Readability findings are issues like any other (cite the figure). (c) CRYSTAL: check the U1.21 XIN / U1.22 XOUT hookup (Y1, R3 1 kOhm, C23/C24) by hand: the passives check only WARNs here (kind crystal not machine-checked). Sources: HDG §4 Crystal Oscillator p.13-14 (Fig. 10), RP2350 datasheet Table 597 p.555, ABM8-272-T3 p.1 (CL 10 pF), p.2 (pads); nets XIN / XOUT / XTAL_OUT in expected_nets.csv (its header now cites HDG Fig. 10 p.13, Reviewer-A F5). (d) Also check the D-012/D-013 choices (P7-6 JP5/JP6 per Fig. 21 p.452, P7-8 agent choices). Report findings only; do not edit files.
