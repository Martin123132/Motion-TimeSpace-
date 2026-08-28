# 5376 - D4 uniform-remainder decomposition and bound reduction

## Decision

`D4_REMAINDER_BOUND_REDUCED_TO_PARENT_FROZEN_EVENT_AND_AWAY_C3_ENCLOSURES__RAW_SPLIT_REJECTED`

The accepted Q8/Q8 adaptive leaves were reconstructed for all seven integrated rungs. The saved analytic-pole and regular-numeric columns close back to the canonical integral after the recorded post-integration correction, but they are not separately invariant: adding any finite analytic chi to the pole subtraction and subtracting it from the regular part leaves the integral unchanged. Their large dyadic innovations visibly cancel, so neither raw column is allowed to masquerade as the physical remainder owner.

## Exact reduction

With a parent-frozen event/away atlas, write `I=sum_k[H_k Log(e/e_ref)+G_k]+W`. Taylor's theorem gives `H3=sum sup|H_k'''|`, `G3=sum sup|G_k'''|`, and a mapped-away bound `W3=sum Vol(U_a) sup|partial_e^3(f_a J_a)|`. Then

`M_D4=max(H3,G3+W3)/6`,

which is sufficient for `|R3|<=M_D4 e^3[1+|Log(e/e_ref)|]`. This is a finite calculational contract, not an existence-only phrase.

## Diagnostics

- maximum raw-component/total dyadic innovation ratio: `282.8629794767444`;
- maximum central seven-rung remainder quotient: `1162262.0173119032`;
- maximum disk-inclusive seven-rung quotient: `238980329.27843818`;
- leading-C0 coefficient quadratic centre candidate: `0.09404423781129737`;
- leading-C0 coefficient disk-inclusive finite-rung diagnostic: `14.419587326452378`.

The 5357 leading-C0 sequence is comparatively mild, but it is not the full endpoint logarithmic coefficient beyond leading order. The exact primitive also contains `+(s C1/2)(z0/z1)^2`, which contributes at order epsilon squared and must be included when deriving C and H3. The total finite-rung quotient is dominated by the nearly epsilon-independent integration disks at the smallest rung; those disks do not scale as epsilon cubed and therefore cannot certify a uniform Taylor constant. Another blind small-epsilon rung would worsen that mismatch rather than prove the limit.

## Next target

Construct one common closed regulator interval and parent-frozen event/away atlas, then interval-enclose H3, G3 and W3. The away mapped-integrand derivative is now the main numerical owner; the raw pole/regular CSV split is retired as a proof route.

The numeric uniform remainder, unconditional D4 regulator-zero, angular, phase-space, UV, local-GR and full-MTS claims remain false.
