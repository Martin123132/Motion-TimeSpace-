# 815 - Y5 R10 Rational Threshold Exponent Source Proof Or Shape Demotion

Current result: **the rational shape clue fails as a parent proof**. `nu=7/4` and `F(u_eq)=3/5` remain interesting, but without an independent source theorem they are not locks; the C1 shape is demoted to stress-only.

Generated UTC: `2026-06-12T17:42:34+00:00`

## Non-Claim Summary

| status | claim_ceiling | proof_verdict | shape_status | what_survives | what_failed | next_target | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Y5_R10_815_rational_threshold_proof_failed_shape_demoted_stress_only_nonclaim | rational_shape_clue_stress_only_no_C1_data_run_no_parent_shape_claim | rational_shape_source_proof_failed | C1_shape_7over4_3over5_demoted_to_stress_only | conditional Weibull theorem and rational numerical clue | independent parent source for nu=7/4 or F(u_eq)=3/5 | 816-Y5-R10-C1-shape-demotion-and-branch-replacement-contract.md | false |

## Proof Route Audit

| route_id | route | result | reason | what_it_would_need | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| R815_0_corpus_direct_source | Search corpus for independent parent statements fixing 7/4 or 3/5. | fail | No independent source theorem for these constants was found; they first appear as numeric clues in 814. | pre-existing parent action, symmetry, dimensional, or fixed-point result selecting the constants | false |
| R815_1_dimension_codimension_ratio | Explain nu=7/4 as d/p from activation-measure dimension over response power. | fail_conditional_only | d/p=7/4 would require a sourced seven-over-four structure; the corpus has no parent derivation of d=7 and p=4 for FLRW activation thresholds. | identified parent threshold manifold dimension and response power, both independent of cosmology data | false |
| R815_2_hazard_regularitiy | Use regularity of h(N) near N=0 to force the exponent. | fail_bounds_only | Regularity can motivate broad constraints such as positive hazard and finite source, but it does not select 7/4. | a precise differentiability/vanishing-order theorem that uniquely fixes nu=7/4 | false |
| R815_3_equality_partition | Derive F(u_eq)=3/5 from matter-memory equality. | fail_clue_only | Equality supplies a natural clock but not a partition rule giving exactly 3/5 activation. | parent conservation or counting law forcing 3 activated weights out of 5 at equality | false |
| R815_4_max_entropy_weibull | Use maximum-entropy or survival-process arguments to select Weibull constants. | fail_form_only | Survival arguments select a family once constraints are chosen; they do not supply the parent constraints that fix 7/4 or 3/5. | parent-derived moment/scale constraints before data | false |

## Rational Candidate Status

| candidate_id | status_before_815 | status_after_815 | reason | allowed_use | forbidden_use | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| C1_shape_7over4_3over5 | interesting_rational_source_target_not_parent_derived | stress_only_candidate | the constants are numerically sharp but source-unsourced | future no-claim stress test or theorem target | C1 parent lock, data-run permission, support claim | false |

## Shape Demotion

| item | new_status | reason | blocks_data_run | valid_for_claim |
| --- | --- | --- | --- | --- |
| Weibull functional form | conditional_skeleton_retained | derived from Poisson/power-law activation measure if parent supplies the measure | false | false |
| nu=7/4 | stress_only | no parent source proof | true | false |
| F(u_eq)=3/5 | stress_only | no parent equality-partition law | true | false |
| alpha_act derived from rational candidate | stress_only | depends on unsourced 3/5 equality activation rule | true | false |

## Next Decision

| decision_id | decision | reason | next_target | run_now | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| D815_0 | demote rational C1 shape to stress-only and write branch-replacement contract | exact shape constants are not parent-derived after proof-route audit | 816-Y5-R10-C1-shape-demotion-and-branch-replacement-contract.md | false | false |

## Source Register

| source_id | path | exists | needle_check | role | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| 814_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\814-Y5-R10-threshold-distribution-parent-law-attempt.md | true | pass | immediate rational-shape proof target | false |
| 814_validation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_814_VALIDATION.csv | true | pass | prior checkpoint validation | false |
| formal_117_shape | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\117-memory-shape-source-gate.md | true | pass | shape source gate | false |
| formal_118_status | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\118-cosmology-memory-status-decision.md | true | pass | cosmology memory demotion source | false |

## Validation

| check_id | result | detail |
| --- | --- | --- |
| V815_0_sources_exist_and_needles | pass | all source paths exist and needles are present |
| V815_1_prior_814_clean | pass | P8_Y5_BRR545_814_VALIDATION.csv clean |
| V815_2_outputs_scoped | pass | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work |
| V815_3_all_rows_nonclaim | pass | all generated rows valid_for_claim=false |
| V815_4_no_successful_exact_proof | pass | no proof route fixed 7/4 or 3/5 |
| V815_5_rational_candidate_demoted | pass | rational shape demoted to stress-only |
| V815_6_shape_blocks_data_run | pass | unsourced exact shape constants block C1 data |
| V815_7_no_data_run_selected | pass | no data run selected |
| V815_8_next_target_selected | pass | 816-Y5-R10-C1-shape-demotion-and-branch-replacement-contract.md |
| V815_9_formalization_workbench_untouched | pass | formalization_changed_after_cutoff=0 |
| V815_10_validation_rows_ready | pass | validation table constructed |

## Verdict

This is a useful failure. The theory has earned the Weibull form conditionally, but not the numbers. So the next branch must not pretend `7/4` and `3/5` are derived; it must either replace the shape with a parent-sourced law or keep the rational shape as a no-claim stress test.

## Next Target

`816-Y5-R10-C1-shape-demotion-and-branch-replacement-contract.md`
