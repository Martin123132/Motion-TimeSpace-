# 611 Y5 R10 real-bound-curve QA or C_X component-prior runner

Generated: 2026-06-05T21:26:26.112738+00:00  
Status: `Y5_R10_review_curve_QA_and_CX_prior_runner_built_nonclaim_real_claim_still_blocked`  
Claim ceiling: `review_candidate_curve_and_CX_prior_pressure_only_no_R10_fifth_force_WEP_PPN_or_local_GR_pass`  
Next target: `612-Y5-R10-CX-component-source-derivation-or-real-bound-curve-promotion.md`  
Run root: `runs/20260605-212626-Y5-R10-real-bound-curve-QA-or-CX-component-prior-runner`

## Verdict
- The existing vector-extracted 2020 R10 curve passes internal review-candidate QA, including source/render assets and alpha=1 anchor recovery.
- It remains non-claim. It is useful pressure data, not a promoted bound curve.
- A finite `p=1` `C_X` prior runner is now wired: `alpha_X=epsilon_shell*C_X`.
- The next real wall is either promote/acquire a claim-grade bound curve or derive numeric/source-backed `C_X` components.

## Source Register
| source_file | exists | role |
| --- | --- | --- |
| 610-Y5-R10-finite-p1-branch-coefficient-envelope-or-marker-exclusion-repair.md | True | immediate 610 handoff |
| source-intake/mts_residuals/P8_Y5_BRR545_610_VALIDATION.csv | True | prior validation gate |
| source-intake/mts_residuals/P8_Y5_R10_610_FINITE_P1_COEFFICIENT_ENVELOPE.csv | True | finite p1 law |
| source-intake/mts_residuals/P8_Y5_R10_610_ALPHA_PRESSURE_ENVELOPE.csv | True | anchor-only pressure grid |
| source-intake/mts_residuals/P8_Y5_R10_610_COMPONENT_BUDGET_SCENARIOS.csv | True | component budget seed |
| source-intake/local_bounds/R10_alpha_lambda_bound_curve_VECTOR_2020_REVIEW_CANDIDATE.csv | True | review candidate curve |
| source-intake/local_bounds/P8_Y5_R10_570_REVIEW_CANDIDATE_QA.csv | True | prior candidate QA |
| source-intake/local_bounds/P8_Y5_R10_570_REVIEW_CURVE_SUMMARY.csv | True | prior candidate curve summary |
| source-intake/local_bounds/R10_alpha_lambda_bound_curve_ANCHOR_SMOKE.csv | True | anchor-only nonclaim rows |
| source-intake/local_bounds/R10_alpha_lambda_bound_curve_DIGITIZED.csv | True | live claim placeholder kept unchanged |
| source-intake/mts_residuals/R10_alpha_lambda_curve_MTS_source_normalization.csv | True | live MTS placeholder kept unchanged |
| 578-Y5-R10-lambda-X-mass-gap-and-product-coefficient-derivation-targets.md | True | lambda target lineage |
| 579-Y5-R10-parent-Hessian-source-charge-fill-or-theorem-zero-return.md | True | C_X source/test factorization |
| scripts/R10_alpha_lambda_bound_prediction_runner.py | True | existing comparator reused unchanged |
| scripts/Y5_R10_real_bound_curve_QA_or_CX_component_prior_runner.py | True | this checkpoint generator |

## Bound Curve QA
| qa_id | check | result | detail | valid_for_claim |
| --- | --- | --- | --- | --- |
| QA611_0_schema_rows | review candidate file has parseable rows | pass | raw_rows=390;numeric_points=390 | false |
| QA611_1_positive_numeric | lambda and alpha are positive numeric | pass | positive_numeric=True | false |
| QA611_2_lambda_order | lambda values can be sorted into a monotonic curve | pass | lambda_min=5.894419132271889e-06;lambda_max=0.0010099153351819316 | false |
| QA611_3_no_missing_markers | review rows contain no MISSING markers | pass | missing_marker_rows=0 | false |
| QA611_4_source_assets_exist | local figure source and render assets exist | pass | source_missing=0;render_missing=0 | false |
| QA611_5_anchor_recovery | nearest review point recovers alpha~1 at 38.6um | pass_review_candidate | nearest_bound_id=R10_VECTOR_2020_REVIEW_0154;lambda=3.866316691563e-05;alpha=9.915372447041e-01;lambda_rel_error=1.636448591456e-03;alpha_log10_error=3.690967927978e-03;prior_570=True | false |
| QA611_6_nonclaim_guard | review candidate remains nonclaim | pass | claim_rows=0 | false |

## Review Curve Stats
| stat_id | metric | value | units | valid_for_claim | notes |
| --- | --- | --- | --- | --- | --- |
| CS611_0_rows | review_candidate_rows | 390 | rows | false | review-candidate curve only; not live claim curve |
| CS611_1_lambda_range | lambda_min_to_max | 5.89441913227189e-06..0.00100991533518193 | m | false | source rows R10_VECTOR_2020_REVIEW_0000 to R10_VECTOR_2020_REVIEW_0389 |
| CS611_2_alpha_range | alpha_bound_min_to_max | 0.00234466430051938..897932.292870452 | dimensionless | false | min at lambda=0.000608078322298804; max at lambda=5.89441913227189e-06 |
| CS611_3_tightest_candidate_bound | tightest_candidate_bound | 0.00234466430051938 | dimensionless | false | lambda=0.000608078322298804; diagnostic only |

## C_X Prior Grid
| grid_id | abs_CX_trial | epsilon_shell | alpha_predicted_p1 | review_candidate_points | passing_points | passing_fraction | allowed_lambda_intervals_m_review_candidate | number_of_intervals | claim_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CX611_C0.001 | 1.000000000000e-03 | 7.432631961577e-06 | 7.432631961577e-09 | 390 | 390 | 1.000000000000e+00 | 5.894419e-06..1.009915e-03 | 1 | review_candidate_nonclaim_pressure | false |
| CX611_C0.01 | 1.000000000000e-02 | 7.432631961577e-06 | 7.432631961577e-08 | 390 | 390 | 1.000000000000e+00 | 5.894419e-06..1.009915e-03 | 1 | review_candidate_nonclaim_pressure | false |
| CX611_C0.1 | 1.000000000000e-01 | 7.432631961577e-06 | 7.432631961577e-07 | 390 | 390 | 1.000000000000e+00 | 5.894419e-06..1.009915e-03 | 1 | review_candidate_nonclaim_pressure | false |
| CX611_C1 | 1.000000000000e+00 | 7.432631961577e-06 | 7.432631961577e-06 | 390 | 390 | 1.000000000000e+00 | 5.894419e-06..1.009915e-03 | 1 | review_candidate_nonclaim_pressure | false |
| CX611_C10 | 1.000000000000e+01 | 7.432631961577e-06 | 7.432631961577e-05 | 390 | 390 | 1.000000000000e+00 | 5.894419e-06..1.009915e-03 | 1 | review_candidate_nonclaim_pressure | false |
| CX611_C100 | 1.000000000000e+02 | 7.432631961577e-06 | 7.432631961577e-04 | 390 | 390 | 1.000000000000e+00 | 5.894419e-06..1.009915e-03 | 1 | review_candidate_nonclaim_pressure | false |
| CX611_C1000 | 1.000000000000e+03 | 7.432631961577e-06 | 7.432631961577e-03 | 390 | 360 | 9.230769230769e-01 | 5.894419e-06..2.595893e-04;2.690493e-04..2.696062e-04;2.792881e-04..2.800097e-04;2.897628e-04..2.927850e-04;3.007899e-04..3.059807e-04;3.122366e-04..3.242851e-04;3.347095e-04..3.367985e-04;3.499804e-04..3.499804e-04;...(+23 more) | 31 | review_candidate_nonclaim_pressure | false |
| CX611_C10000 | 1.000000000000e+04 | 7.432631961577e-06 | 7.432631961577e-02 | 390 | 258 | 6.615384615385e-01 | 5.894419e-06..1.031611e-04;1.037518e-04..1.064227e-04;1.076449e-04..1.098438e-04;1.116821e-04..1.133748e-04;1.170814e-04..1.170814e-04;1.209070e-04..1.209070e-04;1.249239e-04..1.249239e-04;1.290742e-04..1.290742e-04;...(+31 more) | 39 | review_candidate_nonclaim_pressure | false |
| CX611_C100000 | 1.000000000000e+05 | 7.432631961577e-06 | 7.432631961577e-01 | 390 | 195 | 5.000000000000e-01 | 5.894419e-06..4.240255e-05;4.367521e-05..4.367521e-05;4.498606e-05..4.498606e-05;4.619149e-05..4.619149e-05;4.740492e-05..4.740492e-05;4.867605e-05..5.000688e-05;5.158795e-05..5.158795e-05;5.327455e-05..5.327455e-05;...(+26 more) | 34 | review_candidate_nonclaim_pressure | false |
| CX611_C134542 | 1.345418426702e+05 | 7.432631961577e-06 | 1.000000000000e+00 | 390 | 188 | 4.820512820513e-01 | 5.894419e-06..3.788852e-05;3.892441e-05..3.998863e-05;4.118883e-05..4.240255e-05;4.367521e-05..4.367521e-05;4.498606e-05..4.498606e-05;4.619149e-05..4.619149e-05;4.740492e-05..4.740492e-05;4.867605e-05..5.000688e-05;...(+24 more) | 32 | review_candidate_nonclaim_pressure | false |
| CX611_C1e06 | 1.000000000000e+06 | 7.432631961577e-06 | 7.432631961577e+00 | 390 | 142 | 3.641025641026e-01 | 5.894419e-06..2.375537e-05;2.436692e-05..2.499422e-05;2.563767e-05..2.563767e-05;2.631116e-05..2.631116e-05;2.698851e-05..2.698851e-05;2.771219e-05..2.771219e-05;2.844018e-05..2.844018e-05;2.920225e-05..2.920225e-05;...(+11 more) | 19 | review_candidate_nonclaim_pressure | false |

## C_X Component Prior Runner
| scenario_id | Qbar_XH_trial | qbar_XT_trial | source_test_product | tightest_review_alpha_bound | max_abs_normalization_factor_review_candidate | formula | claim_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CPR611_unit_source_unit_test | 1.000000000000e+00 | 1.000000000000e+00 | 1.000000000000e+00 | 2.344664300519e-03 | 3.154554554349e+02 | abs(kappa_norm)*Qbar_XH*qbar_XT*epsilon_shell <= min(alpha_bound_review) | review_candidate_nonclaim_pressure | false |
| CPR611_weak_test_1e_minus_2 | 1.000000000000e+00 | 1.000000000000e-02 | 1.000000000000e-02 | 2.344664300519e-03 | 3.154554554349e+04 | abs(kappa_norm)*Qbar_XH*qbar_XT*epsilon_shell <= min(alpha_bound_review) | review_candidate_nonclaim_pressure | false |
| CPR611_weak_source_1e_minus_2 | 1.000000000000e-02 | 1.000000000000e+00 | 1.000000000000e-02 | 2.344664300519e-03 | 3.154554554349e+04 | abs(kappa_norm)*Qbar_XH*qbar_XT*epsilon_shell <= min(alpha_bound_review) | review_candidate_nonclaim_pressure | false |
| CPR611_both_1e_minus_2 | 1.000000000000e-02 | 1.000000000000e-02 | 1.000000000000e-04 | 2.344664300519e-03 | 3.154554554349e+06 | abs(kappa_norm)*Qbar_XH*qbar_XT*epsilon_shell <= min(alpha_bound_review) | review_candidate_nonclaim_pressure | false |
| CPR611_both_1e_minus_3 | 1.000000000000e-03 | 1.000000000000e-03 | 1.000000000000e-06 | 2.344664300519e-03 | 3.154554554349e+08 | abs(kappa_norm)*Qbar_XH*qbar_XT*epsilon_shell <= min(alpha_bound_review) | review_candidate_nonclaim_pressure | false |
| CPR611_source_screened_1e_minus_4_test_unit | 1.000000000000e-04 | 1.000000000000e+00 | 1.000000000000e-04 | 2.344664300519e-03 | 3.154554554349e+06 | abs(kappa_norm)*Qbar_XH*qbar_XT*epsilon_shell <= min(alpha_bound_review) | review_candidate_nonclaim_pressure | false |
| CPR611_test_screened_1e_minus_4_source_unit | 1.000000000000e+00 | 1.000000000000e-04 | 1.000000000000e-04 | 2.344664300519e-03 | 3.154554554349e+06 | abs(kappa_norm)*Qbar_XH*qbar_XT*epsilon_shell <= min(alpha_bound_review) | review_candidate_nonclaim_pressure | false |

## Allowed Lambda Windows
| window_id | abs_CX_trial | alpha_predicted_p1 | passing_fraction | number_of_intervals | allowed_lambda_intervals_m_review_candidate | claim_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| LW611_C0.001 | 1.000000000000e-03 | 7.432631961577e-09 | 1.000000000000e+00 | 1 | 5.894419e-06..1.009915e-03 | review_candidate_nonclaim_pressure | false |
| LW611_C0.01 | 1.000000000000e-02 | 7.432631961577e-08 | 1.000000000000e+00 | 1 | 5.894419e-06..1.009915e-03 | review_candidate_nonclaim_pressure | false |
| LW611_C0.1 | 1.000000000000e-01 | 7.432631961577e-07 | 1.000000000000e+00 | 1 | 5.894419e-06..1.009915e-03 | review_candidate_nonclaim_pressure | false |
| LW611_C1 | 1.000000000000e+00 | 7.432631961577e-06 | 1.000000000000e+00 | 1 | 5.894419e-06..1.009915e-03 | review_candidate_nonclaim_pressure | false |
| LW611_C10 | 1.000000000000e+01 | 7.432631961577e-05 | 1.000000000000e+00 | 1 | 5.894419e-06..1.009915e-03 | review_candidate_nonclaim_pressure | false |
| LW611_C100 | 1.000000000000e+02 | 7.432631961577e-04 | 1.000000000000e+00 | 1 | 5.894419e-06..1.009915e-03 | review_candidate_nonclaim_pressure | false |
| LW611_C1000 | 1.000000000000e+03 | 7.432631961577e-03 | 9.230769230769e-01 | 31 | 5.894419e-06..2.595893e-04;2.690493e-04..2.696062e-04;2.792881e-04..2.800097e-04;2.897628e-04..2.927850e-04;3.007899e-04..3.059807e-04;3.122366e-04..3.242851e-04;3.347095e-04..3.367985e-04;3.499804e-04..3.499804e-04;...(+23 more) | review_candidate_nonclaim_pressure | false |
| LW611_C10000 | 1.000000000000e+04 | 7.432631961577e-02 | 6.615384615385e-01 | 39 | 5.894419e-06..1.031611e-04;1.037518e-04..1.064227e-04;1.076449e-04..1.098438e-04;1.116821e-04..1.133748e-04;1.170814e-04..1.170814e-04;1.209070e-04..1.209070e-04;1.249239e-04..1.249239e-04;1.290742e-04..1.290742e-04;...(+31 more) | review_candidate_nonclaim_pressure | false |
| LW611_C100000 | 1.000000000000e+05 | 7.432631961577e-01 | 5.000000000000e-01 | 34 | 5.894419e-06..4.240255e-05;4.367521e-05..4.367521e-05;4.498606e-05..4.498606e-05;4.619149e-05..4.619149e-05;4.740492e-05..4.740492e-05;4.867605e-05..5.000688e-05;5.158795e-05..5.158795e-05;5.327455e-05..5.327455e-05;...(+26 more) | review_candidate_nonclaim_pressure | false |
| LW611_C134542 | 1.345418426702e+05 | 1.000000000000e+00 | 4.820512820513e-01 | 32 | 5.894419e-06..3.788852e-05;3.892441e-05..3.998863e-05;4.118883e-05..4.240255e-05;4.367521e-05..4.367521e-05;4.498606e-05..4.498606e-05;4.619149e-05..4.619149e-05;4.740492e-05..4.740492e-05;4.867605e-05..5.000688e-05;...(+24 more) | review_candidate_nonclaim_pressure | false |
| LW611_C1e06 | 1.000000000000e+06 | 7.432631961577e+00 | 3.641025641026e-01 | 19 | 5.894419e-06..2.375537e-05;2.436692e-05..2.499422e-05;2.563767e-05..2.563767e-05;2.631116e-05..2.631116e-05;2.698851e-05..2.698851e-05;2.771219e-05..2.771219e-05;2.844018e-05..2.844018e-05;2.920225e-05..2.920225e-05;...(+11 more) | review_candidate_nonclaim_pressure | false |

## MTS Numeric Prior Template
| model_id | branch_id | curve_id | lambda_value | lambda_units | alpha_predicted | alpha_bound | alpha_bound_source | force_law_form | derivation_status | formula_reference | source_file | assumptions | valid_for_claim | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_finite_p1_prior_nonclaim | R10_finite_p1_CX_1.000000000000e+00 | R10_alpha_lambda_curve_MTS_FINITE_P1_NUMERIC_PRIOR_NONCLAIM | 3.86e-5 | m | 7.432631961577e-06 | 1.0 | source-intake/local_bounds/R10_alpha_lambda_bound_curve_ANCHOR_SMOKE.csv::R10_ANCHOR_EOTWASH_2020_ALPHA1_38P6UM | Yukawa_potential_alpha | numeric_prior_nonclaim_not_parent_sourced | 611-Y5-R10-real-bound-curve-QA-or-CX-component-prior-runner.md::CX611 | 611-Y5-R10-real-bound-curve-QA-or-CX-component-prior-runner.md | C_X_trial_grid_not_parent_sourced;anchor_bound_only;valid_for_claim_false | false | Diagnostic numeric prior only; runner must reject because rows are not parent-sourced claim rows. |
| MTS_finite_p1_prior_nonclaim | R10_finite_p1_CX_1.000000000000e+03 | R10_alpha_lambda_curve_MTS_FINITE_P1_NUMERIC_PRIOR_NONCLAIM | 3.86e-5 | m | 7.432631961577e-03 | 1.0 | source-intake/local_bounds/R10_alpha_lambda_bound_curve_ANCHOR_SMOKE.csv::R10_ANCHOR_EOTWASH_2020_ALPHA1_38P6UM | Yukawa_potential_alpha | numeric_prior_nonclaim_not_parent_sourced | 611-Y5-R10-real-bound-curve-QA-or-CX-component-prior-runner.md::CX611 | 611-Y5-R10-real-bound-curve-QA-or-CX-component-prior-runner.md | C_X_trial_grid_not_parent_sourced;anchor_bound_only;valid_for_claim_false | false | Diagnostic numeric prior only; runner must reject because rows are not parent-sourced claim rows. |
| MTS_finite_p1_prior_nonclaim | R10_finite_p1_CX_1.000000000000e+05 | R10_alpha_lambda_curve_MTS_FINITE_P1_NUMERIC_PRIOR_NONCLAIM | 3.86e-5 | m | 7.432631961577e-01 | 1.0 | source-intake/local_bounds/R10_alpha_lambda_bound_curve_ANCHOR_SMOKE.csv::R10_ANCHOR_EOTWASH_2020_ALPHA1_38P6UM | Yukawa_potential_alpha | numeric_prior_nonclaim_not_parent_sourced | 611-Y5-R10-real-bound-curve-QA-or-CX-component-prior-runner.md::CX611 | 611-Y5-R10-real-bound-curve-QA-or-CX-component-prior-runner.md | C_X_trial_grid_not_parent_sourced;anchor_bound_only;valid_for_claim_false | false | Diagnostic numeric prior only; runner must reject because rows are not parent-sourced claim rows. |
| MTS_finite_p1_prior_nonclaim | R10_finite_p1_CX_1.000000000000e+00 | R10_alpha_lambda_curve_MTS_FINITE_P1_NUMERIC_PRIOR_NONCLAIM | 5.6e-5 | m | 7.432631961577e-06 | 1.0 | source-intake/local_bounds/R10_alpha_lambda_bound_curve_ANCHOR_SMOKE.csv::R10_ANCHOR_EOTWASH_2007_ALPHA1_56UM | Yukawa_potential_alpha | numeric_prior_nonclaim_not_parent_sourced | 611-Y5-R10-real-bound-curve-QA-or-CX-component-prior-runner.md::CX611 | 611-Y5-R10-real-bound-curve-QA-or-CX-component-prior-runner.md | C_X_trial_grid_not_parent_sourced;anchor_bound_only;valid_for_claim_false | false | Diagnostic numeric prior only; runner must reject because rows are not parent-sourced claim rows. |
| MTS_finite_p1_prior_nonclaim | R10_finite_p1_CX_1.000000000000e+03 | R10_alpha_lambda_curve_MTS_FINITE_P1_NUMERIC_PRIOR_NONCLAIM | 5.6e-5 | m | 7.432631961577e-03 | 1.0 | source-intake/local_bounds/R10_alpha_lambda_bound_curve_ANCHOR_SMOKE.csv::R10_ANCHOR_EOTWASH_2007_ALPHA1_56UM | Yukawa_potential_alpha | numeric_prior_nonclaim_not_parent_sourced | 611-Y5-R10-real-bound-curve-QA-or-CX-component-prior-runner.md::CX611 | 611-Y5-R10-real-bound-curve-QA-or-CX-component-prior-runner.md | C_X_trial_grid_not_parent_sourced;anchor_bound_only;valid_for_claim_false | false | Diagnostic numeric prior only; runner must reject because rows are not parent-sourced claim rows. |
| MTS_finite_p1_prior_nonclaim | R10_finite_p1_CX_1.000000000000e+05 | R10_alpha_lambda_curve_MTS_FINITE_P1_NUMERIC_PRIOR_NONCLAIM | 5.6e-5 | m | 7.432631961577e-01 | 1.0 | source-intake/local_bounds/R10_alpha_lambda_bound_curve_ANCHOR_SMOKE.csv::R10_ANCHOR_EOTWASH_2007_ALPHA1_56UM | Yukawa_potential_alpha | numeric_prior_nonclaim_not_parent_sourced | 611-Y5-R10-real-bound-curve-QA-or-CX-component-prior-runner.md::CX611 | 611-Y5-R10-real-bound-curve-QA-or-CX-component-prior-runner.md | C_X_trial_grid_not_parent_sourced;anchor_bound_only;valid_for_claim_false | false | Diagnostic numeric prior only; runner must reject because rows are not parent-sourced claim rows. |

## Runner Summary
| runner_id | mts_curve | bound_curve | mts_rows | valid_mts_rows | bound_rows | valid_bound_rows | comparison_rows | passed_rows | blocked_or_failed_rows | R10_pass_for_claim | claim_allowed | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R10_RUNNER_611_NUMERIC_PRIOR_RECHECK | source-intake/mts_residuals/R10_alpha_lambda_curve_MTS_FINITE_P1_NUMERIC_PRIOR_NONCLAIM.csv | source-intake/local_bounds/R10_alpha_lambda_bound_curve_ANCHOR_SMOKE.csv | 6 | 0 | 2 | 0 | 1 | 0 | 1 | False | False | required blocked result: numeric priors and review/anchor bounds are nonclaim |

## Decision
| decision_id | status | decision | meaning | next_target | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| D611_0_review_curve | review_candidate_QA_pass_nonclaim | use vector curve only as private pressure data | good enough for internal C_X pressure, not enough for public R10 claim | 612-Y5-R10-CX-component-source-derivation-or-real-bound-curve-promotion.md | false |
| D611_1_CX_prior | component_prior_runner_built | use C_X prior grid to size finite p1 branch | the branch is now executable as pressure before parent coefficients exist | 612-Y5-R10-CX-component-source-derivation-or-real-bound-curve-promotion.md | false |
| D611_2_next_gate | data_or_theory_fork | next choose real bound-curve promotion or C_X component derivation | both are now explicit; neither is claim-ready | 612-Y5-R10-CX-component-source-derivation-or-real-bound-curve-promotion.md | false |
| D611_3_claim_ceiling | review_candidate_curve_and_CX_prior_pressure_only_no_R10_fifth_force_WEP_PPN_or_local_GR_pass | no R10, WEP, PPN, or local-GR pass | review candidates and priors are not evidence | 612-Y5-R10-CX-component-source-derivation-or-real-bound-curve-promotion.md | false |

## Route Update
| route_id | allowed_after_611 | forbidden_after_611 | next_action |
| --- | --- | --- | --- |
| RU611_0_data_route | promote real bound curve only after human/independent QA or official table | copy review candidate into live claim curve | 612-Y5-R10-CX-component-source-derivation-or-real-bound-curve-promotion.md |
| RU611_1_theory_route | derive C_X components or set source/test zero factors | treat C_X priors as parent coefficients | 612-Y5-R10-CX-component-source-derivation-or-real-bound-curve-promotion.md |
| RU611_2_runner_route | use nonclaim runner rows for schema/failure-mode checks | declare R10 pass from any valid_for_claim=false row | keep all diagnostics private until claim rows are real |

## Validation
| check_id | result | detail |
| --- | --- | --- |
| V611_0_source_paths_exist | pass | missing=0 |
| V611_1_prior_610_clean | pass | prior_rows=12;prior_failures=0 |
| V611_2_review_curve_QA_passes_nonclaim | pass | qa_rows=7;qa_failures=0 |
| V611_3_curve_stats_written | pass | stats_rows=4 |
| V611_4_CX_grid_numeric_nonclaim | pass | grid_rows=11;numeric=True |
| V611_5_component_prior_numeric_nonclaim | pass | component_rows=7;numeric=True |
| V611_6_lambda_windows_written | pass | window_rows=11;grid_rows=11 |
| V611_7_numeric_prior_template_nonclaim | pass | template_rows=6;numeric=True;nonclaim=True |
| V611_8_runner_blocks_nonclaim_rows | pass | valid_mts=0;valid_bound=0;R10_pass=False;claim_allowed=False |
| V611_9_live_files_not_overwritten | pass | live_mts_rows=2;live_bound_rows=2 |
| V611_10_no_claim_rows | pass | claim_rows=0 |
| V611_11_no_R10_or_local_GR_claim | pass | R10_pass=false;WEP=false;PPN=false;local_GR=false |

## Practical Read
This is exactly where the project becomes test-shaped. We have not won R10, but we now have a review-grade pressure curve and a finite-branch coefficient dial that can be attacked from either side. If `C_X` derives small or the range lands in a forgiving window, the branch survives a round. If it lands near the tight part of the curve with a huge `C_X`, it gets punished and we know where to repair.
