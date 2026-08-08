# 5302 — Mask-edge integrability and limit-order audit

## Result

The unstable 5301 cell is not a generic interpolation failure. Its largest
residual is generated when the exact `MC04` mask turns on at the transverse
hard-leg surface

`F_{+1,-0.3}(sqrt(1-E),-s,-d)=0`.

At the sourced witness slice,

- `E=0.1100816778468012`;
- `|d|=0.338281138367`;
- `|s|_edge=0.4265116840664105`;
- `|F|=0`;
- `dF/d|s|=0.0854532826081`.

The remaining `MC04/MC12` sign-orbit terms cancel to relative error
`2.32686240604e-16`, leaving one
newly active signed `MC04` contribution. This proves why a smooth 3x3
polynomial model fails.

The boundary-aligned finite-regulator integrals over the first
`0.1` in `|s|-|s|_edge` are

- `E040`: `-132.72401997 +
  -130.421874785 i`;
- `E020`: `-132.78110822 +
  -136.410302235 i`;
- `2 E020 - E040`: `-132.83819647 +
  -142.398729685 i`.

The maximum order-4/order-8 edge-integral change is
`7.73699000395e-05`. The
`|I_E020|/|I_E040|` ratio is
`1.02302782179`.

Decision: **MASK_EDGE_DERIVED_AND_FINITE_REGULATORS_CONVERGED__BUILD_REGULATOR_LADDER_BEFORE_FULL_CUBATURE**.

## Consequence

The earlier global angular rules sampled a threshold edge as though it were
a smooth ridge. Their values remain diagnostics, not a converged
phase-space coefficient. The correct next calculation is a regulator ladder
with boundary-aligned angular integration. Only that can distinguish a
finite regulator-zero limit from a pinch divergence or distributional
finite-part requirement.

## Acceptance gates

- `all_outputs_finite`: **PASS**
- `both_finite_regulators_integrated`: **PASS**
- `claims_locked_false`: **PASS**
- `edge_quadrature_converged`: **PASS**
- `exact_mask_edge_solved`: **PASS**
- `formalization_workbench_unchanged`: **PASS**
- `integration_precision_initialized`: **PASS**
- `mask_edge_is_transverse`: **PASS**
- `single_component_edge_reduction_verified`: **PASS**

Validation: **PASS**.

## Claim boundary

This checkpoint derives one exact edge mechanism and integrates the two
available finite regulators. It does not establish the regulator-zero
limit, full angular convergence, the phase-space coefficient, a UV
coefficient, local GR, or the full MTS theory.
