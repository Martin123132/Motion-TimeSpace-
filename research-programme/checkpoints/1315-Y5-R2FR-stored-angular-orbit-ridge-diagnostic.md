# 5299 — Stored angular-orbit ridge diagnostic

## Result

The accepted order-two, order-four, order-six, and order-eight node
shards contain `120` signed angular nodes, which reduce exactly to
`30` parity orbits. The order-six/order-eight
change is `0.138649699702`.

The dominant order-four orbit is interior, at
`(|s|,|d|)=(0.338281138367,
0.338281138367)`, and contributes
`20.4377872409` in
magnitude. Neither the order-six nor order-eight Gauss grid samples
that location. A smooth endpoint-regularized polynomial trained on the
order-eight grid misses the stored order-four orbit by a weighted
residual of
`17.1768316888`.
This is evidence for an unresolved interior ridge, not merely an
angular endpoint tail.

## Acceptance gates

- `all_120_stored_nodes_reassembled_into_30_orbits`: **PASS**
- `all_four_order_totals_reproduced`: **PASS**
- `claims_locked_false`: **PASS**
- `dominant_order4_orbit_is_interior`: **PASS**
- `formalization_workbench_unchanged`: **PASS**
- `higher_order_grid_does_not_sample_order4_hotspot`: **PASS**
- `order6_order8_nonconvergence_reproduced`: **PASS**
- `stored_fit_exposes_non_smooth_cross_order_residual`: **PASS**
- `two_new_diagonal_bracket_orbits_selected`: **PASS**

Validation: **PASS**.

## Next target

Evaluate the two diagonal midpoint sign orbits bracketing the stored
order-four hotspot: eight new signed nodes in total. This directly
measures the ridge width before spending another global order-ten grid.

## Claim boundary

This diagnostic selects new nodes; it does not establish angular
convergence or a full phase-space, UV, local-GR, or full-MTS result.
