# 5442: c1 external01 coarse-refinement gate

## Decision

**C1 EXTERNAL01 IS A RESOLVED COARSE-BOX REFINEMENT EVENT.**

The v49 run recorded four c1 external01 interval failures, but each occurred on a coarse parent box. Adaptive subdivision produced eight new accepted children with positive amplitude and collision-Jacobian denominators.

## Live provenance probe

- Probed pending path: `LRDRDRDLDRU` at depth 11.
- Arc evaluations: 16; failures: 0.
- Selected role in every point/box ablation: `{'box_box_box': ['representative'], 'box_point_box': ['representative'], 'point_box_box': ['representative'], 'point_point_point': ['representative']}`.
- Production c1 count delta: `+4`.
- Newly accepted children: `8`.

## Interpretation

No new c1 identity or closure is justified. The existing exact-invariant and adaptive-subdivision machinery already resolves these boxes. The correct next action is to resume the right-connector frontier and intervene only if c1 persists at maximum depth or stops producing accepted children.

## Claim boundary

This classifies one production failure mode; it does not complete the seven pending right-connector boxes and makes no W3, UV, local-GR, or full-MTS claim.
