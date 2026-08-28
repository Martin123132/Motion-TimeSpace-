# 5360 - D4 derived-A subtraction and E005 holdout preregistration

## Decision

`D4_DERIVED_A_SUBTRACTION_AND_E005_HOLDOUT_FROZEN__RESUME_E005`

## Actual derivation

For each endpoint normal form, substituting `u=z0+z1 delta` gives the exact primitive

`Phi=s[(C0/z1-C1 z0/z1^2)(u Log u-u)+(C1/z1^2)(u^2 Log u/2-u^2/4)]`.

Its lower-end logarithmic coefficient is

`H_e=-s_e[C0_e z0_e/z1_e-(C1_e/2)(z0_e/z1_e)^2]`.

The analytic event continuations imply `H_e=A_e epsilon+C_e epsilon^2+O(epsilon^3)`.  Therefore checkpoint 5359's directly derived total `A` is subtracted rather than fitted:

`J(epsilon)=I(epsilon)-A epsilon Log(epsilon/0.0025)`.

The fixed-A family has four remaining complex coefficients:

`J=I0+B epsilon+C epsilon^2 Log(epsilon/0.0025)+D epsilon^2+R3`.

## Frozen E005 holdout

Only the independently accepted `E00125` and corrected `E0025` integrated rungs are used.  Their fixed-A affine line was frozen before an accepted E005 value existed.

- predicted E005 integral: `5.7283434974085274 +6.4823353306222407 i`;
- conservative prediction disk: `0.11125673393041546`;
- provisional affine intercept: `5.7115691848245387 +6.4959827176179878 i`;
- input-only intercept disk: `0.066559850117243705`.

The E005 comparison has not been performed.  Its integration is resumably paused, so no compatibility result is implied by the prediction.

## Remainder boundary

A finite `M_D4` exists conditionally on a common closed analytic regulator interval, uniformly nonzero denominators, and a compact `C3` away region:

`|R3| <= M_D4 epsilon^3[1+|Log(epsilon/0.0025)|]`.

This checkpoint does not calculate a numerical `M_D4`.  Consequently the provisional intercept is not a regulator-zero result.

## Claim boundary

- derived-A subtraction: `True`;
- pre-measurement E005 holdout freeze: `True`;
- conditional remainder normal form: `True`;
- E005 compatibility, numeric remainder, complete second-order fit, outer-regulator, decay-angle, UV, local-GR and full-MTS claims: `False`.

## Next obstruction

Resume the saved E005 shards, validate the accepted finite value, and compare it to this frozen disk before any refit.  If compatible, use the three fixed-A rungs as the first overdetermined leading-family test.
