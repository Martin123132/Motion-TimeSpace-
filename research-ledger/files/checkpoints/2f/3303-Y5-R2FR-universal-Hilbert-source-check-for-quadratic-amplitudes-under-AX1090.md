# 3303 - Universal Hilbert-source check for quadratic amplitudes under AX1090

Run UTC: `2026-06-27T18:36:47.727427+00:00`

## Verdict

The coupling fork is now explicit.

MTS cannot yet import the pure metric quadratic amplitudes `+1/3` and `-4/3` as predictions, because the parent-owned source/readout/normalization clauses are not all signed. The safe finite-mode law is therefore

`alpha_0 = (1/3) Z_0 Xi_0 U_0`

and

`alpha_2 = (-4/3) Z_2 Xi_2 U_2`.

Pure metric quadratic gravity is recovered only when every factor equals one. That makes the next hard object the source-projection overlap `Xi`, not another vague missing coupling.

## Source Register

- `SRC3303_0`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3302-Y5-R2FR-quadratic-curvature-finite-coefficient-extraction-and-bound-map-under-AX1090.md` — exists=true; role=3302 finite quadratic map
- `SRC3303_1`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3302_LINEARIZED_MODE_MASS_MAP.csv` — exists=true; role=3302 mode map
- `SRC3303_2`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3302_NEWTON_YUKAWA_POTENTIAL_TEMPLATE.csv` — exists=true; role=3302 potential templates
- `SRC3303_3`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3302_DECISION_LEDGER.csv` — exists=true; role=3302 decision
- `SRC3303_4`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3302_NEXT_TARGET.csv` — exists=true; role=3302 next target
- `SRC3303_5`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_3302_VALIDATION.csv` — exists=true; role=3302 validation
- `SRC3303_6`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3293_HILBERT_SOURCE_SIGNATURE_THEOREM.csv` — exists=true; role=3293 Hilbert source theorem
- `SRC3303_7`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3293_LOCAL_GR_MATTER_COUPLING_REDUCTION.csv` — exists=true; role=3293 local matter coupling
- `SRC3303_8`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3294_LOCAL_GR_REDUCTION_CONTRACT.csv` — exists=true; role=3294 local GR contract
- `SRC3303_9`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3294_NEWTON_LIMIT_AND_COMMON_G_CALIBRATION.csv` — exists=true; role=3294 Newton/common-G branch

## Amplitude Import Contract

- `AIC3303_0_pure_metric_branch`: local finite branch is pure metric quadratic gravity: one public metric, Einstein-Hilbert term, and quadratic curvature terms only Status: `NOT_PARENT_SIGNED`.
- `AIC3303_1_universal_Hilbert_source`: all matter couples through one Hilbert source T_H_mu_nu from one descended matter action with no post-variation source weights Status: `EXACT_CONDITIONAL_FROM_3293_NOT_PARENT_SIGNED`.
- `AIC3303_2_same_readout_metric`: the observed metric used by rods, clocks, EM stress, and orbital motion is the same metric whose quadratic curvature operators are diagonalized Status: `CONDITIONAL_FROM_3294_NOT_PARENT_SIGNED`.
- `AIC3303_3_canonical_mode_normalization`: linearized scalar and spin-2 modes have the same kinetic normalization and residue signs as the pure metric convention Status: `MISSING_PARENT_COEFFICIENT_NORMALIZATION`.
- `AIC3303_4_common_G_calibration`: the massless graviton residue defines the same measured G_cal used to normalize the Yukawa amplitudes Status: `CALIBRATION_ALLOWED_NOT_PREDICTIVE`.
- `AIC3303_5_no_screening_or_hidden_source_selector`: no local screening, hidden source selector, species weight, or environmental projector changes the finite-mode coupling relative to the massless graviton Status: `NOT_PARENT_SIGNED`.

## Evidence Score

- `AIC3303_0_pure_metric_branch`: passed=false; status=NOT_PARENT_SIGNED; source=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3302_DECISION_LEDGER.csv`
- `AIC3303_1_universal_Hilbert_source`: passed=false; status=EXACT_CONDITIONAL_FROM_3293_NOT_PARENT_SIGNED; source=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3293_HILBERT_SOURCE_SIGNATURE_THEOREM.csv`
- `AIC3303_2_same_readout_metric`: passed=false; status=CONDITIONAL_FROM_3294_NOT_PARENT_SIGNED; source=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3294_LOCAL_GR_REDUCTION_CONTRACT.csv`
- `AIC3303_3_canonical_mode_normalization`: passed=false; status=MISSING_PARENT_COEFFICIENT_NORMALIZATION; source=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3302_DECISION_LEDGER.csv`
- `AIC3303_4_common_G_calibration`: passed=false; status=CALIBRATION_ALLOWED_NOT_PREDICTIVE; source=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3294_LOCAL_GR_REDUCTION_CONTRACT.csv`
- `AIC3303_5_no_screening_or_hidden_source_selector`: passed=false; status=NOT_PARENT_SIGNED; source=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3293_LOCAL_GR_MATTER_COUPLING_REDUCTION.csv`

## Generalized Amplitude Law

- `ALAW3303_0_scalar` `scalar_R2`: `alpha_0 = (1/3) * Z_0 * Xi_0 * U_0`; pure limit: Z_0=Xi_0=U_0=1.
- `ALAW3303_1_spin2` `massive_spin2_Ricci_Weyl`: `alpha_2 = (-4/3) * Z_2 * Xi_2 * U_2`; pure limit: Z_2=Xi_2=U_2=1.
- `ALAW3303_2_Newton_reference` `massless_graviton_reference`: `G_cal is the measured massless spin-2 coupling; all finite-mode alphas are normalized relative to this reference`; pure limit: massless reference fixed by Newtonian calibration.

## Required Derivations

- `REQ3303_0_Z_factors` `Z_0, Z_2`: linearize the parent local kinetic action, diagonalize scalar and massive spin-2 sectors, normalize kinetic terms
- `REQ3303_1_Xi_factors` `Xi_0, Xi_2`: vary the descended matter action with respect to the diagonalized finite modes or project T_H_mu_nu through the mode projectors
- `REQ3303_2_U_factors` `U_0, U_2`: derive the public metric/readout map and show no Weyl/disformal/screening factor changes the observed potential
- `REQ3303_3_lambdas` `lambda_0, lambda_2`: extract a_R2/b_Ric/b_W with units and compute m_0,m_2 in the chosen convention

## Runner

- `RUN3303_0_import_fixed_amplitudes`: `REFUSE_IMPORT_USE_GENERAL_ALPHA` — AIC3303_0_pure_metric_branch=false;AIC3303_1_universal_Hilbert_source=false;AIC3303_2_same_readout_metric=false;AIC3303_3_canonical_mode_normalization=false;AIC3303_4_common_G_calibration=false;AIC3303_5_no_screening_or_hidden_source_selector=false
- `RUN3303_1_general_law_ready`: `PASS_NONCLAIM` — ALAW3303_0_scalar;ALAW3303_1_spin2;ALAW3303_2_Newton_reference
- `RUN3303_2_projection_requirements_ready`: `PASS_NONCLAIM` — Z_0, Z_2;Xi_0, Xi_2;U_0, U_2;lambda_0, lambda_2

## Promotion Gates

- `GATE3303_0_import_plus_minus_amplitudes`: passed=false; claim=MTS inherits alpha_0=+1/3 and alpha_2=-4/3
- `GATE3303_1_use_general_alpha_law`: passed=true; claim=MTS should use alpha_0=(1/3)Z_0Xi_0U_0 and alpha_2=(-4/3)Z_2Xi_2U_2 until pure limit is proven
- `GATE3303_2_score_bounds`: passed=false; claim=score finite quadratic branch against R10/PPN/orbital bounds

## Decision

- `DEC3303_0`: no — Hilbert/source/readout/normalization clauses remain conditional or missing, so fixed amplitudes would be imported rather than derived
- `DEC3303_1`: alpha_0=(1/3)Z_0Xi_0U_0 and alpha_2=(-4/3)Z_2Xi_2U_2 — pure metric values are recovered as the special case where residue, source projection, and readout overlaps are all unity

## Next Target

- `3304-Y5-R2FR-source-projection-overlap-law-for-alpha-factors-under-AX1090.md`
- `scripts/Y5_R2FR_3304_source_projection_overlap_law_for_alpha_factors.py`
- Objective: derive or bound Xi_0 and Xi_2, the source-projection overlap factors that decide whether finite modes couple universally like Hilbert stress or produce WEP/source-weight residuals
