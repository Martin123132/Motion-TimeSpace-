# 3302 - Quadratic-curvature finite coefficient extraction and bound map under AX1090

Run UTC: `2026-06-27T18:26:39.202514+00:00`

## Verdict

This checkpoint takes the finite route seriously.

If the curvature-squared coefficients are not zeroed by parent grammar, the local Newtonian potential has a concrete two-mode Yukawa structure. In the pure metric quadratic-gravity convention,

`Phi(r) = -G_cal M/r [1 + (1/3) exp(-r/lambda_0) - (4/3) exp(-r/lambda_2)]`.

That is not yet an MTS prediction. It becomes an MTS prediction only if MTS signs the same metric branch, source coupling, and coefficient normalization. Until then, the safe MTS form is

`Phi(r) = -G_cal M/r [1 + alpha_0 exp(-r/lambda_0) + alpha_2 exp(-r/lambda_2)]`.

## Source Register

- `SRC3302_0`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3301-Y5-R2FR-parent-curvature-linear-signature-hunt-or-quadratic-bound-fill-under-AX1090.md` — exists=true; role=3301 parent signature hunt
- `SRC3302_1`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3301_SIGNATURE_DECISION.csv` — exists=true; role=3301 decision row
- `SRC3302_2`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3301_QUADRATIC_BOUND_FILL_SCHEMA.csv` — exists=true; role=3301 finite schema
- `SRC3302_3`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3301_PARENT_SIGNATURE_SCAN.csv` — exists=true; role=3301 scan evidence
- `SRC3302_4`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3301_NEXT_TARGET.csv` — exists=true; role=3301 next target
- `SRC3302_5`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_3301_VALIDATION.csv` — exists=true; role=3301 validation
- `SRC3302_6`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3300_CURVATURE_SQUARED_YUKAWA_BASIS.csv` — exists=true; role=3300 Yukawa basis
- `SRC3302_7`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3300_R2_RICCI2_VARIATION_AUDIT.csv` — exists=true; role=3300 variation audit

## Action Convention

- `S = (1/2 kappa) integral sqrt(-g) [R - 2 Lambda + a_R2 R^2 + b_Ric R_mu_nu R^mu_nu + b_W C^2] + S_m`
- `a_R2`, `b_Ric`, and `b_W` are placeholders until MTS supplies parent-owned coefficients with units.

## Mode Mass Map

- `MODE3302_0_scalar`: m_0^2 ~ 1/[2(3 a_R2 + b_Ric)] in the displayed convention; amplitude template: alpha_0 = +1/3 for pure metric quadratic gravity with universal Hilbert source
- `MODE3302_1_spin2`: m_2^2 ~ -1/b_Ric or equivalent Weyl-normalized expression in the displayed convention; amplitude template: alpha_2 = -4/3 for pure metric quadratic gravity with universal Hilbert source

## Potential Templates

- `POT3302_0` `pure_metric_quadratic_template`: `Phi(r) = -G_cal M/r [1 + (1/3) exp(-r/lambda_0) - (4/3) exp(-r/lambda_2)]`
- `POT3302_1` `MTS_generalized_quadratic_template`: `Phi(r) = -G_cal M/r [1 + alpha_0 exp(-r/lambda_0) + alpha_2 exp(-r/lambda_2)]`
- `POT3302_2_GR_limit` `infinite_mass_or_zero_coefficient_limit`: `lambda_0,lambda_2 -> 0 or alpha_0=alpha_2=0 gives Phi(r) -> -G_cal M/r`

## Parent Coefficient Scan

- `a_R2/b_Ric`: `NO_PARENT_COEFFICIENT_CANDIDATE`; status=MISSING_PARENT_COEFFICIENT; evidence=NO_LINE_EVIDENCE

## Test Inputs

- `TIN3302_0_R10` `R10_short_range_Yukawa`: needs lambda_0, alpha_0 and/or lambda_2, alpha_2 at laboratory ranges; status=WAITING_ON_PARENT_COEFFICIENTS_AND_BOUND_CURVE
- `TIN3302_1_PPN` `solar_system_PPN`: needs gamma(r)-1, beta(r)-1, light-bending residual from scalar/spin-2 modes; status=WAITING_ON_METRIC_PROJECTION
- `TIN3302_2_orbital` `orbital_precession_ephemerides`: needs extra radial acceleration and perihelion/precession residual from finite lambda modes; status=WAITING_ON_RANGE_AND_ACCELERATION_MAP

## Promotion Gates

- `GATE3302_0_use_pure_metric_amplitudes`: passed=false; evidence=template only
- `GATE3302_1_use_parent_coefficients`: passed=false; evidence=reviewed_numeric_parent_rows=0
- `GATE3302_2_score_bounds`: passed=false; evidence=not ready

## Decision

- `DEC3302_0`: no — the finite potential map is derived, but parent-owned coefficient normalization and bound-source rows are not yet claim-ready
- `DEC3302_1`: the finite branch now has a concrete two-mode Yukawa form with scalar amplitude +1/3 and spin-2 amplitude -4/3 in the pure metric convention — this turns c_R2/c_Ric from an abstract residual into test quantities alpha_0/lambda_0 and alpha_2/lambda_2

## Next Target

- `3303-Y5-R2FR-universal-Hilbert-source-check-for-quadratic-amplitudes-under-AX1090.md`
- `scripts/Y5_R2FR_3303_universal_Hilbert_source_check_for_quadratic_amplitudes.py`
- Objective: check whether MTS can legitimately inherit the pure metric quadratic amplitudes +1/3 and -4/3, or must derive modified alpha_0/alpha_2 from its own source projection
