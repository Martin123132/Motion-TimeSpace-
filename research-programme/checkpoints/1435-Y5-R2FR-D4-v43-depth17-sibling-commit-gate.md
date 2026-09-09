# 5419: v43 depth-17 sibling commit gate

## Decision

**PASS FOR COMMITTED DEPTH-17 TRANSITION AND CONTINUED V43 PRODUCTION ONLY.**

The two checkpoint-5418 direct certificates now appear unchanged in the production adaptive ledger. The same bounded resume also certifies the adjacent depth-17 pair, so this is a real frontier contraction rather than a side calculation.

## Production transition

- accepted boxes: `233 -> 237`;
- pending boxes: `14 -> 11`;
- maximum pending depth: `17 -> 15`;
- accepted coverage: `6.3812255859375%`;
- weakest new denominator margin: `0.00039811217983737812`;
- weakest new collision-Jacobian margin: `3.9091326794611647`.

The split ledger retains the same four analytic failure classes. The right connector is still incomplete, but its deepest live frontier has retreated from depth 17 to depth 15.

## Claim boundary

Regular-away W3, event-local W3, combined W3, regulator limit, UV, local-GR, and full-MTS claims remain false.
