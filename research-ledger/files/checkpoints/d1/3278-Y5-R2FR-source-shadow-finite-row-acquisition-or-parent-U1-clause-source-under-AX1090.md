# 3278 - Source-shadow finite row acquisition or parent U1 clause source under AX1090

## Summary

3278 does **not** claim local GR, Maxwell closure, WEP, R10, PPN, clock, or orbital success. It takes one real step forward: the nonconserved silent-compensator route is now promoted to a source-backed local mathematical clause, using the 3276/3277 gauge-variation rows.

The finite `C_J` branch is also forced through an acquisition gate. No real source-backed finite coefficient row is found in the current 3276/3277 intake evidence, so `epsilon_shadow`, `c_A/kappa_A`, `w_A`, and readout reentry remain explicit nonclaim debt rather than hidden assumptions.

## Exact Clause

For a silent source term

`S_shadow = int mu A_Q_mu J_comp^mu`,

with `delta_lambda A_Q_mu = nabla_mu lambda`,

`delta_lambda S_shadow = int mu J_comp^mu nabla_mu lambda = - int mu lambda nabla_mu J_comp^mu + boundary`.

For arbitrary compact-support `lambda`, exact U(1) requires `nabla_mu J_comp^mu=0`, unless `J_comp` is the Noether current of a real charged sector whose Ward identity supplies the conservation law. Therefore a nonconserved silent compensator cannot be used as a hidden cancellation mechanism for variable `kappa_J`.

## Target Selection
| target_id | selected_target | why_this_target | finite_row_result |
| --- | --- | --- | --- |
| TARGET3278_0_exact_clause_first | source the exact U1 nonconserved-compensator rejection clause | it is a real mathematical clause already derived in 3276/3277 and does not require pretending a finite coefficient exists. | no source-backed numeric conserved-shadow/current-rescale/pre-action-weight/readout coefficient found in the searched local evidence set. |
| TARGET3278_1_finite_row_guard | do not promote C_J=0 from absence of a finite row | missing finite data is evidence of a gap, not evidence for the zero theorem; the exact clause only kills nonconserved silent compensation. | finite branch remains explicit and nonclaim. |

## Exact U1 Clause Source Rows
| clause_id | source_backed | parent_action_signed | claim_status | valid_for_claim |
| --- | --- | --- | --- | --- |
| CLAUSE3278_0_nonconserved_silent_compensator_forbidden | true | false | CLAUSE_SOURCE_BACKED_PARENT_ACTION_UNSIGNED | false |
| CLAUSE3278_1_F_only_wave_response_not_CJ_compensator | true | false | CLAUSE_SOURCE_BACKED_SIDE_CONDITIONS_REMAIN | false |
| CLAUSE3278_2_parent_exact_U1_signature_not_signed | true | false | BLOCKS_LOCAL_GR_OR_MAXWELL_CLAIM | false |

## Finite Coefficient Source Scan
| scan_id | source_row | quantity | value_field | real_finite_numeric_candidate | reason |
| --- | --- | --- | --- | --- | --- |
| SCAN3278_0 | SSR3276_0_minimal_domain_zero_conditional | C_J_effective | 0 | false | missing, forbidden, theorem-zero, conditional, or smoke row |
| SCAN3278_1 | SSR3276_1_live_source_shadow_missing | epsilon_shadow | MISSING_SOURCE_BACKED_SHADOW_BLOCK | false | missing, forbidden, theorem-zero, conditional, or smoke row |
| SCAN3278_2 | SSR3276_2_magnetization_exact_no_flux_zero | epsilon_mag_boundary | 0 | false | missing, forbidden, theorem-zero, conditional, or smoke row |
| SCAN3278_3 | SSR3276_3_nonconserved_compensator_forbidden_smoke | epsilon_nonconserved_compensator | FORBIDDEN_BY_U1_UNLESS_REAL_SECTOR | false | missing, forbidden, theorem-zero, conditional, or smoke row |
| SCAN3278_4 | SSR3276_4_half_bound_smoke | C_J_effective | 3.474494278738e-13 | false | missing, forbidden, theorem-zero, conditional, or smoke row |
| SCAN3278_5 | SSR3276_5_twice_bound_smoke | C_J_effective | 1.389797711495e-12 | false | missing, forbidden, theorem-zero, conditional, or smoke row |
| SCAN3278_6 | SSI3277_0_exact_U1_zero_conditional | C_J_effective | 0 | false | missing, forbidden, theorem-zero, conditional, or smoke row |
| SCAN3278_7 | SSI3277_1_conserved_shadow_missing | epsilon_shadow | MISSING_SOURCE_BACKED_CONSERVED_SHADOW | false | missing, forbidden, theorem-zero, conditional, or smoke row |
| SCAN3278_8 | SSI3277_2_current_rescale_missing | c_A_or_kappa_A | MISSING_CURRENT_RESCALE_COEFFICIENT | false | missing, forbidden, theorem-zero, conditional, or smoke row |
| SCAN3278_9 | SSI3277_3_pre_action_weight_missing | w_A | MISSING_PRE_ACTION_WEIGHT | false | missing, forbidden, theorem-zero, conditional, or smoke row |
| SCAN3278_10 | SSI3277_4_magnetization_no_flux_zero | epsilon_mag_boundary | 0 | false | missing, forbidden, theorem-zero, conditional, or smoke row |
| SCAN3278_11 | SSI3277_5_nonconserved_forbidden | J_comp_nonconserved | FORBIDDEN_BY_EXACT_U1_UNLESS_REAL_CHARGED_SECTOR | false | missing, forbidden, theorem-zero, conditional, or smoke row |
| SCAN3278_12 | SSI3277_6_half_bound_smoke | C_J_effective | 3.474494278738e-13 | false | missing, forbidden, theorem-zero, conditional, or smoke row |
| SCAN3278_13 | SSI3277_7_twice_bound_smoke | C_J_effective | 1.389797711495e-12 | false | missing, forbidden, theorem-zero, conditional, or smoke row |
| SCAN3278_SUMMARY | summary | epsilon_shadow/c_A_or_kappa_A/w_A/readout_reentry | NO_REAL_FINITE_SOURCE_BACKED_NUMERIC_ROW_FOUND | false | the searched rows contain only missing, forbidden, theorem-zero, conditional no-flux, or smoke values. |

## Source-Shadow Acquisition Audit
| audit_id | route | target_quantity | result | next_action |
| --- | --- | --- | --- | --- |
| ACQ3278_0_nonconserved_clause | exact U1 clause source | J_comp_nonconserved | SOURCE_BACKED_AS_FORBIDDEN_SILENT_ROUTE | do not put this into numeric runner as a finite residual; route real sectors to conserved-shadow branch. |
| ACQ3278_1_conserved_shadow | finite source-shadow coefficient | epsilon_shadow | BLOCKED_NO_SOURCE_BACKED_NUMERIC_ROW | hunt for a real parent/source row or demote C_J finite branch to closure-only. |
| ACQ3278_2_current_rescale | current normalization/readout rescale | c_A_or_kappa_A | BLOCKED_BY_RESCALING_COUNTEREXAMPLE_AND_MISSING_COEFFICIENT | source an actual current map or treat as explicit residual coefficient. |
| ACQ3278_3_pre_action_weight | pre-action source weight | w_A | BLOCKED_NO_PARENT_WEIGHT_MAP | source a parent variational weight map before using it in C_J. |
| ACQ3278_4_magnetization_boundary | F-only wave/Poynting/magnetization response | epsilon_mag_boundary | EXACT_ZERO_ONLY_WITH_NO_FLUX_SIDE_CONDITION | move wave/Poynting effects into EM stress and boundary residuals, not current-normalization C_J. |

## Intake Rows
| row_id | current_type | coefficient | numeric_value | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| SSI3278_0_exact_U1_clause_nonconserved_forbidden | nonconserved_forbidden_clause | J_comp_nonconserved | FORBIDDEN_BY_SOURCE_BACKED_EXACT_U1_CLAUSE_IF_PARENT_U1_HOLDS | CLAUSE_SOURCE_BACKED_NONCLAIM | false |
| SSI3278_1_conserved_shadow_missing | conserved_shadow | epsilon_shadow | MISSING_SOURCE_BACKED_CONSERVED_SHADOW | INTAKE_REQUIRED | false |
| SSI3278_2_current_rescale_missing | current_rescale | c_A_or_kappa_A | MISSING_CURRENT_RESCALE_COEFFICIENT | INTAKE_REQUIRED | false |
| SSI3278_3_pre_action_weight_missing | pre_action_weight | w_A | MISSING_PRE_ACTION_WEIGHT | INTAKE_REQUIRED | false |
| SSI3278_4_magnetization_no_flux_zero | magnetization_boundary | epsilon_mag_boundary | 0 | THEOREM_ZERO_CONDITIONAL_NONCLAIM | false |
| SSI3278_5_half_bound_smoke | smoke | C_J_effective | 3.474494278738e-13 | SMOKE | false |
| SSI3278_6_twice_bound_smoke | smoke | C_J_effective | 1.389797711495e-12 | SMOKE | false |

## Bound Runner
| row_id | numeric_value | prediction_over_bound | result | expectation_met | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| SSI3278_0_exact_U1_clause_nonconserved_forbidden | FORBIDDEN_BY_SOURCE_BACKED_EXACT_U1_CLAUSE_IF_PARENT_U1_HOLDS | N/A | CLAUSE_PASS_NONNUMERIC_NONCLAIM | true | false |
| SSI3278_1_conserved_shadow_missing | MISSING_SOURCE_BACKED_CONSERVED_SHADOW | MISSING | REFUSE_OR_FAIL | true | false |
| SSI3278_2_current_rescale_missing | MISSING_CURRENT_RESCALE_COEFFICIENT | MISSING | REFUSE_OR_FAIL | true | false |
| SSI3278_3_pre_action_weight_missing | MISSING_PRE_ACTION_WEIGHT | MISSING | REFUSE_OR_FAIL | true | false |
| SSI3278_4_magnetization_no_flux_zero | 0 | 0.000000000000e+00 | PASS_NUMERIC_NONCLAIM | true | false |
| SSI3278_5_half_bound_smoke | 3.474494278738e-13 | 5.000000000001e-01 | PASS_NUMERIC_NONCLAIM | true | false |
| SSI3278_6_twice_bound_smoke | 1.389797711495e-12 | 2.000000000000e+00 | FAIL_BOUND | true | false |

## Promotion Gates
| gate_id | passed | claim_allowed | detail |
| --- | --- | --- | --- |
| GATE3278_0_exact_clause_sourced | true | false | mathematical clause promoted; parent action exact-U1 remains unsigned. |
| GATE3278_1_parent_action_signature | false | false | 3277 verdict remains EXACT_U1_REPRESENTATION_SIGNATURE_NOT_PARENT_SIGNED. |
| GATE3278_2_finite_coefficient_found | false | false | scan found no live finite source-backed numeric row; only missing/theorem-zero/smoke rows. |
| GATE3278_3_runner_behaviour | true | false | SSI3278_0_exact_U1_clause_nonconserved_forbidden=CLAUSE_PASS_NONNUMERIC_NONCLAIM;SSI3278_1_conserved_shadow_missing=REFUSE_OR_FAIL;SSI3278_2_current_rescale_missing=REFUSE_OR_FA... |
| GATE3278_4_no_local_claim | true | false | 3278 is a clause-source and finite-row acquisition checkpoint only. |

## Decisions
| decision_id | decision | why_it_moves_forward | claim_allowed |
| --- | --- | --- | --- |
| DEC3278_0_real_progress | Promote the nonconserved silent-compensator rejection from a target to a source-backed local mathematical clause. | one branch is now closed cleanly: no hidden nonconserved current can be inserted to cancel variable kappa_J without either breaking exact U1 or becoming a real charged sector. | false |
| DEC3278_1_wave_poynting_route | Keep wave/Poynting/F-only response in EM stress and boundary residuals rather than C_J current normalization. | this preserves the user's background-field intuition while keeping the math honest: F-only terms are real physics, but their current is identically conserved. | false |
| DEC3278_2_finite_branch | Finite C_J rows are not found; they remain explicit source-acquisition debt. | the next step cannot be another abstract theorem loop; it must either find a real coefficient/source map or demote the C_J finite branch to closure-only. | false |

## Next Target
| next_id | target_doc | objective | guardrail |
| --- | --- | --- | --- |
| NEXT3278_0_3279 | 3279-Y5-R2FR-first-finite-source-shadow-row-source-hunt-or-CJ-closure-demotion-under-AX1090.md | Make one aggressive finite-row source hunt for epsilon_shadow, c_A/kappa_A, w_A, or readout reentry across the local corpus; if no real numeric/source map exists, demote the fin... | Do not write another theorem-only target unless it names a new source path and a real coefficient map; finite rows must be numeric, unit-labelled, source-backed, and valid_for_c... |

## Validation
| check_id | check | passed | detail |
| --- | --- | --- | --- |
| VAL3278_0_sources_exist | all cited source paths exist | true |  |
| VAL3278_1_sources_parse | all cited source paths parse | true |  |
| VAL3278_2_outputs_parse | all 3278 output CSVs parse | true | non-validation outputs parsed before validation write |
| VAL3278_3_clause_promoted_not_claimed | at least one exact U1 clause is source-backed but no clause is valid_for_claim | true | CLAUSE3278_0_nonconserved_silent_compensator_forbidden=CLAUSE_SOURCE_BACKED_PARENT_ACTION_UNSIGNED;CLAUSE3278_1_F_only_wave_response_not_CJ_compensator=CLAUSE_SOURCE_BACKED_SIDE... |
| VAL3278_4_no_finite_candidate_fabricated | finite source-shadow scan does not fabricate a numeric row | true | no real finite numeric source-backed candidate in 3276/3277 intake rows |
| VAL3278_5_intake_rows_nonclaim | all 3278 intake rows remain nonclaim | true |  |
| VAL3278_6_runner_expectations | bound runner expectations all match | true | SSI3278_0_exact_U1_clause_nonconserved_forbidden=CLAUSE_PASS_NONNUMERIC_NONCLAIM;SSI3278_1_conserved_shadow_missing=REFUSE_OR_FAIL;SSI3278_2_current_rescale_missing=REFUSE_OR_FA... |
| VAL3278_7_claim_gates_false | no 3278 gate allows local-GR/WEP/Maxwell claim | true | all claim_allowed=false |
| VAL3278_8_formalization_untouched | formalization-workbench modified-file count remains zero by this script | true | formalization_changed_count=0 |
| VAL3278_9_overall | 3278 validation overall | true | all required checks passed |

Generated UTC: 2026-06-27T15:17:25.973989+00:00
