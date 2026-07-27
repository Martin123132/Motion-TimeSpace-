# 855 - Y5 R10 Calibration Projection Response Estimator Dry Run

Current result: **the calibration-projection response estimator runs, but it does not prove the SH0ES/no-SH0ES amplitude split**. A pure global calibration offset is projected out by the SN nuisance-offset marginalization. Hubble-flow and low-z indicator vectors can span the required `Delta b_eff`, but only by solving for an effective vector magnitude; that magnitude is not independently sourced yet. So calibration projection remains plausible bookkeeping, not physics.

## Non-Claim Summary

| status | claim_ceiling | what_changed | selected_route | what_is_not_claimed | next_target | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| Y5_R10_855_calibration_projection_estimator_run_nonclaim | projection_estimator_only_no_calibration_proof_no_parent_prediction | ran a finite-difference calibration projection response estimator | independent_calibration_source_or_projection_repair | calibration proof, parent amplitude, support, public evidence, local-GR progress | 856-Y5-R10-memory-projection-repair-or-independent-calibration-source-test.md | false |

## Linear Response Estimator

| branch | vector_name | raw_vector_sum | projected_vector_norm | delta_b_per_unit_vector_mag | response_required_to_match_branch_target | required_vector_mag_to_match_target | estimator_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| no_sh0es | calibrator_indicator | 0 | 0 | 0 | 0 |  | zero_or_singular_projection | false |
| no_sh0es | used_in_sh0es_hf_indicator | 277 | 105.528364169 | -1.31171582531 | 0 | -0 | finite_response | false |
| no_sh0es | low_z_lt_0p15_indicator | 749 | 105.59559558 | -2.44291626706 | 0 | -0 | finite_response | false |
| no_sh0es | ceph_minus_mu_calibrator_residual | 0 | 0 | 0 | 0 |  | zero_or_singular_projection | false |
| sh0es | calibrator_indicator | 77 | 33.7779432711 | -0.179775044804 | 0.0967220815343 | -0.5380172851 | finite_response | false |
| sh0es | used_in_sh0es_hf_indicator | 277 | 106.085348569 | -1.19539952447 | 0.0967220815343 | -0.0809119290703 | finite_response | false |
| sh0es | low_z_lt_0p15_indicator | 826 | 107.376998584 | -2.38983195478 | 0.0967220815343 | -0.0404723358649 | finite_response | false |
| sh0es | ceph_minus_mu_calibrator_residual | 1.4223 | 7.8291891718 | -0.00339002026028 | 0.0967220815343 | -28.5314169557 | finite_response | false |

## Observed Calibration Vector Check

| branch | observed_vector | raw_mean | projected_vector_norm | predicted_delta_b_from_observed_vector | target_delta_b | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| sh0es | observed_MU_SH0ES_minus_m_b_corr | 19.2530000176 | 0.000612967787943 | -3.98444296126e-07 | 0.0967220815343 | insufficient_to_explain_target | false |
| sh0es | observed_CEPH_minus_MU_calibrator_only | 0.000836155202822 | 7.8291891718 | -0.00339002026028 | 0.0967220815343 | insufficient_to_explain_target | false |

## Interpretation Gates

| gate_id | gate | status | reason | next_action | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| IG855_0_global_offset_projected_out | global calibration offset explains branch split | fails | observed MU_SH0ES-minus-m_b_corr predicts delta_b=-3.98444296126e-07 after offset projection | do not use global calibration shift as response proof | false |
| IG855_1_indicator_vectors_can_span_target | HF/low-z branch geometry can span required split | passes_as_fit_space_not_physics | HF required mag=-0.0809119290703; low-z required mag=-0.0404723358649 | source or derive an independent calibration/local-response amplitude | false |
| IG855_2_projection_not_proven | projection law proves SH0ES excess | fails_open | current estimator solves for required vector amplitude rather than deriving it | either source independent delta_cal or repair memory projection | false |

## Route Choice

| route_id | route | status | reason | include | exclude | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| RC855_0_selected | independent_calibration_source_or_projection_repair | selected | linear projection can span the branch split, but observed simple calibration residuals do not independently produce it | source/derive local-response amplitude; if unavailable, demote response law and repair memory projection | claiming calibration proof from required fitted vector amplitude | false |
| RC855_1_deferred | full robustness scoring | deferred | would be premature until branch response amplitude is sourced or projection is repaired | later multi-arena scoring | long run now | false |

## Claim Guard

| guard_id | claim | status | reason | valid_for_claim |
| --- | --- | --- | --- | --- |
| CG855_0_no_calibration_proof | calibration projection explains branch split | forbidden | the estimator needs an independently sourced vector amplitude | false |
| CG855_1_no_parent_prediction | parent b_mem is derived | forbidden | eta/a_F/DeltaR remain open | false |
| CG855_2_no_support | positive memory is now support-grade | forbidden | projection and parent gates remain open | false |
| CG855_3_allowed_estimator | linear response estimator has been run as a private diagnostic | allowed_private_nonclaim | finite-difference J_b and branch vectors are recorded without fitting b_mem | false |

## Decision

| decision_id | finding | reason | status | claim_allowed | next_target | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| D855_0 | global calibration offset is not the explanation | SN nuisance offset projection removes the global MU_SH0ES-minus-m_b_corr mode | projection_estimator_only_no_calibration_proof_no_parent_prediction | false | 856-Y5-R10-memory-projection-repair-or-independent-calibration-source-test.md | false |
| D855_1 | branch indicator response can span the split but is not sourced | HF/low-z vectors require finite effective mag shifts, but those shifts were solved from target rather than derived | projection_estimator_only_no_calibration_proof_no_parent_prediction | false | 856-Y5-R10-memory-projection-repair-or-independent-calibration-source-test.md | false |

## Next Target

| next_target | objective | include | exclude | valid_for_claim |
| --- | --- | --- | --- | --- |
| 856-Y5-R10-memory-projection-repair-or-independent-calibration-source-test.md | decide whether an independent calibration/local-response amplitude exists; otherwise repair the memory projection before more scoring | source delta_cal, low-z/HF response bounds, projection repair contract, no fitted-amplitude proof | support claim, b_mem fit, public evidence, formalization-workbench edits | false |

## Source Register

| source_id | path | exists | needle_check | role | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| 854_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\854-Y5-R10-parent-amplitude-branch-split-law-or-projection-repair.md | true | pass | branch-split law handoff | false |
| 854_validation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_854_VALIDATION.csv | true | pass | prior checkpoint validation | false |
| 852_scores | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_852_FAIR_FIXED_BMEM_SN_BAO_FIT_SCORES.csv | true | pass | fair fixed-bmem fit parameters | false |
| 853_branch_readout | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_853_BRANCH_READOUT.csv | true | pass | b_eff target rows | false |
| 854_law_attempt | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_854_BRANCH_SPLIT_LAW_ATTEMPT.csv | true | pass | projection estimator contract | false |
| pantheon_plus_data | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\data\cosmology\pantheon_plus\Pantheon+SH0ES.dat | true | pass | SN branch/calibration vector source | false |

## Validation

| check_id | result | detail |
| --- | --- | --- |
| V855_0_sources_exist_and_needles | pass | all source paths exist and needles are present |
| V855_1_prior_854_clean | pass | P8_Y5_BRR545_854_VALIDATION.csv clean |
| V855_2_estimator_rows_present | pass | branch/vector estimator rows present |
| V855_3_observed_vector_check_present | pass | observed simple calibration vector does not explain target |
| V855_4_indicator_span_finite | pass | SH0ES HF indicator has finite response coefficient |
| V855_5_interpretation_gates_present | pass | global-offset failure and projection-not-proven gates present |
| V855_6_route_selected | pass | independent calibration source or projection repair selected |
| V855_7_claim_allowed_false | pass | decision rows keep claim_allowed=false |
| V855_8_all_rows_nonclaim | pass | all generated rows valid_for_claim=false |
| V855_9_next_target_selected | pass | 856-Y5-R10-memory-projection-repair-or-independent-calibration-source-test.md |
| V855_10_formalization_workbench_untouched | pass | formalization_changed_after_cutoff=0 |
| V855_11_validation_rows_ready | pass | validation table constructed |
