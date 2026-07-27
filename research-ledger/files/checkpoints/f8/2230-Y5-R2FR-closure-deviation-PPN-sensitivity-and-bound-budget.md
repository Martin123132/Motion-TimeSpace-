# 2230 - Y5/R2FR Closure-Deviation PPN Sensitivity And Bound Budget

## Verdict
- 2230 imports the old `1557` closure-deviation/bound-budget frontier into the current R2FR line.
- The local leakage channels are now explicit: `q_R`, `delta_beta`, matter/coframe spread, clock anomaly, source-normalization drift, preferred-frame leakage, finite-range R10 hair, and tracefree transfer.
- Local bounds are linked for R0-R9 with numeric control rows; R10 correctly remains symbolic until a real `alpha(lambda)` curve and parent range map exist.
- Every budget is still nonclaim: unit-response control bounds are not MTS predictions until parent response coefficients are derived or sourced.
- Next target is the response-coefficient source map: derive or reject the coefficients that turn closure deviations into actual local predictions.

## Source Register
| source_id | source_path | path_exists | validation_overall_pass | role |
| --- | --- | --- | --- | --- |
| SRC2230_0_2229_doc | 2229-Y5-R2FR-local-closure-PPN-benchmark-and-derived-vs-assumed-ledger.md | True |  | current closure benchmark handoff |
| SRC2230_1_2229_validation | source-intake/mts_residuals/P8_Y5_BRR545_2229_VALIDATION.csv | True | True | current closure benchmark handoff |
| SRC2230_2_2229_next | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2229_NEXT_TARGET.csv | True |  | current closure benchmark handoff |
| SRC2230_3_1557_doc | 1557-Y5-closure-deviation-PPN-sensitivity-and-bound-budget.md | True |  | older closure-deviation/bound-budget evidence |
| SRC2230_4_1557_validation | source-intake/mts_residuals/P8_Y5_BRR545_1557_VALIDATION.csv | True | True | older closure-deviation/bound-budget evidence |
| SRC2230_5_1557_channels | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1557_DEVIATION_CHANNELS.csv | True |  | older closure-deviation/bound-budget evidence |
| SRC2230_6_1557_sensitivity | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1557_SENSITIVITY_MAP_NONCLAIM.csv | True |  | older closure-deviation/bound-budget evidence |
| SRC2230_7_1557_bounds | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1557_LOCAL_BOUND_LINKS.csv | True |  | older closure-deviation/bound-budget evidence |
| SRC2230_8_1557_budget | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1557_BOUND_BUDGET_NONCLAIM.csv | True |  | older closure-deviation/bound-budget evidence |
| SRC2230_9_1557_runner | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1557_RUNNER_NONCLAIM.csv | True |  | older closure-deviation/bound-budget evidence |
| SRC2230_10_1557_claim | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1557_CLAIM_GATE.csv | True |  | older closure-deviation/bound-budget evidence |
| SRC2230_11_1557_decision | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1557_DECISION.csv | True |  | older closure-deviation/bound-budget evidence |
| SRC2230_12_1557_next | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1557_NEXT_TARGET.csv | True |  | older closure-deviation/bound-budget evidence |

## Deviation Channels
| channel_id | leak_parameter | meaning | null_lane_value | first_observables | missing_parent_inputs | status |
| --- | --- | --- | --- | --- | --- | --- |
| DEV2230_0_qR_gamma | q_R | reciprocal hair coefficient in R_AB approximately q_R L | 0 | gamma_minus_1; light_bending; Shapiro; perihelion | C_gamma_qR; parent R_AB leakage map; source normalization | BOUND_BUDGET_ONLY_NOT_PREDICTION |
| DEV2230_1_delta_beta | delta_beta | nonlinear completion drift away from beta=1 | 0 | beta_minus_1; perihelion | C_beta_delta; second-order weak-field completion | BOUND_BUDGET_ONLY_NOT_PREDICTION |
| DEV2230_2_epsilon_matter | epsilon_matter | spread away from universal matter/coframe coupling | 0 | eta_WEP_direct_geometry; eta_WEP_source_charge | C_eta_epsilon; matter action descent; no shadow-frame coupling | BOUND_BUDGET_ONLY_NOT_PREDICTION |
| DEV2230_3_alpha_clock | alpha_clock | clock/load redshift anomaly | 0 | alpha_clock_redshift | C_clock; universal clock/load readout map | BOUND_BUDGET_ONLY_NOT_PREDICTION |
| DEV2230_4_Gdot_source_norm | sigma_Gdot | time drift in measured source normalization GM or effective G | 0 yr^-1 | Gdot_over_G | C_Gdot; measured-GM/source normalization theorem | BOUND_BUDGET_ONLY_NOT_PREDICTION |
| DEV2230_5_preferred_frame_alpha1 | epsilon_frame_1 | vector/coframe preferred-frame leakage | 0 | alpha1 | C_alpha1; frame/coframe descent; boundary silence | BOUND_BUDGET_ONLY_NOT_PREDICTION |
| DEV2230_6_preferred_frame_alpha2 | epsilon_frame_2 | spin or anisotropic coframe preferred-frame leakage | 0 | alpha2 | C_alpha2; spin/coframe descent; anisotropy map | BOUND_BUDGET_ONLY_NOT_PREDICTION |
| DEV2230_7_flux_alpha3_xi | epsilon_flux | source flux, momentum nonconservation, or preferred-location leakage | 0 | alpha3; xi | C_alpha3; C_xi; boundary/no-charge/source-flux theorem | BOUND_BUDGET_ONLY_NOT_PREDICTION |
| DEV2230_8_R10_finite_range | alpha_R10(lambda) | finite-range q/source hair outside the exact closure | 0 for all lambda | delta_G_or_fifth_force_yukawa | C_R10(lambda); real digitized alpha(lambda) curve; parent range map | BOUND_BUDGET_ONLY_NOT_PREDICTION |
| DEV2230_9_tracefree_transfer | h_TF_residual | tracefree metric/coframe transfer not fixed by scalar R_AB closure | 0 | PPN tensor/vector residuals | M_TF response matrix; tensor/coframe transfer theorem | BOUND_BUDGET_ONLY_NOT_PREDICTION |

## Sensitivity Map
| sensitivity_id | leak_parameter | observable_channel | control_coefficient | coefficient_status | required_parent_coefficient | claim_status |
| --- | --- | --- | --- | --- | --- | --- |
| SENS2230_0_qR_light_bending | q_R | solar light bending | 0.8756216406841224 | internal conversion factor from 14 | C_gamma_qR | NONCLAIM_INTERNAL_CONVERSION_ONLY |
| SENS2230_1_qR_shapiro | q_R | solar Shapiro delay scale | 59.7375179242781 | internal conversion factor from 14 | C_gamma_qR | NONCLAIM_INTERNAL_CONVERSION_ONLY |
| SENS2230_2_qR_mercury | q_R | Mercury perihelion | 28.65467507274745 | internal conversion factor from 14 | C_gamma_qR; C_peri_qR | NONCLAIM_INTERNAL_CONVERSION_ONLY |
| SENS2230_3_delta_beta_mercury | delta_beta | Mercury perihelion | -14.327337536373726 | internal conversion factor from 14 | C_beta_delta; C_peri_beta | NONCLAIM_INTERNAL_CONVERSION_ONLY |
| SENS2230_4_alpha_clock_gps | alpha_clock | GPS gravitational redshift | 45.718449825926655 | internal conversion factor from 14 | C_clock | NONCLAIM_INTERNAL_CONVERSION_ONLY |
| SENS2230_5_epsilon_matter_eotvos | epsilon_matter | Eotvos proxy | 1 | internal conversion factor from 14 | C_eta_epsilon | NONCLAIM_INTERNAL_CONVERSION_ONLY |
| SENS2230_6_source_norm_Gdot | sigma_Gdot | Gdot/G | MISSING_PARENT_INPUT | not present in 14; bound row exists but response coefficient does not | C_Gdot | NONCLAIM_INTERNAL_CONVERSION_ONLY |
| SENS2230_7_R10_curve | alpha_R10(lambda) | inverse-square/Yukawa curve | MISSING_CURVE_AND_PARENT_INPUT | symbolic curve row only; no scalar bound | C_R10(lambda) | NONCLAIM_INTERNAL_CONVERSION_ONLY |
| SENS2230_8_tracefree_ppn_vector | h_TF_residual | PPN vector/tensor residual | MISSING_RESPONSE_MATRIX | scalar closure does not define the tensor response | M_TF | NONCLAIM_INTERNAL_CONVERSION_ONLY |

## Local Bound Links
| bound_link_id | row_id | used_for_channel | observable | upper_bound | units | numeric_bound_parse | budget_use |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BL2230_R0_identity_coframe_direct | R0_identity_coframe_direct | DEV2230_2_epsilon_matter | eta_WEP_direct_geometry | 2.8e-15 | dimensionless | PASS | control budget only; no MTS prediction until parent coefficient is sourced |
| BL2230_R1_WEP_source_charge | R1_WEP_source_charge | DEV2230_2_epsilon_matter | eta_WEP_source_charge | 2.8e-15 | dimensionless | PASS | control budget only; no MTS prediction until parent coefficient is sourced |
| BL2230_R2_clock_redshift | R2_clock_redshift | DEV2230_3_alpha_clock | alpha_clock_redshift | 2.48e-05 | dimensionless | PASS | control budget only; no MTS prediction until parent coefficient is sourced |
| BL2230_R3_gamma | R3_gamma | DEV2230_0_qR_gamma | gamma_minus_1 | 2.3e-05 | dimensionless | PASS | control budget only; no MTS prediction until parent coefficient is sourced |
| BL2230_R4_beta | R4_beta | DEV2230_1_delta_beta | beta_minus_1 | 7.8e-05 | dimensionless | PASS | control budget only; no MTS prediction until parent coefficient is sourced |
| BL2230_R5_alpha1 | R5_alpha1 | DEV2230_5_preferred_frame_alpha1; DEV2230_9_tracefree_transfer | alpha1 | 1e-04 | dimensionless | PASS | control budget only; no MTS prediction until parent coefficient is sourced |
| BL2230_R6_alpha2 | R6_alpha2 | DEV2230_6_preferred_frame_alpha2; DEV2230_9_tracefree_transfer | alpha2 | 2e-09 | dimensionless | PASS | control budget only; no MTS prediction until parent coefficient is sourced |
| BL2230_R7_alpha3 | R7_alpha3 | DEV2230_7_flux_alpha3_xi | alpha3 | 4e-20 | dimensionless | PASS | control budget only; no MTS prediction until parent coefficient is sourced |
| BL2230_R8_xi | R8_xi | DEV2230_7_flux_alpha3_xi; DEV2230_9_tracefree_transfer | xi | 4e-09 | dimensionless | PASS | control budget only; no MTS prediction until parent coefficient is sourced |
| BL2230_R9_Gdot | R9_Gdot | DEV2230_4_Gdot_source_norm | Gdot_over_G | 9.6e-15 | yr^-1 | PASS | control budget only; no MTS prediction until parent coefficient is sourced |
| BL2230_R10_fifth_force | R10_fifth_force | DEV2230_8_R10_finite_range | delta_G_or_fifth_force_yukawa | alpha(lambda) | range-dependent | SYMBOLIC_CURVE_REQUIRED | control budget only; no MTS prediction until parent coefficient is sourced |

## Bound Budget
| budget_id | leak_parameter | local_bound_rows | control_bound_if_unit_response | bound_units | blocking_input | budget_status |
| --- | --- | --- | --- | --- | --- | --- |
| BUD2230_0_qR | q_R | R3_gamma | 2.3e-05 | dimensionless | MISSING_C_gamma_qR | CONTROL_BOUND_ONLY_NOT_MTS_PREDICTION |
| BUD2230_1_delta_beta | delta_beta | R4_beta | 7.8e-05 | dimensionless | MISSING_C_beta_delta | CONTROL_BOUND_ONLY_NOT_MTS_PREDICTION |
| BUD2230_2_epsilon_matter_direct | epsilon_matter | R0_identity_coframe_direct; R1_WEP_source_charge | 2.8e-15 | dimensionless | MISSING_C_eta_epsilon_AND_MATTER_DESCENT | CONTROL_BOUND_ONLY_NOT_MTS_PREDICTION |
| BUD2230_3_alpha_clock | alpha_clock | R2_clock_redshift | 2.48e-05 | dimensionless | MISSING_C_clock | CONTROL_BOUND_ONLY_NOT_MTS_PREDICTION |
| BUD2230_4_sigma_Gdot | sigma_Gdot | R9_Gdot | 9.6e-15 | yr^-1 | MISSING_C_Gdot_AND_SOURCE_NORMALIZATION | CONTROL_BOUND_ONLY_NOT_MTS_PREDICTION |
| BUD2230_5_alpha1_frame | epsilon_frame_1 | R5_alpha1 | 1e-04 | dimensionless | MISSING_C_alpha1_AND_FRAME_DESCENT | CONTROL_BOUND_ONLY_NOT_MTS_PREDICTION |
| BUD2230_6_alpha2_frame | epsilon_frame_2 | R6_alpha2 | 2e-09 | dimensionless | MISSING_C_alpha2_AND_SPIN_RESPONSE | CONTROL_BOUND_ONLY_NOT_MTS_PREDICTION |
| BUD2230_7_alpha3_flux | epsilon_flux | R7_alpha3 | 4e-20 | dimensionless | MISSING_C_alpha3_AND_BOUNDARY_SILENCE | CONTROL_BOUND_ONLY_NOT_MTS_PREDICTION |
| BUD2230_8_xi_flux | epsilon_flux | R8_xi | 4e-09 | dimensionless | MISSING_C_xi_AND_BOUNDARY_SILENCE | CONTROL_BOUND_ONLY_NOT_MTS_PREDICTION |
| BUD2230_9_R10_curve | alpha_R10(lambda) | R10_fifth_force | alpha(lambda) | range-dependent | MISSING_C_R10_lambda_AND_DIGITIZED_CURVE | CONTROL_BOUND_ONLY_NOT_MTS_PREDICTION |
| BUD2230_10_tracefree_transfer | h_TF_residual | R5_alpha1; R6_alpha2; R8_xi | response-matrix-required | PPN residual vector | MISSING_M_TF_RESPONSE_MATRIX | CONTROL_BOUND_ONLY_NOT_MTS_PREDICTION |

## Runner
| runner_id | test | current_status | detail |
| --- | --- | --- | --- |
| RUN2230_0_sources | 2229 handoff and local-bound source files exist | PASS | source register validates local evidence for the deviation-budget checkpoint |
| RUN2230_1_channels | all closure leakage channels are named | PASS_NONCLAIM | q_R, delta_beta, epsilon_matter, alpha_clock, source normalization, preferred-frame, R10, and tracefree channels are included |
| RUN2230_2_bounds | local bounds link to real source rows | PASS_BOUND_LEDGER | numeric local bounds are parsed for R0-R9; R10 remains symbolic curve-only |
| RUN2230_3_prediction_refusal | do not convert budgets into MTS predictions | REFUSED_MISSING_PARENT_COEFFICIENTS | unit-response control budgets are not predictions until C_gamma_qR, C_beta_delta, C_eta_epsilon, C_clock, C_Gdot, frame coefficients, C_R10(lambda), and M_TF are sourced |
| RUN2230_4_claim_status | local GR/Newton/local-bound claim | BLOCKED_NO_CLAIM | closure deviations are now bounded as a bookkeeping problem, not claimed as empirical success |

## Claim Gate
| gate_id | claim | status | reason |
| --- | --- | --- | --- |
| GATE2230_0_parent_closure_origin |  | BLOCKED_NO_CLAIM | 2229 retained closure-only status |
| GATE2230_1_qR_coefficient |  | BLOCKED_NO_CLAIM | unit gamma map is control bookkeeping only |
| GATE2230_2_beta_completion |  | BLOCKED_NO_CLAIM | no parent second-order weak-field completion |
| GATE2230_3_matter_universality |  | BLOCKED_NO_CLAIM | WEP row is a severe budget, not a pass |
| GATE2230_4_clock_readout |  | BLOCKED_NO_CLAIM | clock coefficient still a response-map placeholder |
| GATE2230_5_source_normalization |  | BLOCKED_NO_CLAIM | Gdot budget cannot score without source theorem |
| GATE2230_6_frame_boundary |  | BLOCKED_NO_CLAIM | alpha1/alpha2/alpha3/xi rows are bound ledgers |
| GATE2230_7_R10_curve |  | BLOCKED_NO_CLAIM | symbolic R10 row cannot score finite-range hair |
| GATE2230_8_tracefree_matrix |  | BLOCKED_NO_CLAIM | scalar closure does not control all PPN residuals |

## Decision Ledger
| decision_id | decision | result | reason |
| --- | --- | --- | --- |
| DEC2230_0_verdict | local closure deviation budget exists but is nonclaim | BOUND_BUDGET_WRITTEN_PARENT_COEFFICIENTS_MISSING | local bounds can now discipline each leakage channel, but no channel has a sourced parent response coefficient |
| DEC2230_1_next | next target | NEXT_2231_COEFFICIENT_SOURCE_MAP | derive or source the first response coefficients before any local-bound scoring |

## Next Target
| next_id | next_target | script | objective | do_not |
| --- | --- | --- | --- | --- |
| NEXT2230_0_2231 | 2231-Y5-R2FR-qR-beta-matter-clock-coefficient-source-map-or-rejection.md | scripts/Y5_R2FR_qR_beta_matter_clock_coefficient_source_map_or_rejection_2231.py | derive or source the response coefficients mapping q_R, delta_beta, epsilon_matter, alpha_clock, source normalization, frame leakage, R10 range hair, and tracefree transfer into local observables | do not treat unit-response control budgets as MTS predictions; do not claim local GR derivation; do not edit formalization-workbench |

## Branch Copies
| copy_id | source_path | target_path | copied | parse_ok |
| --- | --- | --- | --- | --- |
| queue | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2230_BOUND_BUDGET_NONCLAIM.csv | source-intake/rab-sector/acquisition-queue/JR2230_CLOSURE_DEVIATION_BUDGET_NONCLAIM.csv | True | True |
| branch_wep | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2230_BOUND_BUDGET_NONCLAIM.csv | source-intake/microscope/branch_locked_wep/residuals/closure_deviation_budget_nonclaim_2230.csv | True | True |
| beta_docs | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2230_BOUND_BUDGET_NONCLAIM.csv | source-intake/beta-source/docs/CLOSURE_DEVIATION_BUDGET_2230_NONCLAIM.csv | True | True |

## Validation
| check_id | result | detail |
| --- | --- | --- |
| VAL2230_00_sources_exist | PASS | all cited 2230 source paths exist |
| VAL2230_01_prior_validations | PASS | 2229 and 1557 validations pass overall |
| VAL2230_02_channels_complete | PASS | all required local leakage channels are present |
| VAL2230_03_bound_rows_linked | PASS | local bound rows are linked to channels |
| VAL2230_04_numeric_bounds_parse | PASS | numeric R0-R9 local bounds parse cleanly |
| VAL2230_05_R10_symbolic | PASS | R10 remains symbolic curve-only |
| VAL2230_06_sensitivities_present | PASS | sensitivity map includes q_R and other channels |
| VAL2230_07_budgets_blocked | PASS | all bound budgets are control-only nonpredictions |
| VAL2230_08_runner_refuses_prediction | PASS | runner refuses MTS prediction scoring |
| VAL2230_09_claim_gates_block | PASS | all local claim gates remain blocked |
| VAL2230_10_decision_next | PASS | decision selects response-coefficient source map next |
| VAL2230_11_next_target | PASS | next target is current-numbered coefficient source map |
| VAL2230_12_csv_parse | PASS | all generated 2230 CSVs parse cleanly |
| VAL2230_13_claim_flags_false | PASS | all generated flags remain nonclaim |
| VAL2230_14_branch_copies | PASS | branch copies written and parse |
| VAL2230_15_pycache_absent | PASS | scripts __pycache__ absent after run |
| VAL2230_16_formalization_no_2230 | PASS | formalization-workbench has no non-venv 2230 artifacts |
| VAL2230_17_formalization_untouched | PASS | formalization-workbench untouched during 2230 run |
| VAL2230_OVERALL | PASS | 2230 imports closure-deviation channels, local-bound links, and control-only budgets while keeping predictions blocked until response coefficients are sourced |

## Working Interpretation

This is now a usable local test budget, but not yet a local prediction. It tells the theory exactly which response coefficients must be owned by the parent framework before the closure branch can face PPN, WEP, clock, R10, and source-normalization bounds. The win is discipline: instead of saying 'matches GR locally', the branch now says which hidden residuals must be made small, why, and by which missing coefficient.

