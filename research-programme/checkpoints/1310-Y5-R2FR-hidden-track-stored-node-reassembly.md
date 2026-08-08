# 5294 — Hidden-track stored-node reassembly

## Result

The 5292 order-four point evaluations were not rerun. The independently
derived `MC02/MC08` hidden-track poles were subtracted from the stored
quadrature values and their exact logarithmic integrals restored.

- supplemental pole terms:
  `34`;
- new point evaluations: `0`;
- maximum node energy `4 -> 8` change:
  `0.000439778521841`;
- order-four outer energy `4 -> 8` change:
  `0.00118665351741`;
- order-two to order-four angular change:
  `0.307096793334`;
- corrected order-four energy-eight total:
  `23.0266767446 +2.20313243819 i`;
- combined bounded-pole relative ambiguity:
  `5.40625846433e-06`.

## Acceptance gates

- `all_512_components_reassembled`: **PASS**
- `all_nodes_pass_inner_energy_gate`: **PASS**
- `all_values_finite`: **PASS**
- `claims_locked_false`: **PASS**
- `formalization_workbench_unchanged`: **PASS**
- `order4_outer_passes_energy_gate`: **PASS**
- `untouched_components_replay_exactly`: **PASS**
- `zero_new_point_evaluations`: **PASS**

Validation: **PASS**.

## Claim boundary

This can establish a valid order-two/order-four angular smoke only.
Order six remains necessary before angular convergence or a full
phase-space coefficient can be claimed.

## Next target

HIDDEN_TRACK_REPAIR_CLOSES_ENERGY__ANGULAR_NOT_CONVERGED__ADVANCE_ORDER6
