# 1200 - Y5/R10 W_R10 kernel stub and qDT profile envelope

**Current verdict:** `W_R10(lambda)` is now a concrete source-pack object: a unit-alpha R10 denominator and a unit-qDT numerator must be supplied before any R10 score exists. No numeric `W_R10` value is invented.

**Main progress:** the `q_DT` profile envelope is split into cokernel, boundary, regularizer, projector, and profile-shape rows, giving the runner real columns to fill instead of one vague missing-input blob.

**No claim:** no q_loc=0, local-GR, Newton, R10, PPN, WEP, clock, orbital, or public-facing claim follows from this checkpoint.

## Source register

| source_id | relative_path | needle | role | exists | needle_found |
| --- | --- | --- | --- | --- | --- |
| SRC1200_0_1199_next | 1199-Y5-R10-qDT-to-R10-projection-or-Gres-profile-source.md | NEXT1199_0_1200 | direct 1200 handoff. | True | True |
| SRC1200_1_1199_WR10 | 1199-Y5-R10-qDT-to-R10-projection-or-Gres-profile-source.md | R10P1199_2_W_R10_definition | W_R10 response operator definition. | True | True |
| SRC1200_2_1199_qDT | 1199-Y5-R10-qDT-to-R10-projection-or-Gres-profile-source.md | R10P1199_3_alpha_bound_formula | alpha_DT envelope formula. | True | True |
| SRC1200_3_1199_Gres | 1199-Y5-R10-qDT-to-R10-projection-or-Gres-profile-source.md | GRP1199_0_G_res_profile | G_res profile schema. | True | True |
| SRC1200_4_1035_harmonic | 1035-Y5-R10-KX-green-kernel-normalization-and-profile-integral.md | KXD1035_4_R10_harmonic_projection | R10 torque harmonic projection precedent. | True | True |
| SRC1200_5_1035_missing | 1035-Y5-R10-KX-green-kernel-normalization-and-profile-integral.md | KXF1035_3_harmonic | R10 harmonic projection missing status. | True | True |
| SRC1200_6_437_yukawa | 437-R10-alpha-lambda-executable-curve-contract.md | Yukawa_potential | R10 Yukawa potential convention. | True | True |
| SRC1200_7_437_no_scalar | 437-R10-alpha-lambda-executable-curve-contract.md | single_delta_G_scalar | R10 cannot be scalar-only. | True | True |
| SRC1200_8_831_bound | 831-Y5-R10-parent-Khat-tensor-operator-or-local-branch-closure.md | RT831_3_bound | q_DT residual bound components. | True | True |
| SRC1200_9_1197_R10_runner | 1197-Y5-R10-DT-boundary-condition-source-or-cokernel-bound-runner.md | CBI1197_1_R10 | R10 q_DT runner template. | True | True |
| SRC1200_10_R10_candidate | source-intake/local_bounds/R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv | R10_VECTOR_2020_REVIEW_0000 | nonclaim R10 numeric curve for dry-run samples. | True | True |

## W_R10 kernel stub

| kernel_id | object | definition | mathematical_form | required_sources | current_status | numeric_ready | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| WRK1200_0_unit_alpha_denominator | D_Y(lambda) | unit-alpha Yukawa denominator in the actual R10 readout. | D_Y(lambda)=\|\|Pi_R10 T_h[V_N exp(-r/lambda)]\|\|_abs over declared harmonic channels. | R10 geometry; Newtonian source/test density; separation/rotation model; harmonic channel weights; readout normalization | STUB_SOURCE_PACK_ROW_VALUES_MISSING | False | False |
| WRK1200_1_qDT_numerator | N_DT(lambda) | R10 readout response to a unit-normalized q_DT residual profile. | N_DT(lambda)=\|\|Pi_R10 T_h[Phi_DT[G_DT_profile,lambda]]\|\|_abs. | qDT profile convention; Green/force map from q_DT to Phi_DT; same R10 torque kernel; source/test support | STUB_SOURCE_PACK_ROW_VALUES_MISSING | False | False |
| WRK1200_2_harmonic_channels | Pi_R10 | projection onto the measured R10 torque/readout harmonic channels. | Pi_R10 T = abs(w_18 T_18omega)+abs(w_120 T_120omega)+abs(retained_harmonic_tail). | harmonic channel list; weights; phase convention; whether 18omega/120omega are both used for this curve | HARMONIC_CHANNELS_NAMED_WEIGHTS_MISSING | False | False |
| WRK1200_3_WR10_ratio | W_R10(lambda) | dimensionless response factor converting q_DT_bound to alpha_DT envelope. | W_R10(lambda)=N_DT(lambda)/D_Y(lambda), with D_Y(lambda)>0 and all numerator components absolute-summed. | WRK1200_0; WRK1200_1; denominator positivity certificate; same frame/unit convention | SYMBOLIC_RATIO_READY_NUMERIC_VALUES_MISSING | False | False |
| WRK1200_4_denominator_zero_guard | D_Y(lambda)>0 guard | R10 response cannot be normalized where the unit-alpha denominator vanishes or is not defined. | valid row requires finite positive D_Y(lambda_i); otherwise row_status=blocked_zero_or_missing_denominator. | unit-alpha torque denominator table or official response kernel | DENOMINATOR_VALUES_MISSING | False | False |
| WRK1200_5_verdict | W_R10 kernel source pack | 1200 creates the first W_R10 source-pack stub; no W_R10 values are invented. | alpha_DT_bound(lambda)=W_R10(lambda)[f_coker\|\|G_res\|\|+\|\|B_T\|\|+kappa_T C_T\|\|E_reg\|\|+\|\|Delta_P\|\|]. | kernel table plus qDT profile envelope table | KERNEL_STUB_CREATED_NONCLAIM | False | False |

## qDT profile envelope

| profile_id | component | definition | formula | required_fields | current_value | numeric_ready | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| QPE1200_0_total_envelope | q_DT_bound_total | absolute residual budget before R10 projection. | q_DT_bound = q_coker + q_boundary + q_regularizer + q_projector | q_coker;q_boundary;q_regularizer;q_projector;units;domain_id;source_path | MISSING_COMPONENT_VALUES | False | False |
| QPE1200_1_cokernel_component | q_coker | projection of G_res onto surviving D_T adjoint cokernel modes. | q_coker = f_coker \|\|G_res\|\| | f_coker;G_res_norm;cokernel_basis_path;inner_product;boundary_class;source_path | MISSING_P_COKER_AND_G_RES | False | False |
| QPE1200_2_boundary_component | q_boundary | finite bound or zero certificate for the D_T adjoint boundary pairing. | q_boundary = \|\|B_T\|\| >= \|int_partialD n_mu K_T^(mu nu)(P_loc V)_nu dS\| | boundary_geometry;K_T_trace_norm;P_locV_trace_norm;zero_certificate_or_bound;source_path | MISSING_B_T_BOUNDARY_NORM | False | False |
| QPE1200_3_regularizer_component | q_regularizer | regularizer or parent action residue contribution. | q_regularizer = kappa_T C_T \|\|E_reg\|\| | kappa_T;C_T;E_reg_norm;regularizer_source_path;parent_action_status | MISSING_REGULARIZER_COERCIVITY_INPUTS | False | False |
| QPE1200_4_projector_component | q_projector | P_loc/coframe/domain-motion leakage entering the D_T adjoint/range theorem. | q_projector = \|\|Delta_P\|\| or eps_P\|\|G_res\|\| with C_CK eps_P < 1 for zero-route absorption. | eps_P;P_loc_definition;coframe_variation;domain_motion;C_CK;source_path | MISSING_EPS_P_LEAKAGE | False | False |
| QPE1200_5_profile_shape | G_DT_profile_shape | shape profile used by N_DT(lambda), normalized separately from q_DT_bound amplitude. | G_DT_profile(x)=G_res(x)/\|\|G_res\|\| or conservative envelope over allowed local profiles. | profile_grid_or_formula;normalization;support;gauge;coframe;domain;source_path | MISSING_QDT_PROFILE_SHAPE | False | False |

## Source-pack templates

| pack_id | file_to_fill | required_columns | acceptance_rule | current_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| SP1200_0_WR10_kernel_pack | source-intake/mts_residuals/P8_Y5_R10_1200_WR10_KERNEL_VALUES_TO_FILL.csv | lambda;lambda_units;D_Y_unit_alpha;N_DT_unit_profile;W_R10;harmonic_channels;kernel_source_path;valid_for_claim | D_Y_unit_alpha>0;W_R10>=0;kernel_source_path exists;valid_for_claim false until reviewed | TEMPLATE_DECLARED_NOT_FILLED | False |
| SP1200_1_QDT_profile_pack | source-intake/mts_residuals/P8_Y5_R10_1200_QDT_PROFILE_VALUES_TO_FILL.csv | domain_id;profile_id;G_res_norm;f_coker;B_T_norm;kappa_T;C_T;E_reg_norm;Delta_P_norm;q_DT_bound;source_path;valid_for_claim | all components numeric nonnegative; source_path exists;absolute-sum guard active | TEMPLATE_DECLARED_NOT_FILLED | False |
| SP1200_2_curve_join_pack | source-intake/mts_residuals/P8_Y5_R10_1200_R10_JOIN_VALUES_TO_FILL.csv | lambda;alpha_bound;W_R10;q_DT_bound;alpha_DT_bound;passes;curve_source_path;theory_source_path;valid_for_claim | alpha_DT_bound=W_R10*q_DT_bound;alpha_DT_bound<=alpha_bound;no signed cancellation;curve remains nonclaim unless promoted | TEMPLATE_DECLARED_NOT_FILLED | False |

## Nonclaim join samples

| sample_id | bound_id | lambda_value | lambda_units | alpha_bound | D_Y_unit_alpha | N_DT_unit_profile | W_R10 | q_DT_bound | alpha_DT_bound | join_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| JS1200_0_WR10_stub_join_sample | R10_VECTOR_2020_REVIEW_0000 | 5.894419132271889e-06 | m | 897932.2928704522 | MISSING_UNIT_ALPHA_DENOMINATOR | MISSING_QDT_NUMERATOR_RESPONSE | MISSING_WR10 | MISSING_QDT_BOUND | MISSING_WR10_TIMES_QDT | blocked_kernel_and_profile_missing | False |
| JS1200_1_WR10_stub_join_sample | R10_VECTOR_2020_REVIEW_0195 | 7.355973827852426e-05 | m | 0.14850286746800798 | MISSING_UNIT_ALPHA_DENOMINATOR | MISSING_QDT_NUMERATOR_RESPONSE | MISSING_WR10 | MISSING_QDT_BOUND | MISSING_WR10_TIMES_QDT | blocked_kernel_and_profile_missing | False |
| JS1200_2_WR10_stub_join_sample | R10_VECTOR_2020_REVIEW_0351 | 0.000608078322298804 | m | 0.002344664300519378 | MISSING_UNIT_ALPHA_DENOMINATOR | MISSING_QDT_NUMERATOR_RESPONSE | MISSING_WR10 | MISSING_QDT_BOUND | MISSING_WR10_TIMES_QDT | blocked_kernel_and_profile_missing | False |
| JS1200_3_WR10_stub_join_sample | R10_VECTOR_2020_REVIEW_0389 | 0.0010099153351819316 | m | 0.019113309433552817 | MISSING_UNIT_ALPHA_DENOMINATOR | MISSING_QDT_NUMERATOR_RESPONSE | MISSING_WR10 | MISSING_QDT_BOUND | MISSING_WR10_TIMES_QDT | blocked_kernel_and_profile_missing | False |

## Runner dry-run

| run_id | sample_rows | external_curve_available | WR10_ready | qDT_profile_ready | runner_status | alpha_DT_bound | block_reason | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| RUN1200_0_WR10_qDT_join_dryrun | 4 | True | False | False | blocked_missing_kernel_and_profile_values | MISSING_WR10_TIMES_QDT | missing_fields:D_Y_unit_alpha;N_DT_unit_profile;W_R10;G_res_norm;f_coker;B_T_norm;kappa_T;C_T;E_reg_norm;Delta_P_norm;qDT_profile_shape | False | False |

## Claim gates

| gate_id | claim | status | why | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| G1200_0_WR10_values | W_R10(lambda) values are available | BLOCKED_KERNEL_VALUES_MISSING | unit-alpha denominator and qDT numerator response are only stubbed, not numeric/source-backed | False | False |
| G1200_1_qDT_profile | q_DT profile envelope is numeric/source-backed | BLOCKED_PROFILE_VALUES_MISSING | G_res, f_coker, B_T, regularizer, projector leakage, and profile shape are missing | False | False |
| G1200_2_R10_score | R10 qDT dry-run can score | BLOCKED_JOIN_VALUES_MISSING | alpha_DT_bound cannot be computed without W_R10 and q_DT_bound | False | False |
| G1200_3_local_GR | MTS local-GR reduction is R10-safe | BLOCKED_NO_LOCAL_GR_CLAIM | R10 projection, qDT profile, parent action, and boundary/cokernel gates remain open | False | False |

## Decision ledger

| decision_id | decision | reason | next_action | valid_for_claim |
| --- | --- | --- | --- | --- |
| D1200_0_kernel_stub | WR10_source_pack_stub_created | W_R10 needs numerator/denominator torque-readout kernels, not an invented scalar response | fill D_Y and N_DT from geometry/official kernel or build conservative toy kernel explicitly marked nonclaim | False |
| D1200_1_qDT_profile | qDT_profile_envelope_rows_created | R10 cannot constrain q_DT until amplitude components and profile shape are separated | source G_res profile or build a conservative profile-envelope family | False |
| D1200_2_best_next | fill_first_nonclaim_kernel_value_or_profile_family | the runner now has exact columns; the next progress comes from populating one with sourced or explicitly toy nonclaim data | 1201 should attempt an official/geometry W_R10 source; if unavailable, create a transparent toy-kernel smoke row with claim_allowed=false | False |

## Validation

| check_id | result | detail | claim_allowed |
| --- | --- | --- | --- |
| V1200_0_sources_exist | pass | all cited local source paths exist and needles are found | False |
| V1200_1_WR10_stub_present | pass | W_R10 denominator, numerator, and ratio rows are present | False |
| V1200_2_qDT_profile_envelope_present | pass | qDT profile-envelope rows include total, cokernel, and shape components | False |
| V1200_3_source_pack_templates_present | pass | kernel, qDT profile, and join source-pack templates are declared | False |
| V1200_4_samples_numeric_nonclaim | pass | R10 join samples have numeric lambda/alpha bounds and remain nonclaim | False |
| V1200_5_dryrun_blocked | pass | dry-run blocks because kernel/profile values are missing | False |
| V1200_6_claim_gates_blocked | pass | all 1200 claim gates and next target remain blocked/nonclaim | False |
| V1200_7_all_science_rows_nonclaim | pass | all generated science rows keep valid_for_claim=false | False |
| V1200_8_generated_under_post_checkpoint | pass | all generated outputs are under post-checkpoint-work | False |
| V1200_9_formalization_untouched | pass | generator writes no outputs under formalization-workbench | False |
| V1200_SUMMARY | pass | 1200 creates the first W_R10 kernel/source-pack stub and qDT profile-envelope rows, then blocks the R10 join until numerator, denominator, and qDT profile values are sourced | False |

## Next target

| next_id | next_target | objective | include | exclude | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| NEXT1200_0_1201 | 1201-Y5-R10-WR10-official-kernel-source-or-toy-kernel-smoke-row.md | source an official/geometry R10 torque kernel for W_R10, or create a transparent toy-kernel smoke row that exercises the qDT runner while remaining nonclaim | D_Y unit-alpha denominator; N_DT unit qDT numerator; harmonic weights; source/test geometry; qDT profile family; nonclaim dry-run | invented claim W_R10; promoting review curve; local-GR/R10 pass; signed cancellation; GitHub; formalization edits | False | False |
