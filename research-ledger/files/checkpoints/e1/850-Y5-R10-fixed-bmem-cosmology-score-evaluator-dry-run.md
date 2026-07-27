# 850 - Y5 R10 Fixed Bmem Cosmology Score Evaluator Dry Run

Current result: **fixed-`b_mem` SN/BAO sample scoring now runs**. This evaluates candidate amplitudes without fitting `b_mem`, without running an optimizer, and without allowing support language. It is a sanity readout only because the baselines and non-`b_mem` candidate parameters are still sample values rather than fair fitted competitors.

## Non-Claim Summary

| status | claim_ceiling | what_changed | evaluator_status | what_is_not_claimed | next_target | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| Y5_R10_850_fixed_bmem_SN_BAO_sample_scores_written_nonclaim | sample_score_only_no_fit_no_support_no_parent_prediction | added and ran a sample-only fixed-bmem SN/BAO evaluator | fixed_bmem_SN_BAO_sample_scores_written_nonclaim | fitted evidence, support, parent prediction, model-selection win/loss, local-GR progress | 851-Y5-R10-fixed-bmem-SN-BAO-readout-and-eta-law-choice.md | false |

## Evaluator Run Result

| run_id | run_dir | status | dry_run_only | sample_score | no_fit | fit_executed | optimizer_executed | claim_allowed | row_count | pass_count | blocked_count | failure_count | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 20260613-012532-fixed-bmem-SN-BAO-sample-evaluator | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\runs\20260613-012532-fixed-bmem-SN-BAO-sample-evaluator | fixed_bmem_SN_BAO_sample_scores_written_nonclaim | true | true | true | false | false | false | 20 | 18 | 2 | 0 | false |

## Baseline Reference

| branch | baseline_count | best_sample_baseline_by_BIC | best_sample_baseline_BIC | baseline_status | warning | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| no_sh0es | 3 | M0_sample_fixed | 1500.36505244 | sample_only_not_fitted | baseline sample parameters are not optimized; deltas are sanity readout only | false |
| sh0es | 3 | M0_sample_fixed | 1805.38803048 | sample_only_not_fitted | baseline sample parameters are not optimized; deltas are sanity readout only | false |

## Sample Score View

| branch | row_type | config_id | candidate_id | chi2_total | delta_bic_vs_best_sample_baseline | evaluation_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| sh0es | baseline_sample | M0_sample_fixed |  | 1805.38803048 | 0 | pass | false |
| sh0es | baseline_sample | M2_wCDM_sample_fixed |  | 1845.8520011 | 40.46397062 | pass | false |
| sh0es | baseline_sample | M2_CPL_sample_fixed |  | 1823.34964321 | 17.96161273 | pass | false |
| sh0es | candidate_fixed_bmem | M6_fixed_S0_null_bmem_0 | S0_null_bmem_0 | 1850.04226648 | 44.654236 | pass | false |
| sh0es | candidate_fixed_bmem | M6_fixed_S1_C0_CMB_reference | S1_C0_CMB_reference | 1862.77229685 | 57.38426637 | pass | false |
| sh0es | candidate_fixed_bmem | M6_fixed_S1_C0_full_joint_reference | S1_C0_full_joint_reference | 2008.81043427 | 203.42240379 | pass | false |
| sh0es | candidate_fixed_bmem | M6_fixed_S2_corridor_eta1_aFDeltaR_0p1 | S2_corridor_eta1_aFDeltaR_0p1 | 1880.89010673 | 82.94866135 | pass | false |
| sh0es | candidate_fixed_bmem | M6_fixed_S2_corridor_eta1_aFDeltaR_0p3 | S2_corridor_eta1_aFDeltaR_0p3 | 1983.94123833 | 185.99979295 | pass | false |
| sh0es | candidate_fixed_bmem | M6_fixed_S2_corridor_eta1_aFDeltaR_1p0 | S2_corridor_eta1_aFDeltaR_1p0 | 2687.51548876 | 889.57404338 | pass | false |
| sh0es | candidate_fixed_bmem | M6_fixed_S3_parent_predicted_placeholder | S3_parent_predicted_placeholder |  |  | blocked | false |
| no_sh0es | baseline_sample | M0_sample_fixed |  | 1500.36505244 | 0 | pass | false |
| no_sh0es | baseline_sample | M2_wCDM_sample_fixed |  | 1545.22233447 | 44.85728203 | pass | false |
| no_sh0es | baseline_sample | M2_CPL_sample_fixed |  | 1521.88988352 | 21.52483108 | pass | false |
| no_sh0es | candidate_fixed_bmem | M6_fixed_S0_null_bmem_0 | S0_null_bmem_0 | 1539.3554492 | 38.99039676 | pass | false |
| no_sh0es | candidate_fixed_bmem | M6_fixed_S1_C0_CMB_reference | S1_C0_CMB_reference | 1554.59936321 | 54.23431077 | pass | false |
| no_sh0es | candidate_fixed_bmem | M6_fixed_S1_C0_full_joint_reference | S1_C0_full_joint_reference | 1714.84175035 | 214.47669791 | pass | false |
| no_sh0es | candidate_fixed_bmem | M6_fixed_S2_corridor_eta1_aFDeltaR_0p1 | S2_corridor_eta1_aFDeltaR_0p1 | 1575.4601425 | 82.49571064 | pass | false |
| no_sh0es | candidate_fixed_bmem | M6_fixed_S2_corridor_eta1_aFDeltaR_0p3 | S2_corridor_eta1_aFDeltaR_0p3 | 1688.25912458 | 195.29469271 | pass | false |
| no_sh0es | candidate_fixed_bmem | M6_fixed_S2_corridor_eta1_aFDeltaR_1p0 | S2_corridor_eta1_aFDeltaR_1p0 | 2419.02127435 | 926.05684249 | pass | false |
| no_sh0es | candidate_fixed_bmem | M6_fixed_S3_parent_predicted_placeholder | S3_parent_predicted_placeholder |  |  | blocked | false |

## Claim Guard

| guard_id | claim | status | reason | valid_for_claim |
| --- | --- | --- | --- | --- |
| CG850_0_sample_only | 850 provides fitted cosmology evidence | forbidden | only sample parameters were evaluated; optimizer_executed=false | false |
| CG850_1_no_parent_prediction | fixed b_mem rows are parent predictions | forbidden | 847/849 still leave eta, a_F, DeltaR, and endpoint dynamics open | false |
| CG850_2_no_model_selection_claim | sample AIC/BIC decides MTS versus baselines | forbidden | baselines are not fitted and candidate non-MTS parameters use fixed config values | false |
| CG850_3_allowed_sanity_readout | fixed-bmem candidates can be mechanically evaluated against SN/BAO | allowed_private_nonclaim | the evaluator writes finite chi-square rows or explicit blockers without running fits | false |

## Decision

| decision_id | finding | reason | status | claim_allowed | next_target | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| D850_0 | fixed-bmem SN/BAO sample scoring now works | candidate rows can be injected into M6 and evaluated without fitting b_mem | sample_score_only_no_fit_no_support_no_parent_prediction | false | 851-Y5-R10-fixed-bmem-SN-BAO-readout-and-eta-law-choice.md | false |
| D850_1 | readout is only a sanity test | baseline and candidate nuisance/background parameters are sample values, not optimized under parity | sample_score_only_no_fit_no_support_no_parent_prediction | false | 851-Y5-R10-fixed-bmem-SN-BAO-readout-and-eta-law-choice.md | false |

## Next Target

| next_target | objective | include | exclude | valid_for_claim |
| --- | --- | --- | --- | --- |
| 851-Y5-R10-fixed-bmem-SN-BAO-readout-and-eta-law-choice.md | read the fixed-bmem SN/BAO sample score and choose between a fair fitted baseline comparator or eta/a_F/DeltaR derivation | rank sanity, failures/blockers, baseline parity decision, parent-amplitude route choice | support claim, public evidence, local-GR claim, formalization-workbench edits | false |

## Source Register

| source_id | path | exists | needle_check | role | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| 849_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\849-Y5-R10-strict-cosmology-scoring-adapter-or-parent-amplitude-tightening.md | true | pass | adapter handoff | false |
| 849_validation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_849_VALIDATION.csv | true | pass | prior checkpoint validation | false |
| 847_candidates | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_847_STRICT_COSMOLOGY_CANDIDATES.csv | true | pass | strict fixed-bmem candidate rows | false |
| 850_evaluator_script | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\scripts\strict_fixed_bmem_SN_BAO_evaluator.py | true | pass | new fixed-bmem sample evaluator | false |
| R1_cosmology_config | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\configs\cosmology_background_R1_current.json | true | pass | SN/BAO data and sample-parameter config | false |
| cosmology_likelihood_smoke_script | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\scripts\cosmology_likelihood_smoke.py | true | pass | reference likelihood functions imported read-only | false |

## Validation

| check_id | result | detail |
| --- | --- | --- |
| V850_0_sources_exist_and_needles | pass | all source paths exist and needles are present |
| V850_1_prior_849_clean | pass | P8_Y5_BRR545_849_VALIDATION.csv clean |
| V850_2_evaluator_status_clean | pass | sample evaluator wrote nonclaim score rows |
| V850_3_row_count_and_failures | pass | 20 rows expected, failure_count=0 |
| V850_4_no_fit_or_optimizer | pass | fit_executed=false and optimizer_executed=false |
| V850_5_baseline_rows_present | pass | 3 baselines x 2 branches present |
| V850_6_candidate_rows_present | pass | 7 candidates x 2 branches present |
| V850_7_parent_placeholder_blocked | pass | S3 parent-predicted placeholder blocked on both branches |
| V850_8_finite_candidate_scores | pass | all pass candidate rows have finite chi2_total |
| V850_9_baseline_reference_warning | pass | baseline reference rows explicitly warn sample-only not fitted |
| V850_10_claim_allowed_false | pass | runner and decision rows keep claim_allowed=false |
| V850_11_all_rows_nonclaim | pass | all generated rows valid_for_claim=false |
| V850_12_next_target_selected | pass | 851-Y5-R10-fixed-bmem-SN-BAO-readout-and-eta-law-choice.md |
| V850_13_formalization_workbench_untouched | pass | formalization_changed_after_cutoff=0 |
| V850_14_validation_rows_ready | pass | validation table constructed |
