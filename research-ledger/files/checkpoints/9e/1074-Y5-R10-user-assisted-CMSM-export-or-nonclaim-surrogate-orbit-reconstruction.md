# 1074 - User-assisted CMSM export or nonclaim surrogate orbit reconstruction

## Current verdict
1074 found no local user-supplied CMSM export, so it built a strictly nonclaim segment-210 surrogate orbit/gravity reconstruction. This creates physically unitful gx/gz/Sxx/Sxz plumbing for future design-matrix smoke tests, but it is not official MICROSCOPE evidence and cannot support a WEP/local-GR claim.

## Local source register
| source_id | relative_path | exists | needle_found | note |
| --- | --- | --- | --- | --- |
| SRC1074_0_1073_next | source-intake/mts_residuals/P8_Y5_R10_1073_NEXT_TARGET.csv | true | true | 1073 handoff. |
| SRC1074_1_1073_validation | source-intake/mts_residuals/P8_Y5_BRR545_1073_VALIDATION.csv | true | true | 1073 validation summary. |
| SRC1074_2_1073_browser | source-intake/mts_residuals/P8_Y5_R10_1073_BROWSER_ATTEMPT_LEDGER.csv | true | true | browser route blocked. |
| SRC1074_3_1073_contract | source-intake/mts_residuals/P8_Y5_R10_1073_CMSM_EXPORT_CONTRACT.csv | true | true | official array contract. |
| SRC1074_4_1073_schema | source-intake/mts_residuals/P8_Y5_R10_1073_OFFICIAL_ARRAY_SCHEMA_CONTRACT.csv | true | true | official array schema. |
| SRC1074_5_1073_status | source-intake/mts_residuals/P8_Y5_R10_1073_OFFICIAL_ARRAY_EXTRACT_STATUS.csv | true | true | official extraction still blocked. |
| SRC1074_6_1072_preview | source-intake/mts_residuals/P8_Y5_R10_1072_GXS_DRY_RUN_KERNEL_PREVIEW_SEGMENT210.csv | true | true | prior phase-only dry run. |
| SRC1074_7_1071_segments | source-intake/mts_residuals/P8_Y5_R10_1071_SUEP_SEGMENT_TABLE_SOURCE_BACKED.csv | true | true | segment 210 duration source row. |
| SRC1074_8_local_bounds | source-intake/local_bounds/local_bound_claims.csv | true | true | MICROSCOPE WEP bound row. |

## CMSM export inventory check
| inventory_id | search_root | exists | matching_files | contract_match_status | action_taken |
| --- | --- | --- | --- | --- | --- |
| INV1074_0_search_root | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope_cmsm | false | 0 | NO_USER_SUPPLIED_CMSM_EXPORT_FOUND | surrogate reconstruction branch selected |

## Surrogate assumptions
| assumption_id | object | value | units | source_or_reason | claim_status |
| --- | --- | --- | --- | --- | --- |
| SUR1074_0_branch_selection | branch | nonclaim surrogate orbit/gravity reconstruction | text | CMSM export absent and browser/API access blocked in 1073 | FORBIDDEN_FOR_EVIDENCE |
| SUR1074_1_orbit_period | Torb | 5946.0 | s | MICROSCOPE frequency table / 1071 kernel source row | source-backed scalar, but surrogate use only |
| SUR1074_2_orbit_radius | r_surrogate=(mu/n^2)^(1/3) | 7093751.1549701765 | m | derived from Earth monopole and Torb; not official ephemeris | surrogate_only |
| SUR1074_3_gravity_amplitude | g0=mu/r^2 | 7.921106939620683 | m s^-2 | spherical Earth monopole; not MICROSCOPE gravity model | surrogate_only |
| SUR1074_4_gradient_scale | G=mu/r^3 | 1.116631633472345e-06 | s^-2 | spherical Earth monopole gradient scale; no inertia subtraction | surrogate_only |
| SUR1074_5_readout_phase | phi=2*pi*fEP3*t | 0.00311133 | Hz | official fEP3 scalar; zero phase is guessed | FORBIDDEN_FOR_EVIDENCE |
| SUR1074_6_masks_attitude | masks/attitude/inertia | omitted_or_identity_surrogate | text | official products unavailable | FORBIDDEN_FOR_EVIDENCE |

## Surrogate grid metadata
| grid_id | segment | full_grid_samples | preview_rows_written | orbit_model | attitude_model | mask_model | claim_status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GRID1074_0_segment210_surrogate | 210 | 1189200 | 256 | circular_Earth_monopole_from_Torb | zero_phase_rotating_XZ_plane_surrogate | all_samples_unmasked_surrogate | NONCLAIM_PIPELINE_TEST_ONLY |

## Surrogate gxS preview
| row_id | sample_index | t_sec_from_segment_start | gx_surrogate_m_s2 | gz_surrogate_m_s2 | Sxx_surrogate_s2 | Sxz_surrogate_s2 | source_status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SUR1074_210_000 | 0 | 0.0 | -7.921106939621 | -0.0 | 2.233263266944690e-06 | 0.000000000000000e+00 | NOT_CMSM_NOT_OFFICIAL |
| SUR1074_210_001 | 4663 | 1165.75 | 5.529068841475 | 5.672154167082 | 5.155309707622974e-07 | 1.674400913137295e-06 | NOT_CMSM_NOT_OFFICIAL |
| SUR1074_210_002 | 9326 | 2331.5 | 0.202336700362 | -7.918522274301 | -1.114445841858667e-06 | -8.554177046948680e-08 | NOT_CMSM_NOT_OFFICIAL |
| SUR1074_210_003 | 13989 | 3497.25 | -5.811537833242 | 5.382375234198 | 6.865586869663474e-07 | -1.670030756362032e-06 | NOT_CMSM_NOT_OFFICIAL |
| SUR1074_210_004 | 18652 | 4663.0 | 7.910769965098 | 0.404541355377 | 2.224525805367441e-06 | 1.708602784306626e-07 | NOT_CMSM_NOT_OFFICIAL |
| SUR1074_210_005 | 23315 | 5828.75 | -5.232169077801 | -5.947128877888 | 3.449496338732753e-07 | 1.661301848843410e-06 | NOT_CMSM_NOT_OFFICIAL |
| SUR1074_210_006 | 27978 | 6994.5 | -0.606482005875 | 7.897855071186 | -1.096993723324387e-06 | -2.557328440863917e-07 | NOT_CMSM_NOT_OFFICIAL |
| SUR1074_210_007 | 32641 | 8160.25 | 6.078838814028 | -5.078548397129 | 8.562484302673753e-07 | -1.648236972875709e-06 | NOT_CMSM_NOT_OFFICIAL |
| SUR1074_210_008 | 37304 | 9326.0 | -7.879786020851 | -0.808026864971 | 2.198404579596894e-06 | 3.399379515411640e-07 | NOT_CMSM_NOT_OFFICIAL |
| SUR1074_210_009 | 41967 | 10491.75 | 4.921613445353 | 6.206581687485 | 1.765943713896638e-07 | 1.630870227554169e-06 | NOT_CMSM_NOT_OFFICIAL |

## Replacement map
| map_id | official_contract_column | surrogate_column | replacement_status | evidence_policy | next_action |
| --- | --- | --- | --- | --- | --- |
| MAP1074_0_gx | gx | gx_surrogate_m_s2 | SURROGATE_AVAILABLE_OFFICIAL_MISSING | cannot support claim | replace with CMSM/official gx |
| MAP1074_1_gz | gz | gz_surrogate_m_s2 | SURROGATE_AVAILABLE_OFFICIAL_MISSING | cannot support claim | replace with CMSM/official gz |
| MAP1074_2_Sxx | Sxx | Sxx_surrogate_s2 | SURROGATE_AVAILABLE_OFFICIAL_MISSING | cannot support claim | replace with CMSM/official Sxx or official reconstruction |
| MAP1074_3_Sxz | Sxz | Sxz_surrogate_s2 | SURROGATE_AVAILABLE_OFFICIAL_MISSING | cannot support claim | replace with CMSM/official Sxz or official reconstruction |
| MAP1074_4_mask | mask_flag | mask_flag_surrogate | SURROGATE_ALL_UNMASKED_OFFICIAL_MISSING | cannot support claim | replace with exact CMSM mask |

## Status ledger
| status_id | object | status | next_action | claim_allowed |
| --- | --- | --- | --- | --- |
| STAT1074_0_CMSM_export | user-assisted CMSM export | NOT_FOUND_LOCALLY | import user-supplied CMSM export if available | false |
| STAT1074_1_surrogate_orbit | surrogate segment 210 orbit/gravity preview | BUILT_NONCLAIM | wire surrogate into a nonclaim design-matrix/tau-shape smoke runner | false |
| STAT1074_2_official_arrays | official gx/gz/Sxx/Sxz arrays | NOT_ACQUIRED | replace surrogate columns with CMSM official arrays | false |
| STAT1074_3_tau_WEP | numeric tau_WEP | NOT_ACQUIRED | derive only after official arrays or explicitly nonclaim smoke-route selection | false |

## Nonclaim product candidate
| prediction_id | product_symbol | product_value | derivation_status | valid_for_claim |
| --- | --- | --- | --- | --- |
| PRED1074_0_WEP_surrogate_orbit_nonclaim_product | P_WEP_relative_source_weight | MISSING_OFFICIAL_ARRAYS_SURROGATE_ONLY | NONCLAIM_SURROGATE_PIPELINE_ONLY | false |

## Bound import
| bound_id | product_symbol | bound_value | bound_units | valid_for_claim |
| --- | --- | --- | --- | --- |
| BOUND1074_0_MICROSCOPE_R1_eta_source_charge | P_WEP_relative_source_weight | 2.8e-15 | dimensionless | true |

## Product runner status
| runner_id | valid_prediction_rows | valid_bound_rows | claim_allowed | expected_result |
| --- | --- | --- | --- | --- |
| APR1074_0_WEP_surrogate_orbit_product_stub | 0 | 1 | false | reject surrogate-only prediction and keep claim false |

## Product comparison rows
| comparison_id | comparison_status | pass_for_claim | issues |
| --- | --- | --- | --- |
| PRODUCT_COMPARE_NO_VALID_PREDICTIONS | not_run | false | no valid MTS alpha product prediction rows |

## Claim gates
| gate_id | claim_component | gate_pass | claim_allowed | reason |
| --- | --- | --- | --- | --- |
| CG1074_0_CMSM_export | user/CMSM export | false | false | NO_USER_SUPPLIED_CMSM_EXPORT_FOUND |
| CG1074_1_surrogate_preview | surrogate segment 210 gxS preview | true | false | pipeline built but not official arrays |
| CG1074_2_official_arrays | official gx/gz/Sxx/Sxz arrays | false | false | MISSING_OFFICIAL_ARRAYS |
| CG1074_3_product_runner | WEP product runner | false | false | valid_prediction_rows=0 |
| CG1074_4_local_GR_WEP_claim | local-GR/WEP pass | false | false | surrogate-only arrays and no MTS tau_WEP product |

## Decision ledger
| decision_id | decision | evidence | consequence |
| --- | --- | --- | --- |
| DEC1074_0_surrogate_branch_selected | no local CMSM export found, so select nonclaim surrogate branch | INV1074_0_search_root | test pipeline geometry without claiming evidence |
| DEC1074_1_surrogate_is_useful | surrogate gx/gz/Sxx/Sxz arrays now exist with physical units and source flags | P8_Y5_R10_1074_SURROGATE_GXS_PREVIEW_SEGMENT210.csv | next step can build a design-matrix/tau-shape smoke runner |
| DEC1074_2_no_claim | do not treat surrogate arrays as official MICROSCOPE evidence | STAT1074_3_tau_WEP; APR1074_0_WEP_surrogate_orbit_product_stub | WEP/local-GR branch remains blocked |

## Validation
| check_id | result | detail |
| --- | --- | --- |
| V1074_0_sources_exist | pass | all cited local source paths and needles are present |
| V1074_1_no_CMSM_export | pass | no local user-supplied CMSM export found |
| V1074_2_assumptions_nonclaim | pass | surrogate assumptions are nonclaim and mask/attitude gap is explicit |
| V1074_3_grid_metadata | pass | grid metadata has expected segment 210 sample count and nonclaim status |
| V1074_4_preview_rows | pass | surrogate preview rows written and flagged nonofficial |
| V1074_5_replacement_map | pass | replacement map covers official gx/gz/Sxx/Sxz/mask columns |
| V1074_6_tau_not_acquired | pass | numeric tau_WEP remains not acquired |
| V1074_7_prediction_nonclaim_missing | pass | prediction row remains missing official arrays |
| V1074_8_bound_numeric | pass | bound import is positive numeric |
| V1074_9_runner_refuses | pass | runner reports no valid prediction rows and claim false |
| V1074_10_claim_gates_safe | pass | all claim gates deny WEP/local-GR claim |
| V1074_11_next_target | pass | 1075 handoff written |
| V1074_12_generated_under_post_checkpoint | pass | all generated outputs are under post-checkpoint-work |
| V1074_13_csv_parse | pass | all 1074 CSV outputs parse cleanly |
| V1074_14_formalization_untouched | pass | formalization-workbench modified-file count remains zero |
| V1074_SUMMARY | pass | no CMSM export found; nonclaim surrogate orbit/gravity preview built; official WEP/product claim blocked |

## Next target
| next_id | next_target | objective | include | exclude |
| --- | --- | --- | --- | --- |
| NEXT1074_0_1075 | 1075-Y5-R10-surrogate-design-matrix-tau-shape-smoke-runner.md | use the 1074 nonclaim surrogate gx/gz/Sxx/Sxz arrays to build a design-matrix/tau-shape smoke runner that verifies regression plumbing and replacement gates, while refusing any WEP/local-GR claim until official arrays and the MTS material/source map exist. | segment 210 surrogate design matrix; polynomial/gx/gz/Sxx/Sxz columns; condition-number/orthogonality diagnostics; replacement gates; product-runner refusal | treating surrogate fit as MICROSCOPE evidence; official claim; tau=1; guessed masks as final; GitHub; formalization edits |

