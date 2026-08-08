# 5301 — Adaptive local-cell residual integration

## Result

Six new off-diagonal sign orbits complete a three-by-three angular
cell around the order-four interior hotspot. The calculation subtracts
the exact tensor-product even interpolant represented by the accepted
order-eight Gauss rule, then integrates the remaining local residual.

- signed nodes: `24`;
- exact scans: `384`;
- off-contour poles integrated without fitted residues:
  `16`;
- integration arithmetic precision:
  `80` decimal digits;
- maximum analytic/order-eight pole-kernel error:
  `1.35283843834e-11`;
- component evaluations: `388416`;
- maximum nodewise energy change:
  `0.00036052595146`;
- cell interval:
  `[0.260399303825, 0.430592943117]`;
- bilinear-to-biquadratic residual change:
  `1.50515075587`;
- boundary/center residual ratio:
  `8.06969669756`;
- biquadratic local correction:
  `-0.450528120112 +
  -0.077114883697 i`;
- corrected global candidate:
  `6.06184488219 +
  2.09005042237 i`.

Decision: **LOCAL_CELL_RESOLVED_BUT_MODEL_UNSTABLE__REFINE_CORE**.

## Acceptance gates

- `adaptive_atlas_accepted`: **PASS**
- `all_contour_silence_controls_pass`: **PASS**
- `all_nodes_pass_energy_gate`: **PASS**
- `all_residual_samples_finite`: **PASS**
- `all_twenty_four_node_runs_completed`: **PASS**
- `claims_locked_false`: **PASS**
- `formalization_workbench_unchanged`: **PASS**
- `integration_precision_initialized`: **PASS**
- `order8_interpolant_reproduces_outer_total`: **PASS**
- `six_new_sign_orbits_complete`: **PASS**
- `three_by_three_cell_complete`: **PASS**

Validation: **PASS**.

## Claim boundary

This checkpoint performs a real two-dimensional local residual
integration. It does not claim full angular convergence unless the
local model is stable and the residual is shown to be contained or
bounded outside the cell. It makes no full phase-space, UV, local-GR,
or full-MTS claim.
