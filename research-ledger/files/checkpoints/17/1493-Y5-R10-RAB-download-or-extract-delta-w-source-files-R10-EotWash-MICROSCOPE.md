# 1493 - Download or Extract delta_w Source Files: R10, EotWash, MICROSCOPE

## Verdict
- Automated source acquisition has been attempted for EotWash, R10, PubMed metadata, and MICROSCOPE paper/portal routes.
- Any downloaded PDF/HTML is treated as provenance only; no curve, WEP table, CMSM array, or parent coupling row is promoted.
- `delta_w`, WEP, R10, local-GR, and Newton-limit claims remain blocked until numeric target files and same-branch projection kernels exist.

## Download Attempt Ledger
| external_id | arena | download_status | http_status | byte_count | local_path |
| --- | --- | --- | --- | --- | --- |
| EXT1492_0_EOTWASH_PRL_2008 | WEP_EotWash_material_pairs | DOWNLOADED_PDF_PROVENANCE_ONLY | 200 | 329682 | source-intake\eotwash\raw\Schlamminger_2008_PRL_0712.0607.pdf |
| EXT1492_1_EOTWASH_CQG_2012 | WEP_EotWash_material_pairs | DOWNLOADED_PDF_PROVENANCE_ONLY | 200 | 751613 | source-intake\eotwash\docs\Wagner_2012_CQG_1207.2442.pdf |
| EXT1492_2_R10_ARXIV_2020 | R10_short_range_inverse_square | DOWNLOADED_PDF_PROVENANCE_ONLY | 200 | 856030 | source-intake\r10\raw\Lee_2020_PRL_2002.11761.pdf |
| EXT1492_3_R10_PUBMED_2020 | R10_short_range_inverse_square | DOWNLOADED_METADATA_PROVENANCE_ONLY | 200 | 21203 | source-intake\r10\docs\Lee_2020_PRL_pubmed_record.html |
| EXT1492_4_MICROSCOPE_CMSM_PORTAL | WEP_MICROSCOPE_TiPt | FETCH_FAILED_BLOCKED | unavailable | 0 | source-intake\microscope\raw\CMSM_portal_landing.html |
| EXT1492_5_MICROSCOPE_PRL_FINAL | WEP_MICROSCOPE_TiPt | DOWNLOADED_PDF_PROVENANCE_ONLY | 200 | 460403 | source-intake\microscope\docs\Touboul_2022_PRL_final_results.pdf |
| EXT1492_6_MICROSCOPE_CQG_READOUT | WEP_MICROSCOPE_TiPt | DOWNLOADED_PDF_PROVENANCE_ONLY | 200 | 2951049 | source-intake\microscope\docs\Touboul_2022_CQG_readout.pdf |

## Extraction Blockers
| blocker_id | arena | blocking_marker | download_status | reason |
| --- | --- | --- | --- | --- |
| BLK1493_0_EXT1492_0_EOTWASH_PRL_2008 | WEP_EotWash_material_pairs | PDF_TEXT_TABLE_OR_FIGURE_EXTRACTION_MISSING | DOWNLOADED_PDF_PROVENANCE_ONLY | PDF is acquired, but tables/figures have not been extracted into scoreable target files |
| BLK1493_1_EXT1492_1_EOTWASH_CQG_2012 | WEP_EotWash_material_pairs | PDF_TEXT_TABLE_OR_FIGURE_EXTRACTION_MISSING | DOWNLOADED_PDF_PROVENANCE_ONLY | PDF is acquired, but tables/figures have not been extracted into scoreable target files |
| BLK1493_2_EXT1492_2_R10_ARXIV_2020 | R10_short_range_inverse_square | PDF_TEXT_TABLE_OR_FIGURE_EXTRACTION_MISSING | DOWNLOADED_PDF_PROVENANCE_ONLY | PDF is acquired, but tables/figures have not been extracted into scoreable target files |
| BLK1493_3_EXT1492_3_R10_PUBMED_2020 | R10_short_range_inverse_square | METADATA_ONLY_NOT_SCOREABLE | DOWNLOADED_METADATA_PROVENANCE_ONLY | metadata page is acquired, but it is not a bound curve or official data product |
| BLK1493_4_EXT1492_4_MICROSCOPE_CMSM_PORTAL | WEP_MICROSCOPE_TiPt | SOURCE_FETCH_FAILED_OR_INVALID | FETCH_FAILED_BLOCKED | source acquisition did not produce a validated html payload |
| BLK1493_5_EXT1492_5_MICROSCOPE_PRL_FINAL | WEP_MICROSCOPE_TiPt | PDF_TEXT_TABLE_OR_FIGURE_EXTRACTION_MISSING | DOWNLOADED_PDF_PROVENANCE_ONLY | PDF is acquired, but tables/figures have not been extracted into scoreable target files |
| BLK1493_6_EXT1492_6_MICROSCOPE_CQG_READOUT | WEP_MICROSCOPE_TiPt | PDF_TEXT_TABLE_OR_FIGURE_EXTRACTION_MISSING | DOWNLOADED_PDF_PROVENANCE_ONLY | PDF is acquired, but tables/figures have not been extracted into scoreable target files |
| BLK1493_same_branch_projection | all_delta_w_arenas | SAME_BRANCH_PROJECTION_PRODUCTS_MISSING | BLOCKED_BY_THEORY_INPUTS | source PDFs do not supply C_parent, tau maps, source kernels, or response vectors by themselves |
| BLK1493_claim_gate | local_GR_Newton | CLAIM_PROMOTION_FORBIDDEN | NONCLAIM_GATE_ACTIVE | 1493 is acquisition/provenance plumbing, not a local GR/Newton proof or empirical score |

## R10 Curve Digitization Skeleton
| digitization_id | object | source_present | digitization_status | curve_row_type |
| --- | --- | --- | --- | --- |
| R10DIG1493_0_source_pdf | R10_2020_PRL_PDF | True | SOURCE_PDF_AVAILABLE_NONCLAIM | source_file_only |
| R10DIG1493_1_curve_target | R10_alpha_lambda_bound_curve_DIGITIZED.csv | False | NOT_DIGITIZED | required_full_curve_missing |
| R10DIG1493_2_abstract_anchor | R10_gravity_strength_threshold_anchor | True | ANCHOR_ONLY_NON_CURVE | anchor_only_non_curve |
| R10DIG1493_3_claim_gate | R10_delta_w_score_gate | False | KERNEL_MISSING_SCORE_BLOCKED | kernel_required |

## EotWash Extraction Skeleton
| extract_id | object | source_present | extraction_status | next_action |
| --- | --- | --- | --- | --- |
| EOT1493_0_PRL_source | EotWash_2008_PRL_source_pdf | True | PDF_AVAILABLE_TABLE_NOT_EXTRACTED | extract material pair, source attractor, eta, sigma, confidence, units, and source path |
| EOT1493_1_review_source | EotWash_2012_CQG_review_pdf | True | PDF_AVAILABLE_RESPONSE_VECTOR_NOT_EXTRACTED | build same-basis material response vector table with composition/source convention |
| EOT1493_2_claim_gate | EotWash_delta_w_score_gate | False | TARGET_TABLES_MISSING_SCORE_BLOCKED | promote only after both eta bounds and material response vectors parse and remain sourced |

## MICROSCOPE Parse Status
| microscope_id | object | source_present | parse_status | next_action |
| --- | --- | --- | --- | --- |
| MIC1493_0_portal_probe | CMSM_portal_landing | False | PORTAL_PROBE_FAILED_OR_INVALID | obtain official CMSM export/package or a reproducible parser for official arrays |
| MIC1493_1_final_prl_pdf | MICROSCOPE_final_PRL_bound_source | True | PDF_AVAILABLE_BOUND_TEXT_NOT_TABLE_EXTRACTED | extract/confirm eta result and material convention without replacing official arrays |
| MIC1493_2_CQG_readout_pdf | MICROSCOPE_CQG_readout_convention_source | True | PDF_AVAILABLE_READOUT_CONVENTION_NOT_PARSED | validate product convention content against readout/source-kernel units |
| MIC1493_3_official_arrays_gate | MICROSCOPE_score_gate | False | OFFICIAL_ARRAYS_MISSING_SCORE_BLOCKED | do not score MICROSCOPE until official readout/source/product/material tensors are all populated |

## Validation
| check_id | result | detail |
| --- | --- | --- |
| VAL1493_0_local_sources | PASS | all cited 1492 local source paths exist |
| VAL1493_1_attempt_rows | PASS | every download attempt records URL, local path, and status |
| VAL1493_2_hash_rows | PASS | every saved payload has sha256, byte_count, and local file |
| VAL1493_3_downloaded_thresholds | PASS | downloaded/landing payload rows meet minimum byte thresholds |
| VAL1493_4_extraction_blockers | PASS | every acquisition route retains an extraction/claim blocker |
| VAL1493_5_R10_noncurve_gate | PASS | R10 anchor/curve skeleton remains nonclaim |
| VAL1493_6_EotWash_nonclaim | PASS | EotWash extraction skeleton remains nonclaim |
| VAL1493_7_MICROSCOPE_nonclaim | PASS | MICROSCOPE portal/PDF rows remain nonclaim |
| VAL1493_8_readiness_blocked | PASS | delta_w score readiness remains false |
| VAL1493_9_Cparent_refused | PASS | C_parent import was not performed |
| VAL1493_10_csv_parse | PASS | all generated 1493 CSVs parse cleanly |
| VAL1493_11_branch_copies | PASS | branch/quarantine nonclaim copies written |
| VAL1493_12_pycache_absent | PASS | scripts __pycache__ absent after run |
| VAL1493_13_formalization_untouched | PASS | formalization modified-file count since start=0 |
| VAL1493_14_claim_flags_false | PASS | all generated prediction/claim flags remain false |
| VAL1493_15_overall | PASS | 1493 acquired/hashes accessible source files and keeps all delta_w/local claims blocked |

## Next Target
| next_id | next_target | script | objective |
| --- | --- | --- | --- |
| NEXT1493_0_1494 | 1494-Y5-R10-RAB-PDF-table-text-extraction-for-EotWash-and-R10-curve-digitization.md | scripts/Y5_R10_RAB_pdf_table_text_extraction_for_EotWash_and_R10_curve_digitization.py | extract text/tables from acquired PDFs where possible, stage manual R10 curve digitization, and keep EotWash/MICROSCOPE/R10 rows nonclaim until numeric target files validate |
