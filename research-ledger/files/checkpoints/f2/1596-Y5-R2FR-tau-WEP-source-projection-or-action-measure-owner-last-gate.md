# 1596 - R2/fR tau_WEP Source Projection Or Action-Measure Owner Last Gate

## Verdict
- 1596 derives the exact useful amplitude law: the 1595 MICROSCOPE anchor bounds `abs(Delta_w_TiPt*tau_WEP)`, not `Delta_w_TiPt` alone.
- Therefore `abs(Delta_w_TiPt) <= 2.8e-15/tau_min` only if a sourced lower bound `abs(tau_WEP) >= tau_min > 0` exists.
- No such `tau_min` or numeric `tau_WEP` exists in the current corpus; `tau_WEP=1` and measured-`G` absorption are explicitly rejected.
- The action-measure owner route is reopened as a last gate and still does not close: no source signs a pre-variation common action-measure package that kills `w_A`.
- No WEP, local-GR, Newton, PPN, R10, clock, orbital, beta/coupling, or public claim is made.

## Source Register

| source_id | source_path | exists | needle_found | needles |
| --- | --- | --- | --- | --- |
| SRC1596_0_1595_doc | 1595-Y5-R2FR-first-source-backed-beta-or-action-measure-owner-reopen.md | True | True | abs(Delta_w_TiPt*tau_WEP) <= 2.8e-15; NEXT_1596 |
| SRC1596_1_1595_validation | source-intake/mts_residuals/P8_Y5_BRR545_1595_VALIDATION.csv | True | True | VAL1595_OVERALL; PASS |
| SRC1596_2_1595_candidate | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1595_SOURCE_BACKED_BETA_DELTAW_CANDIDATE.csv | True | True | SBC1595_0_MICROSCOPE_Delta_w_tau_bound_anchor; BOUND_ANCHOR_ONLY_NO_MTS_PREDICTION |
| SRC1596_3_1595_next_inputs | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1595_NEXT_INPUT_REQUIREMENTS.csv | True | True | NIR1595_0_tau_WEP; source tau_WEP/readout kernel |
| SRC1596_4_1595_next_target | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1595_NEXT_TARGET.csv | True | True | 1596-Y5-R2FR-tau-WEP-source-projection-or-action-measure-owner-last-gate; tau_WEP |
| SRC1596_5_1066_tau_contract | source-intake/mts_residuals/P8_Y5_R10_1066_TAU_WEP_PROJECTION_CONTRACT.csv | True | True | TWP1066_7_verdict; PROJECTION_CONTRACT_WRITTEN_NOT_DERIVED |
| SRC1596_6_1066_prior_schema | source-intake/mts_residuals/P8_Y5_R10_1066_WEP_DELTA_W_PRIOR_WIDTH_SCHEMA.csv | True | True | DWP1066_3_finite_prior_width; blocked_by_tau_WEP |
| SRC1596_7_1224_finite_weight_contract | source-intake/mts_residuals/P8_Y5_R10_1224_FINITE_SOURCE_WEIGHT_INPUT_CONTRACT.csv | True | True | FSW1224_2_tau_WEP; MISSING_LAB_SOURCE_ORBIT_PROJECTION |
| SRC1596_8_1225_symbolic_tau_formula | source-intake/mts_residuals/P8_Y5_R10_1225_SYMBOLIC_TAU_WEP_FORMULA.csv | True | True | FORM1225_0_tau_WEP_functional; SYMBOLIC_ONLY_NONCLAIM |
| SRC1596_9_1225_tau_projection_attempt | source-intake/mts_residuals/P8_Y5_R10_1225_TAU_WEP_PROJECTION_ATTEMPT.csv | True | True | TAU1225_6_verdict; TAU_WEP_PROJECTION_NOT_DERIVED |
| SRC1596_10_1482_tau_readiness | source-intake/mts_residuals/P8_Y5_R10_1482_TAU_WEP_READINESS_UPDATE.csv | True | True | TAU1482_7_numeric_tau; NOT_EVALUATED |
| SRC1596_11_1083_source_caveat | source-intake/mts_residuals/P8_Y5_R10_1083_SOURCE_VECTOR_CAVEAT_GATE.csv | True | True | SCG1083_0_profile_weighting; MISSING_SOURCE_PROFILE_WEIGHTING |
| SRC1596_12_1084_readout_gate | source-intake/mts_residuals/P8_Y5_R10_1084_MICROSCOPE_READOUT_IMPORT_GATE.csv | True | True | RIG1084_0_CMSM_arrays; OFFICIAL_ARRAYS_NOT_IMPORTED |
| SRC1596_13_1078_action_measure | source-intake/mts_residuals/P8_Y5_R10_1078_ACTION_MEASURE_PROOF_ATTEMPT.csv | True | True | AM1078_4_verdict; ACTION_MEASURE_NOT_SIGNED |
| SRC1596_14_1452_common_measure | source-intake/mts_residuals/P8_Y5_R10_1452_COMMON_MEASURE_CURRENT_THEOREM_ATTEMPT.csv | True | True | CMT1452_6_verdict; FAIL_CURRENT_PROOF_NOT_PARENT_SIGNED |
| SRC1596_15_1453_current_source | source-intake/mts_residuals/P8_Y5_R10_1453_CURRENT_SOURCE_NORMALIZATION_OWNER_THEOREM_ATTEMPT.csv | True | True | CSO1453_7_verdict; PARTIAL_THEOREM_NOT_CLOSED |

## tau_WEP Contraction Law

| law_id | object | statement | derivation_status | conditions |
| --- | --- | --- | --- | --- |
| TCL1596_0_linearized_observable | MICROSCOPE Ti/Pt Eotvos channel | eta_TiPt = Delta_w_TiPt * tau_WEP + O((Delta_w_TiPt*tau_WEP)^2) in the weak finite-source branch | CONDITIONAL_LINEAR_CONTRACTION_DERIVED | same parent branch; weak residual; absolute-product guard; no measured-G absorption; no signed cancellation model |
| TCL1596_1_product_bound | P_WEP_relative_source_weight | abs(Delta_w_TiPt * tau_WEP) <= 2.8e-15 | SOURCE_BACKED_PRODUCT_BOUND_FROM_1595 | MICROSCOPE bound anchor only; tau_WEP not evaluated; Delta_w_TiPt not individually bounded |
| TCL1596_2_delta_w_amplitude_law | Delta_w_TiPt | if abs(tau_WEP) >= tau_min > 0 then abs(Delta_w_TiPt) <= 2.8e-15/tau_min | EXACT_CONDITIONAL_AMPLITUDE_LAW | requires sourced nonzero lower bound tau_min; upper bound on tau alone is insufficient |
| TCL1596_3_tau_null_escape | tau_WEP | if tau_WEP can vanish or be arbitrarily small, the MICROSCOPE product bound gives no finite Delta_w_TiPt bound | NO_SHORTCUT_THEOREM | cannot set tau_WEP=1 by convention; cannot hide missing source projection inside measured G |

## tau_WEP Factor Audit

| factor_id | factor | current_status | source | effect_on_tau |
| --- | --- | --- | --- | --- |
| TFA1596_0_source_worldtube | R_source or T_source^Earth(x) | MISSING_SOURCE_PROFILE_WEIGHTING | P8_Y5_R10_1083_SOURCE_VECTOR_CAVEAT_GATE.csv:SCG1083_0_profile_weighting | tau_WEP cannot be numeric and no tau_min lower bound exists |
| TFA1596_1_orbit_average | orbit/session/mask average | MISSING_ORBIT_AVERAGE_ARRAYS | P8_Y5_R10_1225_TAU_WEP_PROJECTION_ATTEMPT.csv:TAU1225_1_orbit_average | normalization of tau_WEP remains open |
| TFA1596_2_observed_coframe | e_obs/readout frame | CONDITIONAL_FROM_PRIOR_SPINE | P8_Y5_R10_1066_TAU_WEP_PROJECTION_CONTRACT.csv:TWP1066_2_observed_coframe | frame consistency is conditional, not a claim |
| TFA1596_3_material_tensor | Ti/Pt material response | MISSING_FULL_MATERIAL_TENSOR | P8_Y5_R10_1482_TAU_WEP_READINESS_UPDATE.csv:TAU1482_6_material_tensor | Delta_w_TiPt mapping remains incomplete |
| TFA1596_4_readout_matrix | K_MICROSCOPE / K_CMSM | OFFICIAL_ARRAYS_NOT_IMPORTED | P8_Y5_R10_1084_MICROSCOPE_READOUT_IMPORT_GATE.csv:RIG1084_0_CMSM_arrays | no surrogate kernel can promote a WEP claim |
| TFA1596_5_product_convention | eta product normalization | NORMALIZATION_NOT_FILLED | P8_Y5_R10_1084_MICROSCOPE_READOUT_IMPORT_GATE.csv:RIG1084_1_product_convention | tau_WEP=1 shortcut remains forbidden |
| TFA1596_6_parent_coupling_slot | C_parent or action-measure owner | MISSING_C_PARENT_IMPORT | P8_Y5_R10_1482_TAU_WEP_READINESS_UPDATE.csv:TAU1482_5_C_parent | finite branch cannot be promoted to parent-derived local GR |

## Action-Measure Owner Last Gate

| gate_id | route | required_signature | result | effect |
| --- | --- | --- | --- | --- |
| AMG1596_0_common_measure_theorem | zero theorem | single parent-owned action measure/coframe for all matter sectors before variation | UNSIGNED | cannot set w_A=0 |
| AMG1596_1_current_owner_theorem | post-variation current ownership | all effective currents descend from the same parent quotient with no representative weights | PARTIAL_NOT_CLOSING_PRE_VARIATION_W_A | current owner does not kill pre-variation action weights |
| AMG1596_2_classical_equation_route | classical EOM / source equation | EOM removes every representative action/source weight rather than just moving it | DOES_NOT_EXCLUDE_W_A | finite source-weight branch remains necessary |
| AMG1596_3_last_gate_verdict | action-measure owner last gate | parent-signed common action measure plus quotient-invariant matter descent | ACTION_MEASURE_OWNER_LAST_GATE_NOT_CLOSED | 1596 must proceed through tau_WEP source projection/lower-bound route |

## Delta_w Bound Status

| bound_id | quantity | bound_statement | status | numeric_value |
| --- | --- | --- | --- | --- |
| DWB1596_0_product_anchor | abs(Delta_w_TiPt * tau_WEP) | <= 2.8e-15 | AVAILABLE_FROM_1595 | 2.8e-15 |
| DWB1596_1_tau_value | tau_WEP | numeric value or lower bound required | NOT_EVALUATED | not_available |
| DWB1596_2_tau_lower_bound | tau_min | need abs(tau_WEP) >= tau_min > 0 | NO_TAU_MIN_SOURCE | not_available |
| DWB1596_3_delta_w_bound | abs(Delta_w_TiPt) | if tau_min exists, abs(Delta_w_TiPt) <= 2.8e-15/tau_min | SYMBOLIC_ONLY_NO_NUMERIC_DELTA_W | not_available |

## tau Source Acquisition Rows

| acq_id | needed_file_or_object | required_fields | acceptance_gate | priority | status |
| --- | --- | --- | --- | --- | --- |
| TSA1596_0_readout_matrix | P_WEP_K_CMSM_readout.csv | time; segment/session id; gx; gz; Sxx; Sxz; masks; calibration flags; attitude/orbit convention; units | no surrogate-only matrix may claim WEP | highest | SOURCE_NEEDED |
| TSA1596_1_source_worldtube | P_WEP_R_source_Earth_worldtube.csv | radius/depth shell; density/stress proxy; composition/source response; orbit/source kernel convention; units | bulk composition alone is not enough | highest | SOURCE_NEEDED |
| TSA1596_2_material_tensor | P_WEP_TiPt_material_response_tensor.csv | TA6V response; PtRh10 response; source-weight convention; uncertainty; provenance | alloy labels alone are not a response tensor | high | SOURCE_NEEDED |
| TSA1596_3_tau_min | P_WEP_tau_min_lower_bound.csv | tau_min; confidence; derivation/source path; sign/absolute convention; assumptions | must be strictly positive; tau_WEP=1 convention is forbidden | highest | DERIVATION_OR_SOURCE_NEEDED |
| TSA1596_4_action_measure_owner | parent_action_measure_owner_theorem | common measure; coframe; quotient descent; no representative w_A; boundary terms controlled | must be parent-signed, not post-variation redefinition | highest_parallel_route | DERIVATION_NEEDED |

## Runner Refusal

| runner_id | acceptance_rule | input_state | runner_result | effect |
| --- | --- | --- | --- | --- |
| RUN1596_0_product_anchor | accept 1595 MICROSCOPE product bound as source-backed bound input | abs(Delta_w_TiPt*tau_WEP) <= 2.8e-15 | ACCEPT_PRODUCT_BOUND_ONLY | kept as private nonclaim bound anchor |
| RUN1596_1_delta_w_score | numeric Delta_w bound requires tau_WEP or tau_min | tau_WEP not evaluated; no tau_min | REJECT_NUMERIC_DELTA_W_SCORE | no WEP/local-GR score produced |
| RUN1596_2_action_measure_zero | Delta_w=0 requires parent-signed action-measure owner | last gate not closed | REJECT_ZERO_THEOREM_CLAIM | finite source-weight route remains open |
| RUN1596_3_local_gr | local GR requires zero theorem or all finite residuals bounded below test thresholds | tau source projection incomplete | BLOCK_LOCAL_GR_CLAIM | continue derivation/source acquisition |

## Claim Gates

| gate_id | claim | status | reason |
| --- | --- | --- | --- |
| CG1596_0_WEP | MTS passes MICROSCOPE/WEP | BLOCKED | product anchor exists but tau_WEP/source/readout projection is not numeric |
| CG1596_1_Delta_w | finite bound on Delta_w_TiPt | BLOCKED | needs tau_min>0 or tau_WEP numeric value |
| CG1596_2_action_measure | action-measure owner kills w_A | BLOCKED | last gate not parent-signed |
| CG1596_3_local_GR | derived local GR branch | BLOCKED | source-weight/coupling residual still open |

## Decision

| decision_id | decision | reason | next_action |
| --- | --- | --- | --- |
| DEC1596_0_math_progress | PRODUCT_TO_DELTA_W_LAW_DERIVED | the 1595 bound becomes a Delta_w constraint only through a nonzero tau_WEP lower bound | hunt tau_min or close action-measure owner |
| DEC1596_1_no_shortcut | TAU_UNITY_SHORTCUT_REJECTED | tau_WEP is a physical projection, not a convention; measured-G absorption would hide the residual | source readout/source/worldtube factors |
| DEC1596_2_owner_status | ACTION_MEASURE_OWNER_LAST_GATE_NOT_CLOSED | current-owner and common-measure evidence does not remove pre-variation w_A | keep finite branch open |
| DEC1596_3_next | NEXT_1597_TAU_LOWER_BOUND_OR_COUPLING_ZERO_PROOF | that is the cleanest route to make the MICROSCOPE product anchor actionable | derive tau_min>0 from geometry/readout or derive coupling/action-measure zero theorem |

## Next Target

| next_target | script | objective | success_condition | do_not |
| --- | --- | --- | --- | --- |
| 1597-Y5-R2FR-tau-lower-bound-or-coupling-zero-proof.md | scripts/Y5_R2FR_tau_lower_bound_or_coupling_zero_proof.py | derive a strictly positive tau_WEP lower bound from source/readout geometry, or close the parent coupling/action-measure zero theorem | tau_min>0 with source paths, or parent-signed Delta_w_TiPt=0 theorem; otherwise WEP remains product-bound only | do not set tau_WEP=1, do not score WEP from the product anchor alone, do not use measured-G absorption, do not edit formalization-workbench |

## Validation

| check_id | result | detail |
| --- | --- | --- |
| VAL1596_0_sources_exist | PASS | all cited 1596 source paths exist |
| VAL1596_1_needles_found | PASS | all required source needles found |
| VAL1596_2_product_law | PASS | MICROSCOPE product bound retained |
| VAL1596_3_amplitude_law | PASS | conditional Delta_w amplitude law recorded |
| VAL1596_4_tau_null_guard | PASS | tau vanishing escape blocks finite Delta_w bound |
| VAL1596_5_tau_factors_block | PASS | tau factor audit remains nonclaim |
| VAL1596_6_action_last_gate_blocks | PASS | action-measure owner last gate not closed |
| VAL1596_7_delta_w_not_numeric | PASS | Delta_w bound remains symbolic |
| VAL1596_8_acquisition_requires_tau_min | PASS | tau_min acquisition row exists |
| VAL1596_9_runner_refuses_score | PASS | runner rejects numeric Delta_w score |
| VAL1596_10_claim_gates_closed | PASS | all claim gates remain closed |
| VAL1596_11_decision_next | PASS | decision selects 1597 tau lower-bound/coupling-zero target |
| VAL1596_12_csv_parse | PASS | all generated 1596 CSVs parse |
| VAL1596_13_claim_safety_flags | PASS | no generated 1596 rows are score-ready, prediction rows, or claim-allowed |
| VAL1596_14_branch_copies | PASS | branch/quarantine nonclaim copies exist |
| VAL1596_15_pycache_absent | PASS | scripts __pycache__ absent |
| VAL1596_16_formalization_untouched | PASS | no 1596 outputs found under formalization-workbench |
| VAL1596_OVERALL | PASS | 1596 tau-WEP projection or action-measure owner last-gate validation |
