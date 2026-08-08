# 5279 — Algebraic reciprocal branch selector

## Purpose

The 5278 integrand was correct, but every cubature node still inherited
an expensive source-to-node continuation. This checkpoint removes that
numerical path dependency.

## Selector

For each component:

1. solve the representative collision equation and choose its
   maximum-modulus root;
2. solve the reciprocal collision equation and choose its
   minimum-modulus root;
3. use the representative when its modulus is at least one, otherwise
   use the reciprocal.

The spinor `u/v` root dictionary and reciprocal component construction
give `R_rep R_rec=1` away from degeneracy sets. The exact Boolean mask
owns the unit-circle boundary.

## Evidence

- Stored high-precision/transport rows replayed:
  `640`;
- maximum replay chordal distance:
  `8.06041123487e-15`;
- random interior stress rows:
  `4096`;
- maximum stress reciprocal residual:
  `3.76541968142e-13`;
- minimum selected-root unit margin:
  `0.000630959604413`;
- selected roles:
  `{'reciprocal': 1138, 'representative': 2958}`.

## Acceptance gates

- `all_replay_pairs_reciprocal`: **PASS**
- `all_stored_transports_reproduced`: **PASS**
- `all_stress_pairs_reciprocal`: **PASS**
- `all_stress_selectors_pass`: **PASS**
- `both_selector_roles_exercised`: **PASS**
- `claims_locked_false`: **PASS**
- `complete_stress_matrix`: **PASS**
- `formalization_workbench_unchanged`: **PASS**
- `parent_5278_accepted`: **PASS**
- `stress_sample_avoids_degeneracy_sets`: **PASS**
- `theorem_covers_eight_components`: **PASS**

Validation: **PASS**.

## Claim boundary

The selector is an almost-everywhere algebraic replacement for branch
transport in volume cubature. It is not a theorem on the unit-circle or
multiple-root degeneracy sets and does not establish the phase-space
coefficient, UV coefficient, local GR, or full MTS framework. Its
practical consequence is important: the next energy-first calculation
can spend its cost on pole subtraction and convergence rather than
thousands of continuation steps.
