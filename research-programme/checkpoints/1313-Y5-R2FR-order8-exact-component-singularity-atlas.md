# 5297 — Order-eight exact-component singularity atlas

## Result

The order-eight tensor grid contains `64`
nodes. Every regulator/component track was scanned independently.

- independent scans: `1024`;
- geometric poles: `1392`;
- exact-active roots: `922`;
- material poles: `374`;
- bounded ambiguous residues:
  `89`;
- aggregate ambiguous relative bound:
  `1.01715701407e-06`;
- high-precision pole repairs:
  `14`;
- same-component radius repairs:
  `2`;
- cluster-deflated removable roots:
  `2`;
- refined endpoint terms:
  `272`;
- maximum endpoint cancellation residual:
  `2.31035280933e-14`.

## Acceptance gates

- `all_1024_exact_scans_complete`: **PASS**
- `all_ambiguous_bounds_valid`: **PASS**
- `all_exact_active_roots_have_residue_classification`: **PASS**
- `all_geometric_poles_exact_mask_classified`: **PASS**
- `all_material_poles_valid_for_subtraction`: **PASS**
- `all_nodewise_endpoint_cancellations_pass`: **PASS**
- `all_roots_resolved_by_control_or_bound`: **PASS**
- `all_singular_endpoint_controls_pass`: **PASS**
- `ambiguous_global_bound_below_budget`: **PASS**
- `claims_locked_false`: **PASS**
- `cluster_deflated_removable_bounds_valid`: **PASS**
- `endpoint_coefficients_complete`: **PASS**
- `endpoint_grid_complete`: **PASS**
- `formalization_workbench_unchanged`: **PASS**
- `no_family_transport_used`: **PASS**
- `sixteen_exact_component_jobs_derived`: **PASS**
- `sixty_four_order8_nodes_written`: **PASS**

Validation: **PASS**.

## Claim boundary

This atlas only certifies the order-eight singular subtractions. The
order-eight energy integral and order-six/order-eight comparison remain
the next numerical gate.
