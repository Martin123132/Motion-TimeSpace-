# 2564 Y5 R2FR GK Stress-bound Dry-run And Baseline Control Runner

**Status:** dry-run runner works and blocks claims. Toy rows compute where allowed, but every row remains nonclaim because at least one of parent coefficients, arena kernels, bound data, real source paths, units or matched baseline controls is missing.

**Meaning:** the local stress-bound branch now has an executable harness with the fair-comparison rule baked in. If GR/Newton control rows are absent or broken, MTS rows cannot be interpreted; if toy MTS rows compute, they still cannot become evidence without real sourced inputs.

## Source Register
| source_id | source_path | exists | missing_needles | source_pass | role |
| --- | --- | --- | --- | --- | --- |
| SRC2564_00_2563_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2563-Y5-R2FR-GK-stress-bound-local-arena-projection-runner.md | True |  | True | handoff selecting dry-run plus matched-baseline control runner |
| SRC2564_01_2563_schema | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_NO_SHADOW_2563_NONCLAIM_RUNNER_SCHEMA.csv | True |  | True | runner schema requiring baseline status and claim blocking |
| SRC2564_02_2563_arenas | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_NO_SHADOW_2563_ARENA_PROJECTION_ROWS.csv | True |  | True | local arena projection schema |
| SRC2564_03_2563_baseline_guardrails | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_NO_SHADOW_2563_BASELINE_COMPARISON_GUARDRAILS.csv | True |  | True | matched-baseline and anti-circularity guardrails |
| SRC2564_04_2563_missing_inputs | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_NO_SHADOW_2563_MISSING_INPUTS_LEDGER.csv | True |  | True | missing parent, kernel, bound-data and baseline inputs |
| SRC2564_05_2474_precedent | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2474-Y5-R2FR-GK-stress-bound-runner-dry-run-and-placeholder-rejection.md | True |  | True | earlier placeholder rejection runner pattern upgraded with baseline controls |

## Dry-run Inputs
| input_id | arena_id | arena | E_GK_bound | C_metric | K_arena | extra_leak | arena_bound | units | source_path | baseline_model | baseline_residual | baseline_pipeline_status | baseline_data_convention | valid_for_claim | parent_coefficients_sourced | arena_kernel_sourced | bound_data_sourced | forbidden_marker | input_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DRY2564_0_R10_missing | ARENA2563_R10 | R10_short_range |  |  |  |  |  | alpha_bound |  | Newton_GR_control | 0.0 | PASS | same_alpha_lambda_parser | false | false | false | false | none | MISSING_COEFFICIENTS_AND_BOUND_DATA |
| DRY2564_1_PPN_toy_nonclaim | ARENA2563_PPN | PPN_solar_system | 1.0e-12 | 2.0 | 3.0 | 0.0 | 1.0e-10 | dimensionless | toy_internal | GR_PPN_zero_residual_control | 0.0 | PASS | same_ppn_vector_convention | false | false | false | false | none | TOY_NUMERIC_NONCLAIM |
| DRY2564_2_CLOCK_bad_units | ARENA2563_CLOCK | clock_redshift_time | 1.0e-12 | 1.0 | 1.0 | 1.0e-16 | 1.0e-15 | banana_units | toy_internal | GR_clock_redshift_control | 0.0 | PASS | same_clock_frequency_units | false | false | false | false | none | BAD_UNITS |
| DRY2564_3_ORBITAL_fitted_GM | ARENA2563_ORBITAL | orbital_dynamics | 1.0e-13 | 1.0 | 1.0 | 0.0 | 1.0e-12 | dimensionless | toy_internal | GR_orbital_control | 0.0 | PASS | same_source_mass_policy | false | false | false | false | uses_fitted_GM | FITTED_GM_FORBIDDEN |
| DRY2564_4_WEP_missing_baseline | ARENA2563_WEP | WEP_composition | 2.0e-15 | 4.0 | 5.0 | 0.0 | 1.0e-12 | dimensionless | toy_internal |  |  | MISSING |  | false | false | false | false | none | MISSING_BASELINE_CONTROL |
| DRY2564_5_LIGHT_future_shape_missing_parent | ARENA2563_LIGHT | light_deflection_delay | 5.0e-14 | 1.5 | 2.0 | 0.0 | 1.0e-10 | dimensionless | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2563-Y5-R2FR-GK-stress-bound-local-arena-projection-runner.md | GR_null_geodesic_control | 0.0 | PASS | same_null_readout_kernel | true | false | false | false | none | FUTURE_SHAPE_BUT_PARENT_MISSING |

## Dry-run Results
| input_id | arena_id | arena | residual_predicted | baseline_residual | delta_vs_baseline | ratio_to_bound | result_status | block_reasons | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DRY2564_0_R10_missing | ARENA2563_R10 | R10_short_range |  | 0.0 |  |  | CLAIM_BLOCKED | MISSING_OR_INVALID_NUMERIC_INPUT;VALID_FOR_CLAIM_FALSE;MISSING_REAL_SOURCE_PATH;MISSING_PARENT_COEFFICIENTS;MISSING_ARENA_KERNEL;MISSING_BOUND_DATA | False |
| DRY2564_1_PPN_toy_nonclaim | ARENA2563_PPN | PPN_solar_system | 6.000000e-12 | 0.0 | 6.000000e-12 | 6.000000e-02 | COMPUTED_TOY_NONCLAIM | VALID_FOR_CLAIM_FALSE;MISSING_REAL_SOURCE_PATH;MISSING_PARENT_COEFFICIENTS;MISSING_ARENA_KERNEL;MISSING_BOUND_DATA | False |
| DRY2564_2_CLOCK_bad_units | ARENA2563_CLOCK | clock_redshift_time |  | 0.0 |  |  | CLAIM_BLOCKED | BAD_UNITS;VALID_FOR_CLAIM_FALSE;MISSING_REAL_SOURCE_PATH;MISSING_PARENT_COEFFICIENTS;MISSING_ARENA_KERNEL;MISSING_BOUND_DATA | False |
| DRY2564_3_ORBITAL_fitted_GM | ARENA2563_ORBITAL | orbital_dynamics | 1.000000e-13 | 0.0 | 1.000000e-13 | 1.000000e-01 | COMPUTED_TOY_NONCLAIM | VALID_FOR_CLAIM_FALSE;MISSING_REAL_SOURCE_PATH;MISSING_PARENT_COEFFICIENTS;MISSING_ARENA_KERNEL;MISSING_BOUND_DATA;FITTED_GM_FORBIDDEN | False |
| DRY2564_4_WEP_missing_baseline | ARENA2563_WEP | WEP_composition | 4.000000e-14 |  |  | 4.000000e-02 | COMPUTED_TOY_NONCLAIM | VALID_FOR_CLAIM_FALSE;MISSING_REAL_SOURCE_PATH;MISSING_PARENT_COEFFICIENTS;MISSING_ARENA_KERNEL;MISSING_BOUND_DATA;BASELINE_NOT_PASS;MISSING_BASELINE_MODEL;MISSING_BASELINE_CONVENTION;MISSING_OR_INVALID_BASELINE_RESIDUAL | False |
| DRY2564_5_LIGHT_future_shape_missing_parent | ARENA2563_LIGHT | light_deflection_delay | 1.500000e-13 | 0.0 | 1.500000e-13 | 1.500000e-03 | FUTURE_SHAPE_BLOCKED | MISSING_PARENT_COEFFICIENTS;MISSING_ARENA_KERNEL;MISSING_BOUND_DATA | False |

## Baseline Control Ledger
| input_id | arena | baseline_model | baseline_pipeline_status | baseline_data_convention | baseline_residual | baseline_control_status | baseline_reasons | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DRY2564_0_R10_missing | R10_short_range | Newton_GR_control | PASS | same_alpha_lambda_parser | 0.0 | PASS_CONTROL |  | False |
| DRY2564_1_PPN_toy_nonclaim | PPN_solar_system | GR_PPN_zero_residual_control | PASS | same_ppn_vector_convention | 0.0 | PASS_CONTROL |  | False |
| DRY2564_2_CLOCK_bad_units | clock_redshift_time | GR_clock_redshift_control | PASS | same_clock_frequency_units | 0.0 | PASS_CONTROL |  | False |
| DRY2564_3_ORBITAL_fitted_GM | orbital_dynamics | GR_orbital_control | PASS | same_source_mass_policy | 0.0 | PASS_CONTROL |  | False |
| DRY2564_4_WEP_missing_baseline | WEP_composition |  | MISSING |  |  | BLOCKED_CONTROL | BASELINE_NOT_PASS;MISSING_BASELINE_MODEL;MISSING_BASELINE_CONVENTION;MISSING_OR_INVALID_BASELINE_RESIDUAL | False |
| DRY2564_5_LIGHT_future_shape_missing_parent | light_deflection_delay | GR_null_geodesic_control | PASS | same_null_readout_kernel | 0.0 | PASS_CONTROL |  | False |

## Rejection Ledger
| input_id | arena | rejection_reasons | claim_allowed |
| --- | --- | --- | --- |
| DRY2564_0_R10_missing | R10_short_range | MISSING_OR_INVALID_NUMERIC_INPUT;VALID_FOR_CLAIM_FALSE;MISSING_REAL_SOURCE_PATH;MISSING_PARENT_COEFFICIENTS;MISSING_ARENA_KERNEL;MISSING_BOUND_DATA | False |
| DRY2564_1_PPN_toy_nonclaim | PPN_solar_system | VALID_FOR_CLAIM_FALSE;MISSING_REAL_SOURCE_PATH;MISSING_PARENT_COEFFICIENTS;MISSING_ARENA_KERNEL;MISSING_BOUND_DATA | False |
| DRY2564_2_CLOCK_bad_units | clock_redshift_time | BAD_UNITS;VALID_FOR_CLAIM_FALSE;MISSING_REAL_SOURCE_PATH;MISSING_PARENT_COEFFICIENTS;MISSING_ARENA_KERNEL;MISSING_BOUND_DATA | False |
| DRY2564_3_ORBITAL_fitted_GM | orbital_dynamics | VALID_FOR_CLAIM_FALSE;MISSING_REAL_SOURCE_PATH;MISSING_PARENT_COEFFICIENTS;MISSING_ARENA_KERNEL;MISSING_BOUND_DATA;FITTED_GM_FORBIDDEN | False |
| DRY2564_4_WEP_missing_baseline | WEP_composition | VALID_FOR_CLAIM_FALSE;MISSING_REAL_SOURCE_PATH;MISSING_PARENT_COEFFICIENTS;MISSING_ARENA_KERNEL;MISSING_BOUND_DATA;BASELINE_NOT_PASS;MISSING_BASELINE_MODEL;MISSING_BASELINE_CONVENTION;MISSING_OR_INVALID_BASELINE_RESIDUAL | False |
| DRY2564_5_LIGHT_future_shape_missing_parent | light_deflection_delay | MISSING_PARENT_COEFFICIENTS;MISSING_ARENA_KERNEL;MISSING_BOUND_DATA | False |

## Toy Arithmetic Smoke
| input_id | arena | calculation | numeric_result | baseline_delta | toy_only | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- |
| DRY2564_1_PPN_toy_nonclaim | PPN_solar_system | residual_predicted=E_GK_bound*C_metric*K_arena+extra_leak | 6.000000e-12 | 6.000000e-12 | True | False |
| DRY2564_3_ORBITAL_fitted_GM | orbital_dynamics | residual_predicted=E_GK_bound*C_metric*K_arena+extra_leak | 1.000000e-13 | 1.000000e-13 | True | False |
| DRY2564_4_WEP_missing_baseline | WEP_composition | residual_predicted=E_GK_bound*C_metric*K_arena+extra_leak | 4.000000e-14 |  | True | False |
| DRY2564_5_LIGHT_future_shape_missing_parent | light_deflection_delay | residual_predicted=E_GK_bound*C_metric*K_arena+extra_leak | 1.500000e-13 | 1.500000e-13 | True | False |

## Claim Gates
| gate_id | claim | gate_status | reason | gate_pass | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| GATE2564_0_dry_run | Dry-run calculator executes. | PASS | result rows written | True | False |
| GATE2564_1_baseline_controls | Matched baseline controls are evaluated. | PASS | baseline control ledger written | True | False |
| GATE2564_2_placeholder_rejection | Placeholder/missing rows are rejected. | PASS | 6 rejection rows written | True | False |
| GATE2564_3_bad_units | Bad units are rejected. | PASS | clock bad-unit row blocks | True | False |
| GATE2564_4_fitted_GM | Fitted-GM contamination is rejected. | PASS | orbital fitted-GM row blocks | True | False |
| GATE2564_5_missing_baseline | Missing baseline control blocks interpretation. | PASS | WEP missing-baseline row blocks | True | False |
| GATE2564_6_future_shape | A valid-looking sourced row with missing parent coefficients remains blocked. | PASS | light row blocks on parent/kernel/bound inputs | True | False |
| GATE2564_7_claim_rows | Any current row can support a local-test claim. | BLOCKED | all rows have claim_allowed=false and rejection reasons | False | False |
| GATE2564_8_local_GR | local GR/PPN branch is derived. | BLOCKED | dry-run compatibility plumbing cannot replace parent no-hair proof | False | False |
| GATE2564_9_no_GitHub | No public/GitHub update. | PASS_GUARDRAIL | private dry-run only | True | False |

## Decision Ledger
| decision_id | decision | reason | effect |
| --- | --- | --- | --- |
| DEC2564_0_runner_works | Keep the dry-run runner pattern. | it computes toy rows and rejects all placeholder claim routes | safe to receive real rows later |
| DEC2564_1_baseline_required | Keep matched GR/Newton controls as mandatory. | without controls, pipeline failure can masquerade as theory failure | fair-comparison discipline |
| DEC2564_2_no_claim | No local compatibility or local-GR claim. | parent coefficients, kernels, bounds and real sources remain missing | claim discipline retained |
| DEC2564_3_next | Acquire first real local bound/source row with baseline metadata, then separately reopen parent-coefficient derivation. | the harness is ready but has no real inputs | 2565 selected |

## Next Target
| route_id | selection_status | target_file | target_script | task | acceptance_target | guardrails |
| --- | --- | --- | --- | --- | --- | --- |
| NEXT2564_0_selected | selected | 2565-Y5-R2FR-first-real-local-bound-source-and-parent-coefficient-blocker.md | scripts/Y5_R2FR_first_real_local_bound_source_and_parent_coefficient_blocker_2565.py | source the first real local bound/control row for R10 or PPN with units and baseline metadata, while also recording that parent GK coefficients remain missing and no claim is allowed | source acquisition ledger, candidate bound/control row or blocker, parent-coefficient blocker row, units validation, fitted-GM guardrail, claim gates | no local-GR claim; no fitted GM; no M_H_ref reuse; no plateau axiom; no GitHub |

## Branch Copies
| copy_id | source_path | target_path | source_exists | target_exists |
| --- | --- | --- | --- | --- |
| dry_run_results | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_NO_SHADOW_2564_DRY_RUN_RESULTS.csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\GK_stress_bound_dry_run_results_2564_NONCLAIM.csv | True | True |
| baseline_control | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_NO_SHADOW_2564_BASELINE_CONTROL_LEDGER.csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\GK_stress_bound_baseline_control_2564_NONCLAIM.csv | True | True |
| rejection_queue | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_NO_SHADOW_2564_REJECTION_LEDGER.csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\rab-sector\acquisition-queue\JR2564_GK_STRESS_BOUND_REJECTION_LEDGER_NONCLAIM.csv | True | True |

## Validation
| check_id | status | notes | detail |
| --- | --- | --- | --- |
| VAL2564_00_sources_exist | PASS | all cited source paths exist and required needles are present |  |
| VAL2564_01_inputs_written | PASS | six dry-run inputs written for R10, PPN, clocks, orbital, WEP and light |  |
| VAL2564_02_results_written | PASS | one dry-run result per input |  |
| VAL2564_03_all_nonclaim | PASS | all result rows claim-blocked |  |
| VAL2564_04_rejections_written | PASS | every dry-run row has at least one rejection reason |  |
| VAL2564_05_baseline_controls | PASS | baseline control ledger includes pass and blocked controls |  |
| VAL2564_06_toy_arithmetic | PASS | toy arithmetic computes where numeric inputs and units allow it |  |
| VAL2564_07_bad_units_rejected | PASS | bad-unit row rejected |  |
| VAL2564_08_fitted_GM_rejected | PASS | fitted-GM row rejected |  |
| VAL2564_09_missing_baseline_rejected | PASS | missing baseline row rejected |  |
| VAL2564_10_future_shape_blocked | PASS | valid-looking future row blocks on missing parent/kernel/bound inputs |  |
| VAL2564_11_claim_gates_safe | PASS | no claim gate allows local-GR or local compatibility claim |  |
| VAL2564_12_next_target_written | PASS | 2565 source acquisition and parent blocker target selected |  |
| VAL2564_13_branch_copies | PASS | nonclaim branch copies exist |  |
| VAL2564_14_no_formalization_artifacts | PASS | no 2564 artifacts were written to formalization-workbench |  |
| VAL2564_CSV_P8_Y5_NO_SHADOW_2564_SOURCE_REGISTER | PASS | CSV parses with 6 rows | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_NO_SHADOW_2564_SOURCE_REGISTER.csv |
| VAL2564_CSV_P8_Y5_NO_SHADOW_2564_DRY_RUN_INPUTS | PASS | CSV parses with 6 rows | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_NO_SHADOW_2564_DRY_RUN_INPUTS.csv |
| VAL2564_CSV_P8_Y5_NO_SHADOW_2564_DRY_RUN_RESULTS | PASS | CSV parses with 6 rows | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_NO_SHADOW_2564_DRY_RUN_RESULTS.csv |
| VAL2564_CSV_P8_Y5_NO_SHADOW_2564_REJECTION_LEDGER | PASS | CSV parses with 6 rows | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_NO_SHADOW_2564_REJECTION_LEDGER.csv |
| VAL2564_CSV_P8_Y5_NO_SHADOW_2564_BASELINE_CONTROL_LEDGER | PASS | CSV parses with 6 rows | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_NO_SHADOW_2564_BASELINE_CONTROL_LEDGER.csv |
| VAL2564_CSV_P8_Y5_NO_SHADOW_2564_TOY_ARITHMETIC_SMOKE | PASS | CSV parses with 4 rows | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_NO_SHADOW_2564_TOY_ARITHMETIC_SMOKE.csv |
| VAL2564_CSV_P8_Y5_NO_SHADOW_2564_CLAIM_GATES | PASS | CSV parses with 10 rows | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_NO_SHADOW_2564_CLAIM_GATES.csv |
| VAL2564_CSV_P8_Y5_NO_SHADOW_2564_DECISION_LEDGER | PASS | CSV parses with 4 rows | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_NO_SHADOW_2564_DECISION_LEDGER.csv |
| VAL2564_CSV_P8_Y5_NO_SHADOW_2564_NEXT_TARGET | PASS | CSV parses with 1 rows | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_NO_SHADOW_2564_NEXT_TARGET.csv |
| VAL2564_CSV_P8_Y5_NO_SHADOW_2564_BRANCH_COPIES | PASS | CSV parses with 3 rows | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_NO_SHADOW_2564_BRANCH_COPIES.csv |
| VAL2564_COPY_CSV_dry_run_results | PASS | copy CSV parses with 6 rows | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\GK_stress_bound_dry_run_results_2564_NONCLAIM.csv |
| VAL2564_COPY_CSV_baseline_control | PASS | copy CSV parses with 6 rows | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\GK_stress_bound_baseline_control_2564_NONCLAIM.csv |
| VAL2564_COPY_CSV_rejection_queue | PASS | copy CSV parses with 6 rows | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\rab-sector\acquisition-queue\JR2564_GK_STRESS_BOUND_REJECTION_LEDGER_NONCLAIM.csv |
| VAL2564_OVERALL | PASS | 2564 dry-run runner computes toy residuals, checks matched baselines and blocks all claim routes |  |
