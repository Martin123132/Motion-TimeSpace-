# 904 - Y5/R10 Finite Alpha Source Provenance And Real Bound Curve Gate

Status: `Y5_R10_904_finite_alpha_source_provenance_and_real_bound_curve_gate_built_anchor_only_nonclaim`
Claim ceiling: `source_provenance_and_anchor_only_R10_bound_gate_no_digitized_curve_no_numeric_MTS_alpha_no_R10_or_local_GR_claim`
Generated UTC: `2026-06-13T14:44:09.961241+00:00`

Current result: **the R10 testing path is now split into two hard gates: MTS must source `Z_tr`, `lambda_tr`, `Q_tr/m`, and response coefficients; the experiment side must provide a real digitized/source-table `alpha(lambda)` curve.** Lee 2020 gives a source-backed `alpha=1` threshold anchor at `lambda=38.6 um`, but that is not a curve and it is not enough for interpolation, model comparison, or a pass.

## Exact 904 Finding
The evidence situation is clean now. The local trace coupling is not testable yet because the MTS-side `alpha_tr(lambda_tr)` row is still missing parent inputs. The R10 bound side has credible modern provenance, but only anchor rows were acquired here. The existing R10 runner correctly refuses the dry rows because there are zero valid MTS rows and zero valid bound rows.

## Nonclaim Summary
| status | claim_ceiling | what_changed | best_partial_result | hard_blockers | what_is_not_claimed | next_target | valid_for_claim | generated_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Y5_R10_904_finite_alpha_source_provenance_and_real_bound_curve_gate_built_anchor_only_nonclaim | source_provenance_and_anchor_only_R10_bound_gate_no_digitized_curve_no_numeric_MTS_alpha_no_R10_or_local_GR_claim | split finite trace alpha into MTS-side parent provenance and experiment-side R10 bound-curve provenance | Lee 2020 provides a source-backed alpha=1 threshold anchor at lambda=38.6 um and scan metadata, but not a local claim-grade digitized curve in this checkpoint | MTS lacks Z_tr/lambda_tr/Q_tr/m/response coefficients; R10 lacks full digitized alpha(lambda) bound curve; APS supplement acquisition is blocked/unconfirmed | finite alpha value, R10 pass, alpha=0, Q_tr=0, local GR/Newton, or public bound satisfaction | 905-Y5-R10-parent-finite-alpha-input-owner-or-digitized-bound-curve-worker.md | false | 2026-06-13T14:44:09.961241+00:00 |

## Local Source Register
| source_id | path | exists | needle_check | role | valid_for_claim | generated_utc |
| --- | --- | --- | --- | --- | --- | --- |
| 903_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\903-Y5-R10-Qtr-source-cokernel-final-zero-proof-or-finite-alpha-source.md | true | pass | immediate handoff from failed Q_tr theorem promotion | false | 2026-06-13T14:44:09.961241+00:00 |
| 903_validation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_903_VALIDATION.csv | true | pass | prior checkpoint validation | false | 2026-06-13T14:44:09.961241+00:00 |
| 903_finite_alpha_rows | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_903_FINITE_ALPHA_SOURCE_ROWS.csv | true | pass | MTS finite alpha input debt | false | 2026-06-13T14:44:09.961241+00:00 |
| 903_qtr_zero_clauses | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_903_QTR_ZERO_PROOF_CLAUSES.csv | true | pass | conditional theorem ceiling | false | 2026-06-13T14:44:09.961241+00:00 |
| r10_runner | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\scripts\R10_alpha_lambda_bound_prediction_runner.py | true | pass | existing R10 alpha(lambda) comparator | false | 2026-06-13T14:44:09.961241+00:00 |
| live_bound_placeholder | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\R10_alpha_lambda_bound_curve_DIGITIZED.csv | true | pass | live bound curve remains placeholder/nonclaim | false | 2026-06-13T14:44:09.961241+00:00 |

## Web Source Anchors
| web_source_id | title | authors | year | url | doi | source_role | usable_facts | curve_status | valid_for_claim | generated_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R10SRC904_0_Lee2020_arxiv | New Test of the Gravitational 1/r^2 Law at Separations down to 52 um | J.G. Lee; E.G. Adelberger; T.S. Cook; S.M. Fleischer; B.R. Heckel | 2020 | https://arxiv.org/abs/2002.11761 | 10.1103/PhysRevLett.124.101101 | modern R10 short-range anchor | Yukawa form; data separations 52 um to 3.0 mm; 66 lambda values from 5 um to 9 mm; 95 percent alpha=1 threshold at 38.6 um | figure_and_supplement_reference_only_not_digitized_here | false | 2026-06-13T14:44:09.961241+00:00 |
| R10SRC904_1_EotWash_page | Eot-Wash Inverse Square Law current published results | Eot-Wash Group | 2023 | https://www.npl.washington.edu/eotwash/inverse-square-law |  | experiment-group context and figure provenance | page describes 95 percent confidence constraints on Yukawa violation; axes are relative strength and characteristic range; Lee 2020 is the cited current result | visual constraint context_only_no_machine_table | false | 2026-06-13T14:44:09.961241+00:00 |
| R10SRC904_2_Kapner2007_arxiv | Tests of the Gravitational Inverse-Square Law below the Dark-Energy Length Scale | D.J. Kapner; T.S. Cook; E.G. Adelberger; J.H. Gundlach; B.R. Heckel; C.D. Hoyle; H.E. Swanson | 2007 | https://arxiv.org/abs/hep-ph/0611184 | 10.1103/PhysRevLett.98.021101 | continuity anchor for older Eot-Wash bounds | separations 9.53 mm to 55 um; 95 percent alpha<=1 down to lambda=56 um | older anchor_only_non_curve | false | 2026-06-13T14:44:09.961241+00:00 |
| R10SRC904_3_Adelberger2003_review | Tests of the Gravitational Inverse-Square Law | E.G. Adelberger; B.R. Heckel; A.E. Nelson | 2003 | https://arxiv.org/abs/hep-ph/0307284 | 10.1146/annurev.nucl.53.041002.110503 | review/continuity source for inverse-square-law formalism | review of experimental tests and motivations for inverse-square-law breakdown | review_context_only_not_curve | false | 2026-06-13T14:44:09.961241+00:00 |
| R10SRC904_4_APS_supplement | Lee 2020 APS supplemental material | J.G. Lee et al. | 2020 | https://link.aps.org/supplemental/10.1103/PhysRevLett.124.101101 | 10.1103/PhysRevLett.124.101101 | preferred numerical curve source if accessible | search result states supplemental material has numerical values for Fig. 5 and fitting details | access_attempt_blocked_403_in_shell; must acquire manually or via allowed source before claim | false | 2026-06-13T14:44:09.961241+00:00 |

## Finite Alpha Provenance Gate
| provenance_id | quantity | priority | required_parent_input | current_value | current_status | required_source_path | numeric_gate | claim_gate | valid_for_claim | generated_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FAP904_0 | P_tr,H_tr | branch_decision_primary | parent trace projector and Hessian after gauge/constraint reduction | MISSING_PARENT_PROJECTOR_HESSIAN | MISSING_OR_UNSIGNED | MISSING_PARENT_SOURCE_PATH_OR_ZERO_THEOREM | must be finite numeric with units or theorem-zero/no-pole | false_until_no_MISSING_markers_and_source_path_exists | false | 2026-06-13T14:44:09.961241+00:00 |
| FAP904_1 | Z_tr | R10_primary | principal symbol of the trace Hessian on observed local metric background | MISSING_PARENT_SYMBOL | MISSING_OR_UNSIGNED | MISSING_PARENT_SOURCE_PATH_OR_ZERO_THEOREM | must be finite numeric with units or theorem-zero/no-pole | false_until_no_MISSING_markers_and_source_path_exists | false | 2026-06-13T14:44:09.961241+00:00 |
| FAP904_2 | lambda_tr | R10_primary | parent mass gap or no-pole certificate | MISSING_MASS_GAP_OR_NOPOLE | MISSING_OR_UNSIGNED | MISSING_PARENT_SOURCE_PATH_OR_ZERO_THEOREM | must be finite numeric with units or theorem-zero/no-pole | false_until_no_MISSING_markers_and_source_path_exists | false | 2026-06-13T14:44:09.961241+00:00 |
| FAP904_3 | Q_tr_over_m_universal | R10_primary | body-source functional or source-cokernel zero theorem | MISSING_SOURCE_PROJECTION_OR_ZERO_THEOREM | MISSING_OR_UNSIGNED | MISSING_PARENT_SOURCE_PATH_OR_ZERO_THEOREM | must be finite numeric with units or theorem-zero/no-pole | false_until_no_MISSING_markers_and_source_path_exists | false | 2026-06-13T14:44:09.961241+00:00 |
| FAP904_4 | Delta_AB_Q_tr_over_m,C_tr_clock_i,C_tr_alphaEM | local_arena_secondary | species/clock/EM no-marker theorem or sourced response coefficients | MISSING_NO_MARKER_OR_COEFFICIENTS | MISSING_OR_UNSIGNED | MISSING_PARENT_SOURCE_PATH_OR_ZERO_THEOREM | must be finite numeric with units or theorem-zero/no-pole | false_until_no_MISSING_markers_and_source_path_exists | false | 2026-06-13T14:44:09.961241+00:00 |
| FAP904_5 | C_tr_gamma,C_tr_beta,C_tr_source,Gdot_tr | local_arena_secondary | weak-field response and measured-GM/source-normalization split | MISSING_RESPONSE_OPERATOR | MISSING_OR_UNSIGNED | MISSING_PARENT_SOURCE_PATH_OR_ZERO_THEOREM | must be finite numeric with units or theorem-zero/no-pole | false_until_no_MISSING_markers_and_source_path_exists | false | 2026-06-13T14:44:09.961241+00:00 |
| FAP904_6 | alpha_tr_AB(lambda_tr) | R10_primary | derived Z_tr, lambda_tr, Q_tr/m plus claim-grade R10 bound curve | MISSING_Z_LAMBDA_Q_INPUTS_AND_BOUND_CURVE | MISSING_OR_UNSIGNED | MISSING_PARENT_SOURCE_PATH_OR_ZERO_THEOREM | must be finite numeric with units or theorem-zero/no-pole | false_until_no_MISSING_markers_and_source_path_exists | false | 2026-06-13T14:44:09.961241+00:00 |
| FAP904_7 | B_tr_tail,K_perp_trace | branch_decision_primary | boundary support/no-tail certificate or explicit residual bound | MISSING_BOUNDARY_SUPPORT_CERTIFICATE_OR_BOUND | MISSING_OR_UNSIGNED | MISSING_PARENT_SOURCE_PATH_OR_ZERO_THEOREM | must be finite numeric with units or theorem-zero/no-pole | false_until_no_MISSING_markers_and_source_path_exists | false | 2026-06-13T14:44:09.961241+00:00 |

## R10 Bound Anchor Rows
| bound_id | dataset_id | lambda_value | lambda_units | alpha_bound | alpha_bound_source | digitization_method | source_file | valid_for_claim | notes | confidence | row_type | curve_claim_status | generated_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R10_904_LEE2020_ALPHA1_38P6UM_ANCHOR | Lee_Adelberger_Cook_Fleischer_Heckel_PRL124_101101_2020 | 38.6 | um | 1.0 | https://arxiv.org/abs/2002.11761; doi:10.1103/PhysRevLett.124.101101 | source_text_threshold_anchor_only_non_curve | https://arxiv.org/abs/2002.11761 | false | source-backed alpha=1 threshold; not a digitized alpha(lambda) curve and cannot support interpolation or claim scoring | 95_percent_or_2sigma_context | anchor_only_non_curve | invalid_for_claim_until_full_curve_or_supplement_table | 2026-06-13T14:44:09.961241+00:00 |
| R10_904_KAPNER2007_ALPHA1_56UM_ANCHOR | Kapner_Cook_Adelberger_Gundlach_Heckel_Hoyle_Swanson_PRL98_021101_2007 | 56 | um | 1.0 | https://arxiv.org/abs/hep-ph/0611184; doi:10.1103/PhysRevLett.98.021101 | source_text_threshold_anchor_only_non_curve | https://arxiv.org/abs/hep-ph/0611184 | false | older alpha=1 continuity anchor; not current full curve and cannot support MTS claim scoring | 95_percent | anchor_only_non_curve | invalid_for_claim_until_full_curve_or_supplement_table | 2026-06-13T14:44:09.961241+00:00 |

## R10 Curve Acquisition Gate
| gate_id | bound_artifact | priority | current_status | acceptance_rule | valid_for_claim | generated_utc |
| --- | --- | --- | --- | --- | --- | --- |
| RCG904_0_full_abs_alpha_curve | full /alpha/(lambda) exclusion curve | preferred | not_acquired | must contain multiple positive numeric lambda/alpha rows across the plotted range with extraction method and source | false | 2026-06-13T14:44:09.961241+00:00 |
| RCG904_1_positive_negative_curves | +alpha and -alpha curves from supplemental material | preferred_if_supplement_available | not_acquired | must preserve sign branch and confidence convention before conversion to /alpha/ gate | false | 2026-06-13T14:44:09.961241+00:00 |
| RCG904_2_fig5_digitization | digitized Fig. 5 lower panel | acceptable_private_smoke_only | not_done | requires image source, axis calibration, digitization uncertainty, and nonclaim label until audited | false | 2026-06-13T14:44:09.961241+00:00 |
| RCG904_3_text_threshold_anchor | alpha=1 threshold at 38.6 um from Lee 2020 | anchor_only | acquired_nonclaim | may sanity-check units but cannot support interpolation or claim scoring | false | 2026-06-13T14:44:09.961241+00:00 |
| RCG904_4_live_bound_file | source-intake/local_bounds/R10_alpha_lambda_bound_curve_DIGITIZED.csv | live_claim_file | still_placeholder | must not be treated as evidence until placeholder rows are replaced by full source-backed curve rows | false | 2026-06-13T14:44:09.961241+00:00 |

## R10 Alpha Dry Rows
| model_id | branch_id | curve_id | lambda_value | lambda_units | alpha_predicted | alpha_bound | alpha_bound_source | force_law_form | derivation_status | formula_reference | source_file | assumptions | valid_for_claim | notes | generated_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_trace_finite_alpha_source_contract | finite_alpha_missing_parent_sources | FT904_R10_0_missing_MTS_alpha_inputs | MISSING_LAMBDA_TR | m | MISSING_ZTR_QTR_SOURCE_INPUTS | MISSING_BOUND_LOOKUP | source-intake/local_bounds/R10_alpha_lambda_bound_curve_904_SOURCE_BACKED_ANCHORS_NONCLAIM.csv | Yukawa alpha_tr_AB exp(-r/lambda_tr) | FINITE_ALPHA_SOURCE_PROVENANCE_MISSING | alpha_tr_AB=(Q_tr^A/m_A)*(Q_tr^B/m_B)/(4*pi*Z_tr*G_obs) | source-intake/mts_residuals/P8_Y5_R10_904_FINITE_ALPHA_PROVENANCE_GATE.csv | no numeric parent coefficients; bound file is anchor-only nonclaim | false | runner must reject this row until parent values and full bound curve are real | 2026-06-13T14:44:09.961241+00:00 |
| MTS_trace_Qtr_zero_escape | Qtr_zero_not_parent_signed | FT904_R10_1_Qtr_zero_still_unsigned | 38.6 | um | 0.0 | 1.0 | source-intake/local_bounds/R10_alpha_lambda_bound_curve_904_SOURCE_BACKED_ANCHORS_NONCLAIM.csv | alpha_tr=0 only if Q_tr=0 or no local trace pole is parent-signed | QTR_ZERO_THEOREM_UNSIGNED_NONCLAIM | 903 Q_tr source-cokernel theorem clauses | source-intake/mts_residuals/P8_Y5_R10_903_QTR_ZERO_PROOF_CLAUSES.csv | numeric alpha shown only as theorem-shape smoke row; theorem is unsigned and row is invalid | false | prevents accidentally counting alpha=0 as a pass before theorem promotion | 2026-06-13T14:44:09.961241+00:00 |

## Branch Decision
| branch_id | branch | decision | reason | claim_allowed | valid_for_claim | generated_utc |
| --- | --- | --- | --- | --- | --- | --- |
| BD904_0_MTS_parent_inputs | source Z_tr/lambda_tr/Q_tr/m and response coefficients | dominant_blocker | without MTS-side alpha(lambda) inputs, even a perfect R10 curve cannot score the theory | false | false | 2026-06-13T14:44:09.961241+00:00 |
| BD904_1_R10_bound_curve | acquire full digitized/source table R10 bound curve | parallel_data_blocker | Lee 2020 gives source-backed anchors and figure/supplement provenance, but not a claim-grade curve in this checkpoint | false | false | 2026-06-13T14:44:09.961241+00:00 |
| BD904_2_selected_next | parent finite alpha input owner or digitized curve worker | 905-Y5-R10-parent-finite-alpha-input-owner-or-digitized-bound-curve-worker.md | next useful step must choose whether to attack MTS parent coefficients first or launch a bounded curve-digitization worker; both remain private/nonclaim | false | false | 2026-06-13T14:44:09.961241+00:00 |

## Claim Gate
| gate_id | claim | claim_allowed | blocker | valid_for_claim | generated_utc |
| --- | --- | --- | --- | --- | --- |
| CGATE904_0_MTS_alpha | numeric MTS alpha_tr(lambda_tr) | false | Z_tr/lambda_tr/Q_tr/m are missing or theorem-dependent | false | 2026-06-13T14:44:09.961241+00:00 |
| CGATE904_1_R10_bound_curve | claim-grade R10 bound curve | false | only anchor rows are acquired; full curve/supplement table missing | false | 2026-06-13T14:44:09.961241+00:00 |
| CGATE904_2_R10_compare | R10 comparison pass | false | runner has zero valid MTS rows and zero valid bound rows | false | 2026-06-13T14:44:09.961241+00:00 |
| CGATE904_3_Qtr_zero | Q_tr=0 theorem | false | 903 proof remains unsigned | false | 2026-06-13T14:44:09.961241+00:00 |
| CGATE904_4_local_GR | local GR/Newton reduction | false | finite trace coupling not eliminated or bounded | false | 2026-06-13T14:44:09.961241+00:00 |

## Next Target
| next_target | objective | recommended_order | reason | valid_for_claim | generated_utc |
| --- | --- | --- | --- | --- | --- |
| 905-Y5-R10-parent-finite-alpha-input-owner-or-digitized-bound-curve-worker.md | choose the highest-yield next worker: parent finite-alpha input owner first, or R10 digitized-bound worker if empirical plumbing is prioritized | parent_inputs_first_then_bound_digitization | MTS alpha(lambda) is currently missing, so bound digitization alone cannot create a testable comparison | false | 2026-06-13T14:44:09.961241+00:00 |

## Validation
| check_id | result | detail | generated_utc |
| --- | --- | --- | --- |
| V904_0_sources_exist_and_needles | pass | all local source paths exist and needles are present | 2026-06-13T14:44:09.961241+00:00 |
| V904_1_prior_903_clean | pass | P8_Y5_BRR545_903_VALIDATION.csv clean | 2026-06-13T14:44:09.961241+00:00 |
| V904_2_web_anchors_recorded_nonclaim | pass | Lee/EotWash/Kapner/Adelberger/supplement rows recorded | 2026-06-13T14:44:09.961241+00:00 |
| V904_3_bound_anchor_rows_numeric_nonclaim | pass | anchor_rows=2 | 2026-06-13T14:44:09.961241+00:00 |
| V904_4_no_full_curve_claim | pass | full R10 curve remains unacquired/nonclaim | 2026-06-13T14:44:09.961241+00:00 |
| V904_5_finite_alpha_provenance_blocked | pass | finite_rows=8 | 2026-06-13T14:44:09.961241+00:00 |
| V904_6_runner_schema_ok | pass | schema ok | 2026-06-13T14:44:09.961241+00:00 |
| V904_7_R10_runner_blocks_claim | pass | {"blocked_or_failed_rows": 1, "claim_allowed": false, "valid_bound_rows": 0, "valid_mts_rows": 0} | 2026-06-13T14:44:09.961241+00:00 |
| V904_8_claim_gates_false | pass | all alpha/R10/local claims blocked | 2026-06-13T14:44:09.961241+00:00 |
| V904_9_all_generated_rows_nonclaim | pass | all generated rows keep valid_for_claim/claim_allowed false | 2026-06-13T14:44:09.961241+00:00 |
| V904_10_formalization_workbench_untouched | pass | formalization_changed_after_cutoff=0 | 2026-06-13T14:44:09.961241+00:00 |
| V904_11_next_target_selected | pass | 905-Y5-R10-parent-finite-alpha-input-owner-or-digitized-bound-curve-worker.md | 2026-06-13T14:44:09.961241+00:00 |
| V904_12_validation_rows_ready | pass | validation table constructed | 2026-06-13T14:44:09.961241+00:00 |
