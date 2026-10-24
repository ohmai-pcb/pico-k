# EVB comparison: MAX31856MUD+T (U5, sheet `thermocouple`)
Reference: MAX31856 datasheet 19-7534 Rev 0, Fig. 8 Typical Connection to Reduce the Effect of Noise Pickup (p.27).

| Vendor ref | Function | Vendor value / MPN | Ours | Same? | Reason if different (cite) |
|------------|----------|--------------------|------|-------|----------------------------|
| series R (T+) | input filter | 100 Ω | R12 100 Ω | yes | p.27 |
| series R (T-) | input filter | 100 Ω | R13 100 Ω | yes | p.27 |
| diff C | T+ to T- | 0.1 µF | C14 100 nF X7R | yes | p.27 |
| CM C | T+ / T- to GND | 0.01 µF each | C25, C26 10 nF X7R 50 V | yes | p.27 |
| BIAS | to T- | connector side of the T- 100 Ω | U5.2 on TC_N (connector side of R13) | yes | p.27 |
| AVDD / DVDD bypass | 0.1 µF each | 0.1 µF | C12, C13 100 nF on 3V3 | yes | p.27 |
| CS | chip select | - | GP13 via JP2 + R7 10 kΩ pull-up on the IC side | added | architecture.md A2-2 (R-14) |
| DRDY / FAULT | outputs | - | test pads TP11/TP12 + DNF 10 kΩ pull-ups R23/R24 | added | D-009 (P5-9) |
| TC connector | J2/J3 Omega PCC-SMD | - | NOT PLACED: no official KiCad symbol (owner decision, phase 7) | open | STATUS P7-1 |
