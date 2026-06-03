# 468 - mu_extra Coefficient Vector to Local-Bound Scorecard

Private local-bound scorecard checkpoint. This is not a public measured-GM, Newtonian-limit, PPN, local-GR, cosmology, EM, or unified-field claim.

## 1. Question

Checkpoint 467 split `mu_extra` into eight source-normalization coefficients:

```text
epsilon_mu = sum_i epsilon_i.
```

This checkpoint maps those eight `epsilon_i` rows onto local-bound targets. It does not invent scores. If a coefficient, curve, operator vector, or theorem-zero source is missing, the row is explicitly not scoreable.

## 2. Run Metadata

| Field | Value |
| --- | --- |
| Script | `scripts/mu_extra_coefficient_vector_to_local_bound_scorecard.py` |
| Run directory | `runs\20260602-220000-mu-extra-coefficient-vector-to-local-bound-scorecard` |
| Status | `mu_extra_coefficient_vector_to_local_bound_scorecard_written_21_target_rows_no_numeric_predictions_no_score_no_Newton_or_local_GR_pass` |
| Claim ceiling | `mu_extra_local_bound_scorecard_only_no_mu_extra_zero_constant_GM_Newton_PPN_or_local_GR_pass` |
| Scorecard CSV | `source-intake\mts_residuals\P8_MU_EXTRA_LOCAL_BOUND_SCORECARD.csv` |
| Summary CSV | `source-intake\mts_residuals\P8_MU_EXTRA_CHANNEL_BOUND_SUMMARY.csv` |
| Required inputs CSV | `source-intake\mts_residuals\P8_MU_EXTRA_SCORECARD_REQUIRED_INPUTS.csv` |
| Decision CSV | `source-intake\mts_residuals\P8_MU_EXTRA_SCORECARD_DECISION.csv` |
| Next target | `469-fill-or-zero-highest-pressure-mu-extra-row.md` |

## 3. Source Register

| path | exists | role |
| --- | --- | --- |
| 467-mu-extra-zero-owner-or-source-normalization-coefficient-vector.md | True | eight epsilon_i coefficient vector and owner ledger |
| source-intake\mts_residuals\P8_MU_EXTRA_SOURCE_NORMALIZATION_COEFFICIENT_VECTOR.csv | True | machine-readable mu_extra coefficient vector |
| source-intake\mts_residuals\P8_MU_EXTRA_CHANNEL_OWNER_LEDGER.csv | True | machine-readable channel owner ledger |
| runs\20260602-094500-MTS-local-residual-vector-input-contract\results\residual_components.csv | True | local residual component contract with row locks |
| runs\20260602-061500-local-bound-runner-v4-real-data-interface\results\local_bounds_template.csv | True | runner-v4 local-bound template rows |
| runs\20260602-041500-runner-v3-numeric-smoke-extension\results\channel_bound_requirements.csv | True | channel-to-row source-lock requirements |
| runs\20260602-041500-runner-v3-numeric-smoke-extension\results\aggregate_channel_bounds.csv | True | aggregate channel bound summaries from runner-v3 numeric smoke extension |

## 4. Scoring Rule

For each channel-target pair:

```text
predicted residual = response_map(epsilon_i)
pass only if abs(predicted residual) <= target bound
or the channel has a sourced theorem-zero certificate.
```

For `R10`, a scalar placeholder is illegal: an executable `alpha(lambda)` curve is required. For `R11`, an executable operator vector or EH-only theorem is required.

## 5. Local-Bound Scorecard

The scorecard has been written to `source-intake\mts_residuals\P8_MU_EXTRA_LOCAL_BOUND_SCORECARD.csv`.

| model_id | branch_id | epsilon_channel | epsilon_symbol | target_row | observable | mapping_type | response_expression | predicted_input | bound_value | bound_units | bound_source | pass_condition | score_status | reason_not_scoreable | valid_for_claim | required_artifact | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_source_normalized_Newton_branch | mu_extra_local_bound_scorecard | radial_Meff_hair | epsilon_radial_Meff | R4_beta | beta_minus_1 | direct_or_mapped | beta_minus_1 ~ F_radial_beta[epsilon_radial_Meff] | MISSING_DERIVED_ZERO_OR_NUMERIC_COEFFICIENT | 7.8e-05 | dimensionless | runs\20260602-094500-MTS-local-residual-vector-input-contract\results\residual_components.csv | abs(predicted beta_minus_1) <= 7.8e-05 dimensionless, or theorem-zero source | not_scoreable_prediction_missing | MTS prediction, curve, operator vector, or theorem-zero source is missing | false | P8_radial_mu_profile_or_zero.csv | derive radial no-hair or fill epsilon_radial_Meff(r) |
| MTS_source_normalized_Newton_branch | mu_extra_local_bound_scorecard | radial_Meff_hair | epsilon_radial_Meff | R10_fifth_force | delta_G_or_fifth_force_yukawa | curve_required | alpha(lambda) from radial/range source profile | MISSING_ALPHA_LAMBDA_CURVE_OR_THEOREM_ZERO | alpha(lambda) | range-dependent | runs\20260602-094500-MTS-local-residual-vector-input-contract\results\residual_components.csv | for every lambda: abs(alpha_predicted(lambda)) <= alpha_bound(lambda), or theorem-zero | not_scoreable_prediction_missing | MTS prediction, curve, operator vector, or theorem-zero source is missing | false | R10_alpha_lambda_curve_MTS_source_normalization.csv | derive radial no-hair or fill epsilon_radial_Meff(r) |
| MTS_source_normalized_Newton_branch | mu_extra_local_bound_scorecard | boundary_monopole_shift | epsilon_boundary | R4_beta | beta_minus_1 | direct_or_mapped | beta_minus_1 ~ F_boundary_beta[epsilon_boundary] | MISSING_DERIVED_ZERO_OR_NUMERIC_COEFFICIENT | 7.8e-05 | dimensionless | runs\20260602-094500-MTS-local-residual-vector-input-contract\results\residual_components.csv | abs(predicted beta_minus_1) <= 7.8e-05 dimensionless, or theorem-zero source | not_scoreable_prediction_missing | MTS prediction, curve, operator vector, or theorem-zero source is missing | false | P8_mu_extra_boundary_coefficients.csv | derive boundary no-hair or fill epsilon_boundary |
| MTS_source_normalized_Newton_branch | mu_extra_local_bound_scorecard | boundary_monopole_shift | epsilon_boundary | R7_alpha3 | alpha3 | flux_map_required | alpha3 ~ F_boundary_flux[epsilon_boundary] | MISSING_DERIVED_ZERO_OR_NUMERIC_COEFFICIENT | 4e-20 | dimensionless | runs\20260602-094500-MTS-local-residual-vector-input-contract\results\residual_components.csv | abs(predicted alpha3) <= 4e-20 dimensionless, or theorem-zero source | not_scoreable_prediction_missing | MTS prediction, curve, operator vector, or theorem-zero source is missing | false | P8_mu_extra_boundary_coefficients.csv | derive boundary no-hair or fill epsilon_boundary |
| MTS_source_normalized_Newton_branch | mu_extra_local_bound_scorecard | boundary_monopole_shift | epsilon_boundary | R8_xi | xi | anisotropy_map_required | xi ~ F_boundary_shear[epsilon_boundary] | MISSING_DERIVED_ZERO_OR_NUMERIC_COEFFICIENT | 4e-09 | dimensionless | runs\20260602-094500-MTS-local-residual-vector-input-contract\results\residual_components.csv | abs(predicted xi) <= 4e-09 dimensionless, or theorem-zero source | not_scoreable_prediction_missing | MTS prediction, curve, operator vector, or theorem-zero source is missing | false | P8_mu_extra_boundary_coefficients.csv | derive boundary no-hair or fill epsilon_boundary |
| MTS_source_normalized_Newton_branch | mu_extra_local_bound_scorecard | boundary_monopole_shift | epsilon_boundary | R9_Gdot | Gdot_over_G | time_derivative_required | Gdot/G ~ d epsilon_boundary/dt | MISSING_DERIVED_ZERO_OR_NUMERIC_COEFFICIENT | 9.6e-15 | yr^-1 | runs\20260602-094500-MTS-local-residual-vector-input-contract\results\residual_components.csv | abs(predicted Gdot_over_G) <= 9.6e-15 yr^-1, or theorem-zero source | not_scoreable_prediction_missing | MTS prediction, curve, operator vector, or theorem-zero source is missing | false | P8_mu_extra_boundary_coefficients.csv | derive boundary no-hair or fill epsilon_boundary |
| MTS_source_normalized_Newton_branch | mu_extra_local_bound_scorecard | domain_projector_mass | epsilon_domain_projector | R5_alpha1 | alpha1 | vector_map_required | alpha1 ~ F_domain_vector[epsilon_domain_projector] | MISSING_DERIVED_ZERO_OR_NUMERIC_COEFFICIENT | 1e-04 | dimensionless | runs\20260602-094500-MTS-local-residual-vector-input-contract\results\residual_components.csv | abs(predicted alpha1) <= 1e-04 dimensionless, or theorem-zero source | not_scoreable_prediction_missing | MTS prediction, curve, operator vector, or theorem-zero source is missing | false | P8_mu_extra_domain_projector_coefficients.csv | derive projector no-leak theorem or fill epsilon_domain_projector |
| MTS_source_normalized_Newton_branch | mu_extra_local_bound_scorecard | domain_projector_mass | epsilon_domain_projector | R6_alpha2 | alpha2 | vector_map_required | alpha2 ~ F_domain_vector[epsilon_domain_projector] | MISSING_DERIVED_ZERO_OR_NUMERIC_COEFFICIENT | 2e-09 | dimensionless | runs\20260602-094500-MTS-local-residual-vector-input-contract\results\residual_components.csv | abs(predicted alpha2) <= 2e-09 dimensionless, or theorem-zero source | not_scoreable_prediction_missing | MTS prediction, curve, operator vector, or theorem-zero source is missing | false | P8_mu_extra_domain_projector_coefficients.csv | derive projector no-leak theorem or fill epsilon_domain_projector |
| MTS_source_normalized_Newton_branch | mu_extra_local_bound_scorecard | domain_projector_mass | epsilon_domain_projector | R7_alpha3 | alpha3 | flux_map_required | alpha3 ~ F_domain_flux[epsilon_domain_projector] | MISSING_DERIVED_ZERO_OR_NUMERIC_COEFFICIENT | 4e-20 | dimensionless | runs\20260602-094500-MTS-local-residual-vector-input-contract\results\residual_components.csv | abs(predicted alpha3) <= 4e-20 dimensionless, or theorem-zero source | not_scoreable_prediction_missing | MTS prediction, curve, operator vector, or theorem-zero source is missing | false | P8_mu_extra_domain_projector_coefficients.csv | derive projector no-leak theorem or fill epsilon_domain_projector |
| MTS_source_normalized_Newton_branch | mu_extra_local_bound_scorecard | domain_projector_mass | epsilon_domain_projector | R8_xi | xi | anisotropy_map_required | xi ~ F_domain_anisotropy[epsilon_domain_projector] | MISSING_DERIVED_ZERO_OR_NUMERIC_COEFFICIENT | 4e-09 | dimensionless | runs\20260602-094500-MTS-local-residual-vector-input-contract\results\residual_components.csv | abs(predicted xi) <= 4e-09 dimensionless, or theorem-zero source | not_scoreable_prediction_missing | MTS prediction, curve, operator vector, or theorem-zero source is missing | false | P8_mu_extra_domain_projector_coefficients.csv | derive projector no-leak theorem or fill epsilon_domain_projector |
| MTS_source_normalized_Newton_branch | mu_extra_local_bound_scorecard | domain_projector_mass | epsilon_domain_projector | R11_EH_operator_ledger | non_EH_operator_coefficients | operator_vector_required | c_source_normalization_operator includes epsilon_domain_projector | MISSING_OPERATOR_VECTOR_OR_THEOREM_ZERO | symbolic | operator family | runs\20260602-094500-MTS-local-residual-vector-input-contract\results\residual_components.csv | operator coefficient vector supplied and every mapped residual row passes, or EH-only theorem-zero | not_scoreable_prediction_missing | MTS prediction, curve, operator vector, or theorem-zero source is missing | false | R11_nonEH_operator_vector_executable.csv | derive projector no-leak theorem or fill epsilon_domain_projector |
| MTS_source_normalized_Newton_branch | mu_extra_local_bound_scorecard | bulk_X_Yukawa_tail | epsilon_bulk_X | R10_fifth_force | delta_G_or_fifth_force_yukawa | curve_required | alpha_X(lambda_X) from epsilon_bulk_X and range law | MISSING_ALPHA_LAMBDA_CURVE_OR_THEOREM_ZERO | alpha(lambda) | range-dependent | runs\20260602-094500-MTS-local-residual-vector-input-contract\results\residual_components.csv | for every lambda: abs(alpha_predicted(lambda)) <= alpha_bound(lambda), or theorem-zero | not_scoreable_prediction_missing | MTS prediction, curve, operator vector, or theorem-zero source is missing | false | R10_alpha_lambda_curve_MTS_source_normalization.csv | fill epsilon_bulk_X plus lambda_X or theorem-zero |
| MTS_source_normalized_Newton_branch | mu_extra_local_bound_scorecard | nonEH_operator_potential | epsilon_nonEH_source | R3_gamma | gamma_minus_1 | operator_map_required | gamma-1 ~ F_nonEH_gamma[epsilon_nonEH_source] | MISSING_DERIVED_ZERO_OR_NUMERIC_COEFFICIENT | 2.3e-05 | dimensionless | runs\20260602-094500-MTS-local-residual-vector-input-contract\results\residual_components.csv | abs(predicted gamma_minus_1) <= 2.3e-05 dimensionless, or theorem-zero source | not_scoreable_prediction_missing | MTS prediction, curve, operator vector, or theorem-zero source is missing | false | R11_nonEH_operator_vector_executable.csv | derive EH-only or map non-EH coefficients into epsilon_nonEH_source |
| MTS_source_normalized_Newton_branch | mu_extra_local_bound_scorecard | nonEH_operator_potential | epsilon_nonEH_source | R4_beta | beta_minus_1 | operator_map_required | beta-1 ~ F_nonEH_beta[epsilon_nonEH_source] | MISSING_DERIVED_ZERO_OR_NUMERIC_COEFFICIENT | 7.8e-05 | dimensionless | runs\20260602-094500-MTS-local-residual-vector-input-contract\results\residual_components.csv | abs(predicted beta_minus_1) <= 7.8e-05 dimensionless, or theorem-zero source | not_scoreable_prediction_missing | MTS prediction, curve, operator vector, or theorem-zero source is missing | false | R11_nonEH_operator_vector_executable.csv | derive EH-only or map non-EH coefficients into epsilon_nonEH_source |
| MTS_source_normalized_Newton_branch | mu_extra_local_bound_scorecard | nonEH_operator_potential | epsilon_nonEH_source | R10_fifth_force | delta_G_or_fifth_force_yukawa | curve_required | alpha(lambda) from non-EH finite-range mode if present | MISSING_ALPHA_LAMBDA_CURVE_OR_THEOREM_ZERO | alpha(lambda) | range-dependent | runs\20260602-094500-MTS-local-residual-vector-input-contract\results\residual_components.csv | for every lambda: abs(alpha_predicted(lambda)) <= alpha_bound(lambda), or theorem-zero | not_scoreable_prediction_missing | MTS prediction, curve, operator vector, or theorem-zero source is missing | false | R10_alpha_lambda_curve_MTS_source_normalization.csv | derive EH-only or map non-EH coefficients into epsilon_nonEH_source |
| MTS_source_normalized_Newton_branch | mu_extra_local_bound_scorecard | nonEH_operator_potential | epsilon_nonEH_source | R11_EH_operator_ledger | non_EH_operator_coefficients | operator_vector_required | c_nonEH_operator_vector maps to epsilon_nonEH_source | MISSING_OPERATOR_VECTOR_OR_THEOREM_ZERO | symbolic | operator family | runs\20260602-094500-MTS-local-residual-vector-input-contract\results\residual_components.csv | operator coefficient vector supplied and every mapped residual row passes, or EH-only theorem-zero | not_scoreable_prediction_missing | MTS prediction, curve, operator vector, or theorem-zero source is missing | false | R11_nonEH_operator_vector_executable.csv | derive EH-only or map non-EH coefficients into epsilon_nonEH_source |
| MTS_source_normalized_Newton_branch | mu_extra_local_bound_scorecard | species_source_charge | epsilon_species_A | R1_WEP_source_charge | eta_WEP_source_charge | composition_map_required | eta_source_AB ~ Delta_AB ln(1+epsilon_species_A) | MISSING_DERIVED_ZERO_OR_NUMERIC_COEFFICIENT | 2.8e-15 | dimensionless | runs\20260602-094500-MTS-local-residual-vector-input-contract\results\residual_components.csv | abs(predicted eta_WEP_source_charge) <= 2.8e-15 dimensionless, or theorem-zero source | not_scoreable_prediction_missing | MTS prediction, curve, operator vector, or theorem-zero source is missing | false | P8_species_source_charge_residual_or_zero.csv | derive selector-blind source action or fill epsilon_species_A |
| MTS_source_normalized_Newton_branch | mu_extra_local_bound_scorecard | species_source_charge | epsilon_species_A | R2_clock_redshift | alpha_clock_redshift | clock_source_map_required | alpha_clock ~ F_clock_source[epsilon_species_A] | MISSING_DERIVED_ZERO_OR_NUMERIC_COEFFICIENT | 2.48e-05 | dimensionless | runs\20260602-094500-MTS-local-residual-vector-input-contract\results\residual_components.csv | abs(predicted alpha_clock_redshift) <= 2.48e-05 dimensionless, or theorem-zero source | not_scoreable_prediction_missing | MTS prediction, curve, operator vector, or theorem-zero source is missing | false | P8_species_source_charge_residual_or_zero.csv | derive selector-blind source action or fill epsilon_species_A |
| MTS_source_normalized_Newton_branch | mu_extra_local_bound_scorecard | time_drift | epsilon_time_drift | R9_Gdot | Gdot_over_G | time_derivative_required | Gdot/G ~ d epsilon_time_drift/dt | MISSING_DERIVED_ZERO_OR_NUMERIC_COEFFICIENT | 9.6e-15 | yr^-1 | runs\20260602-094500-MTS-local-residual-vector-input-contract\results\residual_components.csv | abs(predicted Gdot_over_G) <= 9.6e-15 yr^-1, or theorem-zero source | not_scoreable_prediction_missing | MTS prediction, curve, operator vector, or theorem-zero source is missing | false | P8_time_drift_residual_or_zero.csv | derive stationarity or fill epsilon_time_drift |
| MTS_source_normalized_Newton_branch | mu_extra_local_bound_scorecard | absolute_calibration_offset | epsilon_calibration | R4_beta | beta_minus_1 | calibration_owner_required | beta-1 unaffected only if epsilon_calibration is parent-fixed constant | MISSING_DERIVED_ZERO_OR_NUMERIC_COEFFICIENT | 7.8e-05 | dimensionless | runs\20260602-094500-MTS-local-residual-vector-input-contract\results\residual_components.csv | abs(predicted beta_minus_1) <= 7.8e-05 dimensionless, or theorem-zero source | not_scoreable_prediction_missing | MTS prediction, curve, operator vector, or theorem-zero source is missing | false | P8_absolute_calibration_owner.csv | derive parent-fixed calibration or retain epsilon_calibration |
| MTS_source_normalized_Newton_branch | mu_extra_local_bound_scorecard | absolute_calibration_offset | epsilon_calibration | R9_Gdot | Gdot_over_G | time_derivative_required | Gdot/G ~ d epsilon_calibration/dt | MISSING_DERIVED_ZERO_OR_NUMERIC_COEFFICIENT | 9.6e-15 | yr^-1 | runs\20260602-094500-MTS-local-residual-vector-input-contract\results\residual_components.csv | abs(predicted Gdot_over_G) <= 9.6e-15 yr^-1, or theorem-zero source | not_scoreable_prediction_missing | MTS prediction, curve, operator vector, or theorem-zero source is missing | false | P8_absolute_calibration_owner.csv | derive parent-fixed calibration or retain epsilon_calibration |

## 6. Channel Summary

The channel summary has been written to `source-intake\mts_residuals\P8_MU_EXTRA_CHANNEL_BOUND_SUMMARY.csv`.

| epsilon_channel | epsilon_symbol | target_rows | numeric_target_count | curve_required | operator_vector_required | tightest_numeric_bound | tightest_numeric_units | tightest_numeric_row | scoreable_rows | blocked_rows | claim_status | next_required_artifact |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| radial_Meff_hair | epsilon_radial_Meff | R4_beta;R10_fifth_force | 1 | True | False | 7.8e-05 | dimensionless | R4_beta | 0 | 2 | not_claimable | P8_radial_mu_profile_or_zero.csv;R10_alpha_lambda_curve_MTS_source_normalization.csv |
| boundary_monopole_shift | epsilon_boundary | R4_beta;R7_alpha3;R8_xi;R9_Gdot | 4 | False | False | 4e-20 | dimensionless | R7_alpha3 | 0 | 4 | not_claimable | P8_mu_extra_boundary_coefficients.csv |
| domain_projector_mass | epsilon_domain_projector | R5_alpha1;R6_alpha2;R7_alpha3;R8_xi;R11_EH_operator_ledger | 4 | False | True | 4e-20 | dimensionless | R7_alpha3 | 0 | 5 | not_claimable | P8_mu_extra_domain_projector_coefficients.csv;R11_nonEH_operator_vector_executable.csv |
| bulk_X_Yukawa_tail | epsilon_bulk_X | R10_fifth_force | 0 | True | False | none | none | none | 0 | 1 | not_claimable | R10_alpha_lambda_curve_MTS_source_normalization.csv |
| nonEH_operator_potential | epsilon_nonEH_source | R3_gamma;R4_beta;R10_fifth_force;R11_EH_operator_ledger | 2 | True | True | 2.3e-05 | dimensionless | R3_gamma | 0 | 4 | not_claimable | R10_alpha_lambda_curve_MTS_source_normalization.csv;R11_nonEH_operator_vector_executable.csv |
| species_source_charge | epsilon_species_A | R1_WEP_source_charge;R2_clock_redshift | 2 | False | False | 2.8e-15 | dimensionless | R1_WEP_source_charge | 0 | 2 | not_claimable | P8_species_source_charge_residual_or_zero.csv |
| time_drift | epsilon_time_drift | R9_Gdot | 1 | False | False | 9.6e-15 | yr^-1 | R9_Gdot | 0 | 1 | not_claimable | P8_time_drift_residual_or_zero.csv |
| absolute_calibration_offset | epsilon_calibration | R4_beta;R9_Gdot | 2 | False | False | 9.6e-15 | yr^-1 | R9_Gdot | 0 | 2 | not_claimable | P8_absolute_calibration_owner.csv |

## 7. Required Inputs

The required-input queue has been written to `source-intake\mts_residuals\P8_MU_EXTRA_SCORECARD_REQUIRED_INPUTS.csv`.

| priority | input_artifact | unblocks_channels | unblocks_rows | minimum_content | acceptance_gate |
| --- | --- | --- | --- | --- | --- |
| 1 | P8_mu_extra_boundary_coefficients.csv | boundary_monopole_shift | R4_beta;R7_alpha3;R8_xi;R9_Gdot | epsilon_boundary value or theorem-zero source plus maps to beta/alpha3/xi/Gdot | all mapped rows score below locks; alpha3 lock is 4e-20 if flux-like |
| 2 | P8_mu_extra_domain_projector_coefficients.csv | domain_projector_mass | R5_alpha1;R6_alpha2;R7_alpha3;R8_xi;R11_EH_operator_ledger | epsilon_domain_projector or theorem-zero plus vector/flux/anisotropy maps | preferred-frame/location and R11 operator rows score or zero |
| 3 | R10_alpha_lambda_curve_MTS_source_normalization.csv | radial_Meff_hair;bulk_X_Yukawa_tail;nonEH_operator_potential | R10_fifth_force | lambda, lambda_units, alpha_predicted, alpha_bound, source path, assumptions | alpha_predicted(lambda) below alpha_bound(lambda) for all curve rows or theorem-zero |
| 4 | R11_nonEH_operator_vector_executable.csv | nonEH_operator_potential | R3_gamma;R4_beta;R10_fifth_force;R11_EH_operator_ledger | non-EH coefficients, units, normalization, weak-field maps, source paths | R11 vector rows have no MISSING_ fields and mapped residuals pass |
| 5 | P8_species_source_charge_residual_or_zero.csv | species_source_charge | R1_WEP_source_charge;R2_clock_redshift | eta_source_AB or theorem-zero plus clock/source split map | eta_source_AB <= 2.8e-15 and clock row mapped or zero |
| 6 | P8_time_drift_residual_or_zero.csv | time_drift | R9_Gdot | d epsilon_time_drift/dt or theorem-zero in yr^-1 | abs(Gdot_over_G contribution) <= 9.6e-15 yr^-1 |
| 7 | P8_radial_mu_profile_or_zero.csv | radial_Meff_hair | R4_beta;R10_fifth_force | epsilon_radial_Meff(r), radial derivative/profile, or no-hair theorem | radial profile maps below beta/R10 locks or is theorem-zero |
| 8 | P8_absolute_calibration_owner.csv | absolute_calibration_offset | R4_beta;R9_Gdot | parent-fixed universal constant proof with zero derivative/source/range/frame dependence | constant calibration is universal and derivative-silent, otherwise coefficient row remains retained |

## 8. Decision

| decision_item | status | evidence | next_action |
| --- | --- | --- | --- |
| source_paths | pass | missing source paths = 0 | continue with cited input artifacts |
| scorecard_written | pass | scorecard rows = 21; channel summaries = 8 | use scorecard as local-bound target table |
| numeric_predictions_available | fail | score-ready rows = 0; blocked rows = 21 | fill epsilon coefficients, curves, operator vectors, or theorem-zero sources |
| curve_rows_ready | fail | curve-required rows = 3; curve file not loaded | build R10_alpha_lambda_curve_MTS_source_normalization.csv |
| operator_rows_ready | fail | operator-vector-required rows = 2; executable R11 vector not loaded | build R11_nonEH_operator_vector_executable.csv or EH-only theorem |
| mu_extra_score_passed | fail | no scorecard row has a numeric/theorem-zero prediction | 469-fill-or-zero-highest-pressure-mu-extra-row.md |
| Newton_or_local_GR_promoted | fail | mu_extra scorecard is target-only, not passed | keep no-claim ceiling |

## 9. Result

The scorecard is now executable as a target table: `21` channel-target rows across `8` epsilon channels.

It is not yet a passed empirical result. Every score row is blocked because the MTS-side prediction is still missing: numeric coefficient, theorem-zero proof, `alpha(lambda)` curve, or non-EH operator vector.

Practical read: this is the fair version of the boxing match. We are not demanding a knockout; we are setting the judges' cards. Each `epsilon_i` gets its opponent and its required evidence. If MTS can slip these punches with theorem-zero or below-bound coefficients, it stays in the round.

## 10. Next Queue

| Priority | Target | Reason |
| --- | --- | --- |
| 1 | `469-fill-or-zero-highest-pressure-mu-extra-row.md` | choose the highest-pressure row and either fill it or prove it zero |
| 2 | `R10_alpha_lambda_curve_MTS_source_normalization.csv` | three scorecard rows require executable range curves |
| 3 | `R11_nonEH_operator_vector_executable.csv` | two scorecard rows require executable operator-vector input |
