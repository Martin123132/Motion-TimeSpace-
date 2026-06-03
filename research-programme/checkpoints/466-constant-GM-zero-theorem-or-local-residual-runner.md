# 466 - Constant-GM Zero Theorem or Local Residual Runner

Private source-normalization checkpoint. This is not a public measured-GM, Newtonian-limit, PPN, local-GR, cosmology, EM, or unified-field claim.

## 1. Question

Checkpoint 465 gave the exact law

```text
D_X ln mu_obs
  = D_X ln G_eff
  + D_X ln M_eff
  + D_X ln(1 + epsilon_mu).
```

This checkpoint asks whether the zero theorem closes now. If it does not, the same terms must become local residual rows with bound targets.

## 2. Run Metadata

| Field | Value |
| --- | --- |
| Script | `scripts/constant_GM_zero_theorem_or_local_residual_runner.py` |
| Run directory | `runs\20260602-213000-constant-GM-zero-theorem-or-local-residual-runner` |
| Status | `constant_GM_zero_theorem_or_local_residual_runner_written_conditional_zero_theorem_failed_local_residual_runner_inputs_loaded_no_Newton_or_local_GR_pass` |
| Claim ceiling | `constant_GM_zero_or_residual_runner_only_no_constant_GM_Newton_PPN_or_local_GR_pass` |
| Zero theorem CSV | `source-intake\mts_residuals\P8_CONSTANT_GM_ZERO_THEOREM_ATTEMPT.csv` |
| Local runner input CSV | `source-intake\mts_residuals\P8_CONSTANT_GM_LOCAL_RESIDUAL_RUNNER_INPUT.csv` |
| Bound matrix CSV | `source-intake\mts_residuals\P8_CONSTANT_GM_RESIDUAL_BOUND_MATRIX.csv` |
| Decision CSV | `source-intake\mts_residuals\P8_CONSTANT_GM_ZERO_OR_RESIDUAL_DECISION.csv` |
| Next target | `467-mu-extra-zero-owner-or-source-normalization-coefficient-vector.md` |

## 3. Source Register

| path | exists | role |
| --- | --- | --- |
| 465-constant-GM-derivative-hair-fill-gate.md | True | exact D_X ln mu_obs derivative-hair law and CGM channel map |
| source-intake\mts_residuals\P8_CONSTANT_GM_DERIVATIVE_HAIR_GATE.csv | True | machine-readable derivative-hair rows |
| source-intake\mts_residuals\P8_CONSTANT_GM_DERIVATIVE_HAIR_FILL_QUEUE.csv | True | minimum fill queue from 465 |
| source-intake\mts_residuals\P8_source_normalization_residual_vector_TEMPLATE.csv | True | P8 source-normalization residual template with bound targets |
| runs\20260602-094500-MTS-local-residual-vector-input-contract\results\residual_components.csv | True | local residual vector contract with source locks for eta, Gdot, R10, R11 |
| source-intake\mts_residuals\R11_SOURCE_NORMALIZATION_DERIVATIVE_HAIR_VECTOR.csv | True | R11 source-normalization derivative vector from 465 |
| 461-PG-residual-input-derive-or-fill-gate.md | True | P8 rows retained/unfilled before this runner |
| 462-charge-current-equality-direct-derivation-attempt.md | True | charge-current equality residual decomposition |
| 464-R11-executable-vector-minimum-fill-skeleton.md | True | source_normalization_operator priority and R10 link requirement |

## 4. Conditional Zero Theorem

The theorem shape is now exact:

```text
If
  D_X ln G_eff = 0,
  D_X ln M_eff = 0,
  D_X epsilon_mu = 0
for every local channel X,
then
  D_X ln mu_obs = 0
for every local channel X.
```

This is a useful conditional theorem, but it is not a proof of the premises.

| premise_id | premise | mathematical_form | current_status | evidence_now | failure_if_missing | residual_channel_activated | promotion_effect | next_action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Z0_decomposition_identity | measured source decomposition exists | mu_obs = G_eff M_eff + mu_extra = G_eff M_eff(1+epsilon_mu) | pass_identity | 465 derives epsilon_mu and D_X ln mu_obs law | no source-normalized GM language | none | identity credit only | use the identity as the runner backbone |
| Z1_global_coupling_superselection | G_eff is parent-fixed and derivative-silent | D_X ln G_eff = 0 for X=t,r,A,lambda,frame,domain | open_not_parent_derived | constant-coupling contracts exist but 461 retains dln_Geff_dt | local Gdot or source/range/frame coupling drift | P8_Geff_time_drift | blocks constant GM and local GR | derive superselection or fill drift/source/range residual rows |
| Z2_calibrated_PiM_flux_conservation | M_eff is a conserved calibrated source charge | D_X ln M_eff = 0 and d(Pi_M J_H)=0 in compact exterior | open_not_parent_derived | Pi_M/charge-current route is conditional; 462 leaves Delta_flux and Delta_PiM active | mass flux, memory exchange, or beta/Gdot source drift | P8_Meff_conservation | blocks measured source mass | derive calibrated Pi_M Ward flux closure or fill dln_Meff_dt |
| Z3_mu_extra_zero_or_universal_constant | epsilon_mu has no active derivative hair | epsilon_mu=0, or epsilon_mu=constant universal calibration and D_X epsilon_mu=0 | failed_missing_coefficient_vector | 465 R11 vector still has MISSING_ markers for epsilon_mu and mu_extra | hidden boundary/bulk/domain/memory/non-EH measured-GM contribution | P8_boundary_bulk_domain_mu_extra;R11_source_normalization_operator | blocks Newton source normalization | try mu_extra owner theorem; otherwise fill coefficient vector |
| Z4_species_blind_source_action | source charge is species/material blind | Delta_AB ln mu_obs = 0 or eta_source_AB = 0 | open_not_parent_derived | 461 keeps direct WEP separate from source-charge WEP | composition-dependent gravitational source charge | P8_species_source_charge | blocks full WEP/source-normalized Newton | derive selector-blind source action or fill eta_source_AB row |
| Z5_no_radial_or_range_hair | no radial/range-dependent measured-GM profile | partial_r ln mu_obs = 0 and alpha(lambda)=0, or executable curves remain below bounds | open_not_parent_derived | R10 link required but missing; radial profile not loaded | radius/range-dependent Newton constant or fifth force | P8_radial_source_hair;P8_range_dependence | blocks inverse-square Newton claim | derive no-range/no-radial theorem or build alpha(lambda)/radial profile inputs |
| Z6_same_frame_source_pullback | source variation and matter readout use one parent-selected observed frame | Delta_frame ln mu_obs = 0 | partial_conditional_only | same-frame matter route exists conditionally, but source variation is not parent-derived | frame/source calibration split | P8_frame_calibration_split | blocks same-frame Newton | attach frame theorem to source variation, not only geodesic readout |
| Z7_parent_identity_cancellation | any cancellation among derivative terms is a parent identity | D_X ln G_eff + D_X ln M_eff + D_X ln(1+epsilon_mu) == 0 as an identity | not_supplied | 465 explicitly forbids tuned cancellation | post-hoc cancellation treated as derivation | all_nonzero_channels | no cancellation credit | do not allow tuned cancellation in runner scoring |
| Z8_second_order_source_stability | first-order source normalization survives PPN second order | delta_beta_source=0 and gamma-1=0 after measured-GM normalization | deferred_until_first_order_rows_scored | 461 and 465 defer beta/gamma source-normalized vector | Newton-only branch cannot become local GR | P8_nonlinear_beta_source_residue | blocks local GR promotion | run second-order PPN source vector after Z1-Z7 are scored |

## 5. Local Residual Runner Input

The local runner input has been written to `source-intake\mts_residuals\P8_CONSTANT_GM_LOCAL_RESIDUAL_RUNNER_INPUT.csv`.

| model_id | branch_id | component_id | symbol | derivative_channel | observable_link | predicted_value | prediction_units | bound_or_target | bound_source | formula_reference | input_source_file | derivation_status | runner_state | valid_for_claim | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_source_normalized_Newton_branch | constant_GM_zero_or_residual_runner | P8_boundary_bulk_domain_mu_extra | epsilon_mu = mu_extra/(G_eff M_eff) | amplitude;D_t;D_r;D_A;D_lambda;Delta_frame | gamma;beta;alpha3;xi;Gdot;operator_ledger | MISSING_NUMERIC_OR_DERIVED_ZERO_EPSILON_MU_VECTOR | dimensionless | zero owned exchange or coefficient residuals below row locks | source-intake\mts_residuals\P8_source_normalization_residual_vector_TEMPLATE.csv | epsilon_mu := mu_extra/(G_eff M_eff) | source-intake\mts_residuals\R11_SOURCE_NORMALIZATION_DERIVATIVE_HAIR_VECTOR.csv | retained_unfilled | not_scoreable_prediction_missing | false | highest priority; constant universal calibration may be absorbed, derivative hair may not |
| MTS_source_normalized_Newton_branch | constant_GM_zero_or_residual_runner | P8_Geff_time_drift | dln_Geff_dt | D_t | Gdot_over_G | MISSING_NUMERIC_OR_DERIVED_ZERO_DRIFT | yr^-1 | 9.6e-15 yr^-1 or derived zero | source-intake\mts_residuals\P8_source_normalization_residual_vector_TEMPLATE.csv | d ln mu_obs/dt = d ln G_eff/dt + d ln M_eff/dt + d ln(1+epsilon_mu)/dt | source-intake\mts_residuals\P8_CONSTANT_GM_DERIVATIVE_HAIR_GATE.csv | retained_unfilled | not_scoreable_prediction_missing | false | must be separated from dln_Meff_dt and epsilon_mu drift |
| MTS_source_normalized_Newton_branch | constant_GM_zero_or_residual_runner | P8_Meff_conservation | dln_Meff_dt | D_t;flux | beta_minus_1;Gdot_over_G | MISSING_NUMERIC_OR_DERIVED_ZERO_MASS_FLUX | yr^-1 | beta/Gdot locks or derived conservation | source-intake\mts_residuals\P8_source_normalization_residual_vector_TEMPLATE.csv | D_X ln mu_obs identity plus Pi_M flux closure | source-intake\mts_residuals\P8_CONSTANT_GM_DERIVATIVE_HAIR_GATE.csv | retained_unfilled | not_scoreable_prediction_missing | false | mass conservation has to be owned by Pi_M/Ward flux, not assumed |
| MTS_source_normalized_Newton_branch | constant_GM_zero_or_residual_runner | P8_species_source_charge | eta_source_AB | D_A;Delta_AB | eta_WEP_source_charge | MISSING_NUMERIC_OR_DERIVED_ZERO_SOURCE_CHARGE | dimensionless | 2.8e-15 or derived universal source charge | source-intake\mts_residuals\P8_source_normalization_residual_vector_TEMPLATE.csv | Delta_AB ln mu_obs = 0 | source-intake\mts_residuals\P8_CONSTANT_GM_DERIVATIVE_HAIR_GATE.csv | retained_unfilled | not_scoreable_prediction_missing | false | direct coframe WEP cannot automatically fill source-charge WEP |
| MTS_source_normalized_Newton_branch | constant_GM_zero_or_residual_runner | P8_radial_source_hair | partial_r_ln_mu_obs | D_r | gamma_minus_1;beta_minus_1;alpha(lambda) | MISSING_RADIAL_PROFILE_OR_DERIVED_ZERO | inverse_length_or_dimensionless_envelope | zero radial hair or mapped PPN/fifth-force residuals | source-intake\mts_residuals\P8_source_normalization_residual_vector_TEMPLATE.csv | partial_r ln mu_obs = partial_r ln G_eff + partial_r ln M_eff + partial_r ln(1+epsilon_mu) | source-intake\mts_residuals\P8_CONSTANT_GM_DERIVATIVE_HAIR_GATE.csv | retained_unfilled | not_scoreable_prediction_missing | false | single-radius calibration does not clear this row |
| MTS_source_normalized_Newton_branch | constant_GM_zero_or_residual_runner | P8_range_dependence | alpha(lambda) | D_lambda;finite_range | delta_G_or_fifth_force_yukawa | MISSING_EXECUTABLE_ALPHA_LAMBDA_CURVE_OR_ZERO_THEOREM | range-dependent | verified alpha(lambda) bound curve or derived zero | source-intake\mts_residuals\P8_source_normalization_residual_vector_TEMPLATE.csv | finite-range source hair maps to alpha(lambda) | source-intake\mts_residuals\P8_CONSTANT_GM_DERIVATIVE_HAIR_GATE.csv | retained_unfilled | not_scoreable_curve_missing | false | this remains curve-required; symbolic R10 text cannot score |
| MTS_source_normalized_Newton_branch | constant_GM_zero_or_residual_runner | P8_frame_calibration_split | delta_frame_source | Delta_frame;D_domain | eta_WEP_direct_geometry;clock_redshift;operator_ledger | MISSING_NUMERIC_OR_DERIVED_ZERO_FRAME_SPLIT | dimensionless | one observed frame or explicit residual below row locks | source-intake\mts_residuals\P8_source_normalization_residual_vector_TEMPLATE.csv | Delta_frame ln mu_obs = 0 | source-intake\mts_residuals\P8_CONSTANT_GM_DERIVATIVE_HAIR_GATE.csv | retained_unfilled | not_scoreable_prediction_missing | false | same-frame theorem must apply to source variation and matter readout |
| MTS_source_normalized_Newton_branch | constant_GM_zero_or_residual_runner | P8_nonlinear_beta_source_residue | delta_beta_source | second_order | beta_minus_1 | MISSING_SECOND_ORDER_PPN_SOURCE_VECTOR | dimensionless | 7.8e-05 or derived second-order source closure | source-intake\mts_residuals\P8_source_normalization_residual_vector_TEMPLATE.csv | PPN beta after measured-GM normalization | source-intake\mts_residuals\P8_CONSTANT_GM_DERIVATIVE_HAIR_GATE.csv | deferred_retained_unfilled | deferred_until_first_order_rows_score | false | first-order Newton cannot be promoted to local GR without this |

## 6. Bound Matrix

The bound matrix has been written to `source-intake\mts_residuals\P8_CONSTANT_GM_RESIDUAL_BOUND_MATRIX.csv`.

| component_id | observable | target_type | target_value | units | source | evaluation_rule | scoreable_now | reason_not_scoreable |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P8_boundary_bulk_domain_mu_extra | epsilon_mu_vector | zero_or_component_locks | zero owned exchange or row-by-row coefficient bounds | dimensionless | source-intake\mts_residuals\P8_source_normalization_residual_vector_TEMPLATE.csv | score only if epsilon_mu coefficient vector has numeric values or theorem-zero source | false | epsilon_mu vector missing |
| P8_Geff_time_drift | Gdot_over_G | upper_bound_or_zero | 9.6e-15 | yr^-1 | source-intake\mts_residuals\P8_source_normalization_residual_vector_TEMPLATE.csv | abs(predicted dln_Geff_dt) <= 9.6e-15 yr^-1 or derived_zero | false | predicted dln_Geff_dt missing |
| P8_Meff_conservation | dln_Meff_dt | derived_conservation_or_decomposed_bound | Gdot/beta locks after decomposition | yr^-1 | source-intake\mts_residuals\P8_source_normalization_residual_vector_TEMPLATE.csv | score only after separating mass flux from G_eff and epsilon_mu drift | false | mass flux residual missing |
| P8_species_source_charge | eta_source_AB | upper_bound_or_zero | 2.8e-15 | dimensionless | source-intake\mts_residuals\P8_source_normalization_residual_vector_TEMPLATE.csv | abs(predicted eta_source_AB) <= 2.8e-15 or derived universal source charge | false | source-charge prediction missing |
| P8_radial_source_hair | partial_r_ln_mu_obs | zero_or_mapped_bound | zero radial hair or mapped PPN/fifth-force residuals | inverse_length_or_dimensionless_envelope | source-intake\mts_residuals\P8_source_normalization_residual_vector_TEMPLATE.csv | score only with radial profile/theorem or explicit mapping to PPN/R10 | false | radial profile missing |
| P8_range_dependence | alpha(lambda) | curve_bound_or_zero | verified alpha(lambda) bound curve | range-dependent | source-intake\mts_residuals\P8_source_normalization_residual_vector_TEMPLATE.csv | score only against executable alpha(lambda) curve with lambda and alpha_predicted columns | false | alpha(lambda) curve missing |
| P8_frame_calibration_split | delta_frame_source | zero_or_row_locks | one observed frame or residual below WEP/clock locks | dimensionless | source-intake\mts_residuals\P8_source_normalization_residual_vector_TEMPLATE.csv | score only with parent frame theorem or numeric split residual | false | frame/source split residual missing |
| P8_nonlinear_beta_source_residue | delta_beta_source | upper_bound_or_zero | 7.8e-05 | dimensionless | source-intake\mts_residuals\P8_source_normalization_residual_vector_TEMPLATE.csv | abs(predicted delta_beta_source) <= 7.8e-05 or second-order theorem-zero | false | deferred until first-order rows score |

## 7. Decision

| decision_item | status | evidence | next_action |
| --- | --- | --- | --- |
| source_paths | pass | missing source paths = 0 | continue only with existing source paths |
| derivative_gate_loaded | pass | derivative rows loaded = 8 | use CGM rows as local runner backbone |
| P8_template_loaded | pass | P8 source-normalization template rows loaded = 8 | copy bound targets into runner input |
| zero_theorem_currently_closes | fail | non-identity theorem premises still open/failed/deferred = 8 | do not promote constant GM; use residual runner |
| runner_predictions_scoreable | fail | runner rows with missing predictions = 8 | fill theorem-zero or numeric prediction source for each row |
| constant_GM_promoted | fail | Z1-Z7 do not all pass and runner rows are not numerically scoreable | 467-mu-extra-zero-owner-or-source-normalization-coefficient-vector.md |
| local_GR_promoted | fail | constant GM not promoted and second-order beta/gamma row deferred | wait for first-order rows plus PPN vector |

## 8. Result

The zero theorem does not close yet. It fails for the right reason: not because the algebra is broken, but because the parent theory has not yet supplied the silence of `G_eff`, `M_eff`, and `epsilon_mu`.

The useful progress is that the failure is now executable. The runner loaded `8` derivative rows and `8` P8 bound-template rows, then produced `8` local residual input rows. `8` rows still have missing MTS predictions or theorem-zero sources, so nothing is claimable yet.

Practical read: we have stopped letting `GM` be a magic pocket. If it is constant, the parent action has to prove it. If it is not proven, every bit of derivative hair has a row, a target, and a place to get punched by data.

## 9. Next Queue

| Priority | Target | Reason |
| --- | --- | --- |
| 1 | `467-mu-extra-zero-owner-or-source-normalization-coefficient-vector.md` | highest blocker is `epsilon_mu = mu_extra/(G_eff M_eff)` because it controls hidden measured-GM contribution |
| 2 | `R10_alpha_lambda_curve_MTS_source_normalization.csv` | range dependence cannot be scored without an executable curve or theorem-zero |
| 3 | `P8_time_drift_residual_or_zero.csv` | local Gdot row is one of the cleanest early quantitative locks |
