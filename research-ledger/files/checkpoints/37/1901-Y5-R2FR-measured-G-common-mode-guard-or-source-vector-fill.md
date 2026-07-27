# 1901 - Measured-G Common-Mode Guard Or Source-Vector Fill

## Purpose

This checkpoint tests whether measured `G_N` / `GM` can absorb source-weight effects without cheating. It accepts the algebraic common-mode guard if valid, then checks whether the relative source vector is actually zero or executable.

## Result

- A single measured-`GM` calibration can absorb one universal common scalar.
- It cannot absorb relative material/source vectors, range dependence, frame dependence, or time dependence.
- This is a real algebraic guardrail, but it is not a parent theorem that relative source weights vanish.
- Bulk Earth DD numbers remain context only; they are not a profile/worldtube-weighted source vector.
- No WEP/local-GR claim is made.

## Source Register

| source_id | source_path | exists | needle_count | missing_needles | status | valid_for_claim | generated_utc |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1900_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1900-Y5-R2FR-wep-source-worldtube-point-source-reduction-or-official-readout-data-runner.md | True | 2 |  | EXISTS_NEEDLES_CONFIRMED | False | 2026-06-19T18:59:02.453786+00:00 |
| 1900_validation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_1900_VALIDATION.csv | True | 1 |  | EXISTS_NEEDLES_CONFIRMED | False | 2026-06-19T18:59:02.453786+00:00 |
| 1900_point_source | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1900_WEP_SOURCE_WORLDTUBE_POINT_SOURCE_REDUCTION_ATTEMPT.csv | True | 2 |  | EXISTS_NEEDLES_CONFIRMED | False | 2026-06-19T18:59:02.453786+00:00 |
| 1900_residuals | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1900_WEP_POINT_SOURCE_RESIDUAL_LEDGER_NONCLAIM.csv | True | 2 |  | EXISTS_NEEDLES_CONFIRMED | False | 2026-06-19T18:59:02.453786+00:00 |
| 1900_next | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1900_NEXT_TARGET.csv | True | 2 |  | EXISTS_NEEDLES_CONFIRMED | False | 2026-06-19T18:59:02.453786+00:00 |
| 1064_common_guard | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1064_COMMON_MODE_GUARD.csv | True | 2 |  | EXISTS_NEEDLES_CONFIRMED | False | 2026-06-19T18:59:02.453786+00:00 |
| 1083_common_alt | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1083_COMMON_MODE_ALTERNATIVE.csv | True | 2 |  | EXISTS_NEEDLES_CONFIRMED | False | 2026-06-19T18:59:02.453786+00:00 |
| 1332_common_theorem | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1332_COMMON_MODE_SOURCE_THEOREM.csv | True | 2 |  | EXISTS_NEEDLES_CONFIRMED | False | 2026-06-19T18:59:02.453786+00:00 |
| 1337_common_update | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1337_COMMON_MODE_THEOREM_UPDATE.csv | True | 2 |  | EXISTS_NEEDLES_CONFIRMED | False | 2026-06-19T18:59:02.453786+00:00 |
| 1338_common_status | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1338_COMMON_MODE_THEOREM_STATUS.csv | True | 2 |  | EXISTS_NEEDLES_CONFIRMED | False | 2026-06-19T18:59:02.453786+00:00 |
| 1425_g_guard | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1425_MEASURED_G_COMMON_MODE_GUARD.csv | True | 2 |  | EXISTS_NEEDLES_CONFIRMED | False | 2026-06-19T18:59:02.453786+00:00 |
| 1425_wep_zero | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1425_COMMON_MODE_WEP_ZERO_PROOF_ATTEMPT.csv | True | 2 |  | EXISTS_NEEDLES_CONFIRMED | False | 2026-06-19T18:59:02.453786+00:00 |
| 1450_absorption | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1450_COMMON_MODE_ABSORPTION_GUARD.csv | True | 2 |  | EXISTS_NEEDLES_CONFIRMED | False | 2026-06-19T18:59:02.453786+00:00 |
| 1602_zero | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1602_COMMON_MODE_ZERO_THEOREM_ATTEMPT.csv | True | 2 |  | EXISTS_NEEDLES_CONFIRMED | False | 2026-06-19T18:59:02.453786+00:00 |
| 1080_earth_candidates | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1080_EARTH_SOURCE_VECTOR_CANDIDATES.csv | True | 2 |  | EXISTS_NEEDLES_CONFIRMED | False | 2026-06-19T18:59:02.453786+00:00 |
| 1083_dd_earth | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1083_DD_EARTH_SOURCE_VECTOR_FIRST_ROW_NONCLAIM.csv | True | 2 |  | EXISTS_NEEDLES_CONFIRMED | False | 2026-06-19T18:59:02.453786+00:00 |
| 1083_caveat | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1083_SOURCE_VECTOR_CAVEAT_GATE.csv | True | 2 |  | EXISTS_NEEDLES_CONFIRMED | False | 2026-06-19T18:59:02.453786+00:00 |
| 1419_source_residual | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1419_SOURCE_RESIDUAL_COEFFICIENT_VECTOR.csv | True | 2 |  | EXISTS_NEEDLES_CONFIRMED | False | 2026-06-19T18:59:02.453786+00:00 |
| 1424_source_contract | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1424_SOURCE_VECTOR_CONTRACT.csv | True | 2 |  | EXISTS_NEEDLES_CONFIRMED | False | 2026-06-19T18:59:02.453786+00:00 |
| local_bound_claims | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\local_bound_claims.csv | True | 2 |  | EXISTS_NEEDLES_CONFIRMED | False | 2026-06-19T18:59:02.453786+00:00 |

## Measured-G Guard Attempt

| attempt_id | claim_piece | formal_statement | status | proof_or_obstruction | source_anchor | algebra_proved | parent_signed | valid_for_claim | claim_allowed | generated_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GMG1901_0_target | measured-G common-mode guard | Measured G_N or GM may absorb one universal, constant, same-frame, range-independent source normalization, but cannot absorb material/source-relative residuals. | TARGET_SHARP | this is the exact calibration rule needed to keep Newton/GR reduction honest | P8_Y5_R10_1450_COMMON_MODE_ABSORPTION_GUARD.csv:CMA1450_0_common_G; P8_Y5_PARENT_QLOC_1900_WEP_POINT_SOURCE_RESIDUAL_LEDGER_NONCLAIM.csv:PSE1900_2_measured_G_guard | True | False | False | False | 2026-06-19T18:59:02.453786+00:00 |
| GMG1901_1_algebraic_absorption | one scalar removes one scalar | If source strength is S_A = G_ref M_E w_common (1+epsilon_A), choosing measured GM absorbs w_common only; epsilon_A remains observable in contrasts unless Delta_AB epsilon=0. | EXACT_ALGEBRA_GUARD_DERIVED | a single calibration scalar cannot erase a nonconstant vector over materials, source profiles, ranges, or frames | P8_Y5_R10_1064_COMMON_MODE_GUARD.csv:CMG1064_1_relative_not_absorbable; P8_Y5_R10_1450_COMMON_MODE_ABSORPTION_GUARD.csv:CMA1450_1_relative_weight | True | False | False | False | 2026-06-19T18:59:02.453786+00:00 |
| GMG1901_2_range_frame_guard | range/time/frame modes are not calibration | A local measured GM cannot absorb D_lambda, D_r, D_t, or frame-dependent source weights across WEP/R10/orbital/PPN arenas. | EXACT_GUARD_POLICY_DERIVED | range- or frame-dependent terms would change between arenas and must be retained as residual rows | P8_Y5_R10_1064_COMMON_MODE_GUARD.csv:CMG1064_2_range_not_absorbable; P8_Y5_R10_1450_COMMON_MODE_ABSORPTION_GUARD.csv:CMA1450_2_range_dependence | True | False | False | False | 2026-06-19T18:59:02.453786+00:00 |
| GMG1901_3_parent_zero_missing | relative source vector is theorem-zero | To claim local GR/WEP zero, MTS must prove epsilon_A=0 or Delta_AB epsilon=0 before calibration, from parent object language/action-current ownership. | RELATIVE_SOURCE_ZERO_NOT_PARENT_DERIVED | common-mode route is conditional; no-source-slot/source-label forgetting is still unsigned | P8_Y5_R10_1337_COMMON_MODE_THEOREM_UPDATE.csv:THM1337_1_no_source_slot_is_minimal; P8_Y5_PARENT_QLOC_1602_COMMON_MODE_ZERO_THEOREM_ATTEMPT.csv:CMZ1602_3_verdict | False | False | False | False | 2026-06-19T18:59:02.453786+00:00 |
| GMG1901_4_source_vector_fallback | source vector fill fallback | If relative source zero is not derived, the source vector must be filled as explicit profile/composition/worldtube data in the same basis as material and parent coefficients. | SOURCE_VECTOR_FILL_REQUIRED_NONCLAIM | bulk Earth DD vector exists only as nonclaim context; profile/worldtube weighting and parent basis map are missing | P8_Y5_R10_1083_DD_EARTH_SOURCE_VECTOR_FIRST_ROW_NONCLAIM.csv:DD_EARTH1083_0_bulk_weighted; P8_Y5_R10_1424_SOURCE_VECTOR_CONTRACT.csv:SRCMAP1424_0_R_source | False | False | False | False | 2026-06-19T18:59:02.453786+00:00 |
| GMG1901_5_verdict | measured-G guard closes WEP/local-GR source branch | The current corpus proves measured GM absorbs only common mode and also proves all relative source weights vanish. | GUARD_ALGEBRA_DERIVED_RELATIVE_ZERO_NOT_DERIVED | the anti-hiding guard is solid, but it does not by itself prove relative source-vector zero; source-label/no-source-slot theorem or finite source vector still needed | GMG1901_0_target through GMG1901_4_source_vector_fallback | True | False | False | False | 2026-06-19T18:59:02.453786+00:00 |

## Common-Mode Absorption Algebra

| algebra_id | statement | result | surviving_term | why_it_matters | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| ALG1901_0_decomposition | w_A = w_common * (1 + epsilon_A) | calibration may choose G_meas = G_ref * w_common | epsilon_A | one scalar calibration cannot remove a material/source vector | ALGEBRA_ACCEPTED_GUARD | False |
| ALG1901_1_contrast | Delta_AB ln a = epsilon_A - epsilon_B + higher order | relative WEP/source contrast survives measured GM | Delta_AB epsilon | WEP tests are contrast tests; common mode cancels, relative mode does not | ALGEBRA_ACCEPTED_GUARD | False |
| ALG1901_2_range | w(lambda,r,t,frame) cannot be represented by one constant G_meas | range/time/frame hair must be retained | D_lambda w; D_r w; D_t w; Delta_frame w | prevents transfer of one local calibration across R10/orbit/PPN | ALGEBRA_ACCEPTED_GUARD | False |
| ALG1901_3_claim_limit | guard != zero theorem | guard blocks cheating but does not prove epsilon_A=0 | source-vector or no-source-slot theorem | this is a discipline theorem, not a local-GR pass | NO_CLAIM_PROMOTION | False |

## Source-Vector Fill Nonclaim

| fill_id | object | current_value | current_status | missing_for_claim | source_anchor | score_ready | valid_prediction_row | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SVF1901_0_bulk_dd_context | bulk Earth DD vector | Q_alpha=1.691260686750872e-03; Q_surface=-1.211918219995745e-02 | NUMERIC_BULK_EARTH_DD_SOURCE_VECTOR_NONCLAIM | profile/worldtube weighting, MTS parent basis map, material tensor matching | P8_Y5_R10_1083_DD_EARTH_SOURCE_VECTOR_FIRST_ROW_NONCLAIM.csv:DD_EARTH1083_0_bulk_weighted | False | False | False | False |
| SVF1901_1_profile_weighting | profile/worldtube weighted Earth source vector | MISSING | MISSING_SOURCE_PROFILE_WEIGHTING | Earth profile or point-source/common-mode theorem with residual bound | P8_Y5_R10_1083_SOURCE_VECTOR_CAVEAT_GATE.csv:SCG1083_0_profile_weighting | False | False | False | False |
| SVF1901_2_parent_basis_map | MTS parent basis to source-vector basis | MISSING | MISSING_PARENT_OPERATOR_BASIS_MAP | map from parent residual vector to DD/source/material response basis | P8_Y5_R10_1083_SOURCE_VECTOR_CAVEAT_GATE.csv:SCG1083_1_parent_to_DD_map | False | False | False | False |
| SVF1901_3_source_vector_contract | R_source^Earth | MISSING_SOURCE_VECTOR | SOURCE_VECTOR_CONTRACT_OPEN | derive common-mode theorem or source-backed composition/worldtube vector | P8_Y5_R10_1424_SOURCE_VECTOR_CONTRACT.csv:SRCMAP1424_0_R_source | False | False | False | False |
| SVF1901_4_residual_coefficients | r_source residual coefficients | VECTOR_DECLARED_VALUES_MISSING | PARENT_RESIDUAL_COEFFICIENTS_MISSING | qbar_source_weight/current_rescaling/non-Hilbert/geometric/readout coefficients | P8_Y5_R10_1419_SOURCE_RESIDUAL_COEFFICIENT_VECTOR.csv:SRCV1419_5_verdict | False | False | False | False |
| SVF1901_5_absorption_guard | measured GM guard | algebra accepted; no relative absorption | GUARD_DERIVED_NONCLAIM | relative source vector theorem-zero or executable finite vector | P8_Y5_PARENT_QLOC_1901_COMMON_MODE_ABSORPTION_ALGEBRA.csv:ALG1901_3_claim_limit | False | False | False | False |
| SVF1901_6_verdict | source-vector executable branch | NONCLAIM_LEDGER_ONLY | SOURCE_VECTOR_NOT_EXECUTABLE_NONCLAIM | SVF1901_1 through SVF1901_4 filled or theorem-zero | SVF1901_0_bulk_dd_context through SVF1901_5_absorption_guard | False | False | False | False |

## Dry-Run Cases

| case_id | guard_algebra_ok | relative_zero_proved | source_vector_filled | uses_bulk_as_profile | uses_measured_g_hiding | score_attempt | expected_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DRY1901_0_use_guard_as_zero | True | False | False | False | False | False | REFUSED_GUARD_IS_NOT_ZERO_THEOREM | False |
| DRY1901_1_measured_g_hiding | True | False | False | False | True | False | REFUSED_MEASURED_G_RELATIVE_HIDING | False |
| DRY1901_2_bulk_as_profile | True | False | False | True | False | False | REFUSED_BULK_VECTOR_AS_PROFILE_WEIGHTED_SOURCE | False |
| DRY1901_3_source_missing | True | False | False | False | False | True | REFUSED_SOURCE_VECTOR_NOT_EXECUTABLE | False |
| DRY1901_4_guard_missing | False | True | True | False | False | False | REFUSED_GUARD_ALGEBRA_MISSING | False |

## Dry-Run Results

| case_id | computed_status | expected_status | status_match | claim_allowed | valid_for_claim | generated_utc |
| --- | --- | --- | --- | --- | --- | --- |
| DRY1901_0_use_guard_as_zero | REFUSED_GUARD_IS_NOT_ZERO_THEOREM | REFUSED_GUARD_IS_NOT_ZERO_THEOREM | True | False | False | 2026-06-19T18:59:02.453786+00:00 |
| DRY1901_1_measured_g_hiding | REFUSED_MEASURED_G_RELATIVE_HIDING | REFUSED_MEASURED_G_RELATIVE_HIDING | True | False | False | 2026-06-19T18:59:02.453786+00:00 |
| DRY1901_2_bulk_as_profile | REFUSED_BULK_VECTOR_AS_PROFILE_WEIGHTED_SOURCE | REFUSED_BULK_VECTOR_AS_PROFILE_WEIGHTED_SOURCE | True | False | False | 2026-06-19T18:59:02.453786+00:00 |
| DRY1901_3_source_missing | REFUSED_SOURCE_VECTOR_NOT_EXECUTABLE | REFUSED_SOURCE_VECTOR_NOT_EXECUTABLE | True | False | False | 2026-06-19T18:59:02.453786+00:00 |
| DRY1901_4_guard_missing | REFUSED_GUARD_ALGEBRA_MISSING | REFUSED_GUARD_ALGEBRA_MISSING | True | False | False | 2026-06-19T18:59:02.453786+00:00 |

## Claim Gate

| gate_id | condition | current_status | source_anchor | gate_pass | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| CG1901_0_guard | measured-G common-mode absorption algebra is explicit | PASS_ALGEBRA_GUARD_DERIVED_NONCLAIM | P8_Y5_PARENT_QLOC_1901_COMMON_MODE_ABSORPTION_ALGEBRA.csv:ALG1901_0_decomposition | False | False |
| CG1901_1_relative_zero | relative source vector is parent theorem-zero | FAIL_RELATIVE_SOURCE_ZERO_NOT_PARENT_DERIVED | P8_Y5_PARENT_QLOC_1901_MEASURED_G_COMMON_MODE_GUARD_ATTEMPT.csv:GMG1901_3_parent_zero_missing | False | False |
| CG1901_2_source_vector | finite source vector is profile-weighted and executable if not zero | FAIL_SOURCE_VECTOR_NOT_EXECUTABLE_NONCLAIM | P8_Y5_PARENT_QLOC_1901_SOURCE_VECTOR_FILL_NONCLAIM.csv:SVF1901_6_verdict | False | False |
| CG1901_3_verdict | measured-G/source-vector branch supports WEP/local-GR claim | CLAIM_BLOCKED | CG1901_0_guard through CG1901_2_source_vector | False | False |

## Decision Ledger

| decision_id | decision | reason | status | next_dependency | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| DEC1901_0_guard | accept measured-G guard as an algebraic discipline theorem | one scalar calibration removes one universal scalar only; it cannot remove relative source vectors, range hair, or frame/time hair | GUARD_ALGEBRA_ACCEPTED_NONCLAIM | relative source zero theorem or source-vector fill | False |
| DEC1901_1_zero | do not claim source-vector zero | no-source-slot/source-label forgetting and common-mode zero theorem are not parent-signed | RELATIVE_SOURCE_ZERO_UNSIGNED | source-label forgetting before GM calibration | False |
| DEC1901_2_next | attack source-label forgetting before GM calibration | it is the minimal theorem that would turn the guard from anti-cheat rule into local-GR source universality | NEXT_TARGET_SELECTED | 1902 source-label forgetting or profile source-vector map | False |

## Next Target

| branch_id | route_id | selection_status | target_doc | target_script | objective | success_condition | do_not | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | NEXT1901_0_primary | selected | 1902-Y5-R2FR-source-label-forgetting-before-GM-calibration-or-profile-source-vector-map.md | scripts/Y5_R2FR_source_label_forgetting_before_GM_calibration_or_profile_source_vector_map_1902.py | try to prove source labels are forgotten before measured-G calibration; if it fails, build a profile/worldtube source-vector map as nonclaim | parent-signed source-label forgetting/no-source-slot theorem, or source-vector profile map rows with no measured-G hiding | do not treat the measured-G guard as a zero theorem, do not use bulk Earth DD vector as profile-weighted source, and do not score WEP from unfilled source vectors | False | False |

## Project Status Snapshot

| status_id | area | summary | risk_level | project_meaning | next_action | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| STAT1901_0_positive | Newton/GR calibration discipline | measured-G/common-mode absorption is now an explicit algebraic guard | ANTI_CHEAT_GUARD_STRONG | this strengthens the derivation discipline: Newtonian calibration cannot hide WEP-active source weights | prove source-label forgetting or fill finite source vector | False |
| STAT1901_1_open | local-GR source universality | relative source-vector zero remains unproved and source vector is not executable | CORE_COUPLING_GAP_REMAINS | we have a good guardrail, not yet a local-GR source theorem | 1902 source-label forgetting before GM calibration | False |

## Validation

| validation_id | status | detail | valid_for_claim |
| --- | --- | --- | --- |
| VAL1901_00_sources | PASS | all local source paths exist and needles found | False |
| VAL1901_01_guard_verdict | PASS | measured-G guard algebra accepted but relative zero remains unsigned | False |
| VAL1901_02_algebra | PASS | absorption algebra rows recorded as guard/nonclaim | False |
| VAL1901_03_source_vector | PASS | source-vector fill rows remain nonclaim/not executable | False |
| VAL1901_04_dryrun | PASS | dry-run refuses guard-as-zero, measured-G hiding, bulk-as-profile, missing vector, and missing guard | False |
| VAL1901_05_claim_gate | PASS | claim remains blocked | False |
| VAL1901_06_next_target | PASS | 1902 target selected | False |
| VAL1901_07_claim_flags_false | PASS | all generated claim/scoring/signature flags remain false | False |
| VAL1901_08_blocked_markers_not_ready | PASS | blocked/unsigned/nonclaim rows are not score-ready | False |
| VAL1901_09_csv_parse | PASS | parsed 10 csv files | False |
| VAL1901_10_branch_copies | PASS | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\branch_locked_wep\residuals\P8_Y5_PARENT_QLOC_1901_MEASURED_G_COMMON_MODE_GUARD_ATTEMPT.csv; D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\source-weight\docs\COMMON_MODE_ABSORPTION_ALGEBRA_1901.csv; D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\rab-sector\acquisition-queue\JR1901_SOURCE_VECTOR_FILL_NONCLAIM.csv; D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\quarantine\1901\P8_Y5_PARENT_QLOC_1901_GUARD_SOURCE_VECTOR_DRYRUN_RESULTS.csv | False |
| VAL1901_11_pycache_absent | PASS | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\scripts\__pycache__ | False |
| VAL1901_12_formalization_untouched | PASS | formalization_1901_count=0 | False |
| VAL1901_OVERALL | PASS | 1901 measured-G common-mode guard or source-vector fill | False |
