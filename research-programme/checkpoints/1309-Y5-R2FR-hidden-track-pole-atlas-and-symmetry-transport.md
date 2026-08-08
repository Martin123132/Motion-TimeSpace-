# 5293 — Hidden-track pole atlas and symmetry transport

## Result

Checkpoint 5292 showed that the order-four failures were dominated by
`MC02/MC08`. The prior atlas had reused a visible component's track
because the family label matched. The exact parent inventory instead
contains distinct source-pair indices, anchors, chambers, and windings.
This checkpoint derives the missing `MC02` jobs from those parent-owned
fields. The low-energy relation `MC02(s,d)=MC08(s,-d)` fails globally
after exact-mask branch changes, so both hidden components are scanned
and residue-fitted independently rather than transported.

- independent hidden scans: `64`;
- geometric poles: `88`;
- exact-active owner roots: `52`;
- independently derived material hidden poles:
  `28`;
- removable hidden roots:
  `18`;
- bounded ambiguous hidden roots:
  `6`;
- maximum symmetry residual:
  `1`.

## Acceptance gates

- `MC02_MC08_global_decay_reflection_transport_rejected`: **PASS**
- `all_ambiguous_bounds_valid`: **PASS**
- `all_exact_active_roots_have_owner_residue`: **PASS**
- `all_hidden_geometric_poles_classified`: **PASS**
- `all_hidden_roots_resolved_by_control_or_bound`: **PASS**
- `all_hidden_rows_derived_independently`: **PASS**
- `all_sixty_four_hidden_scans_complete`: **PASS**
- `ambiguous_global_bound_below_budget`: **PASS**
- `at_least_one_new_hidden_material_pole`: **PASS**
- `claims_locked_false`: **PASS**
- `formalization_workbench_unchanged`: **PASS**
- `four_inventory_derived_jobs_complete`: **PASS**

Validation: **PASS**.

## Claim boundary

This is a derived numerical repair of the hidden source tracks, not a
phase-space or UV claim. Its effect must be checked by reassembling the
already evaluated order-four nodes.

## Next target

Replay the 5292 stored quadrature nodes with these supplemental poles.
