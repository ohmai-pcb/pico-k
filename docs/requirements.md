# Requirements: pico-k

Concept: Raspberry Pi Pico 2 form-factor board with an integrated Type-K thermocouple interface.

Rules: SI units with tolerances. Every number has a source (owner, standard, or datasheet). Unknowns go to
STATUS.md → Open questions, not into this table as guesses.

> **Status: LOCKED by the owner on 2026-10-15, decision D-001.** Changes need a new decision.
> Page numbers are the printed page numbers of the cited PDF. Prices are LCSC unit prices in USD,
> read 2026-10-15; they change daily and are not quotes.

Use case (owner, 2026-10-15): a compact general-purpose USB thermocouple probe module, powered and driven by a
laptop or a powerbank over USB.

## Must (the board fails without these)
| ID | Requirement | Value / limit | Unit | Source | Verify by |
|----|-------------|---------------|------|--------|-----------|
| R-01 | MCU | RP2350A (as on Pico 2) | - | owner, D-001 (Q1) | review |
| R-02 | Pico board outline (no overhang; the socket fits inside it, D-004 F1) | 51 × 21, 1 mm thick | mm | owner, D-001 (Q2), confirmed by D-004; Pico 2 datasheet p.7 | review of fab drawing |
| R-03 | 40 edge pins on the Pico grid, same positions and pin order as the Pico 2; castellated and 2.54 mm through-holes (1 mm holes) | 2 × 20 at 2.54 mm pitch | - | owner, D-001 (Q2); Pico 2 datasheet p.7 | review / 1:1 print |
| R-04 | Same pin functions as the Pico 2 on all 40 pins (GPIO, GND, AGND, RUN, ADC_VREF, 3V3, 3V3_EN, VSYS, VBUS) | as Pico 2 datasheet §3.1 | - | owner, D-001 (full Pico pinout kept); Pico 2 datasheet p.8–9 | review |
| R-05 | No mounting holes (D-017, P8-1 a): the module is soldered by its castellations/pads or carried on pin headers. The 2 Pico 2 holes at the USB end would clash with the USB-C receptacle shell tabs, and the 2 holes at the sensor end are dropped for the PCC-SMD socket. SWD header dropped: SWCLK/SWDIO/GND on flat bottom test pads | 0 holes | - | owner, D-001 (Q2) amended by D-002, D-004 and D-017; Pico 2 datasheet p.7, §3.1 p.9 | review / 1:1 print |
| R-06 | Supported power source: USB 5 V only, from a laptop or a powerbank | VBUS 5 V ± 10 % | V | owner, D-001; VBUS range Pico 2 datasheet §3.3 p.12 | test |
| R-07 | Thermocouple connector mounted on the TOP side; bottom side flat (no parts) so the board can be soldered down by its castellations like a Pico | top side; mini type-K socket = 2 × Omega PCC-SMD clips at the edge opposite USB (D-004) | - | owner, D-001 (Q3), D-004 | review / 1:1 print |
| R-08 | Thermocouple input, type K | 1 channel | - | owner, D-001 (Q4) | test with K probe |
| R-09 | Thermocouple interface IC | MAX31856 | - | owner, D-001 (Q5) | review |
| R-10 | Measurement range: full type K range of the MAX31856 | −200 to +1372 | °C | owner, D-001 (Q5); MAX31856 datasheet Table 1 p.12 | test vs reference |
| R-11 | Accuracy: as specified by the MAX31856 (no tighter board-level target set) | ±0.15 % of full scale TC, ±0.7 °C cold junction (TA −20 to +85 °C) | - | owner, D-001 (Q5); MAX31856 datasheet p.1 | test vs reference |
| R-12 | Works with grounded and ungrounded (insulated) junction probes | both | - | owner, D-001 (Q5) | test with both |
| R-13 | Cold-junction compensation | MAX31856 internal sensor, IC thermally coupled to the connector | - | MAX31856 datasheet "MAX31856 Location" p.28 | test vs reference |
| R-14 | Thermocouple IC on SPI using 4 shared edge GPIO, labelled on the silkscreen, with solder jumpers to disconnect it | 4 GPIO | - | owner, D-001 (Q6) | review / test |
| R-15 | USB connector | USB-C (USB 2.0 device, 5 V sink) | - | owner, D-001 (Q8) | test |
| R-16 | Thermocouple data readable from Pico SDK / MicroPython firmware on the board's own MCU | - | - | implied ("clone"), accepted with D-001 | test |

## Wish (nice to have, traded off in phase 2)
| ID | Wish | Value | Priority (1-3) |
|----|------|-------|----------------|
| W-01 | Thermocouple open-circuit and range fault reporting | MAX31856 FAULT register and pin | 1 |
| W-02 | Mains-noise rejection on the thermocouple input | MAX31856 50/60 Hz filter | 2 |
| W-03 | Keep the Pico 2 VSYS input range (1.8 to 5.5 V) usable even though USB is the only supported source | Pico 2 datasheet §5.5 | 2 |
| W-04 | All parts orderable for JLCPCB assembly from LCSC stock | D-001 (Q7) | 1 |

## Interfaces
- **USB**: USB-C receptacle (R-15), USB 2.0 full speed device from the RP2350. Pico 2 used micro-USB B.
- **40-pin edge**: Pico 2 pinout and functions (R-03, R-04). On the Pico 2, 26 GPIO are on the edge;
  GPIO23 (SMPS power-save), GPIO24 (VBUS sense), GPIO25 (LED) and GPIO29 (VSYS/3 on ADC3) are used
  on-board (Pico 2 datasheet p.8).
- **Thermocouple**: type K, 2 wires (T+, T−), connector on the top side (R-07). Part and position: phase 2.
- **Thermocouple IC bus**: SPI to the MAX31856 on 4 shared edge GPIO with cut-able jumpers (R-14). Pins: phase 2.
- **Debug / boot**: BOOTSEL button and 3-pin SWD header, as on the Pico 2.
- **Power out**: 3V3 pin, recommended load < 300 mA as on the Pico 2 (Pico 2 datasheet p.9).

## Environment
Use case: hand-held / bench "probe on a stick", powered from a laptop or powerbank (owner). Board ambient
range not specified by the owner (non-blocking): the design default is the Pico 2 rating, −20 to +85 °C
operating including self-heating, recommended max ambient 70 °C (Pico 2 datasheet §3.3 p.12). The probe
tip can be far hotter than the board; only the probe sees the measured temperature.

## Cost and volume
| Item | Target | Note |
|------|--------|------|
| Quantity (proto / production) | 5–10 prototypes; production not planned | owner, D-001 (Q7) |
| BOM cost per board at qty | open, non-blocking | owner, D-001 (Q7) |
| PCB size / layers limit | 51 × 21 mm (R-02); layer count decided in phase 2 | |
| Fab/assembly house | JLCPCB PCB + assembly, LCSC parts | owner, D-001 (Q7) |

## Target markets (required, input to phase 3)
| Market | Sold / used there? | Note |
|--------|--------------------|------|
| EU (CE) | yes | owner, D-003 |
| UK (UKCA) | no, not applicable | owner, D-003 |
| US (FCC) | no, not applicable | owner, D-003 |
| Other | no | owner, D-003 |

## Safety and regulatory (input to phase 3)
- Voltages: USB 5 V only on the board, SELV.
- User-touchable parts: thermocouple tip and wires. A grounded-junction probe touching a conductive surface
  connects that surface to T+/T−. MAX31856 inputs are protected to ±45 V (MAX31856 datasheet p.2). Analysed in
  phase 2 (common-mode range) and phase 3.
- Target markets: **EU only** (owner, D-003, 2026-10-15; amends D-001 Q7). CE marking and EU rules apply;
  UK (UKCA) and US (FCC) are **not applicable**. Certification route for the prototypes: phase 3.
- Required user-manual warning MW-01 (grounded-junction probe common-mode limit, A2-4): STATUS.md.

## Out of scope
Wireless (no radio, not a Pico 2 W clone); battery charging; thermocouple types other than K as a hardware
requirement (the MAX31856 supports others in firmware); an enclosure. Approved with the spec, D-001.

---

## Research (background for D-001; options that were not chosen are kept for the record)

### R1. MCU options (Q1, chosen RP2350A)
| Option | Pico board | GPIO | Notes | LCSC price 2026-10-15 |
|--------|-----------|------|-------|-----------------------|
| RP2040 | Pico | 30 (26 on edge) | 2 MB W25Q16JV flash and ABM8-272-T3 12 MHz crystal on Pico (Pico datasheet p.4); KiCad minimal design in the hardware design guide | C2040: $0.9975 @1, $0.7645 @100, $0.7268 @1000 |
| RP2350A | Pico 2 | 30 (26 on edge) | Same 51 × 21 mm board and on-board pin usage as Pico; 4 MB W25Q32RV flash (Pico 2 datasheet); production until at least Jan 2045 (RP2350 product page) | C42411118: $1.299 @1, $1.1348 @100, $1.0987 @1000 |
| RP2350B | none | 48 | QFN-80 10 × 10 mm; frees GPIO for the thermocouple IC, but no Pico board uses it | C42415655: "Not available now" on LCSC (fetched 2026-10-15) |

### R2. Thermocouple interface ICs (Q5, chosen MAX31856)
| Spec | MAX31855K | MAX31856 | MCP9600 |
|------|-----------|----------|---------|
| Interface | SPI, read-only, up to 5 MHz | SPI (4-wire) + FAULT, DRDY pins | I2C, 100 kHz, addresses 0x60–0x67 (8 per bus), uses clock stretching |
| Resolution | 14-bit, 0.25 °C | 19-bit, 0.0078125 °C | 0.0625 °C |
| Hot-junction accuracy (K) | ±2 °C (−200 to +700 °C), ±4 °C (to +1350 °C), at TA −20 to +85 °C | ±0.15 % of full scale (linearized) | ±1.5 °C max (±0.5 °C typ) |
| Linearization | No: linear approximation, firmware must correct for NIST curve | Yes, on-chip, 8 thermocouple types | Yes, on-chip, 8 types |
| Cold-junction compensation | Internal, ±2 °C | Internal, ±0.7 °C (TA −20 to +85 °C) | Internal |
| Fault detection | Open, short to GND, short to VCC | Open, over/under-voltage, range thresholds | None (MCP9601 adds open/short) |
| Input protection | - | ±45 V | - |
| Supply | 3.0 to 3.6 V | 3.0 to 3.6 V | 2.7 to 5.5 V |
| Package | SO-8 | TSSOP-14 | MQFN-20 5 × 5 mm |
| MCU pins used | 3 (SCK, MISO, CS) | 4 (SCK, MOSI, MISO, CS), +2 optional | 2 (SDA, SCL), can share an existing I2C bus |
| LCSC price 2026-10-15 | C52028: $7.3199 @1, $5.4563 @100 (stock 529) | C2653162: $4.3767 @1, $3.2078 @100, $3.0207 @1000 (stock 3,716) | C220851: $10.0147 @1, $6.852 @100 (stock 2,664) |
| Maker list price | ADI from $5.17 @1k | ADI from $6.31 @1k | see Microchip product page |

Datasheet notes relevant to layout (phase 2+): MAX31855 recommends a 10 nF differential capacitor across
T+/T− and T− must not be tied to GND externally (MAX31855 datasheet). The IC measures the cold junction at
its own die, so the junction where the thermocouple metal meets copper must be at the IC's temperature:
place the IC next to the connector, or use a connector with type-K contact alloys.
MAX31855 has an ADI product change notice (PCN 2571A, Apr 2026) listed on its product page.

Chosen (D-001): MAX31856. Cheapest of the three at LCSC on 2026-10-15, linearized, best cold-junction spec,
±45 V input protection.

### R3. GPIO budget (Q6, chosen option A)
RP2040 and RP2350A have 30 GPIO. The Pico puts 26 on the edge pins and uses the other 4 on-board
(GPIO23, 24, 25, 29; Pico datasheet p.8). So a thermocouple IC on a Pico-compatible board must either share
GPIO that are also on the edge pins, or take over one of the 4 on-board functions. Options:
- A: share 3–4 edge GPIO (SPI) or 2 (I2C) and print them on the silkscreen; add solder jumpers so the
  user can disconnect the IC and get the pins back. Chosen (D-001).
- B: I2C MCP9600 on an existing I2C pin pair, shareable with the user's own I2C devices.
- C: RP2350B, which has 18 more GPIO, but breaks the "Pico clone" chip choice and is not in stock at LCSC.

### R4. "On the bottom" (Q3, answered 2026-10-15: connector on the TOP side, bottom stays flat)
Readings: (a) connector on the underside (bottom copper side) of the board; (b) connector at the bottom
edge, the short edge opposite USB; (c) solder pads on the underside. A part on the underside stops the
board from being reflowed flat as an SMT module, which the Pico supports (Pico datasheet p.4, §2.2).
Connector options: miniature type-K PCB jack such as Omega PCC-SMP-K (type-K contacts, mates SMPW plugs,
rated −29 to 180 °C; https://au.omega.com/pptst/PCC-OST-SMP.html), 2-pin screw terminal, or bare pads. Physical fit of a mini jack on a 21 mm
wide board is checked in phase 2.

### Sources
- Raspberry Pi Pico datasheet, release 21, build 03/07/2026: https://datasheets.raspberrypi.com/pico/pico-datasheet.pdf
- Raspberry Pi Pico 2 datasheet (build 03/07/2026 per release history): https://datasheets.raspberrypi.com/pico/pico-2-datasheet.pdf
- Hardware design with RP2040, release 2, build 20/08/2026: https://datasheets.raspberrypi.com/rp2040/hardware-design-with-rp2040.pdf
- RP2350 product page: https://www.raspberrypi.com/products/rp2350/
- MAX31855 product page and datasheet Rev 5: https://www.analog.com/en/products/max31855.html, https://www.analog.com/media/en/technical-documentation/data-sheets/MAX31855.pdf
- MAX31856 product page and datasheet 19-7534 Rev 0 (2/15; copy read from https://cdn-learn.adafruit.com/assets/assets/000/035/948/original/MAX31856.pdf because the ADI URL timed out from the box): https://www.analog.com/en/products/max31856.html, https://www.analog.com/media/en/technical-documentation/data-sheets/MAX31856.pdf
- MCP9600 product page and datasheet DS20005426G: https://www.microchip.com/en-us/product/MCP9600, https://ww1.microchip.com/downloads/en/DeviceDoc/MCP960X-Data-Sheet-20005426.pdf (I2C addresses p.8, clock stretching p.9)
- LCSC product pages (2026-10-15): https://www.lcsc.com/product-detail/C2040.html, https://www.lcsc.com/product-detail/C42411118.html, https://www.lcsc.com/product-detail/C42415655.html, https://www.lcsc.com/product-detail/C52028.html, https://www.lcsc.com/product-detail/C2653162.html, https://www.lcsc.com/product-detail/C220851.html
- Omega PCC-SMP connector spec: https://assets.omega.com/pdf/connectors/thermocouple-and-rtd-connectors/PCC-OST-SMP.pdf
