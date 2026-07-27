# 1059 Y5 R10 alpha counterterm product prior source pack and cross arena gate

**Progress:** the retained alpha counterterm branch is now a product-prior source pack. Clock and WEP have concrete source-backed product bounds/targets; R10 has the finite-branch schema but remains unscoreable.

**Current verdict:** useful for testing discipline, not a pass. The pack forbids standalone `b_alpha`, standalone `beta_source_alpha`, clock-to-WEP transfer, and clock-to-R10 transfer unless the missing projections are derived.

**Next move:** build a product-prediction runner schema. That runner should fail until actual MTS inputs for `tau_clock`, `tau_WEP`, `tau_R10`, `beta_s/beta_t`, and `K_X/Z_X` are supplied.

## Source register
| source_id | source_path | exists | needle_found | role |
| --- | --- | --- | --- | --- |
| SRC1059_0_1058_next | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1058_NEXT_TARGET.csv | true | true | 1058 handoff. |
| SRC1059_1_1058_prior | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1058_ALPHA_COUNTERTERM_PRIOR_BRANCH.csv | true | true | alpha counterterm prior branch. |
| SRC1059_2_1058_cross | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1058_CROSS_ARENA_ALPHA_COUNTERTERM_LINKS.csv | true | true | cross-arena product links. |
| SRC1059_3_1052_clock | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1052_ALPHA_CLOCK_PRODUCT_BOUND_LEDGER.csv | true | true | clock product bounds. |
| SRC1059_4_1052_WEP | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1052_ALPHA_WEP_PROJECTION_LEDGER.csv | true | true | WEP alpha product target. |
| SRC1059_5_1052_R10 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1052_ALPHA_R10_PROJECTION_LEDGER.csv | true | true | R10 product law and missing inputs. |
| SRC1059_6_1053_tau | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1053_TAU_WEP_R10_PROJECTION_AUDIT.csv | true | true | tau/source projection debts. |
| SRC1059_7_1053_KX | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1053_KX_ZX_PLACEHOLDER_LEDGER.csv | true | true | K_X/Z_X placeholder ledger. |
| SRC1059_8_1053_beta | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1053_BETA_SOURCE_ALPHA_DERIVATION_AUDIT.csv | true | true | beta_source_alpha blocked status. |
| SRC1059_9_1054_prior | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1054_NUMERIC_PRIOR_WIDTH_LEDGER.csv | true | true | numeric product-width ledger. |
| SRC1059_10_1057_retained | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1057_RETAINED_BRANCH_LEDGER.csv | true | true | retained branch rows. |
| SRC1059_11_R10_bound_candidate | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv | true | true | R10 review-candidate bound curve for smoke only. |
| SRC1059_12_R10_runner | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\scripts\R10_alpha_lambda_bound_prediction_runner.py | true | true | existing R10 runner and schema. |


## Alpha product-prior source pack
| pack_id | arena | product_symbol | bound_or_target | units | score_rule | missing_for_standalone | score_ready | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| APP1059_0_clock_YbE3E2 | clock | P_clock_alpha := b_alpha*tau_clock_time | abs(P_clock_alpha) <= 2.1e-18 yr^-1 at 1sigma; 3.2e-18 yr^-1 at 2sigma | yr^-1 | usable only as clock product; standalone b_alpha forbidden | tau_clock_time parent derivation; Xhat/chi_X/readout normalization | true_nonclaim_product_only | false |
| APP1059_1_clock_AlHg | clock | P_clock_alpha := b_alpha*tau_clock_time | abs(P_clock_alpha) <= 3.9e-17 yr^-1 at 1sigma; 6.2e-17 yr^-1 at 2sigma | yr^-1 | weaker cross-check row; product-only | tau_clock_time parent derivation; Xhat/chi_X/readout normalization | true_nonclaim_product_only | false |
| APP1059_2_WEP_alpha_Coulomb | MICROSCOPE_WEP | P_WEP_alpha := beta_source_alpha*b_alpha*tau_WEP | abs(P_WEP_alpha) <= 4.797780522732e-05 under the alpha/Coulomb smoke convention | dimensionless in current WEP smoke convention | target for a predicted product; no standalone beta_source_alpha or b_alpha | beta_source_alpha owner; tau_WEP; full material model; shared domain rule | target_only_nonclaim | false |
| APP1059_3_WEP_surface_binding | MICROSCOPE_WEP | P_WEP_surface := beta_source_or_binding*b_A*tau_WEP | abs(P_WEP_surface) <= 2.887280314062e-05 if surface/binding branch survives | dimensionless in current WEP smoke convention | robust target only; not an alpha-only pass | binding coefficient owner; tau_WEP; full composition/material convention | target_only_nonclaim | false |
| APP1059_4_R10_finite_alpha | R10_short_range | P_R10_alpha(lambda) := K_X^R10(lambda)*beta_s(lambda)*beta_t(lambda)+epsilon_tail(lambda) | abs(P_R10_alpha(lambda)) <= alpha_bound(lambda) only after promoted bound curve and sourced inputs | dimensionless alpha(lambda) | currently schema-only; R10 runner must reject placeholders | lambda_X; Z_X; K_X; tau_R10; beta_s; beta_t; promoted bound curve | false | false |


## No-transfer gates
| gate_id | forbidden_transfer | reason | allowed_use | missing_to_unlock | gate_pass | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| NTG1059_0_clock_to_balpha | clock product -> standalone b_alpha | tau_clock_time is product-defined but not parent-derived | quote abs(b_alpha*tau_clock_time) bounds only | tau_clock_time and Xhat/chi_X normalization | false | false |
| NTG1059_1_clock_to_WEP | clock product -> WEP source-force product | WEP uses beta_source_alpha*b_alpha*tau_WEP, not b_alpha*tau_clock_time | compare only after parent map relates tau_clock_time to beta_source_alpha*tau_WEP | beta_source_alpha owner; tau_WEP; shared normalization theorem | false | false |
| NTG1059_2_clock_to_R10 | clock product -> R10 alpha(lambda) | R10 needs source/test charges and K_X/Z_X/tau_R10, not clock drift alone | none for R10 scoring until finite branch inputs are sourced | beta_s; beta_t; tau_R10; K_X/Z_X; lambda_X; promoted curve | false | false |
| NTG1059_3_WEP_to_R10 | WEP target -> R10 pass | composition DeltaQ WEP target and short-range torque alpha(lambda) have different kernels | shared beta/tau maps only if derived in one parent convention | R10 profile/material projection and source/test beta split | false | false |


## Projection debt ledger
| debt_id | projection | status | source | blocks | next_required_input | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| PD1059_0_tau_clock | tau_clock_time | PRODUCT_MAP_NOT_PARENT_DERIVED | TPR1053_0_clock_product | standalone b_alpha | derive local time/readout projection for chi_X or keep product bound | false |
| PD1059_1_beta_source_alpha | beta_source_alpha | OWNER_NOT_DERIVED | BSA1053_5_verdict | WEP product prediction and beta_source standalone prior | theorem-zero or source-backed numeric prior in one material convention | false |
| PD1059_2_tau_WEP | tau_WEP | DEFINITION_REQUIRED_NOT_FOUND | TPR1053_1_tau_WEP_definition | WEP alpha product prediction | lab/source/orbit/material projection tensor | false |
| PD1059_3_tau_R10 | tau_R10 | DEFINITION_ONLY | TPR1053_2_tau_R10_definition | R10 finite branch score | finite-source profile integral and readout trace convention | false |
| PD1059_4_KX_ZX_lambda | K_X/Z_X/lambda_X | SYMBOLIC_CONDITIONAL | KZ1053_3_KX_R10 | R10 alpha(lambda) prediction | parent finite-range branch and R10 harmonic kernel | false |


## Product-only score rules
| rule_id | rule | effect | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- |
| PSR1059_0_product_only | a row with a product_symbol may only score that exact product | prevents product bound from being divided by assumed tau/source factors | false | false |
| PSR1059_1_no_unity_tau | tau_clock, tau_WEP, and tau_R10 cannot be set to unity by convention | blocks unit-rescaling shortcuts | false | false |
| PSR1059_2_no_cancellation | counterterm components are absolute/no-cancellation until a signed parent relation exists | prevents hiding WEP/R10 pressure by branch cancellation | false | false |
| PSR1059_3_claim_validity | valid_for_claim may become true only when product prediction and bound are numeric, sourced, unit-matched, and projection-owned | keeps smoke rows private/nonclaim | false | false |


## Decision ledger
| decision_id | decision | because | next_action | valid_for_claim |
| --- | --- | --- | --- | --- |
| DEC1059_0_pack_status | alpha counterterm branch is now a product-prior pack | clock and WEP have source-backed product bounds/targets, while R10 has a schema and missing inputs | use product-only rows for future tests | false |
| DEC1059_1_claim_status | no standalone b_alpha, beta_source_alpha, WEP pass, or R10 pass | tau/source/K_X/Z_X projections are not parent-derived | keep claim gates blocked | false |
| DEC1059_2_best_next | next target is the first scoreable product-prediction runner | the product-prior pack exists, but MTS does not yet predict the products numerically | 1060-Y5-R10-alpha-product-prediction-stub-runner-and-required-inputs.md | false |


## MTS R10 smoke template
| model_id | branch_id | lambda_value | alpha_predicted | force_law_form | derivation_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| MTS_source_normalized_Newton_branch | alpha_product_prior_pack_template | MISSING_R10_LAMBDA_X | MISSING_R10_PRODUCT_PREDICTION | clock bounds b_alpha*tau_clock; WEP targets beta_source_alpha*b_alpha*tau_WEP; R10 needs K_X^R10 beta_s beta_t + epsilon_tail | template_invalid_product_prior_pack_nonclaim | false |


## Runner smoke status
| smoke_id | valid_mts_rows | valid_bound_rows | comparison_rows | R10_pass_for_claim | claim_allowed | expected_result |
| --- | --- | --- | --- | --- | --- | --- |
| SMOKE1059_0_R10_runner_refusal | 0 | 0 | 1 | false | false | reject alpha-product placeholders until prediction inputs are sourced |


## Placeholder refusal runner
| refusal_id | object | current_status | refusal_status | failure_reasons | score_eligible | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- |
| REF1059_0_standalone | standalone alpha counterterm constants | PRODUCT_ONLY_NONCLAIM | blocked | tau/source projections missing; product rows cannot be divided into standalone constants | false | false |
| REF1059_1_cross_arena | clock/WEP/R10 transfer | NO_TRANSFER_WITHOUT_PARENT_MAP | blocked | tau_clock, tau_WEP, tau_R10, beta_source, and K_X/Z_X are not related by parent theorem | false | false |
| REF1059_2_R10_runner | R10 alpha-product smoke row | runner_refusal_expected | blocked | valid_mts_rows=0; valid_bound_rows=0 | false | false |


## Claim gates
| gate_id | claim | gate_pass | reason | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| CG1059_0_standalone_balpha | standalone b_alpha is known | false | only clock product bound exists | false | false |
| CG1059_1_beta_source_alpha | standalone beta_source_alpha is known | false | only WEP product target exists and source owner is not derived | false | false |
| CG1059_2_WEP | WEP alpha branch passes | false | no MTS product prediction below 4.797780522732e-05 is sourced | false | false |
| CG1059_3_R10 | R10 alpha(lambda) branch passes | false | finite branch inputs and promoted bound curve are missing | false | false |
| CG1059_4_cross_arena | clock/WEP/R10 products can be transferred | false | shared parent normalization map is missing | false | false |


## Validation
| check_id | result | detail | generated_utc |
| --- | --- | --- | --- |
| V1059_SUMMARY | pass | 1059 alpha counterterm product-prior source pack validation summary | 2026-06-14T09:46:16.654520+00:00 |
| V1059_1_sources_exist_and_needles | pass | every cited source path exists and every source needle was found | 2026-06-14T09:46:14.896494+00:00 |
| V1059_2_product_pack_contains_clock_and_WEP | pass | clock and WEP product rows are present | 2026-06-14T09:46:14.896510+00:00 |
| V1059_3_R10_schema_blocked | pass | R10 product row is schema-only and blocked | 2026-06-14T09:46:14.896516+00:00 |
| V1059_4_transfer_gates_blocked | pass | all cross-arena transfer gates are blocked | 2026-06-14T09:46:14.896521+00:00 |
| V1059_5_projection_debts_present | pass | tau/source/KX projection debts are explicit | 2026-06-14T09:46:14.896526+00:00 |
| V1059_6_product_score_rules_nonclaim | pass | product-only score rules block standalone claims | 2026-06-14T09:46:14.896530+00:00 |
| V1059_7_mts_template_schema_nonclaim | pass | MTS template has runner schema and no claim-valid rows | 2026-06-14T09:46:14.896539+00:00 |
| V1059_8_runner_smoke_refuses_claim | pass | existing R10 runner refuses the 1059 placeholder rows | 2026-06-14T09:46:14.896542+00:00 |
| V1059_9_claim_gates_blocked | pass | all standalone/WEP/R10/cross-arena claim gates remain blocked | 2026-06-14T09:46:14.896547+00:00 |
| V1059_10_next_target_written | pass | next target row is present | 2026-06-14T09:46:14.896551+00:00 |
| V1059_11_generated_files_in_post_checkpoint | pass | all generated files are under post-checkpoint-work | 2026-06-14T09:46:14.900898+00:00 |
| V1059_12_formalization_untouched | pass | formalization-workbench modified-file count since script start is 0 | 2026-06-14T09:46:16.654500+00:00 |


## Next target
| next_target | objective | include | exclude | valid_for_claim |
| --- | --- | --- | --- | --- |
| 1060-Y5-R10-alpha-product-prediction-stub-runner-and-required-inputs.md | build the first product-prediction runner schema for the retained alpha counterterm branch, listing exactly which numeric MTS inputs would be needed to compare clock, WEP, and R10 products without claiming a pass | product prediction CSV schema, required tau/source/KX inputs, strict missing-input failure modes, product-only comparison rows, runner refusal smoke | standalone b_alpha claim, guessed tau values, unity shortcuts, cancellation, public local-GR/R10/WEP/clock claim, GitHub action, formalization-workbench edits | false |

