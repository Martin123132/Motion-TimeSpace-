# 2002 - R2FR surrogate design-matrix tau-shape smoke runner

## Current verdict
2002 builds the first R2FR design-matrix/tau-shape smoke runner from the 2001 nonclaim surrogate grid. The useful result is not a WEP claim: the identifiable 8-column surrogate matrix is numerically sane, but the full 9-column matrix shows the tau-like `gxS` channel is rank-degenerate with `gx` in the simple monopole zero-phase surrogate.

Important boundary: this is a code-path and identifiability diagnostic only. It proves that surrogate polishing cannot replace official CMSM arrays or a parent material/source response derivation.

Next honest move: attack the parent material/source response map, while keeping the official CMSM import gate open.

## Local source register
| source_id | source_path | exists | anchor_found | note |
| --- | --- | --- | --- | --- |
| SRC2002_0_2001_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2001-Y5-R2FR-user-CMSM-export-or-nonclaim-surrogate-reconstruction.md | True | True | 2001 handoff and surrogate branch. |
| SRC2002_1_2001_validation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_2001_VALIDATION.csv | True | True | 2001 validation pass. |
| SRC2002_2_2001_grid | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2001_SURROGATE_GRID_METADATA_SEGMENT210.csv | True | True | 2001 surrogate grid metadata. |
| SRC2002_3_2001_thin_grid | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2001_SURROGATE_THIN_GRID_SEGMENT210_NONCLAIM.csv | True | True | 2001 nonclaim thin-grid arrays. |
| SRC2002_4_2001_replacement_map | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2001_SURROGATE_TO_OFFICIAL_REPLACEMENT_MAP.csv | True | True | surrogate-to-official replacement map. |
| SRC2002_5_2001_status | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2001_STATUS_LEDGER.csv | True | True | tau_WEP still missing. |
| SRC2002_6_local_bound | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\local_bound_claims.csv | True | True | MICROSCOPE WEP bound anchor for refusal runner. |

## Design schema
| column_id | column_name | definition | normalization | source_status |
| --- | --- | --- | --- | --- |
| DM2002_0_poly0 | poly0 | constant offset column | always present | identifiable_surrogate_design_matrix |
| DM2002_1_poly1 | poly1 | centered linear drift over segment | derived from t/T | identifiable_surrogate_design_matrix |
| DM2002_2_poly2 | poly2 | centered quadratic drift over segment | derived from t/T | identifiable_surrogate_design_matrix |
| DM2002_3_poly3 | poly3 | centered cubic drift over segment | derived from t/T | identifiable_surrogate_design_matrix |
| DM2002_4_gx_shape | gx_shape | normalized surrogate gx column | gx_surrogate_m_s2/7.921106939621 | SURROGATE_ONLY |
| DM2002_5_gz_shape | gz_shape | normalized surrogate gz column | gz_surrogate_m_s2/7.921106333633 | SURROGATE_ONLY |
| DM2002_6_Sxx_shape | Sxx_shape | normalized surrogate Sxx column | Sxx_surrogate_s2/2.23326326694469e-06 | SURROGATE_ONLY |
| DM2002_7_Sxz_shape | Sxz_shape | normalized surrogate Sxz column | Sxz_surrogate_s2/1.672006524006633e-06 | SURROGATE_ONLY |
| DM2002_8_gxS_shape | gxS_shape | normalized surrogate gxS product shape | gxS_shape_surrogate_m_s4/1.768991716179554e-05 | SURROGATE_ONLY_DEGENERATE_WITH_GX_IN_MONOPOLE_MODEL |

## Identifiable design-matrix preview
| matrix_row_id | source_row_id | sample_index | poly0 | poly1 | gx_shape | gz_shape | Sxx_shape | Sxz_shape | design_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DMROW2002_0000 | SUR2001_210_0000 | 0 | 1.000000000000000e+00 | -1.000000000000000e+00 | -1.000000000000000e+00 | -0.000000000000000e+00 | 1.000000000000000e+00 | 0.000000000000000e+00 | IDENTIFIABLE_SURROGATE_DESIGN_MATRIX_NOT_OFFICIAL |
| DMROW2002_0001 | SUR2001_210_0001 | 1162 | 1.000000000000000e+00 | -9.980457450386815e-01 | -8.229667729028166e-01 | 5.680895528670590e-01 | 5.159114639533352e-01 | -9.366822371259612e-01 | IDENTIFIABLE_SURROGATE_DESIGN_MATRIX_NOT_OFFICIAL |
| DMROW2002_0002 | SUR2001_210_0002 | 2324 | 1.000000000000000e+00 | -9.960914900773630e-01 | -3.545486186044818e-01 | 9.350376520856535e-01 | -3.114429155685176e-01 | -6.641987864886654e-01 | IDENTIFIABLE_SURROGATE_DESIGN_MATRIX_NOT_OFFICIAL |
| DMROW2002_0003 | SUR2001_210_0003 | 3486 | 1.000000000000000e+00 | -9.941372351160443e-01 | 2.394033079227351e-01 | 9.709202852923509e-01 | -4.140290842334775e-01 | 4.657007126693486e-01 | IDENTIFIABLE_SURROGATE_DESIGN_MATRIX_NOT_OFFICIAL |
| DMROW2002_0004 | SUR2001_210_0004 | 4648 | 1.000000000000000e+00 | -9.921829801547258e-01 | 7.485905540913852e-01 | 6.630326157802254e-01 | 3.405817265122068e-01 | 9.944258752087136e-01 | IDENTIFIABLE_SURROGATE_DESIGN_MATRIX_NOT_OFFICIAL |
| DMROW2002_0005 | SUR2001_210_0005 | 5810 | 1.000000000000000e+00 | -9.902287251934073e-01 | 9.927269971295506e-01 | 1.203873389837999e-01 | 9.782603362448948e-01 | 2.394439280501866e-01 | IDENTIFIABLE_SURROGATE_DESIGN_MATRIX_NOT_OFFICIAL |
| DMROW2002_0006 | SUR2001_210_0006 | 6972 | 1.000000000000000e+00 | -9.882744702320888e-01 | 8.853721123113073e-01 | -4.648830560565243e-01 | 6.758256658878682e-01 | -8.246368473618810e-01 | IDENTIFIABLE_SURROGATE_DESIGN_MATRIX_NOT_OFFICIAL |
| DMROW2002_0007 | SUR2001_210_0007 | 8134 | 1.000000000000000e+00 | -9.863202152707703e-01 | 4.645366630444784e-01 | -8.855539558239691e-01 | -1.763085330311653e-01 | -8.241916382151528e-01 | IDENTIFIABLE_SURROGATE_DESIGN_MATRIX_NOT_OFFICIAL |
| DMROW2002_0008 | SUR2001_210_0008 | 9296 | 1.000000000000000e+00 | -9.843659603094518e-01 | -1.207756353496061e-01 | -9.926799064551370e-01 | -4.781198688588473e-01 | 2.402048337728465e-01 | IDENTIFIABLE_SURROGATE_DESIGN_MATRIX_NOT_OFFICIAL |
| DMROW2002_0009 | SUR2001_210_0009 | 10458 | 1.000000000000000e+00 | -9.824117053481332e-01 | -6.633253327823903e-01 | -7.483312024579668e-01 | 1.600007456664534e-01 | 9.945202222076954e-01 | IDENTIFIABLE_SURROGATE_DESIGN_MATRIX_NOT_OFFICIAL |

## Matrix diagnostics
| diagnostic_id | matrix_id | object | value | units | interpretation |
| --- | --- | --- | --- | --- | --- |
| DIAG2002_FULL2002_shape | FULL2002 | design_matrix_shape | 1024x9 | rows x columns | matrix shape |
| DIAG2002_FULL2002_rank | FULL2002 | matrix_rank | 8 | count | full rank requires 9 |
| DIAG2002_FULL2002_condition | FULL2002 | l2_normalized_condition_number | 4.199371519048e+13 | dimensionless | smoke conditioning diagnostic only |
| DIAG2002_FULL2002_max_offdiag | FULL2002 | max_abs_gram_offdiagonal | 1.000000000000e+00 | dimensionless | column orthogonality diagnostic |
| DIAG2002_FULL2002_singular_min | FULL2002 | minimum_singular_value | 3.384852851214e-14 | dimensionless | small value flags degeneracy |
| DIAG2002_IDENT2002_shape | IDENT2002 | design_matrix_shape | 1024x8 | rows x columns | matrix shape |
| DIAG2002_IDENT2002_rank | IDENT2002 | matrix_rank | 8 | count | full rank requires 8 |
| DIAG2002_IDENT2002_condition | IDENT2002 | l2_normalized_condition_number | 4.916661605672e+00 | dimensionless | smoke conditioning diagnostic only |
| DIAG2002_IDENT2002_max_offdiag | IDENT2002 | max_abs_gram_offdiagonal | 9.165154308154e-01 | dimensionless | column orthogonality diagnostic |
| DIAG2002_IDENT2002_singular_min | IDENT2002 | minimum_singular_value | 2.889312599938e-01 | dimensionless | small value flags degeneracy |
| DIAG2002_scales | SCALES2002 | surrogate_scales | gx_scale=7.921106939621e+00; gz_scale=7.921106333633e+00; Sxx_scale=2.233263266945e-06; Sxz_scale=1.672006524007e-06; gxS_scale=1.768991716180e-05 | mixed | normalization values only; not official MICROSCOPE channels |
| DIAG2002_grid | GRID2001 | full_grid_samples | 1189200 | samples | 2001 segment-210 surrogate grid carried forward |

## gxS degeneracy audit
| degeneracy_id | left_column | right_column | slope | max_abs_residual | interpretation |
| --- | --- | --- | --- | --- | --- |
| DEG2002_0_gxS_vs_gx | gxS_shape | gx_shape | 1.000000000000040e+00 | 6.328271240363392e-14 | in the simple monopole zero-phase surrogate the tau-like gxS channel is rank-degenerate with gx, so surrogate data cannot identify a physical tau channel |

## Top surrogate correlations
| correlation_id | left_column | right_column | pearson_r | status |
| --- | --- | --- | --- | --- |
| CORR2002_gx_shape_gxS_shape | gx_shape | gxS_shape | 1.000000000000e+00 | SURROGATE_CORRELATION_ONLY |
| CORR2002_poly1_poly3 | poly1 | poly3 | 9.165154308159e-01 | SURROGATE_CORRELATION_ONLY |
| CORR2002_poly2_gz_shape | poly2 | gz_shape | 9.485407285633e-03 | SURROGATE_CORRELATION_ONLY |
| CORR2002_poly3_Sxx_shape | poly3 | Sxx_shape | -4.580544328799e-03 | SURROGATE_CORRELATION_ONLY |
| CORR2002_poly3_Sxz_shape | poly3 | Sxz_shape | 4.318357130518e-03 | SURROGATE_CORRELATION_ONLY |
| CORR2002_poly2_gxS_shape | poly2 | gxS_shape | -4.094273053502e-03 | SURROGATE_CORRELATION_ONLY |
| CORR2002_poly2_gx_shape | poly2 | gx_shape | -4.094273053501e-03 | SURROGATE_CORRELATION_ONLY |
| CORR2002_gx_shape_Sxz_shape | gx_shape | Sxz_shape | 3.398967888379e-03 | SURROGATE_CORRELATION_ONLY |
| CORR2002_Sxz_shape_gxS_shape | Sxz_shape | gxS_shape | 3.398967888376e-03 | SURROGATE_CORRELATION_ONLY |
| CORR2002_poly1_Sxx_shape | poly1 | Sxx_shape | -2.997365444894e-03 | SURROGATE_CORRELATION_ONLY |
| CORR2002_poly1_Sxz_shape | poly1 | Sxz_shape | 2.824853064427e-03 | SURROGATE_CORRELATION_ONLY |
| CORR2002_gz_shape_Sxx_shape | gz_shape | Sxx_shape | -2.592694407645e-03 | SURROGATE_CORRELATION_ONLY |

## Synthetic tau-shape smoke fit
| fit_id | column_name | true_smoke_coefficient | recovered_smoke_coefficient | abs_error | fit_status |
| --- | --- | --- | --- | --- | --- |
| FIT2002_0_poly0 | poly0 | 2.300000000000000e-01 | 2.300000000000000e-01 | 2.775557561562891e-17 | SMOKE_RECOVERY_ONLY_NOT_PHYSICAL |
| FIT2002_1_poly1 | poly1 | -7.000000000000001e-02 | -7.000000000000002e-02 | 1.387778780781446e-17 | SMOKE_RECOVERY_ONLY_NOT_PHYSICAL |
| FIT2002_2_poly2 | poly2 | 3.100000000000000e-02 | 3.100000000000006e-02 | 5.551115123125783e-17 | SMOKE_RECOVERY_ONLY_NOT_PHYSICAL |
| FIT2002_3_poly3 | poly3 | -1.400000000000000e-02 | -1.400000000000005e-02 | 4.510281037539698e-17 | SMOKE_RECOVERY_ONLY_NOT_PHYSICAL |
| FIT2002_4_gx_shape | gx_shape | 1.800000000000000e-01 | 1.799999999999995e-01 | 4.440892098500626e-16 | SMOKE_RECOVERY_ONLY_NOT_PHYSICAL |
| FIT2002_5_gz_shape | gz_shape | -1.100000000000000e-01 | -1.100000000000000e-01 | 4.163336342344337e-17 | SMOKE_RECOVERY_ONLY_NOT_PHYSICAL |
| FIT2002_6_Sxx_shape | Sxx_shape | 6.200000000000000e-02 | 6.200000000000006e-02 | 6.245004513516506e-17 | SMOKE_RECOVERY_ONLY_NOT_PHYSICAL |
| FIT2002_7_Sxz_shape | Sxz_shape | -4.700000000000000e-02 | -4.700000000000095e-02 | 9.506284648352903e-16 | SMOKE_RECOVERY_ONLY_NOT_PHYSICAL |
| FIT2002_summary | summary | synthetic_deterministic | least_squares_identifiable_matrix | 9.506284648352903e-16 | rank=8; residual_norm=2.389011491907263e-14; singular_min=4.125756773985895e+00 |

## Replacement gates
| gate_id | object | required_for_claim | current_status | runner_policy |
| --- | --- | --- | --- | --- |
| RG2002_0_official_arrays | official gx/gz/Sxx/Sxz arrays | true | MISSING_OFFICIAL_ARRAYS_SURROGATE_ONLY | block product claim |
| RG2002_1_exact_masks | exact segment masks/timestamps | true | MISSING_EXACT_MASKS_AND_UTC | block product claim |
| RG2002_2_parent_material_source_map | MTS material/source response map | true | MISSING_PARENT_MATERIAL_SOURCE_MAP | block tau_WEP interpretation |
| RG2002_3_full_gxS_identifiability | full surrogate gxS channel | true | RANK_DEGENERATE_WITH_GX_IN_MONOPOLE_SURROGATE | requires official geometry or parent source map |
| RG2002_4_identifiable_smoke_runner | identifiable surrogate design matrix | false | SMOKE_RUNNER_AVAILABLE | allowed only as pipeline diagnostic |

## Tau-shape status
| status_id | object | status | diagnostic | claim_allowed |
| --- | --- | --- | --- | --- |
| TAUSHAPE2002_0_identifiable_matrix | identifiable surrogate design matrix | AVAILABLE_NONCLAIM | condition=4.916661605672e+00 | false |
| TAUSHAPE2002_1_smoke_recovery | synthetic tau-shape coefficients | RECOVERED_IN_SMOKE_TEST | rank=8; residual_norm=2.389011491907263e-14; singular_min=4.125756773985895e+00 | false |
| TAUSHAPE2002_2_gxS_degeneracy | full surrogate gxS channel | DEGENERATE_IN_SIMPLE_SURROGATE | max_abs_residual=6.328271240363392e-14 | false |
| TAUSHAPE2002_3_physics_tau | physical tau_WEP | NOT_ACQUIRED | smoke recovery is not physical tau | false |

## Nonclaim product candidate
| prediction_id | product_symbol | product_value | derivation_status | valid_for_claim |
| --- | --- | --- | --- | --- |
| PRED2002_0_WEP_surrogate_design_matrix_tau_shape_nonclaim | P_WEP_relative_source_weight | MISSING_PHYSICAL_TAU_WEP_SURROGATE_SMOKE_ONLY | SMOKE_PLUMBING_ONLY_NO_PHYSICS_PRODUCT | false |

## Bound import
| bound_id | product_symbol | bound_value | bound_units | valid_for_claim |
| --- | --- | --- | --- | --- |
| BOUND2002_0_MICROSCOPE_R1_eta_source_charge | P_WEP_relative_source_weight | 2.8e-15 | dimensionless | true |

## Product runner status
| runner_id | valid_prediction_rows | valid_bound_rows | claim_allowed | expected_result |
| --- | --- | --- | --- | --- |
| APR2002_0_WEP_surrogate_design_matrix_product_stub | 0 | 1 | false | reject smoke-only surrogate product and keep claim false |

## Product comparison rows
| comparison_id | comparison_status | pass_for_claim | issues |
| --- | --- | --- | --- |
| PRODUCT_COMPARE_NO_VALID_PREDICTIONS | not_run | false | no valid MTS alpha product prediction rows |

## Claim gates
| gate_id | claim_component | gate_pass | claim_allowed | reason |
| --- | --- | --- | --- | --- |
| CG2002_0_design_matrix | identifiable surrogate design matrix | true | false | available but nonclaim |
| CG2002_1_tau_shape_smoke | synthetic tau-shape recovery | true | false | synthetic coefficients are not physical tau_WEP |
| CG2002_2_gxS_degeneracy | full surrogate gxS channel | false | false | rank-degenerate with gx in simple monopole surrogate |
| CG2002_3_official_arrays | official MICROSCOPE arrays | false | false | MISSING_OFFICIAL_ARRAYS |
| CG2002_4_parent_material_source_map | parent material/source map | false | false | MISSING_PARENT_MATERIAL_SOURCE_MAP |
| CG2002_5_product_runner | WEP product runner | false | false | valid_prediction_rows=0 |
| CG2002_6_local_GR_WEP_claim | local-GR/WEP pass | false | false | no physical tau_WEP product |

## Decision ledger
| decision_id | decision | evidence | consequence |
| --- | --- | --- | --- |
| DEC2002_0_runner_built | surrogate design-matrix/tau-shape smoke runner is built | identifiable_rank=8; condition=4.916661605672e+00 | pipeline can now test replacement gates and regression plumbing |
| DEC2002_1_degeneracy_found | the full surrogate gxS channel is not independently identifiable | full_rank=8; gxS_vs_gx_residual=6.328271240363392e-14 | simple monopole surrogate is useful for code plumbing but insufficient for physics tau extraction |
| DEC2002_2_best_next_route | stop polishing surrogate evidence and derive the parent material/source response map while keeping official CMSM import open | RG2002_2_parent_material_source_map; RG2002_3_full_gxS_identifiability | next work should attack the coupling/source map or replace the surrogate with official arrays |

## Validation
| validation_id | status | detail |
| --- | --- | --- |
| VAL2002_00_sources | PASS | all source paths exist and needles found |
| VAL2002_01_matrix_rows | PASS | 1024 identifiable design-matrix rows written and nonclaim |
| VAL2002_02_full_degeneracy_detected | PASS | full gxS surrogate channel rank degeneracy detected rather than hidden |
| VAL2002_03_identifiable_matrix | PASS | identifiable surrogate matrix is finite, full-rank, and well conditioned for smoke tests |
| VAL2002_04_smoke_recovery | PASS | synthetic identifiable coefficients recover to numerical tolerance |
| VAL2002_05_replacement_gates | PASS | replacement gates record gxS identifiability blocker |
| VAL2002_06_physical_tau_blocked | PASS | physical tau_WEP remains not acquired |
| VAL2002_07_prediction_nonclaim_missing | PASS | prediction row remains missing physical tau |
| VAL2002_08_product_runner_refuses | PASS | product runner refuses smoke-only surrogate prediction |
| VAL2002_09_claim_gates_safe | PASS | all claim gates deny WEP/local-GR claim |
| VAL2002_10_next_target | PASS | 2003 parent material/source map handoff written |
| VAL2002_11_generated_under_post_checkpoint | PASS | all generated outputs are under post-checkpoint-work |
| VAL2002_12_csv_parse | PASS | all 2002 CSV outputs parse cleanly |
| VAL2002_13_pycache_absent | PASS | scripts __pycache__ absent |
| VAL2002_14_formalization_untouched | PASS | formalization-workbench modified-file count remains zero |
| VAL2002_OVERALL | PASS | 2002 surrogate design-matrix/tau-shape smoke runner with explicit gxS degeneracy gate |

## Next target
| next_id | next_target | objective | include | exclude |
| --- | --- | --- | --- | --- |
| NEXT2002_0_2003 | 2003-Y5-R2FR-parent-material-source-map-or-official-CMSM-import-gate.md | derive or explicitly bound the parent material/source response map needed to turn the WEP design matrix into an MTS product, with official CMSM import kept as a parallel gate. | Ti/Pt material response owner; Earth/source leg; Xhat normalization; source-weight coupling coefficient; proof route for tau_WEP product; official-array swap gate | more surrogate polishing as evidence; tau=1; declaring gxS independent in the monopole surrogate; public WEP/local-GR claim; GitHub; formalization edits |

