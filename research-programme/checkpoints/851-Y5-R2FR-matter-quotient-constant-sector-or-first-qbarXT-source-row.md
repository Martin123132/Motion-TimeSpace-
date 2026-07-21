# 4835 Y5 R2FR matter quotient constant sector or first qbarXT source row

**Status:** 4835 makes the test-body coupling leg executable. The quotient chain-rule can kill geometry coupling, but `qbar_XT=0` still needs parent-signed observed geometry, matter grammar, constants, markers, source support, source-current and non-Hilbert current clauses. Otherwise the first `qbar_XT` source row is retained.

**Decision:** `MATTER_QUOTIENT_CONSTANT_SECTOR_UNSIGNED_FIRST_QBARXT_SOURCE_ROW_STAGED_NONCLAIM`.

**Claim ceiling:** no local-GR, Newtonian, R10, WEP, PPN, clock, EM, source-charge, qbar-zero, or matter-quotient claim is allowed from 4835.

## Core derivation

```text
S_matter = Sbar_m[Obs(q(Phi)), Psi, theta_A]
Dq[v_X] = 0

delta_v S_matter =
  (delta Sbar_m/dE_obs) DObs(Dq[v_X])
  + (partial Sbar_m/partial theta_A) delta_v theta_A
  + marker/lift/worldtube/boundary/direct-current terms

qbar_XT_bound =
  A_geom + A_theta + A_lift + A_marker + A_direct
  + A_worldtube + A_boundary + A_source_weight + A_nonHilbert

alpha_source = K_source Qbar_source_XH_bound qbar_XT_bound
```

## Source register

| source_id | exists | needle_found | role |
| --- | --- | --- | --- |
| SRC4835_00_resume | True | True | 4834 selected this qbarXT target. |
| SRC4835_01_4834_doc | True | True | source-coupling handoff. |
| SRC4835_02_637_chain | True | True | matter chain-rule descent. |
| SRC4835_03_637_constants | True | True | constant-sector descent criterion. |
| SRC4835_04_637_status | True | True | EM/charge constant blocker. |
| SRC4835_05_621_normal | True | True | normal-form constant clause. |
| SRC4835_06_621_decision | True | True | normal form not parent-derived. |
| SRC4835_07_622_contract | True | True | parent matter contract constants. |
| SRC4835_08_622_alpha | True | True | alpha_EM placeholder row. |
| SRC4835_09_618_zero | True | True | qbarXT conditional zero. |
| SRC4835_10_637_qmap | True | True | vertical kernel quotient map. |
| SRC4835_11_621_normal_csv | True | True | normal form CSV. |
| SRC4835_12_621_clauses | True | True | constant proof obligation. |
| SRC4835_13_621_components | True | True | qbarXT component status. |
| SRC4835_14_621_priors | True | True | alpha_EM prior template. |
| SRC4835_15_621_arenas | True | True | clocks/EM arena dependency. |
| SRC4835_16_622_contract_csv | True | True | parent matter contract CSV. |
| SRC4835_17_622_smoke | True | True | prior smoke row. |
| SRC4835_18_2611_chain | True | True | matter descent constants term. |
| SRC4835_19_2611_premise | True | True | descent premise constants. |
| SRC4835_20_2611_interface | True | True | A_theta bound interface. |
| SRC4835_21_2612_grammar | True | True | no direct matter X grammar. |
| SRC4835_22_2587_contract | True | True | minimal parent matter syntax. |
| SRC4835_23_4834_output | True | True | upstream source-coupling runner. |
| SRC4835_24_runner | True | True | 4835 executable runner. |

## qbarXT zero audit

| clause_id | object | current_result | needed_signature_or_input |
| --- | --- | --- | --- |
| MQC4835_0_qmap | parent quotient map | CONDITIONAL_ONLY | q_map_signed |
| MQC4835_1_observed_geometry | observed geometry functor | NOT_PARENT_SIGNED | observed_geometry_functor_signed |
| MQC4835_2_matter_functor | ordinary matter grammar | CONTRACT_ONLY | matter_functor_signed |
| MQC4835_3_constants | constant/superselection sector | OPEN_BLOCKER | constants_superselection_signed |
| MQC4835_4_marker | material marker taxonomy | OPEN_BLOCKER | no_material_marker_signed |
| MQC4835_5_lift | matter-field vertical lift | OPEN_BLOCKER | matter_lift_signed |
| MQC4835_6_worldtube | worldtube/source support | OPEN_BLOCKER | worldtube_support_signed |
| MQC4835_7_direct | no direct matter X vertex | CONDITIONAL_SCHEMA | no_direct_matter_X_vertex_signed |
| MQC4835_8_universal | universal source current | OPEN_BLOCKER | universal_source_current_signed |
| MQC4835_9_nonHilbert | non-Hilbert currents | OPEN_BLOCKER | nonHilbert_current_zero_signed |
| MQC4835_10_guard | no qbar shortcut | GUARD_ACTIVE | no_cancellation_guard |

## qbarXT source-row contract

| contract_id | quantity | definition | status |
| --- | --- | --- | --- |
| QBC4835_0_zero | qbar_XT=0 | all matter quotient, constant, marker, source and current clauses signed | conditional_only |
| QBC4835_1_direct_bound | qbar_XT_bound | A_geom+A_theta+A_lift+A_marker+A_direct+A_worldtube+A_boundary+A_source_weight+A_nonHilbert | runner_ready_values_missing |
| QBC4835_2_component_bound | qbarXT_vec | P_A*(b_g+b_theta_alpha+b_theta_mass+b_m+b_kappa+b_NH+b_direct+b_worldtube+b_boundary) | runner_ready_values_missing |
| QBC4835_3_alpha | alpha_source | K_source*Qbar_source_XH_bound*qbar_XT_bound | runner_ready_values_missing |
| QBC4835_4_next | theta derivative row | d_ln_alpha_EM_dXhat and d_ln_mass_ratio_dXhat are the next constant-sector knife edge | next_target |

## Runner output

| row_id | runner_status | matter_descent_residual_abs | constant_marker_residual_abs | qbar_XT_bound_abs | alpha_source_abs | BY5_qbar_feed_abs | missing_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RUN4835_0_live_qbarXT_zero_missing | BLOCKED_QBARXT_ZERO_CLAUSES | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_source_signed;MISSING_units_signed;MISSING_same_branch_signed;MISSING_no_cancellation_guard;MISSING_q_map_signed;MISSING_observed_geometry_functor_signed;MISSING_matter_functor_signed;MISSING_constants_superselection_signed;MISSING_no_material_marker_signed;MISSING_matter_lift_signed;MISSING_worldtube_support_signed;MISSING_boundary_no_flux_signed;MISSING_no_direct_matter_X_vertex_signed;MISSING_universal_source_current_signed;MISSING_nonHilbert_current_zero_signed;MISSING_no_post_readout_EFT_signed;MISSING_no_physical_charge_removed_signed;MISSING_no_measured_GM_absorption_signed |
| RUN4835_1_conditional_qbarXT_zero_pass | QBARXT_ZERO_PASS_NONCLAIM | 0.000000000000000e+00 | 0.000000000000000e+00 | 0.000000000000000e+00 | 0.000000000000000e+00 | 0.000000000000000e+00 |  |
| RUN4835_2_forbidden_constants_silent_assertion | FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE |
| RUN4835_3_live_qbarXT_bound_missing | BLOCKED_DIRECT_QBARXT_BOUND_INPUTS | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_A_geom_matter_abs;MISSING_A_theta_matter_abs;MISSING_A_lift_matter_abs;MISSING_A_marker_matter_abs;MISSING_A_direct_matter_abs;MISSING_A_worldtube_matter_abs;MISSING_A_boundary_matter_abs;MISSING_A_source_weight_abs;MISSING_A_nonHilbert_abs;MISSING_Qbar_source_XH_bound_abs;MISSING_K_source_abs;MISSING_tau_BY5_qbar_abs |
| RUN4835_4_direct_qbarXT_smoke_pass | DIRECT_QBARXT_BOUND_PASS_NONCLAIM | 6.000000000000000e-03 | 3.000000000000000e-03 | 9.000000000000001e-03 | 1.991250000000000e-04 | 1.800000000000000e-02 |  |
| RUN4835_5_component_qbarXT_smoke_pass | COMPONENT_QBARXT_BOUND_PASS_NONCLAIM | 6.000000000000000e-03 | 3.000000000000000e-03 | 9.000000000000001e-03 | 1.991250000000000e-04 | 1.800000000000000e-02 |  |
| RUN4835_6_forbidden_closure_only_quotient | FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE |
| RUN4835_7_forbidden_hidden_frame_ignored | FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE |
| RUN4835_8_forbidden_marker_ignored | FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE |
| RUN4835_9_forbidden_direct_vertex_dropped | FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE |
| RUN4835_10_forbidden_qbar_policy_only | FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE |
| RUN4835_11_forbidden_measured_GM_source | FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE |
| RUN4835_12_forbidden_cancellation | FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE |
| RUN4835_13_forbidden_GR_import | FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE |

## Decision ledger

| decision_id | decision | because | next_action |
| --- | --- | --- | --- |
| DEC4835_0_zero | Matter quotient and constant-sector qbarXT zero is still unsigned for live MTS. | The quotient chain-rule is clean, but observed geometry, constants, markers, matter lift, worldtube support and source-current clauses are not all parent-owned. | keep qbarXT zero nonclaim |
| DEC4835_1_bound | The first qbarXT source row is now executable. | If descent fails, qbarXT is the absolute sum of matter, constants, marker, direct, support, boundary, source-weight and non-Hilbert residuals. | source or theorem-zero each qbar component |
| DEC4835_2_next | The next target should attack constant superselection first. | The geometry leg is conditional and the constants leg hits EM, masses, clocks and WEP, making it the cleanest next knife-edge. | 4836-Y5-R2FR-constant-superselection-EM-mass-clock-or-first-theta-derivative-row.md |

## Validation

| validation_id | result | detail |
| --- | --- | --- |
| VAL4835_00_sources_exist | PASS | all cited source paths exist |
| VAL4835_01_needles_found | PASS | all source needles found |
| VAL4835_02_output_count | PASS | all runner rows emitted |
| VAL4835_03_expected_statuses | PASS | runner statuses match expected pass/block/fail modes |
| VAL4835_04_live_zero_blocked | PASS | live qbarXT zero remains blocked |
| VAL4835_05_live_bound_blocked | PASS | live first qbarXT row remains missing |
| VAL4835_06_direct_smoke_pass | PASS | direct qbarXT smoke computes matter/constant split and alpha |
| VAL4835_07_component_smoke_pass | PASS | component qbarXT smoke matches direct envelope |
| VAL4835_08_forbidden_routes_fail | PASS | forbidden shortcuts fail closed |
| VAL4835_09_no_claim_allowed | PASS | no runner row allows a claim |
| VAL4835_10_runner_compiles | PASS | runner compiled before execution |
| VAL4835_11_next_target_written | PASS | next target CSV written |

## Next target

`4836-Y5-R2FR-constant-superselection-EM-mass-clock-or-first-theta-derivative-row.md`
