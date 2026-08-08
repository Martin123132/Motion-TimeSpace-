# 1075 - Surrogate design-matrix tau-shape smoke runner

## Current verdict
1075 builds a working surrogate design-matrix/tau-shape smoke runner for SUEP segment 210. It verifies regression plumbing, column diagnostics, and synthetic coefficient recovery, but it still has zero WEP/local-GR evidential force because official MICROSCOPE arrays and the MTS parent material/source map remain missing.

## Local source register
| source_id | relative_path | exists | needle_found | note |
| --- | --- | --- | --- | --- |
| SRC1075_0_1074_next | source-intake/mts_residuals/P8_Y5_R10_1074_NEXT_TARGET.csv | true | true | 1074 handoff. |
| SRC1075_1_1074_validation | source-intake/mts_residuals/P8_Y5_BRR545_1074_VALIDATION.csv | true | true | 1074 validation summary. |
| SRC1075_2_1074_grid | source-intake/mts_residuals/P8_Y5_R10_1074_SURROGATE_GRID_METADATA_SEGMENT210.csv | true | true | surrogate grid metadata. |
| SRC1075_3_1074_preview | source-intake/mts_residuals/P8_Y5_R10_1074_SURROGATE_GXS_PREVIEW_SEGMENT210.csv | true | true | surrogate gxS rows. |
| SRC1075_4_1074_map | source-intake/mts_residuals/P8_Y5_R10_1074_SURROGATE_TO_OFFICIAL_REPLACEMENT_MAP.csv | true | true | surrogate-to-official replacement map. |
| SRC1075_5_1074_status | source-intake/mts_residuals/P8_Y5_R10_1074_SURROGATE_STATUS_LEDGER.csv | true | true | numeric tau still missing. |
| SRC1075_6_1073_schema | source-intake/mts_residuals/P8_Y5_R10_1073_OFFICIAL_ARRAY_SCHEMA_CONTRACT.csv | true | true | official array schema contract. |
| SRC1075_7_local_bounds | source-intake/local_bounds/local_bound_claims.csv | true | true | MICROSCOPE WEP bound row. |

## Design matrix schema
| column_id | column_name | definition | normalization | source_status |
| --- | --- | --- | --- | --- |
| DM1075_0_poly0 | poly0 | constant offset column | always present | surrogate_design_matrix |
| DM1075_1_poly1 | poly1 | centered linear drift over segment preview | derived from t/T | surrogate_design_matrix |
| DM1075_2_poly2 | poly2 | centered quadratic drift over segment preview | derived from t/T | surrogate_design_matrix |
| DM1075_3_poly3 | poly3 | centered cubic drift over segment preview | derived from t/T | surrogate_design_matrix |
| DM1075_4_gx_shape | gx_shape | normalized surrogate gx column | gx_surrogate_m_s2/7.921106939621 | SURROGATE_ONLY |
| DM1075_5_gz_shape | gz_shape | normalized surrogate gz column | gz_surrogate_m_s2/7.921105213 | SURROGATE_ONLY |
| DM1075_6_Sxx_shape | Sxx_shape | normalized surrogate Sxx column | Sxx_surrogate_s2/2.23326326694469e-06 | SURROGATE_ONLY |
| DM1075_7_Sxz_shape | Sxz_shape | normalized surrogate Sxz column | Sxz_surrogate_s2/1.674947085108068e-06 | SURROGATE_ONLY |

## Matrix diagnostics
| diagnostic_id | object | value | units | interpretation |
| --- | --- | --- | --- | --- |
| DIAG1075_0_shape | design_matrix | 256x8 | rows x columns | surrogate preview design matrix shape |
| DIAG1075_1_rank | matrix_rank | 8 | count | full rank if rank equals 8 |
| DIAG1075_2_condition_number | l2_normalized_condition_number | 4.920260673516e+00 | dimensionless | smoke diagnostic only; large values flag column degeneracy |
| DIAG1075_3_max_abs_offdiag | max_abs_gram_offdiagonal | 9.165244391029e-01 | dimensionless | orthogonality smoke check after l2 column normalization |
| DIAG1075_4_surrogate_scale_g | gx_gz_scales | gx=7.921106939621e+00; gz=7.921105213000e+00 | m s^-2 | surrogate normalization values, not official MICROSCOPE channels |
| DIAG1075_5_grid_source | full_grid_samples | 1189200 | samples | 1074 segment-210 surrogate full-grid sample count carried forward |

## Top column correlations
| correlation_id | left_column | right_column | pearson_r | abs_pearson_r |
| --- | --- | --- | --- | --- |
| CORR1075_poly1_poly3 | poly1 | poly3 | 9.165244391042e-01 | 9.165244391042e-01 |
| CORR1075_poly3_Sxz_shape | poly3 | Sxz_shape | -1.584634823674e-02 | 1.584634823674e-02 |
| CORR1075_poly2_gx_shape | poly2 | gx_shape | -1.263616134046e-02 | 1.263616134046e-02 |
| CORR1075_poly3_Sxx_shape | poly3 | Sxx_shape | -1.254656390746e-02 | 1.254656390746e-02 |
| CORR1075_poly1_Sxz_shape | poly1 | Sxz_shape | -1.038525151973e-02 | 1.038525151973e-02 |
| CORR1075_gx_shape_Sxz_shape | gx_shape | Sxz_shape | 1.025300627709e-02 | 1.025300627709e-02 |
| CORR1075_gx_shape_Sxx_shape | gx_shape | Sxx_shape | -9.623169745480e-03 | 9.623169745480e-03 |
| CORR1075_poly1_Sxx_shape | poly1 | Sxx_shape | -8.222127739995e-03 | 8.222127739995e-03 |
| CORR1075_gz_shape_Sxx_shape | gz_shape | Sxx_shape | 7.476703549377e-03 | 7.476703549377e-03 |
| CORR1075_poly2_gz_shape | poly2 | gz_shape | 4.399985912266e-03 | 4.399985912266e-03 |

## Tau-shape smoke fit
| fit_id | column_name | true_smoke_coefficient | recovered_smoke_coefficient | abs_error | fit_status |
| --- | --- | --- | --- | --- | --- |
| FIT1075_0_poly0 | poly0 | 0.000000000000000e+00 | -3.851859888774472e-33 | 3.851859888774472e-33 | SMOKE_RECOVERY_ONLY_NOT_PHYSICAL |
| FIT1075_1_poly1 | poly1 | 0.000000000000000e+00 | 4.930380657631324e-32 | 4.930380657631324e-32 | SMOKE_RECOVERY_ONLY_NOT_PHYSICAL |
| FIT1075_2_poly2 | poly2 | 0.000000000000000e+00 | -1.972152263052530e-31 | 1.972152263052530e-31 | SMOKE_RECOVERY_ONLY_NOT_PHYSICAL |
| FIT1075_3_poly3 | poly3 | 0.000000000000000e+00 | 2.717216317631960e-31 | 2.717216317631960e-31 | SMOKE_RECOVERY_ONLY_NOT_PHYSICAL |
| FIT1075_4_gx_shape | gx_shape | 1.000000000000000e-15 | 1.000000000000000e-15 | 0.000000000000000e+00 | SMOKE_RECOVERY_ONLY_NOT_PHYSICAL |
| FIT1075_5_gz_shape | gz_shape | -2.000000000000000e-16 | -2.000000000000002e-16 | 1.972152263052530e-31 | SMOKE_RECOVERY_ONLY_NOT_PHYSICAL |
| FIT1075_6_Sxx_shape | Sxx_shape | 1.500000000000000e-16 | 1.500000000000003e-16 | 2.711709361697228e-31 | SMOKE_RECOVERY_ONLY_NOT_PHYSICAL |
| FIT1075_7_Sxz_shape | Sxz_shape | -7.500000000000000e-17 | -7.500000000000034e-17 | 3.451266460341927e-31 | SMOKE_RECOVERY_ONLY_NOT_PHYSICAL |
| FIT1075_summary | summary | synthetic_deterministic | least_squares | 3.451266460341927e-31 | rank=8; residual_norm=5.604934277862288e-30; singular_min=2.078547259566598e+00 |

## Design matrix preview
| matrix_row_id | sample_index | poly0 | poly1 | gx_shape | gz_shape | Sxx_shape | Sxz_shape |
| --- | --- | --- | --- | --- | --- | --- | --- |
| DMROW1075_000 | 0 | 1.000000000000000e+00 | -1.000000000000000e+00 | -1.000000000000000e+00 | -0.000000000000000e+00 | 1.000000000000000e+00 | 0.000000000000000e+00 |
| DMROW1075_001 | 4663 | 1.000000000000000e+00 | -9.921577531113354e-01 | 6.980171942659759e-01 | 7.160811546566690e-01 | 2.308420052363962e-01 | 9.996739168803427e-01 |
| DMROW1075_002 | 9326 | 1.000000000000000e+00 | -9.843155062226707e-01 | 2.554399301818808e-02 | -9.996739168803414e-01 | -4.990212566310337e-01 | -5.107132710641282e-02 |
| DMROW1075_003 | 13989 | 1.000000000000000e+00 | -9.764732593340061e-01 | -7.336774869397312e-01 | 6.794980106266644e-01 | 3.074239822632389e-01 | -9.970647856342765e-01 |
| DMROW1075_004 | 18652 | 1.000000000000000e+00 | -9.686310124453414e-01 | 9.986950088413408e-01 | 5.107132710635793e-02 | 9.960875810270221e-01 | 1.020093589521598e-01 |
| DMROW1075_005 | 23315 | 1.000000000000000e+00 | -9.607887655566768e-01 | -6.605350890580632e-01 | -7.507953395351523e-01 | 1.544599058154027e-01 | 9.918533329285578e-01 |
| DMROW1075_006 | 27978 | 1.000000000000000e+00 | -9.529465186680122e-01 | -7.656530968435811e-02 | 9.970647856342266e-01 | -4.912066300294167e-01 | -1.526811481748343e-01 |
| DMROW1075_007 | 32641 | 1.000000000000000e+00 | -9.451042717793474e-01 | 7.674228943459831e-01 | -6.411413888044515e-01 | 3.834068481495252e-01 | -9.840531605626004e-01 |

## Replacement gates
| gate_id | object | current_status | runner_policy |
| --- | --- | --- | --- |
| RG1075_0_official_arrays | official gx/gz/Sxx/Sxz arrays | MISSING_OFFICIAL_ARRAYS_SURROGATE_ONLY | block product claim |
| RG1075_1_exact_masks | exact segment masks | MISSING_EXACT_MASKS_SURROGATE_ALL_UNMASKED | block product claim |
| RG1075_2_material_source_map | MTS material/source response map | MISSING_PARENT_MATERIAL_SOURCE_MAP | block tau_WEP interpretation |
| RG1075_3_design_matrix_plumbing | surrogate design-matrix plumbing | SMOKE_RUNNER_AVAILABLE | allowed only as pipeline diagnostic |
| RG1075_4_tau_shape | tau-shape smoke fit | SYNTHETIC_RECOVERY_ONLY | does not define tau_WEP |

## Tau-shape status
| status_id | object | status | diagnostic | claim_allowed |
| --- | --- | --- | --- | --- |
| TAUSHAPE1075_0_matrix_available | surrogate design matrix | AVAILABLE_NONCLAIM | condition=4.920260673516e+00 | false |
| TAUSHAPE1075_1_smoke_recovery | synthetic tau-shape coefficients | RECOVERED_IN_SMOKE_TEST | rank=8; residual_norm=5.604934277862288e-30; singular_min=2.078547259566598e+00 | false |
| TAUSHAPE1075_2_physics_tau | physical tau_WEP | NOT_ACQUIRED | smoke recovery is not physical tau | false |

## Nonclaim product candidate
| prediction_id | product_symbol | product_value | derivation_status | valid_for_claim |
| --- | --- | --- | --- | --- |
| PRED1075_0_WEP_surrogate_design_matrix_tau_shape_nonclaim | P_WEP_relative_source_weight | MISSING_PHYSICAL_TAU_WEP_SURROGATE_SMOKE_ONLY | SMOKE_PLUMBING_ONLY_NO_PHYSICS_PRODUCT | false |

## Bound import
| bound_id | product_symbol | bound_value | bound_units | valid_for_claim |
| --- | --- | --- | --- | --- |
| BOUND1075_0_MICROSCOPE_R1_eta_source_charge | P_WEP_relative_source_weight | 2.8e-15 | dimensionless | true |

## Product runner status
| runner_id | valid_prediction_rows | valid_bound_rows | claim_allowed | expected_result |
| --- | --- | --- | --- | --- |
| APR1075_0_WEP_surrogate_design_matrix_product_stub | 0 | 1 | false | reject smoke-only surrogate product and keep claim false |

## Product comparison rows
| comparison_id | comparison_status | pass_for_claim | issues |
| --- | --- | --- | --- |
| PRODUCT_COMPARE_NO_VALID_PREDICTIONS | not_run | false | no valid MTS alpha product prediction rows |

## Claim gates
| gate_id | claim_component | gate_pass | claim_allowed | reason |
| --- | --- | --- | --- | --- |
| CG1075_0_design_matrix_smoke | surrogate design matrix | true | false | pipeline diagnostic only |
| CG1075_1_tau_shape_smoke | synthetic tau-shape recovery | true | false | synthetic coefficients are not physical tau_WEP |
| CG1075_2_official_arrays | official MICROSCOPE arrays | false | false | MISSING_OFFICIAL_ARRAYS |
| CG1075_3_parent_material_source_map | parent material/source map | false | false | MISSING_PARENT_MATERIAL_SOURCE_MAP |
| CG1075_4_product_runner | WEP product runner | false | false | valid_prediction_rows=0 |

## Decision ledger
| decision_id | decision | evidence | consequence |
| --- | --- | --- | --- |
| DEC1075_0_runner_built | surrogate design-matrix/tau-shape smoke runner is built | rank=8; condition=4.920260673516e+00 | pipeline can now test replacement gates and regression plumbing |
| DEC1075_1_not_evidence | do not use surrogate smoke fit as MICROSCOPE evidence | RG1075_0_official_arrays; RG1075_2_material_source_map | official-array and parent-map gates remain hard blockers |
| DEC1075_2_next_route | next best route is parent material/source map derivation or official CMSM import | TAUSHAPE1075_2_physics_tau | derive WEP coupling owner rather than polishing surrogate evidence |

## Validation
| check_id | result | detail |
| --- | --- | --- |
| V1075_0_sources_exist | pass | all cited local source paths and needles are present |
| V1075_1_schema_complete | pass | design schema has all expected columns |
| V1075_2_matrix_rows | pass | 256 surrogate design-matrix rows written and nonclaim |
| V1075_3_rank_condition | pass | design matrix is finite and full-rank for smoke purposes |
| V1075_4_correlations | pass | all non-constant column pair correlations written |
| V1075_5_smoke_recovery | pass | synthetic coefficient recovery works but remains nonclaim |
| V1075_6_replacement_gates | pass | official-array replacement gate remains closed |
| V1075_7_physical_tau_blocked | pass | physical tau_WEP remains not acquired |
| V1075_8_prediction_nonclaim_missing | pass | prediction row remains missing physical tau |
| V1075_9_bound_numeric | pass | bound import is positive numeric |
| V1075_10_runner_refuses | pass | runner reports no valid prediction rows and claim false |
| V1075_11_claim_gates_safe | pass | all claim gates deny WEP/local-GR claim |
| V1075_12_next_target | pass | 1076 handoff written |
| V1075_13_generated_under_post_checkpoint | pass | all generated outputs are under post-checkpoint-work |
| V1075_14_csv_parse | pass | all 1075 CSV outputs parse cleanly |
| V1075_15_formalization_untouched | pass | formalization-workbench modified-file count remains zero |
| V1075_SUMMARY | pass | surrogate design-matrix/tau-shape smoke runner built; physical WEP/product claim blocked |

## Next target
| next_id | next_target | objective | include | exclude |
| --- | --- | --- | --- | --- |
| NEXT1075_0_1076 | 1076-Y5-R10-WEP-parent-material-source-map-or-official-CMSM-import-gate.md | try to derive the parent material/source response map needed to turn the WEP design matrix into an MTS product, while keeping an alternative gate open for official CMSM array import if the data become available. | Ti/Pt material response owner; Earth/source leg; Xhat normalization; coupling coefficient ownership; official-array import gate; product-runner refusal | more surrogate polishing as evidence; tau=1; Delta_w=0 by taste; measured-G absorption; public WEP/local-GR claim; GitHub; formalization edits |

