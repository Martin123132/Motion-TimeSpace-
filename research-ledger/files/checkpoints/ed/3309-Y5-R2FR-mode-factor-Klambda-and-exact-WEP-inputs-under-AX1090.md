# 3309 - Mode factor K(lambda) and exact WEP inputs under AX1090

Run UTC: `2026-06-27T19:02:50.508623+00:00`

## Verdict

The WEP mode factor is now derived.

For a Yukawa finite mode,

`eta_AB,E^(i) ~= alpha_i_star Xi_i[E] Delta_Xi_i[A,B] (1+r/lambda_i) exp(-r/lambda_i)`.

So the isolated mode factor is

`K_i(lambda_i,r,E) = alpha_i_star Xi_i[E] (1+r/lambda_i) exp(-r/lambda_i)`.

This turns each WEP row into

`|K_i(lambda_i,r,E) (s_i dot Delta_q_AB)| <= eta_bound_ABE`.

MICROSCOPE and Eot-Wash eta anchors are upgraded to source-backed nonclaim inputs. They are still not final claim bounds because exact material composition, source charge, finite-mode ranges, amplitude factors, and confidence conversion remain unresolved.

## Source Register

- `SRC3309_0` (local_path): `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3308-Y5-R2FR-source-coefficient-sik-gate-or-WEP-linear-bound-runner-under-AX1090.md` — role=3308 linear bound runner handoff
- `SRC3309_1` (local_path): `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3308_WEP_LINEAR_CONSTRAINT_MATRIX.csv` — role=3308 linear constraint matrix
- `SRC3309_2` (local_path): `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3308_UNIT_MODE_FACTOR_SENSITIVITY_PROXY.csv` — role=3308 unit mode proxy rows
- `SRC3309_3` (local_path): `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3308_DECISION_LEDGER.csv` — role=3308 decision
- `SRC3309_4` (local_path): `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3308_NEXT_TARGET.csv` — role=3308 next target
- `SRC3309_5` (local_path): `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_3308_VALIDATION.csv` — role=3308 validation
- `SRC3309_6` (external_primary): `https://arxiv.org/abs/2209.15487` — role=MICROSCOPE final WEP result; eta Ti/Pt and uncertainties
- `SRC3309_7` (external_primary): `https://www.esa.int/Science_Exploration/Space_Science/Microscope` — role=ESA MICROSCOPE mission overview; orbit about 710 km and Pt-Rh/Ti-Al-V alloy category
- `SRC3309_8` (external_primary): `https://arxiv.org/abs/0712.0607` — role=Eot-Wash Be/Ti WEP anchor; eta and differential acceleration

## K(lambda) Derivation

- `KDER3309_0_potential`: For one finite mode, Phi_i(r) = -G_cal M_E/r * alpha_i_star Xi_i[E] Xi_i[A] exp(-r/lambda_i). Result: finite-mode potential contribution relative to Newtonian source E.
- `KDER3309_1_acceleration`: a_i/a_N = alpha_i_star Xi_i[E] Xi_i[A] (1+r/lambda_i) exp(-r/lambda_i). Result: Yukawa acceleration has the derivative factor (1+r/lambda_i) exp(-r/lambda_i).
- `KDER3309_2_Eotvos_difference`: eta_AB,E^(i) ~= alpha_i_star Xi_i[E] Delta_Xi_i[A,B] (1+r/lambda_i) exp(-r/lambda_i). Result: finite-mode WEP signal is K_i(lambda_i,r,E) Delta_Xi_i[A,B].
- `KDER3309_3_mode_factor`: K_i(lambda_i,r,E) = alpha_i_star Xi_i[E] (1+r/lambda_i) exp(-r/lambda_i). Result: mode factor isolated from material contrast s_i dot Delta_q_AB.
- `KDER3309_4_limits`: For lambda_i >> r, K_i -> alpha_i_star Xi_i[E]; for lambda_i << r, K_i is exponentially suppressed. Result: long-range WEP tests constrain source coefficients only when the finite-mode range is comparable to or larger than source separation.

## Exact/Upgraded WEP Input Ledger

- `EXWEP3309_0_MICROSCOPE_eta` `eta_Ti_Pt`: value=-1.5e-15; status=UPGRADED_SOURCE_BACKED; source=https://arxiv.org/abs/2209.15487
- `EXWEP3309_1_MICROSCOPE_materials` `test_body_material_categories`: value=platinum-rhodium alloy vs titanium-aluminium-vanadium alloy; status=PARTIAL_SOURCE_BACKED_CATEGORY; source=https://www.esa.int/Science_Exploration/Space_Science/Microscope
- `EXWEP3309_2_MICROSCOPE_range` `Earth_source_separation_proxy`: value=7081000; status=PARTIAL_SOURCE_BACKED_RANGE_PROXY; source=https://www.esa.int/Science_Exploration/Space_Science/Microscope
- `EXWEP3309_3_EOTWASH_eta` `eta_Earth_Be_Ti`: value=0.3e-13; status=UPGRADED_SOURCE_BACKED; source=https://arxiv.org/abs/0712.0607
- `EXWEP3309_4_EOTWASH_differential_acceleration` `Delta_a_N_and_Delta_a_W`: value=Delta_a_N=(-0.2 +/- 2.8)e-15 m/s^2; Delta_a_W=(0.6 +/- 3.1)e-15 m/s^2; status=UPGRADED_SOURCE_BACKED; source=https://arxiv.org/abs/0712.0607
- `EXWEP3309_5_EOTWASH_range` `Earth_source_separation_proxy`: value=6371000; status=PARTIAL_SOURCE_BACKED_RANGE_PROXY; source=https://arxiv.org/abs/0712.0607

## Constraint Updates

- `LC3308_scalar_WEP3306_0_MICROSCOPE_Ti_Pt`: `|K_0(lambda_0,r_MICROSCOPE_Earth_proxy) * (s_0B*Delta_q_B + s_0p*Delta_q_p + s_0n*Delta_q_n + s_0C*Delta_q_C + s_0D*Delta_q_D)| <= eta_bound_ABE` with r_MICROSCOPE_Earth_proxy=7081000 m.
- `LC3308_spin2_WEP3306_0_MICROSCOPE_Ti_Pt`: `|K_2(lambda_2,r_MICROSCOPE_Earth_proxy) * (s_2B*Delta_q_B + s_2p*Delta_q_p + s_2n*Delta_q_n + s_2C*Delta_q_C + s_2D*Delta_q_D)| <= eta_bound_ABE` with r_MICROSCOPE_Earth_proxy=7081000 m.
- `LC3308_scalar_WEP3306_1_EOTWASH_Be_Ti`: `|K_0(lambda_0,r_EOTWASH_Earth_proxy) * (s_0B*Delta_q_B + s_0p*Delta_q_p + s_0n*Delta_q_n + s_0C*Delta_q_C + s_0D*Delta_q_D)| <= eta_bound_ABE` with r_EOTWASH_Earth_proxy=6371000 m.
- `LC3308_spin2_WEP3306_1_EOTWASH_Be_Ti`: `|K_2(lambda_2,r_EOTWASH_Earth_proxy) * (s_2B*Delta_q_B + s_2p*Delta_q_p + s_2n*Delta_q_n + s_2C*Delta_q_C + s_2D*Delta_q_D)| <= eta_bound_ABE` with r_EOTWASH_Earth_proxy=6371000 m.

## Claim Blockers

- `BLK3309_0_alpha_star` `alpha0_star, alpha2_star`: derive Z_i and U_i or prove pure metric limit for mode residues/readout.
- `BLK3309_1_lambda` `lambda_0, lambda_2`: derive parent quadratic coefficients or bound lambda_i as scan parameter.
- `BLK3309_2_source_charge` `Xi_0[Earth], Xi_2[Earth]`: derive source universality or build Earth source-charge model.
- `BLK3309_3_exact_materials` `exact alloy/isotope composition and binding/EM accounting`: extract material composition tables from experiment papers or official mission docs.
- `BLK3309_4_confidence` `single confidence convention/covariance treatment`: choose one-sided/two-sided CL convention and use full paper uncertainties.

## Runner

- `RUN3309_0_K_derivation`: `PASS_NONCLAIM` — K_i=lambda factor includes (1+r/lambda_i) exp(-r/lambda_i)
- `RUN3309_1_exact_eta_inputs`: `PASS_NONCLAIM` — EXWEP3309_0_MICROSCOPE_eta;EXWEP3309_3_EOTWASH_eta
- `RUN3309_2_constraint_updates`: `PASS_NONCLAIM` — LC3308_scalar_WEP3306_0_MICROSCOPE_Ti_Pt;LC3308_spin2_WEP3306_0_MICROSCOPE_Ti_Pt;LC3308_scalar_WEP3306_1_EOTWASH_Be_Ti;LC3308_spin2_WEP3306_1_EOTWASH_Be_Ti
- `RUN3309_3_claim_permission`: `REFUSE_CLAIM_BLOCKERS_ACTIVE` — alpha0_star, alpha2_star;lambda_0, lambda_2;Xi_0[Earth], Xi_2[Earth];exact alloy/isotope composition and binding/EM accounting;single confidence convention/covariance treatment

## Promotion Gates

- `GATE3309_0_K_numeric`: passed=false; claim=K_i(lambda_i) is numeric for WEP scoring
- `GATE3309_1_exact_WEP_inputs`: passed=false; claim=WEP input rows are exact enough for claim bounds
- `GATE3309_2_WEP_bound_runner`: passed=false; claim=linear WEP runner can bound s_ik combinations for local-GR claim

## Decision

- `DEC3309_0`: yes, symbolically — differentiating the Yukawa potential gives K_i=lambda factor alpha_i_star Xi_i[E](1+r/lambda_i)exp(-r/lambda_i)
- `DEC3309_1`: no — eta anchors are source-backed, but exact material composition, source charge, confidence conversion, and mode ranges are not filled

## Next Target

- `3310-Y5-R2FR-lambda-scan-WEP-envelope-or-parent-range-derivation-under-AX1090.md`
- `scripts/Y5_R2FR_3310_lambda_scan_WEP_envelope_or_parent_range_derivation.py`
- Objective: derive lambda_0/lambda_2 from parent coefficients if possible; otherwise build a nonclaim lambda-scan envelope for K_i(lambda) showing where MICROSCOPE/Eot-Wash can constrain s_ik combinations
