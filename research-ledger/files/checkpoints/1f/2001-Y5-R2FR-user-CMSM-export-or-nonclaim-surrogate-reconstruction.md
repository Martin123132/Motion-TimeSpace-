# 2001 - R2FR user CMSM export or nonclaim surrogate reconstruction

## Current verdict
2001 did not find a claim-grade user/browser CMSM export in the local drop folder, so it created a drop contract plus a strictly nonclaim segment-210 surrogate reconstruction. This is a step forward in plumbing: the path now has unitful gx/gz/Sxx/Sxz/gxS arrays for shape and design-matrix smoke tests, but it is not MICROSCOPE evidence and cannot score WEP/local-GR.

Important boundary: the surrogate is allowed to test code geometry only. It cannot become `tau_WEP`, cannot be treated as official CMSM data, and cannot close the local-GR branch.

Next honest move: use the surrogate only to test the design-matrix/tau-shape runner, or replace it with a real CMSM export dropped into `source-intake/microscope_cmsm`.

## Local source register
| source_id | source_path | exists | anchor_found | note |
| --- | --- | --- | --- | --- |
| SRC2001_0_2000_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2000-Y5-R2FR-CMSM-schema-or-one-segment-official-array-extract.md | True | True | 2000 handoff to this checkpoint. |
| SRC2001_1_2000_validation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_2000_VALIDATION.csv | True | True | 2000 validation pass. |
| SRC2001_2_2000_contract | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2000_CMSM_EXTRACTION_CONTRACT.csv | True | True | official extraction contract. |
| SRC2001_3_2000_schema | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2000_OFFICIAL_ARRAY_SCHEMA_CONTRACT.csv | True | True | official array schema contract. |
| SRC2001_4_1999_numeric_kernel | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1999-Y5-R2FR-MICROSCOPE-numeric-kernel-or-source-worldtube-row.md | True | True | numeric kernel/source-worldtube acquisition handoff. |
| SRC2001_5_1074_prior_surrogate | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1074-Y5-R10-user-assisted-CMSM-export-or-nonclaim-surrogate-orbit-reconstruction.md | True | True | earlier R10 analogue used only as surrogate-plumbing precedent. |
| SRC2001_6_local_bound | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\local_bound_claims.csv | True | True | MICROSCOPE WEP bound anchor for refusal runner. |

## CMSM drop contract
| drop_id | column_name | unit_or_type | required_for_tau | current_status |
| --- | --- | --- | --- | --- |
| DROP2001_00_segment_id | segment_id | label | true | AWAITING_USER_OR_BROWSER_EXPORT |
| DROP2001_01_t_utc | t_utc | UTC timestamp | true | AWAITING_USER_OR_BROWSER_EXPORT |
| DROP2001_02_gx | gx | m s^-2 or documented normalized convention | true | AWAITING_USER_OR_BROWSER_EXPORT |
| DROP2001_03_gz | gz | m s^-2 or documented normalized convention | true | AWAITING_USER_OR_BROWSER_EXPORT |
| DROP2001_04_Sxx | Sxx | s^-2 | true | AWAITING_USER_OR_BROWSER_EXPORT |
| DROP2001_05_Sxz | Sxz | s^-2 | true | AWAITING_USER_OR_BROWSER_EXPORT |
| DROP2001_extra_sample_index | sample_index | integer | true | AWAITING_USER_OR_BROWSER_EXPORT |
| DROP2001_extra_mask_flag | mask_flag | boolean | true | AWAITING_USER_OR_BROWSER_EXPORT |

## CMSM export inventory check
| inventory_id | search_root | candidate_file | required_columns_present | contract_match_status | action_taken |
| --- | --- | --- | --- | --- | --- |
| INV2001_0_search_root | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope_cmsm |  | false | NO_USER_SUPPLIED_CMSM_EXPORT_FOUND | surrogate reconstruction branch selected |

## Surrogate assumptions
| assumption_id | object | value | units | source_or_reason | claim_status |
| --- | --- | --- | --- | --- | --- |
| SUR2001_0_branch_selection | branch | nonclaim surrogate reconstruction | text | no claim-grade CMSM export is validated | FORBIDDEN_FOR_EVIDENCE |
| SUR2001_1_orbit_period | Torb | 5946.0 | s | carried from prior MICROSCOPE segment/frequency source row and 1074 precedent | source-backed scalar, surrogate-only use |
| SUR2001_2_orbit_radius | r_surrogate=(mu/n^2)^(1/3) | 7093751.1549701765 | m | derived from Earth monopole and Torb; not official ephemeris | surrogate_only |
| SUR2001_3_gravity_amplitude | g0=mu/r^2 | 7.921106939620683 | m s^-2 | spherical Earth monopole; not MICROSCOPE gravity model | surrogate_only |
| SUR2001_4_gradient_scale | G=mu/r^3 | 1.116631633472345e-06 | s^-2 | spherical Earth monopole gradient scale; inertia subtraction omitted | surrogate_only |
| SUR2001_5_readout_phase | phi=2*pi*fEP3*t | 0.00311133 | Hz | zero phase is guessed; exact attitude products missing | FORBIDDEN_FOR_EVIDENCE |
| SUR2001_6_masks_attitude | masks/attitude/inertia | omitted_or_identity_surrogate | text | official products unavailable | FORBIDDEN_FOR_EVIDENCE |

## Surrogate grid metadata
| grid_id | segment | full_grid_samples | thin_rows_written | orbit_model | attitude_model | mask_model | claim_status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GRID2001_0_segment210_thin_surrogate | 210 | 1189200 | 1024 | circular_Earth_monopole_from_Torb | zero_phase_rotating_XZ_plane_surrogate | all_samples_unmasked_surrogate | NONCLAIM_PIPELINE_TEST_ONLY |

## Surrogate gxS thin-grid preview
| row_id | sample_index | t_sec_from_segment_start | gx_surrogate_m_s2 | gz_surrogate_m_s2 | Sxx_surrogate_s2 | Sxz_surrogate_s2 | gxS_shape_surrogate_m_s4 | source_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SUR2001_210_0000 | 0 | 0.0 | -7.921106939621e+00 | -0.000000000000e+00 | 2.233263266944690e-06 | 0.000000000000000e+00 | -1.768991716179554e-05 | NOT_CMSM_NOT_OFFICIAL |
| SUR2001_210_0001 | 1162 | 290.5 | -6.518807815918e+00 | 4.499897755286e+00 | 1.152166121442643e-06 | -1.566138811395735e-06 | -1.455821403956261e-05 | NOT_CMSM_NOT_OFFICIAL |
| SUR2001_210_0002 | 2324 | 581.0 | -2.808417523261e+00 | 7.406532668121e+00 | -6.955340230893268e-07 | -1.110544704246337e-06 | -6.271935692941710e-06 | NOT_CMSM_NOT_OFFICIAL |
| SUR2001_210_0003 | 3486 | 871.5 | 1.896339203755e+00 | 7.690762821282e+00 | -9.246359452653742e-07 | 7.786546298176893e-07 | 4.235024685413032e-06 | NOT_CMSM_NOT_OFFICIAL |
| SUR2001_210_0004 | 4648 | 1162.0 | 5.929665832948e+00 | 5.251951852262e+00 | 7.606086592123139e-07 | 1.662686550989975e-06 | 1.324250488997873e-05 | NOT_CMSM_NOT_OFFICIAL |
| SUR2001_210_0005 | 5810 | 1452.5 | 7.863496706112e+00 | 9.536009133138e-01 | 2.184712874444685e-06 | 4.003518098336868e-07 | 1.756125834350046e-05 | NOT_CMSM_NOT_OFFICIAL |
| SUR2001_210_0006 | 6972 | 1743.0 | 7.013127182976e+00 | -3.682388119728e+00 | 1.509296634485811e-06 | -1.378798188725327e-06 | 1.566215932415089e-05 | NOT_CMSM_NOT_OFFICIAL |
| SUR2001_210_0007 | 8134 | 2033.5 | 3.679644585350e+00 | -7.014567048251e+00 | -3.937433704674060e-07 | -1.378053796127450e-06 | 8.217615087874840e-06 | NOT_CMSM_NOT_OFFICIAL |
| SUR2001_210_0008 | 9296 | 2324.0 | -9.566767233049e-01 | -7.863123094292e+00 | -1.067767540318876e-06 | 4.016240491661282e-07 | -2.136510984497807e-06 | NOT_CMSM_NOT_OFFICIAL |
| SUR2001_210_0009 | 10458 | 2614.5 | -5.254270896729e+00 | -5.927611027445e+00 | 3.573237879806501e-07 | 1.662844299787793e-06 | -1.173417018824228e-05 | NOT_CMSM_NOT_OFFICIAL |

## Replacement map
| map_id | official_contract_column | surrogate_column | replacement_status | evidence_policy | next_action |
| --- | --- | --- | --- | --- | --- |
| MAP2001_0_segment_id | segment_id | segment_id | SURROGATE_AVAILABLE_OFFICIAL_MISSING | cannot support claim | replace with exact CMSM segment id |
| MAP2001_1_t_utc | t_utc | t_sec_from_segment_start | SURROGATE_RELATIVE_TIME_OFFICIAL_UTC_MISSING | cannot support claim | replace with exact CMSM timestamps |
| MAP2001_2_sample_index | sample_index | sample_index | SURROGATE_AVAILABLE_OFFICIAL_MISSING | cannot support claim | replace with exact CMSM sample index |
| MAP2001_3_gx | gx | gx_surrogate_m_s2 | SURROGATE_AVAILABLE_OFFICIAL_MISSING | cannot support claim | replace with CMSM/official gx |
| MAP2001_4_gz | gz | gz_surrogate_m_s2 | SURROGATE_AVAILABLE_OFFICIAL_MISSING | cannot support claim | replace with CMSM/official gz |
| MAP2001_5_Sxx | Sxx | Sxx_surrogate_s2 | SURROGATE_AVAILABLE_OFFICIAL_MISSING | cannot support claim | replace with CMSM/official Sxx |
| MAP2001_6_Sxz | Sxz | Sxz_surrogate_s2 | SURROGATE_AVAILABLE_OFFICIAL_MISSING | cannot support claim | replace with CMSM/official Sxz |
| MAP2001_7_mask_flag | mask_flag | mask_flag_surrogate | SURROGATE_ALL_UNMASKED_OFFICIAL_MISSING | cannot support claim | replace with exact CMSM mask |

## Schema validator dry run
| schema_check_id | gate_pass | detail | evidence_policy |
| --- | --- | --- | --- |
| SCHEMA2001_0_official_export_presence | false | no official-like CMSM export present | claim remains false until provenance, units, masks, and source path are validated |
| SCHEMA2001_1_required_columns | false | required official columns absent locally | surrogate columns are not accepted as evidence |
| SCHEMA2001_2_surrogate_numeric_path | true | 1024 surrogate rows written | numeric code path exists, evidence gate remains closed |
| SCHEMA2001_3_tau_WEP_readiness | false | tau_WEP is not acquired | requires official arrays plus MTS material/source map or direct parent product |

## Status ledger
| status_id | object | status | next_action | claim_allowed |
| --- | --- | --- | --- | --- |
| STAT2001_0_CMSM_export | user/browser CMSM export | NOT_FOUND_LOCALLY | drop official export into source-intake/microscope_cmsm if obtained | false |
| STAT2001_1_surrogate_reconstruction | segment 210 thin surrogate gx/gz/Sxx/Sxz/gxS | BUILT_NONCLAIM | use for design-matrix/code plumbing only | false |
| STAT2001_2_official_arrays | official CMSM gx/gz/Sxx/Sxz arrays | NOT_ACQUIRED | replace surrogate columns with official export or source-backed reconstruction | false |
| STAT2001_3_tau_WEP | numeric tau_WEP | NOT_ACQUIRED | derive after official arrays and source-weight/material map exist | false |
| STAT2001_4_local_GR_WEP | local-GR/WEP pass | BLOCKED | do not promote until tau_WEP and product gates pass | false |

## Nonclaim product candidate
| prediction_id | product_symbol | product_value | derivation_status | valid_for_claim |
| --- | --- | --- | --- | --- |
| PRED2001_0_WEP_surrogate_reconstruction_nonclaim_product | P_WEP_relative_source_weight | MISSING_OFFICIAL_ARRAYS_AND_MTS_TAU_SOURCE_SURROGATE_ONLY | NONCLAIM_SURROGATE_PIPELINE_ONLY | false |

## Bound import
| bound_id | product_symbol | bound_value | bound_units | valid_for_claim |
| --- | --- | --- | --- | --- |
| BOUND2001_0_MICROSCOPE_R1_eta_source_charge | P_WEP_relative_source_weight | 2.8e-15 | dimensionless | true |

## Product runner status
| runner_id | valid_prediction_rows | valid_bound_rows | claim_allowed | expected_result |
| --- | --- | --- | --- | --- |
| APR2001_0_WEP_surrogate_reconstruction_product_stub | 0 | 1 | false | reject surrogate-only prediction and keep claim false |

## Product comparison rows
| comparison_id | comparison_status | pass_for_claim | issues |
| --- | --- | --- | --- |
| PRODUCT_COMPARE_NO_VALID_PREDICTIONS | not_run | false | no valid MTS alpha product prediction rows |

## Claim gates
| gate_id | claim_component | gate_pass | claim_allowed | reason |
| --- | --- | --- | --- | --- |
| CG2001_0_CMSM_export | user/browser CMSM export | false | false | NO_USER_SUPPLIED_CMSM_EXPORT_FOUND |
| CG2001_1_surrogate_reconstruction | surrogate segment 210 gxS path | true | false | pipeline built but not official arrays |
| CG2001_2_official_arrays | official gx/gz/Sxx/Sxz arrays | false | false | MISSING_CLAIM_GRADE_OFFICIAL_ARRAYS |
| CG2001_3_product_runner | WEP product runner | false | false | valid_prediction_rows=0 |
| CG2001_4_local_GR_WEP_claim | local-GR/WEP pass | false | false | surrogate-only arrays and no MTS tau_WEP product |

## Decision ledger
| decision_id | decision | evidence | consequence |
| --- | --- | --- | --- |
| DEC2001_0_not_circling | convert blocked CMSM acquisition into a runnable import/drop contract plus surrogate harness | 2000 found the live CMSM module inaccessible here | future official export can be swapped into a known schema instead of restarting the loop |
| DEC2001_1_surrogate_is_useful | build physically unitful gx/gz/Sxx/Sxz/gxS thin-grid plumbing | P8_Y5_PARENT_QLOC_2001_SURROGATE_THIN_GRID_SEGMENT210_NONCLAIM.csv | next runner can test design-matrix shape and replacement gates without claiming evidence |
| DEC2001_2_no_claim | keep WEP/local-GR claim closed | official arrays and tau_WEP product are still missing | project advances by hardening the test harness, not by pretending surrogate data are evidence |

## Validation
| validation_id | status | detail |
| --- | --- | --- |
| VAL2001_00_sources | PASS | all source paths exist and needles found |
| VAL2001_01_drop_contract | PASS | drop README/template and official column contract written |
| VAL2001_02_inventory | PASS | CMSM export inventory recorded without promoting a claim |
| VAL2001_03_surrogate_nonclaim | PASS | surrogate thin grid written and marked nonofficial |
| VAL2001_04_surrogate_numeric | PASS | surrogate gxS shape is finite and nonzero |
| VAL2001_05_replacement_map | PASS | replacement map covers official columns and denies evidence status |
| VAL2001_06_schema_validator | PASS | schema validator blocks tau_WEP readiness |
| VAL2001_07_status_blocked | PASS | numeric tau_WEP remains not acquired |
| VAL2001_08_product_runner_refuses | PASS | product runner refuses surrogate-only prediction |
| VAL2001_09_claim_gates_safe | PASS | all claim gates deny WEP/local-GR claim |
| VAL2001_10_next_target | PASS | 2002 handoff written |
| VAL2001_11_generated_under_post_checkpoint | PASS | all generated outputs are under post-checkpoint-work |
| VAL2001_12_csv_parse | PASS | all 2001 CSV outputs parse cleanly |
| VAL2001_13_pycache_absent | PASS | scripts __pycache__ absent |
| VAL2001_14_formalization_untouched | PASS | formalization-workbench modified-file count remains zero |
| VAL2001_OVERALL | PASS | 2001 user CMSM export/drop contract plus nonclaim surrogate reconstruction |

## Next target
| next_id | next_target | objective | include | exclude |
| --- | --- | --- | --- | --- |
| NEXT2001_0_2002 | 2002-Y5-R2FR-surrogate-design-matrix-tau-shape-smoke-runner.md | use the 2001 nonclaim surrogate thin grid to build a design-matrix/tau-shape smoke runner with condition diagnostics and official-replacement gates. | constant/time-polynomial/gx/gz/Sxx/Sxz/gxS columns; rank and conditioning diagnostics; refusal if official arrays are absent; clear swap contract for CMSM export | claiming MICROSCOPE evidence, treating surrogate masks as final, setting tau_WEP=1, pushing GitHub, or editing formalization-workbench |

