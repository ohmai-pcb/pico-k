# Round 1 `review:bom` Resolutions (`Reviewer-A`)

All 5 blockers (`B1`–`B5`), 2 should-fix items (`S1`–`S2`), and 3 nits (`N1`–`N3`) from `Reviewer-A` Round 1 (`reviews/bom/reviewer-a.md`) have been resolved in `bom/bom.csv`, `parts/selection.md`, `bom/README.md`, and `ohmai/cli/src/ohmai/checks/bom.py`:

## Blockers (`B1`–`B5`)

- **B1 resolved (`Q1` `DMG1012T-7`, `SOT-523`)**:
  - Replaced the `SOT-323` (`SC-70-3`) and high-`VGS(th)` `2N7002` alternates in `bom/bom.csv` row 28 (`Q1`) and `parts/selection.md` with true `SOT-523` (`1.6 × 1.6 mm`) low-`VGS(th)` N-MOSFETs verified in `.toolcache/jlcparts/cache.sqlite3`:
    - `WNM4153-3/TR` (`Will Semicon`, `LCSC C239557`, `SOT-523`, 20 V, `VGS(th) <= 1.0 V`, `RDS(on) = 320 mΩ @ VGS = 1.8 V`, `$0.0423 @100`, 4,667 stock).
    - `PNM523T201E0` (`Prisemi`, `LCSC C110710`, `SOT-523`, 20 V, `VGS(th) <= 1.1 V`, `RDS(on) = 450 mΩ @ VGS = 1.8 V`, `$0.0278 @100`, 6,141 stock).
  - Removed the stale `"no second source named yet (P4-9)"` note from `notes`.

- **B2 resolved (`L2` `DFE201612P-2R2M`, `2016` 2.2 µH)**:
  - Replaced the unverified/underrated alternates in `bom/bom.csv` row 19 (`L2`) and `parts/selection.md` with verified `2016` (`2.0 × 1.6 mm`) 2.2 µH power inductors meeting `Isat >= 1.5 A, Irms >= 1.5 A, DCR <= 150 mΩ` (`TPS63001` `SLVS520C` Table 1 p.10):
    - `WPN201610M2R2MT` (`Sunlord`, `LCSC C97011`, `Isat = 2.0 A`, `Irms = 1.6 A`, `DCR = 135 mΩ`, `$0.0423 @100`, 3,030 stock).
    - `FTC201612S2R2MBCA` (`cjiang`, `LCSC C18724414`, `Isat = 3.3 A`, `Irms = 3.1 A`, `DCR = 90 mΩ`, `$0.0441 @100`, 14,422 stock).
    - `PFM201610-2R2MTS00` (`FH Guangdong Fenghua`, `LCSC C42885593`, `Isat = 2.8 A`, `Irms = 2.1 A`, `DCR = 120 mΩ`, `$0.0332 @100`, 7,011 stock).

- **B3 resolved (`SW1` `TS-1187A-B-A-B`, `5.1 × 5.1 mm` SMD)**:
  - Replaced `K2-1187SA-A4SW-06` (`C127507`, 4.2 mm tall + locating pegs) with 1.5 mm low-profile flat-bottom `1187`-series switches matching the `SW_SPST_TS-1187A` land pattern (`6.4 × 5.1 × 1.6 mm`):
    - `K2-1187SQ-A4SW-06` (`Korean Hroparts Elec`, `LCSC C92584`, `5.2 × 5.2 × 1.5 mm`, `$0.0507 @100`, 41,514 stock).
    - `TS-1187-1526` (`SOFNG`, `LCSC C111461`, `5.2 × 5.2 × 1.5 mm`, `$0.0266 @100`, 12,252 stock).
  - Removed the stale `"no second source named yet (P4-9)"` note from `notes`.

- **B4 resolved (`D2` `KT-0805G`, `0805` green LED)**:
  - Restored `"generic: 0805 green LED (cathode on KiCad Pad 1 = West = GND)"` in `second_source` alongside `approved_alternates`, documented the `KT-0805G` datasheet p.2 pin-numbering note (`Pin 1 = Anode, Pin 2 = Cathode` mapped via `parts/symbol-maps/KT-0805G.yaml` so KiCad Pad 1 = West = GND receives the cathode mark of any alternate LED), and replaced the `0603` / wrong-`C#` alternates with true `0805` green LEDs verified in `jlcparts`:
    - `ORH-G35A` (`Orient`, `LCSC C205442`, `0805`, `$0.0157 @100`, 90,843 stock).
    - `NCD0805G1` (`Foshan NationStar Optoelectronics`, `LCSC C84260`, `0805`, `$0.0232 @100`, 389,063 stock).
    - `LTST-C170KGKT` (`Lite-On`, `LCSC C98221`, `0805`, `$0.0337 @100`, 212,002 stock).

- **B5 resolved (All 19 additional rows with wrong LCSC `C#` in `approved_alternates` / `second_source` + automated `jlcparts` SQLite cross-check)**:
  - Updated all 19 rows (`U2`, `Y1`, `C16 C17 C28 C29`, `C18 C27`, `R5`, `C1..C15 C32`, `C23 C24`, `R3 R4`, `R1 R2`, `R22`, `C19 C21 C22 C31`, `C20`, `R12 R13 R14`, `R15`, `R18`, `R19`, `R16`, `R20`, `R21`, `R10 R11`, `C25 C26`) with exact LCSC `C#` codes and `@100` unit prices verified against `.toolcache/jlcparts/cache.sqlite3`.
  - Added `check_row_jlcparts_codes` to `bom_schema` / `bom_lock` in `ohmai/cli/src/ohmai/checks/bom.py` (with unit test `test_bom_jlcparts_db_cross_check` in `tests/test_improvements.py`) so every `C\d+` code in `supplier_pn`, `approved_alternates`, and `second_source` is automatically cross-checked against the `jlcparts` SQLite database whenever available.

## Should-Fix (`S1`–`S2`)

- **S1 resolved (`D1` `MBR120VLSFT1G`, `SOD-123F` ultra-low-`Vf` Schottky)**:
  - Replaced standard-`Vf` (`0.45–0.60 V`) gull-wing `SOD-123` alternates with flat-lead (`SOD-123W` / `SOD-123F`) ultra-low-`Vf` (`<= 0.36 V @ 1 A`) Schottky diodes preserving the `TPS63001` UVLO margin under `R-02` (`4.75 V` min `VBUS`) and `D-010` USB attach droop:
    - `PMEG2010ER,115` (`Nexperia`, `LCSC C82288`, `SOD-123W`, 20 V, 1 A, `Vf = 340 mV @ 1 A`, `$0.1423 @100`, 8,930 stock).
    - `RB161MM-20TR` (`ROHM Semicon`, `LCSC C123070`, `SOD-123F`, 20 V, 1 A, `Vf = 350 mV @ 1 A`, `$0.1656 @100`, 25,310 stock).
    - `CRS08(TE85L,Q,M)` (`Toshiba`, `LCSC C141550`, `SOD-123F`, 30 V, 1.5 A, `Vf = 360 mV @ 1.5 A`, `$0.1146 @100`, 16,779 stock).

- **S2 resolved (`L1`, `U3` single-source rows)**:
  - Cleared `approved_alternates` on single-source rows `L1` (`MPL-AT2512-3R3`) and `U3` (`TPS63001DRCR`) so all 6 single-source rows (`U1`, `Y1`, `L1`, `U3`, `U5`, `J2 J3`) uniformly leave `approved_alternates` blank and record rejected non-drop-in candidates only in `second_source` (`checked: ...`) and `notes`.

## Nits (`N1`–`N3`)

- **N1 resolved**: Updated `bom/bom.csv` line 3 comment (20 board-only footprints `J4`, `JP1–JP6`, `NT1`, `TP1–TP12` per `D-012`/`D-013`), row 5 (`L1` `notes`: external 1.1 V DVDD fallback via off-board feed at `TP7` with `JP5`/`JP6` per `D-013`), and row 20 (`C19 C21 C22 C31` `notes`: `C20` moved to its own `0805` row per `D-030`, amending `1206` `D-009`).
- **N2 resolved**: Documented in `bom/README.md` that functionally distinct roles (`R15` `3V3_EN` pull-up vs `R16` `TPS63001` `PS/SYNC` pull-down) or independent DNP groups (`R6` flash `CS` pull-up vs `R23 R24` `MAX31856` `DRDY`/`FAULT` pull-ups) may occupy separate rows so role-specific notes and assembly options remain unambiguous.
- **N3 resolved**: Synchronized `parts/selection.md` (`§4B`, `D-025`/`D-030` table, and `§Phase 10 BOM lock`) with the exact verified alternates and `LCSC C#` codes in `bom/bom.csv`.
