# 4828 - Topological Hilbert Equality Or First Req Bzero Row

Marker: `PPC4161_TOPOLOGICAL_HILBERT_EQUALITY_OR_FIRST_REQ_BZERO_ROW_4828`

## Summary

4828 attacks the conserved-wrong-object problem:

```text
Pi_M J_H - J_M_top = dB_zero + R_eq
epsilon_eq_Meff = (|R_eq|+|B_zero|+other retained equality residuals)/M_H_ref
BY5_equality_feed = tau_BY5_Req epsilon_eq_Meff
```

The mathematical route is clean: if `Pi_M J_H` and `J_M_top` are representatives of the same compact Hilbert source-worldtube class, their difference is exact plus a residual, and the residual vanishes when the same-class and zero-boundary premises are parent-signed. The current MTS branch does not yet sign those premises. The finite route is now executable: `R_eq`, `B_zero`, and component equality residuals can feed the source-normalization chain without using a late equality multiplier, reference-only zero, measured `GM`, or cancellation.

## Source register

| source_id | exists | needle_found | role |
| --- | --- | --- | --- |
| SRC4828_00_resume | True | True | 4827 selected this target. |
| SRC4828_01_4827_doc | True | True | current packet handoff. |
| SRC4828_02_1015_sol | True | True | old equality lemma. |
| SRC4828_03_1015_reb | True | True | old residual row. |
| SRC4828_04_1014_req | True | True | commutator checkpoint residual. |
| SRC4828_05_1014_bzero | True | True | boundary exact term residual. |
| SRC4828_06_1013_req | True | True | measured-GM obstruction vector. |
| SRC4828_07_1013_bzero | True | True | boundary flux obstruction. |
| SRC4828_08_top_condition | True | True | topological route condition. |
| SRC4828_09_top_parent | True | True | parent clause attempt. |
| SRC4828_10_top_failure | True | True | wrong conserved object failure. |
| SRC4828_11_top_certificate | True | True | topological equality certificate. |
| SRC4828_12_top_gates | True | True | acceptance gate. |
| SRC4828_13_radial | True | True | radial source-hair input. |
| SRC4828_14_fill | True | True | R_eq fill template. |
| SRC4828_15_bzero_fill | True | True | B_zero fill template. |
| SRC4828_16_worldtube_glue | True | True | worldtube glue blocker. |
| SRC4828_17_worldtube_measure | True | True | source-measure theorem. |
| SRC4828_18_runner | True | True | 4828 executable runner. |

## Zero audit

| clause_id | claim_piece | current_result | finite_fallback |
| --- | --- | --- | --- |
| REQZ4828_0_worldtube | same compact Hilbert source worldtube | NOT_PARENT_SIGNED | Delta_worldtube_domain row |
| REQZ4828_1_source_measure | same observed Hilbert/Noether source measure | NOT_LOCKED | M_H_ref/source-measure row |
| REQZ4828_2_topological_PD | J_M_top is Poincare dual of that worldtube | CONDITIONAL_SHAPE_ONLY | R_eq row |
| REQZ4828_3_same_class | same de Rham compact-support class | KEY_BLOCKER | R_eq_integral row |
| REQZ4828_4_boundary_zero | exact term has zero compact boundary flux | FAIL_OPEN | B_zero_flux row |
| REQZ4828_5_commutator_stress | commutator and projector stress already controlled | PARTIAL_SMOKE_ONLY | 4826/4827 feeds |
| REQZ4828_6_no_extra_exchange | extra projected source channels silent | NOT_PARENT_DERIVED | Delta_extra_vector row |
| REQZ4828_7_calibration_PPN | same charge controls Newton/PPN readout | NOT_REACHED | Delta_cal/Delta_PPN row |
| REQZ4828_8_anti_circularity | no late equality multiplier or measured-GM source | POLICY_GUARD | forbidden-source guard |

## Bound contract

| contract_id | quantity | definition | status |
| --- | --- | --- | --- |
| REQC4828_0_zero | R_eq=B_zero=0 | all same-object and boundary-zero clauses parent-signed in one branch | conditional_only |
| REQC4828_1_direct | (\|R_eq\|+\|B_zero\|)/M_H_ref | first direct equality/boundary residual envelope | runner_ready_values_missing |
| REQC4828_2_component | sum residual components / M_H_ref | R_eq+B_zero+I_commutator+domain+extra+T_PiM+A_parent envelope | runner_ready_values_missing |
| REQC4828_3_BY5 | BY5_equality_feed=tau_BY5_Req epsilon_eq_Meff | feeds same-object failure into BY5/source-normalization branch | runner_ready_values_missing |

## Runner output

| row_id | runner_status | R_eq_norm_abs | B_zero_norm_abs | epsilon_eq_Meff_abs | BY5_equality_feed_abs | missing_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| RUN4828_0_live_zero_missing | BLOCKED_REQ_BZERO_EQUALITY_ZERO_CLAUSES | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_source_signed;MISSING_units_signed;MISSING_same_branch_signed;MISSING_no_cancellation_guard;MISSING_worldtube_fixed_signed;MISSING_source_measure_owned_signed;MISSING_topological_representative_PD_signed;MISSING_same_deRham_class_signed;MISSING_Hilbert_to_PiM_charge_map_signed;MISSING_boundary_zero_flux_signed;MISSING_commutator_zero_signed;MISSING_projector_stress_silence_signed;MISSING_no_extra_exchange_signed;MISSING_calibration_PPN_stable_signed;MISSING_no_readout_mask_signed;MISSING_no_measured_GM_absorption_signed |
| RUN4828_1_conditional_zero_pass | REQ_BZERO_EQUALITY_ZERO_PASS_NONCLAIM | 0.000000000000000e+00 | 0.000000000000000e+00 | 0.000000000000000e+00 | 0.000000000000000e+00 |  |
| RUN4828_2_forbidden_late_multiplier | FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE |
| RUN4828_3_live_direct_bound_missing | BLOCKED_REQ_BZERO_DIRECT_BOUND_INPUTS | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_source_signed;MISSING_units_signed;MISSING_same_branch_signed;MISSING_no_cancellation_guard;MISSING_R_eq_integral_abs;MISSING_B_zero_flux_abs;MISSING_M_H_ref_abs |
| RUN4828_4_direct_Req_Bzero_smoke_pass | REQ_BZERO_DIRECT_BOUND_PASS_NONCLAIM | 1.500000000000000e-02 | 1.000000000000000e-02 | 2.500000000000000e-02 | 3.750000000000001e-02 |  |
| RUN4828_5_component_Req_Bzero_smoke_pass | REQ_BZERO_COMPONENT_BOUND_PASS_NONCLAIM | 1.000000000000000e-02 | 5.000000000000000e-03 | 6.000000000000000e-02 | 1.200000000000000e-01 |  |
| RUN4828_6_forbidden_reference_zero | FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE |
| RUN4828_7_forbidden_measured_GM_source | FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE |
| RUN4828_8_forbidden_cancellation | FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE |

## Decision

`TOPOLOGICAL_HILBERT_EQUALITY_UNSIGNED_FIRST_REQ_BZERO_ROW_STAGED_NONCLAIM`

Next target: `4829-Y5-R2FR-parent-worldtube-source-measure-selector-or-first-MHref-row.md`

## Validation

| validation_id | result | details |
| --- | --- | --- |
| VAL4828_00_sources_exist | PASS | all cited source paths exist |
| VAL4828_01_needles_found | PASS | all source needles found |
| VAL4828_02_live_zero_blocked | PASS | live same-object zero remains blocked |
| VAL4828_03_conditional_zero_pass | PASS | conditional equality zero computes |
| VAL4828_04_late_multiplier_fails | PASS | late equality multiplier fails closed |
| VAL4828_05_live_bound_blocked | PASS | live R_eq/B_zero row missing |
| VAL4828_06_direct_smoke_pass | PASS | direct R_eq/B_zero smoke passes |
| VAL4828_07_component_smoke_pass | PASS | component equality smoke passes |
| VAL4828_08_reference_zero_fails | PASS | reference-only zero fails closed |
| VAL4828_09_measured_GM_fails | PASS | measured-GM shortcut fails closed |
| VAL4828_10_cancellation_fails | PASS | cancellation shortcut fails closed |
| VAL4828_11_no_claim_allowed | PASS | no runner row allows a claim |
