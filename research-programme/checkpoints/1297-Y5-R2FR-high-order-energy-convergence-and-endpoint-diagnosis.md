# 5281 — High-order energy convergence and endpoint diagnosis

## Purpose

Checkpoint 5280 proved the corrected pole-subtraction mechanism at
orders two and four. This checkpoint raises the fixed-angle energy
calculation to orders 4, 8, and 16 using the same exact panels, true
local-limit residues, and algebraic branch selector.

## Results

- order `16`: eight `-79.9474445694-5.68150504244i`; six `-79.9474061408-5.68150504244i`; hidden `-3.84285313478e-05+2.13500028396e-14i`.
- order `4`: eight `73.9984259453-13.9756620603i`; six `73.9984643738-13.9756620603i`; hidden `-3.84285313478e-05+2.13500028396e-14i`.
- order `8`: eight `-13.3369839596-14.2851785519i`; six `-13.3369455311-14.2851785519i`; hidden `-3.84285313478e-05+2.13500028396e-14i`.

- order 4 to 8 relative change:
  `1.1597382124`;
- order 8 to 16 relative change:
  `0.837986078227`;
- endpoint-panel fraction of absolute regular-remainder mass:
  `0.0150198736398`;
- fixed-angle convergence accepted:
  `False`.

The order-4 value reproduces checkpoint 5280 to relative error
`0`.

## Acceptance gates

- `all_active_roots_refined`: **PASS**
- `audited_coefficients_converged`: **PASS**
- `claims_locked_false`: **PASS**
- `component_totals_close_order_totals`: **PASS**
- `endpoint_diagnosis_complete`: **PASS**
- `formalization_workbench_unchanged`: **PASS**
- `order4_reproduces_5280`: **PASS**
- `orders_4_8_16_completed`: **PASS**
- `parent_5280_accepted`: **PASS**

Validation: **PASS**.

## Claim boundary

This checkpoint decides whether ordinary high-order panel quadrature is
enough. If order 8 to 16 is still unstable, the next move is not blind
order inflation: the endpoint scaling must be derived and subtracted.
No angular, full phase-space, UV, local-GR, or full-MTS claim is made.
