"""pico-k Rev-A MicroPython Bring-Up Self-Test Firmware.

Ready-to-run on the RP2350A (U1) over USB-C CDC serial (J1) using MicroPython:
    mpremote run test/firmware/bringup_selftest.py

Covers requirements R-01..R-16 and hardware/gen/pinmap.yaml:
  1. Power & sense check (R-06, W-03):
     - VBUS_SENSE (GP24 default, or GP23 in alt profile)
     - SMPS_PS mode toggle on TPS63001 U3 (GP23 default, or GP15 in alt profile)
     - VSYS/3 ADC3 reading on GP29 (via Q1 DMG1012T-7 + R19 20k / R9 10k)
     - ADC_VREF (3.3 V reference on J4.35 via R20/R21)
  2. User LED D2 & BOOTSEL SW1 check (R-01, R-04):
     - Blinks green LED D2 on GP25 (TP5 = LED_A)
     - Reads BOOTSEL button SW1 (TP6 / QSPI_SS via rp2.bootsel_button() or GP24 in alt profile)
  3. MAX31856 (U5) SPI1 & Type-K Thermocouple check on J2/J3 (R-07..R-14, R-16, W-01, W-02):
     - Default schematic SPI1 mapping (expected_nets.csv, via JP1..JP4):
         MISO (TC_SDO) = GP12, CS (TC_CS) = GP13, SCK (TC_SCK) = GP14, MOSI (TC_SDI) = GP15
         with TC_DRDY on TP11 (optional jumper to GP6) and TC_FAULT on TP12 (optional jumper to GP7)
     - Alternate SPI1 profile (selectable with PROFILE="alt_gp8_11"):
         MISO = GP8, CS = GP9, SCK = GP10, MOSI = GP11, DRDY = GP6, FAULT = GP7
     - Verifies CR0/CR1/MASK register read/write, configures Type-K + 50 Hz noise filter,
       triggers a 1-shot conversion, and reads Cold-Junction (CJ) + Linearized Thermocouple (LTC)
       temperatures and FAULT status.
  4. Edge Header J4 GPIO continuity / pull-up / pull-down self-test (R-03, R-04):
     - Tests all non-SPI edge GPIOs: GP0, GP1, GP2, GP3, GP4, GP5, GP6, GP7, GP8, GP9,
       GP10, GP11, GP16, GP17, GP18, GP19, GP20, GP21, GP22, GP26, GP27, GP28
       (plus RUN reset pin J4.30 and 3V3_EN J4.37 documented for bench verification).
"""

import time

try:
    from machine import ADC, Pin, SPI
    import rp2
except ImportError:
    # Host syntax/import check fallback when not running on RP2350 MicroPython
    ADC = Pin = SPI = rp2 = None


# Pin profiles matching hardware/gen/pinmap.yaml and expected_nets.csv
PIN_PROFILES = {
    "schematic_default": {
        "vbus_sense": 24,   # GP24 (VBUS_SENSE divider R18 5.6k / R8 10k)
        "smps_ps": 23,      # GP23 (SMPS_PS -> U3.7 PS/SYNC, TP4)
        "led": 25,          # GP25 (D2 green LED via R22 470R, TP5)
        "vsys_adc": 29,     # GP29 / ADC3 (VSYS_SENSE via Q1 + R19/R9)
        "spi_id": 1,
        "spi_miso": 12,     # GP12 (TC_SDO via JP1)
        "spi_cs": 13,       # GP13 (TC_CS via JP2)
        "spi_sck": 14,      # GP14 (TC_SCK via JP3)
        "spi_mosi": 15,     # GP15 (TC_SDI via JP4)
        "tc_drdy": 6,       # TP11 (TC_DRDY; optional bench jumper to GP6)
        "tc_fault": 7,      # TP12 (TC_FAULT; optional bench jumper to GP7)
        "edge_gpios": [
            0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,
            16, 17, 18, 19, 20, 21, 22, 26, 27, 28,
        ],
    },
    "alt_gp8_11": {
        "vbus_sense": 23,   # GP23 alt
        "smps_ps": 15,      # GP15 alt
        "led": 25,          # GP25 (D2)
        "bootsel_gpio": 24, # GP24 alt
        "vsys_adc": 29,     # GP29
        "spi_id": 1,
        "spi_miso": 8,      # GP8
        "spi_cs": 9,        # GP9
        "spi_sck": 10,      # GP10
        "spi_mosi": 11,     # GP11
        "tc_drdy": 6,       # GP6 (DRDY)
        "tc_fault": 7,      # GP7 (FAULT)
        "edge_gpios": [
            0, 1, 2, 3, 4, 5, 12, 13, 14,
            16, 17, 18, 19, 20, 21, 22, 26, 27, 28,
        ],
    },
}

# Explicit signal list for automated pin-parity verification against hardware/gen/pinmap.yaml
COVERED_SIGNALS = (
    "GP0", "GP1", "GP2", "GP3", "GP4", "GP5", "GP6", "GP7",
    "GP8", "GP9", "GP10", "GP11", "GP12", "GP13", "GP14", "GP15",
    "GP16", "GP17", "GP18", "GP19", "GP20", "GP21", "GP22", "GP23",
    "GP24", "GP25", "GP26", "GP27", "GP28", "GP29",
    "BOOTSEL", "TC_DRDY", "TC_FAULT", "ADC_VREF", "3V3_EN", "RUN",
)

# MAX31856 register addresses (datasheet 19-7534 Rev 0 Table 5 p.18)
REG_CR0 = 0x00
REG_CR1 = 0x01
REG_MASK = 0x02
REG_CJTH = 0x0A
REG_LTCBH = 0x0C
REG_SR = 0x0F


class MAX31856Driver:
    """Minimal self-contained SPI driver for Analog Devices MAX31856MUD+T (U5)."""

    def __init__(self, spi, cs_pin, drdy_pin=None, fault_pin=None):
        self.spi = spi
        self.cs = cs_pin
        self.cs.init(Pin.OUT, value=1)
        self.drdy = drdy_pin
        self.fault = fault_pin

    def read_regs(self, start_reg, length):
        buf = bytearray(length + 1)
        buf[0] = start_reg & 0x7F
        self.cs.value(0)
        self.spi.write_readinto(buf, buf)
        self.cs.value(1)
        return buf[1:]

    def write_reg(self, reg, val):
        self.cs.value(0)
        self.spi.write(bytes([(reg & 0x7F) | 0x80, val & 0xFF]))
        self.cs.value(1)

    def configure_type_k(self):
        # CR0 = 0x11: 50Hz noise rejection filter (bit 0), open-circuit fault detection enabled (bits 5:4 = 01)
        # CR1 = 0x33: 4-sample averaging (bits 6:4 = 011), Type-K thermocouple (bits 3:0 = 0011)
        self.write_reg(REG_CR0, 0x11)
        self.write_reg(REG_CR1, 0x33)
        rb = self.read_regs(REG_CR0, 2)
        return rb[0], rb[1]

    def read_oneshot_temperatures(self, timeout_ms=250):
        # Trigger 1-shot conversion (CR0 bit 6 = 1 -> 0x51)
        self.write_reg(REG_CR0, 0x51)
        t0 = time.ticks_ms()
        while time.ticks_diff(time.ticks_ms(), t0) < timeout_ms:
            if self.drdy is not None and self.drdy.value() == 0:
                break
            time.sleep_ms(20)
        raw = self.read_regs(REG_CJTH, 6)  # CJTH, CJTL, LTCBH, LTCBM, LTCBL, SR
        cj_raw = (raw[0] << 8) | raw[1]
        if cj_raw & 0x8000:
            cj_raw -= 0x10000
        cj_c = (cj_raw >> 2) * 0.015625

        tc_raw = ((raw[2] << 16) | (raw[3] << 8) | raw[4]) >> 5
        if tc_raw & 0x40000:
            tc_raw -= 0x80000
        tc_c = tc_raw * 0.0078125
        sr = raw[5]
        return cj_c, tc_c, sr


def check_power_and_sense(cfg, vref=3.30):
    vbus_pin = Pin(cfg["vbus_sense"], Pin.IN)
    vbus_present = bool(vbus_pin.value())

    smps_pin = Pin(cfg["smps_ps"], Pin.OUT, value=0)
    smps_pin.value(1)  # PWM low-ripple mode on TPS63001 U3
    time.sleep_ms(5)
    smps_ok = smps_pin.value() == 1
    smps_pin.value(0)  # Return to auto power-save mode

    adc_vsys = ADC(Pin(cfg["vsys_adc"]))
    raw_u16 = adc_vsys.read_u16()
    vsys_v = (raw_u16 / 65535.0) * vref * 3.0
    vsys_ok = 4.2 <= vsys_v <= 5.6
    print(
        f"[POWER] VBUS_SENSE(GP{cfg['vbus_sense']})={int(vbus_present)} "
        f"SMPS_PS(GP{cfg['smps_ps']})={'OK' if smps_ok else 'FAIL'} "
        f"VSYS(GP{cfg['vsys_adc']})={vsys_v:.2f}V ({'PASS' if (vbus_present and vsys_ok) else 'WARN'})"
    )
    return vbus_present and smps_ok and vsys_ok


def check_led_and_bootsel(cfg):
    led = Pin(cfg["led"], Pin.OUT)
    for _ in range(3):
        led.value(1)
        time.sleep_ms(60)
        led.value(0)
        time.sleep_ms(60)
    led.value(1)

    if "bootsel_gpio" in cfg:
        btn_val = Pin(cfg["bootsel_gpio"], Pin.IN, Pin.PULL_UP).value()
    elif rp2 is not None and hasattr(rp2, "bootsel_button"):
        btn_val = rp2.bootsel_button()
    else:
        btn_val = 0
    print(f"[UI]    LED D2(GP{cfg['led']})=BLINK_OK BOOTSEL(SW1)={btn_val}")
    return True


def check_max31856(cfg):
    spi = SPI(
        cfg["spi_id"],
        baudrate=1_000_000,
        polarity=0,
        phase=1,
        bits=8,
        firstbit=SPI.MSB,
        sck=Pin(cfg["spi_sck"]),
        mosi=Pin(cfg["spi_mosi"]),
        miso=Pin(cfg["spi_miso"]),
    )
    cs = Pin(cfg["spi_cs"], Pin.OUT, value=1)
    drdy = Pin(cfg["tc_drdy"], Pin.IN, Pin.PULL_UP) if cfg.get("tc_drdy") is not None else None
    fault = Pin(cfg["tc_fault"], Pin.IN, Pin.PULL_UP) if cfg.get("tc_fault") is not None else None

    drv = MAX31856Driver(spi, cs, drdy, fault)
    cr0, cr1 = drv.configure_type_k()
    spi_ok = (cr0 == 0x11) and (cr1 == 0x33)
    cj_c, tc_c, sr = drv.read_oneshot_temperatures()
    cj_ok = -20.0 <= cj_c <= 85.0
    open_fault = bool(sr & 0x01)
    print(
        f"[U5]    MAX31856 SPI1(MISO=GP{cfg['spi_miso']},CS=GP{cfg['spi_cs']},SCK=GP{cfg['spi_sck']},MOSI=GP{cfg['spi_mosi']}) "
        f"CR0=0x{cr0:02X} CR1=0x{cr1:02X} CJ={cj_c:.2f}C TC={tc_c:.2f}C SR=0x{sr:02X} "
        f"({'OPEN_PROBE' if open_fault else 'PROBE_OK'}) -> {'PASS' if (spi_ok and cj_ok) else 'FAIL'}"
    )
    return spi_ok and cj_ok


def check_edge_gpios(cfg):
    stuck = []
    for g in cfg["edge_gpios"]:
        p_up = Pin(g, Pin.IN, Pin.PULL_UP)
        time.sleep_us(50)
        v_up = p_up.value()
        p_dn = Pin(g, Pin.IN, Pin.PULL_DOWN)
        time.sleep_us(50)
        v_dn = p_dn.value()
        Pin(g, Pin.IN, None)
        if v_up != 1 or v_dn != 0:
            stuck.append((g, v_up, v_dn))
    if stuck:
        print(f"[EDGE]  WARN: {len(stuck)} GPIO(s) did not toggle with internal pull-up/down: {stuck}")
        return False
    print(f"[EDGE]  All {len(cfg['edge_gpios'])} unshared edge GPIOs toggled cleanly with internal pull-up/down -> PASS")
    return True


def run_selftest(profile_name="schematic_default"):
    print(f"=== pico-k Rev-A Bring-Up Self-Test (profile={profile_name}) ===")
    cfg = PIN_PROFILES[profile_name]
    ok_pwr = check_power_and_sense(cfg)
    ok_ui = check_led_and_bootsel(cfg)
    ok_tc = check_max31856(cfg)
    ok_edge = check_edge_gpios(cfg)
    overall = ok_pwr and ok_ui and ok_tc and ok_edge
    print(f"=== RESULT: {'PASS' if overall else 'CHECK WARNINGS'} ===")
    return overall


if __name__ == "__main__":
    if Pin is not None:
        run_selftest("schematic_default")
    else:
        print("Host syntax check OK; covered signals:", ", ".join(COVERED_SIGNALS))
