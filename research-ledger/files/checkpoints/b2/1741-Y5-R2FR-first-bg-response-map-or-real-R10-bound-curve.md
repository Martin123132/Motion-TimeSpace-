# 1741 - First b_g Response Map Or Real R10 Bound Curve

## Verdict
- 1741 chooses the first `b_g` response map route because the Cassini PPN gamma bound is already locally sourced, while the R10 curve is still placeholder-only.
- The first source-backed response row is conditional and nonclaim: a universal conformal shadow frame with `sigma_X=s_X U/c^2` gives `gamma_eff=(1+s_X)/(1-s_X)`.
- Linearized, Cassini's `|gamma-1| <= 2.3e-5` implies `|s_X| <= 1.15e-5` only if no other PPN/source channels contribute.
- MTS still has no numeric PPN claim because `b_g`, the `X_U` profile coefficient, source normalization, and no-other-channel theorem are missing.
- R10 remains blocked because the curve file is a placeholder, not a real digitized alpha(lambda) table.

## Source Register
| source_id | source_key | source_path | exists | needles_present |
| --- | --- | --- | --- | --- |
| SRC1741_0_1740_doc | 1740_handoff_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1740-Y5-R2FR-no-shadow-frame-zero-or-bg-bound-projection-map.md | True | True |
| SRC1741_1_1740_projection_map | 1740_bg_projection_map | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1740_BG_BOUND_PROJECTION_MAP.csv | True | True |
| SRC1741_2_1740_bound_inputs | 1740_bg_bound_inputs | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1740_BG_BOUND_INPUT_ROWS.csv | True | True |
| SRC1741_3_1739_bg_rows | 1739_bg_rows | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1739_COMMON_FRAME_LOG_DERIVATIVE_ROWS.csv | True | True |
| SRC1741_4_local_bounds | local_bound_claims | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\local_bound_claims.csv | True | True |
| SRC1741_5_R10_curve | R10_alpha_lambda_curve | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\R10_alpha_lambda_bound_curve_DIGITIZED.csv | True | True |
| SRC1741_6_785_ppn_chain | 785_GR_Newton_reduction | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_785_PSI_METRIC_COFRAME_CONTRACT.csv | True | True |
| SRC1741_7_1504_countermodel | 1504_common_frame_countermodel | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1504_OBSERVED_COFRAME_INDEPENDENCE_AUDIT.csv | True | True |

## b_g Response Map
| response_id | ansatz | observable | derived_response | empirical_upper_bound | conditional_linear_sX_bound | missing_inputs |
| --- | --- | --- | --- | --- | --- | --- |
| BRM1741_0_conformal_PPN_gamma | g_obs=e^(2 sigma_X) g_GR with sigma_X=s_X U/c^2 and s_X=b_g,X x_U | gamma_minus_1 | gamma_eff=(1+s_X)/(1-s_X); gamma_minus_1=2 s_X/(1-s_X) ~= 2 s_X for \|s_X\|<<1 | 2.3e-05 | 1.15e-05 | MISSING_BG_VALUE;MISSING_X_U_PROFILE;MISSING_SOURCE_NORMALIZATION;MISSING_NO_OTHER_CHANNELS |
| BRM1741_1_WEP_conformal_common_mode_guard | all ordinary matter sees the same conformal e_obs | eta_AB | pure universal metric scaling does not produce composition dependence by itself; WEP needs source/readout/marker/species-prefactor leakage | 2.8e-15 | NOT_DIRECT_WITHOUT_COMPOSITION_MAP | MISSING_SOURCE_READOUT_MARKER_MAP;MISSING_DELTA_W_AB;MISSING_RESPONSE_COEFFICIENT |

## PPN Gamma Bound Bridge
| bridge_id | dataset_id | observable | upper_bound | bridge_formula | linearized_sX_bound | bridge_status |
| --- | --- | --- | --- | --- | --- | --- |
| PGB1741_0_Cassini_gamma_bridge | Cassini_Shapiro_gamma_2003 | gamma_minus_1 | 2.3e-05 | if sigma_X=s_X U/c^2 and no other PPN channels, \|2 s_X/(1-s_X)\| <= upper_bound | 1.15e-05 | SOURCE_BACKED_CONDITIONAL_NONCLAIM |

## R10 Curve Status
| curve_row_id | source_bound_id | lambda_value | alpha_bound | digitization_method | curve_status |
| --- | --- | --- | --- | --- | --- |
| R10CURVE1741_0 | R10_BOUND_PLACEHOLDER_0 | MISSING_NUMERIC_LAMBDA | MISSING_DIGITIZED_ALPHA_BOUND | template_invalid_missing_digitized_curve | PLACEHOLDER_NONCLAIM |
| R10CURVE1741_1 | R10_BOUND_PLACEHOLDER_1 | MISSING_NUMERIC_LAMBDA | MISSING_DIGITIZED_ALPHA_BOUND | template_invalid_missing_source | PLACEHOLDER_NONCLAIM |

## Response Claim Gate
| gate_id | claim_piece | gate_status | evidence |
| --- | --- | --- | --- |
| RCG1741_0_response_map_exists | first b_g response map exists | PASS_NONCLAIM | BRM1741_0_conformal_PPN_gamma gives source-backed conditional map to Cassini gamma |
| RCG1741_1_numeric_prediction | MTS predicts gamma_minus_1 from b_g | BLOCKED | MISSING_BG_VALUE;MISSING_X_U_PROFILE;MISSING_NO_OTHER_CHANNELS |
| RCG1741_2_R10_curve | R10 curve is real and score-ready | BLOCKED | R10 curve rows remain placeholder/nonclaim |

## Runner Refusal
| runner_id | runner | current_status | reason |
| --- | --- | --- | --- |
| RUN1741_0_gamma_response_smoke | b_g to Cassini gamma comparison | REFUSE_CLAIM_RUN | response map exists, but b_g value, X_U profile and no-other-channel proof are missing |
| RUN1741_1_R10_curve_scoring | R10 alpha(lambda) scoring | REFUSE_CLAIM_RUN | digitized R10 bound curve remains placeholder/nonclaim |

## Decisions
| decision_id | decision | reason | next_action |
| --- | --- | --- | --- |
| DEC1741_0_route_choice | FIRST_BG_RESPONSE_MAP_CHOSEN_OVER_R10_CURVE | Cassini gamma bound is already locally sourced while R10 curve file is placeholder-only | use PPN gamma bridge as first empirical discipline row |
| DEC1741_1_gamma_bridge | CONFORMAL_BG_TO_GAMMA_MAP_STAGED | universal conformal shadow frame produces gamma_eff=(1+s)/(1-s) after Newtonian normalization | derive or source s_X=b_g,X x_U profile coefficient |
| DEC1741_2_claim_status | NO_NUMERIC_MTS_PPN_CLAIM | b_g, X_U profile, source normalization and other channels are missing | keep PPN/WEP/R10 claims blocked |
| DEC1741_3_best_next_domino | TARGET_SIGMAX_PROFILE_OR_REAL_R10_CURVE | the response map is now available; the missing empirical ingredient is either s_X profile or the real R10 curve | derive/source x_U for b_g gamma map, or digitize/acquire real R10 alpha(lambda) |

## Claim Gates
| gate_id | claim | gate_pass | status | blocker |
| --- | --- | --- | --- | --- |
| GATE1741_0_response_source | first b_g response map is source-backed | True | PASS_NONCLAIM_ONLY | claim still blocked by missing b_g and X_U profile |
| GATE1741_1_gamma_score | MTS passes Cassini gamma via b_g map | False | BLOCKED | MISSING_BG_VALUE_AND_X_U_PROFILE |
| GATE1741_2_R10_score | MTS passes R10 shadow-frame bound | False | BLOCKED | MISSING_REAL_R10_CURVE_AND_ALPHA_PREDICTION |

## Next Target
| route_id | next_target | script | objective | selection_status |
| --- | --- | --- | --- | --- |
| NEXT1741_0_primary | 1742-Y5-R2FR-sigmaX-profile-coefficient-or-real-R10-curve.md | scripts/Y5_R2FR_sigmaX_profile_coefficient_or_real_R10_curve.py | derive or source s_X=b_g,X x_U for the PPN gamma bridge, or replace the placeholder R10 alpha(lambda) curve | selected |
| NEXT1741_1_parallel_readout_marker | 1742b-Y5-R2FR-source-readout-marker-Dq-zero-or-finite-row.md | scripts/Y5_R2FR_source_readout_marker_Dq_zero_or_finite_row.py | prove source/readout and marker functors descend through q, or keep finite leak rows | held_parallel |

## Validation
| check_id | result | detail |
| --- | --- | --- |
| VAL1741_0_sources_exist | PASS | all cited source paths exist |
| VAL1741_1_needles_present | PASS | required source needles are present |
| VAL1741_2_response_map_present | PASS | first conformal b_g to PPN gamma response map exists |
| VAL1741_3_response_source_backed_nonclaim | PASS | response map is source-backed but nonclaim |
| VAL1741_4_gamma_bound_bridge | PASS | Cassini gamma bound bridge is recorded |
| VAL1741_5_R10_placeholder_blocked | PASS | R10 curve remains placeholder/nonclaim |
| VAL1741_6_claim_gate_blocks_numeric | PASS | numeric MTS gamma prediction remains blocked |
| VAL1741_7_runners_refuse | PASS | claim runners refuse missing response/R10 inputs |
| VAL1741_8_decision_next_domino | PASS | decision selects sigma_X profile or real R10 curve |
| VAL1741_9_claim_gates_safe | PASS | all claim gates keep local claims false |
| VAL1741_10_no_claim_flags | PASS | all generated rows keep claim/no-score flags false |
| VAL1741_11_missing_not_ready | PASS | no row containing MISSING_* is marked prediction-backed, claim-ready, or score-ready |
| VAL1741_12_next_selected | PASS | next target selects sigma_X profile coefficient or real R10 curve |
| VAL1741_13_csv_parse | PASS | all generated 1741 CSVs parse |
| VAL1741_14_branch_copies | PASS | branch/quarantine/queue copies exist |
| VAL1741_15_pycache_absent | PASS | scripts __pycache__ absent |
| VAL1741_16_formalization_untouched | PASS | no 1741 outputs found under formalization-workbench |
| VAL1741_OVERALL | PASS | 1741 first b_g response map or real R10 bound curve validation |

## Working Interpretation
This is the first real counter-punch from the local branch into a published local bound. It does not prove MTS passes Cassini; it tells us exactly what must be derived next: the profile coefficient `s_X=b_g,X x_U`, or a real R10 curve if we want to fight the short-range round instead.
