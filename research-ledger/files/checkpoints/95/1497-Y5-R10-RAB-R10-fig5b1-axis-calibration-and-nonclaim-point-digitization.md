# 1497 - R10 fig5b1 Axis Calibration and Nonclaim Point Digitization

## Verdict
- No normal PDF renderer was available, but the `fig5b1.pdf` vector stream was parseable.
- Plot-axis geometry and colored curve/band candidates were extracted into a nonclaim vector skeleton.
- No physical `alpha(lambda)` points are promoted because axis tick labels and curve identity still require rendered/manual calibration.

## Renderer Capability
| renderer_id | command | available | render_effect |
| --- | --- | --- | --- |
| REN1497_vector_parse | pypdf_content_stream_parse | True | used_for_nonclaim_geometry_skeleton |

## Axis Candidates
| axis_id | axis_role | min_coord | max_coord | fixed_coord | calibration_status |
| --- | --- | --- | --- | --- | --- |
| AXIS1497_0_horizontal | horizontal_plot_axis_candidate | 1223.21 | 4624.73 | 775.344 | GEOMETRY_FOUND_LABEL_VALUES_MISSING |
| AXIS1497_1_vertical | vertical_plot_axis_candidate | 775.344 | 3836.71 | 1223.21 | GEOMETRY_FOUND_LABEL_VALUES_MISSING |

## Curve Path Candidates
| candidate_id | source_path_id | stroke_color | point_count | candidate_status |
| --- | --- | --- | --- | --- |
| CURVE1497_0 | PATH1497_962 | rgb(0,1,0) | 47 | VECTOR_CURVE_OR_BAND_CANDIDATE_NONCLAIM |
| CURVE1497_1 | PATH1497_987 | rgb(1,1,0.5) | 25 | VECTOR_CURVE_OR_BAND_CANDIDATE_NONCLAIM |
| CURVE1497_2 | PATH1497_1060 | rgb(1,1,0.5) | 18 | VECTOR_CURVE_OR_BAND_CANDIDATE_NONCLAIM |
| CURVE1497_3 | PATH1497_1104 | rgb(1,1,0.5) | 18 | VECTOR_CURVE_OR_BAND_CANDIDATE_NONCLAIM |
| CURVE1497_4 | PATH1497_1087 | rgb(1,1,0.5) | 18 | VECTOR_CURVE_OR_BAND_CANDIDATE_NONCLAIM |
| CURVE1497_5 | PATH1497_1042 | rgb(1,1,0.5) | 7 | VECTOR_CURVE_OR_BAND_CANDIDATE_NONCLAIM |
| CURVE1497_6 | PATH1497_1069 | rgb(1,1,0.5) | 9 | VECTOR_CURVE_OR_BAND_CANDIDATE_NONCLAIM |
| CURVE1497_7 | PATH1497_1035 | rgb(1,1,0.5) | 6 | VECTOR_CURVE_OR_BAND_CANDIDATE_NONCLAIM |
| CURVE1497_8 | PATH1497_1029 | rgb(1,1,0.5) | 43 | VECTOR_CURVE_OR_BAND_CANDIDATE_NONCLAIM |
| CURVE1497_9 | PATH1497_1333 | rgb(1,0,0) | 2 | VECTOR_CURVE_OR_BAND_CANDIDATE_NONCLAIM |

## Point Digitization Status
| point_status_id | skeleton_path | skeleton_rows | point_status | reason |
| --- | --- | --- | --- | --- |
| PTS1497_0_vector_skeleton | source-intake\r10\derived\staging\R10_fig5b1_vector_curve_skeleton_1497.csv | 20 | VECTOR_SKELETON_WRITTEN_NO_NUMERIC_ALPHA_LAMBDA_POINTS | axis labels/scale and curve identity not yet verified |

## Axis Calibration Contract
| contract_id | required_object | current_status | promotion_requirement |
| --- | --- | --- | --- |
| AXCON1497_0_plot_box | fig5b1 plot box | VECTOR_GEOMETRY_FOUND | manual/rendered verification of axis tick labels |
| AXCON1497_1_x_axis | lambda axis calibration | LABEL_VALUES_MISSING | map vector x coordinate to lambda units and record log/linear scale |
| AXCON1497_2_y_axis | |alpha| axis calibration | LABEL_VALUES_MISSING | map vector y coordinate to dimensionless |alpha| and record log/linear scale |
| AXCON1497_3_points | digitized curve points | VECTOR_SKELETON_WRITTEN_NO_NUMERIC_ALPHA_LAMBDA_POINTS | replace vector skeleton with numeric positive lambda/alpha rows |

## Validation
| check_id | result | detail |
| --- | --- | --- |
| VAL1497_0_local_sources | PASS | all cited 1496/source figure paths exist |
| VAL1497_1_vector_parse | PASS | vector path rows=6760 |
| VAL1497_2_axis_candidates | PASS | plot-axis geometry candidates found |
| VAL1497_3_curve_candidates | PASS | curve candidate rows=20 |
| VAL1497_4_skeleton | PASS | vector skeleton exists and remains nonclaim |
| VAL1497_5_live_targets_absent | PASS | live R10 curve/kernel targets remain absent |
| VAL1497_6_readiness_blocked | PASS | delta_w/R10 readiness remains false |
| VAL1497_7_Cparent_refused | PASS | C_parent import was not performed |
| VAL1497_8_csv_parse | PASS | all generated 1497 CSVs parse cleanly |
| VAL1497_9_branch_copies | PASS | branch/quarantine nonclaim copies written |
| VAL1497_10_pycache_absent | PASS | scripts __pycache__ absent after run |
| VAL1497_11_formalization_untouched | PASS | formalization modified-file count since start=0 |
| VAL1497_12_claim_flags_false | PASS | all generated prediction/claim flags remain false |
| VAL1497_13_overall | PASS | 1497 parsed fig5b1 vector geometry and wrote a nonclaim curve skeleton |

## Next Target
| next_id | next_target | script | objective |
| --- | --- | --- | --- |
| NEXT1497_0_1498 | 1498-Y5-R10-RAB-R10-rendered-axis-label-recovery-or-manual-calibration-packet.md | scripts/Y5_R10_RAB_R10_rendered_axis_label_recovery_or_manual_calibration_packet.py | recover physical axis labels for fig5b1 via rendering/manual calibration, then convert vector skeleton candidates into nonclaim alpha(lambda) rows |
