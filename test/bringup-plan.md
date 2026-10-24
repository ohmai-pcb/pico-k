# Bring-up plan: pico-k rev-A

Results go into GitHub issues (one per finding, label `rev-B`), not into this file. Bench measurement cells below are marked `[awaiting board arrival]` until physical rev-A PCBs arrive and are tested on the bench.

## Equipment
- Programmable bench DC power supply with adjustable voltage (0–6 V) and current limit (10 mA–1 A)
- Digital multimeter (DMM, 4.5-digit DCV / resistance / continuity / diode mode)
- Oscilloscope (≥ 100 MHz bandwidth) with short probe ground spring for switching ripple and USB VBUS droop capture
- Thermal camera or calibrated reference thermometer + Type-K thermocouple probes:
  - 1 × ungrounded (insulated-junction) miniature Type-K probe (SMPW-K-M or equivalent flat-pin plug)
  - 1 × grounded-junction miniature Type-K probe (for `R-12` and `MW-01` verification)
  - Permanent magnet (to verify Alumel `−` magnetic leg vs Chromel `+` non-magnetic leg on `J3`/`J2`, `D-009` `P5-12`)
- Electronic load (or precision power resistors: 33 Ω 1 W for 100 mA and 11 Ω 2 W for 300 mA on `3V3`)
- Raspberry Pi Debug Probe (or CMSIS-DAP SWD probe) for bottom test pads `TP1` (`GND`), `TP2` (`SWCLK`), `TP3` (`SWDIO`)
- USB-C cables (short ≤ 0.5 m cable and 2 m cable), bus-powered USB 2.0 hub, laptop on battery, and USB 5 V powerbank

## 0. Before power
- [ ] **Visual and BOM inspection against `bom/bom.csv` and `out/release/rev-A/assembly-top.pdf`**:
  - Verify pin-1 and orientation of `U1` (`RP2350A` QFN-60), `U2` (`W25Q32RVXHJQ` XSON-8), `U3` (`TPS63001DRCR` VSON-10), `U4` (`USBLC6-2SC6` SOT-23-6), `U5` (`MAX31856MUD+T` TSSOP-14), `Q1` (`DMG1012T-7` SOT-523), `Y1` (`ABM8-272-T3`), `D1` (`MBR120VLSFT1G` cathode bar toward `VSYS`), and `D2` (`KT-0805G` cathode toward `GND`, `D-012`).
  - Record `L1` (`MPL-AT2512-3R3`) winding-start dot orientation: **Build A** (dot at `VREG_LX`, `U1.47`) vs **Build B** (dot at `DVDD`/`1V1`, `U1.46`/`U1.48`) (`D-007`, `D-009`).
  - Hand-solder `J2` (`T+`, right clip seen from sensor edge top-up) and `J3` (`T−`, left clip) from the `PCC-SMD-20` strip (`D-006 P4-5`, `D-009 P5-12`); measure shell tab protrusion on the bottom side of the 1.0 mm PCB for `J1` (`TYPE-C 16PIN 2MD(073)`, expected ≤ 0.21 mm, `D-006 P4-6`, `D-017 P8-4`) and `J2`/`J3` (`PCC-SMD`, expected ≈ 0.17 mm).
  - Verify `R6`, `R23`, `R24` are unpopulated (`DNF`), `JP1`–`JP4` (SPI1 `GP12`–`GP15`) and `JP5` (`VREG_FB`–`DVDD`) are bridged by default, and `JP6` (`VREG_FB`–`GND`) is open (`D-012`, `D-013`).
- [ ] **Resistance from each rail to `GND` (`TP1` / `J4.38`) before applying power** (DMM in high-ohms mode, red lead on rail, black lead on `GND`, allow ceramic caps to charge):
  - `VBUS` (`J4.40` to `GND`): expected ≈ `15.6 kΩ` (`R18` `5.6 kΩ` + `R8` `10 kΩ` `VBUS_SENSE` divider, plus `D1` forward path) — Measured: `[awaiting board arrival]`
  - `VSYS` (`J4.39` to `GND`): expected `> 50 kΩ` (`R15` `100 kΩ` to `3V3_EN`; `Q1` off when `3V3 = 0 V`) — Measured: `[awaiting board arrival]`
  - `3V3` (`J4.36` to `GND`): expected `> 10 kΩ` (no hard short; `U1`/`U2`/`U3`/`U5` unpowered high-Z) — Measured: `[awaiting board arrival]`
  - `DVDD` / `1V1` (`TP7` to `GND`): expected `> 1 kΩ` (no short across `C17`/`C28`/`C1`–`C3`/`U1` core) — Measured: `[awaiting board arrival]`
  - `ADC_VREF` (`J4.35` to `GND`) and `ADC_AVDD` (`C27`/`C32` to `GND`): expected `> 10 kΩ` (`201 Ω` to `3V3` via `R20`+`R21`) — Measured: `[awaiting board arrival]`

## 1. First power (current limited)
Apply DC power from the current-limited bench supply between `VSYS` (`J4.39`) and `GND` (`J4.38`) first, then test via `VBUS` (`J4.40` / `J1` USB-C) once the `TPS63001` (`U3`) and `RP2350A` (`U1`) core rails start cleanly.

| Step | Supply net & V | Current limit | Expected behavior & current | Measured | Pass? |
|------|----------------|---------------|-----------------------------|----------|-------|
| 1a | `VSYS = 2.5 V` (`J4.39`, ~50 % of 5 V nom; above `U3` 1.8 V UVLO, `SLVS520C` p.4) | `50 mA` | `U3` (`TPS63001`) starts in boost mode (`3V3 ≈ 3.30 V`), `U1` (`RP2350A`) boots to USB BOOTSEL idle (`DVDD ≈ 1.10 V`); expected `I_VSYS ≈ 10–35 mA`, no foldback | `[awaiting board arrival]` | `[awaiting board arrival]` |
| 1b | `VSYS = 1.80 V` (`J4.39`, min `VSYS` per `W-03` / Pico 2 §5.5) | `80 mA` | `U3` maintains `3V3 = 3.30 V ± 3 %` down to 1.80 V input; expected `I_VSYS ≈ 15–50 mA` | `[awaiting board arrival]` | `[awaiting board arrival]` |
| 1c | `VBUS = 5.00 V` (`J4.40` / `J1` USB-C) | `100 mA` | `D1` drops ≈ `0.25–0.34 V` (`VSYS ≈ 4.66–4.75 V`); `U3` runs in buck/PFM (`PS=0`) or PWM (`PS=1`); expected idle `I_VBUS ≈ 12–30 mA` (`docs/architecture.md` §A2-1) | `[awaiting board arrival]` | `[awaiting board arrival]` |

## 2. Rails
Measure DC voltage with DMM and peak-to-peak switching ripple with oscilloscope (20 MHz BW limit, 1× probe with short ground spring across the output decoupling capacitor). Test at `VBUS = 5.00 V` (USB powered) and with `SMPS_PS` (`GP23`, `TP4`) both Low (`PFM` power-save) and High (`PWM` low-ripple mode).

| Rail (Test point) | Expected DC range (min..max) | Measured DC | Expected ripple (mVpp max) | Measured ripple | Cite / Source | Pass? |
|-------------------|------------------------------|-------------|----------------------------|-----------------|---------------|-------|
| `VBUS` (`J4.40` / `C19`) | `4.50 V .. 5.50 V` (`5.0 V ± 10 %`) | `[awaiting board arrival]` | `≤ 100 mVpp` (host USB 5 V rail) | `[awaiting board arrival]` | `R-06`; Pico 2 datasheet §3.3 p.12 | `[awaiting board arrival]` |
| `VSYS` (`J4.39` / `C20`) | `4.16 V .. 5.25 V` (from USB via `D1` `MBR120VLSFT1G`, `Vf ≤ 0.34 V`; `1.80..5.50 V` external `W-03`) | `[awaiting board arrival]` | `≤ 50 mVpp` | `[awaiting board arrival]` | `docs/architecture.md` §A2-1; `MBR120VLSFT1G.pdf` p.2 | `[awaiting board arrival]` |
| `3V3` (`J4.36` / `C21`) | `3.20 V .. 3.40 V` (`3.30 V` typ; `3.26..3.36 V` in PWM mode `PS=1`) | `[awaiting board arrival]` | `≤ 30 mVpp` (`PWM`, `GP23=1`) / `≤ 80 mVpp` (`PFM`, `GP23=0`) | `[awaiting board arrival]` | `TPS63001DRCR.pdf` (`SLVS520C` p.5); `docs/architecture.md` §A2-1 | `[awaiting board arrival]` |
| `DVDD` / `1V1` (`TP7` / `C17`) | `1.045 V .. 1.155 V` (`1.10 V ± 5 %`) | `[awaiting board arrival]` | `≤ 40 mVpp` | `[awaiting board arrival]` | `RP2350A.pdf` §6.3 p.450–455 | `[awaiting board arrival]` |
| `VREG_AVDD` (`C18`) | `3.20 V .. 3.40 V` (`3V3` via `R5` `33 Ω`, `I ≈ 200 µA`, drop `≈ 6.6 mV`) | `[awaiting board arrival]` | `≤ 10 mVpp` (RC filtered, `fc ≈ 1.8 MHz`) | `[awaiting board arrival]` | Hardware design with RP2350 p.7 | `[awaiting board arrival]` |
| `ADC_VREF` / `ADC_AVDD` (`J4.35` / `C27`, `C32`) | `3.17 V .. 3.39 V` (`3V3` via `R20` `200 Ω` + `R21` `1 Ω`, drop `≈ 30 mV` at `150 µA`) | `[awaiting board arrival]` | `≤ 10 mVpp` (RC filtered by `R20` + `C27` `4.7 µF` + `C32` `100 nF`) | `[awaiting board arrival]` | Pico 2 datasheet §4.3 p.14; `D-009 P5-11`, `D-030` | `[awaiting board arrival]` |

## 2a. Phase 5 / 7 / 8 carry-over checks (`D-007` … `D-017`, `D-030`)
- [ ] **L1 orientation (`D-007`/`D-009`)**: on build A ("MPS dot at `VREG_LX`") and build B ("MPS dot at `VOUT`/`DVDD`") measure `DVDD` (`TP7`) DC offset, switching ripple, and load-step response (idle to dual-core active); keep the better orientation; if both fail, execute the external 1.1 V fallback below.
  - Result (Build A vs Build B `DVDD` ripple & offset): `[awaiting board arrival]`
- [ ] **External 1.1 V DVDD fallback (`D-012 P7-6`, `D-013`; RP2350 datasheet §6.3 p.451 text, Fig. 21 p.452)**. Only if both `L1` orientations fail. Off-board feed, no on-board regulator:
  1. Remove `L1`. Cut `JP5` (`VREG_FB`–`DVDD`, bridged by default). **Before bridging `JP6`, check with the meter that `JP5` is open (continuity `DVDD`/`TP7` to `VREG_FB` = open)**: `JP5` and `JP6` share `VREG_FB`, so `JP6` bridged with `JP5` intact shorts `DVDD` to `GND` (Reviewer-A F11). Then bridge `JP6` (`VREG_FB`–`GND`): "Connect `VREG_FB` directly to ground" (p.451).
  2. Keep `VREG_VIN` and `VREG_AVDD` powered (`3V3`), as Fig. 21 requires for power-on reset / brown-out (p.451).
  3. Feed `1.10 V` from a current-limited bench supply into `TP7` (`DVDD`) and `GND`. Supply sequencing versus `3V3` is not stated in §6.3: check the RP2350 power-sequencing text before the first fallback power-up.
  4. **Firmware:** the on-chip regulator still powers on with `VREG_VIN`/`VREG_AVDD` and draws ≈ 400 µA until shut down; the fallback firmware must write `1` to the `VREG` register's `HIZ` field early after reset (p.452). Record the firmware build used. Measure `3V3` current before/after the `HIZ` write (ESTIMATE: drop of ≈ 400 µA, p.452).
  5. Record `DVDD` at `TP7`, ripple, and that the board enumerates and runs the thermocouple read loop: `[awaiting board arrival]`
- [ ] **MAX31856 `DRDY`/`FAULT` drive type (`D-009 P5-9`)**: with `R23`/`R24` not fitted (`DNF`), check `TC_DRDY` (`TP11`) and `TC_FAULT` (`TP12`) in both logic states (`3.3 V` high level with no pull-up = push-pull CMOS output per `MAX31856` p.3 `VOH ≥ VDD − 0.4 V`); fit `R23`/`R24` (`10 kΩ`) only if open-drain.
  - Result (`TP11` `DRDY` / `TP12` `FAULT` high/low levels): `[awaiting board arrival]`
- [ ] **USB attach `VBUS` droop (`D-010`, documented deviation from USB 2.0 §7.2.4.1 p.177; target `≤ 330 mV` droop)**:
  - Setup: scope probe (ground spring) on `VBUS`–`GND` at the upstream port the board plugs into: a downstream port of a bus-powered USB 2.0 hub (worst case: hub fed from a laptop on battery, other ports loaded), and for comparison a laptop root port. Short USB-C cable as delivered with the board, then a 2 m cable. Note: `D-030` reduced `C20` from `1206` `50 V` to `0805` `25 V` (`CL21A106KAYNNNE`), reducing the `VSYS` effective capacitance and attach charge compared to `D-009`.
  - Trigger on the falling `VBUS` edge at the host side, `10 µs/div` then `1 ms/div`; 10 hot-plugs per setup, record the worst droop below the pre-attach `VBUS` level, the peak current, and whether any other device on the hub resets.
  - Pass criteria: droop `≤ 330 mV` and no other device on the hub disconnects.
  - If it fails: open a `rev-B` issue to add a slew-rate-controlled load switch between `VBUS` and `VSYS` (ramp `≥ 3 ms`) and change `C19` to `4.7 µF` (`CL10A475KO8NNNC`).
  - Result (worst `VBUS` droop across 10 hot-plugs): `[awaiting board arrival]`
- [ ] **Thermocouple polarity sanity checks (`D-009 P5-12`; polarity from Omega `PCC-SMD` p.2 drawing)**:
  - (1) Magnet test on the Type-K probe legs: the Alumel (`−`, red/negative) leg is magnetic, Chromel (`+`, yellow/positive) is non-magnetic; verify the magnetic Alumel (`−`) blade mates into `J3` (left clip seen from the sensor edge, component side up) and Chromel (`+`) mates into `J2` (right clip).
  - (2) Warm-tip test: warming the probe tip between fingers must increase the `MAX31856` linearized temperature (`LTCBH..L`).
  - Result (magnet + warm-tip polarity check): `[awaiting board arrival]`

## 3. Buses and firmware
- [ ] **Programming / SWD & USB-C BOOTSEL connection**:
  - Hold `SW1` (`BOOTSEL`) while plugging in USB-C (`J1`); verify `RP2350` enumerates as USB Mass Storage (`RP2350` UF2 drive) and flashes MicroPython for RP2350 cleanly.
  - Verify SWD debug attach on bottom test pads `TP1` (`GND`), `TP2` (`SWCLK`), `TP3` (`SWDIO`) (`D-002`).
  - Result: `[awaiting board arrival]`
- [ ] **SPI1 bus (`U5` `MAX31856MUD+T` on `GP12`=MISO, `GP13`=CS, `GP14`=SCK, `GP15`=MOSI via `JP1`–`JP4`)**:
  - Note: `pico-k` has no on-board I2C slave ICs (`I2C0`/`I2C1` on `J4` edge pins are free for user peripherals); the on-board peripheral bus is **SPI1** to `U5` (`MAX31856`, `D-004`).
  - Run the automated MicroPython self-test script over USB-C CDC serial:
    ```bash
    mpremote run test/firmware/bringup_selftest.py
    ```
  - Verify `MAX31856` `CR0` (`0x00`) writes/reads back `0x11` (50 Hz rejection, open-circuit detection enabled) and `CR1` (`0x01`) writes/reads back `0x33` (4-sample average, Type-K), cold-junction temperature (`CJTH`/`CJTL`) reads within `±0.7 °C` of ambient thermometer, and all 22 unshared edge GPIOs pass internal pull-up / pull-down toggling.
  - Result (`bringup_selftest.py` console output): `[awaiting board arrival]`

## 4. Load and thermal
Run each condition at ambient room temperature (`TA ≈ 20–25 °C`), measure peak component surface temperatures with thermal camera or reference thermocouple after thermal equilibrium, and verify against component ratings (`S3-7` / `parts/selection.md`) and `U5` cold-junction drift (`docs/architecture.md` §A2-3).

| Condition | Load on `3V3` (`J4.36`) | Duration | Hottest part | Measured Temp | Limit (source) | Pass? |
|-----------|-------------------------|----------|--------------|---------------|----------------|-------|
| Idle + TC polling (1 Hz) | `0 mA` external (`≈ 17 mA` board idle, `docs/architecture.md` §A2-1) | `15 min` | `U1` / `U3` / `U5` (`ΔT` from `U1`/`U3` to `U5`/`J2`/`J3`) | `[awaiting board arrival]` | Board `≤ 85 °C` (`Pico 2` §3.3 p.12); `U5`–`J2`/`J3` gradient `≤ 0.5 °C` (`R-11`/`R-13`) | `[awaiting board arrival]` |
| Nominal external load | `100 mA` (`33 Ω` on `3V3`, `VBUS = 5.0 V`) | `15 min` | `U3` (`TPS63001`) / `D1` (`MBR120VLSFT1G`) | `[awaiting board arrival]` | `TA ≤ 85 °C` (`SLVS520C` p.1), `TJ ≤ 125 °C` (`MBR120VLSFT1G` p.2) | `[awaiting board arrival]` |
| Rated max external load (`R-04`) | `300 mA` (`11 Ω` on `3V3`, `VBUS = 5.0 V`, `PS=1` PWM) | `15 min` | `U3` (`TPS63001`) / `L2` (`DFE201612P-2R2M`) / `D1` | `[awaiting board arrival]` | `3V3` stays `3.20..3.40 V`; `U3`/`L2`/`D1` `≤ 85 °C` surface (`Pico 2` p.9, `S3-7`) | `[awaiting board arrival]` |
| Low-`VSYS` boost corner (`W-03`) | `300 mA` on `3V3` with `VSYS = 1.80 V` (`I_VSYS ≈ 0.72 A`) | `10 min` | `U3` (`TPS63001`) / `L2` (`DFE201612P-2R2M`) | `[awaiting board arrival]` | `L2` `ΔT ≤ 40 °C` (`Itemp = 1.5 A`, `DFE201612P` p.2); `U3` no thermal shutdown | `[awaiting board arrival]` |

## 5. Functional tests (one per requirement `R-01` .. `R-16`)

| Req | Test procedure | Expected result | Measured | Pass? |
|-----|----------------|-----------------|----------|-------|
| `R-01` | Read RP2350A `SYSINFO_CHIP_ID` and `GITREF_RP2350` registers via `bringup_selftest.py` / SWD | Identifies `RP2350A` (`QFN-60`), dual Cortex-M33 @ 150 MHz, 520 KB SRAM | `[awaiting board arrival]` | `[awaiting board arrival]` |
| `R-02` | Measure PCB length, width, and thickness with digital calipers; verify `J1`/`J2`/`J3` overhang | `51.0 × 21.0 × 1.0 mm` (`±0.2 mm`), `J2`/`J3` inside outline (`D-004 F1`) | `[awaiting board arrival]` | `[awaiting board arrival]` |
| `R-03` | Place board on 1:1 Pico 2 footprint / standard `2 × 20` 2.54 mm breadboard header | All 40 pins align on 2.54 mm pitch (`15.24 mm` row spacing); 36 intermediate pins have 1.0 mm through-holes + castellations, 4 corner pins (`1, 20, 21, 40`) have castellations (`D-017 P8-2`) | `[awaiting board arrival]` | `[awaiting board arrival]` |
| `R-04` | Run `bringup_selftest.py` (`check_power_and_sense`, `check_led_and_bootsel`, `check_edge_gpios`) and probe `RUN` (`J4.30`), `3V3_EN` (`J4.37`), `ADC_VREF` (`J4.35`), `AGND` (`J4.33`), `GND`, `3V3`, `VSYS`, `VBUS` | All 26 edge GPIOs (`GP0`–`GP22`, `GP26`–`GP28`) + 4 internal GPIOs (`GP23` `SMPS_PS`, `GP24` `VBUS_SENSE`, `GP25` `LED`, `GP29` `VSYS/3`) and power/control pins match Pico 2 §3.1 | `[awaiting board arrival]` | `[awaiting board arrival]` |
| `R-05` | Inspect PCB for mounting holes and bottom test pads `TP1` (`GND`), `TP2` (`SWCLK`), `TP3` (`SWDIO`), `TP4`–`TP7`, `TP11`, `TP12` | 0 mounting holes (`D-017 P8-1`); SWD programming works via bottom test pads `TP1`–`TP3` (`D-002`) | `[awaiting board arrival]` | `[awaiting board arrival]` |
| `R-06` | Power `pico-k` over USB-C from (a) laptop USB port, (b) 5 V USB powerbank, and (c) bench supply swept `4.50 V .. 5.50 V` on `VBUS` | Stable operation, USB enumeration, and Type-K conversions across `VBUS = 4.50..5.50 V` (`5 V ± 10 %`) | `[awaiting board arrival]` | `[awaiting board arrival]` |
| `R-07` | Inspect top-side `J2`/`J3` (`PCC-SMD`) placement and bottom-side flatness on a flat surface | `J2`/`J3` mounted on top side at sensor edge opposite `J1`; no bottom components; shell tab tips `≤ 0.21 mm` (`D-006 P4-6`, `D-017 P8-4`) | `[awaiting board arrival]` | `[awaiting board arrival]` |
| `R-08` | Plug miniature Type-K thermocouple plug into `J2`/`J3` and run `bringup_selftest.py` | 1-channel Type-K probe seats firmly in `J2`/`J3`; `MAX31856` reports `PROBE_OK` (`SR = 0x00`) and live temperature | `[awaiting board arrival]` | `[awaiting board arrival]` |
| `R-09` | Read `MAX31856` (`U5`) default registers (`CR0=0x00`, `CR1=0x03`, `MASK=0xFF`) after power-on reset over SPI1 | Matches `MAX31856` datasheet Table 5 p.18 POR defaults | `[awaiting board arrival]` | `[awaiting board arrival]` |
| `R-10` | Test Type-K conversion across cold bath (`0 °C` ice bath), ambient (`25 °C`), boiling water (`100 °C`), and precision mV thermocouple simulator across `−200 °C` (`−5.891 mV`) to `+1372 °C` (`+54.886 mV`) | `MAX31856` linearized output (`LTCBH..L`) tracks full `−200 .. +1372 °C` range without saturation or false fault (`MAX31856` Table 1 p.12) | `[awaiting board arrival]` | `[awaiting board arrival]` |
| `R-11` | Compare `MAX31856` cold-junction (`CJTH..L`) and hot-junction (`LTCBH..L`) readings against calibrated reference thermometer at `0 °C`, `25 °C`, and `100 °C` | Cold-junction error within `±0.7 °C` and linearized TC error within `±0.15 %` FS (`MAX31856` p.1) | `[awaiting board arrival]` | `[awaiting board arrival]` |
| `R-12` | Test with (a) ungrounded (insulated-junction) Type-K probe and (b) grounded-junction Type-K probe (powered from powerbank / ungrounded laptop per `MW-01`) | Both probe types convert accurately with `SR = 0x00` (`D-001 Q5`, `D-004 A2-4`) | `[awaiting board arrival]` | `[awaiting board arrival]` |
| `R-13` | Log `MAX31856` internal cold-junction sensor (`CJTH..L`) against a reference sensor attached directly to `J2`/`J3` clips over 15 min idle run | `U5` internal CJC tracks `J2`/`J3` clip temperature closely via thermal copper coupling (`MAX31856` p.28) | `[awaiting board arrival]` | `[awaiting board arrival]` |
| `R-14` | Verify `GP12=MISO`, `GP13=CS`, `GP14=SCK`, `GP15=MOSI` silkscreen labels and `JP1`–`JP4` continuity; optionally test opening one jumper and re-bridging | Silkscreen clearly labels shared SPI1 pins; `JP1`–`JP4` connect `U5` by default and isolate `GP12`–`GP15` when cut (`D-001 Q6`, `D-004`) | `[awaiting board arrival]` | `[awaiting board arrival]` |
| `R-15` | Connect `J1` (`TYPE-C 16PIN 2MD(073)`) via USB-C-to-USB-C cable (both orientations) and USB-A-to-USB-C cable to host PC | `5.1 kΩ` `Rd` resistors (`R10`, `R11`) negotiate 5 V VBUS in both USB-C orientations; USB 2.0 Full-Speed (`12 Mbps`) CDC enumerates with 0 CRC errors | `[awaiting board arrival]` | `[awaiting board arrival]` |
| `R-16` | Run `mpremote run test/firmware/bringup_selftest.py` on the board's own `RP2350A` MCU under MicroPython | Reads and prints `CJ` and `TC` temperatures (`°C`) and fault byte (`SR`) over USB serial (`=== RESULT: PASS ===`) | `[awaiting board arrival]` | `[awaiting board arrival]` |
