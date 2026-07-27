# 5241 — Decay-angle order-9 causal-topology resolution

## Purpose

Extend 5240 from nested outer orders 3 and 5 to order 9 without discarding its five completed causal nodes. Four new nodes are evaluated through the complete 5239 inner continuation, dynamic winding, pole subtraction, and E040/E020 extrapolation machinery.

## Derived measure

The parent Sobol map gives `du_soft du_decay = (d cos_soft/2)(d cos_decay/2)`, so the two-angle Jacobian remains exactly `1/4`.

## Results

- Nodes: `9` total; `5` reused and `4` new.
- Order-3→5 relative difference: `0.64847386793`.
- Order-5→9 relative difference: `0.869464996278`.
- Order-9 two-angle value: `18.92637003551503 -0.5644314513109665 i`.
- Degree-5..8 Chebyshev tail fraction: `0.767493823116`.
- Maximum/median node magnitude ratio: `9.53946919094`.
- Bracketed outer topology-transition intervals: `8`.
- Runtime: `6357.823 s`.

## Decision

`HOLD_OUTER_CUBATURE__DERIVE_PIECEWISE_DECAY_TOPOLOGY`

Failed gates: `WINDING_INTERVAL_TRACK_RESOLUTION`, `OUTER_ORDER_3_TO_5_CONVERGENCE`, `OUTER_ORDER_5_TO_9_CONVERGENCE`, `ORDER9_CHEBYSHEV_TAIL_DECAY`.

## Interpretation

A failed order-5→9 or high-order Chebyshev-tail gate is not repaired by loosening a tolerance. Together with a change in active/geometric pole count between adjacent decay-angle nodes, it means the next mathematical object is a piecewise decay-angle topology map: localize each transition, derive its causal winding jump, and integrate regular subdomains separately.

## Claim boundary

This remains one fixed-soft-energy, cutoff two-angle slice. It is not a numerical UV coefficient, local-GR derivation, or full-MTS result.

## Next exact target

Localize the intervals in `decay_angle_topology_transition_intervals.csv` by bisection in decay cosine, construct the outer dynamic-winding map, and test a piecewise pole-subtracted outer integral before adding soft-energy integration.
