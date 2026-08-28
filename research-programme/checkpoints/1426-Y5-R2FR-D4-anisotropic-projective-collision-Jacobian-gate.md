# 5410: anisotropic projective collision-Jacobian gate

## Decision

**PASS FOR CONTINUED V42 PRODUCTION ONLY.**

The dominant v41 geometric split was not a physical collision and not a missing parent Jacobian. The selected representative branch is `minus_u`, so the existing anisotropic explicit `minus_v` fallback was algebraically inapplicable. The valid projective fallback was unnecessarily restricted to square covers.

## Exact repair

Revision v42 generalizes the projective union from `N x N` to independent `N_x x N_t` closed subcovers. This changes only the finite partition used to enclose the same parent mixed-root derivative; it introduces no fitted coefficient, sign axiom, or closure term.

On the historical depth-15 parent box:

- `8 x 8` collision-Jacobian lower bound: `0`;
- `8 x 16` collision-Jacobian lower bound: `27.466941964759005`;
- `8 x 16` projective denominator lower bound: `0.0072605403097022589`.

## Production regression

- active state migrated `v41 -> v42` without requeuing accepted rows;
- current active partition: `67` accepted and `12` pending boxes;
- accepted production rows using the new `8 x 16` proof: `2`;
- exact accepted-plus-pending area: `0.039327536205488567`.

## Claim boundary

This removes one conservative collision-Jacobian split class on the active contour path. The remaining edge refinements, complete path, regular-away W3 sum, event-local W3, UV, local-GR, and full-MTS gates remain open.
