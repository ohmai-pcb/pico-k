# EVB comparison: W25Q32RVXHJQ (U2, sheet `mcu_core`)
Reference: Hardware design with RP2350 Minimal Design, Appendix A Fig. 15 (p.20) (W25Q128JVS, C2 100 nF) and
Pico 2 W schematic RP-008306 (W25Q32RVXHJQ).

| Vendor ref | Function | Vendor value / MPN | Ours | Same? | Reason if different (cite) |
|------------|----------|--------------------|------|-------|----------------------------|
| U3 | QSPI flash | W25Q128JVS / W25Q32RVXHJQ (Pico 2 W) | U2 W25Q32RVXHJQ | yes (Pico 2 W) | D-006 |
| C2 | VCC decoupling | 100 nF | C11 100 nF | yes | HDG p.20 |
| CS pull-up | QSPI_SS to 3V3 | 10 kΩ DNF | R6 10 kΩ DNF | yes | HDG p.10; fit with GD25Q32E (D-006) |
| EP | centre pad | - | U2.9 to GND | choice | W25Q32RV §10.3 p.77: floating or GND |
| symbol | - | - | official `Memory_Flash:W25Q32JVZP` (same pinout family), MPN field W25Q32RVXHJQ | owner check | STATUS P7-2 |
