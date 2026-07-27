# 1033 Y5 R10 tau_R10 projection derivation or source acquisition

**Status:** `tau_R10` is now defined as an R10 arena projection, not a magic constant. It cannot be set to one or scored until the full finite-branch factorization is sourced: `K_X(lambda)`, `Qbar_XH`, `tau_R10`, `c_g`, a digitized/source-backed `alpha_bound(lambda)` curve, and the retained-tail absolute envelope.

**Claim ceiling:** no `tau_R10` derivation claim, finite-`c_g` score, R10 pass, PPN pass, SPM-derived claim, local-GR/Newton pass, or source-side GR pass is allowed from 1033.

## Source register
| source_id | source_path | exists | needle_found | role |
| --- | --- | --- | --- | --- |
| SRC1033_0_1032_next | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1032_NEXT_TARGET.csv | true | true | 1032 handoff to tau_R10 projection. |
| SRC1033_1_1032_acquisition | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1032_CG_TAU_ACQUISITION_TEMPLATE.csv | true | true | 1032 tau_R10 acquisition slot. |
| SRC1033_2_1032_readiness | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1032_R10_PPN_READINESS_MAP.csv | true | true | 1032 R10 readiness map. |
| SRC1033_3_1032_refusal | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1032_PLACEHOLDER_REFUSAL_RUNNER.csv | true | true | 1032 placeholder refusal evidence. |
| SRC1033_4_1029_tau | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1029_TAU_PROJECTION_REQUIREMENTS.csv | true | true | 1029 tau projection requirements. |
| SRC1033_5_1030_provenance | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1030_CG_PROVENANCE_GATE_BINDING.csv | true | true | 1030 c_g/tau provenance binding. |
| SRC1033_6_946_interface | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_946_CG_BA_BOUND_INTERFACE.csv | true | true | 946 R10 c_g bound interface. |
| SRC1033_7_947_projection | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_947_PROJECTION_FILL_ATTEMPT.csv | true | true | 947 R10 projection missing row. |
| SRC1033_8_947_update | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_947_BOUND_INTERFACE_UPDATE.csv | true | true | 947 R10 bound interface update. |
| SRC1033_9_631_charge_law | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_631_SOURCE_TEST_CHARGE_LAW.csv | true | true | 631 source/test charge law. |
| SRC1033_10_633_frame | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_633_MATTER_FRAME_CANDIDATE_CLASSIFICATION.csv | true | true | 633 matter-frame candidate classification. |
| SRC1033_11_mts_curve | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\R10_alpha_lambda_curve_MTS_source_normalization.csv | true | true | current MTS R10 prediction placeholder. |
| SRC1033_12_bound_curve | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\R10_alpha_lambda_bound_curve_DIGITIZED.csv | true | true | current R10 bound curve placeholder. |
| SRC1033_13_local_bounds | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\local_bound_claims.csv | true | true | local R10 symbolic bound anchor. |

## tau_R10 derivation audit
| audit_id | target | mathematical_form | result | missing_for_claim | if_missing | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| TAUR1033_0_R10_observable | map MTS finite X response to the R10 Yukawa alpha(lambda) convention | V(r)=-G m_s m_t/r [1 + alpha(lambda) exp(-r/lambda)] | OBSERVABLE_CONVENTION_IDENTIFIED | digitized/source-backed alpha_bound(lambda) curve | no R10 scoring, only schema work | false |
| TAUR1033_1_factorization | factor finite MTS prediction into source, test, Green-kernel, and projection factors | alpha_R10(lambda)=K_X(lambda) Qbar_XH(source,lambda) [tau_R10(test,lambda)c_g + retained tails] | PROJECTION_CONTRACT_WRITTEN | K_X(lambda), Qbar_XH, tau_R10, c_g, source/test profile, tail envelope | finite branch remains unscoreable | false |
| TAUR1033_2_tau_definition | define tau_R10 without inventing a value | tau_R10 := normalized test-leg/material/readout projection that converts c_g into the R10 test charge under the selected Yukawa profile convention | DEFINITION_ONLY | material/readout trace convention, Xhat normalization, finite-source correction, and profile integral | tau_R10 cannot be assumed unity | false |
| TAUR1033_3_KX_definition | separate the propagator/normalization factor from material projection | K_X(lambda) contains static Green-function normalization, X kinetic normalization, 4pi/G conversion, and range/profile factors | DEFINITION_ONLY | parent kinetic normalization, X mass/range relation, and Newtonian comparison convention | K_X cannot be absorbed into tau_R10 without losing units/provenance | false |
| TAUR1033_4_Qbar_source | separate source-leg charge from test-leg tau_R10 | Qbar_XH(source,lambda) := source-normalized Hilbert/trace/source charge entering the Yukawa field solution | DEFINITION_ONLY | same-worldtube Hilbert source, measured-GM calibration, source support, and hidden-current silence | source leg may hide q_nonH or support terms | false |
| TAUR1033_5_universal_cg_limit | check whether universal conformal coupling makes tau_R10=1 | if beta_source=beta_test=c_g in a fully normalized scalar-tensor convention, alpha is proportional to c_g^2, not a free tau_R10=1 claim | UNITY_SHORTCUT_REJECTED | full convention proving beta_source, beta_test, K_X, and Newton normalization | do not set tau_R10=1 by intuition | false |
| TAUR1033_6_verdict | derive or source tau_R10 for current MTS finite branch | tau_R10 is score-ready only with sourced profile/material/projection convention and all companion factors | NOT_DERIVED_CURRENT_CORPUS | tau_R10, K_X(lambda), Qbar_XH, c_g, digitized alpha_bound(lambda), and tail envelope | write acquisition rows and refuse R10 scoring | false |

## R10 profile-normalization contract
| contract_id | required_input | mathematical_form | current_status | needed_source | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| R10PC1033_0_force_law | Yukawa force law convention | alpha(lambda) multiplies exp(-r/lambda) correction to Newtonian potential | SYMBOLIC_ANCHOR_ONLY | digitized/source-backed alpha_bound(lambda) curve | false | false |
| R10PC1033_1_range_relation | lambda_X relation | lambda_X is the static range of the finite X mode in metres under the selected kinetic/mass normalization | MISSING_PARENT_RANGE_NORMALIZATION | parent X kinetic/mass row or sourced finite range | false | false |
| R10PC1033_2_KX | K_X(lambda) | static Green-kernel and Newton-normalized conversion between MTS charges and alpha(lambda) | MISSING_KERNEL_NORMALIZATION | derived propagator normalization and G comparison | false | false |
| R10PC1033_3_Qbar_XH | Qbar_XH | source-normalized Hilbert/source charge for the source body under R10 support convention | MISSING_SOURCE_CHARGE | same-worldtube source measure and measured-GM calibration | false | false |
| R10PC1033_4_tau_R10 | tau_R10 | test-leg/material projection converting c_g into R10 test charge under selected profile convention | MISSING_ARENA_PROJECTION | test-body trace/readout convention and finite-size/material correction | false | false |
| R10PC1033_5_tail_envelope | retained tails | absolute envelope for b_A,b_alpha,b_dis,q_nonH,Delta_W_support and hidden components | ABSOLUTE_ENVELOPE_REQUIRED | theorem-zero or numeric/source-backed rows for every retained component | false | false |
| R10PC1033_6_score_gate | R10 score gate | score only if alpha_predicted(lambda) and alpha_bound(lambda) are numeric, unit-matched, sourced, and valid_for_claim=true | CLAIM_BLOCKED | all R10PC1033_0 through R10PC1033_5 closed | false | false |

## R10 acquisition template
| acquisition_id | quantity | candidate_value | units | source_path | source_row_id | derivation_status | required_columns | ready_for_score | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R10ACQ1033_0_alpha_bound_curve | alpha_bound(lambda) | MISSING_DIGITIZED_ALPHA_BOUND | range-dependent | source-intake/local_bounds/R10_alpha_lambda_bound_curve_DIGITIZED.csv | R10_BOUND_PLACEHOLDER_0 | MISSING_DIGITIZED_BOUND_CURVE | lambda_value;lambda_units;alpha_bound;alpha_bound_source;digitization_method;valid_for_claim | false | false |
| R10ACQ1033_1_KX_lambda | K_X(lambda) | MISSING_KERNEL_NORMALIZATION | model_dependent | MISSING_PARENT_SOURCE | MISSING_SOURCE_ROW_ID | MISSING_GREEN_FUNCTION_DERIVATION | lambda_value;K_X;normalization;kinetic_term;G_conversion;source_path | false | false |
| R10ACQ1033_2_Qbar_XH | Qbar_XH | MISSING_SOURCE_CHARGE | dimensionless_or_declared | MISSING_PARENT_SOURCE | MISSING_SOURCE_ROW_ID | MISSING_SOURCE_NORMALIZATION | source_body;support_rule;Qbar_XH;units;measured_GM_calibration;source_path | false | false |
| R10ACQ1033_3_tau_R10 | tau_R10 | MISSING_ARENA_PROJECTION | dimensionless | MISSING_PROJECTION_SOURCE | MISSING_SOURCE_ROW_ID | MISSING_R10_PROJECTION_DERIVATION | test_body;material;profile;tau_R10;units;trace_convention;source_path | false | false |
| R10ACQ1033_4_cg | c_g | MISSING_PARENT_INPUT | dimensionless | MISSING_PARENT_SOURCE | MISSING_SOURCE_ROW_ID | MISSING_PARENT_CG_OR_ZERO_THEOREM | branch;c_g;units;source_path;derivation_status;claim_policy | false | false |
| R10ACQ1033_5_alpha_predicted | alpha_predicted(lambda) | MISSING_SOURCE_NORMALIZED_ALPHA_PREDICTION | dimensionless | source-intake/mts_residuals/R10_alpha_lambda_curve_MTS_source_normalization.csv | bulk_memory_range_template | MISSING_MTS_PREDICTION | lambda_value;alpha_predicted;K_X;Qbar_XH;tau_R10;c_g;tail_envelope;source_paths | false | false |

## Placeholder refusal runner
| run_id | acquisition_id | quantity | candidate_value | refusal_status | failure_reasons | score_eligible | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R10REF1033_0_alpha_boundlambda | R10ACQ1033_0_alpha_bound_curve | alpha_bound(lambda) | MISSING_DIGITIZED_ALPHA_BOUND | rejected_missing_R10_inputs | MISSING_VALUE;MISSING_DERIVATION_STATUS;NOT_READY_FOR_SCORE;CLAIM_POLICY_FALSE | false | false | false |
| R10REF1033_1_K_Xlambda | R10ACQ1033_1_KX_lambda | K_X(lambda) | MISSING_KERNEL_NORMALIZATION | rejected_missing_R10_inputs | MISSING_VALUE;MISSING_SOURCE_PATH;MISSING_SOURCE_ROW_ID;MISSING_DERIVATION_STATUS;NOT_READY_FOR_SCORE;CLAIM_POLICY_FALSE | false | false | false |
| R10REF1033_2_Qbar_XH | R10ACQ1033_2_Qbar_XH | Qbar_XH | MISSING_SOURCE_CHARGE | rejected_missing_R10_inputs | MISSING_VALUE;MISSING_SOURCE_PATH;MISSING_SOURCE_ROW_ID;MISSING_DERIVATION_STATUS;NOT_READY_FOR_SCORE;CLAIM_POLICY_FALSE | false | false | false |
| R10REF1033_3_tau_R10 | R10ACQ1033_3_tau_R10 | tau_R10 | MISSING_ARENA_PROJECTION | rejected_missing_R10_inputs | MISSING_VALUE;MISSING_SOURCE_PATH;MISSING_SOURCE_ROW_ID;MISSING_DERIVATION_STATUS;NOT_READY_FOR_SCORE;CLAIM_POLICY_FALSE | false | false | false |
| R10REF1033_4_c_g | R10ACQ1033_4_cg | c_g | MISSING_PARENT_INPUT | rejected_missing_R10_inputs | MISSING_VALUE;MISSING_SOURCE_PATH;MISSING_SOURCE_ROW_ID;MISSING_DERIVATION_STATUS;NOT_READY_FOR_SCORE;CLAIM_POLICY_FALSE | false | false | false |
| R10REF1033_5_alpha_predictedlambda | R10ACQ1033_5_alpha_predicted | alpha_predicted(lambda) | MISSING_SOURCE_NORMALIZED_ALPHA_PREDICTION | rejected_missing_R10_inputs | MISSING_VALUE;MISSING_DERIVATION_STATUS;NOT_READY_FOR_SCORE;CLAIM_POLICY_FALSE | false | false | false |

## Claim gates
| gate_id | claim | gate_pass | reason | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| CGATE1033_0_sources | all 1033 cited sources exist | true | validated by source register | false | false |
| CGATE1033_1_tau_derived | tau_R10 is derived or sourced | false | tau_R10 remains MISSING_ARENA_PROJECTION | false | false |
| CGATE1033_2_alpha_bound_curve | R10 alpha(lambda) bound curve is score-ready | false | bound curve file contains placeholder rows, not digitized alpha_bound(lambda) | false | false |
| CGATE1033_3_alpha_prediction | MTS alpha_predicted(lambda) is score-ready | false | K_X, Qbar_XH, tau_R10, c_g, and tail envelope are missing | false | false |
| CGATE1033_4_R10_pass | R10 passes finite c_g branch | false | both bound and prediction rows are unscoreable placeholders | false | false |
| CGATE1033_5_no_cancellation | unknown local terms may cancel | true | absolute no-cancellation envelope remains required | false | false |

## Decision ledger
| decision_id | decision | because | next_action | valid_for_claim |
| --- | --- | --- | --- | --- |
| DEC1033_0_tau_status | tau_R10 is not a free constant and is not derived yet. | it bundles the R10 material/test projection, trace convention, source-test profile, and Xhat normalization. | derive/source tau_R10 as a projection row rather than setting it to unity | false |
| DEC1033_1_factor_status | R10 finite branch needs K_X(lambda), Qbar_XH, tau_R10, c_g, and the tail envelope. | without separating these factors, alpha(lambda) cannot be compared to the external bound curve. | acquire/derive K_X and Qbar_XH alongside tau_R10 | false |
| DEC1033_2_bound_status | R10 bound data is still symbolic/placeholder. | local bound claims name the source but do not provide a digitized alpha_bound(lambda) curve. | digitize/source the R10 alpha(lambda) bound curve before any score | false |
| DEC1033_3_next_target | Next target is R10 bound curve digitization plus projection input pack. | the theory-side tau row and external alpha(lambda) bound are both required before finite-branch scoring. | 1034-Y5-R10-alpha-bound-curve-digitization-and-projection-input-pack.md | false |

## Validation
| check_id | result | detail | generated_utc |
| --- | --- | --- | --- |
| V1033_SUMMARY | pass | 1033 tau_R10 projection derivation/acquisition validation summary | 2026-06-14T06:36:15.686561+00:00 |
| V1033_0_sources_exist | pass | all cited source paths exist and expected needles are present | 2026-06-14T06:36:15.686513+00:00 |
| V1033_1_derivation_rows_complete | pass | derivation audit covers observable, factorization, tau, K_X, Qbar, unity shortcut, and verdict | 2026-06-14T06:36:15.686526+00:00 |
| V1033_2_tau_not_claimed | pass | tau_R10 remains nonclaim | 2026-06-14T06:36:15.686529+00:00 |
| V1033_3_unity_shortcut_rejected | pass | tau_R10=1 shortcut is rejected | 2026-06-14T06:36:15.686532+00:00 |
| V1033_4_profile_contract_complete | pass | profile contract covers force law, range, K_X, Qbar, tau, tails, and score gate | 2026-06-14T06:36:15.686534+00:00 |
| V1033_5_profile_nonclaim | pass | profile contract rows remain nonclaim | 2026-06-14T06:36:15.686537+00:00 |
| V1033_6_acquisition_complete | pass | acquisition rows cover bound curve, K_X, Qbar, tau_R10, c_g, and alpha prediction | 2026-06-14T06:36:15.686539+00:00 |
| V1033_7_acquisition_not_ready | pass | acquisition rows refuse scoring | 2026-06-14T06:36:15.686542+00:00 |
| V1033_8_refusals_complete | pass | refusal runner rejects every placeholder acquisition row | 2026-06-14T06:36:15.686544+00:00 |
| V1033_9_claim_gates_blocked | pass | all claim gates refuse promotion | 2026-06-14T06:36:15.686547+00:00 |
| V1033_10_no_cancellation_guard | pass | no-cancellation guard is active | 2026-06-14T06:36:15.686549+00:00 |
| V1033_11_decision_next | pass | decision ledger selects the 1034 target | 2026-06-14T06:36:15.686551+00:00 |
| V1033_12_next_target_written | pass | 1034 next target row is present | 2026-06-14T06:36:15.686554+00:00 |
| V1033_13_no_overclaim | pass | all generated rows remain valid_for_claim=false | 2026-06-14T06:36:15.686556+00:00 |
| V1033_14_formalization_untouched | pass | formalization-workbench modified-file count since script start is 0 | 2026-06-14T06:36:15.686558+00:00 |

## Next target
| next_target | objective | include | exclude | valid_for_claim |
| --- | --- | --- | --- | --- |
| 1034-Y5-R10-alpha-bound-curve-digitization-and-projection-input-pack.md | obtain/source a real R10 alpha_bound(lambda) curve and build a projection input pack for K_X(lambda), Qbar_XH, tau_R10, c_g, and retained tails without scoring placeholders | R10 alpha_bound(lambda), digitization provenance, lambda units, K_X(lambda), Qbar_XH, tau_R10, c_g provenance, source/test profile convention, no-cancellation envelope | R10 pass claim, invented bound rows, invented tau/c_g/K_X values, unity tau shortcut, PPN/local-GR claim, GitHub action, formalization-workbench edits | false |

