# 5414: v43 post-edge production-stability gate

## Decision

**PASS FOR CONTINUED V43 PRODUCTION ONLY.**

The left `(2,3)` mixed-angle repair survives three hours of subsequent production. Its historical failure counter does not increase, no seventh failure category appears, and the adaptive frontier contracts materially.

## Production evidence

- accepted boxes: `285 -> 418`;
- pending boxes: `11 -> 9`;
- maximum pending depth: `12 -> 10`;
- certified area coverage: `25.024414% -> 56.250000%`;
- repaired `(2,3)` historical failure count: `1` before and after the regression;
- geometric-denominator historical failure count: `27` before and after the regression.

Every accepted proof row retains finite positive denominator and collision-Jacobian margins. Accepted plus pending area exactly reproduces the parent rectangle.

## Claim boundary

The active connector remains incomplete. Regular-away W3, event-local W3, combined W3, regulator limit, UV, local-GR, and full-MTS claims remain open.
