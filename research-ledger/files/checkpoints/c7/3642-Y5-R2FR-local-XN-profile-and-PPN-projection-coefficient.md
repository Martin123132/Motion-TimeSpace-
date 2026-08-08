# 3642 Y5 R2FR local XN profile and PPN projection coefficient

**Status:** 3642 derives the local X_N profile laws needed for Gdot/radial/R10 bounds and maps beta_common to the existing Ward-safe C_qgamma PPN operator. It does not claim Xdot_N=0, radial hair zero, or C_gamma numeric; it sharpens each into theorem-zero premises or explicit amplitude/range/operator inputs.

**Claim ceiling:** no local-GR/Newton, PPN, Gdot, R10, radial, or beta_common pass is allowed from 3642.

## Derivation result

`X_N` now has two non-smuggled local branches. The clean branch is theorem-zero: `Xdot_N=0` and `partial_r X_N=0` only if local stationarity, source-normalization descent, boundary silence, and projector/calibration silence are signed. The finite branch is a local exterior profile: `delta X_N=A_X exp(-r/ell_X)/r`, giving `partial_r X_N=-(1/r+1/ell_X) delta X_N`.

The PPN coefficient is also tied down: `C_gamma` is not a free knob. It is the existing Ward-safe `C_qgamma` operator applied to the beta-induced conserved source, `C_gamma=C_qgamma[S_beta]`.

## Profile derivation rows

- `XN3642_0_local_generator_definition`: DERIVED_DEFINITION — beta_common = X_N[ln mu_obs_common]; local drift and radial hair require Xdot_N := u^a nabla_a X_N and Xr_N := n^a nabla_a X_N
- `XN3642_1_stationary_exterior_zero`: CONDITIONAL_ZERO_NOT_PARENT_SIGNED — if L_u X_N=0 in the calibrated local source frame and all explicit_t Ward residuals vanish, then d ln mu_obs/dt=0
- `XN3642_2_exterior_profile_operator`: PROFILE_LAW_DERIVED_CONDITIONALLY — (Box_loc - m_X^2) delta X_N = J_X^eff with J_X^eff=0 outside the compact source gives delta X_N(r)=A_X exp(-r/ell_X)/r + X_inf for a static spherical exterior
- `XN3642_3_radial_derivative_law`: RADIAL_LAW_FILLED_SYMBOLIC — for delta X_N=A_X exp(-r/ell_X)/r, partial_r X_N = -(1/r + 1/ell_X) delta X_N
- `XN3642_4_time_drift_law`: TIME_LAW_FILLED_SYMBOLIC — Xdot_N = dot_A_X exp(-r/ell_X)/r + A_X exp(-r/ell_X) dot_ell_X/ell_X^2 + dot_X_inf plus source-motion/projector terms
- `XN3642_5_ppn_coefficient_definition`: CGAMMA_MAP_DERIVED_SYMBOLIC — gamma-1 = C_gamma beta_common^2 + C_grad nabla X_N + retained channels; C_gamma := C_qgamma[N_beta->q_loc]

## Profile candidates

- `XNP3642_0_stationary_constant`: `X_N=X_inf constant in local exterior` | `Xdot_N=0` | `partial_r_X_N=0`.
- `XNP3642_1_massive_yukawa`: `X_N=X_inf + A_X exp(-r/ell_X)/r` | `Xdot_N=dot_A_X exp(-r/ell_X)/r + A_X exp(-r/ell_X) dot_ell_X/ell_X^2 + dot_X_inf` | `partial_r_X_N=-(1/r+1/ell_X) A_X exp(-r/ell_X)/r`.
- `XNP3642_2_massless_gauss`: `X_N=X_inf + Q_X/r` | `Xdot_N=dot_Q_X/r + dot_X_inf` | `partial_r_X_N=-Q_X/r^2`.
- `XNP3642_3_cosmological_bleed`: `X_N=X_inf(t)+local screened correction` | `Xdot_N=dot_X_inf + screened local terms` | `partial_r_X_N=screened local terms only`.

## PPN coefficient map

- `CG3642_0_metric_slip_definition`: PPN_CONVENTION_LINKED — `gamma-1 = (Psi-Phi)/Phi_GR in weak-field scalar/isotropic PPN projection`.
- `CG3642_1_ward_safe_operator`: SYMBOLIC_OPERATOR_COEFFICIENT_DERIVED — `C_gamma := C_qgamma[S_beta] = -(c^2/(2U_ref)) P_scalar P_metric G_EH Div^-1[S_beta]`.
- `CG3642_2_norm_bound`: NORM_BOUND_DERIVED_INPUTS_MISSING — `|C_gamma| <= (c^2/(2U_min)) N_G N_D N_beta`.
- `CG3642_3_qR_bridge_guard`: SHORTCUT_BLOCKED_UNLESS_BRIDGE_SIGNED — `C_gamma=-1/2 may be used only if beta_common-induced q_loc equals q_R_hat with same GM convention, gauge, source averaging, and no retained channels`.

## Bound updates

- `B3642_0_gdot_stationary_or_profile`: Gdot_clock — `|beta_common| <= (9.0e-13 yr^-1 + |explicit_t residuals|)/|dot_A_X exp(-r/ell_X)/r + A_X exp(-r/ell_X) dot_ell_X/ell_X^2 + dot_X_inf|`.
- `B3642_1_ppn_cgamma_operator`: PPN_local_GR — `|beta_common| <= sqrt(2.3e-5/|C_gamma|), C_gamma=C_qgamma[S_beta]`.
- `B3642_2_radial_yukawa`: orbital_radial — `|beta_common| <= (|partial_r ln mu|_limit + |explicit_r residuals|)/(|A_X| exp(-r/ell_X)(1/r+1/ell_X)/r)`.
- `B3642_3_r10_profile_link`: R10_short_range — `lambda_X=ell_X and alpha_common(lambda)=K_X beta_common^2 tau_R10(lambda)/M_X^2 with profile support A_X exp(-r/ell_X)/r`.

## Claim gates

- `G3642_0_no_constant_profile_axiom`: ENFORCED — Do not assert Xdot_N=partial_r X_N=0 as a local plateau axiom.
- `G3642_1_no_qR_shortcut`: ENFORCED — Do not import C_gamma=-1/2 from q_R unless q_loc/q_R normalization bridge is signed.
- `G3642_2_local_gr_newton_route`: ACTIVE — Local GR/Newton recovery requires constant measured source normalization and zero/scored PPN slip.

## Next target

`3643-Y5-R2FR-local-stationarity-nohair-or-first-profile-amplitude-row.md` via `scripts/Y5_R2FR_3643_local_stationarity_nohair_or_first_profile_amplitude_row.py`.

## Sources

- `next_3641`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3641_NEXT_TARGET.csv` exists=True needle_found=True
- `fill_3641`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3641_BETA_COMMON_FIRST_NUMERIC_FILL.csv` exists=True needle_found=True
- `bounds_3640`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3640_BETA_COMMON_BOUND_INVERSION_ROWS.csv` exists=True needle_found=True
- `ward_residuals_3640`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3640_BETA_COMMON_WARD_RESIDUAL_DECOMPOSITION.csv` exists=True needle_found=True
- `cgm_gate`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_CONSTANT_GM_DERIVATIVE_HAIR_GATE.csv` exists=True needle_found=True
- `time_drift`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_time_drift_residual_or_zero.csv` exists=True needle_found=True
- `radial_mu`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_radial_mu_profile_or_zero.csv` exists=True needle_found=True
- `local_profile_schema`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2029_LOCAL_PROFILE_SCHEMA.csv` exists=True needle_found=True
- `first_qloc_profile`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1712_FIRST_QLOC_PROFILE_ROW.csv` exists=True needle_found=True
- `ppn_projection_1182`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1182_SYMBOLIC_PPN_PROJECTION_MAP.csv` exists=True needle_found=True
- `cqgamma_1370`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1370_WARD_SAFE_CQGAMMA_DERIVATION.csv` exists=True needle_found=True
- `cqgamma_inputs_1371`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1371_CQGAMMA_NORM_BOUND_INPUT_TABLE.csv` exists=True needle_found=True
- `ppn_parent_1520`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_LCG_1520_CQGAMMA_DERIVATION_ATTEMPT.csv` exists=True needle_found=True
