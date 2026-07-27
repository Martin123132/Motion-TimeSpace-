# 563 Y5 R10 real bound curve acquisition and alpha-row smoke runner

Status: `Y5_R10_real_bound_anchor_staged_nonclaim_smoke_runner_blocks_claim`  
Claim ceiling: `R10_real_source_anchor_and_smoke_only_no_fifth_force_Newton_PPN_or_local_GR_pass`  
Next target: `564-Y5-R10-full-curve-digitization-or-parent-coefficient-fill.md`

## Verdict
- Real Eot-Wash source-backed anchor points are now staged in a separate non-claim bound file.
- The live claim files are intentionally unchanged and still blocked by the existing runner.
- MTS alpha rows are smoke-only because the parent coefficients are still symbolic.
- This is data plumbing, not a local-GR/R10 pass.

## Bound Source Provenance
| source_id | title | year | source_kind | source_url | doi | extraction_method | confidence_level | data_status | confidence | valid_for_claim | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EOTWASH_2020_PRL124101101 | New Test of the Gravitational 1/r^2 Law at Separations down to 52 um | 2020 | modern_anchor | https://pubmed.ncbi.nlm.nih.gov/32216404/; https://arxiv.org/abs/2002.11761 | 10.1103/PhysRevLett.124.101101 | anchor_only_from_abstract_statement_alpha_equals_1_range_less_than_38.6_um | 95_percent | anchor_only_non_curve | high_for_threshold_anchor_low_for_curve | false | Used only as a source-backed gravitational-strength Yukawa threshold anchor; no figure digitization or machine-readable curve was acquired here. |
| EOTWASH_2007_PRL98021101 | Tests of the Gravitational Inverse-Square Law below the Dark-Energy Length Scale | 2007 | continuity_anchor | https://arxiv.org/abs/hep-ph/0611184 | 10.1103/PhysRevLett.98.021101 | anchor_only_from_abstract_statement_abs_alpha_le_1_down_to_lambda_56_um | 95_percent | anchor_only_non_curve | high_for_threshold_anchor_low_for_curve | false | Used only as an older Eot-Wash threshold continuity anchor; not a digitized alpha(lambda) curve. |
| ADELBERGER_HECKEL_NELSON_2003_REVIEW | Tests of the Gravitational Inverse-Square Law | 2003 | review_context | https://arxiv.org/abs/hep-ph/0307284 | 10.1146/annurev.nucl.53.041002.110503 | review_context_only_no_numeric_rows_extracted | not_a_new_threshold_row | review_context_no_curve | high_for_source_hierarchy_low_for_numeric_curve | false | Recorded for continuity with the existing placeholder source hierarchy; no numeric bound row is created from this review in checkpoint 563. |

## Anchor Bound Rows
| bound_id | dataset_id | lambda_value | lambda_units | alpha_bound | alpha_bound_source | digitization_method | source_file | valid_for_claim | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R10_ANCHOR_EOTWASH_2020_ALPHA1_38P6UM | Lee_Adelberger_Cook_Fleischer_Heckel_2020_PRL124101101 | 3.86e-5 | m | 1.0 | https://pubmed.ncbi.nlm.nih.gov/32216404/; https://arxiv.org/abs/2002.11761; doi:10.1103/PhysRevLett.124.101101 | anchor_only_non_curve_from_alpha_equals_1_threshold_statement | https://arxiv.org/abs/2002.11761 | false | Modern source-backed anchor only: gravitational-strength Yukawa interactions limited to ranges below 38.6 um at 95 percent confidence; not a full alpha(lambda) curve. |
| R10_ANCHOR_EOTWASH_2007_ALPHA1_56UM | Kapner_Cook_Adelberger_Gundlach_Heckel_Hoyle_Swanson_2007_PRL98021101 | 5.6e-5 | m | 1.0 | https://arxiv.org/abs/hep-ph/0611184; doi:10.1103/PhysRevLett.98.021101 | anchor_only_non_curve_from_abs_alpha_le_1_threshold_statement | https://arxiv.org/abs/hep-ph/0611184 | false | Continuity anchor only: inverse-square law holds with abs(alpha)<=1 down to lambda=56 um at 95 percent confidence; not a full alpha(lambda) curve. |

## MTS Smoke Rows
| model_id | branch_id | curve_id | lambda_value | lambda_units | alpha_predicted | alpha_bound | alpha_bound_source | force_law_form | derivation_status | formula_reference | source_file | assumptions | valid_for_claim | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_source_normalized_Newton_branch | R10_symbolic_parent_prefactor_smoke | R10_alpha_lambda_curve_MTS_SMOKE_NONCLAIM | 3.86e-5 | m | K_X*Qbar_XH(lambda_X)*qbar_XT/(4*pi*Z_X*G_obs) | 1.0 | source-intake/local_bounds/R10_alpha_lambda_bound_curve_ANCHOR_SMOKE.csv::R10_ANCHOR_EOTWASH_2020_ALPHA1_38P6UM | Yukawa_potential_and_acceleration_ratio | symbolic_prefactor_nonclaim_smoke_parent_coefficients_absent | 562-Y5-R10-ZX-lambda-mass-gap-and-bound-curve-fill-or-theorem-zero.md::alpha_X(lambda)=K_X Qbar_XH(lambda) qbar_XT | 562-Y5-R10-ZX-lambda-mass-gap-and-bound-curve-fill-or-theorem-zero.md | Z_X,M_X_squared,numerator_coefficients,source_paths_not_numeric_or_parent_derived | false | Schema and unit smoke row only; alpha is intentionally symbolic and must remain invalid for claim scoring. |
| MTS_source_normalized_Newton_branch | R10_symbolic_parent_prefactor_smoke | R10_alpha_lambda_curve_MTS_SMOKE_NONCLAIM | 5.6e-5 | m | K_X*Qbar_XH(lambda_X)*qbar_XT/(4*pi*Z_X*G_obs) | 1.0 | source-intake/local_bounds/R10_alpha_lambda_bound_curve_ANCHOR_SMOKE.csv::R10_ANCHOR_EOTWASH_2007_ALPHA1_56UM | Yukawa_potential_and_acceleration_ratio | symbolic_prefactor_nonclaim_smoke_parent_coefficients_absent | 562-Y5-R10-ZX-lambda-mass-gap-and-bound-curve-fill-or-theorem-zero.md::lambda_X=sqrt(Z_X/M_X^2) | 562-Y5-R10-ZX-lambda-mass-gap-and-bound-curve-fill-or-theorem-zero.md | Z_X,M_X_squared,numerator_coefficients,source_paths_not_numeric_or_parent_derived | false | Second anchor-aligned smoke row; remains non-claim because parent coefficients are not sourced. |

## Acquisition Ledger
| item | requested | method | status | result | next_action |
| --- | --- | --- | --- | --- | --- |
| full_2020_Eot_Wash_alpha_lambda_curve | true | web_metadata_and_abstract_anchor_review | not_acquired | threshold anchor found; no full digitized curve extracted | digitize PRL 2020 bound figure or locate machine-readable supplementary table |
| older_2007_Eot_Wash_alpha_lambda_anchor | true | arxiv_metadata_and_abstract_anchor_review | anchor_acquired_noncurve | abs(alpha)<=1 down to lambda=56um recorded as anchor-only row | use only for continuity unless full curve points are digitized |
| 2003_Adelberger_review_continuity | true | arxiv_metadata_review | recorded_no_numeric_row | review source recorded in provenance, no bound row created | digitize review plots only if needed for historical comparison, not modern claim |

## Runner Summary
| runner_id | mts_curve | bound_curve | mts_rows | valid_mts_rows | bound_rows | valid_bound_rows | comparison_rows | passed_rows | blocked_or_failed_rows | R10_pass_for_claim | claim_allowed | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R10_RUNNER_563_LIVE_PLACEHOLDER_RECHECK | source-intake/mts_residuals/R10_alpha_lambda_curve_MTS_source_normalization.csv | source-intake/local_bounds/R10_alpha_lambda_bound_curve_DIGITIZED.csv | 2 | 0 | 2 | 0 | 1 | 0 | 1 | False | False | existing runner result; false is required at checkpoint 563 |
| R10_RUNNER_563_ANCHOR_SMOKE_RECHECK | source-intake/mts_residuals/R10_alpha_lambda_curve_MTS_SMOKE_NONCLAIM.csv | source-intake/local_bounds/R10_alpha_lambda_bound_curve_ANCHOR_SMOKE.csv | 2 | 0 | 2 | 0 | 1 | 0 | 1 | False | False | existing runner result; false is required at checkpoint 563 |
| R10_NONCLAIM_ANCHOR_INTERPOLATION_DRY_CHECK | source-intake/mts_residuals/R10_alpha_lambda_curve_MTS_SMOKE_NONCLAIM.csv | source-intake/local_bounds/R10_alpha_lambda_bound_curve_ANCHOR_SMOKE.csv | 2 | 0 | 2 | 0 | 0 | 0 | 0 | False | False | pass_nonclaim: R10_ANCHOR_EOTWASH_2020_ALPHA1_38P6UM->R10_ANCHOR_EOTWASH_2007_ALPHA1_56UM;lambda_mid=4.649301e-05;alpha_mid=1.000000e+00 |

## Evaluator
| criterion_id | criterion | result | claim_impact |
| --- | --- | --- | --- |
| E563_0_real_source_anchor_started | Real Eot-Wash source hierarchy is recorded with DOI/URL/year/provenance. | pass | source plumbing improved; no R10 claim |
| E563_1_full_curve_missing | Full alpha(lambda) curve must be digitized or table-sourced before claim scoring. | blocked | anchor-only rows are not enough for R10/local-GR pass |
| E563_2_mts_parent_coefficients_missing | MTS alpha rows require Z_X, M_X^2, numerator coefficients, and source-backed formula paths. | blocked | symbolic smoke rows remain non-claim |
| E563_3_live_runner_blocks | Existing comparator must keep live placeholder files blocked. | pass | guardrail intact |
| E563_4_smoke_runner_blocks | Candidate/smoke files must validate failure modes and still block claims. | pass | guardrail intact |
| E563_5_nonclaim_interpolation_smoke | Positive numeric anchors can be log-interpolated only as a non-claim plumbing dry check. | pass | interpolation plumbing checked without promoting anchors |

## Blocker Ledger
| blocker_id | blocker | why_it_matters | next_action | claim_blocked |
| --- | --- | --- | --- | --- |
| B563_0_no_full_bound_curve | Only alpha=1 threshold anchors were staged; there is no dense alpha(lambda) curve. | R10 scoring needs bound strength at the MTS predicted lambda, not a single threshold sentence. | digitize 2020 PRL figure points or locate official machine-readable curve data | true |
| B563_1_no_numeric_MTS_alpha | MTS alpha rows remain symbolic because Z_X, M_X^2, K_X, Qbar_XH, and qbar_XT are not numerically parent-sourced. | The comparator cannot test abs(alpha_predicted)<=alpha_bound without numeric alpha(lambda). | derive theorem-zero source silence or fill source-backed parent coefficients | true |
| B563_2_anchor_rows_nonclaim_by_design | Anchor rows are valid evidence provenance but invalid claim rows. | A threshold anchor can guide the next data pass but cannot replace a conservative bound curve. | promote only after full-curve extraction and independent validation | true |

## Decision
| decision_id | status | decision | rationale | next_target |
| --- | --- | --- | --- | --- |
| D563_0_checkpoint_status | Y5_R10_real_bound_anchor_staged_nonclaim_smoke_runner_blocks_claim | stage source-backed anchors and smoke alpha rows only | real sources improve plumbing, but every claim gate remains deliberately closed | 564-Y5-R10-full-curve-digitization-or-parent-coefficient-fill.md |
| D563_1_claim_ceiling | R10_real_source_anchor_and_smoke_only_no_fifth_force_Newton_PPN_or_local_GR_pass | do not claim R10/local-GR pass | full bound curve and parent-derived MTS alpha are both absent | 564-Y5-R10-full-curve-digitization-or-parent-coefficient-fill.md |

## Source Register
| source_file | role | exists |
| --- | --- | --- |
| 562-Y5-R10-ZX-lambda-mass-gap-and-bound-curve-fill-or-theorem-zero.md | immediate upstream R10 lambda/prefactor gate | True |
| source-intake/mts_residuals/P8_Y5_BRR545_562_VALIDATION.csv | upstream validation confirming placeholder claim remains blocked | True |
| source-intake/mts_residuals/P8_Y5_R10_BOUND_CURVE_DIGITIZATION_CONTRACT.csv | accepted contract for real bound curve rows | True |
| source-intake/mts_residuals/P8_Y5_R10_ZX_LAMBDA_PREFACtOR_FORMULA_REGISTER.csv | conditional alpha(lambda) prefactor relation from 562 | True |
| source-intake/mts_residuals/R10_alpha_lambda_curve_MTS_source_normalization.csv | live MTS placeholder curve kept unchanged | True |
| source-intake/local_bounds/R10_alpha_lambda_bound_curve_DIGITIZED.csv | live bound placeholder file kept unchanged | True |
| source-intake/local_bounds/local_bound_claims.csv | symbolic local-bound source hierarchy manifest | True |
| scripts/R10_alpha_lambda_bound_prediction_runner.py | existing R10 comparator reused without changing claim logic | True |
| scripts/Y5_R10_real_bound_curve_acquisition_and_alpha_row_smoke_runner.py | this private checkpoint generator | True |

## Validation
| check_id | result | detail |
| --- | --- | --- |
| V563_0_source_paths_exist | pass | missing=0 |
| V563_1_prior_562_clean | pass | prior_validation_rows=10;prior_fails=0 |
| V563_2_provenance_sources_recorded | pass | provenance_rows=3;urls_recorded=True |
| V563_3_anchor_bound_rows_numeric_nonclaim | pass | anchor_rows=2;issues=none |
| V563_4_mts_smoke_rows_symbolic_nonclaim | pass | smoke_rows=2;issues=none |
| V563_5_live_runner_blocks_placeholders | pass | valid_mts=0;valid_bound=0;R10_pass=False |
| V563_6_smoke_runner_blocks_nonclaim | pass | valid_mts=0;valid_bound=0;R10_pass=False |
| V563_7_nonclaim_interpolation_dry_check | pass | status=pass_nonclaim |
| V563_8_live_files_not_overwritten | pass | live_bound_rows=2;live_mts_rows=2 |
| V563_9_no_claim_rows | pass | claim_rows=0 |
| V563_10_no_overclaim | pass | R10_pass=false;Newton=false;PPN=false;local_GR=false;anchor_only=true;parent_alpha_numeric=false |

## Route Update
| route_id | current_state | next_gate | success_condition |
| --- | --- | --- | --- |
| RU563_0_data_route | anchor_only_noncurve_source_backed | full_curve_digitization | dense positive numeric lambda_value and alpha_bound rows with valid_for_claim=true only after provenance and extraction checks |
| RU563_1_theory_route | symbolic_MTS_alpha_nonclaim | parent_coefficient_or_theorem_zero | derive/source Z_X, M_X^2, numerator coefficients, and formula source paths, or prove no-range theorem-zero |

## Private Readout
This checkpoint improves the R10 evidence plumbing but keeps the physics gate shut. The right next move is either a real digitized bound curve or a parent-derived/theorem-zero MTS alpha row; anything weaker would be dressing a placeholder up as evidence, and we are not doing that.
