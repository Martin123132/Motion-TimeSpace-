# 2781 - Y5 R2/f(R): Surrogate Design-Matrix Tau-Shape Smoke Runner Under AX1090

## Private Verdict

2781 builds the surrogate MICROSCOPE design-matrix/tau-shape smoke runner in the live R2/f(R) branch. The matrix is full-rank, synthetic coefficient recovery works, and the replacement gates are explicit. This is useful plumbing, not evidence: official MICROSCOPE arrays, exact masks, and the parent material/source map are still missing, so WEP/local-GR claims remain blocked.

## Source Register

| row_id | source_key | source_path | exists | needle_found | source_role | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| SRC2781_00_2780_next | 2780_next | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_2780_NEXT_TARGET.csv | True | True | current handoff into surrogate design-matrix smoke runner | False |
| SRC2781_01_2780_validation | 2780_validation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_2780_VALIDATION.csv | True | True | current validation baseline | False |
| SRC2781_02_2780_grid | 2780_grid | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_2780_SURROGATE_GRID_METADATA_SEGMENT210.csv | True | True | current surrogate grid metadata | False |
| SRC2781_03_2780_preview | 2780_preview | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_2780_SURROGATE_GXS_PREVIEW_SEGMENT210.csv | True | True | current surrogate gxS rows | False |
| SRC2781_04_2780_replacement | 2780_replacement | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_2780_SURROGATE_TO_OFFICIAL_REPLACEMENT_MAP.csv | True | True | current replacement map | False |
| SRC2781_05_2780_status | 2780_status | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_2780_SURROGATE_STATUS_LEDGER.csv | True | True | current physical tau blocker | False |
| SRC2781_06_2779_array_contract | 2779_array_contract | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_2779_OFFICIAL_ARRAY_SCHEMA_CONTRACT.csv | True | True | current official-array schema contract | False |
| SRC2781_07_1075_doc | 1075_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1075-Y5-R10-surrogate-design-matrix-tau-shape-smoke-runner.md | True | True | R10 precedent for design matrix diagnostics | False |
| SRC2781_08_1076_next | 1076_next | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1076_NEXT_TARGET.csv | True | True | R10 precedent for next parent coupling-owner route | False |
| SRC2781_09_local_bounds | local_bounds | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\local_bound_claims.csv | True | True | local MICROSCOPE WEP bound source row | False |

## Design Matrix Schema

| column_id | column_name | definition | normalization | source_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| DM2781_0_poly0 | poly0 | constant offset column | always present | surrogate_design_matrix | False |
| DM2781_1_poly1 | poly1 | centered linear drift over segment preview | x in [-1,1] from preview row order | surrogate_design_matrix | False |
| DM2781_2_poly2 | poly2 | centered quadratic drift over segment preview | x^2 | surrogate_design_matrix | False |
| DM2781_3_poly3 | poly3 | centered cubic drift over segment preview | x^3 | surrogate_design_matrix | False |
| DM2781_4_gx_shape | gx_shape | normalized surrogate gx column | gx_surrogate_m_s2/max_abs_gx | SURROGATE_ONLY | False |
| DM2781_5_gz_shape | gz_shape | normalized surrogate gz column | gz_surrogate_m_s2/max_abs_gz | SURROGATE_ONLY | False |
| DM2781_6_Sxx_shape | Sxx_shape | normalized surrogate Sxx column | Sxx_surrogate_s2/max_abs_Sxx | SURROGATE_ONLY | False |
| DM2781_7_Sxz_shape | Sxz_shape | normalized surrogate Sxz column | Sxz_surrogate_s2/max_abs_Sxz | SURROGATE_ONLY | False |

## Matrix Diagnostics

| diagnostic_id | object | value | units | interpretation | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| DIAG2781_0_shape | design_matrix | 256x8 | rows x columns | surrogate preview design matrix shape | False |
| DIAG2781_1_rank | matrix_rank | 8 | count | full rank if rank equals 8 | False |
| DIAG2781_2_condition_number | l2_normalized_condition_number | 4.793093383308e+00 | dimensionless | smoke diagnostic only; large values flag column degeneracy | False |
| DIAG2781_3_max_abs_offdiag | max_abs_gram_offdiagonal | 9.165244625498e-01 | dimensionless | orthogonality smoke check after l2 column normalization | False |
| DIAG2781_4_surrogate_scale_g | gx_gz_scales | gx=7.921106939621e+00; gz=7.921105213000e+00 | m s^-2 | surrogate normalization values, not official MICROSCOPE channels | False |
| DIAG2781_5_surrogate_scale_S | Sxx_Sxz_scales | Sxx=2.233263266945e-06; Sxz=1.674947085108e-06 | s^-2 | surrogate gradient normalization values | False |

## Top Column Correlations

| correlation_id | left_column | right_column | pearson_r | abs_pearson_r | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| CORR2781_poly1_poly3 | poly1 | poly3 | 9.165244625498e-01 | 9.165244625498e-01 | False |
| CORR2781_poly3_Sxz_shape | poly3 | Sxz_shape | -1.584674853222e-02 | 1.584674853222e-02 | False |
| CORR2781_poly2_gx_shape | poly2 | gx_shape | -1.263625597552e-02 | 1.263625597552e-02 | False |
| CORR2781_poly3_Sxx_shape | poly3 | Sxx_shape | -1.254606019390e-02 | 1.254606019390e-02 | False |
| CORR2781_poly1_Sxz_shape | poly1 | Sxz_shape | -1.038525151974e-02 | 1.038525151974e-02 | False |
| CORR2781_gx_shape_Sxz_shape | gx_shape | Sxz_shape | 1.025300627708e-02 | 1.025300627708e-02 | False |
| CORR2781_gx_shape_Sxx_shape | gx_shape | Sxx_shape | -9.623169745491e-03 | 9.623169745491e-03 | False |
| CORR2781_poly1_Sxx_shape | poly1 | Sxx_shape | -8.222127739992e-03 | 8.222127739992e-03 | False |
| CORR2781_gz_shape_Sxx_shape | gz_shape | Sxx_shape | 7.476703549373e-03 | 7.476703549373e-03 | False |
| CORR2781_poly2_gz_shape | poly2 | gz_shape | 4.399717731650e-03 | 4.399717731650e-03 | False |

## Tau-Shape Smoke Fit

| fit_id | column_name | true_smoke_coefficient | recovered_smoke_coefficient | abs_error | fit_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| FIT2781_0_poly0 | poly0 | 0.000000000000000e+00 | -2.049189460828019e-31 | 2.049189460828019e-31 | SMOKE_RECOVERY_ONLY_NOT_PHYSICAL | False |
| FIT2781_1_poly1 | poly1 | 0.000000000000000e+00 | -4.190823558986625e-31 | 4.190823558986625e-31 | SMOKE_RECOVERY_ONLY_NOT_PHYSICAL | False |
| FIT2781_2_poly2 | poly2 | 0.000000000000000e+00 | 3.990526844770353e-31 | 3.990526844770353e-31 | SMOKE_RECOVERY_ONLY_NOT_PHYSICAL | False |
| FIT2781_3_poly3 | poly3 | 0.000000000000000e+00 | -2.556739301389203e-31 | 2.556739301389203e-31 | SMOKE_RECOVERY_ONLY_NOT_PHYSICAL | False |
| FIT2781_4_gx_shape | gx_shape | 1.000000000000000e-15 | 1.000000000000000e-15 | 3.944304526105059e-31 | SMOKE_RECOVERY_ONLY_NOT_PHYSICAL | False |
| FIT2781_5_gz_shape | gz_shape | -2.000000000000000e-16 | -2.000000000000002e-16 | 2.465190328815662e-31 | SMOKE_RECOVERY_ONLY_NOT_PHYSICAL | False |
| FIT2781_6_Sxx_shape | Sxx_shape | 1.500000000000000e-16 | 1.500000000000005e-16 | 4.930380657631324e-31 | SMOKE_RECOVERY_ONLY_NOT_PHYSICAL | False |
| FIT2781_7_Sxz_shape | Sxz_shape | -7.500000000000000e-17 | -7.500000000000036e-17 | 3.574525976782710e-31 | SMOKE_RECOVERY_ONLY_NOT_PHYSICAL | False |
| FIT2781_summary | summary | synthetic_deterministic | least_squares | 4.930380657631324e-31 | rank=8; residual_norm=1.029865531073714e-29; singular_min=2.079123900629017e+00 | False |

## Design Matrix Preview

| matrix_row_id | sample_index | poly0 | poly1 | gx_shape | gz_shape | Sxx_shape | Sxz_shape | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DMROW2781_000 | 0 | 1.000000000000000e+00 | -1.000000000000000e+00 | -1.000000000000000e+00 | -0.000000000000000e+00 | 1.000000000000000e+00 | 0.000000000000000e+00 | False |
| DMROW2781_001 | 4663 | 1.000000000000000e+00 | -9.921568627450981e-01 | 6.980171942659759e-01 | 7.160811546566690e-01 | -2.554399301813973e-02 | 9.996739168803427e-01 | False |
| DMROW2781_002 | 9326 | 1.000000000000000e+00 | -9.843137254901961e-01 | 2.554399301818808e-02 | -9.996739168803414e-01 | -9.986950088413783e-01 | -5.107132710641624e-02 | False |
| DMROW2781_003 | 13989 | 1.000000000000000e+00 | -9.764705882352941e-01 | -7.336774869397312e-01 | 6.794980106266644e-01 | 7.656530968432350e-02 | -9.970647856342765e-01 | False |
| DMROW2781_004 | 18652 | 1.000000000000000e+00 | -9.686274509803922e-01 | 9.986950088413408e-01 | 5.107132710635793e-02 | 9.947834413693620e-01 | 1.020093589521666e-01 | False |
| DMROW2781_005 | 23315 | 1.000000000000000e+00 | -9.607843137254902e-01 | -6.605350890580632e-01 | -7.507953395351523e-01 | -1.273867922461386e-01 | 9.918533329285567e-01 | False |
| DMROW2781_006 | 27978 | 1.000000000000000e+00 | -9.529411764705882e-01 | -7.656530968435811e-02 | 9.970647856342266e-01 | -9.882755067058874e-01 | -1.526811481748444e-01 | False |
| DMROW2781_007 | 32641 | 1.000000000000000e+00 | -9.450980392156862e-01 | 7.674228943459831e-01 | -6.411413888044515e-01 | 1.778757975327123e-01 | -9.840531605625986e-01 | False |

_Only the first 8 of 256 design rows are shown here; the full CSV is written separately._

## Replacement Gates

| gate_id | object | required_for_claim | current_status | runner_policy | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| RG2781_0_official_arrays | official gx/gz/Sxx/Sxz arrays | True | MISSING_OFFICIAL_ARRAYS_SURROGATE_ONLY | block product claim | False |
| RG2781_1_exact_masks | exact segment masks | True | MISSING_EXACT_MASKS_SURROGATE_ALL_UNMASKED | block product claim | False |
| RG2781_2_material_source_map | MTS material/source response map | True | MISSING_PARENT_MATERIAL_SOURCE_MAP | block tau_WEP interpretation | False |
| RG2781_3_design_matrix_plumbing | surrogate design-matrix plumbing | False | SMOKE_RUNNER_AVAILABLE | allowed only as pipeline diagnostic | False |
| RG2781_4_tau_shape | tau-shape smoke fit | False | SYNTHETIC_RECOVERY_ONLY | does not define tau_WEP | False |

## Tau-Shape Status

| status_id | object | status | diagnostic | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| TAUSHAPE2781_0_matrix_available | surrogate design matrix | AVAILABLE_NONCLAIM | condition=4.793093383308e+00 | False | False |
| TAUSHAPE2781_1_smoke_recovery | synthetic tau-shape coefficients | RECOVERED_IN_SMOKE_TEST | rank=8; residual_norm=1.029865531073714e-29; singular_min=2.079123900629017e+00 | False | False |
| TAUSHAPE2781_2_physics_tau | physical tau_WEP | NOT_ACQUIRED | smoke recovery is not physical tau | False | False |

## Nonclaim Product Candidate

| prediction_id | arena | product_symbol | product_value | product_units | derivation_status | notes | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| PRED2781_0_WEP_surrogate_design_matrix_tau_shape_nonclaim | MICROSCOPE_WEP | P_WEP_relative_source_weight | MISSING_PHYSICAL_TAU_WEP_SURROGATE_SMOKE_ONLY | dimensionless | SMOKE_PLUMBING_ONLY_NO_PHYSICS_PRODUCT | synthetic recovery verifies matrix plumbing only; it is not official MICROSCOPE evidence and not an MTS tau_WEP prediction | False |

## Bound Import

| bound_id | arena | product_symbol | bound_value | bound_units | bound_type | source_row_id | bound_valid_for_internal_runner | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BOUND2781_0_MICROSCOPE_R1_eta_source_charge | MICROSCOPE_WEP | P_WEP_relative_source_weight | 2.8e-15 | dimensionless | source_backed_upper_bound_anchor | R1_WEP_source_charge | True | False |

## Product Runner Status

| runner_id | prediction_rows | bound_rows | valid_prediction_rows | valid_bound_rows | claim_allowed | expected_result | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| APR2781_0_WEP_surrogate_design_matrix_product_stub | 1 | 1 | 0 | 1 | False | reject smoke-only surrogate product and keep claim false | False |

## Product Comparison Rows

| comparison_id | comparison_status | pass_for_claim | issues | valid_for_claim |
| --- | --- | --- | --- | --- |
| PRODUCT_COMPARE_NO_VALID_PREDICTIONS | not_run | False | no valid MTS tau_WEP/direct-product prediction rows | False |

## Claim Gates

| gate_id | claim_component | gate_pass | claim_allowed | reason | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| CG2781_0_design_matrix_smoke | surrogate design matrix | True | False | pipeline diagnostic only | False |
| CG2781_1_tau_shape_smoke | synthetic tau-shape recovery | True | False | synthetic coefficients are not physical tau_WEP | False |
| CG2781_2_official_arrays | official MICROSCOPE arrays | False | False | MISSING_OFFICIAL_ARRAYS | False |
| CG2781_3_parent_material_source_map | parent material/source map | False | False | MISSING_PARENT_MATERIAL_SOURCE_MAP | False |
| CG2781_4_product_runner | WEP product runner | False | False | valid_prediction_rows=0 | False |

## Decision Ledger

| decision_id | decision | evidence | consequence | valid_for_claim |
| --- | --- | --- | --- | --- |
| DEC2781_0_runner_built | surrogate design-matrix/tau-shape smoke runner is built in the R2/f(R) branch | rank=8; condition=4.793093383308e+00 | pipeline can now test replacement gates and regression plumbing | False |
| DEC2781_1_not_evidence | do not use surrogate smoke fit as MICROSCOPE evidence | RG2781_0_official_arrays; RG2781_2_material_source_map | official-array and parent-map gates remain hard blockers | False |
| DEC2781_2_next_route | next best route is parent material/source coupling-owner theorem or official CMSM import | TAUSHAPE2781_2_physics_tau | derive WEP coupling owner rather than polishing surrogate evidence | False |

## Next Target

| row_id | next_target | script | objective | include | exclude | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| NEXT2781_0_2782 | 2782-Y5-R2FR-WEP-parent-material-source-map-or-official-CMSM-import-gate-under-AX1090.md | scripts/Y5_R2FR_WEP_parent_material_source_map_or_official_CMSM_import_gate_under_AX1090_2782.py | try to derive the parent material/source response map needed to turn the WEP design matrix into an MTS product, while keeping an alternative gate open for official CMSM array import if the data become available | Ti/Pt material response owner; Earth/source leg; Xhat normalization; coupling coefficient ownership; official-array import gate; product-runner refusal | more surrogate polishing as evidence; tau=1; Delta_w=0 by taste; measured-G absorption; public WEP/local-GR claim; GitHub; formalization edits | False |

## Branch Copies

| copy_id | table_key | source_table | copy_path | purpose | exists | row_count | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BR2781_0_matrix_queue | matrix | source-intake\mts_residuals\P8_Y5_R2FR_2781_MATRIX_DIAGNOSTICS.csv | source-intake\rab-sector\acquisition-queue\JR2781_SURROGATE_DESIGN_MATRIX_DIAGNOSTICS_NONCLAIM.csv | surrogate design-matrix diagnostics nonclaim copy | True | 49 | False |
| BR2781_1_gate_queue | gates | source-intake\mts_residuals\P8_Y5_R2FR_2781_REPLACEMENT_GATES.csv | source-intake\rab-sector\acquisition-queue\JR2781_REPLACEMENT_AND_PARENT_GATES_NONCLAIM.csv | replacement and parent gates nonclaim copy | True | 14 | False |
| BR2781_2_beta_doc | beta_doc | source-intake\mts_residuals\P8_Y5_R2FR_2781_TAU_SHAPE_STATUS.csv | source-intake\beta-source\docs\MICROSCOPE_SURROGATE_TAU_SHAPE_2781_NONCLAIM.csv | beta/source-facing tau-shape smoke copy | True | 19 | False |
| BR2781_3_microscope_copy | microscope | source-intake\mts_residuals\P8_Y5_R2FR_2781_WEP_PRODUCT_CANDIDATE_NONCLAIM.csv | source-intake\microscope\branch_locked_wep\residuals\microscope_surrogate_tau_shape_2781_nonclaim.csv | MICROSCOPE surrogate tau-shape smoke copy | True | 299 | False |
| BR2781_4_next_queue | next | source-intake\mts_residuals\P8_Y5_R2FR_2781_NEXT_TARGET.csv | source-intake\rab-sector\acquisition-queue\JR2781_PARENT_WEP_COUPLING_OWNER_NEXT.csv | next parent coupling-owner route | True | 1 | False |

## Validation

| validation_id | passed | detail | timestamp_utc |
| --- | --- | --- | --- |
| VAL2781_0_sources | True | every cited source path exists and source needle was found | 2026-06-23T17:56:18.616100+00:00 |
| VAL2781_1_schema_complete | True | design schema has all expected columns | 2026-06-23T17:56:18.616114+00:00 |
| VAL2781_2_matrix_rows | True | 256 surrogate design-matrix rows written and nonclaim | 2026-06-23T17:56:18.616118+00:00 |
| VAL2781_3_rank_condition | True | design matrix is finite and full-rank for smoke purposes | 2026-06-23T17:56:18.616120+00:00 |
| VAL2781_4_correlations | True | top non-constant column pair correlations written | 2026-06-23T17:56:18.616123+00:00 |
| VAL2781_5_smoke_recovery | True | synthetic coefficient recovery works but remains nonclaim | 2026-06-23T17:56:18.616126+00:00 |
| VAL2781_6_replacement_gates | True | official-array replacement gate remains closed | 2026-06-23T17:56:18.616128+00:00 |
| VAL2781_7_physical_tau_blocked | True | physical tau_WEP remains not acquired | 2026-06-23T17:56:18.616131+00:00 |
| VAL2781_8_prediction_nonclaim_missing | True | prediction row remains missing physical tau | 2026-06-23T17:56:18.616133+00:00 |
| VAL2781_9_bound_numeric | True | bound import is positive numeric | 2026-06-23T17:56:18.616136+00:00 |
| VAL2781_10_runner_refuses | True | runner reports no valid prediction rows and claim false | 2026-06-23T17:56:18.616138+00:00 |
| VAL2781_11_claim_gates_safe | True | all claim gates deny WEP/local-GR claim | 2026-06-23T17:56:18.616140+00:00 |
| VAL2781_12_next_target | True | next target selects parent material/source map or official CMSM import gate | 2026-06-23T17:56:18.616143+00:00 |
| VAL2781_13_branch_outputs | True | branch copies exist and contain rows | 2026-06-23T17:56:18.616145+00:00 |
| VAL2781_14_csv_parse | True | all generated CSV outputs parse cleanly | 2026-06-23T17:56:18.616148+00:00 |
| VAL2781_15_no_claim_flags | True | no generated row is valid_for_claim=true/claim_allowed=true/pass_for_claim=true | 2026-06-23T17:56:18.616150+00:00 |
| VAL2781_16_generated_under_post_checkpoint | True | all generated outputs are under post-checkpoint-work | 2026-06-23T17:56:18.616152+00:00 |
| VAL2781_17_formalization_untouched | True | formalization-workbench modified-file count remains zero during this run | 2026-06-23T17:56:18.616155+00:00 |
| VAL2781_18_pycache_absent | True | scripts __pycache__ removed | 2026-06-23T17:56:18.616157+00:00 |
| VAL2781_OVERALL | True | 2781 builds a working nonclaim surrogate design-matrix/tau-shape smoke runner for SUEP segment 210 in the R2/f(R) branch. Regression plumbing, rank/condition diagnostics, correlation checks, and synthetic coefficient recovery pass. Official MICROSCOPE arrays, exact masks, and parent material/source map remain missing, so WEP/local-GR claims stay blocked and 2782 targets the coupling-owner/material-source map gate. | 2026-06-23T17:56:18.616163+00:00 |

## Plain-English Read

This is a good little gym session: the matrix machinery behaves, so the next bottleneck is not linear algebra. The next serious fight is the coupling owner: what parent object makes Ti/Pt respond differently, or proves they cannot differ under universal metric/coframe coupling?

