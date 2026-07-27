# 569 Y5 R10 supplement ingest or vector axis-calibrated digitizer

Generated: 2026-06-04T19:05:26.702506+00:00  
Status: `Y5_R10_vector_axis_calibrated_2020_curve_review_candidate_no_claim`  
Claim ceiling: `review_grade_vector_digitization_only_no_live_R10_claim_no_local_GR_pass`  
Next target: `570-Y5-R10-review-candidate-bound-curve-runner-and-MTS-coefficient-pressure.md`

## Verdict
- The vector fallback is now substantially stronger: the rendered figure gives visible axis labels, and the extracted purple `Eot-Wash 2020` curve recovers the paper's `alpha=1` at `lambda=38.6 um` anchor.
- A numeric review-candidate bound curve was written, with `390` positive `lambda/alpha` rows.
- It is still not a live claim curve. Every candidate row is `valid_for_claim=false` until supplemental-table or human visual QA promotes it.
- This means the next private test can quantify coefficient pressure without pretending MTS has passed R10/local-GR.

## Render Evidence
| render_path | rendered | width_px | height_px | notes |
| --- | --- | --- | --- | --- |
| source-intake/local_bounds/downloads/arxiv_2002_11761/source_extract/fig5b1_render_300dpi.png | true | 1980 | 1724 | rendered from vector PDF for visual axis/label QA |

## Axis Calibration
| axis_id | axis | pdf_coordinate | physical_value | physical_units | abs_log10_residual | calibration_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| x_major_10um | x_lambda | 2102.79 | 1e-05 | m | 1.3245699772568287e-06 | axis_label_visual_and_tick_geometry_agree | false |
| x_major_100um | x_lambda | 3361.06 | 0.0001 | m | 2.6491294304875623e-06 | axis_label_visual_and_tick_geometry_agree | false |
| x_major_1mm | x_lambda | 4619.34 | 0.001 | m | 1.3245594510102876e-06 | axis_label_visual_and_tick_geometry_agree | false |
| y_major_1e-3 | y_alpha | 775.344 | 0.001 | dimensionless | 8.799315780860795e-05 | axis_label_visual_and_tick_geometry_agree | false |
| y_major_1e-2 | y_alpha | 1115.5 | 0.01 | dimensionless | 0.00038947790894194867 | axis_label_visual_and_tick_geometry_agree | false |
| y_major_1e-1 | y_alpha | 1455.36 | 0.1 | dimensionless | 3.655486483289394e-06 | axis_label_visual_and_tick_geometry_agree | false |
| y_major_1e0 | y_alpha | 1795.23 | 1.0 | dimensionless | 0.000367376568997102 | axis_label_visual_and_tick_geometry_agree | false |
| y_major_1e1 | y_alpha | 2135.38 | 10.0 | dimensionless | 9.244711000633288e-05 | axis_label_visual_and_tick_geometry_agree | false |
| y_major_1e2 | y_alpha | 2475.25 | 100.0 | dimensionless | 0.00027127397250747975 | axis_label_visual_and_tick_geometry_agree | false |
| y_major_1e3 | y_alpha | 2815.4 | 1000.0 | dimensionless | 0.00018854970649595515 | axis_label_visual_and_tick_geometry_agree | false |
| y_major_1e4 | y_alpha | 3155.27 | 10000.0 | dimensionless | 0.0001751713760169693 | axis_label_visual_and_tick_geometry_agree | false |
| y_major_1e5 | y_alpha | 3495.43 | 100000.0 | dimensionless | 0.00031406461589700285 | axis_label_visual_and_tick_geometry_agree | false |
| y_major_1e6 | y_alpha | 3835.29 | 1000000.0 | dimensionless | 7.906877952823521e-05 | axis_label_visual_and_tick_geometry_agree | false |

## Curve Identity
| identity_id | curve_id | evidence | status | valid_for_claim |
| --- | --- | --- | --- | --- |
| CI569_0_visual_label | Lee_Adelberger_Cook_Fleischer_Heckel_2020_EotWash_vector_curve | rendered figure label 'Eot-Wash 2020' points by arrow to the purple thick curve | visual_qa_pass_by_codex_render | false |
| CI569_1_anchor_recovery | Lee_Adelberger_Cook_Fleischer_Heckel_2020_EotWash_vector_curve | candidate nearest alpha=1 anchor gives lambda=3.866316691563022e-05 and alpha=0.9915372447041295 | pass_review_candidate | false |
| CI569_2_row_count | Lee_Adelberger_Cook_Fleischer_Heckel_2020_EotWash_vector_curve | extracted_rows=390 from color=0.333008 0 1 stroke=13.0392 | pass_review_candidate | false |

## Candidate Curve Samples
| bound_id | lambda_value | alpha_bound | log10_lambda | log10_alpha | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| R10_VECTOR_2020_REVIEW_0000 | 5.894419132271889e-06 | 897932.2928704522 | -5.229558986171696 | 5.953243590630186 | false |
| R10_VECTOR_2020_REVIEW_0195 | 7.355973827852426e-05 | 0.14850286746800798 | -4.133359824626931 | -0.8282651603972084 | false |
| R10_VECTOR_2020_REVIEW_0389 | 0.0010099153351819316 | 0.019113309433552817 | -2.995715033152519 | -1.718664109162002 | false |

## Anchor Recovery
| anchor_id | target_lambda_m | target_alpha | candidate_lambda_m | candidate_alpha | lambda_relative_error | alpha_log10_error | recovery_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AR569_0_paper_alpha1_38p6um | 3.86e-05 | 1.0 | 3.866316691563022e-05 | 0.9915372447041295 | 0.0016364485914564457 | 0.0036909679279784123 | pass_review_candidate | false |

## Promotion Gate
| gate_id | gate | result | required_for_promotion | valid_for_claim |
| --- | --- | --- | --- | --- |
| PG569_0_numeric_rows | candidate has positive numeric lambda/alpha rows | pass | true | false |
| PG569_1_axis_labels | rendered figure axis labels mapped to vector tick geometry | pass | true | false |
| PG569_2_anchor_recovery | candidate recovers alpha=1 at 38.6 micrometers | pass | true | false |
| PG569_3_curve_identity | Eot-Wash 2020 label/arrow maps to extracted purple curve | pass | true | false |
| PG569_4_supplement_or_human_QA | supplemental table or human visual QA confirms the extracted curve | blocked | true | false |
| PG569_5_live_file_update | live claim curve replaced only after QA and provenance signoff | blocked | true | false |

## Diagnostic Status
| status_id | path | rows | status | valid_rows_for_claim | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| DS569_0_review_candidate | source-intake/local_bounds/R10_alpha_lambda_bound_curve_VECTOR_2020_REVIEW_CANDIDATE.csv | 390 | numeric_review_candidate_not_live_claim | 0 | false |
| DS569_1_live_claim_curve | source-intake/local_bounds/R10_alpha_lambda_bound_curve_DIGITIZED.csv | 2 | placeholder_retained | 0 | false |

## Blocker Ledger
| blocker_id | blocker | why_it_matters | next_action | claim_blocked |
| --- | --- | --- | --- | --- |
| B569_0_candidate_not_promoted | Vector extraction is review-grade but not promoted to live claim curve. | Internal evidence can guide coefficient pressure, but public/local-GR claims need stronger provenance. | Run diagnostic comparator against candidate with explicit non-claim mode, or get supplemental table. | true |
| B569_1_supplement_missing | Supplemental numerical table remains inaccessible from CLI. | The table is the cleanest way to replace figure digitization uncertainty. | Manual browser download or alternate mirror lookup. | true |
| B569_2_mts_alpha_coefficients_missing | MTS finite-alpha coefficients remain symbolic. | A real external curve only matters for R10 once alpha_X(lambda) is numeric or theorem-zero. | Fill or bound K_X, Qbar_XH(lambda), qbar_XT, Z_X, and M_X^2. | true |

## Decision
| decision_id | decision | meaning | status | next_target |
| --- | --- | --- | --- | --- |
| D569_0_vector_candidate_built | axis-calibrated Eot-Wash 2020 vector candidate is now available | R10 external bound curve is no longer only anchors; it is a review-grade numeric candidate | candidate_nonclaim | 570-Y5-R10-review-candidate-bound-curve-runner-and-MTS-coefficient-pressure.md |
| D569_1_live_claim_stays_blocked | do not update live R10 claim curve yet | supplement/human QA and MTS coefficients are still missing | blocked_for_claim | 570-Y5-R10-review-candidate-bound-curve-runner-and-MTS-coefficient-pressure.md |
| D569_2_next_pressure | use candidate curve to quantify coefficient pressure next | diagnostic-only runner can show what alpha_X(lambda) would need to beat | next_required | 570-Y5-R10-review-candidate-bound-curve-runner-and-MTS-coefficient-pressure.md |

## Validation
| check_id | result | detail |
| --- | --- | --- |
| V569_0_prior_568_clean | pass | prior_validation_rows=8;prior_fails=0 |
| V569_1_render_exists | pass | rendered=true;path=source-intake/local_bounds/downloads/arxiv_2002_11761/source_extract/fig5b1_render_300dpi.png;size=1980x1724 |
| V569_2_axis_calibration_low_residual | pass | axis_rows=13;max_abs_log10_residual=0.00038947790894194867 |
| V569_3_curve_candidate_numeric | pass | curve_rows=390;numeric_positive=390 |
| V569_4_anchor_recovery | pass | recovery_status=pass_review_candidate;lambda=3.866316691563022e-05;alpha=0.9915372447041295 |
| V569_5_candidate_not_claim | pass | valid_for_claim_true_rows=0 |
| V569_6_live_claim_curve_unchanged | pass | live_status=placeholder_retained;live_rows=2 |
| V569_7_promotion_still_blocked | pass | blocked_gates=2 |
| V569_8_no_overclaim | pass | review_candidate=true;live_claim_curve=false;MTS_alpha_numeric=false;R10_pass=false;local_GR=false |

## Route Update
| route_id | allowed_after_569 | forbidden_after_569 | next_action |
| --- | --- | --- | --- |
| RU569_0_data_route | Use the vector 2020 candidate for private diagnostic coefficient pressure. | Treat the candidate as a live source-backed claim curve without QA. | 570-Y5-R10-review-candidate-bound-curve-runner-and-MTS-coefficient-pressure.md |
| RU569_1_supplement_route | Replace or validate the candidate using the supplemental numerical table if obtained. | Ignore the supplement if it contradicts the vector candidate. | manual/browser supplemental ingest remains best provenance upgrade |
| RU569_2_theory_route | Turn the candidate into bounds on K_X Qbar_XH qbar_XT as a non-claim diagnostic. | Claim MTS passes R10 while MTS alpha coefficients are symbolic. | build diagnostic runner against symbolic coefficient envelopes |

## Practical Read
This is the first point where the local R10 test route has a real-shaped external curve instead of just a threshold anchor. The curve is not promoted, but it is good enough for a disciplined private diagnostic: it tells us the approximate `alpha_bound(lambda)` wall that any finite MTS `X` branch has to duck under. The next round should run this candidate as a non-claim comparator and translate it into pressure on `K_X Qbar_XH(lambda) qbar_XT`, while continuing the derivation route toward theorem-zero if possible.
