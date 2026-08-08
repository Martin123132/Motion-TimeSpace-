# 1242-Y5-R10-QR-hat-source-or-zero-theorem-input-contract

**Current verdict:** 1242 defines the exact acceptable input contract for `q_R_hat`, but it does **not** supply or invent a value. Future rows must be either `finite_qR_hat` with units/provenance/policy or `parent_zero_theorem` with a real theorem source.

**Main progress:** a dedicated `source-intake/qr-hat` lane now exists with raw/docs/accepted/rejected folders, templates, acceptance gates, and a dry-run that fabricates nothing.

**No-claim guard:** no `Q_R=0`, PPN pass, local-GR pass, WEP/R10 pass, or public source-coupling claim is promoted.

Generated UTC: 2026-06-15T08:08:14.612076+00:00

## Source Register
| source_id | local_path | needle | purpose | absolute_path | path_exists | needle_found | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SRC1242_0_1241_next | source-intake/mts_residuals/P8_Y5_R10_1241_NEXT_TARGET.csv | NEXT1241_0_1242 | 1241 handoff to q_R_hat input contract | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1241_NEXT_TARGET.csv | True | True | False | False |
| SRC1242_1_1241_smoke | source-intake/mts_residuals/P8_Y5_R10_1241_SMOKE_RESULTS.csv | REFUSED_MISSING_QR | smoke runner refuses missing q_R_hat | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1241_SMOKE_RESULTS.csv | True | True | False | False |
| SRC1242_2_1241_policy | source-intake/mts_residuals/P8_Y5_R10_1241_REFUSAL_GATES.csv | REF1241_3_policy_refused | statistical policy refusal gate | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1241_REFUSAL_GATES.csv | True | True | False | False |
| SRC1242_3_1240_bound | source-intake/mts_residuals/P8_Y5_R10_1240_QR_BOUND_INPUT_SCHEMA.csv | QB1240_0_qR_input | q_R_hat finite input schema | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1240_QR_BOUND_INPUT_SCHEMA.csv | True | True | False | False |
| SRC1242_4_1240_zero | source-intake/mts_residuals/P8_Y5_R10_1240_QR_ZERO_CHARGE_THEOREM_ATTEMPT.csv | ZQR1240_5_verdict | Q_R zero theorem not derived | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1240_QR_ZERO_CHARGE_THEOREM_ATTEMPT.csv | True | True | False | False |
| SRC1242_5_1240_map | source-intake/mts_residuals/P8_Y5_R10_1240_QR_TO_PPN_MAPPING_SCHEMA.csv | QMAP1240_2_dimensionless_qR | q_R_hat normalization | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1240_QR_TO_PPN_MAPPING_SCHEMA.csv | True | True | False | False |

## QR Hat Directory Contract
| directory_id | path | purpose | required_use | created_or_verified | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- |
| QDIR1242_0_root | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\qr-hat | q_R_hat candidate intake root | place future candidate CSVs in raw; supporting papers/notes in docs | True | False | False |
| QDIR1242_1_raw | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\qr-hat\raw | unreviewed q_R_hat candidate rows | raw candidate CSVs only; no automatic claim use | True | False | False |
| QDIR1242_2_docs | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\qr-hat\docs | provenance docs and derivation notes | store source notes, theorem sketches, or extraction docs | True | False | False |
| QDIR1242_3_accepted | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\qr-hat\accepted | reviewed nonclaim candidate rows | only rows passing all schema gates; still valid_for_claim=false | True | False | False |
| QDIR1242_4_rejected | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\qr-hat\rejected | candidate rows with precise missing-field reason | archive rejected candidates and gate failures | True | False | False |

## QR Hat Input Contract
| field_name | required_for | type | acceptance_rule | reject_if_missing | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- |
| candidate_id | finite_or_zero | string | unique stable id | True | False | False |
| route_type | finite_or_zero | enum | finite_qR_hat \| parent_zero_theorem | True | False | False |
| q_R_hat | finite_qR_hat | numeric | finite dimensionless value q_R_hat=Q_R*c^2/(GM) | True | False | False |
| q_R_hat_units | finite_qR_hat | string | must be dimensionless | True | False | False |
| Q_R_units_before_normalization | finite_qR_hat | string | declares raw Q_R units or says directly_dimensionless_q_R_hat | True | False | False |
| GM_convention | finite_qR_hat | string | same measured GM/source convention used in PPN comparator | True | False | False |
| source_path | finite_or_zero | path_or_reference | local path or external provenance string; no placeholder markers | True | False | False |
| derivation_status | finite_or_zero | enum | parent_derived_zero \| sourced_finite_model \| phenomenological_bound_nonclaim | True | False | False |
| N_sigma | finite_qR_hat | numeric | declared statistical policy for comparator | True | False | False |
| sigma_gamma | finite_qR_hat | numeric | uncertainty used by pass rule, e.g. 2.3e-5 from comparator row | True | False | False |
| zero_theorem_statement | parent_zero_theorem | string | states theorem proving Q_R=0 without closure R_AB=0 | True | False | False |
| closure_used | finite_or_zero | boolean | must be False for claim-like theorem route; closure rows stay benchmark-only | True | False | False |
| valid_for_claim | finite_or_zero | boolean | False in this checkpoint even if accepted for smoke runner | True | False | False |
| claim_allowed | finite_or_zero | boolean | False in this checkpoint | True | False | False |

## QR Hat Acceptance Gates
| gate_id | gate | acceptance_condition | failure_status | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| QGATE1242_0_no_closure_zero | closure q_R_hat=0 is rejected as input evidence | closure_used=False or branch explicitly closure_benchmark and not scored | REJECT_CLOSURE_AS_EVIDENCE | False | False |
| QGATE1242_1_finite_numeric | finite candidate has numeric q_R_hat | q_R_hat parses as finite float and units=dimensionless | REJECT_MISSING_OR_NONNUMERIC_QR | False | False |
| QGATE1242_2_GM_convention | GM/source convention declared | GM_convention is non-placeholder and tied to comparator source | REJECT_MISSING_GM_CONVENTION | False | False |
| QGATE1242_3_policy | statistical pass policy declared | N_sigma and sigma_gamma parse as finite positive numbers | REJECT_MISSING_STATISTICAL_POLICY | False | False |
| QGATE1242_4_source | source/provenance declared | source_path is non-placeholder and either exists locally or is an explicit external source/provenance id | REJECT_MISSING_SOURCE | False | False |
| QGATE1242_5_zero_theorem | parent zero theorem route proves Q_R=0 without closure | route_type=parent_zero_theorem and zero_theorem_statement plus source_path are present; closure_used=False | REJECT_ZERO_THEOREM_UNDERIVED | False | False |

## QR Hat Candidate Template
| candidate_id | route_type | q_R_hat | q_R_hat_units | Q_R_units_before_normalization | GM_convention | source_path | derivation_status | N_sigma | sigma_gamma | zero_theorem_statement | closure_used | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| QR1242_TEMPLATE_FINITE | finite_qR_hat | MISSING_NUMERIC_QR_HAT | dimensionless | MISSING_QR_UNITS_OR_DIRECT_DIMENSIONLESS | MISSING_GM_CONVENTION | MISSING_SOURCE_PATH_OR_EXTERNAL_PROVENANCE | phenomenological_bound_nonclaim | MISSING_N_SIGMA | MISSING_SIGMA_GAMMA |  | False | False | False |

## Zero Theorem Template
| candidate_id | route_type | q_R_hat | q_R_hat_units | Q_R_units_before_normalization | GM_convention | source_path | derivation_status | N_sigma | sigma_gamma | zero_theorem_statement | closure_used | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| QR1242_TEMPLATE_ZERO_THEOREM | parent_zero_theorem | 0 | dimensionless | theorem_zero | not_required_for_parent_zero_but_state_comparator_convention_if_scored | MISSING_PARENT_ZERO_THEOREM_SOURCE | parent_derived_zero |  |  | MISSING_THEOREM_STATEMENT_PROVING_Q_R_EQUALS_ZERO_WITHOUT_R_AB_CLOSURE | False | False | False |

## Candidate Validator Dry-Run
| dryrun_id | candidate_file | status | reason | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| QRDRY1242_0_no_candidates | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\qr-hat\raw | NO_CANDIDATE_FILES_FOUND | no q_R_hat candidates were present; no value fabricated | False | False |

## Decision Ledger
| decision_id | decision | because | next_action | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| DEC1242_0_no_fabrication | do not create a numeric q_R_hat | 1241/1240 show q_R_hat is the missing physics input | wait for a real source/theorem row or build a future validator | False | False |
| DEC1242_1_two_routes | allow exactly two future routes: finite_qR_hat or parent_zero_theorem | closure zero and comparator-only rows are known failure modes | route future rows through QGATE1242 gates | False | False |
| DEC1242_2_next_validator | next implementation should validate candidate rows against this contract | contract is now explicit but no candidate files exist | build candidate intake validator or source-hunt ledger | False | False |

## Claim Gates
| gate_id | claim | status | reason | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| GATE1242_0_contract_exists | q_R_hat input contract exists | PASS_NONCLAIM | contract, gates, templates, directories, and dry-run rows generated | False | False |
| GATE1242_1_qR_value | numeric q_R_hat exists | BLOCKED | no candidate files and template row keeps MISSING markers | False | False |
| GATE1242_2_zero_theorem | parent Q_R=0 theorem exists | BLOCKED | zero theorem template is missing source and proof statement | False | False |
| GATE1242_3_local_GR | local GR/Newton pass | BLOCKED | input contract is not a physics result | False | False |

## Next Target
| next_id | target_file | target_script | task | success_condition | do_not_do | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NEXT1242_0_1243 | 1243-Y5-R10-QR-hat-candidate-intake-validator-or-source-hunt-ledger.md | scripts/Y5_R10_QR_hat_candidate_intake_validator_or_source_hunt_ledger.py | build the row-level validator for source-intake/qr-hat/raw candidates and, if none exist, create a source-hunt ledger for finite q_R_hat or parent Q_R=0 theorem inputs | candidate rows are either accepted as nonclaim runner inputs or rejected with exact missing fields; if no rows exist, the source-hunt ledger names the missing source/theorem targets | do not fabricate q_R_hat, do not claim local GR, and do not push to GitHub | False | False |

## Validation
| check_id | check | status | details | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| VAL1242_0_sources_exist | all cited local sources exist | PASS | 6/6 sources exist | False | False |
| VAL1242_1_needles_found | all cited local needles found | PASS | 6/6 needles found | False | False |
| VAL1242_2_directories | q_R_hat intake directories exist | PASS | directories=5 | False | False |
| VAL1242_3_contract_fields | input contract has required fields | PASS | contract_fields=14 | False | False |
| VAL1242_4_acceptance_gates | acceptance gates cover known failure modes | PASS | acceptance_gates=6 | False | False |
| VAL1242_5_templates_nonclaim | templates remain nonclaim and contain missing markers | PASS | finite and zero-theorem templates valid_for_claim=false | False | False |
| VAL1242_6_no_fabrication | dry-run does not fabricate q_R_hat | PASS | NO_CANDIDATE_FILES_FOUND | False | False |
| VAL1242_7_claim_gates | claim gates remain blocked/nonclaim | PASS | claim_gate_rows=4 | False | False |
| VAL1242_8_nonclaim_policy | all generated rows remain nonclaim | PASS | valid_for_claim=false and claim_allowed=false throughout generated tables | False | False |
| VAL1242_9_next_target_1243 | next target is q_R_hat intake validator or source hunt | PASS | 1243-Y5-R10-QR-hat-candidate-intake-validator-or-source-hunt-ledger.md | False | False |
| VAL1242_10_csv_parse | all generated CSVs parse cleanly | PASS | P8_Y5_R10_1242_SOURCE_REGISTER.csv:6; P8_Y5_R10_1242_QR_HAT_DIRECTORY_CONTRACT.csv:5; P8_Y5_R10_1242_QR_HAT_INPUT_CONTRACT.csv:14; P8_Y5_R10_1242_QR_HAT_ACCEPTANCE_GATES.csv:6; P8_Y5_R10_1242_QR_HAT_CANDIDATE_TEMPLATE_NONCLAIM.csv:1; P8_Y5_R10_1242_ZERO_THEOREM_TEMPLATE_NONCLAIM.csv:1; P8_Y5_R10_1242_QR_HAT_CANDIDATE_VALIDATOR_DRYRUN.csv:1; P8_Y5_R10_1242_DECISION_LEDGER.csv:3; P8_Y5_R10_1242_CLAIM_GATES.csv:4; P8_Y5_R10_1242_NEXT_TARGET.csv:1 | False | False |
| VAL1242_11_formalization_untouched | formalization-workbench untouched during run | PASS | formalization_recent_write_count_since_run_start=0 | False | False |
| VAL1242_12_overall | overall 1242 validation | PASS | 1242 defines the exact q_R_hat/zero-theorem input contract without fabricating a value or promoting a claim | False | False |
