# 5324 - Decay-angle measure, symmetry, and topology preflight

## Derived measure

With `a=|cos(theta_soft)|`, `b=|cos(theta_decay)|`, and

`G(a,b)=sum_{sigma_s,sigma_d=+-1} F(sigma_s a,sigma_d b)`,

the parent Sobol map gives

`(1/4) integral_-L^L ds integral_-L^L dd F = (1/4) integral_0^L da integral_0^L db G`,

with `L=0.995`. The fixed-decay runner already
integrates `a` and sums all four signs, so only the paired decay rule
and the inherited factor `1/4` remain.

## Result

- order-2 requires `D2_MID`;
- order-4 requires `D4_INNER` and `D4_OUTER`;
- `D4_INNER` is the validated 5323 slice and its topology is reproduced;
- both genuinely new decay-node topology contracts pass;
- maximum sign-orbit reduction residual: `3.67387973501e-14`;
- decision: **DECAY_ANGLE_MEASURE_AND_GL2_GL4_TOPOLOGIES_DERIVED__RUN_NEW_FIXED_DECAY_LADDERS**;
- validation: **PASS**.

## Claim boundary

The two new fixed-decay regulator ladders and the angular order-2/order-4
comparison have not yet been run. The cutoff endpoint cap also remains an
explicit separate bound. No full angular, UV, local-GR, or MTS claim follows.
