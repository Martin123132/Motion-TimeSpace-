# 5073 - full-chain estimator recost

Marker: `MTS_5073_FULL_CHAIN_ESTIMATOR_RECOST`.

The accepted recursive argument chain and epsilon transport reduce the mean
projected high event to `4201.22 s`, paired correction to `4569.52 s`, and
low-only event to `944.57 s`. The calculation includes measured certificate
time and a deliberately inflated `0.1 s` serialization allowance per generated
artifact.

For the admissible componentwise-conservative one-event design, 11 low units
first cross the `0.8` efficiency threshold at `7.963 h` with score ratio
`0.7979`. This is the first unit-consistent sub-ten-hour candidate, but remains
a retrospective projection.

## Evidence

- Result: `source-intake/functional_rg/5073/full_chain_estimator_recost.json`
- Event costs: `source-intake/functional_rg/5073/full_chain_event_costs.csv`
- Designs: `source-intake/functional_rg/5073/full_chain_designs.csv`
- Generator: `scripts/Y5_R2FR_5073_full_chain_estimator_recost.py`
- Validation: `source-intake/mts_residuals/P8_Y5_BRR545_5073_VALIDATION.csv`

No fresh execution is authorized until anchor choice and cost sensitivity are
locked.
