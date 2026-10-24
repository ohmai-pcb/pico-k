# Layout retro notes

## Fit check ignored pads (D-029 replan, 2026-10-23)
- **What happened:** `ohmai layout fit REF --ignore J4` was used because J4's castellated-edge courtyard always overlaps the edge parts. `--ignore` dropped J4 entirely, pads included, and the fit check had never compared pad copper anyway. So the replan's C18/C27 spots "fit" but shorted J4.31/J4.32, with mask bridges. This was only found when the plan was executed.
- **Fix:** OhmAI 4ec69a8 adds `--ignore-courtyard REF`, which skips the courtyard but still counts the pads. It also adds a pad-copper check: pads of other nets within `--pad-gap` (0.1 mm by default) on a shared copper layer.
- **Lesson:** "fits" means fits by the tool's model, not by DRC. Before a placement goes into a plan, rebuild a temporary board with every move applied and run a real `kicad-cli pcb drc`: 0 shorts, 0 mask bridges, no new courtyard or clearance errors. Then restore the board. Ignore only what you mean to ignore: a courtyard, never the copper.
- **Also:** OhmAI's loader reads J4's courtyard as one bounding box over both edge strips (99.755–121.245), so without the ignore everything near J4 looks blocked. KiCad's real east strip starts at x=118.345. Trust DRC for the J4 courtyard.

## L1 deferral (D-029, 2026-10-23)
- **What happened:** four tries to bring C20 to U3 VIN all failed. A placement that "fits" (corrected fit plus bare DRC) did not route: the rip step in one process left stale GND/3V3/VSYS copper (50 shorts), and one manual link clashed with GND.
- **Lesson:** budget for a corner re-placement and plan its routing before committing to it. Moving U3 by 90° moves every link of the regulator. Plan the rip list from a net-wise diff, rip whole nets (including the pour feeds), and dry-run the manual links on the ripped board before the one allowed try.
- **Lesson:** keep the reviewed board as the fallback until the fix is fully clean. A restore keeps files_hash, so the review and its waiver (D-028) stay valid.

## Project-level 3D `.step` model fetching and missing-model dummy STEP blocks (2026-10-24, owner decision)
- **What happened:** `ohmai kicad-libs install` installs only KiCad symbol libraries (`kicad-symbols`) and footprint libraries (`kicad-footprints`) into shared storage (`$OHMAI_KICAD_LIBS`), not `kicad-packages3D` (whose full archive exceeds 5 GB). Consequently, `kicad-cli pcb render` initially rendered `docs/layout/routed-3d.png` and `docs/layout/placement-3d.png` without 3D component bodies. Furthermore, 4 official KiCad footprints (`U1`, `U3`, `Q1`, `SW1`) reference `${KICAD9_3DMODEL_DIR}/...` paths that return HTTP 404 in upstream `kicad-packages3D@9.0.9.1`, and 5 custom `pico-k:` component footprints (`J1`, `J2`, `J3`, `L1`, `L2`) had no `(model ...)` entry.
- **Owner design decision:**
  1. **Fetch 3D `.step` models only at the project level** (`<project>/out/3dmodels/`, gitignored via `out/`, with `KICAD9_3DMODEL_DIR` pointed at `<project>/out/3dmodels` by `ohmai.kicadlibs.activate(project)`) for only the footprints actually used on that project's PCB, so shared storage (`$OHMAI_KICAD_LIBS`) does not grow fast.
  2. **Flag missing 3D models and generate parametric dummy `.step` blocks**: `ohmai kicad-libs models` (in `ohmai/models3d.py`) inspects every footprint in `project.pcb`, downloads available official `.step` files from `https://gitlab.com/kicad/libraries/kicad-packages3D/-/raw/<tag>/<rel_path>`, flags any physical component footprint whose 3D model is missing (`missing_upstream_step` for HTTP 404 in `kicad-packages3D`, or `missing_model_entry` for custom footprints without `(model ...)`), and generates a valid ISO-10303-21 STEP AP214 colored bounding-box solid (`MANIFOLD_SOLID_BREP` with `FACE_OUTER_BOUND`) from the footprint's `F.Fab` / `F.CrtYd` X×Y outline and the part's Z height constraint (`parts/constraints/*.yaml`, `bom/bom.csv`, or package family).
  3. **Non-destructive PCB staging (`--stage-pcb`)**: when `hardware/<project>.kicad_pcb` is locked by a review `files_hash`, `ohmai kicad-libs models --stage-pcb out/<project>-3d.kicad_pcb` injects `(model ...)` references for custom footprints into a temporary copy for 3D rendering without altering `hardware/<project>.kicad_pcb`.
- **`pico-k` 3D model summary (`out/3dmodels/`, total 795,113 B = ~776 KB across 19 `.step` files for all 69 physical BOM components):**
  - **10 official KiCad `9.0.9.1` `.step` files fetched (60 component instances, 743,730 B total):**
    - `Capacitor_SMD.3dshapes/C_0402_1005Metric.step` (43,502 B) — 22 refs (`C1`–`C15`, `C18`, `C23`–`C27`, `C32`)
    - `Capacitor_SMD.3dshapes/C_0603_1608Metric.step` (43,450 B) — 8 refs (`C16`, `C17`, `C19`, `C21`, `C22`, `C28`, `C29`, `C31`)
    - `Capacitor_SMD.3dshapes/C_0805_2012Metric.step` (43,618 B) — 1 ref (`C20`)
    - `Crystal.3dshapes/Crystal_SMD_3225-4Pin_3.2x2.5mm.step` (44,789 B) — 1 ref (`Y1`)
    - `Diode_SMD.3dshapes/D_SOD-123F.step` (42,604 B) — 1 ref (`D1`)
    - `LED_SMD.3dshapes/LED_0805_2012Metric.step` (78,220 B) — 1 ref (`D2`)
    - `Package_SO.3dshapes/TSSOP-14_4.4x5mm_P0.65mm.step` (198,789 B) — 1 ref (`U5`, MAX31856MUD+)
    - `Package_SON.3dshapes/Winbond_USON-8-1EP_3x2mm_P0.5mm_EP0.2x1.6mm.step` (108,363 B) — 1 ref (`U2`, W25Q32RVXHJQ)
    - `Package_TO_SOT_SMD.3dshapes/SOT-23-6.step` (99,639 B) — 1 ref (`U4`, USBLC6-2SC6)
    - `Resistor_SMD.3dshapes/R_0402_1005Metric.step` (40,756 B) — 23 refs (`R1`–`R16`, `R18`–`R24`)
  - **9 footprints flagged missing and rendered with generated STEP AP214 dummy blocks (9 component instances, 51,383 B total):**
    - `U1` (`Package_DFN_QFN:QFN-60-1EP_7x7mm_P0.4mm_EP3.4x3.4mm_ThermalVias`, RP2350A) — `missing_upstream_step` (404 in `kicad-packages3D@9.0.9.1`) -> dummy block **7.00 × 7.00 × 0.90 mm**
    - `U3` (`Package_SON:Texas_DRC0010J_ThermalVias`, TPS63001DRCR) — `missing_upstream_step` (404 in `kicad-packages3D@9.0.9.1`) -> dummy block **3.00 × 3.00 × 1.00 mm**
    - `Q1` (`Package_TO_SOT_SMD:SOT-523`, DMG1012T-7) — `missing_upstream_step` (404 in `kicad-packages3D@9.0.9.1`) -> dummy block **0.80 × 1.60 × 0.65 mm**
    - `SW1` (`Button_Switch_SMD:SW_Push_1P1T_XKB_TS-1187A`, TS-1187A-B-A-B) — `missing_upstream_step` (404 in `kicad-packages3D@9.0.9.1`) -> dummy block **6.50 × 5.10 × 1.60 mm**
    - `J1` (`pico-k:USB_C_Receptacle_ShouHan_TYPE-C-16PIN-2MD-073`, TYPE-C 16PIN 2MD(073)) — `missing_model_entry` (custom footprint) -> dummy block **8.94 × 7.30 × 3.16 mm**
    - `J2` (`pico-k:Omega_PCC-SMD_Clip_R`, PCC-SMD T+ clip) — `missing_model_entry` (custom footprint) -> dummy block **5.61 × 11.94 × 2.37 mm**
    - `J3` (`pico-k:Omega_PCC-SMD_Clip_L`, PCC-SMD T- clip) — `missing_model_entry` (custom footprint) -> dummy block **5.61 × 11.94 × 2.37 mm**
    - `L1` (`pico-k:L_MPS_MPL-AT2512`, MPL-AT2512-3R3) — `missing_model_entry` (custom footprint) -> dummy block **2.50 × 2.00 × 1.20 mm**
    - `L2` (`pico-k:L_Murata_DFE201612P`, DFE201612P-2R2M) — `missing_model_entry` (custom footprint) -> dummy block **2.00 × 1.60 × 1.20 mm**
  - **20 bare-copper PCB features skipped (0 mm height, non-BOM):** `J4` (2×20 castellated edge), `TP1`–`TP12` (12 test points), `JP1`–`JP6` (6 solder jumpers), `NT1` (1 net tie).

---

## Full Workflow & Tool Retrospective: Root-Cause Analysis & Proposed Improvements (2026-10-24)

### Why `pico-k` Took So Long and So Many Tries (Root Causes Across Phases 4–8)

Across `pico-k`, Phase 8 (`phase/layout`) alone accumulated **31 commits** and **13 formal owner/layout decisions (`D-018` through `D-030`)**, plus two full external review rounds with Reviewer-A (`L1`–`L13`, `Q3`). Tracing every stall and rework loop back to its root cause shows 7 systemic bottlenecks in the OhmAI workflow and CLI tools:

1. **Over-strict BOM lock on simple passives (`D-007`, `D-008`, `D-009`, `D-024`, `D-025`, `D-030`):**
   - Because the workflow rule treated *any* BOM edit after Phase 4/5 as requiring an explicit owner decision (`D-xxx`), the agent had to stop and ask the owner four separate times just to:
     - Swap `R23`/`R24` and `C1`/`C2` values in Phase 5 (`D-007`, `D-008`),
     - Add a standard 100 nF 0402 HF decoupling cap `C32` on `ADC_AVDD` when Schematic review flagged it (`D-009`),
     - Shrink `L2` from 3.0×3.0 mm unshielded (`LQH3NPN2R2MMEL`) to 2.0×1.6 mm metal-alloy shielded (`DFE201612P-2R2M`) and `C20` from 1206 to 0805 (`D-025`),
     - Shrink `C18`/`C27` from 0603 to 0402 (`D-030`).
   - Worse, *before* asking for `D-025` and `D-030`, the agent spent dozens of placement and routing iterations trying to force oversized 1206/0603/3030 passives into a 21×51 mm board with 15.0 mm free width between castellated strips.

2. **All-at-once courtyard-only placement (`placement != routability`) & `--ignore J4` blind spot (`D-018`, `D-020`, `D-022`, `D-027`, `D-029`, `D-030`):**
   - All 89 footprints were placed in one shot checking only courtyard boxes (`ohmai layout fit`), and because `J4` (`pico-k:RPi_Pico_Castellated_2x20`) had a two-strip courtyard parsed as a single full-width bounding box (`x = 99.755..121.245`), `--ignore J4` was passed—which ignored `J4`'s copper pads too (`D-029`, causing a 0.75 mm shift fiasco that shorted `J4.31`/`J4.32`).
   - Placing all 89 parts before testing escape fanout or critical hot loops meant that routing failures (`U1` trapped pins, `U4` blocking the `J1` `VBUS`/`CC` corridor, `C20` 4.23 mm from `U3.5 VIN`, `L2` sitting over `F.Cu` traces) were only discovered **after** hours of routing or during the external review gate.

3. **No machine check for datasheet hot-loop distances & under-body keepouts at placement time (`L1`–`L13` in Reviewer-A review):**
   - Datasheet layout rules were captured as prose in `parts/constraints/*.yaml` during Phase 5, not as machine-checkable pad-to-pad distance or keepout assertions.
   - As a result, `C20` (`U3` `VIN` cap at 4.23 mm pad-to-pad, `L1`), `C18` (`U1.45` `IOVDD` cap at 13.7 mm, `L2`), `C27` (`U5` `AVDD` cap at 7.45 mm, `L3`), `C31` (`U5` `DVDD` cap at 4.7 mm, `L4`), `C21`/`C22` (`U3` `VOUT` caps sharing one via 4.1 mm away, `L5`), and `F.Cu` traces under `L2` (`L6`/`L13`) all slipped past placement and routing into the Reviewer-A review gate.

4. **Unbounded router retry loops instead of fast-failing back to placement (`D-018`..`D-029`):**
   - When a placement was congested, the agent ran 15–25 consecutive `route.py` / `handroute.py` tweaks (and encountered stateful rip-up bugs where `copper_island` offered only one layer of a via or kept ripped copper alive, fixed in `110babd` and `119714c`) instead of immediately stopping after 3 tries to move the blocking component by 0.5 mm or downsize a passive.

5. **Inner-plane (`In2.Cu` `3V3`) splits and narrow necks discovered late (`D-020`, `D-023`):**
   - Signal vias and inner-layer jumpers sliced `In2.Cu` (`3V3`) into disconnected islands or `< 0.5 mm` necks while `kicad-cli pcb drc` still reported `0 unconnected` if a single thin bridge remained. Only after building the Shapely morphological-opening check (`pourgeom.py`) did every routing pass automatically enforce `pieces == 1` and `neck >= 0.8 mm` (`local_neck >= 1.38 mm` around `U1`).

6. **Two external review rounds required because datasheet layout checklists weren't self-audited pre-review:**
   - Reviewer-A Round 1 returned `CONCERNS` (`L1`–`L12`) and Round 2 caught `L13` (a leftover `F.Cu` stub under `L2` after the `D-025` swap) and `Q3` (crystal ground guard ring). A pre-review automated check against per-IC `layout_checklist` constraints would have caught all of these before `ohmai review start layout`.

7. **Repo & environment friction (Git hooks, Git LFS datasheets, `jlcparts` schema v2, Freerouting 2.2 Java 25 pin, 3D STEP models):**
   - Missing `.git/hooks/commit-msg` in plain git repos (`d4a86cf`), `jlcparts` switching to `source-db-v2` (`e5a061b`), Freerouting 2.1 hanging on single-net passes vs. Freerouting 2.2.4 needing Java 25 and `--opt-passes=2` (`D-019`, `73baa12`), 5+ GB `kicad-packages3D` missing from shared storage (`9e3b2af`), and binary PDF datasheets in Git LFS causing push/filter friction.

---

### Proposed Workflow & Tool Improvements (Menu for Owner Selection Before Cleanup)

#### 1. Autonomous Passive Package Swaps & Addition of Standard Decouplers (Owner Feedback)
- **Rule change (`skill/phases/04-parts.md`, `06-schematic.md`, `07-layout.md`, `AGENTS.md`):**
  - Empower the agent during Phase 6/7 (Schematic) and Phase 8 (Layout) to **autonomously swap passive package sizes** (resistors, MLCCs, inductors within `0402`–`0805` / compact shielded power inductors) and **add/co-locate standard datasheet-recommended HF decoupling capacitors** to resolve placement congestion, hot-loop distance violations, or schematic review findings **without stopping for an owner decision**, provided:
    1. Electrical & derating constraints pass (`ohmai check constraints`: effective capacitance at DC bias $\ge$ datasheet minimum, voltage rating $\ge 2\times V_{\text{rail}}$ or documented derating, resistor power rating, inductor $I_{\text{sat}} / I_{\text{rms}} / \text{DCR}$ and shielded construction),
    2. JLCPCB availability passes (in stock, basic part preferred over extended where specs match),
    3. `ohmai check schematic` and `ohmai check layout` (ERC = 0, DRC = 0, schematic$\leftrightarrow$PCB$\leftrightarrow$BOM parity = 0) pass, and
    4. The swap/addition is automatically logged in `bom/bom.csv`, `parts/constraints/`, and `STATUS.md`.
  - **When to still ask the owner:** Changing active ICs, connectors, switches, crystals, mechanical/board outline, net topology, or any change that trades off a hard requirement (`R-xx`) or requires an explicit datasheet waiver (`D-028`).
- **Tool support (`ohmai passives swap <REF> --package <PKG>` / `ohmai check constraints`):**
  - Add a passive-derating validator in `ohmai check constraints` and helper CLI `ohmai passives swap` that updates `bom/bom.csv`, schematic symbol footprint/LCSC fields, netlist, and PCB footprint atomically in one command.

#### 2. Placement $\ne$ Fit: Incremental Block Placement + Pre-Route `critical_loops` & `keepouts` Check + Multi-Island Courtyard Fix
- **2a. Incremental block-by-block placement workflow (`skill/phases/07-layout.md`):**
  - Replace all-89-parts-at-once placement with 4 staged checkpoints:
    1. **Stage A (Fixed & Mechanical):** Board outline, mounting/castellated headers (`J4`), edge connectors (`J1`, `J2`, `J3`), switch (`SW1`). Run `kicad-cli pcb drc`.
    2. **Stage B (Power Stage & Critical Hot Loops):** Regulators (`U3`), inductors (`L1`, `L2`), input/output caps (`C19`–`C22`), ESD (`U4`, `D1`). Run `ohmai check placement` + trial route of power loops immediately.
    3. **Stage C (MCU Core, Clock, Flash, AFE & Decouplers):** Place `U1`, `Y1`, `U2`, `U5` together with their tight decouplers (`C1`–`C18`, `C23`–`C32`). Run `ohmai check escape-room` + `ohmai layout fanout` before placing non-critical passives.
    4. **Stage D (Remaining Passives, Jumpers, Test Points):** Place `JP1`–`JP6`, `TP1`–`TP12`, LED/pull-ups in remaining free lanes via `ohmai layout fit --scan`.
- **2b. Sub-second `ohmai check placement` (`critical_loops` & `keepouts` in `parts/constraints/*.yaml`):**
  - Extend `parts/constraints/<IC>.yaml` with machine-checked geometric assertions evaluated on `.kicad_pcb` pad coordinates in `< 1 s` *before* routing:
    - `critical_loops`: max pad-to-pad distance (and same-layer requirement) for hot loops and decouplers (e.g., buck/boost `C_IN -> VIN/PGND <= 2.5 mm`, `L_SW -> SW <= 3.0 mm`, `C_OUT -> VOUT/PGND <= 3.0 mm`, MCU/AFE decouplers `<= 3.5 mm`).
    - `keepouts`: under-body copper keepouts (e.g., `no_signal_traces_under_body: [F.Cu]` for unshielded/semi-shielded inductors like `L2` or crystal `Y1`).
  - This catches `L1`–`L6` and `L13` in **1 second at placement time** instead of after 20 routing runs and an external review gate.
- **2c. Multi-island courtyard fix in `ohmai/layout/placement.py` (fixing the `J4` single-box bug):**
  - Change `Footprint.courtyard` from a single union bounding box `(min(xs), min(ys), max(xs), max(ys))` across all `CrtYd` graphics to `courtyards: list[Box]` (one bounding box per disconnected `fp_rect`/`fp_poly` loop on `F.CrtYd`/`B.CrtYd`). Dual-row edge headers like `J4` (`x = 99.755..102.655` and `x = 118.345..121.245`) will then model their two actual edge strips leaving the 15.69 mm interior free—eliminating the need for `--ignore-courtyard J4` and always checking real edge-strip courtyards and pad copper.
- **2d. Finish wiring `ohmai layout {fanout,autoroute,pour,handroute}` CLI subcommands in `ohmai`:**
  - Port the remaining `pcbnew` execution wrappers (`fanout.py`, `route.py`, `pour.py`, `handroute.py`) onto the pure-Python core (`config.py`, `dsn.py`, `pourgeom.py`, `grid.py`) already committed in `ohmai/cli/src/ohmai/layout/`.

#### 3. Plane Neck & Pour Continuity Check Built Into `ohmai layout pour` & `ohmai check layout`
- Promote `ohmai.layout.pourgeom` (`pieces == 1`, `min_neck >= 0.5 mm`, `local_neck >= 0.8 mm`) from a standalone helper to a mandatory subcheck inside `ohmai layout pour` and `ohmai check layout` whenever `hardware/layout.yaml` declares `pour:`. Any routing pass that splits an inner plane or pinches a power neck fails immediately with the exact $(x, y)$ neck coordinates.

#### 4. Fast-Fail / 3-Try Cap on Router Loops & Atomic Rip-and-Reroute
- **Workflow rule (`skill/phases/07-layout.md`):** Hard cap of **3 consecutive router/handroute iterations** on any fixed placement. If `unconnected > 0` or `DRC > 0` persists after 3 tries:
  1. Stop tweaking trace waypoints,
  2. Identify the bottleneck net/component from the rip-up/congestion report, and
  3. Either move/rotate the blocking footprint (`ohmai layout fit --scan`) or autonomously downsize the blocking passive (Improvement #1).
- **Atomic dry-run in `ohmai layout handroute` / `fit`:** Always apply candidate moves/routes on a staged copy of `.kicad_pcb`, run `kicad-cli pcb drc` + `pourgeom`, and commit to the working board only if DRC errors do not increase.

#### 5. Pre-Review Self-Audit Against Datasheet `layout_checklist` (`ohmai check layout`)
- During Phase 5 (`parts/constraints/<IC>.yaml`), extract every datasheet layout bullet into a structured `layout_checklist:` block (pin-to-cap loop limit, sense trace routing, guard ring / keepout under body, thermal pad via count & diameter, differential pair skew/length).
- Have `ohmai check layout --gate` evaluate all machine-checkable `layout_checklist` items and print a mandatory verification table before `ohmai review start layout` can be invoked—preventing multi-round external review rejections (`L1`–`L13`, `Q3`).

#### 6. Project-Level 3D Models (`ohmai kicad-libs models`) + Datasheet Manifest (`ohmai datasheets fetch`) & Pre-Push Guard
- **3D Models (already implemented in `ohmai` `9e3b2af`):** `ohmai kicad-libs models` fetches official `.step` files into `<project>/out/3dmodels/` only for footprints used on the board, flags missing upstream/custom 3D models, and generates valid ISO-10303-21 STEP AP214 colored bounding-box solids (`--stage-pcb` for hash-locked boards).
- **Datasheet Manifest (`ohmai datasheets fetch` + pre-push guard):** Replace Git-LFS-tracked binary PDFs in the repo with a tracked `datasheets/manifest.yaml` (`mpn`, `lcsc`, `url`, `sha256`, `cited_pages`) + `ohmai datasheets fetch --verify` (which downloads/caches PDFs into gitignored `out/datasheets/` or `$OHMAI_DATASHEET_CACHE` and verifies `sha256`), paired with a pre-commit/pre-push check that blocks committing raw PDFs or LFS pointers without a working filter.

#### 7. Environment & Tooling Friction Fixes (Already Ported or Ready to Finalize)
- **Git hooks auto-install (`d4a86cf`):** `ohmai init` installs `.git/hooks/commit-msg` automatically, and `ohmai doctor` warns whenever the hook is missing or outdated.
- **`jlcparts` schema v2 (`e5a061b`):** `ohmai parts search` natively reads `source-db-v2` (`jlc_components`).
- **Freerouting 2.2.4 + Java 25 pin (`73baa12`) & timeout/pass caps:** Lock `freerouting >= 2.2` with Java 25 in `toolchain.lock.yaml`, default `--opt-passes 2` and per-pass timeout in `ohmai layout autoroute`, and never use Freerouting for single-net incremental surgical edits (use the `ohmai.layout.grid` A* router instead).
