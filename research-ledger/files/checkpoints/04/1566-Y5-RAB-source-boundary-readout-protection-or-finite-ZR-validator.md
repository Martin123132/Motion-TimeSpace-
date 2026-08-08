# 1566 - R_AB Source/Boundary/Readout Protection or Finite Z_R Validator

## Verdict
- The second-class auxiliary route is still the best local mechanism, but it does not close unless four leaks are jointly sealed: `J_R=0`, `B_R=0`, readout stability, and operator exclusion.
- Current corpus status: all four are unsigned or exact-conditional, so no `Z_R=0`, `q_R=0`, local GR/Newton, R10, PPN, clock, or orbital claim is allowed.
- The fallback branch is now guarded by a stricter finite-`Z_R` validator: docs templates are rejected, `MISSING` markers are rejected, absent source paths/anchors are rejected, and no accepted source-ready rows exist.
- This is grim in the useful way: the leak map is now precise, not vague.

## Source Register
| source_id | source_path | exists | needle_found | needles |
| --- | --- | --- | --- | --- |
| SRC1566_0_1565_doc | 1565-Y5-RAB-parent-theta-Omega-vR-fill-or-finite-ZR-source-row.md | True | True | The catch is important: this is second-class auxiliary elimination; No `Z_R=0`, `q_R=0`, local GR/Newton |
| SRC1566_1_1565_validation | source-intake/mts_residuals/P8_Y5_BRR545_1565_VALIDATION.csv | True | True | VAL1565_OVERALL; PASS |
| SRC1566_2_1565_decision | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1565_DECISION.csv | True | True | DEC1565_2_best_route; SECOND_CLASS_ELIMINATION_OR_FINITE_ZR_INTAKE |
| SRC1566_3_1565_elim | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1565_SECOND_CLASS_ELIMINATION_CONDITIONS.csv | True | True | ELIM1565_1_E_R; PASS_ONLY_IF_SOURCES_ZERO |
| SRC1566_4_1565_requirements | source-intake/rab-sector/docs/ZR1565_FINITE_ZR_SOURCE_ROW_INTAKE_REQUIREMENTS_NONCLAIM.csv | True | True | REQ1565_0_ZR; REQUIRED_BEFORE_RAW_OR_ACCEPTED |
| SRC1566_5_1563_grammar | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1563_NO_DERIVATIVE_GRAMMAR_GATE.csv | True | True | GRAM1563_5_verdict; FAIL_CURRENT_THEOREM |
| SRC1566_6_1563_elim | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1563_AUXILIARY_ELIMINATION_GATE.csv | True | True | ELIM1563_1_E_R; PASS_ONLY_IF_SOURCES_ZERO |
| SRC1566_7_1562_boundary | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1562_BOUNDARY_DEGREE_COUNT_GATE.csv | True | True | BD1562_2_matter; UNSIGNED |
| SRC1566_8_1265_protection | source-intake/mts_residuals/P8_Y5_R10_1265_AUXILIARY_PROTECTION_AUDIT.csv | True | True | AP1265_4_readout_stability; UNSIGNED_READOUT_PROTECTION |
| SRC1566_9_1265_risk | source-intake/mts_residuals/P8_Y5_R10_1265_REGENERATION_RISK_LEDGER.csv | True | True | RR1265_3_readout_EFT; UNSIGNED |
| SRC1566_10_1268_action | source-intake/mts_residuals/P8_Y5_R10_1268_COMPATIBILITY_ACTION_CANDIDATE.csv | True | True | CAC1268_5_conditional_theorem; EXACT_CONDITIONAL_NOT_PARENT_SIGNED |
| SRC1566_11_1269_operator | source-intake/mts_residuals/P8_Y5_R10_1269_OPERATOR_EXCLUSION_PARENT_SORT_ATTEMPT.csv | True | True | OP1269_4_theorem_candidate; BLOCKED_EXACT_CONDITIONAL |
| SRC1566_12_1269_rules | source-intake/mts_residuals/P8_Y5_R10_1269_ZR_INTAKE_VALIDATOR_RULES.csv | True | True | RULE1269_1_no_missing_markers; MISSING_MARKER_PRESENT |
| SRC1566_13_1269_summary | source-intake/mts_residuals/P8_Y5_R10_1269_ZR_INTAKE_VALIDATOR_SUMMARY.csv | True | True | NO_ACCEPTED_SOURCE_READY_ROWS; DOCS_TEMPLATES_REJECTED_AS_EXPECTED |
| SRC1566_14_1023_doc | 1023-Y5-R10-q-vX-action-descent-certificate-or-scalar-nohair-demotion.md | True | True | matter/no-marker descent; boundary silence |

## Protection Proof Audit
| protection_id | quantity | zero_condition | status | blocking_gap | fallback_if_missing |
| --- | --- | --- | --- | --- | --- |
| PROT1566_0_JR_matter | J_R = delta S_matter/delta R_AB | J_R=0 if matter descends through q(Phi), theta, top and carries no hidden R_AB marker | UNSIGNED_MATTER_DESCENT | 1023 and 1562 keep matter/no-marker descent unsigned | finite J_R source row or matter descent theorem |
| PROT1566_1_BR_boundary | B_R or Pi_R^n | B_R=Pi_R^n=0 if boundary/corner grammar has no R_AB functional and theta_R=0 | UNSIGNED_BOUNDARY_SILENCE | bulk auxiliary status does not exclude corner/source-worldtube hair | finite B_R/Pi_Rn bound or boundary no-hair theorem |
| PROT1566_2_readout | readout_regen and S_eff | readout_regen=0 if effective/readout map remains inside ParentGenerate[q,theta,top] | UNSIGNED_READOUT_STABILITY | radiative/readout closure is not parent-proved | finite tau_clock/tau_R10/tau_PPN/tau_orbital row or stability theorem |
| PROT1566_3_operator | Z_R |D R_AB|^2 and D Lambda_R operators | Z_R=0 if parent object language forbids derivative constructors and vertical metrics | UNSIGNED_OPERATOR_EXCLUSION | 1269 keeps AP1265_1 blocked exact-conditional | finite Z_R/M_R2 row or operator-exclusion theorem |
| PROT1566_4_joint | second-class local-GR protection package | all of PROT1566_0 through PROT1566_3 must close together | JOINT_PROTECTION_NOT_CLOSED | one leak is enough to leave finite q_R/Z_R residuals | parent protection contract or finite residual workflow |

## Joint Gate
| joint_id | target | condition_or_result | status |
| --- | --- | --- | --- |
| JOINT1566_0_eliminate_auxiliary | E_Lambda and E_R eliminate R_AB,Lambda_R before readout | blocked unless J_R=B_R=readout_regen=0 and derivative grammar is signed | BLOCKED_NO_CLAIM |
| JOINT1566_1_forbid_ZR | Z_R operator cannot be generated | blocked unless no-derivative/object-exhaustion proof is parent-owned and readout-stable | BLOCKED_NO_CLAIM |
| JOINT1566_2_local_qR | q_R=0 or q_R residual below local bounds | blocked because theorem-zero fails and no finite source rows exist | BLOCKED_NO_CLAIM |
| JOINT1566_3_verdict | local GR/Newton gate | second-class route survives as best conditional but cannot be claimed | JOINT_PROTECTION_NOT_CLOSED |

## Finite Z_R Validator Rules
| rule_id | rule | failure_status | severity |
| --- | --- | --- | --- |
| RULE1566_0_docs_not_live | Rows under source-intake/rab-sector/docs are never live intake. | DOCS_TEMPLATE_NOT_LIVE_INTAKE | hard_reject |
| RULE1566_1_no_missing_markers | Any field containing MISSING rejects the row. | MISSING_MARKER_PRESENT | hard_reject |
| RULE1566_2_required_columns | Rows must include coefficient_symbol, coefficient_value, coefficient_units, normalization_convention, parent_action_block, source_path, source_anchor, and arena_projection. | MISSING_REQUIRED_COLUMNS_OR_EMPTY_FIELD | hard_reject |
| RULE1566_3_source_path | source_path must be non-placeholder and resolve to a local source file for this private checkpoint. | SOURCE_PATH_MISSING_OR_NOT_FOUND | hard_reject |
| RULE1566_4_source_anchor | source_anchor must be non-placeholder and appear in source_path text. | SOURCE_ANCHOR_MISSING_OR_NOT_FOUND | hard_reject |
| RULE1566_5_private_nonclaim | valid_for_claim=true or claim_allowed=true rejects a row in this private phase. | CLAIM_FLAG_TRUE_REJECTED | hard_reject |
| RULE1566_6_no_score_without_arena | arena_projection must map the row to R10, PPN, clock, orbital, or all. | ARENA_PROJECTION_EMPTY | hard_reject |

## Finite Z_R Validator Summary
| summary_id | docs_rows | raw_rows | accepted_rows | rejected_rows | accepted_ready_rows | invalid_live_rows | status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| VS1566_0_scan_counts | 19 | 0 | 0 | 19 | 0 | 0 | NO_ACCEPTED_SOURCE_READY_ROWS |
| VS1566_1_template_refusal | 19 | 0 | 0 | 19 | 0 | 0 | DOCS_TEMPLATES_REJECTED_AS_EXPECTED |

## Finite Z_R Validator Results
| scan_id | intake_class | row_id | coefficient_symbol | status | reasons | source_exists | anchor_found |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SCAN1566_docs_ZR1259_RAB_GRADIENT_COEFFICIENT_TEMPLATE_NONCLAIM_0 | docs | ZR1259_TEMPLATE_DO_NOT_SCORE | Z_R_or_M_R2_or_J_R_or_B_R | REJECT | DOCS_TEMPLATE_NOT_LIVE_INTAKE|MISSING_REQUIRED_COLUMNS:source_anchor,arena_projection|MISSING_MARKER_PRESENT|SOURCE_PATH_MISSING_OR_NOT_FOUND|SOURCE_ANCHOR_MISSING_OR_NOT_FOUND|ARENA_PROJECTION_EMPTY | False | False |
| SCAN1566_docs_ZR1262_RAB_PRIOR_ENVELOPE_TEMPLATE_NONCLAIM_0 | docs | ZR1262_TEMPLATE_DO_NOT_SCORE | Z_R_or_M_R2_or_J_R_or_B_R | REJECT | DOCS_TEMPLATE_NOT_LIVE_INTAKE|MISSING_REQUIRED_COLUMNS:parent_action_block|MISSING_MARKER_PRESENT|SOURCE_PATH_MISSING_OR_NOT_FOUND|SOURCE_ANCHOR_MISSING_OR_NOT_FOUND|ARENA_PROJECTION_EMPTY | False | False |
| SCAN1566_docs_ZR1264_FINITE_ZR_SOURCE_ROW_TEMPLATE_NONCLAIM_0 | docs | ZR1264_TEMPLATE_DO_NOT_SCORE | Z_R | REJECT | DOCS_TEMPLATE_NOT_LIVE_INTAKE|MISSING_REQUIRED_COLUMNS:normalization_convention,parent_action_block|MISSING_MARKER_PRESENT|SOURCE_PATH_MISSING_OR_NOT_FOUND|SOURCE_ANCHOR_MISSING_OR_NOT_FOUND|ARENA_PROJECTION_EMPTY | False | False |
| SCAN1566_docs_ZR1268_FINITE_ZR_SOURCE_ROW_TEMPLATE_NONCLAIM_0 | docs | ZR1268_TEMPLATE_ZR | Z_R | REJECT | DOCS_TEMPLATE_NOT_LIVE_INTAKE|MISSING_MARKER_PRESENT|SOURCE_PATH_MISSING_OR_NOT_FOUND|SOURCE_ANCHOR_MISSING_OR_NOT_FOUND|ARENA_PROJECTION_EMPTY | False | False |
| SCAN1566_docs_ZR1268_FINITE_ZR_SOURCE_ROW_TEMPLATE_NONCLAIM_1 | docs | ZR1268_TEMPLATE_MR2 | M_R^2 | REJECT | DOCS_TEMPLATE_NOT_LIVE_INTAKE|MISSING_MARKER_PRESENT|SOURCE_PATH_MISSING_OR_NOT_FOUND|SOURCE_ANCHOR_MISSING_OR_NOT_FOUND|ARENA_PROJECTION_EMPTY | False | False |
| SCAN1566_docs_ZR1268_FINITE_ZR_SOURCE_ROW_TEMPLATE_NONCLAIM_2 | docs | ZR1268_TEMPLATE_JR | J_R | REJECT | DOCS_TEMPLATE_NOT_LIVE_INTAKE|MISSING_MARKER_PRESENT|SOURCE_PATH_MISSING_OR_NOT_FOUND|SOURCE_ANCHOR_MISSING_OR_NOT_FOUND|ARENA_PROJECTION_EMPTY | False | False |
| SCAN1566_docs_ZR1268_FINITE_ZR_SOURCE_ROW_TEMPLATE_NONCLAIM_3 | docs | ZR1268_TEMPLATE_BR | B_R_or_Pi_Rn | REJECT | DOCS_TEMPLATE_NOT_LIVE_INTAKE|MISSING_MARKER_PRESENT|SOURCE_PATH_MISSING_OR_NOT_FOUND|SOURCE_ANCHOR_MISSING_OR_NOT_FOUND|ARENA_PROJECTION_EMPTY | False | False |
| SCAN1566_docs_ZR1268_FINITE_ZR_SOURCE_ROW_TEMPLATE_NONCLAIM_4 | docs | ZR1268_TEMPLATE_TAU_R10 | tau_R10 | REJECT | DOCS_TEMPLATE_NOT_LIVE_INTAKE|MISSING_MARKER_PRESENT|SOURCE_PATH_MISSING_OR_NOT_FOUND|SOURCE_ANCHOR_MISSING_OR_NOT_FOUND | False | False |
| SCAN1566_docs_ZR1268_FINITE_ZR_SOURCE_ROW_TEMPLATE_NONCLAIM_5 | docs | ZR1268_TEMPLATE_TAU_PPN | tau_PPN | REJECT | DOCS_TEMPLATE_NOT_LIVE_INTAKE|MISSING_MARKER_PRESENT|SOURCE_PATH_MISSING_OR_NOT_FOUND|SOURCE_ANCHOR_MISSING_OR_NOT_FOUND | False | False |
| SCAN1566_docs_ZR1268_FINITE_ZR_SOURCE_ROW_TEMPLATE_NONCLAIM_6 | docs | ZR1268_TEMPLATE_TAU_CLOCK | tau_clock | REJECT | DOCS_TEMPLATE_NOT_LIVE_INTAKE|MISSING_MARKER_PRESENT|SOURCE_PATH_MISSING_OR_NOT_FOUND|SOURCE_ANCHOR_MISSING_OR_NOT_FOUND | False | False |
| SCAN1566_docs_ZR1268_FINITE_ZR_SOURCE_ROW_TEMPLATE_NONCLAIM_7 | docs | ZR1268_TEMPLATE_TAU_ORBITAL | tau_orbital | REJECT | DOCS_TEMPLATE_NOT_LIVE_INTAKE|MISSING_MARKER_PRESENT|SOURCE_PATH_MISSING_OR_NOT_FOUND|SOURCE_ANCHOR_MISSING_OR_NOT_FOUND | False | False |
| SCAN1566_docs_ZR1565_FINITE_ZR_SOURCE_ROW_INTAKE_REQUIREMENTS_NONCLAIM_0 | docs | REQ1565_0_ZR | Z_R | REJECT | DOCS_TEMPLATE_NOT_LIVE_INTAKE|MISSING_REQUIRED_COLUMNS:coefficient_symbol,coefficient_value,coefficient_units,normalization_convention,parent_action_block,source_path,source_anchor|SOURCE_PATH_MISSING_OR_NOT_FOUND|SOURCE_ANCHOR_MISSING_OR_NOT_FOUND | False | False |
| SCAN1566_docs_ZR1565_FINITE_ZR_SOURCE_ROW_INTAKE_REQUIREMENTS_NONCLAIM_1 | docs | REQ1565_1_MR2 | M_R^2 | REJECT | DOCS_TEMPLATE_NOT_LIVE_INTAKE|MISSING_REQUIRED_COLUMNS:coefficient_symbol,coefficient_value,coefficient_units,normalization_convention,parent_action_block,source_path,source_anchor|SOURCE_PATH_MISSING_OR_NOT_FOUND|SOURCE_ANCHOR_MISSING_OR_NOT_FOUND | False | False |
| SCAN1566_docs_ZR1565_FINITE_ZR_SOURCE_ROW_INTAKE_REQUIREMENTS_NONCLAIM_2 | docs | REQ1565_2_JR | J_R | REJECT | DOCS_TEMPLATE_NOT_LIVE_INTAKE|MISSING_REQUIRED_COLUMNS:coefficient_symbol,coefficient_value,coefficient_units,normalization_convention,parent_action_block,source_path,source_anchor|SOURCE_PATH_MISSING_OR_NOT_FOUND|SOURCE_ANCHOR_MISSING_OR_NOT_FOUND | False | False |
| SCAN1566_docs_ZR1565_FINITE_ZR_SOURCE_ROW_INTAKE_REQUIREMENTS_NONCLAIM_3 | docs | REQ1565_3_BR | B_R_or_Pi_Rn | REJECT | DOCS_TEMPLATE_NOT_LIVE_INTAKE|MISSING_REQUIRED_COLUMNS:coefficient_symbol,coefficient_value,coefficient_units,normalization_convention,parent_action_block,source_path,source_anchor|SOURCE_PATH_MISSING_OR_NOT_FOUND|SOURCE_ANCHOR_MISSING_OR_NOT_FOUND | False | False |
| SCAN1566_docs_ZR1565_FINITE_ZR_SOURCE_ROW_INTAKE_REQUIREMENTS_NONCLAIM_4 | docs | REQ1565_4_tau_R10 | tau_R10 | REJECT | DOCS_TEMPLATE_NOT_LIVE_INTAKE|MISSING_REQUIRED_COLUMNS:coefficient_symbol,coefficient_value,coefficient_units,normalization_convention,parent_action_block,source_path,source_anchor|MISSING_MARKER_PRESENT|SOURCE_PATH_MISSING_OR_NOT_FOUND|SOURCE_ANCHOR_MISSING_OR_NOT_FOUND | False | False |
| SCAN1566_docs_ZR1565_FINITE_ZR_SOURCE_ROW_INTAKE_REQUIREMENTS_NONCLAIM_5 | docs | REQ1565_5_tau_PPN | tau_PPN | REJECT | DOCS_TEMPLATE_NOT_LIVE_INTAKE|MISSING_REQUIRED_COLUMNS:coefficient_symbol,coefficient_value,coefficient_units,normalization_convention,parent_action_block,source_path,source_anchor|SOURCE_PATH_MISSING_OR_NOT_FOUND|SOURCE_ANCHOR_MISSING_OR_NOT_FOUND | False | False |
| SCAN1566_docs_ZR1565_FINITE_ZR_SOURCE_ROW_INTAKE_REQUIREMENTS_NONCLAIM_6 | docs | REQ1565_6_tau_clock | tau_clock | REJECT | DOCS_TEMPLATE_NOT_LIVE_INTAKE|MISSING_REQUIRED_COLUMNS:coefficient_symbol,coefficient_value,coefficient_units,normalization_convention,parent_action_block,source_path,source_anchor|SOURCE_PATH_MISSING_OR_NOT_FOUND|SOURCE_ANCHOR_MISSING_OR_NOT_FOUND | False | False |
| SCAN1566_docs_ZR1565_FINITE_ZR_SOURCE_ROW_INTAKE_REQUIREMENTS_NONCLAIM_7 | docs | REQ1565_7_tau_orbital | tau_orbital | REJECT | DOCS_TEMPLATE_NOT_LIVE_INTAKE|MISSING_REQUIRED_COLUMNS:coefficient_symbol,coefficient_value,coefficient_units,normalization_convention,parent_action_block,source_path,source_anchor|SOURCE_PATH_MISSING_OR_NOT_FOUND|SOURCE_ANCHOR_MISSING_OR_NOT_FOUND | False | False |

## Runner
| runner_id | test | current_status | detail |
| --- | --- | --- | --- |
| RUN1566_0_sources | load protection/validator source chain | PASS | 1565, 1563, 1562, 1265, 1268, 1269, and 1023 sources loaded |
| RUN1566_1_protection | J_R/B_R/readout/operator protection | FAILED_CURRENT_PROOF | all four clauses remain unsigned or exact-conditional |
| RUN1566_2_joint_gate | joint second-class local gate | JOINT_PROTECTION_NOT_CLOSED | one leak is enough to leave finite q_R/Z_R residuals |
| RUN1566_3_validator | finite Z_R intake validator | PASS_NONCLAIM | docs rows are rejected and no accepted source-ready rows exist |
| RUN1566_4_claim | local GR/Newton claim | BLOCKED_NO_CLAIM | theorem-zero and finite residual scoring both remain blocked |

## Claim Gates
| gate_id | claim_gate | status | reason |
| --- | --- | --- | --- |
| GATE1566_0_JR | J_R=0 matter/source theorem | BLOCKED_NO_CLAIM | matter/no-marker descent is unsigned |
| GATE1566_1_BR | B_R=Pi_Rn=0 boundary theorem | BLOCKED_NO_CLAIM | boundary/corner no-hair is unsigned |
| GATE1566_2_readout | readout/EFT stability | BLOCKED_NO_CLAIM | readout closure is unsigned |
| GATE1566_3_operator | Z_R derivative operator exclusion | BLOCKED_NO_CLAIM | operator/object-language exclusion is not parent-signed |
| GATE1566_4_finite | finite Z_R/q_R source-row scoring | BLOCKED_NO_CLAIM | validator finds no accepted source-ready rows |
| GATE1566_5_local_GR | derived local GR/Newton/PPN safety | BLOCKED_NO_CLAIM | joint protection and finite branch are both incomplete |

## Decision
| decision_id | decision | result | reason |
| --- | --- | --- | --- |
| DEC1566_0_protection | source/boundary/readout/operator protection | FAILED_CURRENT_PARENT_PROOF | J_R, B_R, readout stability, and operator exclusion are all unsigned or exact-conditional |
| DEC1566_1_route | best current local route | RETAIN_SECOND_CLASS_CONDITIONAL_PLUS_FINITE_VALIDATOR | auxiliary route is coherent but leak protection is not closed |
| DEC1566_2_finite | finite residual branch | VALIDATOR_READY_NO_SOURCE_ROWS | finite rows are now guarded, but no real Z_R/J_R/B_R/tau row exists |
| DEC1566_3_next | next target | NEXT_1567_PARENT_PROTECTION_CONTRACT_OR_LIVE_FINITE_ZR_SOURCE_ACQUISITION | either sign the one parent protection contract or acquire source-backed finite residual rows |

## Validation
| check_id | result | detail |
| --- | --- | --- |
| VAL1566_0_sources_exist | PASS | all cited 1566 source paths exist |
| VAL1566_1_needles_found | PASS | all registered evidence needles found |
| VAL1566_2_protection_not_closed | PASS | joint protection remains open |
| VAL1566_3_joint_gate_blocks | PASS | joint gate blocks local claim |
| VAL1566_4_validator_rules | PASS | validator rejects missing markers |
| VAL1566_5_no_source_ready_rows | PASS | validator finds no accepted source-ready rows |
| VAL1566_6_docs_rejected | PASS | docs templates rejected as expected |
| VAL1566_7_runner_blocks_claim | PASS | runner blocks local claim |
| VAL1566_8_claim_gates | PASS | all claim gates remain blocked |
| VAL1566_9_decision_next | PASS | decision selects parent protection contract or live source acquisition |
| VAL1566_10_next_target | PASS | next target is parent protection contract or finite source acquisition |
| VAL1566_11_csv_parse | PASS | all generated 1566 CSVs parse cleanly |
| VAL1566_12_claim_flags_false | PASS | all generated prediction/claim flags remain false |
| VAL1566_13_branch_copies | PASS | branch/quarantine nonclaim copies written |
| VAL1566_14_pycache_absent | PASS | scripts __pycache__ absent after run |
| VAL1566_15_formalization_untouched | PASS | formalization modified-file count since start=0 |
| VAL1566_OVERALL | PASS | 1566 source/boundary/readout protection or finite ZR validator validation |

## Next Target
| next_target | script | objective | do_not |
| --- | --- | --- | --- |
| 1567-Y5-RAB-parent-protection-contract-or-live-finite-ZR-source-acquisition.md | scripts/Y5_RAB_parent_protection_contract_or_live_finite_ZR_source_acquisition.py | try to write a single parent contract that jointly proves J_R=0, B_R=0, readout stability, and operator exclusion; if that cannot be signed, start live source acquisition for finite Z_R/J_R/B_R/tau rows | do not claim local GR from separate unsigned zero conditions; do not accept docs templates as finite-ZR data; do not edit formalization-workbench |
