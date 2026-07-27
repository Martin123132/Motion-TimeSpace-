# 1060 Y5 R10 alpha product prediction stub runner and required inputs

**Progress:** the retained alpha branch now has a product-prediction runner schema. The runner has prediction rows, bound rows, validations, comparison output, and strict refusal modes.

**Current verdict:** the runner correctly refuses all current MTS predictions because every prediction row still has missing tau/source/KX inputs. This is exactly the desired behaviour.

**Next move:** fill the first WEP alpha product input set: `beta_source_alpha`, `tau_WEP`, and the material convention for `P_WEP_alpha`, or prove why it cannot be filled.

## Source register
| source_id | source_path | exists | needle_found | role |
| --- | --- | --- | --- | --- |
| SRC1060_0_1059_next | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1059_NEXT_TARGET.csv | true | true | 1059 handoff. |
| SRC1060_1_1059_pack | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1059_ALPHA_PRODUCT_PRIOR_PACK.csv | true | true | alpha product-prior pack. |
| SRC1060_2_1059_transfer | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1059_NO_TRANSFER_GATES.csv | true | true | no-transfer gates. |
| SRC1060_3_1059_debt | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1059_PROJECTION_DEBT_LEDGER.csv | true | true | projection debt ledger. |
| SRC1060_4_1059_rules | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1059_PRODUCT_ONLY_SCORE_RULES.csv | true | true | product-only score rules. |
| SRC1060_5_1052_clock | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1052_ALPHA_CLOCK_PRODUCT_BOUND_LEDGER.csv | true | true | clock product bound source. |
| SRC1060_6_1052_WEP | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1052_ALPHA_WEP_PROJECTION_LEDGER.csv | true | true | WEP product target source. |
| SRC1060_7_1052_R10 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1052_ALPHA_R10_PROJECTION_LEDGER.csv | true | true | R10 finite branch schema. |
| SRC1060_8_1053_tau | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1053_TAU_WEP_R10_PROJECTION_AUDIT.csv | true | true | tau projection debt. |
| SRC1060_9_1053_KX | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1053_KX_ZX_PLACEHOLDER_LEDGER.csv | true | true | KX/ZX/lambda debt. |
| SRC1060_10_R10_bound_candidate | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv | true | true | R10 review-candidate curve. |
| SRC1060_11_R10_runner | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\scripts\R10_alpha_lambda_bound_prediction_runner.py | true | true | existing R10 runner. |


## Product prediction schema
| column | definition | required | valid_for_claim |
| --- | --- | --- | --- |
| prediction_id | stable row id | true | false |
| arena | clock, MICROSCOPE_WEP, R10_short_range, or cross_arena | true | false |
| product_symbol | exact product being predicted; runner may not algebraically split it | true | false |
| product_value | numeric predicted product value only; no placeholders or derived-by-division values | true | false |
| product_units | yr^-1, dimensionless, or dimensionless alpha(lambda) convention | true | false |
| product_source | local source path for the prediction derivation | true | false |
| inputs_present | semicolon-separated concrete input names that are numeric/sourced | true | false |
| required_inputs | semicolon-separated input names required for this product | true | false |
| derivation_status | DERIVED_NUMERIC, SYMBOLIC_ONLY, or MISSING_* status | true | false |
| valid_for_claim | true only after all required inputs, numeric values, and source paths are real | true | false |
| notes | nonclaim caveats | true | false |


## Required inputs
| input_id | arena | product_symbol | required_numeric_inputs | currently_available | missing_status | blocks |
| --- | --- | --- | --- | --- | --- | --- |
| REQ1060_0_clock_product | clock | P_clock_alpha | b_alpha_counterterm;tau_clock_time OR directly derived P_clock_alpha | source-backed bound only, no MTS product prediction | MISSING_MTS_PRODUCT_PREDICTION | clock product comparison as MTS prediction |
| REQ1060_1_WEP_alpha | MICROSCOPE_WEP | P_WEP_alpha | beta_source_alpha;b_alpha_counterterm;tau_WEP OR directly derived P_WEP_alpha | source-backed product target only | MISSING_BETA_SOURCE_ALPHA_AND_TAU_WEP | WEP alpha product prediction |
| REQ1060_2_WEP_surface | MICROSCOPE_WEP | P_WEP_surface | beta_source_or_binding;b_A;tau_WEP OR directly derived P_WEP_surface | source-backed robust target only | MISSING_BINDING_OWNER_AND_TAU_WEP | robust WEP product prediction |
| REQ1060_3_R10_alpha | R10_short_range | P_R10_alpha(lambda) | lambda_X;Z_X;K_X^R10(lambda);beta_s(lambda);beta_t(lambda);tau_R10;epsilon_tail;promoted alpha_bound(lambda) | schema plus review-candidate nonclaim bound curve | MISSING_R10_FINITE_BRANCH_INPUTS | R10 alpha(lambda) product comparison |


## Prediction template
| prediction_id | arena | product_symbol | product_value | product_units | required_inputs | derivation_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| PRED1060_0_clock_alpha_template | clock | P_clock_alpha | MISSING_DERIVED_P_CLOCK_ALPHA | yr^-1 | b_alpha_counterterm;tau_clock_time OR directly derived P_clock_alpha | MISSING_MTS_PRODUCT_PREDICTION | false |
| PRED1060_1_WEP_alpha_template | MICROSCOPE_WEP | P_WEP_alpha | MISSING_BETA_SOURCE_ALPHA_B_ALPHA_TAU_WEP_PRODUCT | dimensionless | beta_source_alpha;b_alpha_counterterm;tau_WEP OR directly derived P_WEP_alpha | MISSING_BETA_SOURCE_ALPHA_AND_TAU_WEP | false |
| PRED1060_2_R10_alpha_template | R10_short_range | P_R10_alpha(lambda) | MISSING_KX_BETA_SOURCE_BETA_TEST_TAU_R10_PRODUCT | dimensionless | lambda_X;Z_X;K_X^R10(lambda);beta_s(lambda);beta_t(lambda);tau_R10;epsilon_tail | MISSING_R10_FINITE_BRANCH_INPUTS | false |


## Bound import
| bound_id | arena | product_symbol | bound_value | bound_units | bound_type | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| BOUND1060_0_clock_YbE3E2 | clock | P_clock_alpha | 2.1e-18 | yr^-1 | upper_abs_1sigma_product_bound | false |
| BOUND1060_1_WEP_alpha | MICROSCOPE_WEP | P_WEP_alpha | 4.797780522732e-05 | dimensionless | required_abs_product_max_smoke_convention | false |
| BOUND1060_2_WEP_surface | MICROSCOPE_WEP | P_WEP_surface | 2.887280314062e-05 | dimensionless | required_abs_product_max_smoke_convention | false |
| BOUND1060_3_R10_alpha | R10_short_range | P_R10_alpha(lambda) | MISSING_PROMOTED_ALPHA_BOUND_CURVE | dimensionless | review_candidate_only | false |


## Product runner status
| runner_id | prediction_rows | bound_rows | valid_prediction_rows | valid_bound_rows | comparison_rows | claim_allowed | expected_result |
| --- | --- | --- | --- | --- | --- | --- | --- |
| APR1060_0_alpha_product_stub | 3 | 4 | 0 | 3 | 1 | false | reject placeholder predictions and keep claim false |


## Product comparison rows
| comparison_id | arena | product_symbol | product_value | bound_value | comparison_status | pass_for_claim | issues |
| --- | --- | --- | --- | --- | --- | --- | --- |
| PRODUCT_COMPARE_NO_VALID_PREDICTIONS |  |  |  |  | not_run | false | no valid MTS alpha product prediction rows |


## R10 runner smoke status
| smoke_id | valid_mts_rows | valid_bound_rows | comparison_rows | R10_pass_for_claim | claim_allowed | expected_result |
| --- | --- | --- | --- | --- | --- | --- |
| SMOKE1060_0_R10_runner_refusal | 0 | 0 | 1 | false | false | reject R10 alpha product placeholders until prediction inputs are sourced |


## Strict failure modes
| failure_id | object | expected_failure | observed_status | meaning | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| SFR1060_0_missing_product_predictions | alpha product prediction template | valid_prediction_rows=0 | valid_prediction_rows=0 | runner refuses missing tau/source/KX placeholder rows | false |
| SFR1060_1_no_standalone_claim | standalone b_alpha or beta_source_alpha | not represented as scoreable products | standalone claims absent from prediction schema | runner cannot divide by guessed tau/source factors | false |
| SFR1060_2_R10_runner | R10 alpha(lambda) smoke row | valid_mts_rows=0 | valid_mts_rows=0; valid_bound_rows=0 | existing R10 runner refuses finite-branch placeholders | false |


## Claim gates
| gate_id | claim | gate_pass | reason | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| CG1060_0_product_runner_claim | alpha product runner has scoreable MTS predictions | false | prediction template contains missing tau/source/KX inputs | false | false |
| CG1060_1_clock | clock product prediction is tested | false | source-backed clock bound exists but MTS P_clock_alpha prediction is missing | false | false |
| CG1060_2_WEP | WEP alpha product prediction is tested | false | P_WEP_alpha prediction and tau_WEP/beta_source inputs are missing | false | false |
| CG1060_3_R10 | R10 alpha(lambda) product prediction is tested | false | R10 finite branch inputs and promoted bound curve are missing | false | false |


## Decision ledger
| decision_id | decision | because | next_action | valid_for_claim |
| --- | --- | --- | --- | --- |
| DEC1060_0_runner_built | alpha product-prediction runner schema now exists | prediction rows, bound rows, validations, and comparisons are generated | fill one product prediction input set rather than claiming from bounds alone | false |
| DEC1060_1_runner_refuses | runner correctly refuses all current MTS placeholder predictions | valid prediction rows are zero and missing markers remain | source tau_WEP/beta_source_alpha first, or derive P_WEP_alpha directly | false |
| DEC1060_2_best_next | next target is the first WEP alpha product input fill | WEP has the clearest numeric product target and the missing inputs are explicitly named | 1061-Y5-R10-WEP-alpha-product-first-input-fill-tauWEP-betaSource-material-map.md | false |


## Validation
| check_id | result | detail | generated_utc |
| --- | --- | --- | --- |
| V1060_SUMMARY | pass | 1060 alpha product prediction stub-runner validation summary | 2026-06-14T09:54:17.232366+00:00 |
| V1060_1_sources_exist_and_needles | pass | every cited source path exists and every source needle was found | 2026-06-14T09:54:15.433667+00:00 |
| V1060_2_prediction_schema_written | pass | product prediction schema contains all required columns | 2026-06-14T09:54:15.433679+00:00 |
| V1060_3_required_inputs_written | pass | required tau/source/KX inputs are explicit | 2026-06-14T09:54:15.433685+00:00 |
| V1060_4_prediction_template_nonclaim | pass | prediction template rows are nonclaim placeholders | 2026-06-14T09:54:15.433689+00:00 |
| V1060_5_bound_import_contains_clock_and_WEP | pass | bound import includes clock and WEP product rows | 2026-06-14T09:54:15.433695+00:00 |
| V1060_6_product_runner_refuses_placeholders | pass | custom alpha product runner refuses missing prediction rows | 2026-06-14T09:54:15.433698+00:00 |
| V1060_7_R10_runner_refuses_placeholders | pass | existing R10 runner refuses placeholder rows | 2026-06-14T09:54:15.433706+00:00 |
| V1060_8_failure_modes_written | pass | strict failure modes are written | 2026-06-14T09:54:15.433713+00:00 |
| V1060_9_claim_gates_blocked | pass | all product test claim gates remain blocked | 2026-06-14T09:54:15.433718+00:00 |
| V1060_10_next_target_written | pass | next target row is present | 2026-06-14T09:54:15.433722+00:00 |
| V1060_11_generated_files_in_post_checkpoint | pass | all generated files are under post-checkpoint-work | 2026-06-14T09:54:15.438497+00:00 |
| V1060_12_formalization_untouched | pass | formalization-workbench modified-file count since script start is 0 | 2026-06-14T09:54:17.232347+00:00 |


## Next target
| next_target | objective | include | exclude | valid_for_claim |
| --- | --- | --- | --- | --- |
| 1061-Y5-R10-WEP-alpha-product-first-input-fill-tauWEP-betaSource-material-map.md | try to fill the first scoreable WEP alpha product prediction input set by deriving or sourcing beta_source_alpha, tau_WEP, and the material convention for P_WEP_alpha, while keeping the product target nonclaim unless all inputs are real | tau_WEP definition source, beta_source_alpha source/theorem route, material convention, product prediction row, failure if any input is missing | standalone b_alpha claim, guessed tau values, unity shortcuts, cancellation, public WEP/R10/clock/local-GR claim, GitHub action, formalization-workbench edits | false |

