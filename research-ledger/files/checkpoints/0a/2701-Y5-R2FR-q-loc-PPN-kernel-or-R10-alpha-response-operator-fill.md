# 2701: q_loc PPN Kernel Or R10 alpha(lambda) Response Operator Fill

**Branch:** `Y5_R2FR_Q_LOC_PPN_KERNEL_OR_R10_ALPHA_RESPONSE_OPERATOR_FILL_2701`

## Private Verdict

2701 does the useful testing move. The PPN kernel is too underdetermined because the metric response, source frame, and q_loc profile are all missing. The R10 route is cleaner: compare the q_loc radial acceleration to the Yukawa acceleration ratio alpha(1+r/lambda)exp(-r/lambda). This creates a real alpha(lambda) operator, but it remains strictly nonclaim until q_loc(r,lambda), source normalization, and a full alpha-bound curve exist.

## PPN Kernel Audit

| audit_id | object | mathematical_form | requirement | evidence | status | valid_for_claim | claim_allowed | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PPN2701_0_input | PPN response target | Delta_PPN_GK^a = integral K_PPN^a{}_nu q_loc^nu dV | requires metric perturbation response, source normalization, q_loc profile and observed frame | from 2700 operator row | TOO_UNDERDETERMINED | false | false | 2026-06-23T08:36:25.807019+00:00 |
| PPN2701_1_metric_response | metric response matrix | delta g_obs / delta q_loc or delta g_obs / delta T_GK | required to know whether q_loc sources gamma,beta,alpha_i,zeta_i,xi | QLOC2699_6_readout says metric response matrix missing | MISSING | false | false | 2026-06-23T08:36:25.807024+00:00 |
| PPN2701_2_source_frame | source-normalized frame | same M_eff/H_tau/Pi_M source map before PPN readout | otherwise q_loc projection can hide source-measure residuals | 2700 missing inputs include source_normalization_map | MISSING | false | false | 2026-06-23T08:36:25.807027+00:00 |
| PPN2701_3_profile | q_loc radial/source profile | q_loc^nu(r,source,frame,lambda) | PPN kernel cannot be evaluated without profile support and dimensions | QLOC2581 rows have MISSING_NUMERIC_VALUE | MISSING | false | false | 2026-06-23T08:36:25.807030+00:00 |
| PPN2701_4_verdict | PPN kernel derivation status | K_PPN cannot be derived from current inputs | fallback to R10 alpha(lambda) operator because the Yukawa acceleration-ratio form is explicit | NEXT2700 allows R10 fallback | PPN_KERNEL_REJECTED_FOR_NOW | false | false | 2026-06-23T08:36:25.807033+00:00 |

## R10 alpha(lambda) Response Operator

| operator_id | arena | input_residual | operator_symbol | force_law_reference | response_formula | conservative_envelope | input_units | output_units | source_paths | claim_status | score_ready | valid_for_claim | claim_allowed | notes | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R10OP2701_0_QLOC_YUKAWA_ALPHA_RESPONSE | R10_short_range | q_loc_radial_acceleration_profile | R_R10_alpha[q_loc;lambda,r_window,source] | a_Y/a_N = alpha(lambda)*(1+r/lambda)*exp(-r/lambda) | alpha_q(lambda;r)=a_q(r,lambda)/a_N(r)*exp(r/lambda)/(1+r/lambda) | abs_alpha_q(lambda)=sup_{r in window}\|a_q(r,lambda)/a_N(r)\|*exp(r/lambda)/(1+r/lambda) | a_q in m s^-2 or dimensionless a_q/a_N after source normalization | dimensionless alpha(lambda) | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2700-Y5-R2FR-Gamma-eff-candidate-metric-response-or-first-q-loc-response-row.md;D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\563-Y5-R10-real-bound-curve-acquisition-and-alpha-row-smoke-runner.md;D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2206-Y5-R2FR-GammaKhat-q-loc-parent-action-signature-or-official-residual-demotion.md;D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2581-Y5-R2FR-GammaKhat-q_loc-coupling-double-zero-or-residual-lock.md | SCHEMA_ONLY_NONCLAIM | false | false | false | This maps q_loc to the same alpha(lambda) language used by inverse-square-law tests, but it needs a source-backed q_loc profile, source mass and full bound curve before scoring. | 2026-06-23T08:36:25.807100+00:00 |
| R10OP2701_1_QLOC_FORCE_DENSITY_CONVERSION | R10_short_range | q_loc_force_density_or_stress_divergence | a_q=q_loc/rho_test or q_loc/m_test after matter-frame normalization | convert residual force density to test-body acceleration before alpha projection | alpha_q(lambda;r)=q_loc^r(r,lambda)/(rho_test*a_N(r))*exp(r/lambda)/(1+r/lambda) | use absolute component envelope with no cancellation between q_loc defects | force_density N m^-3 or acceleration m s^-2 after normalization | dimensionless alpha(lambda) | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2700-Y5-R2FR-Gamma-eff-candidate-metric-response-or-first-q-loc-response-row.md;D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\563-Y5-R10-real-bound-curve-acquisition-and-alpha-row-smoke-runner.md;D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2206-Y5-R2FR-GammaKhat-q-loc-parent-action-signature-or-official-residual-demotion.md;D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2581-Y5-R2FR-GammaKhat-q_loc-coupling-double-zero-or-residual-lock.md | UNIT_CONVERSION_SCHEMA_ONLY | false | false | false | The rho_test/m_test normalization is the live missing source-frame input; this row prevents silently comparing incompatible units. | 2026-06-23T08:36:25.807105+00:00 |

## R10 Smoke Rows

| row_id | lambda_value | lambda_units | alpha_predicted | alpha_bound_anchor | bound_reference | bound_status | score_ready | valid_for_claim | claim_allowed | notes | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R10SMOKE2701_0_2020_anchor | 3.86e-5 | m | alpha_q(lambda;r)=MISSING_QLOC_PROFILE_TO_ALPHA | 1.0 | R10_ANCHOR_EOTWASH_2020_ALPHA1_38P6UM | anchor_only_non_curve | false | false | false | Smoke row only: alpha prediction is a formula slot, not a number; anchor bound is not a digitized curve. | 2026-06-23T08:36:25.807109+00:00 |
| R10SMOKE2701_1_2007_anchor | 5.6e-5 | m | alpha_q(lambda;r)=MISSING_QLOC_PROFILE_TO_ALPHA | 1.0 | R10_ANCHOR_EOTWASH_2007_ALPHA1_56UM | anchor_only_non_curve | false | false | false | Smoke row only: alpha prediction is a formula slot, not a number; anchor bound is not a digitized curve. | 2026-06-23T08:36:25.807113+00:00 |

## Missing Inputs

| missing_id | input | purpose | why_required | status | source_backed | score_ready | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MISS2701_0_q_loc_profile | q_loc^r(r,lambda,source,frame) | radial acceleration or force-density profile | required to calculate alpha_q(lambda) | MISSING_PROFILE | false | false | false | 2026-06-23T08:36:25.807117+00:00 |
| MISS2701_1_source_mass | M_source or a_N(r)=G M_source/r^2 | source-normalized Newtonian acceleration | required denominator for alpha ratio | MISSING_SOURCE_MEASURE_LOCK | false | false | false | 2026-06-23T08:36:25.807120+00:00 |
| MISS2701_2_test_body_normalization | rho_test or m_test map | convert force density/stress divergence to test acceleration | required if q_loc is not already acceleration | MISSING_MATTER_FRAME_NORMALIZATION | false | false | false | 2026-06-23T08:36:25.807123+00:00 |
| MISS2701_3_range_kernel | lambda dependence of q_loc | project q_loc onto Yukawa range lambda | required to sample alpha(lambda) | MISSING_RANGE_KERNEL | false | false | false | 2026-06-23T08:36:25.807126+00:00 |
| MISS2701_4_bound_curve | full alpha_bound(lambda) curve | dense or interpolable source-backed bound rows | required for claim scoring | MISSING_FULL_DIGITIZED_BOUND_CURVE | false | false | false | 2026-06-23T08:36:25.807128+00:00 |
| MISS2701_5_anchor_policy | anchor-only nonclaim policy | do not treat alpha=1 threshold anchors as full curve | prevents false R10 pass | ANCHORS_NONCLAIM_ONLY | false | false | false | 2026-06-23T08:36:25.807130+00:00 |
| MISS2701_6_no_cancellation | absolute q_loc component envelope | sum/bound residual components without cancellation credit | required for conservative local tests | MISSING_COMPONENT_VALUES | false | false | false | 2026-06-23T08:36:25.807133+00:00 |

## Bound Asset Status

| asset_id | asset_path_or_name | status | detail | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- |
| BOUND2701_0_live_digitized | source-intake/local_bounds/R10_alpha_lambda_bound_curve_DIGITIZED.csv | placeholder_invalid | MISSING_NUMERIC_LAMBDA and missing digitized alpha_bound rows | false | 2026-06-23T08:36:25.807137+00:00 |
| BOUND2701_1_anchor_smoke | source-intake/local_bounds/R10_alpha_lambda_bound_curve_ANCHOR_SMOKE.csv | anchor_only_non_curve | two positive Eot-Wash threshold anchors useful for smoke plumbing only | false | 2026-06-23T08:36:25.807139+00:00 |
| BOUND2701_2_mts_smoke | source-intake/mts_residuals/R10_alpha_lambda_curve_MTS_SMOKE_NONCLAIM.csv | symbolic_nonclaim | alpha_predicted uses symbolic parent coefficients, not numeric q_loc/R10 projection | false | 2026-06-23T08:36:25.807142+00:00 |
| BOUND2701_3_required | future_full_curve_or_table | missing | full digitized or machine-readable alpha(lambda) curve needed before claim scoring | false | 2026-06-23T08:36:25.807145+00:00 |

## Source Register

| source_id | relative_path | absolute_path | exists | required_needles | found_needles | missing_needles | purpose | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SRC2701_2700_NEXT | 2700-Y5-R2FR-Gamma-eff-candidate-metric-response-or-first-q-loc-response-row.md | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2700-Y5-R2FR-Gamma-eff-candidate-metric-response-or-first-q-loc-response-row.md | true | QOP2700_0_PPN_GK_q_loc_response_operator;MISS2700_0_K_PPN_kernel;NEXT2700_0_selected;VAL2700_OVERALL | QOP2700_0_PPN_GK_q_loc_response_operator;MISS2700_0_K_PPN_kernel;NEXT2700_0_selected;VAL2700_OVERALL |  | imports the staged PPN operator row and selected 2701 target | false | 2026-06-23T08:36:25.804411+00:00 |
| SRC2701_2206_APQ | 2206-Y5-R2FR-GammaKhat-q-loc-parent-action-signature-or-official-residual-demotion.md | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2206-Y5-R2FR-GammaKhat-q-loc-parent-action-signature-or-official-residual-demotion.md | true | APQ2206_0_PPN;APQ2206_1_R10;QDEM2206_9_total | APQ2206_0_PPN;APQ2206_1_R10;QDEM2206_9_total |  | imports q_loc PPN/R10 projection queue and total residual | false | 2026-06-23T08:36:25.804896+00:00 |
| SRC2701_2581_TESTS | 2581-Y5-R2FR-GammaKhat-q_loc-coupling-double-zero-or-residual-lock.md | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2581-Y5-R2FR-GammaKhat-q_loc-coupling-double-zero-or-residual-lock.md | true | TEST2581_0_PPN_alpha;TEST2581_1_R10;QLOC2581_TOTAL | TEST2581_0_PPN_alpha;TEST2581_1_R10;QLOC2581_TOTAL |  | imports official q_loc local-test residual interface | false | 2026-06-23T08:36:25.805337+00:00 |
| SRC2701_563_R10 | 563-Y5-R10-real-bound-curve-acquisition-and-alpha-row-smoke-runner.md | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\563-Y5-R10-real-bound-curve-acquisition-and-alpha-row-smoke-runner.md | true | E563_1_full_curve_missing;E563_2_mts_parent_coefficients_missing;V563_10_no_overclaim | E563_1_full_curve_missing;E563_2_mts_parent_coefficients_missing;V563_10_no_overclaim |  | imports R10 bound/source-plumbing status and no-claim ceiling | false | 2026-06-23T08:36:25.805768+00:00 |
| SRC2701_BOUND_ANCHORS | source-intake/local_bounds/R10_alpha_lambda_bound_curve_ANCHOR_SMOKE.csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\R10_alpha_lambda_bound_curve_ANCHOR_SMOKE.csv | true | R10_ANCHOR_EOTWASH_2020_ALPHA1_38P6UM;R10_ANCHOR_EOTWASH_2007_ALPHA1_56UM | R10_ANCHOR_EOTWASH_2020_ALPHA1_38P6UM;R10_ANCHOR_EOTWASH_2007_ALPHA1_56UM |  | imports nonclaim Eot-Wash anchor rows for smoke checks only | false | 2026-06-23T08:36:25.806183+00:00 |
| SRC2701_LIVE_BOUND_PLACEHOLDER | source-intake/local_bounds/R10_alpha_lambda_bound_curve_DIGITIZED.csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\R10_alpha_lambda_bound_curve_DIGITIZED.csv | true | R10_BOUND_PLACEHOLDER_0;MISSING_NUMERIC_LAMBDA | R10_BOUND_PLACEHOLDER_0;MISSING_NUMERIC_LAMBDA |  | imports live placeholder bound curve that remains invalid for claim scoring | false | 2026-06-23T08:36:25.806585+00:00 |
| SRC2701_R10_PREFACTOR | source-intake/mts_residuals/P8_Y5_R10_ZX_LAMBDA_PREFACtOR_FORMULA_REGISTER.csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_ZX_LAMBDA_PREFACtOR_FORMULA_REGISTER.csv | true | PR562_4_prefactor;PR562_6_spectral_generalization | PR562_4_prefactor;PR562_6_spectral_generalization |  | imports earlier Yukawa alpha(lambda) prefactor grammar for comparison | false | 2026-06-23T08:36:25.807008+00:00 |

## Claim Gates

| claim_gate_id | gate | status | gate_passed | claim_allowed | reason | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- |
| CG2701_0_PPN_kernel | PPN response kernel is derived | BLOCKED_NONCLAIM | false | false | metric response, source frame and q_loc profile are missing | 2026-06-23T08:36:25.807148+00:00 |
| CG2701_1_R10_operator | R10 alpha(lambda) response operator exists | PASS_SCHEMA_ONLY | true | false | operator formula is written but not score-ready | 2026-06-23T08:36:25.807151+00:00 |
| CG2701_2_R10_profile | q_loc alpha(lambda) prediction is numeric | BLOCKED_NONCLAIM | false | false | q_loc profile/range/source normalization missing | 2026-06-23T08:36:25.807154+00:00 |
| CG2701_3_bound_curve | R10 bound curve is claim-valid | BLOCKED_NONCLAIM | false | false | only placeholder plus anchor-only rows exist | 2026-06-23T08:36:25.807157+00:00 |
| CG2701_4_R10_pass | R10/fifth-force pass can be claimed | BLOCKED_NONCLAIM | false | false | prediction and bound are not valid_for_claim | 2026-06-23T08:36:25.807159+00:00 |
| CG2701_5_local_GR | local GR/Newton can be claimed | BLOCKED_NONCLAIM | false | false | q_loc remains finite residual and unbounded | 2026-06-23T08:36:25.807162+00:00 |
| CG2701_6_public | public/GitHub readiness | BLOCKED_PRIVATE_WORK | false | false | private derivation/test plumbing only | 2026-06-23T08:36:25.807164+00:00 |

## Decisions

| decision_id | decision | rationale | next_action | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- |
| DEC2701_0_PPN | PPN_KERNEL_REJECTED_FOR_NOW | current data cannot derive K_PPN without metric response, source frame and q_loc profile | do not pretend PPN can be scored | false | 2026-06-23T08:36:25.807167+00:00 |
| DEC2701_1_R10 | R10_ALPHA_OPERATOR_WRITTEN | Yukawa acceleration ratio gives a clean alpha(lambda) response operator for q_loc | use this as the first executable local-bound projection grammar | false | 2026-06-23T08:36:25.807170+00:00 |
| DEC2701_2_nonclaim | R10_REMAINS_NONCLAIM | operator has no profile and bound assets are placeholder/anchor-only | keep all valid_for_claim=false | false | 2026-06-23T08:36:25.807173+00:00 |
| DEC2701_3_next | QLOC_PROFILE_OR_FULL_BOUND_CURVE_NEXT | the next real move is either source a q_loc radial/range profile or digitize the full Eot-Wash curve | run 2702 | false | 2026-06-23T08:36:25.807175+00:00 |

## Next Target

| next_id | selection | target_doc | target_script | task | success_condition | forbidden_shortcuts | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NEXT2701_0_selected | selected_primary | 2702-Y5-R2FR-q-loc-radial-profile-or-R10-bound-curve-digitization-input.md | scripts/Y5_R2FR_q_loc_radial_profile_or_R10_bound_curve_digitization_input_2702.py | try to source or derive the q_loc radial/range profile needed for alpha_q(lambda); if unavailable, stage the full R10 bound-curve digitization input contract without claiming a pass | either q_loc profile/range/source-normalization inputs become source-backed nonclaim rows, or full-bound-curve digitization requirements are made executable with no placeholder scoring | score anchor-only rows; invent q_loc profile; treat symbolic alpha as numeric; claim R10/local GR; GitHub action; formalization-workbench edits | false | 2026-06-23T08:36:25.807178+00:00 |

## Project Status

| status_id | topic | status | meaning | next_action | claim_allowed | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- |
| STATUS2701_0_q_loc | q_loc testing | R10_OPERATOR_EXISTS_NONCLAIM | q_loc can now be expressed in alpha(lambda) language if a profile exists | derive/source profile next | false | 2026-06-23T08:36:25.807181+00:00 |
| STATUS2701_1_PPN | PPN kernel | HELD_UNTIL_METRIC_RESPONSE | PPN is too broad until metric response/source frame is signed | do not score | false | 2026-06-23T08:36:25.807187+00:00 |
| STATUS2701_2_R10 | short-range tests | OPERATOR_READY_INPUTS_MISSING | operator is cleaner than PPN but still lacks profile and full bound curve | 2702 profile or bound curve | false | 2026-06-23T08:36:25.807190+00:00 |
| STATUS2701_3_local_GR | local GR/Newton | STILL_BLOCKED_BUT_MORE_TESTABLE | we moved from abstract residual to a concrete local-bound projection grammar | fill inputs | false | 2026-06-23T08:36:25.807192+00:00 |
| STATUS2701_4_public | public/GitHub | NO_ACTION_PRIVATE | private nonclaim checkpoint only | keep private | false | 2026-06-23T08:36:25.807194+00:00 |

## Validation

| check_id | passed | detail | timestamp_utc |
| --- | --- | --- | --- |
| VAL2701_0_sources_exist | true | all cited source paths exist | 2026-06-23T08:36:25.911055+00:00 |
| VAL2701_1_needles_found | true | all required source needles were found | 2026-06-23T08:36:25.911067+00:00 |
| VAL2701_2_csv_parse | true | all generated CSVs and branch copies parse with at least one row | 2026-06-23T08:36:25.911070+00:00 |
| VAL2701_3_ppn_rejected | true | PPN kernel derivation is explicitly rejected for current inputs | 2026-06-23T08:36:25.911073+00:00 |
| VAL2701_4_r10_operator_present | true | R10 alpha(lambda) response operator exists with units and nonclaim status | 2026-06-23T08:36:25.911076+00:00 |
| VAL2701_5_smoke_nonclaim | true | anchor-aligned smoke rows remain nonclaim and nonscoreable | 2026-06-23T08:36:25.911078+00:00 |
| VAL2701_6_missing_inputs_recorded | true | q_loc profile/source/bound inputs are explicit | 2026-06-23T08:36:25.911081+00:00 |
| VAL2701_7_bound_assets_nonclaim | true | bound assets remain nonclaim | 2026-06-23T08:36:25.911084+00:00 |
| VAL2701_8_no_claims | true | all claim gates keep claim_allowed=false | 2026-06-23T08:36:25.911087+00:00 |
| VAL2701_9_next_2702 | true | 2702 q_loc profile or bound-curve target selected | 2026-06-23T08:36:25.911089+00:00 |
| VAL2701_10_no_formalization_outputs | true | no output path points into formalization-workbench | 2026-06-23T08:36:25.911092+00:00 |
| VAL2701_11_no_github_outputs | true | no GitHub/public-output path was written | 2026-06-23T08:36:25.911094+00:00 |
| VAL2701_PARSE_source_register | true | parsed; rows=7 | 2026-06-23T08:36:25.911099+00:00 |
| VAL2701_PARSE_ppn_kernel_audit | true | parsed; rows=5 | 2026-06-23T08:36:25.911103+00:00 |
| VAL2701_PARSE_r10_operator | true | parsed; rows=2 | 2026-06-23T08:36:25.911106+00:00 |
| VAL2701_PARSE_r10_smoke_rows | true | parsed; rows=2 | 2026-06-23T08:36:25.911109+00:00 |
| VAL2701_PARSE_missing_inputs | true | parsed; rows=7 | 2026-06-23T08:36:25.911112+00:00 |
| VAL2701_PARSE_bound_asset_status | true | parsed; rows=4 | 2026-06-23T08:36:25.911115+00:00 |
| VAL2701_PARSE_claim_gates | true | parsed; rows=7 | 2026-06-23T08:36:25.911118+00:00 |
| VAL2701_PARSE_decision_ledger | true | parsed; rows=4 | 2026-06-23T08:36:25.911120+00:00 |
| VAL2701_PARSE_next_target | true | parsed; rows=1 | 2026-06-23T08:36:25.911124+00:00 |
| VAL2701_PARSE_project_status | true | parsed; rows=5 | 2026-06-23T08:36:25.911126+00:00 |
| VAL2701_PARSE_branch_copies | true | parsed; rows=5 | 2026-06-23T08:36:25.911130+00:00 |
| VAL2701_PARSE_local_r10_operator | true | parsed; rows=2 | 2026-06-23T08:36:25.911132+00:00 |
| VAL2701_PARSE_local_r10_smoke | true | parsed; rows=2 | 2026-06-23T08:36:25.911140+00:00 |
| VAL2701_PARSE_wep_r10_operator | true | parsed; rows=2 | 2026-06-23T08:36:25.911143+00:00 |
| VAL2701_PARSE_source_weight_r10_operator | true | parsed; rows=2 | 2026-06-23T08:36:25.911147+00:00 |
| VAL2701_PARSE_rab_next | true | parsed; rows=1 | 2026-06-23T08:36:25.911150+00:00 |
| VAL2701_OVERALL | true | 2701 rejects the underdetermined q_loc-to-PPN kernel, writes the R10 Yukawa alpha(lambda) response operator, keeps smoke rows nonclaim, and selects q_loc profile or full bound-curve input next | 2026-06-23T08:36:25.911157+00:00 |
