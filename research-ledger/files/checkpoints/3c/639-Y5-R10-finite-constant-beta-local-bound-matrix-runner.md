# 639 Y5 R10 finite constant beta local bound matrix runner

Status: `Y5_R10_finite_constant_beta_local_bound_matrix_built_bounds_present_predictions_symbolic_nonclaim`  
Claim ceiling: `local_bound_matrix_assembly_only_no_numeric_MTS_score_no_cg_zero_R10_WEP_PPN_clock_or_local_GR_pass`  
Next target: `640-Y5-R10-charge-topology-or-kappa-alpha-numeric-prior.md`

## Verdict
- The local bound matrix now exists: WEP, clocks, PPN, Gdot, R10, and EH-operator rows are mapped to the constant-beta prediction side.
- Bounds are present, but MTS predictions are not numeric yet: `kappa_i`, `beta_A`, `Z_eff`, `lambda_X`, `tau_arena`, and the operator vector remain missing.
- The R10 pressure import is retained as a private nonclaim diagnostic only.
- No local test score or pass is allowed from this checkpoint.

## Bound Matrix Logic
Each row has the same structure:

`observable_bound` from `local_bound_claims.csv`,

`prediction_law` from the 638 constant-beta laws,

`required_mts_inputs` naming the exact coefficients still missing.

This prevents the old failure mode where R10 is tested in isolation while WEP, clocks, PPN, or source-normalization couplings are left in the fog.

## Source Register
| source_id | source_path | exists | role | valid_for_claim |
| --- | --- | --- | --- | --- |
| SRC639_0 | 638-Y5-R10-constant-sector-zero-or-finite-beta-derivation.md | true | immediate 638 checkpoint | false |
| SRC639_1 | source-intake/mts_residuals/P8_Y5_BRR545_638_VALIDATION.csv | true | 638 validation gate | false |
| SRC639_2 | source-intake/mts_residuals/P8_Y5_R10_638_FINITE_BETA_LAWS.csv | true | 638 symbolic finite beta laws | false |
| SRC639_3 | source-intake/mts_residuals/P8_Y5_R10_638_ARENA_PROJECTION_MATRIX.csv | true | 638 arena projection matrix | false |
| SRC639_4 | source-intake/mts_residuals/P8_Y5_R10_638_CONSTANT_VERDICT.csv | true | 638 constant verdict | false |
| SRC639_5 | source-intake/mts_residuals/P8_Y5_R10_635_TWO_LEG_NUMERIC_INPUT_RUNNER.csv | true | R10 pressure-only two-leg envelope summary | false |
| SRC639_6 | source-intake/local_bounds/local_bound_claims.csv | true | verified local bound claims table | false |
| SRC639_7 | source-intake/local_bounds/README.md | true | local bound source intake rule | false |
| SRC639_8 | source-intake/local_bounds/R10_alpha_lambda_bound_curve_VECTOR_2020_REVIEW_CANDIDATE.csv | true | R10 vector curve review candidate, nonclaim | false |
| SRC639_9 | scripts/Y5_R10_finite_constant_beta_local_bound_matrix_runner.py | true | this checkpoint generator | false |

## Constant Beta Symbol Table
| symbol_id | symbol | meaning | units | needed_for | current_value | owner_needed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SYM639_0_kappa_alpha | kappa_alpha | d ln alpha_EM / dXhat | per_Xhat_unit | EM spectra;clock ratios;WEP composition | MISSING_PARENT_NUMERIC | charge topology/gauge kinetic parent derivation or numeric finite prior | false |
| SYM639_1_kappa_mass | kappa_mass_i | d ln dimensionless mass/binding ratio i / dXhat | per_Xhat_unit | WEP;clock ratios;body beta_A | MISSING_PARENT_NUMERIC | mass-spectrum/representation parent derivation or numeric sensitivity prior | false |
| SYM639_2_beta_A | beta_A | sum_i S_Ai kappa_i plus any material marker derivative | dimensionless_per_Xhat_unit | R10;WEP;orbital source/test coupling | MISSING_COMPOSITION_NUMERIC | composition sensitivity matrix S_Ai and marker theorem/coefficients | false |
| SYM639_3_Z_eff | Z_eff | quadratic normalization of exchanged local residual mode | action_normalization | R10 finite-range alpha_X(lambda) | MISSING_PARENT_HESSIAN | second variation of parent local action | false |
| SYM639_4_lambda_X | lambda_X | range of exchanged mode sqrt(Z_eff/M_X^2) | m | R10;orbital finite-range profile | MISSING_PARENT_HESSIAN | local mode mass/range from Hessian and boundary/domain spectrum | false |
| SYM639_5_tau_arena | tau_R10,tau_WEP,tau_clock,tau_PPN,tau_orbital | arena-specific projection/normalization from beta law to observable | dimensionless_or_arena_units | all local bound rows | MISSING_ARENA_PROJECTION | apparatus/source geometry, clock sensitivities, PPN map, orbital source normalization | false |
| SYM639_6_delta_GM | delta_GM | source-normalization/operator residual in measured GM | dimensionless_or_per_time | Gdot;orbital;PPN source normalization | MISSING_GR_OPERATOR_NUMERIC | EH/PPN/source-normalization derivation | false |

## Local Bound Matrix
| matrix_id | row_id | arena | observable | bound_value | bound_units | bound_kind | reference_path_or_url | prediction_law | required_mts_inputs | projection_route | bound_present | prediction_numeric_ready | runner_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LBM639_0 | R0_identity_coframe_direct | MICROSCOPE/Eotvos/composition | eta_WEP_direct_geometry | 2.8e-15 | dimensionless | numeric_bound | https://arxiv.org/abs/2209.15487; doi:10.1103/PhysRevLett.129.121102 | eta_AB ~ tau_WEP beta_source sum_i(S_Ai-S_Bi) kappa_i | kappa_i;S_Ai;S_Bi;beta_source;tau_WEP | WEP/composition beta vector | true | false | bound_present_prediction_symbolic_nonclaim | false |
| LBM639_1 | R1_WEP_source_charge | MICROSCOPE/Eotvos/composition | eta_WEP_source_charge | 2.8e-15 | dimensionless | numeric_bound | https://arxiv.org/abs/2209.15487; doi:10.1103/PhysRevLett.129.121102 | eta_AB ~ tau_WEP beta_source sum_i(S_Ai-S_Bi) kappa_i | kappa_i;S_Ai;S_Bi;beta_source;tau_WEP | WEP/composition beta vector | true | false | bound_present_prediction_symbolic_nonclaim | false |
| LBM639_2 | R2_clock_redshift | redshift/clocks | alpha_clock_redshift | 2.48e-05 | dimensionless | numeric_bound | https://arxiv.org/abs/1812.03711; doi:10.1103/PhysRevLett.121.231101 | alpha_clock ~ tau_clock sum_i(K_ai-K_bi) kappa_i | kappa_i;K_ai;K_bi;tau_clock | clock sensitivity vector | true | false | bound_present_prediction_symbolic_nonclaim | false |
| LBM639_3 | R3_gamma | Cassini/VLBI/solar-system light propagation | gamma_minus_1 | 2.3e-05 | dimensionless | numeric_bound | https://www.nature.com/articles/nature01997; doi:10.1038/nature01997 | gamma_minus_1_pred = PPN_operator_projection(delta_GM,disformal_residual,non_EH_vector) | delta_GM;disformal_residual;non_EH_operator_vector;tau_PPN | PPN/operator residual vector | true | false | bound_present_prediction_symbolic_nonclaim | false |
| LBM639_4 | R4_beta | planetary ephemerides/LLR | beta_minus_1 | 7.8e-05 | dimensionless | numeric_bound | https://www2.math.ethz.ch/EMIS/journals/LRG/Articles/lrr-2014-4/articlese4.html | beta_minus_1_pred = PPN_operator_projection(delta_GM,disformal_residual,non_EH_vector) | delta_GM;disformal_residual;non_EH_operator_vector;tau_PPN | PPN/operator residual vector | true | false | bound_present_prediction_symbolic_nonclaim | false |
| LBM639_5 | R5_alpha1 | pulsar/solar-system preferred-frame | alpha1 | 1e-04 | dimensionless | numeric_bound | https://www2.math.ethz.ch/EMIS/journals/LRG/Articles/lrr-2014-4/articlese4.html | alpha1_pred = PPN_operator_projection(delta_GM,disformal_residual,non_EH_vector) | delta_GM;disformal_residual;non_EH_operator_vector;tau_PPN | PPN/operator residual vector | true | false | bound_present_prediction_symbolic_nonclaim | false |
| LBM639_6 | R6_alpha2 | solar-spin/pulsar preferred-frame | alpha2 | 2e-09 | dimensionless | numeric_bound | https://www2.math.ethz.ch/EMIS/journals/LRG/Articles/lrr-2014-4/articlese4.html | alpha2_pred = PPN_operator_projection(delta_GM,disformal_residual,non_EH_vector) | delta_GM;disformal_residual;non_EH_operator_vector;tau_PPN | PPN/operator residual vector | true | false | bound_present_prediction_symbolic_nonclaim | false |
| LBM639_7 | R7_alpha3 | pulsar/solar-system momentum flux | alpha3 | 4e-20 | dimensionless | numeric_bound | https://www2.math.ethz.ch/EMIS/journals/LRG/Articles/lrr-2014-4/articlese4.html | alpha3_pred = PPN_operator_projection(delta_GM,disformal_residual,non_EH_vector) | delta_GM;disformal_residual;non_EH_operator_vector;tau_PPN | PPN/operator residual vector | true | false | bound_present_prediction_symbolic_nonclaim | false |
| LBM639_8 | R8_xi | local anisotropy/preferred-location | xi | 4e-09 | dimensionless | numeric_bound | https://www2.math.ethz.ch/EMIS/journals/LRG/Articles/lrr-2014-4/articlese4.html | xi_pred = PPN_operator_projection(delta_GM,disformal_residual,non_EH_vector) | delta_GM;disformal_residual;non_EH_operator_vector;tau_PPN | PPN/operator residual vector | true | false | bound_present_prediction_symbolic_nonclaim | false |
| LBM639_9 | R9_Gdot | LLR/ephemerides/pulsars | Gdot_over_G | 9.6e-15 | yr^-1 | numeric_bound | https://www.ife.uni-hannover.de/de/forschung/publikationen/detail-ansicht?tx_univiepure_univiepure%5Buuid%5D=cbe8f824-b21b-4e80-b736-944c3f960f7a; doi:10.3390/universe7020034 | Gdot/G = d(delta_GM)/dt + source_normalization_drift | delta_GM;source_normalization_residual;time_map | source-normalization/orbital drift | true | false | bound_present_prediction_symbolic_nonclaim | false |
| LBM639_10 | R10_fifth_force | fifth-force/inverse-square | delta_G_or_fifth_force_yukawa | alpha(lambda) | range-dependent | alpha(lambda) | https://arxiv.org/abs/hep-ph/0307284; doi:10.1146/annurev.nucl.53.041002.110503 | alpha_X(lambda)=tau_R10(lambda) beta_source beta_test / Z_eff | beta_source;beta_test;Z_eff;lambda_X;tau_R10;alpha_bound(lambda) | R10 two-leg finite range | true | false | bound_present_prediction_symbolic_nonclaim | false |
| LBM639_11 | R11_EH_operator_ledger | local operator closure | non_EH_operator_coefficients | symbolic | operator family | symbolic | 425-EH-operator-retained-ledger-and-source-normalization-test-plan.md | non_EH_operator_coefficients -> PPN/source-normalization residual rows | EH_operator_coefficients;boundary_terms;source_normalization | EH/operator closure | true | false | bound_present_prediction_symbolic_nonclaim | false |

## R10 Pressure Import
| pressure_id | profile_factor | law | tightest_lambda_m | tightest_abs_c_eff_pressure_bound | physical_inputs_ready | missing_inputs | import_status | source | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R10P639_0 | 0.01 | alpha_X=profile_factor*c_eff^2 | 0.000608 | 0.48421733762 | false | beta_source;beta_test;Z_eff;lambda_X;profile_factor_source;cross_arena_projection | pressure_only_nonclaim | source-intake/mts_residuals/P8_Y5_R10_635_TWO_LEG_NUMERIC_INPUT_RUNNER.csv | false |
| R10P639_1 | 0.1 | alpha_X=profile_factor*c_eff^2 | 0.000608 | 0.153122966942 | false | beta_source;beta_test;Z_eff;lambda_X;profile_factor_source;cross_arena_projection | pressure_only_nonclaim | source-intake/mts_residuals/P8_Y5_R10_635_TWO_LEG_NUMERIC_INPUT_RUNNER.csv | false |
| R10P639_2 | 1 | alpha_X=profile_factor*c_eff^2 | 0.000608 | 0.048421733762 | false | beta_source;beta_test;Z_eff;lambda_X;profile_factor_source;cross_arena_projection | pressure_only_nonclaim | source-intake/mts_residuals/P8_Y5_R10_635_TWO_LEG_NUMERIC_INPUT_RUNNER.csv | false |
| R10P639_3 | 10 | alpha_X=profile_factor*c_eff^2 | 0.000608 | 0.0153122966942 | false | beta_source;beta_test;Z_eff;lambda_X;profile_factor_source;cross_arena_projection | pressure_only_nonclaim | source-intake/mts_residuals/P8_Y5_R10_635_TWO_LEG_NUMERIC_INPUT_RUNNER.csv | false |

## Numeric Slot Ledger
| slot_id | slot | needed_by_rows | current_status | minimum_to_score | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| NSL639_0_kappa_vector | kappa_alpha,kappa_mass_i,kappa_binding_i,kappa_clock_i | R0;R1;R2;EM_spectra | MISSING_PARENT_NUMERIC | numeric values or theorem-zero for each dimensionless constant derivative | false |
| NSL639_1_composition_sensitivities | S_Ai,S_Bi,source/test material composition | R0;R1;R10 | MISSING_COMPOSITION_NUMERIC | test/source body sensitivity vectors and material labels | false |
| NSL639_2_mode_normalization | Z_eff,M_X^2,lambda_X | R10;orbital finite-range | MISSING_PARENT_HESSIAN | local quadratic action/Hessian with units | false |
| NSL639_3_arena_tau | tau_R10,tau_WEP,tau_clock,tau_PPN,tau_orbital | all local matrix rows | MISSING_ARENA_PROJECTION | projection from MTS residual variables to each experimental observable | false |
| NSL639_4_operator_vector | delta_GM,disformal_residual,non_EH_operator_coefficients,boundary terms | R3;R4;R5;R6;R7;R8;R9;R11 | MISSING_GR_OPERATOR_NUMERIC | local EH/PPN/source-normalization derivation or explicit coefficient bounds | false |
| NSL639_5_bound_curve_promotion | alpha_bound(lambda) claim-grade curve | R10 | REVIEW_CANDIDATE_ONLY_FOR_R10_CURVE | verified table or human-QA promoted digitization; current pressure import remains nonclaim | false |

## Scoreability Gate
| gate_id | requirement | result | detail | score_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| SG639_0_bounds_loaded | local bound claims loaded into matrix | pass | matrix_rows=12;numeric_bounds=10 | false | false |
| SG639_1_predictions_numeric | MTS prediction side numeric for every score row | blocked | prediction_numeric_ready_rows=0 | false | false |
| SG639_2_missing_slots | all kappa/beta/Z/lambda/tau/operator slots filled | blocked | missing_slot_rows=6 | false | false |
| SG639_3_r10_pressure_import | R10 pressure import allowed only as nonclaim diagnostic | pass | pressure_rows=4 | false | false |
| SG639_4_claim_leak | no matrix row or pressure row valid for claim | pass | claim_rows=0 | false | false |

## Decision
| decision_id | decision | meaning | status | next_target | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| D639_0_main_verdict | Y5_R10_finite_constant_beta_local_bound_matrix_built_bounds_present_predictions_symbolic_nonclaim | local experimental bounds are assembled, but MTS prediction coefficients are still symbolic | matrix_ready_not_scoreable | 640-Y5-R10-charge-topology-or-kappa-alpha-numeric-prior.md | false |
| D639_1_r10 | R10_pressure_imported_nonclaim | unit-profile pressure bound remains |c_eff|~0.048 at lambda 0.000608 m, but beta/Z/lambda/profile inputs are missing | pressure_only | 640-Y5-R10-charge-topology-or-kappa-alpha-numeric-prior.md | false |
| D639_2_cross_arena | same_constant_failure_vector_maps_to_WEP_clock_R10_PPN_orbital | the matrix now prevents testing one arena while ignoring the same coupling in the others | discipline_improvement | 640-Y5-R10-charge-topology-or-kappa-alpha-numeric-prior.md | false |
| D639_3_claim_ceiling | local_bound_matrix_assembly_only_no_numeric_MTS_score_no_cg_zero_R10_WEP_PPN_clock_or_local_GR_pass | no local score or pass until missing numeric slots are parent-owned or source-backed | hard_guardrail | 640-Y5-R10-charge-topology-or-kappa-alpha-numeric-prior.md | false |

## Next Contract
| contract_id | required_output | success_condition | if_success | if_fail | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| NC639_0_kappa_alpha_route | derive charge/gauge coupling topologically or assign a sourced kappa_alpha prior for private pressure | alpha_EM row is either theorem-zero or numeric finite input | EM/clock/WEP rows can be partially scored | constant branch remains unscoreable | false |
| NC639_1_mass_clock_sensitivities | fill mass/composition/clock sensitivity vectors or prove representation/topological silence | beta_A and clock projection rows have numeric coefficients | WEP and clock pressure can run | zero branch still blocked by constants | false |
| NC639_2_R10_numeric_side | fill beta_source,beta_test,Z_eff,lambda_X,tau_R10 and promote/QA alpha(lambda) curve before scoring R10 | R10 row has both numeric prediction and claim-grade bound curve | R10 local pressure can be evaluated | R10 remains pressure-only | false |

## Nonclaim Summary
| status | claim_ceiling | matrix_rows | numeric_bound_rows | prediction_numeric_ready_rows | missing_slot_rows | r10_pressure_rows | unit_profile_tightest_abs_c_eff_pressure_bound | unit_profile_tightest_lambda_m | finite_branch_scoreable | next_target | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Y5_R10_finite_constant_beta_local_bound_matrix_built_bounds_present_predictions_symbolic_nonclaim | local_bound_matrix_assembly_only_no_numeric_MTS_score_no_cg_zero_R10_WEP_PPN_clock_or_local_GR_pass | 12 | 10 | 0 | 6 | 4 | 0.048421733762 | 0.000608 | false | 640-Y5-R10-charge-topology-or-kappa-alpha-numeric-prior.md | false |

## Validation
| check_id | result | detail |
| --- | --- | --- |
| V639_0_source_paths_exist | pass | missing=0 |
| V639_1_prior_638_clean | pass | prior_rows=11;prior_fails=0 |
| V639_2_local_bounds_loaded | pass | matrix_rows=12;bound_claim_rows=12 |
| V639_3_numeric_bounds_present_predictions_blocked | pass | numeric_bounds=10;prediction_ready=0 |
| V639_4_symbol_table_complete | pass | symbol_rows=7 |
| V639_5_r10_pressure_import_nonclaim | pass | pressure_rows=4;unit_bound=0.048421733762 |
| V639_6_missing_slots_complete | pass | slot_rows=6 |
| V639_7_scoreability_blocked | pass | gate_rows=5 |
| V639_8_next_contract_written | pass | contract_rows=3 |
| V639_9_no_claim_rows | pass | claim_rows=0 |
| V639_10_no_local_claim | pass | matrix_score=false;c_g_zero_claimed=false;finite_branch_scoreable=false;R10=false;WEP=false;PPN=false;clock=false;orbital=false;local_GR=false |

## Interpretation
This is the boring-but-essential testing scaffold. The theory is not being scored yet; the matrix simply says what a score would require. The next useful move is to try the charge/topology route first because `kappa_alpha` feeds EM, clock, and WEP rows. If that fails, assign a private numeric prior/envelope for `kappa_alpha` and see how violently the matrix reacts.
