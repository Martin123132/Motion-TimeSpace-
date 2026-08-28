# 5416: v43 right-connector production-stability gate

## Decision

**PASS FOR A COMMITTED FINITE TRANSITION AND CONTINUED V43 PRODUCTION ONLY.**

The preserved `S_X006_MC04_SP_DP` right-connector partition advances under the unchanged v43 evaluator. The deepest directly audited depth-17 transition is now an accepted production row, and the active ledger exposes no new analytic obstruction.

## Production evidence

- accepted boxes: `21 -> 131` (`+110`);
- pending boxes: `14` at maximum depth `17`;
- certified parameter-area coverage: `1.68609619140626%`;
- accepted plus pending area: `0.039327536205488567`;
- failure classes: `4`, all already declared at checkpoint 5415.

## Audited transition

The depth-`17` path `LLDLDRDLDLDRDLDRU` is committed with amplitude-denominator lower bound `0.00061355696355832505` and collision-Jacobian lower bound `4.9247652444358438`. Its certificate uses `SUBDIVIDED_PATH_CORRELATED_PROJECTIVE_UNION_8X8` rather than a point sample or fitted closure.

## Claim boundary

The right connector and 211 further contour jobs remain open. Regular-away W3, event-local W3, combined W3, regulator limit, UV, local-GR, and full-MTS claims remain false.
