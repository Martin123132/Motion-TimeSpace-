# 567 Y5 R10 finite alpha coefficient fill and real bound curve runner

Generated: 2026-06-04T18:30:17.914081+00:00  
Status: `Y5_R10_finite_alpha_coefficient_fill_scaffold_written_reverse_bounds_anchor_only_no_claim`  
Claim ceiling: `finite_alpha_coefficient_scaffold_only_no_R10_fifth_force_WEP_PPN_or_local_GR_pass`  
Next target: `568-Y5-R10-real-bound-curve-digitization-or-coefficient-prior-scan.md`

## Verdict
- The clean zero-route remains blocked unless a future parent action derives the quotient/no-marker clause.
- The retained physical branch is now written as a finite `alpha_X(lambda)` coefficient contract instead of being left vague.
- The current numerical state is still non-claim: alpha rows are symbolic, and the external R10 evidence is anchor-only rather than a full digitized `alpha_bound(lambda)` curve.
- The useful progress is that we now know exactly what has to be filled: `Z_X`, `M_X^2`, `qbar_XT`, `Qbar_XH(lambda)`, and the real R10 bound curve.

## Finite Alpha Law
| law_id | object | symbolic_form | equivalent_contract | needed_inputs | derived_from_parent | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| FA567_0_finite_alpha | alpha_X(lambda_X) | alpha_X(lambda_X)=s_X*Qbar_XH(lambda_X)*qbar_XT/(4*pi*Z_X*G_obs) | alpha_X(lambda_X)=K_X*Qbar_XH(lambda_X)*qbar_XT | s_X;Z_X;G_obs;Qbar_XH(lambda_X);qbar_XT | false | false |
| FA567_1_range | lambda_X | lambda_X=sqrt(Z_X/M_X^2) | M_X^2=Z_X/lambda_X^2 | Z_X;M_X^2 | false | false |
| FA567_2_bound_product | P_X(lambda) | P_X(lambda)=abs(K_X*Qbar_XH(lambda)*qbar_XT) | P_X(lambda)<=alpha_bound(lambda) | K_X;Qbar_XH(lambda);qbar_XT;alpha_bound(lambda) | false | false |
| FA567_3_reverse_anchor | anchor-only reverse constraint | abs(K_X*Qbar_XH(lambda_anchor)*qbar_XT)<=alpha_anchor | source-backed anchors define non-claim target magnitudes only | anchor lambda;anchor alpha_bound;full curve before claim | false | false |

## Coefficient Requirements
| requirement_id | symbol | needed_for | current_status | fill_contract | blocks | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| AF566_0_ZX | Z_X | lambda_X and K_X | missing_parent_Hessian_value | derive positive kinetic Hessian coefficient or define conservative scan prior | lambda_X;K_X;ghost/stability sign | false |
| AF566_1_MX | M_X^2;lambda_X | R10 lambda_value | missing_parent_Hessian_value | derive positive Hessian mass gap or scan lambda_X directly as non-claim | range selection;interpolation into R10 bound curve | false |
| AF566_2_qtest | qbar_XT | ordinary test-body X charge | not_theorem_zero | derive ordinary test-body X neutrality or enter residual coupling bound | WEP/local fifth-force amplitude | false |
| AF566_3_source | Qbar_XH(lambda) | source projected X charge | hidden_source_channels_open | derive source projected X charge or channelwise source form factor | source amplitude in torsion-balance bodies | false |
| AF566_4_bound_curve | alpha_bound(lambda) | external R10 comparison | anchor_only_noncurve | digitize/source full alpha_bound(lambda) curve with valid claim rows | external evidence comparison | false |

## Reverse Bound Targets
| target_id | bound_id | lambda_value | lambda_units | alpha_bound | max_abs_KQqbar_at_anchor | claim_blocker | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RBT567_0 | R10_ANCHOR_EOTWASH_2020_ALPHA1_38P6UM | 3.86e-5 | m | 1.0 | 1.0 | anchor_only_noncurve | false |
| RBT567_1 | R10_ANCHOR_EOTWASH_2007_ALPHA1_56UM | 5.6e-5 | m | 1.0 | 1.0 | anchor_only_noncurve | false |

## Prior Scan Template
| scan_id | parameter | suggested_domain | units | why | claim_use | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| PST567_0_lambda_anchor_window | lambda_X | 3.0e-5 m <= lambda_X <= 6.5e-5 m | m | covers current Eot-Wash alpha=1 anchor thresholds without pretending to have full curve | smoke_only | false |
| PST567_1_lambda_broad_R10 | lambda_X | 1.0e-6 m <= lambda_X <= 1.0e-2 m | m | broad non-claim R10 range for later digitized curve interpolation stress | smoke_only_until_curve_digitized | false |
| PST567_2_product_amplitude | abs(K_X*Qbar_XH*qbar_XT) | log10 product from -30 to +3 | dimensionless_alpha_convention | tests whether any finite source/test charge branch can sit below short-range fifth-force bounds | nonclaim_prior_scan | false |
| PST567_3_sign | s_X | -1,+1 | sign | keeps attractive/repulsive convention explicit while R10 compares abs(alpha) | diagnostic_only | false |
| PST567_4_source_charge | Qbar_XH(lambda) | parent integral or channelwise bound required | parent_normalized | torsion-balance source composition must not be hand-waved | blocked_until_parent_or_external_source_model | false |
| PST567_5_test_charge | qbar_XT | zero theorem or residual bound required | parent_normalized | ordinary test-body neutrality is the local-GR/WEP pressure point | blocked_until_parent_or_residual_bound | false |

## MTS Smoke Alpha Rows
| curve_id | lambda_value | lambda_units | alpha_predicted | alpha_bound | derivation_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| R10_alpha_lambda_curve_MTS_FINITE_ALPHA_SMOKE_NONCLAIM_0 | 3.86e-5 | m | K_X*Qbar_XH(lambda)*qbar_XT | 1.0 | symbolic_coefficient_fill_required_not_numeric | false |
| R10_alpha_lambda_curve_MTS_FINITE_ALPHA_SMOKE_NONCLAIM_1 | 5.6e-5 | m | K_X*Qbar_XH(lambda)*qbar_XT | 1.0 | symbolic_coefficient_fill_required_not_numeric | false |

## Runner Summary
| runner_id | mts_curve | bound_curve | valid_mts_rows | valid_bound_rows | comparison_rows | R10_pass_for_claim | claim_allowed | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R10_RUNNER_567_LIVE_PLACEHOLDER_RECHECK | source-intake/mts_residuals/R10_alpha_lambda_curve_MTS_source_normalization.csv | source-intake/local_bounds/R10_alpha_lambda_bound_curve_DIGITIZED.csv | 0 | 0 | 1 | False | False | live files remain blocked exactly as intended |
| R10_RUNNER_567_FINITE_ALPHA_ANCHOR_SMOKE | source-intake/mts_residuals/R10_alpha_lambda_curve_MTS_FINITE_ALPHA_SMOKE_NONCLAIM.csv | source-intake/local_bounds/R10_alpha_lambda_bound_curve_ANCHOR_SMOKE.csv | 0 | 0 | 1 | False | False | symbolic finite-alpha smoke rows and anchor-only bound rows remain non-claim |

## Evaluator
| gate_id | gate | result | detail | valid_for_claim |
| --- | --- | --- | --- | --- |
| E567_0_zero_route | promote R10 theorem-zero | blocked | quotient/no-marker clause is sufficient but still not parent-derived | false |
| E567_1_finite_alpha_law | write exact finite-alpha amplitude contract | pass_scaffold | alpha_X(lambda)=K_X Qbar_XH(lambda) qbar_XT with abs product compared to R10 bound | false |
| E567_2_reverse_bounds | turn available anchors into reverse coefficient targets | pass_nonclaim | reverse_targets=2; all anchor-only | false |
| E567_3_runner_guardrail | confirm no branch passes R10 for claim | pass | live placeholder and finite-alpha smoke runner both block claim | false |

## Blocker Ledger
| blocker_id | blocker | why_it_matters | next_action | claim_blocked |
| --- | --- | --- | --- | --- |
| B567_0_no_numeric_parent_coefficients | Z_X, M_X^2, qbar_XT, and Qbar_XH(lambda) remain unfilled. | alpha_X(lambda) cannot be computed from parent data. | derive coefficients or run an explicitly non-claim prior scan. | true |
| B567_1_real_bound_curve_missing | R10 alpha_bound(lambda) is still anchor-only/noncurve. | interpolation and exclusion claims require a real curve, not threshold sentences. | digitize full Eot-Wash bound curve or find source-backed machine-readable rows. | true |
| B567_2_vertical_branch_not_derived | ordinary matter X neutrality is not a theorem. | cannot set qbar_XT=0 without a parent quotient/no-marker proof. | either derive qbar_XT=0 or keep finite-alpha branch under R10 pressure. | true |

## Decision
| decision_id | decision | meaning | status | next_target |
| --- | --- | --- | --- | --- |
| D567_0_finite_alpha_branch_retained | retain physical X finite-alpha branch | R10 risk is now an amplitude product, not an informal worry | retained_nonclaim | 568-Y5-R10-real-bound-curve-digitization-or-coefficient-prior-scan.md |
| D567_1_no_R10_claim | do not claim R10/local-GR pass | symbolic alpha and anchor-only bound rows are diagnostic only | blocked_for_claim | 568-Y5-R10-real-bound-curve-digitization-or-coefficient-prior-scan.md |
| D567_2_next_fork | choose digitized curve or coefficient prior scan next | data curve and parent coefficients are now separable missing pieces | next_required | 568-Y5-R10-real-bound-curve-digitization-or-coefficient-prior-scan.md |

## Source Register
| source_file | role | source_type | exists | valid_for_claim |
| --- | --- | --- | --- | --- |
| 566-Y5-R10-primitive-quotient-no-marker-parent-clause-or-alpha-coefficient-fill.md | immediate upstream fork: primitive quotient/no-marker route ended in coefficient fill | local_path | true | false |
| source-intake/mts_residuals/P8_Y5_BRR545_566_VALIDATION.csv | prior checkpoint validation guardrail | local_path | true | false |
| source-intake/mts_residuals/P8_Y5_R10_566_ALPHA_COEFFICIENT_FILL_QUEUE.csv | coefficient fill queue inherited from 566 | local_path | true | false |
| source-intake/mts_residuals/R10_alpha_lambda_curve_MTS_source_normalization.csv | live MTS alpha(lambda) placeholder retained unchanged | local_path | true | false |
| source-intake/local_bounds/R10_alpha_lambda_bound_curve_DIGITIZED.csv | live R10 bound placeholder retained unchanged | local_path | true | false |
| source-intake/local_bounds/R10_alpha_lambda_bound_curve_ANCHOR_SMOKE.csv | source-backed anchor-only smoke bound rows | local_path | true | false |
| scripts/R10_alpha_lambda_bound_prediction_runner.py | existing alpha(lambda) comparator reused | local_path | true | false |
| scripts/Y5_R10_finite_alpha_coefficient_fill_and_real_bound_curve_runner.py | this checkpoint generator | local_path | true | false |
| https://pubmed.ncbi.nlm.nih.gov/32216404/ | modern Eot-Wash short-range anchor metadata | web_source_recorded_not_reacquired | not_applicable_url | false |
| https://arxiv.org/abs/2002.11761 | modern Eot-Wash 2020 source-backed anchor row | web_source_recorded_not_reacquired | not_applicable_url | false |
| https://arxiv.org/abs/hep-ph/0611184 | 2007 Eot-Wash continuity anchor row | web_source_recorded_not_reacquired | not_applicable_url | false |

## Validation
| check_id | result | detail |
| --- | --- | --- |
| V567_0_source_paths_exist | pass | missing=0 |
| V567_1_prior_566_clean | pass | prior_validation_rows=8;prior_fails=0 |
| V567_2_finite_alpha_law_written | pass | law_rows=4 |
| V567_3_coefficient_requirements_preserved | pass | requirement_rows=5 |
| V567_4_reverse_bounds_anchor_only | pass | reverse_rows=2;numeric_positive=2;valid_for_claim_true=0 |
| V567_5_smoke_rows_nonclaim_symbolic | pass | smoke_rows=2;claim_or_missing_marker_rows=0 |
| V567_6_live_runner_still_blocks | pass | valid_mts=0;valid_bound=0;R10_pass=False |
| V567_7_finite_smoke_runner_blocks | pass | valid_mts=0;valid_bound=0;R10_pass=False |
| V567_8_no_overclaim | pass | finite_alpha_numeric=false;real_bound_curve=false;R10_pass=false;WEP=false;PPN=false;local_GR=false |

## Route Update
| route_id | allowed_after_567 | forbidden_after_567 | next_action |
| --- | --- | --- | --- |
| RU567_0_allowed | Use finite-alpha law as a private coefficient-fill scaffold. | Claim R10 fifth-force pass, WEP pass, PPN pass, local-GR pass, or alpha=0 theorem. | 568-Y5-R10-real-bound-curve-digitization-or-coefficient-prior-scan.md |
| RU567_1_data_route | Acquire/digitize the real alpha_bound(lambda) curve before exclusion scoring. | Treat alpha=1 threshold anchors as a full bound curve. | build curve digitizer or source-backed table intake |
| RU567_2_theory_route | Derive or bound Z_X, M_X^2, qbar_XT, and Qbar_XH(lambda). | Hide a physical finite-range X mode behind the earlier closure route. | coefficient prior scan only if clearly marked non-claim |

## Practical Read
This checkpoint does not rescue R10 by declaration. It does the useful engineering thing: it converts the surviving local fifth-force risk into an exact amplitude product and reverse-bound target. If the parent action later proves `qbar_XT=0` or `Qbar_XH=0`, the branch can return to theorem-zero. If not, the theory has to show the finite product sits below a real digitized Eot-Wash-style `alpha_bound(lambda)` curve.
