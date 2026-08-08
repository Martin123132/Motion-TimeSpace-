# 3636 Y5 R2FR source-mass quotient signature or JX normalization

**Status:** 3636 attempts the source-mass quotient signature and finds the live corpus still does not parent-sign measured source mass/GM/Hamiltonian/orbit readout as q-data. The fallback is now sharper: normalize the source coupling with beta_X=partial_XN ln mu_obs and J_X_source=rho_H beta_X/X_*. The first comparator channel is source-charge WEP eta_source_AB, before Gdot and R10 alpha(lambda).

**Claim ceiling:** no source-zero, Newton, local-GR, R10/R11, WEP, or PPN claim is allowed from 3636.

## Main result

The source-mass route now has a clean signature:

```text
mu_obs = G_eff M_eff(1+epsilon_mu)
beta_X^H := partial_{X_N} ln(mu_obs)
          = partial_{X_N} ln(G_eff)
          + partial_{X_N} ln(M_eff)
          + partial_{X_N} ln(1+epsilon_mu)
J_X_source = rho_H beta_X^H / X_*.
```

If `M_obs` is truly quotient-owned, `beta_X^H=0`. If not, `beta_X` is the normalized source charge to test. The least machinery comparator is now source-charge WEP, not R10 first.

## Source register

| source_id | path | exists | needle_found | role |
| --- | --- | --- | --- | --- |
| handoff_3635 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3635_NEXT_TARGET.csv | True | True | 3635 selected source-mass quotient signature versus JX normalization. |
| jx_row_3635 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3635_JX_SOURCE_RESIDUAL_ROW.csv | True | True | symbolic JX source row that 3636 normalizes. |
| component_gate_3635 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3635_SOURCE_READOUT_COMPONENT_GATE.csv | True | True | source/readout subcomponent gate. |
| constant_gm_zero_attempt | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_CONSTANT_GM_ZERO_THEOREM_ATTEMPT.csv | True | True | measured-GM identity and open derivative-hair premises. |
| constant_gm_runner | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_CONSTANT_GM_LOCAL_RESIDUAL_RUNNER_INPUT.csv | True | True | existing source-normalization residual runner rows. |
| source_norm_template | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_source_normalization_residual_vector_TEMPLATE.csv | True | True | template definitions for source-normalization comparator channels. |
| charge_current_attempt | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_charge_current_equality_DIRECT_ATTEMPT.csv | True | True | charge-current route for source mass and measured GM. |
| charge_current_residuals | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_charge_current_equality_RESIDUAL_DECOMPOSITION.csv | True | True | residual decomposition if charge-current equality fails. |
| mass_flux_contract | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_mass_flux_projector_Euler_calibration_CONTRACT.csv | True | True | mass flux, PiM, and absolute measured-GM calibration contract. |
| pim_contract | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_PiM_parent_symplectic_projector_algebra_CONTRACT.csv | True | True | Pi_M algebra and flux-closure contract. |
| hamiltonian_measure_contract | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_HAMILTONIAN_SOURCE_MEASURE_CONTRACT.csv | True | True | Hamiltonian source-measure and Gauss/orbital readout contract. |

## Source-mass quotient signature

| signature_id | object | required_identity | derivation | quotient_zero_condition | status |
| --- | --- | --- | --- | --- | --- |
| SMQ3636_0_decomposition | measured source monopole | mu_obs = G_eff M_eff(1+epsilon_mu) | This is the source-normalization identity already present in the constant-GM runner; it separates coupling, conserved source charge, and extra mass-channel hair. | partial_X ln G_eff = partial_X ln M_eff = partial_X ln(1+epsilon_mu) = 0 componentwise | IDENTITY_AVAILABLE_NOT_ZERO |
| SMQ3636_1_dimensionless_source_charge | beta_X_source | beta_X^H := partial_{X_N} ln mu_obs = partial_{X_N} ln G_eff + partial_{X_N} ln M_eff + partial_{X_N} ln(1+epsilon_mu) | Normalize the X/Z direction to a dimensionless coordinate X_N. Then beta_X is the source coupling that feeds J_X and source-charge residuals. | beta_X^H=0 for every source body/material/channel, with no cancellation credit unless parent identity proves it | DERIVED_NORMALIZED_COUPLING_DEFINITION |
| SMQ3636_2_projected_mass | M_eff | M_eff = integral_{S or Sigma} Pi_M J_H with Pi_M parent-derived before readout | This is the charge-current route: the mass used in Newtonian/orbital calibration must be the same parent Hilbert/Ward source charge, not a fitted orbital denominator. | partial_X Pi_M=0, partial_X J_H=0 in the fibre direction, and d(Pi_M J_H)=0 in the compact exterior | CONDITIONAL_NOT_PARENT_SIGNED |
| SMQ3636_3_GM_Gauss_readout | GM_obs | mu_obs=G_eff M_eff equals the Poisson/Gauss/orbital monopole in the same observed frame | A closed Hamiltonian/source charge is not enough; it must calibrate to the slow-particle inverse-square readout without importing orbital GM as a premise. | constant universal G_eff, absolute calibration, no radial/range hair, and no extra mass-channel charge | CONDITIONAL_NOT_PARENT_SIGNED |
| SMQ3636_4_source_zero_theorem | J_X_source | J_X_source = rho_H beta_X^H plus geometry/boundary terms after normalization | If beta_X^H=0 and geometry/boundary components vanish, the source current from 3635 is zero. | M_obs=M_bar(q), G_obs=G_bar(q), B_obs=B_bar(q) or proper/exact | THEOREM_CONDITIONAL_NOT_LIVE |

## Parent signature audit

| audit_id | required_clause | source_anchor | current_result | residual_if_failed |
| --- | --- | --- | --- | --- |
| SMA3636_0_Geff | G_eff/kappa_eff is parent-fixed, universal, derivative-silent, and range-blind | Z1_global_coupling_superselection; HSM541_6_constant_universal_G | OPEN_NOT_PARENT_DERIVED | dln_Geff_dt; eta_source_AB; alpha(lambda); delta_frame_source |
| SMA3636_1_Meff_flux | M_eff is a parent projected Hilbert/Ward source charge with d(Pi_M J_H)=0 | Z2_calibrated_PiM_flux_conservation; CC3; MF2; PM6 | OPEN_NOT_PARENT_DERIVED | dln_Meff_dt; partial_r_ln_mu_obs; Delta_PiM; Delta_flux |
| SMA3636_2_mu_extra | epsilon_mu=0 or universal derivative-free calibration with no active boundary/bulk/domain/memory/non-EH mass charge | Z3_mu_extra_zero_or_universal_constant; CC6; MF6 | FAILED_MISSING_COEFFICIENT_VECTOR | mu_extra_boundary_bulk_domain; R11_source_normalization_operator; alpha3; xi |
| SMA3636_3_species | source charge is species/material blind | Z4_species_blind_source_action; P8_species_source_charge | OPEN_NOT_PARENT_DERIVED | eta_source_AB |
| SMA3636_4_radial_range | measured source strength has no radial/range-dependent hair | Z5_no_radial_or_range_hair; P8_radial_source_hair; P8_range_dependence | OPEN_NOT_PARENT_DERIVED | partial_r_ln_mu_obs; alpha(lambda) |
| SMA3636_5_frame_calibration | source variation and matter/orbit readout use one observed frame | Z6_same_frame_source_pullback; CC1; Delta_frame | PARTIAL_CONDITIONAL_ONLY | delta_frame_source; clock/source calibration split |
| SMA3636_6_absolute_Gauss | Hamiltonian/source charge equals Poisson/Gauss/orbital monopole without circular orbital-GM import | CC7; MF5; HSM541_5 | OPEN_NOT_PARENT_DERIVED | Delta_cal; partial_r_ln_mu_obs; alpha(lambda) |
| SMA3636_7_verdict | M_obs=M_bar(q) is parent-signed for rest mass, GM, Hamiltonian source, and orbit readout | 3635 next target | SOURCE_MASS_QUOTIENT_NOT_SIGNED_JX_NORMALIZATION_REQUIRED | J_X_source normalized source-charge row active |

## JX normalization gate

| norm_id | quantity | definition | units | needed_input | score_status |
| --- | --- | --- | --- | --- | --- |
| JXN3636_0_field_coordinate | X_N | X_N := X / X_* is the dimensionless normalized fibre/source-coupling coordinate | dimensionless | field scale X_* or parent canonical normalization from the X/Z kinetic term | symbolic_normalization_declared_scale_missing |
| JXN3636_1_source_charge | beta_X^H | beta_X^H := partial_{X_N} ln mu_obs = partial_{X_N} ln G_eff + partial_{X_N} ln M_eff + partial_{X_N} ln(1+epsilon_mu) | dimensionless | component derivatives or theorem-zero certificates for G_eff, M_eff, epsilon_mu | formula_ready_components_missing |
| JXN3636_2_source_current_density | J_X_source | J_X_source = rho_H beta_X^H / X_* for dimensional X, or rho_H beta_X^H for dimensionless X_N | energy_density_per_X or energy_density_for_dimensionless_XN | rho_H convention, X_* or canonical field units, source support/worldtube | symbolic_current_law_units_not_fixed |
| JXN3636_3_test_charge | beta_X^T | beta_X^T := partial_{X_N} ln m_test_obs for the test body/clock/matter readout | dimensionless | test-body matter pullback and species/material marker map | needed_for_force_comparison_missing |
| JXN3636_4_force_projection | alpha_X(lambda_X) | alpha_X(lambda_X) = K_X beta_X^H beta_X^T with lambda_X=sqrt(Z_X/M_X^2), after parent Green-function normalization | dimensionless function of range | K_X, beta_X^H, beta_X^T, lambda_X, R10 bound curve | not_scoreable_until_operator_and_charges_numeric_or_zero |
| JXN3636_5_source_normalization_vector | D_a ln mu_obs | D_a ln mu_obs = D_a ln G_eff + D_a ln M_eff + D_a ln(1+epsilon_mu) for a in {t,r,A,lambda,frame} | yr^-1, inverse_length, dimensionless, or range-dependent by channel | channel derivatives and no-cancellation parent identity if terms are combined | runner_skeleton_ready_but_values_missing |

## First comparator channel

| comparator_id | rank | channel | observable_link | prediction_formula | bound_or_target | why_first | missing_to_score | score_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CMP3636_0_first_channel_species_source_charge | 1 | P8_species_source_charge | eta_source_AB;eta_WEP_source_charge | eta_source_AB = 2\|beta_X^A-beta_X^B\|/\|2+beta_X^A+beta_X^B\|, small-charge limit approx \|beta_X^A-beta_X^B\| | 2.8e-15 or derived universal source charge from existing template | dimensionless source-charge channel tests whether beta_X is species/material blind without needing an R10 curve first | beta_X^A, beta_X^B, test/source material map, parent field normalization if beta defined from dimensional X | comparator_selected_not_numeric |
| CMP3636_1_second_channel_Gdot | 2 | P8_Geff_time_drift plus P8_Meff_conservation | Gdot_over_G | d_t ln mu_obs = d_t ln G_eff + d_t ln M_eff + d_t ln(1+epsilon_mu) | 9.6e-15 yr^-1 or derived zero from existing template | time drift can score a source-normalization leak even when composition maps are unavailable | time derivative profile and separation of G_eff, M_eff, epsilon_mu | comparator_available_values_missing |
| CMP3636_2_third_channel_R10 | 3 | P8_range_dependence | delta_G_or_fifth_force_yukawa | alpha_X(lambda_X)=K_X beta_X^H beta_X^T | verified alpha(lambda) curve or derived zero | this is the direct R10/fifth-force channel, but it needs more machinery than eta_source_AB | K_X, lambda_X, beta_X charges, real bound curve | deferred_curve_and_operator_missing |

## Decisions

| decision_id | decision | status | next_action |
| --- | --- | --- | --- |
| DEC3636_0_source_quotient | Measured source mass/GM/Hamiltonian readout is not parent-signed as q-data in the live corpus. | SOURCE_MASS_QUOTIENT_NOT_SIGNED | do not claim Newton/local-GR source normalization from source descent alone |
| DEC3636_1_jx_normalization | J_X_source now has a normalized charge language: beta_X=partial_XN ln mu_obs and J_X_source=rho_H beta_X / X_*. | JX_NORMALIZATION_SYMBOLICALLY_DEFINED | fill beta_X component derivatives or prove beta_X=0 from parent quotient data |
| DEC3636_2_first_comparator | The first comparator channel should be source-charge WEP eta_source_AB, with Gdot second and R10 alpha(lambda) third. | FIRST_COMPARATOR_SELECTED | next target should derive species/material blindness or fill beta_X^A-beta_X^B row |

## Next target

| target_doc | target_script | objective | success_gate |
| --- | --- | --- | --- |
| 3637-Y5-R2FR-species-blind-source-charge-zero-or-betaX-row.md | scripts/Y5_R2FR_3637_species_blind_source_charge_zero_or_betaX_row.py | try to derive beta_X^A=beta_X^B for source/test species from parent matter/source quotient data; if not, create a beta_X species-difference row for eta_source_AB with units, material map, and bound target | either species/material blindness is theorem-zero from q-data, or eta_source_AB has a nonclaim executable beta_X difference skeleton tied to the 2.8e-15 target |
