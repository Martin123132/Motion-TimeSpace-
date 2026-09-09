# 5424: v43 right-connector progress checkpoint

## Decision

**PASS FOR COMMITTED SAME-REVISION PROGRESS ONLY.**

The unchanged v43 production evaluator commits `70` additional exact interval boxes. The next live box is `LLDRDRDRDLDLDRDRU` at depth `17`. Additional pending boxes reflect subdivision of a newly entered region, not invalidation of accepted certificates.

## Evidence

- accepted boxes: `274 -> 344`;
- accepted area fraction: `6.75048828125% -> 8.21151733398436%`;
- pending boxes: `10 -> 12`;
- maximum pending depth: `13 -> 17`;
- newly certified depth distribution: `depth 7: 1, depth 9: 2, depth 11: 3, depth 13: 6, depth 15: 11, depth 17: 47`;
- weakest new denominator margin: `0.00039811162934668591`;
- weakest new collision-Jacobian margin: `3.0210209452122596`.

No new interval-obstruction category appears, and every accepted row retains finite positive local certificate fields.

## Claim boundary

Regular-away W3, event-local W3, combined W3, regulator limit, UV, local-GR, and full-MTS claims remain false.
