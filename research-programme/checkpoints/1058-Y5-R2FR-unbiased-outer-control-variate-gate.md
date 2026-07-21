# 5042 — Unbiased outer control-variate gate

**Status: RECOMPUTED after the 5048 restricted-scope matrix repair.**

## Question

Can the completed four-scramble, two-point matrix support a cheap outer-variable
control variate before any further production kernels are generated?

## Exact estimator contract

For any feature vector `f(u)` with known expectation zero and coefficients fixed
without the held-out scramble,

`mean[Y - beta f]`

is unbiased for `E[Y]`. The six tested features are normalized shifted Legendre
`L1/L2` functions of the soft-energy, soft-cosine, and decay-cosine Sobol
coordinates. Their exact uniform expectations, rather than empirical feature
means, define the zero.

Coefficients were trained by leave-one-independent-scramble-out ridge regression.
The fixed target values were not used in the regression.

## Result

All three predeclared models fail the retrospective gate:

| model | worst target-normalized SD ratio | largest Richardson-real ratio |
|---|---:|---:|
| `soft_L12` | 1.261 | 1.431 |
| `soft_L12_angular_L2` | 1.374 | 1.682 |
| `all_main_L12` | 1.295 | 1.413 |

The eight high-magnitude events also do not occupy one simple soft or angular
corner. Generic low-order polynomials are therefore not the measured variance
mechanism.

## Decision

- No polynomial-control pilot is authorized.
- Do not spend new kernels on these feature models.
- Preserve the unbiased-estimator construction for a physically correlated
  low-fidelity observable.
- The promising candidate discovered in the same audit is the `E040` nonlocal
  vector, which is tested directly in checkpoint 5043.

## Evidence

- Generator: `scripts/Y5_R2FR_5042_unbiased_outer_control_variate_gate.py`
- Result: `source-intake/functional_rg/5042/unbiased_control_variate_gate.json`
- Model table: `source-intake/functional_rg/5042/retrospective_model_comparison.csv`
- Component table: `source-intake/functional_rg/5042/retrospective_component_ratios.csv`
- Locked rejection: `source-intake/functional_rg/5042/locked_independent_pilot_contract.json`
- Validation: `source-intake/mts_residuals/P8_Y5_BRR545_5042_VALIDATION.csv`

This is an internal estimator-design result, not production `hhh`, local-GR,
Newton, Maxwell, or full-MTS evidence.
