# 5242 — Homotopy branch resolution or collision classifier

## Purpose

Test whether the failed 5240/5241 winding-resolution gate is fixed by adding homotopy samples, or whether MC03/MC07 retain a finite branch jump near a collision.

## Resolution ladder

`1024 → 2048 → 4096 → 8192 → 16384 → 32768` homotopy steps.

## Results

- `Q01_E040_MC07_endpoint-positive`: `RESOLUTION_CONVERGED`; state `(-1,1)`; step `0.0459178440065`; ratio `0.503937355028`; reciprocal residual `9.53014747384e-12`; margin `1.08787423596e-06`.
- `Q07_E040_MC03_endpoint-positive`: `RESOLUTION_CONVERGED`; state `(-1,1)`; step `0.0459178440065`; ratio `0.503937355028`; reciprocal residual `9.53014747384e-12`; margin `1.08787423596e-06`.
- `Q00_E040_MC07_endpoint-negative`: `RESOLUTION_CONVERGED`; state `(-1,1)`; step `0.0447416296415`; ratio `0.502183630783`; reciprocal residual `5.85808803356e-12`; margin `6.55677946923e-07`.
- `Q08_E040_MC03_endpoint-negative`: `RESOLUTION_CONVERGED`; state `(-1,1)`; step `0.0447416296415`; ratio `0.502183630783`; reciprocal residual `5.85808803356e-12`; margin `6.55677946923e-07`.
- `Q06_E040_MC04_resolved-control`: `RESOLUTION_CONVERGED`; state `(0,0)`; step `0.00579916827709`; ratio `0.500011344978`; reciprocal residual `2.22044604925e-15`; margin `1`.
- Runtime: `264.985 s`.

## Decision

`ADOPT_HIGHER_HOMOTOPY_RESOLUTION`

## Consequence

The fixed 1024/4096 winding ladder used by 5239-5241 is insufficient for these near-collision states. At 32768 steps the projective step falls below 0.05, the asymptotic winding state is stable, and reciprocal identity returns below 2e-8. The next repair is an adaptive doubling evaluator that requires both projective-step and reciprocal-residual gates before accepting a winding state.

## Next exact target

Rebuild the Q03/Q05 high-chatter winding intervals with adaptive 1024-to-32768 confirmation, compare transition counts with the fixed-resolution intervals, and only then rerun their inner integrals.

## Claim boundary

This is a numerical branch-classification result, not a UV coefficient, local-GR derivation, or full-MTS claim.
