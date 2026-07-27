# 1499 - Isolate EotWash 2020 Curve and Sample Nonclaim alpha(lambda) Points

## Verdict
- A rough Eot-Wash 2020 `|alpha|(lambda)` candidate was sampled from the 1498 rendered R10 figure.
- The `38.6 um, alpha=1` source-text threshold is included as an anchor, but all rows remain nonclaim.
- No live R10 curve or MTS/R10 score is promoted; the projection kernel is still missing.

## Curve Selection
| selection_id | curve_identity | selection_status | review_requirement |
| --- | --- | --- | --- |
| SEL1499_0_EotWash2020_candidate | EotWash_2020_fig5b1_candidate | SELECTED_FOR_NONCLAIM_VISUAL_SAMPLING_ONLY | human/render verification required before any live curve promotion |
| SEL1499_1_live_refusal | R10_alpha_lambda_bound_curve_DIGITIZED | LIVE_TARGET_NOT_WRITTEN | write live target only after reviewed digitization and projection-kernel separation |

## Nonclaim Point Preview
| point_id | lambda_value | lambda_units | alpha_bound_abs | point_source | promotion_status |
| --- | --- | --- | --- | --- | --- |
| R10EW2020_0_visual_left_high | 7.00000000e-06 | m | 2.00000000e+05 | visual_curve_candidate | NONCLAIM_APPROXIMATE_VISUAL_POINT_REQUIRES_REVIEW |
| R10EW2020_1_visual_knee_high | 1.00000000e-05 | m | 2.50000000e+04 | visual_curve_candidate | NONCLAIM_APPROXIMATE_VISUAL_POINT_REQUIRES_REVIEW |
| R10EW2020_2_arrow_endpoint | 1.90000000e-05 | m | 9.00000000e+01 | blue_label_arrow_endpoint_candidate | NONCLAIM_APPROXIMATE_VISUAL_POINT_REQUIRES_REVIEW |
| R10EW2020_3_text_threshold_anchor | 3.86000000e-05 | m | 1.00000000e+00 | source_text_alpha1_threshold_anchor | NONCLAIM_APPROXIMATE_VISUAL_POINT_REQUIRES_REVIEW |
| R10EW2020_4_visual_post_threshold | 5.00000000e-05 | m | 1.60000000e-01 | visual_curve_candidate | NONCLAIM_APPROXIMATE_VISUAL_POINT_REQUIRES_REVIEW |
| R10EW2020_5_visual_minimum_left | 8.00000000e-05 | m | 3.00000000e-02 | visual_curve_candidate | NONCLAIM_APPROXIMATE_VISUAL_POINT_REQUIRES_REVIEW |
| R10EW2020_6_visual_floor | 1.20000000e-04 | m | 1.20000000e-02 | visual_curve_candidate | NONCLAIM_APPROXIMATE_VISUAL_POINT_REQUIRES_REVIEW |
| R10EW2020_7_visual_right_tail | 2.50000000e-04 | m | 5.00000000e-03 | visual_curve_candidate | NONCLAIM_APPROXIMATE_VISUAL_POINT_REQUIRES_REVIEW |
| R10EW2020_8_visual_far_right | 5.00000000e-04 | m | 3.00000000e-03 | visual_curve_candidate | NONCLAIM_APPROXIMATE_VISUAL_POINT_REQUIRES_REVIEW |

## Overlay
| overlay_id | overlay_png | overlay_status |
| --- | --- | --- |
| OVERLAY1499_0_sample_points | source-intake\r10\derived\staging\fig5b1_EotWash2020_nonclaim_sample_overlay_1499.png | NONCLAIM_REVIEW_OVERLAY_WRITTEN |

## Quality Ledger
| quality_id | object | status | detail |
| --- | --- | --- | --- |
| QUAL1499_0_method | point_set_method | ROUGH_VISUAL_NONCLAIM | points mix visual estimates with one source-text threshold anchor; they are not a digitized primary curve |
| QUAL1499_1_monotonic_lambda | lambda_order | PASS | lambda values increase left-to-right |
| QUAL1499_2_alpha1_anchor | 38p6um_alpha1_anchor | PRESENT_NONCLAIM | source text says gravitational-strength Yukawa interactions limited to ranges <38.6um; stored as alpha=1 anchor only |
| QUAL1499_3_live_target | live_curve_target | ABSENT_BY_DESIGN | source-intake\r10\derived\R10_alpha_lambda_bound_curve_DIGITIZED.csv |

## Validation
| check_id | result | detail |
| --- | --- | --- |
| VAL1499_0_local_sources | PASS | all cited 1498/source render paths exist |
| VAL1499_1_points_written | PASS | visual point rows=9 |
| VAL1499_2_points_nonclaim | PASS | visual point file remains nonclaim |
| VAL1499_3_alpha1_anchor | PASS | 38.6um alpha=1 anchor present |
| VAL1499_4_overlay | PASS | overlay path=source-intake\r10\derived\staging\fig5b1_EotWash2020_nonclaim_sample_overlay_1499.png |
| VAL1499_5_live_targets_absent | PASS | live R10 curve/kernel targets remain absent |
| VAL1499_6_Cparent_refused | PASS | C_parent import was not performed |
| VAL1499_7_csv_parse | PASS | all generated 1499 CSVs parse cleanly |
| VAL1499_8_branch_copies | PASS | branch/quarantine nonclaim copies written |
| VAL1499_9_pycache_absent | PASS | scripts __pycache__ absent after run |
| VAL1499_10_formalization_untouched | PASS | formalization modified-file count since start=0 |
| VAL1499_11_claim_flags_false | PASS | all generated prediction/claim flags remain false |
| VAL1499_12_overall | PASS | 1499 wrote approximate nonclaim EotWash 2020 alpha(lambda) samples and kept R10 scoring blocked |

## Next Target
| next_id | next_target | script | objective |
| --- | --- | --- | --- |
| NEXT1499_0_1500 | 1500-Y5-R10-RAB-reviewed-R10-curve-promotion-gate-or-kernel-derivation-contract.md | scripts/Y5_R10_RAB_reviewed_R10_curve_promotion_gate_or_kernel_derivation_contract.py | either review/refine the visual R10 alpha(lambda) points into a live claim-eligible curve candidate, or keep the curve staged and derive the delta_w-to-alpha projection kernel contract |
