# BOM options to fix L1 at 51x21 (PROPOSAL ONLY)

This is a proposal only: the BOM, schematic and board are unchanged. The owner decided on 2026-10-23 to keep 51x21 (R-02).
Parts data comes from the jlcparts snapshot of 2026-10-15/17 (`ohmai parts search`). Datasheets are the public ones; probes used temporary netlist footprint patches that were restored afterwards (cmp OK, pcb sha 2d0f674a54a7 unchanged).

## Candidates

| # | Change | Part (LCSC) | Pkg | Basic/Ext | Stock | Price | Space freed |
|---|--------|-------------|-----|-----------|-------|-------|-------------|
| A | L2 SWPA3015S2R2MT (C43389) -> **Murata DFE201612P-2R2M=P2** | C79317 | 0806 (2016) | ext | 7,809 | $0.1061 | courtyard 3.65x4.66 -> ~2.5x2.1 (-12.3 mm2, ~70%) |
| A' | alt L2: Sunlord WPN252012H2R2MT | C98350 | 1008 (2520) | ext | 70,539 | $0.0432 | ~3.0x2.6 courtyard; **not probed**; datasheet image-only |
| A'' | alt L2: Sunlord WPN201610H2R2MT | C97005 | 0806 | ext | 8,437 | $0.0417 | same as A; Isat 1.45 A, DCR 170 mOhm (worse) |
| B | C20 CL31A106KBHNNNE 1206 (C13585) -> **CL21A106KAYNNNE 0805 10 uF 25 V X5R** | C15850 | 0805 | **basic** | 3,710,191 | $0.0692 | 1206->0805: ~-1.2 mm length, -0.35 mm width; keeps C20 off the J4 strip |
| C | Drop SW1 (TS-1187A, courtyard 7.55x7.42), BOOTSEL via TP6 | - | - | - | - | -$ | ~56 mm2 east of U1 (helps L4/L5 decap, not L1); not probed |
| D | Q3: 100 nF ADC_AVDD | CL05B104KO5NNNC C1525 | 0402 | basic | 22.5 M | $0.0043 | adds a part (~1.0x0.6 courtyard); placement not probed |
| X | C20 -> 22 uF 0805 CL21A226MAQNNNE C45783 | | 0805 | basic | | $0.2384 | **rejected**: VBUS capacitance > 10 uF (USB 2.0 7.2.4.1) |

## Electrical justification

- **A (L2):**
  - TPS63001 SLVS520C asks for L = 2.2 uH (Table 1, p.10). Low DCR is advised (p.11).
  - The Isat requirement comes from Eq. 3-4 (p.11-12) plus a 20 % margin (p.12). The project's peak is 0.79 A (VIN 1.8 V, 0.352 A out), so Isat must be >= 0.95 A (selection.md).
  - The DFE201612P-2R2M=P2 (spec p.2/9) gives 2.2 uH +/-20 %, a rated current of 2.1 A (inductance change) and 1.5 A (temperature rise), and DCR 144 mOhm max. That meets the Isat need with margin. The current part's DCR is 78 mOhm, so losses go from ~40 mW to ~75 mW at 1.8 V in (~0.72 A rms). At the usual 3.0-4.2 V input the extra loss is well under half of that.
  - The DFE family is not in the Table 2 list (p.11). That list is examples, not a requirement; the electrical parameters above fit.
  - Murata notes (spec ~p.7): no vias or copper directly under the coil, and no contact with other parts. Keep inner-layer copper clear under L2 or accept that.
  - Footprint: the probes used KiCad `Inductor_SMD:L_Murata_DFE201610P` as a stand-in (same 2016 body). Check the land pattern against spec p.5 before adopting it.
- **B (C20):**
  - Cin must be >= 4.7 uF near VIN/PGND (SLVS520C p.12, 8.2.2.3.1).
  - Samsung char sheet CL21A106KAYNNNE_Char.pdf, graph 3 (DC bias), reads about -42 % at 5 V, so ~5.8 uF typical. At -10 % tolerance and 5.25 V it is ~5.0 uF. That still meets 4.7 uF, but with little margin. The current 1206 gives ~7.75 uF.
  - VBUS total capacitance drops slightly, which is good for the 10 uF limit.
- **C (SW1):** RP2350 BOOTSEL is QSPI_SS pulled to GND at reset. TP6 already exposes it. Removing SW1 loses the user/boot button; you would need tweezers or a pogo pin on TP6. This is a product decision.
- **D:** a standard 0402 X7R 16 V decap; the bias derating at 3.3 V is negligible for 100 nF.

## Fit / DRC verification (51x21, temporary board, restored afterwards)

Probes live in `.toolcache/rv2/probes/`.

| Probe | BOM | Result |
|-------|-----|--------|
| f1-f3, f5 | A | U3 block fails (L2 vs L1/U3, or C21 vs U4/J1) |
| f4 | A | fit ALL OK. DRC: courtyard J4-C20 (1206) and J4-R18, plus 2 silk |
| **f6** | **A+B** | **fit ALL OK. DRC: 1 courtyard (R18-J4), 2 silk (R11/U4, R11/D1). U3 block is clean.** C20.1-U3.5 2.21 mm, L2.1-U3.4 2.33, C21.2-U3.3 2.75, C15.1-U3.8 2.49 |
| f7, f8 | A+B, R18 moved | R18 does not fit beside U4 (3.8,10.65) or near C22 (4,14.2) |

In f6 U3 is at (14.0,9.6) r90, L2 at (16.0,13.3) r0, C20 at (17.2,9.8) r90 and C21 at (10.5,11.4). With these, the U3 (TPS63001) loop is compact and clear of J4.

The R18-J4 courtyard overlap left over is in the U4/USB block, not the U3 block. It is a placement problem, not caused by the BOM change. Possible fixes (not verified): R18 -> 0201, or route the VBUS_SENSE divider elsewhere.

## Recommendation (minimal set for L1)

**A + B**: L2 -> DFE201612P-2R2M=P2 (C79317, ext; L2 is already ext, so no extra feeder fee category) and C20 -> CL21A106KAYNNNE (C15850, basic).

- Combined price change ~+$0.08 per board.
- A alone fits the U3 block, but the 1206 C20 then intrudes on J4. B fixes that.
- C and D are optional and independent: C frees space for L4/L5 (U1 decap) at the cost of the button; D is the Q3 item.
