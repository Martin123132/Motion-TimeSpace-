# 3954 - Z Source-Current Silence And PPN Normalization Map

Timestamp: `2026-07-01T14:22:16+00:00`

## Result

3954 derives the source-current chain rule for the constructed `Z^A` branch:

`J_A := (1/sqrt(-g)) delta S_matter / delta Z^A`.

If matter descends through the observable metric, then:

`J_A = 1/2 T_obs^mu_nu C_A_mu_nu + J_A^direct + J_A^measure + J_A^support`

where:

`C_A_mu_nu := partial g_obs_mu_nu / partial Z^A`.

## Silence Condition

`J_A=0` follows if:

- `partial_Z g_obs|0=0`;
- no direct `Z` matter/source weights exist;
- measure, coframe, material labels and source support descend through the same observable structure;
- boundary/support terms are fixed before readout.

So the coupling problem is now concrete: derive or bound `C_A`.

## Newton / G Status

The framework can derive constancy and universality conditions for the measured coupling:

`D_X ln mu_obs = D_X ln G_eff + D_X ln M_eff + D_X ln(1+epsilon_mu)`.

A universal constant offset can be calibrated. Time/radius/species/frame/range dependence cannot be hidden inside measured `GM`.

The absolute value of `G_N` still needs a parent-fixed `M_EH` / source-normalization scale or external calibration.

## Source Register

- Source rows found: `15/15`
- Register: `source-intake\mts_residuals\P8_Y5_R2FR_3954_SOURCE_REGISTER.csv`
- Validation: `source-intake\mts_residuals\P8_Y5_BRR545_3954_VALIDATION.csv`

## Next Target

`3955-Y5-R2FR-observable-metric-Z-linear-coefficient-or-source-current-bound.md`
