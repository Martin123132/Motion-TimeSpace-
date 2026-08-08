# 1241-Y5-R10-PPN-QR-nonclaim-smoke-runner-and-refusal-gates

**Current verdict:** 1241 builds the `Q_R -> gamma` nonclaim smoke runner and it refuses the dangerous cases correctly: closure zero, missing finite `q_R_hat`, comparator-only, and missing statistical policy.

**Main progress:** the local-GR testing lane now has executable refusal logic. A sourced finite `q_R_hat` or a real zero-charge theorem is still missing, but the runner will no longer confuse closure with evidence.

**No-claim guard:** no derived GR, local-GR pass, PPN pass, WEP/R10 pass, or public source-coupling claim is promoted.

Generated UTC: 2026-06-15T08:04:34.561194+00:00

## Source Register
| source_id | local_path | needle | purpose | absolute_path | path_exists | needle_found | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SRC1241_0_1240_next | source-intake/mts_residuals/P8_Y5_R10_1240_NEXT_TARGET.csv | NEXT1240_0_1241 | 1240 handoff to Q_R nonclaim smoke runner | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1240_NEXT_TARGET.csv | True | True | False | False |
| SRC1241_1_1240_bound_schema | source-intake/mts_residuals/P8_Y5_R10_1240_QR_BOUND_INPUT_SCHEMA.csv | QB1240_0_qR_input | Q_R bound input schema | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1240_QR_BOUND_INPUT_SCHEMA.csv | True | True | False | False |
| SRC1241_2_1240_map | source-intake/mts_residuals/P8_Y5_R10_1240_QR_TO_PPN_MAPPING_SCHEMA.csv | QMAP1240_3_gamma_projection | Q_R to gamma projection schema | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1240_QR_TO_PPN_MAPPING_SCHEMA.csv | True | True | False | False |
| SRC1241_3_1240_comparator | source-intake/mts_residuals/P8_Y5_R10_1240_PPN_COMPARATOR_LEDGER.csv | COMP1240_0_gamma_Cassini | Cassini gamma comparator status | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1240_PPN_COMPARATOR_LEDGER.csv | True | True | False | False |
| SRC1241_4_1240_zero_attempt | source-intake/mts_residuals/P8_Y5_R10_1240_QR_ZERO_CHARGE_THEOREM_ATTEMPT.csv | ZQR1240_5_verdict | Q_R zero theorem refused | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1240_QR_ZERO_CHARGE_THEOREM_ATTEMPT.csv | True | True | False | False |
| SRC1241_5_1239_inputs | source-intake/mts_residuals/P8_Y5_R10_1239_BRANCH_INPUT_ROWS_TEMPLATE.csv | IN1239_1_QR_finite | finite Q_R input row from 1239 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1239_BRANCH_INPUT_ROWS_TEMPLATE.csv | True | True | False | False |
| SRC1241_6_1181_gamma | source-intake/mts_residuals/P8_Y5_R10_1181_PPN_RESIDUAL_VECTOR_COMPARATOR_ROWS.csv | PPNV1181_0_gamma | gamma comparator source row | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1181_PPN_RESIDUAL_VECTOR_COMPARATOR_ROWS.csv | True | True | False | False |

## Nonclaim Runner Rules
| rule_id | rule | applies_to | refusal_if | claim_policy | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- |
| RULE1241_0_projection | gamma_minus_1_QR = -0.5*q_R_hat | finite_residual rows with numeric q_R_hat | q_R_hat missing or not normalized | nonclaim projection schema only | False | False |
| RULE1241_1_closure | branch_type=closure_benchmark can compute gamma=0 but must return REFUSED_CLOSURE_NOT_EVIDENCE | closure q_R=0 rows | always refused as evidence | private baseline only | False | False |
| RULE1241_2_comparator | Cassini gamma comparator cannot score without an MTS q_R_hat prediction/value | comparator-only rows | no q_R_hat supplied | comparator is not a prediction | False | False |
| RULE1241_3_pass_policy | pass_rule requires N_sigma and sigma_gamma | numeric finite rows | statistical policy missing | even numeric pass remains nonclaim until source/model gates close | False | False |

## Smoke Cases
| case_id | description | branch_type | value_mode | q_R_hat | N_sigma | sigma_gamma | source_status | expected_status | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CASE1241_0_closure_zero | closure benchmark q_R_hat=0 | closure_benchmark | closure_value | 0 | MISSING_STATISTICAL_POLICY | 2.3e-5 | closure_only | REFUSED_CLOSURE_NOT_EVIDENCE | False | False |
| CASE1241_1_finite_missing_qR | finite row from 1239/1240 with q_R_hat missing | finite_residual | missing_source | MISSING_QR_VALUE | MISSING_STATISTICAL_POLICY | 2.3e-5 | missing_source | REFUSED_MISSING_QR | False | False |
| CASE1241_2_comparator_only | Cassini comparator loaded without MTS q_R_hat | finite_residual | comparator_only | MISSING_QR_VALUE | 1 | 2.3e-5 | comparator_available_prediction_missing | REFUSED_COMPARATOR_ONLY | False | False |
| CASE1241_3_numeric_no_policy | numeric q_R_hat supplied but pass policy missing | finite_residual | numeric_value | 1.0e-5 | MISSING_STATISTICAL_POLICY | 2.3e-5 | hypothetical_schema_math_only | REFUSED_MISSING_STATISTICAL_POLICY | False | False |
| CASE1241_4_hypothetical_numeric | synthetic numeric row exercises arithmetic only | finite_residual | numeric_value | 1.0e-5 | 1 | 2.3e-5 | hypothetical_schema_math_only | SCHEMA_MATH_ONLY_NOT_EVIDENCE | False | False |

## Smoke Results
| case_id | branch_type | q_R_hat | gamma_minus_1_QR | abs_gamma_minus_1_QR | N_sigma | sigma_gamma | pass_rule_evaluated | raw_numeric_pass | runner_status | refusal_or_status_reason | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CASE1241_0_closure_zero | closure_benchmark | 0 | -0.0 | 0.0 | MISSING_STATISTICAL_POLICY | 2.3e-5 | False | False | REFUSED_CLOSURE_NOT_EVIDENCE | closure q_R=0 may be displayed as private baseline but cannot pass as evidence | False | False |
| CASE1241_1_finite_missing_qR | finite_residual | MISSING_QR_VALUE |  |  | MISSING_STATISTICAL_POLICY | 2.3e-5 | False | False | REFUSED_MISSING_QR | finite residual row lacks numeric q_R_hat or derived zero theorem | False | False |
| CASE1241_2_comparator_only | finite_residual | MISSING_QR_VALUE |  |  | 1 | 2.3e-5 | False | False | REFUSED_COMPARATOR_ONLY | Cassini comparator exists but no MTS q_R_hat prediction/value is supplied | False | False |
| CASE1241_3_numeric_no_policy | finite_residual | 1.0e-5 | -5e-06 | 5e-06 | MISSING_STATISTICAL_POLICY | 2.3e-5 | False | False | REFUSED_MISSING_STATISTICAL_POLICY | numeric q_R_hat exists but no N_sigma/sigma_gamma pass policy is supplied | False | False |
| CASE1241_4_hypothetical_numeric | finite_residual | 1.0e-5 | -5e-06 | 5e-06 | 1 | 2.3e-5 | True | True | SCHEMA_MATH_ONLY_NOT_EVIDENCE | synthetic value exercises arithmetic only; it is not a sourced MTS prediction | False | False |

## Refusal Gates
| gate_id | refusal | case_id | expected_status | observed_status | gate_pass | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| REF1241_0_closure_refused | closure q_R=0 cannot pass as evidence | CASE1241_0_closure_zero | REFUSED_CLOSURE_NOT_EVIDENCE | REFUSED_CLOSURE_NOT_EVIDENCE | True | False | False |
| REF1241_1_missing_qR_refused | finite row with missing q_R_hat cannot score | CASE1241_1_finite_missing_qR | REFUSED_MISSING_QR | REFUSED_MISSING_QR | True | False | False |
| REF1241_2_comparator_only_refused | Cassini comparator alone cannot become an MTS prediction | CASE1241_2_comparator_only | REFUSED_COMPARATOR_ONLY | REFUSED_COMPARATOR_ONLY | True | False | False |
| REF1241_3_policy_refused | numeric q_R_hat without statistical policy cannot score | CASE1241_3_numeric_no_policy | REFUSED_MISSING_STATISTICAL_POLICY | REFUSED_MISSING_STATISTICAL_POLICY | True | False | False |
| REF1241_4_hypothetical_nonclaim | synthetic numeric arithmetic is not evidence | CASE1241_4_hypothetical_numeric | SCHEMA_MATH_ONLY_NOT_EVIDENCE | SCHEMA_MATH_ONLY_NOT_EVIDENCE | True | False | False |

## Decision Ledger
| decision_id | decision | because | next_action | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| DEC1241_0_runner_refuses_correctly | keep Q_R smoke runner as refusal-first nonclaim tool | closure, missing finite, comparator-only, missing-policy, and hypothetical rows are all blocked from claims | acquire real q_R_hat or derive Q_R=0 before any numeric score | False | False |
| DEC1241_1_next_input | next useful work is q_R_hat source/theorem acquisition | the runner logic is ready but the physics input remains missing | write source/theorem intake contract for q_R_hat | False | False |

## Claim Gates
| gate_id | claim | status | reason | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| GATE1241_0_smoke_runner | nonclaim smoke runner exists | PASS_NONCLAIM | smoke cases and refusal gates generated | False | False |
| GATE1241_1_QR_numeric_pass | finite Q_R passes gamma bound | BLOCKED | no sourced q_R_hat and no statistical policy | False | False |
| GATE1241_2_closure_evidence | closure Q_R=0 counts as evidence | BLOCKED | CASE1241_0 is refused as closure-only | False | False |
| GATE1241_3_local_GR | derived local GR/Newton pass | BLOCKED | Q_R finite input/theorem, beta, source, and conservation remain open | False | False |

## Next Target
| next_id | target_file | target_script | task | success_condition | do_not_do | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NEXT1241_0_1242 | 1242-Y5-R10-QR-hat-source-or-zero-theorem-input-contract.md | scripts/Y5_R10_QR_hat_source_or_zero_theorem_input_contract.py | define the exact acceptable input contract for q_R_hat: either a parent zero-charge theorem source or a finite normalized q_R_hat value with GM convention, units, statistical policy, and provenance | future Q_R smoke runner can load a real candidate row or reject it for precise missing fields | do not fabricate q_R_hat, do not use closure zero as input evidence, and do not claim local GR | False | False |

## Validation
| check_id | check | status | details | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| VAL1241_0_sources_exist | all cited local sources exist | PASS | 7/7 sources exist | False | False |
| VAL1241_1_needles_found | all cited local needles found | PASS | 7/7 needles found | False | False |
| VAL1241_2_refusal_gates | all refusal gates pass | PASS | refusal_gates=5/5 | False | False |
| VAL1241_3_closure_refused | closure Q_R=0 is refused as evidence | PASS | REFUSED_CLOSURE_NOT_EVIDENCE present | False | False |
| VAL1241_4_missing_qR_refused | finite row missing q_R_hat is refused | PASS | REFUSED_MISSING_QR present | False | False |
| VAL1241_5_comparator_refused | comparator-only row is refused | PASS | REFUSED_COMPARATOR_ONLY present | False | False |
| VAL1241_6_hypothetical_nonclaim | hypothetical arithmetic row remains nonclaim | PASS | SCHEMA_MATH_ONLY_NOT_EVIDENCE present | False | False |
| VAL1241_7_claim_gates | claim gates remain blocked/nonclaim | PASS | claim_gate_rows=4 | False | False |
| VAL1241_8_nonclaim_policy | all generated rows remain nonclaim | PASS | valid_for_claim=false and claim_allowed=false throughout generated tables | False | False |
| VAL1241_9_next_target_1242 | next target is q_R_hat input contract | PASS | 1242-Y5-R10-QR-hat-source-or-zero-theorem-input-contract.md | False | False |
| VAL1241_10_csv_parse | all generated CSVs parse cleanly | PASS | P8_Y5_R10_1241_SOURCE_REGISTER.csv:7; P8_Y5_R10_1241_NONCLAIM_RUNNER_RULES.csv:4; P8_Y5_R10_1241_SMOKE_CASES.csv:5; P8_Y5_R10_1241_SMOKE_RESULTS.csv:5; P8_Y5_R10_1241_REFUSAL_GATES.csv:5; P8_Y5_R10_1241_DECISION_LEDGER.csv:2; P8_Y5_R10_1241_CLAIM_GATES.csv:4; P8_Y5_R10_1241_NEXT_TARGET.csv:1 | False | False |
| VAL1241_11_formalization_untouched | formalization-workbench untouched during run | PASS | formalization_recent_write_count_since_run_start=0 | False | False |
| VAL1241_12_overall | overall 1241 validation | PASS | 1241 builds a refusal-first nonclaim Q_R smoke runner and proves closure/comparator/missing-source rows cannot pass as evidence | False | False |
