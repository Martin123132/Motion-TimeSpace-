# 5076 - central-anchor delete-one sensitivity

Marker: `MTS_5076_CENTRAL_ANCHOR_DELETE_ONE_SENSITIVITY`.

The fixed `A08` design is recomputed for the full panel, eight delete-one-event
panels, and four delete-one-seed panels. No topology choice, coefficient, or
threshold is refit inside a panel.

At fixed costs, 11 low units pass every panel with maximum score ratio `0.7946`
and runtime `5.971 h`. Under joint statistical and event-cost deletion, the
robust allocation is four high plus 12 low units; its worst ratio is `0.7789`
and worst projected runtime `7.411 h`.

## Evidence

- Result: `source-intake/functional_rg/5076/central_anchor_delete_one_sensitivity.json`
- Panels: `source-intake/functional_rg/5076/delete_one_sensitivity_panels.csv`
- Locked manifest: `source-intake/functional_rg/5076/locked_central_anchor_pilot_manifest.json`
- Generator: `scripts/Y5_R2FR_5076_central_anchor_delete_one_sensitivity.py`
- Validation: `source-intake/mts_residuals/P8_Y5_BRR545_5076_VALIDATION.csv`

The statistical design is locked here, but execution remains blocked pending a
runner and fresh runtime smoke.
