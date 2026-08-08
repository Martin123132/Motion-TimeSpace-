# 1597 - R2/fR tau Lower Bound Or Coupling Zero Proof

## Verdict
- 1597 derives the precise `tau_min` condition: a usable lower bound needs nonzero readout, source and material norms **plus** a positive alignment/non-null bound.
- Nonzero factors alone do not prove `tau_WEP != 0`; the source-material vector can sit in the readout kernel, giving `tau_WEP=0` while every component is nonzero.
- The coupling-zero route also remains open: the parent action-measure package still has not killed pre-variation `w_A`.
- Therefore the MICROSCOPE row remains a source-backed product bound only: `abs(Delta_w_TiPt*tau_WEP) <= 2.8e-15`.
- No WEP, local-GR, Newton, PPN, R10, clock, orbital, beta/coupling, or public claim is made.

## Source Register

| source_id | source_path | exists | needle_found | needles |
| --- | --- | --- | --- | --- |
| SRC1597_0_1596_doc | 1596-Y5-R2FR-tau-WEP-source-projection-or-action-measure-owner-last-gate.md | True | True | NEXT_1597_TAU_LOWER_BOUND_OR_COUPLING_ZERO_PROOF; tau_min |
| SRC1597_1_1596_validation | source-intake/mts_residuals/P8_Y5_BRR545_1596_VALIDATION.csv | True | True | VAL1596_OVERALL; PASS |
| SRC1597_2_1596_contraction_law | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1596_TAU_WEP_CONTRACTION_LAW.csv | True | True | TCL1596_2_delta_w_amplitude_law; tau_min > 0 |
| SRC1597_3_1596_tau_factor_audit | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1596_TAU_FACTOR_AUDIT.csv | True | True | TFA1596_4_readout_matrix; OFFICIAL_ARRAYS_NOT_IMPORTED |
| SRC1597_4_1596_action_last_gate | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1596_ACTION_MEASURE_OWNER_LAST_GATE.csv | True | True | AMG1596_3_last_gate_verdict; ACTION_MEASURE_OWNER_LAST_GATE_NOT_CLOSED |
| SRC1597_5_1596_delta_w_status | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1596_DELTA_W_BOUND_STATUS.csv | True | True | DWB1596_3_delta_w_bound; SYMBOLIC_ONLY_NO_NUMERIC_DELTA_W |
| SRC1597_6_1596_tau_acquisition | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1596_TAU_SOURCE_ACQUISITION_ROWS.csv | True | True | TSA1596_3_tau_min; strictly positive |
| SRC1597_7_1596_next_target | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1596_NEXT_TARGET.csv | True | True | 1597-Y5-R2FR-tau-lower-bound-or-coupling-zero-proof; tau_min>0 |
| SRC1597_8_1595_candidate | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1595_SOURCE_BACKED_BETA_DELTAW_CANDIDATE.csv | True | True | SBC1595_0_MICROSCOPE_Delta_w_tau_bound_anchor; 2.8e-15 |
| SRC1597_9_1083_source_caveat | source-intake/mts_residuals/P8_Y5_R10_1083_SOURCE_VECTOR_CAVEAT_GATE.csv | True | True | SCG1083_0_profile_weighting; MISSING_SOURCE_PROFILE_WEIGHTING |
| SRC1597_10_1084_readout_gate | source-intake/mts_residuals/P8_Y5_R10_1084_MICROSCOPE_READOUT_IMPORT_GATE.csv | True | True | RIG1084_0_CMSM_arrays; OFFICIAL_ARRAYS_NOT_IMPORTED |
| SRC1597_11_1482_tau_readiness | source-intake/mts_residuals/P8_Y5_R10_1482_TAU_WEP_READINESS_UPDATE.csv | True | True | TAU1482_7_numeric_tau; NOT_EVALUATED |

## tau Lower-Bound Theorem Audit

| theorem_id | statement | current_status | result |
| --- | --- | --- | --- |
| TLB1597_0_projection_definition | tau_WEP = N_eta^{-1} <K_CMSM, S_Earth x M_TiPt> in the branch-locked linear readout convention | FORMAL_PAIRING_ONLY | DEFINITION_SHARPENED_NOT_EVALUATED |
| TLB1597_1_sufficient_lower_bound | if ||K_CMSM||>=k_min, ||S_Earth||>=s_min, ||M_TiPt||>=m_min, |cos(theta)|>=c_min>0 and N_eta<=N_max then |tau_WEP|>=k_min*s_min*m_min*c_min/N_max | CONDITIONAL_THEOREM_DERIVED | TAU_MIN_REQUIRES_ALIGNMENT_NOT_JUST_NONZERO_FACTORS |
| TLB1597_2_norms_insufficient | nonzero source, material and readout factors do not imply nonzero tau_WEP because the readout pairing can be orthogonal to the source-material vector | NO_SHORTCUT_LEMMA_DERIVED | GENERIC_TAU_MIN_NOT_PROVEN |
| TLB1597_3_current_corpus_verdict | current corpus lacks K_CMSM, source worldtube, material response tensor, product normalization and alignment proof | TAU_LOWER_BOUND_NOT_DERIVED | NO_NUMERIC_TAU_MIN |

## Null-Space Countermodel

| countermodel_id | construction | math_result | meaning | escape_condition |
| --- | --- | --- | --- | --- |
| NSC1597_0_linear_space_model | Let K be a nonzero linear readout functional and let V=S_Earth x M_TiPt be nonzero but chosen in ker(K). | <K,V>=0 while K!=0 and V!=0 | tau_WEP can vanish even with nonzero source/material/readout objects | prove V not in ker(K), or import data showing the branch-locked V has nonzero readout projection |
| NSC1597_1_cancellation_model | Allow shell/orbit/readout contributions with opposite signs and no signed material model. | positive and negative pieces can cancel in the orbit average | bulk-source positivity does not imply tau_WEP positivity after readout projection | sourced signed kernel plus no-cancellation or absolute-response theorem |
| NSC1597_2_measured_G_absorption_guard | If a common-mode source response is absorbed into measured G, only relative residuals remain visible. | absorption cannot establish tau_min for the differential channel | measured-G renormalization is not a proof of local-GR reduction | derive zero residual, or bound the differential residual directly |

## Coupling Zero Proof Audit

| proof_id | target | current_status | result |
| --- | --- | --- | --- |
| CZP1597_0_delta_w_zero_route | Delta_w_TiPt=0 | ACTION_MEASURE_OWNER_LAST_GATE_NOT_CLOSED | ZERO_PROOF_NOT_AVAILABLE |
| CZP1597_1_current_owner_limit | remove pre-variation w_A | CURRENT_OWNER_INSUFFICIENT | POST_VARIATION_ROUTE_DOES_NOT_KILL_COUPLING |
| CZP1597_2_coupling_zero_verdict | coupling/source-weight zero theorem | COUPLING_ZERO_PROOF_NOT_DERIVED | FINITE_PRODUCT_BRANCH_REMAINS_OPEN |

## WEP Product Branch Status

| status_id | quantity | status | value_or_formula | what_it_does_not_allow |
| --- | --- | --- | --- | --- |
| WPS1597_0_product_bound | abs(Delta_w_TiPt*tau_WEP) | SOURCE_BACKED_BOUND_ANCHOR_RETAINED | <= 2.8e-15 | no Delta_w number, no WEP pass, no local-GR claim |
| WPS1597_1_delta_w | abs(Delta_w_TiPt) | BLOCKED_BY_NO_TAU_MIN | if tau_min>0 then <=2.8e-15/tau_min | no numeric Delta_w bound |
| WPS1597_2_zero_route | Delta_w_TiPt=0 | BLOCKED_BY_NO_PARENT_COUPLING_ZERO_PROOF | not derived | no zero theorem claim |

## Required Nondegeneracy Inputs

| input_id | needed_input | why_needed | source_route | status | priority |
| --- | --- | --- | --- | --- | --- |
| NDI1597_0_K_norm | k_min lower bound for official K_CMSM readout functional | readout must be nonzero in the branch-locked channel | official MICROSCOPE readout/design matrix | MISSING | highest |
| NDI1597_1_source_norm | s_min lower bound for Earth source-weight vector | source object must be nonzero in the same convention | source worldtube/profile import or parent source theorem | MISSING | highest |
| NDI1597_2_material_norm | m_min lower bound for Ti/Pt material response difference | test-pair vector must be nonzero in the finite source-weight channel | material response tensor or parent matter-action map | MISSING | high |
| NDI1597_3_alignment | c_min lower bound for |cos(theta)| between readout functional and source-material vector | this is what excludes the null-space countermodel | official data computation or parent nondegeneracy theorem | MISSING_CRITICAL | highest |
| NDI1597_4_normalization | N_max upper bound and sign/absolute convention for eta normalization | turns pairing lower bound into dimensionless tau_min | MICROSCOPE product convention/readout normalization | MISSING | high |

## Runner Refusal

| runner_id | acceptance_rule | input_state | runner_result | effect |
| --- | --- | --- | --- | --- |
| RUN1597_0_tau_min | tau_min requires positive alignment/non-null proof or sourced data | no K/source/material/alignment/normalization inputs | REJECT_TAU_MIN_CLAIM | Delta_w remains unbounded numerically |
| RUN1597_1_null_countermodel | if countermodel exists, generic tau lower-bound theorem fails | nonzero vector may sit in readout kernel | ACCEPT_BLOCKING_COUNTERMODEL | official data or parent nondegeneracy proof required |
| RUN1597_2_coupling_zero | coupling zero requires parent action-measure/matter descent proof | last gate not closed | REJECT_COUPLING_ZERO_CLAIM | finite source-weight branch retained |

## Claim Gates

| gate_id | claim | status | reason |
| --- | --- | --- | --- |
| CG1597_0_tau_min | tau_WEP lower bound exists | BLOCKED | blocked by null-space countermodel and missing data |
| CG1597_1_delta_w | numeric Delta_w_TiPt bound exists | BLOCKED | blocked by no tau_min |
| CG1597_2_zero | Delta_w_TiPt=0 theorem | BLOCKED | blocked by no parent coupling/action-measure proof |
| CG1597_3_wep | MTS passes WEP/MICROSCOPE | BLOCKED | blocked; product anchor only |
| CG1597_4_local_gr | derived local GR branch | BLOCKED | blocked; coupling/source residual remains open |

## Decision

| decision_id | decision | reason | next_action |
| --- | --- | --- | --- |
| DEC1597_0_tau_min | TAU_MIN_NOT_DERIVED | nonzero factors do not exclude readout-kernel orthogonality | import official readout/source data or derive parent nondegeneracy |
| DEC1597_1_coupling_zero | COUPLING_ZERO_NOT_DERIVED | action-measure owner still fails at pre-variation w_A | continue zero theorem only if parent action package can be supplied |
| DEC1597_2_best_route | NEXT_1598_OFFICIAL_READOUT_OR_PARENT_NONDEGENERACY | the theorem route now needs exactly the same nondegeneracy object the data route would compute | build official MICROSCOPE readout/source import gate, or prove K not orthogonal to branch source vector |

## Next Target

| next_target | script | objective | success_condition | do_not |
| --- | --- | --- | --- | --- |
| 1598-Y5-R2FR-official-MICROSCOPE-readout-or-parent-nondegeneracy.md | scripts/Y5_R2FR_official_MICROSCOPE_readout_or_parent_nondegeneracy.py | either import/source the official readout/source objects needed to compute tau_WEP, or prove a parent nondegeneracy theorem excluding the readout-kernel null case | a sourced nonzero projection/alignment row, or a parent theorem that forces c_min>0; otherwise keep WEP product-bound only | do not use tau_WEP=1, surrogate-only readout matrices, measured-G absorption, or public/local-GR claims |

## Validation

| check_id | result | detail |
| --- | --- | --- |
| VAL1597_0_sources_exist | PASS | all cited 1597 source paths exist |
| VAL1597_1_needles_found | PASS | all required 1597 source needles found |
| VAL1597_2_conditional_tau_bound | PASS | conditional tau lower-bound theorem recorded |
| VAL1597_3_norms_insufficient | PASS | nonzero norms insufficient lemma recorded |
| VAL1597_4_null_countermodel | PASS | readout-kernel countermodel recorded |
| VAL1597_5_coupling_zero_blocked | PASS | coupling zero proof remains blocked |
| VAL1597_6_product_branch_only | PASS | WEP product anchor retained only |
| VAL1597_7_alignment_input_required | PASS | alignment/non-null input required |
| VAL1597_8_runner_blocks_tau_min | PASS | runner rejects tau_min claim |
| VAL1597_9_claim_gates_closed | PASS | all 1597 claim gates remain closed |
| VAL1597_10_decision_next | PASS | decision selects 1598 official readout/parent nondegeneracy |
| VAL1597_11_csv_parse | PASS | all generated 1597 CSVs parse |
| VAL1597_12_claim_safety_flags | PASS | no generated 1597 rows are score-ready, prediction rows, or claim-allowed |
| VAL1597_13_branch_copies | PASS | branch/quarantine nonclaim copies exist |
| VAL1597_14_pycache_absent | PASS | scripts __pycache__ absent |
| VAL1597_15_formalization_untouched | PASS | no 1597 outputs found under formalization-workbench |
| VAL1597_OVERALL | PASS | 1597 tau lower-bound or coupling-zero proof validation |
