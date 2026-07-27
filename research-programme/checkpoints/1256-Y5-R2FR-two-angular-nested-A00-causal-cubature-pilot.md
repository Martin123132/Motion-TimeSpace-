# 5240 — Two-angular nested A00 causal cubature pilot

## Scope

This checkpoint promotes the 5239 one-dimensional `soft_cosine` slice to a nested integration over `soft_cosine` and `decay_cosine` at the inherited fixed `soft_energy=0.2630569525063038`.

## Measure derivation

The parent Sobol events use `u_soft,u_decay in [0,1]` with `cosine=2u-1`. Therefore

$$
du_{\rm soft}\,du_{\rm decay}=\frac14\,d c_{\rm soft}\,d c_{\rm decay}.
$$

The factor `1/4` is inherited from the parent sampling map; it is not fitted. Both cosine integrals use the explicit cutoff domain `[-0.995,0.995]`, covering normalized angular measure `0.990025000`.

## Construction

All 15 reciprocal components are continued along `decay_cosine`. The six material components generate 60 inner regulator jobs. The nine omitted components are re-evaluated at every outer node and regulator rather than assumed to stay zero.

At each outer node the complete 5239 machinery is rerun: inner branch continuation, piecewise integer-winding maps, causal pole classification, full-component residue fits, global pole subtraction, E040/E020 extrapolation, and dynamic merged-topology closure.

## Results

- Outer nodes: `5`.
- Nested regulator jobs: `60`.
- Outer branch tracks: `60`.
- Persistent structural-zero rows: `90/90`.
- Geometric poles: `44`.
- Dynamically active poles: `4`.
- Accepted residue fits: `4/4`.
- Outer order-3 to order-5 relative difference: `0.64847386793`.
- Nested inner order-128 to order-512 relative difference: `4.94154960008e-07`.
- Order-5/order-512 normalized two-angular value: `35.37918950094151 -1.147062606374593 i`.
- Cache: node hits `0`, winding hits `0`, winding misses `60`.
- Runtime: `2558.654 s`.

## Decision

`HOLD_TWO_ANGULAR_CUBATURE_PENDING_FAILED_GATE`

## Claim boundary

This is not yet the physical multidimensional A00 coefficient. Soft energy remains fixed, the angular endpoint strips carry unbounded omitted measure `0.009975000`, and only the nested outer orders 3 and 5 have been run. No numeric-UV, local-GR, or full-MTS claim follows.

## Next target

Add the nested order-9 outer rule and an angular-cutoff ladder, then carry the resulting two-angular density into the final soft-energy integration with its endpoint subtraction.

## Validation

- `SOURCE_PATHS_EXIST_AND_MATCH`: `PASS`.
- `NESTED_JOB_COUNT`: `PASS`.
- `OUTER_BRANCH_TRACK_STABLE`: `PASS`.
- `STRUCTURAL_ZEROS_PERSIST`: `PASS`.
- `DYNAMIC_CLOSURE`: `PASS`.
- `WINDING_INTERVAL_TRACK_RESOLUTION`: `FAIL`.
- `ACTIVE_POLES_FITTED`: `PASS`.
- `ALL_OUTER_NODES_PASS_INNER_GATES`: `PASS`.
- `OUTER_RULE_MOMENTS`: `PASS`.
- `OUTER_ORDER_3_TO_5_CONVERGENCE`: `FAIL`.
- `NESTED_INNER_CONVERGENCE`: `PASS`.
- `FORMALIZATION_WORKBENCH_UNCHANGED`: `PASS`.
- `RUNTIME_BOUNDED`: `PASS`.
- `CLAIMS_REMAIN_FALSE`: `PASS`.
