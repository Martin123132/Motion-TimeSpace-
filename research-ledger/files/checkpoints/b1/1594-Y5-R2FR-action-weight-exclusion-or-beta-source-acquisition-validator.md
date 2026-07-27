# 1594 - R2/fR Action-Weight Exclusion Or Beta Source Acquisition Validator

## Verdict
- 1594 tries to kill the pre-variation `w_A` source/action-weight counterexample directly. The proof route is sharp, but still **not parent-signed**.
- Classical matter equations do not remove `w_A`: the metric/Hilbert variation inherits it. Current-owner arguments kill post-variation rescalings only after a common action is fixed; they do not kill weights already inside `S_matter`.
- The missing theorem package is now precise: no-source-only parent grammar, common action measure, source-label forgetting, Hilbert/current owner, non-Hilbert silence, readout order, and common-`G_N` absorption guard.
- Since the theorem still does not close, 1594 adds a strict beta-row validator. It rejects every current 1593 beta row because they are nonclaim templates lacking source paths, anchors, extraction method, beta convention, and arena maps.
- No local-GR, Newton, PPN, R10, WEP, clock, orbital, beta, action-weight, measured-`G`, or public claim is made.

## Source Register

| source_id | source_path | exists | needle_found | needles |
| --- | --- | --- | --- | --- |
| SRC1594_0_1593_doc | 1593-Y5-R2FR-canonical-coupling-zero-theorem-or-finite-beta-source-rows.md | True | True | NEXT_1594_ACTION_WEIGHT_EXCLUSION_OR_BETA_SOURCE_ACQUISITION_VALIDATOR; w_A |
| SRC1594_1_1593_validation | source-intake/mts_residuals/P8_Y5_BRR545_1593_VALIDATION.csv | True | True | VAL1593_OVERALL; PASS |
| SRC1594_2_1593_beta_rows | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1593_FINITE_BETA_SOURCE_ROWS.csv | True | True | FBR1593_11_verdict; FINITE_BETA_SOURCE_ROWS_READY_NONCLAIM |
| SRC1594_3_1593_source_residual | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1593_ACTION_WEIGHT_SOURCE_RESIDUAL.csv | True | True | SWR1593_6_verdict; SOURCE_RESIDUAL_VECTOR_READY_NONCLAIM |
| SRC1594_4_1066_source_scalar | source-intake/mts_residuals/P8_Y5_R10_1066_SOURCE_SCALAR_EXCLUSION_LEMMA.csv | True | True | SSE1066_5_verdict; CONDITIONAL_SOURCE_SCALAR_EXCLUSION_NOT_PARENT_DERIVED |
| SRC1594_5_1066_field_measure | source-intake/mts_residuals/P8_Y5_R10_1066_FIELD_MEASURE_QUANTUM_NORMALIZATION_AUDIT.csv | True | True | FMQ1066_4_verdict; NOT_PARENT_SIGNED |
| SRC1594_6_1078_object_language | source-intake/mts_residuals/P8_Y5_R10_1078_OBJECT_LANGUAGE_PROOF_ATTEMPT.csv | True | True | OL1078_4_verdict; OBJECT_LANGUAGE_NOT_SIGNED |
| SRC1594_7_1078_action_measure | source-intake/mts_residuals/P8_Y5_R10_1078_ACTION_MEASURE_PROOF_ATTEMPT.csv | True | True | AM1078_4_verdict; ACTION_MEASURE_NOT_SIGNED |
| SRC1594_8_1078_current_owner | source-intake/mts_residuals/P8_Y5_R10_1078_CURRENT_OWNER_PROOF_ATTEMPT.csv | True | True | CO1078_4_verdict; CURRENT_OWNER_NOT_SIGNED |
| SRC1594_9_1079_narrow_current | source-intake/mts_residuals/P8_Y5_R10_1079_NARROW_CURRENT_OWNER_THEOREM_ATTEMPT.csv | True | True | NCO1079_6_verdict; NARROW_CURRENT_OWNER_PARTIAL_NOT_WEP_CLOSED |
| SRC1594_10_1224_owner_clauses | source-intake/mts_residuals/P8_Y5_R10_1224_OWNER_PROOF_CLAUSES.csv | True | True | OWN1224_6_verdict; SOURCE_WEIGHT_OWNER_PROOF_NOT_DERIVED |
| SRC1594_11_1224_weight_obstruction | source-intake/mts_residuals/P8_Y5_R10_1224_SOURCE_WEIGHT_OBSTRUCTION_LEDGER.csv | True | True | OBS1224_0_wA_action_multiplier; valid_for_claim |
| SRC1594_12_1229_source_contract | source-intake/mts_residuals/P8_Y5_R10_1229_LOCAL_GR_SOURCE_COUPLING_THEOREM_CONTRACT.csv | True | True | THM1229_2_countermodel; OBSTRUCTION_ACTIVE |
| SRC1594_13_1229_counterexamples | source-intake/mts_residuals/P8_Y5_R10_1229_SOURCE_COUPLING_COUNTEREXAMPLE_LEDGER.csv | True | True | CEX1229_0_action_multiplier; ACTIVE |
| SRC1594_14_1229_clause_audit | source-intake/mts_residuals/P8_Y5_R10_1229_UNIVERSAL_SOURCE_COUPLING_CLAUSE_AUDIT.csv | True | True | CLC1229_8_verdict; NOT_CLOSED |
| SRC1594_15_1387_action_weight | source-intake/mts_residuals/P8_Y5_R10_1387_ACTION_WEIGHT_EXCLUSION_AUDIT.csv | True | True | AWE1387_7_verdict; COUNTEREXAMPLE_SURVIVES_FIRST_FILL_REQUIRED |
| SRC1594_16_1387_beta_fill | source-intake/mts_residuals/P8_Y5_R10_1387_DELTA_W_SOURCE_BETA_FIRST_FILL.csv | True | True | DWB1387_6_first_fill_verdict; NONCLAIM_FIRST_FILL_READY |
| SRC1594_17_1450_hilbert_label | source-intake/mts_residuals/P8_Y5_R10_1450_HILBERT_SOURCE_LABEL_FORGETTING_THEOREM_ATTEMPT.csv | True | True | HT1450_6_verdict; CONDITIONAL_THEOREM_NOT_PARENT_DERIVED |
| SRC1594_18_1451_operator_grammar | source-intake/mts_residuals/P8_Y5_R10_1451_NO_SOURCE_ONLY_SLOT_OPERATOR_GRAMMAR_THEOREM_ATTEMPT.csv | True | True | OG1451_6_verdict; FAIL_CURRENT_PROOF_NOT_PARENT_SIGNED |
| SRC1594_19_1452_common_measure | source-intake/mts_residuals/P8_Y5_R10_1452_COMMON_MEASURE_CURRENT_THEOREM_ATTEMPT.csv | True | True | CMT1452_6_verdict; FAIL_CURRENT_PROOF_NOT_PARENT_SIGNED |
| SRC1594_20_1453_current_source | source-intake/mts_residuals/P8_Y5_R10_1453_CURRENT_SOURCE_NORMALIZATION_OWNER_THEOREM_ATTEMPT.csv | True | True | CSO1453_7_verdict; PARTIAL_THEOREM_NOT_CLOSED |
| SRC1594_21_1584_gr_runner | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1584_GR_REDUCTION_RUNNER.csv | True | True | RUN1584_4_local_gr; BLOCKED_NO_CLAIM |

## Action-Weight Exclusion Theorem Attempt

| theorem_id | clause | formal_statement | would_close | status | blocking_gap |
| --- | --- | --- | --- | --- | --- |
| AWT1594_0_target | exclude independent pre-variation source weights | Allowed[S_matter] = sum_A S_A[Psi_A,e_obs(q),A_Q,theta_A] with no independent w_A S_A source/action multiplier. | Would kill Delta_w_A, beta_w_A and the cleanest source-normalization obstruction. | TARGET_SHARPENED | requires parent grammar, action-measure and current-owner premises together |
| AWT1594_1_classical_EOM_rejection | isolated classical equations cannot kill w_A | delta(w_A S_A)/delta Psi_A=0 can have the same form as delta S_A/delta Psi_A=0 while delta(w_A S_A)/delta g = w_A T_A. | Prevents fake derivation by free-fall/classical dynamics alone. | SHORTCUT_REJECTED | source variation still sees w_A |
| AWT1594_2_object_language | no source-only slot | A species-indexed inert scalar with no field/current/representation/geometry type should not be an admissible parent argument. | Would make partial S_matter/partial w_A undefined rather than merely small. | CONDITIONAL_NOT_PARENT_SIGNED | absence of a slot is still a parent grammar theorem, not derived from covariance alone |
| AWT1594_3_common_action_measure | single hbar/action-measure owner | One parent action scale and matter measure would make independent exp(i w_A S_A/hbar_parent) factors inadmissible. | Would kill relative action weights and species Jacobian source weights. | CONDITIONAL_ROUTE_CLEAN_NOT_SIGNED | no parent statistical/path-integral measure owner is signed |
| AWT1594_4_current_owner_limit | Hilbert current before readout | T_H is unique once one common action is fixed and varied before readout. | Kills post-variation source rescalings conditionally. | PARTIAL_THEOREM_ONLY | T_H inherits w_A if w_A is already inside S_matter before variation |
| AWT1594_5_naturality_limit | connected ordinary matter category | Naturality can force a common scalar only if ordinary matter components are connected by parent morphisms. | Helpful if signed, but disconnected simple components can carry independent constants. | HELPFUL_CONDITIONAL_ONLY | connectedness of ordinary matter category not derived |
| AWT1594_6_nonHilbert_bypass | no non-Hilbert source bypass | J_src = kappa T_Hilbert plus possible non-Hilbert currents must have all zeta_A zero/exact/projected-silent. | Prevents spin/torsion/boundary/current bypass of the Hilbert theorem. | PARALLEL_GATE_OPEN | non-Hilbert current absence/silence not proven |
| AWT1594_7_verdict | action-weight exclusion theorem | No-source-only-slot + common action-measure + current owner + label forgetting + non-Hilbert silence would imply w_A=w_star or null-projected. | The route is exact as a contract, but current corpus does not parent-sign it. | ACTION_WEIGHT_EXCLUSION_NOT_DERIVED_VALIDATOR_REQUIRED | use strict beta/source validator until the parent theorem closes |

## Common Measure Current Audit

| audit_id | required_clause | source_basis | current_status | effect_if_open |
| --- | --- | --- | --- | --- |
| CMC1594_0_single_action_scale | one universal action scale/hbar | FMQ1066/AM1078/CMT1452 | NOT_PARENT_SIGNED | Delta_w_A cannot be set to zero |
| CMC1594_1_species_blind_measure | species-blind measure and Jacobian | CMT1452 species Jacobian countermodel | COUNTERMODEL_SURVIVES | measure-induced weights retained |
| CMC1594_2_label_forgetting | source functor forgets species labels before coupling | HT1450 conditional uniqueness | CONDITIONAL_NOT_PARENT_DERIVED | relative kappa_A can be formed if labels survive |
| CMC1594_3_hilbert_current_owner | Hilbert source is varied before readout | NCO1079/CSO1453 exact conditional subtheorem | CONDITIONAL_PARTIAL_ONLY | post-variation rescaling controlled, pre-variation w_A survives |
| CMC1594_4_no_nonhilbert_current | no spin/torsion/boundary/non-Hilbert source bypass | HT1450/CSO1453 non-Hilbert guard | PARALLEL_GATE_OPEN | zeta_A finite rows retained |
| CMC1594_5_readout_order | readout cannot retroactively redefine source | SSE1066/NCO1079 variation-before-readout | CONTRACT_WRITTEN_NOT_DERIVED | readout tails retained |
| CMC1594_6_common_G_absorption | only common derivative-silent w_star can be absorbed into G_N | CLC1229/DWB1387 measured-G guard | GUARD_ACTIVE_INPUTS_MISSING | relative or phi-dependent weights are physics |
| CMC1594_7_verdict | common measure/current owner | CMT1452/CSO1453 verdicts | COMMON_MEASURE_CURRENT_NOT_DERIVED | strict finite-row validation required |

## Beta Validator Spec

| spec_id | field_or_gate | requirement | failure_rule |
| --- | --- | --- | --- |
| BVS1594_0_branch | same_parent_branch_id | must equal MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | reject mismatched branch or blank branch |
| BVS1594_1_identity | quantity;definition | must declare source/test leg, product, weight, kernel, or tail with explicit convention | reject vague coupling symbols |
| BVS1594_2_units | required_units | must be concrete beta, dimensionless, kernel, or arena residual units | reject missing or placeholder units |
| BVS1594_3_source | source_path;source_anchor;extraction_method | must cite a local source and how the value/theorem was obtained | reject missing, toy, proxy, or unsourced rows |
| BVS1594_4_beta_convention | beta_convention | must state canonical normalization and whether source/test legs are already packed | reject linear-coupling shortcuts |
| BVS1594_5_arena | arena_map;observable_links | must name R10/PPN/WEP/clock/orbital/Newton map and kernel role | reject no-arena rows |
| BVS1594_6_status | current_status | must be SOURCE_BACKED_NUMERIC, THEOREM_ZERO_PARENT_SIGNED, or EXPLICIT_BOUND_SOURCE_BACKED | reject MISSING, TEMPLATE, NONCLAIM, TOY, PLACEHOLDER |
| BVS1594_7_flags | valid_for_claim;claim_allowed;score_ready | may be true only if all previous gates pass | default false |
| BVS1594_8_no_absorption | measured_G_guard | must prove common derivative-silent factor before any G_N absorption | reject relative or phi-dependent absorption |
| BVS1594_9_verdict | validator policy | strict validator is ready and should be used before every local score | current 1593 beta rows are expected to fail |

## Beta Validator Results

| validation_id | input_row_id | quantity | input_status | validator_result | missing_required_fields | bad_markers |
| --- | --- | --- | --- | --- | --- | --- |
| BVR1594_0_FBR1593_0_beta_source | FBR1593_0_beta_source | beta_source | MISSING_SOURCE_BETA | REJECT | source_path;source_anchor;extraction_method;beta_convention;arena_map | MISSING;VALID_FOR_CLAIM_FALSE |
| BVR1594_1_FBR1593_1_beta_test | FBR1593_1_beta_test | beta_test | MISSING_TEST_BETA | REJECT | source_path;source_anchor;extraction_method;beta_convention;arena_map | MISSING;VALID_FOR_CLAIM_FALSE |
| BVR1594_2_FBR1593_2_beta_product | FBR1593_2_beta_product | beta_source*beta_test | PRODUCT_FORMULA_READY_VALUES_MISSING | REJECT | source_path;source_anchor;extraction_method;beta_convention;arena_map | MISSING;VALID_FOR_CLAIM_FALSE |
| BVR1594_3_FBR1593_3_beta_geom | FBR1593_3_beta_geom | beta_geom | MISSING_GEOMETRY_OR_SHADOW_FRAME_ROW | REJECT | source_path;source_anchor;extraction_method;beta_convention;arena_map | MISSING;VALID_FOR_CLAIM_FALSE |
| BVR1594_4_FBR1593_4_beta_const | FBR1593_4_beta_const | beta_const | MISSING_CONSTANT_SUPERSELECTION_OR_ROW | REJECT | source_path;source_anchor;extraction_method;beta_convention;arena_map | MISSING;VALID_FOR_CLAIM_FALSE |
| BVR1594_5_FBR1593_5_beta_weight_source | FBR1593_5_beta_weight_source | beta_w_source | MISSING_SOURCE_BETA_WEIGHT_FUNCTION | REJECT | source_path;source_anchor;extraction_method;beta_convention;arena_map | MISSING;VALID_FOR_CLAIM_FALSE |
| BVR1594_6_FBR1593_6_beta_weight_test | FBR1593_6_beta_weight_test | beta_w_test | MISSING_TEST_BETA_WEIGHT_FUNCTION | REJECT | source_path;source_anchor;extraction_method;beta_convention;arena_map | MISSING;VALID_FOR_CLAIM_FALSE |
| BVR1594_7_FBR1593_7_Delta_w_A | FBR1593_7_Delta_w_A | Delta_w_A | FIRST_FILL_ROW_READY_VALUE_MISSING | REJECT | source_path;source_anchor;extraction_method;beta_convention;arena_map | MISSING;VALID_FOR_CLAIM_FALSE |
| BVR1594_8_FBR1593_8_K_profile | FBR1593_8_K_profile | K_arena(lambda) | MISSING_PROFILE_KERNEL | REJECT | source_path;source_anchor;extraction_method;beta_convention;arena_map | MISSING;VALID_FOR_CLAIM_FALSE |
| BVR1594_9_FBR1593_9_epsilon_tail | FBR1593_9_epsilon_tail | epsilon_tail | MISSING_TAIL_ENVELOPE | REJECT | source_path;source_anchor;extraction_method;beta_convention;arena_map | MISSING;VALID_FOR_CLAIM_FALSE |
| BVR1594_10_FBR1593_10_beta_acceptance | FBR1593_10_beta_acceptance | finite beta row acceptance rule | ACCEPTANCE_CONTRACT_READY_NO_ROW_ACCEPTED | REJECT | source_path;source_anchor;extraction_method;beta_convention;arena_map | MISSING;TOY;VALID_FOR_CLAIM_FALSE |
| BVR1594_11_FBR1593_11_verdict | FBR1593_11_verdict | finite beta acquisition pack | FINITE_BETA_SOURCE_ROWS_READY_NONCLAIM | REJECT | source_path;source_anchor;extraction_method;beta_convention;arena_map | NONCLAIM;VALID_FOR_CLAIM_FALSE |
| BVR1594_VERDICT | aggregate_1593_finite_beta_rows | all_beta_rows | aggregate | NO_ACCEPTED_BETA_ROWS | source_path;source_anchor;extraction_method;beta_convention;arena_map | MISSING;NONCLAIM;VALID_FOR_CLAIM_FALSE |

## Beta Source Acquisition Queue

| queue_id | quantity | required_source | arena_links | priority | why_next |
| --- | --- | --- | --- | --- | --- |
| BSQ1594_0_beta_source | beta_source | source worldtube plus matter descent map | R10;Newton;WEP | high | source/test product cannot score without source leg |
| BSQ1594_1_beta_test | beta_test | test-body matter action and material response map | R10;WEP;clock;orbital | high | source/test product cannot score without test leg |
| BSQ1594_2_Delta_w_A | Delta_w_A | action-weight exclusion theorem or finite source/material bound | Newton;common matter;WEP | highest | kills or quantifies w_A gremlin |
| BSQ1594_3_beta_w | beta_w_source;beta_w_test | phi-dependence of source/test action weights | R10;PPN;WEP | high | finite scalar exchange if w_A(phi) survives |
| BSQ1594_4_K_arena | K_arena(lambda) | arena kernel with mu_m2, source/test geometry and no double counting | R10;PPN;clock;orbital | medium | data scoring waits until beta legs exist |
| BSQ1594_5_epsilon_tail | epsilon_tail | boundary/readout/projector/non-Hilbert/CDB tail envelope | all local arenas | high | prevents fake zero by ignoring tails |
| BSQ1594_6_measured_G_guard | measured_G_guard | common derivative-silent proof for any absorbed factor | Newton;PPN;WEP | highest | blocks calibration cheating |
| BSQ1594_7_verdict | acquisition_order | prove action-weight exclusion first; otherwise acquire beta/Delta_w rows before arena kernels | all | decision | least-scrutiny order selected |

## Runner Refusal

| runner_id | acceptance_rule | input_state | runner_result | effect |
| --- | --- | --- | --- | --- |
| RUN1594_0_action_weight_theorem | accept w_A exclusion only if object-language, action-measure, current-owner, label-forgetting and non-Hilbert gates close | AWT1594 verdict is not derived | REJECT_ACTION_WEIGHT_ZERO_CLAIM | finite Delta_w/beta_w rows remain mandatory |
| RUN1594_1_beta_validator | accept beta rows only if strict validator returns ACCEPT | BVR1594 verdict has no accepted beta rows | REJECT_ALL_CURRENT_BETA_ROWS | no local empirical scoring |
| RUN1594_2_measured_G | accept G_N absorption only for common derivative-silent w_star | relative/phi/source weights remain unsourced | REJECT_MEASURED_G_ABSORPTION_SHORTCUT | Newton/common matter blocked |
| RUN1594_3_local_GR | accept local GR only after action weights/beta/current/conservation/Newton gates close | 1584 and 1593 still block local GR | REJECT_LOCAL_GR_REENTRY | continue derivation/source acquisition |
| RUN1594_4_next | next run should either prove action-measure owner or source first beta rows | validator exists but has no accepted inputs | WAIT_FOR_THEOREM_OR_SOURCE_ROWS | do not score yet |

## Claim Gates

| gate_id | claim | status | reason |
| --- | --- | --- | --- |
| GATE1594_0_action_weight | action-weight exclusion theorem | BLOCKED_NO_CLAIM | parent grammar/action-measure/current-owner package not signed |
| GATE1594_1_beta_validation | finite beta/source row score | BLOCKED_NO_CLAIM | strict validator accepts no current beta rows |
| GATE1594_2_measured_G | absorb source weights into measured G_N | BLOCKED_NO_CLAIM | relative or phi-dependent weights are physics unless common derivative-silent proof exists |
| GATE1594_3_Newton | Newton source normalization | BLOCKED_NO_CLAIM | Delta_w/common current gates open |
| GATE1594_4_R10_PPN_WEP | R10/PPN/WEP score | BLOCKED_NO_CLAIM | beta legs, kernels and tails are missing |
| GATE1594_5_local_GR | local GR reduction | BLOCKED_NO_CLAIM | source/coupling/conservation gates do not close together |

## Decision

| decision_id | decision | reason | next_action |
| --- | --- | --- | --- |
| DEC1594_0_theorem_status | ACTION_WEIGHT_EXCLUSION_NOT_DERIVED | all proof routes are sharp but remain unsigned; current owner kills post-variation tricks only, not pre-variation w_A | keep w_A as live finite source residual |
| DEC1594_1_validator_status | STRICT_BETA_VALIDATOR_NOW_EXISTS | current beta rows fail because they are templates lacking source paths, anchors, extraction method, beta convention and arena maps | run validator before any local R10/PPN/WEP/clock/orbital score |
| DEC1594_2_best_route | SOURCE_FIRST_ROWS_BEFORE_ARENA_KERNELS | arena kernels are useless until beta_source, beta_test, Delta_w and measured-G guard have source-backed rows or theorem-zero certificates | source beta/Delta_w rows or prove action-measure owner next |
| DEC1594_3_next | NEXT_1595_FIRST_SOURCE_BACKED_BETA_OR_ACTION_MEASURE_OWNER_REOPEN | the next useful checkpoint should either close the parent action-measure owner or fill the first source-backed beta/Delta_w row that the validator can inspect | attempt action-measure owner one more time from parent primitives, otherwise build first acquisition row |

## Validation

| check_id | result | detail |
| --- | --- | --- |
| VAL1594_0_sources_exist | PASS | all cited 1594 source paths exist |
| VAL1594_1_needles_found | PASS | all 1594 source needles found |
| VAL1594_2_action_weight_not_derived | PASS | action-weight exclusion theorem remains unsigned |
| VAL1594_3_measure_current_not_derived | PASS | common measure/current owner remains unsigned |
| VAL1594_4_validator_spec_complete | PASS | strict beta validator policy is present |
| VAL1594_5_validator_rejects_current_rows | PASS | current 1593 beta rows are rejected as nonclaim templates |
| VAL1594_6_acquisition_queue_present | PASS | beta/Delta_w acquisition queue is present |
| VAL1594_7_runner_rejects_claims | PASS | runner refuses theorem, beta and measured-G shortcuts |
| VAL1594_8_claim_gates_closed | PASS | all 1594 claim gates remain closed |
| VAL1594_9_decision_next | PASS | decision selects action-measure owner reopen or first source-backed beta row |
| VAL1594_10_csv_parse | PASS | all generated 1594 CSVs parse cleanly |
| VAL1594_11_claim_flags_false | PASS | all generated claim/prediction/theorem flags remain false |
| VAL1594_12_no_raw_accepted | PASS | no 1594 rows written to raw/accepted finite directories |
| VAL1594_13_branch_copies | PASS | branch/quarantine nonclaim copies written |
| VAL1594_14_pycache_absent | PASS | scripts __pycache__ absent after run |
| VAL1594_15_formalization_untouched | PASS | all generated 1594 paths are outside formalization-workbench; git status is clean when available |
| VAL1594_OVERALL | PASS | 1594 action-weight exclusion or beta source acquisition validator validation |

## Next Target

| next_target | script | objective | success_condition | do_not |
| --- | --- | --- | --- | --- |
| 1595-Y5-R2FR-first-source-backed-beta-or-action-measure-owner-reopen.md | scripts/Y5_R2FR_first_source_backed_beta_or_action_measure_owner_reopen.py | try once more to derive the parent action-measure owner from MTS primitives; if it still fails, create the first source-backed finite beta/Delta_w acquisition row and run the 1594 validator against it | parent-signed action-measure owner that kills w_A, or at least one beta/Delta_w row that passes schema/provenance but remains nonclaim until arena bounds exist | do not score local tests from templates, do not absorb relative weights into measured G, do not edit formalization-workbench or GitHub |
