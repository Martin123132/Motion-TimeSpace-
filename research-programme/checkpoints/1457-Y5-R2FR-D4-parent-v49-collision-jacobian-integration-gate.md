# 5441: parent v49 collision-Jacobian integration gate

## Decision

**PARENT V49 COLLISION-JACOBIAN INTEGRATION PASSES.**

Parent v49 adds the source-proved `8 x 64` path-correlated projective cover from checkpoint 5440. It changes only enclosure resolution; it inserts no value, fit, or closure assumption.

## Production delta

- Revision: `D4-deformed-contour-regular-away-W3-v48` -> `D4-deformed-contour-regular-away-W3-v49`.
- Accepted boxes: 521 -> 529 (`+8`).
- Pending boxes: 11 -> 7 (`-4`).
- Collision-Jacobian failures: 5 -> 5.
- External01 c0 failures: 23 -> 23.
- External01 c1 failures: 258 -> 262.

## Interpretation

The geometric failure count froze while the frontier advanced, so the v49 resolution extension works in production. The only increasing category is the already known c1 external01 edge. That edge, not collision geometry, is now the active derivation target.

## Claim boundary

This validates only parent integration of the local collision-Jacobian cover. Seven right-connector boxes remain pending; no right-connector, regular-away W3, UV, local-GR, or full-MTS claim is made.
