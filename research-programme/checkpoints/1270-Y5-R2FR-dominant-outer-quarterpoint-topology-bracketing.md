# 5254 - Dominant outer quarterpoint topology bracketing

## Calculation

Checkpoint 5253 localized more than eighty percent of its cancellation-safe first-level discrepancy to I01 and I06. Each interval is now sampled at both quarter points. The five-point sequence is audited for the canonical active-pole signature before any smooth Simpson Richardson formula is allowed.

- `B01L` at `-0.865337912957`: `(627.0943504746973+1311.3101021115842j)`, active poles `2`.
- `B01R` at `-0.757493469173`: `(-878.7534271510075+0.0007209145067452092j)`, active poles `0`.
- `B06L` at `0.757493469173`: `(1785.778579701395-0.004004244128558445j)`, active poles `0`.
- `B06R` at `0.865337912957`: `(-951.6748534529053-1311.3103684830774j)`, active poles `2`.

## Topology test

- `I01` active-count sequence `0|2|2|0|0`; topology uniform `False`; raw |S2-S1| `30.2994559748`; Richardson authorized `False`.
- `I06` active-count sequence `0|0|2|2|0`; topology uniform `False`; raw |S2-S1| `50.6596118861`; Richardson authorized `False`.

The topology is not uniform, so `|S2-S1|/15` is deliberately not reported as an error estimate. The raw difference remains a diagnostic only.

## Transition brackets

- `I01_T00`: `[-0.919260134849, -0.865337912957]`, counts `0 -> 2`, next midpoint `-0.892299023903`.
- `I01_T01`: `[-0.811415691065, -0.757493469173]`, counts `2 -> 0`, next midpoint `-0.784454580119`.
- `I06_T00`: `[0.757493469173, 0.811415691065]`, counts `0 -> 2`, next midpoint `0.784454580119`.
- `I06_T01`: `[0.865337912957, 0.919260134849]`, counts `2 -> 0`, next midpoint `0.892299023903`.

- Maximum bracket/parent-width ratio: `0.25`.
- Nonclaim two-panel adaptive value (inner 512): `(12.068415573842124-0.9370468892575871j)`.
- Adaptive inner 128/512 relative difference: `1.51342955489e-07`.

## Decision

`ADOPT_DOMINANT_TOPOLOGY_BRACKETS__SOLVE_OUTER_BOUNDARIES`

## Physics boundary

The large I01/I06 curvature is now identified as a change in the active causal-residue sector, not merely a high-degree smooth polynomial. This invalidates blind global-order escalation and smooth-panel error claims across those regions.

No numeric p8 coefficient, all-operator local-GR result, or full-MTS claim is promoted.

## Next exact target

Evaluate the four predeclared bisection coordinates in the transition-bracket table. Continue bracketed bisection until the outer-boundary location uncertainty times a measured residue-envelope bound fits inside the allocated outer error budget. Integrate separately on each constant-topology chamber.
