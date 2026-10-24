# `pico-k` Bring-Up Self-Test Firmware

Ready-to-run MicroPython bring-up test script (`bringup_selftest.py`) for `pico-k` Rev-A (`RP2350A` `U1` + `MAX31856MUD+T` `U5` + `TPS63001DRCR` `U3`). No firmware needs to be written during bench bring-up.

## Quick Start

1. Flash standard Raspberry Pi Pico 2 (RP2350A) MicroPython UF2 onto `pico-k` by holding `BOOTSEL` (`SW1`) while plugging in USB-C (`J1`).
2. Run the self-test directly from the host without modifying flash:
   ```bash
   mpremote run test/firmware/bringup_selftest.py
   ```

## Pin Mapping & Requirement Coverage (`hardware/gen/pinmap.yaml`)

| Subsystem | Signal / Pin | Net / Ref | Requirement | Verification in `bringup_selftest.py` |
|-----------|--------------|-----------|-------------|---------------------------------------|
| USB & 3V3 rail | `VBUS`, `VSYS`, `3V3`, `DVDD`, `GND`, `3V3_EN`, `RUN` | `J1`, `U3`, `L1`, `J4.30`, `J4.36..40` | R-01, R-04, R-06, W-03 | Bench DMM check + on-chip `VBUS_SENSE` / `VSYS_SENSE` |
| VBUS sense | `GP24` (alt `GP23`) | `VBUS_SENSE` (`R18`/`R8`) | R-04, R-06 | Reads digital HIGH when powered from USB-C `J1` |
| SMPS mode | `GP23` (alt `GP15`) | `SMPS_PS` (`U3.7`, `TP4`) | R-04, W-03 | Toggles `TPS63001` power-save / PWM mode |
| VSYS/3 sense | `GP29` (`ADC3`) + `ADC_VREF` | `VSYS_SENSE` (`Q1`, `R19`/`R9`, `R20`/`R21`) | R-04, W-03 | Reads `ADC3` and checks `4.2 V <= VSYS <= 5.6 V` |
| User LED | `GP25` | `LED_A` (`D2`, `R22`, `TP5`) | R-01, R-04 | Blinks green LED `D2` 3 times and leaves it ON |
| Boot button | `BOOTSEL` (alt `GP24`) | `BOOTSEL` (`SW1`, `TP6`, `R4`) | R-01, R-04 | Reads `SW1` state via `rp2.bootsel_button()` |
| Thermocouple SPI1 | `GP12` (`TC_SDO`), `GP13` (`TC_CS`), `GP14` (`TC_SCK`), `GP15` (`TC_SDI`) (or alt `GP8..GP11`) | `JP1..JP4`, `U5`, `J2`/`J3` | R-07..R-14, R-16, W-01, W-02 | Verifies `CR0`/`CR1` SPI loopback (`0x11`/`0x33`), reads Cold-Junction & Type-K temperature, and reports `SR` fault bits |
| Thermocouple status | `TC_DRDY` (`TP11` / opt `GP6`), `TC_FAULT` (`TP12` / opt `GP7`) | `U5.7`, `U5.13` | R-09, W-01 | Polls `DRDY` / `FAULT` when jumpered to `GP6`/`GP7` or via status register `SR` |
| Edge Header `J4` | `GP0..GP11`, `GP16..GP22`, `GP26..GP28` | `J4` castellations | R-03, R-04 | Internal pull-up / pull-down toggle check on every unshared GPIO |
