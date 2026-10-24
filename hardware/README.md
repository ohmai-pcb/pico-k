# hardware/

KiCad 9 project: `pico-k.kicad_pro`, `.kicad_sch` (root sheet), `.kicad_pcb`.

- Phase 7: the root sheet holds only hierarchical sheets, **one functional block per sheet**
  (`power_in.kicad_sch`, `regulator.kicad_sch`, ...).
- Symbols and footprints come from KiCad's official libraries or `lib/` (project library, reviewed
  in a PR). Never generate them.
- Put each part's MPN in a symbol field named `MPN` so checks can match `parts/constraints/`.
- Phase 8: fab design rules go in `pico-k.kicad_dru` (fab capabilities plus creepage from `docs/safety.md`).
- `release.kibot.yaml` holds the KiBot outputs for tagged releases (CI only).

## Phase 7 notes (2026-10-15, D-012)
- Libraries: official KiCad **9.0.9.1** symbols and footprints, pinned in `ohmai.yaml` (`kicad.libraries`), installed
  with `ohmai kicad-libs install` and referenced through the project tables `sym-lib-table` / `fp-lib-table`
  (`${OHMAI_KICAD_SYMBOLS}` / `${OHMAI_KICAD_FOOTPRINTS}`, written by `ohmai kicad-libs tables`). Symbols are embedded
  verbatim; ERC reports no `lib_symbol_issues`.
- Source of the sheets: `gen/layout/_root.yaml` + one yaml per block (power_usb, mcu_core, regulator, thermocouple,
  edge, led_boot_adc), drawn by `ohmai schematic build` in datasheet-figure style (real wires; hierarchical labels
  only between blocks). Each yaml names its reference figure. Do not hand-edit the .kicad_sch files while the
  generator is the source; change the yaml and rebuild. The old `gen/*.py` draft generator is retired.
- Library pins that differ from the datasheet are mapped in `../parts/symbol-maps/` (the reviewed constraints are
  not edited).
- Footprints left empty on purpose (phase 8, STATUS P7-10): J1, U1, U2, U3, U4, U5, L1, L2, Q1, J2/J3 (Omega PCC-SMD
  custom footprint), J4.
- VREG_PGND is a wired net (no power symbol): C16/C29/C17 returns at U1 pin 47, joined to GND only through NT1.
