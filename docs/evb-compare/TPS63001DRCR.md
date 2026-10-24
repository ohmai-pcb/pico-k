# EVB comparison: TPS63001DRCR (U3, sheet `regulator`)
Reference: TI SLVS520C §8.2 Fig. 2 Typical Application Circuit and Table 1 List of Components (p.10).
Ours: `hardware/regulator.kicad_sch`. Pin functions p.3.

| Vendor ref | Function | Vendor value / MPN | Ours | Same? | Reason if different (cite) |
|------------|----------|--------------------|------|-------|----------------------------|
| L1 | L1-L2 inductor | 2.2 µH VLF4012-2R2 (TDK) | L2 2.2 µH SWPA3015S2R2MT | value yes, part no | JLC stock / 3 × 3 mm (D-006, parts/selection.md) |
| C1 | VIN cap | 10 µF 6.3 V 0603 X7R | C20 10 µF 50 V 1206 X5R CL31A106KBHNNNE | value yes | DC-bias derating at VSYS 5 V (D-008, D-009) |
| C2 | VOUT cap | 2 × 10 µF 6.3 V 0603 X7R | C21 C22 C31 3 × 10 µF 25 V 0603 X5R | no (3 × instead of 2 ×) | DC-bias derating to keep ≈ 15 µF effective (D-008) |
| C3 | VINA cap | 0.1 µF X7R | C15 100 nF 16 V X7R 0402 | yes | - |
| R3 | VIN → VINA filter | 100 Ω | R14 100 Ω | yes | - |
| R1, R2 | FB divider | not used at TPS63001 | none, FB (pin 10) to VOUT | yes | fixed-output part: FB to VOUT (p.10) |
| EN | enable | drawn at the IC in Fig. 2; no part in Table 1 | R15 100 kΩ pull-up to VSYS + Pico pin 37 3V3_EN | no | Pico 2 3V3_EN behaviour (Pico 2 datasheet §5.4 p.15) |
| PS/SYNC | power save | drawn at the IC in Fig. 2; no part in Table 1 | R16 100 kΩ to GND + RP2350 GPIO23 (SMPS_PS) + TP4 | no | Pico 2 GPIO23 PS control (D-004, constraints/TPS63001DRCR.yaml pin 7) |
| EP | thermal pad | PGND | pin 11 to GND | yes | p.3 |
