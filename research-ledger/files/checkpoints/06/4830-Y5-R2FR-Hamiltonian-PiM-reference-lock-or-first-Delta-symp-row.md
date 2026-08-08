# 4830 Y5 R2FR Hamiltonian PiM reference lock or first Delta symp row

**Status:** 4830 makes the Hamiltonian/PiM reference lock executable. The exact path needs parent-owned `L/Theta/Q_tau`, an integrable `H_tau`, derivative-silent `H_ref`, zero or retained boundary/symplectic/projector flux, one time generator, and a positive source-backed `M_H_ref`. Current MTS has not signed those clauses.

**Decision:** `HAMILTONIAN_PIM_REFERENCE_LOCK_UNSIGNED_FIRST_DELTA_SYMP_ROW_STAGED_NONCLAIM`.

**Claim ceiling:** no local-GR, Newtonian, R10, PPN, stable `M_H_ref`, source-charge, measured-GM, or reference-lock claim is allowed from 4830.

## Core equations

```text
delta H_tau[S] = int_S(delta Q_tau - i_tau Theta_total) - delta H_ref[S]
epsilon_ref_boundary = (|Delta_symp|+|H_ref_shift|+|B_zero_flux|+|symplectic_boundary_flux|)/M_H_ref
epsilon_HPiM_integrability = (|delta_H_tau_nonintegrable|+|reference_curl|+|H_ref_shift|
                              +|B_zero_flux|+|Delta_symp|+|symplectic_boundary_flux|
                              +|projector_boundary_flux|+|tau_mismatch|+|Delta_PiM|
                              +|Delta_nonEH|)/M_H_ref
BY5_reference_lock_feed = tau_BY5_ref epsilon_HPiM_integrability
```

## Source register

| source_id | exists | needle_found | role |
| --- | --- | --- | --- |
| SRC4830_00_resume | True | True | 4829 selected this reference-lock target. |
| SRC4830_01_4829_doc | True | True | current denominator handoff. |
| SRC4830_02_1017_lock | True | True | reference-lock law. |
| SRC4830_03_1017_schema | True | True | symplectic boundary row schema. |
| SRC4830_04_1018_boundary | True | True | sector-owner boundary row. |
| SRC4830_05_hci554 | True | True | Hamiltonian integrability obstruction. |
| SRC4830_06_hci_fill | True | True | FB5540 fill row. |
| SRC4830_07_parent_lock_666 | True | True | parent boundary/reference lock attempt. |
| SRC4830_08_source_hunt_666 | True | True | Delta_symp source hunt. |
| SRC4830_09_term_map_667 | True | True | FB5540 term map. |
| SRC4830_10_flux_residual | True | True | source-measure residual map. |
| SRC4830_11_worldtube_runner | True | True | worldtube residual runner. |
| SRC4830_12_4829_output | True | True | upstream MHref selector feed. |
| SRC4830_13_runner | True | True | 4830 executable runner. |

## Reference-lock zero audit

| clause_id | claim_piece | current_result | finite_fallback |
| --- | --- | --- | --- |
| REFZ4830_0_parent_variation | MTS owns L, Theta, Q_tau and constraints | CONTRACT_ONLY | delta_H_tau_nonintegrable row |
| REFZ4830_1_covariant_phase_space | Hamiltonian variation has zero curl | NOT_DERIVED | integrability_curl row |
| REFZ4830_2_reference_lock | H_ref is branch-selected and derivative-silent | FAIL_OPEN | H_ref_shift/Delta_ref row |
| REFZ4830_3_boundary_class | exact/improvement boundary flux is fixed or zero | FAIL_OPEN | B_zero/symplectic_boundary row |
| REFZ4830_4_Delta_symp | reference plus symplectic/projector transfer obstruction vanishes | KEY_BLOCKER | Delta_symp row |
| REFZ4830_5_projector_silence | Pi_M^H is not carrying hidden boundary/symplectic hair | NOT_PARENT_SIGNED | projector_boundary_flux row |
| REFZ4830_6_tau_lock | same observed time generator is used | NOT_PARENT_SIGNED | tau_mismatch row |
| REFZ4830_7_denominator_guard | M_H_ref is positive and source-backed | GUARD_PASS_NO_VALUE | M_H_ref source row |
| REFZ4830_8_anti_circularity | no GR import, measured GM, reference-only zero, or cancellation | POLICY_GUARD | forbidden-source guard |

## Delta-symp contract

| contract_id | quantity | definition | status |
| --- | --- | --- | --- |
| REFC4830_0_zero | epsilon_HPiM_integrability=0 | all Hamiltonian/reference/boundary/projector/tau clauses parent-signed in one branch | conditional_only |
| REFC4830_1_direct_Delta_symp | (Delta_symp+H_ref_shift+B_zero+symplectic_boundary_flux)/M_H_ref | first reference/boundary source row before promoting M_H_ref | runner_ready_values_missing |
| REFC4830_2_component_FB5540 | sum FB5540 reference-lock components/M_H_ref | integrability curl + reference curl + boundary flux + projector + tau + nonEH envelope | runner_ready_values_missing |
| REFC4830_3_BY5 | BY5_reference_lock_feed=tau_BY5_ref epsilon_HPiM_integrability | feeds reference-lock leakage into BY5/source-normalization branch | runner_ready_values_missing |

## Runner output

| row_id | runner_status | Delta_symp_over_MH_abs | Delta_ref_over_MH_abs | epsilon_ref_boundary_abs | epsilon_HPiM_integrability_abs | BY5_reference_lock_feed_abs | missing_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RUN4830_0_live_reference_zero_missing | BLOCKED_REFERENCE_LOCK_ZERO_CLAUSES | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_source_signed;MISSING_units_signed;MISSING_same_branch_signed;MISSING_no_cancellation_guard;MISSING_parent_L_theta_Q_signed;MISSING_covariant_phase_space_identity_signed;MISSING_Hamiltonian_PiM_map_signed;MISSING_integrability_curl_zero_signed;MISSING_reference_superselection_signed;MISSING_H_ref_derivative_silent_signed;MISSING_boundary_class_exact_signed;MISSING_symplectic_boundary_flux_zero_signed;MISSING_projector_silence_signed;MISSING_tau_lock_signed;MISSING_M_H_ref_positive_signed;MISSING_no_readout_mask_signed;MISSING_no_measured_GM_absorption_signed |
| RUN4830_1_conditional_reference_zero_pass | REFERENCE_LOCK_ZERO_PASS_NONCLAIM | 0.000000000000000e+00 | 0.000000000000000e+00 | 0.000000000000000e+00 | 0.000000000000000e+00 | 0.000000000000000e+00 |  |
| RUN4830_2_forbidden_GR_import | FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE |
| RUN4830_3_live_Delta_symp_missing | BLOCKED_DIRECT_DELTA_SYMP_INPUTS | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_M_H_ref_abs;MISSING_Delta_symp_abs;MISSING_H_ref_shift_abs;MISSING_B_zero_flux_abs;MISSING_symplectic_boundary_flux_abs;MISSING_tau_BY5_ref_abs |
| RUN4830_4_direct_Delta_symp_smoke_pass | DIRECT_DELTA_SYMP_ROW_PASS_NONCLAIM | 1.500000000000000e-02 | 5.000000000000000e-03 | 5.000000000000000e-02 | 5.000000000000000e-02 | 1.000000000000000e-01 |  |
| RUN4830_5_component_FB5540_smoke_pass | COMPONENT_FB5540_ROW_PASS_NONCLAIM | 1.500000000000000e-02 | 5.000000000000000e-03 | 5.000000000000000e-02 | 1.000000000000000e-01 | 2.000000000000000e-01 |  |
| RUN4830_6_forbidden_reference_only_zero | FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE |
| RUN4830_7_forbidden_measured_GM_source | FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE |
| RUN4830_8_forbidden_cancellation | FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE |
| RUN4830_9_forbidden_bare_mass_denominator | FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE |

## Decision ledger

| decision_id | decision | because | next_action |
| --- | --- | --- | --- |
| DEC4830_0_reference_lock | Hamiltonian/PiM reference lock is still unsigned for current MTS. | The EH route is a valid template, but MTS still needs its own L/Theta/Q, fixed H_ref, boundary class, projector silence and tau lock. | keep M_H_ref and local-GR promotion blocked |
| DEC4830_1_Delta_symp | Delta_symp is now a first-class source-normalization residual, not a note in the margin. | Reference shift, exact boundary flux, symplectic leakage and projector boundary hair can all move the source charge. | source or zero each numerator before scoring local tests |
| DEC4830_2_next | The next hard target is boundary cohomology/projector silence. | Delta_symp cannot close until boundary exactness/no-hair and PiM boundary orthogonality are parent-owned or bounded. | 4831-Y5-R2FR-boundary-cohomology-projector-silence-or-first-flux-coefficient-row.md |

## Validation

| validation_id | result | detail |
| --- | --- | --- |
| VAL4830_00_sources_exist | PASS | all cited source paths exist |
| VAL4830_01_needles_found | PASS | all source needles found |
| VAL4830_02_output_count | PASS | all runner rows emitted |
| VAL4830_03_expected_statuses | PASS | runner statuses match expected pass/block/fail modes |
| VAL4830_04_live_zero_blocked | PASS | live reference-lock zero remains blocked |
| VAL4830_05_live_delta_symp_blocked | PASS | live Delta_symp row remains missing |
| VAL4830_06_direct_smoke_pass | PASS | direct Delta_symp smoke computes reference-boundary residual |
| VAL4830_07_component_smoke_pass | PASS | component FB5540 smoke computes full retained residual |
| VAL4830_08_forbidden_routes_fail | PASS | forbidden shortcuts fail closed |
| VAL4830_09_no_claim_allowed | PASS | no runner row allows a claim |
| VAL4830_10_runner_compiles | PASS | runner compiled before execution |
| VAL4830_11_next_target_written | PASS | next target CSV written |

## Next target

`4831-Y5-R2FR-boundary-cohomology-projector-silence-or-first-flux-coefficient-row.md`
