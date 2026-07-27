# 820 - Y5 R10 C2A Source-Axiom Algebraic Stress Test

Current result: **C2A_TS1 survives as useful algebra but fails as a claimable/predictive branch until X(N) is parent-locked**. The exact derivative and budget identities are real. The killer caveat is also real: if X(N) is free, the closure can reproduce any monotone target history.

Generated UTC: `2026-06-12T18:09:48+00:00`

## Nonclaim Summary

| status | axiom_id | claim_ceiling | verdict | sharpest_failure | next_target | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| Y5_R10_820_C2A_algebra_survives_only_as_parent_locked_closure_nonclaim | C2A_TS1_threshold_survival_source_closure | Level_2_effective_closure_candidate_only_no_parent_derivation_no_data_run | algebra useful but not predictive until X(N) is parent-locked | free X(N) can encode any monotone target F_fit(N) | 821-Y5-R10-C2A-parent-control-scalar-candidate-hunt.md | false |

## Stress Tests

| test_id | question | result | derivation | required_condition | failure_mode | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| T820_0_exact_derivative | Is S_Gamma exactly the derivative of a bounded cumulative source? | survives_conditionally | For F_X=1-exp[-(X/X_star)^p], dF_X/dN=p*(X/X_star)^(p-1)*(dX/dN)/X_star*exp[-(X/X_star)^p]. Thus S_Gamma=B_mem*dF_X/dN. | X differentiable or absolutely continuous; p>0; X_star>0 | without a defined parent X(N), the derivative identity is algebraic closure only | false |
| T820_1_positivity | When is the source nonnegative? | survives_only_with_sign_locks | The exponential and power factor are nonnegative for X>=0. The sign is sign(B_mem*dX/dN) when p>0 and X_star>0. | B_mem>=0 and dX/dN>=0 on the branch, or an explicit signed-source policy | any interval with dX/dN<0 creates a sink/negative source | false |
| T820_2_normalization | When does the total source equal B_mem? | survives_only_with_endpoint_locks | Integral S_Gamma dN=B_mem[F_X(N_f)-F_X(N_i)]. Full normalization needs F_X(N_i)=0 and F_X(N_f)=1. | X(N_i)=0 and X(N_f)->infinity, or a declared finite-budget fraction | finite terminal X gives only B_mem*(1-exp[-(X_f/X_star)^p]) | false |
| T820_3_onset_regularity | Can the source diverge at activation? | regularity_requires_rp_ge_1 | If X~C*(N-N_i)^r with r>0, then S_Gamma~B_mem*p*r*(C/X_star)^p*(N-N_i)^(r*p-1). | integrable for r*p>0; finite at onset only if r*p>=1; zero onset only if r*p>1 | 0<r*p<1 gives an integrable but divergent activation spike | false |
| T820_4_shape_identifiability | Does p_source determine the source history by itself? | fails_without_parent_X | The N-profile is multiplied by dX/dN; therefore p_source fixes only the density with respect to X, not with respect to N. | derive or predeclare X(N) independently of target cosmology residuals | a free monotone X(N) can reshape the source in N almost arbitrarily | false |
| T820_5_arbitrary_fit_inversion | Can the closure encode any desired monotone memory history if X(N) is free? | hard_fail_for_claims | For any desired monotone F_fit(N) in [0,1), choose X(N)=X_star*(-ln(1-F_fit(N)))^(1/p). Then F_X(N)=F_fit(N). | X(N) must be parent-derived or predeclared before data; otherwise this is a universal monotone-history parametrizer | target-data leakage and fit-renaming | false |

## Endpoint And Regularity Laws

| law_id | statement | status | implication | valid_for_claim |
| --- | --- | --- | --- | --- |
| E820_0_total_budget | Delta_Gamma = integral_{N_i}^{N_f} S_Gamma dN = B_mem*(F_f-F_i). | exact_if_absolute_continuity_holds | amplitude budget cannot be interpreted without endpoint values | false |
| E820_1_full_activation | Full activation Delta_Gamma=B_mem requires X_i=0 and X_f->infinity. | conditional | finite X_f leaves unactivated memory fraction exp[-(X_f/X_star)^p] | false |
| E820_2_finite_endpoint | If X_i=0 and X_f=X_star, then Delta_Gamma=B_mem*(1-exp[-1])~0.632 B_mem. | counterexample_anchor | normalization to B_mem is false unless endpoints are locked | false |
| E820_3_onset_power_law | For X~C tau^r near activation, S_Gamma~tau^(r*p-1). | regularity_gate | finite source onset requires r*p>=1 | false |
| E820_4_X_density_peak | The density dF/dX peaks at (X/X_star)^p=(p-1)/p only for p>1; p=1 peaks at X=0; 0<p<1 is singular at X=0. | shape_warning | a smooth source onset prefers p>1 or an X onset with r*p>=1, but the N-peak still depends on dX/dN | false |

## Counterexamples

| counterexample_id | construction | breaks | lesson | valid_for_claim |
| --- | --- | --- | --- | --- |
| CE820_0_nonmonotone_X | Choose X(N)=1+0.1*sin(N) on an interval where cos(N)<0. | positivity | X>=0 is not enough; dX/dN sign must be controlled. | false |
| CE820_1_finite_terminal_X | Choose X(N_i)=0 and X(N_f)=X_star. | full_budget_normalization | integral is only 1-exp[-1] of B_mem, not B_mem. | false |
| CE820_2_activation_spike | Choose p=1/2 and X~C*(N-N_i). | finite_onset_regularness | source is integrable but diverges like (N-N_i)^(-1/2). | false |
| CE820_3_arbitrary_monotone_fit | Given any monotone target F_fit(N), set X=X_star*(-ln(1-F_fit))^(1/p). | independent_predictivity | without parent X, C2A can become a dressed fit function. | false |

## Survival Conditions

| condition_id | requirement | reason | status | next_action | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| SC820_0_parent_X | Define X(N) from parent/coarse-grained invariants before target-data comparison. | blocks arbitrary monotone-history inversion | missing | hunt candidate X from Gamma_mem, flow, curvature, matter, or coarse-graining variables | false |
| SC820_1_sign | Prove X>=0 and dX/dN>=0, or explicitly choose a signed-source branch. | needed for nonnegative memory activation | missing | derive monotonicity or demote to signed stress closure | false |
| SC820_2_endpoints | State and prove X_i=0 and X_f->infinity, or carry the finite activation fraction. | needed for honest B_mem interpretation | missing | treat B_mem as total budget only after endpoint law is signed | false |
| SC820_3_regular_onset | If X~C tau^r, require r*p>=1 for finite onset source. | avoids an unphysical activation spike unless explicitly allowed | new_gate | derive onset power r from candidate X dynamics | false |
| SC820_4_shape | Derive or predeclare p_source independent of SN/BAO/CMB/growth data. | prevents reusing C1 fit clues as derivation | missing | source p_source from threshold geometry or keep it stress-only | false |
| SC820_5_perturbations | Specify c_s^2, pi_Gamma, Q_m^nu, early limit, and growth sign response. | background source law alone cannot support growth/CMB claims | missing | defer until parent X is chosen | false |

## Decision

| decision_id | decision | reason | claim_ceiling | runnable | next_target | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| D820_0 | C2A_TS1 survives as a conditional algebraic closure only | exact derivative and normalization identities hold, but only with unsourced sign, endpoint, and parent-X conditions | Level_2_effective_closure_candidate_only_no_parent_derivation_no_data_run | false | 821-Y5-R10-C2A-parent-control-scalar-candidate-hunt.md | false |
| D820_1 | parent-lock X(N) before any data or support claim | free X(N) can reproduce any monotone F_fit(N), so independent predictivity is otherwise zero | Level_2_effective_closure_candidate_only_no_parent_derivation_no_data_run | false | 821-Y5-R10-C2A-parent-control-scalar-candidate-hunt.md | false |

## Next Target

| next_target | objective | allowed_work | forbidden_work | valid_for_claim |
| --- | --- | --- | --- | --- |
| 821-Y5-R10-C2A-parent-control-scalar-candidate-hunt.md | hunt a parent-derived or predeclared control scalar X(N) and test monotonicity/endpoints before data | source audit, symbolic candidate ranking, sign/endpoints/units proof | SN/BAO/CMB/growth fitting or evidence claim | false |

## Source Register

| source_id | path | exists | needle_check | role | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| 819_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\819-Y5-R10-C2A-minimal-source-axiom-candidate-manifest.md | true | pass | immediate source-axiom manifest | false |
| 819_validation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_819_VALIDATION.csv | true | pass | prior checkpoint validation | false |
| 819_manifest | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_819_AXIOM_CANDIDATE_MANIFEST.csv | true | pass | machine-readable candidate source law | false |
| formal_120_promotion | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\120-derivability-promotion-gate.md | true | pass | promotion standard and anti-fit-smuggling gate | false |
| formal_155_Hz | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\155-cosmology-status-after-Hz-covariance.md | true | pass | background-only and perturbation-contract warning | false |

## Validation

| check_id | result | detail |
| --- | --- | --- |
| V820_0_sources_exist_and_needles | pass | all source paths exist and needles are present |
| V820_1_prior_819_clean | pass | P8_Y5_BRR545_819_VALIDATION.csv clean |
| V820_2_exact_derivative_test_present | pass | exact derivative identity tested |
| V820_3_arbitrary_fit_inversion_flagged | pass | free X(N) arbitrary-fit inversion flagged |
| V820_4_endpoint_laws_present | pass | budget, full activation, and onset laws present |
| V820_5_counterexamples_present | pass | counterexamples cover sign, endpoint, regularity, and predictivity |
| V820_6_survival_conditions_complete | pass | survival conditions complete |
| V820_7_decision_nonrunnable | pass | C2A remains non-runnable |
| V820_8_next_target_selected | pass | 821-Y5-R10-C2A-parent-control-scalar-candidate-hunt.md |
| V820_9_all_rows_nonclaim | pass | all generated rows valid_for_claim=false |
| V820_10_formalization_workbench_untouched | pass | formalization_changed_after_cutoff=0 |
| V820_11_validation_rows_ready | pass | validation table constructed |

## Verdict

This is a good sharpening, not a loss. We now know exactly where the theory has to become real: the control scalar X(N). Without that, C2A is too flexible. With a parent-derived X and signed endpoints, the same algebra becomes a disciplined branch rather than a fitted costume.