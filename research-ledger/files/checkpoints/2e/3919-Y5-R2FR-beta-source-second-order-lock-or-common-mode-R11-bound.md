# 3919 - Beta Source Second-Order Lock or Common-Mode R11 Bound

Timestamp: `2026-07-01T10:46:59+00:00`

## Result

The beta/source piece now has a clean conditional route:

`g00=-1+2 A_source U_N - 2 B_source U_N^2 + O(U_N^3)`

with

`delta_beta_source = B_source/A_source^2 - 1`.

Inside the same-frame EH/Hilbert/local source branch, Newton calibration gives `A_source=1`, and the EH nonlinear completion gives:

`g00_EH=-1+2 U_obs - 2 U_obs^2 + O(U_obs^3)`

therefore:

`B_source=A_source^2 => delta_beta_source=0`.

## Common-Mode Residual

3918 showed that `gamma` only sees the traceless/STF slip. A gamma-blind common mode can still survive:

`A_eff=1+xi_1, B_eff=1+xi_2, delta_beta_common=(1+xi_2)/(1+xi_1)^2-1`.

The square-law condition for harmless mass renormalization is:

`xi_2=2 xi_1+xi_1^2 => delta_beta_common=0`.

Small-residual fallback:

`|delta_beta_common| ~= |xi_2-2 xi_1| <= 7.8e-05`.

## Meaning

This is the next real narrowing: `beta` is not just another vague missing coefficient. It splits into a GR/EH source square law plus a common-mode square-law test. Constant square-law mass renormalization can be calibration; radial, time-dependent, or source-dependent common mode cannot be hidden inside orbital `GM`.

## Source Register

- Source rows found: `22/22`
- Register: `source-intake\mts_residuals\P8_Y5_R2FR_3919_SOURCE_REGISTER.csv`
- Validation: `source-intake\mts_residuals\P8_Y5_BRR545_3919_VALIDATION.csv`

## Generated Tables

- `source-intake\mts_residuals\P8_Y5_R2FR_3919_BETA_SOURCE_LOCK_DERIVATION.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_3919_COMMON_MODE_SQUARE_LAW.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_3919_BETA_BOUND_INPUTS.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_3919_DECISION_GATE.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_3919_NEXT_TARGET.csv`

## Next Target

`3920-Y5-R2FR-common-mode-square-law-or-XiN-bound-runner.md`
