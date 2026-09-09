# 5421: v43 right-connector progress checkpoint

## Decision

**PASS FOR COMMITTED SAME-REVISION PROGRESS ONLY.**

The unchanged v43 production evaluator commits `7` additional exact interval boxes. The next live box is `LLDRDLDRDLDLDR` at depth `14`. Additional pending boxes reflect subdivision of a newly entered region, not invalidation of accepted certificates.

## Evidence

- accepted boxes: `239 -> 246`;
- accepted area fraction: `6.396484375% -> 6.646728515625%`;
- pending boxes: `9 -> 12`;
- maximum pending depth: `11 -> 14`;
- newly certified depth distribution: `depth 9: 1, depth 11: 1, depth 15: 1, depth 17: 4`;
- weakest new denominator margin: `0.00039811214925251275`;
- weakest new collision-Jacobian margin: `3.859424781561132`.

No new interval-obstruction category appears, and every accepted row retains finite positive local certificate fields.

## Claim boundary

Regular-away W3, event-local W3, combined W3, regulator limit, UV, local-GR, and full-MTS claims remain false.
