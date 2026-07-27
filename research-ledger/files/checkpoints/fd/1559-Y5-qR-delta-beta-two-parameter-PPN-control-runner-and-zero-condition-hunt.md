# 1559 - q_R/delta_beta Two-Parameter PPN Control Runner and Zero-Condition Hunt

## Verdict
- The `q_R/delta_beta` local branch now has a two-parameter PPN control runner.
- `q_R` is clamped by the Cassini/gamma row through `gamma-1=q_R`; `delta_beta` is clamped by the beta row through `beta-1=delta_beta`.
- Mercury perihelion exposes the degeneracy line `(2 q_R-delta_beta)/3`, so it cannot by itself separate spatial reciprocal hair from nonlinear beta drift.
- The runner can reject hypothetical leak vectors, but it still cannot score MTS as a prediction because the parent action has not produced the vector.
- The next honest target is the parent weak-field zero-condition derivation: prove `q_R=0` and `delta_beta=0`, or demote local GR to bounded closure.

## Source Register
| source_id | source_path | exists | needle_found | needles |
| --- | --- | --- | --- | --- |
| SRC1559_0_1558_doc | 1558-Y5-qR-beta-matter-clock-coefficient-source-map-or-rejection.md | True | True | `q_R` now has a derived PPN translation; not yet a local-GR derivation |
| SRC1559_1_1558_validation | source-intake/mts_residuals/P8_Y5_BRR545_1558_VALIDATION.csv | True | True | VAL1558_OVERALL; PASS |
| SRC1559_2_1558_next | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1558_NEXT_TARGET.csv | True | True | 1559-Y5-qR-delta-beta-two-parameter-PPN-control-runner |
| SRC1559_3_1558_coefficients | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1558_PPN_COEFFICIENT_DERIVATION.csv | True | True | PPNC1558_0_qR_gamma; PPNC1558_6_perihelion_degeneracy |
| SRC1559_4_1558_readiness | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1558_COEFFICIENT_READINESS_MATRIX.csv | True | True | READY1558_0_qR_gamma; TRANSLATION_ONLY |
| SRC1559_5_1557_budget | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1557_BOUND_BUDGET_NONCLAIM.csv | True | True | BUD1557_0_qR; BUD1557_1_delta_beta |
| SRC1559_6_14_doc | 14-closure-deviation-PPN-sensitivity.md | True | True | Mercury shift factor = (2 q_R - delta_beta)/3. |
| SRC1559_7_13_doc | 13-local-closure-PPN-benchmark.md | True | True | R_AB approx q_R L; gamma approx 1 + q_R. |
| SRC1559_8_10_doc | 10-observer-map-symplectic-contract.md | True | True | derive R_AB=0 from the parent theory; beta - 1 = 0 |
| SRC1559_9_local_bound_claims | source-intake/local_bounds/local_bound_claims.csv | True | True |  |

## Two-Parameter Model
| model_id | observable_response | leak_parameter | coefficient | units | model_status |
| --- | --- | --- | --- | --- | --- |
| MODEL1559_0_gamma | gamma_minus_1 | q_R | 1 | dimensionless | PPN_TRANSLATION_CONTROL_NOT_MTS_PREDICTION |
| MODEL1559_1_beta | beta_minus_1 | delta_beta | 1 | dimensionless | PPN_TRANSLATION_CONTROL_NOT_MTS_PREDICTION |
| MODEL1559_2_light | solar_light_bending_residual_arcsec | q_R | 0.8756216406841224 | arcsec | PPN_TRANSLATION_CONTROL_NOT_MTS_PREDICTION |
| MODEL1559_3_shapiro | solar_Shapiro_residual_microseconds | q_R | 59.7375179242781 | microseconds | PPN_TRANSLATION_CONTROL_NOT_MTS_PREDICTION |
| MODEL1559_4_mercury_qR | Mercury_perihelion_residual_arcsec_per_century | q_R | 28.65467507274745 | arcsec/century | PPN_TRANSLATION_CONTROL_NOT_MTS_PREDICTION |
| MODEL1559_5_mercury_beta | Mercury_perihelion_residual_arcsec_per_century | delta_beta | -14.32733753637373 | arcsec/century | PPN_TRANSLATION_CONTROL_NOT_MTS_PREDICTION |
| MODEL1559_6_mercury_combo | Mercury_perihelion_fractional_factor | q_R; delta_beta | (2 q_R - delta_beta)/3 | dimensionless | PPN_TRANSLATION_CONTROL_NOT_MTS_PREDICTION |

## Parameter Bound Box
| bound_id | parameter_or_combo | local_bound_rows | measured_or_central | one_sigma | control_bound | interpretation |
| --- | --- | --- | --- | --- | --- | --- |
| BOX1559_0_qR | q_R | R3_gamma | 2.1e-05 | 2.3e-05 | 2.3e-05 | q_R = gamma-1 in the PPN translation map |
| BOX1559_1_delta_beta | delta_beta | R4_beta | -4.1e-05 | 7.8e-05 | 7.8e-05 | delta_beta = beta-1 by PPN parameter definition; beta row carries its original gamma-prior caveat |
| BOX1559_2_perihelion_combo | 2 q_R - delta_beta | R3_gamma; R4_beta | not_independently_fit_here | not_independently_fit_here | derived_combination_only | perihelion constrains the combination through (2 q_R-delta_beta)/3, but no independent Mercury covariance is reconstructed here |

## Control Runner
| case_id | label | q_R_input | delta_beta_input | gamma_minus_1 | beta_minus_1 | mercury_residual_arcsec_per_century | control_status | purpose |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CASE1559_0_GR_origin | GR/null closure origin | 0 | 0 | 0 | 0 | 0 | PASS_CONTROL_BOX | baseline origin of q_R/delta_beta plane |
| CASE1559_1_Cassini_q_edge | positive q_R bound edge | 2.3e-05 | 0 | 2.3e-05 | 0 | 0.000659057526673 | PASS_CONTROL_BOX | Cassini gamma-edge control point |
| CASE1559_2_beta_edge | positive delta_beta bound edge | 0 | 7.8e-05 | 0 | 7.8e-05 | -0.00111753232784 | PASS_CONTROL_BOX | beta edge control point |
| CASE1559_3_perihelion_degeneracy | perihelion degeneracy line | 2e-05 | 4e-05 | 2e-05 | 4e-05 | 0 | PASS_CONTROL_BOX | 2 q_R - delta_beta = 0 while gamma/beta bounds still matter |
| CASE1559_4_q_fail | q_R too large | 5e-05 | 0 | 5e-05 | 0 | 0.00143273375364 | FAIL_CONTROL_BOX | shows Cassini/gamma clamp |
| CASE1559_5_beta_fail | delta_beta too large | 0 | 0.00012 | 0 | 0.00012 | -0.00171928050436 | FAIL_CONTROL_BOX | shows beta clamp |

## Parent Zero-Condition Hunt
| zero_id | target_zero | required_statement | mathematical_content | status | next_derivation_step |
| --- | --- | --- | --- | --- | --- |
| ZERO1559_0_qR_linear | q_R=0 | parent equations must force R_AB=O(L^2), not R_AB=q_R L | linear reciprocal strain coefficient vanishes | MISSING_PARENT_FIELD_EQUATION | derive first-order observer-sector equation whose regular/local-vacuum solution has T^2 S=1+O(L^2) |
| ZERO1559_1_qR_charge | q_R=0 | no reciprocal boundary/current charge may source R_AB at O(L) | Q_R local charge is zero or pure gauge with proper boundary term | MISSING_ZERO_CHARGE_THEOREM | supply first-class constraint/no-boundary-charge proof rather than closure axiom |
| ZERO1559_2_qR_matter | q_R observed by matter | matter and photons must read the same T,S coframe, otherwise gamma translation is not universal | universal coframe descent | MISSING_MATTER_DESCENT | derive matter action descent through the same observer map |
| ZERO1559_3_beta_second_order | delta_beta=0 | second-order weak-field completion must match beta=1 in a valid PPN gauge | nonlinear source self-coupling equals GR control lane | MISSING_SECOND_ORDER_PARENT_COMPLETION | derive O(U^2) metric/coframe field equation and coordinate/gauge map |
| ZERO1559_4_beta_conservation | delta_beta=0 | Bianchi/conservation identity must fix the nonlinear potential terms consistently | local conservation closes source normalization and beta completion | MISSING_BIANCHI_SOURCE_IDENTITY | derive the parent identity linking field equations to matter conservation |
| ZERO1559_5_no_extra_modes | q_R=0 and delta_beta=0 | extra finite-range/scalar/tracefree modes must decouple or be suppressed locally | no surviving local hair in the PPN residual vector | MISSING_MODE_DECOUPLING_THEOREM | derive decoupling/suppression or keep local branch as bounded closure |

## Claim Gates
| gate_id | claim_gate | status | reason |
| --- | --- | --- | --- |
| GATE1559_0_control_runner | two-parameter PPN control runner | PASS_NONCLAIM_CONTROL | control-plane arithmetic works and can reject trial leak vectors |
| GATE1559_1_parent_prediction | MTS predicts q_R and delta_beta | BLOCKED_NO_CLAIM | no parent equations produce q_R/delta_beta values |
| GATE1559_2_GR_origin | MTS derives local GR origin q_R=0, delta_beta=0 | BLOCKED_NO_CLAIM | zero-condition ledger remains unsigned |
| GATE1559_3_matter_universal | local bounds apply to all matter/photons | BLOCKED_NO_CLAIM | matter/coframe descent still missing |
| GATE1559_4_empirical_score | empirical MTS local-bound score | BLOCKED_NO_CLAIM | runner can score hypothetical vectors, not the theory |

## Decision
| decision_id | decision | result | reason |
| --- | --- | --- | --- |
| DEC1559_0_verdict | two-parameter local control status | CONTROL_RUNNER_READY_ZERO_THEOREM_MISSING | q_R/delta_beta local residuals are now test-shaped, but the parent theory has not derived the GR origin |
| DEC1559_1_next | next target | NEXT_1560_PARENT_WEAK_FIELD_ZERO_CONDITION_DERIVATION | the best next route is to attack the parent equations needed for q_R=0 and delta_beta=0 |

## Validation
| check_id | result | detail |
| --- | --- | --- |
| VAL1559_0_sources_exist | PASS | all cited 1559 source paths exist |
| VAL1559_1_needles_found | PASS | all registered evidence needles found |
| VAL1559_2_model_q_beta | PASS | q_R and delta_beta unit translation rows present |
| VAL1559_3_model_perihelion_combo | PASS | perihelion degeneracy model present |
| VAL1559_4_bound_box | PASS | q_R and delta_beta bound box written |
| VAL1559_5_GR_origin_passes | PASS | GR origin passes control box |
| VAL1559_6_q_fail_fails | PASS | oversized q_R fails Cassini/gamma bound |
| VAL1559_7_degeneracy_line | PASS | perihelion degeneracy example has zero Mercury residual |
| VAL1559_8_zero_conditions | PASS | parent zero-condition hunt ledger written |
| VAL1559_9_claim_gates | PASS | local GR derivation remains blocked |
| VAL1559_10_decision_next | PASS | decision selects parent weak-field zero-condition derivation next |
| VAL1559_11_next_target | PASS | next target is parent weak-field zero-condition derivation or demotion |
| VAL1559_12_csv_parse | PASS | all generated 1559 CSVs parse cleanly |
| VAL1559_13_claim_flags_false | PASS | all generated prediction/claim flags remain false |
| VAL1559_14_branch_copies | PASS | branch/quarantine nonclaim copies written |
| VAL1559_15_pycache_absent | PASS | scripts __pycache__ absent after run |
| VAL1559_16_formalization_untouched | PASS | formalization modified-file count since start=0 |
| VAL1559_OVERALL | PASS | 1559 q_R/delta_beta two-parameter PPN control runner and zero-condition hunt validation |

## Next Target
| next_target | script | objective | do_not |
| --- | --- | --- | --- |
| 1560-Y5-parent-weak-field-zero-condition-derivation-or-demotion.md | scripts/Y5_parent_weak_field_zero_condition_derivation_or_demotion.py | attempt to derive the first-order q_R=0 condition and second-order delta_beta=0 condition from a parent weak-field field-equation/action structure; if this fails, demote the local GR branch to an explicit bounded-closure control lane | do not use the PPN control runner as a parent derivation; do not claim local GR/Newton reduction; do not edit formalization-workbench |
