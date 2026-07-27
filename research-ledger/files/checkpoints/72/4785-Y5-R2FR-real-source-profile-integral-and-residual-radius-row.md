# 4785 - Real source-profile integral and residual-radius row

Marker: `PPC4161_REAL_SOURCE_PROFILE_INTEGRAL_AND_RESIDUAL_RADIUS_ROW_4785`
Generated: `2026-07-08T05:06:19+00:00`
Decision: `SOURCE_PROFILE_INTEGRAL_AND_RESIDUAL_RADIUS_RUNNER_INSTALLED_PROFILE_WITHOUT_RADIUS_STILL_BLOCKS_REAL_PHYSICAL_PROFILE_VALUES_MISSING_NONCLAIM`

## Result

4785 turns the remaining 4784 profile gap into an executable two-part gate:

```text
rho_H(W_H)=sum_i int_shell_i rho_H dV
          = c^-2 sum_i int_shell_i T_total(n,n)dV

Delta_H_abs = |R_eq|+|B_zero|+|boundary_flux|+|open_EM|
            + |nonEM_owner_gap|+|projector_comm|+|domain_shadow|+|kappa_drift|.
```

The important split is now mechanical: a profile integral alone is not enough; it must travel with the residual-radius row before `M0`, `epsilon_abs`, `M_lower`, and `M_H^dress` become usable.

## Source Profile Law Rows

| law_id | formula | meaning |
| --- | --- | --- |
| SPL4785_0_profile_integral | rho_H(W_H)=sum_i int_{shell_i} rho_H dV = c^-2 sum_i int T_total(n,n)dV | turns a worldtube profile table into a source mass integral |
| SPL4785_1_shell_volume | dV_i is explicit or 4*pi/3*(r_out^3-r_in^3) | prevents hidden profile normalization |
| SPL4785_2_radius | Delta_H_abs=sum \|R_eq\|+\|B_zero\|+\|boundary_flux\|+\|open_EM\|+\|nonEM\|+\|projector\|+\|domain\|+\|kappa\| | separates profile mass from the no-cancellation residual radius |
| SPL4785_3_poynting | Poynting is inside T_EM Hilbert stress or an explicit boundary/open_EM residual | blocks double counting the EM flux |
| SPL4785_4_firewall | GM/PPN/clock/R10 fitted outputs cannot define rho_H(W_H) | keeps the source profile independent of the arena readout |

## Profile Runner Output

| profile_id | rho_H_integral_kg | Delta_H_abs_kg | source_profile_mode | residual_radius_mode | runner_status |
| --- | --- | --- | --- | --- | --- |
| physical_profile_values_missing | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_MASS_DENSITY_OR_TNN | NOT_COMPUTED_WITHOUT_PROFILE | BLOCKED_MISSING_SOURCE_PROFILE_COMPONENTS |
| profile_without_residual_radius_control | 1.000000000000000e+00 | MISSING_NUMERIC_VALUE | RHO_H_TIMES_VOLUME | MISSING_R_eq_abs_kg;B_zero_abs_kg;boundary_flux_abs_kg;open_EM_abs_kg;nonEM_owner_gap_abs_kg;projector_comm_abs_kg;domain_shadow_abs_kg;kappa_drift_abs_kg | PROFILE_INTEGRAL_COMPUTED_RESIDUALS_MISSING_NONCLAIM |
| private_unit_profile_with_zero_radius | 1.000000000000000e+00 | 0.000000000000000e+00 | RHO_H_TIMES_VOLUME | RESIDUAL_COMPONENT_SUM | PROFILE_INTEGRAL_AND_RADIUS_EXACT_PRIVATE_NONCLAIM |
| finite_profile_radius_smoke_nonclaim | 1.988409870698051e+30 | 3.976819741396102e+28 | RHO_H_TIMES_VOLUME | RESIDUAL_COMPONENT_SUM | PROFILE_INTEGRAL_AND_RADIUS_COMPUTED_NONCLAIM |
| forbidden_orbital_GM_profile_control | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | FAILED_FORBIDDEN_SOURCE | FAILED_FORBIDDEN_SOURCE | FAILED_CIRCULAR_SOURCE_PROFILE |
| counterfactual_profile_equals_comparator | 1.988409870698051e+30 | 0.000000000000000e+00 | RHO_H_TIMES_VOLUME | RESIDUAL_COMPONENT_SUM | PROFILE_COUNTERFACTUAL_SMOKE_PASS_NONCLAIM |

## rhoH Runner Output

| density_id | rho_H_integral_kg | H_tau_bulk_kg | M0_kg | epsilon_abs | M_lower_kg | runner_status |
| --- | --- | --- | --- | --- | --- | --- |
| physical_profile_values_missing | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | BLOCKED_MISSING_RHOH_NUMERIC_INTEGRAL |
| profile_without_residual_radius_control | 1.000000000000000e+00 | 1.000000000000000e+00 | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | BLOCKED_MISSING_RHOH_RESIDUAL_RADIUS |
| private_unit_profile_with_zero_radius | 1.000000000000000e+00 | 1.000000000000000e+00 | 1.000000000000000e+00 | 0.000000000000000e+00 | 1.000000000000000e+00 | RHOH_SELF_DENOMINATOR_EXACT_PRIVATE_NONCLAIM |
| finite_profile_radius_smoke_nonclaim | 1.988409870698051e+30 | 1.988409870698051e+30 | 1.988409870698051e+30 | 2.000000000000000e-02 | 1.948641673284090e+30 | RHOH_PARENT_INTEGRAL_INTERVAL_COMPUTED_NONCLAIM |
| forbidden_orbital_GM_profile_control | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | BLOCKED_MISSING_RHOH_NUMERIC_INTEGRAL |
| counterfactual_profile_equals_comparator | 1.988409870698051e+30 | 1.988409870698051e+30 | 1.988409870698051e+30 | 0.000000000000000e+00 | 1.988409870698051e+30 | RHOH_COUNTERFACTUAL_SMOKE_PASS_NONCLAIM |

## Chain Score

| profile_id | profile_runner_status | rhoh_runner_status | density_runner_status | parent_runner_status | source_runner_status | open_runner_status |
| --- | --- | --- | --- | --- | --- | --- |
| physical_profile_values_missing | BLOCKED_MISSING_SOURCE_PROFILE_COMPONENTS | BLOCKED_MISSING_RHOH_NUMERIC_INTEGRAL | BLOCKED_MISSING_DENSITY_CURRENT_COMPONENTS | BLOCKED_MISSING_PARENT_CHARGE_COMPONENTS | BLOCKED_MISSING_HTAU_OR_HREF | BLOCKED_MISSING_MHDRESS |
| profile_without_residual_radius_control | PROFILE_INTEGRAL_COMPUTED_RESIDUALS_MISSING_NONCLAIM | BLOCKED_MISSING_RHOH_RESIDUAL_RADIUS | BLOCKED_MISSING_DENSITY_CURRENT_COMPONENTS | BLOCKED_MISSING_PARENT_CHARGE_COMPONENTS | BLOCKED_MISSING_HTAU_OR_HREF | BLOCKED_MISSING_MHDRESS |
| private_unit_profile_with_zero_radius | PROFILE_INTEGRAL_AND_RADIUS_EXACT_PRIVATE_NONCLAIM | RHOH_SELF_DENOMINATOR_EXACT_PRIVATE_NONCLAIM | DENSITY_CURRENT_EXACT_COMPUTED_NONCLAIM | PARENT_CHARGE_EXACT_COMPUTED_NONCLAIM | MHDRESS_COMPUTED_NONCLAIM | RUNNER_NUMERIC_FAIL_OR_TOLERANCE_MISSING_NONCLAIM |
| finite_profile_radius_smoke_nonclaim | PROFILE_INTEGRAL_AND_RADIUS_COMPUTED_NONCLAIM | RHOH_PARENT_INTEGRAL_INTERVAL_COMPUTED_NONCLAIM | DENSITY_CURRENT_INTERVAL_COMPUTED_NONCLAIM | PARENT_CHARGE_INTERVAL_COMPUTED_NONCLAIM | MHDRESS_COMPUTED_NONCLAIM | RUNNER_NUMERIC_PASS_NONCLAIM |
| forbidden_orbital_GM_profile_control | FAILED_CIRCULAR_SOURCE_PROFILE | BLOCKED_MISSING_RHOH_NUMERIC_INTEGRAL | BLOCKED_MISSING_DENSITY_CURRENT_COMPONENTS | BLOCKED_MISSING_PARENT_CHARGE_COMPONENTS | BLOCKED_MISSING_HTAU_OR_HREF | BLOCKED_MISSING_MHDRESS |
| counterfactual_profile_equals_comparator | PROFILE_COUNTERFACTUAL_SMOKE_PASS_NONCLAIM | RHOH_COUNTERFACTUAL_SMOKE_PASS_NONCLAIM | DENSITY_CURRENT_COUNTERFACTUAL_SMOKE_PASS_NONCLAIM | PARENT_CHARGE_COUNTERFACTUAL_SMOKE_PASS_NONCLAIM | MHDRESS_COUNTERFACTUAL_SMOKE_PASS_NONCLAIM | RUNNER_SMOKE_PASS_NONCLAIM |

## Route Selection

| route_id | route | selection_status |
| --- | --- | --- |
| RT4785_0_physical_values | fill a real parent/source-backed T_total(n,n) or rho_H profile over W_H | SELECTED_NEXT |
| RT4785_1_zero_certificate | try a parent zero-profile certificate for non-GR residual components | SELECTED_NEXT_PARALLEL |
| RT4785_2_radius_values | source the eight residual-radius components if exact zero fails | SELECTED_NEXT_PARALLEL |

## Conclusion

The local source branch has a clean executable throat now. The next real input is not abstract `M0`; it is a parent/source-backed profile table for `T_total(n,n)` or `rho_H`, plus the eight residual-radius components or a parent zero certificate for them. Orbital `GM`, PPN fits, clocks and R10 bounds remain comparison outputs only.

## Next Target

`4786-Y5-R2FR-source-profile-physical-values-or-parent-zero-profile-certificate.md`
