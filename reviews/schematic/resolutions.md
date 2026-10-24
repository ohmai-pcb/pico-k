---
accepted_changes:
- files_hash: sha256:93f6c22fb2fd716cf941dc16c9adbee36ccc1ba8c3aba426abecf72a5afba0af
  by: owner
  reason: Phase 8 layout pin-swap and C32 /ADC_AVDD schematic updates per D-021, D-023,
    D-026, D-030
accepted_independence:
- gate: schematic
  reviewer: Reviewer-A
  level: 3
  files_hash: sha256:93f6c22fb2fd716cf941dc16c9adbee36ccc1ba8c3aba426abecf72a5afba0af
  by: owner
  owner: owner
  reason: 'owner decision (D-016): accept Reviewer-A level 3 for the phase 7 schematic
    gate'
  alternatives_tried:
  - 'level 1 (different vendor model): no different-vendor reviewer is set up in this
    environment'
  - 'level 2 (different model, same vendor): not set up in this environment; a cloud
    agent on a different model was possible, but the owner chose to accept Reviewer-A'
  ref: D-016
---
# Resolutions: phase `schematic` review findings

Resolution: `fixed` (Ref = commit hash), `accepted` (By = owner, Reason required), `answered` (questions)
`pending` (By = owner; an open owner decision), or `fixed-post-review` (Ref = commit; only for the
reviewer's own [nit] issues: the files they name may change after the review without re-verification).

Review: `reviews/schematic/reviewer-a.md`, Reviewer-A, 2026-10-15, files_hash 0616527e..., pass with should-fixes, 0 blockers.
Fixes in bcfdc1c (author, 2026-10-15), each checked against the cited page. F1-F3 change the files in scope, so
Reviewer-A must re-verify against a new brief (`ohmai review start schematic`). Questions F8/F9 (TP5 placement) and
F18 (KiCad app version pin) answered by the owner in D-014 (d389e6e). Notes in OK rows F21 (ABM8 orientation by pad
layout, CL cite p.1), F23 (TPS63001 ground split) and F24 (SW1 A/B pair) are tracked in STATUS P7-10 (bcfdc1c).

| ID | Reviewer | Resolution | Ref | By | Reason |
|----|----------|------------|-----|----|--------|
| F1 | Reviewer-A | fixed | bcfdc1c | author | Regulator: R15 (EN pull-up) moved 20.32 mm left of U3.6, so its VSYS symbol no longer sits under the R14/C15/VINA junction; VINA reads as its own node and R14 no longer looks shorted. Readability now FAILs a power name next to another node's junction or wire (OhmAI 1d15d99). |
| F2 | Reviewer-A | fixed | bcfdc1c | author | Source of F1: `regulator.yaml` R15 attach `at: [-20.32, 0]`, comment cites F1/F2. |
| F3 | Reviewer-A | fixed | bcfdc1c | author | mcu_core: C16/C29 (C_IN, VREG_VIN) and C17 (C_OUT, DVDD) wired to VREG_PGND at U1.47, joined to GND only through NT1 (RP2350 Fig. 22 p.453, single-point join p.454); C17 no longer among the DVDD caps; title 'RP2350 Fig. 22 + 21, HDG Fig. 10'. The KiCad RP2350A symbol has VREG_PGND on the bottom edge, opposite VREG_VIN/LX/FB, so the loop is drawn at pin 47 with 3V3/DVDD symbols on the cap tops; L1 and JP5/JP6 stay at the top pins. Re-verify, please. |
| F5 | Reviewer-A | fixed-post-review | bcfdc1c | author | expected_nets.csv header: crystal now cites HDG §4 Fig. 10 p.13 (same circuit in Fig. 15 p.20); brief note updated. |
| F6 | Reviewer-A | fixed-post-review | bcfdc1c | author | expected_nets.csv header: (1) TPS63001 typical application p.1, Table 1 p.10; (2) W25Q32RV §3.3 Pin Description p.5; (3) AGND tie cites Pico 2 datasheet §3.1 p.9, quoted, ESTIMATE removed. |
| F11 | Reviewer-A | fixed-post-review | bcfdc1c | author | bring-up §2a: check JP5 open (DVDD/TP7 to VREG_FB) before bridging JP6; STATUS P7-10: JP5 at C17, VREG_FB from C_OUT away from L1/VREG_LX (p.454), JP5/JP6 role silkscreen. |
| F12 | Reviewer-A | fixed-post-review | bcfdc1c | author | mcu_core reference figures: title "RP2350 Fig. 22 + 21, HDG Fig. 10"; header comment cites Fig. 22 p.453 for the regulator as drawn, Fig. 21 p.452 only for JP5/JP6, HDG Fig. 10 p.13 (Fig. 15 p.20) for the crystal. (Text corrected after Reviewer-A's re-verify: it first described the F3 C17 move.) |
| F13 | Reviewer-A | fixed-post-review | bcfdc1c | author | U2 ref/value moved off the pin-8 number; R4 text left of the R6 DNP cross; NT1 value hidden, VREG_PGND wired. Readability checks pin numbers, pin lines and DNP crosses (OhmAI 1d15d99). |
| F14 | Reviewer-A | fixed-post-review | bcfdc1c | author | power_usb: R11's GND moved 5.08 mm right of its value; thermocouple R24 route moved off R7's 3V3 (found by the new rule). |
| F15 | Reviewer-A | fixed-post-review | bcfdc1c | author | All sheet titles shortened to fit the title-block field; readability FAILs an overflowing title (OhmAI 1d15d99). |
| F16 | Reviewer-A | fixed-post-review | bcfdc1c | author | `power:GNDPWR` removed for VREG_PGND (_root.yaml); now a wired local net, with no chassis-ground symbol. OhmAI 5793dee resolves pin-name passives targets on such nets. |
| F17 | Reviewer-A | fixed-post-review | bcfdc1c | author | STATUS P7-10 and hardware/README empty-footprint list: J1, U1, U2, U3, U4, U5, L1, L2, Q1, J2, J3, J4. |
| F20 | Reviewer-A | fixed-post-review | bcfdc1c | author | STATUS P7-10: D2 cathode mark on silkscreen, CPL by the KT-0805G green cathode mark (p.2). |
| F8 | Reviewer-A | answered | d389e6e | owner | D-014 (owner, 2026-10-15). TP5 moved to LED_A (LED anode, between R22 and D2), as Pico 2 §3.1 p.9 / Fig. 11 p.20, test pads as Pico 2 (D-002). Drawn on sheet 6 at the D2 anode; expected_nets.csv updated. |
| F9 | Reviewer-A | answered | d389e6e | owner | D-014 (owner, 2026-10-15). Source of F8: TP5 removed from edge.yaml and added to led_boot_adc.yaml (nets 1: LED_A); edge.yaml comment points to sheet 6. |
| F18 | Reviewer-A | answered | d389e6e | owner | D-014 (owner, 2026-10-15). KiCad application pinned to 9.0.x: ohmai.yaml `kicad.app: ">=9.0.2,<9.1"`, checked by `ohmai check kicad-app` (OhmAI 9f48356; PASS, kicad-cli 9.0.2). |

Re-verification: Reviewer-A, files_hash a052ad17...bea, pass, no new findings (2026-10-15). Gate not approved: owner
decision pending on Reviewer-A's level-3 independence (gate minimum level 2).
Owner waiver D-016: Reviewer-A's level-3 independence (gate minimum level 2) accepted by the owner for this gate and
files_hash only (front matter `accepted_independence`); gate approved (D-016).
