# 1199 - Y5/R10 q_DT to R10 projection or G_res profile source

**Current verdict:** q_DT-to-R10 is now an explicit projection contract, not a slogan. The required object is `W_R10(lambda) q_DT_bound`, normalized against a unit-alpha Yukawa torque/readout signal. No numeric R10 score follows yet.

**Main progress:** the nonclaim 2020 R10 curve can now be joined to sample lambda rows, but every sample remains blocked because `W_R10`, `G_res`, `P_coker`, `B_T`, and `eps_P` are still missing on the MTS side.

**No claim:** no q_loc=0, local-GR, Newton, R10, PPN, WEP, clock, orbital, or public-facing claim follows from this checkpoint.

## Source register

| source_id | relative_path | needle | role | exists | needle_found |
| --- | --- | --- | --- | --- | --- |
| SRC1199_0_1198_next | 1198-Y5-R10-DT-parent-anchor-source-or-first-real-bound-input-fill.md | NEXT1198_0_1199 | direct 1199 handoff. | True | True |
| SRC1199_1_1198_R10_import | 1198-Y5-R10-DT-parent-anchor-source-or-first-real-bound-input-fill.md | QDT1198_0_R10_external_bound_import | nonclaim R10 external curve import. | True | True |
| SRC1199_2_1198_dryrun | 1198-Y5-R10-DT-parent-anchor-source-or-first-real-bound-input-fill.md | DR1198_0_R10_qDT_bound_import_dryrun | R10 dry-run blocked by missing MTS-side inputs. | True | True |
| SRC1199_3_1198_anchor_no_go | 1198-Y5-R10-DT-parent-anchor-source-or-first-real-bound-input-fill.md | DTA1198_5_verdict | D_T natural-boundary anchor no-go. | True | True |
| SRC1199_4_1035_R10_projection | 1035-Y5-R10-KX-green-kernel-normalization-and-profile-integral.md | KXD1035_4_R10_harmonic_projection | R10 harmonic projection contract precedent. | True | True |
| SRC1199_5_1035_harmonic_missing | 1035-Y5-R10-KX-green-kernel-normalization-and-profile-integral.md | KXF1035_3_harmonic | R10 harmonic projection is missing/nonnumeric. | True | True |
| SRC1199_6_437_yukawa | 437-R10-alpha-lambda-executable-curve-contract.md | Yukawa_potential | accepted R10 Yukawa potential convention. | True | True |
| SRC1199_7_437_no_scalar_shortcut | 437-R10-alpha-lambda-executable-curve-contract.md | single_delta_G_scalar | R10 is range-dependent; scalar residual is insufficient. | True | True |
| SRC1199_8_831_bound | 831-Y5-R10-parent-Khat-tensor-operator-or-local-branch-closure.md | RT831_3_bound | q_loc/D_T residual bound by cokernel, boundary, and regularizer. | True | True |
| SRC1199_9_1197_runner | 1197-Y5-R10-DT-boundary-condition-source-or-cokernel-bound-runner.md | CBI1197_1_R10 | R10 q_DT runner input row. | True | True |
| SRC1199_10_R10_candidate | source-intake/local_bounds/R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv | R10_VECTOR_2020_REVIEW_0000 | real numeric external review-candidate curve. | True | True |
| SRC1199_11_1034_projection_blocked | 1034-Y5-R10-alpha-bound-curve-digitization-and-projection-input-pack.md | CGATE1034_2_mts_projection | MTS R10 projection blocked precedent. | True | True |

## R10 projection contract

| contract_id | quantity | contract | mathematical_form | status | missing_for_claim | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| R10P1199_0_observable_convention | alpha_DT(lambda) | Use the same Yukawa convention as the R10 bound curve: V=V_N[1+alpha(lambda) exp(-r/lambda)] or the equivalent acceleration/torque projection. | unit_alpha_signal(lambda)=Pi_R10[Torque[V_N exp(-r/lambda)]]. | CONVENTION_FIXED_NONCLAIM | same-frame normalization and official/human-promoted bound curve | False |
| R10P1199_1_qDT_residual_budget | q_DT_bound | Carry the D_T residual as an absolute positive budget before any R10 projection. | q_DT_bound = f_coker\|\|G_res\|\| + \|\|B_T\|\| + kappa_T C_T\|\|E_reg\|\| + \|\|Delta_P\|\|. | BOUND_FORM_DEFINED_INPUTS_MISSING | f_coker, G_res profile, B_T norm, kappa_T, C_T, E_reg, Delta_P source rows | False |
| R10P1199_2_W_R10_definition | W_R10(lambda) | Define the R10 response operator as the unit-normalized torque/readout response to a unit q_DT residual profile. | W_R10(lambda)=\|\|Pi_R10 K_exp(lambda) G_DT\|\| / \|unit_alpha_signal(lambda)\|, with K_exp the experiment/source-test kernel. | PROJECTION_OPERATOR_DEFINED_SYMBOLICALLY | R10 geometry kernel, source/test density, harmonic weights, q_DT profile convention, unit-alpha denominator | False |
| R10P1199_3_alpha_bound_formula | alpha_DT_envelope(lambda) | The scoreable prediction is a conservative envelope, not a signed cancellation. | \|alpha_DT(lambda)\| <= W_R10(lambda) q_DT_bound. | ABSOLUTE_ENVELOPE_FORM_DEFINED | numeric W_R10(lambda) and numeric q_DT_bound components | False |
| R10P1199_4_non_yukawa_guard | non_Yukawa_qDT | If q_DT does not produce a Yukawa-profile force, compare only through a conservative alpha_envelope(lambda) over the R10 separation/harmonic range. | alpha_envelope(lambda) >= sup_R \|delta a_DT(R)/a_N(R)\| / \|(1+R/lambda) exp(-R/lambda)\|, or the torque-kernel analogue. | NON_YUKAWA_SHORTCUT_BLOCKED | declared R range/kernel, q_DT force profile, conservative supremum calculation | False |
| R10P1199_5_curve_join_rule | R10 pass condition | For every curve row, require abs(alpha_DT(lambda_i)) <= alpha_bound(lambda_i), with no signed cancellation between components. | W_R10(lambda_i)[f_coker\|\|G\|\|+\|\|B_T\|\|+kappa_T C_T\|\|E_reg\|\|+\|\|Delta_P\|\|] <= alpha_bound(lambda_i). | JOIN_RULE_DEFINED_NONEXECUTABLE | all theory-side inputs and promoted/nonclaim policy decision for bound curve | False |
| R10P1199_6_verdict | MTS-side R10 projection | 1199 converts q_DT-to-R10 from a vague missing input into a concrete response-operator contract. | alpha_DT_bound(lambda)=W_R10(lambda) q_DT_bound, with all W/q inputs source-gated. | CONTRACT_DERIVED_NO_NUMERIC_R10_SCORE | W_R10, G_res, P_coker, B_T, E_reg, eps_P, and response/source paths | False |

## G_res profile schema

| schema_id | required_object | definition | required_fields | current_value | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| GRP1199_0_G_res_profile | G_res^nu(x) | local source vector entering D_TK_T=G_res, e.g. P_loc nabla^nu Gamma_eff after branch-specific corrections | domain_id;coframe;gauge;units;profile_grid_or_formula;norm_L2_or_weighted;source_path;equation_ref | MISSING_G_RES_PROFILE | False |
| GRP1199_1_P_coker_fraction | f_coker(lambda/domain) | fraction or projection norm of G_res into Ker(D_T^dagger) after boundary/quotient restrictions | cokernel_basis_path;projection_inner_product;domain_boundary_class;fraction_abs;source_path | MISSING_P_COKER_FRACTION | False |
| GRP1199_2_B_T_boundary_norm | \|\|B_T\|\| | bound on int_partialD n_mu K_T^(mu nu)(P_loc V)_nu or a zero certificate | boundary_geometry;trace_norm;K_T_normal_norm;P_locV_trace_norm;zero_certificate_or_bound_path;units | MISSING_B_T_BOUNDARY_NORM | False |
| GRP1199_3_projector_leakage | eps_P or \|\|Delta_P\|\| | nabla P_loc, coframe, domain-motion, and boundary-pullback leakage entering the D_T adjoint/range theorem | P_loc_definition;derivative_bound;coframe_variation;boundary_pullback;source_path;C_CK_eps_P_status | MISSING_EPS_P_LEAKAGE | False |
| GRP1199_4_W_R10 | W_R10(lambda) | normalized R10 torque/readout response to q_DT_bound, divided by unit-alpha Yukawa response | lambda;lambda_units;unit_alpha_denominator;torque_kernel_path;source_test_density_path;harmonic_weights;normalization;source_path | MISSING_W_R10_ALPHA_LAMBDA | False |
| GRP1199_5_no_cancellation | absolute component envelope | all q_DT residual contributions must be summed by absolute values before comparing to alpha_bound(lambda) | component_list;component_abs_values;sum_abs;no_signed_cancellation_guard | GUARD_ACTIVE_ABSOLUTE_SUM_ONLY | False |

## Nonclaim curve join samples

| sample_id | bound_id | lambda_value | lambda_units | alpha_bound | alpha_bound_source | alpha_predicted_bound | W_R10 | q_DT_bound | pass_condition | score_status | candidate_valid_for_claim | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R10J1199_0_nonclaim_curve_join_sample | R10_VECTOR_2020_REVIEW_0000 | 5.894419132271889e-06 | m | 897932.2928704522 | https://arxiv.org/abs/2002.11761; doi:10.1103/PhysRevLett.124.101101 | MISSING_W_R10_TIMES_QDT_BOUND | MISSING_W_R10_ALPHA_LAMBDA | MISSING_QDT_BOUND_COMPONENTS | abs_alpha_predicted_bound <= alpha_bound | blocked_missing_MTS_side_projection | false | False |
| R10J1199_1_nonclaim_curve_join_sample | R10_VECTOR_2020_REVIEW_0195 | 7.355973827852426e-05 | m | 0.14850286746800798 | https://arxiv.org/abs/2002.11761; doi:10.1103/PhysRevLett.124.101101 | MISSING_W_R10_TIMES_QDT_BOUND | MISSING_W_R10_ALPHA_LAMBDA | MISSING_QDT_BOUND_COMPONENTS | abs_alpha_predicted_bound <= alpha_bound | blocked_missing_MTS_side_projection | false | False |
| R10J1199_2_nonclaim_curve_join_sample | R10_VECTOR_2020_REVIEW_0351 | 0.000608078322298804 | m | 0.002344664300519378 | https://arxiv.org/abs/2002.11761; doi:10.1103/PhysRevLett.124.101101 | MISSING_W_R10_TIMES_QDT_BOUND | MISSING_W_R10_ALPHA_LAMBDA | MISSING_QDT_BOUND_COMPONENTS | abs_alpha_predicted_bound <= alpha_bound | blocked_missing_MTS_side_projection | false | False |
| R10J1199_3_nonclaim_curve_join_sample | R10_VECTOR_2020_REVIEW_0389 | 0.0010099153351819316 | m | 0.019113309433552817 | https://arxiv.org/abs/2002.11761; doi:10.1103/PhysRevLett.124.101101 | MISSING_W_R10_TIMES_QDT_BOUND | MISSING_W_R10_ALPHA_LAMBDA | MISSING_QDT_BOUND_COMPONENTS | abs_alpha_predicted_bound <= alpha_bound | blocked_missing_MTS_side_projection | false | False |

## Runner input row

| row_id | arena | observable | external_bound_curve_path | external_bound_status | W_R10_lambda | G_res_norm | coker_fraction | boundary_norm | regularizer_norm | coercivity_inverse | kappa_T | projector_leakage_norm | unit_alpha_denominator_path | torque_kernel_path | qDT_profile_path | numeric_ready | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| QDR1199_0_R10_projection_template | R10_alpha_lambda | alpha_DT(lambda) | source-intake\\local_bounds\\R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv | REVIEW_CANDIDATE_NONCLAIM | MISSING_W_R10_ALPHA_LAMBDA | MISSING_G_RES_PROFILE | MISSING_P_COKER_FRACTION | MISSING_B_T_BOUNDARY_NORM | MISSING_E_REG_NORM | MISSING_C_T_COERCIVITY | MISSING_KAPPA_T | MISSING_EPS_P_LEAKAGE | MISSING_SOURCE_PATH | MISSING_SOURCE_PATH | MISSING_SOURCE_PATH | False | False | False |

## Runner dry-run output

| run_id | curve_samples | external_bound_available | theory_side_ready | runner_status | alpha_DT_bound | tightest_candidate_alpha | passes_all | block_reason | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| QDO1199_0_R10_join_dryrun | 4 | True | False | blocked_missing_MTS_side_projection | MISSING_W_R10_TIMES_QDT_BOUND | 0.002344664300519378 | False | missing_fields:W_R10_lambda;G_res_profile;P_coker_fraction;B_T_boundary_norm;E_reg_norm;C_T;kappa_T;eps_P;unit_alpha_denominator;torque_kernel;qDT_profile | False | False |

## Claim gates

| gate_id | claim | status | why | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| G1199_0_projection_contract | q_DT-to-R10 projection is numerically sourced | BLOCKED_CONTRACT_ONLY | W_R10(lambda) is defined but no torque/readout kernel, unit-alpha denominator, or q_DT profile is sourced | False | False |
| G1199_1_G_res_profile | G_res profile and P_coker fraction are sourced | BLOCKED_PROFILE_AND_COKERNEL_MISSING | G_res, cokernel basis/projection, boundary norm, and projector leakage rows are still placeholders | False | False |
| G1199_2_R10_score | R10 q_DT row can pass/fail against alpha_bound(lambda) | BLOCKED_NO_ALPHA_DT_PREDICTION | external curve exists as nonclaim review candidate, but alpha_DT(lambda) is not computed | False | False |
| G1199_3_local_GR | MTS reduces to local GR/Newton through R10-safe q_DT suppression | BLOCKED_NO_LOCAL_GR_CLAIM | projection, source profile, boundary/cokernel, and parent action gates remain open | False | False |

## Decision ledger

| decision_id | decision | reason | next_action | valid_for_claim |
| --- | --- | --- | --- | --- |
| D1199_0_projection_contract | W_R10_contract_written | R10 requires a normalized torque/readout projection against a unit-alpha Yukawa signal | source or approximate the R10 torque kernel/unit-alpha denominator before numeric scoring | False |
| D1199_1_profile_status | G_res_profile_pack_missing | q_DT_bound cannot be converted to alpha(lambda) until the local residual profile, cokernel fraction, boundary norm, and eps_P leakage are specified | build a q_DT profile source pack or choose a conservative profile envelope | False |
| D1199_2_external_curve_status | R10_curve_used_only_for_nonclaim_join | the 2020 review-candidate curve is numeric and useful, but not promoted to a claim curve | keep using it for private dry-runs while sourcing MTS-side inputs | False |
| D1199_3_best_next | build_W_R10_kernel_stub_or_qDT_profile_pack | the largest remaining uncertainty is not the external bound, it is the mapping from MTS q_DT residuals into the R10 measured harmonics | 1200 should create the first W_R10 kernel/source-pack stub and qDT profile envelope rows | False |

## Validation

| check_id | result | detail | claim_allowed |
| --- | --- | --- | --- |
| V1199_0_sources_exist | pass | all cited local source paths exist and needles are found | False |
| V1199_1_projection_contract_present | pass | W_R10 definition, alpha envelope, and curve join rule are present | False |
| V1199_2_Gres_profile_schema_present | pass | G_res, P_coker, boundary/leakage, and W_R10 schema rows are present | False |
| V1199_3_curve_join_samples_numeric_nonclaim | pass | R10 curve join samples have numeric lambda/alpha bound values and remain nonclaim | False |
| V1199_4_runner_inputs_nonclaim | pass | R10 qDT runner input row remains nonclaim with missing W/q inputs | False |
| V1199_5_runner_outputs_blocked | pass | R10 join dry-run blocks because MTS-side projection/profile inputs are missing | False |
| V1199_6_claim_gates_blocked | pass | all 1199 claim gates and next target remain blocked/nonclaim | False |
| V1199_7_decisions_nonclaim | pass | decision ledger remains private/nonclaim | False |
| V1199_8_generated_under_post_checkpoint | pass | all generated outputs are under post-checkpoint-work | False |
| V1199_9_formalization_untouched | pass | generator writes no outputs under formalization-workbench | False |
| V1199_SUMMARY | pass | 1199 derives the q_DT-to-R10 projection contract W_R10(lambda), stages the G_res/P_coker/B_T/eps_P profile schema, joins nonclaim curve samples, and keeps R10/local-GR scoring blocked until MTS-side inputs are sourced | False |

## Next target

| next_id | next_target | objective | include | exclude | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| NEXT1199_0_1200 | 1200-Y5-R10-WR10-kernel-stub-and-qDT-profile-envelope.md | build the first nonclaim W_R10(lambda) kernel/source-pack stub and q_DT profile-envelope rows, so the R10 runner can eventually compute alpha_DT(lambda) instead of only listing missing fields | unit-alpha Yukawa denominator; R10 torque/readout kernel schema; qDT profile envelope; P_coker fraction placeholder discipline; B_T/eps_P source rows; nonclaim curve join | promoting review curve; invented W_R10 values; local-GR/R10 pass; signed cancellation; GitHub; formalization edits | False | False |
