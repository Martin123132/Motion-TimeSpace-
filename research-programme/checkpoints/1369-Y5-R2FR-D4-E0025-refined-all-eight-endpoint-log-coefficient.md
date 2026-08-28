# 5353: D4 E0025 refined all-eight endpoint log coefficient

## Purpose

Checkpoint 5353 reruns the complete E0025 endpoint coefficient with the
checkpoint-5352 source-backed branch coordinates and the accepted
checkpoint-5351 support coefficients.

## Result

The accepted finite-regulator coefficient is

```text
A_E0025 = 0.0007535421758997085 + 0.47073682415733986 i;
|A_E0025| = 0.4707374272814402;
diagnostic disk radius = 7.879439046930316e-07;
coherent sum ratio = 0.9999997734842182.
```

All eight event coefficients are present. All four branch parent fits,
endpoint-gap resolution checks, coefficient contracts, primitive checks and
boundary-sign derivations pass. The branch-event diagnostic radii fall to the
`2.55e-12` to `5.43e-12` range after replacing the inherited multi-nanometre
coordinate errors with the bisection bound.

## Interpretation

The original E0025 all-eight failure was repaired by a previously derived
coordinate bound. The accepted total differs from the blocked provisional
centre by only about `1.29e-09` in the real part, so the numerical centre was
already stable; what was missing was a defensible uncertainty contract.

## Claim boundary

True:

```text
valid_for_D4_E0025_all_eight_endpoint_coefficients.
```

False:

```text
valid_for_D4_endpoint_coefficient_regulator_zero_limit;
valid_for_D4_outer_regulator_zero_limit;
valid_for_decay_angle_integral;
valid_for_full_angular_convergence;
valid_for_full_phase_space_coefficient;
valid_for_numeric_UV_claim;
valid_for_local_GR_claim;
valid_for_full_MTS_claim.
```

No GitHub action is taken.
