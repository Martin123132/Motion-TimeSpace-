# 568 Y5 R10 real bound curve digitization or coefficient prior scan

Generated: 2026-06-04T18:55:08.942831+00:00  
Status: `Y5_R10_real_curve_source_found_supplement_blocked_vector_fallback_nonclaim`  
Claim ceiling: `source_acquisition_and_vector_scout_only_no_R10_bound_curve_claim_no_local_GR_pass`  
Next target: `569-Y5-R10-supplement-ingest-or-vector-axis-calibrated-digitizer.md`

## Verdict
- The real R10 curve route improved: the arXiv source package and vector figure are now local, and the TeX text confirms the paper scanned 66 lambda values and says numerical alpha constraints are in supplemental material.
- The cleanest numerical table is not acquired yet: the APS supplemental link is present but direct CLI access is blocked by a Cloudflare/403 JavaScript challenge.
- The fallback is viable but non-claim: `fig5b1.pdf` contains extractable vector path groups, but axis labels and curve identities still need calibration.
- Therefore R10 remains blocked for evidence, while the next useful move is either supplemental ingest or an axis-calibrated vector digitizer.

## Acquisition Status
| artifact_id | path | role | exists | bytes | access_result | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| AQ568_0_arxiv_eprint | source-intake/local_bounds/downloads/arxiv_2002_11761/2002.11761.eprint | downloaded arXiv source package | true | 530474 | present | false |
| AQ568_1_arxiv_pdf | source-intake/local_bounds/downloads/arxiv_2002_11761/2002.11761.pdf | downloaded arXiv PDF | true | 856030 | present | false |
| AQ568_2_tex_source | source-intake/local_bounds/downloads/arxiv_2002_11761/source_extract/FB_ISL_pdf.tex | extractable TeX source from arXiv package | true | 25056 | present | false |
| AQ568_3_fig5b_vector_pdf | source-intake/local_bounds/downloads/arxiv_2002_11761/source_extract/fig5b1.pdf | vector figure containing alpha(lambda) constraints plot | true | 65659 | present | false |
| AQ568_4_aps_harvest_fulltext | source-intake/local_bounds/downloads/aps_prl_124_101101/https_harvest_aps_org_v2_journals_articles_10_1103_PhysRevLett_124_101101_fulltext.html | APS harvest fulltext PDF copy | true | 594127 | present | false |
| AQ568_5_aps_supplement_attempt | source-intake/local_bounds/downloads/aps_prl_124_101101/link_aps_supplemental_attempt.html | direct APS supplemental access attempt output | true | 5788 | blocked_cloudflare_or_js_challenge | false |
| AQ568_6_live_digitized_placeholder | source-intake/local_bounds/R10_alpha_lambda_bound_curve_DIGITIZED.csv | live claim curve placeholder retained unchanged | true | 778 | present | false |
| AQ568_7_anchor_smoke_curve | source-intake/local_bounds/R10_alpha_lambda_bound_curve_ANCHOR_SMOKE.csv | source-backed anchor-only smoke curve retained | true | 1064 | present | false |

## Source Text Evidence
| evidence_id | source_file | line_number | matched | meaning | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| TE568_0_abstract_anchor | source-intake/local_bounds/downloads/arxiv_2002_11761/source_extract/FB_ISL_pdf.tex | 33 | true | paper threshold anchor: gravitational-strength Yukawa ranges below 38.6 micrometers | false |
| TE568_1_yukawa_law | source-intake/local_bounds/downloads/arxiv_2002_11761/source_extract/FB_ISL_pdf.tex | 43 | true | paper defines the standard Yukawa alpha-lambda comparison law | false |
| TE568_2_scan_count | source-intake/local_bounds/downloads/arxiv_2002_11761/source_extract/FB_ISL_pdf.tex | 150 | true | paper reports alpha constraints for 66 assumed lambda values | false |
| TE568_3_supplement_table | source-intake/local_bounds/downloads/arxiv_2002_11761/source_extract/FB_ISL_pdf.tex | 151 | true | paper says numerical alpha-constraint values are in supplemental material | false |

## Supplemental Access Ledger
| attempt_id | url | result | contains_machine_readable_table | valid_for_claim | next_action |
| --- | --- | --- | --- | --- | --- |
| SA568_0 | https://journals.aps.org/prl/supplemental/10.1103/PhysRevLett.124.101101/supplement.pdf | direct_candidate_not_downloaded_or_forbidden | false | false | open in browser/manual download or locate alternate public mirror/data package |
| SA568_1 | https://journals.aps.org/prl/supplemental/10.1103/PhysRevLett.124.101101/supplemental.pdf | direct_candidate_not_downloaded_or_forbidden | false | false | open in browser/manual download or locate alternate public mirror/data package |
| SA568_2 | https://journals.aps.org/prl/supplemental/10.1103/PhysRevLett.124.101101/Supplemental_Material.pdf | direct_candidate_not_downloaded_or_forbidden | false | false | open in browser/manual download or locate alternate public mirror/data package |
| SA568_3 | https://journals.aps.org/prl/supplemental/10.1103/PhysRevLett.124.101101/FB_ISL_supp.pdf | direct_candidate_not_downloaded_or_forbidden | false | false | open in browser/manual download or locate alternate public mirror/data package |
| SA568_4 | https://journals.aps.org/prl/supplemental/10.1103/PhysRevLett.124.101101/FB_ISL_supplement.pdf | direct_candidate_not_downloaded_or_forbidden | false | false | open in browser/manual download or locate alternate public mirror/data package |
| SA568_5 | http://link.aps.org/supplemental/10.1103/PhysRevLett.124.101101 | blocked_cloudflare_403_js_challenge | false | false | open in browser/manual download or locate alternate public mirror/data package |

## Vector Figure Audit
| audit_id | source_file | result | detail | valid_for_claim |
| --- | --- | --- | --- | --- |
| VF568_0_vector_file | source-intake/local_bounds/downloads/arxiv_2002_11761/source_extract/fig5b1.pdf | present | bytes=65659 | false |
| VF568_1_content_stream | source-intake/local_bounds/downloads/arxiv_2002_11761/source_extract/fig5b1.pdf | parsed | content_stream_bytes=259702;nonblack_inplot_segments=2836;groups=21 | false |
| VF568_2_text_labels | source-intake/local_bounds/downloads/arxiv_2002_11761/source_extract/fig5b1.pdf | not_extractable_by_pypdf | figure labels are vector paths, not extractable text; axis calibration cannot be verified automatically yet | false |

## Vector Path Scout
| scout_id | color_rgb | stroke_width | segment_count | x_pdf_min | x_pdf_max | y_pdf_min | y_pdf_max | digitization_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| VS568_0 | 0.333008 0 1 | 8.5038 | 626 | 3582.73 | 4496.04 | 2297.52 | 2695.5 | raw_vector_group_only_axis_unresolved | false |
| VS568_1 | 0.333008 0 1 | 13.0392 | 387 | 1813.94 | 4624.73 | 901.199 | 3819.42 | raw_vector_group_only_axis_unresolved | false |
| VS568_2 | 1 0.5 0 | 7.65342 | 311 | 1980.9 | 2861.04 | 1056.82 | 1158.86 | raw_vector_group_only_axis_unresolved | false |
| VS568_3 | 1 0.667969 0.667969 | 6.51958 | 268 | 1691.2 | 4624.73 | 1669.66 | 3826.22 | raw_vector_group_only_axis_unresolved | false |
| VS568_4 | 1 1 0.5 | 6.51958 | 263 | 1223.21 | 4624.73 | 821.262 | 3835.29 | raw_vector_group_only_axis_unresolved | false |
| VS568_5 | 0.333008 0 1 | 0 | 126 | 2361.59 | 3661.82 | 1899.83 | 2490.56 | raw_vector_group_only_axis_unresolved | false |
| VS568_6 | 1 0 1 | 7.65342 | 125 | 1444.88 | 1768.87 | 2297.52 | 2374.06 | raw_vector_group_only_axis_unresolved | false |
| VS568_7 | 0 1 0.5 | 7.65342 | 116 | 1444.88 | 1730.6 | 1062.77 | 1139.3 | raw_vector_group_only_axis_unresolved | false |

## Axis Calibration Requirements
| requirement_id | need | current_state | acceptance_for_claim | valid_for_claim |
| --- | --- | --- | --- | --- |
| AC568_0_x_axis_units | map raw x PDF coordinates to lambda values | plot vector coordinates found but tick labels are path glyphs | two or more independently verified x-axis tick labels, preferably all major ticks | false |
| AC568_1_y_axis_units | map raw y PDF coordinates to abs(alpha) values | plot vector coordinates found but y-axis log labels are path glyphs | two or more independently verified y-axis tick labels, preferably all major ticks | false |
| AC568_2_curve_identity | separate Lee 2020 constraint curve from prior-work curves, legend strokes, glyphs, and tick marks | color groups extracted without semantic curve identity | source caption/legend or manual visual QA maps each extracted group to a named experiment | false |
| AC568_3_machine_table_preferred | ingest supplemental numerical alpha constraints if accessible | paper says supplemental has numerical values; direct link is Cloudflare/403 blocked in CLI | downloaded supplemental PDF/table or alternate official machine-readable rows | false |

## Bound Curve Candidate Status
| candidate_id | path | row_count | status | valid_rows_for_claim | valid_for_claim | notes |
| --- | --- | --- | --- | --- | --- | --- |
| BC568_0_live_digitized_claim_file | source-intake/local_bounds/R10_alpha_lambda_bound_curve_DIGITIZED.csv | 2 | placeholder_claim_blocked | 0 | false | Retained unchanged; still contains placeholder rows rather than real digitized curve. |
| BC568_1_anchor_smoke | source-intake/local_bounds/R10_alpha_lambda_bound_curve_ANCHOR_SMOKE.csv | 2 | anchor_only_noncurve | 0 | false | Useful threshold anchors only; not a full alpha(lambda) curve. |
| BC568_2_vector_path_scout | source-intake/local_bounds/R10_alpha_lambda_bound_curve_VECTOR_PATH_SCOUT_NONCLAIM.csv | 21 | raw_vector_groups_axis_unresolved | 0 | false | Proves vector fallback exists; cannot become alpha(lambda) until axis and curve identity are calibrated. |

## Coefficient Prior Scan Plan
| plan_id | parameter | suggested_domain | status_after_acquisition | reason | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| CPS568_0 | lambda_X | 3.0e-5 m <= lambda_X <= 6.5e-5 m | allowed_as_nonclaim_only | real alpha_bound(lambda) curve is not yet claim-grade | false |
| CPS568_1 | lambda_X | 1.0e-6 m <= lambda_X <= 1.0e-2 m | allowed_as_nonclaim_only | real alpha_bound(lambda) curve is not yet claim-grade | false |
| CPS568_2 | abs(K_X*Qbar_XH*qbar_XT) | log10 product from -30 to +3 | allowed_as_nonclaim_only | real alpha_bound(lambda) curve is not yet claim-grade | false |
| CPS568_3 | s_X | -1,+1 | allowed_as_nonclaim_only | real alpha_bound(lambda) curve is not yet claim-grade | false |
| CPS568_4 | Qbar_XH(lambda) | parent integral or channelwise bound required | allowed_as_nonclaim_only | real alpha_bound(lambda) curve is not yet claim-grade | false |
| CPS568_5 | qbar_XT | zero theorem or residual bound required | allowed_as_nonclaim_only | real alpha_bound(lambda) curve is not yet claim-grade | false |

## Blocker Ledger
| blocker_id | blocker | why_it_matters | next_action | claim_blocked |
| --- | --- | --- | --- | --- |
| B568_0_supplement_access | The paper states numerical alpha constraints are in supplemental material, but direct CLI access hits a Cloudflare/403 JavaScript challenge. | The supplemental table would be the cleanest claim-grade curve source. | Use browser/manual download or locate an alternate official mirror. | true |
| B568_1_axis_calibration | The vector figure paths are extractable but axis labels are not text-extractable. | Raw PDF path coordinates are not physical lambda/alpha rows. | Build an axis-calibrated digitizer with manually verified tick anchors. | true |
| B568_2_curve_identity | The bottom figure combines this and previous work; color groups are not yet semantically assigned. | We must not accidentally use a prior-work curve as the 2020 Lee curve or vice versa. | Map legend/curve identity before any full curve file is promoted. | true |

## Decision
| decision_id | decision | meaning | status | next_target |
| --- | --- | --- | --- | --- |
| D568_0_real_curve_source_identified | real numerical curve source is identified but not acquired | the paper explicitly points to supplemental numerical alpha constraints | source_found_access_blocked | 569-Y5-R10-supplement-ingest-or-vector-axis-calibrated-digitizer.md |
| D568_1_vector_fallback_retained | retain vector digitization fallback | fig5b1.pdf contains extractable vector path groups, but needs calibration | fallback_nonclaim | 569-Y5-R10-supplement-ingest-or-vector-axis-calibrated-digitizer.md |
| D568_2_prior_scan_only_nonclaim | coefficient prior scan remains diagnostic only | without a real curve, coefficient scanning cannot become evidence | nonclaim_only | 569-Y5-R10-supplement-ingest-or-vector-axis-calibrated-digitizer.md |

## Validation
| check_id | result | detail |
| --- | --- | --- |
| V568_0_prior_567_clean | pass | prior_validation_rows=9;prior_fails=0 |
| V568_1_source_package_present | pass | arxiv_eprint=true;tex=true |
| V568_2_source_text_evidence_found | pass | matched=4;expected=4 |
| V568_3_supplement_access_blocked_recorded | pass | supplement_blocked=true;attempts=6 |
| V568_4_vector_figure_parsed | pass | vector_groups=21 |
| V568_5_live_claim_curve_still_blocked | pass | live_rows=2;placeholder_marker=true |
| V568_6_no_claim_rows | pass | valid_for_claim_true_rows=0 |
| V568_7_no_overclaim | pass | supplement_table_ingested=false;axis_calibrated=false;curve_identity_verified=false;R10_pass=false;local_GR=false |

## Route Update
| route_id | allowed_after_568 | forbidden_after_568 | next_action |
| --- | --- | --- | --- |
| RU568_0_best_next | Try to ingest the supplemental numerical table by browser/manual download. | Pretend the blocked supplemental table has been acquired. | 569-Y5-R10-supplement-ingest-or-vector-axis-calibrated-digitizer.md |
| RU568_1_vector_route | Build an axis-calibrated vector digitizer using verified tick anchors and curve identity mapping. | Promote raw PDF path coordinates directly to lambda/alpha rows. | calibrate x-axis, y-axis, and experiment curve identity |
| RU568_2_theory_route | Run coefficient priors only as explicit non-claim diagnostics. | Use prior-scan survival as R10 evidence while external curve is non-claim. | keep deriving qbar_XT, Qbar_XH(lambda), Z_X, and M_X^2 |

## Practical Read
This is not grim; it is a data-access fork, not a physics failure. The paper itself tells us the exact thing we need exists: numerical alpha constraints in the supplemental material. The CLI cannot currently pull that supplemental link because APS/link.aps is throwing a JavaScript challenge. Meanwhile the source package gives us a vector figure fallback. The next hard-nosed move is either to ingest the supplemental file manually or build the vector digitizer with explicit axis anchors, while keeping all coefficient scans non-claim until the external curve is real.
