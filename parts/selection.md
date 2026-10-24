# Part selection: pico-k

One table per block. Prices: list price in USD at the given quantity (unit price for an order of that size;
"(MOQ n)" = the distributor's minimum order applies), with source and date. Estimates are labelled `ESTIMATE:`.
Stock and lifecycle come from the distributor page on that date. "JLC basic / extended" is the JLCPCB
assembly library type from `https://jlcpcb.com/partdetail/<C#>`; extended parts cost $3.07 feeder loading
per unique part per Economic PCBA order (JLCPCB fee table, updated 2026-09-09, fetched 2026-10-15,
https://jlcpcb.com/help/article/pcb-assembly-price). JLC stock is the `overseasStockCount` field on that page.
LCSC data: `https://www.lcsc.com/product-detail/<C#>.html`, fetched 2026-10-15. Lifecycle "Active (LCSC
"normal")" is LCSC's `productCycle` field; no manufacturer lifecycle page was read unless named.

Rules applied (D-005, S3-7): every part rated for −20 … +85 °C board ambient; capacitors on VBUS/VSYS
≥ 10 V; resistors ≤ 50 % of rated power (0402 thick film = 62.5 mW, so ≤ 31 mW); RoHS declaration per
part (table at the end). Locked by D-001 … D-005: RP2350A, MAX31856, TPS63001, Omega PCC-SMD,
HRO TYPE-C-31-M-12, USBLC6-2SC6, 4-layer 1.0 mm.

Reference designs used for values: Raspberry Pi "Hardware design with RP2350" (build 2026-07-03,
`datasheets/hardware-design-with-rp2350.pdf`), Pico 2 datasheet (`datasheets/pico-2-datasheet.pdf`),
Pico 2 W schematic RP-008306 (`datasheets/pico-2-w-schematic.pdf`). Refs are provisional (phase 5 sets
final designators).

Decision items are numbered **P4-n** and listed in `STATUS.md`.

## MCU (U1)
Requirements it must meet: R-01, R-04 (D-001: RP2350A)

| Candidate (MPN) | Mfr | Key specs vs requirement | Package | Price @1 | @100 | @1000 | Price source + date | Stock (source, date) | Lifecycle | Second source | Datasheet (rev) | Notes / risks |
|-----------------|-----|--------------------------|---------|----------|------|-------|---------------------|----------------------|-----------|---------------|-----------------|---------------|
| RP2350A | Raspberry Pi | Dual Cortex-M33/Hazard3, 520 KB SRAM, 30 GPIO (QFN-60 = A); TA −40 … +85 °C (RP2350 datasheet Table 1435) | QFN-60 7×7 | $1.2990 | $1.1348 | $1.0987 | LCSC C42411118, 2026-10-15 | LCSC 6317, JLC 6317 (2026-10-15) | Active (LCSC "normal") | none (only maker) | datasheets/RP2350A.pdf (build 2025-07-29) | JLC extended. Locked D-001. Single source → **P4-1**. |

Recommendation: RP2350A (locked). No second source exists; accept single-source risk (P4-1). Buy all
rev-A MCUs in one LCSC/JLC order (6,317 in stock).

## QSPI flash (U2)
Requirements: R-04 (4 MB as Pico 2, Pico 2 datasheet §1 / schematic "32MBit (4MiB) Flash")

| Candidate (MPN) | Mfr | Key specs vs requirement | Package | Price @1 | @100 | @1000 | Price source + date | Stock (source, date) | Lifecycle | Second source | Datasheet (rev) | Notes / risks |
|-----------------|-----|--------------------------|---------|----------|------|-------|---------------------|----------------------|-----------|---------------|-----------------|---------------|
| W25Q32RVXHJQ | Winbond | 32 Mbit, Quad SPI, −40 … +105 °C (Rev E p.4); the Pico 2 / Pico 2 W part | XSON-8 2×3×0.4 (Rev E §10.3 p.77) | $3.8844 | $3.1441 | $3.0087 | LCSC C32246052, 2026-10-15 | LCSC 1674, JLC 1674 (2026-10-15) | Active (LCSC "normal") | GigaDevice GD25Q32EEIGR | datasheets/W25Q32RVXHJQ.pdf (Rev E) | JLC extended. JLC stock = LCSC stock. |
| GD25Q32EEIGR | GigaDevice | 32 Mbit, Quad SPI, −40 … +85 °C (Rev 1.3) | USON-8 3×2×0.45 with exposed pad (Rev 1.3 §10.3 p.54) | $1.2308 | $0.8063 | $0.7109 | LCSC C2973794, 2026-10-15 | LCSC 6750, JLC 7061 (2026-10-15) | Active (LCSC "normal") | Winbond W25Q32RVXHJQ | datasheets/GD25Q32EEIGR.pdf (Rev 1.3, May 2022) | JLC extended. Same 8-pin assignment (USON8/WSON8 Fig. 2). RPi: with a different flash the 10 k CS pull-up may become important (Hardware design p.8) → fit R6. Exposed pad: land pattern must suit both (phase 6). |

Recommendation: **W25Q32RVXHJQ** (Pico 2 parity, the part RPi validated), approved alternate
**GD25Q32EEIGR** with R6 fitted (P4-2). The GD part is ≈ $2.3–2.7 cheaper per board; switching primary is
an owner option, not recommended for rev-A.

## Crystal (Y1) and load parts
Requirements: R-04 (12 MHz, D-004)

| Candidate (MPN) | Mfr | Key specs vs requirement | Package | Price @1 | @100 | @1000 | Price source + date | Stock (source, date) | Lifecycle | Second source | Datasheet (rev) | Notes / risks |
|-----------------|-----|--------------------------|---------|----------|------|-------|---------------------|----------------------|-----------|---------------|-----------------|---------------|
| ABM8-272-T3 | Abracon | 12 MHz, CL 10 pF, ESR ≤ 50 Ω, ±30 ppm, −40 … +85 °C (RP2350 datasheet Table 597; RPi recommends it) | SMD3225-4P | $0.6255 | $0.4088 | $0.3661 | LCSC C20625731, 2026-10-15 | LCSC 6248, JLC 6243 (2026-10-15) | Active (LCSC "normal") | none qualified | datasheets/ABM8-272-T3.pdf (rev "IR") | JLC extended. Single source → **P4-3**. |
| X322512MSB4SI | YXC | 12 MHz, CL 20 pF, ESR 80 Ω (LCSC page) — **fails** ESR ≤ 50 Ω and needs other load caps | SMD3225-4P | $0.0960 (MOQ 5) | $0.0769 | $0.0589 | LCSC C9002, 2026-10-15 | LCSC 4,900; JLC 1 (2026-10-15) | Active (LCSC "normal") | - | not saved | JLC basic. Rejected. |

Load caps 2 × 15 pF C0G 0402 (FH 0402CG150J500NT, C1548, JLC basic) and 1 kΩ series resistor, as the RPi
minimal design (p.13). Recommendation: **ABM8-272-T3**, accept single source (P4-3).

## RP2350 core regulator inductor (L1) and VREG parts
Requirements: R-04; RPi: "if you choose not to use our example, then you do so at your own risk" (Hardware design p.6–7)

| Candidate (MPN) | Mfr | Key specs vs requirement | Package | Price @1 | @100 | @1000 | Price source + date | Stock (source, date) | Lifecycle | Second source | Datasheet (rev) | Notes / risks |
|-----------------|-----|--------------------------|---------|----------|------|-------|---------------------|----------------------|-----------|---------------|-----------------|---------------|
| AOTA-B201610S3R3-101-T | Abracon | 3.3 µH, polarity dot, aligned on reel; 2.1 A, Isat 2.8 A, 140 mΩ max (Symmetry page); −40 … +125 °C (Rev A) | 0806 (2016) | $0.2100 | $0.1500 | $0.1200 | Symmetry Electronics, 2026-10-15: https://www.symmetryelectronics.com/products/abracon/aota-b201610s3r3-101-t/ | Symmetry 4,695; LCSC 0; JLC 4; Future Electronics 0 (2026-10-15) | Active (Future Electronics "Part Status: Active") | none (RPi-specified) | datasheets/AOTA-B201610S3R3-101-T.pdf (Rev A, 2024-09-13) | not in JLC library. LCSC ladder 5+ $0.3178 / 150+ $0.223 / 3000+ $0.1717 (out of stock). Search snippet only, not verified: DigiKey 423, Mouser 5,098 (Mouser blocked fetch). **P4-4**. |

VREG caps C16–C18 4.7 µF 10 V X5R 0402 (Samsung CL05A475MP5NRNC, C23733, basic) and R5 33 Ω (C25105, basic)
as RPi C6/C7/C9 and R3 (p.7). Phase 4 recommendation was AOTA-B201610S3R3-101-T (P4-4); the owner rejected it on 2026-10-15 →
replacement **P4-4b** below. Nothing is bought.

## 3.3 V buck-boost (U3) and inductor (L2)
Requirements: R-04 (3V3 < 300 mA user load, 3V3_EN, PS on GPIO23), W-03 (VSYS 1.8–5.5 V); D-004 locks TPS63001

| Candidate (MPN) | Mfr | Key specs vs requirement | Package | Price @1 | @100 | @1000 | Price source + date | Stock (source, date) | Lifecycle | Second source | Datasheet (rev) | Notes / risks |
|-----------------|-----|--------------------------|---------|----------|------|-------|---------------------|----------------------|-----------|---------------|-----------------|---------------|
| TPS63001DRCR | Texas Instruments | Fixed 3.3 V, VIN 1.8–5.5 V, 1.8 A switches, TA −40 … +85 °C (SLVS520C p.1) | VSON-10 3×3 | $1.6184 | $1.0095 | $0.8962 | LCSC C28060, 2026-10-15 | LCSC 10143, JLC 10143 (2026-10-15) | Active (LCSC "normal") | TI TPS63000DRCR | datasheets/TPS63001DRCR.pdf (SLVS520C, Oct 2015) | JLC extended. Locked D-004. |
| TPS63000DRCR | Texas Instruments | Adjustable version, same package; needs FB divider (SLVS520C Eq. 2) | VSON-10 3×3 | $0.8280 | $0.4906 | $0.4149 | LCSC C24966, 2026-10-15 | LCSC 23984, JLC 24935 (2026-10-15) | Active (LCSC "normal") | TI TPS63001DRCR | same file (SLVS520C covers TPS63000/1/2) | JLC extended. Alternate only with divider pads in the layout. Same maker → TI single-source (P4-1). |

Inductor peak current (SLVS520C Eq. 3–4 p.11–12, boost mode at the lowest VSYS): ESTIMATE inputs
VIN = 1.8 V (W-03), IOUT = 0.352 A (architecture power budget), η = 0.9 (datasheet default), f = 2.5 MHz,
L = 2.2 µH → D = 0.455, IPEAK = 0.717 + 0.074 = **0.79 A**; +20 % (TI) → **Isat ≥ 0.95 A**. From USB
(VSYS ≈ 4.65 V) the part runs in buck mode with a lower peak.

| Candidate (MPN) | Mfr | Key specs vs requirement | Package | Price @1 | @100 | @1000 | Price source + date | Stock (source, date) | Lifecycle | Second source | Datasheet (rev) | Notes / risks |
|-----------------|-----|--------------------------|---------|----------|------|-------|---------------------|----------------------|-----------|---------------|-----------------|---------------|
| SWPA3015S2R2MT | Sunlord | 2.2 µH ±20 %, Isat 1.60 A (max column) / 2.00 A typ, DCR 78 mΩ max, Irms 1.60 A (Sunlord p.5); −40 … +125 °C (p.1). Meets ≥ 0.95 A | 3.0×3.0×1.5 | $0.0470 | $0.0470 | $0.0265 | JLCPCB C43389, 2026-10-15 (offer range $0.047 … $0.0265; tiers not shown) | JLC 92,071 (2026-10-15); LCSC page gave no data | no data | Murata LQH3NPN2R2MMEL | datasheets/SWPA3015S2R2MT.pdf (Sunlord, rev 2025/5/8) | not in JLC library. @100 = first-tier price (upper bound). |
| LQH3NPN2R2MMEL | Murata | 2.2 µH ±20 %, Isat 1.8 A, 1.22 A rated, 65 mΩ (LCSC); −40 … +125 °C incl. self-heating (datasheet). In TI's list (LQH3NP, SLVS520C Table 2) | 3×3 | $0.1697 (MOQ 5) | $0.1397 | $0.1135 | LCSC C668451, 2026-10-15 | LCSC 6350, JLC 6538 (2026-10-15) | Active (LCSC "normal") | Sunlord SWPA3015S2R2MT | datasheets/LQH3NPN2R2MMEL.pdf | JLC extended. Land pattern to check against the Sunlord part (phase 6). |
| APSWPA3015S2R2NTF | APV | 2.2 µH ±30 %, Isat 1.6 A, 78 mΩ (JLC page) | 3×3 | no data | no data | no data | JLC page, no price | JLC 0 (2026-10-15) | Active (LCSC "normal") | - | not saved | JLC extended. Rejected (no stock). |

Passives (SLVS520C Table 1 p.10, p.12): C20 Cin 10 µF 25 V X5R 0805 (≥ 4.7 µF; ≥ 10 V on VSYS), C21/C22
Cout 2 × 10 µF 25 V 0805 (nominal 15 µF; 25 V parts keep more capacitance under DC bias — derated value
checked in phase 5 from the Samsung curve), R14 100 Ω + C15 100 nF VINA filter, R15 100 kΩ 3V3_EN pull-up
to VSYS (Pico 2 datasheet p.15). Recommendation: **TPS63001DRCR + SWPA3015S2R2MT**, alternates
TPS63000DRCR (with DNP divider pads) and LQH3NPN2R2MMEL.

## VBUS → VSYS diode (D1)
Requirements: R-04, R-06 (Pico 2 power chain, datasheet §5.4 p.15)

| Candidate (MPN) | Mfr | Key specs vs requirement | Package | Price @1 | @100 | @1000 | Price source + date | Stock (source, date) | Lifecycle | Second source | Datasheet (rev) | Notes / risks |
|-----------------|-----|--------------------------|---------|----------|------|-------|---------------------|----------------------|-----------|---------------|-----------------|---------------|
| MBR120VLSFT1G | onsemi | 20 V 1 A Schottky, Vf 0.30 V @ 1 A, TJ −65 … +125 °C (Rev. 4) | SOD-123FL | $0.1828 (MOQ 5) | $0.1401 | $0.0971 | LCSC C223608, 2026-10-15 | LCSC 27305, JLC 27309 (2026-10-15) | Active (LCSC "normal") | Nexperia PMEG6010ELR | datasheets/MBR120VLSFT1G.pdf (Rev. 4) | JLC extended.  |
| PMEG6010ELR/B115 | Nexperia | 60 V 1 A, Vf 660 mV @ 1 A (LCSC); the Pico 2 W D1 | SOD-123W | $3.0248 | $3.0248 | $1.1467 | LCSC C17282745, 2026-10-15 | LCSC 0, JLC 0 (2026-10-15) | Active (LCSC "normal") | onsemi MBR120VLSFT1G | not saved | JLC extended. Out of stock; different package (SOD-123W vs SOD-123FL, footprint to check); higher Vf lowers VSYS by ≈ 0.36 V at 1 A. |

Recommendation: **MBR120VLSFT1G**, alternate PMEG6010ELR (footprint compatibility checked in phase 6).

## USB-C receptacle (J1)
Requirements: R-04 (USB-C, D-001), D-004 A2-5 incl. the 1.0 mm board tab check

| Candidate (MPN) | Mfr | Key specs vs requirement | Package | Price @1 | @100 | @1000 | Price source + date | Stock (source, date) | Lifecycle | Second source | Datasheet (rev) | Notes / risks |
|-----------------|-----|--------------------------|---------|----------|------|-------|---------------------|----------------------|-----------|---------------|-----------------|---------------|
| TYPE-C-31-M-12 | Korean Hroparts | 16 contacts + 4 shell tabs in plated slots; 5 A / 20 V; **−30 … +80 °C** (drawing note 5) → misses S3-7 (+85 °C) | SMD + THT tabs, 8.94 × 7.35 mm | $0.1879 (MOQ 5) | $0.1483 | $0.1046 | LCSC C165948, 2026-10-15 | LCSC 364570, JLC 381728 (2026-10-15) | Active (LCSC "normal") | SHOU HAN TYPE-C 16PIN 2MD(073) | datasheets/TYPE-C-31-M-12.pdf (drawing 2020-12-08, rev A) | JLC extended. Locked by D-004. Tab check below. **P4-6**. |
| TYPE-C 16PIN 2MD(073) | SHOU HAN | 16 contacts + 4 shell tabs; 3 A / 5 V; −25 … +85 °C (spec p.3, drawing note 5) → meets S3-7; recommended PCB 0.80 mm (drawing) | SMD + THT tabs, 8.94 × 7.35 mm | $0.0753 (MOQ 20) | $0.0753 | $0.0513 | LCSC C2765186, 2026-10-15 | LCSC 938780, JLC 976875 (2026-10-15) | Active (LCSC "normal") | Korean Hroparts TYPE-C-31-M-12 | datasheets/TYPE-C-16PIN-2MD-073.pdf (rev A) | JLC extended. Slot pitch 8.64 vs HRO 8.65 mm, locating pegs 5.78 mm on both drawings; pad-by-pad check in phase 6. |

**Tab check (1.0 mm board).** HRO drawing (side view): 4 shell tabs **1.01 mm** below the seating plane
("4-1.01"), tolerance ±0.10 mm (title-block table for dimensions ≤ 5 mm), widths 0.80 / 1.10 mm. On a
1.00 mm board the tips end **0.01 mm beyond the bottom surface nominal**, range −0.09 … +0.11 mm with the
part tolerance; with an assumed board thickness tolerance of ±10 % (ESTIMATE: typical fab tolerance, to
confirm with the JLC quote) **−0.19 … +0.21 mm**. The tabs do reach the bottom (they solder through the
plated slots) and may stand proud by up to ≈ 0.2 mm plus solder. The SHOU HAN part shows the same tab
style, 1.00 mm long (front view), so it is not flatter. Neither part is fully SMD.
Options (P4-6): keep the tabs and declare "flat bottom except J1 tab tips ≤ 0.2 mm (and the PCC-SMD tab
tips, ESTIMATE ≈ 0.17 mm)", like the Pico 2's own USB pads on the underside (Pico 2 datasheet §3.2 p.10);
or trim the tips flush after soldering (rework step).

Recommendation (P4-6): **swap primary to SHOU HAN TYPE-C 16PIN 2MD(073)** (meets −20 … +85 °C, cheaper,
JLC stock 976,875) with **HRO as approved alternate**, one footprint for both; accept tab tips ≤ 0.2 mm.
If the owner keeps HRO (D-004), S3-7 needs a written exception for J1 (+80 °C).

## USB ESD (U4) and USB passives
Requirements: R-04; D-004 (USBLC6-2SC6)

| Candidate (MPN) | Mfr | Key specs vs requirement | Package | Price @1 | @100 | @1000 | Price source + date | Stock (source, date) | Lifecycle | Second source | Datasheet (rev) | Notes / risks |
|-----------------|-----|--------------------------|---------|----------|------|-------|---------------------|----------------------|-----------|---------------|-----------------|---------------|
| USBLC6-2SC6 | STMicroelectronics | 2 lines + VBUS, IEC 61000-4-2 level 4, TJ −40 … +125 °C (Rev 5) | SOT-23-6 | $0.1786 (MOQ 5) | $0.1375 | $0.0995 | LCSC C7519, 2026-10-15 | LCSC 27175, JLC 31364 (2026-10-15) | Active (LCSC "normal") | UMW USBLC6-2SC6 | datasheets/USBLC6-2SC6.pdf (ST Rev 5) | JLC extended.  |
| USBLC6-2SC6 (UMW) | UMW | Same function and pinout per LCSC listing; 15 V clamp at 6 A | SOT-23-6 | $0.0477 (MOQ 10) | $0.0384 | $0.0336 | LCSC C2687116, 2026-10-15 | LCSC 57190, JLC 57174 (2026-10-15) | Active (LCSC "normal") | ST USBLC6-2SC6 | not saved (LCSC pdf for C2687116) | JLC extended. Electrical equivalence to confirm from the UMW datasheet in phase 5. |

Passives: R1/R2 27 Ω (C25100, JLC extended; RPi p.15), R10/R11 5.1 kΩ CC Rd (C25905, basic), C19 10 µF 25 V on VBUS
(≤ 10 µF at attach, USB 2.0 §7.2.4.1). Recommendation: **ST USBLC6-2SC6**, alternate UMW.

## Thermocouple converter (U5) and front end
Requirements: R-11 … R-14, D-001 (MAX31856), safety: Fig. 8 filter, TVS check

| Candidate (MPN) | Mfr | Key specs vs requirement | Package | Price @1 | @100 | @1000 | Price source + date | Stock (source, date) | Lifecycle | Second source | Datasheet (rev) | Notes / risks |
|-----------------|-----|--------------------------|---------|----------|------|-------|---------------------|----------------------|-----------|---------------|-----------------|---------------|
| MAX31856MUD+T | Analog Devices (Maxim) | Type K, ±0.15 % TC / ±0.7 °C CJ (−20 … +85 °C); −55 … +125 °C; inputs ±45 V (19-7534 Rev 0 p.1–2) | TSSOP-14 | $4.3767 | $3.2078 | $3.0207 | LCSC C2653162, 2026-10-15 | LCSC 3716, JLC 4066 (2026-10-15) | PRODUCTION (analog.com, 1ku "from $6.31") | none (only maker) | datasheets/MAX31856MUD+T.pdf (19-7534 Rev 0, 2/15) | JLC extended. Locked D-001. Single source → **P4-1**. |

Front end per MAX31856 Fig. 8 (p.27): R12/R13 100 Ω series (C25076, basic), C14 100 nF differential,
C25/C26 10 nF common-mode X7R (C15195, basic), C12/C13 100 nF AVDD/DVDD, R7 10 kΩ CS pull-up on the IC
side of the jumper (A2-2).

**TVS on T+/T− (safety plan input).** Recommendation: **no TVS** (P4-8). The MAX31856 inputs survive ±45 V
(p.2) and Fig. 8 adds RC filtering; a TVS leakage current flows through the 2 × 100 Ω and the probe
and reads as signal. ESTIMATE: 1 µA × 200 Ω = 0.2 mV ≈ 5 °C at type K's ≈ 41 µV/°C, far outside R-11.
Mains contact stays a MW-02 instruction, not a board feature (D-005, S3-3 = A).

## Thermocouple socket (J2, J3)
Requirements: D-004 (2 × Omega PCC-SMD, F1), MW-04

| Candidate (MPN) | Mfr | Key specs vs requirement | Package | Price @1 | @100 | @1000 | Price source + date | Stock (source, date) | Lifecycle | Second source | Datasheet (rev) | Notes / risks |
|-----------------|-----|--------------------------|---------|----------|------|-------|---------------------|----------------------|-----------|---------------|-----------------|---------------|
| PCC-SMD | Omega (DwyerOmega) | SMT clip, Ni-plated BeCu, −50 … +120 °C, RoHS 2015/863 certificate, pair = 1 mini jack (spec p.1) | SMT clip 11.94 × 5.6 mm | $2.6890 (MOQ 20) | $2.6890 | $2.4150 | PCC-SMD-20 strip $53.78 ⇒ $2.689/clip: dwyeromega.com product page (WebFetch 2026-10-15); PCC-SMD-1000 reel sale $2,415.15 ⇒ $2.415/clip: rspsupply.com (2026-10-15) | Omega "Models In Stock"; RSP "Normally In Stock" (2026-10-15) | Active (sold by Omega; no lifecycle field) | none (Omega only) | datasheets/PCC-SMD.pdf (Omega spec sheet) | not in JLC library. Not on LCSC/JLC. RSP PCC-SMD-500 sale $1,226.81 ($2.454/clip). Search snippets only, not verified: globaltestsupply PCC-SMD-1000 ≈ $2,236.25; Unikeyic 99 pcs at $67.34. curl to Omega is blocked (485-byte page). **P4-5**. |

**Assembly.** JLC cannot place it from stock. Routes:
- **Rev-A (5 boards):** JLC assembles everything else; the owner hand-solders 10 clips from one PCC-SMD-20
  strip ($53.78) with hot air or a hot plate (flat bottom, side tabs in plated slots). ESTIMATE: 20 min.
- **Qty 100+:** consign the clips to JLC. JLC: "only parts with JLC number can be consigned … If the part is
  not with the part number yet, please submit the consigned part. The engineer will approve it if it is
  workable for our assembly"; overseas parcels need a customs agent, about $45 below 5,000 CNY value and
  $85 above (https://jlcpcb.com/help/article/important-note-before-you-consign-the-part-to-jlcpcb, fetched
  2026-10-15). 200 clips as 10 strips ($537.80) stay under 5,000 CNY (ESTIMATE exchange rate); whether JLC
  can machine-place from strips or needs the -500 reel is to ask JLC.
- Tab tips: ESTIMATE ≈ 0.17 mm below the 1.0 mm board (phase 2, Section B-B on a 1.6 mm board); confirm
  on the rev-A strip.

Recommendation: **PCC-SMD**, accept single source (P4-5); hand-solder for rev-A, consign for volume.

## Support parts (BOOTSEL, LED, ADC3 FET)
Requirements: R-04 (Pico 2 functions)

| Candidate (MPN) | Mfr | Key specs vs requirement | Package | Price @1 | @100 | @1000 | Price source + date | Stock (source, date) | Lifecycle | Second source | Datasheet (rev) | Notes / risks |
|-----------------|-----|--------------------------|---------|----------|------|-------|---------------------|----------------------|-----------|---------------|-----------------|---------------|
| TS-1187A-B-A-B | XKB Connection | Tact switch 5.1 × 5.1, 1.6 mm, 160 gf, 50 mA 12 V, −30 … +85 °C (drawing) | SMD 4-pad | $0.0207 (MOQ 20) | $0.0207 | $0.0140 | LCSC C318884, 2026-10-15 | LCSC 52220, JLC 306654 (2026-10-15) | Active (LCSC "normal") | Korean Hroparts K2-1187SQ-A4SW-06 (C92584); SOFNG TS-1187-1526 (C111461) | datasheets/TS-1187A-B-A-B.pdf (rev A0) | JLC basic. 1187-series 5.1×5.1×1.5 mm SMD-4P alternates locked in Phase 10. |
| KT-0805G | Hubei KENTO Elec | Green LED, −40 … +85 °C (datasheet) | 0805 | $0.0165 (MOQ 50) | $0.0165 | $0.0128 | LCSC C2297, 2026-10-15 | LCSC 1865950, JLC 2716576 (2026-10-15) | Active (LCSC "normal") | generic 0805 green LED; Orient ORH-G35A (C205442); NationStar NCD0805G1 (C84260); Lite-On LTST-C170KGKT (C98221) | datasheets/KT-0805G.pdf | JLC basic. Cathode mapped to KiCad Pad 1 (West = GND); orient alternate LED cathode mark to Pad 1. |
| KT-0603G | Hubei KENTO Elec | Green LED, −40 … +85 °C (datasheet) | 0603 | $0.0117 (MOQ 50) | $0.0117 | $0.0092 | LCSC C12624, 2026-10-15 | LCSC 516150, JLC 522825 (2026-10-15) | Active (LCSC "normal") | KT-0805G | datasheets/KT-0603G.pdf | JLC extended (not selected; 0805 KT-0805G chosen in D-006). |
| DMG1012T-7 | Diodes Inc. | N-MOSFET, TJ −55 … +150 °C (Rev. 8-2); stops ADC3 leakage into 3V3 when 3V3 is off (Pico 2 W schematic note) | SOT-523 | $0.1019 (MOQ 5) | $0.0837 | $0.0678 | LCSC C20512, 2026-10-15 | LCSC 142510, JLC 142512 (2026-10-15) | Active (LCSC "normal") | Will Semicon WNM4153-3/TR (C239557); Prisemi PNM523T201E0 (C110710) | datasheets/DMG1012T-7.pdf (Rev. 8-2) | JLC extended. SOT-523 low-VGS(th) alternates locked in Phase 10. |

LED resistor R22 470 Ω (C25117; value from the Pico 2 W palette, ESTIMATE ≤ 3.2 mA). Recommendation:
TS-1187A-B-A-B, KT-0805G, DMG1012T-7; second sources for SW1 (`K2-1187SQ-A4SW-06` `C92584`, `TS-1187-1526` `C111461`), D2 (`ORH-G35A` `C205442`, `NCD0805G1` `C84260`, `LTST-C170KGKT` `C98221`), and Q1 (`WNM4153-3/TR` `C239557`, `PNM523T201E0` `C110710`) verified against `jlcparts` in Phase 10.

## Passives (all blocks)
Requirements: S3-7 (temperature, ≥ 10 V on VBUS/VSYS, ≤ 50 % power); JLC basic preferred.

| Value | MPN (LCSC) | Refs | JLC | Price @100 / @1000 (LCSC, 2026-10-15) | Rating check | Source of value |
|-------|------------|------|-----|---------------------------------------|--------------|-----------------|
| 100 nF 16 V X7R 0402 | CL05B104KO5NNNC (C1525) | C1–C15, C32 (D-030) | basic | $0.0049 / $0.0039 | 16 V ≥ 10 V (C15 on VSYS) | RPi p.8 (10 on RP2350A), flash, MAX31856 p.27, SLVS520C Table 1, C32 on ADC_AVDD pin 44 (D-030) |
| 4.7 µF 16 V X5R **0603** (D-007) | CL10A475KO8NNNC (C19666; Samsung NRND, successor CL10A475KO8NQNC C377756) | C16, C17, C28, C29 (D-008); C18/C27 moved to 0402 by D-025 | basic | $0.0159 / $0.0124 | 1.1/3.3 V nets; DC bias ≈ −4 % @1.1 V, ≈ −32 % @3.3 V (ESTIMATE, curve) | RPi p.7, p.455 |
| 4.7 µF 25 V X5R **0402** (D-025) | TDK105CBJ475MV-F (Taiyo Yuden, C22385335) | C18, C27 | extended | $0.0345 / $0.0266 (LCSC 2026-10-17) | 3.3 V nets; DC bias ≈ −42 % @3.3 V → ≈ 2.7 µF (ESTIMATE, curve AQC19J26-08D); owner accepted vs ≈ 3.2 µF for the 0603 | RPi p.7; Pico 2 Fig. 11 C13 |
| 10 µF 25 V X5R **0603** (D-007) | CL10A106MA8NRNC (C96446) | C19, C21, C22, C31 (D-008) | basic | $0.0395 / $0.0309 (@4000) | 25 V ≥ 10 V on VBUS/VSYS; DC bias ≈ −33 % @3.3 V, ≈ −52 % @5 V (ESTIMATE, curve) | SLVS520C p.10–12; USB 2.0 §7.2.4.1 |
| 15 pF 50 V C0G 0402 | 0402CG150J500NT, FH (C1548) | C23, C24 | basic | $0.0038 / $0.0029 | - | RPi p.13 |
| 10 nF 50 V X7R 0402 | CL05B103KB5NNNC (C15195) | C25, C26 | basic | $0.0041 / $0.0032 | - | MAX31856 Fig. 8 |
| 10 µF 25 V X5R **0805** (D-030, replaces 1206 D-009) | CL21A106KAYNNNE (C15850) | C20 | basic | $0.0692 / $0.0692 (jlcparts snapshot 2026-10-15) | 25 V ≥ 10 V on VSYS; DC bias ≈ −42 % @5 V → ≈ 5.8 µF, ≈ −44 % @5.25 V → ≈ 5.6 µF; worst (−10 % tol) ≈ 5.0 µF ≥ 4.7 µF (ESTIMATE, curve) | SLVS520C p.12; D-030 |
| 10 kΩ 0402 DNF (D-009) | 0402WGF1002TCE (C25744) | R23, R24 | basic | $0.0033 / $0.0026 | DNF | MAX31856 p.10 (outputs; drive type open) |
| 27 Ω | 0402WGF270JTCE (C25100) | R1, R2 | extended | $0.0019 / $0.0015 | < 1 mW | RPi p.15 |
| 1 kΩ | 0402WGF1001TCE (C11702) | R3, R4 | basic | $0.0036 / $0.0027 | < 1 mW | RPi p.8, p.13 |
| 33 Ω | 0402WGF330JTCE (C25105) | R5 | basic | $0.0012 / $0.0009 | < 1 mW | RPi p.7 |
| 10 kΩ | 0402WGF1002TCE (C25744) | R6 (DNF), R7, R8, R9 | basic | $0.0033 / $0.0026 | ≤ 2.5 mW | RPi p.8; A2-2; Pico 2 R1; Pico 2 W R6 |
| 5.1 kΩ | 0402WGF5101TCE (C25905) | R10, R11 | basic | $0.0024 / $0.0019 | ≤ 0.6 mW | USB Type-C Rd |
| 100 Ω | 0402WGF1000TCE (C25076) | R12–R14 | basic | $0.0013 / $0.0010 | < 1 mW | MAX31856 Fig. 8; SLVS520C Table 1 |
| 100 kΩ | 0402WGF1003TCE (C25741) | R15, R16 | basic | $0.0015 / $0.0012 | 0.3 mW | Pico 2 p.15; R16 ESTIMATE (Pico 2 W palette) |
| 5.6 kΩ | 0402WGF5601TCE (C25908) | R18 | extended | $0.0010 / $0.0008 | 0.6 mW | Pico 2 R10 (W schematic value) |
| 20 kΩ | 0402WGF2002TCE (C25765) | R19 | basic | $0.0013 / $0.0010 | < 1 mW | Pico 2 W R5 (VSYS/3) |
| 200 Ω | 0402WGF2000TCE (C25087) | R20 | basic | $0.0029 / $0.0022 | 0.45 mW | Pico 2 p.14 |
| 1 Ω | 0402WGF100KTCE (C25086) | R21 | extended | $0.0040 / $0.0031 | ≈ 0 | Pico 2 p.14 (R9) |
| 470 Ω | 0402WGF4700TCE (C25117) | R22 | basic | $0.0027 / $0.0021 | ≤ 5 mW (ESTIMATE) | Pico 2 W R3; kept D-007 (P5-3) |

All resistors UNI-ROYAL 0402 1 % 62.5 mW thick film (−55 … +155 °C per LCSC listing); all capacitors X5R
(−55 … +85 °C), X7R / C0G (−55 … +125 °C) by EIA class. Worst resistor load ≈ 5 mW = 8 % of rating.
Second source for every passive: any maker's part with the same size, value, tolerance, dielectric and ≥
voltage / power (generic; JLC basic equivalents). The 1 Ω, 5.6 kΩ and 27 Ω are JLC extended
(3 × $3.07 per order; 560 kΩ R17 removed by D-007); 27 Ω could become 22 Ω basic (C25092) only with an owner decision against RPi p.15.
Size: **0402** (RPi minimal design uses 0402, p.7; JLC basic; hand-reworkable) instead of the Pico 2's
0201 (M0603 metric in RP-008306) → **P4-7**. Values marked ESTIMATE are confirmed in the phase 5 schematic.

## PCB features (no purchased part)
- JP1–JP4: cuttable solder jumpers on GP12–GP15 (R-14, A2-2), bridged by default.
- Test pads: TP1–TP7 as the Pico 2 (incl. SWCLK, SWDIO, GND, D-002), plus DRDY and FAULT of the MAX31856.
These are copper only; they are listed as comment lines in `bom/bom.csv`.

## RoHS / REACH (D-005)
LCSC `isRohsCert` flag (2026-10-15): certificate on file for TPS63001, TPS63000, MAX31856, W25Q32RV, ABM8,
AOTA, SHOU HAN Type-C, USBLC6 (ST and UMW), MBR120, DMG1012T, TS-1187A, both LEDs, all Samsung caps except
C1548 (FH), Murata LQH3NP, and the 1 kΩ, 33 Ω, 100 Ω, 200 Ω, 10 kΩ resistors. **No certificate listed** for RP2350A, GD25Q32E,
HRO TYPE-C-31-M-12, PMEG6010ELR, FH 15 pF and the other UNI-ROYAL values. Omega gives a RoHS 2015/863
certificate for PCC-SMD. **REACH SVHC declarations were not collected** (no supplier page offers them
directly); open item before first supply (D-005 S3-1), not a rev-A blocker.


## Cost estimate per board (ESTIMATE)
Parts = sum of `bom/bom.csv` rows (DNP excluded) at the order quantity (boards × qty per board, LCSC MOQ
applied), LCSC/JLC list prices of 2026-10-15; L1 at JLC (P4-4b recommendation), PCC-SMD in PCC-SMD-20 strips ($53.78).
Assembly = JLCPCB **Economic PCBA** fee table (updated 2026-09-09, fetched 2026-10-15,
https://jlcpcb.com/help/article/pcb-assembly-price): setup $8.18, stencil $1.53, $3.07 per unique extended
part (15 here), SMT $0.0016/joint, pre-reflow (pin-in-paste) $0.016/joint, X-ray per leadless part
(RP2350, flash, TPS63001). Joint count ≈ 235 per board is an ESTIMATE from the pad counts.

| Item | 5 boards (rev-A) | 100 boards | Source |
|------|------------------|------------|--------|
| Parts (all rows except PCC-SMD; L1 = MPL-AT2512-3R3, P4-4b) | $14.92 | $10.46 | bom.csv, LCSC/JLC 2026-10-15 |
| PCC-SMD (2 per board) | $10.76 (one strip of 20 for 10 clips) | $5.38 (10 strips) | Omega $53.78 / PCC-SMD-20 |
| **Parts subtotal** | **$25.68** | **$15.84** | |
| JLC setup + stencil | $1.94 | $0.10 | JLC fee table |
| Extended-part feeder loading (15 × $3.07) | $9.21 | $0.46 | JLC fee table |
| SMT joints + 4 pin-in-paste joints | $0.44 | $0.44 | JLC fee table, ESTIMATE joint count |
| X-ray (3 leadless parts per board) | $2.46 ($0.82/pc tier) | $0.99 ($0.33/pc tier) | JLC fee table |
| PCC-SMD placement | owner hand-solders (no fee) | consignment customs agent ≈ $45 ⇒ $0.45 | JLC consignment note |
| **Subtotal without PCB** | **≈ $39.73** | **≈ $18.28** | ESTIMATE |
| PCB fabrication, 4-layer 1.0 mm, castellated, 51 × 21 mm | **not quoted** | **not quoted** | JLC quote page is JS-only; JLC home page lists FR-4 "from $2.00 / 5 pcs", which is not this spec |
| Shipping, import VAT/duty, AOTA sourcing route | not included | not included | |

Biggest levers: PCC-SMD (43 % of rev-A parts), MAX31856, flash. The GD25Q32EEIGR alternate would save
$2.65 (5) / $2.34 (100) per board. If L1 is consigned for rev-A, add ≈ $45 customs per order
(≈ $9 per board at 5 boards). D-007 delta (ESTIMATE, not re-summed into the table): 0603 caps + R17 removed ≈ −$0.19 parts/board at 5 boards and ≈ −$0.11 at 100; one extended part fewer (14) = −$3.07 per order. D-008 delta (ESTIMATE): +1 × 4.7 µF + 2 × 10 µF (basic, no feeder fee) ≈ +$0.095 per board at 100 ($0.0159 + 2 × $0.0395), ≈ +$0.10 at 5 boards (MOQ cut-tape). The cost target is still an open non-blocking item (D-001).

## P4-4b: replacement for the core-regulator inductor (L1), accepted D-007
Owner 2026-10-15 (D-007): MPL-AT2512-3R3 accepted, second source MPL-AL4020-3R3, rev-A built with both dot orientations. The comparison below is kept as the record.

The owner decided on 2026-10-15 to replace AOTA-B201610S3R3-101-T (low stock), not to buy it.

**Raspberry Pi requirements** (RP2350 datasheet, build 2025-07-29, `datasheets/RP2350A.pdf`):
- §6.3.8.2 "Component values", p.455: L_X "must be fully shielded, 3.3 µH ±20 % and with a maximum DC
  resistance of 250 mΩ. Saturation current should be at least 1.5 A. The inductor must be marked for
  polarity (see Figure 25) and placed on the layout as indicated in Figure 23. … we recommend the
  AOTA-B201610S3R3-101-T."
- §6.3.8.3 "Regulator sensitivities", p.456: efficiency is sensitive to inductance roll-off ("an inductor
  with low roll-off is required … generally the higher saturation current the better"); leakage field of
  even shielded inductors couples into the LX/COUT loop, so "the inductor has to be the right way around …
  especially at higher output currents and for higher load transients. This necessitates an inductor with
  marked polarity." RPi and Abracon made the custom 2.0 × 1.6 mm part for this (p.456, Fig. 25–26).
- §6.3.8.1 "Layout recommendations", p.454–455: follow Fig. 22 / Fig. 23 as closely as possible; keep
  C_IN/L_X/C_OUT on one side; cut copper under L_X / VREG_LX on the top layer and layer 2 (Fig. 24).
- Hardware design with RP2350 (build 2026-07-03), p.6–7: RPi found no suitable polarity-marked part in
  0806; "if you choose not to use our example, then you do so at your own risk".
- Alternative from the same datasheet, §6.3 p.451 Fig. 21: power DVDD from an external 1.1 V supply,
  disable the regulator, omit the inductor (VREG_VIN/VREG_AVDD still powered, VREG_FB to GND).

| Candidate (MPN) | Mfr | Key specs vs requirement | Package | Price @1 | @100 | @1000 | Price source + date | Stock (source, date) | Lifecycle | Second source | Datasheet (rev) | Notes / risks |
|-----------------|-----|--------------------------|---------|----------|------|-------|---------------------|----------------------|-----------|---------------|-----------------|---------------|
| MPL-AT2512-3R3 | Monolithic Power Systems | 3.3 µH ±20 %; DCR 116 typ / **140 mΩ max** (≤ 250 ✓); Isat 3 A typ at 25 °C and 100 °C (30 % drop; ≥ 1.5 A ✓, typ only); top mark "Start of Winding · (dot)" ✓ (p.3); "molded construction", −40 … +125 °C (p.1–2) | 2.5 × 2.0 × 1.2 mm; land 2.90 × 2.30 (p.3) | $0.6568 | ESTIMATE ≤ $0.6568 | $0.4251 (lowest JLC tier) | JLC C3224274, 2026-10-15 (JLC offer range; tiers not shown in the page data) | JLC 146; LCSC page gave no data; MPS store 100 (search snippet) | Active ("正在供货", MPS page snippet) | MPS MPL-AL4020-3R3 (other footprint) | datasheets/MPL-AT2512-3R3.pdf (Rev. 1.2, 7/6/2023) | Datasheet does not say "shielded" (one distributor listing says "Unshielded"; MPS brochure calls its molded series magnetic-shielded): owner/RPi to confirm. Larger than 0806, so Fig. 23 layout cannot be copied 1:1. JLC extended. |
| MPL-AL4020-3R3 | Monolithic Power Systems | 3.3 µH ±20 %; DCR 34.5 typ / 38.4 mΩ max; Isat 5.2 A typ; dot = start of winding (p.3); −40 … +155 °C | 4.1 × 4.1 × 1.9 mm | $1.4554 | ESTIMATE ≤ $1.4554 | $0.8886 | JLC C3222847, 2026-10-15 | JLC 16 | Active | MPS MPL-AT2512-3R3 | datasheets/MPL-AL4020-3R3.pdf (Rev. 1.1) | Highest Isat, lowest roll-off, but large; 16 in stock. JLC extended. |
| PIM201610-3R3MTS00 | FH (Fenghua) | 3.3 µH, 140 mΩ, Isat 2 A, 0806 (search snippet of FH approval sheet) | 2.0 × 1.6 mm | $0.0345 | - | $0.0289 | JLC C5137211, 2026-10-15 | JLC 0, LCSC out of stock | no data | - | not saved | **Rejected**: no polarity mark documented, no stock. (Used on a Kamami RP2350 board per search snippet.) |
| AOTA-B201610S3R3-101-T | Abracon | RPi-recommended reference | 0806 | - | - | - | phase 4 table | LCSC 0, JLC 4 | Active | - | datasheets/AOTA-B201610S3R3-101-T.pdf | **Rejected by owner** (2026-10-15). |
| External 1.1 V LDO, regulator off | (part not chosen) | No inductor (RP2350 datasheet Fig. 21 p.451) | - | - | - | - | - | - | - | - | - | Changes the power tree (D-004), adds an LDO + caps; linear 3.3 → 1.1 V loss; no RP2350 Pico 2 parity. Fallback only. |

No candidate with good LCSC/JLC stock was found that documents a polarity mark: high-stock 2016 parts
seen (FH PIM201610) have no documented mark. Würth WE-MAPI, DigiKey/Mouser and the RPi forum blocked the
fetch, so they could not be checked.

**Recommendation (P4-4b): MPL-AT2512-3R3** (meets every numeric RPi limit with margin and has a documented
winding-start dot), with **MPL-AL4020-3R3** as the named second source (needs its own footprint
variant; MPS, same maker). Because the winding sense relative to the Abracon part is unknown, rev-A
should build boards with the dot in both orientations and measure DVDD offset at a load step (the
"right way around" test, p.456). JLC stock (146) covers rev-A and one 100-board run; nothing is bought by the agent.
If the owner wants no RPi deviation at all, the fallback is the external 1.1 V LDO route (Fig. 21).

## Summary of recommendations (owner decided: D-006)
| ID | Item | Recommendation |
|----|------|----------------|
| P4-1 | Single-source ICs: RP2350A, MAX31856 (both locked D-001), TPS6300x (TI only) | Accept the single-source risk in writing |
| P4-2 | Flash | W25Q32RVXHJQ; approved alternate GD25Q32EEIGR with R6 10 k fitted |
| P4-3 | Crystal | ABM8-272-T3; accept single source (RPi-specified; YXC C9002 fails ESR/CL) |
| P4-4 | VREG inductor AOTA-B201610S3R3-101-T | Superseded by the owner: replace (P4-4b, open) |
| P4-4b | VREG inductor replacement | MPL-AT2512-3R3, second source MPL-AL4020-3R3 (open, pending owner OK) |
| P4-5 | PCC-SMD | Accept single source (Omega); rev-A: owner hand-solders from one PCC-SMD-20 strip; volume: consign to JLC |
| P4-6 | USB-C | (accepted, option A) Swap primary to SHOU HAN TYPE-C 16PIN 2MD(073) (meets +85 °C), HRO TYPE-C-31-M-12 as alternate (amends D-004); accept tab tips ≤ 0.2 mm below the board |
| P4-7 | Passive size | 0402 (JLC basic), not the Pico 2's 0201 |
| P4-8 | TVS on T+/T− | None; rely on MAX31856 ±45 V + Fig. 8 filter + MW-02 |
| P4-9 | SW1, Q1 without a named second source | Accept for rev-A; name alternates in phase 5 |
| P4-10 | LED | KT-0805G (basic) |
| P4-11 | Assembly service | JLC Economic PCBA if it accepts 4-layer + castellated holes at order time, else Standard (higher setup and per-part fees, not costed) |

## Blockers and open data
- PCB fabrication price not quoted (JLC quote page needs a browser session / Gerbers).
- L1: AOTA rejected by the owner; P4-4b open. Replacement MPL-AT2512-3R3 has JLC stock 146 only. DigiKey/Mouser numbers are search snippets (Mouser and Findchips blocked the fetch).
- PCC-SMD: Omega price from the product page via WebFetch (curl blocked); JLC consignment approval for a part without a JLC number not yet asked.
- REACH SVHC declarations not collected; RoHS certificates missing on LCSC for some parts (table above).
- Values marked ESTIMATE in phase 4: resolved in phase 5 where a source allows, see "Phase 5 resolution" below.
- Datasheets not saved: UMW USBLC6-2SC6, PMEG6010ELR, APV/YXC rejects, generic passive series sheets.

## Phase 5 resolution of phase-4 ESTIMATE values (2026-10-15)
Sources and pages are in `parts/constraints/*.yaml`. No BOM row was added or removed; changes are proposals for the owner (P5-x in STATUS.md).

| Item | Phase 4 | Phase 5 result | Source |
|------|---------|----------------|--------|
| RP2350A 100 nF count | ESTIMATE 10 | **10, resolved**: 6 IOVDD + 3 DVDD + 1 shared on pins 53/54. ADC_AVDD gets only its RC-filter capacitor (Pico 2 W: no 100 nF on pin 44). Matches RPi minimal design C8, C10–C18. C1–C15 total stays 15 | HDG §2.2.1 p.8, Fig. 15 p.20; Pico 2 W schematic |
| VSYS/3 divider | R19 20 kΩ + 10 kΩ, mapping ESTIMATE | **Resolved**: VSYS → 20 kΩ → Q1 drain; Q1 source → GPIO29_ADC3 → 10 kΩ → GND; ratio 1/3 | Pico 2 W R5 20K / Q1 / R6 10K |
| Q1 network (R16 100 kΩ, R17 560 kΩ) | ESTIMATE | **Not supported**: Pico 2 W Q1 has no gate resistors (gate = GPIO25/WL_CS). Its 100K parts are R2 (3V3_EN pull-up, = R15) and R8 (PS pull-down, = R16); 560K is R21 in the RT6154 FB divider, which TPS63001 does not need (FB to VOUT, SLVS520C p.3). R16 = PS pull-down; **R17: propose removal (P5-2)**. Gate drive on pico-k is open (P5-5) | Pico 2 W schematic; SLVS520C p.3, p.10 |
| LED resistor R22 | 470 Ω, ESTIMATE ≤ 3.2 mA | 470 Ω = Pico 2 W R3. ESTIMATE 0.3–1.5 mA from 3.3 V with KT-0805G VF 2.6–3.1 V (±0.05 V); KENTO gives intensity only at 5 mA → **P5-3** | KT-0805G p.3–4; Pico 2 W |
| Derated ceramic capacitance | to check | **Not resolved**: no DC-bias curve for CL05A475MP5NRNC / CL21A106KAYNNNE among the saved datasheets. RP2350 C_IN ≥ 4.7 µF, C_OUT 4.7 µF ±20 % (p.455) and TPS63001 15 µF nominal (p.12) → **P5-6** | RP2350 p.455; SLVS520C p.12 |
| Extra 4.7 µF at DVDD pin 23 | not in phase 4 | RP2350 "recommend" for best performance; not in RPi minimal design → **P5-4** | RP2350 §6.3.8.1 p.455 |


## D-007 outcomes (owner, 2026-10-15)
| Item | Result | Source |
|------|--------|--------|
| L1 (P4-4b) | MPL-AT2512-3R3 approved, second source MPL-AL4020-3R3, both orientations on rev-A | D-007; MPL Rev 1.2 |
| R17 (P5-2) | removed from the BOM | D-007 |
| R22 (P5-3) | 470 Ω kept | D-007 |
| DVDD pin 23 (P5-4) | 2nd 4.7 µF added (C28, provisional ref) | RP2350 p.455 |
| Q1 gate (P5-5) | to 3V3 | D-007; DMG1012T p.2 |
| 4.7 µF / 10 µF (P5-6) | 0603: CL10A475KO8NNNC C19666 (16 V, LCSC 927 680 / JLC 3 651 395) and CL10A106MA8NRNC C96446 (25 V, LCSC 2 762 780 / JLC 4 820 292), stock 2026-10-15 | LCSC pages 2026-10-15 |
| S3-7 derating | voltage: 16 V on 1.1/3.3 V nets, 25 V ≥ 10 V on VBUS/VSYS; temperature X5R −55…+85 °C. Capacitance (ESTIMATE, read from the Samsung DC-bias plots): 4.7 µF ≈ 4.5 µF @1.1 V, ≈ 3.2 µF @3.3 V; 10 µF ≈ 6.7 µF @3.3 V, ≈ 4.8 µF @5 V. Shortfalls vs RP2350 C_IN ≥ 4.7 µF and TPS63001 15 µF nominal → **P5-10** (owner) | datasheets/CL10A475KO8NNNC.pdf, datasheets/CL10A106MA8NRNC.pdf |
| Crystal pads 2/4, USB shell (P5-7) | GND; shell via the 4 tab pads | D-007 |
| Source conflicts (P5-8) | accepted as resolved in RP2350A.yaml | D-007 |

## D-008 outcomes (owner, 2026-10-15): P5-10 DC-bias derating
Added one capacitor at each derated spot, same in-stock 0603 JLC basic parts (stock as in D-007). Effective values
(ESTIMATE, re-read from the Samsung plots; range = author read and Reviewer-A F25/F28 read; worst case adds tolerance and the
85 °C TCC point: 4.7 µF −12 %, 10 µF −5 %):

| Spot | Parts | Requirement | Typ effective | Worst case | Meets |
|------|-------|-------------|---------------|------------|-------|
| RP2350 VREG_VIN C_IN (3.3 V) | C16 + C29, 2 × CL10A475KO8NNNC | ≥ 4.7 µF (RP2350 p.455) | 6.4–6.6 µF (−32/−30 %) | ≈ 5.1 µF (−10 % tol) | yes |
| TPS63001 VIN (VSYS ≈ 5 V), superseded by D-009 | C20 + C30, 2 × CL10A106MA8NRNC | ≥ 4.7 µF (SLVS520C p.12) | 8.8–9.6 µF (−56/−52 %) | ≈ 6.7 µF (−20 % tol) | yes |
| TPS63001 VOUT (3.3 V) | C21 + C22 + C31, 3 × CL10A106MA8NRNC | 15 µF recommended nominal (p.12) | 18.6–20.1 µF (−38/−33 %) | ≈ 14.9–16.1 µF at −20 % tol (≈ 14.1–15.3 µF incl. 85 °C) | typ yes; tolerance corner ≈ 15 µF (recommendation, no upper limit p.12) |

New open item from this change (not decided): **P5-14** VBUS inrush. C30 sits on VSYS behind D1, so at plug-in
VBUS sees C19 + C20 + C30 ≈ 13–14 µF effective (30 µF nominal) against the USB 2.0 §7.2.4.1 10 µF limit noted for
C19; the spec text is not in `datasheets/` and was not checked.

## D-009 outcomes (owner, 2026-10-15)
| Item | Result | Source |
|------|--------|--------|
| P5-9 DRDY/FAULT | no pull-up fitted; R23/R24 10 kΩ DNF to 3V3 at the test pads | MAX31856 p.5, p.10 |
| P5-11 ADC_AVDD | C27 4.7 µF CL10A475KO8NNNC (was 2.2 µF 0402 C12530; row removed); D-025: now 0402 TDK105CBJ475MV-F (C22385335) | Pico 2 Fig. 11 p.20 C13 4u7; pico-2-w-schematic.pdf p.1 C13 4u7 |
| P5-12 PCC-SMD polarity | from the drawing: board edge seen from outside, component side up: + right (J2), − left (J3) | PCC-SMD p.2 |
| P5-13 L1 | documented rev-A deviation, both orientations, DNF external 1.1 V footprint | RP2350 Fig. 21 p.452 |
| P5-14 TPS63001 Cin | ONE C20 CL31A106KBHNNNE 10 µF 50 V X5R 1206 (LCSC C13585: LCSC stock 20, JLC basic stock 2 346 959, 2026-10-15) instead of 2 × 0603 | datasheets/CL31A106KBHNNNE.pdf |

Effective values of C20 (ESTIMATE, Samsung DC-bias curve, read 2026-10-15): −22.5 % at 5.0 V → 7.75 µF;
−24.8 % at 5.25 V → 7.5 µF; worst case −10 % tolerance and ≈ −10 % at 85 °C (TCC plot) → ≈ 6.1 µF ≥ 4.7 µF.
For comparison, D-008's 2 × CL10A106MA8NRNC: −55.6 % at 5 V → 2 × 4.44 = 8.9 µF typ, but ≈ 71 µC charge at attach.

USB attach charge budget (ESTIMATE; charge integrated from the DC-bias curves, 0 → 5 V on VBUS, ≈ 4.7 V on VSYS):

| Item | Charge | Note |
|------|--------|------|
| C19 10 µF 0603 on VBUS | ≈ 37 µC | directly across VBUS |
| C20 1206 on VSYS | ≈ 44 µC | D1 is forward-biased at attach, so the cap charges from VBUS |
| 3V3 + 1V1 caps via TPS63001 | ≈ 51–56 µC | stored ≈ 224 µJ (C21 C22 C31, C16 C18 C27 C29, 100 nF), η 0.85–0.9 assumed; soft start begins at 400 mA average (SLVS520C §7.4.1 p.9) |
| Total | ≈ 132–137 µC | USB 2.0 load model 10 µF × 5 V = 50 µC (§7.2.4.1 p.177, Note 9 p.184) |

Conclusion: no single input capacitor satisfies both the TPS63001 4.7 µF minimum and the USB 2.0 limit, because the
regulator-side charge alone is ≈ 50 µC. Minimal alternative (not taken for rev-A, D-010; it is the rev-B action if the bring-up droop test fails): C19 → 4.7 µF and a slew-rate-controlled
load switch between VBUS and VSYS (ramp ≥ 3 ms keeps the average attach current below 100 mA); or accept and measure
the droop on rev-A. Cost of D-009 changes at 100 (ESTIMATE): C20 $0.1614 instead of 2 × $0.0395 → +$0.08 per board; C27 0603 4.7 µF
instead of 0402 2.2 µF → +$0.01; R23/R24 DNF → $0.

## D-025 and D-030 outcomes (layout-phase BOM updates, 2026-10-17 & 2026-10-23)

| Decision | Refs | Change | MPN & Sourcing | Technical & Datasheet Basis |
|----------|------|--------|----------------|-----------------------------|
| **D-025** (2026-10-17) | `C18, C27` | `0603` (`CL10A475KO8NNNC`) → `0402` 4.7 µF 25 V X5R (`TDK105CBJ475MV-F`) | Primary: Taiyo Yuden `TDK105CBJ475MV-F` (LCSC `C22385335`, $0.0345 @100, JLC extended 44,829 stock). Alternates: Chinocera `HGC0402R5475M250NTEJ` (LCSC `C22367824`), FH `0402X475K160NT` (LCSC `C20624278`). | Frees escape room at U1 north-east corner (`GP22/26/27/28`, pins 34, 40–42). DC bias at 3.3 V ≈ −42 % → ≈ 2.7 µF typ (≈ 2.2 µF at −20 % tol) vs ≈ 3.2 µF on 0603 (`datasheets/TDK105CBJ475MV-F.pdf` curve `AQC19J26-08D`), accepted by owner (`D-025`). |
| **D-030** (2026-10-23) | `L2` | `3015` (`SWPA3015S2R2MT`) → `2016` 2.2 µH (`DFE201612P-2R2M`) | Primary: Murata `DFE201612P-2R2M` (ordered MPN `DFE201612P-2R2M=P2`, LCSC `C79317`, $0.1061, JLC extended 7,809 stock). Alternates: Sunlord `WPN201610M2R2MT` (LCSC `C97011`, Isat 2.0 A, Irms 1.6 A, DCR 135 mΩ), cjiang `FTC201612S2R2MBCA` (LCSC `C18724414`, Isat 3.3 A, Irms 3.1 A, DCR 90 mΩ), FH `PFM201610-2R2MTS00` (LCSC `C42885593`, Isat 2.8 A, Irms 2.1 A, DCR 120 mΩ). | Frees the `U3` (`TPS63001`) power block on the 51 × 21 mm board. Rated 2.1 A (`Isat`, 30 % drop) / 1.5 A (`Itemp`) ≥ 0.95 A required (`SLVS520C` Eq. 4 + 20 %), DCR 144 mΩ max (`datasheets/DFE201612P-2R2M.pdf` p.2/9). |
| **D-030** (2026-10-23) | `C20` | `1206` (`CL31A106KBHNNNE`) → `0805` 10 µF 25 V X5R (`CL21A106KAYNNNE`) | Primary: Samsung `CL21A106KAYNNNE` (LCSC `C15850`, $0.0692, JLC basic 3,710,191 stock). Alternates: Murata `GRM21BR61E106KA73L` (LCSC `C84416`), FH `0805X106K250NT` (LCSC `C40894`), Walsin `0805X106K250CT` (LCSC `C89284`). | Clears `J4` castellated edge courtyard at 51 × 21 mm. DC bias at 5.0 V ≈ −42 % → ≈ 5.8 µF typ, worst case (−10 % tol) ≈ 5.0 µF ≥ 4.7 µF min (`SLVS520C` p.12; `datasheets/CL21A106KAYNNNE.pdf` graph 3). Also reduces USB attach charge on `VSYS` (`D-010`). |
| **D-030** (2026-10-23) | `C32` | Added 16th `0402` 100 nF 16 V X7R (`CL05B104KO5NNNC`) | Same row as `C1–C15` (Samsung `CL05B104KO5NNNC`, LCSC `C1525`, qty 15 → 16). | High-frequency decoupling directly at `U1` `ADC_AVDD` pin 44 alongside `C27` (`4.7 µF`), resolving `Reviewer-A` Q3 (`D-030`). |

## Phase 10 BOM lock & 3 sourcing rules verification (`bom/bom.csv`)

Every fitted row in `bom/bom.csv` is now set to `status: locked` (36 rows total, 69 component references; `R6` and `R23/R24` are `dnp: yes` and `status: locked`), and `ohmai check bom-schema` + `ohmai check bom-lock` pass with 0 errors against the Phase 6/8 schematic netlist and the local `jlcparts` SQLite database:

1. **Rule 1 — Generic passives + LED (`generic: ...` + ≥2 concrete alternates from unique manufacturers with LCSC codes)**:
   - Every generic capacitor row, resistor row, and `D2` (`KT-0805G`, 0805 green LED) in `bom/bom.csv` specifies `generic: ...` criteria in `approved_alternates` and `second_source` plus at least two concrete drop-in MPNs from distinct manufacturers (`Murata`, `Taiyo Yuden`, `TDK`, `YAGEO`, `Walsin`, `Panasonic`, `KOA Speer`, `Samsung`, `Chinocera`, `FH`, `Orient`, `NationStar`, `Lite-On`) with their LCSC `C#` part numbers and @100 unit prices verified against `.toolcache/jlcparts/cache.sqlite3`.
2. **Rule 2 — Non-generic multi-source components (≥2 unique manufacturers across primary + drop-in alternates)**:
   - `U2` (Winbond `W25Q32RVXHJQ` → GigaDevice `GD25Q32EEIGR` `C2973794`, PUYA `PY25Q32HB-UAAH-IR` `C3036326`), `SW1` (XKB `TS-1187A-B-A-B` → Korean Hroparts `K2-1187SQ-A4SW-06` `C92584`, SOFNG `TS-1187-1526` `C111461`), `D2` (KENTO `KT-0805G` → `generic: 0805 green LED` + Orient `ORH-G35A` `C205442`, NationStar `NCD0805G1` `C84260`, Lite-On `LTST-C170KGKT` `C98221`), `L2` (Murata `DFE201612P-2R2M` → Sunlord `WPN201610M2R2MT` `C97011`, cjiang `FTC201612S2R2MBCA` `C18724414`, FH `PFM201610-2R2MTS00` `C42885593`), `D1` (onsemi `MBR120VLSFT1G` → flat-lead ultra-low-`Vf` Schottky diodes Nexperia `PMEG2010ER,115` `C82288`, ROHM `RB161MM-20TR` `C123070`, Toshiba `CRS08(TE85L,Q,M)` `C141550`), `Q1` (Diodes Inc. `DMG1012T-7` → SOT-523 low-`VGS(th)` FETs Will Semicon `WNM4153-3/TR` `C239557`, Prisemi `PNM523T201E0` `C110710`), `J1` (SHOU HAN `TYPE-C 16PIN 2MD(073)` → Korean Hroparts `TYPE-C-31-M-12` `C165948`), `U4` (STMicroelectronics `USBLC6-2SC6` → UMW `USBLC6-2SC6` `C2687116`).
3. **Rule 3 — Single-source components (6 rows qualified with `single-source (D-xxx)`, blank `approved_alternates`, and `checked:` exhausted candidate search)**:
   - `U1` (`RP2350A`, Raspberry Pi) [`D-001, D-006`] — `checked: RP2040 (QFN-56, not pin-compatible with QFN-60 7x7); RP2350B (QFN-80, different package); STM32/ESP32 (different MCU architecture, violates R-01/D-001)`
   - `Y1` (`ABM8-272-T3`, Abracon) [`D-006`] — `checked: YXC X322512MSB4SI (LCSC C9002, rejected: CL 20 pF / ESR 80 ohm > 50 ohm RP2350 Table 597); YXC X322512MMB4SI (LCSC C50430, rejected: ESR 80 ohm > 50 ohm); Epson Q22FA23V00501 (LCSC C255903, rejected: ESR 100 ohm > 50 ohm); YXC X322512MLB4SI (LCSC C112971, rejected: CL 9 pF / ESR 80 ohm > 50 ohm)`
   - `L1` (`MPL-AT2512-3R3`, Monolithic Power Systems) [`D-007, D-009, D-006`] — `checked: Abracon AOTA-B201610S3R3-101-T (0 stock on LCSC/JLC); MPS MPL-AL4020-3R3 (LCSC C3222847, rejected as drop-in: 4.1x4.1 mm separate footprint); Murata DFE252012F-3R3M (LCSC C2906241, rejected: unpolarized without winding start dot required by RP2350 Fig. 23)`
   - `U3` (`TPS63001DRCR`, Texas Instruments) [`D-004, D-006`] — `checked: TI TPS63000DRCR (LCSC C24966, rejected as drop-in: adjustable version needs FB divider pads + same manufacturer TI); TI TPS63021 (14-pin DSBGA/VSON, not pin-compatible with VSON-10 3x3 DRC0010J); ADI LTC3112 / Renesas ISL91107 (incompatible package and pinout)`
   - `U5` (`MAX31856MUD+T`, Analog Devices) [`D-001, D-006`] — `checked: ADI MAX31855KASA+ (SOIC-8, K-type only, no DRDY/FAULT pins, not pin-compatible with TSSOP-14); TI ADS1118IDGSR (VSSOP-10 raw ADC without built-in linearization/fault engine, incompatible pinout); Microchip MCP9600 (20-lead QFN I2C, incompatible interface and footprint)`
   - `J2 J3` (`PCC-SMD`, Omega) [`D-004, D-006`] — `checked: Omega SMPW-CC-K-F (full plastic housing, incompatible with compact 2-clip PCC-SMD land pattern); Newport/Labfacility miniature thermocouple PCB jacks (through-hole only, no SMT clip equivalent on LCSC/JLC)`
