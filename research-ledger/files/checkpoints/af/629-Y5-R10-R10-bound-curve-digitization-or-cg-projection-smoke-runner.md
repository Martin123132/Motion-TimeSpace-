# 629 Y5 R10 bound curve digitization or cg projection smoke runner

Status: `Y5_R10_review_curve_and_cg_projection_smoke_runner_built_claim_still_blocked`  
Claim ceiling: `nonclaim_smoke_only_no_cg_zero_no_R10_WEP_PPN_clock_or_local_GR_pass`  
Next target: `630-Y5-R10-cg-projection-parent-input-derivation-or-source-prior-envelope.md`

## Verdict
- 629 did not promote the R10 bound curve and did not claim a local pass.
- It built the missing bridge between the review-candidate Eot-Wash curve and the `c_g` projection contract.
- The smoke runner correctly blocks all MTS rows because `c_g`, `tau_R10`, `K_X`, `Qbar_XH`, `qbar_XT`, `Z_eff`, and curve-promotion provenance are still not sourced.

## Source Register
| source_id | source_path | exists | role | valid_for_claim |
| --- | --- | --- | --- | --- |
| SRC629_0 | 628-Y5-R10-real-local-bound-input-sources-for-cg-or-Zcg-proof.md | true | immediate 628 source-acquisition checkpoint | false |
| SRC629_1 | source-intake/mts_residuals/P8_Y5_BRR545_628_VALIDATION.csv | true | 628 validation gate | false |
| SRC629_2 | source-intake/mts_residuals/P8_Y5_R10_628_EXTERNAL_SOURCE_CANDIDATES.csv | true | external local-bound source candidates | false |
| SRC629_3 | source-intake/mts_residuals/P8_Y5_R10_628_NONCLAIM_NUMERIC_ANCHORS.csv | true | nonclaim numeric anchors | false |
| SRC629_4 | 570-Y5-R10-review-candidate-bound-curve-runner-and-MTS-coefficient-pressure.md | true | review-candidate R10 pressure wall | false |
| SRC629_5 | source-intake/mts_residuals/P8_Y5_BRR545_570_VALIDATION.csv | true | 570 validation gate | false |
| SRC629_6 | source-intake/local_bounds/P8_Y5_R10_570_REVIEW_CANDIDATE_QA.csv | true | review-candidate curve QA | false |
| SRC629_7 | source-intake/local_bounds/P8_Y5_R10_569_PROMOTION_GATE.csv | true | promotion blocker gate | false |
| SRC629_8 | source-intake/local_bounds/R10_alpha_lambda_bound_curve_VECTOR_2020_REVIEW_CANDIDATE.csv | true | axis-calibrated review-candidate R10 curve | false |
| SRC629_9 | source-intake/local_bounds/R10_alpha_lambda_bound_curve_DIGITIZED.csv | true | live claim curve that must remain placeholder | false |
| SRC629_10 | scripts/Y5_R10_R10_bound_curve_digitization_or_cg_projection_smoke_runner.py | true | this checkpoint generator | false |

## Source Search Status
| search_id | target | status | evidence | source_path_or_url | consequence | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| SS629_0_primary_paper | R10_alpha_bound_lambda | primary_source_located | Eot-Wash 2020 PRL/arXiv gives alpha=1 threshold and figure source for bound curve | https://arxiv.org/abs/2002.11761; https://doi.org/10.1103/PhysRevLett.124.101101 | source usable for anchor and review-candidate curve, not alone a machine-ready claim curve | false |
| SS629_1_machine_table | full_alpha_lambda_machine_table | not_found_in_checkpoint | no source-backed supplemental table was promoted; existing vector extraction remains review-candidate | source-intake/local_bounds/R10_alpha_lambda_bound_curve_VECTOR_2020_REVIEW_CANDIDATE.csv | do not overwrite live digitized bound file | false |
| SS629_2_review_candidate | axis_calibrated_vector_curve | available_as_private_pressure_wall | numeric review rows=390; all rows valid_for_claim=false | source-intake/local_bounds/R10_alpha_lambda_bound_curve_VECTOR_2020_REVIEW_CANDIDATE.csv | may compute private coefficient pressure samples only | false |
| SS629_3_cg_projection | c_g_tau_R10_projection | not_sourced | 628 c_g/tau_R10 rows remain MISSING_PARENT_INPUT or MISSING_ARENA_PROJECTION | 628-Y5-R10-real-local-bound-input-sources-for-cg-or-Zcg-proof.md | R10 runner must block any MTS claim row | false |

## R10 Curve Promotion Audit
| audit_id | check | result | detail | valid_for_claim |
| --- | --- | --- | --- | --- |
| PA629_0_candidate_numeric | review candidate has positive numeric lambda/alpha rows | pass | numeric_rows=390 | false |
| PA629_1_candidate_nonclaim | review candidate has no claim rows | pass | claim_rows=0 | false |
| PA629_2_anchor_qa | 570 anchor QA remains review-only | pass | QA570_0_prior_validation=pass;QA570_1_anchor_recovery=pass_review_candidate;QA570_2_promotion_gate=pass;QA570_3_candidate_nonclaim=pass;QA570_4_live_placeholder_retained=pass | false |
| PA629_3_promotion_blocker | supplement/human QA and live-file promotion remain blocked | pass | blocked_rows=2 | false |
| PA629_4_live_claim_file | live digitized bound file remains placeholder | pass | live_rows=2;contains_missing_marker=true | false |

## Review-Candidate Pressure Samples
| sample_id | lambda_value | lambda_units | alpha_bound_review_candidate | interpolation_method | pressure_class | future_pass_condition | max_abs_effective_product | promotion_status | valid_for_claim | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PS629_0 | 5.9e-06 | m | 897932.29287 | nearest_review_point:R10_VECTOR_2020_REVIEW_0000;lambda_relative_error=0.00094591 | weak_pressure_alpha_bound_above_100 | abs(alpha_MTS_R10(lambda))<=alpha_bound(lambda) | 897932.29287 | review_candidate_private_pressure_only | false | Nonclaim sample from review-candidate vector curve; do not treat as live R10 evidence. |
| PS629_1 | 1e-05 | m | 41538.8057283 | nearest_review_point:R10_VECTOR_2020_REVIEW_0041;lambda_relative_error=3.04994e-06 | weak_pressure_alpha_bound_above_100 | abs(alpha_MTS_R10(lambda))<=alpha_bound(lambda) | 41538.8057283 | review_candidate_private_pressure_only | false | Nonclaim sample from review-candidate vector curve; do not treat as live R10 evidence. |
| PS629_2 | 2e-05 | m | 183.665577985 | nearest_review_point:R10_VECTOR_2020_REVIEW_0105;lambda_relative_error=0.000140624 | weak_pressure_alpha_bound_above_100 | abs(alpha_MTS_R10(lambda))<=alpha_bound(lambda) | 183.665577985 | review_candidate_private_pressure_only | false | Nonclaim sample from review-candidate vector curve; do not treat as live R10 evidence. |
| PS629_3 | 3.86e-05 | m | 0.991537244704 | nearest_review_point:R10_VECTOR_2020_REVIEW_0154;lambda_relative_error=0.00163645 | strong_pressure_alpha_bound_0p1_to_1 | abs(alpha_MTS_R10(lambda))<=alpha_bound(lambda) | 0.991537244704 | review_candidate_private_pressure_only | false | Nonclaim sample from review-candidate vector curve; do not treat as live R10 evidence. |
| PS629_4 | 5.6e-05 | m | 0.300428094431 | nearest_review_point:R10_VECTOR_2020_REVIEW_0178;lambda_relative_error=9.99526e-05 | strong_pressure_alpha_bound_0p1_to_1 | abs(alpha_MTS_R10(lambda))<=alpha_bound(lambda) | 0.300428094431 | review_candidate_private_pressure_only | false | Nonclaim sample from review-candidate vector curve; do not treat as live R10 evidence. |
| PS629_5 | 0.0001 | m | 17.5879273456 | nearest_review_point:R10_VECTOR_2020_REVIEW_0212;lambda_relative_error=6.09983e-06 | moderate_pressure_alpha_bound_1_to_100 | abs(alpha_MTS_R10(lambda))<=alpha_bound(lambda) | 17.5879273456 | review_candidate_private_pressure_only | false | Nonclaim sample from review-candidate vector curve; do not treat as live R10 evidence. |
| PS629_6 | 0.0003 | m | 0.215104553289 | nearest_review_point:R10_VECTOR_2020_REVIEW_0301;lambda_relative_error=0.00263296 | strong_pressure_alpha_bound_0p1_to_1 | abs(alpha_MTS_R10(lambda))<=alpha_bound(lambda) | 0.215104553289 | review_candidate_private_pressure_only | false | Nonclaim sample from review-candidate vector curve; do not treat as live R10 evidence. |
| PS629_7 | 0.000608 | m | 0.00234466430052 | nearest_review_point:R10_VECTOR_2020_REVIEW_0351;lambda_relative_error=0.00012882 | knife_edge_pressure_alpha_bound_below_0p01 | abs(alpha_MTS_R10(lambda))<=alpha_bound(lambda) | 0.00234466430052 | review_candidate_private_pressure_only | false | Nonclaim sample from review-candidate vector curve; do not treat as live R10 evidence. |
| PS629_8 | 0.001 | m | 0.00998933369038 | nearest_review_point:R10_VECTOR_2020_REVIEW_0384;lambda_relative_error=3.04992e-06 | knife_edge_pressure_alpha_bound_below_0p01 | abs(alpha_MTS_R10(lambda))<=alpha_bound(lambda) | 0.00998933369038 | review_candidate_private_pressure_only | false | Nonclaim sample from review-candidate vector curve; do not treat as live R10 evidence. |

## c_g Projection Contract
| contract_id | object | required_value | status | formula_or_condition | source_requirement | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| CG629_0_effective_alpha | alpha_MTS_R10(lambda) | numeric_or_theorem_zero | blocked_symbolic | alpha_MTS_R10(lambda)=abs(c_g*tau_R10(lambda)*K_X*Qbar_XH(lambda;lambda_X)*qbar_XT/Z_eff) | parent action must define c_g, Z_eff, source/test charges, and R10 projection map | false |
| CG629_1_zero_route | Z_cg or c_g | Z_cg=true with c_g=0, or sourced numeric c_g | not_signed | if c_g=0 by parent geometry, alpha_MTS_R10(lambda)=0 for all lambda | quotient-invariant matter action plus no representative Weyl/disformal residue | false |
| CG629_2_projection | tau_R10(lambda) | dimensionless apparatus projection | missing_arena_projection | tau_R10 must map parent local mode into Yukawa-alpha observable for the Eot-Wash source/detector geometry | derive from local profile, material coupling, and experimental source geometry | false |
| CG629_3_range | lambda_X | positive numeric meters or no-range theorem | missing_parent_hessian | lambda_X=sqrt(Z_X/M_X^2) | parent Hessian/eigenvalue block for the local residual mode | false |
| CG629_4_profile | Qbar_XH(lambda;lambda_X) | source/profile response | missing_profile_map | Qbar_XH must be evaluated on the R10 source geometry and local transition profile | derive from local compact-shell/profile solution or demote to explicit empirical closure | false |
| CG629_5_claim_gate | R10 pass | all valid physical rows satisfy bound | blocked | abs(alpha_MTS_R10(lambda_i))<=alpha_bound(lambda_i) for all source-backed curve rows | valid physical MTS alpha rows plus promoted source-backed bound curve | false |

## Runner Block Report
| report_id | item | status | detail | valid_for_claim |
| --- | --- | --- | --- | --- |
| RB629_0_runner_status | R10_alpha_lambda_bound_prediction_runner | blocked_as_expected | {"R10_pass_for_claim": false, "blocked_or_failed_rows": 1, "bound_curve": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_VECTOR_2020_REVIEW_CANDIDATE.csv", "bound_rows": 390, "claim_allowed": false, "comparison_rows": 1, "generated_at_utc": "2026-06-06T11:48:52.128690+00:00", "mts_curve": "source-intake/mts_residuals/R10_alpha_lambda_curve_MTS_CG_PROJECTION_SMOKE_NONCLAIM.csv", "mts_rows": 9, "output_dir": "runs/20260606-032900-Y5-R10-629-cg-projection-smoke-runner/results", "passed_rows": 0, "valid_bound_rows": 0, "valid_mts_rows": 0} | false |
| RB629_1_MTS_validation | MTS cg smoke rows | invalid_as_expected | {"alpha_predicted_not_numeric": 9, "valid_for_claim_not_true": 9} | false |
| RB629_2_bound_validation | review candidate bound rows | invalid_for_claim_as_expected | {"valid_for_claim_not_true": 390} | false |
| RB629_3_comparison | comparison rows | no_claim_comparison | comparison_rows=1;passed_rows=0;blocked_or_failed_rows=1 | false |

## Nonclaim Summary
| status | claim_ceiling | review_curve_rows | pressure_sample_rows | tightest_sample_alpha_bound | tightest_sample_lambda_m | runner_claim_allowed | cg_projection_ready | r10_curve_promoted | next_target | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Y5_R10_review_curve_and_cg_projection_smoke_runner_built_claim_still_blocked | nonclaim_smoke_only_no_cg_zero_no_R10_WEP_PPN_clock_or_local_GR_pass | 390 | 9 | 0.00234466430052 | 0.000608 | false | false | false | 630-Y5-R10-cg-projection-parent-input-derivation-or-source-prior-envelope.md | false |

## Decision
| decision_id | decision | meaning | status | next_target | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| D629_0_smoke_runner_built | Y5_R10_review_curve_and_cg_projection_smoke_runner_built_claim_still_blocked | R10 review curve can now be sampled against a formal c_g projection contract | diagnostic_progress | 630-Y5-R10-cg-projection-parent-input-derivation-or-source-prior-envelope.md | false |
| D629_1_no_curve_promotion | do_not_promote_review_curve_to_live_claim_file | supplemental table or human visual QA signoff is still missing | blocked_for_claim | supplement_or_manual_QA_only_if_public_R10_claim_needed | false |
| D629_2_projection_gap | derive_or_bound_c_g_tau_R10_next | data side is good enough for pressure; theory side still lacks physical alpha rows | next_required | 630-Y5-R10-cg-projection-parent-input-derivation-or-source-prior-envelope.md | false |
| D629_3_claim_ceiling | nonclaim_smoke_only_no_cg_zero_no_R10_WEP_PPN_clock_or_local_GR_pass | no R10, local-GR, WEP, PPN, clock, or orbital pass follows from this checkpoint | hard_guardrail | 630-Y5-R10-cg-projection-parent-input-derivation-or-source-prior-envelope.md | false |

## Route Update
| route_id | allowed_after_629 | forbidden_after_629 | next_action |
| --- | --- | --- | --- |
| RU629_0_allowed | Use review-candidate pressure samples as private coefficient targets. | Claim R10/local-GR pass from review curve or symbolic c_g rows. | 630-Y5-R10-cg-projection-parent-input-derivation-or-source-prior-envelope.md |
| RU629_1_allowed | Try to derive c_g=0 or a sourced c_g*tau_R10 projection. | Fit c_g post hoc without a parent coefficient/projection contract. | 630-Y5-R10-cg-projection-parent-input-derivation-or-source-prior-envelope.md |
| RU629_2_data_route | Promote the Eot-Wash curve only after supplement/manual QA signoff. | Overwrite R10_alpha_lambda_bound_curve_DIGITIZED.csv with review-candidate rows. | curve promotion remains separate provenance work |

## Validation
| check_id | result | detail |
| --- | --- | --- |
| V629_0_source_paths_exist | pass | missing=0 |
| V629_1_prior_628_clean | pass | prior_rows=8;prior_fails=0 |
| V629_2_review_curve_private_only | pass | numeric_rows=390;claim_rows=0 |
| V629_3_anchor_sample_recovers_alpha1 | pass | lambda=3.86e-5m;nearest_candidate_alpha=0.9915372447041295;relative_lambda_error=0.0016364485914564457 |
| V629_4_promotion_remains_blocked | pass | PA629_0_candidate_numeric=pass;PA629_1_candidate_nonclaim=pass;PA629_2_anchor_qa=pass;PA629_3_promotion_blocker=pass;PA629_4_live_claim_file=pass |
| V629_5_contract_blocks_claim | pass | contract_rows=6;claim_rows=0 |
| V629_6_smoke_runner_blocks_claim | pass | smoke_rows=9;valid_mts=0;valid_bound=0;claim_allowed=False |
| V629_7_live_claim_file_not_modified_into_claim | pass | live_rows=2;contains_missing=true;claim_rows=0 |
| V629_8_no_local_claim | pass | Z_cg=false;c_g=false;R10=false;WEP=false;PPN=false;clock=false;orbital=false;local_GR=false |
