# 1494 - PDF Text/Table Extraction for EotWash and R10 Curve Digitization

## Verdict
- PDF text extraction succeeded where source PDFs were available, and candidate anchors were staged for manual review.
- No extracted text anchor is promoted into a live bound curve, WEP table, MICROSCOPE array, or parent coupling coefficient.
- The highest-leverage next step is the real R10 `alpha(lambda)` curve: digitize/source it, then derive the `delta_w -> alpha(lambda)` kernel.

## PDF Text Extraction Ledger
| external_id | arena | extraction_status | page_count | normalized_char_count | text_path |
| --- | --- | --- | --- | --- | --- |
| EXT1492_0_EOTWASH_PRL_2008 | WEP_EotWash_material_pairs | TEXT_EXTRACTED_NONCLAIM | 4 | 17068 | source-intake\eotwash\extracted_text\Schlamminger_2008_PRL_0712.0607.txt |
| EXT1492_1_EOTWASH_CQG_2012 | WEP_EotWash_material_pairs | TEXT_EXTRACTED_NONCLAIM | 17 | 39736 | source-intake\eotwash\extracted_text\Wagner_2012_CQG_1207.2442.txt |
| EXT1492_2_R10_ARXIV_2020 | R10_short_range_inverse_square | TEXT_EXTRACTED_NONCLAIM | 5 | 20938 | source-intake\r10\extracted_text\Lee_2020_PRL_2002.11761.txt |
| EXT1492_5_MICROSCOPE_PRL_FINAL | WEP_MICROSCOPE_TiPt | TEXT_EXTRACTED_NONCLAIM | 9 | 51766 | source-intake\microscope\extracted_text\Touboul_2022_PRL_final_results.txt |
| EXT1492_6_MICROSCOPE_CQG_READOUT | WEP_MICROSCOPE_TiPt | TEXT_EXTRACTED_NONCLAIM | 36 | 88692 | source-intake\microscope\extracted_text\Touboul_2022_CQG_readout.txt |

## Anchor Candidate Summary
| external_id | anchor_name | anchor_status | char_start |
| --- | --- | --- | --- |
| EXT1492_0_EOTWASH_PRL_2008 | Be_Ti_eta_Earth | ANCHOR_NOT_FOUND_OR_NEEDS_MANUAL_REVIEW |  |
| EXT1492_0_EOTWASH_PRL_2008 | Be_Ti_delta_a | CANDIDATE_ANCHOR_FOUND_NONCLAIM | 14564 |
| EXT1492_0_EOTWASH_PRL_2008 | Milky_Way_DM_eta | ANCHOR_NOT_FOUND_OR_NEEDS_MANUAL_REVIEW |  |
| EXT1492_0_EOTWASH_PRL_2008 | Yukawa_charge_formula | CANDIDATE_ANCHOR_FOUND_NONCLAIM | 2128 |
| EXT1492_1_EOTWASH_CQG_2012 | Be_Al_or_Be_Ti_context | CANDIDATE_ANCHOR_FOUND_NONCLAIM | 13983 |
| EXT1492_1_EOTWASH_CQG_2012 | torsion_balance_context | CANDIDATE_ANCHOR_FOUND_NONCLAIM | 38 |
| EXT1492_1_EOTWASH_CQG_2012 | WEP_precision_context | CANDIDATE_ANCHOR_FOUND_NONCLAIM | 23133 |
| EXT1492_2_R10_ARXIV_2020 | R10_separation_range | ANCHOR_NOT_FOUND_OR_NEEDS_MANUAL_REVIEW |  |
| EXT1492_2_R10_ARXIV_2020 | R10_gravity_strength_threshold | CANDIDATE_ANCHOR_FOUND_NONCLAIM | 693 |
| EXT1492_2_R10_ARXIV_2020 | R10_Yukawa_potential | ANCHOR_NOT_FOUND_OR_NEEDS_MANUAL_REVIEW |  |
| EXT1492_2_R10_ARXIV_2020 | R10_curve_language | CANDIDATE_ANCHOR_FOUND_NONCLAIM | 674 |
| EXT1492_5_MICROSCOPE_PRL_FINAL | SUEP_materials | CANDIDATE_ANCHOR_FOUND_NONCLAIM | 7880 |
| EXT1492_5_MICROSCOPE_PRL_FINAL | EP_plot_units | CANDIDATE_ANCHOR_FOUND_NONCLAIM | 22009 |
| EXT1492_5_MICROSCOPE_PRL_FINAL | Eotvos_parameter_definition | CANDIDATE_ANCHOR_FOUND_NONCLAIM | 7692 |
| EXT1492_5_MICROSCOPE_PRL_FINAL | MICROSCOPE_final_bound_context | CANDIDATE_ANCHOR_FOUND_NONCLAIM | 3680 |
| EXT1492_6_MICROSCOPE_CQG_READOUT | SUEP_SUREF_materials | CANDIDATE_ANCHOR_FOUND_NONCLAIM | 9963 |
| EXT1492_6_MICROSCOPE_CQG_READOUT | PtRh10_composition | CANDIDATE_ANCHOR_FOUND_NONCLAIM | 10014 |
| EXT1492_6_MICROSCOPE_CQG_READOUT | session_table_context | CANDIDATE_ANCHOR_FOUND_NONCLAIM | 20115 |
| EXT1492_6_MICROSCOPE_CQG_READOUT | EP_units_context | CANDIDATE_ANCHOR_FOUND_NONCLAIM | 52303 |

## R10 Digitization Queue
| queue_id | object | current_status | required_output | promotion_blocker |
| --- | --- | --- | --- | --- |
| R10Q1494_0_pdf_text | R10 PDF text | TEXT_ANCHOR_FOUND_NONCLAIM | source-intake\r10\derived\R10_alpha_lambda_bound_curve_DIGITIZED.csv | FULL_CURVE_NOT_DIGITIZED |
| R10Q1494_1_curve_digitization | alpha(lambda) curve | NOT_DIGITIZED | source-intake\r10\derived\R10_alpha_lambda_bound_curve_DIGITIZED.csv | DIGITIZED_CURVE_REQUIRED |
| R10Q1494_2_delta_w_kernel | delta_w to alpha(lambda) projection kernel | MISSING | source-intake\r10\derived\R10_delta_w_kernel_lambda.csv | PARENT_PROJECTION_KERNEL_REQUIRED |

## EotWash Promotion Queue
| queue_id | object | current_status | required_output | promotion_blocker |
| --- | --- | --- | --- | --- |
| EOTQ1494_0_eta_bound | EotWash Be-Ti eta bound | TEXT_ANCHOR_NEEDS_MANUAL_REVIEW | source-intake\eotwash\derived\P_WEP_EotWash_material_pair_bounds.csv | ETA_TABLE_ROW_NOT_PROMOTED |
| EOTQ1494_1_material_vectors | EotWash material response vectors | MISSING | source-intake\eotwash\derived\P_WEP_EotWash_material_response_vectors.csv | MATERIAL_RESPONSE_BASIS_MISSING |

## MICROSCOPE Promotion Queue
| queue_id | object | current_status | required_output | promotion_blocker |
| --- | --- | --- | --- | --- |
| MICQ1494_0_material_convention | MICROSCOPE material convention | TEXT_ANCHOR_FOUND_NONCLAIM | source-intake\microscope\derived\P_WEP_R_material_TA6V_minus_PtRh10_full_tensor.csv | MATERIAL_TENSOR_NOT_PROMOTED |
| MICQ1494_1_official_readout | CMSM official readout/design matrix | MISSING_PORTAL_FETCH_BLOCKED | source-intake\microscope\official_readout\P_WEP_K_CMSM_readout.csv | OFFICIAL_ARRAYS_MISSING |
| MICQ1494_2_source_worldtube | Earth/source worldtube | MISSING | source-intake\microscope\source_worldtube\P_WEP_R_source_Earth_worldtube.csv | SOURCE_WORLDTUBE_MISSING |

## Target Promotion Blockers
| blocker_id | target_name | target_status | blocking_marker |
| --- | --- | --- | --- |
| TBLK1494_0_EOTWASH_bounds | EOTWASH_bounds | MISSING_OR_UNPROMOTED | TARGET_FILE_MISSING |
| TBLK1494_1_EOTWASH_vectors | EOTWASH_vectors | MISSING_OR_UNPROMOTED | TARGET_FILE_MISSING |
| TBLK1494_2_R10_curve | R10_curve | MISSING_OR_UNPROMOTED | TARGET_FILE_MISSING |
| TBLK1494_3_R10_kernel | R10_kernel | MISSING_OR_UNPROMOTED | TARGET_FILE_MISSING |
| TBLK1494_4_MICROSCOPE_readout | MICROSCOPE_readout | MISSING_OR_UNPROMOTED | TARGET_FILE_MISSING |
| TBLK1494_5_MICROSCOPE_source | MICROSCOPE_source | MISSING_OR_UNPROMOTED | TARGET_FILE_MISSING |
| TBLK1494_6_MICROSCOPE_product | MICROSCOPE_product | EXISTS_REQUIRES_CONTENT_VALIDATION | PRODUCT_CONVENTION_CONTENT_NOT_VALIDATED |
| TBLK1494_7_MICROSCOPE_tensor | MICROSCOPE_tensor | MISSING_OR_UNPROMOTED | TARGET_FILE_MISSING |
| TBLK1494_overall | delta_w_cross_arena_score | NOT_SCORE_READY | EXTRACTED_TEXT_IS_NOT_A_SCORE |

## Validation
| check_id | result | detail |
| --- | --- | --- |
| VAL1494_0_local_sources | PASS | all cited 1493 local source paths exist |
| VAL1494_1_pdf_extractor | PASS | PDF extractor available=pypdf |
| VAL1494_2_text_extracted | PASS | all downloaded PDFs produced text files |
| VAL1494_3_text_minimum | PASS | all extracted text rows exceed minimum normalized character threshold |
| VAL1494_4_anchor_candidates | PASS | candidate anchors found=15 |
| VAL1494_5_R10_curve_blocked | PASS | R10 curve/kernel remain unpromoted |
| VAL1494_6_readiness_blocked | PASS | delta_w score readiness remains false |
| VAL1494_7_Cparent_refused | PASS | C_parent import was not performed |
| VAL1494_8_csv_parse | PASS | all generated 1494 CSVs parse cleanly |
| VAL1494_9_branch_copies | PASS | branch/quarantine nonclaim copies written |
| VAL1494_10_pycache_absent | PASS | scripts __pycache__ absent after run |
| VAL1494_11_formalization_untouched | PASS | formalization modified-file count since start=0 |
| VAL1494_12_claim_flags_false | PASS | all generated prediction/claim flags remain false |
| VAL1494_13_overall | PASS | 1494 extracted PDF text/anchors and kept all delta_w/local claims blocked |

## Next Target
| next_id | next_target | script | objective |
| --- | --- | --- | --- |
| NEXT1494_0_1495 | 1495-Y5-R10-RAB-R10-alpha-lambda-curve-digitization-or-machine-readable-table-hunt.md | scripts/Y5_R10_RAB_R10_alpha_lambda_curve_digitization_or_machine_readable_table_hunt.py | extract or source a real R10 alpha(lambda) bound curve, keep anchor-only rows invalid for claim, and specify the delta_w-to-alpha kernel inputs still needed |
