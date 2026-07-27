# 1495 - R10 alpha(lambda) Curve Digitization or Machine-Readable Table Hunt

## Verdict
- The R10 source archive/table/figure route has been tested and ledgered.
- Any source assets found remain nonclaim: the live `R10_alpha_lambda_bound_curve_DIGITIZED.csv` and `R10_delta_w_kernel_lambda.csv` are not promoted.
- R10 can only become score-ready after a validated curve and the same-branch `delta_w -> alpha(lambda)` kernel both exist.

## Archive Acquisition
| archive_id | download_status | http_status | byte_count | local_path |
| --- | --- | --- | --- | --- |
| ARCH1495_R10_ARXIV_SOURCE | DOWNLOADED_SOURCE_ARCHIVE_NONCLAIM | 200 | 530474 | source-intake\r10\raw\Lee_2020_PRL_2002.11761_source.tar.gz |

## Archive Manifest Summary
| file_role_guess | count |
| --- | --- |
| figure_or_graphic_asset | 10 |
| source_text | 1 |

## Source Anchor Scan Preview
| pattern_name | scan_status | file_path |
| --- | --- | --- |
| alpha_lambda_yukawa | SOURCE_PATTERN_FOUND_NONCLAIM | source-intake\r10\raw\Lee_2020_PRL_2002.11761_source_1495\FB_ISL_pdf.tex |
| lambda_threshold_38p6 | SOURCE_PATTERN_FOUND_NONCLAIM | source-intake\r10\raw\Lee_2020_PRL_2002.11761_source_1495\FB_ISL_pdf.tex |
| confidence_95 | SOURCE_PATTERN_FOUND_NONCLAIM | source-intake\r10\raw\Lee_2020_PRL_2002.11761_source_1495\FB_ISL_pdf.tex |
| figure_reference | SOURCE_PATTERN_FOUND_NONCLAIM | source-intake\r10\raw\Lee_2020_PRL_2002.11761_source_1495\FB_ISL_pdf.tex |
| separation_range | SOURCE_PATTERN_FOUND_NONCLAIM | source-intake\r10\raw\Lee_2020_PRL_2002.11761_source_1495\FB_ISL_pdf.tex |

## Machine Table Hunt
| table_id | file_path | table_status | required_validation |
| --- | --- | --- | --- |
| TAB1495_no_machine_table | not_found_in_arxiv_source_archive | NO_MACHINE_READABLE_TABLE_FOUND | manual figure digitization or external primary-source table required |

## Figure Digitization Targets
| figure_id | file_path | figure_status | priority | required_output |
| --- | --- | --- | --- | --- |
| FIG1495_0 | source-intake\r10\raw\Lee_2020_PRL_2002.11761_source_1495\capAF.pdf | FIGURE_ASSET_FOUND_MANUAL_DIGITIZATION_REQUIRED | medium | source-intake\r10\derived\R10_alpha_lambda_bound_curve_DIGITIZED.csv |
| FIG1495_1 | source-intake\r10\raw\Lee_2020_PRL_2002.11761_source_1495\capPF.pdf | FIGURE_ASSET_FOUND_MANUAL_DIGITIZATION_REQUIRED | medium | source-intake\r10\derived\R10_alpha_lambda_bound_curve_DIGITIZED.csv |
| FIG1495_2 | source-intake\r10\raw\Lee_2020_PRL_2002.11761_source_1495\fig1.pdf | FIGURE_ASSET_FOUND_MANUAL_DIGITIZATION_REQUIRED | high | source-intake\r10\derived\R10_alpha_lambda_bound_curve_DIGITIZED.csv |
| FIG1495_3 | source-intake\r10\raw\Lee_2020_PRL_2002.11761_source_1495\fig2a.pdf | FIGURE_ASSET_FOUND_MANUAL_DIGITIZATION_REQUIRED | high | source-intake\r10\derived\R10_alpha_lambda_bound_curve_DIGITIZED.csv |
| FIG1495_4 | source-intake\r10\raw\Lee_2020_PRL_2002.11761_source_1495\fig2b.pdf | FIGURE_ASSET_FOUND_MANUAL_DIGITIZATION_REQUIRED | high | source-intake\r10\derived\R10_alpha_lambda_bound_curve_DIGITIZED.csv |
| FIG1495_5 | source-intake\r10\raw\Lee_2020_PRL_2002.11761_source_1495\fig5a.pdf | FIGURE_ASSET_FOUND_MANUAL_DIGITIZATION_REQUIRED | high | source-intake\r10\derived\R10_alpha_lambda_bound_curve_DIGITIZED.csv |
| FIG1495_6 | source-intake\r10\raw\Lee_2020_PRL_2002.11761_source_1495\fig5b1.pdf | FIGURE_ASSET_FOUND_MANUAL_DIGITIZATION_REQUIRED | high | source-intake\r10\derived\R10_alpha_lambda_bound_curve_DIGITIZED.csv |
| FIG1495_7 | source-intake\r10\raw\Lee_2020_PRL_2002.11761_source_1495\magsysZB.pdf | FIGURE_ASSET_FOUND_MANUAL_DIGITIZATION_REQUIRED | medium | source-intake\r10\derived\R10_alpha_lambda_bound_curve_DIGITIZED.csv |
| FIG1495_8 | source-intake\r10\raw\Lee_2020_PRL_2002.11761_source_1495\magsysZs.pdf | FIGURE_ASSET_FOUND_MANUAL_DIGITIZATION_REQUIRED | medium | source-intake\r10\derived\R10_alpha_lambda_bound_curve_DIGITIZED.csv |
| FIG1495_9 | source-intake\r10\raw\Lee_2020_PRL_2002.11761_source_1495\xyCenter.pdf | FIGURE_ASSET_FOUND_MANUAL_DIGITIZATION_REQUIRED | medium | source-intake\r10\derived\R10_alpha_lambda_bound_curve_DIGITIZED.csv |

## Curve Status
| curve_status_id | curve_status | machine_table_candidate | figure_asset_candidate | text_threshold_anchor | next_action |
| --- | --- | --- | --- | --- | --- |
| CURVE1495_0_R10_alpha_lambda | FIGURE_ASSET_FOUND_DIGITIZATION_REQUIRED | False | True | True | digitize alpha(lambda) curve from source figure asset |

## Kernel Input Contract
| kernel_input_id | required_input | input_owner | current_status | failure_effect |
| --- | --- | --- | --- | --- |
| KERN1495_0_curve | R10 alpha(lambda) bound curve | empirical_input | MISSING_OR_UNPROMOTED | R10 delta_w score remains blocked |
| KERN1495_1_geometry | R10 test/source geometry response function | experimental_projection | MISSING | R10 delta_w score remains blocked |
| KERN1495_2_basis | delta_w component basis and units | theory_projection | MISSING | R10 delta_w score remains blocked |
| KERN1495_3_parent | parent coupling normalization or explicit residual prior | parent_action_input | FORBIDDEN_TO_IMPORT_UNDER_1495 | R10 delta_w score remains blocked |
| KERN1495_4_mapping | map from delta_w residual to Yukawa alpha convention | same_branch_kernel | MISSING | R10 delta_w score remains blocked |

## Validation
| check_id | result | detail |
| --- | --- | --- |
| VAL1495_0_local_sources | PASS | all cited 1494 local source paths exist |
| VAL1495_1_archive_attempt | PASS | archive status=DOWNLOADED_SOURCE_ARCHIVE_NONCLAIM |
| VAL1495_2_archive_hash | PASS | downloaded archive has sha256 and byte_count over threshold or failure is explicit |
| VAL1495_3_manifest | PASS | archive manifest/blocker row written |
| VAL1495_4_scan | PASS | TeX/source scan rows written |
| VAL1495_5_curve_not_promoted | PASS | R10 curve/kernel live targets remain absent |
| VAL1495_6_readiness_blocked | PASS | delta_w/R10 score readiness remains false |
| VAL1495_7_Cparent_refused | PASS | C_parent import was not performed |
| VAL1495_8_csv_parse | PASS | all generated 1495 CSVs parse cleanly |
| VAL1495_9_branch_copies | PASS | branch/quarantine nonclaim copies written |
| VAL1495_10_pycache_absent | PASS | scripts __pycache__ absent after run |
| VAL1495_11_formalization_untouched | PASS | formalization modified-file count since start=0 |
| VAL1495_12_claim_flags_false | PASS | all generated prediction/claim flags remain false |
| VAL1495_13_overall | PASS | 1495 hunted R10 source archive/table/figure route and kept curve/kernel nonclaim |

## Next Target
| next_id | next_target | script | objective |
| --- | --- | --- | --- |
| NEXT1495_0_1496 | 1496-Y5-R10-RAB-R10-source-figure-axis-detection-and-digitization-stub.md | scripts/Y5_R10_RAB_R10_source_figure_axis_detection_and_digitization_stub.py | inspect source figure assets, identify alpha(lambda) axes, and produce a nonclaim digitization template with units/confidence gates |
