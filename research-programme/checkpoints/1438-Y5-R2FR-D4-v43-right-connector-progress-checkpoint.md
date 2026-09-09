# 5422: v43 right-connector progress checkpoint

## Decision

**PASS FOR COMMITTED SAME-REVISION PROGRESS ONLY.**

The unchanged v43 production evaluator commits `10` additional exact interval boxes. The next live box is `LLDRDLDRDLDRDLU` at depth `15`. The pending frontier contracts under the same evaluator.

## Evidence

- accepted boxes: `246 -> 256`;
- accepted area fraction: `6.646728515625% -> 6.66809082031251%`;
- pending boxes: `12 -> 12`;
- maximum pending depth: `14 -> 15`;
- newly certified depth distribution: `depth 13: 1, depth 15: 1, depth 17: 8`;
- weakest new denominator margin: `0.0003981120880835055`;
- weakest new collision-Jacobian margin: `3.7596349445826247`.

No new interval-obstruction category appears, and every accepted row retains finite positive local certificate fields.

## Claim boundary

Regular-away W3, event-local W3, combined W3, regulator limit, UV, local-GR, and full-MTS claims remain false.
