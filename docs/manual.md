# User instructions: pico-k

> **Regulatory status (`D-003`, `D-005`):** Target market is **EU only** (`STATUS.md` `markets: [EU]`; UK/US not applicable). Revision `rev-A` (5–10 prototype boards) is built solely for the manufacturer's own R&D (`D-005` S3-1 = D3) and is not placed on the market. Before any unit is supplied to another person or placed on the EU market, the pre-compliance/EMC assessment (`S3-9`), RoHS/REACH technical file, WEEE registration, and final EU Declaration of Conformity must be completed (`docs/safety.md` §Certification path).

## Product Identification
- **Product name:** `pico-k` (RP2350A Type-K Thermocouple Stick Module)
- **Model / type number:** `PICO-K-REVA`
- **Hardware revision:** `rev-A` (printed on bottom silkscreen as `pico-k rev-A`)
- **Batch or serial number:** Printed on the unit packaging label and accompanying document in format `Batch YYYY-WW-NNN` (and optional unit serial number `SN-YYYY-NNNN` for tracked test units; the 51 × 21 mm bare PCB carries `pico-k rev-A` on the bottom silkscreen per `GPSR (EU) 2023/988` Art. 9(5) and `EMC 2014/30/EU` Art. 7(5)).
- **Form factor & layout:** 51.0 × 21.0 × 1.0 mm 4-layer bare stick PCB (`R-02`) with a top-mounted USB-C receptacle (`J1`) at the west edge, a top-mounted miniature Type-K thermocouple socket (`J2` `T+` Chromel / `J3` `T−` Alumel, 2 × Omega `PCC-SMD` clips) at the east edge (`R-07`), and 40 Pico-2-compatible edge pins (`J4`, 2.54 mm pitch) along the north and south edges (`R-03`, `R-04`). See `out/release/rev-A/assembly-top.pdf` and `out/release/rev-A/schematic.pdf` for mechanical and component drawings.

## Manufacturer and Contact
- **Manufacturer & economic operator established in the EU (`Reg. (EU) 2019/1020` Art. 4; `GPSR (EU) 2023/988` Art. 9(6); `EMC 2014/30/EU` Art. 7(6)):**
  - **Name / trade name:** Hardware Lab (placeholder; replace with registered legal entity name prior to placing on the EU market)
  - **Postal address (street & postal code):** Examplegatan 1, 111 22 Stockholm, Sweden (placeholder postal address; printed on packaging and this manual because a full postal address cannot fit legibly on the 21 mm wide board per `docs/safety.md` §Labelling)
  - **Electronic address:** `support@example.com` and `https://example.com/pico-k`
  - **EU economic operator status:** The manufacturer is established in the EU (Sweden) and acts as the responsible economic operator established in the EU under Regulation (EU) 2019/1020 Art. 4 (no separate non-EU importer or authorised representative is required when manufactured and placed on the market by the EU manufacturer).

## Intended Use
- **Intended purpose:** `pico-k` is a USB-powered microcontroller and 1-channel Type-K thermocouple measurement module (`RP2350A` + `MAX31856MUD+T`) designed for benchtop temperature logging, laboratory prototyping, and integration into low-voltage electronic projects as a drop-in Raspberry Pi Pico 2 footprint module (`R-01`..`R-16`).
- **Intended users:** Competent adults, engineers, technicians, educators, and makers (`D-005`, `H8`).
- **EMC environment (`EMC Directive 2014/30/EU` Art. 18):** Designed for Class B residential, commercial, and light-industrial electromagnetic environments (`EN 55032` Class B / `EN 55035`; no residential use restriction applies).
- **Foreseeable misuse (strictly prohibited):**
  - **Never touch or probe live electrical circuits or mains voltage:** The thermocouple input (`T+`/`T−`) is **not electrically isolated** from the USB ground (`D-004` A2-4, `MW-02`).
  - **Do not immerse the PCB or connector in the hot zone:** Only the rated thermocouple probe tip and sheath may enter the heated zone (`MW-03`, `MW-04`).
  - **Do not use for medical, life-support, safety-critical shutoff, or direct food contact** (unless the external thermocouple probe itself is certified food-safe, `MW-06`).
  - **Do not power from supplies above 5.5 V DC** or apply external power contradicting `MW-05`.

## Ratings and Specifications
> **Note:** All electrical and thermal figures below are **design ratings** traced to `docs/requirements.md`, `docs/architecture.md`, and component datasheets (`RP2350A`, `TPS63001DRCR`, `MAX31856MUD+T`, `PCC-SMD`), pending `rev-A` bench verification (`test/bringup-plan.md`).

| Parameter | Rating / Specification | Unit | Source / Traceability |
|-----------|------------------------|------|-----------------------|
| Supply voltage (`VBUS` via USB-C `J1` or pin 40) | `5.0 ± 10 %` (`4.50 to 5.50`) | V DC | `R-06`; Pico 2 datasheet §3.3 p.12 |
| `VSYS` pin input range (pin 39, design capability) | `1.80 to 5.50` (USB 5 V is the only supported supply per `R-06`/`MW-05`) | V DC | `W-03`; Pico 2 datasheet §3.3 p.12; `TPS63001` `SLVS520C` p.1 |
| Board supply current (`VBUS = 5.0 V`, no external `3V3` load) | `17` typ (idle + 1 Hz TC read) to `120` max (dual-core active + flash) | mA | `docs/architecture.md` §A2-1 (design rating pending rev-A bench test) |
| Regulated `3V3` output (pin 36, for external circuitry) | `3.30 ± 3 %` (`≤ 300 mA` max external load) | V DC / mA | `R-04`; Pico 2 datasheet p.9; `docs/architecture.md` §A2-1 |
| GPIO logic level (`GP0`–`GP22`, `GP26`–`GP28`) | `3.3` nominal (not 5 V tolerant when unpowered) | V DC | `R-04`; `RP2350` datasheet §5.5.3 |
| Thermocouple input (`J2` `T+` / `J3` `T−`) | 1 channel, Type K (Chromel `+` / Alumel `−`), miniature flat-pin plug (`SMPW-K-M`) | - | `R-07`, `R-08`, `D-004` |
| Thermocouple measurement range (Type K) | `−200 to +1372` | °C | `R-10`; `MAX31856` datasheet Table 1 p.12 |
| Thermocouple conversion accuracy (linearized) | `±0.15 %` of full-scale TC voltage (`TA = −20 to +85 °C`, excl. probe error) | % FS | `R-11`; `MAX31856` datasheet p.1, p.3 |
| Cold-junction compensation (CJC) accuracy | `±0.7` (`TA = −20 to +85 °C`, internal sensor in `U5` coupled to `J2`/`J3`) | °C | `R-11`, `R-13`; `MAX31856` datasheet p.1, p.28 |
| Thermocouple input absolute maximum voltage | `±45` (protection limit on `T+`/`T−` vs `GND`; **not** safety isolation) | V | `MAX31856` datasheet p.2, p.14 (`MW-02`) |
| Board operating ambient temperature (incl. self-heating) | `−20 to +85` (recommended max ambient `+70 °C`) | °C | `docs/requirements.md` §Environment; Pico 2 datasheet §3.3 p.12 (`MW-04`) |
| Thermocouple socket (`J2`/`J3` `PCC-SMD`) temperature range | `−50 to +120` | °C | Omega `PCC-SMD` datasheet p.1 (`MW-04`) |
| Relative humidity & ingress protection | `10 % to 80 %` RH (non-condensing); `IP00` (bare open PCB module, indoor dry use) | - | `docs/safety.md` §Insulation (Pollution Degree 2, indoor) |
| Dimensions & mass | `51.0 × 21.0 × 1.0` mm, 4-layer FR-4 PCB (`≈ 3.5 g`) | mm / g | `R-02`, `D-004` |

## Safety Information
Read and follow all safety warnings below before connecting or powering `pico-k`. Every warning ID (`MW-01` through `MW-06`) is registered in `STATUS.md` and `docs/safety.md`:

- **MW-01: WARNING – Grounded-junction probes and common-mode voltage limit.** If a grounded-junction thermocouple probe touches an electrically conductive object that is referenced to the same earth as the USB host (for example, an earthed metal chassis or pipe while the board is plugged into a mains-earthed desktop PC or laptop on an earthed charger), the thermocouple input lies outside the `MAX31856` common-mode input range (`0.5 V to 1.4 V` above `GND`, `MAX31856` datasheet p.3): temperature readings are unspecified and the over/under-voltage (`OVUV`) fault may halt conversions (p.26). **How to avoid:** Power `pico-k` from an isolated USB powerbank or a battery-operated (ungrounded) laptop when using a grounded-junction probe on earthed objects, or use an ungrounded (insulated-junction) thermocouple probe (`D-004` A2-4).
- **MW-02: WARNING – Electric shock and equipment damage (no galvanic isolation).** Never touch live electrical parts, mains wiring, or hazardous voltages with the thermocouple probe or its cable. The thermocouple input (`T+`/`T−`) is biased from the board and is **not electrically isolated** from the USB ground (`GND`). Touching a live circuit puts that voltage directly onto the `pico-k` board, the USB cable, and the host computer, creating a risk of electric shock, fire, and permanent damage (`docs/safety.md` `H1`; `MAX31856` datasheet p.2, p.14).
- **MW-03: WARNING – Burn and fire hazard from hot thermocouple probe.** The thermocouple probe tip and sheath can reach extreme temperatures (Type K up to `+1372 °C`, `R-10`) and remain dangerously hot long after removal from the heat source, causing severe burns or igniting nearby materials. **How to avoid:** Use only thermocouple probes rated for the target temperature, clamp the probe securely, keep flammable materials away, and allow the probe to cool completely before touching or storing (`docs/safety.md` `H3`).
- **MW-04: CAUTION – Board and connector temperature limits.** Only the thermocouple probe tip and sheath may enter the hot measurement zone. Keep the `pico-k` PCB within `−20 °C to +85 °C` (including self-heating, `Pico 2` datasheet §3.3 p.12) and keep the miniature socket clips (`J2`/`J3` `PCC-SMD`) and mating plug within `−50 °C to +120 °C` (`PCC-SMD` datasheet p.1; `docs/safety.md` `H4`). Use a sufficiently long probe cable (`≤ 3 m` total, `D-005` S3-5) to keep the board away from heat sources.
- **MW-05: CAUTION – Power supply limits.** Power `pico-k` only from a regulated USB 5 V source (`4.5 V to 5.5 V` DC from a computer USB port or USB powerbank, `R-06`). Do not apply voltages outside `1.8 V to 5.5 V` to `VSYS` (`J4.39`) or feed external power into `VBUS` (`J4.40`) while a USB cable is connected (`docs/safety.md` `H6`).
- **MW-06: CAUTION – Bare electronic module, ESD, children, and food contact.** `pico-k` is an unenclosed bare PCB module, not a toy; keep out of reach of children (`docs/safety.md` `H8`). Do not use the probe in contact with food or liquids intended for consumption unless the external thermocouple probe is specifically certified for food contact. Handle the bare board by its edges and observe electrostatic discharge (ESD) precautions to avoid damaging exposed components (`docs/safety.md` `H7`).

## Installation and Use
1. **Handling and mounting (`R-03`, `R-05`, `R-07`):**
   - Hold the board by its edges (`MW-06`).
   - `pico-k` can be used stand-alone on an insulated bench surface, fitted with standard 2.54 mm pitch `1 × 20` pin headers on the 36 through-hole edge pins (`J4.2`–`J4.19`, `J4.22`–`J4.39`), or reflow/hand-soldered flat onto a carrier PCB using all 40 castellated edge pads (`J4.1`–`J4.40`, `D-017`). Do not place the bare bottom side of the PCB onto conductive surfaces.
2. **Connecting the Type-K thermocouple (`R-07`, `R-08`, `D-009` `P5-12`):**
   - Insert a standard miniature flat-pin Type-K thermocouple plug (`SMPW-K-M` or equivalent, 7.9 mm pin spacing) horizontally into the top-side socket clips `J2` and `J3` at the sensor edge opposite the USB-C port.
   - Observe polarity marked on the top silkscreen: **`+` (`J2`, Chromel non-magnetic narrower blade, right clip seen from the sensor edge with components up)** and **`−` (`J3`, Alumel magnetic wider blade, left clip)**. Reversing `+` and `−` causes temperature readings to move in the opposite direction when heated.
3. **Power-up and USB connection (`R-06`, `R-15`, `D-010`):**
   - Connect `J1` (USB-C) to a 5 V USB port on a computer or powerbank using a USB-C cable (`≤ 3 m`).
   - Note (`D-010`): `pico-k` uses direct USB 5 V decoupling without a USB logo/compliance claim; connect directly to a host USB port, powered hub, or powerbank.
4. **EMC installation precautions (`EMC Directive 2014/30/EU` Art. 18; `D-005` S3-5):**
   - Keep both the USB cable and the thermocouple probe cable **≤ 3 m in total length** (`D-005` S3-5) to maintain immunity to conducted RF (`IEC 61000-4-6`) and electrical fast transients (`IEC 61000-4-4`).
   - Route thermocouple leads away from mains power cords, variable-frequency drives, and relay coils. Enable the `MAX31856` on-chip 50 Hz (EU) or 60 Hz notch filter in firmware (`CR0` bit 0).
5. **Firmware and SPI1 pin sharing (`R-14`, `R-16`):**
   - On-board `MAX31856` (`U5`) communicates with `RP2350A` (`U1`) over **SPI1** (`1 MHz` to `5 MHz`, SPI Mode 1 `CPOL=0, CPHA=1` or Mode 3 `CPOL=1, CPHA=1`) using four shared edge pins labeled on the silkscreen:
     - `GP12` (`J4.16`): `MISO` (`TC_SDO`) via solder jumper `JP1`
     - `GP13` (`J4.17`): `CS` (`TC_CS`, active-low, `10 kΩ` pull-up `R7` to `3V3`) via solder jumper `JP2`
     - `GP14` (`J4.19`): `SCK` (`TC_SCK`) via solder jumper `JP3`
     - `GP15` (`J4.20`): `MOSI` (`TC_SDI`) via solder jumper `JP4`
   - Optional status outputs `TC_DRDY` (`TP11`) and `TC_FAULT` (`TP12`) are available on bottom test pads.
   - To disconnect `U5` and reclaim `GP12`–`GP15` as general-purpose edge I/O, cut the trace bridges on `JP1`–`JP4` on the top side; re-bridge with solder to restore SPI1 operation.
   - Example self-test and readout command (MicroPython on RP2350):
     ```bash
     mpremote run test/firmware/bringup_selftest.py
     ```
6. **Troubleshooting:**
   - **`OPEN_PROBE` fault (`SR` bit 0 set):** Check that the Type-K plug is fully seated in `J2` and `J3` and that the thermocouple wire is not broken.
   - **`OVUV` fault (`SR` bit 1 set) or erratic readings:** Check `MW-01` (grounded-junction probe touching an earthed surface while the USB host is mains-earthed); switch to battery/powerbank operation or an insulated probe.
   - **Temperature decreases when probe tip is warmed:** Thermocouple wires are reversed inside the plug; swap Chromel (`+` → `J2`) and Alumel (`−` → `J3`).

## Maintenance and Cleaning
- **Maintenance:** `pico-k` contains no user-serviceable internal parts. Periodically inspect the `J2`/`J3` `PCC-SMD` socket clips and USB-C receptacle `J1` for dust, oxidation, or bent contacts. Do not attempt to operate a board with cracked components, charred PCB traces, or a damaged USB-C receptacle.
- **Cleaning:** Disconnect both the USB-C cable and the thermocouple probe before cleaning. Clean the PCB only with a dry, ESD-safe brush or a lint-free swab lightly moistened with ≥ 99 % isopropyl alcohol (IPA), and allow the board to dry completely before applying power. Never use water, household cleaners, or compressed air containing moisture.
- **Firmware updates:** Hold `SW1` (`BOOTSEL`) while connecting the USB-C cable (`J1`) to mount the `RP2350` UF2 bootloader drive, then copy the `.uf2` firmware image onto the drive.

## Disposal
- **WEEE separate collection (`Directive 2012/19/EU` Art. 14(2), Art. 14(4), Annex IX; `EN 50419:2022`):**
  - The **crossed-out wheeled bin symbol** with horizontal bar (`EN 50419:2022` §4.2.1) is printed on the bottom silkscreen of `pico-k` (and on the packaging and this manual per §4.2.4).
  - **Meaning:** Electrical and electronic equipment (EEE) must **not** be disposed of as unsorted municipal household waste. Separate collection and recycling of waste equipment prevents potential release of hazardous substances (including beryllium-copper alloy in the `J2`/`J3` socket clips) and conserves resources.
  - **User action:** At end of life, return `pico-k` to a designated municipal WEEE collection point for electronic waste or to the retailer/manufacturer take-back scheme in your EU Member State.

## Conformity
- **Markings (`Regulation (EC) 765/2008` Art. 30):** The **CE** mark (`≥ 5 mm` height) and the crossed-out wheeled bin symbol are placed on the flat bottom silkscreen of the board (`docs/safety.md` §Labelling, `D-005` S3-8). *(Note: For `rev-A` own-R&D prototypes under `D-005` D3 that are not placed on the market, the silkscreen artwork is verified for layout fit, and formal CE marking applies only once conformity assessment is completed prior to supplying any board.)*
- **Applicable EU legislation (`D-003`, `D-005`):**
  - **EMC Directive 2014/30/EU** (harmonised standards: `EN 55032:2015+A11:2020` Class B, `EN 55035:2017+A11:2020`)
  - **RoHS Directive 2011/65/EU** as amended by `(EU) 2015/863` (technical documentation standard: `EN IEC 63000:2018`)
  - **General Product Safety Regulation (EU) 2023/988 (GPSR)** (safety risk analysis referencing `EN IEC 62368-1`)
  - **WEEE Directive 2012/19/EU** (`EN 50419:2022`) and **REACH Regulation (EC) 1907/2006**
- **EU declaration of conformity:** Prior to placing `pico-k` on the EU market, the full text of the **EU declaration of conformity** (`EMC Directive 2014/30/EU` Art. 15; `RoHS Directive 2011/65/EU` Art. 7(c)) will be included in the technical documentation and published online at `https://example.com/pico-k/doc`.

## Language Versions
- **Supplied language versions (`GPSR (EU) 2023/988` Art. 9(7); `EMC Directive 2014/30/EU` Art. 7(7); `D-005` S3-8):**
  - Target first EU Member State is **Sweden**: this manual and all safety warnings (`MW-01`..`MW-06`) are supplied in **English (EN)** and **Swedish (SV)** (see Swedish summary of safety warnings below) prior to supplying any unit in Sweden (`Konsumentverket` guidance `[S20]`). Additional official EU Member State language translations are added before placing the product on the market in those Member States.
- **Document revision and date:** Revision `rev-A` (1.0), dated `2026-10-25`.

### Säkerhetsinformation på svenska (Swedish Safety Summary — `S3-8`)
- **Avsedd användning:** `pico-k` är en USB-driven (5 V DC) mätmodul för typ K-termoelement (`RP2350A` + `MAX31856`), avsedd för laboratoriebruk, elektronikbyggen och utveckling av vuxna användare inomhus.
- **MW-01 (VARNING – Jordade givare):** Om ett jordat termoelement berör ett jordat föremål samtidigt som USB-värddatorn är skyddsjordad hamnar ingången utanför `MAX31856` common-mode-område (`0,5–1,4 V`), vilket ger felaktiga mätvärden eller `OVUV`-fel. Driv kortet från en powerbank eller batteridriven bärbar dator, eller använd en ojordad (isolerad) givare.
- **MW-02 (VARNING – Risk för elchock, ingen isolering):** Berör aldrig spänningsförande delar eller nätspänning med givaren eller dess kabel. Termoelementingången är **inte** galvaniskt isolerad från USB-jord; kontakt med nätspänning leder spänningen direkt till kortet, USB-kabeln och datorn.
- **MW-03 (VARNING – Het givare, brännskador och brandrisk):** Givarens spets och mantel kan bli extremt heta (upp till `+1372 °C`) och förblir heta efter användning. Låt givaren svalna helt innan du vidrör den.
- **MW-04 (FÖRSIKTIGHET – Temperaturgränser för kort och kontakt):** Endast givarspetsen får placeras i den heta zonen. Håll kretskortet inom `−20 till +85 °C` och termoelementkontakten (`J2`/`J3`) inom `−50 till +120 °C`. Använd kablar som är högst `3 m` långa.
- **MW-05 (FÖRSIKTIGHET – Strömförsörjning):** Strömförsörj endast via USB 5 V (dator eller powerbank). Anslut inga andra spänningar till `VBUS`- eller `VSYS`-stiften.
- **MW-06 (FÖRSIKTIGHET – Öppet kretskort, ESD, barn och livsmedel):** Produkten är ingen leksak; förvaras oåtkomligt för barn. Ej för kontakt med livsmedel om inte själva givaren är godkänd för livsmedel. Hantera det oskyddade kortet i kanterna (ESD-känsligt).
- **Avfallshantering (WEEE):** Symbolen med en överkryssad soptunna på hjul innebär att produkten inte får slängas i hushållssoporna utan ska lämnas till separat elektronikåtervinning.

## Sources (what each section serves)
| Section | Rule | Markets |
|---------|------|---------|
| Product Identification | GPSR (EU) 2023/988 Art. 9(5); EMC 2014/30/EU Art. 7(5); RoHS 2011/65/EU Art. 7(g) | EU |
| Manufacturer and Contact | GPSR Art. 9(6); EMC Art. 7(6); RoHS Art. 7(h); Reg. (EU) 2019/1020 Art. 4 (economic operator established in the EU) | EU |
| Intended Use, Installation and Use | EMC Art. 18(1)-(3) | EU |
| Safety Information, Language Versions | GPSR Art. 9(7); EMC Art. 7(7) | EU |
| Disposal | WEEE 2012/19/EU Art. 14(2)(e), 14(4), Annex IX; EN 50419:2022 | EU |
| Conformity | CE: Reg. (EC) 765/2008 Art. 30; EMC Art. 15-17; RoHS Art. 7(c) | EU |
