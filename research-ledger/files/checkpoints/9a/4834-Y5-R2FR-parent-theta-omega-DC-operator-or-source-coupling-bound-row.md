# 4834 Y5 R2FR parent theta omega DC operator or source coupling bound row

**Status:** 4834 makes the actual coupling hinge executable. The category-correct owner identity is `DC_X^dagger eta = Omega_Y^flat(v_eta)`. Current MTS has not signed the parent `theta/Omega/DC/vertical/matter/constants` chain, so the fallback is an explicit source-coupling residual bound.

**Decision:** `PARENT_THETA_OMEGA_DC_UNSIGNED_SOURCE_COUPLING_BOUND_ROW_STAGED_NONCLAIM`.

**Claim ceiling:** no local-GR, Newtonian, R10, R11, PPN, source-charge, source-coupling-zero, or qbar/theta/Omega/DC claim is allowed from 4834.

## Core derivation

```text
delta L_parent = E_A deltaY^A + d theta_Y(deltaY)
Omega_Y = delta theta_Y
delta G_eta[deltaY] = <eta, DC_X[deltaY]> + delta Q_X
                    = <DC_X^dagger eta, deltaY> + B_DC[eta,deltaY]
Hamiltonian owner condition:
    DC_X^dagger eta = Omega_Y^flat(v_eta)

source_coupling_residual =
    |Omega-DCdagger| + |unmapped v| + |B_DC| + |B_ct mismatch|
    + |reduced degeneracy| + |delta_v S_matter| + |delta_v theta_A|

qbar_XT_bound = |delta_v S_matter| + |delta_v theta_A|
Qbar_source_XH_bound <= PiM_norm source_coupling_residual/M_H_ref_min
alpha_source = K_source Qbar_source_XH_bound qbar_XT_bound
```

## Source register

| source_id | exists | needle_found | role |
| --- | --- | --- | --- |
| SRC4834_00_resume | True | True | 4833 selected this Theta/Omega/DC target. |
| SRC4834_01_4833_doc | True | True | parent LThetaQ handoff. |
| SRC4834_02_590_precise_map | True | True | DCdagger maps to Omega-flat, not directly to a vector. |
| SRC4834_03_590_omega_gate | True | True | parent Omega gate. |
| SRC4834_04_637_doc | True | True | constant-sector descent criterion. |
| SRC4834_05_669_doc | True | True | source-coupling coefficient route. |
| SRC4834_06_591_dc | True | True | linearized DC operator. |
| SRC4834_07_591_boundary | True | True | DC boundary covector. |
| SRC4834_08_591_dagger | True | True | DCdagger/Omega-flat comparison. |
| SRC4834_09_591_compare | True | True | Omega missing row. |
| SRC4834_10_591_verdict | True | True | formal progress/no certificate verdict. |
| SRC4834_11_590_fields | True | True | field-by-field vertical action map. |
| SRC4834_12_670_omega | True | True | vertical generator certificate. |
| SRC4834_13_670_matter | True | True | matter quotient blocker. |
| SRC4834_14_618_source_zero | True | True | qbar_XT chain-rule theorem. |
| SRC4834_15_637_qmap | True | True | vertical kernel quotient map. |
| SRC4834_16_669_theta | True | True | Theta_X variation ledger. |
| SRC4834_17_669_yukawa | True | True | finite source coupling projection. |
| SRC4834_18_4833_output | True | True | upstream b_X norm runner. |
| SRC4834_19_runner | True | True | 4834 executable runner. |

## Theta/Omega/DC owner audit

| clause_id | object | current_result | needed_signature_or_input |
| --- | --- | --- | --- |
| TOD4834_0_theta | parent symplectic potential | UNSIGNED | theta_Y_signed |
| TOD4834_1_omega | parent presymplectic form | UNSIGNED | omega_Y_signed |
| TOD4834_2_DC | linearized constraint operator | FORMULA_ONLY | DC_X_operator_signed |
| TOD4834_3_DCadjoint | adjoint covector | FORMULA_ONLY | DCdagger_formula_signed |
| TOD4834_4_match | Hamiltonian generator identity | NOT_CLOSED | omega_flat_match_signed |
| TOD4834_5_vertical | vertical action on every field | PARTIAL | vertical_action_all_fields_signed |
| TOD4834_6_boundary | differentiable boundary generator | NOT_DERIVED | boundary_differentiability_signed;Bct_cancels_boundary_covector_signed |
| TOD4834_7_matter | ordinary matter/source descent | CONDITIONAL_ONLY | matter_quotient_signed;constant_sector_descends_signed |
| TOD4834_8_guard | no category/circular shortcut | GUARD_ACTIVE | no_cancellation_guard |

## Source-coupling contract

| contract_id | quantity | definition | status |
| --- | --- | --- | --- |
| SCC4834_0_owner_zero | source_coupling_residual=0 | theta/Omega/DC owner plus matter and constant descent signs all local source legs to zero | conditional_only |
| SCC4834_1_direct_bound | source_coupling_residual | \|Omega-DCdagger\|+\|unmapped v\|+\|B_DC\|+\|Bct mismatch\|+\|degeneracy\|+\|matter quotient\|+\|constant marker\| | runner_ready_values_missing |
| SCC4834_2_qbarXT | qbar_XT_bound | \|matter quotient residual\|+\|constant marker residual\| | runner_ready_values_missing |
| SCC4834_3_Qbar | Qbar_source_XH_bound | PiM_norm*source_coupling_residual/M_H_ref_min | runner_ready_values_missing |
| SCC4834_4_alpha | alpha_source | K_source*Qbar_source_XH_bound*qbar_XT_bound | runner_ready_values_missing |

## Runner output

| row_id | runner_status | source_coupling_residual_abs | Qbar_source_XH_bound_abs | qbar_XT_bound_abs | alpha_source_abs | BY5_source_feed_abs | missing_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RUN4834_0_live_theta_omega_DC_owner_missing | BLOCKED_THETA_OMEGA_DC_OWNER_CLAUSES | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_source_signed;MISSING_units_signed;MISSING_same_branch_signed;MISSING_no_cancellation_guard;MISSING_theta_Y_signed;MISSING_omega_Y_signed;MISSING_DC_X_operator_signed;MISSING_DCdagger_formula_signed;MISSING_omega_flat_match_signed;MISSING_vertical_action_all_fields_signed;MISSING_boundary_differentiability_signed;MISSING_Bct_cancels_boundary_covector_signed;MISSING_reduced_nondegeneracy_signed;MISSING_matter_quotient_signed;MISSING_constant_sector_descends_signed;MISSING_no_physical_charge_removed_signed;MISSING_no_measured_GM_absorption_signed |
| RUN4834_1_conditional_theta_omega_DC_owner_pass | THETA_OMEGA_DC_OWNER_PASS_NONCLAIM | 0.000000000000000e+00 | 0.000000000000000e+00 | 0.000000000000000e+00 | 0.000000000000000e+00 | 0.000000000000000e+00 |  |
| RUN4834_2_forbidden_formula_only_theta | FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE |
| RUN4834_3_live_source_coupling_missing | BLOCKED_DIRECT_SOURCE_COUPLING_BOUND_INPUTS | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_omega_DC_mismatch_abs;MISSING_unmapped_vertical_action_abs;MISSING_boundary_covector_abs;MISSING_Bct_mismatch_abs;MISSING_reduced_degeneracy_residual_abs;MISSING_matter_quotient_residual_abs;MISSING_constant_marker_residual_abs;MISSING_M_H_ref_min_abs;MISSING_PiM_norm_abs;MISSING_K_source_abs;MISSING_tau_BY5_source_abs |
| RUN4834_4_direct_source_coupling_smoke_pass | DIRECT_SOURCE_COUPLING_BOUND_PASS_NONCLAIM | 5.900000000000001e-02 | 1.475000000000000e-02 | 9.000000000000001e-03 | 1.991250000000001e-04 | 2.950000000000001e-02 |  |
| RUN4834_5_component_source_coupling_smoke_pass | COMPONENT_SOURCE_COUPLING_BOUND_PASS_NONCLAIM | 5.900000000000000e-02 | 1.475000000000000e-02 | 9.000000000000001e-03 | 1.991250000000000e-04 | 2.950000000000000e-02 |  |
| RUN4834_6_forbidden_DCdagger_equals_vector | FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE |
| RUN4834_7_forbidden_omega_by_analogy | FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE |
| RUN4834_8_forbidden_DC_operator_inserted | FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE |
| RUN4834_9_forbidden_constants_silent | FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE |
| RUN4834_10_forbidden_measured_GM_source | FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE |
| RUN4834_11_forbidden_cancellation | FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE |
| RUN4834_12_forbidden_GR_import | FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE |

## Decision ledger

| decision_id | decision | because | next_action |
| --- | --- | --- | --- |
| DEC4834_0_owner | Theta/Omega/DC ownership is still unsigned for live MTS. | The category-correct identity is known, but theta, Omega, DC_X, vertical action, boundary differentiability, matter quotient and constants descent are not signed together. | keep theorem-zero source coupling blocked |
| DEC4834_1_bound | The first source-coupling residual bound is now executable. | If owner descent fails, matter/constant coupling becomes qbar_XT_bound and source coupling is retained absolutely. | source or theorem-zero qbar_XT/Qbar/K_source inputs |
| DEC4834_2_next | The next derivation target should attack matter quotient plus constants. | The test-body leg qbar_XT is now the cleanest coupling knife-edge after theta/Omega/DC. | 4835-Y5-R2FR-matter-quotient-constant-sector-or-first-qbarXT-source-row.md |

## Validation

| validation_id | result | detail |
| --- | --- | --- |
| VAL4834_00_sources_exist | PASS | all cited source paths exist |
| VAL4834_01_needles_found | PASS | all source needles found |
| VAL4834_02_output_count | PASS | all runner rows emitted |
| VAL4834_03_expected_statuses | PASS | runner statuses match expected pass/block/fail modes |
| VAL4834_04_live_owner_blocked | PASS | live theta/Omega/DC owner remains blocked |
| VAL4834_05_live_bound_blocked | PASS | live source-coupling bound row remains missing |
| VAL4834_06_direct_smoke_pass | PASS | direct source-coupling smoke computes residual/qbar/Qbar/alpha/BY5 |
| VAL4834_07_component_smoke_pass | PASS | component source-coupling smoke matches direct envelope |
| VAL4834_08_forbidden_routes_fail | PASS | forbidden shortcuts fail closed |
| VAL4834_09_no_claim_allowed | PASS | no runner row allows a claim |
| VAL4834_10_runner_compiles | PASS | runner compiled before execution |
| VAL4834_11_next_target_written | PASS | next target CSV written |

## Next target

`4835-Y5-R2FR-matter-quotient-constant-sector-or-first-qbarXT-source-row.md`
