# 853 - Y5 R10 Fixed Bmem Fitted Readout Or Projection Repair

Current result: **the fair fixed-`b_mem` SN/BAO comparator turns positive memory into a private nonclaim lead**. The earlier sample-only pessimism was largely a parameter-artifact warning: after fair refit, positive fixed-memory rows beat the fitted baselines in both SH0ES and no-SH0ES branches. The new bottleneck is not immediate empirical viability; it is what the amplitude means, because the preferred effective `b_mem` is branch-dependent and still not parent-derived.

## Non-Claim Summary

| status | claim_ceiling | what_changed | selected_route | what_is_not_claimed | next_target | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| Y5_R10_853_fixed_bmem_fair_fit_readout_positive_lead_nonclaim | readout_only_positive_lead_no_support_no_parent_prediction | converted fair fixed-bmem comparator into a positive nonclaim lead and amplitude-split problem | parent_amplitude_branch_split_law_or_projection_repair | support, parent prediction, public evidence, local-GR progress | 854-Y5-R10-parent-amplitude-branch-split-law-or-projection-repair.md | false |

## Branch Readout

| branch | best_positive_candidate | b_mem_fixed | eta1_aF_DeltaR_implied | chi2_total | delta_BIC_vs_best_fit_baseline | lead_status | interpretation | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| no_sh0es | S1_C0_CMB_reference | 0.0157305087947 | 0.0471915263842 | 1467.52226529 | -2.53382619 | competitive_nonclaim | positive fixed memory survives fair short SN/BAO comparator | false |
| sh0es | S1_C0_full_joint_reference | 0.112452590329 | 0.337357770986 | 1756.93143186 | -10.12020615 | competitive_nonclaim | positive fixed memory survives fair short SN/BAO comparator | false |

## Amplitude Split Audit

| split_id | no_sh0es_best_b_mem | sh0es_best_b_mem | absolute_split | ratio_sh0es_over_no_sh0es | eta1_aF_DeltaR_no_sh0es | eta1_aF_DeltaR_sh0es | status | meaning | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AS853_0_best_branch_amplitudes | 0.0157305087947 | 0.112452590329 | 0.0967220815343 | 7.14869377695 | 0.0471915263841 | 0.337357770987 | branch_dependent_effective_amplitude | local calibration pressure prefers a larger effective memory amplitude than Pantheon shape-only branch | false |

## Interpretation Gates

| gate_id | gate | status | reason | required_before_claim | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| IG853_0_positive_memory_alive | positive fixed b_mem can beat fair fitted SN/BAO baselines | passes_private_nonclaim | best positive fixed-bmem rows have negative delta_BIC in both sh0es and no_sh0es branches | derive b_mem parent amplitude and run robustness matrix | false |
| IG853_1_parent_prediction_missing | support-grade b_mem prediction | fails_open | winning amplitudes are C0/CMB references, not eta/a_F/DeltaR-derived predictions | derive eta, a_F, DeltaR and endpoint dynamics without using fitted amplitude as input | false |
| IG853_2_branch_split | single branch-invariant amplitude | fails_or_needs_effective_response_law | best sh0es amplitude is much larger than best no_sh0es amplitude | derive a calibration/observable projection law or repair the memory projection | false |

## Route Choice

| route_id | route | status | reason | include | exclude | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| RC853_0_selected | parent_amplitude_branch_split_law_or_projection_repair | selected | fair comparator turns positive memory into a lead, but the preferred amplitude is branch-dependent and not parent-derived | derive whether b_mem is invariant parent memory, effective observable response, or a projection needing BAO/SH0ES split repair | claiming support from fitted C0 references | false |
| RC853_1_deferred | full robustness scoring | deferred | worth doing after the amplitude/projection meaning is specified so the run is not just more phenomenology | later SN/BAO/H(z)/growth-CMB robustness | long execution now | false |

## Claim Guard

| guard_id | claim | status | reason | valid_for_claim |
| --- | --- | --- | --- | --- |
| CG853_0_no_support | 852/853 supports MTS cosmology | forbidden | the fit is short, private, and uses candidate amplitudes not parent predictions | false |
| CG853_1_no_parent_amplitude | eta/a_F/DeltaR has been derived | forbidden | 853 only identifies the branch-split target the parent law must explain | false |
| CG853_2_no_public_evidence | negative delta_BIC rows are public evidence | forbidden | robustness, residuals, data-split stability, and parent derivation remain open | false |
| CG853_3_allowed_lead | positive fixed memory is a private lead after fair refit | allowed_private_nonclaim | both branches have a positive fixed-bmem row with negative delta_BIC against fair fitted baselines | false |

## Decision

| decision_id | finding | reason | status | claim_allowed | next_target | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| D853_0 | fair refit reverses the crude 850 pessimism | positive fixed memory beats the fair fitted baselines in both SN/BAO branches | readout_only_positive_lead_no_support_no_parent_prediction | false | 854-Y5-R10-parent-amplitude-branch-split-law-or-projection-repair.md | false |
| D853_1 | amplitude meaning is now the bottleneck | best no_sh0es and sh0es amplitudes differ substantially, and neither is parent-derived | readout_only_positive_lead_no_support_no_parent_prediction | false | 854-Y5-R10-parent-amplitude-branch-split-law-or-projection-repair.md | false |

## Next Target

| next_target | objective | include | exclude | valid_for_claim |
| --- | --- | --- | --- | --- |
| 854-Y5-R10-parent-amplitude-branch-split-law-or-projection-repair.md | derive or repair the meaning of branch-dependent effective b_mem before more scoring | branch split law, eta/a_F/DeltaR targets, calibration-response versus invariant-memory distinction, projection repair options | support claim, public evidence, local-GR claim, formalization-workbench edits | false |

## Source Register

| source_id | path | exists | needle_check | role | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| 852_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\852-Y5-R10-fair-fixed-bmem-SN-BAO-fitted-comparator-dry-run.md | true | pass | fair comparator handoff | false |
| 852_validation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_852_VALIDATION.csv | true | pass | prior checkpoint validation | false |
| 852_scores | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_852_FAIR_FIXED_BMEM_SN_BAO_FIT_SCORES.csv | true | pass | fair fixed-bmem fit scores | false |
| 852_readout | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_852_FIT_READOUT.csv | true | pass | fair comparator branch readout | false |

## Validation

| check_id | result | detail |
| --- | --- | --- |
| V853_0_sources_exist_and_needles | pass | all source paths exist and needles are present |
| V853_1_prior_852_clean | pass | P8_Y5_BRR545_852_VALIDATION.csv clean |
| V853_2_positive_lead_present | pass | both branches have best positive fixed-bmem delta_BIC < 0 |
| V853_3_amplitude_split_recorded | pass | branch-dependent effective amplitude row recorded |
| V853_4_interpretation_gates_present | pass | positive lead and branch-split gates present |
| V853_5_route_selected | pass | parent amplitude branch-split law/projection repair selected |
| V853_6_claim_allowed_false | pass | decision rows keep claim_allowed=false |
| V853_7_all_rows_nonclaim | pass | all generated rows valid_for_claim=false |
| V853_8_next_target_selected | pass | 854-Y5-R10-parent-amplitude-branch-split-law-or-projection-repair.md |
| V853_9_formalization_workbench_untouched | pass | formalization_changed_after_cutoff=0 |
| V853_10_validation_rows_ready | pass | validation table constructed |
