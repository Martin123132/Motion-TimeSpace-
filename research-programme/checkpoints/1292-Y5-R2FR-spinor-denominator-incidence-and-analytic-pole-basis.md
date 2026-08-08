# 5276 — Spinor denominator incidence and analytic pole basis

## Purpose

Checkpoint 5275 replaced the old six-component source-event list with
an eight-component generic pole basis. This checkpoint derives that
basis from the spinor denominators rather than another displacement
scan.

## Label dictionary

For a rotated internal direction, write

`e=sqrt((1-c)/(1+c))`,
`h=(p_x+i p_y)/(E+p_z)`, and
`hbar=(p_x-i p_y)/(E+p_z)`.

The four roots are

`z_+u=e/h`, `z_+v=hbar/e`,
`z_-u=-1/(e h)`, and `z_-v=-e hbar`.

Therefore `plus/minus` selects right external leg `0/4`, while `u/v`
selects angle/square chirality `0/1`.

## Direct sector

Each term in the hhh product contains one right five-point KLT factor
of a fixed chirality. A mixed `u/v` collision therefore cannot supply
two denominators to the same term and is at most simple.

For same-chirality pairs, the script counts cyclic MHV denominator
incidence and subtracts:

1. zeros supplied by the KLT momentum kernel;
2. four powers supplied when the special leg equals the pole source.

The surviving direct double components are
`MC02, MC03, MC04, MC07, MC08, MC12`.

## Endpoint sector

The gravitational soft factor appears to have a double collinear
denominator, but its leading numerator is

`sum_l <0l>[l3] = <0|sum_l p_l|3] = 0`.

Momentum conservation therefore reduces it to a simple pole. The
endpoint four-point KLT factor contributes one further simple decay
pole. Exactly one chirality/special-leg term survives for each endpoint
double:

- MC14: `right_chirality=0;special=2;decay_leg=1`;
- MC15: `right_chirality=0;special=1;decay_leg=2`.

All other endpoint-labelled components lack a soft-g3 and decay pole
inside the same additive summand.

## Theorem

- Analytic almost-everywhere double basis:
  `MC02, MC03, MC04, MC07, MC08, MC12, MC14, MC15`.
- Analytic at-most-simple complement:
  `MC01, MC05, MC06, MC09, MC10, MC11, MC13`.

This agrees exactly with the 150 arbitrary-precision limits in 5275.

## Acceptance gates

- `analytic_basis_matches_5275`: **PASS**
- `analytic_eight_component_basis`: **PASS**
- `analytic_seven_component_complement`: **PASS**
- `claims_locked_false`: **PASS**
- `direct_label_dictionary_closes`: **PASS**
- `direct_leading_terms_exact`: **PASS**
- `direct_term_matrix_complete`: **PASS**
- `endpoint_decay_dictionary_closes`: **PASS**
- `endpoint_leading_terms_exact`: **PASS**
- `formalization_workbench_unchanged`: **PASS**
- `mixed_chirality_direct_pairs_at_most_simple`: **PASS**
- `parent_5275_accepted`: **PASS**
- `soft_double_leading_identity_cancels`: **PASS**

Validation: **PASS**.

## Claim boundary

The result is analytic and almost everywhere: coefficient-zero or
collision-degeneracy submanifolds may lower pole order but have no
volume measure in the intended cubature. It is not a
pointwise-everywhere theorem and does not yet provide the integrated
phase-space coefficient, UV coefficient, local GR, or full MTS theory.

## Next target

Insert all eight analytically retained components into the exact Boolean
masks from 5273/5274 and perform a low-order, two-regulator joint
cubature. MC02 and MC08 must be included; the old six-component result
must not be reused.
