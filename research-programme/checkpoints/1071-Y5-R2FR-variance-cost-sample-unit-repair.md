# 5055 - variance/cost sample-unit repair

Marker: `MTS_5055_VARIANCE_COST_SAMPLE_UNIT_REPAIR`.

## Unit defect

Checkpoints 5049-5054 estimate variance across four independent Owen scrambles
after averaging two nested events per scramble. A variance unit therefore costs
two events. Earlier wall-time projections charged only one event. Score ratios
remain unchanged when both high and low costs share the factor, but projected
runtime does not.

## Repaired designs

| design | optimal score ratio | minimum runtime below 0.8 |
|---|---:|---:|
| paired two-event scramble | 0.671 | 27.69 h |
| single point, index 0 diagnostic | 0.763 | 16.96 h |
| single point, index 1 diagnostic | 0.594 | 13.33 h |
| conservative one-point envelope | 0.726 | 14.88 h |

The two individual one-point strata are diagnostics only and cannot be selected
post hoc. The admissible one-point design takes the componentwise larger
variance of the two strata. At the 10-hour cap its score ratio is `1.129`, so it
is worse than high-only sampling. No unit-consistent design passes below 10
hours and no fresh kernels are authorized.

The exact unit-Richardson control remains statistically useful; only the claimed
execution scale is repaired.

## Evidence

- Result: `source-intake/functional_rg/5055/variance_cost_sample_unit_repair.json`
- Designs: `source-intake/functional_rg/5055/paired_vs_single_sample_designs.csv`
- Generator: `scripts/Y5_R2FR_5055_variance_cost_sample_unit_repair.py`
- Validation: `source-intake/mts_residuals/P8_Y5_BRR545_5055_VALIDATION.csv`

This is an estimator/cost correction, not production amplitude or MTS evidence.
