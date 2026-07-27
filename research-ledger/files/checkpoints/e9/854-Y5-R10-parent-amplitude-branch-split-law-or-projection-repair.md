# 854 - Y5 R10 Parent Amplitude Branch Split Law Or Projection Repair

Current result: **the branch-dependent fixed-`b_mem` lead has been converted into a parent-plus-observable-projection contract, not a claim**. The least-ad-hoc route is to treat `b_parent = a_F DeltaR/(3 eta^2)` as the invariant corridor quantity and test whether SH0ES/no-SH0ES differences arise from an observable calibration projection, `b_eff[B] = b_parent + Pi_B(...)`. If that estimator fails, the memory projection itself must be repaired before more scoring.

## Non-Claim Summary

| status | claim_ceiling | what_changed | selected_route | what_is_not_claimed | next_target | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| Y5_R10_854_branch_split_law_contract_ready_nonclaim | formal_branch_split_contract_only_no_parent_prediction_no_support | converted branch-dependent b_eff into a formal parent-plus-projection contract | calibration_projection_response_estimator | parent amplitude, calibration proof, support, public evidence, local-GR progress | 855-Y5-R10-calibration-projection-response-estimator-dry-run.md | false |

## Branch Targets

| branch | empirical_best_positive_candidate | b_eff_target | eta1_aF_DeltaR_target | delta_BIC_vs_best_fit_baseline | target_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| no_sh0es | S1_C0_CMB_reference | 0.0157305087947 | 0.0471915263841 | -2.53382619 | private_nonclaim_target_for_parent_law | false |
| sh0es | S1_C0_full_joint_reference | 0.112452590329 | 0.337357770987 | -10.12020615 | private_nonclaim_target_for_parent_law | false |

## Branch Split Law Attempt

| law_id | statement | status | numeric_target_or_coefficient | derivation_status | blocks_claim | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| BSL854_0_parent_identity | b_parent = a_F DeltaR/(3 eta^2) | formal_identity_survives | not_unique | corridor_only_from_178 | true | false |
| BSL854_1_effective_branch_law | b_eff[B] = b_parent + Pi_B(calibration/local-offset response) | proposed_contract_not_derived | b_parent_probe=0.0157305087947; response_sh0es_minus_no_sh0es=0.0967220815343 | requires projection operator from SN calibration/marginalization geometry | true | false |
| BSL854_2_linear_response_estimator | delta b_B = (J_b^T W_B P_B J_cal)/(J_b^T W_B P_B J_b) delta cal_B | least_squares_projection_candidate | must reproduce response_sh0es_minus_no_sh0es without fitting b_mem | algebraic estimator can be tested next; parent physical origin not yet signed | true | false |
| BSL854_3_multiplicative_response_fallback | b_eff[B] = R_B b_parent | fallback_phenomenological_parameterization | R_sh0es_over_no_sh0es=7.14869377695 | not acceptable as final theory unless R_B is derived from observables | true | false |

## Parent Clause Audit

| clause_id | parent_clause | required_for_branch_law | status | next_test | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| PC854_0_eta | eta = H0 L_cg/c | derive whether L_cg is invariant or observer/calibration projected | open | calibration projection estimator cannot prove eta but can tell whether branch split is observational | false |
| PC854_1_aF | a_F sign and normalization | derive trace-coupling normalization and whether it couples to local calibration sector | open | if response term aligns with calibration projection, a_F may remain invariant while Pi_B changes | false |
| PC854_2_DeltaR | DeltaR endpoint memory dynamics | derive whether endpoint difference is single cosmic memory or branch-effective observable memory | open | projection estimator should separate invariant shape-only target from SH0ES response excess | false |
| PC854_3_conservation | covariant conservation/Bianchi compatibility | response term must be observational/projection-level or have conserved stress-energy source | open_guardrail | do not promote response_B to physical field term unless conservation accounting is signed | false |

## Projection Repair Options

| option_id | option | pros | risk | next_action | selected | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| RO854_0_observable_projection | b_eff is branch-projected while b_parent is invariant | explains why no_SH0ES and SH0ES prefer different effective amplitudes without making parent memory inconsistent | can become post-hoc unless projection operator predicts the split before scoring | estimate Pi_B from SN covariance/calibration vectors and BAO response | true | false |
| RO854_1_projection_repair | current M6 memory projection shape is incomplete | directly addresses branch split if response estimator fails | too much freedom if alpha/nu or shape are opened without parent derivation | only after calibration projection estimator fails | fallback | false |
| RO854_2_single_amplitude_claim | declare one branch amplitude fundamental | simple | ignores observed branch dependence and would be weak/overclaiming | reject for now | false | false |

## Route Choice

| route_id | route | status | reason | include | exclude | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| RC854_0_selected | calibration_projection_response_estimator | selected | branch split can be a principled observable response only if a projection estimator predicts the SH0ES excess from data geometry | SN branch masks, nuisance offset/calibrator vector, J_b response, BAO response, no b_mem fitting | support claim, branch-amplitude assertion, parent derivation by fitted target | false |
| RC854_1_deferred | projection_shape_repair | deferred | only needed if calibration projection fails to account for the branch split | activation-shape or BAO-response repair contract | opening free shape parameters now | false |

## Claim Guard

| guard_id | claim | status | reason | valid_for_claim |
| --- | --- | --- | --- | --- |
| CG854_0_no_parent_prediction | 854 derives b_parent | forbidden | 854 proposes a branch-split law contract; eta/a_F/DeltaR remain unsigned | false |
| CG854_1_no_response_claim | SH0ES excess is proven calibration response | forbidden | projection estimator has not yet been run | false |
| CG854_2_no_support | positive fixed memory is public support | forbidden | positive lead remains private and parent/robustness gates are open | false |
| CG854_3_allowed_contract | a concrete branch-split law contract is ready to test | allowed_private_nonclaim | 854 converts the amplitude split into a falsifiable projection-estimator target | false |

## Decision

| decision_id | finding | reason | status | claim_allowed | next_target | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| D854_0 | branch split should not be collapsed into a single fitted amplitude | no_SH0ES and SH0ES prefer different effective amplitudes after fair refit | formal_branch_split_contract_only_no_parent_prediction_no_support | false | 855-Y5-R10-calibration-projection-response-estimator-dry-run.md | false |
| D854_1 | observable projection law is the least-ad-hoc next route | it can be tested against SN calibration/marginalization geometry before changing the physics projection | formal_branch_split_contract_only_no_parent_prediction_no_support | false | 855-Y5-R10-calibration-projection-response-estimator-dry-run.md | false |

## Next Target

| next_target | objective | include | exclude | valid_for_claim |
| --- | --- | --- | --- | --- |
| 855-Y5-R10-calibration-projection-response-estimator-dry-run.md | estimate whether the SH0ES/no-SH0ES b_eff split follows from calibration projection geometry rather than a new fitted field amplitude | linear response estimator, SN branch masks, calibrator/local-offset vector, finite-difference J_b, BAO penalty, no support claim | fitting b_mem, deriving eta from the fitted split, formalization-workbench edits | false |

## Source Register

| source_id | path | exists | needle_check | role | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| 853_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\853-Y5-R10-fixed-bmem-fitted-readout-or-projection-repair.md | true | pass | positive lead and branch-split handoff | false |
| 853_validation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_853_VALIDATION.csv | true | pass | prior checkpoint validation | false |
| 853_branch_readout | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_853_BRANCH_READOUT.csv | true | pass | best branch fixed-bmem amplitudes | false |
| 853_amplitude_split | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_853_AMPLITUDE_SPLIT_AUDIT.csv | true | pass | branch amplitude split summary | false |
| 177_parent_amplitude_contract | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\177-parent-amplitude-repair-contract.md | true | pass | parent amplitude obligations | false |
| 178_parent_amplitude_attempt | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\178-parent-amplitude-theorem-attempt.md | true | pass | prior theorem attempt and open gaps | false |

## Validation

| check_id | result | detail |
| --- | --- | --- |
| V854_0_sources_exist_and_needles | pass | all source paths exist and needles are present |
| V854_1_prior_853_clean | pass | P8_Y5_BRR545_853_VALIDATION.csv clean |
| V854_2_branch_targets_present | pass | no_sh0es and sh0es b_eff targets present |
| V854_3_branch_split_law_contract_present | pass | parent-plus-projection and linear estimator laws recorded |
| V854_4_parent_clauses_remain_open | pass | eta/a_F/DeltaR/conservation clauses remain open |
| V854_5_observable_projection_selected | pass | calibration projection estimator selected |
| V854_6_claim_allowed_false | pass | decision rows keep claim_allowed=false |
| V854_7_all_rows_nonclaim | pass | all generated rows valid_for_claim=false |
| V854_8_next_target_selected | pass | 855-Y5-R10-calibration-projection-response-estimator-dry-run.md |
| V854_9_formalization_workbench_untouched | pass | formalization_changed_after_cutoff=0 |
| V854_10_validation_rows_ready | pass | validation table constructed |
