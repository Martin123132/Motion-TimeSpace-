# 4840 Y5 R2FR source action pullback signature or first density qbasic bound row

**Status:** 4840 reduces the `M_H_ref`/Newton source-denominator problem to the parent matter grammar. If the ordinary matter+EM source action is a pullback through the observed stack, and source-only weights/selectors are illegal, then `rho_H dV_H` is q-basic by the 3561 theorem. The live branch remains nonclaim because the parent source-action pullback and no-source-only theorem are not signed.

**Decision:** `SOURCE_ACTION_PULLBACK_UNSIGNED_FIRST_DENSITY_QBASIC_BOUND_ROW_STAGED_NONCLAIM`.

## Core derivation

```text
S_src = q^* Sbar_src[q(Phi), psi, theta, A_obs]
T_H = variation of S_src with respect to g_obs before readout
rho_H dV_H = n_mu tau_nu T_H_mu_nu dSigma_H
rho_H dV_H = rhobar_H(q(Phi), psi, theta)
```

For a vertical direction `v` with `Dq(v)=0`:

```text
D_v(rho_H dV_H) =
  d rhobar_H(Dq(v)) + Euler_matter + gauge + boundary
```

The first term is zero only if the source action really factors through `q` and no source-only coefficient survives.

## Source Register

| source_id | exists | needle_found | role |
| --- | --- | --- | --- |
| SRC4840_00_resume | True | True | 4839 selected this pullback target. |
| SRC4840_01_4839_doc | True | True | source-action pullback handoff. |
| SRC4840_02_4839_output | True | True | live source descent row remains blocked. |
| SRC4840_03_3561_theorem | True | True | density q-basic theorem. |
| SRC4840_04_3561_countermodel | True | True | source-only countermodel. |
| SRC4840_05_3561_decomp | True | True | density residual decomposition. |
| SRC4840_06_3561_bound | True | True | bound vector row. |
| SRC4840_07_3293_signature | True | True | Hilbert-source signature target. |
| SRC4840_08_3293_gap | True | True | parent action descent gap. |
| SRC4840_09_2587_contract | True | True | minimal matter pullback contract. |
| SRC4840_10_2587_no_slot | True | True | no source-only slot contract. |
| SRC4840_11_2646_owner | True | True | single action-density owner. |
| SRC4840_12_2612_nohom | True | True | no-Hom source-only route. |
| SRC4840_13_3142_em | True | True | EM q-basic stress theorem. |
| SRC4840_14_no_source_only | True | True | source-only residual rows. |
| SRC4840_15_4835_output | True | True | matter quotient source row blocked. |
| SRC4840_16_4836_output | True | True | theta constant row blocked. |
| SRC4840_17_source_current | True | True | source current definition. |
| SRC4840_18_runner | True | True | 4840 executable runner. |

## Pullback Audit

| clause_id | object | current_result | needed_signature_or_input |
| --- | --- | --- | --- |
| SAP4840_0_signature | Hilbert-source signature | CONDITIONAL_SIGNATURE_EXISTS | parent action adoption |
| SAP4840_1_pullback | source action pullback | CORE_UNSIGNED | actual MTS parent action or no-extra-slot theorem |
| SAP4840_2_density | density q-basic theorem | EXACT_CONDITIONAL_NOT_LIVE | sign pullback clauses |
| SAP4840_3_source_weights | source-only weights | LIVE_COUNTERMODEL | single action-density/no-Hom proof |
| SAP4840_4_hidden_marker | hidden marker source coefficient | LIVE_COUNTERMODEL | no-Hom hidden marker theorem |
| SAP4840_5_EM | EM q-basic stress | CONDITIONAL_OPEN_FROM_4837 | EM owner or finite flux row |
| SAP4840_6_theta | constant sector | OPEN_FROM_4836 | theta derivative or zero theorem |
| SAP4840_7_vertical | vertical density derivative | CONDITIONAL_NOT_LIVE | vertical profile bound if not zero |
| SAP4840_8_anti | anti-circularity | GUARD_ACTIVE | runner forbidden rows |

## Runner Contract

| contract_id | quantity | definition | status |
| --- | --- | --- | --- |
| DQB4840_0_zero | density q-basic zero | all source-action pullback, q-owned stack, variation-before-readout, source-only exclusion and EM/theta clauses signed | conditional_only |
| DQB4840_1_bound | density_qbasic_residual_abs | E_action_pullback+delta_w_species+kappa_A+hidden_marker+measure/tau/EM/theta/lift/boundary/nonHilbert/readout terms | runner_ready_values_missing |
| DQB4840_2_vertical | vertical_density_residual_abs | rho_vertical_slope*vertical_amplitude + matter_Euler + gauge_fix + boundary_layer | runner_ready_values_missing |
| DQB4840_3_feed | density residual to MHref/Newton feed | delta_MHref_density=qbar feed -> alpha/BY5 source-normalization rows | runner_ready_values_missing |
| DQB4840_4_next | single action-density line | prove no source-only weights or fill first delta_w_species row | next_target |

## Runner Output

| row_id | runner_status | source_action_residual_abs | density_qbasic_residual_abs | vertical_density_residual_abs | delta_MHref_density_abs | alpha_source_abs | BY5_density_feed_abs | missing_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| RUN4840_0_live_pullback_zero_missing | BLOCKED_SOURCE_ACTION_PULLBACK_ZERO_CLAUSES | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_source_signed;MISSING_units_signed;MISSING_same_branch_signed;MISSING_no_cancellation_guard;MISSING_parent_action_diffeomorphic_signed;MISSING_q_map_signed;MISSING_observed_stack_q_owned_signed;MISSING_source_action_pullback_signed;MISSING_single_action_density_line_signed;MISSING_variation_before_readout_signed;MISSING_measure_coframe_time_qbasic_signed;MISSING_EM_qbasic_or_flux_retained_signed;MISSING_theta_representation_superselection_signed;MISSING_no_source_only_weights_signed;MISSING_no_kappa_A_source_selector_signed;MISSING_no_hidden_marker_source_signed;MISSING_matter_labels_fixed_or_on_shell_signed;MISSING_no_boundary_source_layer_signed;MISSING_nonHilbert_current_zero_signed;MISSING_no_readout_mask_signed;MISSING_no_measured_GM_absorption_signed |
| RUN4840_1_conditional_pullback_zero_pass | SOURCE_ACTION_PULLBACK_ZERO_PASS_NONCLAIM | 0.000000000000000e+00 | 0.000000000000000e+00 | 0.000000000000000e+00 | 0.000000000000000e+00 | 0.000000000000000e+00 | 0.000000000000000e+00 |  |
| RUN4840_2_live_density_bound_missing | BLOCKED_SOURCE_ACTION_DENSITY_BOUND_INPUTS | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_E_action_pullback_abs;MISSING_delta_w_species_abs;MISSING_kappa_A_source_abs;MISSING_hidden_marker_source_abs;MISSING_E_measure_qbasic_abs;MISSING_E_tau_frame_abs;MISSING_E_EM_qbasic_abs;MISSING_E_theta_abs;MISSING_E_matter_lift_abs;MISSING_E_boundary_source_abs;MISSING_E_nonHilbert_bypass_abs;MISSING_E_readout_mask_abs;MISSING_P_density_qbar_abs;MISSING_Qbar_source_XH_bound_abs;MISSING_K_source_abs;MISSING_tau_BY5_density_abs |
| RUN4840_3_density_bound_smoke_pass | SOURCE_ACTION_DENSITY_BOUND_PASS_NONCLAIM | 3.100000000000000e-03 | 8.500000000000001e-03 | MISSING_NUMERIC_VALUE | 8.500000000000001e-03 | 1.880625000000000e-04 | 1.700000000000000e-02 |  |
| RUN4840_4_live_vertical_profile_missing | BLOCKED_VERTICAL_DENSITY_PROFILE_INPUTS | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_rho_vertical_slope_abs;MISSING_vertical_amplitude_abs;MISSING_matter_Euler_residual_abs;MISSING_gauge_fix_residual_abs;MISSING_boundary_layer_abs;MISSING_P_density_qbar_abs;MISSING_Qbar_source_XH_bound_abs;MISSING_K_source_abs;MISSING_tau_BY5_density_abs |
| RUN4840_5_vertical_profile_smoke_pass | VERTICAL_DENSITY_PROFILE_BOUND_PASS_NONCLAIM | MISSING_NUMERIC_VALUE | 2.400000000000000e-03 | 2.400000000000000e-03 | 2.400000000000000e-03 | 5.310000000000000e-05 | 4.800000000000000e-03 |  |
| RUN4840_6_forbidden_density_assertion | FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE |
| RUN4840_7_forbidden_source_weight_zero | FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE |
| RUN4840_8_forbidden_kappa_selector | FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE |
| RUN4840_9_forbidden_EM_dropped | FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE |
| RUN4840_10_forbidden_measured_GM_source | FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE |

## Validation

| check_id | status | detail |
| --- | --- | --- |
| VAL4840_00_sources_exist | PASS | all cited source paths exist |
| VAL4840_01_needles_found | PASS | all source needles found |
| VAL4840_02_runner_compiles | PASS | runner compiles |
| VAL4840_03_generator_compiles | PASS | generator compiles |
| VAL4840_04_output_count | PASS | outputs=11 inputs=11 |
| VAL4840_05_claims_false | PASS | runner hard-codes nonclaim rows |
| VAL4840_06_live_zero_blocked | PASS | MISSING_source_signed;MISSING_units_signed;MISSING_same_branch_signed;MISSING_no_cancellation_guard;MISSING_parent_action_diffeomorphic_signed;MISSING_q_map_signed;MISSING_observed_stack_q_owned_signed;MISSING_source_action_pullback_signed;MISSING_single_action_density_line_signed;MISSING_variation_before_readout_signed;MISSING_measure_coframe_time_qbasic_signed;MISSING_EM_qbasic_or_flux_retained_signed;MISSING_theta_representation_superselection_signed;MISSING_no_source_only_weights_signed;MISSING_no_kappa_A_source_selector_signed;MISSING_no_hidden_marker_source_signed;MISSING_matter_labels_fixed_or_on_shell_signed;MISSING_no_boundary_source_layer_signed;MISSING_nonHilbert_current_zero_signed;MISSING_no_readout_mask_signed;MISSING_no_measured_GM_absorption_signed |
| VAL4840_07_live_bound_blocked | PASS | MISSING_E_action_pullback_abs;MISSING_delta_w_species_abs;MISSING_kappa_A_source_abs;MISSING_hidden_marker_source_abs;MISSING_E_measure_qbasic_abs;MISSING_E_tau_frame_abs;MISSING_E_EM_qbasic_abs;MISSING_E_theta_abs;MISSING_E_matter_lift_abs;MISSING_E_boundary_source_abs;MISSING_E_nonHilbert_bypass_abs;MISSING_E_readout_mask_abs;MISSING_P_density_qbar_abs;MISSING_Qbar_source_XH_bound_abs;MISSING_K_source_abs;MISSING_tau_BY5_density_abs |
| VAL4840_08_density_smoke_values | PASS | density bound smoke row computes expected source-action and density feed |
| VAL4840_09_vertical_smoke_values | PASS | vertical profile smoke row computes expected residual feed |
| VAL4840_10_forbidden_routes_fail | PASS | all forbidden shortcuts fail |
| VAL4840_11_next_target_recorded | PASS | next target recorded in CSV and resume |
| VAL4840_12_no_pycache_left | PASS | scripts __pycache__ removed |

## What changed

- The live local-source problem is now narrowed from “coupling” to a parent matter-grammar theorem.
- The runner distinguishes source-action residual, full density-qbasic residual, and vertical-profile residual.
- The most dangerous countermodel is isolated: relative source-only action-density weights or active-source selectors.

## Next target

`4841-Y5-R2FR-single-action-density-line-no-source-only-weight-theorem-or-first-delta-w-row.md`
