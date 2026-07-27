# 851 - Y5 R10 Fixed Bmem SN BAO Readout And Eta Law Choice

Current result: **the 850 fixed-`b_mem` sample test is a useful warning, not a verdict**. Positive memory rows can reduce or soften SN residuals in places, but BAO dominates the penalty under current sample parameters. Because even the `b_mem=0` M6 null control is worse than sample M0, the next step is a fair fixed-`b_mem` fitted comparator before either deriving `eta/a_F/DeltaR` or demoting the branch.

## Non-Claim Summary

| status | claim_ceiling | what_changed | selected_route | what_is_not_claimed | next_target | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| Y5_R10_851_fixed_bmem_SN_BAO_readout_selects_fair_comparator_nonclaim | readout_and_route_choice_only_no_support_no_death_no_parent_prediction | converted 850 sample scores into a sector-tension readout and route choice | fair_fixed_bmem_fitted_SN_BAO_comparator | support, death, parent prediction, local-GR progress, public evidence | 852-Y5-R10-fair-fixed-bmem-SN-BAO-fitted-comparator-dry-run.md | false |

## Branch Readout

| branch | best_sample_baseline | best_candidate | best_candidate_delta_BIC | best_positive_candidate | best_positive_delta_BIC | readout | interpretation | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| no_sh0es | M0_sample_fixed | S0_null_bmem_0 | 38.99039676 | S1_C0_CMB_reference | 54.23431077 | sample_M6_fixed_bmem_worse_than_sample_M0 | not a support or death result because nuisance/background parameters are not fitted under parity | false |
| sh0es | M0_sample_fixed | S0_null_bmem_0 | 44.654236 | S1_C0_CMB_reference | 57.38426637 | sample_M6_fixed_bmem_worse_than_sample_M0 | not a support or death result because nuisance/background parameters are not fitted under parity | false |

## Sector Tension

| branch | candidate_id | delta_chi2_SN_vs_best_sample_baseline | delta_chi2_BAO_vs_best_sample_baseline | sector_tension | readout | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| no_sh0es | S0_null_bmem_0 | 9.9365713 | 29.0538254658 | SN_and_BAO_worse | BAO_dominates_positive_memory_penalty | false |
| no_sh0es | S1_C0_CMB_reference | 6.31570014 | 47.9186106342 | SN_and_BAO_worse | BAO_dominates_positive_memory_penalty | false |
| no_sh0es | S1_C0_full_joint_reference | -2.19433706 | 216.671034961 | SN_improves_BAO_worsens | BAO_dominates_positive_memory_penalty | false |
| no_sh0es | S2_corridor_eta1_aFDeltaR_0p1 | 3.04349683 | 72.0515932309 | SN_and_BAO_worse | BAO_dominates_positive_memory_penalty | false |
| no_sh0es | S2_corridor_eta1_aFDeltaR_0p3 | -2.34358127 | 190.237653405 | SN_improves_BAO_worsens | BAO_dominates_positive_memory_penalty | false |
| no_sh0es | S2_corridor_eta1_aFDeltaR_1p0 | 50.86859607 | 867.787625838 | SN_and_BAO_worse | BAO_dominates_positive_memory_penalty | false |
| sh0es | S0_null_bmem_0 | 15.60041053 | 29.0538254658 | SN_and_BAO_worse | BAO_dominates_positive_memory_penalty | false |
| sh0es | S1_C0_CMB_reference | 9.46565573 | 47.9186106342 | SN_and_BAO_worse | BAO_dominates_positive_memory_penalty | false |
| sh0es | S1_C0_full_joint_reference | -13.24863117 | 216.671034961 | SN_improves_BAO_worsens | BAO_dominates_positive_memory_penalty | false |
| sh0es | S2_corridor_eta1_aFDeltaR_0p1 | 3.45048302 | 72.0515932309 | SN_and_BAO_worse | BAO_dominates_positive_memory_penalty | false |
| sh0es | S2_corridor_eta1_aFDeltaR_0p3 | -11.68444555 | 190.237653405 | SN_improves_BAO_worsens | BAO_dominates_positive_memory_penalty | false |
| sh0es | S2_corridor_eta1_aFDeltaR_1p0 | 14.33983244 | 867.787625838 | SN_and_BAO_worse | BAO_dominates_positive_memory_penalty | false |

## Artifact Diagnosis

| artifact_id | finding | meaning | risk | required_fix | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| AD851_0_null_control | S0 null b_mem is already worse than M0 | sample M6 background values h0=72, omega_m0=0.27 differ from M0 sample values h0=70, omega_m0=0.3 | do not interpret null-control loss as memory-sector loss | fit shared nuisance/background parameters under baseline parity with b_mem fixed | false |
| AD851_1_BAO_pressure | positive b_mem tends to improve or barely affect SN but strongly worsens BAO in the sample test | the current memory shape/amplitude may be BAO-stiff, or the non-bmem parameters need fair refit | a positive-amplitude derivation could be forced into a BAO conflict if fair refit does not repair it | run fixed-bmem fitted comparator before deriving eta as if positive b_mem were empirically safe | false |
| AD851_2_parent_eta_route | eta/a_F/DeltaR derivation remains necessary but should not be the immediate empirical route | a derived amplitude is valuable only if the fair comparator shows the branch is not structurally BAO-broken | deriving a beautiful amplitude for a bad projection wastes effort | choose fair comparator next, then feed its result back into parent-amplitude derivation | false |

## Route Choice

| route_id | route | status | reason | include | exclude | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| RC851_0_selected | fair_fixed_bmem_fitted_SN_BAO_comparator | selected | sample test is dominated by un-fitted nuisance/background choices; fair comparator is needed before eta-law derivation or branch demotion | fit h0, omega_m0, rd and baseline dark-energy parameters under parity while keeping b_mem fixed | fitting b_mem, support claims, death claims, public evidence | false |
| RC851_1_deferred | eta_aF_DeltaR_derivation_next | deferred | still essential, but fair data check should tell us whether the positive-memory projection is worth deriving in its current form | return after 852 comparator | using sample-score losses as proof eta route fails | false |
| RC851_2_rejected | demote_M6_or_C0_from_sample_score | rejected | sample baselines are not fitted and null-control M6 differs from M0 background parameters | none | branch death from 850 | false |

## Claim Guard

| guard_id | claim | status | reason | valid_for_claim |
| --- | --- | --- | --- | --- |
| CG851_0_no_support | 850/851 supports MTS cosmology | forbidden | only a sample-score readout exists and candidate rows are nonclaim | false |
| CG851_1_no_death | positive b_mem or M6 is dead | forbidden | null-control M6 is not parameter-matched to M0 and no fair fit has run | false |
| CG851_2_no_parent_prediction | eta/a_F/DeltaR is now derived | forbidden | 851 only chooses whether to pursue derivation before or after fair comparator | false |
| CG851_3_allowed_readout | 850 reveals a BAO-pressure clue under sample parameters | allowed_private_nonclaim | sector deltas show positive fixed b_mem improves/softens SN in places but BAO dominates the penalty | false |

## Decision

| decision_id | finding | reason | status | claim_allowed | next_target | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| D851_0 | 850 is a useful pipeline and tension clue, not evidence | fixed-bmem rows evaluate cleanly but baselines and nuisance/background values are sample-only | readout_and_route_choice_only_no_support_no_death_no_parent_prediction | false | 852-Y5-R10-fair-fixed-bmem-SN-BAO-fitted-comparator-dry-run.md | false |
| D851_1 | BAO pressure is the immediate empirical issue | positive bmem rows can lower SN chi2 but strongly raise BAO chi2 under current sample shape/parameters | readout_and_route_choice_only_no_support_no_death_no_parent_prediction | false | 852-Y5-R10-fair-fixed-bmem-SN-BAO-fitted-comparator-dry-run.md | false |
| D851_2 | fair fixed-bmem fitted comparator is selected before eta derivation | we need to separate projection/BAO failure from un-fitted parameter artifact before investing in the parent amplitude law | readout_and_route_choice_only_no_support_no_death_no_parent_prediction | false | 852-Y5-R10-fair-fixed-bmem-SN-BAO-fitted-comparator-dry-run.md | false |

## Next Target

| next_target | objective | include | exclude | valid_for_claim |
| --- | --- | --- | --- | --- |
| 852-Y5-R10-fair-fixed-bmem-SN-BAO-fitted-comparator-dry-run.md | fit fair SN/BAO baselines and fixed-bmem M6 candidates while keeping b_mem fixed and nonclaim | baseline parity, h0/omega_m0/rd refits, fixed b_mem injection, edge flags, AIC/BIC, no support/death language | fitting b_mem, long run without explicit go-ahead, parent prediction claim, formalization-workbench edits | false |

## Source Register

| source_id | path | exists | needle_check | role | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| 850_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\850-Y5-R10-fixed-bmem-cosmology-score-evaluator-dry-run.md | true | pass | sample score handoff | false |
| 850_validation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_850_VALIDATION.csv | true | pass | prior checkpoint validation | false |
| 850_scores | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_850_FIXED_BMEM_SN_BAO_SAMPLE_SCORES.csv | true | pass | sample fixed-bmem SN/BAO score rows | false |
| 850_evaluator | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\scripts\strict_fixed_bmem_SN_BAO_evaluator.py | true | pass | sample-only evaluator implementation | false |

## Validation

| check_id | result | detail |
| --- | --- | --- |
| V851_0_sources_exist_and_needles | pass | all source paths exist and needles are present |
| V851_1_prior_850_clean | pass | P8_Y5_BRR545_850_VALIDATION.csv clean |
| V851_2_readout_two_branches | pass | sh0es and no_sh0es readouts present |
| V851_3_sector_tension_detected | pass | SN/BAO tension rows include SN_improves_BAO_worsens cases |
| V851_4_artifact_diagnosis_present | pass | null-control and BAO-pressure artifact diagnoses present |
| V851_5_route_selected | pass | fair fixed-bmem fitted comparator selected |
| V851_6_claim_allowed_false | pass | decision rows keep claim_allowed=false |
| V851_7_all_rows_nonclaim | pass | all generated rows valid_for_claim=false |
| V851_8_next_target_selected | pass | 852-Y5-R10-fair-fixed-bmem-SN-BAO-fitted-comparator-dry-run.md |
| V851_9_formalization_workbench_untouched | pass | formalization_changed_after_cutoff=0 |
| V851_10_validation_rows_ready | pass | validation table constructed |
