# 2232 - Y5/R2FR q_R/delta_beta Two-Parameter PPN Control Runner And Zero-Condition Hunt

## Verdict
- 2232 imports the old `1559` q_R/delta_beta two-parameter PPN control runner into the current R2FR line.
- The control plane is now explicit: `q_R` maps to `gamma-1`, `delta_beta` maps to `beta-1`, and Mercury tracks the degeneracy `(2 q_R - delta_beta)/3`.
- The runner can reject hypothetical leak vectors, including oversized `q_R` and oversized `delta_beta`, but it cannot score MTS because the parent action has not produced the vector.
- The parent zero-condition hunt is now the real derivation target: force `R_AB=O(L^2)`, kill reciprocal charge, supply matter descent, derive second-order beta completion, and suppress extra local modes.
- Next target is the parent weak-field zero-condition derivation or demotion.

## Source Register
| source_id | source_path | path_exists | validation_overall_pass | role |
| --- | --- | --- | --- | --- |
| SRC2232_0_2231_doc | 2231-Y5-R2FR-qR-beta-matter-clock-coefficient-source-map-or-rejection.md | True |  | current coefficient source-map handoff |
| SRC2232_1_2231_validation | source-intake/mts_residuals/P8_Y5_BRR545_2231_VALIDATION.csv | True | True | current coefficient source-map handoff |
| SRC2232_2_2231_next | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2231_NEXT_TARGET.csv | True |  | current coefficient source-map handoff |
| SRC2232_3_1559_doc | 1559-Y5-qR-delta-beta-two-parameter-PPN-control-runner-and-zero-condition-hunt.md | True |  | older two-parameter PPN control evidence |
| SRC2232_4_1559_validation | source-intake/mts_residuals/P8_Y5_BRR545_1559_VALIDATION.csv | True | True | older two-parameter PPN control evidence |
| SRC2232_5_1559_model | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1559_TWO_PARAMETER_MODEL.csv | True |  | older two-parameter PPN control evidence |
| SRC2232_6_1559_bound_box | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1559_PARAMETER_BOUND_BOX_NONCLAIM.csv | True |  | older two-parameter PPN control evidence |
| SRC2232_7_1559_zero_hunt | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1559_PARENT_ZERO_CONDITION_HUNT.csv | True |  | older two-parameter PPN control evidence |
| SRC2232_8_1559_runner | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1559_TWO_PARAMETER_CONTROL_RUNNER_NONCLAIM.csv | True |  | older two-parameter PPN control evidence |
| SRC2232_9_1559_claim | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1559_CLAIM_GATE.csv | True |  | older two-parameter PPN control evidence |
| SRC2232_10_1559_decision | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1559_DECISION.csv | True |  | older two-parameter PPN control evidence |
| SRC2232_11_1559_next | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1559_NEXT_TARGET.csv | True |  | older two-parameter PPN control evidence |

## Two-Parameter Model
| model_id | observable_response | leak_parameter | coefficient | units | model_status |
| --- | --- | --- | --- | --- | --- |
| MODEL2232_0_gamma | gamma_minus_1 | q_R | 1 | dimensionless | PPN_TRANSLATION_CONTROL_NOT_MTS_PREDICTION |
| MODEL2232_1_beta | beta_minus_1 | delta_beta | 1 | dimensionless | PPN_TRANSLATION_CONTROL_NOT_MTS_PREDICTION |
| MODEL2232_2_light | solar_light_bending_residual_arcsec | q_R | 0.8756216406841224 | arcsec | PPN_TRANSLATION_CONTROL_NOT_MTS_PREDICTION |
| MODEL2232_3_shapiro | solar_Shapiro_residual_microseconds | q_R | 59.7375179242781 | microseconds | PPN_TRANSLATION_CONTROL_NOT_MTS_PREDICTION |
| MODEL2232_4_mercury_qR | Mercury_perihelion_residual_arcsec_per_century | q_R | 28.65467507274745 | arcsec/century | PPN_TRANSLATION_CONTROL_NOT_MTS_PREDICTION |
| MODEL2232_5_mercury_beta | Mercury_perihelion_residual_arcsec_per_century | delta_beta | -14.32733753637373 | arcsec/century | PPN_TRANSLATION_CONTROL_NOT_MTS_PREDICTION |
| MODEL2232_6_mercury_combo | Mercury_perihelion_fractional_factor | q_R; delta_beta | (2 q_R - delta_beta)/3 | dimensionless | PPN_TRANSLATION_CONTROL_NOT_MTS_PREDICTION |

## Parameter Bound Box
| bound_id | parameter_or_combo | local_bound_rows | measured_or_central | one_sigma | control_bound | bound_status |
| --- | --- | --- | --- | --- | --- | --- |
| BOX2232_0_qR | q_R | R3_gamma | 2.1e-05 | 2.3e-05 | 2.3e-05 | CONTROL_CONSTRAINT_NOT_PARENT_PREDICTION |
| BOX2232_1_delta_beta | delta_beta | R4_beta | -4.1e-05 | 7.8e-05 | 7.8e-05 | CONTROL_CONSTRAINT_NOT_PARENT_PREDICTION |
| BOX2232_2_perihelion_combo | 2 q_R - delta_beta | R3_gamma; R4_beta | not_independently_fit_here | not_independently_fit_here | derived_combination_only | CONTROL_CONSTRAINT_NOT_PARENT_PREDICTION |

## Control Runner
| case_id | label | q_R_input | delta_beta_input | gamma_minus_1 | beta_minus_1 | mercury_residual_arcsec_per_century | control_status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CASE2232_0_GR_origin | GR/null closure origin | 0 | 0 | 0 | 0 | 0 | PASS_CONTROL_BOX |
| CASE2232_1_Cassini_q_edge | positive q_R bound edge | 2.3e-05 | 0 | 2.3e-05 | 0 | 0.000659057526673 | PASS_CONTROL_BOX |
| CASE2232_2_beta_edge | positive delta_beta bound edge | 0 | 7.8e-05 | 0 | 7.8e-05 | -0.00111753232784 | PASS_CONTROL_BOX |
| CASE2232_3_perihelion_degeneracy | perihelion degeneracy line | 2e-05 | 4e-05 | 2e-05 | 4e-05 | 0 | PASS_CONTROL_BOX |
| CASE2232_4_q_fail | q_R too large | 5e-05 | 0 | 5e-05 | 0 | 0.00143273375364 | FAIL_CONTROL_BOX |
| CASE2232_5_beta_fail | delta_beta too large | 0 | 0.00012 | 0 | 0.00012 | -0.00171928050436 | FAIL_CONTROL_BOX |

## Parent Zero-Condition Hunt
| zero_id | target_zero | required_statement | mathematical_content | status | next_derivation_step |
| --- | --- | --- | --- | --- | --- |
| ZERO2232_0_qR_linear | q_R=0 | parent equations must force R_AB=O(L^2), not R_AB=q_R L | linear reciprocal strain coefficient vanishes | MISSING_PARENT_FIELD_EQUATION | derive first-order observer-sector equation whose regular/local-vacuum solution has T^2 S=1+O(L^2) |
| ZERO2232_1_qR_charge | q_R=0 | no reciprocal boundary/current charge may source R_AB at O(L) | Q_R local charge is zero or pure gauge with proper boundary term | MISSING_ZERO_CHARGE_THEOREM | supply first-class constraint/no-boundary-charge proof rather than closure axiom |
| ZERO2232_2_qR_matter | q_R observed by matter | matter and photons must read the same T,S coframe, otherwise gamma translation is not universal | universal coframe descent | MISSING_MATTER_DESCENT | derive matter action descent through the same observer map |
| ZERO2232_3_beta_second_order | delta_beta=0 | second-order weak-field completion must match beta=1 in a valid PPN gauge | nonlinear source self-coupling equals GR control lane | MISSING_SECOND_ORDER_PARENT_COMPLETION | derive O(U^2) metric/coframe field equation and coordinate/gauge map |
| ZERO2232_4_beta_conservation | delta_beta=0 | Bianchi/conservation identity must fix the nonlinear potential terms consistently | local conservation closes source normalization and beta completion | MISSING_BIANCHI_SOURCE_IDENTITY | derive the parent identity linking field equations to matter conservation |
| ZERO2232_5_no_extra_modes | q_R=0 and delta_beta=0 | extra finite-range/scalar/tracefree modes must decouple or be suppressed locally | no surviving local hair in the PPN residual vector | MISSING_MODE_DECOUPLING_THEOREM | derive decoupling/suppression or keep local branch as bounded closure |

## Claim Gate
| gate_id | claim_gate | status | reason |
| --- | --- | --- | --- |
| GATE2232_0_control_runner | two-parameter PPN control runner | PASS_NONCLAIM_CONTROL | control-plane arithmetic works and can reject trial leak vectors |
| GATE2232_1_parent_prediction | MTS predicts q_R and delta_beta | BLOCKED_NO_CLAIM | no parent equations produce q_R/delta_beta values |
| GATE2232_2_GR_origin | MTS derives local GR origin q_R=0, delta_beta=0 | BLOCKED_NO_CLAIM | zero-condition ledger remains unsigned |
| GATE2232_3_matter_universal | local bounds apply to all matter/photons | BLOCKED_NO_CLAIM | matter/coframe descent still missing |
| GATE2232_4_empirical_score | empirical MTS local-bound score | BLOCKED_NO_CLAIM | runner can score hypothetical vectors, not the theory |

## Decision Ledger
| decision_id | decision | result | reason |
| --- | --- | --- | --- |
| DEC2232_0_verdict | two-parameter local control status | CONTROL_RUNNER_READY_ZERO_THEOREM_MISSING | q_R/delta_beta local residuals are now test-shaped, but the parent theory has not derived the GR origin |
| DEC2232_1_next | next target | NEXT_2233_PARENT_WEAK_FIELD_ZERO_CONDITION_DERIVATION | the best next route is to attack the parent equations needed for q_R=0 and delta_beta=0 |

## Next Target
| next_id | next_target | script | objective | do_not |
| --- | --- | --- | --- | --- |
| NEXT2232_0_2233 | 2233-Y5-R2FR-parent-weak-field-zero-condition-derivation-or-demotion.md | scripts/Y5_R2FR_parent_weak_field_zero_condition_derivation_or_demotion_2233.py | attempt to derive the first-order q_R=0 condition and second-order delta_beta=0 condition from a parent weak-field field-equation/action structure; if this fails, demote the local GR branch to an explicit bounded-closure control lane | do not use the PPN control runner as a parent derivation; do not claim local GR/Newton reduction; do not edit formalization-workbench |

## Branch Copies
| copy_id | source_path | target_path | copied | parse_ok |
| --- | --- | --- | --- | --- |
| queue | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2232_PARENT_ZERO_CONDITION_HUNT.csv | source-intake/rab-sector/acquisition-queue/JR2232_QR_BETA_CONTROL_RUNNER_NONCLAIM.csv | True | True |
| branch_wep | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2232_PARENT_ZERO_CONDITION_HUNT.csv | source-intake/microscope/branch_locked_wep/residuals/qR_beta_control_runner_nonclaim_2232.csv | True | True |
| beta_docs | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2232_PARENT_ZERO_CONDITION_HUNT.csv | source-intake/beta-source/docs/QR_BETA_CONTROL_RUNNER_2232_NONCLAIM.csv | True | True |

## Validation
| check_id | result | detail |
| --- | --- | --- |
| VAL2232_00_sources_exist | PASS | all cited 2232 source paths exist |
| VAL2232_01_prior_validations | PASS | 2231 and 1559 validations pass overall |
| VAL2232_02_model_q_beta | PASS | q_R and delta_beta unit translation rows present |
| VAL2232_03_model_perihelion_combo | PASS | perihelion degeneracy model present |
| VAL2232_04_bound_box | PASS | q_R and delta_beta bound box written |
| VAL2232_05_GR_origin_passes | PASS | GR origin passes control box |
| VAL2232_06_q_fail_fails | PASS | oversized q_R fails Cassini/gamma bound |
| VAL2232_07_degeneracy_line | PASS | perihelion degeneracy example has zero Mercury residual |
| VAL2232_08_zero_conditions | PASS | parent zero-condition hunt ledger written |
| VAL2232_09_claim_gates | PASS | local GR derivation remains blocked |
| VAL2232_10_decision_next | PASS | decision selects parent weak-field zero-condition derivation next |
| VAL2232_11_next_target | PASS | next target is parent weak-field zero-condition derivation or demotion |
| VAL2232_12_csv_parse | PASS | all generated 2232 CSVs parse cleanly |
| VAL2232_13_claim_flags_false | PASS | all generated flags remain nonclaim |
| VAL2232_14_branch_copies | PASS | branch copies written and parse |
| VAL2232_15_pycache_absent | PASS | scripts __pycache__ absent after run |
| VAL2232_16_formalization_no_2232 | PASS | formalization-workbench has no non-venv 2232 artifacts |
| VAL2232_17_formalization_untouched | PASS | formalization-workbench untouched during 2232 run |
| VAL2232_OVERALL | PASS | 2232 imports q_R/delta_beta two-parameter PPN control runner and zero-condition hunt while keeping local predictions blocked |

## Working Interpretation

This gives the local branch a useful control dashboard, not a trophy. If a future parent derivation predicts `q_R` and `delta_beta`, this runner tells us immediately whether the values survive gamma, beta, light/Shapiro, and perihelion constraints. Until then, the important work is not fitting the control plane; it is deriving why the parent theory lands at or near the GR origin.

