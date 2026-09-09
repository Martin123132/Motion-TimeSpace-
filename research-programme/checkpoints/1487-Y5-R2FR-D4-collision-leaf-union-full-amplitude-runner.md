# 5471: D4 collision leaf-union full-amplitude runner

## Construction

Checkpoint 5470 proves that the unresolved collision-Jacobian box is pointwise regular and that a path-only 128-leaf union separates every selected Jacobian and projective denominator from zero. This runner applies the unchanged parent-v51 full-amplitude evaluator to those exact same leaves. Each leaf is committed atomically, so interruption loses at most the active leaf.

## Current state

Passed leaves: `128/128`. Failed leaves: `0`. Remaining leaves: `0`.

Minimum amplitude denominator: `4.190199893160776e-06`. Minimum collision Jacobian: `215.40652565018635`.

## Decision

**UNRESOLVED_SUBCUBOID_FULL_AMPLITUDE_LEAF_UNION_CERTIFIED__INTEGRATE_REPAIR**

## Claim boundary

Only a complete 128/128 pass repairs the one checkpoint-5469 unresolved subcuboid. The parent cuboid still has pending siblings afterward; full outer enclosure, W3, the regulator limit, local GR and full MTS remain unclaimed.
