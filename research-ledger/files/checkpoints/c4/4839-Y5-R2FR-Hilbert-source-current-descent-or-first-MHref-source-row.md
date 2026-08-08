# 4839 Y5 R2FR Hilbert source current descent or first MHref source row

**Status:** 4839 turns `M_H_ref` into the actual source-current object demanded by 4838. The conditional route is clear: define `T_H` by varying the same observed matter+EM action before readout, build `rho_H dV_H`, and require the Hamiltonian surface charge to equal the volume Hilbert source mass. The live branch remains nonclaim because the parent source-action pullback and first source-backed `M_H_ref` values are not yet supplied.

**Decision:** `HILBERT_SOURCE_CURRENT_DESCENT_UNSIGNED_FIRST_MHREF_SOURCE_ROW_STAGED_NONCLAIM`.

## Core derivation

```text
T_H^{mu nu} = (2/sqrt(-g_obs)) delta S_src[e_obs,A_obs,psi,theta]/delta g_obs_mu_nu
J_H[tau] = T_H^{mu nu} n_mu tau_nu dSigma
rho_H dV_H = n_mu tau_nu T_H^{mu nu} dSigma_H
M_H_ref = H_tau[S_outer] - H_ref = integral_W rho_H dV_H
```

If `S_src=q^*Sbar_src` and the measure/coframe/time/EM source data are q-owned before readout, then `rho_H dV_H` is q-basic. If the Hamiltonian surface charge and the Hilbert volume charge match, `M_H_ref` becomes the source denominator needed by 4838. Otherwise the finite branch is:

```text
source_descent_residual =
  E_action_pullback + E_variation_readout + E_measure_qbasic
  + E_tau_frame + E_EM_once + E_theta_constants
  + E_worldtube_boundary + E_nonHilbert_current
  + E_PiM_Htau + E_readout_mask
```

## Source Register

| source_id | exists | needle_found | role |
| --- | --- | --- | --- |
| SRC4839_00_resume | True | True | 4838 selected this source-current target. |
| SRC4839_01_4838_doc | True | True | Newton bridge handoff. |
| SRC4839_02_4838_output | True | True | live Newton source denominator blocked. |
| SRC4839_03_1016_schema | True | True | first M_H_ref input schema. |
| SRC4839_04_1017_schema | True | True | Hamiltonian denominator schema. |
| SRC4839_05_source_current | True | True | Hilbert current definition contract. |
| SRC4839_06_parent_identity | True | True | Hilbert mass closure residual identity. |
| SRC4839_07_source_measure | True | True | source measure/exterior flux equality. |
| SRC4839_08_Hilbert_def | True | True | same-frame Hilbert current definition. |
| SRC4839_09_Hilbert_closure | True | True | closure sufficient conditions. |
| SRC4839_10_density | True | True | density q-basic pullback theorem. |
| SRC4839_11_countermodel | True | True | source-only weight countermodel. |
| SRC4839_12_active_mass | True | True | active mass equals Hilbert mass conditionally. |
| SRC4839_13_residual | True | True | Hamiltonian-Hilbert residual row. |
| SRC4839_14_4829_output | True | True | live M_H_ref row remains missing. |
| SRC4839_15_4829_contract | True | True | direct M_H_ref contract. |
| SRC4839_16_EM | True | True | EM stress inclusion remains a source clause. |
| SRC4839_17_runner | True | True | 4839 executable runner. |

## Descent Audit

| clause_id | object | current_result | needed_signature_or_input |
| --- | --- | --- | --- |
| HSD4839_0_definition | same-frame Hilbert current | EXACT_CONDITIONAL_DEFINITION | parent source action and q_obs branch |
| HSD4839_1_density | Hilbert source density | EXACT_DEFINITION_UNSIGNED_OWNER | q-basic source action/measure/time/coframe |
| HSD4839_2_pullback | source-action pullback | CORE_UNSIGNED | 4840 source-action signature |
| HSD4839_3_variation | variation before readout | GUARD_ACTIVE | no post-readout mask |
| HSD4839_4_MHref | first M_H_ref source row | RUNNER_READY_VALUES_MISSING | real source-backed H_tau/H_ref/rho_H row |
| HSD4839_5_Hamiltonian | Hamiltonian-Hilbert equality | CONDITIONAL_UNSIGNED | integrability/reference/worldtube/PiM closure |
| HSD4839_6_EM | ordinary EM stress included once | OPEN_FROM_4837 | EM normal form or finite residual row |
| HSD4839_7_anti_circularity | no GM laundering | GUARD_ACTIVE | forbidden-source runner checks |

## Runner Contract

| contract_id | quantity | definition | status |
| --- | --- | --- | --- |
| HSC4839_0_zero | Hilbert source descent zero | all source-action, q-map, variation, q-basic density, worldtube, Hamiltonian and anti-circularity clauses signed | conditional_only |
| HSC4839_1_direct_MHref | M_H_ref source row | H_tau_outer-H_ref equals integral rho_H dV_H equals M_H_ref within tolerances | runner_ready_values_missing |
| HSC4839_2_descent_bound | source_descent_residual_abs | sum retained source-action, variation, qbasic, tau/frame, EM, theta, worldtube, nonHilbert, PiM/Htau and readout-mask residuals | runner_ready_values_missing |
| HSC4839_3_feed | delta_MHref to Newton feed | qbar=P_Newton_qbar*delta_MHref; alpha=K_source*Qbar_source_XH*qbar; BY5=tau*qbar | runner_ready_values_missing |
| HSC4839_4_next | source-action pullback signature | prove or bound S_src=q^*Sbar_src and density q-basicness | next_target |

## Runner Output

| row_id | runner_status | source_descent_residual_abs | M_H_ref_abs | M_H_ref_surface_mismatch_abs | M_H_ref_volume_mismatch_abs | delta_MHref_abs | alpha_source_abs | BY5_MHref_feed_abs | missing_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| RUN4839_0_live_descent_zero_missing | BLOCKED_HILBERT_SOURCE_DESCENT_ZERO_CLAUSES | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_source_signed;MISSING_units_signed;MISSING_same_branch_signed;MISSING_no_cancellation_guard;MISSING_parent_action_diffeomorphic_signed;MISSING_q_observed_map_signed;MISSING_matter_action_pullback_signed;MISSING_variation_before_readout_signed;MISSING_same_frame_tau_n_dSigma_signed;MISSING_Hilbert_density_qbasic_signed;MISSING_compact_worldtube_support_signed;MISSING_Hamiltonian_surface_charge_match_signed;MISSING_H_ref_branch_fixed_signed;MISSING_PiM_identity_chainmap_signed;MISSING_ordinary_EM_stress_included_once_signed;MISSING_no_source_only_weights_signed;MISSING_no_nonHilbert_source_bypass_signed;MISSING_no_boundary_source_layer_signed;MISSING_positive_MHref_signed;MISSING_no_measured_GM_absorption_signed |
| RUN4839_1_conditional_descent_zero_pass | HILBERT_SOURCE_DESCENT_ZERO_PASS_NONCLAIM | 0.000000000000000e+00 | THEOREM_POSITIVE_DEFINED | 0.000000000000000e+00 | 0.000000000000000e+00 | 0.000000000000000e+00 | 0.000000000000000e+00 | 0.000000000000000e+00 |  |
| RUN4839_2_live_MHref_source_missing | BLOCKED_DIRECT_MHREF_SOURCE_INPUTS | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_H_tau_outer_abs;MISSING_H_ref_abs;MISSING_integral_rhoH_abs;MISSING_M_H_ref_abs;MISSING_reference_tolerance_abs;MISSING_volume_tolerance_abs;MISSING_P_Newton_qbar_abs;MISSING_Qbar_source_XH_bound_abs;MISSING_K_source_abs;MISSING_tau_BY5_MHref_abs |
| RUN4839_3_direct_MHref_source_smoke_pass | DIRECT_MHREF_SOURCE_ROW_PASS_NONCLAIM | 0.000000000000000e+00 | 2.000000000000000e+00 | 0.000000000000000e+00 | 1.999999999999780e-03 | 9.999999999998899e-04 | 2.212499999999756e-05 | 1.999999999999780e-03 |  |
| RUN4839_4_live_descent_bound_missing | BLOCKED_HILBERT_SOURCE_DESCENT_BOUND_INPUTS | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_E_action_pullback_abs;MISSING_E_variation_readout_abs;MISSING_E_measure_qbasic_abs;MISSING_E_tau_frame_abs;MISSING_E_EM_once_abs;MISSING_E_theta_constants_abs;MISSING_E_worldtube_boundary_abs;MISSING_E_nonHilbert_current_abs;MISSING_E_PiM_Htau_abs;MISSING_E_readout_mask_abs;MISSING_P_Newton_qbar_abs;MISSING_Qbar_source_XH_bound_abs;MISSING_K_source_abs;MISSING_tau_BY5_MHref_abs |
| RUN4839_5_descent_bound_smoke_pass | HILBERT_SOURCE_DESCENT_BOUND_PASS_NONCLAIM | 8.600000000000000e-03 | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | 8.600000000000000e-03 | 1.902750000000000e-04 | 1.720000000000000e-02 |  |
| RUN4839_6_forbidden_measured_GM_source | FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE |
| RUN4839_7_forbidden_variation_after_readout | FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE |
| RUN4839_8_forbidden_density_assertion | FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE |
| RUN4839_9_forbidden_nonHilbert_bypass | FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE |
| RUN4839_10_forbidden_reference_only_zero | FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE |

## Validation

| check_id | status | detail |
| --- | --- | --- |
| VAL4839_00_sources_exist | PASS | all cited source paths exist |
| VAL4839_01_needles_found | PASS | all source needles found |
| VAL4839_02_runner_compiles | PASS | runner compiles |
| VAL4839_03_generator_compiles | PASS | generator compiles |
| VAL4839_04_output_count | PASS | outputs=11 inputs=11 |
| VAL4839_05_claims_false | PASS | runner hard-codes nonclaim rows |
| VAL4839_06_live_zero_blocked | PASS | MISSING_source_signed;MISSING_units_signed;MISSING_same_branch_signed;MISSING_no_cancellation_guard;MISSING_parent_action_diffeomorphic_signed;MISSING_q_observed_map_signed;MISSING_matter_action_pullback_signed;MISSING_variation_before_readout_signed;MISSING_same_frame_tau_n_dSigma_signed;MISSING_Hilbert_density_qbasic_signed;MISSING_compact_worldtube_support_signed;MISSING_Hamiltonian_surface_charge_match_signed;MISSING_H_ref_branch_fixed_signed;MISSING_PiM_identity_chainmap_signed;MISSING_ordinary_EM_stress_included_once_signed;MISSING_no_source_only_weights_signed;MISSING_no_nonHilbert_source_bypass_signed;MISSING_no_boundary_source_layer_signed;MISSING_positive_MHref_signed;MISSING_no_measured_GM_absorption_signed |
| VAL4839_07_live_direct_blocked | PASS | MISSING_H_tau_outer_abs;MISSING_H_ref_abs;MISSING_integral_rhoH_abs;MISSING_M_H_ref_abs;MISSING_reference_tolerance_abs;MISSING_volume_tolerance_abs;MISSING_P_Newton_qbar_abs;MISSING_Qbar_source_XH_bound_abs;MISSING_K_source_abs;MISSING_tau_BY5_MHref_abs |
| VAL4839_08_direct_MHref_smoke_values | PASS | direct MHref smoke row computes surface/volume mismatch and feed |
| VAL4839_09_descent_bound_smoke_values | PASS | descent bound smoke row computes expected residual feed |
| VAL4839_10_forbidden_routes_fail | PASS | all forbidden shortcuts fail |
| VAL4839_11_next_target_recorded | PASS | next target recorded in CSV and resume |
| VAL4839_12_no_pycache_left | PASS | scripts __pycache__ removed |

## What changed

- The source denominator is now explicitly `M_H_ref=H_tau-H_ref=integral rho_H dV_H`, not bare mass or orbital `GM`.
- The runner can test a theorem-zero route, a direct first source row, or a finite source-descent residual.
- The live branch remains blocked, but the exact missing object is smaller: source-action pullback plus density q-basicness.

## Next target

`4840-Y5-R2FR-source-action-pullback-signature-or-first-density-qbasic-bound-row.md`
