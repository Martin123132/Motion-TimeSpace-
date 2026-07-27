# 3308 - Source coefficient s_ik gate or WEP linear bound runner under AX1090

Run UTC: `2026-06-27T18:55:38.425930+00:00`

## Verdict

The WEP fallback is now a linear constraint system.

For each finite mode `i`,

`Delta_Xi_i[A,B] = s_i dot Delta_q_AB`.

Each WEP anchor therefore constrains

`|K_i(lambda_i) (s_i dot Delta_q_AB)| <= eta_bound_ABE`,

where

`K_i(lambda_i)=alpha_i_star Xi_i[E] (1+r/lambda_i) exp(-r/lambda_i)`.

This is not a claim runner yet. It is a clean algebraic gate: either derive `s_ik=0`, derive `K_i(lambda_i)`, or use exact WEP material/source data to bound the allowed source-coefficient combinations.

## Source Register

- `SRC3308_0`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3307-Y5-R2FR-material-source-charge-model-for-DeltaXi-WEP-bounds-under-AX1090.md` — exists=true; role=3307 material charge model
- `SRC3308_1`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3307_MATERIAL_CHARGE_BASIS.csv` — exists=true; role=3307 charge basis
- `SRC3308_2`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3307_MATERIAL_PROXY_CHARGES.csv` — exists=true; role=3307 proxy material charges
- `SRC3308_3`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3307_WEP_PAIR_CHARGE_DELTAS.csv` — exists=true; role=3307 WEP pair charge deltas
- `SRC3308_4`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3307_WEP_BOUND_ROWS_NONCLAIM.csv` — exists=true; role=3307 nonclaim bound rows
- `SRC3308_5`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3307_DELTA_XI_LINEAR_MODEL.csv` — exists=true; role=3307 DeltaXi linear model
- `SRC3308_6`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3307_NEXT_TARGET.csv` — exists=true; role=3307 next target
- `SRC3308_7`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_3307_VALIDATION.csv` — exists=true; role=3307 validation
- `SRC3308_8`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3306_WEP_SOURCE_ANCHORS.csv` — exists=true; role=3306 WEP anchors

## s_ik Gate

- `SIK3308_0_scalar_zero` `s_0k`: all scalar nonuniversal source coefficients s_0B,s_0p,s_0n,s_0C,s_0D vanish or project out of all material contrasts
- `SIK3308_1_spin2_zero` `s_2k`: all spin2 nonuniversal source coefficients s_2B,s_2p,s_2n,s_2C,s_2D vanish or project out of all material contrasts
- `SIK3308_2_combined` `s_ik`: both scalar and spin2 nonuniversal source coefficient families vanish or are bounded below WEP residuals

## Linear Constraint Matrix

- `LC3308_scalar_WEP3306_0_MICROSCOPE_Ti_Pt`: `|K_0(lambda_0)=alpha0_star Xi_0[E](1+r/lambda_0)exp(-r/lambda_0) * (s_0 dot Delta_q_AB)| <= eta_bound_ABE` with Delta_q_norm=2.65411754847 eta_sigma=2.74590604355e-15.
- `LC3308_spin2_WEP3306_0_MICROSCOPE_Ti_Pt`: `|K_2(lambda_2)=alpha2_star Xi_2[E](1+r/lambda_2)exp(-r/lambda_2) * (s_2 dot Delta_q_AB)| <= eta_bound_ABE` with Delta_q_norm=2.65411754847 eta_sigma=2.74590604355e-15.
- `LC3308_scalar_WEP3306_1_EOTWASH_Be_Ti`: `|K_0(lambda_0)=alpha0_star Xi_0[E](1+r/lambda_0)exp(-r/lambda_0) * (s_0 dot Delta_q_AB)| <= eta_bound_ABE` with Delta_q_norm=2.01876322083 eta_sigma=1.8e-13.
- `LC3308_spin2_WEP3306_1_EOTWASH_Be_Ti`: `|K_2(lambda_2)=alpha2_star Xi_2[E](1+r/lambda_2)exp(-r/lambda_2) * (s_2 dot Delta_q_AB)| <= eta_bound_ABE` with Delta_q_norm=2.01876322083 eta_sigma=1.8e-13.

## Unit Mode-Factor Sensitivity Proxy

- `UP3308_LC3308_scalar_WEP3306_0_MICROSCOPE_Ti_Pt`: unit K proxy bound `1.0345834325e-15` (K_i, exact materials, confidence convention, and source charge are not filled).
- `UP3308_LC3308_spin2_WEP3306_0_MICROSCOPE_Ti_Pt`: unit K proxy bound `1.0345834325e-15` (K_i, exact materials, confidence convention, and source charge are not filled).
- `UP3308_LC3308_scalar_WEP3306_1_EOTWASH_Be_Ti`: unit K proxy bound `8.91635027539e-14` (K_i, exact materials, confidence convention, and source charge are not filled).
- `UP3308_LC3308_spin2_WEP3306_1_EOTWASH_Be_Ti`: unit K proxy bound `8.91635027539e-14` (K_i, exact materials, confidence convention, and source charge are not filled).

## Runner

- `RUN3308_0_constraint_matrix`: `PASS_NONCLAIM` — LC3308_scalar_WEP3306_0_MICROSCOPE_Ti_Pt;LC3308_spin2_WEP3306_0_MICROSCOPE_Ti_Pt;LC3308_scalar_WEP3306_1_EOTWASH_Be_Ti;LC3308_spin2_WEP3306_1_EOTWASH_Be_Ti
- `RUN3308_1_unit_proxy`: `PASS_NONCLAIM` — 1.0345834325e-15;1.0345834325e-15;8.91635027539e-14;8.91635027539e-14
- `RUN3308_2_claim_permission`: `REFUSE_CLAIM_K_FACTORS_AND_EXACT_DATA_MISSING` — K_i(lambda), exact materials, source-body charge Xi_i[E], confidence conversion, and s_ik derivation remain missing

## Promotion Gates

- `GATE3308_0_sik_zero`: passed=false; claim=s_0k=s_2k=0 by parent source projector
- `GATE3308_1_linear_WEP_bound`: passed=false; claim=WEP data bounds s_ik combinations below required local-GR tolerance
- `GATE3308_2_source_composition_safe`: passed=false; claim=source-composition branch is safe for local GR

## Decision

- `DEC3308_0`: no — no parent source projector algebra is available, so s_ik remains an unknown source-coefficient vector
- `DEC3308_1`: the Ti/Pt and Be/Ti WEP anchors are now linear constraints on s_0k and s_2k combinations — the runner maps each experiment to |K_i(lambda) (s_i dot Delta_q)| <= eta_bound

## Next Target

- `3309-Y5-R2FR-mode-factor-Klambda-and-exact-WEP-inputs-under-AX1090.md`
- `scripts/Y5_R2FR_3309_mode_factor_Klambda_and_exact_WEP_inputs.py`
- Objective: derive the mode factor K_i(lambda)=alpha_i_star Xi_i[E](1+r/lambda_i)exp(-r/lambda_i), and replace proxy material/confidence rows with exact WEP inputs where source-backed data are available
