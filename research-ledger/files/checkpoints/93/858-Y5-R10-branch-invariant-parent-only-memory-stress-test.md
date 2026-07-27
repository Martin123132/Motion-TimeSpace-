# 858 - Y5 R10 Branch-Invariant Parent-Only Memory Stress Test

Current result: **the parent-only memory route has been stress-tested with one shared `b_P` and response forced to zero**. This is stricter than the earlier branch readout: non-derived parent amplitudes pay a selection penalty, no branch-specific `b_mem` is fitted, and SN/BAO sector deltas are reported separately.

## Non-Claim Summary

| status | claim_ceiling | what_changed | best_parent_candidate | best_combined_delta_bic | best_status | what_is_not_claimed | next_target | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Y5_R10_858_branch_invariant_parent_only_stress_test_complete_nonclaim | parent_only_stress_test_no_support_no_parent_derivation_no_response_source | scored strict parent-only shared b_P candidates with response forced to zero | P858_2_midpoint_parent | 1.42131264 | borderline_parent_only_private_nonclaim | support, parent derivation, response physics, local-GR pass, public evidence | 859-Y5-R10-parent-memory-shape-amplitude-repair-or-derivation.md | false |

## Run Result

| run_id | run_dir | status | short_fit | fit_executed | b_mem_fit_executed | claim_allowed | row_count | pass_count | blocked_count | failure_count | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 20260613-022053-fair-fixed-bmem-SN-BAO-fitted-comparator | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\runs\20260613-022053-fair-fixed-bmem-SN-BAO-fitted-comparator | fair_fixed_bmem_SN_BAO_short_fit_written_nonclaim | true | true | false | false | 22 | 20 | 2 | 0 | false |

## Parent-Only Candidate Grid

| candidate_id | branch_class | b_mem_numeric | eta_assumption | a_F_DeltaR_assumption | family_selection_penalty | claim_label | execution_eligible_for_scoring | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P858_0_null_parent | parent_only_null_control | 0.0 | not_applicable | not_applicable | 0 | benchmark_only | true | false |
| P858_1_no_sh0es_anchor_parent | parent_only_target_anchor_stress | 0.0157305087947 | eta_unsolved | 0.0471915263841 | 1 | exploratory_parent_only_nonclaim | true | false |
| P858_2_midpoint_parent | parent_only_split_midpoint_stress | 0.0640915495618 | eta_unsolved | 0.192274648686 | 1 | exploratory_parent_only_nonclaim | true | false |
| P858_3_sh0es_anchor_parent | parent_only_target_anchor_stress | 0.112452590329 | eta_unsolved | 0.337357770987 | 1 | exploratory_parent_only_nonclaim | true | false |
| P858_4_corridor_eta1_aFDeltaR_0p1 | parent_only_corridor_stress | 0.0333333333333 | eta=1 | 0.1 | 1 | exploratory_parent_only_nonclaim | true | false |
| P858_5_corridor_eta1_aFDeltaR_0p3 | parent_only_corridor_stress | 0.1 | eta=1 | 0.3 | 1 | exploratory_parent_only_nonclaim | true | false |
| P858_6_corridor_eta1_aFDeltaR_1p0 | parent_only_corridor_stress | 0.333333333333 | eta=1 | 1 | 1 | exploratory_parent_only_nonclaim | true | false |
| P858_7_parent_predicted_placeholder | parent_only_parent_predicted |  | MISSING_PARENT_ETA | MISSING_PARENT_AF_DELTAR | 0 | support_grade_candidate_blocked | false | false |

## Branch Readout

| branch | best_bic_baseline | best_parent_candidate | b_parent | b_response | delta_chi2_vs_best_baseline | delta_aic_vs_best_baseline | delta_bic_vs_best_baseline | edge_flags | readout | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| no_sh0es | M0_fit_fair | P858_2_midpoint_parent | 0.0640915495618 | 0 | 1.23456899 | 0.81707413 | 2.86354123 |  | branch_diagnostic_only_parent_value_shared_candidate_pool | false |
| sh0es | M2_wCDM_fit_fair | P858_5_corridor_eta1_aFDeltaR_0p3 | 0.1 | 0 | 0.67769706 | -1.32230294 | -3.17117663 |  | branch_diagnostic_only_parent_value_shared_candidate_pool | false |

## Joint Parent Ledger

| candidate_id | b_parent | b_response_no_sh0es | b_response_sh0es | combined_delta_chi2 | combined_delta_aic | combined_delta_bic | combined_delta_chi2_sn_vs_bic_baseline | combined_delta_chi2_bao_vs_bic_baseline | max_branch_delta_bic | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P858_0_null_parent | 0.0 | 0 | 0 | 23.7064685 | 17.28897364 | 6.63936138 | 11.27348458 | 2.81246189548 | 6.63936138 | null_control | false |
| P858_1_no_sh0es_anchor_parent | 0.0157305087947 | 0 | 0 | 15.8163582 | 13.39886334 | 13.59645676 | 5.02105651 | 1.17477966048 | 8.72966237 | disfavored_parent_only_private_nonclaim | false |
| P858_2_midpoint_parent | 0.0640915495618 | 0 | 0 | 3.64121408 | 1.22371922 | 1.42131264 | -3.90434377 | -2.0749641753 | 2.86354123 | borderline_parent_only_private_nonclaim | false |
| P858_3_sh0es_anchor_parent | 0.112452590329 | 0 | 0 | 8.58794339 | 6.17044853 | 6.36804195 | 1.10958026 | -2.14215889061 | 9.041663 | disfavored_parent_only_private_nonclaim | false |
| P858_4_corridor_eta1_aFDeltaR_0p1 | 0.0333333333333 | 0 | 0 | 9.31256382 | 6.89506896 | 7.09266237 | 0.02927877 | -0.33723697887 | 3.94675725 | disfavored_parent_only_private_nonclaim | false |
| P858_5_corridor_eta1_aFDeltaR_0p3 | 0.1 | 0 | 0 | 5.75644825 | 3.33895339 | 3.5365468 | -1.40170768 | -2.46236609996 | 6.70772343 | weakly_disfavored_but_competitive_private_nonclaim | false |
| P858_6_corridor_eta1_aFDeltaR_1p0 | 0.333333333333 | 0 | 0 | 210.80342144 | 208.38592658 | 208.58352 | 149.71041342 | 51.4724859996 | 122.71385707 | disfavored_parent_only_private_nonclaim | false |
| P858_7_parent_predicted_placeholder |  | 0 | 0 |  |  |  |  |  |  | blocked_parent_prediction_missing | false |

## SN BAO Sector Ledger

| branch | candidate_id | b_parent | sector_baseline | delta_chi2_sn_vs_bic_baseline | delta_chi2_bao_vs_bic_baseline | delta_chi2_total_vs_bic_baseline | delta_bic_vs_best_fit_baseline | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| sh0es | P858_0_null_parent | 0.0 | M2_wCDM_fit_fair | 11.27348458 | 2.81246189548 | 14.08594647 | 6.63936138 | false |
| sh0es | P858_1_no_sh0es_anchor_parent | 0.0157305087947 | M2_wCDM_fit_fair | 6.87519411 | 1.85446825088 | 8.72966236 | 8.72966237 | false |
| sh0es | P858_2_midpoint_parent | 0.0640915495618 | M2_wCDM_fit_fair | -1.15072928 | -0.29149931634 | -1.4422286 | -1.44222859 | false |
| sh0es | P858_3_sh0es_anchor_parent | 0.112452590329 | M2_wCDM_fit_fair | -1.7081898 | -0.96543125998 | -2.67362106 | -2.67362105 | false |
| sh0es | P858_4_corridor_eta1_aFDeltaR_0p1 | 0.0333333333333 | M2_wCDM_fit_fair | 3.02227476 | 0.92448248908 | 3.94675725 | 3.94675725 | false |
| sh0es | P858_5_corridor_eta1_aFDeltaR_0p3 | 0.1 | M2_wCDM_fit_fair | -2.22011143 | -0.9510651992 | -3.17117663 | -3.17117663 | false |
| sh0es | P858_6_corridor_eta1_aFDeltaR_1p0 | 0.333333333333 | M2_wCDM_fit_fair | 63.44355196 | 22.4261109687 | 85.86966292 | 85.86966293 | false |
| no_sh0es | P858_0_null_parent | 0.0 | M0_fit_fair | 0 | 0 | 0 | 0 | false |
| no_sh0es | P858_1_no_sh0es_anchor_parent | 0.0157305087947 | M0_fit_fair | -1.8541376 | -0.6796885904 | -2.53382619 | 4.86679439 | false |
| no_sh0es | P858_2_midpoint_parent | 0.0640915495618 | M0_fit_fair | -2.75361449 | -1.78346485896 | -4.53707935 | 2.86354123 | false |
| no_sh0es | P858_3_sh0es_anchor_parent | 0.112452590329 | M0_fit_fair | 2.81777006 | -1.17672763063 | 1.64104242 | 9.041663 | false |
| no_sh0es | P858_4_corridor_eta1_aFDeltaR_0p1 | 0.0333333333333 | M0_fit_fair | -2.99299599 | -1.26171946795 | -4.25471546 | 3.14590512 | false |
| no_sh0es | P858_5_corridor_eta1_aFDeltaR_0p3 | 0.1 | M0_fit_fair | 0.81840375 | -1.51130090076 | -0.69289715 | 6.70772343 | false |
| no_sh0es | P858_6_corridor_eta1_aFDeltaR_1p0 | 0.333333333333 | M0_fit_fair | 86.26686146 | 29.0463750309 | 115.31323649 | 122.71385707 | false |

## Null Control Parity

| branch | M0_chi2 | null_parent_chi2 | null_minus_M0_chi2 | parity_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| no_sh0es | 1470.05609148 | 1470.05609148 | 0 | numerically_close | false |
| sh0es | 1773.69099938 | 1773.69099939 | 9.99989424599e-09 | numerically_close | false |

## Acceptance Readout

| test_id | result | detail | valid_for_claim |
| --- | --- | --- | --- |
| AT858_0_shared_parent | pass | each candidate uses one b_P value across no_SH0ES and SH0ES | false |
| AT858_1_response_zero | pass | all candidate rows set b_response_no_sh0es=b_response_sh0es=0 in joint ledger | false |
| AT858_2_null_parity | pass | b_P=0 M6 tracks M0 within tolerance | false |
| AT858_3_SN_BAO_split | pass | sector deltas are reported separately from total BIC | false |
| AT858_4_parent_survival | pass | best_nonnull=P858_2_midpoint_parent status=borderline_parent_only_private_nonclaim combined_delta_bic=1.42131264 | false |

## Claim Guard

| guard_id | claim | status | reason | valid_for_claim |
| --- | --- | --- | --- | --- |
| CG858_0_no_support | parent-only cosmology is support-grade | forbidden | parent amplitude is not derived and this is a short private stress test | false |
| CG858_1_no_response | response channel explains the branch split | forbidden | response is deliberately forced to zero in every scored candidate | false |
| CG858_2_no_branch_knob | separate branch b_mem values are used | forbidden | all scored non-null candidates use one shared b_P across both branches | false |
| CG858_3_allowed_private_stress_readout | strict parent-only stress-test readout is available | allowed_private_nonclaim | shared parent values were scored with response zero and sector ledgers recorded | false |

## Decision

| decision_id | finding | reason | status | claim_allowed | next_target | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| D858_0 | borderline_parent_only_private_nonclaim | best shared parent candidate is P858_2_midpoint_parent with combined_delta_bic=1.42131264 and max_branch_delta_bic=2.86354123 | parent_only_stress_test_no_support_no_parent_derivation_no_response_source | false | 859-Y5-R10-parent-memory-shape-amplitude-repair-or-derivation.md | false |
| D858_1 | parent-only route remains private and derivation-gated | even if competitive, the amplitude must be derived rather than selected from the stress grid | parent_only_stress_test_no_support_no_parent_derivation_no_response_source | false | 859-Y5-R10-parent-memory-shape-amplitude-repair-or-derivation.md | false |

## Next Target

| next_target | objective | include | exclude | valid_for_claim |
| --- | --- | --- | --- | --- |
| 859-Y5-R10-parent-memory-shape-amplitude-repair-or-derivation.md | derive or repair the parent memory shape/amplitude because the strict shared-parent test is competitive but not evidence-grade | eta/a_F/DeltaR derivation attempt, parent shape audit, no fitted target inversion, response source remains closed unless independently signed | support claim, local-GR claim, public evidence, formalization-workbench edits | false |

## Source Register

| source_id | path | exists | needle_check | role | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| 857_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\857-Y5-R10-branch-invariant-memory-projection-repair-contract.md | true | pass | parent-only repair contract handoff | false |
| 857_validation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_857_VALIDATION.csv | true | pass | prior checkpoint validation | false |
| 857_acceptance_tests | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_857_ACCEPTANCE_TESTS.csv | true | pass | acceptance gates for this stress test | false |
| 857_response_gate | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_857_RESPONSE_SOURCE_GATE.csv | true | pass | response forced to zero | false |
| 852_comparator | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\scripts\strict_fixed_bmem_SN_BAO_fitted_comparator.py | true | pass | fair fitted scoring engine | false |
| R1_cosmology_config | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\configs\cosmology_background_R1_current.json | true | pass | SN/BAO config | false |
| 858_parent_only_candidates | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_858_PARENT_ONLY_CANDIDATES.csv | true | pass | strict parent-only candidate input | false |

## Validation

| check_id | result | detail |
| --- | --- | --- |
| V858_0_sources_exist_and_needles | pass | all source paths exist and needles are present |
| V858_1_prior_857_clean | pass | P8_Y5_BRR545_857_VALIDATION.csv clean |
| V858_2_parent_only_candidates_ready | pass | 8 parent-only candidates including null and blocked parent-predicted placeholder |
| V858_3_run_status_clean | pass | fair fixed-bmem comparator completed |
| V858_4_row_count_and_failures | pass | 22 rows expected, failure_count=0 |
| V858_5_no_bmem_fit | pass | no passing fit_param_names include b_mem |
| V858_6_shared_parent_candidates | pass | each scored candidate has one b_P across both branches |
| V858_7_parent_placeholder_blocked | pass | support-grade parent-predicted placeholder blocked on both branches |
| V858_8_branch_readouts_present | pass | two branch diagnostic readouts generated |
| V858_9_joint_ledger_present | pass | joint shared-parent ledger generated |
| V858_10_sector_ledger_present | pass | SN and BAO sector deltas generated for scored candidates |
| V858_11_null_control_parity | pass | b_P=0 M6 tracks M0 after fair refit |
| V858_12_acceptance_passes | pass | all strict 858 acceptance tests pass |
| V858_13_claim_allowed_false | pass | runner and decision rows keep claim_allowed=false |
| V858_14_all_rows_nonclaim | pass | all generated rows valid_for_claim=false |
| V858_15_next_target_selected | pass | 859-Y5-R10-parent-memory-shape-amplitude-repair-or-derivation.md |
| V858_16_formalization_workbench_untouched | pass | formalization_changed_after_cutoff=0 |
| V858_17_validation_rows_ready | pass | validation table constructed |
