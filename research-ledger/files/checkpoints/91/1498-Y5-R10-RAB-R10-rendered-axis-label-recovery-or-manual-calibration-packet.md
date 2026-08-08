# 1498 - R10 Rendered Axis Label Recovery or Manual Calibration Packet

## Verdict
- `fig5b1.pdf` was rendered locally from its vector stream into a readable PNG.
- Visible axis calibration anchors were recorded as nonclaim review assumptions.
- Candidate vector bboxes were converted into approximate physical ranges, but no live `alpha(lambda)` point rows were promoted.

## Render Packet
| render_id | render_png | render_byte_count | visual_status |
| --- | --- | --- | --- |
| RENDER1498_0_fig5b1_vector | source-intake\r10\derived\staging\fig5b1_vector_render_1498.png | 51650 | READABLE_FOR_MANUAL_AXIS_CALIBRATION_NONCLAIM |

## Axis Visual Calibration
| axis_calibration_id | axis | vector_coord | physical_value | physical_units | calibration_status |
| --- | --- | --- | --- | --- | --- |
| AXCAL1498_0_x_left | x_lambda | 1223.21 | 2e-6 | m | VISUAL_CALIBRATION_NONCLAIM_REQUIRES_REVIEW |
| AXCAL1498_1_x_major_1e5 | x_lambda | 2102.79 | 1e-5 | m | VISUAL_CALIBRATION_NONCLAIM_REQUIRES_REVIEW |
| AXCAL1498_2_x_major_1e4 | x_lambda | 3361.06 | 1e-4 | m | VISUAL_CALIBRATION_NONCLAIM_REQUIRES_REVIEW |
| AXCAL1498_3_x_major_1e3 | x_lambda | 4619.34 | 1e-3 | m | VISUAL_CALIBRATION_NONCLAIM_REQUIRES_REVIEW |
| AXCAL1498_4_y_bottom | y_abs_alpha | 775.344 | 1e-3 | dimensionless | VISUAL_CALIBRATION_NONCLAIM_REQUIRES_REVIEW |
| AXCAL1498_5_y_top | y_abs_alpha | 3836.71 | 1e6 | dimensionless | VISUAL_CALIBRATION_NONCLAIM_REQUIRES_REVIEW |

## Calibrated Candidate BBox Preview
| bbox_id | stroke_color | lambda_min_m_approx | lambda_max_m_approx | alpha_min_approx | alpha_max_approx | bbox_status |
| --- | --- | --- | --- | --- | --- | --- |
| BBOX1498_CURVE1497_0 | rgb(0,1,0) | 3.699458e-06 | 1.009912e-03 | 1.909088e-02 | 9.904305e+05 | CALIBRATED_BBOX_ONLY_NOT_CURVE_POINTS |
| BBOX1498_CURVE1497_1 | rgb(1,1,0.5) | 9.000393e-06 | 9.999974e-04 | 2.487826e-03 | 1.388347e+05 | CALIBRATED_BBOX_ONLY_NOT_CURVE_POINTS |
| BBOX1498_CURVE1497_2 | rgb(1,1,0.5) | 1.999713e-05 | 9.999974e-04 | 1.109149e-02 | 9.904305e+05 | CALIBRATED_BBOX_ONLY_NOT_CURVE_POINTS |
| BBOX1498_CURVE1497_3 | rgb(1,1,0.5) | 3.032953e-05 | 7.002276e-04 | 3.336814e-03 | 1.000000e+06 | CALIBRATED_BBOX_ONLY_NOT_CURVE_POINTS |
| BBOX1498_CURVE1497_4 | rgb(1,1,0.5) | 2.841045e-05 | 6.377993e-04 | 4.935419e-03 | 9.904305e+05 | CALIBRATED_BBOX_ONLY_NOT_CURVE_POINTS |
| BBOX1498_CURVE1497_5 | rgb(1,1,0.5) | 5.399741e-06 | 6.572843e-05 | 1.426120e+02 | 9.904305e+05 | CALIBRATED_BBOX_ONLY_NOT_CURVE_POINTS |
| BBOX1498_CURVE1497_6 | rgb(1,1,0.5) | 1.999694e-06 | 2.042689e-05 | 7.188843e+03 | 9.904305e+05 | CALIBRATED_BBOX_ONLY_NOT_CURVE_POINTS |
| BBOX1498_CURVE1497_7 | rgb(1,1,0.5) | 7.020257e-06 | 3.824362e-05 | 5.888409e+03 | 1.000000e+06 | CALIBRATED_BBOX_ONLY_NOT_CURVE_POINTS |
| BBOX1498_CURVE1497_8 | rgb(1,1,0.5) | 3.775107e-04 | 1.009912e-03 | 1.364555e-03 | 2.834543e-02 | CALIBRATED_BBOX_ONLY_NOT_CURVE_POINTS |
| BBOX1498_CURVE1497_9 | rgb(1,0,0) | 4.708629e-06 | 1.599915e-05 | 9.137471e+02 | 9.866452e+03 | CALIBRATED_BBOX_ONLY_NOT_CURVE_POINTS |

## Point Status
| point_status_id | bbox_rows | point_status | reason |
| --- | --- | --- | --- |
| PTS1498_0_bbox_ranges | 20 | APPROX_BBOX_RANGES_ONLY_NO_DIGITIZED_POINTS | 1498 preserves axis calibration and candidate ranges, but does not sample the correct curve into alpha(lambda) rows |

## Validation
| check_id | result | detail |
| --- | --- | --- |
| VAL1498_0_local_sources | PASS | all cited 1497/source figure paths exist |
| VAL1498_1_render | PASS | render path=source-intake\r10\derived\staging\fig5b1_vector_render_1498.png |
| VAL1498_2_axis_calibration | PASS | visual axis calibration rows written |
| VAL1498_3_bbox_ranges | PASS | calibrated bbox rows=20 |
| VAL1498_4_live_targets_absent | PASS | live R10 curve/kernel targets remain absent |
| VAL1498_5_Cparent_refused | PASS | C_parent import was not performed |
| VAL1498_6_csv_parse | PASS | all generated 1498 CSVs parse cleanly |
| VAL1498_7_branch_copies | PASS | branch/quarantine nonclaim copies written |
| VAL1498_8_pycache_absent | PASS | scripts __pycache__ absent after run |
| VAL1498_9_formalization_untouched | PASS | formalization modified-file count since start=0 |
| VAL1498_10_claim_flags_false | PASS | all generated prediction/claim flags remain false |
| VAL1498_11_overall | PASS | 1498 rendered fig5b1 and wrote nonclaim visual axis calibration/bbox ranges |

## Next Target
| next_id | next_target | script | objective |
| --- | --- | --- | --- |
| NEXT1498_0_1499 | 1499-Y5-R10-RAB-isolate-EotWash-2020-curve-and-sample-nonclaim-alpha-lambda-points.md | scripts/Y5_R10_RAB_isolate_EotWash_2020_curve_and_sample_nonclaim_alpha_lambda_points.py | isolate the Eot-Wash 2020 curve in fig5b1, sample approximate nonclaim alpha(lambda) points, and keep R10 scoring blocked until the projection kernel exists |
