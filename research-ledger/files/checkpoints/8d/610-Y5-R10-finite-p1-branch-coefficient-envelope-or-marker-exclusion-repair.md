# 610 Y5 R10 finite p1 branch coefficient envelope or marker-exclusion repair

Generated: 2026-06-05T21:17:00.042602+00:00  
Status: `Y5_R10_best_method_selected_finite_p1_coefficient_envelope_nonclaim_marker_closure_deferred`  
Claim ceiling: `finite_p1_envelope_and_pressure_only_no_R10_fifth_force_WEP_PPN_or_local_GR_pass`  
Next target: `611-Y5-R10-real-bound-curve-QA-or-CX-component-prior-runner.md`  
Run root: `runs/20260605-211700-Y5-R10-finite-p1-branch-coefficient-envelope-or-marker-exclusion-repair`

## Verdict
- Best method selected: finite `p=1` coefficient envelope, not an unearned `O(E_D)` closure.
- The working law is `alpha_X(lambda_X)=epsilon_shell*C_X(lambda_X)`.
- Anchor-only pressure says order-one `C_X` is not immediately absurd, but that is private guidance only, not evidence.
- The next executable wall is now precise: real `alpha_bound(lambda)` curve plus numeric/source-backed `C_X(lambda_X)` and `lambda_X`.

## Source Register
| source_file | exists | role |
| --- | --- | --- |
| 609-Y5-R10-parent-own-norm-square-activation-or-finite-p1-branch.md | True | immediate 609 handoff |
| source-intake/mts_residuals/P8_Y5_BRR545_609_VALIDATION.csv | True | prior validation gate |
| source-intake/mts_residuals/P8_Y5_R10_609_FINITE_P1_BRANCH_LEDGER.csv | True | finite p1 branch trigger |
| source-intake/mts_residuals/P8_Y5_R10_609_P_BRANCH_DECISION.csv | True | p branch decision |
| 607-Y5-R10-compact-shell-parent-coefficient-factorization-or-theorem-zero.md | True | alpha=epsilon^p C_X factorization |
| source-intake/mts_residuals/P8_Y5_R10_607_COEFFICIENT_PRESSURE_TABLE.csv | True | prior epsilon pressure rows |
| 578-Y5-R10-lambda-X-mass-gap-and-product-coefficient-derivation-targets.md | True | lambda/product coefficient derivation |
| source-intake/mts_residuals/P8_Y5_R10_578_PRODUCT_COEFFICIENT_DERIVATION.csv | True | C_X component definitions |
| 579-Y5-R10-parent-Hessian-source-charge-fill-or-theorem-zero-return.md | True | source charge decomposition and countermodel |
| source-intake/mts_residuals/P8_Y5_R10_579_SOURCE_CHARGE_DECOMPOSITION.csv | True | source/test/K_X exact expressions |
| 608-Y5-R10-double-zero-exponent-origin-or-source-neutrality-proof.md | True | p2 theorem target kept but not promoted |
| source-intake/local_bounds/R10_alpha_lambda_bound_curve_ANCHOR_SMOKE.csv | True | anchor-only non-claim R10 bound rows |
| source-intake/local_bounds/R10_alpha_lambda_bound_curve_DIGITIZED.csv | True | live claim placeholder kept unchanged |
| source-intake/mts_residuals/R10_alpha_lambda_curve_MTS_source_normalization.csv | True | live MTS placeholder kept unchanged |
| scripts/R10_alpha_lambda_bound_prediction_runner.py | True | existing comparator reused unchanged |
| scripts/Y5_R10_finite_p1_branch_coefficient_envelope_or_marker_exclusion_repair.py | True | this checkpoint generator |

## Method Selection
| method_id | method | selection | why_best | physics_cost | output | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| MS610_0_finite_p1_envelope | finite p=1 coefficient envelope | selected_best_method | it is testable, does not add an unearned parent axiom, and keeps p2 as a theorem target without pretending it is derived | finite residual branch is not local-GR theorem-zero | alpha_X=lambda branch = epsilon_shell C_X(lambda_X) | false |
| MS610_1_parent_OED_closure | explicit parent O(E_D) norm-square clause | deferred_repair_option | would close p=2 cleanly only if labelled as new closure/action clause | closure is less derivation-pure and must be publicly labelled | p=2 theorem target retained but not used as evidence | false |
| MS610_2_p3_determinant | det(Q_coh) p=3 route | deferred | beautiful shape but too many ownership blockers remain | raw det(Q) shear leak forbids shortcut | theorem target only | false |

## Finite P1 Coefficient Envelope
| coefficient_id | object | formula | definition | known | missing | claim_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CE610_0_alpha_law | finite p1 alpha law | alpha_X(lambda_X)=epsilon_shell*C_X(lambda_X) | C_X=sigma_X*kappa_X*Qbar_XH(lambda_X)*qbar_XT/(4*pi*Z_X*G_obs) | epsilon_shell=7.43263196157697e-06 | C_X(lambda_X), lambda_X, claim-grade alpha_bound(lambda) | symbolic_nonclaim | false |
| CE610_1_CX | C_X(lambda_X) | sigma_X*kappa_X*Qbar_XH(lambda_X)*qbar_XT/(4*pi*Z_X*G_obs) | dimensionless source-test-normalization product in the R10 Yukawa convention | exact factorization from 607/578/579 | numeric sign, Hessian normalization, source projection, test projection | factorized_symbolic | false |
| CE610_2_lambda | lambda_X | lambda_X=sqrt(Z_X/M_X^2) | finite range from parent Hessian ratio | conditional law derived | numeric positive M_X^2/Z_X with units | symbolic_nonclaim | false |
| CE610_3_claim_gate | R10 claim promotion | abs(epsilon_shell*C_X(lambda_X)) <= alpha_bound(lambda_X) | claim-grade comparison after all rows are numeric/sourced | runner schema exists | real bound curve plus numeric parent C_X and lambda_X | blocked | false |

## Alpha Pressure Envelope
| pressure_id | bound_id | lambda_value | lambda_units | alpha_bound_anchor | abs_CX_trial | epsilon_shell | alpha_predicted_p1 | ratio_to_anchor_bound | anchor_private_pass | claim_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AP610_R10_ANCHOR_EOTWASH_2020_ALPHA1_38P6UM_C0.001 | R10_ANCHOR_EOTWASH_2020_ALPHA1_38P6UM | 3.86e-5 | m | 1 | 1.000000000000e-03 | 7.432631961577e-06 | 7.432631961577e-09 | 7.432631961577e-09 | True | anchor_only_nonclaim_pressure | false |
| AP610_R10_ANCHOR_EOTWASH_2020_ALPHA1_38P6UM_C0.01 | R10_ANCHOR_EOTWASH_2020_ALPHA1_38P6UM | 3.86e-5 | m | 1 | 1.000000000000e-02 | 7.432631961577e-06 | 7.432631961577e-08 | 7.432631961577e-08 | True | anchor_only_nonclaim_pressure | false |
| AP610_R10_ANCHOR_EOTWASH_2020_ALPHA1_38P6UM_C0.1 | R10_ANCHOR_EOTWASH_2020_ALPHA1_38P6UM | 3.86e-5 | m | 1 | 1.000000000000e-01 | 7.432631961577e-06 | 7.432631961577e-07 | 7.432631961577e-07 | True | anchor_only_nonclaim_pressure | false |
| AP610_R10_ANCHOR_EOTWASH_2020_ALPHA1_38P6UM_C1 | R10_ANCHOR_EOTWASH_2020_ALPHA1_38P6UM | 3.86e-5 | m | 1 | 1.000000000000e+00 | 7.432631961577e-06 | 7.432631961577e-06 | 7.432631961577e-06 | True | anchor_only_nonclaim_pressure | false |
| AP610_R10_ANCHOR_EOTWASH_2020_ALPHA1_38P6UM_C10 | R10_ANCHOR_EOTWASH_2020_ALPHA1_38P6UM | 3.86e-5 | m | 1 | 1.000000000000e+01 | 7.432631961577e-06 | 7.432631961577e-05 | 7.432631961577e-05 | True | anchor_only_nonclaim_pressure | false |
| AP610_R10_ANCHOR_EOTWASH_2020_ALPHA1_38P6UM_C100 | R10_ANCHOR_EOTWASH_2020_ALPHA1_38P6UM | 3.86e-5 | m | 1 | 1.000000000000e+02 | 7.432631961577e-06 | 7.432631961577e-04 | 7.432631961577e-04 | True | anchor_only_nonclaim_pressure | false |
| AP610_R10_ANCHOR_EOTWASH_2020_ALPHA1_38P6UM_C1000 | R10_ANCHOR_EOTWASH_2020_ALPHA1_38P6UM | 3.86e-5 | m | 1 | 1.000000000000e+03 | 7.432631961577e-06 | 7.432631961577e-03 | 7.432631961577e-03 | True | anchor_only_nonclaim_pressure | false |
| AP610_R10_ANCHOR_EOTWASH_2020_ALPHA1_38P6UM_C10000 | R10_ANCHOR_EOTWASH_2020_ALPHA1_38P6UM | 3.86e-5 | m | 1 | 1.000000000000e+04 | 7.432631961577e-06 | 7.432631961577e-02 | 7.432631961577e-02 | True | anchor_only_nonclaim_pressure | false |
| AP610_R10_ANCHOR_EOTWASH_2020_ALPHA1_38P6UM_C100000 | R10_ANCHOR_EOTWASH_2020_ALPHA1_38P6UM | 3.86e-5 | m | 1 | 1.000000000000e+05 | 7.432631961577e-06 | 7.432631961577e-01 | 7.432631961577e-01 | True | anchor_only_nonclaim_pressure | false |
| AP610_R10_ANCHOR_EOTWASH_2020_ALPHA1_38P6UM_C134542 | R10_ANCHOR_EOTWASH_2020_ALPHA1_38P6UM | 3.86e-5 | m | 1 | 1.345418426702e+05 | 7.432631961577e-06 | 1.000000000000e+00 | 1.000000000000e+00 | True | anchor_only_nonclaim_pressure | false |
| AP610_R10_ANCHOR_EOTWASH_2020_ALPHA1_38P6UM_C1e06 | R10_ANCHOR_EOTWASH_2020_ALPHA1_38P6UM | 3.86e-5 | m | 1 | 1.000000000000e+06 | 7.432631961577e-06 | 7.432631961577e+00 | 7.432631961577e+00 | False | anchor_only_nonclaim_pressure | false |
| AP610_R10_ANCHOR_EOTWASH_2007_ALPHA1_56UM_C0.001 | R10_ANCHOR_EOTWASH_2007_ALPHA1_56UM | 5.6e-5 | m | 1 | 1.000000000000e-03 | 7.432631961577e-06 | 7.432631961577e-09 | 7.432631961577e-09 | True | anchor_only_nonclaim_pressure | false |
| AP610_R10_ANCHOR_EOTWASH_2007_ALPHA1_56UM_C0.01 | R10_ANCHOR_EOTWASH_2007_ALPHA1_56UM | 5.6e-5 | m | 1 | 1.000000000000e-02 | 7.432631961577e-06 | 7.432631961577e-08 | 7.432631961577e-08 | True | anchor_only_nonclaim_pressure | false |
| AP610_R10_ANCHOR_EOTWASH_2007_ALPHA1_56UM_C0.1 | R10_ANCHOR_EOTWASH_2007_ALPHA1_56UM | 5.6e-5 | m | 1 | 1.000000000000e-01 | 7.432631961577e-06 | 7.432631961577e-07 | 7.432631961577e-07 | True | anchor_only_nonclaim_pressure | false |
| AP610_R10_ANCHOR_EOTWASH_2007_ALPHA1_56UM_C1 | R10_ANCHOR_EOTWASH_2007_ALPHA1_56UM | 5.6e-5 | m | 1 | 1.000000000000e+00 | 7.432631961577e-06 | 7.432631961577e-06 | 7.432631961577e-06 | True | anchor_only_nonclaim_pressure | false |
| AP610_R10_ANCHOR_EOTWASH_2007_ALPHA1_56UM_C10 | R10_ANCHOR_EOTWASH_2007_ALPHA1_56UM | 5.6e-5 | m | 1 | 1.000000000000e+01 | 7.432631961577e-06 | 7.432631961577e-05 | 7.432631961577e-05 | True | anchor_only_nonclaim_pressure | false |
| AP610_R10_ANCHOR_EOTWASH_2007_ALPHA1_56UM_C100 | R10_ANCHOR_EOTWASH_2007_ALPHA1_56UM | 5.6e-5 | m | 1 | 1.000000000000e+02 | 7.432631961577e-06 | 7.432631961577e-04 | 7.432631961577e-04 | True | anchor_only_nonclaim_pressure | false |
| AP610_R10_ANCHOR_EOTWASH_2007_ALPHA1_56UM_C1000 | R10_ANCHOR_EOTWASH_2007_ALPHA1_56UM | 5.6e-5 | m | 1 | 1.000000000000e+03 | 7.432631961577e-06 | 7.432631961577e-03 | 7.432631961577e-03 | True | anchor_only_nonclaim_pressure | false |
| AP610_R10_ANCHOR_EOTWASH_2007_ALPHA1_56UM_C10000 | R10_ANCHOR_EOTWASH_2007_ALPHA1_56UM | 5.6e-5 | m | 1 | 1.000000000000e+04 | 7.432631961577e-06 | 7.432631961577e-02 | 7.432631961577e-02 | True | anchor_only_nonclaim_pressure | false |
| AP610_R10_ANCHOR_EOTWASH_2007_ALPHA1_56UM_C100000 | R10_ANCHOR_EOTWASH_2007_ALPHA1_56UM | 5.6e-5 | m | 1 | 1.000000000000e+05 | 7.432631961577e-06 | 7.432631961577e-01 | 7.432631961577e-01 | True | anchor_only_nonclaim_pressure | false |
| AP610_R10_ANCHOR_EOTWASH_2007_ALPHA1_56UM_C134542 | R10_ANCHOR_EOTWASH_2007_ALPHA1_56UM | 5.6e-5 | m | 1 | 1.345418426702e+05 | 7.432631961577e-06 | 1.000000000000e+00 | 1.000000000000e+00 | True | anchor_only_nonclaim_pressure | false |
| AP610_R10_ANCHOR_EOTWASH_2007_ALPHA1_56UM_C1e06 | R10_ANCHOR_EOTWASH_2007_ALPHA1_56UM | 5.6e-5 | m | 1 | 1.000000000000e+06 | 7.432631961577e-06 | 7.432631961577e+00 | 7.432631961577e+00 | False | anchor_only_nonclaim_pressure | false |

## Component Budget Scenarios
| scenario_id | Qbar_XH_trial | qbar_XT_trial | source_test_product | max_abs_normalization_factor_anchor_only | meaning | claim_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CB610_unit_source_unit_test | 1.000000000000e+00 | 1.000000000000e+00 | 1.000000000000e+00 | 1.345418426702e+05 | allowed \|sigma*kappa/(4*pi Z_X G_obs)\| under anchor-only alpha_bound=1 pressure | private_pressure_only_not_claim | false |
| CB610_weak_test_1e_minus_2 | 1.000000000000e+00 | 1.000000000000e-02 | 1.000000000000e-02 | 1.345418426702e+07 | allowed \|sigma*kappa/(4*pi Z_X G_obs)\| under anchor-only alpha_bound=1 pressure | private_pressure_only_not_claim | false |
| CB610_weak_source_1e_minus_2 | 1.000000000000e-02 | 1.000000000000e+00 | 1.000000000000e-02 | 1.345418426702e+07 | allowed \|sigma*kappa/(4*pi Z_X G_obs)\| under anchor-only alpha_bound=1 pressure | private_pressure_only_not_claim | false |
| CB610_both_1e_minus_2 | 1.000000000000e-02 | 1.000000000000e-02 | 1.000000000000e-04 | 1.345418426702e+09 | allowed \|sigma*kappa/(4*pi Z_X G_obs)\| under anchor-only alpha_bound=1 pressure | private_pressure_only_not_claim | false |
| CB610_both_1e_minus_3 | 1.000000000000e-03 | 1.000000000000e-03 | 1.000000000000e-06 | 1.345418426702e+11 | allowed \|sigma*kappa/(4*pi Z_X G_obs)\| under anchor-only alpha_bound=1 pressure | private_pressure_only_not_claim | false |
| CB610_source_screened_1e_minus_4_test_unit | 1.000000000000e-04 | 1.000000000000e+00 | 1.000000000000e-04 | 1.345418426702e+09 | allowed \|sigma*kappa/(4*pi Z_X G_obs)\| under anchor-only alpha_bound=1 pressure | private_pressure_only_not_claim | false |

## Marker-Exclusion Repair Option
| repair_id | repair_option | clause | would_buy | why_not_selected_now | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| MR610_0_explicit_OED_clause | add parent O(E_D) norm-square activation | S_act depends on compact-shell amplitude only through \|\|a_D\|\|^2 | p=2 by construction and no linear marker | it is a new parent closure/action clause, not derived from current corpus | labelled_closure_option_only | false |
| MR610_1_no_marker_repair | prove no natural marker covector exists | E_D has no parent-owned covectors besides zero after quotienting | p=1 counterexample removed | 573/574 marker generator debts remain open | theorem_target | false |
| MR610_2_readout_repair | formal readout-after-variation parent theorem | readout maps Sol(S_parent)->Obs and cannot source reduced parent terms | blocks post-readout linear marker | not enough by itself; material/domain markers still survive | partial_repair_target | false |

## MTS Finite P1 Template
| model_id | branch_id | curve_id | lambda_value | lambda_units | alpha_predicted | alpha_bound | alpha_bound_source | force_law_form | derivation_status | formula_reference | source_file | assumptions | valid_for_claim | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_finite_p1_envelope | R10_finite_p1_symbolic_CX | R10_alpha_lambda_curve_MTS_FINITE_P1_ENVELOPE_TEMPLATE | 3.86e-5 | m | epsilon_shell*C_X(lambda_X) | 1.0 | source-intake/local_bounds/R10_alpha_lambda_bound_curve_ANCHOR_SMOKE.csv::R10_ANCHOR_EOTWASH_2020_ALPHA1_38P6UM | Yukawa_potential_alpha | finite_p1_symbolic_envelope_nonclaim | 610-Y5-R10-finite-p1-branch-coefficient-envelope-or-marker-exclusion-repair.md::CE610_0_alpha_law | 610-Y5-R10-finite-p1-branch-coefficient-envelope-or-marker-exclusion-repair.md | MISSING_C_X;MISSING_PARENT_LAMBDA;anchor_bound_only;finite_p1_not_local_GR_theorem | false | Template row only; runner must reject until C_X, lambda_X, and alpha_bound(lambda) are real. |
| MTS_finite_p1_envelope | R10_finite_p1_symbolic_CX | R10_alpha_lambda_curve_MTS_FINITE_P1_ENVELOPE_TEMPLATE | 5.6e-5 | m | epsilon_shell*C_X(lambda_X) | 1.0 | source-intake/local_bounds/R10_alpha_lambda_bound_curve_ANCHOR_SMOKE.csv::R10_ANCHOR_EOTWASH_2007_ALPHA1_56UM | Yukawa_potential_alpha | finite_p1_symbolic_envelope_nonclaim | 610-Y5-R10-finite-p1-branch-coefficient-envelope-or-marker-exclusion-repair.md::CE610_0_alpha_law | 610-Y5-R10-finite-p1-branch-coefficient-envelope-or-marker-exclusion-repair.md | MISSING_C_X;MISSING_PARENT_LAMBDA;anchor_bound_only;finite_p1_not_local_GR_theorem | false | Template row only; runner must reject until C_X, lambda_X, and alpha_bound(lambda) are real. |

## Runner Summary
| runner_id | mts_curve | bound_curve | mts_rows | valid_mts_rows | bound_rows | valid_bound_rows | comparison_rows | passed_rows | blocked_or_failed_rows | R10_pass_for_claim | claim_allowed | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R10_RUNNER_610_FINITE_P1_TEMPLATE_RECHECK | source-intake/mts_residuals/R10_alpha_lambda_curve_MTS_FINITE_P1_ENVELOPE_TEMPLATE.csv | source-intake/local_bounds/R10_alpha_lambda_bound_curve_ANCHOR_SMOKE.csv | 2 | 0 | 2 | 0 | 1 | 0 | 1 | False | False | required blocked result: finite p1 template remains symbolic and anchor bounds are nonclaim |

## Decision
| decision_id | status | decision | meaning | next_target | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| D610_0_method | Y5_R10_best_method_selected_finite_p1_coefficient_envelope_nonclaim_marker_closure_deferred | select finite p1 coefficient envelope as best method | testable and honest; avoids adding unearned O(E_D) closure | 611-Y5-R10-real-bound-curve-QA-or-CX-component-prior-runner.md | false |
| D610_1_pressure | private_pressure_useful | use anchor-only pressure to size C_X, not as evidence | order-one C_X is not immediately absurd, but real bound curve is still mandatory | 611-Y5-R10-real-bound-curve-QA-or-CX-component-prior-runner.md | false |
| D610_2_marker_repair | deferred | keep marker exclusion repair as labelled closure/theorem target | p2 can return only through explicit parent clause or no-marker proof | 611-Y5-R10-real-bound-curve-QA-or-CX-component-prior-runner.md | false |
| D610_3_claim_ceiling | finite_p1_envelope_and_pressure_only_no_R10_fifth_force_WEP_PPN_or_local_GR_pass | no R10, WEP, PPN, or local-GR pass | finite branch is a residual envelope, not GR reduction | 611-Y5-R10-real-bound-curve-QA-or-CX-component-prior-runner.md | false |

## Route Update
| route_id | allowed_after_610 | forbidden_after_610 | next_action |
| --- | --- | --- | --- |
| RU610_0_data_route | QA real R10 bound curve or acquire official/digitized alpha(lambda) rows | use anchor-only pressure as claim evidence | 611-Y5-R10-real-bound-curve-QA-or-CX-component-prior-runner.md |
| RU610_1_theory_route | derive or bound C_X components K/Z, Qbar_XH, qbar_XT, lambda_X | treat symbolic C_X as a prediction | 611-Y5-R10-real-bound-curve-QA-or-CX-component-prior-runner.md |
| RU610_2_closure_route | write O(E_D) norm-square clause only as labelled closure | smuggle p2 closure into derived local GR | defer unless finite branch fails badly |

## Validation
| check_id | result | detail |
| --- | --- | --- |
| V610_0_source_paths_exist | pass | missing=0 |
| V610_1_prior_609_clean | pass | prior_rows=11;prior_failures=0 |
| V610_2_best_method_selected | pass | selected=finite p=1 coefficient envelope |
| V610_3_coefficient_envelope_written | pass | coefficient_rows=4 |
| V610_4_pressure_numeric_nonclaim | pass | pressure_rows=22;numeric=True;nonclaim=True |
| V610_5_component_budget_numeric_nonclaim | pass | budget_rows=6;numeric=True |
| V610_6_marker_repair_not_smuggled | pass | repair_rows=3;claim_rows=0 |
| V610_7_template_symbolic_nonclaim | pass | template_rows=2;symbolic=True;nonclaim=True |
| V610_8_runner_blocks_template | pass | valid_mts=0;valid_bound=0;R10_pass=False;claim_allowed=False |
| V610_9_live_files_not_overwritten | pass | live_mts_rows=2;live_bound_rows=2 |
| V610_10_no_claim_rows | pass | claim_rows=0 |
| V610_11_no_R10_or_local_GR_claim | pass | R10_pass=false;WEP=false;PPN=false;local_GR=false |

## Practical Read
This is the Money Mayweather move: stay in the fight, do not throw a fake knockout punch. We are not claiming local GR from `p=1`; we are making the finite branch measurable. If the real curve and real coefficients let it survive, we have a respectable residual branch. If it fails, we know exactly where to return: marker exclusion or a labelled parent norm-square closure.
