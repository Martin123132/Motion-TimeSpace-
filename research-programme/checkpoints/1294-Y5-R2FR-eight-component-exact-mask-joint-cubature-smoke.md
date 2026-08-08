# 5278 — Eight-component exact-mask joint cubature smoke

## Purpose

Checkpoint 5277 supplied the true pointwise double-residue evaluator.
This checkpoint performs the first actual three-dimensional interior
integration over soft energy, soft cosine, and decay cosine using the
analytic eight-component pole basis.

## Integrand

Each active component contributes

`Delta w * orientation * C_2 / (R G (g_1'-g_2'))`.

The exact Boolean mask is evaluated before the expensive arbitrary-
precision limit. The two reciprocal representatives give the same mask,
and the historical 5239 winding intervals are replayed as a sign check.
That replay finds
`8` old
endpoint-adjacent false negatives and
`0` false
positives. All discrepancies are one-sided corrections supplied by the
analytic mask, rather than sign reversals.

## Domain and measure

- energy: `[0.0001, 0.9999]`;
- soft cosine: `[-0.995, 0.995]`;
- decay cosine: `[-0.995, 0.995]`;
- normalized angular measure: `d cos(theta_s) d cos(theta_d) / 4`;
- regulator combination: `2 E020 - E040`;
- tensor Gauss orders: `[2, 3]`.

## Numerical results

- order `2`: eight `13.6823992413-3.98771538921e-06i`; true-six `14.040593454-3.9917330916e-06i`; hidden fraction `0.0261791960853`.
- order `3`: eight `1.38682802704-1.04165639781e-06i`; true-six `2.4519248861-1.03142178174e-06i`; hidden fraction `0.768009326529`.

Order-to-order relative changes:

- `eight_component_integral`: `0.898641458813`.
- `hidden_MC02_MC08_integral`: `0.663697991775`.
- `six_component_integral`: `0.825368856798`.

The largest local-limit relative change is
`3.32389208241e-17` and the largest
root residual is `7.16869466128e-80`.

## Acceptance gates

- `all_active_coefficients_converged`: **PASS**
- `all_active_nodes_evaluated`: **PASS**
- `all_active_roots_refined`: **PASS**
- `all_active_winding_deltas_nonzero`: **PASS**
- `all_totals_finite`: **PASS**
- `all_transport_paths_passed`: **PASS**
- `claims_locked_false`: **PASS**
- `complete_two_regulator_node_matrix`: **PASS**
- `exact_mask_implementations_agree`: **PASS**
- `formalization_workbench_unchanged`: **PASS**
- `hidden_components_actively_integrated`: **PASS**
- `historical_replay_is_one_sided_endpoint_correction`: **PASS**
- `no_quadrature_node_on_mask_boundary`: **PASS**
- `parent_5277_accepted`: **PASS**

Validation: **PASS**.

## Claim boundary

This is a real integration smoke, not another inventory. It proves that
the exact eight-component integrand can be transported, masked,
evaluated, and integrated on a finite interior grid. It does not yet
establish the coefficient: discontinuous mask chambers require adapted
cubature, orders two and three are only diagnostics, and the excluded
angular endpoint caps still require bounds or restoration.
