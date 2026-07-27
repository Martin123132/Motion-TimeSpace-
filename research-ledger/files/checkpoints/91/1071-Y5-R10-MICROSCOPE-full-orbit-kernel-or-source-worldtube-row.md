# 1071 - MICROSCOPE full orbit kernel or source-worldtube row

## Current verdict
1071 acquires the official MICROSCOPE WEP readout kernel **skeleton**: data vector, fit basis, source-gravity proxy, inertia-gradient subtraction, segment/window rule, and frequency projection. It still does **not** acquire a numeric tau_WEP kernel or direct MTS product, so WEP/local-GR claims remain blocked.

## Local source register
| source_id | relative_path | exists | needle_found | note |
| --- | --- | --- | --- | --- |
| SRC1071_0_1070_next | source-intake/mts_residuals/P8_Y5_R10_1070_NEXT_TARGET.csv | true | true | 1070 handoff. |
| SRC1071_1_1070_validation | source-intake/mts_residuals/P8_Y5_BRR545_1070_VALIDATION.csv | true | true | 1070 validation summary. |
| SRC1071_2_1070_eta | source-intake/mts_residuals/P8_Y5_R10_1070_ETA_READOUT_FORMULA_ROWS.csv | true | true | eta formula acquired. |
| SRC1071_3_1070_orbit | source-intake/mts_residuals/P8_Y5_R10_1070_ORBIT_KERNEL_SOURCE_ROWS.csv | true | true | orbit metadata partial. |
| SRC1071_4_1070_fill | source-intake/mts_residuals/P8_Y5_R10_1070_READOUT_FILL_MATRIX_UPDATE.csv | true | true | full orbit kernel still missing. |
| SRC1071_5_1070_tau | source-intake/mts_residuals/P8_Y5_R10_1070_TAU_IMPACT_LEDGER.csv | true | true | tau still missing. |
| SRC1071_6_1070_product | source-intake/mts_residuals/P8_Y5_R10_1070_WEP_PRODUCT_CANDIDATE_NONCLAIM.csv | true | true | product runner remains blocked. |
| SRC1071_7_1068_worldtube | source-intake/mts_residuals/P8_Y5_R10_1068_SOURCE_WORLDTUBE_REQUIREMENTS.csv | true | true | source worldtube missing. |
| SRC1071_8_1061_material | source-intake/mts_residuals/P8_Y5_R10_1061_WEP_MATERIAL_CONVENTION.csv | true | true | material pair context only. |
| SRC1071_9_local_bounds | source-intake/local_bounds/local_bound_claims.csv | true | true | source-backed WEP bound row. |

## External kernel source ledger
| external_id | source_lines | kernel_status | kernel_item | valid_for_claim |
| --- | --- | --- | --- | --- |
| EXT1071_0_data_products | CQG 2022 PDF lines 308-351 | SOURCE_BACKED_DATA_PRODUCT_REQUIREMENTS | session data include 4 Hz accelerations, same-stamp attitude/angular velocity/angular acceleration in J2000, and minute-sampled satellite position/velocity | false |
| EXT1071_1_measurement_model_eq3 | CQG 2022 PDF lines 399-412 | SOURCE_BACKED_MEASUREMENT_MODEL | differential measured acceleration equals bias plus mapped applied differential acceleration plus common-mode/angular-coupling/noise terms | false |
| EXT1071_2_applied_acceleration_eq4 | CQG 2022 PDF lines 428-445 | SOURCE_BACKED_SOURCE_WORLDTUBE_PROXY_FORM | applied differential acceleration has WEP source leg delta*g(Osat), gravity-gradient/inertia offcentring leg ([T]-[In])*Delta, and physical bias | false |
| EXT1071_3_fundamental_eq6 | CQG 2022 PDF lines 491-523 | SOURCE_BACKED_REGRESSION_KERNEL_SKELETON | corrected X-axis regression uses bias, delta_x*g_x, delta_z*g_z, Delta_x*Sxx, Delta_z*Sxz, and noise; g/S functions are computed from position, pointing, angular velocity and acceleration | false |
| EXT1071_4_polynomial_eq7 | CQG 2022 PDF lines 533-543 | SOURCE_BACKED_FIT_BASIS | bias trend is a degree-three polynomial; final fit basis is polynomial trend plus gx,gz,Sxx,Sxz | false |
| EXT1071_5_frequency_table | CQG 2022 PDF lines 210-220 | SOURCE_BACKED_FREQUENCY_KERNEL | forb=0.16818e-3 Hz; fspin2=0.75681e-3 Hz; fspin3=2.94315e-3 Hz; fEP2=0.92499e-3 Hz; fEP3=3.11133e-3 Hz | false |
| EXT1071_6_segmentation_dft | CQG 2022 PDF lines 584-600 | SOURCE_BACKED_SEGMENT_WINDOW_RULE | selected segments are even numbers of orbits so combinations of orbital and spin frequencies land on DFT bins with low theoretical correlation | false |
| EXT1071_7_suep_segment_table | CQG 2022 PDF lines 607-628 | SOURCE_BACKED_SUEP_SEGMENT_LEDGER | SUEP selected segment durations and glitch percentages are tabulated for 19 segments totalling 1362 orbits | false |
| EXT1071_8_position_pointing_requirements | CQG 2012 PDF lines 209-227 | SOURCE_BACKED_POSITION_POINTING_REQUIREMENTS | kernel construction requires measurement dating, satellite position, instrument pointing, and fEP=forb+fspin in spin mode | false |
| EXT1071_9_onera_data_availability_page | ONERA public page | SOURCE_BACKED_DATA_PORTAL_POINTER | ONERA states MICROSCOPE mission data are available at https://cmsm-ds.onera.fr/user/microscope | false |

## Data portal probe
| url | probe_status | http_status | bytes_sampled | error |
| --- | --- | --- | --- | --- |
| https://microscope.onera.fr/fr/publication/microscope-data-are-available | HTTP_OK | 200 | 512 |  |
| https://cmsm-ds.onera.fr/user/microscope | BLOCKED_OR_UNREACHABLE_FROM_THIS_RUN |  | 0 | URLError: <urlopen error [WinError 10061] No connection could be made because the target machine actively refused it> |

## Official kernel components
| kernel_id | component | official_form | acquired_level | needed_numeric_inputs | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| KER1071_0_data_vector | observed vector | y(t)=Gamma_x,corr^(d)(t) after calibration/correction | FORM_AND_DATA_PRODUCT_REQUIREMENT_ONLY | 4Hz corrected differential acceleration per selected segment | false |
| KER1071_1_fit_basis | regression design basis | columns=[1,(t-t0),(t-t0)^2,(t-t0)^3,gx(t),gz(t),Sxx(t),Sxz(t)] | OFFICIAL_KERNEL_SKELETON_ACQUIRED | time stamps; gx; gz; Sxx; Sxz in instrument frame | false |
| KER1071_2_source_gravity_leg | Earth/source gravity proxy | g(Osat) and gravity-gradient tensor T computed at satellite centre | SOURCE_WORLDTUBE_PROXY_FORM_ACQUIRED_NOT_NUMERIC | satellite position/velocity and gravity model used by MICROSCOPE processing | false |
| KER1071_3_inertial_leg | inertia-gradient subtraction | S is the symmetric part of T-In, with In=Omega^2+Omega_dot | FORM_ACQUIRED_NOT_NUMERIC | attitude, angular velocity, angular acceleration at accelerometer time stamps | false |
| KER1071_4_segment_window | segment/window operator | selected continuous segments; even-orbit DFT-aligned windows; glitch masks | SOURCE_BACKED_SEGMENT_TABLE_ACQUIRED | segment masks, removed-sample indices, exact timestamps | false |
| KER1071_5_frequency_projection | frequency separation | gx,gz at fEP in phase quadrature; Sxx,Sxz mainly DC and 2fEP | FREQUENCY_KERNEL_FORM_ACQUIRED | mode-specific fEP, phase convention, segment timestamps | false |
| KER1071_6_verdict | tau_WEP kernel verdict | official kernel skeleton acquired, but no numeric orbit/attitude/source-worldtube kernel has been downloaded or reconstructed | KERNEL_SKELETON_YES_NUMERIC_TAU_NO | data portal products or reproduced gx/gz/Sxx/Sxz arrays | false |

## SUEP segment table
| segment_id | duration_orbits | position_begin_orbit | position_end_orbit | glitch_eliminated_percent | source_id |
| --- | --- | --- | --- | --- | --- |
| SUEP1071_210 | 50 | 1 | 50 | 18 | EXT1071_7_suep_segment_table |
| SUEP1071_212 | 60 | 1 | 60 | 17 | EXT1071_7_suep_segment_table |
| SUEP1071_218 | 120 | 1 | 120 | 15 | EXT1071_7_suep_segment_table |
| SUEP1071_234 | 92 | 1 | 92 | 18 | EXT1071_7_suep_segment_table |
| SUEP1071_236 | 120 | 1 | 120 | 21 | EXT1071_7_suep_segment_table |
| SUEP1071_238 | 120 | 1 | 120 | 24 | EXT1071_7_suep_segment_table |
| SUEP1071_252 | 106 | 1 | 106 | 26 | EXT1071_7_suep_segment_table |
| SUEP1071_254 | 120 | 1 | 120 | 27 | EXT1071_7_suep_segment_table |
| SUEP1071_256 | 120 | 1 | 120 | 28 | EXT1071_7_suep_segment_table |
| SUEP1071_326-1 | 66 | 2 | 67 | 12 | EXT1071_7_suep_segment_table |
| SUEP1071_326-2 | 34 | 69 | 102 | 7 | EXT1071_7_suep_segment_table |
| SUEP1071_358 | 92 | 1 | 92 | 14 | EXT1071_7_suep_segment_table |
| SUEP1071_402 | 18 | 3 | 20 | 35 | EXT1071_7_suep_segment_table |
| SUEP1071_404 | 120 | 1 | 120 | 23 | EXT1071_7_suep_segment_table |
| SUEP1071_406 | 20 | 1 | 20 | 23 | EXT1071_7_suep_segment_table |
| SUEP1071_438 | 32 | 1 | 32 | 21 | EXT1071_7_suep_segment_table |
| SUEP1071_442 | 40 | 1 | 40 | 21 | EXT1071_7_suep_segment_table |
| SUEP1071_748 | 24 | 1 | 24 | 25 | EXT1071_7_suep_segment_table |
| SUEP1071_750 | 8 | 1 | 8 | 19 | EXT1071_7_suep_segment_table |

## Tau projection status
| tau_status_id | object | status | remaining_gap | claim_allowed |
| --- | --- | --- | --- | --- |
| TAU1071_0_projection_form | tau_WEP readout projection form | PARTIAL_FORM_ACQUIRED | numeric gx/gz/Sxx/Sxz arrays and exact segment masks | false |
| TAU1071_1_source_worldtube_proxy | source leg | OFFICIAL_PROXY_FORM_ACQUIRED | Earth gravity model/source profile not reconstructed inside MTS tau branch | false |
| TAU1071_2_data_portal | official data access | PUBLIC_POINTER_ACQUIRED_DIRECT_ACCESS_UNVERIFIED_OR_BLOCKED | machine-readable product schema and downloaded kernel arrays | false |
| TAU1071_3_verdict | tau_WEP numeric projection | NOT_ACQUIRED | full numeric orbit/attitude/averaging kernel or direct parent product | false |

## Nonclaim product candidate
| prediction_id | product_symbol | product_value | derivation_status | valid_for_claim |
| --- | --- | --- | --- | --- |
| PRED1071_0_WEP_kernel_skeleton_nonclaim_product | P_WEP_relative_source_weight | MISSING_NUMERIC_TAU_WEP_KERNEL_OR_DIRECT_PARENT_PRODUCT | KERNEL_SKELETON_YES_NUMERIC_PRODUCT_NO | false |

## Bound import
| bound_id | product_symbol | bound_value | bound_units | valid_for_claim |
| --- | --- | --- | --- | --- |
| BOUND1071_0_MICROSCOPE_R1_eta_source_charge | P_WEP_relative_source_weight | 2.8e-15 | dimensionless | true |

## Product runner status
| runner_id | valid_prediction_rows | valid_bound_rows | claim_allowed | expected_result |
| --- | --- | --- | --- | --- |
| APR1071_0_WEP_kernel_skeleton_product_stub | 0 | 1 | false | reject skeleton-only prediction and keep claim false |

## Product comparison rows
| comparison_id | comparison_status | pass_for_claim | issues |
| --- | --- | --- | --- |
| PRODUCT_COMPARE_NO_VALID_PREDICTIONS | not_run | false | no valid MTS alpha product prediction rows |

## Claim gates
| gate_id | claim_component | gate_pass | claim_allowed | reason |
| --- | --- | --- | --- | --- |
| CG1071_0_official_kernel_skeleton | official MICROSCOPE fit kernel skeleton | true | false | form acquired, numeric arrays absent |
| CG1071_1_suep_segment_table | 19 SUEP segment windows | true | false | segment metadata acquired but exact masks/timestamps absent |
| CG1071_2_source_worldtube | source worldtube/numeric gravity leg | false | false | only g(Osat)/T proxy form acquired |
| CG1071_3_tau_WEP_numeric | numeric tau_WEP or direct parent product | false | false | MISSING_NUMERIC_TAU_WEP_KERNEL_OR_DIRECT_PARENT_PRODUCT |
| CG1071_4_product_runner | WEP product runner | false | false | valid_prediction_rows=0 |
| CG1071_5_local_GR_WEP_claim | local-GR/WEP pass | false | false | kernel shape acquired but no MTS product score |

## Decision ledger
| decision_id | decision | evidence | consequence |
| --- | --- | --- | --- |
| DEC1071_0_kernel_skeleton_acquired | the official MICROSCOPE WEP readout kernel skeleton is acquired | KER1071_1_fit_basis; EXT1071_3_fundamental_eq6; EXT1071_4_polynomial_eq7 | the next branch can target numeric arrays, not just equations |
| DEC1071_1_segment_table_acquired | the 19 SUEP selected segments are staged as a source-backed table | P8_Y5_R10_1071_SUEP_SEGMENT_TABLE_SOURCE_BACKED.csv | future reproducibility work has a first window ledger |
| DEC1071_2_no_claim | do not claim WEP/local-GR pass | TAU1071_3_verdict; APR1071_0_WEP_kernel_skeleton_product_stub | numeric tau_WEP remains the next barrier |

## Validation
| check_id | result | detail |
| --- | --- | --- |
| V1071_0_sources_exist | pass | all cited local source paths and needles are present |
| V1071_1_external_kernel_sources | pass | official model equations recorded |
| V1071_2_data_products_recorded | pass | data product requirements recorded |
| V1071_3_portal_probe_recorded | pass | ONERA/CMSM portal probes recorded whether reachable or blocked |
| V1071_4_kernel_skeleton_acquired | pass | kernel skeleton acquired but numeric tau not acquired |
| V1071_5_suep_segments | pass | 19 SUEP segments total 1362 orbits |
| V1071_6_tau_not_acquired | pass | tau_WEP numeric verdict remains blocked |
| V1071_7_prediction_nonclaim_missing | pass | prediction row remains nonclaim and missing numeric kernel |
| V1071_8_bound_numeric | pass | bound import is positive numeric |
| V1071_9_runner_refuses | pass | runner reports no valid prediction rows and claim false |
| V1071_10_claim_gates_safe | pass | all claim gates deny WEP/local-GR claim |
| V1071_11_next_target | pass | 1072 handoff written |
| V1071_12_generated_under_post_checkpoint | pass | all generated outputs are under post-checkpoint-work |
| V1071_13_csv_parse | pass | all 1071 CSV outputs parse cleanly |
| V1071_14_formalization_untouched | pass | formalization-workbench modified-file count remains zero |
| V1071_SUMMARY | pass | official kernel skeleton and SUEP segment table acquired; numeric tau/product claim blocked |

## Next target
| next_id | next_target | objective | include | exclude |
| --- | --- | --- | --- | --- |
| NEXT1071_0_1072 | 1072-Y5-R10-MICROSCOPE-data-portal-schema-or-reconstructed-gxS-kernel.md | turn the official 1071 kernel skeleton into a numeric tau_WEP component by either acquiring the CMSM data schema/products or reconstructing gx,gz,Sxx,Sxz from sourced orbit/attitude/gravity-model inputs for at least one SUEP segment. | CMSM portal access notes; file/schema inventory; exact timestamps/masks; gx/gz/Sxx/Sxz arrays or dry-run reconstruction; segment 210 or another single SUEP pilot; refusal gates | public WEP/local-GR claim; tau=1; guessed phase; guessed masks; measured-G absorption; GitHub; formalization edits |

