# 5283 — Two-pole stored-node reassembly

## Purpose

Checkpoint 5282 proved that MC04 and MC12, not MC04 alone, are the
material fixed-angle energy poles. This checkpoint reuses all 20,608
already evaluated 5281 nodes, subtracts both sourced poles, restores
their analytic logarithmic integrals, and retests orders 4, 8, and 16.
No local-limit coefficient or root is reevaluated.

## Physical order sequence

- order 16: `-2.23337533789+2.12934507074i`
- order 4: `-2.23277869161+2.13012114681i`
- order 8: `-2.23271452954+2.13108141474i`

- order 4 to 8 relative change:
  `0.000311811789024`;
- order 8 to 16 relative change:
  `0.000601922262726`;
- fixed-angle convergence:
  `True`.

The largest order-16 regular panel is `EP033` with
magnitude
`0.0606048867978`.

## Audit

- old MC04-only replay error:
  `9.91437452893e-14`;
- raw-integral replay error:
  `6.84253344278e-14`;
- node reevaluations: `0`.

- `all_reassembled_totals_finite`: **PASS**
- `claims_locked_false`: **PASS**
- `component_sum_crosscheck_passes`: **PASS**
- `formalization_workbench_unchanged`: **PASS**
- `material_pole_set_is_MC04_MC12`: **PASS**
- `old_MC04_replay_reproduces_5281`: **PASS**
- `raw_integral_reproduces_5281`: **PASS**
- `stored_node_count_preserved`: **PASS**

Validation: **PASS**.

## Claim boundary

This is a fixed-angle energy convergence gate only. It does not yet
authorize a full angular coefficient, UV claim, local-GR claim, or full
MTS claim.
