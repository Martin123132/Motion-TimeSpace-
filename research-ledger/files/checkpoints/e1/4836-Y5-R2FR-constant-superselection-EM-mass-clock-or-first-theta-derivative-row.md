# 4836 Y5 R2FR constant superselection EM mass clock or first theta derivative row

**Status:** 4836 narrows the coupling problem to the constant sector. The exact local-zero route is now explicit: `theta_A` is silent only when it is fixed representation/superselection data or descends through the parent quotient. If that is not parent-signed, the theory must retain dimensionless derivative rows for `alpha_EM`, mass ratios, clock ratios and material standards.

**Decision:** `CONSTANT_SUPERSELECTION_UNSIGNED_FIRST_THETA_DERIVATIVE_ROW_STAGED_NONCLAIM`.

**Claim ceiling:** no local-GR, Newtonian, R10, WEP, clock, EM, Maxwell-stress, source-charge, constant-zero, or calibrated-coupling claim is allowed from 4836.

## Core derivation

```text
theta_A = theta_bar_A(q(Phi)) or fixed representation data
Dq[v_X] = 0
=> Lie_v theta_A = D theta_bar_A(Dq[v_X]) = 0

If not parent-signed:

D_v ln theta =
  (d ln alpha_EM/dXhat,
   d ln mass_ratio/dXhat,
   d ln clock_ratio/dXhat,
   d ln material_standard/dXhat)

d ln clock_ratio <= K_alpha d ln alpha_EM
                    + K_mass d ln mass_ratio
                    + K_nuclear d ln nuclear_ratio

A_theta <= ||J_theta||_* (
  S_alpha |d ln alpha_EM|
  + S_mass |d ln mass_ratio|
  + S_clock |d ln clock_ratio|
  + S_material |d ln material_standard|
)

qbar_XT_theta_feed = P_theta_qbar A_theta
alpha_source = K_source Qbar_source_XH_bound qbar_XT_theta_feed
```

## Source register

| source_id | exists | needle_found | role |
| --- | --- | --- | --- |
| SRC4836_00_resume | True | True | 4835 selected this constants target. |
| SRC4836_01_4835_doc | True | True | constant superselection handoff. |
| SRC4836_02_637_descent | True | True | theta descent criterion. |
| SRC4836_03_637_alpha | True | True | EM charge/alpha blocker. |
| SRC4836_04_637_mass | True | True | mass-ratio blocker. |
| SRC4836_05_621_normal | True | True | normal-form constant clause. |
| SRC4836_06_621_alpha | True | True | alpha derivative prior. |
| SRC4836_07_621_clocks | True | True | clock/EM arena dependency. |
| SRC4836_08_622_contract | True | True | parent constant contract. |
| SRC4836_09_622_map_alpha | True | True | alpha prior map. |
| SRC4836_10_622_mass | True | True | mass prior smoke row. |
| SRC4836_11_621_priors_alpha | True | True | source CSV alpha derivative. |
| SRC4836_12_621_priors_mass | True | True | source CSV mass derivative. |
| SRC4836_13_621_arenas | True | True | source CSV clocks/EM arena. |
| SRC4836_14_622_contract_csv | True | True | contract CSV constants. |
| SRC4836_15_622_smoke_alpha | True | True | alpha placeholder row. |
| SRC4836_16_622_smoke_mass | True | True | mass placeholder row. |
| SRC4836_17_2611_chain | True | True | matter descent constants term. |
| SRC4836_18_2611_premise | True | True | constant premise audit. |
| SRC4836_19_2611_interface | True | True | A_theta bound interface. |
| SRC4836_20_2587_contract | True | True | minimal matter syntax. |
| SRC4836_21_4835_output | True | True | upstream qbarXT feed. |
| SRC4836_22_runner | True | True | 4836 executable runner. |

## Constant-sector audit

| clause_id | object | current_result | needed_signature_or_input |
| --- | --- | --- | --- |
| TSC4836_0_descent | theta descent criterion | MATH_CONDITIONAL_PASS | parent classification of each theta_A |
| TSC4836_1_alpha | fine-structure/charge | OPEN_BLOCKER | derive alpha_EM as quotient/topological representation datum or source derivative row |
| TSC4836_2_mass | mass ratios | OPEN_BLOCKER | derive mass-ratio representation theorem or source derivative row |
| TSC4836_3_clock | clock ratios | BOUND_INTERFACE_READY | clock sensitivities plus sourced primitive derivatives |
| TSC4836_4_dimensionless_guard | unit-choice guard | GUARD_ACTIVE | dimensionless source rows |
| TSC4836_5_A_theta | A_theta matter residual | RUNNER_READY_VALUES_MISSING | source-backed derivative and sensitivity coefficients |
| TSC4836_6_source_test | same source/test constants | OPEN_BLOCKER | same-branch certificate |
| TSC4836_7_G_guard | Newton constant/calibration guard | GUARD_ACTIVE | future kappa/source-current derivation |

## Theta derivative contract

| contract_id | quantity | definition | status |
| --- | --- | --- | --- |
| THC4836_0_zero | b_theta=0 | representation category + theta superselection + quotient/topological alpha + mass-ratio theorem + clock ratio theorem | conditional_only |
| THC4836_1_vector | D_v ln theta | (d_ln_alpha_EM_dXhat, d_ln_mass_ratio_dXhat, d_ln_clock_ratio_dXhat, d_ln_material_standard_dXhat) | first_source_row_schema |
| THC4836_2_clock | clock sensitivity projection | d_ln_nu_clock <= K_alpha d_ln_alpha + K_mass d_ln_mu + K_nuclear d_ln_nuclear | runner_ready |
| THC4836_3_A_theta | A_theta_matter | \|\|J_theta\|\|_* \|\|D_v ln theta\|\|_sensitivity | runner_ready_values_missing |
| THC4836_4_qbar | qbar_XT theta feed | P_theta_qbar A_theta -> alpha_source=K Qbar qbar_theta | runner_ready_values_missing |
| THC4836_5_next | EM stress/Poynting alpha branch | derive Maxwell stress/charge normal form or source d_ln_alpha row | next_target |

## Runner output

| row_id | runner_status | theta_log_residual_abs | clock_ratio_bound_abs | A_theta_matter_abs | qbar_XT_theta_feed_abs | alpha_source_abs | BY5_theta_feed_abs | missing_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| RUN4836_0_live_theta_zero_missing | BLOCKED_THETA_ZERO_CLAUSES | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_source_signed;MISSING_dimensionless_units_signed;MISSING_same_branch_signed;MISSING_no_cancellation_guard;MISSING_representation_category_signed;MISSING_theta_superselection_signed;MISSING_vertical_theta_derivative_zero_signed;MISSING_alpha_EM_quotient_or_topological_signed;MISSING_mass_ratios_representation_signed;MISSING_clock_ratios_from_same_theta_signed;MISSING_no_X_running_coupling_slot_signed;MISSING_no_unit_rescaling_of_dimensionless_observables_signed;MISSING_no_material_marker_theta_signed;MISSING_no_clock_readout_absorption_signed;MISSING_same_theta_for_source_and_test_signed;MISSING_no_measured_GM_absorption_signed |
| RUN4836_1_conditional_theta_zero_pass | THETA_ZERO_PASS_NONCLAIM | 0.000000000000000e+00 | 0.000000000000000e+00 | 0.000000000000000e+00 | 0.000000000000000e+00 | 0.000000000000000e+00 | 0.000000000000000e+00 |  |
| RUN4836_2_live_theta_bound_missing | BLOCKED_DIRECT_THETA_DERIVATIVE_INPUTS | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_J_theta_norm_abs;MISSING_d_ln_alpha_EM_dXhat_abs;MISSING_S_alpha_abs;MISSING_d_ln_mass_ratio_dXhat_abs;MISSING_S_mass_abs;MISSING_d_ln_clock_ratio_dXhat_abs;MISSING_S_clock_abs;MISSING_d_ln_material_standard_dXhat_abs;MISSING_S_material_abs;MISSING_P_theta_qbar_abs;MISSING_Qbar_source_XH_bound_abs;MISSING_K_source_abs;MISSING_tau_BY5_theta_abs |
| RUN4836_3_direct_theta_bound_smoke_pass | DIRECT_THETA_DERIVATIVE_BOUND_PASS_NONCLAIM | 2.400000000000000e-03 | 4.000000000000000e-04 | 4.800000000000000e-03 | 4.800000000000000e-03 | 1.062000000000000e-04 | 9.600000000000001e-03 |  |
| RUN4836_4_clock_sensitivity_smoke_pass | CLOCK_SENSITIVITY_THETA_BOUND_PASS_NONCLAIM | 2.400000000000000e-03 | 4.000000000000001e-04 | 4.800000000000000e-03 | 4.800000000000000e-03 | 1.062000000000000e-04 | 9.600000000000001e-03 |  |
| RUN4836_5_forbidden_constants_asserted_silent | FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE |
| RUN4836_6_forbidden_unit_rescaling | FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE |
| RUN4836_7_forbidden_bare_dimensionful_constant | FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE |
| RUN4836_8_forbidden_clock_readout_absorption | FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE |
| RUN4836_9_forbidden_measured_GM_source | FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE |
| RUN4836_10_forbidden_source_test_split_ignored | FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE |
| RUN4836_11_forbidden_charge_normalization_cheat | FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE |
| RUN4836_12_forbidden_cancellation | FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE |
| RUN4836_13_forbidden_GR_import | FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE |

## Decision ledger

| decision_id | decision | because | next_action |
| --- | --- | --- | --- |
| DEC4836_0_zero | Constant superselection has a clean conditional theorem but is not live-signed. | If theta_A is fixed representation data or descends through q, Lie_v theta_A=0; current corpus has not classified alpha_EM, mass ratios and clocks that way. | keep b_theta zero nonclaim |
| DEC4836_1_bound | The first theta derivative source row is executable. | If superselection fails, alpha_EM, mass-ratio, clock-ratio and material-standard derivatives feed A_theta and then qbar_XT. | source or theorem-zero each theta derivative |
| DEC4836_2_guard | Dimensionful constants and measured GM cannot be used as shortcuts. | Only dimensionless observables/ratios can test constant variation; kappa/Newton-G ownership belongs to the separate source-current branch. | do not use unit rescaling or measured GM as proof |
| DEC4836_3_next | The next target should attack EM stress/Poynting/alpha. | alpha_EM is the sharpest constant-sector bridge into Maxwell/EM stress and the user's Poynting-vector intuition. | 4837-Y5-R2FR-EM-stress-Poynting-alpha-normal-form-or-source-row.md |

## Validation

| validation_id | result | detail |
| --- | --- | --- |
| VAL4836_00_sources_exist | PASS | all cited source paths exist |
| VAL4836_01_needles_found | PASS | all source needles found |
| VAL4836_02_output_count | PASS | all runner rows emitted |
| VAL4836_03_expected_statuses | PASS | runner statuses match expected pass/block/fail modes |
| VAL4836_04_live_zero_blocked | PASS | live b_theta zero remains blocked |
| VAL4836_05_live_bound_blocked | PASS | live theta derivative row remains missing |
| VAL4836_06_direct_smoke_pass | PASS | direct theta smoke computes A_theta and qbar feed |
| VAL4836_07_clock_smoke_pass | PASS | clock sensitivity smoke derives same theta envelope |
| VAL4836_08_forbidden_routes_fail | PASS | forbidden shortcuts fail closed |
| VAL4836_09_no_claim_allowed | PASS | no runner row allows a claim |
| VAL4836_10_runner_compiles | PASS | runner compiled before execution |
| VAL4836_11_next_target_written | PASS | next target CSV written |

## Next target

`4837-Y5-R2FR-EM-stress-Poynting-alpha-normal-form-or-source-row.md`
