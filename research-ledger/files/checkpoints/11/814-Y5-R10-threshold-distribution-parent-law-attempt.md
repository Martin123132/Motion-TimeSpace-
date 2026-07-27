# 814 - Y5 R10 Threshold Distribution Parent Law Attempt

Current result: **the Weibull threshold law can be derived conditionally, but the fitted shape constants are not yet parent-derived**. The useful surprise is that `nu_act` is essentially `7/4`, and the equality activation is close to `3/5`; that creates a sharper theorem target, not a claim.

Generated UTC: `2026-06-12T17:38:52+00:00`

## Non-Claim Summary

| status | claim_ceiling | what_derived | what_not_derived | C1_status | next_target | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| Y5_R10_814_threshold_distribution_conditional_theorem_rational_clue_not_parent_lock_nonclaim | conditional_shape_theorem_only_no_C1_data_run_no_cosmology_support_claim | Weibull threshold law follows from a Poisson activation measure with power-law cumulative hazard. | parent origin of nu=7/4, equality-clock normalization, F_eq=3/5, and exact alpha_act | shape_lock_not_satisfied_data_run_blocked | 815-Y5-R10-rational-threshold-exponent-source-proof-or-shape-demotion.md | false |

## Threshold Theorem Attempt

| step | statement | status | blocks_C1_data_run | valid_for_claim |
| --- | --- | --- | --- | --- |
| T814_0_activation_survival_identity | Let U(N)=1-F(N). If dF/dN=h(N)(1-F), then dU/dN=-h(N)U and U(N)=exp[-integral_0^N h(s)ds]. | derived | false | false |
| T814_1_poisson_threshold_measure | If activation thresholds form a Poisson process over expansion-load measure dmu=h(N)dN, then F(N)=P(N_th<N)=1-exp[-mu([0,N])]. | derived | false | false |
| T814_2_weibull_condition | If h(N)=(nu/u_s)(N/u_s)^(nu-1), then mu([0,N])=(N/u_s)^nu and F(N)=1-exp[-(N/u_s)^nu]. | conditional_theorem | false | false |
| T814_3_parent_exponent_gap | The parent action/corpus still does not derive why the activation measure density must scale as N^(nu-1), nor why nu equals 7/4. | not_derived | true | false |
| T814_4_parent_scale_gap | The equality clock gives a natural scale u_eq, but the parent theory does not derive alpha_act or an exact F(u_eq) rule. | not_derived | true | false |

## Rational Diagnostics

| diagnostic | value | interpretation | valid_for_claim |
| --- | --- | --- | --- |
| nu_fit | 1.7500073382761008 | numeric diagnostic | false |
| nu_rational_7_4 | 1.75 | numeric diagnostic | false |
| nu_abs_diff_from_7_4 | 7.3382761007767527e-06 | nu_fit is extremely close to 7/4; this is a derivation target, not proof | false |
| nu_rel_diff_from_7_4 | 4.193300629015287e-06 | numeric diagnostic | false |
| alpha_fit | 1.0543379145228584 | numeric diagnostic | false |
| F_eq_fit | 0.5981031223224107 | numeric diagnostic | false |
| F_eq_diff_from_3_5 | -0.0018968776775892815 | F at equality is close to 3/5; rational clue only | false |
| alpha_from_Feq_3_5_nu_7_4 | 1.051223983540585 | numeric diagnostic | false |
| alpha_diff_from_3_5_7_4_candidate | 0.0031139309822734162 | alpha candidate from nu=7/4 and F_eq=3/5 is close but not exact | false |
| F_eq_nu_7_4_alpha_fit | 0.59810326457370211 | numeric diagnostic | false |
| F_eq_alpha_1 | 0.63212055882855767 | alpha=1 would give 1-exp(-1), not the fitted equality activation | false |

## Shape Lock Verdict

| shape_item | verdict | reason | C1_consequence | valid_for_claim |
| --- | --- | --- | --- | --- |
| Weibull functional form | conditionally_derived | follows from Poisson activation measure with power-law cumulative hazard | skeleton survives | false |
| nu_act exact value | rational_clue_not_parent_lock | nu_fit is within 7.338276100776753e-06 of 7/4, but no corpus theorem derives 7/4 | blocks data run | false |
| alpha_act exact value | equality_scale_clue_not_parent_lock | alpha is close to equality-clock normalization and F_eq is near 3/5, but no parent rule fixes either | blocks data run | false |
| threshold distribution N_th | conditional_measure_only | required density dmu=(nu/u_s^nu)N^(nu-1)dN is identified but not generated from parent dynamics | C1 shape remains source-hunt only | false |

## Candidate Shape Contract

| candidate_id | candidate_rule | alpha_candidate | alpha_fit | nu_candidate | nu_fit | status | allowed_use | forbidden_use | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C1_shape_7over4_3over5 | nu=7/4 and F(u_eq)=3/5, giving alpha=[1/ln(5/2)]^(4/7) | 1.051223983540585 | 1.0543379145228584 | 1.75 | 1.7500073382761008 | interesting_rational_source_target_not_parent_derived | future theorem target or stress-only predeclared shape | claim fitted shape is derived | false |

## Next Decision

| decision_id | decision | reason | next_target | next_question | run_now | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| D814_0 | do not run C1 data branch | functional form is conditionally derived but exact shape constants are not parent-locked | 815-Y5-R10-rational-threshold-exponent-source-proof-or-shape-demotion.md | Can nu=7/4 and/or F(u_eq)=3/5 be derived from parent source geometry rather than noticed after fitting? | false | false |

## Source Register

| source_id | path | exists | needle_check | role | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| 813_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\813-Y5-R10-C1-parent-lock-source-hunt-or-demotion.md | true | pass | immediate source-hunt selector | false |
| 813_validation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_813_VALIDATION.csv | true | pass | prior checkpoint validation | false |
| formal_117_shape | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\117-memory-shape-source-gate.md | true | pass | threshold/survival mechanism source | false |
| formal_118_status | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\118-cosmology-memory-status-decision.md | true | pass | frozen cosmology-memory status | false |

## Validation

| check_id | result | detail |
| --- | --- | --- |
| V814_0_sources_exist_and_needles | pass | all source paths exist and needles are present |
| V814_1_prior_813_clean | pass | P8_Y5_BRR545_813_VALIDATION.csv clean |
| V814_2_outputs_scoped | pass | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work |
| V814_3_all_rows_nonclaim | pass | all generated rows valid_for_claim=false |
| V814_4_conditional_weibull_theorem_present | pass | Weibull conditional theorem recorded |
| V814_5_exact_shape_not_parent_locked | pass | alpha_act and nu_act remain unpromoted |
| V814_6_rational_clue_recorded | pass | 7/4 and 3/5 candidate recorded as nonclaim target |
| V814_7_no_data_run_selected | pass | no C1 data run selected |
| V814_8_next_target_selected | pass | 815-Y5-R10-rational-threshold-exponent-source-proof-or-shape-demotion.md |
| V814_9_formalization_workbench_untouched | pass | formalization_changed_after_cutoff=0 |
| V814_10_validation_rows_ready | pass | validation table constructed |

## Verdict

This is a partial derivation win and a promotion failure. The form `F=1-exp[-(N/u_s)^nu]` is not arbitrary if the parent supplies a power-law activation measure. But the parent has not supplied the exponent or equality normalization. The next move is therefore not data; it is a targeted proof attempt for `nu=7/4` and the `F(u_eq)≈3/5` equality rule.

## Next Target

`815-Y5-R10-rational-threshold-exponent-source-proof-or-shape-demotion.md`
