# 1492 - delta_w Source Acquisition Ledger: EotWash, R10, MICROSCOPE

## Verdict
- Source leads are now explicit for EotWash WEP, R10 short-range inverse-square, and MICROSCOPE official files.
- This pass does not claim acquisition of the actual data products; it writes local target paths, required columns, extraction methods, and claim gates.
- `delta_w` scoring remains blocked until the target files are populated, parsed, sourced, and projected in one same-branch convention.

## External Source Ledger
| external_id | arena | title | url | doi_or_data_id | current_status |
| --- | --- | --- | --- | --- | --- |
| EXT1492_0_EOTWASH_PRL_2008 | WEP_EotWash_material_pairs | Test of the Equivalence Principle Using a Rotating Torsion Balance | https://arxiv.org/abs/0712.0607 | https://doi.org/10.1103/PhysRevLett.100.041101 | source resolved by web; local PDF/table not acquired in this pass |
| EXT1492_1_EOTWASH_CQG_2012 | WEP_EotWash_material_pairs | Torsion-balance tests of the weak equivalence principle | https://arxiv.org/abs/1207.2442 | https://doi.org/10.1088/0264-9381/29/18/184002 | source resolved by web; local PDF/table not acquired in this pass |
| EXT1492_2_R10_ARXIV_2020 | R10_short_range_inverse_square | New Test of the Gravitational 1/r^2 Law at Separations down to 52 um | https://arxiv.org/abs/2002.11761 | https://doi.org/10.1103/PhysRevLett.124.101101 | source resolved by web; curve not digitized/promoted in this pass |
| EXT1492_3_R10_PUBMED_2020 | R10_short_range_inverse_square | PubMed record for PRL 124 101101 | https://pubmed.ncbi.nlm.nih.gov/32216404/ | https://doi.org/10.1103/PhysRevLett.124.101101 | search result resolved; page itself may require browser challenge |
| EXT1492_4_MICROSCOPE_CMSM_PORTAL | WEP_MICROSCOPE_TiPt | MICROSCOPE science data portal | https://cmsm-ds.onera.fr/user/microscope | not_applicable_data_portal | source resolved by web/search; no data package downloaded in this pass |
| EXT1492_5_MICROSCOPE_PRL_FINAL | WEP_MICROSCOPE_TiPt | MICROSCOPE Mission: Final Results of the Test of the Equivalence Principle | https://arxiv.org/abs/2209.15487 | https://doi.org/10.1103/PhysRevLett.129.121102 | bound already present locally as anchor; official source file not downloaded in this pass |
| EXT1492_6_MICROSCOPE_CQG_READOUT | WEP_MICROSCOPE_TiPt | Result of the MICROSCOPE Weak Equivalence Principle test | https://arxiv.org/abs/2209.15488 | https://doi.org/10.1088/1361-6382/ac84be | source already referenced locally; official arrays still missing |

## Local Target Manifest
| target_id | arena | target_path | target_exists | current_status |
| --- | --- | --- | --- | --- |
| TGT1492_0_EotWash_bound | WEP_EotWash_material_pairs | source-intake\eotwash\derived\P_WEP_EotWash_material_pair_bounds.csv | False | TARGET_FILE_MISSING_OR_UNPROMOTED |
| TGT1492_1_EotWash_vectors | WEP_EotWash_material_pairs | source-intake\eotwash\derived\P_WEP_EotWash_material_response_vectors.csv | False | TARGET_FILE_MISSING_OR_UNPROMOTED |
| TGT1492_2_R10_curve | R10_short_range_inverse_square | source-intake\r10\derived\R10_alpha_lambda_bound_curve_DIGITIZED.csv | False | TARGET_FILE_MISSING_OR_UNPROMOTED |
| TGT1492_3_R10_kernel | R10_short_range_inverse_square | source-intake\r10\derived\R10_delta_w_kernel_lambda.csv | False | TARGET_FILE_MISSING_OR_UNPROMOTED |
| TGT1492_4_MICROSCOPE_readout | WEP_MICROSCOPE_TiPt | source-intake\microscope\official_readout\P_WEP_K_CMSM_readout.csv | False | TARGET_FILE_MISSING_OR_UNPROMOTED |
| TGT1492_5_MICROSCOPE_source | WEP_MICROSCOPE_TiPt | source-intake\microscope\source_worldtube\P_WEP_R_source_Earth_worldtube.csv | False | TARGET_FILE_MISSING_OR_UNPROMOTED |
| TGT1492_6_MICROSCOPE_product | WEP_MICROSCOPE_TiPt | source-intake\microscope\product_convention\P_WEP_eta_product_convention.csv | True | TARGET_EXISTS_REQUIRES_CONTENT_VALIDATION |
| TGT1492_7_MICROSCOPE_tensor | WEP_MICROSCOPE_TiPt | source-intake\microscope\derived\P_WEP_R_material_TA6V_minus_PtRh10_full_tensor.csv | False | TARGET_FILE_MISSING_OR_UNPROMOTED |

## Acquisition Status
| status_id | arena | current_status | next_action |
| --- | --- | --- | --- |
| ACQ1492_0_EotWash | WEP_EotWash_material_pairs | SOURCE_URLS_IDENTIFIED_LOCAL_TABLE_MISSING | extract eta bounds and material pairs into EotWash target files |
| ACQ1492_1_R10 | R10_short_range_inverse_square | SOURCE_URLS_IDENTIFIED_CURVE_MISSING | digitize or locate machine-readable alpha(lambda) curve and build delta_w kernel |
| ACQ1492_2_MICROSCOPE | WEP_MICROSCOPE_TiPt | PORTAL_AND_PAPER_SOURCES_IDENTIFIED_OFFICIAL_FILES_MISSING | download/parse CMSM files or create reproducible official-kernel extraction |
| ACQ1492_3_delta_w | all_delta_w_arenas | SCORING_BLOCKED | do not run scoring until all required target files are filled and validated |

## Extraction Requirements
| requirement_id | arena | required_object | extraction_method | current_status |
| --- | --- | --- | --- | --- |
| EXTREQ1492_0_EotWash_bound | WEP_EotWash_material_pairs | eta bound plus uncertainty/confidence | PDF table/text extraction | REQUIRED_NOT_FILLED |
| EXTREQ1492_1_EotWash_material | WEP_EotWash_material_pairs | material response vectors | composition/model extraction | REQUIRED_NOT_FILLED |
| EXTREQ1492_2_R10_curve | R10_short_range_inverse_square | alpha(lambda) bound curve | figure digitization or machine table | REQUIRED_NOT_FILLED |
| EXTREQ1492_3_R10_kernel | R10_short_range_inverse_square | delta_w-to-alpha kernel | theory/projection construction | REQUIRED_NOT_FILLED |
| EXTREQ1492_4_MICROSCOPE_arrays | WEP_MICROSCOPE_TiPt | official readout arrays/design matrix | CMSM portal extraction | REQUIRED_NOT_FILLED |
| EXTREQ1492_5_MICROSCOPE_source | WEP_MICROSCOPE_TiPt | Earth/source worldtube profile | dataset/model plus orbit projection | REQUIRED_NOT_FILLED |
| EXTREQ1492_6_MICROSCOPE_product | WEP_MICROSCOPE_TiPt | eta product convention | schema fill from official readout convention | REQUIRED_NOT_FILLED |

## Delta w Scoring Blockers
| blocker_id | blocking_marker | reason |
| --- | --- | --- |
| BLK1492_0_EotWash | EOTWASH_TABLE_MISSING | local material-pair eta/source-vector rows absent |
| BLK1492_1_R10 | R10_CURVE_MISSING | alpha(lambda) bound curve and delta_w kernel absent |
| BLK1492_2_MICROSCOPE | MICROSCOPE_OFFICIAL_FILES_MISSING | official arrays/source/product/material tensor absent |
| BLK1492_3_same_branch | SAME_BRANCH_LOCK_MISSING | input factors do not yet share one units/sign/basis convention |
| BLK1492_4_projection | PROJECTION_KERNELS_MISSING | tau_WEP/tau_R10/tau_clock/orbital projection maps missing |
| BLK1492_5_no_claim | CLAIM_PROMOTION_FORBIDDEN | source acquisition ledger is not a score or a local-GR proof |

## Local GR/Newton Status
| status_id | target | current_status | claim_effect |
| --- | --- | --- | --- |
| LRS1492_0_sources | delta_w source acquisition | LEDGER_BUILT_INPUTS_NOT_ACQUIRED | empirical branch not score-ready |
| LRS1492_1_WEP | WEP/MICROSCOPE/EotWash | SOURCE_ACQUISITION_OPEN | WEP claim blocked |
| LRS1492_2_R10 | R10 short-range | CURVE_DIGITIZATION_OPEN | R10 claim blocked |
| LRS1492_3_local_GR | local GR/Newton | NOT_CLOSED | no local-GR/Newton claim |
| LRS1492_4_verdict | overall | NEXT_TARGET_EXTRACTION_OR_DOWNLOAD | no WEP/R10/local claim from 1492 |

## Rejection Ledger
| rejection_id | blocking_marker | reason |
| --- | --- | --- |
| REJ1492_0_downloads | SOURCE_FILES_NOT_DOWNLOADED_OR_PARSED | external sources identified but target data files are not populated |
| REJ1492_1_EotWash | EOTWASH_MATERIAL_PAIR_ROWS_MISSING | EotWash tables/vectors must be extracted before scoring |
| REJ1492_2_R10 | R10_ALPHA_LAMBDA_CURVE_MISSING | R10 remains symbolic until curve/kernel exists |
| REJ1492_3_MICROSCOPE | MICROSCOPE_OFFICIAL_ARRAYS_MISSING | CMSM/readout/source/product files missing |
| REJ1492_4_projection | DELTA_W_PROJECTION_KERNELS_MISSING | source-backed bounds do not become predictions without kernels |
| REJ1492_5_Cparent | C_PARENT_IMPORT_FORBIDDEN | source acquisition does not prove coupling |
| REJ1492_6_claim | CLAIM_PROMOTION_FORBIDDEN | no WEP/R10/local-GR/Newton claim allowed |

## Decision Ledger
- `DEC1492_0_ledger_not_claim`: treat source acquisition as ledger only - do not score delta_w yet.
- `DEC1492_1_EotWash`: use EotWash 2008 PRL plus 2012 review as source leads - extract bound/material rows next.
- `DEC1492_2_R10`: use R10 2020 PRL/arXiv as curve lead - digitize alpha(lambda) curve or find machine table.
- `DEC1492_3_MICROSCOPE`: use CMSM portal plus final/readout papers as official route - download/parse official files or document access blocker.

## Validation
| check_id | result | detail |
| --- | --- | --- |
| VAL1492_0_local_sources | PASS | all cited local source paths exist |
| VAL1492_1_external_urls | PASS | external URLs are recorded and browser-resolved |
| VAL1492_2_no_download_claim | PASS | external sources are ledgered, not falsely marked downloaded |
| VAL1492_3_target_parents | PASS | all local target parent directories exist |
| VAL1492_4_targets_nonclaim | PASS | target files are nonclaim and not score-ready |
| VAL1492_5_status_blocked | PASS | all acquisition status rows remain blocked/non-score |
| VAL1492_6_requirements | PASS | extraction requirements are explicit and unfilled |
| VAL1492_7_blockers | PASS | delta_w scoring blockers remain active |
| VAL1492_8_no_Cparent_import | PASS | live C_parent import remains absent and refused |
| VAL1492_9_local_blocked | PASS | local GR/Newton/WEP remains blocked pending extraction/download |
| VAL1492_10_rejections | PASS | rejection ledger blocks claim promotion |
| VAL1492_11_decisions | PASS | decision ledger covers MICROSCOPE source route |
| VAL1492_12_next | PASS | 1493 handoff written |
| VAL1492_13_csv_parse | PASS | all generated 1492 CSVs parse cleanly |
| VAL1492_14_branch_copies | PASS | branch/quarantine nonclaim copies written |
| VAL1492_15_pycache_absent | PASS | scripts __pycache__ absent after run |
| VAL1492_16_formalization_untouched | PASS | formalization modified-file count since start=0 |
| VAL1492_17_claim_flags_false | PASS | all prediction/claim flags remain false |
| VAL1492_18_overall | PASS | 1492 records source URLs/targets and blocks delta_w scoring until extraction/download succeeds |

## Next Target
| next_id | next_target | script | objective |
| --- | --- | --- | --- |
| NEXT1492_0_1493 | 1493-Y5-R10-RAB-download-or-extract-delta-w-source-files-R10-EotWash-MICROSCOPE.md | scripts/Y5_R10_RAB_download_or_extract_delta_w_source_files_R10_EotWash_MICROSCOPE.py | attempt actual source-file acquisition or extraction: download PDFs/portal metadata where accessible, stage R10 curve digitization skeleton, and create EotWash/MICROSCOPE parse blockers if access fails |
