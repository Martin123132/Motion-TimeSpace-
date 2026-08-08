# 4135 - Survivor Operator Excision or Bound Map

## Verdict

- Decision: `SURVIVOR_OPERATORS_REDUCED_TO_LOCAL_NORMAL_FORM_OR_COEFFICIENT_EXTRACTOR`.
- The survivor-operator remainder is now a precise fork: local normal-form adoption, or coefficient extraction.
- This is the cleanest route because it forbids unwanted operators instead of trying to tune them away.
- No Newton/local-GR/PPN/R10 pass is claimed.

## Generated Outputs

- `P8_Y5_R2FR_4135_SOURCE_REGISTER`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4135_SOURCE_REGISTER.csv`
- `P8_Y5_R2FR_4135_NORMAL_FORM_THEOREM`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4135_NORMAL_FORM_THEOREM.csv`
- `P8_Y5_R2FR_4135_OPERATOR_EXCISION_MAP`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4135_OPERATOR_EXCISION_MAP.csv`
- `P8_Y5_R2FR_4135_COEFFICIENT_EXTRACTOR_ROWS`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4135_COEFFICIENT_EXTRACTOR_ROWS.csv`
- `P8_Y5_R2FR_4135_REDUCED_BOUND_ROWS`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4135_REDUCED_BOUND_ROWS.csv`
- `P8_Y5_R2FR_4135_DECISION_GATES`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4135_DECISION_GATES.csv`
- `P8_Y5_R2FR_4135_STATUS`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4135_STATUS.csv`
- `P8_Y5_R2FR_4135_NEXT_TARGET`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4135_NEXT_TARGET.csv`

## Normal-Form Theorem

| claim piece | status | formula |
|---|---|---|
| local 2PN normal form | NORMAL_FORM_IMPORTED_FROM_WIT4021 | S_loc^{<=2PN}=S_vert[Phi]+(2 kappa_*)^-1 int R[g_obs]eps_obs+S_matter+S_EM+S_binding+dB+S_top+S_aux^double-zero |
| survivor operator excision theorem | DERIVED_CANDIDATE_EXCISION_THEOREM | If every retained survivor is exact/topological, vertical with Dq=0, auxiliary double-zero, higher than 2PN, or absent, then R_survivor_ops=0. |
| adoption or coefficient fork | PUBLIC_CLAIM_BLOCKED_UNTIL_ADOPTION_OR_BOUNDS | R_survivor_ops=0 requires actual corpus adoption of the normal form; otherwise every survivor must expose coefficient, units, weak-field projection, source path, and arena tolerance. |
| reduced Qextra remainder | MASTER_REMAINDER_REDUCED | epsilon_Qextra_4135 = R_survivor_ops[normal_form_or_coefficients] + R_boundary_harmonic + R_undescended_support + R_unstationary_flux + R_parent_adoption |

## Operator Map

| operator | verdict | coefficient |
|---|---|---|
| R2_fR_scalar_mode | EXCISED_BY_WIT4021_IF_ADOPTED_ELSE_COEFFICIENT_REQUIRED | c_R2_or_c_fR |
| Ricci_Weyl_squared | TOPOLOGICAL_GB_OR_EXCISED_ELSE_COEFFICIENT_REQUIRED | c_Ricci_or_c_Weyl |
| scalar_tensor_class_metric | EXCISED_BY_FIXED_SCALAR_OR_DOUBLE_ZERO_ELSE_BOUND_REQUIRED | F_phi_C_or_c_scalar |
| vector_preferred_frame | EXCISED_BY_NO_VECTOR_THEOREM_ELSE_PREFERRED_FRAME_BOUND | c_domain_vector_or_selector_marker |
| torsion_nonmetricity | EXCISED_BY_LEVI_CIVITA_OBSERVED_BRANCH_ELSE_CONNECTION_BOUND | c_T_or_c_Q |
| bulk_X_force_law | EXCISED_BY_VERTICAL_SOURCE_SILENCE_ELSE_FINITE_RANGE_BOUND | q_X_or_c_X |
| nonlocal_memory_kernel | EXCISED_BY_DOUBLE_ZERO_MEMORY_KERNEL_ELSE_KERNEL_BOUND | c_nonlocal_or_K_norm |
| Gamma_Khat_q_loc | PRIMARY_RESIDUAL_REQUIRES_ACTION_OR_QLOC_BOUND | D_GK_or_Q_loc_profile |
| source_normalization_operator | EXCISED_BY_SAME_SOURCE_THEOREM_ELSE_SOURCE_PREFAC_BOUND | c_domain_source_normalization_operator |

## Coefficient Extractor

| operator | required fields | target rows |
|---|---|---|
| R2_fR_scalar_mode | c_R2_or_c_fR, m0, coupling_to_T, lambda0=1/m0 | dimensionless alpha(lambda); delta_gamma; delta_beta |
| Ricci_Weyl_squared | c_GB, c_Ricci_res, c_Weyl_res, spin2_mass_or_projection | delta_gamma; xi; wave/slip sector |
| scalar_tensor_class_metric | F_phi, F_phiphi, alpha_phi, m_phi, D_t phi, D_r phi | Gdot/G; clocks; gamma/beta; alpha(lambda) |
| vector_preferred_frame | u_mu, c_i, norm constraint, domain anisotropy, W_domain_alpha_i | alpha1; alpha2; alpha3; xi |
| torsion_nonmetricity | T^a_bc, Q_abc, c_T, c_Q, hypermomentum/source coupling | WEP; clock; lightcone; R11 |
| bulk_X_force_law | q_X, m_X, lambda_X, alpha_X, source composition factor | R10 alpha(lambda); WEP; gamma/beta |
| nonlocal_memory_kernel | K_mem^loc, support radius, monopole projection, D_t/D_r kernel response | alpha3; Gdot/G; R10 |
| Gamma_Khat_q_loc | D_trace, D_A_grad, D_gamma_grad, D_cross_AG, D_mass_gap, D_boundary, P_loc | delta_beta_q_loc; alpha(lambda); source-exchange |
| source_normalization_operator | c_source_prefactor, domain dependence, species dependence, beta_source drift | Newton GM; delta_beta_source; preferred-frame source terms |

## Current Meaning

- If the local parent action normal-form is adopted, most survivor operators are not merely small; they are absent, vertical, topological/exact, or double-zero silent.
- If adoption fails, the branch does not collapse into vibes: it becomes a coefficient/projection extractor for PPN, R10, WEP, clocks and Newton/source coupling.
- `Gamma/Khat/q_loc` remains the special hard case because it may be killed by a variational stress theorem or retained as an explicit q_loc profile.

## Claim Ceiling

- no local_GR, Newton, PPN, R10, Gdot, clock, EM prediction, Maxwell derivation, alpha derivation, or source-normalization pass.
- This checkpoint narrows the local-GR proof route; it does not complete it.

## Next Target

- `4136-Y5-R2FR-local-parent-action-normal-form-adoption-or-coefficient-extractor.md`
