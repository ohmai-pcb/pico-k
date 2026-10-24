# BOM

`bom.csv` is the single BOM. One row per unique part or functional/DNP group (`refs` are space-separated; functionally distinct roles such as `R15` `3V3_EN` pull-up vs `R16` `TPS63001` `PS/SYNC` pull-down, or independent DNP options such as `R6` flash `CS` pull-up vs `R23 R24` `MAX31856` `DRDY`/`FAULT` pull-ups, may occupy separate rows so role-specific notes and assembly options stay clear).

| Column | Meaning |
|--------|---------|
| status | `candidate` (phase 4) → `approved` (owner approved) → `locked` (phase 10) |
| mpn / approved_alternates | Locked MPN; alternates separated by `;`. The fab may only buy one of these. |
| price_qty1/100/1000, currency, price_source, price_date | No price without source and date |
| rating_notes | Ratings that matter, e.g. `250 mW`, `50 V X7R`. `ohmai check bom-diff` compares power ratings. |
| dnp | `yes` = do not populate |

Before approving a fab order, export the fab's **actual purchase list** to `bom/fab-actual.csv` (or pass
`--fab`) and run `ohmai check bom-diff`. Every substitution must be in `approved_alternates` or be approved
and added first. Real lesson: a fab quietly bought MP2651-Z for MP2651-P, picked its own passive MPNs, and
one resistor came in at 0.2 W against a 250 mW requirement.
