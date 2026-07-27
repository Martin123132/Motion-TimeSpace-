# 852 - Y5 R10 Fair Fixed Bmem SN BAO Fitted Comparator Dry Run

Current result: **a short fair SN/BAO fitted comparator has run with `b_mem` fixed**. Baselines and fixed-`b_mem` M6 candidates were refit over shared background/nuisance parameters, while `b_mem` itself was not fitted. This is still private nonclaim evidence: it can diagnose projection pressure, but it cannot prove support or death without parent-amplitude and robustness gates.

## Non-Claim Summary

| status | claim_ceiling | what_changed | comparator_status | what_is_not_claimed | next_target | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| Y5_R10_852_fair_fixed_bmem_SN_BAO_short_fit_complete_nonclaim | short_fitted_comparator_only_no_support_no_parent_prediction | ran a short fair SN/BAO fitted comparator with b_mem fixed | fair_fixed_bmem_SN_BAO_short_fit_written_nonclaim | support, death, parent prediction, public evidence, local-GR progress | 853-Y5-R10-fixed-bmem-fitted-readout-or-projection-repair.md | false |

## Run Result

| run_id | run_dir | status | short_fit | fit_executed | b_mem_fit_executed | claim_allowed | integration_steps | maxiter | starts | row_count | pass_count | blocked_count | failure_count | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 20260613-013628-fair-fixed-bmem-SN-BAO-fitted-comparator | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\runs\20260613-013628-fair-fixed-bmem-SN-BAO-fitted-comparator | fair_fixed_bmem_SN_BAO_short_fit_written_nonclaim | true | true | false | false | 1024 | 80 | 2 | 20 | 18 | 2 | 0 | false |

## Branch Readout

| branch | best_fit_baseline | best_candidate | best_candidate_delta_BIC | best_positive_candidate | best_positive_delta_BIC | edge_flagged_row_count | readout | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| no_sh0es | M0_fit_fair | S1_C0_CMB_reference | -2.53382619 | S1_C0_CMB_reference | -2.53382619 | 0 | fair_comparator_completed_nonclaim | false |
| sh0es | M2_wCDM_fit_fair | S1_C0_full_joint_reference | -10.12020615 | S1_C0_full_joint_reference | -10.12020615 | 0 | fair_comparator_completed_nonclaim | false |

## Null Control Parity

| branch | M0_chi2 | null_M6_chi2 | null_minus_M0_chi2 | parity_status | interpretation | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| no_sh0es | 1470.05609148 | 1470.05609148 | 0 | numerically_close | b_mem=0 M6 should reduce to M0 when shared parameters are fitted | false |
| sh0es | 1773.69099938 | 1773.69099939 | 9.99989424599e-09 | numerically_close | b_mem=0 M6 should reduce to M0 when shared parameters are fitted | false |

## Score View

| branch | row_type | config_id | candidate_id | chi2_total | delta_bic_vs_best_fit_baseline | edge_flags | evaluation_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| sh0es | baseline_fit | M0_fit_fair |  | 1773.69099938 | 6.63936137 |  | pass | false |
| sh0es | baseline_fit | M2_wCDM_fit_fair |  | 1759.60505292 | 0 |  | pass | false |
| sh0es | baseline_fit | M2_CPL_fit_fair |  | 1755.75617923 | 3.59771142 |  | pass | false |
| sh0es | candidate_fixed_bmem_fit | M6_fixed_S0_null_bmem_0_fit_fair | S0_null_bmem_0 | 1773.69099939 | 6.63936138 |  | pass | false |
| sh0es | candidate_fixed_bmem_fit | M6_fixed_S1_C0_CMB_reference_fit_fair | S1_C0_CMB_reference | 1768.33471528 | 1.28307727 |  | pass | false |
| sh0es | candidate_fixed_bmem_fit | M6_fixed_S1_C0_full_joint_reference_fit_fair | S1_C0_full_joint_reference | 1756.93143186 | -10.12020615 |  | pass | false |
| sh0es | candidate_fixed_bmem_fit | M6_fixed_S2_corridor_eta1_aFDeltaR_0p1_fit_fair | S2_corridor_eta1_aFDeltaR_0p1 | 1763.55181017 | 3.94675725 |  | pass | false |
| sh0es | candidate_fixed_bmem_fit | M6_fixed_S2_corridor_eta1_aFDeltaR_0p3_fit_fair | S2_corridor_eta1_aFDeltaR_0p3 | 1756.43387629 | -3.17117663 |  | pass | false |
| sh0es | candidate_fixed_bmem_fit | M6_fixed_S2_corridor_eta1_aFDeltaR_1p0_fit_fair | S2_corridor_eta1_aFDeltaR_1p0 | 1845.47471584 | 85.86966293 |  | pass | false |
| sh0es | candidate_fixed_bmem_fit | M6_fixed_S3_parent_predicted_placeholder_fit_fair | S3_parent_predicted_placeholder |  |  |  | blocked | false |
| no_sh0es | baseline_fit | M0_fit_fair |  | 1470.05609148 | 0 |  | pass | false |
| no_sh0es | baseline_fit | M2_wCDM_fit_fair |  | 1464.701938 | 2.0464671 |  | pass | false |
| no_sh0es | baseline_fit | M2_CPL_fit_fair |  | 1464.28444314 | 9.02959282 |  | pass | false |
| no_sh0es | candidate_fixed_bmem_fit | M6_fixed_S0_null_bmem_0_fit_fair | S0_null_bmem_0 | 1470.05609148 | 0 |  | pass | false |
| no_sh0es | candidate_fixed_bmem_fit | M6_fixed_S1_C0_CMB_reference_fit_fair | S1_C0_CMB_reference | 1467.52226529 | -2.53382619 |  | pass | false |
| no_sh0es | candidate_fixed_bmem_fit | M6_fixed_S1_C0_full_joint_reference_fit_fair | S1_C0_full_joint_reference | 1471.6971339 | 1.64104242 |  | pass | false |
| no_sh0es | candidate_fixed_bmem_fit | M6_fixed_S2_corridor_eta1_aFDeltaR_0p1_fit_fair | S2_corridor_eta1_aFDeltaR_0p1 | 1465.80137601 | 3.14590511 |  | pass | false |
| no_sh0es | candidate_fixed_bmem_fit | M6_fixed_S2_corridor_eta1_aFDeltaR_0p3_fit_fair | S2_corridor_eta1_aFDeltaR_0p3 | 1469.36319433 | 6.70772343 |  | pass | false |
| no_sh0es | candidate_fixed_bmem_fit | M6_fixed_S2_corridor_eta1_aFDeltaR_1p0_fit_fair | S2_corridor_eta1_aFDeltaR_1p0 | 1585.36932797 | 122.71385707 |  | pass | false |
| no_sh0es | candidate_fixed_bmem_fit | M6_fixed_S3_parent_predicted_placeholder_fit_fair | S3_parent_predicted_placeholder |  |  |  | blocked | false |

## Claim Guard

| guard_id | claim | status | reason | valid_for_claim |
| --- | --- | --- | --- | --- |
| CG852_0_no_parent_prediction | fitted fixed-bmem rows are parent-predicted amplitudes | forbidden | b_mem values remain candidate/benchmark/corridor rows, not derived eta/a_F/DeltaR values | false |
| CG852_1_no_bmem_fit | b_mem was fitted by 852 | forbidden | comparator excludes b_mem from all fit_param_names | false |
| CG852_2_no_support_or_death | 852 decides support or death | forbidden | short fit is a private branch diagnostic; full robustness and parent derivation remain open | false |
| CG852_3_allowed_comparator | fair fixed-bmem SN/BAO short comparator has run | allowed_private_nonclaim | baselines and fixed-bmem candidates were fitted under the same SN/BAO data branch with b_mem fixed | false |

## Decision

| decision_id | finding | reason | status | claim_allowed | next_target | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| D852_0 | positive_fixed_bmem_remains_competitive_enough_for_parent_amplitude_work | best positive candidate delta_BIC range across branches is -10.1202 to -2.53383 | short_fitted_comparator_only_no_support_no_parent_prediction | false | 853-Y5-R10-fixed-bmem-fitted-readout-or-projection-repair.md | false |
| D852_1 | next step chosen from fair comparator | feed the preferred fixed amplitude back into eta/a_F/DeltaR derivation | short_fitted_comparator_only_no_support_no_parent_prediction | false | 853-Y5-R10-fixed-bmem-fitted-readout-or-projection-repair.md | false |

## Next Target

| next_target | objective | include | exclude | valid_for_claim |
| --- | --- | --- | --- | --- |
| 853-Y5-R10-fixed-bmem-fitted-readout-or-projection-repair.md | decide whether fitted fixed-bmem results require projection repair, sign/amplitude revision, or renewed eta/a_F/DeltaR derivation | read fitted deltas, inspect BAO residual pressure, check null-control parity, select derivation or repair route | support claim, public evidence, local-GR claim, formalization-workbench edits | false |

## Source Register

| source_id | path | exists | needle_check | role | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| 851_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\851-Y5-R10-fixed-bmem-SN-BAO-readout-and-eta-law-choice.md | true | pass | route choice handoff | false |
| 851_validation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_851_VALIDATION.csv | true | pass | prior checkpoint validation | false |
| 852_comparator_script | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\scripts\strict_fixed_bmem_SN_BAO_fitted_comparator.py | true | pass | new short fitted comparator | false |
| 847_candidates | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_847_STRICT_COSMOLOGY_CANDIDATES.csv | true | pass | strict fixed-bmem candidate rows | false |
| R1_cosmology_config | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\configs\cosmology_background_R1_current.json | true | pass | SN/BAO data and sample-parameter config | false |

## Validation

| check_id | result | detail |
| --- | --- | --- |
| V852_0_sources_exist_and_needles | pass | all source paths exist and needles are present |
| V852_1_prior_851_clean | pass | P8_Y5_BRR545_851_VALIDATION.csv clean |
| V852_2_run_status_clean | pass | short fair comparator completed without fit failures |
| V852_3_row_count_and_failures | pass | 20 rows expected, failure_count=0 |
| V852_4_no_bmem_fit | pass | no passing fit_param_names include b_mem |
| V852_5_baseline_rows_present | pass | 3 baselines x 2 branches present |
| V852_6_candidate_rows_present | pass | 7 candidates x 2 branches present |
| V852_7_parent_placeholder_blocked | pass | S3 parent-predicted placeholder blocked on both branches |
| V852_8_readouts_present | pass | branch readouts generated |
| V852_9_null_control_parity | pass | b_mem=0 M6 tracks M0 after fair refit |
| V852_10_claim_allowed_false | pass | runner and decision rows keep claim_allowed=false |
| V852_11_all_rows_nonclaim | pass | all generated rows valid_for_claim=false |
| V852_12_next_target_selected | pass | 853-Y5-R10-fixed-bmem-fitted-readout-or-projection-repair.md |
| V852_13_formalization_workbench_untouched | pass | formalization_changed_after_cutoff=0 |
| V852_14_validation_rows_ready | pass | validation table constructed |
