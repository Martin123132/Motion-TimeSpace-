# 1503 - Matter Coupling Normalization from Newton Limit or Closure Bound

## Verdict
- The Newton limit fixes the common measured inverse-square normalization, not a finite-range Yukawa amplitude.
- A direct R10 matter coupling is zero only if the parent action proves observed-coframe independence from the residual field.
- Otherwise beta_a s_a / Z_a remains an explicit closure-bound input; no C_parent import or R10/local-GR claim is made.

## Newton Limit Coupling Audit
| audit_id | object | formula | status | derived_or_calibrated |
| --- | --- | --- | --- | --- |
| NL1503_0_standard_limit | observed Newton limit | a_N=-G_N M/r^2 | DERIVED_STANDARD_INPUT | True |
| NL1503_1_common_rescaling | universal massless rescaling | G_parent -> G_N = G_parent(1+epsilon_common) | CALIBRATION_ONLY | True |
| NL1503_2_finite_range_residual | finite-range residual force | delta a/a_N = alpha_a(1+r/lambda_a)exp(-r/lambda_a) | NOT_FIXED_BY_NEWTON_LIMIT | False |
| NL1503_3_composition_readout | species/source readout | epsilon_A, beta_A, s_A, or C_A | NOT_FIXED_BY_NEWTON_LIMIT | False |
| NL1503_4_same_frame_action | single observed coframe matter action | S_matter=sum_A S_A[Psi_A,e_obs,omega[e_obs],theta_A] | CONDITIONAL_ZERO_ROUTE | False |
| NL1503_5_conformal_readout | if e_obs depends on X_a | e_obs -> exp(beta_a X_a)e_obs | CLOSURE_UNLESS_PARENT_DERIVED | False |
| NL1503_6_verdict | coupling normalization verdict | Newton limit fixes only the common zero-range/massless calibration, not finite alpha(lambda) | NO_UNIQUE_C_FROM_NEWTON_ALONE | False |

## Coupling Theorem
| theorem_id | proof_status | claim_effect |
| --- | --- | --- |
| THM1503_0_no_newton_unique_finite_coupling | DERIVED_AS_NO_GO_FOR_NEWTON_ONLY | C_a cannot be imported from Newton calibration alone |
| THM1503_1_conditional_zero_by_same_frame_independence | EXACT_CONDITIONAL_THEOREM_NOT_PARENT_SIGNED | would give alpha_a=0 for the direct matter readout, but parent coframe-independence is still open |
| THM1503_2_conditional_finite_coupling_formula | CONDITIONAL_TEMPLATE_FORMULA_ONLY | gives exact closure variables, not a claim-grade value |

## Formula Register
| formula_id | formula | status |
| --- | --- | --- |
| FORM1503_0_Newton_calibration | Phi_N=-G_N M/r | measured common calibration only |
| FORM1503_1_finite_Yukawa_potential | delta Phi_a=-G_N M alpha_a exp(-r/lambda_a)/r | R10 convention |
| FORM1503_2_finite_Yukawa_acceleration | delta a/a_N=alpha_a(1+r/lambda_a)exp(-r/lambda_a) | cannot be absorbed into constant G_N |
| FORM1503_3_matter_readout | delta Phi_a=beta_a c^2 X_a | requires parent coframe/readout coefficient beta_a |
| FORM1503_4_point_source_solution | X_a(r)=s_a M exp(-r/lambda_a)/(4 pi Z_a r) | conditional on 1502 Helmholtz template |
| FORM1503_5_alpha_map | alpha_a=-beta_a s_a c^2/(4 pi G_N Z_a) | conditional and unit/sign dependent |
| FORM1503_6_R10_comparison | |sum_a alpha_a tau_R10_a(lambda_i) delta_w_a| <= alpha_bound(lambda_i) | closure-bound comparison only |

## Beta Zero Route
| zero_route_id | required_clause | current_status | effect_if_open |
| --- | --- | --- | --- |
| BZ1503_0_single_coframe | all ordinary matter varies through one e_obs | SUPPORTED_CONTRACT_NOT_PARENT_GLOBAL | beta_a remains explicit closure coefficient |
| BZ1503_1_no_direct_X_vertex | no X_a psi psi, X_a F^2, or source-only scalar matter vertex | POLICY_ONLY_NOT_PARENT_SIGNED | beta_a remains explicit closure coefficient |
| BZ1503_2_local_independence | partial e_obs / partial X_a = 0 at compact local branch | MISSING | beta_a remains explicit closure coefficient |
| BZ1503_3_variation_before_readout | vary parent matter action before arena readout/projection | CONTRACT_ONLY | beta_a remains explicit closure coefficient |
| BZ1503_4_boundary_projection_silence | boundary/readout maps do not reintroduce beta_a | MISSING | beta_a remains explicit closure coefficient |
| BZ1503_5_beta_zero_verdict | beta_a=0 for every R10-active residual component | NOT_PARENT_DERIVED | beta_a remains explicit closure coefficient |

## Closure Bound Row Contract
| field | type | required_value_or_policy | current_status |
| --- | --- | --- | --- |
| schema_version | string | R10_COUPLING_CLOSURE_BOUND_1503 | SCHEMA_ONLY_NONCLAIM |
| same_parent_branch_id | string | MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | SCHEMA_ONLY_NONCLAIM |
| component_id | string | stable residual component id | SCHEMA_ONLY_NONCLAIM |
| lambda_value | positive_float | range in declared units | SCHEMA_ONLY_NONCLAIM |
| lambda_units | string | m or converted unit | SCHEMA_ONLY_NONCLAIM |
| delta_w_a | float_or_derived_zero | residual amplitude | SCHEMA_ONLY_NONCLAIM |
| Z_a | float_or_derived_zero | kinetic normalization | SCHEMA_ONLY_NONCLAIM |
| s_a | float_or_derived_zero | source coupling | SCHEMA_ONLY_NONCLAIM |
| beta_a | float_or_derived_zero | matter readout coefficient | SCHEMA_ONLY_NONCLAIM |
| alpha_predicted | float_or_derived_zero | same-frame Yukawa amplitude | SCHEMA_ONLY_NONCLAIM |
| tau_R10_a | float_or_derived_zero | finite-source geometry response | SCHEMA_ONLY_NONCLAIM |
| alpha_bound | positive_float | reviewed R10 alpha(lambda) bound | SCHEMA_ONLY_NONCLAIM |
| source_paths | path_list | local files/URLs/DOIs for every coefficient | SCHEMA_ONLY_NONCLAIM |
| parent_status | enum | PARENT_DERIVED|DERIVED_ZERO|SOURCE_BACKED_NUMERIC|CLOSURE_NONCLAIM | SCHEMA_ONLY_NONCLAIM |
| valid_for_claim | boolean | false unless all fields are real and sourced | SCHEMA_ONLY_NONCLAIM |

## Validation
| check_id | result | detail |
| --- | --- | --- |
| VAL1503_0_local_sources | PASS | all cited coupling/Newton source paths exist |
| VAL1503_1_newton_no_go | PASS | Newton limit does not determine finite Yukawa coupling |
| VAL1503_2_beta_zero_not_parent | PASS | beta zero route remains unclaimed |
| VAL1503_3_closure_contract | PASS | explicit coupling closure-bound schema written |
| VAL1503_4_live_targets_absent | PASS | live R10 curve/kernel targets remain absent |
| VAL1503_5_Cparent_refused | PASS | C_parent import was not performed |
| VAL1503_6_csv_parse | PASS | all generated 1503 CSVs parse cleanly |
| VAL1503_7_branch_copies | PASS | branch/quarantine nonclaim copies written |
| VAL1503_8_pycache_absent | PASS | scripts __pycache__ absent after run |
| VAL1503_9_formalization_untouched | PASS | formalization modified-file count since start=0 |
| VAL1503_10_claim_flags_false | PASS | all generated prediction/claim flags remain false |
| VAL1503_11_overall | PASS | 1503 rejected Newton-only coupling derivation and converted beta/C into a precise zero-or-bound obligation |

## Next Target
| next_id | next_target | script | objective |
| --- | --- | --- | --- |
| NEXT1503_0_1504 | 1504-Y5-R10-RAB-observed-coframe-independence-beta-zero-or-explicit-coupling-bound.md | scripts/Y5_R10_RAB_observed_coframe_independence_beta_zero_or_explicit_coupling_bound.py | try to prove partial e_obs / partial X_a = 0 in the compact local branch; if not, emit beta_a as an explicit closure-bound input |
