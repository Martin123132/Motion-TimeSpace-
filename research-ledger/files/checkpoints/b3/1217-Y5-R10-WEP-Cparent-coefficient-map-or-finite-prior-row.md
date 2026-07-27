# 1217 Y5/R10 WEP Cparent Coefficient Map Or Finite Prior Row

**Current verdict:** 1217 does **not** derive the `C_parent -> (c_alpha, c_surface, q_tail)` map and does **not** prove the coefficient vector zero. It tightens the exact coupling contract and stages finite coefficient-prior rows as nonclaim scaffolding.

**Main progress:** the missing object is now sharper: we need a parent-owned alpha operator, a parent-owned surface/binding operator, a tail/basis envelope, and one same-branch normalization tying coefficients to range, source profile, and MICROSCOPE readout. The coupling is the lock; the numeric WEP pressure rows only tell us the scale a future coefficient would have to survive.

**No-claim rule:** thresholds from WEP are not theory priors. A coefficient row becomes claim-valid only if the value is derived from the parent action or sourced externally with units, signs, branch, profile, and readout provenance.

## Source Register

| source_id | local_path | needle | purpose | absolute_path | path_exists | needle_found | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SRC1217_0_1216_next | source-intake/mts_residuals/P8_Y5_R10_1216_NEXT_TARGET.csv | 1217-Y5-R10-WEP-Cparent-coefficient-map-or-finite-prior-row.md | 1216 handoff to C_parent coefficient-map target | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1216_NEXT_TARGET.csv | True | True | False | False |
| SRC1217_1_1216_pressure | source-intake/mts_residuals/P8_Y5_R10_1216_DD_SOURCE_MATERIAL_PRODUCT_PRESSURE.csv | DDP1216_2_combined_abs | numeric source-material coefficient pressure rows | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1216_DD_SOURCE_MATERIAL_PRODUCT_PRESSURE.csv | True | True | False | False |
| SRC1217_2_1216_update | source-intake/mts_residuals/P8_Y5_R10_1216_SAME_NORM_PRODUCT_UPDATE.csv | SNU1216_0_formula_update | same-norm product formula with C_parent lock | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1216_SAME_NORM_PRODUCT_UPDATE.csv | True | True | False | False |
| SRC1217_3_1215_contract | source-intake/mts_residuals/P8_Y5_R10_1215_SAME_NORM_PRODUCT_CONTRACT.csv | SNP1215_0_WEP_formula | absolute same-basis WEP product contract | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1215_SAME_NORM_PRODUCT_CONTRACT.csv | True | True | False | False |
| SRC1217_4_1080_Cparent | source-intake/mts_residuals/P8_Y5_R10_1080_C_PARENT_COEFFICIENT_CONTRACT.csv | CP1080_0_definition | original C_parent missing coefficient contract | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1080_C_PARENT_COEFFICIENT_CONTRACT.csv | True | True | False | False |
| SRC1217_5_1082_map | source-intake/mts_residuals/P8_Y5_R10_1082_PARENT_TO_DD_COEFFICIENT_MAP_ATTEMPT.csv | PTD1082_4_verdict | prior parent-to-DD map failure | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1082_PARENT_TO_DD_COEFFICIENT_MAP_ATTEMPT.csv | True | True | False | False |
| SRC1217_6_1086_first_row | source-intake/mts_residuals/P8_Y5_R10_1086_DD_PARENT_MAP_FIRST_ROW_ATTEMPT.csv | PDM1086_4_verdict | first DD coefficient row obstruction | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1086_DD_PARENT_MAP_FIRST_ROW_ATTEMPT.csv | True | True | False | False |
| SRC1217_7_1086_delta_obstruction | source-intake/mts_residuals/P8_Y5_R10_1086_COMPOSITION_DELTA_OBSTRUCTION.csv | CDO1086_2_cancellation_line | forbidden TA6V-PtRh10 cancellation line | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1086_COMPOSITION_DELTA_OBSTRUCTION.csv | True | True | False | False |
| SRC1217_8_1086_guard | source-intake/mts_residuals/P8_Y5_R10_1086_NO_CANCELLATION_GUARD.csv | NCG1086_0_no_pair_tuning | no pair tuning policy | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1086_NO_CANCELLATION_GUARD.csv | True | True | False | False |
| SRC1217_9_1087_source_pack | source-intake/mts_residuals/P8_Y5_R10_1087_DD_COEFFICIENT_SOURCE_PACK.csv | DDSP1087_0_c_alpha | coefficient source requirements | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1087_DD_COEFFICIENT_SOURCE_PACK.csv | True | True | False | False |
| SRC1217_10_1087_template | source-intake/mts_residuals/P8_Y5_R10_1087_DD_COEFFICIENT_SOURCE_PACK_TEMPLATE_NONCLAIM.csv | DDCOEFF1087_0_alpha | nonclaim coefficient template | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1087_DD_COEFFICIENT_SOURCE_PACK_TEMPLATE_NONCLAIM.csv | True | True | False | False |
| SRC1217_11_1096_zero | source-intake/mts_residuals/P8_Y5_R10_1096_COEFFICIENT_ZERO_THEOREM_ATTEMPT.csv | CZ1096_4_verdict | coefficient-vector zero theorem attempt | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1096_COEFFICIENT_ZERO_THEOREM_ATTEMPT.csv | True | True | False | False |
| SRC1217_12_1096_prior | source-intake/mts_residuals/P8_Y5_R10_1096_DD_COEFFICIENT_PRIOR_TEMPLATE_NONCLAIM.csv | PRI1096_0_alpha | threshold-bounded prior template | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1096_DD_COEFFICIENT_PRIOR_TEMPLATE_NONCLAIM.csv | True | True | False | False |
| SRC1217_13_1097_requirements | source-intake/mts_residuals/P8_Y5_R10_1097_SOURCE_PRIOR_REQUIREMENTS.csv | FSR1097_1_external_prior | requirements for source-backed finite prior | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1097_SOURCE_PRIOR_REQUIREMENTS.csv | True | True | False | False |
| SRC1217_14_1084_readout | source-intake/mts_residuals/P8_Y5_R10_1084_MICROSCOPE_READOUT_IMPORT_GATE.csv | RIG1084_0_CMSM_arrays | official readout still missing | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1084_MICROSCOPE_READOUT_IMPORT_GATE.csv | True | True | False | False |
| SRC1217_15_1083_profile | source-intake/mts_residuals/P8_Y5_R10_1083_SOURCE_VECTOR_CAVEAT_GATE.csv | SCG1083_0_profile_weighting | source-profile weighting still missing | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1083_SOURCE_VECTOR_CAVEAT_GATE.csv | True | True | False | False |
| SRC1217_16_1100_alpha_norm | source-intake/mts_residuals/P8_Y5_R10_1100_ALPHA_NORMALIZATION_DECOMPOSITION.csv | Z1100_4_total | alpha normalization remains finite-branch, not theorem-zero | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1100_ALPHA_NORMALIZATION_DECOMPOSITION.csv | True | True | False | False |
| SRC1217_17_1101_route | source-intake/mts_residuals/P8_Y5_R10_1101_ALPHA_ROUTE_DECISION.csv | ROUTE1101_2_finite_alpha_products | finite alpha product route discipline | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1101_ALPHA_ROUTE_DECISION.csv | True | True | False | False |

## Cparent Map Attempt

| map_id | target | candidate_formula | needed_parent_object | attempt_result | gap | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CMAP1217_0_mass_response_formula | C_parent -> DD material response vector | partial_X ln m_A = c_0 + c_alpha Q_alpha_Coulomb(A) + c_surface Q_surface_binding(A) + q_tail(A) | parent ordinary-matter mass functional m_A[q(Phi), X] and its vertical derivative | FORMULA_RETAINED_AS_EXTERNAL_DD_DECOMPOSITION | the DD formula is a comparator basis until the MTS parent action supplies the derivative and basis map | False | False |
| CMAP1217_1_alpha_operator_owner | c_alpha | c_alpha := N_X partial_X ln alpha_EM in the DD Q_alpha_Coulomb convention | signed EM/fine-structure operator owner, normalization N_X, and material charge pullback | NOT_DERIVED | PTD1082_1 and PDM1086_1 keep the parent EM derivative unsigned; Z1100_4 retains finite alpha branch | False | False |
| CMAP1217_2_surface_operator_owner | c_surface | c_surface := N_X partial_X ln a_surface_or_binding in the DD Q_surface_binding convention | signed nuclear/surface/binding response operator and same normalization N_X | NOT_DERIVED | PTD1082_2 and PDM1086_2 keep the parent binding derivative unsigned | False | False |
| CMAP1217_3_same_branch_normalization | basis, units, signs, range, and readout placement | one branch supplies Z_X, M_X^2, lambda_X, N_X, K_MICROSCOPE, Qeff_E, c_alpha, c_surface, q_tail | single same-branch normalization and Green-kernel/readout convention | NOT_DERIVED | range/readout/profile gates remain live; C_parent cannot be mixed with source/readout rows from different branches | False | False |
| CMAP1217_4_no_absorption_shortcut | avoid hiding C_parent inside measured G, unit proxy, or fitted normalization | B_species,WEP <= \|K\| sum_I \|C_I\| \|R_source,I\| \|DeltaR_I\| | explicit coefficient vector or theorem-zero certificate | SHORTCUTS_REJECTED | unit proxies, measured-G absorption, and pair cancellation are not parent derivations | False | False |
| CMAP1217_5_verdict | claim-valid C_parent coefficient map | C_parent -> (c_alpha, c_surface, q_tail) in the same DD/MTS branch | source-backed or parent-derived coefficient vector with units, signs, basis, and normalization | CPARENT_MAP_NOT_DERIVED | 1217 sharpens the exact coefficient contract but supplies no sourced/derived coefficient value | False | False |

## Coefficient Zero Audit

| zero_id | coefficient | zero_route | status | obstruction | claim_effect | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ZERO1217_0_alpha | c_alpha | no independent hidden-dependent F_Q^2 term plus fixed gauge norm plus radiative/readout closure | CONDITIONAL_NOT_SIGNED | Z1100_4 keeps hidden counterterm and readout terms alive; no-extra-F2 theorem is not promoted | alpha coefficient remains finite/missing | False | False |
| ZERO1217_1_surface | c_surface | ordinary nuclear/binding constants are parent superselection data with no hidden-visible morphism | CONDITIONAL_NOT_SIGNED | constant-sector universality and binding operator owner remain unsigned | surface/binding coefficient remains finite/missing | False | False |
| ZERO1217_2_tail | q_tail(A) | alpha/surface DD rows form a complete material response basis and all remaining channels vanish | NOT_DERIVED | DD alpha/surface rows are useful dominant channels but not a parent-complete basis | tail envelope remains a required lock | False | False |
| ZERO1217_3_vector | C_parent vector | CZ1096_1 conditional theorem: constant-sector universality plus no hidden-visible hom | COEFFICIENT_ZERO_NOT_DERIVED | CZ1096_4 remains active; parent signatures, basis ownership, and readout closure are unsigned | do not claim WEP/local-GR pass from zero | False | False |

## Finite Coefficient Prior Contract

| prior_id | branch_id | coefficient | value | units | allowed_abs_threshold_from_1216 | threshold_source_row | promotion_rule | status | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CPRIOR1217_0_alpha | MTS_WEP_finite_branch | c_alpha_DD | MISSING_PARENT_EM_DERIVATIVE_OR_SOURCE_BACKED_PRIOR | dimensionless_after_parent_normalization_in_DD_convention | 8.320244933243531978e-10 | DDP1216_0_alpha | requires parent EM derivative or explicit external coefficient prior; threshold alone is not a theory prediction | FINITE_PRIOR_VALUE_MISSING_THRESHOLD_AVAILABLE_NONCLAIM | False | False |
| CPRIOR1217_1_surface | MTS_WEP_finite_branch | c_surface_DD | MISSING_PARENT_BINDING_DERIVATIVE_OR_SOURCE_BACKED_PRIOR | dimensionless_after_parent_normalization_in_DD_convention | 6.987501646143863402e-11 | DDP1216_1_surface | requires parent binding derivative or explicit external coefficient prior; no pair tuning | FINITE_PRIOR_VALUE_MISSING_THRESHOLD_AVAILABLE_NONCLAIM | False | False |
| CPRIOR1217_2_common_abs | MTS_WEP_finite_branch | c_common_abs_if_single_combined_scale | MISSING_PARENT_VECTOR_NORM_OR_SOURCE_BACKED_PRIOR | dimensionless_after_parent_normalization_in_DD_convention | 6.446142229433907306e-11 | DDP1216_2_combined_abs | requires parent coefficient-vector norm or source-backed prior; common scale is a diagnostic only | FINITE_PRIOR_VALUE_MISSING_THRESHOLD_AVAILABLE_NONCLAIM | False | False |
| CPRIOR1217_3_tail | MTS_WEP_finite_branch | q_tail_envelope | MISSING_MATERIAL_BASIS_TAIL_ENVELOPE | dimensionless_eta_contribution_or_charge_envelope | MISSING_TAIL_THRESHOLD | MISSING_PARENT_OR_EMPIRICAL_ENVELOPE | requires basis completeness theorem or empirical all-material residual envelope | TAIL_LOCK_MISSING_NONCLAIM | False | False |
| CPRIOR1217_4_same_branch_packet | MTS_WEP_finite_branch | lambda_X;K_MICROSCOPE;Qeff_E;N_X | MISSING_SAME_BRANCH_RANGE_READOUT_PROFILE_NORMALIZATION | m;dimensionless;DD_charge;normalization | not_applicable | SNP1215_1_basis_lock;RIG1084_0_CMSM_arrays;SCG1083_0_profile_weighting | all factors must share one branch before any coefficient row can be claim-valid | SAME_BRANCH_PACKET_MISSING_NONCLAIM | False | False |

## Numeric Pressure Reuse

| reuse_id | coefficient | source_material_product_abs | eta_bound | threshold_abs | source_row | meaning | status | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PREUSE1217_0_alpha | c_alpha_DD | 3.365285544434638e-06 | 2.800000000000000e-15 | 8.320244933243531978e-10 | DDP1216_0_alpha | if a real same-branch c_alpha exists in this DD convention, this is the approximate absolute scale it must sit below | NUMERIC_PRESSURE_REUSED_NONCLAIM | False | False |
| PREUSE1217_1_surface | c_surface_DD | 4.007154691040701e-05 | 2.800000000000000e-15 | 6.987501646143863402e-11 | DDP1216_1_surface | if a real same-branch c_surface exists in this DD convention, this is the approximate absolute scale it must sit below | NUMERIC_PRESSURE_REUSED_NONCLAIM | False | False |
| PREUSE1217_2_common_abs | c_common_abs_if_single_combined_scale | 4.343683245484165e-05 | 2.800000000000000e-15 | 6.446142229433907306e-11 | DDP1216_2_combined_abs | equal/common coefficient diagnostic only; not a derived coefficient-vector norm | NUMERIC_PRESSURE_REUSED_NONCLAIM | False | False |

## No-Cancellation Guard

| guard_id | object | value | source_row | policy | status | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NCG1217_0_forbidden_pair_line | TA6V_minus_PtRh10 two-channel cancellation line | c_surface/c_alpha=-6.017949967452794e-01 | CDO1086_2_cancellation_line | recorded only as an algebraic line; forbidden as evidence unless parent-derived before material choice and checked across materials | FORBIDDEN_CANCELLATION_LINE_NONCLAIM | False | False |
| NCG1217_1_absolute_sum_rule | WEP coefficient pressure calculation | use \|c_alpha product_alpha\| + \|c_surface product_surface\| + \|tail\| unless a sourced covariance/correlation model exists | SNP1215_3_no_cancellation;NCG1086_0_no_pair_tuning;AMC1087_0_pair_line_forbidden | no signs chosen after seeing the material pair | ACTIVE_GUARD | False | False |

## WEP Factor Feed Update

| feed_id | target_row | field_to_fill | source_row | update_value | current_status | claim_policy | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WFEED1217_0_to_WEP1215_6 | WEP1215_6_C_parent | strict finite-prior contract | CPRIOR1217_0_alpha;CPRIOR1217_1_surface;CPRIOR1217_2_common_abs;CPRIOR1217_3_tail | C_parent remains missing; threshold-bounded nonclaim prior rows staged | MISSING_COEFFICIENT_VALUE_STRICT_PRIOR_CONTRACT_AVAILABLE | do not promote until coefficient values are parent-derived or source-backed | False | False |
| WFEED1217_1_to_SNU1216_0 | SNU1216_0_formula_update | C_parent factor | CMAP1217_5_verdict | map not derived; same-norm product remains blocked | CPARENT_MAP_BLOCKED | numeric DD source-material pressure rows stay scaffolding | False | False |
| WFEED1217_2_to_DSB1214_5 | DSB1214_5_projection_map | WEP_C_parent | CPRIOR1217_0_alpha;CPRIOR1217_1_surface;CPRIOR1217_3_tail | coefficient owner isolated as active missing projection factor | MISSING_PARENT_OPERATOR_COEFFICIENT_MAP | no local-GR/WEP/R10 claim | False | False |

## Product Runner Stub

| runner_id | prediction_rows | valid_prediction_rows | numeric_pressure_rows | finite_prior_contract_rows | claim_allowed | expected_result | reason | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| APR1217_0_Cparent_prior_stub | 1 | 0 | 3 | 5 | False | reject full WEP product while preserving numeric pressure and prior-contract rows | C_parent values, same-branch normalization, K_MICROSCOPE, and profile weighting remain missing | False |

## Decision Ledger

| decision_id | decision | because | next_action | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| DEC1217_0_derivation_attempt | C_parent map is not derived at 1217 | alpha owner, surface owner, same-branch normalization, and tail basis are unsigned | hunt the parent alpha/surface operator owner instead of assigning coefficient values | False | False |
| DEC1217_1_finite_prior_contract | stage explicit finite-prior rows as nonclaim | numeric pressure thresholds are useful discipline but are not coefficient sources | require parent derivation or external coefficient-prior provenance before promotion | False | False |
| DEC1217_2_no_cancellation | keep the cancellation line forbidden | single material-pair cancellation would be post-hoc and not a field-theory result | only allow coefficient vectors fixed before material choice and checked across arenas | False | False |

## Claim Gates

| gate_id | gate | status | reason | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| GATE1217_0_sources | source path and needle audit | PASS | all local inputs used by 1217 are traceable | False | False |
| GATE1217_1_Cparent_map | C_parent -> DD coefficient map | BLOCKED | CMAP1217_5_verdict=CPARENT_MAP_NOT_DERIVED | False | False |
| GATE1217_2_coefficient_zero | C_parent coefficient vector theorem-zero | BLOCKED | ZERO1217_3_vector=COEFFICIENT_ZERO_NOT_DERIVED | False | False |
| GATE1217_3_finite_prior | claim-valid finite coefficient prior | BLOCKED | thresholds exist, but coefficient values and provenance remain missing | False | False |
| GATE1217_4_no_cancellation | no pair-tuned cancellation | PASS_NONCLAIM | forbidden cancellation line is explicitly quarantined | False | False |
| GATE1217_5_WEP_product | claim-valid WEP/local-GR product | BLOCKED | valid_prediction_rows=0 and same-branch packet is missing | False | False |

## Next Target

| next_id | target_file | target_script | task | success_condition | do_not_do | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NEXT1217_0_1218 | 1218-Y5-R10-parent-alpha-surface-operator-owner-or-coefficient-prior-source.md | scripts/Y5_R10_parent_alpha_surface_operator_owner_or_coefficient_prior_source.py | try to identify the parent operator owner for alpha/surface material response; if that fails, acquire or explicitly reject source-backed coefficient prior rows | either c_alpha/c_surface become parent-derived/theorem-zero, or the missing coefficient-prior source requirement is tightened into a source-acquisition ledger | do not invent coefficient priors; do not use threshold bounds as predictions; do not tune cancellation; do not claim WEP/local-GR/R10; do not edit formalization-workbench or push GitHub | False | False |

## Validation

| check_id | check | status | details | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| VAL1217_0_sources_exist | all cited local sources exist | PASS | 18/18 sources exist | False | False |
| VAL1217_1_needles_found | all cited source needles found | PASS | 18/18 needles found | False | False |
| VAL1217_2_map_not_overclaimed | C_parent map failure is explicit | PASS | CMAP1217_5_verdict=CPARENT_MAP_NOT_DERIVED | False | False |
| VAL1217_3_zero_not_overclaimed | coefficient zero is not overclaimed | PASS | ZERO1217_3_vector=COEFFICIENT_ZERO_NOT_DERIVED | False | False |
| VAL1217_4_thresholds_positive | finite-prior thresholds are positive | PASS | CPRIOR1217_0_alpha=8.320244933243531978e-10; CPRIOR1217_1_surface=6.987501646143863402e-11; CPRIOR1217_2_common_abs=6.446142229433907306e-11 | False | False |
| VAL1217_5_prior_rows_nonclaim | prior rows remain nonclaim | PASS | all finite prior rows valid_for_claim=false and claim_allowed=false | False | False |
| VAL1217_6_missing_rows_nonclaim | no MISSING row is valid for claim | PASS | missing coefficient/prior/source values are quarantined | False | False |
| VAL1217_7_cancellation_forbidden | pair cancellation line is forbidden | PASS | c_surface/c_alpha=-6.017949967452794e-01 | False | False |
| VAL1217_8_pressure_reuse_positive | numeric pressure reuse rows are positive | PASS | PREUSE1217_0_alpha=8.320244933243531978e-10; PREUSE1217_1_surface=6.987501646143863402e-11; PREUSE1217_2_common_abs=6.446142229433907306e-11 | False | False |
| VAL1217_9_runner_refuses | runner stub refuses missing full product | PASS | valid_prediction_rows=0 and claim_allowed=false | False | False |
| VAL1217_10_claim_locks_blocked | claim locks remain blocked | PASS | Cparent map, zero theorem, finite prior, and WEP product blocked | False | False |
| VAL1217_11_nonclaim_policy | all generated rows remain nonclaim | PASS | valid_for_claim=false and claim_allowed=false throughout | False | False |
| VAL1217_12_csv_parse | all generated CSVs parse cleanly | PASS | P8_Y5_R10_1217_SOURCE_REGISTER.csv:18; P8_Y5_R10_1217_CPARENT_MAP_ATTEMPT.csv:6; P8_Y5_R10_1217_COEFFICIENT_ZERO_AUDIT.csv:4; P8_Y5_R10_1217_FINITE_COEFFICIENT_PRIOR_CONTRACT.csv:5; P8_Y5_R10_1217_NUMERIC_PRESSURE_REUSE.csv:3; P8_Y5_R10_1217_NO_CANCELLATION_GUARD.csv:2; P8_Y5_R10_1217_WEP_FACTOR_FEED_UPDATE.csv:3; P8_Y5_R10_1217_PRODUCT_RUNNER_STUB.csv:1; P8_Y5_R10_1217_DECISION_LEDGER.csv:3; P8_Y5_R10_1217_CLAIM_GATES.csv:6; P8_Y5_R10_1217_NEXT_TARGET.csv:1 | False | False |
| VAL1217_13_formalization_untouched | formalization-workbench untouched during run | PASS | formalization_recent_after_run_start_count=0 | False | False |
| VAL1217_14_next_target | next target is staged | PASS | 1218-Y5-R10-parent-alpha-surface-operator-owner-or-coefficient-prior-source.md | False | False |
| VAL1217_15_overall | overall 1217 validation | PASS | 1217 C_parent map/prior pack is reproducible, nonclaim, and claim-locked | False | False |
