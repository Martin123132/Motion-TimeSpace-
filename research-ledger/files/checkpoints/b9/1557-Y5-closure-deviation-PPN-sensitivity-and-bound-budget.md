# 1557 - Closure-Deviation PPN Sensitivity and Bound Budget

## Verdict
- The local closure branch now has a concrete deviation budget, not a claim.
- The first dangerous leakage channels are `q_R`, `epsilon_matter`, `alpha_clock`, source-normalization drift, preferred-frame/boundary leakage, finite-range R10 hair, and tracefree transfer.
- Real local bound rows are linked: MICROSCOPE/WEP, Galileo redshift, Cassini gamma, beta/PPN preferred-frame bounds, LLR Gdot, and symbolic R10 inverse-square limits.
- No MTS local prediction is scored here because the parent response coefficients are still missing.
- The next target is to derive or source those response coefficients before any local-bound scoring.

## Source Register
| source_id | source_path | exists | needle_found | needles |
| --- | --- | --- | --- | --- |
| SRC1557_0_1556_doc | 1556-Y5-local-closure-PPN-benchmark-and-derived-vs-assumed-ledger.md | True | True | R_AB=0; not parent-derived; closure-deviation |
| SRC1557_1_1556_validation | source-intake/mts_residuals/P8_Y5_BRR545_1556_VALIDATION.csv | True | True |  |
| SRC1557_2_1556_next | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1556_NEXT_TARGET.csv | True | True | 1557-Y5-closure-deviation-PPN-sensitivity-and-bound-budget.md |
| SRC1557_3_1556_ppn | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1556_PPN_BENCHMARK_REQUIREMENTS.csv | True | True | gamma_minus_1; beta_minus_1; alpha(lambda) |
| SRC1557_4_1556_derived | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1556_DERIVED_VS_ASSUMED_LEDGER.csv | True | True | DVA1556_8_parent_origin; BLOCKED_NOT_DERIVED |
| SRC1557_5_14_doc | 14-closure-deviation-PPN-sensitivity.md | True | True | q_R:; Mercury shift factor = (2 q_R - delta_beta)/3.; not an empirical claim yet |
| SRC1557_6_13_doc | 13-local-closure-PPN-benchmark.md | True | True |  |
| SRC1557_7_10_doc | 10-observer-map-symplectic-contract.md | True | True |  |
| SRC1557_8_local_bound_claims | source-intake/local_bounds/local_bound_claims.csv | True | True |  |

## Deviation Channels
| channel_id | leak_parameter | first_observables | leading_control_map | missing_parent_inputs | local_bound_rows | status |
| --- | --- | --- | --- | --- | --- | --- |
| DEV1557_0_qR_gamma | q_R | gamma_minus_1; light_bending; Shapiro; perihelion | gamma_minus_1 ~= C_gamma_qR q_R, with internal control C_gamma_qR=1 not parent-signed | C_gamma_qR; parent R_AB leakage map; source normalization | R3_gamma | BOUND_BUDGET_ONLY_NOT_PREDICTION |
| DEV1557_1_delta_beta | delta_beta | beta_minus_1; perihelion | beta_minus_1 ~= C_beta_delta delta_beta; Mercury control factor=(2 q_R-delta_beta)/3 | C_beta_delta; second-order weak-field completion | R4_beta | BOUND_BUDGET_ONLY_NOT_PREDICTION |
| DEV1557_2_epsilon_matter | epsilon_matter | eta_WEP_direct_geometry; eta_WEP_source_charge | eta ~= C_eta_epsilon epsilon_matter | C_eta_epsilon; matter action descent; no shadow-frame coupling | R0_identity_coframe_direct; R1_WEP_source_charge | BOUND_BUDGET_ONLY_NOT_PREDICTION |
| DEV1557_3_alpha_clock | alpha_clock | alpha_clock_redshift | redshift anomaly ~= C_clock alpha_clock | C_clock; universal clock/load readout map | R2_clock_redshift | BOUND_BUDGET_ONLY_NOT_PREDICTION |
| DEV1557_4_Gdot_source_norm | sigma_Gdot | Gdot_over_G | Gdot/G ~= C_Gdot sigma_Gdot | C_Gdot; measured-GM/source normalization theorem | R9_Gdot | BOUND_BUDGET_ONLY_NOT_PREDICTION |
| DEV1557_5_preferred_frame_alpha1 | epsilon_frame_1 | alpha1 | alpha1 ~= C_alpha1 epsilon_frame_1 | C_alpha1; frame/coframe descent; boundary silence | R5_alpha1 | BOUND_BUDGET_ONLY_NOT_PREDICTION |
| DEV1557_6_preferred_frame_alpha2 | epsilon_frame_2 | alpha2 | alpha2 ~= C_alpha2 epsilon_frame_2 | C_alpha2; spin/coframe descent; anisotropy map | R6_alpha2 | BOUND_BUDGET_ONLY_NOT_PREDICTION |
| DEV1557_7_flux_alpha3_xi | epsilon_flux | alpha3; xi | alpha3 ~= C_alpha3 epsilon_flux; xi ~= C_xi epsilon_flux | C_alpha3; C_xi; boundary/no-charge/source-flux theorem | R7_alpha3; R8_xi | BOUND_BUDGET_ONLY_NOT_PREDICTION |
| DEV1557_8_R10_finite_range | alpha_R10(lambda) | delta_G_or_fifth_force_yukawa | Yukawa alpha(lambda) ~= C_R10(lambda) residual_hair(lambda) | C_R10(lambda); real digitized alpha(lambda) curve; parent range map | R10_fifth_force | BOUND_BUDGET_ONLY_NOT_PREDICTION |
| DEV1557_9_tracefree_transfer | h_TF_residual | PPN tensor/vector residuals | PPN residual vector ~= M_TF h_TF_residual | M_TF response matrix; tensor/coframe transfer theorem | R5_alpha1; R6_alpha2; R8_xi | BOUND_BUDGET_ONLY_NOT_PREDICTION |

## Local Bound Links
| row_id | used_for_channel | observable | upper_bound | units | numeric_bound_parse | reference_path_or_url |
| --- | --- | --- | --- | --- | --- | --- |
| R0_identity_coframe_direct | DEV1557_2_epsilon_matter | eta_WEP_direct_geometry | 2.8e-15 | dimensionless | PASS | https://arxiv.org/abs/2209.15487; doi:10.1103/PhysRevLett.129.121102 |
| R1_WEP_source_charge | DEV1557_2_epsilon_matter | eta_WEP_source_charge | 2.8e-15 | dimensionless | PASS | https://arxiv.org/abs/2209.15487; doi:10.1103/PhysRevLett.129.121102 |
| R2_clock_redshift | DEV1557_3_alpha_clock | alpha_clock_redshift | 2.48e-05 | dimensionless | PASS | https://arxiv.org/abs/1812.03711; doi:10.1103/PhysRevLett.121.231101 |
| R3_gamma | DEV1557_0_qR_gamma | gamma_minus_1 | 2.3e-05 | dimensionless | PASS | https://www.nature.com/articles/nature01997; doi:10.1038/nature01997 |
| R4_beta | DEV1557_1_delta_beta | beta_minus_1 | 7.8e-05 | dimensionless | PASS | https://www2.math.ethz.ch/EMIS/journals/LRG/Articles/lrr-2014-4/articlese4.html |
| R5_alpha1 | DEV1557_5_preferred_frame_alpha1; DEV1557_9_tracefree_transfer | alpha1 | 1e-04 | dimensionless | PASS | https://www2.math.ethz.ch/EMIS/journals/LRG/Articles/lrr-2014-4/articlese4.html |
| R6_alpha2 | DEV1557_6_preferred_frame_alpha2; DEV1557_9_tracefree_transfer | alpha2 | 2e-09 | dimensionless | PASS | https://www2.math.ethz.ch/EMIS/journals/LRG/Articles/lrr-2014-4/articlese4.html |
| R7_alpha3 | DEV1557_7_flux_alpha3_xi | alpha3 | 4e-20 | dimensionless | PASS | https://www2.math.ethz.ch/EMIS/journals/LRG/Articles/lrr-2014-4/articlese4.html |
| R8_xi | DEV1557_7_flux_alpha3_xi; DEV1557_9_tracefree_transfer | xi | 4e-09 | dimensionless | PASS | https://www2.math.ethz.ch/EMIS/journals/LRG/Articles/lrr-2014-4/articlese4.html |
| R9_Gdot | DEV1557_4_Gdot_source_norm | Gdot_over_G | 9.6e-15 | yr^-1 | PASS | https://www.ife.uni-hannover.de/de/forschung/publikationen/detail-ansicht?tx_univiepure_univiepure%5Buuid%5D=cbe8f824-b21b-4e80-b736-944c3f960f7a; doi:10.3390/universe7020034 |
| R10_fifth_force | DEV1557_8_R10_finite_range | delta_G_or_fifth_force_yukawa | alpha(lambda) | range-dependent | SYMBOLIC_CURVE_REQUIRED | https://arxiv.org/abs/hep-ph/0307284; doi:10.1146/annurev.nucl.53.041002.110503 |

## Sensitivity Map
| sensitivity_id | leak_parameter | observable_channel | control_coefficient | coefficient_units | required_parent_coefficient | claim_status |
| --- | --- | --- | --- | --- | --- | --- |
| SENS1557_0_qR_light_bending | q_R | solar light bending | 0.8756216406841224 | arcsec per unit q_R | C_gamma_qR | NONCLAIM_INTERNAL_CONVERSION_ONLY |
| SENS1557_1_qR_shapiro | q_R | solar Shapiro delay scale | 59.7375179242781 | microseconds per unit q_R | C_gamma_qR | NONCLAIM_INTERNAL_CONVERSION_ONLY |
| SENS1557_2_qR_mercury | q_R | Mercury perihelion | 28.65467507274745 | arcsec/century per unit q_R | C_gamma_qR; C_peri_qR | NONCLAIM_INTERNAL_CONVERSION_ONLY |
| SENS1557_3_delta_beta_mercury | delta_beta | Mercury perihelion | -14.327337536373726 | arcsec/century per unit delta_beta | C_beta_delta; C_peri_beta | NONCLAIM_INTERNAL_CONVERSION_ONLY |
| SENS1557_4_alpha_clock_gps | alpha_clock | GPS gravitational redshift | 45.718449825926655 | microseconds/day per unit alpha_clock | C_clock | NONCLAIM_INTERNAL_CONVERSION_ONLY |
| SENS1557_5_epsilon_matter_eotvos | epsilon_matter | Eotvos proxy | 1 | dimensionless proxy per unit coupling spread | C_eta_epsilon | NONCLAIM_INTERNAL_CONVERSION_ONLY |
| SENS1557_6_source_norm_Gdot | sigma_Gdot | Gdot/G | MISSING_PARENT_INPUT | yr^-1 per unit source-normalization drift | C_Gdot | NONCLAIM_INTERNAL_CONVERSION_ONLY |
| SENS1557_7_R10_curve | alpha_R10(lambda) | inverse-square/Yukawa curve | MISSING_CURVE_AND_PARENT_INPUT | alpha(lambda) per residual hair amplitude | C_R10(lambda) | NONCLAIM_INTERNAL_CONVERSION_ONLY |
| SENS1557_8_tracefree_ppn_vector | h_TF_residual | PPN vector/tensor residual | MISSING_RESPONSE_MATRIX | PPN residual per tracefree transfer amplitude | M_TF | NONCLAIM_INTERNAL_CONVERSION_ONLY |

## Bound Budget
| budget_id | leak_parameter | local_bound_rows | control_bound_if_unit_response | bound_units | blocking_input | budget_status |
| --- | --- | --- | --- | --- | --- | --- |
| BUD1557_0_qR | q_R | R3_gamma | 2.3e-05 | dimensionless | MISSING_C_gamma_qR | CONTROL_BOUND_ONLY_NOT_MTS_PREDICTION |
| BUD1557_1_delta_beta | delta_beta | R4_beta | 7.8e-05 | dimensionless | MISSING_C_beta_delta | CONTROL_BOUND_ONLY_NOT_MTS_PREDICTION |
| BUD1557_2_epsilon_matter_direct | epsilon_matter | R0_identity_coframe_direct; R1_WEP_source_charge | 2.8e-15 | dimensionless | MISSING_C_eta_epsilon_AND_MATTER_DESCENT | CONTROL_BOUND_ONLY_NOT_MTS_PREDICTION |
| BUD1557_3_alpha_clock | alpha_clock | R2_clock_redshift | 2.48e-05 | dimensionless | MISSING_C_clock | CONTROL_BOUND_ONLY_NOT_MTS_PREDICTION |
| BUD1557_4_sigma_Gdot | sigma_Gdot | R9_Gdot | 9.6e-15 | yr^-1 | MISSING_C_Gdot_AND_SOURCE_NORMALIZATION | CONTROL_BOUND_ONLY_NOT_MTS_PREDICTION |
| BUD1557_5_alpha1_frame | epsilon_frame_1 | R5_alpha1 | 1e-04 | dimensionless | MISSING_C_alpha1_AND_FRAME_DESCENT | CONTROL_BOUND_ONLY_NOT_MTS_PREDICTION |
| BUD1557_6_alpha2_frame | epsilon_frame_2 | R6_alpha2 | 2e-09 | dimensionless | MISSING_C_alpha2_AND_SPIN_RESPONSE | CONTROL_BOUND_ONLY_NOT_MTS_PREDICTION |
| BUD1557_7_alpha3_flux | epsilon_flux | R7_alpha3 | 4e-20 | dimensionless | MISSING_C_alpha3_AND_BOUNDARY_SILENCE | CONTROL_BOUND_ONLY_NOT_MTS_PREDICTION |
| BUD1557_8_xi_flux | epsilon_flux | R8_xi | 4e-09 | dimensionless | MISSING_C_xi_AND_BOUNDARY_SILENCE | CONTROL_BOUND_ONLY_NOT_MTS_PREDICTION |
| BUD1557_9_R10_curve | alpha_R10(lambda) | R10_fifth_force | alpha(lambda) | range-dependent | MISSING_C_R10_lambda_AND_DIGITIZED_CURVE | CONTROL_BOUND_ONLY_NOT_MTS_PREDICTION |
| BUD1557_10_tracefree_transfer | h_TF_residual | R5_alpha1; R6_alpha2; R8_xi | response-matrix-required | PPN residual vector | MISSING_M_TF_RESPONSE_MATRIX | CONTROL_BOUND_ONLY_NOT_MTS_PREDICTION |

## Runner
| runner_id | test | current_status | detail |
| --- | --- | --- | --- |
| RUN1557_0_sources | 1556 handoff and local-bound source files exist | PASS | source register validates local evidence for the deviation-budget checkpoint |
| RUN1557_1_channels | all closure leakage channels are named | PASS_NONCLAIM | q_R, delta_beta, epsilon_matter, alpha_clock, source normalization, preferred-frame, R10, and tracefree channels are included |
| RUN1557_2_bounds | local bounds link to real source rows | PASS_BOUND_LEDGER | numeric local bounds are parsed for R0-R9; R10 remains symbolic curve-only |
| RUN1557_3_prediction_refusal | do not convert budgets into MTS predictions | REFUSED_MISSING_PARENT_COEFFICIENTS | unit-response control budgets are not predictions until C_gamma_qR, C_beta_delta, C_eta_epsilon, C_clock, C_Gdot, frame coefficients, C_R10(lambda), and M_TF are sourced |
| RUN1557_4_claim_status | local GR/Newton/local-bound claim | BLOCKED_NO_CLAIM | closure deviations are now bounded as a bookkeeping problem, not claimed as empirical success |

## Claim Gates
| gate_id | claim_gate | status | reason |
| --- | --- | --- | --- |
| GATE1557_0_parent_closure_origin | derive R_AB=0 and Q_R=0 from parent action | BLOCKED_NO_CLAIM | 1556 retained closure-only status |
| GATE1557_1_qR_coefficient | source C_gamma_qR and perihelion response | BLOCKED_NO_CLAIM | unit gamma map is control bookkeeping only |
| GATE1557_2_beta_completion | derive beta drift response from second-order field equations | BLOCKED_NO_CLAIM | no parent second-order weak-field completion |
| GATE1557_3_matter_universality | derive universal matter/coframe coupling | BLOCKED_NO_CLAIM | WEP row is a severe budget, not a pass |
| GATE1557_4_clock_readout | derive clock/load redshift response | BLOCKED_NO_CLAIM | clock coefficient still a response-map placeholder |
| GATE1557_5_source_normalization | derive measured GM/Gdot source normalization | BLOCKED_NO_CLAIM | Gdot budget cannot score without source theorem |
| GATE1557_6_frame_boundary | derive preferred-frame and boundary silence | BLOCKED_NO_CLAIM | alpha1/alpha2/alpha3/xi rows are bound ledgers |
| GATE1557_7_R10_curve | provide real digitized alpha(lambda) curve and parent range map | BLOCKED_NO_CLAIM | symbolic R10 row cannot score finite-range hair |
| GATE1557_8_tracefree_matrix | derive tensor/coframe response matrix M_TF | BLOCKED_NO_CLAIM | scalar closure does not control all PPN residuals |

## Decision
| decision_id | decision | result | reason |
| --- | --- | --- | --- |
| DEC1557_0_verdict | local closure deviation budget exists but is nonclaim | BOUND_BUDGET_WRITTEN_PARENT_COEFFICIENTS_MISSING | local bounds can now discipline each leakage channel, but no channel has a sourced parent response coefficient |
| DEC1557_1_next | next target | NEXT_1558_COEFFICIENT_SOURCE_MAP | derive or source the first response coefficients before any local-bound scoring |

## Validation
| check_id | result | detail |
| --- | --- | --- |
| VAL1557_0_sources_exist | PASS | all cited 1557 source paths exist |
| VAL1557_1_needles_found | PASS | all registered evidence needles found |
| VAL1557_2_channels_complete | PASS | all required local leakage channels are present |
| VAL1557_3_bound_rows_linked | PASS | local bound rows are linked to channels |
| VAL1557_4_numeric_bounds_parse | PASS | numeric R0-R9 local bounds parse cleanly |
| VAL1557_5_R10_symbolic | PASS | R10 remains symbolic curve-only |
| VAL1557_6_sensitivities_present | PASS | sensitivity map includes q_R and other channels |
| VAL1557_7_budgets_blocked | PASS | all bound budgets are control-only nonpredictions |
| VAL1557_8_runner_refuses_prediction | PASS | runner refuses MTS prediction scoring |
| VAL1557_9_claim_gates_block | PASS | all local claim gates remain blocked |
| VAL1557_10_decision_next | PASS | decision selects response-coefficient source map next |
| VAL1557_11_next_target | PASS | next target is response-coefficient mapping |
| VAL1557_12_csv_parse | PASS | all generated 1557 CSVs parse cleanly |
| VAL1557_13_claim_flags_false | PASS | all generated prediction/claim flags remain false |
| VAL1557_14_branch_copies | PASS | branch/quarantine nonclaim copies written |
| VAL1557_15_pycache_absent | PASS | scripts __pycache__ absent after run |
| VAL1557_16_formalization_untouched | PASS | formalization modified-file count since start=0 |
| VAL1557_OVERALL | PASS | 1557 closure-deviation PPN sensitivity and bound-budget checkpoint validation |

## Next Target
| next_target | script | objective | do_not |
| --- | --- | --- | --- |
| 1558-Y5-qR-beta-matter-clock-coefficient-source-map-or-rejection.md | scripts/Y5_qR_beta_matter_clock_coefficient_source_map_or_rejection.py | derive or source the response coefficients mapping q_R, delta_beta, epsilon_matter, alpha_clock, source normalization, frame leakage, R10 range hair, and tracefree transfer into local observables | do not treat unit-response control budgets as MTS predictions; do not claim local GR derivation; do not edit formalization-workbench |
