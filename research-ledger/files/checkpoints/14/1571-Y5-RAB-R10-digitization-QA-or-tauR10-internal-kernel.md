# 1571 - R_AB R10 Digitization QA or tau_R10 Internal Kernel

## Verdict
- The R10 Fig. 2 curve is now a cleaner QA candidate: blue connected components were classified, likely label/axis text rejected, and a trace overlay was written.
- The cleaned curve is still not accepted evidence; it remains a private nonclaim input for smoke tooling until independent/manual QA verifies the axis and curve trace.
- The theory side is unchanged in the important way: the internal `tau_R10` source-normalized kernel is still missing.
- No R10 pass, local GR/Newton reduction, PPN, WEP, clock, orbital, `Z_R=0`, or `q_R=0` claim is made.

## Source Register
| source_id | source_path | exists | needle_found | needles |
| --- | --- | --- | --- | --- |
| SRC1571_0_1570_doc | 1570-Y5-RAB-R10-curve-digitization-or-tau-kernel-source-normalization.md | True | True | candidate blue-curve digitization; internal MTS side is still missing |
| SRC1571_1_1570_validation | source-intake/mts_residuals/P8_Y5_BRR545_1570_VALIDATION.csv | True | True | VAL1570_OVERALL; PASS |
| SRC1571_2_1570_curve | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1570_R10_ALPHA_LAMBDA_DIGITIZED_CANDIDATE.csv | True | True | DIG1570_000; CANDIDATE_IMAGE_TRACE_NONCLAIM |
| SRC1571_3_1570_method | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1570_R10_DIGITIZATION_METHOD.csv | True | True | METHOD1570_3_acceptance; NOT_ACCEPTED |
| SRC1571_4_1570_tau | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1570_TAU_KERNEL_SOURCE_NORMALIZATION_GATE.csv | True | True | TAUG1570_4_verdict; NOT_READY |
| SRC1571_5_fig2 | source-intake/rab-sector/external/r10/1570/extracted_images/page_5_image_1_Im3.png | True | True |  |
| SRC1571_6_text | source-intake/rab-sector/external/r10/1570/aps_harvest_fulltext.txt | True | True | FIG. 2. Constraints on Y; function of λ |
| SRC1571_7_pdf | source-intake/rab-sector/external/r10/1570/aps_harvest_fulltext.pdf | True | True | Combined Test of the Gravitational Inverse-Square Law at the Centimeter Range |
| SRC1571_8_1569_tau | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1569_TAU_R10_PROJECTION_ATTEMPT.csv | True | True | TAU1569_3_projection_kernel; KERNEL_CONTRACT_WRITTEN_NOT_FILLED |

## Blue Component QA Audit
| component_id | pixel_count | min_x | max_x | min_y | max_y | qa_status | reason |
| --- | --- | --- | --- | --- | --- | --- | --- |
| COMP1571_00 | 1291 | 139 | 282 | 20 | 430 | KEEP_CURVE_CANDIDATE | large/medium blue component in plot region above label band |
| COMP1571_01 | 501 | 872 | 1012 | 203 | 305 | KEEP_CURVE_CANDIDATE | large/medium blue component in plot region above label band |
| COMP1571_02 | 378 | 775 | 863 | 309 | 406 | KEEP_CURVE_CANDIDATE | large/medium blue component in plot region above label band |
| COMP1571_03 | 2425 | 283 | 770 | 414 | 645 | KEEP_CURVE_CANDIDATE | large/medium blue component in plot region above label band |
| COMP1571_04 | 120 | 752 | 770 | 601 | 624 | REJECT_LABEL_OR_AXIS_TEXT | blue text/label band below curve region |
| COMP1571_05 | 146 | 774 | 788 | 601 | 624 | REJECT_LABEL_OR_AXIS_TEXT | blue text/label band below curve region |
| COMP1571_06 | 138 | 883 | 897 | 601 | 624 | REJECT_LABEL_OR_AXIS_TEXT | blue text/label band below curve region |
| COMP1571_07 | 53 | 793 | 795 | 607 | 624 | REJECT_LABEL_OR_AXIS_TEXT | blue text/label band below curve region |
| COMP1571_08 | 129 | 800 | 813 | 607 | 625 | REJECT_LABEL_OR_AXIS_TEXT | blue text/label band below curve region |
| COMP1571_09 | 167 | 826 | 849 | 607 | 624 | REJECT_LABEL_OR_AXIS_TEXT | blue text/label band below curve region |
| COMP1571_10 | 136 | 852 | 867 | 607 | 625 | REJECT_LABEL_OR_AXIS_TEXT | blue text/label band below curve region |
| COMP1571_11 | 72 | 872 | 880 | 607 | 624 | REJECT_LABEL_OR_AXIS_TEXT | blue text/label band below curve region |

## QA Method
| method_id | method_piece | value | status | risk |
| --- | --- | --- | --- | --- |
| QA1571_0_components | blue connected component filtering | kept=4; rejected=8; total=12 | QA_FILTER_APPLIED | curve still image-traced and needs independent/manual acceptance |
| QA1571_1_axis | axis calibration | x_left=114.0, x_decade=243.0, y_top=20.0, y_decade=155.0 | REUSED_1570_MANUAL_CALIBRATION | axis calibration approximate until tick-by-tick QA |
| QA1571_2_centerline | curve y selection | 15th percentile y per x, sampled every 8 pixels | LABEL_CONTAMINATION_REDUCED | may trace upper edge of thick line rather than exact centerline |
| QA1571_3_overlay | visual QA overlay | source-intake/rab-sector/external/r10/1571/R10_fig2_blue_curve_cleaned_trace_overlay_1571.png | OVERLAY_CREATED | human visual pass still required before accepted use |
| QA1571_4_acceptance | accepted curve gate | cleaned_points=108 | NOT_ACCEPTED_NONCLAIM | candidate supports smoke tests only |

## Cleaned Curve Candidate
| point_id | lambda_m | alpha_abs_bound | pixel_x | pixel_y | digitization_status | qa_rule |
| --- | --- | --- | --- | --- | --- | --- |
| QA1571_000 | 0.0012673036 | 1 | 139 | 20.00 | QA_CLEANED_CANDIDATE_NONCLAIM | kept_blue_components_minimized_label_contamination_15th_percentile_y |
| QA1571_001 | 0.0013671069 | 0.71587749 | 147 | 42.50 | QA_CLEANED_CANDIDATE_NONCLAIM | kept_blue_components_minimized_label_contamination_15th_percentile_y |
| QA1571_002 | 0.00147477 | 0.45742783 | 155 | 72.65 | QA_CLEANED_CANDIDATE_NONCLAIM | kept_blue_components_minimized_label_contamination_15th_percentile_y |
| QA1571_003 | 0.0015909118 | 0.29293698 | 163 | 102.65 | QA_CLEANED_CANDIDATE_NONCLAIM | kept_blue_components_minimized_label_contamination_15th_percentile_y |
| QA1571_004 | 0.0017162 | 0.18759696 | 171 | 132.65 | QA_CLEANED_CANDIDATE_NONCLAIM | kept_blue_components_minimized_label_contamination_15th_percentile_y |
| QA1571_005 | 0.001851355 | 0.12193518 | 179 | 161.65 | QA_CLEANED_CANDIDATE_NONCLAIM | kept_blue_components_minimized_label_contamination_15th_percentile_y |
| QA1571_006 | 0.0019971539 | 0.080801487 | 187 | 189.35 | QA_CLEANED_CANDIDATE_NONCLAIM | kept_blue_components_minimized_label_contamination_15th_percentile_y |
| QA1571_007 | 0.0021544347 | 0.054791057 | 195 | 215.50 | QA_CLEANED_CANDIDATE_NONCLAIM | kept_blue_components_minimized_label_contamination_15th_percentile_y |
| QA1571_008 | 0.0023241018 | 0.037402723 | 203 | 241.20 | QA_CLEANED_CANDIDATE_NONCLAIM | kept_blue_components_minimized_label_contamination_15th_percentile_y |
| QA1571_009 | 0.0025071306 | 0.026518465 | 211 | 264.35 | QA_CLEANED_CANDIDATE_NONCLAIM | kept_blue_components_minimized_label_contamination_15th_percentile_y |
| QA1571_010 | 0.0027045734 | 0.018648554 | 219 | 288.05 | QA_CLEANED_CANDIDATE_NONCLAIM | kept_blue_components_minimized_label_contamination_15th_percentile_y |
| QA1571_011 | 0.0029175652 | 0.0136509 | 227 | 309.05 | QA_CLEANED_CANDIDATE_NONCLAIM | kept_blue_components_minimized_label_contamination_15th_percentile_y |
| QA1571_012 | 0.0031473308 | 0.010142127 | 235 | 329.05 | QA_CLEANED_CANDIDATE_NONCLAIM | kept_blue_components_minimized_label_contamination_15th_percentile_y |
| QA1571_013 | 0.0033951909 | 0.0076480089 | 243 | 348.05 | QA_CLEANED_CANDIDATE_NONCLAIM | kept_blue_components_minimized_label_contamination_15th_percentile_y |
| QA1571_014 | 0.0036625706 | 0.0058666084 | 251 | 365.90 | QA_CLEANED_CANDIDATE_NONCLAIM | kept_blue_components_minimized_label_contamination_15th_percentile_y |
| QA1571_015 | 0.0039510072 | 0.0045573216 | 259 | 382.90 | QA_CLEANED_CANDIDATE_NONCLAIM | kept_blue_components_minimized_label_contamination_15th_percentile_y |
| QA1571_016 | 0.0042621588 | 0.0035481339 | 267 | 399.75 | QA_CLEANED_CANDIDATE_NONCLAIM | kept_blue_components_minimized_label_contamination_15th_percentile_y |
| QA1571_017 | 0.0045978144 | 0.0027975264 | 275 | 415.75 | QA_CLEANED_CANDIDATE_NONCLAIM | kept_blue_components_minimized_label_contamination_15th_percentile_y |
| QA1571_018 | 0.0049599038 | 0.0021237176 | 283 | 434.30 | QA_CLEANED_CANDIDATE_NONCLAIM | kept_blue_components_minimized_label_contamination_15th_percentile_y |
| QA1571_019 | 0.0053505085 | 0.0017915371 | 291 | 445.75 | QA_CLEANED_CANDIDATE_NONCLAIM | kept_blue_components_minimized_label_contamination_15th_percentile_y |
| QA1571_020 | 0.0057718744 | 0.0014551348 | 299 | 459.75 | QA_CLEANED_CANDIDATE_NONCLAIM | kept_blue_components_minimized_label_contamination_15th_percentile_y |
| QA1571_021 | 0.0062264239 | 0.0011845363 | 307 | 473.60 | QA_CLEANED_CANDIDATE_NONCLAIM | kept_blue_components_minimized_label_contamination_15th_percentile_y |
| QA1571_022 | 0.0067167703 | 0.0009889203 | 315 | 485.75 | QA_CLEANED_CANDIDATE_NONCLAIM | kept_blue_components_minimized_label_contamination_15th_percentile_y |
| QA1571_023 | 0.0072457326 | 0.00081706774 | 323 | 498.60 | QA_CLEANED_CANDIDATE_NONCLAIM | kept_blue_components_minimized_label_contamination_15th_percentile_y |
| QA1571_024 | 0.0078163521 | 0.0006836577 | 331 | 510.60 | QA_CLEANED_CANDIDATE_NONCLAIM | kept_blue_components_minimized_label_contamination_15th_percentile_y |
| QA1571_025 | 0.0084319093 | 0.00058059189 | 339 | 521.60 | QA_CLEANED_CANDIDATE_NONCLAIM | kept_blue_components_minimized_label_contamination_15th_percentile_y |
| QA1571_026 | 0.0090959431 | 0.00049416385 | 347 | 532.45 | QA_CLEANED_CANDIDATE_NONCLAIM | kept_blue_components_minimized_label_contamination_15th_percentile_y |
| QA1571_027 | 0.0098122713 | 0.00043135885 | 355 | 541.60 | QA_CLEANED_CANDIDATE_NONCLAIM | kept_blue_components_minimized_label_contamination_15th_percentile_y |
| QA1571_028 | 0.010585012 | 0.00037821778 | 363 | 550.45 | QA_CLEANED_CANDIDATE_NONCLAIM | kept_blue_components_minimized_label_contamination_15th_percentile_y |
| QA1571_029 | 0.011418608 | 0.00033088526 | 371 | 559.45 | QA_CLEANED_CANDIDATE_NONCLAIM | kept_blue_components_minimized_label_contamination_15th_percentile_y |

## Curve Comparison
| comparison_id | metric | old_1570 | new_1571 | status | interpretation |
| --- | --- | --- | --- | --- | --- |
| CMP1571_0_point_count | point_count | 78 | 108 | QA_CHANGED_CANDIDATE_TRACE | cleaned component selection may include previously missed curve segment and reduce label contamination |
| CMP1571_1_lambda_range | lambda_m_range | 0.0012673036..4.8667921 | 0.0012673036..4.7303919 | RANGE_RECORDED_NONCLAIM | range check only; not an acceptance test |
| CMP1571_2_alpha_range | alpha_abs_bound_range | 9.493347e-05..1 | 9.6425866e-05..1 | RANGE_RECORDED_NONCLAIM | axis/centerline QA still needed before accepted bound curve |

## tau_R10 Internal Kernel Attempt
| kernel_id | kernel_piece | role | status | blocking_gap |
| --- | --- | --- | --- | --- |
| KERN1571_0_form | alpha_MTS(lambda_R) = tau_R10 * A_R[Z_R,M_R^2,J_R,B_R,readout] | formal bridge to compare with R10 bound curve | FORMAL_KERNEL_SHAPE_ONLY | all source-normalized internal inputs missing |
| KERN1571_1_range | lambda_R = sqrt(Z_R/M_R^2) | sets x-axis location if finite residual branch is active | MISSING_ZR_MR2 | no parent-normalized Z_R or M_R^2 |
| KERN1571_2_source | A_R source amplitude from J_R/B_R/readout coupling to test masses | sets y-axis alpha prediction | MISSING_SOURCE_NORMALIZATION | matter/source/boundary/readout descent not theorem-zeroed and no finite row exists |
| KERN1571_3_bound_eval | pass if abs(alpha_MTS(lambda_R)) <= alpha_bound_digitized(lambda_R) | eventual R10 comparator | BLOCKED_NO_INTERNAL_PREDICTION | external curve cannot be scored alone |
| KERN1571_4_verdict | tau_R10 internal kernel | not ready | NOT_READY | next derivation must fill source normalization or theorem-zero branch |

## Runner
| runner_id | test | current_status | detail |
| --- | --- | --- | --- |
| RUN1571_0_sources | load 1570 assets and handoff | PASS | all source register needles found |
| RUN1571_1_qa_curve | QA-cleaned R10 curve candidate | PASS_QA_CANDIDATE_NONCLAIM | cleaned_points=108; overlay=source-intake/rab-sector/external/r10/1571/R10_fig2_blue_curve_cleaned_trace_overlay_1571.png |
| RUN1571_2_acceptance | accepted R10 curve | NOT_ACCEPTED | human/independent QA still required |
| RUN1571_3_tau_kernel | tau_R10 internal kernel | NOT_READY | source-normalized internal prediction missing |
| RUN1571_4_raw_accepted | raw/accepted finite rows | NO_LIVE_SCORE_ROWS | raw_rows=0; accepted_rows=0 |
| RUN1571_5_claim | R10/local GR claim | BLOCKED_NO_CLAIM | QA curve exists but internal MTS prediction is missing |

## Claim Gates
| gate_id | claim_gate | status | reason |
| --- | --- | --- | --- |
| GATE1571_0_QA_curve | QA-cleaned R10 candidate curve | PASS_NONCLAIM | cleaned trace and overlay exist but are not accepted |
| GATE1571_1_accepted_curve | accepted R10 curve | BLOCKED_NO_CLAIM | independent/manual digitization QA missing |
| GATE1571_2_tau_kernel | tau_R10 internal source-normalized kernel | BLOCKED_NO_CLAIM | Z_R/M_R2/J_R/B_R/readout inputs missing |
| GATE1571_3_R10_score | R10 score/pass/fail | BLOCKED_NO_CLAIM | no internal MTS alpha(lambda) prediction |
| GATE1571_4_local_GR | derived local GR/Newton safety | BLOCKED_NO_CLAIM | R10 external bound work does not solve local theorem gaps |

## Decision
| decision_id | decision | result | reason |
| --- | --- | --- | --- |
| DEC1571_0_curve | R10 digitization QA | QA_CLEANED_CANDIDATE_CREATED_NONCLAIM | component filtering and overlay reduce obvious label contamination but do not make an accepted curve |
| DEC1571_1_tau | tau_R10 internal kernel | NOT_READY_SOURCE_NORMALIZATION_MISSING | formal kernel shape exists, but theory coefficients/source normalization remain absent |
| DEC1571_2_next | next target | NEXT_1572_TAU_R10_SOURCE_NORMALIZATION_OR_ACCEPTED_CURVE_QA | best next move is derive source-normalized tau_R10 or independently QA the curve into accepted nonclaim input |

## Validation
| check_id | result | detail |
| --- | --- | --- |
| VAL1571_0_sources_exist | PASS | all cited 1571 source paths exist |
| VAL1571_1_needles_found | PASS | all registered evidence needles found |
| VAL1571_2_component_audit | PASS | component audit keeps and rejects blue components |
| VAL1571_3_method_overlay | PASS | overlay exists and method records it |
| VAL1571_4_curve_candidate | PASS | QA-cleaned candidate curve rows created |
| VAL1571_5_curve_positive | PASS | candidate curve lambda/alpha values are positive |
| VAL1571_6_comparison | PASS | 1570-to-1571 comparison recorded |
| VAL1571_7_tau_not_ready | PASS | tau kernel remains not ready |
| VAL1571_8_raw_accepted_empty | PASS | raw/accepted finite rows remain empty |
| VAL1571_9_runner_blocks_claim | PASS | runner blocks local/R10 claim |
| VAL1571_10_claim_gates | PASS | claim gates remain closed |
| VAL1571_11_decision_next | PASS | decision selects tau source normalization or accepted curve QA |
| VAL1571_12_next_target | PASS | next target is tau source normalization or accepted curve QA |
| VAL1571_13_csv_parse | PASS | all generated 1571 CSVs parse cleanly |
| VAL1571_14_claim_flags_false | PASS | all generated prediction/claim flags remain false |
| VAL1571_15_branch_copies | PASS | branch/quarantine nonclaim copies written |
| VAL1571_16_pycache_absent | PASS | scripts __pycache__ absent after run |
| VAL1571_17_formalization_untouched | PASS | formalization modified-file count since start=0 |
| VAL1571_OVERALL | PASS | 1571 R10 digitization QA or tauR10 internal kernel validation |

## Next Target
| next_target | script | objective | do_not |
| --- | --- | --- | --- |
| 1572-Y5-RAB-tauR10-source-normalization-or-accepted-curve-QA.md | scripts/Y5_RAB_tauR10_source_normalization_or_accepted_curve_QA.py | try to derive/fill the internal tau_R10 source-normalization kernel; in parallel, QA the cleaned curve against manual tick/curve checks before any accepted nonclaim input | do not claim R10 pass; do not accept the curve without independent QA; do not edit formalization-workbench |
