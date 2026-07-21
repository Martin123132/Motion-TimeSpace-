# 4838 Y5 R2FR kappa G source normalization Newtonian limit gate

**Status:** 4838 makes the local GR/Newton bridge precise. The Poisson coefficient route is available conditionally,

```text
G_eff = kappa_eff c^4/(8*pi)
nabla^2 Phi = 4*pi G_eff rho_H + Delta_Poisson
```

but MTS still cannot claim a local-GR/Newton pass until `rho_H/M_H_ref`, `Pi_M/H_tau`, worldtube support, EM stress inclusion, and the PPN residual vector are parent-signed or source-bounded.

**Decision:** `KAPPA_G_SOURCE_NEWTON_LIMIT_UNSIGNED_SOURCE_DENOMINATOR_STAGED_NONCLAIM`.

## Core derivation

The fair target is not to derive the decimal value of Newton's constant. GR also carries a measured coupling. The competitive MTS target is sharper:

```text
kappa_eff parent-owned or superselected
G_ref = kappa_eff c^4/(8*pi)
T_H, rho_H, M_H_ref from the same observed matter+EM source action
mu_obs = G_ref M_H (1 + epsilon_mu), with epsilon_mu explicit
```

Then the weak-field `00` equation gives the Newton coefficient, while all deviations are forced into named residuals:

```text
source_denominator_residual =
  delta_kappa + delta_Gref + delta_MHref + delta_PiM_Htau
  + delta_worldtube + delta_EM_stress + delta_nonHilbert
  + delta_source_prefactor

Newton_Poisson_residual = source_denominator_residual + delta_Poisson_operator
PPN_local_residual = Newton_Poisson_residual + delta_PPN_vector
qbar_XT_Newton_feed = P_Newton_qbar PPN_local_residual
alpha_source = K_source Qbar_source_XH qbar_XT_Newton_feed
```

## Source Register

| source_id | exists | needle_found | role |
| --- | --- | --- | --- |
| SRC4838_00_resume | True | True | 4837 handoff to kappa/G/Newton gate. |
| SRC4838_01_4837_doc | True | True | EM stress must be included once, not dropped or double-counted. |
| SRC4838_02_4719_poisson | True | True | linearized EH to Poisson bridge. |
| SRC4838_03_4778_mass | True | True | Hamiltonian mass/source residual runner. |
| SRC4838_04_4825_BY5 | True | True | BY5 source-normalization tail. |
| SRC4838_05_4825_output | True | True | live BY5 source row remains blocked. |
| SRC4838_06_4826_output | True | True | PiM commutator live bound remains blocked. |
| SRC4838_07_kappa_status | True | True | kappa/G policy and Newton gate status. |
| SRC4838_08_hilbert_denominator | True | True | Hilbert source denominator status. |
| SRC4838_09_pim_htau | True | True | PiM/Htau zero mechanism status. |
| SRC4838_10_kappa_contract | True | True | EH coefficient and calibrated G contract. |
| SRC4838_11_poisson_gates | True | True | Newton/Poisson gate. |
| SRC4838_12_denominator_bounds | True | True | denominator bound targets. |
| SRC4838_13_poisson_chain | True | True | EH 00 to Poisson theorem chain. |
| SRC4838_14_gref_signature | True | True | no orbital GM absorption guard. |
| SRC4838_15_kappa_gref | True | True | G_ref/product lock identity. |
| SRC4838_16_hilbert_current | True | True | Hilbert source current closure. |
| SRC4838_17_pim_identity | True | True | typed PiM identity-chainmap route. |
| SRC4838_18_density_qbasic | True | True | Hilbert density q-basic pullback route. |
| SRC4838_19_em_source | True | True | EM stress/source calibration gate. |
| SRC4838_20_source_runner | True | True | source-normalization no-cancellation guard. |
| SRC4838_21_poisson_calibration | True | True | Poisson coefficient law. |
| SRC4838_22_kappa_theorem | True | True | Bianchi route for kappa derivative silence. |
| SRC4838_23_kappa_coeffs | True | True | kappa residual coefficient row. |
| SRC4838_24_newton_gm | True | True | active/inertial source mass residual. |
| SRC4838_25_newton_hamiltonian | True | True | same-action Newton source theorem. |
| SRC4838_26_runner | True | True | 4838 executable runner. |

## Zero Audit

| clause_id | object | current_result | needed_signature_or_input |
| --- | --- | --- | --- |
| KGN4838_0_EH_operator | EH/linearized operator | CONDITIONAL_TEMPLATE | parent EH operator or E00/PPN residual row |
| KGN4838_1_kappa | kappa/G_ref constant | ROUTE_EXISTS_UNSIGNED | parent coupling owner and no readout absorption |
| KGN4838_2_product_lock | G_eff product lock | EXACT_IDENTITY_ACTIVE | source scale terms zero/bounded |
| KGN4838_3_Hilbert_source | Hilbert source current | CONDITIONAL_UNSIGNED | same-frame source descent and EM included once |
| KGN4838_4_MHref | M_H_ref positive denominator | LIVE_GAP | worldtube/source-measure selector or finite MHref residual |
| KGN4838_5_PiM_Htau | PiM/H_tau reference lock | PARTIAL_ROUTE_UNSIGNED | commutator/reference-lock/source-support residuals |
| KGN4838_6_no_GM_launder | no measured GM absorption | GUARD_ACTIVE | independent source mass/current and coupling rows |
| KGN4838_7_Poisson_Gauss | Newtonian limit/readout | DERIVED_CONDITIONAL | source denominator plus PPN residual vector must be controlled |
| KGN4838_8_EM_once | EM stress included exactly once | OPEN_FROM_4837 | EM normal form or finite source row |

## Runner Contract

| contract_id | quantity | definition | status |
| --- | --- | --- | --- |
| KGS4838_0_zero | Newton/local-GR source residual zero | all kappa/source/Poisson/PPN clauses signed in same branch | conditional_only |
| KGS4838_1_source_denominator | source_denominator_residual_abs | delta_kappa+delta_Gref+delta_MHref+delta_PiM_Htau+delta_worldtube+delta_EM_stress+delta_nonHilbert+delta_source_prefactor | runner_ready_values_missing |
| KGS4838_2_Newton_Poisson | Newton_Poisson_residual_abs | source_denominator_residual_abs + delta_Poisson_operator | runner_ready_values_missing |
| KGS4838_3_PPN_local | PPN_local_residual_abs | Newton_Poisson_residual_abs + delta_PPN_vector | runner_ready_values_missing |
| KGS4838_4_projection | qbar/alpha/BY5 feed | qbar=P_Newton_qbar*PPN_local; alpha=K_source*Qbar_source_XH*qbar; BY5=tau*qbar | runner_ready_values_missing |
| KGS4838_5_poisson_coefficient | G_eff coefficient residual | delta_kappa+delta_ZH+delta_GN_readout plus E00/MH terms | runner_ready_values_missing |
| KGS4838_6_next | Hilbert source-current descent | attack T_H/rho_H/M_H_ref ownership directly | next_target |

## Runner Output

| row_id | runner_status | source_denominator_residual_abs | Newton_Poisson_residual_abs | PPN_local_residual_abs | qbar_XT_Newton_feed_abs | alpha_source_abs | BY5_Newton_feed_abs | missing_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| RUN4838_0_live_Newton_zero_missing | BLOCKED_NEWTON_SOURCE_ZERO_CLAUSES | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_source_signed;MISSING_units_signed;MISSING_same_branch_signed;MISSING_no_cancellation_guard;MISSING_EH_or_linearized_operator_signed;MISSING_Hilbert_source_current_signed;MISSING_kappa_constant_or_parent_owned_signed;MISSING_Gref_to_GN_readout_signed;MISSING_MHref_positive_same_frame_signed;MISSING_PiM_Htau_chainmap_signed;MISSING_worldtube_support_signed;MISSING_EM_stress_included_once_signed;MISSING_no_nonHilbert_bypass_signed;MISSING_no_source_prefactor_signed;MISSING_Poisson_Gauss_limit_signed;MISSING_PPN_residual_vector_zero_signed;MISSING_no_measured_GM_absorption_signed |
| RUN4838_1_conditional_Newton_zero_pass | NEWTON_SOURCE_ZERO_PASS_NONCLAIM | 0.000000000000000e+00 | 0.000000000000000e+00 | 0.000000000000000e+00 | 0.000000000000000e+00 | 0.000000000000000e+00 | 0.000000000000000e+00 |  |
| RUN4838_2_live_Newton_bound_missing | BLOCKED_NEWTON_SOURCE_BOUND_INPUTS | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_delta_kappa_abs;MISSING_delta_Gref_abs;MISSING_delta_MHref_abs;MISSING_delta_PiM_Htau_abs;MISSING_delta_worldtube_abs;MISSING_delta_EM_stress_abs;MISSING_delta_nonHilbert_abs;MISSING_delta_source_prefactor_abs;MISSING_delta_Poisson_operator_abs;MISSING_delta_PPN_vector_abs;MISSING_P_Newton_qbar_abs;MISSING_Qbar_source_XH_bound_abs;MISSING_K_source_abs;MISSING_tau_BY5_Newton_abs |
| RUN4838_3_direct_Newton_source_bound_smoke_pass | NEWTON_SOURCE_BOUND_PASS_NONCLAIM | 7.800000000000000e-03 | 9.100000000000000e-03 | 1.050000000000000e-02 | 1.050000000000000e-02 | 2.323125000000000e-04 | 2.100000000000000e-02 |  |
| RUN4838_4_poisson_coefficient_smoke_pass | POISSON_COEFFICIENT_BOUND_PASS_NONCLAIM | 8.000000000000000e-04 | 5.100000000000000e-03 | 5.100000000000000e-03 | 5.100000000000000e-03 | 1.128375000000000e-04 | 1.020000000000000e-02 |  |
| RUN4838_5_forbidden_measured_GM_source | FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE |
| RUN4838_6_forbidden_calibrated_G_derived | FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE |
| RUN4838_7_forbidden_source_prefactor_ignored | FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE |
| RUN4838_8_forbidden_PiM_Htau_assertion | FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE |
| RUN4838_9_forbidden_GR_import | FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE |
| RUN4838_10_forbidden_cancellation | FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE |

## Validation

| check_id | status | detail |
| --- | --- | --- |
| VAL4838_00_sources_exist | PASS | all cited source paths exist |
| VAL4838_01_needles_found | PASS | all source needles found |
| VAL4838_02_runner_compiles | PASS | runner compiles |
| VAL4838_03_generator_compiles | PASS | generator compiles |
| VAL4838_04_output_count | PASS | outputs=11 inputs=11 |
| VAL4838_05_claims_false | PASS | runner hard-codes nonclaim rows |
| VAL4838_06_live_zero_blocked | PASS | MISSING_source_signed;MISSING_units_signed;MISSING_same_branch_signed;MISSING_no_cancellation_guard;MISSING_EH_or_linearized_operator_signed;MISSING_Hilbert_source_current_signed;MISSING_kappa_constant_or_parent_owned_signed;MISSING_Gref_to_GN_readout_signed;MISSING_MHref_positive_same_frame_signed;MISSING_PiM_Htau_chainmap_signed;MISSING_worldtube_support_signed;MISSING_EM_stress_included_once_signed;MISSING_no_nonHilbert_bypass_signed;MISSING_no_source_prefactor_signed;MISSING_Poisson_Gauss_limit_signed;MISSING_PPN_residual_vector_zero_signed;MISSING_no_measured_GM_absorption_signed |
| VAL4838_07_live_bound_blocked | PASS | MISSING_delta_kappa_abs;MISSING_delta_Gref_abs;MISSING_delta_MHref_abs;MISSING_delta_PiM_Htau_abs;MISSING_delta_worldtube_abs;MISSING_delta_EM_stress_abs;MISSING_delta_nonHilbert_abs;MISSING_delta_source_prefactor_abs;MISSING_delta_Poisson_operator_abs;MISSING_delta_PPN_vector_abs;MISSING_P_Newton_qbar_abs;MISSING_Qbar_source_XH_bound_abs;MISSING_K_source_abs;MISSING_tau_BY5_Newton_abs |
| VAL4838_08_direct_smoke_values | PASS | direct smoke row computes source, Poisson, PPN, qbar, alpha and BY5 feed |
| VAL4838_09_coefficient_smoke_values | PASS | Poisson coefficient smoke row computes expected values |
| VAL4838_10_forbidden_routes_fail | PASS | all forbidden shortcuts fail |
| VAL4838_11_next_target_recorded | PASS | next target recorded in CSV and resume |
| VAL4838_12_no_pycache_left | PASS | scripts __pycache__ removed |

## What changed

- The old complaint "G/source coupling is missing" is now an executable gate with zero and finite-residual branches.
- `G_eff=kappa_eff c^4/(8*pi)` is treated as the conditional GR/Newton coefficient bridge, not as a fake derivation of the measured number `G`.
- The source-denominator failure is narrowed to same-frame Hilbert source descent, `M_H_ref`, `Pi_M/H_tau`, worldtube support, EM stress, non-Hilbert bypass and PPN residual ownership.
- Smoke rows pass only as nonclaim arithmetic. Live zero and live source-bound rows remain blocked.

## Next target

`4839-Y5-R2FR-Hilbert-source-current-descent-or-first-MHref-source-row.md`
