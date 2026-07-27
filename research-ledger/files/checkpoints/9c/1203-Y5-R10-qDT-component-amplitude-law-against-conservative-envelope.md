# 1203 Y5/R10 qDT Component Amplitude Law Against Conservative Envelope

**Current verdict:** 1203 derives the executable amplitude pressure law but does not close the R10/local-GR branch. The global tightest private threshold inherited from 1202 is `q_DT_bound_total <= 2.34466430052e-05` under `WR10F1202_2_brutal_100x`.

**Main progress:** the missing local-GR problem is now sharply localized: either prove theorem-zero for the cokernel, boundary, regularizer, and projector terms, or source finite bounds whose absolute sum stays below the scenario threshold. No signed cancellation is allowed.

## Source Register

| source_id | local_path | needle | purpose | path_exists | needle_found | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SRC1203_0_1202_next | 1202-Y5-R10-conservative-geometry-kernel-or-qDT-profile-family.md | NEXT1202_0_1203 | handoff requiring q_DT component amplitude law against conservative envelope | True | True | False | False |
| SRC1203_1_1202_envelope | source-intake/mts_residuals/P8_Y5_R10_1202_QDT_ALLOWED_ENVELOPE.csv | QAE1202_0351_WR10F1202_2_brutal_100x | computed qDT_allowed thresholds from W_R10={1,10,100} | True | True | False | False |
| SRC1203_2_1199_budget | 1199-Y5-R10-qDT-to-R10-projection-or-Gres-profile-source.md | R10P1199_1_qDT_residual_budget | absolute residual budget formula | True | True | False | False |
| SRC1203_3_1199_join | 1199-Y5-R10-qDT-to-R10-projection-or-Gres-profile-source.md | R10P1199_5_curve_join_rule | R10 pass condition with no signed cancellation | True | True | False | False |
| SRC1203_4_1200_components | 1200-Y5-R10-WR10-kernel-stub-and-qDT-profile-envelope.md | QPE1200_0_total_envelope | q_DT component split | True | True | False | False |
| SRC1203_5_1196_cokernel | 1196-Y5-R10-DT-cokernel-zero-boundary-theorem-or-parent-action-block.md | CKZ1196_1_dirichlet_anchor_kills_kernel | conditional no-cokernel theorem route | True | True | False | False |
| SRC1203_6_1198_boundary_no_go | 1198-Y5-R10-DT-parent-anchor-source-or-first-real-bound-input-fill.md | DTA1198_5_verdict | natural-boundary shortcut rejected; boundary component remains live | True | True | False | False |
| SRC1203_7_1200_template | source-intake/mts_residuals/P8_Y5_R10_1200_QDT_PROFILE_ENVELOPE.csv | QPE1200_5_profile_shape | existing qDT profile component template | True | True | False | False |

## Amplitude Law

| law_id | object | formula | derivation | status | source_anchor | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| LAW1203_0_absolute_budget | q_DT_bound_total | q_DT_bound_total = q_coker + q_boundary + q_regularizer + q_projector | 1200 split plus 1199 absolute-envelope rule; all terms are nonnegative upper bounds before R10 projection. | DERIVED_SYMBOLIC_COMPONENT_LAW | 1200-Y5-R10-WR10-kernel-stub-and-qDT-profile-envelope.md::QPE1200_0_total_envelope | False | False |
| LAW1203_1_cokernel_component | q_coker | q_coker = f_coker \|\|G_res\|\| | project G_res onto surviving Ker(D_T^dagger) modes; if the no-cokernel theorem is parent-signed, f_coker=0. | DERIVED_SYMBOLIC_COMPONENT_INPUTS_MISSING | 1199-Y5-R10-qDT-to-R10-projection-or-Gres-profile-source.md::GRP1199_1_P_coker_fraction | False | False |
| LAW1203_2_boundary_component | q_boundary | q_boundary = \|\|B_T\|\| >= \|int_partialD n_mu K_T^(mu nu)(P_loc V)_nu dS\| | finite trace bound or zero certificate for the D_T adjoint boundary pairing. | DERIVED_SYMBOLIC_BOUNDARY_INPUT_MISSING | 1200-Y5-R10-WR10-kernel-stub-and-qDT-profile-envelope.md::QPE1200_2_boundary_component | False | False |
| LAW1203_3_regularizer_component | q_regularizer | q_regularizer = kappa_T C_T \|\|E_reg\|\| | regularizer residue enters the tracefree solver bound unless parent action makes it vanish. | DERIVED_SYMBOLIC_REGULARIZER_INPUTS_MISSING | 1200-Y5-R10-WR10-kernel-stub-and-qDT-profile-envelope.md::QPE1200_3_regularizer_component | False | False |
| LAW1203_4_projector_component | q_projector | q_projector = \|\|Delta_P\|\| or eps_P \|\|G_res\|\| with C_CK eps_P < 1 for absorption | P_loc/coframe/domain-motion leakage is either absorbed by the Korn inequality or scored as a finite residual. | DERIVED_SYMBOLIC_PROJECTOR_INPUTS_MISSING | 1199-Y5-R10-qDT-to-R10-projection-or-Gres-profile-source.md::GRP1199_3_projector_leakage | False | False |
| LAW1203_5_R10_gate | R10 nonclaim gate | q_DT_bound_total <= min_i[alpha_bound(lambda_i)/W_R10(lambda_i)] | from \|alpha_DT(lambda_i)\| <= W_R10(lambda_i) q_DT_bound_total <= alpha_bound(lambda_i). | DERIVED_EXECUTABLE_NONCLAIM_THRESHOLD | source-intake/mts_residuals/P8_Y5_R10_1202_QDT_ALLOWED_ENVELOPE.csv | False | False |

## Scenario Pressure Thresholds

| threshold_id | scenario_id | W_R10_assumed | tightest_source_row | lambda_value | lambda_units | alpha_bound | qDT_allowed_min | single_component_limit_if_others_zero | equal_two_component_limit | equal_four_component_limit | interpretation | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| THR1203_WR10F1202_0_matched_yukawa | WR10F1202_0_matched_yukawa | 1 | QAE1202_0351_WR10F1202_0_matched_yukawa | 0.000608078322299 | m | 0.00234466430052 | 0.00234466430052 | 0.00234466430052 | 0.00117233215026 | 0.00058616607513 | all active nonzero q_DT components must absolute-sum below qDT_allowed_min | False | False |
| THR1203_WR10F1202_1_pessimistic_10x | WR10F1202_1_pessimistic_10x | 10 | QAE1202_0351_WR10F1202_1_pessimistic_10x | 0.000608078322299 | m | 0.00234466430052 | 0.000234466430052 | 0.000234466430052 | 0.000117233215026 | 5.8616607513e-05 | all active nonzero q_DT components must absolute-sum below qDT_allowed_min | False | False |
| THR1203_WR10F1202_2_brutal_100x | WR10F1202_2_brutal_100x | 100 | QAE1202_0351_WR10F1202_2_brutal_100x | 0.000608078322299 | m | 0.00234466430052 | 2.34466430052e-05 | 2.34466430052e-05 | 1.17233215026e-05 | 5.8616607513e-06 | all active nonzero q_DT components must absolute-sum below qDT_allowed_min | False | False |

## Component Bound Status

| component_id | component | current_numeric_value | current_source_path | zero_route | finite_route | status | blocking_reason | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| COMP1203_0_cokernel | q_coker=f_coker\|\|G_res\|\| |  |  | parent-signed Ker(D_T^dagger)=0 or f_coker=0 on the local quotient domain | source f_coker and \|\|G_res\|\| in same norm/domain as R10 profile | MISSING_NUMERIC_PARENT_INPUT | no D_T cokernel fraction or G_res norm row is source-backed | False | False |
| COMP1203_1_boundary | q_boundary=\|\|B_T\|\| |  |  | parent boundary condition kills int_partialD n_mu K_T^(mu nu)(P_loc V)_nu dS | source a boundary trace norm bound below the qDT threshold | MISSING_NUMERIC_PARENT_INPUT | 1198 rejected generic natural boundary wording as insufficient | False | False |
| COMP1203_2_regularizer | q_regularizer=kappa_T C_T\|\|E_reg\|\| |  |  | parent action has no retained regularizer residue in the local GR branch | source kappa_T, C_T, and \|\|E_reg\|\| with compatible units | MISSING_NUMERIC_PARENT_INPUT | regularizer coefficient/coercivity/residue rows are not numeric | False | False |
| COMP1203_3_projector | q_projector=\|\|Delta_P\|\| or eps_P\|\|G_res\|\| |  |  | P_loc/coframe/domain-motion leakage vanishes or is absorbed with C_CK eps_P<1 | source Delta_P or eps_P and the absorption constant C_CK | MISSING_NUMERIC_PARENT_INPUT | projector leakage and absorption constant are not source-backed | False | False |

## Component Allocation Targets

| allocation_id | scenario_id | W_R10_assumed | tightest_source_row | qDT_allowed_min | allocation_mode | mode_description | component_limit | active_component_count_assumed | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ALLOC1203_WR10F1202_0_matched_yukawa_single_component_if_others_zero | WR10F1202_0_matched_yukawa | 1 | QAE1202_0351_WR10F1202_0_matched_yukawa | 0.00234466430052 | single_component_if_others_zero | one live component; other three theorem-zero | 0.00234466430052 | 1 | False | False |
| ALLOC1203_WR10F1202_0_matched_yukawa_two_component_equal_split | WR10F1202_0_matched_yukawa | 1 | QAE1202_0351_WR10F1202_0_matched_yukawa | 0.00234466430052 | two_component_equal_split | two live components; other two theorem-zero | 0.00117233215026 | 2 | False | False |
| ALLOC1203_WR10F1202_0_matched_yukawa_four_component_equal_split | WR10F1202_0_matched_yukawa | 1 | QAE1202_0351_WR10F1202_0_matched_yukawa | 0.00234466430052 | four_component_equal_split | all four components live and equally budgeted | 0.00058616607513 | 4 | False | False |
| ALLOC1203_WR10F1202_0_matched_yukawa_one_order_safety_per_component | WR10F1202_0_matched_yukawa | 1 | QAE1202_0351_WR10F1202_0_matched_yukawa | 0.00234466430052 | one_order_safety_per_component | all four live with tenfold safety margin per component | 5.8616607513e-05 | 4 | False | False |
| ALLOC1203_WR10F1202_1_pessimistic_10x_single_component_if_others_zero | WR10F1202_1_pessimistic_10x | 10 | QAE1202_0351_WR10F1202_1_pessimistic_10x | 0.000234466430052 | single_component_if_others_zero | one live component; other three theorem-zero | 0.000234466430052 | 1 | False | False |
| ALLOC1203_WR10F1202_1_pessimistic_10x_two_component_equal_split | WR10F1202_1_pessimistic_10x | 10 | QAE1202_0351_WR10F1202_1_pessimistic_10x | 0.000234466430052 | two_component_equal_split | two live components; other two theorem-zero | 0.000117233215026 | 2 | False | False |
| ALLOC1203_WR10F1202_1_pessimistic_10x_four_component_equal_split | WR10F1202_1_pessimistic_10x | 10 | QAE1202_0351_WR10F1202_1_pessimistic_10x | 0.000234466430052 | four_component_equal_split | all four components live and equally budgeted | 5.8616607513e-05 | 4 | False | False |
| ALLOC1203_WR10F1202_1_pessimistic_10x_one_order_safety_per_component | WR10F1202_1_pessimistic_10x | 10 | QAE1202_0351_WR10F1202_1_pessimistic_10x | 0.000234466430052 | one_order_safety_per_component | all four live with tenfold safety margin per component | 5.8616607513e-06 | 4 | False | False |
| ALLOC1203_WR10F1202_2_brutal_100x_single_component_if_others_zero | WR10F1202_2_brutal_100x | 100 | QAE1202_0351_WR10F1202_2_brutal_100x | 2.34466430052e-05 | single_component_if_others_zero | one live component; other three theorem-zero | 2.34466430052e-05 | 1 | False | False |
| ALLOC1203_WR10F1202_2_brutal_100x_two_component_equal_split | WR10F1202_2_brutal_100x | 100 | QAE1202_0351_WR10F1202_2_brutal_100x | 2.34466430052e-05 | two_component_equal_split | two live components; other two theorem-zero | 1.17233215026e-05 | 2 | False | False |
| ALLOC1203_WR10F1202_2_brutal_100x_four_component_equal_split | WR10F1202_2_brutal_100x | 100 | QAE1202_0351_WR10F1202_2_brutal_100x | 2.34466430052e-05 | four_component_equal_split | all four components live and equally budgeted | 5.8616607513e-06 | 4 | False | False |
| ALLOC1203_WR10F1202_2_brutal_100x_one_order_safety_per_component | WR10F1202_2_brutal_100x | 100 | QAE1202_0351_WR10F1202_2_brutal_100x | 2.34466430052e-05 | one_order_safety_per_component | all four live with tenfold safety margin per component | 5.8616607513e-07 | 4 | False | False |

## Symbolic Comparison

| comparison_id | q_coker | q_boundary | q_regularizer | q_projector | q_DT_bound_total | threshold_used | threshold_value | score_status | interpretation | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CMP1203_0_current | MISSING | MISSING | MISSING | MISSING | MISSING | THR1203_WR10F1202_2_brutal_100x | 2.34466430052e-05 | BLOCKED_MISSING_COMPONENT_AMPLITUDES | The inequality is executable, but current corpus lacks numeric q_DT component amplitudes. | False | False |
| CMP1203_1_zero_branch_sufficient_condition | 0 | 0 | 0 | 0 | 0 | THR1203_WR10F1202_2_brutal_100x | 2.34466430052e-05 | CONDITIONAL_PASS_IF_ALL_ZERO_THEOREMS_PARENT_SIGNED | A real local-GR reduction route would pass this nonclaim envelope if all four components are theorem-zero from the parent action. | False | False |

## Claim Gates

| gate_id | gate | status | reason | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| GATE1203_0_component_values | numeric q_DT component amplitudes | BLOCKED | all four q_DT components remain missing parent-signed numeric values or zero certificates | False | False |
| GATE1203_1_WR10_official | official/source-reconstructed W_R10 | BLOCKED | 1203 still uses 1202 scenario W values, not the official R10 geometry kernel | False | False |
| GATE1203_2_bound_curve_promotion | promoted R10 bound curve | BLOCKED | review-candidate curve remains nonclaim | False | False |
| GATE1203_3_no_tuned_cancellation | absolute sum only | ACTIVE_GUARD | component signs cannot cancel; every live component consumes positive qDT budget | False | False |

## Decision Ledger

| decision_id | condition | decision | result | next_action | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- |
| DEC1203_0_verdict | amplitude law derived but no component amplitudes sourced | keep R10/local-GR branch blocked, but define the next target as a component-zero or component-bound attack | global tightest private target is q_DT_bound_total <= 2.34466430052e-05 under WR10F1202_2_brutal_100x | try to close the strongest component first: boundary B_T zero/bound or projector absorption, because those can remove whole positive terms | False | False |

## Next Target

| next_id | target_file | target_script | task | success_condition | do_not_do | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NEXT1203_0_1204 | 1204-Y5-R10-boundary-projector-zero-or-finite-amplitude-bound.md | scripts/Y5_R10_boundary_projector_zero_or_finite_amplitude_bound.py | attack q_boundary and q_projector first: either derive parent-signed zero/absorption conditions or produce finite source-ready bounds small enough for the 1203 amplitude targets | at least one live positive q_DT component is either theorem-zero or has a numeric nonclaim upper bound; no R10/local-GR pass is claimed | do not tune cancellations, do not promote the review curve, do not edit formalization-workbench, do not push GitHub | False | False |

## Validation

| check_id | check | status | details | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| VAL1203_0_sources_exist | all cited local sources exist | PASS | 8/8 sources exist | False | False |
| VAL1203_1_needles_found | all cited source needles found | PASS | 8/8 needles found | False | False |
| VAL1203_2_thresholds_positive | scenario thresholds are positive | PASS | scenario_threshold_count=3 | False | False |
| VAL1203_3_global_threshold | global tight threshold inherited from 1202 | PASS | global_tight=2.34466430052e-05;source=QAE1202_0351_WR10F1202_2_brutal_100x | False | False |
| VAL1203_4_components_blocked | component amplitudes remain explicitly blocked | PASS | blocked_components=4/4 | False | False |
| VAL1203_5_current_comparison_blocked | current comparison does not claim a pass | PASS | BLOCKED_MISSING_COMPONENT_AMPLITUDES | False | False |
| VAL1203_6_zero_branch_nonclaim | zero branch is only conditional nonclaim | PASS | CONDITIONAL_PASS_IF_ALL_ZERO_THEOREMS_PARENT_SIGNED | False | False |
| VAL1203_7_allocations_positive | component allocation targets are positive | PASS | allocation_rows=12 | False | False |
| VAL1203_8_nonclaim_policy | all generated rows remain nonclaim | PASS | valid_for_claim=false and claim_allowed=false throughout | False | False |
| VAL1203_9_csv_parse | all generated CSVs parse cleanly | PASS | P8_Y5_R10_1203_SOURCE_REGISTER.csv:8; P8_Y5_R10_1203_AMPLITUDE_LAW.csv:6; P8_Y5_R10_1203_SCENARIO_PRESSURE_THRESHOLDS.csv:3; P8_Y5_R10_1203_COMPONENT_BOUND_STATUS.csv:4; P8_Y5_R10_1203_COMPONENT_ALLOCATION_TARGETS.csv:12; P8_Y5_R10_1203_SYMBOLIC_COMPARISON.csv:2; P8_Y5_R10_1203_CLAIM_GATES.csv:4; P8_Y5_R10_1203_DECISION_LEDGER.csv:1; P8_Y5_R10_1203_NEXT_TARGET.csv:1 | False | False |
| VAL1203_10_formalization_untouched | formalization-workbench untouched during run | PASS | formalization_recent_after_run_start_count=0 | False | False |
| VAL1203_11_overall | overall 1203 validation | PASS | 1203 amplitude law and component pressure targets are reproducible | False | False |
