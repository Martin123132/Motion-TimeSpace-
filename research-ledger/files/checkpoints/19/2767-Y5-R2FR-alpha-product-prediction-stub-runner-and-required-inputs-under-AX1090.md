# 2767 - Y5 R2/f(R): Alpha Product-Prediction Stub Runner And Required Inputs Under AX1090

## Private Verdict

The runner is now in place for the current R2/f(R) branch. It does exactly what we want: it refuses to score alpha/coupling products while `tau_clock`, `tau_WEP`, `tau_R10`, `beta_source_alpha`, `K_X/Z_X`, and direct product derivations are missing.

This is not a physics pass. It is a guardrail against accidentally winning by notation. The next real move is to try to fill the WEP alpha product input set, because that is the nearest concrete lab arena with a numerical product target.

## Source Register

| row_id | source_key | source_path | exists | needles_found | source_role | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| SRC2767_00_2766_next | 2766_next | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_2766_NEXT_TARGET.csv | True | True | 2766 handoff selecting alpha product-prediction runner | False |
| SRC2767_01_2766_pack | 2766_product_pack | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_2766_ALPHA_PRODUCT_PRIOR_PACK.csv | True | True | R2/f(R) alpha product pack | False |
| SRC2767_02_2766_transfer | 2766_transfer | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_2766_NO_TRANSFER_GATES.csv | True | True | R2/f(R) no-transfer gates | False |
| SRC2767_03_2766_debts | 2766_debts | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_2766_PROJECTION_DEBT_LEDGER.csv | True | True | R2/f(R) projection debts | False |
| SRC2767_04_1060_doc | 1060_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1060-Y5-R10-alpha-product-prediction-stub-runner-and-required-inputs.md | True | True | R10 product-runner precedent | False |
| SRC2767_05_1060_schema | 1060_schema | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1060_PRODUCT_PREDICTION_SCHEMA.csv | True | True | prior runner schema | False |
| SRC2767_06_1060_required | 1060_required | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1060_REQUIRED_INPUTS.csv | True | True | prior required input list | False |
| SRC2767_07_1060_status | 1060_status | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1060_PRODUCT_RUNNER_STATUS.csv | True | True | prior product runner refusal status | False |
| SRC2767_08_1061_doc | 1061_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1061-Y5-R10-WEP-alpha-product-first-input-fill-tauWEP-betaSource-material-map.md | True | True | next WEP input-fill precedent | False |
| SRC2767_09_r10_runner | r10_runner | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\scripts\R10_alpha_lambda_bound_prediction_runner.py | True | True | existing R10 alpha(lambda) refusal runner | False |
| SRC2767_10_r10_bound_candidate | r10_bound_candidate | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv | True | True | nonclaim R10 review-candidate bound curve | False |

## Product Prediction Schema

| column | definition | required | valid_for_claim |
| --- | --- | --- | --- |
| prediction_id | stable row id | True | False |
| arena | clock, MICROSCOPE_WEP, R10_short_range, or cross_arena | True | False |
| product_symbol | exact product being predicted; runner may not algebraically split it | True | False |
| product_value | numeric predicted product value only; no placeholders or derived-by-division values | True | False |
| product_units | yr^-1, dimensionless, or dimensionless alpha(lambda) convention | True | False |
| product_source | local source path for the prediction derivation | True | False |
| inputs_present | semicolon-separated concrete input names that are numeric/sourced | True | False |
| required_inputs | semicolon-separated input names required for this product | True | False |
| derivation_status | DERIVED_NUMERIC, SYMBOLIC_ONLY, or MISSING_* status | True | False |
| comparison_allowed | true only for rows with numeric product_value, source path, and all required inputs | True | False |
| valid_for_claim | true only after all required inputs, numeric values, and source paths are real | True | False |
| notes | nonclaim caveats and refusal reasons | True | False |

## Required Inputs

| row_id | arena | product_symbol | required_numeric_inputs | currently_available | missing_status | blocks | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| REQ2767_0_clock_product | clock | P_clock_alpha | b_alpha_counterterm;tau_clock_time OR directly derived P_clock_alpha | source-backed bound only, no MTS product prediction | MISSING_MTS_PRODUCT_PREDICTION | clock product comparison as MTS prediction | False |
| REQ2767_1_WEP_alpha | MICROSCOPE_WEP | P_WEP_alpha | beta_source_alpha;b_alpha_counterterm;tau_WEP OR directly derived P_WEP_alpha | source-backed smoke target only | MISSING_BETA_SOURCE_ALPHA_B_ALPHA_TAU_WEP_PRODUCT | WEP alpha product prediction | False |
| REQ2767_2_WEP_surface | MICROSCOPE_WEP | P_WEP_surface | beta_source_or_binding;b_A;tau_WEP OR directly derived P_WEP_surface | source-backed robust target only | MISSING_BINDING_OWNER_AND_TAU_WEP | robust WEP product prediction | False |
| REQ2767_3_R10_alpha | R10_short_range | P_R10_alpha(lambda) | lambda_X;Z_X;K_X^R10(lambda);beta_s(lambda);beta_t(lambda);tau_R10;epsilon_tail;promoted alpha_bound(lambda) | schema plus review-candidate nonclaim bound curve | MISSING_R10_FINITE_BRANCH_INPUTS | R10 alpha(lambda) product comparison | False |
| REQ2767_4_operator_domain | cross_arena | alpha theorem-zero branch | derived visible operator-domain exhaustion OR retained finite product predictions | exact contract, not theorem | MISSING_VISIBLE_OPERATOR_UNIVERSAL_PROPERTY | standalone zero claim | False |

## Prediction Template

| prediction_id | arena | product_symbol | product_value | product_units | required_inputs | derivation_status | comparison_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PRED2767_0_clock_alpha_template | clock | P_clock_alpha | MISSING_DERIVED_P_CLOCK_ALPHA | yr^-1 | b_alpha_counterterm;tau_clock_time OR directly derived P_clock_alpha | MISSING_MTS_PRODUCT_PREDICTION | False | False |
| PRED2767_1_WEP_alpha_template | MICROSCOPE_WEP | P_WEP_alpha | MISSING_BETA_SOURCE_ALPHA_B_ALPHA_TAU_WEP_PRODUCT | dimensionless | beta_source_alpha;b_alpha_counterterm;tau_WEP OR directly derived P_WEP_alpha | MISSING_BETA_SOURCE_ALPHA_B_ALPHA_TAU_WEP_PRODUCT | False | False |
| PRED2767_2_WEP_surface_template | MICROSCOPE_WEP | P_WEP_surface | MISSING_BINDING_SOURCE_BA_TAU_WEP_PRODUCT | dimensionless | beta_source_or_binding;b_A;tau_WEP OR directly derived P_WEP_surface | MISSING_BINDING_OWNER_AND_TAU_WEP | False | False |
| PRED2767_3_R10_alpha_template | R10_short_range | P_R10_alpha(lambda) | MISSING_KX_BETA_SOURCE_BETA_TEST_TAU_R10_PRODUCT | dimensionless | lambda_X;Z_X;K_X^R10(lambda);beta_s(lambda);beta_t(lambda);tau_R10;epsilon_tail | MISSING_R10_FINITE_BRANCH_INPUTS | False | False |

## Bound Import

| bound_id | arena | product_symbol | bound_value | bound_units | bound_type | source_row | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BOUND2767_0_clock_YbE3E2 | clock | P_clock_alpha | 2.1e-18 | yr^-1 | upper_abs_1sigma_product_bound | APP2766_0_clock_YbE3E2 | False |
| BOUND2767_1_clock_AlHg | clock | P_clock_alpha | 3.9e-17 | yr^-1 | weaker_upper_abs_1sigma_product_bound | APP2766_1_clock_AlHg | False |
| BOUND2767_2_WEP_alpha | MICROSCOPE_WEP | P_WEP_alpha | 4.797780522732e-05 | dimensionless | required_abs_product_max_smoke_convention | APP2766_2_WEP_alpha_Coulomb | False |
| BOUND2767_3_WEP_surface | MICROSCOPE_WEP | P_WEP_surface | 2.887280314062e-05 | dimensionless | required_abs_product_max_smoke_convention | APP2766_3_WEP_surface_binding | False |
| BOUND2767_4_R10_alpha | R10_short_range | P_R10_alpha(lambda) | MISSING_PROMOTED_ALPHA_BOUND_CURVE | dimensionless | review_candidate_only | APP2766_4_R10_finite_alpha | False |

## Product Runner Status

| runner_id | prediction_rows | bound_rows | valid_prediction_rows | valid_bound_rows | comparison_rows | claim_allowed | expected_result | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| APR2767_0_alpha_product_stub | 4 | 5 | 0 | 4 | 1 | False | reject placeholder predictions and keep claim false | False |

## Product Comparison Rows

| comparison_id | arena | product_symbol | product_value | bound_value | comparison_status | pass_for_claim | issues | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PRODUCT_COMPARE_NO_VALID_PREDICTIONS |  |  |  |  | not_run | False | no valid MTS alpha product prediction rows | False |

## R10 Runner Smoke Status

| smoke_id | valid_mts_rows | valid_bound_rows | comparison_rows | R10_pass_for_claim | claim_allowed | expected_result | output_dir | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SMOKE2767_0_R10_runner_refusal | 0 | 0 | 1 | False | False | reject R10 alpha product placeholders until prediction inputs are sourced | source-intake/mts_residuals/R10_runner_2767_alpha_product_refusal | False |

## Strict Failure Modes

| row_id | object | expected_failure | observed_status | meaning | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| SFR2767_0_missing_product_predictions | alpha product prediction template | valid_prediction_rows=0 | valid_prediction_rows=0 | runner refuses missing tau/source/KX placeholder rows | False |
| SFR2767_1_no_standalone_claim | standalone b_alpha or beta_source_alpha | not represented as scoreable products | standalone claims absent from prediction schema | runner cannot divide by guessed tau/source factors | False |
| SFR2767_2_no_unity_shortcuts | tau_clock;tau_WEP;tau_R10;beta_source_alpha | no variable set to 1 by convention | all unity shortcuts absent | coupling must come from theory or stay nonclaim | False |
| SFR2767_3_R10_runner | R10 alpha(lambda) smoke row | valid_mts_rows=0 | valid_mts_rows=0; valid_bound_rows=0 | existing R10 runner refuses finite-branch placeholders | False |

## Claim Gates

| row_id | claim | gate_pass | reason | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| CG2767_0_product_runner_claim | alpha product runner has scoreable MTS predictions | False | prediction template contains missing tau/source/KX inputs | False | False |
| CG2767_1_clock | clock product prediction is tested | False | source-backed clock bound exists but MTS P_clock_alpha prediction is missing | False | False |
| CG2767_2_WEP | WEP alpha product prediction is tested | False | P_WEP_alpha prediction and tau_WEP/beta_source/b_alpha product are missing | False | False |
| CG2767_3_R10 | R10 alpha(lambda) product prediction is tested | False | R10 finite branch inputs and promoted bound curve are missing | False | False |
| CG2767_4_local_GR | local GR/Newton follows from alpha product runner | False | runner is a refusal guardrail, not a derivation of the local constant sector | False | False |

## Decision Ledger

| row_id | decision | because | next_action | valid_for_claim |
| --- | --- | --- | --- | --- |
| DEC2767_0_runner_built | alpha product-prediction runner schema now exists in the current R2/f(R) branch | 2766 retained the alpha counterterm/product-prior branch and forbade transfer shortcuts | fill one product prediction input set rather than claiming from bounds alone | False |
| DEC2767_1_runner_refuses | runner correctly refuses all current MTS placeholder predictions | valid prediction rows are zero and missing markers remain | derive or source tau_WEP/beta_source_alpha/b_alpha product first | False |
| DEC2767_2_best_next | next target is the first WEP alpha product input fill in the R2/f(R) branch | WEP has the clearest numeric product target and the missing inputs are explicitly named | 2768-Y5-R2FR-WEP-alpha-product-first-input-fill-tauWEP-betaSource-material-map-under-AX1090.md | False |

## Next Target

| row_id | next_target | script | why | include | exclude | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| NEXT2767_0_2768 | 2768-Y5-R2FR-WEP-alpha-product-first-input-fill-tauWEP-betaSource-material-map-under-AX1090.md | scripts/Y5_R2FR_WEP_alpha_product_first_input_fill_tauWEP_betaSource_material_map_under_AX1090_2768.py | the runner now blocks all placeholder alpha products; the least handwavy next step is to fill or reject the WEP product inputs beta_source_alpha, b_alpha/tau product, tau_WEP, and material convention in one parent/source map | tau_WEP definition source, beta_source_alpha owner route, WEP material convention, direct P_WEP_alpha theorem route, strict failure if any input is missing | standalone b_alpha claim, guessed tau values, beta_source_alpha=1, tau_WEP=1, cancellation, public WEP/R10/clock/local-GR claim, GitHub, formalization-workbench edits | False |

## Branch Copies

| copy_id | table_key | source_table | copy_path | purpose | exists | row_count | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BR2767_0_runner_queue | runner | source-intake\mts_residuals\P8_Y5_R2FR_2767_PRODUCT_RUNNER_STATUS.csv | source-intake\rab-sector\acquisition-queue\JR2767_ALPHA_PRODUCT_PREDICTION_RUNNER_NONCLAIM.csv | alpha product-prediction refusal runner | True | 15 | False |
| BR2767_1_required_queue | required | source-intake\mts_residuals\P8_Y5_R2FR_2767_REQUIRED_INPUTS.csv | source-intake\rab-sector\acquisition-queue\JR2767_ALPHA_PRODUCT_REQUIRED_INPUTS.csv | required tau/source/KX input list | True | 5 | False |
| BR2767_2_beta_doc | beta_doc | source-intake\mts_residuals\P8_Y5_R2FR_2767_REQUIRED_INPUTS.csv | source-intake\beta-source\docs\ALPHA_PRODUCT_PREDICTION_RUNNER_2767_NONCLAIM.csv | beta/source-facing required-input copy | True | 14 | False |
| BR2767_3_microscope_copy | microscope | source-intake\mts_residuals\P8_Y5_R2FR_2767_ALPHA_PRODUCT_PREDICTION_TEMPLATE_NONCLAIM.csv | source-intake\microscope\branch_locked_wep\residuals\alpha_product_prediction_runner_2767_nonclaim.csv | MICROSCOPE WEP product runner copy | True | 11 | False |
| BR2767_4_next_queue | next | source-intake\mts_residuals\P8_Y5_R2FR_2767_NEXT_TARGET.csv | source-intake\rab-sector\acquisition-queue\JR2767_WEP_ALPHA_PRODUCT_INPUT_FILL_NEXT.csv | next WEP alpha input-fill target | True | 1 | False |

## Validation

| validation_id | passed | detail | timestamp_utc |
| --- | --- | --- | --- |
| VAL2767_0_sources | True | every cited source path exists and needles are found | 2026-06-23T16:32:03.040285+00:00 |
| VAL2767_1_prediction_schema_written | True | product prediction schema contains all required columns | 2026-06-23T16:32:03.040317+00:00 |
| VAL2767_2_required_inputs_written | True | required tau/source/KX inputs are explicit | 2026-06-23T16:32:03.040327+00:00 |
| VAL2767_3_prediction_template_nonclaim | True | prediction template rows are nonclaim placeholders | 2026-06-23T16:32:03.040334+00:00 |
| VAL2767_4_bound_import_contains_clock_WEP | True | bound import includes clock and WEP product rows | 2026-06-23T16:32:03.040342+00:00 |
| VAL2767_5_product_runner_refuses_placeholders | True | custom alpha product runner refuses missing prediction rows | 2026-06-23T16:32:03.040350+00:00 |
| VAL2767_6_R10_runner_refuses_placeholders | True | existing R10 runner refuses placeholder rows | 2026-06-23T16:32:03.040358+00:00 |
| VAL2767_7_failure_modes_written | True | strict failure modes are written | 2026-06-23T16:32:03.040366+00:00 |
| VAL2767_8_claim_gates_blocked | True | all product test claim gates remain blocked | 2026-06-23T16:32:03.040373+00:00 |
| VAL2767_9_next_target_written | True | next target row is present | 2026-06-23T16:32:03.040382+00:00 |
| VAL2767_10_branch_outputs | True | branch copies exist and contain rows | 2026-06-23T16:32:03.040389+00:00 |
| VAL2767_11_csv_parse | True | all generated CSV outputs parse cleanly | 2026-06-23T16:32:03.040397+00:00 |
| VAL2767_12_no_claim_flags | True | no generated row is valid_for_claim=true/claim_allowed=true/allowed=true/pass_for_claim=true | 2026-06-23T16:32:03.040405+00:00 |
| VAL2767_13_generated_under_post_checkpoint | True | all generated outputs are under post-checkpoint-work | 2026-06-23T16:32:03.040412+00:00 |
| VAL2767_14_formalization_untouched | True | formalization-workbench modified-file count remains zero during this run | 2026-06-23T16:32:03.040419+00:00 |
| VAL2767_15_pycache_absent | True | scripts __pycache__ removed | 2026-06-23T16:32:03.040426+00:00 |
| VAL2767_OVERALL | True | 2767 builds the current R2/f(R) alpha product-prediction refusal runner, imports clock/WEP/R10 product bounds, confirms all MTS prediction rows are placeholders with missing tau/source/KX inputs, verifies the R10 runner also refuses the placeholder alpha(lambda) curve, keeps all claim gates blocked, and selects WEP alpha product input fill as the next target. | 2026-06-23T16:32:03.040447+00:00 |

## Plain-English Read

This checkpoint is the referee. If the theory cannot produce the coupling product, the code now says no. That is good discipline: before we try to beat GR/DM/MOND in a lab arena, we first force MTS to speak in the exact product the lab actually constrains.

