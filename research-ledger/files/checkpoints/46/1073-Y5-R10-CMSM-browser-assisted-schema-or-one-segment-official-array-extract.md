# 1073 - CMSM browser-assisted schema or one-segment official array extract

## Current verdict
1073 attempted the browser-assisted CMSM route and did not obtain schema/data: the CMSM REGARDS module refused connection from this runtime. This checkpoint therefore stages the exact official-array extraction contract and keeps the WEP/local-GR product branch blocked.

## Local source register
| source_id | relative_path | exists | needle_found | note |
| --- | --- | --- | --- | --- |
| SRC1073_0_1072_next | source-intake/mts_residuals/P8_Y5_R10_1072_NEXT_TARGET.csv | true | true | 1072 handoff. |
| SRC1073_1_1072_validation | source-intake/mts_residuals/P8_Y5_BRR545_1072_VALIDATION.csv | true | true | 1072 validation summary. |
| SRC1073_2_1072_portal | source-intake/mts_residuals/P8_Y5_R10_1072_PORTAL_ROUTE_PROBE.csv | true | true | prior portal route probes. |
| SRC1073_3_1072_endpoints | source-intake/mts_residuals/P8_Y5_R10_1072_CMSM_REGARDS_API_CANDIDATE_ENDPOINTS.csv | true | true | candidate REGARDS endpoints. |
| SRC1073_4_1072_requirements | source-intake/mts_residuals/P8_Y5_R10_1072_RECONSTRUCTION_REQUIREMENTS.csv | true | true | missing reconstruction inputs. |
| SRC1073_5_1072_dry_meta | source-intake/mts_residuals/P8_Y5_R10_1072_GXS_DRY_RUN_METADATA_SEGMENT210.csv | true | true | dry-run preview metadata. |
| SRC1073_6_1072_preview | source-intake/mts_residuals/P8_Y5_R10_1072_GXS_DRY_RUN_KERNEL_PREVIEW_SEGMENT210.csv | true | true | dry-run preview columns. |
| SRC1073_7_1072_tau | source-intake/mts_residuals/P8_Y5_R10_1072_NUMERIC_TAU_STATUS.csv | true | true | numeric tau still missing. |
| SRC1073_8_local_bounds | source-intake/local_bounds/local_bound_claims.csv | true | true | MICROSCOPE WEP bound row. |

## Browser attempt ledger
| browser_id | surface | target_url | observed_title | observed_status | schema_inventory_acquired | official_array_acquired | note |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BROW1073_0_direct_cmsm_module | Codex in-app browser | https://cmsm-ds.onera.fr/user/microscope/modules/7 | This site can't be reached | ERR_CONNECTION_REFUSED | false | false | browser-facing route refused connection from this runtime; no CMSM UI schema or file inventory visible |
| BROW1073_1_dom_or_log_inspection | Codex in-app browser | https://cmsm-ds.onera.fr/user/microscope/modules/7 | not_available_after_blocked_error_state | DOM_AND_LOG_INSPECTION_NOT_AVAILABLE | false | false | after the refused connection, further DOM/log inspection was unavailable; no workaround was attempted |

## Prior API response attempts
| attempt_id | target_url | probe_status | http_status | schema_inventory_acquired | official_array_acquired | error_summary |
| --- | --- | --- | --- | --- | --- | --- |
| API1073_prior_0 | https://microscope.onera.fr/fr/publication/microscope-data-are-available | HTTP_OK | 200 | false | false |  |
| API1073_prior_1 | https://www.oca.eu/fr/microscope | BLOCKED_OR_UNREACHABLE_FROM_THIS_RUN |  | false | false | URLError: <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1032)> |
| API1073_prior_2 | https://cmsm-ds.onera.fr/user/microscope | BLOCKED_OR_UNREACHABLE_FROM_THIS_RUN |  | false | false | URLError: <urlopen error [WinError 10061] No connection could be made because the target machine actively refused it> |
| API1073_prior_3 | https://cmsm-ds.onera.fr/user/microscope/modules/7 | BLOCKED_OR_UNREACHABLE_FROM_THIS_RUN |  | false | false | URLError: <urlopen error [WinError 10061] No connection could be made because the target machine actively refused it> |
| API1073_prior_4 | https://cmsm-ds.onera.fr/api/v1/rs-access-project/datasets/search | BLOCKED_OR_UNREACHABLE_FROM_THIS_RUN |  | false | false | URLError: <urlopen error [WinError 10061] No connection could be made because the target machine actively refused it> |
| API1073_prior_5 | https://cmsm-ds.onera.fr/api/v1/rs-access-project/dataobjects/search | BLOCKED_OR_UNREACHABLE_FROM_THIS_RUN |  | false | false | URLError: <urlopen error [WinError 10061] No connection could be made because the target machine actively refused it> |
| API1073_prior_6 | https://cmsm-ds.onera.fr/api/v1/rs-access-project/dataobjects/datasets/search | BLOCKED_OR_UNREACHABLE_FROM_THIS_RUN |  | false | false | URLError: <urlopen error [WinError 10061] No connection could be made because the target machine actively refused it> |
| API1073_prior_7 | https://cmsm-ds.onera.fr/api/v1/rs-access-project/applications/microscope/modules | BLOCKED_OR_UNREACHABLE_FROM_THIS_RUN |  | false | false | URLError: <urlopen error [WinError 10061] No connection could be made because the target machine actively refused it> |

## CMSM export contract
| contract_id | required_artifact | minimum_fields | acceptance_rule | current_status |
| --- | --- | --- | --- | --- |
| CMSM1073_0_dataset_inventory | dataset/file inventory | dataset_name;product_type;file_name;download_url_or_order_id;time_coverage;sensor_unit;session_or_segment | source-backed CMSM/REGARDS export or screenshot/API response naming MICROSCOPE data products | NOT_ACQUIRED |
| CMSM1073_1_time_mask | segment 210 exact timestamps and mask | segment_id;t_utc;sample_index;mask_flag;mask_reason | must be exact exported time grid, not reconstructed from duration only | NOT_ACQUIRED |
| CMSM1073_2_acceleration_channel | corrected X-axis differential acceleration or raw+calibration products | segment_id;t_utc;Gamma_x_corr_d OR Gamma1_x/Gamma2_x plus calibration flags | must state whether channel is raw, calibrated, corrected, reconstructed, or masked | NOT_ACQUIRED |
| CMSM1073_3_attitude_rate | attitude/angular velocity/angular acceleration products | t_utc;q0;q1;q2;q3;Omega_x;Omega_y;Omega_z;Omegadot_x;Omegadot_y;Omegadot_z;frame | same timestamp grid as accelerometer or documented interpolation rule | NOT_ACQUIRED |
| CMSM1073_4_orbit_ephemeris | satellite J2000 position/velocity | t_utc;r_x;r_y;r_z;v_x;v_y;v_z;frame;units | CMSM minute-sampled orbit product or source-backed official ephemeris | NOT_ACQUIRED |
| CMSM1073_5_official_gxS_arrays | gx,gz,Sxx,Sxz arrays or inputs sufficient to reproduce them | segment_id;t_utc;gx;gz;Sxx;Sxz;frame;generation_method;source_file | official arrays or exact source-reconstruction with documented gravity model and attitude/orbit inputs | NOT_ACQUIRED |

## Official array schema contract
| column_id | column_name | units | required | source_status | replaces_1072_dry_run_column |
| --- | --- | --- | --- | --- | --- |
| ARR1073_0_segment_id | segment_id | label | true | MISSING_CMSM_EXPORT | segment |
| ARR1073_1_t_utc | t_utc | UTC timestamp | true | MISSING_EXACT_TIMESTAMPS | t_sec_from_segment_start |
| ARR1073_2_mask_flag | mask_flag | boolean_or_enum | true | MISSING_EXACT_MASKS | none |
| ARR1073_3_gx | gx | m s^-2 or documented normalized convention | true | MISSING_OFFICIAL_ARRAY | gx_unit |
| ARR1073_4_gz | gz | m s^-2 or documented normalized convention | true | MISSING_OFFICIAL_ARRAY | gz_unit |
| ARR1073_5_Sxx | Sxx | s^-2 | true | MISSING_OFFICIAL_ARRAY | Sxx_unit |
| ARR1073_6_Sxz | Sxz | s^-2 | true | MISSING_OFFICIAL_ARRAY | Sxz_unit |
| ARR1073_7_generation_method | generation_method | text | true | MISSING_PROVENANCE | source_basis |

## Extraction status
| status_id | object | status | next_action | claim_allowed |
| --- | --- | --- | --- | --- |
| EX1073_0_browser_schema | CMSM browser schema/file inventory | NOT_ACQUIRED_CONNECTION_REFUSED | open CMSM in a user-controlled normal browser/session or obtain API response from accessible network | false |
| EX1073_1_api_schema | REGARDS API schema/file inventory | NOT_ACQUIRED | supply public endpoint response, login/export, or exact query parameters | false |
| EX1073_2_official_segment210_arrays | official segment 210 gx/gz/Sxx/Sxz arrays | NOT_ACQUIRED | replace 1072 dry-run preview with source-backed official arrays | false |
| EX1073_3_tau_WEP | numeric tau_WEP | NOT_ACQUIRED | derive tau_WEP only after official arrays and MTS material/source map exist | false |

## Nonclaim product candidate
| prediction_id | product_symbol | product_value | derivation_status | valid_for_claim |
| --- | --- | --- | --- | --- |
| PRED1073_0_WEP_CMSM_extract_blocked_nonclaim_product | P_WEP_relative_source_weight | MISSING_CMSM_SCHEMA_AND_OFFICIAL_SEGMENT210_ARRAYS | EXTRACTION_BLOCKED_NO_NUMERIC_PRODUCT | false |

## Bound import
| bound_id | product_symbol | bound_value | bound_units | valid_for_claim |
| --- | --- | --- | --- | --- |
| BOUND1073_0_MICROSCOPE_R1_eta_source_charge | P_WEP_relative_source_weight | 2.8e-15 | dimensionless | true |

## Product runner status
| runner_id | valid_prediction_rows | valid_bound_rows | claim_allowed | expected_result |
| --- | --- | --- | --- | --- |
| APR1073_0_WEP_CMSM_extract_blocked_product_stub | 0 | 1 | false | reject blocked-extraction placeholder and keep claim false |

## Product comparison rows
| comparison_id | comparison_status | pass_for_claim | issues |
| --- | --- | --- | --- |
| PRODUCT_COMPARE_NO_VALID_PREDICTIONS | not_run | false | no valid MTS alpha product prediction rows |

## Claim gates
| gate_id | claim_component | gate_pass | claim_allowed | reason |
| --- | --- | --- | --- | --- |
| CG1073_0_browser_access | CMSM browser access | false | false | ERR_CONNECTION_REFUSED; schema/file inventory not visible |
| CG1073_1_schema_inventory | CMSM schema/file inventory | false | false | NOT_ACQUIRED |
| CG1073_2_official_arrays | official segment 210 gx/gz/Sxx/Sxz arrays | false | false | MISSING_OFFICIAL_ARRAYS |
| CG1073_3_product_runner | WEP product runner | false | false | valid_prediction_rows=0 |
| CG1073_4_local_GR_WEP_claim | local-GR/WEP pass | false | false | no official arrays and no MTS tau_WEP/product |

## Decision ledger
| decision_id | decision | evidence | consequence |
| --- | --- | --- | --- |
| DEC1073_0_browser_route_blocked | CMSM browser route was attempted and blocked/refused from this runtime | BROW1073_0_direct_cmsm_module | do not keep looping on CMSM from this runtime |
| DEC1073_1_contract_not_data | 1073 produces an extraction contract, not official arrays | CMSM1073_5_official_gxS_arrays; ARR1073_3_gx | future official extraction has exact acceptance columns |
| DEC1073_2_no_claim | keep WEP/local-GR branch blocked | EX1073_3_tau_WEP; APR1073_0_WEP_CMSM_extract_blocked_product_stub | next work must be user-assisted CMSM export or nonclaim surrogate reconstruction only |

## Validation
| check_id | result | detail |
| --- | --- | --- |
| V1073_0_sources_exist | pass | all cited local source paths and needles are present |
| V1073_1_browser_block_recorded | pass | browser route refusal recorded |
| V1073_2_prior_api_attempts_imported | pass | prior API attempts imported and remain nonclaim |
| V1073_3_contract_complete | pass | CMSM extraction contract covers inventory/time/mask/attitude/orbit/gxS |
| V1073_4_schema_columns | pass | official array schema contract includes required replacement columns |
| V1073_5_status_not_acquired | pass | all extraction statuses remain blocked/nonclaim |
| V1073_6_prediction_nonclaim_missing | pass | prediction row remains missing official arrays |
| V1073_7_bound_numeric | pass | bound import is positive numeric |
| V1073_8_runner_refuses | pass | runner reports no valid prediction rows and claim false |
| V1073_9_claim_gates_safe | pass | all claim gates deny WEP/local-GR claim |
| V1073_10_next_target | pass | 1074 handoff written |
| V1073_11_generated_under_post_checkpoint | pass | all generated outputs are under post-checkpoint-work |
| V1073_12_csv_parse | pass | all 1073 CSV outputs parse cleanly |
| V1073_13_formalization_untouched | pass | formalization-workbench modified-file count remains zero |
| V1073_SUMMARY | pass | CMSM browser/API extraction blocked; official array contract staged; WEP/product claim blocked |

## Next target
| next_id | next_target | objective | include | exclude |
| --- | --- | --- | --- | --- |
| NEXT1073_0_1074 | 1074-Y5-R10-user-assisted-CMSM-export-or-nonclaim-surrogate-orbit-reconstruction.md | either import a user/browser-supplied CMSM schema/file export matching the 1073 contract, or build a clearly nonclaim surrogate segment-210 orbit/gravity reconstruction to test the code path while keeping tau_WEP/product claims blocked. | user-supplied CMSM files if available; contract validation; exact required columns; surrogate route labelled nonclaim; no guessed official masks; runner refusal gates | repeating blocked CMSM browser loop; treating dry-run/surrogate arrays as official; public WEP/local-GR claim; tau=1; GitHub; formalization edits |

