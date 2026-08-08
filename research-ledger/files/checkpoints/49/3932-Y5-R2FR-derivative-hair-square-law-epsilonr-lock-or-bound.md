# 3932 - Derivative Hair, Square Law, and Epsilon_r Lock or Bound

Timestamp: `2026-07-01T11:47:50+00:00`

## Result

Adopted the calibrated-monopole/EH square-law lock for the private local branch.

Calibration signature:

`local calibrated-monopole branch: Xi_N=xi_0 U_N+const, xi_0 is universal/time-independent/source-independent/frame-independent, Xi_N^res=0, and the public metric is the EH one-metric completion written in measured U_obs=(1+xi_0)U_N`.

EH square law:

`g00_EH=-1+2U_obs-2U_obs^2+O(U_obs^3), U_obs=(1+xi_0)U_N => xi_1=xi_0, xi_2=2xi_0+xi_0^2, Delta_sq=xi_2-2xi_1-xi_1^2=0`.

Radial lock:

`epsilon_r=|((1+xi_1)-r partial_r xi_1)/(1+xi_ref)-1|=0 when xi_1=xi_ref=xi_0 and partial_r xi_1=0`.

Derivative lock:

`B_deriv=|partial_t xi_1|+|partial_r xi_1|+|Delta_AB xi_1|+|delta_frame xi_1|=0 for universal derivative-silent xi_0`.

Local escape result:

`B_escape_loc=|Delta_sq|/(1+xi_1)^2+|epsilon_r|+B_deriv=0`.

## Meaning

This is the tight local result we were aiming at for the escape sector. Once projector/domain, boundary/harmonic and history/nonlocal channels are closed, the remaining common mode is harmless only if it is a universal derivative-silent measured-GM monopole and its second-order metric coefficient follows the EH square law.

Anything else is not calibration: radial shape, time drift, source dependence, frame/readout dependence, finite range, or a non-square `xi_2` must use the fallback rows.

## Current Verdict

- `Delta_sq=0`, `epsilon_r=0`, and `B_deriv=0` inside the private calibrated local branch.
- Therefore `B_escape_loc=0` inside that branch.
- This is still not a public local-GR claim; the next step is a rollup audit across all PPN/Newton/Maxwell/source-coupling rows.
- No change to `formalization-workbench`; no GitHub action.

## Source Register

- Source rows found: `17/17`
- Register: `source-intake\mts_residuals\P8_Y5_R2FR_3932_SOURCE_REGISTER.csv`
- Validation: `source-intake\mts_residuals\P8_Y5_BRR545_3932_VALIDATION.csv`

## Generated Tables

- `source-intake\mts_residuals\P8_Y5_R2FR_3932_COMMON_MODE_CALIBRATION_SIGNATURE.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_3932_DERIVATIVE_SQUARE_EPSILON_ZERO_RESULT.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_3932_COMMON_MODE_FALLBACK_BOUND_ROWS.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_3932_LOCAL_BESCAPE_RESULT.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_3932_DECISION_GATE.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_3932_NEXT_TARGET.csv`

## Next Target

`3933-Y5-R2FR-local-GR-PPN-conditional-closure-rollup-or-residual-scorecard.md`
