# 3920 - Common-Mode Square Law or XiN Bound Runner

Timestamp: `2026-07-01T10:53:05+00:00`

## Result

The common-mode obstruction has been turned into exact algebra plus a bound runner.

Linear common-mode source:

`C_0 nabla^2 Xi_N = -kappa_R P00[R11], with C_0:=C00_Phi+C00_Psi and Phi_R11=Psi_R11=Xi_N`

so formally:

`Xi_N = -(kappa_R/C_0) nabla^{-2} P00[R11]`.

Define `xi_1:=Xi_N/U_N`. The exact beta residual is:

`delta_beta_common = (1+xi_2)/(1+xi_1)^2 - 1 = (xi_2-2 xi_1-xi_1^2)/(1+xi_1)^2`.

Therefore the harmless square-law condition is:

`Delta_sq:=xi_2-2 xi_1-xi_1^2=0`.

Fallback beta gate:

`|Delta_sq| <= 7.8e-05*(1+xi_1)^2`.

## Calibration Split

`a_obs/a_N = (1+xi_1)-r partial_r xi_1; constant xi_1 is GM calibration, nonconstant xi_1 is a Newton/ephemeris residual`.

This is the useful split: constant square-law common mode can be measured-`GM` calibration, but radial, time-dependent, finite-range, or source-dependent common mode is a real residual. For time dependence:

`partial_t ln(GM_obs)=partial_t ln(1+xi_1)`.

## Meaning

This is a leap forward in the local-GR route: the common-mode problem is no longer a vague complaint. It is either an EH one-metric square law, or it becomes explicit rows for `Delta_sq`, `P00[R11]`, `partial_r xi_1`, `partial_t xi_1`, and source-dependence.

## Source Register

- Source rows found: `22/22`
- Register: `source-intake\mts_residuals\P8_Y5_R2FR_3920_SOURCE_REGISTER.csv`
- Validation: `source-intake\mts_residuals\P8_Y5_BRR545_3920_VALIDATION.csv`

## Generated Tables

- `source-intake\mts_residuals\P8_Y5_R2FR_3920_COMMON_MODE_SOURCE_AND_SQUARE_LAW.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_3920_XIN_BOUND_RUNNER_ROWS.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_3920_NEWTON_EPHEMERIS_GDOT_LINKS.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_3920_DECISION_GATE.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_3920_NEXT_TARGET.csv`

## Next Target

`3921-Y5-R2FR-P00-common-mode-source-zero-or-XiN-numeric-bound-fill.md`
