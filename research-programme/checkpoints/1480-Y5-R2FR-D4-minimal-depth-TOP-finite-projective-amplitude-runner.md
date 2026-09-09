# 5464: Minimal-depth D4 TOP finite projective amplitude runner

## Decision

**MINIMAL_DEPTH_TOP_PARTIAL__RESUME**

## Derived depth rule

Parent v51 enables its special correlated/projective reconstruction only at `refinement_depth >= 8`. The established `16 x 32` dyadic grid has depth `4 + 5 = 9`. This checkpoint uses `8 x 32`, whose exact dyadic depth is `3 + 5 = 8`: the minimum depth that retains the parent gate while preserving the previous 32-way path-parameter resolution.

Every selector, projective owner and amplitude interval is recomputed. A failed minimal-depth cell is not evidence against the target and is never promoted; it routes to the established `16 x 32` certificate or a local derivation.

Externally certified TOP targets: `5`. Minimal-depth certificates: `20`. Pending minimal-depth amplitude targets: `0`. First failures: `0`.

## Claim boundary

A completed row certifies one extreme representative only. It does not certify all outer leaves, event-local W3, the regulator limit, local GR or full MTS.
