# 5049 - restricted coarse `E040` multilevel reaudit

Marker: `MTS_5049_RESTRICTED_COARSE_E040_MULTILEVEL_REAUDIT`.

## Corrected matrix

The complete `coarse12` matrix converges `120/120` jobs with zero failures and
zero unconverged rows. Its 97 exact theorem-zero rows all pass both restricted
family and independent-witness guards. No broad certificate survives.

## Corrected statistical result

Uniform coarse `E040` now has:

- low/high future cost ratio `0.287`;
- equal-cost target-normalized score ratio `0.674`;
- `6/10` cross-fitted channels improved;
- worst cross-fitted SD ratio `1.581`.

The aggregate efficiency gate therefore passes, overturning the quarantined
5043 ratio `1.370`. A fresh pilot is still blocked because the unstable
channels are imaginary: the five real-channel ratios are all at most `0.161`,
whereas three imaginary channels exceed one. The result points to phase-sector
control rather than exterior-argument coarsening.

## Evidence

- Benchmark: `source-intake/functional_rg/5049/restricted_coarse_profile_benchmark.json`
- Status: `source-intake/functional_rg/5049/runs/coarse12/status.json`
- Result: `source-intake/functional_rg/5049/restricted_multilevel_coarse_E040_gate.json`
- Components: `source-intake/functional_rg/5049/restricted_multilevel_component_gate.csv`
- Generator: `scripts/Y5_R2FR_5049_restricted_coarse_E040_multilevel_reaudit.py`
- Validation: `source-intake/mts_residuals/P8_Y5_BRR545_5049_VALIDATION.csv`

This is a retrospective estimator-design result, not amplitude evidence.
