# 845 - Y5 R10 Strict MTS Cosmology Branch Contract

Current result: **a stricter cosmology branch is now specified as a contract, not as a new fit**. C0 remains a closure-only benchmark. The clean support route is a parent-predicted `b_mem` before data; the operational exploratory route is a predeclared parent-corridor holdout that cannot become support unless upgraded by a parent amplitude theorem.

## Non-Claim Summary

| status | claim_ceiling | what_changed | clean_support_route | operational_route | what_is_not_claimed | next_target | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Y5_R10_845_strict_cosmology_branch_contract_locked_nonclaim | strict_branch_contract_only_no_new_fit_no_support_claim | strict cosmology branch contract installed with explicit amplitude-freedom and outcome-language rules | parent-predicted b_mem before data | predeclared parent amplitude corridor for exploratory holdout only | new evidence, C0 support, b_mem prediction, dark energy derivation, local GR relevance | 846-Y5-R10-strict-cosmology-branch-dry-run-spec.md | false |

## Strict Branch Contract

| branch_id | branch_name | purpose | amplitude_rule | free_amplitude_status | allowed_use | forbidden_use | support_claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SB845_0_C0_archive | C0_closure_benchmark | retain the old C0/radflat shape as a benchmark and diagnostic only | may display fitted b_mem values, but they do not count as predictions or support | benchmark_only | pipeline regression, sanity checks, residual anatomy comparison | support claim, public evidence pillar, parent amplitude proof | false | false |
| SB845_1_parent_predicted | strict_parent_predicted_amplitude | the clean route: b_mem fixed before data by a parent amplitude theorem | b_mem = a_F DeltaR / [3 eta^2] or equivalent must be parent-derived with signed inputs | blocked_until_theorem | future support-grade branch only after the amplitude prediction is derived | running as if b_mem were already predicted | false | false |
| SB845_2_predeclared_corridor | strict_predeclared_parent_corridor | exploratory route using the derived parent amplitude corridor without treating it as a prediction | b_mem prior/range must be declared before looking at new scores and must not be set by the full-joint best fit | exploratory_nonclaim | holdout stress test and branch pruning | support claim unless upgraded to parent-predicted amplitude | false | false |
| SB845_3_null_control | strict_null_control | verify the same pipeline can recover fitted baseline behaviour and reject artificial improvements | b_mem=0 or baseline-equivalent limit | control | pipeline and model-selection sanity check | MTS support or demotion claim | false | false |

## Parameter Freedom Ledger

| parameter | role | allowed_mode | source_rule | counts_in_AIC_BIC | support_allowed_if_free | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| F(z)_shape | memory/activation shape | fixed_or_predeclared | must come from parent/equality-scale argument or predeclared shape family before scoring | true_if_selected_from_family_or_tuned | false | false |
| b_mem | memory amplitude | parent_predicted_or_predeclared_corridor | parent-predicted for support; predeclared corridor only for exploratory pruning | true_if_fitted_or_corridor_selected_after_data | false | false |
| z50_act_width_act | transition location/width if used | fixed_by_physics_or_counted | must not be edge-seeking or retuned per dataset without parameter penalty | true_if_fitted | false | false |
| Omega_m0_H0_calibration | background calibration/nuisance | same_freedom_as_baselines | MTS and fitted baselines must receive symmetric calibration treatment | true_if_fitted | only_if_baseline_symmetric_and_other_gates_pass | false |
| sigma8_0 | growth nuisance | analytic_refit_allowed_if_baselines_same | count as fitted parameter and apply equally to baselines | true | only_if_baseline_symmetric_and_other_gates_pass | false |
| local_GR_closure | local theory guardrail | external_closure_only | cosmology scoring cannot improve or prove local GR status | not_applicable | false | false |

## Strict Test Gate

| gate_id | gate | pass_condition | failure_consequence | valid_for_claim |
| --- | --- | --- | --- | --- |
| TG845_0_no_rescue_fit | no C0 rescue-fitting | b_mem/shape freedoms are fixed or predeclared before scoring and not chosen from the previous full-joint optimum | branch remains closure benchmark only | false |
| TG845_1_same_baselines | same baseline treatment | LambdaCDM, wCDM, CPL, and MTS receive symmetric nuisance/calibration/covariance treatment | readout is pipeline diagnostic, not evidence | false |
| TG845_2_multi_arena_holdout | multi-arena holdout | candidate survives SN/BAO, H(z), growth, and compressed CMB gates without relying on one fragile arena | label as sector clue or demote to phenomenology | false |
| TG845_3_model_selection | fair AIC/BIC and residual anatomy | all fitted freedoms counted and residual anatomy matches the proposed mechanism | near-tie language only, no support claim | false |
| TG845_4_parent_upgrade | parent-amplitude upgrade | amplitude corridor becomes a no-fit parent prediction with signed inputs | strict branch remains exploratory even if numerically close | false |
| TG845_5_local_gr_firewall | local GR firewall | cosmology result does not alter local transition closure-only status | interpretation blocked until local closure conflict is resolved | false |

## Outcome Language Rules

| outcome_id | condition | allowed_language | forbidden_language | current_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| OR845_0_support_grade | parent-predicted b_mem plus robust multi-arena improvement over fitted baselines | support-grade empirical clue | fundamental theory confirmed or local GR derived | not_available | false |
| OR845_1_near_competitive | AIC/BIC near tie or small loss with no edge flag but no parent prediction | alive as constraint/clue; closure benchmark remains useful | evidence pillar | current_C0_zone | false |
| OR845_2_arena_specific | works in one arena but fails H(z), growth, CMB, or BAO holdout | sector-specific phenomenology | cosmology branch survives | possible | false |
| OR845_3_failure | fails symmetric baselines across multiple arenas | strict branch demoted | MTS cosmology is dead | future_possible | false |

## Claim Guard

| guard_id | claim | status | reason | valid_for_claim |
| --- | --- | --- | --- | --- |
| CG845_0_no_new_fit_claim | 845 provides new cosmology evidence | forbidden | 845 is a contract only; no new fit or optimisation is run | false |
| CG845_1_no_C0_support | C0 is support evidence | forbidden | C0 remains a closure benchmark until amplitude is parent-predicted and stable | false |
| CG845_2_no_amplitude_prediction | b_mem is predicted by the parent theory | forbidden | 178 derived a corridor but explicitly not a prediction | false |
| CG845_3_no_local_gr_claim | strict cosmology branch helps derive local GR | forbidden | local GR remains a separate closure-only theory obligation | false |
| CG845_4_allowed_contract | a stricter nonclaim cosmology branch contract is now defined | allowed_private_nonclaim | the output restricts future fitting freedoms and outcome language | false |

## Decision

| decision_id | finding | reason | status | claim_allowed | next_target | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| D845_0 | strict branch contract is required before further cosmology fitting | current C0 is near-competitive but amplitude freedom is not stable or predicted | strict_branch_contract_only_no_new_fit_no_support_claim | false | 846-Y5-R10-strict-cosmology-branch-dry-run-spec.md | false |
| D845_1 | clean support route is parent-predicted amplitude | only a no-fit b_mem theorem escapes rescue-fitting criticism | strict_branch_contract_only_no_new_fit_no_support_claim | false | 846-Y5-R10-strict-cosmology-branch-dry-run-spec.md | false |
| D845_2 | operational exploratory route is predeclared parent corridor | 178 gives a plausible corridor but not a unique prediction | strict_branch_contract_only_no_new_fit_no_support_claim | false | 846-Y5-R10-strict-cosmology-branch-dry-run-spec.md | false |

## Next Target

| next_target | objective | include | exclude | valid_for_claim |
| --- | --- | --- | --- | --- |
| 846-Y5-R10-strict-cosmology-branch-dry-run-spec.md | turn the strict branch contract into a dry-run scoring specification without running long fits | candidate branch rows, frozen/predeclared parameter file shape, baseline symmetry, data arenas, pass/fail outcomes, no-claim output schema | new data fit, GitHub action, formalization-workbench edits, support/death/local-GR claims | false |

## Source Register

| source_id | path | exists | needle_check | role | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| 844_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\844-Y5-R10-cosmology-evidence-readout-pack.md | true | pass | latest cosmology evidence ledger and strict-branch handoff | false |
| 844_validation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_844_VALIDATION.csv | true | pass | prior checkpoint validation | false |
| 175_full_joint_radflat_fit | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\175-full-joint-radflat-phenomenology-fit.md | true | pass | full joint radflat fit motivating stricter amplitude discipline | false |
| 176_C0_demotion_decision | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\176-C0-radflat-demotion-decision.md | true | pass | C0 closure-benchmark decision | false |
| 177_parent_amplitude_repair_contract | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\177-parent-amplitude-repair-contract.md | true | pass | parent amplitude repair contract | false |
| 178_parent_amplitude_theorem_attempt | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\178-parent-amplitude-theorem-attempt.md | true | pass | latest parent-amplitude theorem attempt | false |

## Validation

| check_id | result | detail |
| --- | --- | --- |
| V845_0_sources_exist_and_needles | pass | all source paths exist and needles are present |
| V845_1_prior_844_clean | pass | P8_Y5_BRR545_844_VALIDATION.csv clean |
| V845_2_strict_branches_recorded | pass | C0 benchmark, parent-predicted, predeclared-corridor, and null-control branches recorded |
| V845_3_bmem_freedom_restricted | pass | b_mem free support is forbidden unless parent-predicted |
| V845_4_test_gates_complete | pass | no-rescue, baseline, holdout, model-selection, parent-upgrade, and local-GR gates recorded |
| V845_5_outcome_language_complete | pass | support, near-competitive, arena-specific, and failure language rules recorded |
| V845_6_no_support_claim_allowed | pass | no strict branch currently allows support or parent-amplitude prediction claim |
| V845_7_all_rows_nonclaim | pass | all generated rows valid_for_claim=false |
| V845_8_next_target_selected | pass | 846-Y5-R10-strict-cosmology-branch-dry-run-spec.md |
| V845_9_formalization_workbench_untouched | pass | formalization_changed_after_cutoff=0 |
| V845_10_validation_rows_ready | pass | validation table constructed |
