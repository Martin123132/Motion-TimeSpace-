# 5408: representative external-4/first square subcover gate

## Decision

**PASS FOR CONTINUED V41 PRODUCTION ONLY.**

The proposed `{1,4}` invariant override is rejected. At the support endpoint the global displacement lifts that invariant to only order `10^-10`, and its phase winds around the four contour arcs. A rectangular invariant lower bound would therefore be the wrong certificate.

## Derived edge

For right external leg 4 in its plus chart and hard leg 1 in its plus chart,

```text
p4 = (1,-T,0,-z),
tilde_lambda_4 = (1,-T/(1-z)),
tilde_lambda_1 = (1,hbar_1/p1_plus),
[14] = -T/(1-z) - hbar_1/p1_plus.
```

This ratio form removes the interval dependency introduced by reconstructing the two spinors independently. It is an identity, not a closure or fitted replacement.

## Numeric certificate

- maximum pointwise direct-versus-derived identity error: `1.1102230318952986e-16`;
- finite path subcover: `16 x 16` on each of `4` global arcs;
- minimum rigorous `[14]` absolute lower bound: `0.020081548912116359`;
- formerly failing depth-18 leaf denominator margin after repair: `0.00039811151694132469`;
- production state after the bounded resume: `27/240` path jobs, `7` accepted and `15` pending boxes in the active path.

## Claim boundary

This checkpoint certifies one representative-chart denominator and authorizes continued v41 production. It does not establish the complete regular-away W3 bound, event-local W3, UV finiteness, local GR, or the full MTS theory.
