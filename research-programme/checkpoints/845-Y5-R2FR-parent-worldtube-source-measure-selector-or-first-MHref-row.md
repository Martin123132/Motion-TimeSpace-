# 4829 Y5 R2FR parent worldtube source-measure selector or first MHref row

**Status:** 4829 turns the local source denominator into an executable gate. The exact path is `W_source = closure(supp J_H[tau])` plus `M_H_ref = H_tau[S_outer] - H_ref` with same-frame parent ownership. Current MTS has not signed that path, so the branch stays nonclaim.

**Decision:** `PARENT_WORLDTUBE_SOURCE_MEASURE_UNSIGNED_FIRST_MHREF_ROW_STAGED_NONCLAIM`.

**Claim ceiling:** no local-GR, Newtonian, R10, PPN, source-measure, measured-GM, or `M_H_ref` claim is allowed from 4829.

## Core equations

```text
W_source := closure(supp J_H[tau])
M_H_ref := H_tau[S_outer] - H_ref > 0
epsilon_selector_Meff = (|B_zero|+|Delta_symp|+|H_ref_shift|+|Delta_worldtube|
                         +|Delta_frame|+|coupling_residual|+|R_eq|+|I_commutator|
                         +|T_PiM|+|A_parent|)/M_H_ref
BY5_selector_feed = tau_BY5_MHref epsilon_selector_Meff
```

## Source register

| source_id | exists | needle_found | role |
| --- | --- | --- | --- |
| SRC4829_00_resume | True | True | 4828 selected this source-measure target. |
| SRC4829_01_4828_doc | True | True | current same-object handoff. |
| SRC4829_02_1016_selector | True | True | selector/source-measure clause. |
| SRC4829_03_1016_first_input | True | True | first M_H_ref input schema. |
| SRC4829_04_1017_denominator | True | True | denominator row schema. |
| SRC4829_05_1017_guard | True | True | no bare/orbital mass guard. |
| SRC4829_06_worldtube_glue | True | True | worldtube/exterior charge glue. |
| SRC4829_07_worldtube_measure | True | True | dressed source measure correction. |
| SRC4829_08_flux_residual | True | True | symplectic/reference residual. |
| SRC4829_09_worldtube_runner | True | True | worldtube residual runner. |
| SRC4829_10_4828_output | True | True | upstream equality runner feed. |
| SRC4829_11_runner | True | True | 4829 executable runner. |

## Selector zero audit

| clause_id | claim_piece | current_result | finite_fallback |
| --- | --- | --- | --- |
| MHZ4829_0_parent_action | parent action owns the source current and observed time flow | CONTRACT_WRITTEN_NOT_PARENT_SIGNED | parent action covariant source row |
| MHZ4829_1_worldtube_selector | compact source worldtube is selected by Hilbert support | FORMAL_SELECTOR_ONLY | Delta_worldtube_domain row |
| MHZ4829_2_same_frame_measure | source, charge, clock, and readout share one observed frame | FAIL_OPEN | Delta_frame_source row |
| MHZ4829_3_Htau_integrable | Hamiltonian variation is integrable on the selected branch | NOT_DERIVED | delta_H_tau_nonintegrable row |
| MHZ4829_4_Href_lock | reference subtraction cannot absorb source calibration | NOT_DERIVED | H_ref_shift row |
| MHZ4829_5_MHref_denominator | positive source denominator is parent-owned | KEY_BLOCKER | first M_H_ref row |
| MHZ4829_6_PiM_Hamiltonian_map | Pi_M is the Hamiltonian mass-charge map | NOT_PARENT_SIGNED | PiM/Hamiltonian map certificate |
| MHZ4829_7_boundary_reference_lock | exact/boundary/symplectic terms are zero or retained | FAIL_OPEN | boundary/reference residual rows |
| MHZ4829_8_coupling_descent | matter coupling descends without hidden readout coefficients | NOT_SIGNED | coupling_residual row |
| MHZ4829_9_anti_circularity | no bare mass, measured GM, reference-only zero, or cancellation | POLICY_GUARD | forbidden-source guard |

## MHref contract

| contract_id | quantity | definition | status |
| --- | --- | --- | --- |
| MHC4829_0_selector_zero | epsilon_selector_Meff=0 | all selector, integrability, reference, frame, coupling and PiM clauses parent-signed in one branch | conditional_only |
| MHC4829_1_direct_MHref | M_H_ref=H_tau[S_outer]-H_ref | first source-backed denominator row with units, reference rule and source path | runner_ready_values_missing |
| MHC4829_2_component_selector | epsilon_selector_Meff=sum retained source-selector residuals/M_H_ref | B_zero+Delta_symp+H_ref+worldtube+frame+coupling+R_eq+I_commutator+T_PiM+A_parent envelope | runner_ready_values_missing |
| MHC4829_3_BY5 | BY5_selector_feed=tau_BY5_MHref epsilon_selector_Meff | feeds source-measure leakage into the same BY5/source-normalization branch | runner_ready_values_missing |

## Runner output

| row_id | runner_status | M_H_ref_abs | M_H_ref_mismatch_abs | epsilon_selector_Meff_abs | BY5_selector_feed_abs | missing_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| RUN4829_0_live_selector_zero_missing | BLOCKED_PARENT_SELECTOR_MHREF_ZERO_CLAUSES | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_source_signed;MISSING_units_signed;MISSING_same_branch_signed;MISSING_no_cancellation_guard;MISSING_parent_action_covariant_signed;MISSING_observed_tau_signed;MISSING_same_frame_source_measure_signed;MISSING_compact_worldtube_support_signed;MISSING_linking_surfaces_fixed_signed;MISSING_Htau_integrability_signed;MISSING_H_ref_fixed_signed;MISSING_M_H_ref_positive_signed;MISSING_PiM_Hamiltonian_map_signed;MISSING_boundary_reference_lock_signed;MISSING_coupling_descent_silence_signed;MISSING_no_readout_mask_signed;MISSING_no_measured_GM_absorption_signed |
| RUN4829_1_conditional_selector_zero_pass | PARENT_SELECTOR_MHREF_ZERO_PASS_NONCLAIM | THEOREM_POSITIVE_DEFINED | 0.000000000000000e+00 | 0.000000000000000e+00 | 0.000000000000000e+00 |  |
| RUN4829_2_forbidden_bare_mass_shortcut | FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE |
| RUN4829_3_live_MHref_missing | BLOCKED_DIRECT_MHREF_INPUTS | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_H_tau_outer_abs;MISSING_H_ref_abs;MISSING_M_H_ref_abs;MISSING_reference_tolerance_abs |
| RUN4829_4_direct_MHref_smoke_pass | DIRECT_MHREF_ROW_PASS_NONCLAIM | 2.000000000000000e+00 | 0.000000000000000e+00 | 0.000000000000000e+00 | 0.000000000000000e+00 |  |
| RUN4829_5_component_selector_smoke_pass | COMPONENT_SELECTOR_ROW_PASS_NONCLAIM | 2.000000000000000e+00 | MISSING_NUMERIC_VALUE | 9.000000000000000e-02 | 1.800000000000000e-01 |  |
| RUN4829_6_forbidden_reference_only_zero | FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE |
| RUN4829_7_forbidden_measured_GM_source | FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE |
| RUN4829_8_forbidden_cancellation | FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE |

## Decision ledger

| decision_id | decision | because | next_action |
| --- | --- | --- | --- |
| DEC4829_0_selector | The parent worldtube/source-measure selector is still unsigned. | The exact route is mathematically well-formed but needs parent ownership of J_H, tau, H_tau, H_ref, Pi_M^H and coupling descent. | keep local-GR/Newton claims blocked until signed or bounded |
| DEC4829_1_MHref | M_H_ref is now the required denominator row, not a hidden normalization. | R_eq/B_zero/I_commutator/T_PiM rows cannot be scored against measured GM, bare mass, or reference-only one. | source H_tau/H_ref/M_H_ref or carry selector residuals |
| DEC4829_2_next | The next hard target is Hamiltonian PiM reference/boundary lock. | M_H_ref depends on integrability, reference subtraction, and Delta_symp/B_zero boundary ownership. | 4830-Y5-R2FR-Hamiltonian-PiM-reference-lock-or-first-Delta-symp-row.md |

## Validation

| validation_id | result | detail |
| --- | --- | --- |
| VAL4829_00_sources_exist | PASS | all cited source paths exist |
| VAL4829_01_needles_found | PASS | all source needles found |
| VAL4829_02_output_count | PASS | all runner rows emitted |
| VAL4829_03_expected_statuses | PASS | runner statuses match expected pass/block/fail modes |
| VAL4829_04_live_zero_blocked | PASS | live selector zero remains blocked |
| VAL4829_05_direct_MHref_blocked | PASS | live M_H_ref row remains missing |
| VAL4829_06_smoke_MHref_pass | PASS | direct smoke denominator is internally consistent |
| VAL4829_07_component_smoke_pass | PASS | component smoke computes retained selector residual |
| VAL4829_08_forbidden_routes_fail | PASS | forbidden shortcuts fail closed |
| VAL4829_09_no_claim_allowed | PASS | no runner row allows a claim |
| VAL4829_10_runner_compiles | PASS | runner compiled before execution |
| VAL4829_11_next_target_written | PASS | next target CSV written |

## Next target

`4830-Y5-R2FR-Hamiltonian-PiM-reference-lock-or-first-Delta-symp-row.md`
