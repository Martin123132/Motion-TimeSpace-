# 5363 - D4 four-rung complete fixed-A fit and dual holdout freeze

## Decision

`D4_COMPLETE_FIXED_A_FOUR_RUNG_INTERPOLATION_AND_DUAL_HOLDOUT_FROZEN__RUN_E000625_PRIMARY`

## Complete fixed-A family

With `A` derived independently, four accepted rungs determine the four remaining complex coefficients in

`J(epsilon)=I0+B epsilon+C epsilon^2 Log(epsilon/0.0025)+D epsilon^2`,

where `J=I-A epsilon Log(epsilon/0.0025)`. This is an exact four-point interpolation, not an overdetermined fit and not a regulator-zero proof.

## Frozen holdouts

- `E000625` prediction: `5.7137147615280091 +6.4935296256232826 i`, disk `0.083463978151965684`, absolute weight sum `3.6875`;
- `E020` prediction: `5.7732981533451806 +6.4423552472974865 i`, disk `3.5662813628316221`, absolute weight sum `149`;

The E000625 prediction is the primary asymptotic holdout because its exact weights `(2,-21/16,11/32,-1/32)` have absolute sum `59/16`. E020 is retained as a deliberately severe outward extrapolation; its weights `(-32,64,-42,11)` have absolute sum `149`, so its conservative disk is expected to be much broader.

## Claim boundary

Neither holdout has been read or fitted. A fifth accepted rung is required for an overdetermined complete-family test; additional rungs and a numerical remainder constant are required for the D4 regulator-zero limit.
