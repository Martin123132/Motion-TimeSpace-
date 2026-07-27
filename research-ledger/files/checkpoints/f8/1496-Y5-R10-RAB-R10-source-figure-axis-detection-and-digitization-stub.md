# 1496 - R10 Source Figure Axis Detection and Digitization Stub

## Verdict
- `fig5b1.pdf` is selected as the R10 `|alpha|(lambda)` source-figure target from the paper TeX caption map.
- A nonclaim digitization template was written, but no numeric curve points were fabricated or promoted.
- R10 remains blocked until axes are calibrated, curve points are digitized, and the `delta_w -> alpha(lambda)` kernel exists.

## Figure Caption Map: Selected Context
| figure_map_id | figure_label | graphic_path | caption_role | selection_status |
| --- | --- | --- | --- | --- |
| FCM1496_0_0 | fig1 | source-intake\r10\raw\Lee_2020_PRL_2002.11761_source_1495\FBpend.eps | NON_CURVE_SUPPORT_FIGURE | NOT_SELECTED_FOR_ALPHA_LAMBDA_CURVE |
| FCM1496_0_1 | fig1 | source-intake\r10\raw\Lee_2020_PRL_2002.11761_source_1495\gluedFoil.eps | NON_CURVE_SUPPORT_FIGURE | NOT_SELECTED_FOR_ALPHA_LAMBDA_CURVE |
| FCM1496_0_2 | fig1 | source-intake\r10\raw\Lee_2020_PRL_2002.11761_source_1495\FBpend_mounted.eps | NON_CURVE_SUPPORT_FIGURE | NOT_SELECTED_FOR_ALPHA_LAMBDA_CURVE |
| FCM1496_0_3 | fig1 | source-intake\r10\raw\Lee_2020_PRL_2002.11761_source_1495\theory.eps | NON_CURVE_SUPPORT_FIGURE | NOT_SELECTED_FOR_ALPHA_LAMBDA_CURVE |
| FCM1496_0_4 | fig1 | source-intake\r10\raw\Lee_2020_PRL_2002.11761_source_1495\fig1.pdf | NON_CURVE_SUPPORT_FIGURE | NOT_SELECTED_FOR_ALPHA_LAMBDA_CURVE |
| FCM1496_1_0 | fig2 | source-intake\r10\raw\Lee_2020_PRL_2002.11761_source_1495\fig2a.pdf | NON_CURVE_SUPPORT_FIGURE | NOT_SELECTED_FOR_ALPHA_LAMBDA_CURVE |
| FCM1496_1_1 | fig2 | source-intake\r10\raw\Lee_2020_PRL_2002.11761_source_1495\fig2b.pdf | NON_CURVE_SUPPORT_FIGURE | NOT_SELECTED_FOR_ALPHA_LAMBDA_CURVE |
| FCM1496_2_0 | fig3 | source-intake\r10\raw\Lee_2020_PRL_2002.11761_source_1495\xyCenter.pdf | NON_CURVE_SUPPORT_FIGURE | NOT_SELECTED_FOR_ALPHA_LAMBDA_CURVE |
| FCM1496_2_1 | fig3 | source-intake\r10\raw\Lee_2020_PRL_2002.11761_source_1495\capPF.pdf | NON_CURVE_SUPPORT_FIGURE | NOT_SELECTED_FOR_ALPHA_LAMBDA_CURVE |
| FCM1496_2_2 | fig3 | source-intake\r10\raw\Lee_2020_PRL_2002.11761_source_1495\capAF.pdf | NON_CURVE_SUPPORT_FIGURE | NOT_SELECTED_FOR_ALPHA_LAMBDA_CURVE |
| FCM1496_3_0 | fig4 | source-intake\r10\raw\Lee_2020_PRL_2002.11761_source_1495\magsysZB.pdf | NON_CURVE_SUPPORT_FIGURE | NOT_SELECTED_FOR_ALPHA_LAMBDA_CURVE |
| FCM1496_3_1 | fig4 | source-intake\r10\raw\Lee_2020_PRL_2002.11761_source_1495\magsysZs.pdf | NON_CURVE_SUPPORT_FIGURE | NOT_SELECTED_FOR_ALPHA_LAMBDA_CURVE |
| FCM1496_4_0 | fig5 | source-intake\r10\raw\Lee_2020_PRL_2002.11761_source_1495\fig5a.pdf | R10_TORQUE_DATA_CONTEXT | CONTEXT_NOT_BOUND_CURVE |
| FCM1496_4_1 | fig5 | source-intake\r10\raw\Lee_2020_PRL_2002.11761_source_1495\fig5b1.pdf | R10_ALPHA_LAMBDA_LIMIT_CURVE_TARGET | SELECTED_CURVE_DIGITIZATION_TARGET_NONCLAIM |

## Curve Target Selection
| selection_id | curve_figure_path | selection_status | curve_target_path | reason |
| --- | --- | --- | --- | --- |
| SEL1496_0_fig5b1 | source-intake\r10\raw\Lee_2020_PRL_2002.11761_source_1495\fig5b1.pdf | CURVE_TARGET_IDENTIFIED_NONCLAIM | source-intake\r10\derived\R10_alpha_lambda_bound_curve_DIGITIZED.csv | TeX caption maps fig5b1.pdf to the bottom plot: 95% confidence upper limits on |alpha| |

## Axis Detection Gate
| axis_gate_id | axis | expected_quantity | scale_requirement | auto_axis_text_status |
| --- | --- | --- | --- | --- |
| AXIS1496_0_x | x | lambda | verify whether log scale before digitization | FIGURE_AXIS_TEXT_NOT_EXTRACTABLE_MANUAL_CALIBRATION_REQUIRED |
| AXIS1496_1_y | y | absolute Yukawa strength |alpha| | verify whether log scale before digitization | FIGURE_AXIS_TEXT_NOT_EXTRACTABLE_MANUAL_CALIBRATION_REQUIRED |
| AXIS1496_2_confidence | curve | 95 percent upper limit | record whether curve is |alpha|, +alpha, or -alpha; 1496 only selects |alpha| caption target | FIGURE_AXIS_TEXT_NOT_EXTRACTABLE_MANUAL_CALIBRATION_REQUIRED |

## Digitization Template Status
| template_id | template_path | template_status | required_before_promotion |
| --- | --- | --- | --- |
| DT1496_0_template | source-intake\r10\derived\staging\R10_alpha_lambda_bound_curve_DIGITIZATION_TEMPLATE_1496.csv | NONCLAIM_TEMPLATE_WRITTEN_NO_POINTS | replace placeholder with digitized positive numeric lambda/alpha rows, source figure, method, units, and validation |

## Kernel Contract Refresh
| kernel_input_id | required_input | current_status | failure_effect |
| --- | --- | --- | --- |
| KERN1496_0_curve | digitized R10 |alpha|(lambda) upper-limit curve | MISSING_LIVE_TARGET | R10 score remains blocked |
| KERN1496_1_axis | axis calibration and log/linear convention for fig5b1 | MANUAL_CALIBRATION_REQUIRED | R10 score remains blocked |
| KERN1496_2_geometry | R10 geometry response kernel | MISSING | R10 score remains blocked |
| KERN1496_3_basis | delta_w component basis and units | MISSING | R10 score remains blocked |
| KERN1496_4_mapping | delta_w to Yukawa alpha mapping | MISSING | R10 score remains blocked |

## Validation
| check_id | result | detail |
| --- | --- | --- |
| VAL1496_0_local_sources | PASS | all cited 1495/source figure paths exist |
| VAL1496_1_fig5b1_selected | PASS | fig5b1 selected from TeX caption map |
| VAL1496_2_selection_row | PASS | curve target selection row is explicit |
| VAL1496_3_template | PASS | digitization template exists and remains nonclaim |
| VAL1496_4_live_targets_absent | PASS | live R10 curve/kernel targets remain absent |
| VAL1496_5_readiness_blocked | PASS | delta_w/R10 readiness remains false |
| VAL1496_6_Cparent_refused | PASS | C_parent import was not performed |
| VAL1496_7_csv_parse | PASS | all generated 1496 CSVs parse cleanly |
| VAL1496_8_branch_copies | PASS | branch/quarantine nonclaim copies written |
| VAL1496_9_pycache_absent | PASS | scripts __pycache__ absent after run |
| VAL1496_10_formalization_untouched | PASS | formalization modified-file count since start=0 |
| VAL1496_11_claim_flags_false | PASS | all generated prediction/claim flags remain false |
| VAL1496_12_overall | PASS | 1496 identified R10 fig5b1 curve target and wrote a nonclaim digitization template |

## Next Target
| next_id | next_target | script | objective |
| --- | --- | --- | --- |
| NEXT1496_0_1497 | 1497-Y5-R10-RAB-R10-fig5b1-axis-calibration-and-nonclaim-point-digitization.md | scripts/Y5_R10_RAB_R10_fig5b1_axis_calibration_and_nonclaim_point_digitization.py | render or manually calibrate fig5b1 axes, fill nonclaim alpha(lambda) point rows, and keep the R10 score blocked until the projection kernel exists |
