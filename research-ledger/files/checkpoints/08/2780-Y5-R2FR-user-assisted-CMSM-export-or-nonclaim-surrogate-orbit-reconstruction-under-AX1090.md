# 2780 - Y5 R2/f(R): User-Assisted CMSM Export Or Nonclaim Surrogate Orbit Reconstruction Under AX1090

## Private Verdict

2780 found no local user-supplied CMSM export, so it selected the only honest route available from this machine: a strictly nonclaim segment-210 surrogate orbit/gravity reconstruction. This gives the R2/f(R) branch unitful gx/gz/Sxx/Sxz plumbing for the next smoke runner, but it is not official MICROSCOPE evidence and cannot support a WEP/local-GR claim.

## Source Register

| row_id | source_key | source_path | exists | needle_found | source_role | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| SRC2780_00_2779_next | 2779_next | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_2779_NEXT_TARGET.csv | True | True | current handoff into CMSM export or surrogate reconstruction | False |
| SRC2780_01_2779_validation | 2779_validation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_2779_VALIDATION.csv | True | True | current validation baseline | False |
| SRC2780_02_2779_contract | 2779_contract | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_2779_CMSM_EXPORT_CONTRACT.csv | True | True | current CMSM export contract | False |
| SRC2780_03_2779_array_contract | 2779_array_contract | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_2779_OFFICIAL_ARRAY_SCHEMA_CONTRACT.csv | True | True | current official-array schema contract | False |
| SRC2780_04_2779_dry_run | 2779_dry_run | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_2779_GXS_DRY_RUN_KERNEL_PREVIEW_SEGMENT210.csv | True | True | current phase-only dry-run path | False |
| SRC2780_05_2779_tau | 2779_tau | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_2779_NUMERIC_TAU_STATUS.csv | True | True | current numeric tau blocker | False |
| SRC2780_06_1074_doc | 1074_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1074-Y5-R10-user-assisted-CMSM-export-or-nonclaim-surrogate-orbit-reconstruction.md | True | True | R10 precedent for nonclaim surrogate reconstruction | False |
| SRC2780_07_1074_assumptions | 1074_assumptions | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1074_SURROGATE_ASSUMPTIONS.csv | True | True | prior surrogate assumption ledger | False |
| SRC2780_08_1074_replacement | 1074_replacement | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1074_SURROGATE_TO_OFFICIAL_REPLACEMENT_MAP.csv | True | True | prior surrogate replacement map | False |
| SRC2780_09_local_bounds | local_bounds | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\local_bound_claims.csv | True | True | local MICROSCOPE WEP bound source row | False |

## CMSM Export Inventory Check

| inventory_id | search_root | exists | known_non_export_files_seen | matching_files | contract_match_status | action_taken | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| INV2780_0_search_root | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope_cmsm | True | CMSM_EXPORT_AND_ARRAY_CONTRACT_2779_NONCLAIM.csv;README_2001_DROP_CMSM_EXPORTS_HERE.txt;TEMPLATE_2001_expected_official_array_schema.csv | 0 | NO_USER_SUPPLIED_CMSM_EXPORT_FOUND | surrogate reconstruction branch selected | False |

## Surrogate Assumptions

| assumption_id | object | value | units | source_or_reason | claim_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| SUR2780_0_branch_selection | branch | nonclaim surrogate orbit/gravity reconstruction | text | CMSM export absent and CMSM/API access blocked in 2779 | FORBIDDEN_FOR_EVIDENCE | False |
| SUR2780_1_orbit_period | Torb | 5946.0 | s | MICROSCOPE frequency table / 2778 kernel source row | source-backed scalar, but surrogate use only | False |
| SUR2780_2_orbit_radius | r_surrogate=(mu/n^2)^(1/3) | 7093751.1549701765 | m | derived from Earth monopole and Torb; not official ephemeris | surrogate_only | False |
| SUR2780_3_gravity_amplitude | g0=mu/r^2 | 7.921106939620683 | m s^-2 | spherical Earth monopole; not MICROSCOPE gravity model | surrogate_only | False |
| SUR2780_4_gradient_scale | G=mu/r^3 | 1.116631633472345e-06 | s^-2 | spherical Earth monopole gradient scale; no inertia subtraction | surrogate_only | False |
| SUR2780_5_readout_phase | phi=2*pi*fEP3*t | 0.00311133 | Hz | official fEP3 scalar; zero phase is guessed | FORBIDDEN_FOR_EVIDENCE | False |
| SUR2780_6_masks_attitude | masks/attitude/inertia | omitted_or_identity_surrogate | text | official products unavailable | FORBIDDEN_FOR_EVIDENCE | False |

## Surrogate Grid Metadata

| grid_id | segment | duration_orbits | torb_s | sample_rate_hz | full_grid_samples | preview_rows_written | orbit_radius_m | orbit_model | attitude_model | mask_model | inertia_subtraction | claim_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GRID2780_0_segment210_surrogate | 210 | 50 | 5946.0 | 4.0 | 1189200 | 256 | 7093751.1549701765 | circular_Earth_monopole_from_Torb | zero_phase_rotating_XZ_plane_surrogate | all_samples_unmasked_surrogate | omitted | NONCLAIM_PIPELINE_TEST_ONLY | False |

## Surrogate gxS Preview

| row_id | sample_index | t_sec_from_segment_start | gx_surrogate_m_s2 | gz_surrogate_m_s2 | Sxx_surrogate_s2 | Sxz_surrogate_s2 | source_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SUR2780_210_000 | 0 | 0.0 | -7.921106939621 | -0.000000000000 | 2.233263266944690e-06 | 0.000000000000000e+00 | NOT_CMSM_NOT_OFFICIAL | False |
| SUR2780_210_001 | 4663 | 1165.75 | 5.529068841475 | 5.672154167082 | -5.704646129850310e-08 | 1.674400913137295e-06 | NOT_CMSM_NOT_OFFICIAL | False |
| SUR2780_210_002 | 9326 | 2331.5 | 0.202336700362 | -7.918522274301 | -2.230348878126453e-06 | -8.554177046949253e-08 | NOT_CMSM_NOT_OFFICIAL | False |
| SUR2780_210_003 | 13989 | 3497.25 | -5.811537833242 | 5.382375234198 | 1.709904936402442e-07 | -1.670030756362032e-06 | NOT_CMSM_NOT_OFFICIAL | False |
| SUR2780_210_004 | 18652 | 4663.0 | 7.910769965098 | 0.404541355377 | 2.221613318175023e-06 | 1.708602784306740e-07 | NOT_CMSM_NOT_OFFICIAL | False |
| SUR2780_210_005 | 23315 | 5828.75 | -5.232169077801 | -5.947128877888 | -2.844882438172160e-07 | 1.661301848843408e-06 | NOT_CMSM_NOT_OFFICIAL | False |
| SUR2780_210_006 | 27978 | 6994.5 | -0.606482005875 | 7.897855071186 | -2.207079386747409e-06 | -2.557328440864087e-07 | NOT_CMSM_NOT_OFFICIAL | False |
| SUR2780_210_007 | 32641 | 8160.25 | 6.078838814028 | -5.078548397129 | 3.972434847082974e-07 | -1.648236972875706e-06 | NOT_CMSM_NOT_OFFICIAL | False |
| SUR2780_210_008 | 37304 | 9326.0 | -7.879786020851 | -0.808026864971 | 2.186785017147622e-06 | 3.399379515411873e-07 | NOT_CMSM_NOT_OFFICIAL | False |
| SUR2780_210_009 | 41967 | 10491.75 | 4.921613445353 | 6.206581687485 | -5.089619271287125e-07 | 1.630870227554163e-06 | NOT_CMSM_NOT_OFFICIAL | False |

_Only the first 10 of 256 preview rows are shown here; the full CSV is written separately._

## Replacement Map

| map_id | official_contract_column | surrogate_column | replacement_status | evidence_policy | next_action | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| MAP2780_0_gx | gx | gx_surrogate_m_s2 | SURROGATE_AVAILABLE_OFFICIAL_MISSING | cannot support claim | replace with CMSM/official gx | False |
| MAP2780_1_gz | gz | gz_surrogate_m_s2 | SURROGATE_AVAILABLE_OFFICIAL_MISSING | cannot support claim | replace with CMSM/official gz | False |
| MAP2780_2_Sxx | Sxx | Sxx_surrogate_s2 | SURROGATE_AVAILABLE_OFFICIAL_MISSING | cannot support claim | replace with CMSM/official Sxx or official reconstruction | False |
| MAP2780_3_Sxz | Sxz | Sxz_surrogate_s2 | SURROGATE_AVAILABLE_OFFICIAL_MISSING | cannot support claim | replace with CMSM/official Sxz or official reconstruction | False |
| MAP2780_4_mask | mask_flag | mask_flag_surrogate | SURROGATE_ALL_UNMASKED_OFFICIAL_MISSING | cannot support claim | replace with exact CMSM mask | False |

## Status Ledger

| status_id | object | status | next_action | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| STAT2780_0_CMSM_export | user-assisted CMSM export | NOT_FOUND_LOCALLY | import user-supplied CMSM export if available | False | False |
| STAT2780_1_surrogate_orbit | surrogate segment 210 orbit/gravity preview | BUILT_NONCLAIM | wire surrogate into a nonclaim design-matrix/tau-shape smoke runner | False | False |
| STAT2780_2_official_arrays | official gx/gz/Sxx/Sxz arrays | NOT_ACQUIRED | replace surrogate columns with CMSM official arrays | False | False |
| STAT2780_3_tau_WEP | numeric tau_WEP | NOT_ACQUIRED | derive only after official arrays or explicitly nonclaim smoke-route selection | False | False |

## Nonclaim Product Candidate

| prediction_id | arena | product_symbol | product_value | product_units | derivation_status | notes | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| PRED2780_0_WEP_surrogate_orbit_nonclaim_product | MICROSCOPE_WEP | P_WEP_relative_source_weight | MISSING_OFFICIAL_ARRAYS_SURROGATE_ONLY | dimensionless | NONCLAIM_SURROGATE_PIPELINE_ONLY | surrogate arrays are unitful plumbing checks, not MICROSCOPE evidence and not an MTS tau_WEP product | False |

## Bound Import

| bound_id | arena | product_symbol | bound_value | bound_units | bound_type | source_row_id | bound_valid_for_internal_runner | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BOUND2780_0_MICROSCOPE_R1_eta_source_charge | MICROSCOPE_WEP | P_WEP_relative_source_weight | 2.8e-15 | dimensionless | source_backed_upper_bound_anchor | R1_WEP_source_charge | True | False |

## Product Runner Status

| runner_id | prediction_rows | bound_rows | valid_prediction_rows | valid_bound_rows | claim_allowed | expected_result | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| APR2780_0_WEP_surrogate_orbit_product_stub | 1 | 1 | 0 | 1 | False | reject surrogate-only prediction and keep claim false | False |

## Product Comparison Rows

| comparison_id | comparison_status | pass_for_claim | issues | valid_for_claim |
| --- | --- | --- | --- | --- |
| PRODUCT_COMPARE_NO_VALID_PREDICTIONS | not_run | False | no valid MTS tau_WEP/direct-product prediction rows | False |

## Claim Gates

| gate_id | claim_component | gate_pass | claim_allowed | reason | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| CG2780_0_CMSM_export | user/CMSM export | False | False | NO_USER_SUPPLIED_CMSM_EXPORT_FOUND | False |
| CG2780_1_surrogate_preview | surrogate segment 210 gxS preview | True | False | pipeline built but not official arrays | False |
| CG2780_2_replacement_map | surrogate-to-official replacement map | True | False | replacement requirements explicit | False |
| CG2780_3_official_arrays | official gx/gz/Sxx/Sxz arrays | False | False | MISSING_OFFICIAL_ARRAYS | False |
| CG2780_4_product_runner | WEP product runner | False | False | valid_prediction_rows=0 | False |
| CG2780_5_local_GR_WEP_claim | local-GR/WEP pass | False | False | surrogate-only arrays and no MTS tau_WEP product | False |

## Decision Ledger

| decision_id | decision | evidence | consequence | valid_for_claim |
| --- | --- | --- | --- | --- |
| DEC2780_0_surrogate_branch_selected | no local CMSM export found, so select nonclaim surrogate branch | INV2780_0_search_root | test pipeline geometry without claiming evidence | False |
| DEC2780_1_surrogate_is_useful | surrogate gx/gz/Sxx/Sxz arrays now exist with physical units and source flags in the R2/f(R) branch | P8_Y5_R2FR_2780_SURROGATE_GXS_PREVIEW_SEGMENT210.csv | next step can build a design-matrix/tau-shape smoke runner | False |
| DEC2780_2_no_claim | do not treat surrogate arrays as official MICROSCOPE evidence | STAT2780_3_tau_WEP; APR2780_0_WEP_surrogate_orbit_product_stub | WEP/local-GR branch remains blocked | False |

## Next Target

| row_id | next_target | script | objective | include | exclude | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| NEXT2780_0_2781 | 2781-Y5-R2FR-surrogate-design-matrix-tau-shape-smoke-runner-under-AX1090.md | scripts/Y5_R2FR_surrogate_design_matrix_tau_shape_smoke_runner_under_AX1090_2781.py | use the 2780 nonclaim surrogate gx/gz/Sxx/Sxz arrays to build a design-matrix/tau-shape smoke runner that verifies regression plumbing and replacement gates, while refusing any WEP/local-GR claim until official arrays and the MTS material/source map exist | segment 210 surrogate design matrix; polynomial/gx/gz/Sxx/Sxz columns; condition-number/orthogonality diagnostics; replacement gates; product-runner refusal | treating surrogate fit as MICROSCOPE evidence; official claim; tau=1; guessed masks as final; GitHub; formalization edits | False |

## Branch Copies

| copy_id | table_key | source_table | copy_path | purpose | exists | row_count | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BR2780_0_inventory_queue | inventory | source-intake\mts_residuals\P8_Y5_R2FR_2780_CMSM_EXPORT_INVENTORY_CHECK.csv | source-intake\rab-sector\acquisition-queue\JR2780_CMSM_EXPORT_INVENTORY_OR_SURROGATE_NONCLAIM.csv | CMSM inventory decision nonclaim copy | True | 11 | False |
| BR2780_1_surrogate_queue | surrogate | source-intake\mts_residuals\P8_Y5_R2FR_2780_SURROGATE_GXS_PREVIEW_SEGMENT210.csv | source-intake\rab-sector\acquisition-queue\JR2780_SEGMENT210_SURROGATE_GXS_NONCLAIM.csv | segment-210 surrogate gxS nonclaim copy | True | 280 | False |
| BR2780_2_beta_doc | beta_doc | source-intake\mts_residuals\P8_Y5_R2FR_2780_SURROGATE_STATUS_LEDGER.csv | source-intake\beta-source\docs\MICROSCOPE_SURROGATE_GXS_2780_NONCLAIM.csv | beta/source-facing surrogate kernel copy | True | 13 | False |
| BR2780_3_microscope_copy | microscope | source-intake\mts_residuals\P8_Y5_R2FR_2780_WEP_PRODUCT_CANDIDATE_NONCLAIM.csv | source-intake\microscope\branch_locked_wep\residuals\microscope_surrogate_gxS_2780_nonclaim.csv | MICROSCOPE surrogate orbit acquisition copy | True | 276 | False |
| BR2780_4_cmsm_surrogate | cmsm_surrogate | source-intake\mts_residuals\P8_Y5_R2FR_2780_SURROGATE_GXS_PREVIEW_SEGMENT210.csv | source-intake\microscope_cmsm\SURROGATE_SEGMENT210_GXS_2780_NONCLAIM.csv | surrogate file placed beside CMSM drop folder for replacement workflow | True | 256 | False |
| BR2780_5_next_queue | next | source-intake\mts_residuals\P8_Y5_R2FR_2780_NEXT_TARGET.csv | source-intake\rab-sector\acquisition-queue\JR2780_SURROGATE_DESIGN_MATRIX_NEXT.csv | next surrogate design-matrix smoke-runner target | True | 1 | False |

## Validation

| validation_id | passed | detail | timestamp_utc |
| --- | --- | --- | --- |
| VAL2780_0_sources | True | every cited source path exists and source needle was found | 2026-06-23T17:49:57.912153+00:00 |
| VAL2780_1_no_CMSM_export | True | no local user-supplied CMSM export found | 2026-06-23T17:49:57.912173+00:00 |
| VAL2780_2_assumptions_nonclaim | True | surrogate assumptions are nonclaim and mask/attitude gap is explicit | 2026-06-23T17:49:57.912183+00:00 |
| VAL2780_3_grid_metadata | True | grid metadata has expected segment 210 sample count and nonclaim status | 2026-06-23T17:49:57.912191+00:00 |
| VAL2780_4_preview_rows | True | surrogate preview rows written and flagged nonofficial | 2026-06-23T17:49:57.912199+00:00 |
| VAL2780_5_preview_units_numeric | True | surrogate gx/S values are numeric unitful columns | 2026-06-23T17:49:57.912208+00:00 |
| VAL2780_6_replacement_map | True | replacement map covers official gx/gz/Sxx/Sxz/mask columns | 2026-06-23T17:49:57.912216+00:00 |
| VAL2780_7_tau_not_acquired | True | numeric tau_WEP remains not acquired | 2026-06-23T17:49:57.912224+00:00 |
| VAL2780_8_prediction_nonclaim_missing | True | prediction row remains missing official arrays | 2026-06-23T17:49:57.912232+00:00 |
| VAL2780_9_bound_numeric | True | bound import is positive numeric | 2026-06-23T17:49:57.912240+00:00 |
| VAL2780_10_runner_refuses | True | runner reports no valid prediction rows and claim false | 2026-06-23T17:49:57.912248+00:00 |
| VAL2780_11_claim_gates_safe | True | all claim gates deny WEP/local-GR claim while acknowledging surrogate build | 2026-06-23T17:49:57.912255+00:00 |
| VAL2780_12_next_target | True | next target selects surrogate design-matrix tau-shape smoke runner | 2026-06-23T17:49:57.912263+00:00 |
| VAL2780_13_branch_outputs | True | branch copies exist and contain rows | 2026-06-23T17:49:57.912271+00:00 |
| VAL2780_14_csv_parse | True | all generated CSV outputs parse cleanly | 2026-06-23T17:49:57.912279+00:00 |
| VAL2780_15_no_claim_flags | True | no generated row is valid_for_claim=true/claim_allowed=true/pass_for_claim=true | 2026-06-23T17:49:57.912286+00:00 |
| VAL2780_16_generated_under_post_checkpoint | True | all generated outputs are under post-checkpoint-work | 2026-06-23T17:49:57.912294+00:00 |
| VAL2780_17_formalization_untouched | True | formalization-workbench modified-file count remains zero during this run | 2026-06-23T17:49:57.912302+00:00 |
| VAL2780_18_pycache_absent | True | scripts __pycache__ removed | 2026-06-23T17:49:57.912310+00:00 |
| VAL2780_OVERALL | True | 2780 finds no user-supplied CMSM export in the current drop folder, selects the explicitly nonclaim surrogate branch, builds unitful segment-210 gx/gz/Sxx/Sxz surrogate rows with replacement gates, refuses WEP/local-GR scoring, and selects a surrogate design-matrix/tau-shape smoke runner as 2781. | 2026-06-23T17:49:57.912325+00:00 |

## Plain-English Read

We did not get through the official-data door, so we stopped rattling the handle and built the sparring partner. The surrogate is not evidence, but it is useful: it lets us test whether the MICROSCOPE regression/tau plumbing is mathematically sane before we spend another round hunting official arrays.

