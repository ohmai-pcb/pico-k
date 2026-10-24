# EVB comparison: TS-1187A-B-A-B (SW1, sheet `led_boot_adc`)
Reference: Hardware design with RP2350 Minimal Design, §3.1 Fig. 8 (p.10): USB_BOOT switch between the 1 kΩ
from QSPI_SS and GND.

| Vendor ref | Function | Vendor value / MPN | Ours | Same? | Reason if different (cite) |
|------------|----------|--------------------|------|-------|----------------------------|
| SW | BOOTSEL to GND | push button | SW1 TS-1187A-B-A-B: BOOTSEL net → GND | yes | HDG p.10 |
| R (1 kΩ) | QSPI_SS → switch | 1 kΩ | R4 1 kΩ (sheet `mcu_core`, next to the flash) | yes | HDG p.10-11 |
| TP6 | BOOTSEL pad | Pico 2 TP6 | TP6 on BOOTSEL | yes | Pico 2 datasheet §3.1 p.9 |
