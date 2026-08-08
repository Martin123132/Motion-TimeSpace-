# 5280 — Algebraic-selector energy pole-subtracted smoke

## Purpose

This checkpoint inserts the 5279 algebraic selector into the true
eight-component pointwise evaluator and returns to the energy-first
strategy required by the nonconverged 5278 tensor result.

## Construction

- exact energy mask boundaries: `2`;
- composite panels: `46`, maximum width
  `0.025`;
- sourced geometric poles refitted with true local-limit residues:
  `2`;
- unique component evaluations:
  `4432`;
- audited local-limit changes: maximum
  `1.32442910203e-12`.

The MC04 simple pole is subtracted analytically as
`A/(E-E_p)`, the regular remainder is integrated panel by panel, and
`A[log(E_max-E_p)-log(E_min-E_p)]` is restored exactly.

## Fixed-angle results

- order `2`: raw `13.4202887003-0.067897611795i`; subtracted eight `13.4699285625-14.2911658744i`; subtracted six `13.4699669909-14.2911658744i`.
- order `4`: raw `74.0293691681-0.333391617529i`; subtracted eight `73.9984259453-13.9756620603i`; subtracted six `73.9984643738-13.9756620603i`.

Raw order change:
`0.818716247561`.

Pole-subtracted order change:
`0.803771622701`.

## Acceptance gates

- `algebraic_evaluator_produced_active_rows`: **PASS**
- `all_active_roots_refined`: **PASS**
- `audited_coefficients_converged`: **PASS**
- `claims_locked_false`: **PASS**
- `component_sum_closes`: **PASS**
- `composite_panels_cover_domain`: **PASS**
- `formalization_workbench_unchanged`: **PASS**
- `one_true_limit_pole_fit_per_regulator`: **PASS**
- `parent_5279_accepted`: **PASS**
- `pole_subtraction_improves_low_order_stability`: **PASS**
- `two_exact_energy_mask_boundaries_recovered`: **PASS**

Validation: **PASS**.

## Claim boundary

This is the first corrected energy-first calculation using the exact
eight-component basis and no path tracker. It validates the mechanism
and subtraction pipeline, but orders two and four are deliberately only
a smoke test. Higher energy orders must converge before restoring the
two angular integrations; no phase-space, UV, local-GR, or full-MTS
claim follows here.
