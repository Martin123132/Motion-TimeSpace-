# 5272 — Exact analytic boundary surface and event solver

## Scope

This checkpoint replaces the nearest-coordinate energy tracking in 5271
with a derived boundary equation. It is private, leaves the formalization
workbench untouched, and makes no UV, local-GR, or full-MTS claim.

## Exact reduction

Let

- `x` be the soft energy;
- `q = sqrt(1-x)`;
- `a` be the soft-direction cosine;
- `d` be the decay-direction cosine;
- `r = a d - sqrt(1-a^2)sqrt(1-d^2)` in the sourced `phi=pi` chamber;
- `s=+1` for `direct:g1` and `s=-1` for `direct:g2`;
- `t=+0.3` for plus roots and `t=-0.3` for minus roots.

The unit-circle root-margin boundary is exactly

`F=(a-t)(1+s r)q^2+2s(d-a r)q+(a+t)(s r-1)=0`.

This is quadratic in `q`, so each angular point has direct algebraic
soft-energy inversion. With the half-angle coordinate
`u=sqrt((1-c)/(1+c))`, `(1+u^2)^2 F` is quartic in the scanned angle.
Interior folds therefore satisfy `P=0` and `dP/du=0`; crossings satisfy
`P_i=P_j=0`. Checkpoint 5272 solves the corresponding resultants.

## Results

- Shared surfaces: **7**.
- Raw 5271 boundary rows reproduced: **3582**.
- Ladder surface slices checked: **1736**.
- Exact endpoint events: **32**.
- Physical interior folds: **12**.
- Physical surface crossings: **15**.
- Maximum raw equation residual: `1.60517210634e-10`.
- Maximum energy inversion residual: `3.2293598351e-10`.
- Maximum ladder coordinate residual: `5.79104542098e-11`.
- Maximum fold-system residual: `4.04537514598e-15`.
- Maximum crossing-system residual: `8.40993941154e-15`.
- 5271 coarse events confirmed: **38/50**.

The unmatched 5271 event rows are not hidden failures. They are explicitly
marked as nearest-coordinate artifacts superseded by the labelled analytic
equations.

## Acceptance gates

- `all_crossing_candidates_classified`: **PASS**
- `all_crossing_residuals_tight`: **PASS**
- `all_fold_candidates_classified`: **PASS**
- `all_fold_residuals_tight`: **PASS**
- `all_ladder_roots_reproduced`: **PASS**
- `all_raw_boundaries_reproduced`: **PASS**
- `claims_locked_false`: **PASS**
- `event_count_balance_closes`: **PASS**
- `formalization_workbench_unchanged`: **PASS**
- `hard_denominators_nonzero`: **PASS**
- `parent_5271_accepted`: **PASS**
- `surface_inventory_closed`: **PASS**

Validation: **PASS**.

## Claim boundary

The exact shared boundary law, direct soft-energy inversion, algebraic
endpoint events, and resultant-isolated events on the sampled transverse
slices are accepted if validation passes. This is not yet a proof of the
complete two-angle continuum topology, the final phase-space coefficient,
the UV coefficient, local GR, or the full MTS theory.

## Next target

Use the exact quadratic/quartic law to continue the event curves in the
second angular coordinate, then construct topology-safe joint angular and
soft-energy cubature without an interpolated chamber mask.
