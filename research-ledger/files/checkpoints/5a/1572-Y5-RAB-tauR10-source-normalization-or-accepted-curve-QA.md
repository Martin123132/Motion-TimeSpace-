# 1572 - R_AB tau_R10 Source Normalization or Accepted Curve QA

## Verdict
- The cleaned R10 curve is now a reviewed private candidate: machine visual QA passes and the overlay follows the blue curve.
- It is still not accepted evidence because independent/manual tick and curve QA are missing.
- The internal `tau_R10` source-normalization kernel remains the hard blocker: `J_R`, `B_R`, readout, and `lambda_R=sqrt(Z_R/M_R^2)` are not sourced or theorem-zeroed.
- No R10 score, local GR/Newton reduction, PPN, WEP, clock, orbital, `Z_R=0`, or `q_R=0` claim is made.

## Source Register
| source_id | source_path | exists | needle_found | needles |
| --- | --- | --- | --- | --- |
| SRC1572_0_1571_doc | 1571-Y5-RAB-R10-digitization-QA-or-tauR10-internal-kernel.md | True | True | R10 Fig. 2 curve is now a cleaner QA candidate; internal `tau_R10` source-normalized kernel is still missing |
| SRC1572_1_1571_validation | source-intake/mts_residuals/P8_Y5_BRR545_1571_VALIDATION.csv | True | True | VAL1571_OVERALL; PASS |
| SRC1572_2_1571_curve | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1571_R10_ALPHA_LAMBDA_DIGITIZED_QA_CANDIDATE.csv | True | True | QA1571_000; QA_CLEANED_CANDIDATE_NONCLAIM |
| SRC1572_3_1571_components | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1571_BLUE_COMPONENT_QA_AUDIT.csv | True | True | KEEP_CURVE_CANDIDATE; REJECT_LABEL_OR_AXIS_TEXT |
| SRC1572_4_1571_method | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1571_DIGITIZATION_QA_METHOD.csv | True | True | QA1571_3_overlay; OVERLAY_CREATED |
| SRC1572_5_1571_comparison | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1571_CURVE_COMPARISON_1570_TO_1571.csv | True | True | CMP1571_0_point_count; QA_CHANGED_CANDIDATE_TRACE |
| SRC1572_6_1571_tau | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1571_TAU_R10_INTERNAL_KERNEL_ATTEMPT.csv | True | True | KERN1571_4_verdict; NOT_READY |
| SRC1572_7_overlay | source-intake/rab-sector/external/r10/1571/R10_fig2_blue_curve_cleaned_trace_overlay_1571.png | True | True |  |

## Visual QA Review
| qa_id | qa_item | result | evidence | limitation |
| --- | --- | --- | --- | --- |
| VQA1572_0_overlay_exists | trace overlay rendered | PASS_MACHINE_VISUAL_REVIEW | source-intake/rab-sector/external/r10/1571/R10_fig2_blue_curve_cleaned_trace_overlay_1571.png | not independent human/manual digitization |
| VQA1572_1_curve_following | red trace follows blue This work curve | PASS_MACHINE_VISUAL_REVIEW | overlay trace follows the blue boundary across the plotted range | axis calibration and centerline still approximate |
| VQA1572_2_label_rejection | label/text contamination reduced | PASS_COMPONENT_FILTER_REVIEW | component audit rejects blue label/axis text and keeps curve candidates | arrow/text contamination cannot be ruled out without manual point review |
| VQA1572_3_point_count | reviewed candidate point count | PASS_INTERNAL_QA_CANDIDATE | points=108 | candidate-only, not accepted for claims |

## Curve Acceptance Gate
| gate_id | gate | status | meaning |
| --- | --- | --- | --- |
| ACCEPT1572_0_overlay | visual overlay exists and follows curve | PASS_INTERNAL_QA | sufficient for reviewed candidate |
| ACCEPT1572_1_axis | manual tick-by-tick axis calibration | MISSING_INDEPENDENT_QA | required before accepted curve |
| ACCEPT1572_2_curve | manual/independent curve point check | MISSING_INDEPENDENT_QA | required before accepted curve |
| ACCEPT1572_3_curve_status | accepted nonclaim bound curve | NOT_ACCEPTED | candidate remains reviewed-only |
| ACCEPT1572_4_claim_status | claim-valid R10 curve | BLOCKED_NO_CLAIM | even accepted external curve would still need internal MTS prediction |

## Reviewed Curve Candidate
| point_id | lambda_m | alpha_abs_bound | pixel_x | pixel_y | digitization_status | review_status |
| --- | --- | --- | --- | --- | --- | --- |
| QA1571_000 | 0.0012673036 | 1 | 139 | 20.00 | REVIEWED_QA_CANDIDATE_NONCLAIM | INTERNAL_MACHINE_VISUAL_QA_PASS_NOT_INDEPENDENT |
| QA1571_001 | 0.0013671069 | 0.71587749 | 147 | 42.50 | REVIEWED_QA_CANDIDATE_NONCLAIM | INTERNAL_MACHINE_VISUAL_QA_PASS_NOT_INDEPENDENT |
| QA1571_002 | 0.00147477 | 0.45742783 | 155 | 72.65 | REVIEWED_QA_CANDIDATE_NONCLAIM | INTERNAL_MACHINE_VISUAL_QA_PASS_NOT_INDEPENDENT |
| QA1571_003 | 0.0015909118 | 0.29293698 | 163 | 102.65 | REVIEWED_QA_CANDIDATE_NONCLAIM | INTERNAL_MACHINE_VISUAL_QA_PASS_NOT_INDEPENDENT |
| QA1571_004 | 0.0017162 | 0.18759696 | 171 | 132.65 | REVIEWED_QA_CANDIDATE_NONCLAIM | INTERNAL_MACHINE_VISUAL_QA_PASS_NOT_INDEPENDENT |
| QA1571_005 | 0.001851355 | 0.12193518 | 179 | 161.65 | REVIEWED_QA_CANDIDATE_NONCLAIM | INTERNAL_MACHINE_VISUAL_QA_PASS_NOT_INDEPENDENT |
| QA1571_006 | 0.0019971539 | 0.080801487 | 187 | 189.35 | REVIEWED_QA_CANDIDATE_NONCLAIM | INTERNAL_MACHINE_VISUAL_QA_PASS_NOT_INDEPENDENT |
| QA1571_007 | 0.0021544347 | 0.054791057 | 195 | 215.50 | REVIEWED_QA_CANDIDATE_NONCLAIM | INTERNAL_MACHINE_VISUAL_QA_PASS_NOT_INDEPENDENT |
| QA1571_008 | 0.0023241018 | 0.037402723 | 203 | 241.20 | REVIEWED_QA_CANDIDATE_NONCLAIM | INTERNAL_MACHINE_VISUAL_QA_PASS_NOT_INDEPENDENT |
| QA1571_009 | 0.0025071306 | 0.026518465 | 211 | 264.35 | REVIEWED_QA_CANDIDATE_NONCLAIM | INTERNAL_MACHINE_VISUAL_QA_PASS_NOT_INDEPENDENT |
| QA1571_010 | 0.0027045734 | 0.018648554 | 219 | 288.05 | REVIEWED_QA_CANDIDATE_NONCLAIM | INTERNAL_MACHINE_VISUAL_QA_PASS_NOT_INDEPENDENT |
| QA1571_011 | 0.0029175652 | 0.0136509 | 227 | 309.05 | REVIEWED_QA_CANDIDATE_NONCLAIM | INTERNAL_MACHINE_VISUAL_QA_PASS_NOT_INDEPENDENT |
| QA1571_012 | 0.0031473308 | 0.010142127 | 235 | 329.05 | REVIEWED_QA_CANDIDATE_NONCLAIM | INTERNAL_MACHINE_VISUAL_QA_PASS_NOT_INDEPENDENT |
| QA1571_013 | 0.0033951909 | 0.0076480089 | 243 | 348.05 | REVIEWED_QA_CANDIDATE_NONCLAIM | INTERNAL_MACHINE_VISUAL_QA_PASS_NOT_INDEPENDENT |
| QA1571_014 | 0.0036625706 | 0.0058666084 | 251 | 365.90 | REVIEWED_QA_CANDIDATE_NONCLAIM | INTERNAL_MACHINE_VISUAL_QA_PASS_NOT_INDEPENDENT |
| QA1571_015 | 0.0039510072 | 0.0045573216 | 259 | 382.90 | REVIEWED_QA_CANDIDATE_NONCLAIM | INTERNAL_MACHINE_VISUAL_QA_PASS_NOT_INDEPENDENT |
| QA1571_016 | 0.0042621588 | 0.0035481339 | 267 | 399.75 | REVIEWED_QA_CANDIDATE_NONCLAIM | INTERNAL_MACHINE_VISUAL_QA_PASS_NOT_INDEPENDENT |
| QA1571_017 | 0.0045978144 | 0.0027975264 | 275 | 415.75 | REVIEWED_QA_CANDIDATE_NONCLAIM | INTERNAL_MACHINE_VISUAL_QA_PASS_NOT_INDEPENDENT |
| QA1571_018 | 0.0049599038 | 0.0021237176 | 283 | 434.30 | REVIEWED_QA_CANDIDATE_NONCLAIM | INTERNAL_MACHINE_VISUAL_QA_PASS_NOT_INDEPENDENT |
| QA1571_019 | 0.0053505085 | 0.0017915371 | 291 | 445.75 | REVIEWED_QA_CANDIDATE_NONCLAIM | INTERNAL_MACHINE_VISUAL_QA_PASS_NOT_INDEPENDENT |
| QA1571_020 | 0.0057718744 | 0.0014551348 | 299 | 459.75 | REVIEWED_QA_CANDIDATE_NONCLAIM | INTERNAL_MACHINE_VISUAL_QA_PASS_NOT_INDEPENDENT |
| QA1571_021 | 0.0062264239 | 0.0011845363 | 307 | 473.60 | REVIEWED_QA_CANDIDATE_NONCLAIM | INTERNAL_MACHINE_VISUAL_QA_PASS_NOT_INDEPENDENT |
| QA1571_022 | 0.0067167703 | 0.0009889203 | 315 | 485.75 | REVIEWED_QA_CANDIDATE_NONCLAIM | INTERNAL_MACHINE_VISUAL_QA_PASS_NOT_INDEPENDENT |
| QA1571_023 | 0.0072457326 | 0.00081706774 | 323 | 498.60 | REVIEWED_QA_CANDIDATE_NONCLAIM | INTERNAL_MACHINE_VISUAL_QA_PASS_NOT_INDEPENDENT |
| QA1571_024 | 0.0078163521 | 0.0006836577 | 331 | 510.60 | REVIEWED_QA_CANDIDATE_NONCLAIM | INTERNAL_MACHINE_VISUAL_QA_PASS_NOT_INDEPENDENT |
| QA1571_025 | 0.0084319093 | 0.00058059189 | 339 | 521.60 | REVIEWED_QA_CANDIDATE_NONCLAIM | INTERNAL_MACHINE_VISUAL_QA_PASS_NOT_INDEPENDENT |
| QA1571_026 | 0.0090959431 | 0.00049416385 | 347 | 532.45 | REVIEWED_QA_CANDIDATE_NONCLAIM | INTERNAL_MACHINE_VISUAL_QA_PASS_NOT_INDEPENDENT |
| QA1571_027 | 0.0098122713 | 0.00043135885 | 355 | 541.60 | REVIEWED_QA_CANDIDATE_NONCLAIM | INTERNAL_MACHINE_VISUAL_QA_PASS_NOT_INDEPENDENT |
| QA1571_028 | 0.010585012 | 0.00037821778 | 363 | 550.45 | REVIEWED_QA_CANDIDATE_NONCLAIM | INTERNAL_MACHINE_VISUAL_QA_PASS_NOT_INDEPENDENT |
| QA1571_029 | 0.011418608 | 0.00033088526 | 371 | 559.45 | REVIEWED_QA_CANDIDATE_NONCLAIM | INTERNAL_MACHINE_VISUAL_QA_PASS_NOT_INDEPENDENT |

## tau_R10 Source Normalization
| normalization_id | kernel_piece | role | status | blocking_gap |
| --- | --- | --- | --- | --- |
| TAUN1572_0_kernel_target | alpha_MTS(lambda_R)=tau_R10 A_R | convert internal finite R_AB residual into the external Yukawa alpha(lambda) language | FORMAL_TARGET_ONLY | not yet source-normalized |
| TAUN1572_1_test_mass_source | A_R must be proportional to source response of both test masses | requires matter/source normalization and composition dependence or zero theorem | MISSING_JR_SOURCE_NORMALIZATION | no J_R theorem-zero/finite row |
| TAUN1572_2_boundary_readout | A_R may receive B_R/readout contributions | requires boundary/readout projection theorem or finite row | MISSING_BR_READOUT_NORMALIZATION | boundary/readout gates still unsigned |
| TAUN1572_3_range | lambda_R=sqrt(Z_R/M_R^2) | requires Z_R and M_R^2 in shared normalization | MISSING_RANGE_NORMALIZATION | no Z_R/M_R^2 source-backed rows |
| TAUN1572_4_verdict | tau_R10 internal source-normalization kernel | cannot be filled from external curve QA | NOT_READY | derive source-normalized kernel or fill internal coefficient rows next |

## Runner
| runner_id | test | current_status | detail |
| --- | --- | --- | --- |
| RUN1572_0_sources | load 1571 handoff and overlay | PASS | all source register needles found |
| RUN1572_1_reviewed_curve | reviewed R10 curve candidate | PASS_REVIEWED_CANDIDATE_NONCLAIM | points=108 |
| RUN1572_2_acceptance | accepted R10 curve | NOT_ACCEPTED | independent/manual axis and curve QA missing |
| RUN1572_3_tau | tau_R10 source normalization | NOT_READY | J_R/B_R/readout/range normalization missing |
| RUN1572_4_raw_accepted | raw/accepted finite rows | NO_LIVE_SCORE_ROWS | raw_rows=0; accepted_rows=0 |
| RUN1572_5_claim | R10/local GR claim | BLOCKED_NO_CLAIM | external curve QA still lacks internal MTS prediction |

## Claim Gates
| gate_id | claim_gate | status | reason |
| --- | --- | --- | --- |
| GATE1572_0_reviewed_curve | reviewed R10 curve candidate | PASS_NONCLAIM | internal machine visual QA passed |
| GATE1572_1_accepted_curve | accepted R10 curve | BLOCKED_NO_CLAIM | independent/manual QA missing |
| GATE1572_2_tau | tau_R10 internal kernel | BLOCKED_NO_CLAIM | source normalization missing |
| GATE1572_3_R10_score | R10 score/pass/fail | BLOCKED_NO_CLAIM | no internal MTS alpha(lambda) prediction |
| GATE1572_4_local_GR | derived local GR/Newton | BLOCKED_NO_CLAIM | R10 data plumbing does not prove local limit |

## Decision
| decision_id | decision | result | reason |
| --- | --- | --- | --- |
| DEC1572_0_curve | R10 curve status | REVIEWED_CANDIDATE_NOT_ACCEPTED | machine visual QA passes, but independent/manual curve QA is still missing |
| DEC1572_1_tau | tau_R10 source normalization | NOT_READY | external curve quality is no substitute for internal source-normalized theory kernel |
| DEC1572_2_next | next target | NEXT_1573_INTERNAL_TAU_R10_SOURCE_KERNEL_OR_MANUAL_CURVE_ACCEPTANCE | derive the internal source kernel or perform independent manual curve QA |

## Validation
| check_id | result | detail |
| --- | --- | --- |
| VAL1572_0_sources_exist | PASS | all cited 1572 source paths exist |
| VAL1572_1_needles_found | PASS | all registered evidence needles found |
| VAL1572_2_visual_qa | PASS | machine visual QA recorded |
| VAL1572_3_acceptance_not_promoted | PASS | curve is not promoted to accepted |
| VAL1572_4_reviewed_curve | PASS | reviewed candidate curve rows written |
| VAL1572_5_tau_not_ready | PASS | tau source normalization remains not ready |
| VAL1572_6_raw_accepted_empty | PASS | raw/accepted finite rows remain empty |
| VAL1572_7_runner_blocks_claim | PASS | runner blocks local/R10 claim |
| VAL1572_8_claim_gates | PASS | claim gates remain closed |
| VAL1572_9_decision_next | PASS | decision selects internal kernel or manual curve acceptance |
| VAL1572_10_next_target | PASS | next target is internal tau kernel or manual curve acceptance |
| VAL1572_11_csv_parse | PASS | all generated 1572 CSVs parse cleanly |
| VAL1572_12_claim_flags_false | PASS | all generated prediction/claim flags remain false |
| VAL1572_13_branch_copies | PASS | branch/quarantine nonclaim copies written |
| VAL1572_14_pycache_absent | PASS | scripts __pycache__ absent after run |
| VAL1572_15_formalization_untouched | PASS | formalization modified-file count since start=0 |
| VAL1572_OVERALL | PASS | 1572 tauR10 source normalization or accepted curve QA validation |

## Next Target
| next_target | script | objective | do_not |
| --- | --- | --- | --- |
| 1573-Y5-RAB-internal-tauR10-source-kernel-or-manual-curve-acceptance.md | scripts/Y5_RAB_internal_tauR10_source_kernel_or_manual_curve_acceptance.py | derive the internal tau_R10 source kernel from Z_R/M_R2/J_R/B_R/readout inputs, or run an independent/manual digitization acceptance pass on the reviewed R10 curve | do not score R10 without internal alpha_MTS(lambda); do not claim local GR; do not edit formalization-workbench |
