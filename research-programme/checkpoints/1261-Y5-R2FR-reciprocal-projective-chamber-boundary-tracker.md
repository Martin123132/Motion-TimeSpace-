# 5245 — Reciprocal-projective chamber-boundary tracker

## Exact transport law

Every non-synthetic chamber endpoint is a root of `z^2 - 2 eta z + 1 = 0`. Hence its two sheets obey `z_+ z_- = 1`; they are one reciprocal pair on `CP1`, not two independently selectable square roots.

The tracker evaluates the non-cancelling root, obtains its partner by exact reciprocal division, and labels the pair at each homotopy node by minimum bottleneck chordal distance followed by minimum total chordal distance. This remains regular through the zero/infinity chart exchange that defeated the Euclidean square-root rule.

## Resolution contract

A state is accepted only after two consecutive ladder resolutions satisfy both projective gates, both reciprocity gates, the boundary-polynomial gate, and return identical winding integers.

## Results

- Ten-case two-resolution convergence: `10/10`.
- 5242 high-resolution control states reproduced: `5/5`.
- Maximum accepted collision-pair projective step: `0.0229946659667`.
- Maximum accepted boundary-pair projective step: `0.0179549809361`.
- Maximum accepted boundary reciprocal residual: `2.28878339926e-16`.
- Maximum accepted normalized boundary-polynomial residual: `3.33066711468e-16`.
- Legacy Q03 cache states retained: `1/5`.
- Converged Q03 paired states: `[(0, 0)]`.
- Runtime: `470.909 s`.

## Decision

`SUPERSEDE_Q03_LEGACY_WINDING_CACHE__REBUILD_WITH_RECIPROCAL_PROJECTIVE_BOUNDARIES`

## Interpretation

The old near-unit boundary jump was not a physical topology signal. It came from independently transporting one principal-square-root representative through a reciprocal zero/infinity chart exchange. The paired polynomial transport removes that discontinuity while preserving the independently established 5242 controls.

## Claim boundary

This is a topology/transport correction on ten bounded reference cases. It does not supply a corrected Q03/Q05 integral, a numeric UV coefficient, local GR, or full MTS.

## Next exact target

Invalidate only the legacy Q03 winding cache rows whose states fail this paired convergence contract, rebuild the Q03 interval topology with the reciprocal-projective endpoint tracker, and then rerun the Q03 inner slice. Do not return to uniform 5243 state doubling.
