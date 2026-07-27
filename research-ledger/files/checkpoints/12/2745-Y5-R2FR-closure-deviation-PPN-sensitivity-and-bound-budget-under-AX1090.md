# 2745 - Y5 R2/f(R): Closure-Deviation PPN Sensitivity And Bound Budget Under AX1090

Status: `Y5_R2FR_2745_closure_deviation_bound_budget_written_parent_coefficients_missing`

## Private Verdict

2745 turns the local closure into a falsifiability map without pretending it is a prediction.

The dangerous leakage channels are now explicit:

`q_R`, `delta_beta`, `epsilon_matter`, `alpha_clock`, `sigma_Gdot`, preferred-frame leakage, boundary/source-flux leakage, finite-range R10 hair, and tracefree transfer.

The local bound ledger is harsh. The cleanest scalar first lane is `q_R -> gamma_minus_1`, because Cassini gives the direct control budget. The most brutal lane is matter universality: if `epsilon_matter` maps one-to-one into Eotvos `eta`, the budget is about `2.8e-15`.

But no MTS local prediction is scored here. Every budget remains control-only until the parent response coefficients are derived or source-backed. That is the next target.

## Source Register

| source_id | description | source_path | exists | needles_present | missing_needles | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| SRC2745_0_2744_doc | 2744 selects closure-deviation PPN sensitivity and bound budget. | 2744-Y5-R2FR-local-closure-PPN-benchmark-derived-vs-assumed-ledger-under-AX1090.md | True | True |  | False |
| SRC2745_1_2744_validation | 2744 validation output. | source-intake/mts_residuals/P8_Y5_BRR545_2744_VALIDATION.csv | True | True |  | False |
| SRC2745_2_1557_doc | prior closure-deviation sensitivity and bound budget. | 1557-Y5-closure-deviation-PPN-sensitivity-and-bound-budget.md | True | True |  | False |
| SRC2745_3_14_deviation_doc | internal deviation sensitivity source text. | 14-closure-deviation-PPN-sensitivity.md | True | True |  | False |
| SRC2745_4_2744_ppn | live PPN benchmark requirements feeding deviation rows. | source-intake/mts_residuals/P8_Y5_R2FR_2744_PPN_BENCHMARK_REQUIREMENTS.csv | True | True |  | False |
| SRC2745_5_local_bound_claims | local bound rows used as nonclaim budget constraints. | source-intake/local_bounds/local_bound_claims.csv | True | True |  | False |
| SRC2745_6_1557_channels | machine-readable prior channel map. | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1557_DEVIATION_CHANNELS.csv | True | True |  | False |
| SRC2745_7_1557_budget | machine-readable prior bound budget. | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1557_BOUND_BUDGET_NONCLAIM.csv | True | True |  | False |
| SRC2745_8_2744_queue | live queue into this checkpoint. | source-intake/rab-sector/acquisition-queue/JR2744_CLOSURE_DEVIATION_PPN_SENSITIVITY_NEXT.csv | True | True |  | False |

## Deviation Channels

| channel_id | leak_parameter | meaning | null_lane_value | first_observables | leading_control_map | missing_parent_inputs | local_bound_rows | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DEV2745_0_qR_gamma | q_R | reciprocal hair coefficient in R_AB approximately q_R L | 0 | gamma_minus_1; light_bending; Shapiro; perihelion | gamma_minus_1 ~= C_gamma_qR q_R, with internal control C_gamma_qR=1 not parent-signed | C_gamma_qR; parent R_AB leakage map; source normalization | R3_gamma | BOUND_BUDGET_ONLY_NOT_PREDICTION | False |
| DEV2745_1_delta_beta | delta_beta | nonlinear completion drift away from beta=1 | 0 | beta_minus_1; perihelion | beta_minus_1 ~= C_beta_delta delta_beta; Mercury control factor=(2 q_R-delta_beta)/3 | C_beta_delta; second-order weak-field completion | R4_beta | BOUND_BUDGET_ONLY_NOT_PREDICTION | False |
| DEV2745_2_epsilon_matter | epsilon_matter | spread away from universal matter/coframe coupling | 0 | eta_WEP_direct_geometry; eta_WEP_source_charge | eta ~= C_eta_epsilon epsilon_matter | C_eta_epsilon; matter action descent; no shadow-frame coupling | R0_identity_coframe_direct; R1_WEP_source_charge | BOUND_BUDGET_ONLY_NOT_PREDICTION | False |
| DEV2745_3_alpha_clock | alpha_clock | clock/load redshift anomaly | 0 | alpha_clock_redshift | redshift anomaly ~= C_clock alpha_clock | C_clock; universal clock/load readout map | R2_clock_redshift | BOUND_BUDGET_ONLY_NOT_PREDICTION | False |
| DEV2745_4_Gdot_source_norm | sigma_Gdot | time drift in measured source normalization GM or effective G | 0 yr^-1 | Gdot_over_G | Gdot/G ~= C_Gdot sigma_Gdot | C_Gdot; measured-GM/source normalization theorem | R9_Gdot | BOUND_BUDGET_ONLY_NOT_PREDICTION | False |
| DEV2745_5_preferred_frame_alpha1 | epsilon_frame_1 | vector/coframe preferred-frame leakage | 0 | alpha1 | alpha1 ~= C_alpha1 epsilon_frame_1 | C_alpha1; frame/coframe descent; boundary silence | R5_alpha1 | BOUND_BUDGET_ONLY_NOT_PREDICTION | False |
| DEV2745_6_preferred_frame_alpha2 | epsilon_frame_2 | spin or anisotropic coframe preferred-frame leakage | 0 | alpha2 | alpha2 ~= C_alpha2 epsilon_frame_2 | C_alpha2; spin/coframe descent; anisotropy map | R6_alpha2 | BOUND_BUDGET_ONLY_NOT_PREDICTION | False |
| DEV2745_7_flux_alpha3_xi | epsilon_flux | source flux, momentum nonconservation, or preferred-location leakage | 0 | alpha3; xi | alpha3 ~= C_alpha3 epsilon_flux; xi ~= C_xi epsilon_flux | C_alpha3; C_xi; boundary/no-charge/source-flux theorem | R7_alpha3; R8_xi | BOUND_BUDGET_ONLY_NOT_PREDICTION | False |
| DEV2745_8_R10_finite_range | alpha_R10(lambda) | finite-range q/source hair outside the exact closure | 0 for all lambda | delta_G_or_fifth_force_yukawa | Yukawa alpha(lambda) ~= C_R10(lambda) residual_hair(lambda) | C_R10(lambda); real digitized alpha(lambda) curve; parent range map | R10_fifth_force | BOUND_BUDGET_ONLY_NOT_PREDICTION | False |
| DEV2745_9_tracefree_transfer | h_TF_residual | tracefree metric/coframe transfer not fixed by scalar R_AB closure | 0 | PPN tensor/vector residuals | PPN residual vector ~= M_TF h_TF_residual | M_TF response matrix; tensor/coframe transfer theorem | R5_alpha1; R6_alpha2; R8_xi | BOUND_BUDGET_ONLY_NOT_PREDICTION | False |

## Local Bound Links

| row_id | used_for_channel | observable | upper_bound | units | numeric_bound_parse | reference_path_or_url | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| R0_identity_coframe_direct | DEV2745_2_epsilon_matter | eta_WEP_direct_geometry | 2.8e-15 | dimensionless | PASS | https://arxiv.org/abs/2209.15487; doi:10.1103/PhysRevLett.129.121102 | False |
| R1_WEP_source_charge | DEV2745_2_epsilon_matter | eta_WEP_source_charge | 2.8e-15 | dimensionless | PASS | https://arxiv.org/abs/2209.15487; doi:10.1103/PhysRevLett.129.121102 | False |
| R2_clock_redshift | DEV2745_3_alpha_clock | alpha_clock_redshift | 2.48e-05 | dimensionless | PASS | https://arxiv.org/abs/1812.03711; doi:10.1103/PhysRevLett.121.231101 | False |
| R3_gamma | DEV2745_0_qR_gamma | gamma_minus_1 | 2.3e-05 | dimensionless | PASS | https://www.nature.com/articles/nature01997; doi:10.1038/nature01997 | False |
| R4_beta | DEV2745_1_delta_beta | beta_minus_1 | 7.8e-05 | dimensionless | PASS | https://www2.math.ethz.ch/EMIS/journals/LRG/Articles/lrr-2014-4/articlese4.html | False |
| R5_alpha1 | DEV2745_5_preferred_frame_alpha1; DEV2745_9_tracefree_transfer | alpha1 | 1e-04 | dimensionless | PASS | https://www2.math.ethz.ch/EMIS/journals/LRG/Articles/lrr-2014-4/articlese4.html | False |
| R6_alpha2 | DEV2745_6_preferred_frame_alpha2; DEV2745_9_tracefree_transfer | alpha2 | 2e-09 | dimensionless | PASS | https://www2.math.ethz.ch/EMIS/journals/LRG/Articles/lrr-2014-4/articlese4.html | False |
| R7_alpha3 | DEV2745_7_flux_alpha3_xi | alpha3 | 4e-20 | dimensionless | PASS | https://www2.math.ethz.ch/EMIS/journals/LRG/Articles/lrr-2014-4/articlese4.html | False |
| R8_xi | DEV2745_7_flux_alpha3_xi; DEV2745_9_tracefree_transfer | xi | 4e-09 | dimensionless | PASS | https://www2.math.ethz.ch/EMIS/journals/LRG/Articles/lrr-2014-4/articlese4.html | False |
| R9_Gdot | DEV2745_4_Gdot_source_norm | Gdot_over_G | 9.6e-15 | yr^-1 | PASS | https://www.ife.uni-hannover.de/de/forschung/publikationen/detail-ansicht?tx_univiepure_univiepure%5Buuid%5D=cbe8f824-b21b-4e80-b736-944c3f960f7a; doi:10.3390/universe7020034 | False |
| R10_fifth_force | DEV2745_8_R10_finite_range | delta_G_or_fifth_force_yukawa | alpha(lambda) | range-dependent | SYMBOLIC_CURVE_REQUIRED | https://arxiv.org/abs/hep-ph/0307284; doi:10.1146/annurev.nucl.53.041002.110503 | False |

## Sensitivity Map

| sensitivity_id | leak_parameter | observable_channel | control_coefficient | coefficient_units | required_parent_coefficient | claim_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SENS2745_0_qR_light_bending | q_R | solar light bending | 0.8756216406841224 | arcsec per unit q_R | C_gamma_qR | NONCLAIM_INTERNAL_CONVERSION_ONLY | False |
| SENS2745_1_qR_shapiro | q_R | solar Shapiro delay scale | 59.7375179242781 | microseconds per unit q_R | C_gamma_qR | NONCLAIM_INTERNAL_CONVERSION_ONLY | False |
| SENS2745_2_qR_mercury | q_R | Mercury perihelion | 28.65467507274745 | arcsec/century per unit q_R | C_gamma_qR; C_peri_qR | NONCLAIM_INTERNAL_CONVERSION_ONLY | False |
| SENS2745_3_delta_beta_mercury | delta_beta | Mercury perihelion | -14.327337536373726 | arcsec/century per unit delta_beta | C_beta_delta; C_peri_beta | NONCLAIM_INTERNAL_CONVERSION_ONLY | False |
| SENS2745_4_alpha_clock_gps | alpha_clock | GPS gravitational redshift | 45.718449825926655 | microseconds/day per unit alpha_clock | C_clock | NONCLAIM_INTERNAL_CONVERSION_ONLY | False |
| SENS2745_5_epsilon_matter_eotvos | epsilon_matter | Eotvos proxy | 1 | dimensionless proxy per unit coupling spread | C_eta_epsilon | NONCLAIM_INTERNAL_CONVERSION_ONLY | False |
| SENS2745_6_source_norm_Gdot | sigma_Gdot | Gdot/G | MISSING_PARENT_INPUT | yr^-1 per unit source-normalization drift | C_Gdot | NONCLAIM_INTERNAL_CONVERSION_ONLY | False |
| SENS2745_7_R10_curve | alpha_R10(lambda) | inverse-square/Yukawa curve | MISSING_CURVE_AND_PARENT_INPUT | alpha(lambda) per residual hair amplitude | C_R10(lambda) | NONCLAIM_INTERNAL_CONVERSION_ONLY | False |
| SENS2745_8_tracefree_ppn_vector | h_TF_residual | PPN vector/tensor residual | MISSING_RESPONSE_MATRIX | PPN residual per tracefree transfer amplitude | M_TF | NONCLAIM_INTERNAL_CONVERSION_ONLY | False |

## Bound Budget

| budget_id | leak_parameter | local_bound_rows | control_bound_if_unit_response | bound_units | interpretation | blocking_input | budget_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BUD2745_0_qR | q_R | R3_gamma | 2.3e-05 | dimensionless | abs(q_R) <= 2.3e-5 only if C_gamma_qR=1 is parent-derived | MISSING_C_gamma_qR | CONTROL_BOUND_ONLY_NOT_MTS_PREDICTION | False |
| BUD2745_1_delta_beta | delta_beta | R4_beta | 7.8e-05 | dimensionless | abs(delta_beta) <= 7.8e-5 only if beta drift maps one-to-one | MISSING_C_beta_delta | CONTROL_BOUND_ONLY_NOT_MTS_PREDICTION | False |
| BUD2745_2_epsilon_matter_direct | epsilon_matter | R0_identity_coframe_direct; R1_WEP_source_charge | 2.8e-15 | dimensionless | abs(epsilon_matter) <= 2.8e-15 only if eta map is one-to-one | MISSING_C_eta_epsilon_AND_MATTER_DESCENT | CONTROL_BOUND_ONLY_NOT_MTS_PREDICTION | False |
| BUD2745_3_alpha_clock | alpha_clock | R2_clock_redshift | 2.48e-05 | dimensionless | abs(alpha_clock) <= 2.48e-5 only if redshift map is one-to-one | MISSING_C_clock | CONTROL_BOUND_ONLY_NOT_MTS_PREDICTION | False |
| BUD2745_4_sigma_Gdot | sigma_Gdot | R9_Gdot | 9.6e-15 | yr^-1 | abs(Gdot/G) <= 9.6e-15 yr^-1 constrains time drift only after source-normalization theorem | MISSING_C_Gdot_AND_SOURCE_NORMALIZATION | CONTROL_BOUND_ONLY_NOT_MTS_PREDICTION | False |
| BUD2745_5_alpha1_frame | epsilon_frame_1 | R5_alpha1 | 1e-04 | dimensionless | preferred-frame leakage must fit alpha1 <= 1e-4 after frame descent | MISSING_C_alpha1_AND_FRAME_DESCENT | CONTROL_BOUND_ONLY_NOT_MTS_PREDICTION | False |
| BUD2745_6_alpha2_frame | epsilon_frame_2 | R6_alpha2 | 2e-09 | dimensionless | spin/anisotropy leakage must fit alpha2 <= 2e-9 after response map | MISSING_C_alpha2_AND_SPIN_RESPONSE | CONTROL_BOUND_ONLY_NOT_MTS_PREDICTION | False |
| BUD2745_7_alpha3_flux | epsilon_flux | R7_alpha3 | 4e-20 | dimensionless | momentum/source-flux leakage must fit alpha3 <= 4e-20 after boundary theorem | MISSING_C_alpha3_AND_BOUNDARY_SILENCE | CONTROL_BOUND_ONLY_NOT_MTS_PREDICTION | False |
| BUD2745_8_xi_flux | epsilon_flux | R8_xi | 4e-09 | dimensionless | preferred-location leakage must fit xi <= 4e-9 after boundary/location response map | MISSING_C_xi_AND_BOUNDARY_SILENCE | CONTROL_BOUND_ONLY_NOT_MTS_PREDICTION | False |
| BUD2745_9_R10_curve | alpha_R10(lambda) | R10_fifth_force | alpha(lambda) | range-dependent | finite-range hair cannot be scored until a real alpha(lambda) curve and parent range map exist | MISSING_C_R10_lambda_AND_DIGITIZED_CURVE | CONTROL_BOUND_ONLY_NOT_MTS_PREDICTION | False |
| BUD2745_10_tracefree_transfer | h_TF_residual | R5_alpha1; R6_alpha2; R8_xi | response-matrix-required | PPN residual vector | tracefree leakage has no scalar budget until tensor/coframe response matrix exists | MISSING_M_TF_RESPONSE_MATRIX | CONTROL_BOUND_ONLY_NOT_MTS_PREDICTION | False |

## Response Coefficient Source Queue

| coefficient_id | required_coefficient | role | feeds_channel | source_or_derivation_requirement | priority | current_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| COEF2745_0_C_gamma_qR | C_gamma_qR | maps reciprocal hair q_R into gamma_minus_1 | DEV2745_0_qR_gamma | derive from weak-field metric/coframe response or source from parent q-sector leakage equation | HIGH_CASSINI | MISSING_PARENT_RESPONSE_COEFFICIENT | False |
| COEF2745_1_C_beta_delta | C_beta_delta | maps second-order completion drift into beta_minus_1 | DEV2745_1_delta_beta | derive from second-order local field equations and source normalization | HIGH_BETA_PERIHELION | MISSING_PARENT_RESPONSE_COEFFICIENT | False |
| COEF2745_2_C_eta_epsilon | C_eta_epsilon | maps matter/coframe nonuniversality into Eotvos eta | DEV2745_2_epsilon_matter | derive matter action descent and composition response | SEVERE_WEP | MISSING_PARENT_RESPONSE_COEFFICIENT | False |
| COEF2745_3_C_clock | C_clock | maps clock-load readout drift into redshift anomaly | DEV2745_3_alpha_clock | derive universal clock/load readout from matter action or source clock model | HIGH_CLOCK | MISSING_PARENT_RESPONSE_COEFFICIENT | False |
| COEF2745_4_C_Gdot | C_Gdot | maps source-normalization drift into Gdot/G | DEV2745_4_Gdot_source_norm | derive measured GM theorem and time-stationary source normalization | HIGH_LLR | MISSING_PARENT_RESPONSE_COEFFICIENT | False |
| COEF2745_5_C_frame | C_alpha1; C_alpha2 | maps frame/coframe leakage into preferred-frame PPN parameters | DEV2745_5_preferred_frame_alpha1; DEV2745_6_preferred_frame_alpha2 | derive frame descent, spin response, and anisotropy map | HIGH_PREFERRED_FRAME | MISSING_PARENT_RESPONSE_COEFFICIENT | False |
| COEF2745_6_C_flux | C_alpha3; C_xi | maps boundary/source flux into alpha3 and xi | DEV2745_7_flux_alpha3_xi | derive boundary silence/no-charge/source-flux theorem | EXTREME_ALPHA3 | MISSING_PARENT_RESPONSE_COEFFICIENT | False |
| COEF2745_7_C_R10_lambda | C_R10(lambda) | maps finite-range residual hair into Yukawa alpha(lambda) | DEV2745_8_R10_finite_range | derive parent range map and acquire real digitized alpha(lambda) curve | HIGH_R10 | MISSING_PARENT_RESPONSE_COEFFICIENT | False |
| COEF2745_8_M_TF | M_TF | maps tracefree metric/coframe residual into PPN residual vector | DEV2745_9_tracefree_transfer | derive tensor/coframe transfer theorem and response matrix | HIGH_TRACEFREE | MISSING_PARENT_RESPONSE_COEFFICIENT | False |

## Runner

| runner_id | test | current_status | detail | valid_for_claim |
| --- | --- | --- | --- | --- |
| RUN2745_0_sources | 2744 handoff, 1557 prior, and local-bound source files exist | PASS | source register validates local evidence for the deviation-budget checkpoint | False |
| RUN2745_1_channels | all closure leakage channels are named | PASS_NONCLAIM | q_R, beta drift, matter, clock, source normalization, preferred-frame, R10, and tracefree channels included | False |
| RUN2745_2_bounds | local bounds link to real source rows | PASS_BOUND_LEDGER | numeric local bounds parse for R0-R9; R10 remains symbolic curve-only | False |
| RUN2745_3_coefficients | response coefficients are source-ready | PASS_QUEUE_ONLY | coefficient queue names the missing parent inputs before scoring | False |
| RUN2745_4_prediction_refusal | do not convert budgets into MTS predictions | REFUSED_MISSING_PARENT_COEFFICIENTS | unit-response control budgets are not predictions until response coefficients are sourced | False |
| RUN2745_5_claim_status | local GR/Newton/local-bound claim | BLOCKED_NO_CLAIM | closure deviations are now bounded as bookkeeping, not empirical success | False |

## Claim Gates

| claim_gate_id | claim_gate | status | reason | valid_for_claim |
| --- | --- | --- | --- | --- |
| GATE2745_0_parent_closure_origin | derive R_AB=0 and Q_R=0 from parent action | BLOCKED_NO_CLAIM | 2744 retained closure-only status | False |
| GATE2745_1_qR_coefficient | source C_gamma_qR and perihelion response | BLOCKED_NO_CLAIM | unit gamma map is control bookkeeping only | False |
| GATE2745_2_beta_completion | derive beta drift response from second-order field equations | BLOCKED_NO_CLAIM | no parent second-order weak-field completion | False |
| GATE2745_3_matter_universality | derive universal matter/coframe coupling | BLOCKED_NO_CLAIM | WEP row is severe budget, not a pass | False |
| GATE2745_4_clock_readout | derive clock/load redshift response | BLOCKED_NO_CLAIM | clock coefficient still a response-map placeholder | False |
| GATE2745_5_source_normalization | derive measured GM/Gdot source normalization | BLOCKED_NO_CLAIM | Gdot budget cannot score without source theorem | False |
| GATE2745_6_frame_boundary | derive preferred-frame and boundary silence | BLOCKED_NO_CLAIM | alpha1/alpha2/alpha3/xi rows are bound ledgers | False |
| GATE2745_7_R10_curve | provide real digitized alpha(lambda) curve and parent range map | BLOCKED_NO_CLAIM | symbolic R10 row cannot score finite-range hair | False |
| GATE2745_8_tracefree_matrix | derive tensor/coframe response matrix M_TF | BLOCKED_NO_CLAIM | scalar closure does not control all PPN residuals | False |

## Decision Ledger

| decision_id | decision | result | reason | valid_for_claim |
| --- | --- | --- | --- | --- |
| DEC2745_0_verdict | local closure deviation budget exists but is nonclaim | BOUND_BUDGET_WRITTEN_PARENT_COEFFICIENTS_MISSING | local bounds can now discipline each leakage channel, but no channel has a sourced parent response coefficient | False |
| DEC2745_1_hardest_gate | matter universality is the most brutal local budget | WEP_SEVERE | epsilon_matter is constrained at roughly 2.8e-15 only after C_eta_epsilon is parent-derived | False |
| DEC2745_2_first_testing_lane | q_R/gamma is the cleanest first scalar leakage lane | Q_R_GAMMA_FIRST | Cassini gamma gives a direct scalar budget while beta and perihelion are more degenerate | False |
| DEC2745_3_next | next target is response-coefficient source map | NEXT_2746_COEFFICIENT_SOURCE_MAP | derive or source the first response coefficients before any local-bound scoring | False |

## Next Target

| next_id | status | target_doc | target_script | mission | acceptance | forbidden | selected | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NEXT2745_0_2746 | selected_primary | 2746-Y5-R2FR-qR-beta-matter-clock-coefficient-source-map-or-rejection-under-AX1090.md | scripts/Y5_R2FR_qR_beta_matter_clock_coefficient_source_map_or_rejection_under_AX1090_2746.py | derive or source response coefficients mapping q_R, delta_beta, epsilon_matter, alpha_clock, source normalization, frame leakage, R10 range hair, and tracefree transfer into local observables | promote only coefficients with parent derivation or source-backed mapping; otherwise keep each local test nonclaim and choose the first derivable coefficient target | do not treat unit-response control budgets as MTS predictions; do not claim local GR derivation; do not edit formalization-workbench | True | False |

## Branch Copies

| copy_id | source_table | copy_path | purpose | exists | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| BR2745_0_budget | source-intake/mts_residuals/P8_Y5_R2FR_2745_BOUND_BUDGET_NONCLAIM.csv | source-intake/local_bounds/closure_deviation_bound_budget_2745_NONCLAIM.csv | local-bound closure deviation budget | True | False |
| BR2745_1_coefficients | source-intake/mts_residuals/P8_Y5_R2FR_2745_RESPONSE_COEFFICIENT_SOURCE_QUEUE.csv | source-intake/source-weight/response_coefficient_source_queue_2745_NONCLAIM.csv | source-weight response coefficient queue | True | False |
| BR2745_2_next_queue | source-intake/mts_residuals/P8_Y5_R2FR_2745_NEXT_TARGET.csv | source-intake/rab-sector/acquisition-queue/JR2745_RESPONSE_COEFFICIENT_SOURCE_MAP_NEXT.csv | RAB acquisition queue for response-coefficient source map | True | False |

## Validation

| validation_id | passed | detail | timestamp_utc |
| --- | --- | --- | --- |
| VAL2745_0_sources | True | all source paths exist and required anchors/needles are present | 2026-06-23T14:21:58.761346+00:00 |
| VAL2745_1_channels_complete | True | all required local leakage channels are present | 2026-06-23T14:21:58.761361+00:00 |
| VAL2745_2_bound_rows_linked | True | R0-R10 local bound rows are linked to channels | 2026-06-23T14:21:58.761366+00:00 |
| VAL2745_3_numeric_bounds_parse | True | numeric R0-R9 local bounds parse cleanly and R10 remains symbolic | 2026-06-23T14:21:58.761369+00:00 |
| VAL2745_4_sensitivities_present | True | sensitivity map includes q_R and tracefree channels | 2026-06-23T14:21:58.761372+00:00 |
| VAL2745_5_budgets_blocked | True | all bound budgets are control-only nonpredictions | 2026-06-23T14:21:58.761375+00:00 |
| VAL2745_6_coefficients_queued | True | response coefficient source queue is present and missing-parent flagged | 2026-06-23T14:21:58.761378+00:00 |
| VAL2745_7_runner_refuses_prediction | True | runner refuses MTS prediction scoring | 2026-06-23T14:21:58.761381+00:00 |
| VAL2745_8_claim_gates | True | all local claim gates remain blocked and flags false | 2026-06-23T14:21:58.761384+00:00 |
| VAL2745_9_next_target | True | next target is response-coefficient source map | 2026-06-23T14:21:58.761386+00:00 |
| VAL2745_10_branch_outputs | True | branch copies exist | 2026-06-23T14:21:58.761389+00:00 |
| VAL2745_11_csv_parse | True | P8_Y5_R2FR_2745_SOURCE_REGISTER.csv:9:ok; P8_Y5_R2FR_2745_DEVIATION_CHANNELS.csv:10:ok; P8_Y5_R2FR_2745_LOCAL_BOUND_LINKS.csv:11:ok; P8_Y5_R2FR_2745_SENSITIVITY_MAP_NONCLAIM.csv:9:ok; closure_deviation_bound_budget_2745_NONCLAIM.csv:11:ok; response_coefficient_source_queue_2745_NONCLAIM.csv:9:ok; P8_Y5_R2FR_2745_RUNNER_NONCLAIM.csv:6:ok; P8_Y5_R2FR_2745_DECISION_LEDGER.csv:4:ok; P8_Y5_R2FR_2745_CLAIM_GATES.csv:9:ok; P8_Y5_R2FR_2745_NEXT_TARGET.csv:1:ok; P8_Y5_R2FR_2745_BRANCH_COPIES.csv:3:ok; JR2745_RESPONSE_COEFFICIENT_SOURCE_MAP_NEXT.csv:1:ok | 2026-06-23T14:21:58.761394+00:00 |
| VAL2745_12_pycache_absent | True | scripts __pycache__ absent=True | 2026-06-23T14:21:58.761404+00:00 |
| VAL2745_13_formalization_untouched | True | formalization-workbench recent modified-file count since script start = 0 | 2026-06-23T14:21:58.761408+00:00 |
| VAL2745_OVERALL | True | 2745 writes a nonclaim closure-deviation PPN sensitivity/bound budget and selects response-coefficient sourcing next | 2026-06-23T14:21:58.761416+00:00 |

## Plain-English Read

This is the point where the work becomes properly test-shaped. The closure lane itself is not a claim, but every way it can leak is now connected to a local observable and a bound. The next round is the coefficient hunt: if we can derive even the first clean response coefficient, the local branch stops being just a benchmark and starts becoming a real constrained theory lane.
