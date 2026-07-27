# 5075 - central-anchor estimator recost

Marker: `MTS_5075_CENTRAL_ANCHOR_ESTIMATOR_RECOST`.

The fixed `A08` chain lowers projected means to `3723.01 s` for a high event,
`4091.31 s` for a paired correction event, and `466.36 s` for a low-only event.
Certificate runtimes are measured explicitly; the separate `0.1 s` allowance
covers construction/serialization after each certificate.

The admissible componentwise-conservative design first passes with nine low
units: score ratio `0.7850` at `5.712 h`. The best candidate under ten hours
uses 42 lows and has ratio `0.5609`, but that is not selected because the next
gate must protect against statistical and cost sensitivity.

## Evidence

- Result: `source-intake/functional_rg/5075/central_anchor_estimator_recost.json`
- Event costs: `source-intake/functional_rg/5075/central_anchor_event_costs.csv`
- Designs: `source-intake/functional_rg/5075/central_anchor_designs.csv`
- Generator: `scripts/Y5_R2FR_5075_central_anchor_estimator_recost.py`
- Validation: `source-intake/mts_residuals/P8_Y5_BRR545_5075_VALIDATION.csv`

This remains a retrospective cost model rather than fresh evidence.
