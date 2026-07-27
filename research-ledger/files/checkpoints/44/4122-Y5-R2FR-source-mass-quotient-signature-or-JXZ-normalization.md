# 4122 - Source-Mass Quotient Signature or JX/JZ Normalization

## Verdict

- Decision: `SOURCE_MASS_QUOTIENT_UNSIGNED_JXZ_NORMALIZATION_DEFINED_FIRST_COMPARATOR_SELECTED`.
- Source-mass quotient signature remains unsigned: measured mass/GM/Hamiltonian/orbit/EM readout is not yet proven q-owned.
- Fallback is now normalized: `beta_A^H=partial_{A_N} ln mu_obs` and `J_A_source=rho_H beta_A^H/A_*` for `A in {X,Z}`.
- First comparator is source-charge WEP `eta_source_AB`; `Gdot` is second; R10 `alpha(lambda)` is third.
- No source-zero or local-GR claim is made.

## Generated Outputs

- `P8_Y5_R2FR_4122_SOURCE_REGISTER`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4122_SOURCE_REGISTER.csv`
- `P8_Y5_R2FR_4122_SOURCE_MASS_QUOTIENT_SIGNATURE`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4122_SOURCE_MASS_QUOTIENT_SIGNATURE.csv`
- `P8_Y5_R2FR_4122_PARENT_SIGNATURE_AUDIT`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4122_PARENT_SIGNATURE_AUDIT.csv`
- `P8_Y5_R2FR_4122_JXZ_NORMALIZATION_GATE`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4122_JXZ_NORMALIZATION_GATE.csv`
- `P8_Y5_R2FR_4122_FIRST_COMPARATOR_CHANNEL`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4122_FIRST_COMPARATOR_CHANNEL.csv`
- `P8_Y5_R2FR_4122_DECISION_GATES`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4122_DECISION_GATES.csv`
- `P8_Y5_R2FR_4122_NEXT_TARGET`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4122_NEXT_TARGET.csv`
- `P8_Y5_R2FR_4122_STATUS`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4122_STATUS.csv`

## Source-Mass Signature

| signature_id | required_identity | status |
|---|---|---|
| SMQ4122_0_decomposition | `mu_obs=G_eff M_eff(1+epsilon_mu)` | IDENTITY_AVAILABLE_NOT_ZERO |
| SMQ4122_1_dimensionless_source_charge | `beta_A^H:=partial_{A_N} ln mu_obs=partial_{A_N} ln G_eff+partial_{A_N} ln M_eff+partial_{A_N} ln(1+epsilon_mu), A in {X,Z}` | DERIVED_NORMALIZED_COUPLING_DEFINITION |
| SMQ4122_2_projected_mass | `M_eff=integral_{S or Sigma} Pi_M J_H with Pi_M parent-derived before readout` | CONDITIONAL_NOT_PARENT_SIGNED |
| SMQ4122_3_GM_Gauss_readout | `mu_obs=G_eff M_eff equals Poisson/Gauss/orbital monopole in the same observed frame` | CONDITIONAL_NOT_PARENT_SIGNED |
| SMQ4122_4_source_zero_theorem | `J_A_source=rho_H beta_A^H/A_* plus geometry/boundary/EM terms after normalization` | THEOREM_CONDITIONAL_NOT_LIVE |

## Normalization Gate

| norm_id | quantity | definition | score_status |
|---|---|---|---|
| JXZN4122_0_field_coordinate | A_N for A in {X,Z} | `A_N:=A/A_* is the dimensionless normalized fibre/source-coupling coordinate` | symbolic_normalization_declared_scale_missing |
| JXZN4122_1_source_charge | beta_A^H | `beta_A^H:=partial_{A_N} ln mu_obs = partial_{A_N} ln G_eff + partial_{A_N} ln M_eff + partial_{A_N} ln(1+epsilon_mu)` | formula_ready_components_missing |
| JXZN4122_2_source_current_density | J_A_source | `J_A_source=rho_H beta_A^H/A_* for dimensional A, or rho_H beta_A^H for dimensionless A_N` | symbolic_current_law_units_not_fixed |
| JXZN4122_3_test_charge | beta_A^T | `beta_A^T:=partial_{A_N} ln m_test_obs for test body/clock/matter readout` | needed_for_force_comparison_missing |
| JXZN4122_4_force_projection | alpha_A(lambda_A) | `alpha_A(lambda_A)=K_A beta_A^H beta_A^T with lambda_A=sqrt(Z_A/M_A^2), after parent Green-function normalization` | not_scoreable_until_operator_and_charges_numeric_or_zero |
| JXZN4122_5_source_normalization_vector | D_a ln mu_obs | `D_a ln mu_obs=D_a ln G_eff+D_a ln M_eff+D_a ln(1+epsilon_mu) for a in {t,r,A,lambda,frame}` | runner_skeleton_ready_but_values_missing |
| JXZN4122_6_EM_source_charge | beta_A^EM | `beta_A^EM:=partial_{A_N} ln EM_obs or EM source calibration coefficient` | symbolic_EM_charge_missing |

## First Comparator

| comparator_id | rank | observable_link | score_status |
|---|---|---|---|
| CMP4122_0_first_channel_species_source_charge | 1 | eta_source_AB;eta_WEP_source_charge | comparator_selected_not_numeric |
| CMP4122_1_second_channel_Gdot | 2 | Gdot_over_G | comparator_available_values_missing |
| CMP4122_2_third_channel_R10 | 3 | delta_G_or_fifth_force_yukawa | deferred_curve_and_operator_missing |
| CMP4122_3_fourth_channel_EM | 4 | EM stress/Poynting flux source coupling | em_comparator_defined_not_numeric |

## Next Target

- `4123-Y5-R2FR-species-blind-source-charge-zero-or-betaXZ-row.md`
- Try species/material blindness first; if it fails, make beta-difference rows executable against the `2.8e-15` source-charge target.
