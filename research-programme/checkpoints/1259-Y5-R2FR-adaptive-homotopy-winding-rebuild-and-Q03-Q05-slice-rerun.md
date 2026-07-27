# 5243 — Adaptive homotopy winding rebuild and Q03/Q05 slice rerun

## Outcome

The uniform adaptive-doubling route was stopped before integration because it is computationally unsuitable for the full interval map.

- One Q03/E040/MC03 job generated `2625` cached homotopy-resolution states.
- `636` physical coordinates reached the strict projective, reciprocal, stability, and step-ratio gates.
- Five distinct winding states and `29` sampled state transitions were found.
- The run exceeded the bounded execution window before completing even the first of 24 scheduled jobs.
- The exact state cache is preserved in `source-intake/functional_rg/5243/adaptive_homotopy_state_cache.json`.

## Decision

`HOLD_UNIFORM_ADAPTIVE_REBUILD__DERIVE_PROJECTIVE_RECIPROCAL_TRACKING`

## Interpretation

The failure is computational, not a rejection of the winding map. Uniformly rebuilding a 32768-step target homotopy at every physical-coordinate bisection repeats almost all transport work. The correct next object is a sparse projective tracker that transports reciprocal collision roots and reciprocal chamber-boundary roots jointly.

## Claim boundary

No corrected Q03/Q05 integral, order-9 cubature, UV coefficient, local-GR result, or full-MTS claim follows from this stopped run.

## Superseding checkpoint

Checkpoint 5244 tests the first half of that repair: coupled reciprocal collision-root transport. It preserves reciprocal identity but exposes the remaining unresolved chamber-boundary transport.
