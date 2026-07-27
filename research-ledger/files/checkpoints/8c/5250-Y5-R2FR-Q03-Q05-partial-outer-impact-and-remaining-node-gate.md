# 5250 — Q03/Q05 partial outer impact and remaining-node gate

## Exact partial update

The locked order-9 rule is reconstructed from all nine 5241 node values. Only Q03 and Q05 are then replaced by their accepted 5247/5249 values. This hybrid is an impact diagnostic, not a corrected cubature.

## Results

- Fixed order-9 value: `(18.92637003551503-0.5644314513109665j)`.
- Q03 weighted correction: `(-2.053482525167633-3.061014735929739e-06j)`.
- Q05 weighted correction: `(-1.7406664468096131-6.0172681271727245e-06j)`.
- Two-node weighted correction: `(-3.7941489719772523-9.078282863117515e-06j)`.
- Hybrid order-9 value: `(15.132221063537779-0.5644405295938296j)`.
- Relative hybrid shift: `0.200379833419`.
- Fixed versus hybrid order5/order9 differences: `0.869464996278`, `1.33762737391`.
- Runtime: `34.588 s`.

## Decision

`HOLD_HYBRID_OUTER_VALUE__REBUILD_ORDER5_BACKBONE_WITH_PAIRED_TRANSPORT`

## Interpretation

The two corrected order-9-only nodes move the weighted sum by about twenty percent and make the comparison with the inherited order-5 value worse. That is not a failure of the paired correction: the order-5 baseline itself still contains five independently transported legacy maps, so mixing corrected and uncorrected nodes is not a valid convergence test.

## Claim boundary

The hybrid value must not be quoted as the corrected coefficient. Q00, Q02, Q04, Q06, Q08, Q01, and Q07 remain on inherited topology.

## Next exact target

Rebuild the nested order-5 backbone Q00/Q02/Q04/Q06/Q08 with the reciprocal-projective tracker first. This gives a like-for-like corrected order-5 baseline before Q01 and Q07 complete the corrected order-9 rule.
