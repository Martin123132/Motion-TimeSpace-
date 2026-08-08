# 1558 - q_R/Beta/Matter/Clock Coefficient Source Map or Rejection

## Verdict
- `q_R` now has a derived PPN translation: at first weak-field order, `R_AB ~= (gamma-1)L` and `R_AB ~= q_R L`, so `gamma-1=q_R`.
- The light-bending, Shapiro, and Mercury `q_R` coefficients follow directly from standard PPN scaling; `delta_beta` enters Mercury through `(2 q_R - delta_beta)/3`.
- This is progress: the local residual scorecard is mathematically sharper than it was at 1557.
- This is not yet a local-GR derivation, because the parent theory still has to prove or predict `q_R=0` and `delta_beta=0`.
- Clock and WEP coefficients remain phenomenological proxy definitions; Gdot, preferred-frame, R10, and tracefree response coefficients are rejected for scoring at 1558.

## Source Register
| source_id | source_path | exists | needle_found | needles |
| --- | --- | --- | --- | --- |
| SRC1558_0_1557_doc | 1557-Y5-closure-deviation-PPN-sensitivity-and-bound-budget.md | True | True | No MTS local prediction is scored here; response coefficients are still missing |
| SRC1558_1_1557_validation | source-intake/mts_residuals/P8_Y5_BRR545_1557_VALIDATION.csv | True | True | VAL1557_OVERALL; PASS |
| SRC1558_2_1557_budget | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1557_BOUND_BUDGET_NONCLAIM.csv | True | True | BUD1557_0_qR; MISSING_C_gamma_qR |
| SRC1558_3_1557_sensitivity | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1557_SENSITIVITY_MAP_NONCLAIM.csv | True | True | SENS1557_0_qR_light_bending; SENS1557_3_delta_beta_mercury |
| SRC1558_4_14_doc | 14-closure-deviation-PPN-sensitivity.md | True | True | Mercury shift factor = (2 q_R - delta_beta)/3.; solar light bending vs q_R |
| SRC1558_5_13_doc | 13-local-closure-PPN-benchmark.md | True | True | R_AB approx q_R L; gamma approx 1 + q_R. |
| SRC1558_6_10_doc | 10-observer-map-symplectic-contract.md | True | True | PPN gamma:; PPN beta: |
| SRC1558_7_local_bound_claims | source-intake/local_bounds/local_bound_claims.csv | True | True |  |

## PPN Coefficient Derivation
| coefficient_id | leak_parameter | observable_response | coefficient_value | coefficient_units | coefficient_status |
| --- | --- | --- | --- | --- | --- |
| PPNC1558_0_qR_gamma | q_R | gamma_minus_1 | 1 | dimensionless per unit q_R | DERIVED_PPN_DICTIONARY_NOT_PARENT_PREDICTION |
| PPNC1558_1_qR_light_bending | q_R | solar_light_bending_residual | 0.8756216406841224 | arcsec per unit q_R | DERIVED_FROM_STANDARD_PPN_SCALING_NOT_PARENT_PREDICTION |
| PPNC1558_2_qR_shapiro | q_R | solar_Shapiro_residual | 59.7375179242781 | microseconds per unit q_R | DERIVED_FROM_STANDARD_PPN_SCALING_NOT_PARENT_PREDICTION |
| PPNC1558_3_qR_mercury | q_R | Mercury_perihelion_residual | 28.65467507274745 | arcsec/century per unit q_R | DERIVED_FROM_STANDARD_PPN_SCALING_NOT_PARENT_PREDICTION |
| PPNC1558_4_delta_beta_definition | delta_beta | beta_minus_1 | 1 | dimensionless per unit delta_beta | PPN_PARAMETER_DEFINITION_NOT_PARENT_COMPLETION |
| PPNC1558_5_delta_beta_mercury | delta_beta | Mercury_perihelion_residual | -14.32733753637373 | arcsec/century per unit delta_beta | DERIVED_FROM_STANDARD_PPN_SCALING_NOT_PARENT_PREDICTION |
| PPNC1558_6_perihelion_degeneracy | q_R; delta_beta | Mercury_perihelion_residual | (2 q_R - delta_beta)/3 times GR perihelion | dimensionless factor | DERIVED_PPN_DEGENERACY_STRUCTURE_NOT_PARENT_PREDICTION |

## Phenomenological Coefficient Map
| phenomenology_id | leak_parameter | observable_response | coefficient_value | coefficient_status | limitation |
| --- | --- | --- | --- | --- | --- |
| PHEN1558_0_alpha_clock_redshift | alpha_clock | alpha_clock_redshift | 1 | PHENOMENOLOGICAL_PARAMETER_DEFINITION_ONLY | alpha_clock can be used as the observed redshift-deviation parameter, but the MTS clock/load map is not parent-derived |
| PHEN1558_1_epsilon_matter_eta | epsilon_matter | eta_WEP_proxy | 1 | PHENOMENOLOGICAL_PROXY_ONLY | epsilon_matter measures matter-coupling spread, but universal matter-action descent is not derived |
| PHEN1558_2_sigma_Gdot | sigma_Gdot | Gdot_over_G | MISSING | REJECTED_FOR_NOW_MISSING_PARENT_SOURCE_NORMALIZATION | requires measured-GM/source-normalization theorem before Gdot bound can be applied to MTS |

## Rejection Ledger
| rejection_id | leak_parameter | observable_response | missing_input | reason | reentry_condition |
| --- | --- | --- | --- | --- | --- |
| REJ1558_0_source_normalization | sigma_Gdot | Gdot_over_G | MISSING_C_Gdot | no parent measured-GM/source-normalization theorem; cannot decide whether source drift maps to measured Gdot | derive source-normalization theorem or leave as external bound only |
| REJ1558_1_preferred_frame_alpha1 | epsilon_frame_1 | alpha1 | MISSING_C_alpha1 | no frame/coframe descent coefficient from parent observer split | derive frame-descent response or keep alpha1 as no-claim diagnostic |
| REJ1558_2_preferred_frame_alpha2 | epsilon_frame_2 | alpha2 | MISSING_C_alpha2 | spin/anisotropic coframe leakage lacks a response map | derive spin/coframe response or keep alpha2 as no-claim diagnostic |
| REJ1558_3_flux_alpha3_xi | epsilon_flux | alpha3; xi | MISSING_C_alpha3_AND_C_xi | boundary silence and momentum/source-flux conservation are not parent-derived | derive boundary/no-charge theorem before using ultra-tight alpha3/xi bounds |
| REJ1558_4_R10_range_curve | alpha_R10(lambda) | Yukawa alpha(lambda) | MISSING_C_R10_lambda_AND_DIGITIZED_CURVE | R10 bound remains symbolic curve-only and parent range map is absent | acquire real alpha(lambda) curve and derive lambda/residual-hair map |
| REJ1558_5_tracefree_transfer | h_TF_residual | PPN residual vector | MISSING_M_TF_RESPONSE_MATRIX | scalar R_AB closure does not define tensor/vector transfer | derive tensor/coframe response matrix before vector/tensor PPN scoring |

## Readiness Matrix
| readiness_id | leak_parameter | observable_response | translation_ready | parent_prediction_ready | score_ready | status | reason |
| --- | --- | --- | --- | --- | --- | --- | --- |
| READY1558_0_qR_gamma | q_R | gamma_minus_1/light/Shapiro/perihelion | True | False | False | TRANSLATION_ONLY | PPN translation is derived; parent still must predict q_R |
| READY1558_1_delta_beta | delta_beta | beta_minus_1/perihelion | True | False | False | TRANSLATION_ONLY | PPN translation is derived; parent still must supply beta completion |
| READY1558_2_alpha_clock | alpha_clock | redshift/clocks | True | False | False | TRANSLATION_ONLY | phenomenological clock parameter usable; parent clock/load response missing |
| READY1558_3_epsilon_matter | epsilon_matter | WEP/Eotvos | True | False | False | TRANSLATION_ONLY | proxy parameter usable; parent matter descent missing |
| READY1558_4_sigma_Gdot | sigma_Gdot | Gdot/G | False | False | False | REJECTED_PENDING_INPUTS | source-normalization coefficient missing |
| READY1558_5_frame | epsilon_frame_1; epsilon_frame_2 | alpha1/alpha2 | False | False | False | REJECTED_PENDING_INPUTS | frame/coframe descent coefficients missing |
| READY1558_6_flux | epsilon_flux | alpha3/xi | False | False | False | REJECTED_PENDING_INPUTS | boundary/source-flux coefficients missing |
| READY1558_7_R10 | alpha_R10(lambda) | Yukawa alpha(lambda) | False | False | False | REJECTED_PENDING_INPUTS | digitized curve and parent range map missing |
| READY1558_8_tracefree | h_TF_residual | PPN residual vector | False | False | False | REJECTED_PENDING_INPUTS | tensor response matrix missing |

## Runner
| runner_id | test | current_status | detail |
| --- | --- | --- | --- |
| RUN1558_0_sources | 1557 handoff and coefficient sources exist | PASS | all coefficient source files exist and evidence needles are present |
| RUN1558_1_qR_beta_ppn | derive q_R and delta_beta PPN translation coefficients | PASS_TRANSLATION_ONLY | q_R maps to gamma-1; light/Shapiro/perihelion and beta perihelion coefficients are derived from standard PPN scaling |
| RUN1558_2_clock_matter | classify clock and matter coefficients | PASS_PHENOMENOLOGICAL_ONLY | clock and WEP parameters can be used as proxy observables but not as parent-derived MTS predictions |
| RUN1558_3_rejections | reject unsupported coefficients | PASS_REJECTION_LEDGER | Gdot, preferred-frame, flux, R10, and tracefree coefficients remain blocked |
| RUN1558_4_scoring | local-bound scoring | REFUSED_NO_PARENT_PREDICTIONS | translation coefficients do not produce a claim until the parent action predicts q_R, delta_beta, clock/matter drift, or their zeros |

## Claim Gates
| gate_id | claim_gate | status | reason |
| --- | --- | --- | --- |
| GATE1558_0_qR_translation | q_R PPN translation | OPEN_TRANSLATION_ONLY | coefficient map exists, but parent q_R prediction is missing |
| GATE1558_1_beta_translation | delta_beta PPN translation | OPEN_TRANSLATION_ONLY | coefficient map exists, but parent beta completion is missing |
| GATE1558_2_clock | clock coefficient | BLOCKED_NO_CLAIM | phenomenological redshift parameter only |
| GATE1558_3_matter | matter/WEP coefficient | BLOCKED_NO_CLAIM | phenomenological WEP proxy only |
| GATE1558_4_Gdot | source normalization | BLOCKED_NO_CLAIM | source-normalization theorem missing |
| GATE1558_5_frame_flux_tracefree_R10 | remaining local residual vector | BLOCKED_NO_CLAIM | response matrix/range/boundary coefficients missing |
| GATE1558_6_local_GR | derived local GR/Newton reduction | BLOCKED_NO_CLAIM | translation map is not a parent derivation of R_AB=0, Q_R=0, or beta=1 |

## Decision
| decision_id | decision | result | reason |
| --- | --- | --- | --- |
| DEC1558_0_verdict | coefficient source-map status | Q_R_AND_DELTA_BETA_TRANSLATION_DERIVED_PARENT_PREDICTIONS_MISSING | the q_R/beta PPN observable map is now mathematically sharp, but MTS still needs parent equations that set or predict the leak parameters |
| DEC1558_1_next | next target | NEXT_1559_TWO_PARAMETER_PPN_CONTROL_RUNNER_AND_ZERO_CONDITION_HUNT | use the derived q_R/delta_beta map to build a two-parameter local control runner while separately hunting the parent zero conditions |

## Validation
| check_id | result | detail |
| --- | --- | --- |
| VAL1558_0_sources_exist | PASS | all cited 1558 source paths exist |
| VAL1558_1_needles_found | PASS | all registered evidence needles found |
| VAL1558_2_qR_gamma | PASS | q_R to gamma-minus-one coefficient derived |
| VAL1558_3_light_coefficient | PASS | light-bending q_R coefficient equals GR/2 |
| VAL1558_4_shapiro_coefficient | PASS | Shapiro q_R coefficient equals GR/2 |
| VAL1558_5_perihelion_coefficients | PASS | perihelion coefficients match (2 q_R - delta_beta)/3 |
| VAL1558_6_clock_matter_nonparent | PASS | clock/matter rows remain non-parent predictions |
| VAL1558_7_rejection_ledger | PASS | unsupported coefficients rejected for scoring |
| VAL1558_8_readiness_translation_only | PASS | q_R row is translation-ready but not score-ready |
| VAL1558_9_runner_refuses_scoring | PASS | runner refuses local-bound scoring |
| VAL1558_10_claim_gate_blocks_GR | PASS | derived local GR claim remains blocked |
| VAL1558_11_decision_next | PASS | decision selects two-parameter runner plus zero-condition hunt |
| VAL1558_12_next_target | PASS | next target is q_R/delta_beta two-parameter PPN control runner |
| VAL1558_13_csv_parse | PASS | all generated 1558 CSVs parse cleanly |
| VAL1558_14_claim_flags_false | PASS | all generated prediction/claim flags remain false |
| VAL1558_15_branch_copies | PASS | branch/quarantine nonclaim copies written |
| VAL1558_16_pycache_absent | PASS | scripts __pycache__ absent after run |
| VAL1558_17_formalization_untouched | PASS | formalization modified-file count since start=0 |
| VAL1558_OVERALL | PASS | 1558 q_R/beta/matter/clock coefficient source-map or rejection validation |

## Next Target
| next_target | script | objective | do_not |
| --- | --- | --- | --- |
| 1559-Y5-qR-delta-beta-two-parameter-PPN-control-runner-and-zero-condition-hunt.md | scripts/Y5_qR_delta_beta_two_parameter_PPN_control_runner_and_zero_condition_hunt.py | use the derived q_R and delta_beta PPN translation coefficients to build a nonclaim two-parameter local control runner, then identify the exact parent zero conditions needed to promote q_R=0 and delta_beta=0 from closure to derivation | do not score MTS predictions without parent-predicted leak parameters; do not claim local GR derivation; do not edit formalization-workbench |
