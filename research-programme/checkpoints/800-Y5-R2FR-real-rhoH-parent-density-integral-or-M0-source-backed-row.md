# 4784 - Real rhoH parent density integral or M0 source-backed row

Marker: `PPC4161_REAL_RHOH_PARENT_DENSITY_INTEGRAL_OR_M0_SOURCE_BACKED_ROW_4784`
Generated: `2026-07-08T04:58:35+00:00`
Decision: `RHOH_PARENT_DENSITY_INTEGRAL_ASSEMBLER_INSTALLED_SELF_DENOMINATOR_LAW_DERIVED_REAL_NUMERIC_PROFILE_STILL_MISSING_NONCLAIM`

## Result

4784 removes one fake degree of freedom from the local source-mass branch. `M0` does not need to be an extra axiom if the same parent branch supplies a positive Hilbert density integral:

```text
rho_H(W_H) = c^-2 int_W T_total(n,n) dV_eobs
H_tau_bulk = rho_H(W_H) + H_tau_surface_center
M0 = H_tau_bulk - H_ref
epsilon_abs = Delta_H_abs/M0
M_lower = M0(1-epsilon_abs).
```

This is still not a local-GR or Newton claim because the live physical row has no numeric/source-backed `rho_H(W_H)` profile integral. The useful gain is that independent `M0` has been demoted: either it is the positive Hilbert source integral itself, or an external source-backed value must be supplied without using observed orbital `GM`.

## rhoH/M0 Law Rows

| law_id | formula | meaning |
| --- | --- | --- |
| RML4784_0_rhoH_integral | rho_H(W_H)=c^-2 int_{W_H} T_total(n,n)dV_eobs | defines the real parent density integral from the same Hilbert stress |
| RML4784_1_Htau_bulk | H_tau_bulk=rho_H(W_H)+H_tau_surface_center | turns the density integral into the parent H_tau bulk row |
| RML4784_2_M0_self | M0=H_tau_bulk-H_ref when H_ref is fixed and the Hilbert energy branch is positive | removes independent M0 as an extra axiom on the signed positive branch |
| RML4784_3_Mlower | epsilon_abs=Delta_H_abs/M0 and M_lower=M0(1-epsilon_abs) | makes positivity a residual-radius inequality |
| RML4784_4_firewall | orbital GM, fitted acceleration, and post-fit reference subtraction cannot source rho_H or M0 | keeps source mass from being read backward out of the test |

## rhoH Runner Output

| density_id | rho_H_integral_kg | H_tau_bulk_kg | M0_kg | epsilon_abs | M_lower_kg | runner_status |
| --- | --- | --- | --- | --- | --- | --- |
| physical_candidate_parent_density_law_values_missing | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | BLOCKED_MISSING_RHOH_NUMERIC_INTEGRAL |
| private_positive_density_self_denominator_control | 1.000000000000000e+00 | 1.000000000000000e+00 | 1.000000000000000e+00 | 0.000000000000000e+00 | 1.000000000000000e+00 | RHOH_SELF_DENOMINATOR_EXACT_PRIVATE_NONCLAIM |
| finite_residual_self_denominator_smoke_nonclaim | 1.988409870698051e+30 | 1.988409870698051e+30 | 1.988409870698051e+30 | 2.000000000000000e-02 | 1.948641673284090e+30 | RHOH_PARENT_INTEGRAL_INTERVAL_COMPUTED_NONCLAIM |
| external_M0_without_rho_integral_control | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | 1.000000000000000e+00 | 0.000000000000000e+00 | MISSING_NUMERIC_VALUE | BLOCKED_MISSING_RHOH_NUMERIC_INTEGRAL |
| forbidden_orbital_GM_M0_control | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | FAILED_CIRCULAR_RHOH_OR_M0_SOURCE |
| counterfactual_rhoH_equals_comparator | 1.988409870698051e+30 | 1.988409870698051e+30 | 1.988409870698051e+30 | 0.000000000000000e+00 | 1.988409870698051e+30 | RHOH_COUNTERFACTUAL_SMOKE_PASS_NONCLAIM |

## Density Runner Output

| density_id | H_tau_bulk_kg | H_ref_kg | M_lower_kg | Delta_H_abs_kg | runner_status |
| --- | --- | --- | --- | --- | --- |
| physical_candidate_parent_density_law_values_missing | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | BLOCKED_MISSING_DENSITY_CURRENT_COMPONENTS |
| private_positive_density_self_denominator_control | 1.000000000000000e+00 | 0.000000000000000e+00 | 1.000000000000000e+00 | 0.000000000000000e+00 | DENSITY_CURRENT_EXACT_COMPUTED_NONCLAIM |
| finite_residual_self_denominator_smoke_nonclaim | 1.988409870698051e+30 | 0.000000000000000e+00 | 1.948641673284090e+30 | 3.976819741396102e+28 | DENSITY_CURRENT_INTERVAL_COMPUTED_NONCLAIM |
| external_M0_without_rho_integral_control | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | BLOCKED_MISSING_DENSITY_CURRENT_COMPONENTS |
| forbidden_orbital_GM_M0_control | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | FAILED_CIRCULAR_DENSITY_CURRENT_SOURCE |
| counterfactual_rhoH_equals_comparator | 1.988409870698051e+30 | 0.000000000000000e+00 | 1.988409870698051e+30 | 0.000000000000000e+00 | DENSITY_CURRENT_COUNTERFACTUAL_SMOKE_PASS_NONCLAIM |

## Chain Score

| density_id | rhoh_runner_status | density_runner_status | parent_runner_status | source_runner_status | open_runner_status |
| --- | --- | --- | --- | --- | --- |
| physical_candidate_parent_density_law_values_missing | BLOCKED_MISSING_RHOH_NUMERIC_INTEGRAL | BLOCKED_MISSING_DENSITY_CURRENT_COMPONENTS | BLOCKED_MISSING_PARENT_CHARGE_COMPONENTS | BLOCKED_MISSING_HTAU_OR_HREF | BLOCKED_MISSING_MHDRESS |
| private_positive_density_self_denominator_control | RHOH_SELF_DENOMINATOR_EXACT_PRIVATE_NONCLAIM | DENSITY_CURRENT_EXACT_COMPUTED_NONCLAIM | PARENT_CHARGE_EXACT_COMPUTED_NONCLAIM | MHDRESS_COMPUTED_NONCLAIM | RUNNER_NUMERIC_FAIL_OR_TOLERANCE_MISSING_NONCLAIM |
| finite_residual_self_denominator_smoke_nonclaim | RHOH_PARENT_INTEGRAL_INTERVAL_COMPUTED_NONCLAIM | DENSITY_CURRENT_INTERVAL_COMPUTED_NONCLAIM | PARENT_CHARGE_INTERVAL_COMPUTED_NONCLAIM | MHDRESS_COMPUTED_NONCLAIM | RUNNER_NUMERIC_PASS_NONCLAIM |
| external_M0_without_rho_integral_control | BLOCKED_MISSING_RHOH_NUMERIC_INTEGRAL | BLOCKED_MISSING_DENSITY_CURRENT_COMPONENTS | BLOCKED_MISSING_PARENT_CHARGE_COMPONENTS | BLOCKED_MISSING_HTAU_OR_HREF | BLOCKED_MISSING_MHDRESS |
| forbidden_orbital_GM_M0_control | FAILED_CIRCULAR_RHOH_OR_M0_SOURCE | FAILED_CIRCULAR_DENSITY_CURRENT_SOURCE | BLOCKED_MISSING_PARENT_CHARGE_COMPONENTS | BLOCKED_MISSING_HTAU_OR_HREF | BLOCKED_MISSING_MHDRESS |
| counterfactual_rhoH_equals_comparator | RHOH_COUNTERFACTUAL_SMOKE_PASS_NONCLAIM | DENSITY_CURRENT_COUNTERFACTUAL_SMOKE_PASS_NONCLAIM | PARENT_CHARGE_COUNTERFACTUAL_SMOKE_PASS_NONCLAIM | MHDRESS_COUNTERFACTUAL_SMOKE_PASS_NONCLAIM | RUNNER_SMOKE_PASS_NONCLAIM |

## Route Selection

| route_id | route | selection_status |
| --- | --- | --- |
| RT4784_0_profile | fill a real source-profile T_total(n,n) integral over W_H | SELECTED_NEXT |
| RT4784_1_residual_radius | source R_eq/B_zero/boundary/open-EM/projector/domain/kappa residual radius | SELECTED_NEXT_PARALLEL |
| RT4784_2_parent_signature | promote the 3883/4587 source action clauses from conditional to parent-signed | SELECTED_NEXT_PARALLEL |

## Conclusion

The branch is tighter, not looser. `H_ref` is already fixed by 4783; 4784 makes `M0` self-derived on the positive Hilbert branch. The remaining real gap is now a source-profile problem: supply `int_W T_total(n,n)dV/c^2` plus a finite residual-radius row without reading the answer from orbital `GM`.

## Next Target

`4785-Y5-R2FR-real-source-profile-integral-and-residual-radius-row.md`
