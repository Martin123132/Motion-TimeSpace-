# 1570 - R_AB R10 Curve Digitization or tau_R10 Kernel Source Normalization

## Verdict
- The external R10 side improved materially: the APS fulltext PDF payload, text extraction, Fig. 2 image, and a candidate blue-curve digitization now exist locally.
- The digitized curve is candidate-only: it is an image trace with approximate axis calibration and possible blue-arrow/text contamination.
- The internal MTS side is still missing: `tau_R10` source normalization, `Z_R`, `M_R^2`, `J_R`, `B_R`, and readout inputs are not filled.
- Therefore this supports future smoke tooling, not a claim.
- No R10, local GR/Newton, PPN, WEP, clock, orbital, `Z_R=0`, or `q_R=0` claim is made.

## Source Register
| source_id | source_path | exists | needle_found | needles |
| --- | --- | --- | --- | --- |
| SRC1570_0_1569_doc | 1569-Y5-RAB-first-internal-ZR-or-tauR10-projection-row.md | True | True | first external R10 metadata source is now localized; source-normalization kernel is missing |
| SRC1570_1_1569_validation | source-intake/mts_residuals/P8_Y5_BRR545_1569_VALIDATION.csv | True | True | VAL1569_OVERALL; PASS |
| SRC1570_2_1569_decision | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1569_DECISION.csv | True | True | DEC1569_3_next; NEXT_1570_R10_CURVE_DIGITIZATION_OR_TAU_KERNEL_SOURCE_NORMALIZATION |
| SRC1570_3_1569_tau | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1569_TAU_R10_PROJECTION_ATTEMPT.csv | True | True | TAU1569_3_projection_kernel; KERNEL_CONTRACT_WRITTEN_NOT_FILLED |
| SRC1570_4_1569_external | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1569_EXTERNAL_R10_BOUND_METADATA_ROW.csv | True | True | EXTBOUND1569_R10_CROSSREF_PRL126_211101; LOCAL_CROSSREF_METADATA_PRESENT |
| SRC1570_5_pdf | source-intake/rab-sector/external/r10/1570/aps_harvest_fulltext.pdf | True | True | Combined Test of the Gravitational Inverse-Square Law at the Centimeter Range |
| SRC1570_6_text | source-intake/rab-sector/external/r10/1570/aps_harvest_fulltext.txt | True | True | FIG. 2. Constraints on Y; function of λ |
| SRC1570_7_fig2 | source-intake/rab-sector/external/r10/1570/extracted_images/page_5_image_1_Im3.png | True | True |  |

## PDF/Figure Source Audit
| audit_id | local_path | exists | bytes | anchor | anchor_found | status |
| --- | --- | --- | --- | --- | --- | --- |
| PDF1570_0_pdf_payload | source-intake/rab-sector/external/r10/1570/aps_harvest_fulltext.pdf | True | 428290 | Combined Test of the Gravitational Inverse-Square Law at the Centimeter Range | True | LOCAL_FULLTEXT_PDF_PAYLOAD_PRESENT |
| PDF1570_1_text_extract | source-intake/rab-sector/external/r10/1570/aps_harvest_fulltext.txt | True | 25459 | FIG. 2. Constraints on Y | True | TEXT_EXTRACTION_PRESENT |
| PDF1570_2_fig2_image | source-intake/rab-sector/external/r10/1570/extracted_images/page_5_image_1_Im3.png | True | 131273 | page_5_image_1_Im3.png | True | FIG2_IMAGE_EXTRACTED |

## Digitization Method
| method_id | method_piece | value | status | risk |
| --- | --- | --- | --- | --- |
| METHOD1570_0_source | source assets | pdf=source-intake/rab-sector/external/r10/1570/aps_harvest_fulltext.pdf; text=source-intake/rab-sector/external/r10/1570/aps_harvest_fulltext.txt; fig2=source-intake/rab-sector/external/r10/1570/extracted_images/page_5_image_1_Im3.png | LOCAL_SOURCE_ASSETS_PRESENT | figure tracing still needs manual QA before accepted use |
| METHOD1570_1_axis_calibration | log axis calibration | x_left=114.0 at lambda=1e-3; x_decade=243.0 px; y_top=20.0 at alpha=1; y_decade=155.0 px | MANUAL_IMAGE_CALIBRATION_CANDIDATE | axis calibration is approximate and must be QA'd against plot ticks |
| METHOD1570_2_curve_detection | blue pixel connected components | points=78 | CANDIDATE_TRACE_CREATED | blue arrow/text may contaminate candidate; no claim until cleaned |
| METHOD1570_3_acceptance | accepted curve gate | manual or independent digitization check required before valid_for_claim | NOT_ACCEPTED | candidate curve can support tooling smoke tests only |

## Digitized Curve Candidate
| point_id | lambda_m | alpha_abs_bound | pixel_x | pixel_y | curve | digitization_status |
| --- | --- | --- | --- | --- | --- | --- |
| DIG1570_000 | 0.0012673036 | 1 | 139 | 20.00 | This_work_blue_curve | CANDIDATE_IMAGE_TRACE_NONCLAIM |
| DIG1570_001 | 0.0013932624 | 0.60795435 | 149 | 53.50 | This_work_blue_curve | CANDIDATE_IMAGE_TRACE_NONCLAIM |
| DIG1570_002 | 0.0015317405 | 0.3431499 | 159 | 92.00 | This_work_blue_curve | CANDIDATE_IMAGE_TRACE_NONCLAIM |
| DIG1570_003 | 0.001683982 | 0.19952623 | 169 | 128.50 | This_work_blue_curve | CANDIDATE_IMAGE_TRACE_NONCLAIM |
| DIG1570_004 | 0.001851355 | 0.11515699 | 179 | 165.50 | This_work_blue_curve | CANDIDATE_IMAGE_TRACE_NONCLAIM |
| DIG1570_005 | 0.0020353635 | 0.069492108 | 189 | 199.50 | This_work_blue_curve | CANDIDATE_IMAGE_TRACE_NONCLAIM |
| DIG1570_006 | 0.0022376607 | 0.043200012 | 199 | 231.50 | This_work_blue_curve | CANDIDATE_IMAGE_TRACE_NONCLAIM |
| DIG1570_007 | 0.0024600645 | 0.027460578 | 209 | 262.00 | This_work_blue_curve | CANDIDATE_IMAGE_TRACE_NONCLAIM |
| DIG1570_008 | 0.0027045734 | 0.01798203 | 219 | 290.50 | This_work_blue_curve | CANDIDATE_IMAGE_TRACE_NONCLAIM |
| DIG1570_009 | 0.0029733842 | 0.012311829 | 229 | 316.00 | This_work_blue_curve | CANDIDATE_IMAGE_TRACE_NONCLAIM |
| DIG1570_010 | 0.0032689125 | 0.0084924355 | 239 | 341.00 | This_work_blue_curve | CANDIDATE_IMAGE_TRACE_NONCLAIM |
| DIG1570_011 | 0.0035938137 | 0.0060345538 | 249 | 364.00 | This_work_blue_curve | CANDIDATE_IMAGE_TRACE_NONCLAIM |
| DIG1570_012 | 0.0039510072 | 0.0044173447 | 259 | 385.00 | This_work_blue_curve | CANDIDATE_IMAGE_TRACE_NONCLAIM |
| DIG1570_013 | 0.0043437026 | 0.003257641 | 269 | 405.50 | This_work_blue_curve | CANDIDATE_IMAGE_TRACE_NONCLAIM |
| DIG1570_014 | 0.0047754285 | 0.0024203098 | 279 | 425.50 | This_work_blue_curve | CANDIDATE_IMAGE_TRACE_NONCLAIM |
| DIG1570_015 | 0.0052500641 | 0.0018524306 | 289 | 443.50 | This_work_blue_curve | CANDIDATE_IMAGE_TRACE_NONCLAIM |
| DIG1570_016 | 0.0057718744 | 0.0014177932 | 299 | 461.50 | This_work_blue_curve | CANDIDATE_IMAGE_TRACE_NONCLAIM |
| DIG1570_017 | 0.006345548 | 0.0011095868 | 309 | 478.00 | This_work_blue_curve | CANDIDATE_IMAGE_TRACE_NONCLAIM |
| DIG1570_018 | 0.0069762398 | 0.0008748538 | 319 | 494.00 | This_work_blue_curve | CANDIDATE_IMAGE_TRACE_NONCLAIM |
| DIG1570_019 | 0.0076696167 | 0.00070532146 | 329 | 508.50 | This_work_blue_curve | CANDIDATE_IMAGE_TRACE_NONCLAIM |
| DIG1570_020 | 0.0084319093 | 0.00056864171 | 339 | 523.00 | This_work_blue_curve | CANDIDATE_IMAGE_TRACE_NONCLAIM |
| DIG1570_021 | 0.009269967 | 0.00046877856 | 349 | 536.00 | This_work_blue_curve | CANDIDATE_IMAGE_TRACE_NONCLAIM |
| DIG1570_022 | 0.01019132 | 0.00039516111 | 359 | 547.50 | This_work_blue_curve | CANDIDATE_IMAGE_TRACE_NONCLAIM |
| DIG1570_023 | 0.011204248 | 0.00033558802 | 369 | 558.50 | This_work_blue_curve | CANDIDATE_IMAGE_TRACE_NONCLAIM |
| DIG1570_024 | 0.012317852 | 0.00028926129 | 379 | 568.50 | This_work_blue_curve | CANDIDATE_IMAGE_TRACE_NONCLAIM |
| DIG1570_025 | 0.013542138 | 0.00025118864 | 389 | 578.00 | This_work_blue_curve | CANDIDATE_IMAGE_TRACE_NONCLAIM |
| DIG1570_026 | 0.014888108 | 0.00021651295 | 399 | 588.00 | This_work_blue_curve | CANDIDATE_IMAGE_TRACE_NONCLAIM |
| DIG1570_027 | 0.016367855 | 0.00019082935 | 409 | 596.50 | This_work_blue_curve | CANDIDATE_IMAGE_TRACE_NONCLAIM |
| DIG1570_028 | 0.017994676 | 0.00016694778 | 419 | 605.50 | This_work_blue_curve | CANDIDATE_IMAGE_TRACE_NONCLAIM |
| DIG1570_029 | 0.019783189 | 0.0001482408 | 429 | 613.50 | This_work_blue_curve | CANDIDATE_IMAGE_TRACE_NONCLAIM |

## tau_R10 Kernel Gate
| gate_id | target | current_status | result |
| --- | --- | --- | --- |
| TAUG1570_0_external_bound | external alpha(lambda) curve | candidate curve now exists | CANDIDATE_NONCLAIM |
| TAUG1570_1_internal_range | lambda_R=sqrt(Z_R/M_R^2) | Z_R and M_R^2 missing | BLOCKED |
| TAUG1570_2_internal_amplitude | alpha_MTS=tau_R10*A_R | A_R/J_R/B_R/readout source normalization missing | BLOCKED |
| TAUG1570_3_comparator | abs(alpha_MTS(lambda_R)) <= alpha_bound(lambda_R) | cannot evaluate without internal projection | BLOCKED |
| TAUG1570_4_verdict | tau kernel source normalization | not derived; candidate curve only improves external side | NOT_READY |

## Runner
| runner_id | test | current_status | detail |
| --- | --- | --- | --- |
| RUN1570_0_sources | load 1569 handoff and R10 PDF/text/figure | PASS | all source register needles found |
| RUN1570_1_curve | candidate R10 alpha(lambda) digitization | PASS_CANDIDATE_NONCLAIM | candidate_points=78 |
| RUN1570_2_acceptance | accepted R10 bound curve | NOT_ACCEPTED | manual/independent QA required |
| RUN1570_3_tau | tau_R10 source-normalized projection | BLOCKED_NO_CLAIM | internal source normalization missing |
| RUN1570_4_raw_accepted | raw/accepted finite rows | NO_LIVE_SCORE_ROWS | raw_rows=0; accepted_rows=0 |
| RUN1570_5_claim | R10/local GR claim | BLOCKED_NO_CLAIM | candidate curve exists but internal MTS prediction is missing |

## Claim Gates
| gate_id | claim_gate | status | reason |
| --- | --- | --- | --- |
| GATE1570_0_curve_candidate | candidate R10 bound curve | PASS_NONCLAIM | image-trace candidate exists but is not accepted |
| GATE1570_1_curve_accepted | accepted R10 bound curve | BLOCKED_NO_CLAIM | manual/independent digitization QA missing |
| GATE1570_2_tau_kernel | tau_R10 source-normalized projection | BLOCKED_NO_CLAIM | internal source normalization missing |
| GATE1570_3_MTS_prediction | alpha_MTS(lambda) | BLOCKED_NO_CLAIM | Z_R/M_R2/J_R/B_R/readout inputs missing |
| GATE1570_4_local_GR | derived local GR/Newton/R10 safety | BLOCKED_NO_CLAIM | external curve alone is not theory evidence |

## Decision
| decision_id | decision | result | reason |
| --- | --- | --- | --- |
| DEC1570_0_curve | R10 bound curve | CANDIDATE_DIGITIZED_CURVE_CREATED_NONCLAIM | Fig. 2 blue curve was extracted and traced, but requires QA before accepted use |
| DEC1570_1_tau | tau_R10 kernel | SOURCE_NORMALIZATION_MISSING | external curve side improved; internal MTS projection still missing |
| DEC1570_2_next | next target | NEXT_1571_DIGITIZATION_QA_OR_TAU_R10_INTERNAL_KERNEL | either QA the digitized curve or derive/fill the internal tau_R10 projection kernel |

## Validation
| check_id | result | detail |
| --- | --- | --- |
| VAL1570_0_sources_exist | PASS | all cited 1570 source paths exist |
| VAL1570_1_needles_found | PASS | all registered evidence needles found |
| VAL1570_2_pdf_assets | PASS | PDF/text/Fig2 assets exist and are anchored |
| VAL1570_3_method_recorded | PASS | digitization method and nonacceptance recorded |
| VAL1570_4_curve_candidate | PASS | candidate digitized curve rows created |
| VAL1570_5_curve_positive | PASS | candidate curve lambda/alpha values are positive |
| VAL1570_6_tau_blocked | PASS | tau kernel remains not ready |
| VAL1570_7_raw_accepted_empty | PASS | raw/accepted finite rows remain empty |
| VAL1570_8_runner_blocks_claim | PASS | runner blocks local/R10 claim |
| VAL1570_9_claim_gates | PASS | claim gates remain closed |
| VAL1570_10_decision_next | PASS | decision selects digitization QA or tau kernel |
| VAL1570_11_next_target | PASS | next target is digitization QA or tau kernel |
| VAL1570_12_csv_parse | PASS | all generated 1570 CSVs parse cleanly |
| VAL1570_13_claim_flags_false | PASS | all generated prediction/claim flags remain false |
| VAL1570_14_branch_copies | PASS | branch/quarantine nonclaim copies written |
| VAL1570_15_pycache_absent | PASS | scripts __pycache__ absent after run |
| VAL1570_16_formalization_untouched | PASS | formalization modified-file count since start=0 |
| VAL1570_OVERALL | PASS | 1570 R10 curve digitization or tau kernel source-normalization validation |

## Next Target
| next_target | script | objective | do_not |
| --- | --- | --- | --- |
| 1571-Y5-RAB-R10-digitization-QA-or-tauR10-internal-kernel.md | scripts/Y5_RAB_R10_digitization_QA_or_tauR10_internal_kernel.py | QA/clean the candidate R10 digitized curve and separately try to derive the internal tau_R10 source-normalization kernel from Z_R/M_R2/J_R/B_R/readout inputs | do not accept the candidate curve without QA; do not claim R10 pass without an internal MTS prediction; do not edit formalization-workbench |
