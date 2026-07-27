# 1423 - CMSM export import or surrogate smoke runner

**Current verdict:** 1423 found no complete local CMSM export, so it executed only a labelled nonclaim surrogate smoke replay. The replay verifies matrix/tau-shape plumbing, but it is not MICROSCOPE evidence and it does not unlock WEP, tau, or local-GR claims.

## Source register
| source_id | source_path | path_exists | anchor | anchor_found | role | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SRC1423_0_1422_next | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1422_NEXT_TARGET.csv | True | NEXT1422_0_1423 | True | 1422 handoff naming this CMSM import or surrogate smoke runner. | False | False |
| SRC1423_1_1422_contract | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1422_LOCAL_EXPORT_CONTRACT.csv | True | EXP1422_4_verdict | True | local CMSM export contract and required files. | False | False |
| SRC1423_2_1422_validation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_1422_VALIDATION.csv | True | VAL1422_10_overall | True | 1422 validation; official schema/pilot not acquired. | False | False |
| SRC1423_3_1074_surrogate_preview | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1074_SURROGATE_GXS_PREVIEW_SEGMENT210.csv | True | SUR1074_210_000 | True | nonclaim segment-210 surrogate gx/gz/Sxx/Sxz preview. | False | False |
| SRC1423_4_1074_grid | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1074_SURROGATE_GRID_METADATA_SEGMENT210.csv | True | GRID1074_0_segment210_surrogate | True | surrogate segment-210 grid metadata. | False | False |
| SRC1423_5_1075_matrix | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1075_MATRIX_DIAGNOSTICS.csv | True | DIAG1075_0_shape | True | prior surrogate design-matrix smoke diagnostic. | False | False |
| SRC1423_6_1075_tau_fit | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1075_TAU_SHAPE_SMOKE_FIT.csv | True | FIT1075_summary | True | prior synthetic tau-shape recovery check. | False | False |

## CMSM export inventory
| inventory_id | object | absolute_path | exists | headers_seen | required_fields | missing_fields | required_fields_present | status | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| INV1423_0_root_manifest | CMSM root manifest | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope_cmsm\dataset_inventory.csv | False |  | dataset_name;product_type;file_name;time_coverage;session_or_segment | dataset_name;product_type;file_name;time_coverage;session_or_segment | False | NOT_FOUND_OR_SCHEMA_INCOMPLETE | False | False |
| INV1423_1_segment210_time_mask | segment 210 exact time grid and masks | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope_cmsm\segment210\time_mask.csv | False |  | segment_id;t_utc;sample_index;mask_flag;mask_reason | segment_id;t_utc;sample_index;mask_flag;mask_reason | False | NOT_FOUND_OR_SCHEMA_INCOMPLETE | False | False |
| INV1423_2_segment210_orbit | segment 210 orbit ephemeris | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope_cmsm\segment210\orbit.csv | False |  | t_utc;r_x;r_y;r_z;v_x;v_y;v_z;frame;units | t_utc;r_x;r_y;r_z;v_x;v_y;v_z;frame;units | False | NOT_FOUND_OR_SCHEMA_INCOMPLETE | False | False |
| INV1423_3_segment210_attitude | segment 210 attitude/rate product | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope_cmsm\segment210\attitude_rates.csv | False |  | t_utc;frame;q0;q1;q2;q3 | t_utc;frame;q0;q1;q2;q3 | False | NOT_FOUND_OR_SCHEMA_INCOMPLETE | False | False |
| INV1423_4_segment210_gxgzS | segment 210 gx/gz/Sxx/Sxz source-leg arrays | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope_cmsm\segment210\gxgzSxxSxz.csv | False |  | segment_id;t_utc;gx;gz;Sxx;Sxz;frame;generation_method;source_file | segment_id;t_utc;gx;gz;Sxx;Sxz;frame;generation_method;source_file | False | NOT_FOUND_OR_SCHEMA_INCOMPLETE | False | False |
| INV1423_5_any_local_files | any files under source-intake/microscope_cmsm | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope_cmsm | False |  | contract files from INV1423_0 through INV1423_4 | NO_LOCAL_CMSM_EXPORT_FOLDER_OR_FILES | False | local_file_count=0 | False | False |

## Official import status
| status_id | object | status | evidence | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| OFF1423_0_branch | CMSM export branch | NO_USER_SUPPLIED_CMSM_EXPORT_FOUND | INV1423_0_root_manifest;INV1423_1_segment210_time_mask;INV1423_2_segment210_orbit;INV1423_3_segment210_attitude;INV1423_4_segment210_gxgzS | False | False |
| OFF1423_1_official_arrays | gx/gz/Sxx/Sxz source-leg arrays | NOT_AVAILABLE | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope_cmsm\segment210\gxgzSxxSxz.csv | False | False |
| OFF1423_2_parent_map | MTS parent material/source response map | MISSING_PARENT_MATERIAL_SOURCE_MAP | WEP tau cannot become physical without parent-owned material/source coefficients | False | False |
| OFF1423_3_verdict | official import evidential ceiling | SURROGATE_SMOKE_BRANCH_ONLY | official arrays alone are still not local-GR/WEP evidence without parent map and bound runner | False | False |

## Official array preview
| preview_id | segment_id | t_utc | gx | gz | Sxx | Sxz | frame | source_file | source_status | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OFFPREV1423_0_no_official_rows | 210 |  |  |  |  |  |  | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope_cmsm\segment210\gxgzSxxSxz.csv | NO_OFFICIAL_CMSM_EXPORT_AVAILABLE | False | False |

## Surrogate smoke input status
| input_id | object | status | detail | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| SIN1423_0_official_override | local CMSM export | ABSENT | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope_cmsm | False | False |
| SIN1423_1_surrogate_preview | 1074 segment-210 surrogate gx/gz/Sxx/Sxz | AVAILABLE_SURROGATE_ONLY | rows=256; segment=210; claim_status=NONCLAIM_PIPELINE_TEST_ONLY | False | False |
| SIN1423_2_branch | 1423 execution branch | NO_EXPORT_SO_SURROGATE_SMOKE_ONLY | surrogate is only plumbing evidence; physical tau remains unavailable | False | False |

## Surrogate matrix diagnostics
| diagnostic_id | object | value | units | interpretation | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- |
| DIAG1423_0_branch | execution_branch | SURROGATE_SMOKE_ONLY_NONCLAIM | text | official export absent or nonclaim | False | False |
| DIAG1423_1_shape | design_matrix_shape | 256x8 | rows x columns | same column family as 1075; replayed under 1423 import gate | False | False |
| DIAG1423_2_rank | matrix_rank | 8 | count | full rank only proves smoke plumbing | False | False |
| DIAG1423_3_condition | l2_normalized_condition_number | 4.920260673516e+00 | dimensionless | not a physics likelihood | False | False |
| DIAG1423_4_max_offdiag | max_abs_gram_offdiag | 9.165244391029e-01 | dimensionless | column degeneracy smoke diagnostic | False | False |
| DIAG1423_5_grid | surrogate_grid | segment=210; samples=1189200; preview=256 | metadata | not official MICROSCOPE product | False | False |
| DIAG1423_6_scales | normalization_scales | gx_scale=7.921106939621e+00;gz_scale=7.921105213000e+00;Sxx_scale=2.233263266945e-06;Sxz_scale=1.674947085108e-06 | mixed | surrogate normalization only | False | False |

## Surrogate tau-shape fit
| fit_id | column_name | true_smoke_coefficient | recovered_smoke_coefficient | abs_error | fit_status | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| FIT1423_0_poly0 | poly0 | 0.000000000000000e+00 | -3.851859888774472e-33 | 3.851859888774472e-33 | SURROGATE_SMOKE_RECOVERY_ONLY_NOT_PHYSICAL_TAU | False | False |
| FIT1423_1_poly1 | poly1 | 0.000000000000000e+00 | 4.930380657631324e-32 | 4.930380657631324e-32 | SURROGATE_SMOKE_RECOVERY_ONLY_NOT_PHYSICAL_TAU | False | False |
| FIT1423_2_poly2 | poly2 | 0.000000000000000e+00 | -1.972152263052530e-31 | 1.972152263052530e-31 | SURROGATE_SMOKE_RECOVERY_ONLY_NOT_PHYSICAL_TAU | False | False |
| FIT1423_3_poly3 | poly3 | 0.000000000000000e+00 | 2.717216317631960e-31 | 2.717216317631960e-31 | SURROGATE_SMOKE_RECOVERY_ONLY_NOT_PHYSICAL_TAU | False | False |
| FIT1423_4_gx_shape | gx_shape | 1.000000000000000e-15 | 1.000000000000000e-15 | 0.000000000000000e+00 | SURROGATE_SMOKE_RECOVERY_ONLY_NOT_PHYSICAL_TAU | False | False |
| FIT1423_5_gz_shape | gz_shape | -2.000000000000000e-16 | -2.000000000000002e-16 | 1.972152263052530e-31 | SURROGATE_SMOKE_RECOVERY_ONLY_NOT_PHYSICAL_TAU | False | False |
| FIT1423_6_Sxx_shape | Sxx_shape | 1.500000000000000e-16 | 1.500000000000003e-16 | 2.711709361697228e-31 | SURROGATE_SMOKE_RECOVERY_ONLY_NOT_PHYSICAL_TAU | False | False |
| FIT1423_7_Sxz_shape | Sxz_shape | -7.500000000000000e-17 | -7.500000000000034e-17 | 3.451266460341927e-31 | SURROGATE_SMOKE_RECOVERY_ONLY_NOT_PHYSICAL_TAU | False | False |
| FIT1423_summary | summary | synthetic_deterministic | least_squares | 3.451266460341927e-31 | rank=8; residual_norm=5.604934277862288e-30; singular_min=2.078547259566598e+00 | False | False |

## Replacement gates
| gate_id | object | current_status | required_replacement | runner_policy | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| REP1423_0_gxgzS | gx/gz/Sxx/Sxz columns | MISSING_OFFICIAL_EXPORT | CMSM official/user-exported gxgzSxxSxz.csv with provenance and frame | surrogate columns cannot support WEP/local-GR claim | False | False |
| REP1423_1_masks | exact time masks | MISSING_EXACT_MASKS_SURROGATE_ALL_UNMASKED | time_mask.csv matching the exact segment grid | no guessed masks in claim path | False | False |
| REP1423_2_orbit_attitude | orbit and attitude/rates | MISSING_ORBIT_ATTITUDE_EXPORT | orbit.csv plus attitude_rates.csv with frames/units | surrogate circular orbit is a pipeline check only | False | False |
| REP1423_3_parent_material_map | MTS parent material/source response map | MISSING_PARENT_MATERIAL_SOURCE_MAP | parent-derived Ti/Pt/source vector coefficients | official arrays alone do not define physical tau_WEP | False | False |

## Product runner status
| runner_id | official_export_ready | surrogate_smoke_rows | valid_prediction_rows | valid_bound_rows | comparison_status | expected_result | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| APR1423_0_import_or_surrogate_product_gate | False | 256 | 0 | 0 | NOT_RUN_NO_PHYSICAL_PREDICTION | reject surrogate/import-only rows and keep claim false | False | False |

## Claim gates
| gate_id | claim_component | gate_pass | claim_allowed | reason | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| CG1423_0_CMSM_export | user-supplied CMSM export | False | False | NO_USER_SUPPLIED_CMSM_EXPORT_FOUND | False |
| CG1423_1_surrogate_smoke | surrogate design matrix replay | True | False | pipeline diagnostic only; not official MICROSCOPE evidence | False |
| CG1423_2_physical_tau | physical tau_WEP | False | False | MISSING_PARENT_MATERIAL_SOURCE_MAP_AND_OFFICIAL_BOUND_RUNNER_INPUTS | False |
| CG1423_3_local_GR_WEP_claim | local-GR/WEP pass | False | False | import/surrogate plumbing is not a derived GR reduction or WEP prediction | False |

## Decision ledger
| decision_id | decision | evidence | consequence | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| DEC1423_0_branch | use official import branch if complete; otherwise replay surrogate smoke only | CMSM export inventory incomplete or absent | nonclaim surrogate smoke runner executed | False | False |
| DEC1423_1_no_evidence_upgrade | do not promote 1074/1075 surrogate products | surrogate branch uses circular Earth monopole, guessed phase, no official masks | WEP/local-GR remains blocked | False | False |
| DEC1423_2_next_route | move to parent material/source-map derivation or wait for real CMSM export | physical tau_WEP still lacks parent-owned material/source coefficients | 1424 should attack the parent Ti/Pt/source vector map rather than polish surrogate evidence | False | False |

## Validation
| check_id | result | detail | generated_utc |
| --- | --- | --- | --- |
| VAL1423_0_sources | PASS | all cited 1422/1074/1075 source rows exist and anchors match | 2026-06-16T04:28:55.495752+00:00 |
| VAL1423_1_inventory | PASS | CMSM export inventory checked under source-intake/microscope_cmsm | 2026-06-16T04:28:55.495765+00:00 |
| VAL1423_2_official_branch | PASS | no complete local CMSM export found; surrogate branch selected | 2026-06-16T04:28:55.495768+00:00 |
| VAL1423_3_surrogate_rank | PASS | surrogate replay rank=8, columns=8 | 2026-06-16T04:28:55.495771+00:00 |
| VAL1423_4_claim_gates | PASS | all claim gates keep claim_allowed=false | 2026-06-16T04:28:55.495774+00:00 |
| VAL1423_5_csv_parse | PASS | all generated 1423 CSVs parse cleanly | 2026-06-16T04:28:55.495776+00:00 |
| VAL1423_6_formalization_untouched | PASS | formalization modified-file count since start=0 | 2026-06-16T04:28:55.495779+00:00 |
| VAL1423_7_next_target | PASS | 1424 handoff written | 2026-06-16T04:28:55.495781+00:00 |
| VAL1423_8_overall | PASS | CMSM export absent; surrogate smoke replay works; WEP/local-GR claim remains blocked | 2026-06-16T04:28:55.495786+00:00 |

## Next target
| next_id | next_target | script | objective | include | exclude | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NEXT1423_0_1424 | 1424-Y5-R10-RAB-parent-TiPt-source-vector-map-or-official-CMSM-import-lock.md | scripts/Y5_R10_RAB_parent_TiPt_source_vector_map_or_official_CMSM_import_lock.py | derive or explicitly source the parent-owned Ti/Pt material/source vector map needed to turn official MICROSCOPE arrays into a physical MTS WEP product; keep CMSM import as a locked side gate if the user supplies the export. | parent material/source map; Ti/Pt response vector; source-leg contraction convention; measured-G guard; official-import lock; no surrogate evidence upgrade | tau=1; guessed masks; circular-orbit evidence; WEP/local-GR claim; GitHub; formalization-workbench edits | False | False |
