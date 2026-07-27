# 1509 - Acquire Reviewed R10 Bound Curve and Tau Kernel or Freeze Local R10

## Verdict
- Real R10 source bundles are now local, including the 2020 modern Eot-Wash paper source, the 2007 continuity paper source, and the 2003 review source.
- The 2020 source gives strong anchor facts but says the numerical positive/negative alpha constraints are in Supplemental Material; the arXiv bundle does not provide a claim-ready curve table.
- Therefore the local R10 scoring branch is frozen as nonclaim until a reviewed alpha_bound(lambda) curve, tau_R10(lambda) kernel, and parent alpha_predicted(lambda) are available.

## Source Ledger
| source_id | local_path | exists | bytes | status |
| --- | --- | --- | --- | --- |
| SRC1509_0_2020_arxiv_source | source-intake/r10/raw/1509/arxiv_2002_11761_source.tar | True | 530474 | LOCAL_SOURCE_AVAILABLE |
| SRC1509_1_2020_tex | source-intake/r10/raw/1509/arxiv_2002_11761_source/FB_ISL_pdf.tex | True | 25056 | LOCAL_SOURCE_AVAILABLE |
| SRC1509_2_2007_arxiv_source | source-intake/r10/raw/1509/arxiv_hep-ph_0611184_source.tar | True | 248949 | LOCAL_SOURCE_AVAILABLE |
| SRC1509_3_2007_tex | source-intake/r10/raw/1509/arxiv_hep-ph_0611184_source/kapner6.tex | True | 20269 | LOCAL_SOURCE_AVAILABLE |
| SRC1509_4_2003_review_source | source-intake/r10/raw/1509/arxiv_hep-ph_0307284_source.tar | True | 355885 | LOCAL_SOURCE_AVAILABLE |
| SRC1509_5_2003_review_tex | source-intake/r10/raw/1509/arxiv_hep-ph_0307284_source/gravityreview.tex | True | 143066 | LOCAL_SOURCE_AVAILABLE |

## Web Source Anchors
| anchor_id | paper | lambda_value | alpha_bound | curve_status |
| --- | --- | --- | --- | --- |
| ANCHOR1509_0_2020_grav_strength_threshold | Lee et al. 2020 PRL / arXiv:2002.11761 | 3.86000000e-05 | 1.00000000e+00 | ANCHOR_ONLY_NON_CURVE |
| ANCHOR1509_1_2007_grav_strength_threshold | Kapner et al. 2007 PRL / arXiv:hep-ph/0611184 | 5.60000000e-05 | 1.00000000e+00 | ANCHOR_ONLY_NON_CURVE |
| ANCHOR1509_2_2003_review_context | Adelberger, Heckel, Nelson 2003 review / arXiv:hep-ph/0307284 | MISSING_REVIEW_ROW_NOT_NUMERIC | MISSING_REVIEW_ROW_NOT_NUMERIC | NOT_A_BOUND_ROW |

## Candidate Bound Rows
| bound_id | lambda_value | alpha_bound | curve_status | valid_for_claim |
| --- | --- | --- | --- | --- |
| BOUND1509_0_2020_grav_strength_threshold | 3.86000000e-05 | 1.00000000e+00 | ANCHOR_ONLY_NON_CURVE | False |
| BOUND1509_1_2007_grav_strength_threshold | 5.60000000e-05 | 1.00000000e+00 | ANCHOR_ONLY_NON_CURVE | False |

## Tau Kernel Schema
| kernel_id | lambda_value | tau_R10 | status | valid_for_claim |
| --- | --- | --- | --- | --- |
| TAU1509_0_R10_geometry_kernel | MISSING_lambda_grid | MISSING_tau_R10 | SCHEMA_ONLY_NONCLAIM | False |

## Claim Gate
| gate_id | requirement | current_status |
| --- | --- | --- |
| GATE1509_0_full_curve | reviewed alpha_bound(lambda) full curve | MISSING |
| GATE1509_1_tau_kernel | tau_R10(lambda) finite-source response kernel | MISSING |
| GATE1509_2_parent_alpha | MTS alpha_predicted(lambda) from parent coefficients or zero theorem | MISSING |
| GATE1509_3_interpolation | interpolation over overlapping lambda grid | BLOCKED_BY_MISSING_CURVE_KERNEL |
| GATE1509_4_decision | R10/local-GR claim | FALSE_FREEZE_LOCAL_R10_SCORE |

## Freeze Ledger
| freeze_id | decision | unfreeze_condition |
| --- | --- | --- |
| FREEZE1509_0 | FREEZE_LOCAL_R10_SCORE_NOT_THEORY | supply full alpha_bound(lambda), tau_R10(lambda), and parent alpha_predicted(lambda), or close field-specific zero theorem |

## Validation
| check_id | result | detail |
| --- | --- | --- |
| VAL1509_0_local_sources | PASS | all cited 1508 and R10 source paths exist |
| VAL1509_1_source_tars_nonempty | PASS | downloaded arXiv source bundles are present and nonempty |
| VAL1509_2_2020_anchor_text | PASS | 2020 source text contains 52 um, 38.6 um, and supplemental-material cues |
| VAL1509_3_2007_anchor_text | PASS | 2007 source text contains |alpha|<=1 and lambda=56 um cues |
| VAL1509_4_anchor_numeric | PASS | anchor rows have positive numeric lambda and alpha values |
| VAL1509_5_anchor_nonclaim | PASS | anchor rows are not full curves and are valid_for_claim=false |
| VAL1509_6_tau_schema_nonclaim | PASS | tau kernel remains schema-only and nonclaim |
| VAL1509_7_claim_gate_frozen | PASS | R10/local scoring is explicitly frozen |
| VAL1509_8_live_targets_absent | PASS | live derived R10 curve/kernel targets remain absent |
| VAL1509_9_csv_parse | PASS | all generated 1509 CSVs parse cleanly |
| VAL1509_10_branch_copies | PASS | branch/quarantine nonclaim copies written |
| VAL1509_11_pycache_absent | PASS | scripts __pycache__ absent after run |
| VAL1509_12_formalization_untouched | PASS | formalization modified-file count since start=0 |
| VAL1509_13_claim_flags_false | PASS | all generated prediction/claim flags remain false |
| VAL1509_14_overall | PASS | 1509 acquired local source bundles and anchor rows, but froze R10 scoring until full curve/tau/parent-alpha inputs exist |

## Next Target
| next_id | next_target | script | objective |
| --- | --- | --- | --- |
| NEXT1509_0_1510 | 1510-Y5-R10-RAB-reviewed-figure-digitization-protocol-or-return-to-GR-derivation.md | scripts/Y5_R10_RAB_reviewed_figure_digitization_protocol_or_return_to_GR_derivation.py | either create a reviewed digitization protocol for the R10 Fig. 5 alpha_bound(lambda) curve and tau kernel, or deliberately pivot back to parent GR/Newton derivation while R10 scoring stays frozen |
