# 5120 - locked beta-one complex-control analysis

## Locked execution

The completed `180/180` control matrix is evaluated under the 5110 design
without refitting:

- high observable: `H=2 A_020-B_040`;
- paired and independent control: `C=A_020`;
- fixed complex coefficient: `beta=1` in all ten channels;
- high/low units: `4/12`, ratio `3`;
- score threshold: `<0.8`;
- accepted-final-job runtime cap: `10 h`;
- target central values used: none.

The paired identity closes numerically with zero residual. All matrices and
covariances are finite, and all seventeen validation checks pass.

## Result

The locked decision is `LOCKED_BETA_ONE_COMPLEX_CONTROL_DOES_NOT_PASS`:

- realized cost-normalized score: `1.5148246022524876`;
- threshold: `0.8`;
- score gate: failed;
- accepted final-job runtime: `9.860421870944458 h`;
- runtime gate: passed;
- bottleneck: `real_z-0.3`;
- maximum delete-one shift: `0.9871889597534148` estimator standard errors.

The fixed estimator is algebraically valid but is not an efficiency
improvement. This rejects the locked numerical control route, not the high
matrix, kernel, local-GR programme or MTS theory.

## Outputs

- `scripts/Y5_R2FR_5120_locked_beta_one_complex_control_analysis.py`
- `source-intake/functional_rg/5120/locked_beta_one_complex_control_analysis.json`
- `source-intake/functional_rg/5120/locked_beta_one_complex_control_channels.csv`
- `source-intake/functional_rg/5120/locked_beta_one_complex_control_event_costs.csv`
- `source-intake/functional_rg/5120/locked_beta_one_complex_control_jackknife.csv`
- `source-intake/mts_residuals/P8_Y5_BRR545_5120_VALIDATION.csv`
