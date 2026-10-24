# Safety and compliance plan: pico-k

> **Status: APPROVED by the owner 2026-10-15 (D-005: S3-1 … S3-9 as recommended).** Target market EU only (D-003); UK/US
> not applicable. Not legal advice: every act and standard below is a **candidate** with its source; the
> owner (or a compliance lab) decides. Decisions needed: S3-1 … S3-9 in STATUS.md. `ESTIMATE:` marks
> numbers not taken from a source. Sources are listed at the end (read 2026-10-15) and cited as [Sx].

## Target markets and legislation
Market: **EU** (STATUS.md `markets: [EU]`). Product: 51 × 21 mm bare board, USB 5 V only, RP2350A (no
radio), MAX31856 type K input, mini type-K socket (D-001, D-004).

| Market | Act | Applies? | Why / scope clause | Marks and documents | Source |
|--------|-----|----------|--------------------|---------------------|--------|
| EU | EMC Directive 2014/30/EU | **Yes**, once placed on the market for end users (S3-1, S3-2) | Board is an "apparatus" or a "component/sub-assembly intended for incorporation into an apparatus by the end-user" (Art. 3(1)(2), 3(2); EMC guide §1.5.3 p.22–23). Not "inherently benign" (150 MHz MCU, switching regulator). The custom-built evaluation-kit exclusion (Art. 2(2)(e)) needs a kit built for a specific professional R&D customer (EMC guide §1.4.5 p.18), so it does not fit a Pico-style board sold to hobbyists | CE, EU DoC (Art. 15), technical documentation (Annex II), type/batch number and address (Art. 7(5)-(6)), instructions + Art. 18 information (Art. 7(7)) | [S1] [S2] |
| EU | RoHS Directive 2011/65/EU | **Yes** (substance limits always; CE/DoC when sold as finished EEE) | A board supplied for direct use by an end user is finished EEE; one sold only for integration by manufacturers is not (RoHS FAQ Q6.5 p.18). Components must meet Art. 4 limits but need no CE (Q7.3 p.20). Prototypes / development vehicles used solely for R&D are excluded (FAQ p.14) | CE + DoC covering RoHS (Art. 7(c)), technical documentation (EN IEC 63000:2018, as used by the Pico 2 DoC) | [S3] [S4] [S5] |
| EU | GPSR (EU) 2023/988 | **Yes** if consumers can buy or use it; complements EMC/RoHS for risks they do not cover (recital 8) | Electrical-safety, thermal (hot probe) and misuse risks are not covered by EMC/RoHS, so the GPSR general safety requirement covers them | Risk analysis in the technical documentation (Art. 9(2)); type/batch/serial (Art. 9(5)); name, postal + electronic address (Art. 9(6)); instructions and safety information in the language of each Member State (Art. 9(7)); online listing information (Art. 19) | [S6] [S7] |
| EU | WEEE Directive 2012/19/EU | **Yes** (EEE placed on the market) | Producer marks EEE with the crossed-out wheeled bin (Art. 14(4), Annex IX); users informed (Art. 14(2)); producer registration in each Member State where sold (Art. 16) | Bin symbol per EN 50419:2022, minimum 7 mm high with bar (§4.2.1); on packaging, instructions and warranty if the product is too small (§4.2.4) | [S8] [S9] |
| EU | REACH (EC) 1907/2006 | **Yes** (article supplier) | If any article contains a Candidate-List SVHC > 0.1 % w/w: Art. 33 information to recipients (consumers on request, free, within 45 days); SCIP notification under the Waste Framework Directive Art. 9(1)(i) | Supplier SVHC declarations collected in phase 4 (incl. the BeCu socket clips) | [S10] |
| EU | CE marking rules: Reg. (EC) 765/2008 Art. 30, Annex II; Decision 768/2008 Module A; Reg. (EU) 2019/1020 Art. 4 | **Yes** with EMC/RoHS | CE ≥ 5 mm high unless the specific act says otherwise; an economic operator established in the EU (the manufacturer, if established in the EU) | CE mark, DoC | [S11] |
| EU | Low Voltage Directive 2014/35/EU | **No** | Applies only to equipment rated 50–1000 V AC or 75–1500 V DC (Art. 1). pico-k is USB 5 V only (R-06) | - | [S12] |
| EU | Radio Equipment Directive 2014/53/EU | **No** | No radio: RP2350A, no wireless (requirements "Out of scope", D-001). Not a Pico 2 W | - | requirements.md |
| EU | Cyber Resilience Act (EU) 2024/2847 | **Candidate, check before selling** | A board shipped with firmware and a USB data connection may be a "product with digital elements". Main obligations apply from 11 Dec 2027; Art. 14 vulnerability/incident reporting from 11 Sep 2026, also for products already on the market (Art. 71). Scope for pico-k not analysed in this phase | Decide before first sale | [S21] |
| EU | Packaging and Packaging Waste Regulation (EU) 2025/40 | Candidate (only if sold in packaging) | Not researched in this phase | Phase 10/11 | not verified |
| UK / US | UKCA, FCC Part 15 | **Not applicable** | D-003 (EU only) | - | decisions.md |

### Component / dev board vs finished product (S3-2)
| Positioning | EMC | RoHS | GPSR | Consequence |
|-------------|-----|------|------|-------------|
| D1 finished board for end users (hobbyists, makers, labs), the Pico 2 model | Apparatus or component for incorporation by the end-user (Art. 3(2)) → full EMC: CE, DoC, tests, instructions | Finished EEE → CE + DoC | Applies (consumers can buy it) | Full CE route below. Raspberry Pi does this for the Pico 2: EU DoC under EMC + RoHS, EN 55032 / EN 55024 / EN IEC 63000 [S4] |
| D2 component sold only to manufacturers who build it into their own product | Outside "apparatus" only if all EMC guide §1.5.3 conditions hold (no stand-alone risk assessment possible, supplied only to future-product manufacturers, incorporated only by them) [S2 p.23] | Not finished EEE: substance limits, no CE (FAQ Q6.5, Q7.3) | Usually not a consumer product | Integrator does the CE work. Does not fit a Pico drop-in with its own USB and sensor socket sold openly |
| D3 prototypes (rev-A, 5–10 boards) for the owner's own R&D, not supplied to anyone | Not placed on the market (Blue Guide 2022 §2.3: prototypes, own use) | R&D exclusion (FAQ p.14) | Not made available | No CE needed **until any board is supplied to someone else**, paid or free. Keep the file ready |

## Hazards
| Hazard | Where | Voltage / energy | Mitigation |
|--------|-------|------------------|------------|
| H1 Probe touches a live (mains) part | T+/T− at the socket. T− is biased from the board (BIAS → T−, MAX31856 p.27) and the board ground is the USB host ground | Up to mains voltage on the probe, the board and the host USB ground. MAX31856 inputs survive only ±45 V (p.2, p.14); no isolation (A2-4 G1, D-004) | Not designed for use on or near live parts: intended use excludes it; warning **MW-02**. No insulation is claimed between the probe and USB |
| H2 Grounded-junction probe on an earthed object with an earthed host | T+/T− common mode | Ground offset, low energy | Readings unspecified, OVUV fault (p.26); warning **MW-01** (D-004 A2-4) |
| H3 Hot probe → burns, fire | Probe tip and sheath; the board is never at the measuring point | Type K up to +1372 °C (R-10, MAX31856 Table 1 p.12) | Warning **MW-03**: probe stays hot after use; the probe's own rating applies |
| H4 Socket, plug or board overheated | Board end with the PCC-SMD socket | Socket clips −50 to +120 °C (PCC-SMD p.1); board −20 to +85 °C incl. self-heating (Pico 2 datasheet §3.3 p.12) | Warning **MW-04**: only the probe enters the hot zone; keep board, socket and plug within these ranges |
| H5 Board self-heating | Regulator, D1 | ESTIMATE 0.26 W worst case (architecture.md, power tree) | Low; touch temperature checked in phase 12 (EN IEC 62368-1 TS classes, if S3-4 = C1) |
| H6 Wrong supply or overvoltage on VSYS/VBUS pins | Edge pins 39/40 | VSYS 1.8–5.5 V (Pico 2 §3.3 p.12) | Warning **MW-05**: USB 5 V only (R-06); do not feed other voltages to pins |
| H7 ESD on bare board and probe | Exposed copper, socket | ESD | Instructions: handle by the edges; EMC immunity test (ESD) on the socket and USB shell |
| H8 Small bare board; children | Whole board | - | Warning **MW-06**: not a toy; intended use is by adults (makers, labs). Food contact excluded from intended use unless the probe is certified for it |

## Applicable standards (candidates, with source)
| Standard | Why it applies | Clause(s) used | Source |
|----------|----------------|----------------|--------|
| **EMC, option E1 (rec): EN 55032:2015+A11:2020 (+A1:2020) Class B + EN 55035:2017+A11:2020** | Multimedia/ITE product standards; the Pico 2 is declared to EN 55032 + EN 55024 (EN 55035 replaced EN 55024) [S4]. Class B = residential, so no Art. 18(2) restriction. Hobby and home use fits better than 61326-1 | EN 55032 radiated emissions, Table 1 upper frequency; EN 55035 Tables 1, 3, 4 | [S4] [S13] [S14] [S15] |
| EMC, option E2: EN IEC 61326-1:2021 (+A11:2026), emissions CISPR 11 Group 1 Class B | Product-family standard for measurement and test equipment, incl. transducers; scope is professional, industrial-process, manufacturing and educational use [S16]. Fits if pico-k is sold as a measuring instrument for labs. Compatible Electronics quotes it at about 2× the E1 cost [S17] | Basic electromagnetic environment table | [S16] [S17] |
| EMC, option E3: generic EN IEC 61000-6-3 + EN IEC 61000-6-1 (residential) | Generic fallback when no product standard fits | - | edition to check in the [S13] summary list |
| **Safety reference for the GPSR risk analysis, C1 (rec): EN IEC 62368-1** (ES1/PS1 SELV board) | Not mandatory (LVD does not apply). Raspberry Pi has the Pico 2 W CB-certified to IEC 62368-1:2018 [S18]. Used as state of the art (GPSR Art. 8) for touch temperature, energy-source classes and the hot-probe and mains-probe misuse | Energy-source classification, thermal burn (TS classes), instructional safeguards | [S6] [S18] |
| Safety reference, C2: EN 61010-1 | For electrical measurement equipment; fits if E2 / lab positioning is chosen | Marking, temperature limits | name only; not researched in this phase |
| EN IEC 63000:2018 | RoHS technical documentation | whole | [S4] |
| EN 50419:2022 | WEEE marking | §4.2.1, §4.2.4 | [S9] |

### Test levels (E1, to confirm with the lab and the purchased standards)
| Test | Port | Level | Applies? | Source |
|------|------|-------|----------|--------|
| Radiated emissions, Class B | enclosure (bare board + USB cable + probe) | 30 MHz up to 2 GHz: highest internal frequency 150 MHz (Pico 2 p.4) falls in 108–500 MHz → 2 GHz. The RP2350 PLL VCO runs at 750–1600 MHz (RP2350 datasheet p.528); if the lab counts the VCO, up to 6 GHz | yes | [S14] |
| Conducted emissions | AC mains | only if the test setup includes a mains USB adapter; laptop or powerbank use has no mains port on the EUT | lab decides | [S14] |
| ESD (IEC 61000-4-2) | enclosure: socket, USB shell, exposed copper | ±4 kV contact, ±8 kV air, criterion B | yes | [S15] |
| Radiated RF immunity (IEC 61000-4-3) | enclosure | 3 V/m, 80 MHz–1 GHz + spot 1.8 / 2.6 / 3.5 / 5 GHz, criterion A | yes | [S15] |
| Conducted RF immunity (IEC 61000-4-6) | DC power (USB) and signal (thermocouple) ports | 3 V 0.15–10 MHz, falling to 1 V at 30 MHz, 1 V to 80 MHz | only for cables that may be longer than 3 m (S3-5) | [S15] |
| EFT/burst (IEC 61000-4-4) | DC power and signal ports | 0.5 kV | only for cables > 3 m (S3-5) | [S15] |
| Surge (IEC 61000-4-5) | DC power | - | only outdoor cables: no | [S15] |
| Performance criterion A | temperature reading | PROPOSAL: reading change ≤ the R-11 accuracy limit during the test; no reset, no USB disconnect | owner approves (S3-6) | R-11 |

### What can be self-assessed
- **EMC**: internal production control, Module A (Art. 14, Annex II). No notified body; the manufacturer
  can do the EMC assessment and write the DoC. Lab tests are the evidence, not a legal requirement [S1].
- **RoHS**: Module A (Art. 7(b)) using supplier declarations and EN IEC 63000 [S3].
- **GPSR**: no conformity assessment; the manufacturer's risk analysis (Art. 9(2)) [S6].
- **WEEE/REACH**: registration, marking and declarations, no testing.

### Test budget (ESTIMATE)
| Route | What | ESTIMATE cost | How estimated |
|-------|------|---------------|---------------|
| T1 accredited lab, formal EN 55032 B + EN 55035 | 2–3 shifts, one report | ESTIMATE €2,500–5,500 excl. VAT | Compatible Electronics planning range US$3,000–6,000 for EN 55032 B + EN 55035, typically 2–3 shifts [S17]; INDES EMC (AT) supervised day €1,800 excl. VAT, May 2026 [S19] |
| T2 pre-compliance day, then self-declaration on the documented results | 1 supervised day + extended report | ESTIMATE €2,350 excl. VAT (€1,800 day + €550 report) | INDES EMC price list, May 2026 [S19] |
| T3 engineering assessment only, no test | design review + documentation | ESTIMATE €0 cash, owner time | legal under Module A, weakest evidence if market surveillance asks |
| Re-test after a fix | +1 shift | ESTIMATE +€1,200–1,800 | [S19] short / standard day |

## Insulation, creepage and clearance
All circuits are SELV (USB 5 V, ES1 ≤ 60 V DC per EN IEC 62368-1 energy-source class). No
basic or reinforced insulation is needed or claimed between any net classes. The thermocouple input is
**not isolated** from USB ground (D-004 A2-4 G1), so no spacing on the board protects against H1; the
control is the intended use + MW-02.

| Between (net class A ↔ B) | Working voltage | Insulation type | Pollution degree | Clearance (mm) | Creepage (mm) | Standard + table |
|---------------------------|-----------------|-----------------|------------------|----------------|---------------|------------------|
| any ↔ any (SELV, ≤ 5.5 V) | ≤ 5.5 V DC | functional only | 2 (indoor, assumed) | fab minimum (JLCPCB rules, phase 8) | fab minimum | none required for ES1; EN IEC 62368-1 energy-source class |
| TC input (T+/T−) ↔ USB GND | ≤ 1.4 V common mode in normal use (MAX31856 p.3) | none (not isolated, G1) | - | - | - | D-004; hazard H1 handled by MW-02 |

Phase 8: no creepage DRC rules beyond the fab's minimums.

## Component ratings and derating
| Part class | Rule (PROPOSAL, owner approves in S3-7) | Source |
|------------|------------------------------------------|--------|
| All parts | Rated operating temperature covers −20 to +85 °C board ambient incl. self-heating | Pico 2 datasheet §3.3 p.12 (board rating that R-02/R-04 drop-in implies) |
| Socket PCC-SMD | ≤ 120 °C at the clips; MW-04 | PCC-SMD p.1 |
| MAX31856 | Inputs ≤ ±45 V abs. max; Fig. 8 filter (100 nF differential) | MAX31856 p.2, p.27 |
| Capacitors on VBUS/VSYS | Rated voltage ≥ 10 V (ESTIMATE rule: ≥ 1.8 × 5.5 V max) | ESTIMATE; VSYS max Pico 2 §3.3 p.12 |
| Ceramic capacitors | Use the DC-bias derated capacitance from the maker's curve, not the nominal value | phase 4, per part |
| Resistors | ≤ 50 % rated power (ESTIMATE rule) | ESTIMATE |
| RoHS | Every part with a RoHS declaration; REACH SVHC declaration where the supplier gives one | [S3] [S10] |

## Protection
- **ESD on USB**: USBLC6-2SC6 on D+/D− (architecture A2-5 block). ESD on the socket: MAX31856 input
  protection + Fig. 8 RC filter (p.27); phase 4 checks whether a low-leakage TVS on T+/T− is needed
  without hurting µV accuracy.
- **Overvoltage on the TC input**: survives ±45 V only (p.14). Series resistors per Fig. 9 (p.28) protect
  the IC against higher fault voltages but **do not make the board safe on mains** (no isolation). Not
  added unless S3-3 says so.
- **Supply**: USB host current limit; VBUS→VSYS Schottky as Pico 2; regulator thermal shutdown
  (TPS63001 datasheet, phase 4 constraints). No fuse (as Pico 2). No reverse polarity risk with USB-C.
- **Touch current**: SELV only; not applicable.

## Required manual warnings
Every ID is registered in STATUS.md "Manual warnings" and goes into `docs/manual.md` §Safety information.

| ID | Warning (hazard, consequence, how to avoid) | Source (phase, doc) |
|----|---------------------------------------------|---------------------|
| MW-01 | Grounded-junction probe on an object at the same earth as the USB host: outside the MAX31856 common-mode range (0.5–1.4 V); readings unspecified, OVUV fault may stop conversions. Use a powerbank or ungrounded host, or an insulated-junction probe | phase 2, A2-4, D-004; MAX31856 p.3, p.26 |
| MW-02 | Never touch live electrical parts or mains with the probe or its cable. The probe is not insulated from the USB host; a live part puts that voltage on the board, the USB cable and the computer → electric shock and damage | phase 3, H1; MAX31856 p.2, p.14 |
| MW-03 | The probe tip and sheath can be very hot (type K up to 1372 °C) and stay hot after use: burns and fire. Use the probe within its own rating; let it cool before touching | phase 3, H3; R-10 |
| MW-04 | Only the probe goes into the hot zone. Keep the board within −20 to +85 °C and the socket and plug within −50 to +120 °C | phase 3, H4; Pico 2 §3.3 p.12; PCC-SMD p.1 |
| MW-05 | Power only from USB 5 V (computer or powerbank). Do not apply other voltages to the VBUS/VSYS pins (VSYS 1.8–5.5 V) | phase 3, H6; R-06; Pico 2 §3.3 p.12 |
| MW-06 | Not a toy; keep away from children. Not for food contact unless the probe is approved for it. Handle the bare board by its edges (ESD) | phase 3, H7, H8 |

EMC information for the manual (EMC Art. 18): intended use; Class B (no residential restriction); use
cables ≤ 3 m if S3-5 is accepted; the board is a component that users build in, so the instructions assume
no EMC knowledge (EMC guide §1.5.3 p.23).

## Labelling (51 × 21 mm board)
| Item | Rule | Where (PROPOSAL, S3-8) | Source |
|------|------|------------------------|--------|
| CE | ≥ 5 mm high; on the apparatus, or packaging + documents where not possible | Bottom silkscreen (bottom has no parts, only pads, D-001 R-07) | [S11]; EMC Art. 17 |
| WEEE bin with bar | ≥ 7 mm high (bin ≈ 5 mm); packaging + instructions + warranty if the product is too small | Bottom silkscreen, next to CE (ESTIMATE: 5 + 7 mm marks fit in the 16.18 mm between pad rows) | [S9] §4.2.1, §4.2.4 |
| Product ID: type + revision + batch | GPSR Art. 9(5); EMC Art. 7(5) | Silkscreen "pico-k rev-A" + batch/date code per order; serial number not planned | [S6] [S1] |
| Manufacturer name, postal + electronic address | GPSR Art. 9(6); EMC Art. 7(6); on the product or, where not possible, packaging / accompanying document. Only size justifies moving it (GPSR guidelines) | Packaging + manual (an address does not fit legibly at 21 mm width); short brand name + URL on silkscreen | [S6] [S7] |
| Instructions + safety information | language of each Member State where sold (GPSR Art. 9(7); EMC Art. 7(7)) | Printed leaflet + PDF; languages per S3-8 (Sweden: Swedish, per Konsumentverket guidance [S20]) | [S6] [S20] |

## Technical file contents (keep 10 years)
- General description, photos, intended use and foreseeable misuse (EMC Annex II §3(a); GPSR Art. 9(2)).
- Schematic, layout, BOM, drawings (Annex II §3(b)-(c)); this repo at the release tag.
- EMC assessment: standards applied (E1/E2), test plan, test reports or pre-compliance results, EUT
  configuration, firmware version, performance criteria (Annex II §3(d)-(f)).
- GPSR risk analysis: hazards H1–H8, mitigations, warnings MW-01 … MW-06 (Art. 9(2)(a)), list of standards
  used (Art. 9(2)(b)).
- RoHS: supplier declarations per part, EN IEC 63000 assessment (Art. 7(b)).
- REACH: SVHC declarations; SCIP number if needed.
- EU declaration of conformity (EMC Art. 15, Annex IV; RoHS).
- User manual (`docs/manual.md`) and the label artwork.
- WEEE producer registration numbers for each Member State.
- Retention: 10 years after the last unit is placed on the market (EMC Art. 7(3); GPSR Art. 9(3)).

## Certification path
1. rev-A (5–10 prototypes, D3): owner's own R&D, not supplied to anyone → no CE yet; keep the file growing.
2. Before supplying any board to anyone (paid or free): choose S3-1 … S3-8, run the test route (T1/T2),
   collect RoHS/REACH declarations, register for WEEE, write the DoC, finalize the manual (phase 12),
   apply CE.
3. All routes are self-declaration (Module A); no notified body.
4. USB 2.0 inrush (D-010): rev-A exceeds the USB 2.0 §7.2.4.1 attach load (10 µF ∥ 44 Ω) as a documented deviation.
   This is a USB-IF interoperability rule, not a CE/EMC/LVD/GPSR requirement, so it changes no CE route and needs no
   manual warning. Consequence: no USB-IF certification and no USB logo or "USB compliant" claim on the product,
   packaging or manual while the deviation stands. The attach transient (contact arcing, VBUS droop) is measured at
   bring-up; EMC tests (T1/T2) use the same hardware, so nothing extra is planned.

## Sources (read 2026-10-15)
- [S1] Directive 2014/30/EU (EMC), consolidated, EUR-Lex: https://eur-lex.europa.eu/eli/dir/2014/30/oj (Art. 2(2)(e), 3, 6, 7, 14-18, Annex II)
- [S2] Guide for the EMCD (Directive 2014/30/EU), March 2025 draft, §1.4.5 p.18, §1.5.3 p.22-23: https://www.ibf-solutions.com/fileadmin/dateidownloads/draft-emcd-guide-march-2025.pdf (published version: https://ec.europa.eu/docsroom/documents/33601)
- [S3] Directive 2011/65/EU (RoHS), Art. 4, 7: https://eur-lex.europa.eu/eli/dir/2011/65/oj
- [S4] Raspberry Pi Pico 2 EU Declaration of Conformity (2024-08-08): https://pip-assets.raspberrypi.com/categories/1007-approvals/documents/RP-006498-CF-2-rpi-pico2%20EU%20Declaration%20of%20Conformity.pdf
- [S5] Commission RoHS 2 FAQ (12 Dec 2012), Q6.5 p.18, Q7.3 p.20, R&D exclusion p.14: https://environment.ec.europa.eu/system/files/2021-01/FAQ%20key%20guidance%20document%20-%20RoHS.pdf
- [S6] Regulation (EU) 2023/988 (GPSR), Art. 8, 9, 19, recital 8: https://eur-lex.europa.eu/eli/reg/2023/988/oj
- [S7] Commission notice, GPSR guidelines for businesses (C/2025/6233): https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=OJ%3AC_202506233
- [S8] Directive 2012/19/EU (WEEE), Art. 14, 16, Annex IX: https://eur-lex.europa.eu/eli/dir/2012/19/oj
- [S9] EN 50419:2022 (NEK copy) §4.2.1 p.7, §4.2.4 p.9: https://www.nek.no/wp-content/uploads/2026/01/nek-en-50419_2022_en_001.pdf
- [S10] ECHA, Candidate List obligations and SCIP: https://www.echa.europa.eu/candidate-list-obligations, https://www.echa.europa.eu/scip
- [S11] Regulation (EC) 765/2008, Art. 30, Annex II: https://eur-lex.europa.eu/eli/reg/2008/765/oj
- [S12] Directive 2014/35/EU (LVD), Art. 1: https://eur-lex.europa.eu/eli/dir/2014/35/oj
- [S13] Commission EMC harmonised standards page (summary list, Implementing Decision (EU) 2019/1326 cites EN 55035:2017): https://single-market-economy.ec.europa.eu/single-market/goods/european-standards/harmonised-standards/electromagnetic-compatibility-emc_en
- [S14] BS EN 55032:2015+A11:2020 Table 1 (upper frequency vs highest internal frequency): https://nobelcert.com/DataFiles/FreeUpload/BS%20EN%2055032-2015%20plus%20Cor2016%20plus%20A11-2020.pdf
- [S15] EN 55035 levels: BS EN 55035:2017 Tables 1, 3 (https://nobelcert.com/DataFiles/FreeUpload/BS%20EN%2055035-2017.pdf) and ETSI TR 103 400 V1.1.1 Tables 4-5 (https://www.etsi.org/deliver/etsi_tr/103400_103499/103400/01.01.01_60/tr_103400v010101p.pdf)
- [S16] EVS-EN IEC 61326-1:2021+A11:2026 scope: https://www.evs.ee/en/evs-en-iec-61326-1-2021-a11-2026-consolidated
- [S17] Compatible Electronics, EMC Testing Cost Guide: https://www.celectronics.com/Resources/EMC-Testing-Cost-Guide
- [S18] Pico 2 W CB test certificate, IEC 62368-1:2018 (2024-12-06): https://pip-assets.raspberrypi.com/categories/1090-approvals/documents/RP-007563-CF-1-rpi-pico2w%20Electrical%20Safety%20CB%20Certificate.pdf
- [S19] INDES EMC e.U. price list (May 2026): https://www.indes-emc.at/services-9
- [S20] Konsumentverket, "Säkra produkter – Ditt ansvar" (Swedish-language instructions for consumer products, search summary; verify): https://publikationer.konsumentverket.se/downloads/sakra-produkter-ditt-ansvar/279/file
- [S21] Commission, CRA summary and Art. 71 dates: https://digital-strategy.ec.europa.eu/en/policies/cra-summary
- Datasheets as in `docs/architecture.md` (MAX31856 19-7534 Rev 0; Pico 2; RP2350; Omega PCC-SMD).
