# 5470: D4 unresolved-cuboid collision-Jacobian leaf-union gate

## Question

Checkpoint 5469 closes four neighboring depth-24 subcuboids, while one descendant remains unresolved after exact x and epsilon splits. Its relative-root and selected-global-root factors stay positive; only the coarse collision-Jacobian interval reaches zero. The dimension ablation keeps the full x and epsilon boxes nonzero whenever t is fixed, while every test retaining the full t interval remains unresolved. The finite cover therefore refines t only rather than paying for an unmotivated square grid.

## Exact law

For a finite cover `D = union_i D_i`, separate interval certificates `0 notin J(D_i)` imply `inf_D |J| >= min_i dist(0,J(D_i)) > 0`. The rectangular hull of all image intervals is not required and may fill gaps that the leaf union does not contain.

## Result

Selected configurations: `2`. Pointwise-positive configurations: `2`.

Selected common cover: `1 x 128`. Leaf count per configuration: `128`. Minimum leaf-union `|J|`: `21.353680854057128`. Minimum projective denominator: `7.433723707686598e-05`.

## Decision

**COLLISION_JACOBIAN_LEAF_UNION_CERTIFIED__BUILD_RESUMABLE_AMPLITUDE_COVER**

## Claim boundary

A positive Jacobian leaf union licenses a resume-safe full-amplitude evaluation on the same finite leaves; it does not by itself certify the unresolved subcuboid, the full outer cover, W3, the regulator limit, local GR or full MTS.
