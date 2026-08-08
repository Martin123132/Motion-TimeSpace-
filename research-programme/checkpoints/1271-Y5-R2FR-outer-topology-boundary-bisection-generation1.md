# 5255 - Outer topology-boundary bisection generation 1

## Calculation

The four predeclared checkpoint-5254 transition midpoints were evaluated with the same reciprocal-projective topology and corrected-inner-slice engine. A midpoint is assigned only when its complete active-pole signature equals exactly one bracket endpoint signature.

- `C01A` / `I01_T00` at `-0.892299023903`: `(966.8994645726191+1330.5431007929958j)`, active poles `2`.
- `C01B` / `I01_T01` at `-0.784454580119`: `(-3872.2504417637733+5.1629860775567895j)`, active poles `0`.
- `C06A` / `I06_T00` at `0.784454580119`: `(-53.26027931914561-3415.1593904588767j)`, active poles `2`.
- `C06B` / `I06_T01` at `0.892299023903`: `(-1267.1776551477276-1330.5433763445476j)`, active poles `2`.

## Narrowed brackets

- `I01_T00` -> `[-0.919260134849, -0.892299023903]`, counts `0 -> 2`, width `0.026961110946`, next `-0.905779579376`.
- `I01_T01` -> `[-0.811415691065, -0.784454580119]`, counts `2 -> 0`, width `0.026961110946`, next `-0.797935135592`.
- `I06_T00` -> `[0.757493469173, 0.784454580119]`, counts `0 -> 2`, width `0.026961110946`, next `0.770974024646`.
- `I06_T01` -> `[0.892299023903, 0.919260134849]`, counts `2 -> 0`, width `0.026961110946`, next `0.905779579376`.

All four brackets are halved without a third topology.

## Boundary-location error identity

For a boundary known only within width `delta_x`,

```text
|delta I_boundary| <= J delta_x sup |f_left_branch-f_right_branch|.
```

The rows below use measured endpoint differences only. They are planning proxies, not certified suprema or error bounds.

- `I01_T00` measured jump proxy `1890.90094368`, location proxy `12.7451975326`, provisional generations remaining `5`.
- `I01_T01` measured jump proxy `4345.50991847`, location proxy `29.2899437572`, provisional generations remaining `6`.
- `I06_T00` measured jump proxy `3878.83361811`, location proxy `26.1444158797`, provisional generations remaining `6`.
- `I06_T01` measured jump proxy `1900.58539193`, location proxy `12.8104734035`, provisional generations remaining `5`.

- Total measured location proxy: `80.9900305731`.
- Provisional outer absolute budget: `2.42094784195`.
- Maximum provisional generations remaining: `6`.

## Decision

`ADOPT_BISECTION_GENERATION1__CONTINUE_BOUNDARY_SOLVE`

## Claim boundary

No finite-sample envelope is promoted to a mathematical supremum. No outer-convergence, numeric p8, all-operator local-GR, or full-MTS claim follows.

## Next exact target

Run the four recorded generation-2 bisection coordinates. In parallel, derive a chamber-local residue-envelope bound from the fitted pole numerator and denominator derivatives; that bound, rather than sampled endpoint magnitudes, must own the stopping rule.
