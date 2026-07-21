# 4787 - Physical Ttotal profile row or minimal controlled source model

Marker: `PPC4161_PHYSICAL_TTOTAL_PROFILE_ROW_OR_MINIMAL_CONTROLLED_SOURCE_MODEL_4787`
Generated: `2026-07-08T05:19:39+00:00`
Decision: `CONTROLLED_TTOTAL_PROFILE_RUNNER_INSTALLED_MINIMAL_SOURCE_MODEL_COMPUTES_PROFILE_NONCLAIM_RESIDUAL_CERTIFICATE_STILL_GATES_LOCAL_GR`

## Result

4787 builds the minimal controlled-source model needed by the local GR/Newton branch:

```text
T_total(n,n) = rho_rest c^2 + u_internal + u_EM + u_rad
rho_H(W_H) = int_W T_total(n,n)dV / c^2.
```

This is not a solar/planetary claim. It is a controlled upstream source model: density, EM energy and volume are declared before any arena readout. Orbital `GM`, PPN residuals, clock calibration and R10 bounds cannot define the profile.

## Controlled Ttotal Law

| law_id | rule | meaning |
| --- | --- | --- |
| CTL4787_0_Ttotal | T_total(n,n)=rho_rest c^2+u_internal+u_EM+u_rad | minimal controlled profile source density |
| CTL4787_1_volume | rho_H(W)=int_W T_total(n,n)dV/c^2 | turns controlled local energy density into the profile integral |
| CTL4787_2_pressure | pressure/stress is reported but not hidden inside rho_H unless it enters T(n,n) | keeps PPN pressure/stress effects separate |
| CTL4787_3_poynting | u_EM is Hilbert Maxwell energy; radiative Poynting is boundary/open_EM residual | prevents double-counting EM flow |
| CTL4787_4_firewall | GM/PPN/clock/R10 readouts cannot set rho_rest, u_EM, volume, or normalization | keeps controlled source upstream of tests |

## Controlled Runner Output

| model_id | profile_id | rho_H_integral_kg | T_total_mode | pressure_to_energy_ratio | runner_status |
| --- | --- | --- | --- | --- | --- |
| physical_controlled_profile_values_missing | physical_controlled_profile_values_missing | MISSING_NUMERIC_VALUE | MISSING_REST_MASS_OR_TTOTAL_DENSITY | MISSING_NUMERIC_VALUE | BLOCKED_MISSING_CONTROLLED_TTOTAL_PROFILE_INPUTS |
| controlled_uniform_partial_zero_model | controlled_uniform_partial_zero_model | 1.000000000000000e+00 | REST_PLUS_INTERNAL_PLUS_EM_ENERGY_DENSITY | MISSING_NUMERIC_VALUE | CONTROLLED_TTOTAL_PROFILE_COMPUTED_NONCLAIM |
| private_uniform_dust_full_zero_model | private_uniform_dust_full_zero_model | 1.000000000000000e+00 | REST_PLUS_INTERNAL_PLUS_EM_ENERGY_DENSITY | MISSING_NUMERIC_VALUE | CONTROLLED_TTOTAL_PROFILE_PRIVATE_NONCLAIM |
| controlled_matter_EM_finite_bound_smoke | controlled_matter_EM_finite_bound_smoke | 3.000000000000000e+30 | REST_PLUS_INTERNAL_PLUS_EM_ENERGY_DENSITY | 1.112650056053619e-42 | CONTROLLED_TTOTAL_PROFILE_COMPUTED_NONCLAIM |
| forbidden_orbital_GM_Ttotal_control | forbidden_orbital_GM_Ttotal_control | MISSING_NUMERIC_VALUE | REST_PLUS_INTERNAL_PLUS_EM_ENERGY_DENSITY | MISSING_NUMERIC_VALUE | FAILED_CIRCULAR_TTOTAL_PROFILE_SOURCE |
| counterfactual_solar_mass_profile | counterfactual_solar_mass_profile | 1.988409870698051e+30 | REST_PLUS_INTERNAL_PLUS_EM_ENERGY_DENSITY | MISSING_NUMERIC_VALUE | CONTROLLED_TTOTAL_PROFILE_COUNTERFACTUAL_SMOKE_PASS_NONCLAIM |

## Profile Runner Output

| profile_id | rho_H_integral_kg | Delta_H_abs_kg | residual_radius_mode | runner_status |
| --- | --- | --- | --- | --- |
| physical_controlled_profile_values_missing | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | NOT_COMPUTED_WITHOUT_PROFILE | BLOCKED_MISSING_SOURCE_PROFILE_COMPONENTS |
| controlled_uniform_partial_zero_model | 1.000000000000000e+00 | MISSING_NUMERIC_VALUE | MISSING_R_eq_abs_kg;B_zero_abs_kg;boundary_flux_abs_kg;nonEM_owner_gap_abs_kg;projector_comm_abs_kg;domain_shadow_abs_kg | PROFILE_INTEGRAL_COMPUTED_RESIDUALS_MISSING_NONCLAIM |
| private_uniform_dust_full_zero_model | 1.000000000000000e+00 | 0.000000000000000e+00 | RESIDUAL_COMPONENT_SUM | PROFILE_INTEGRAL_AND_RADIUS_EXACT_PRIVATE_NONCLAIM |
| controlled_matter_EM_finite_bound_smoke | 3.000000000000000e+30 | 9.942049353490256e+27 | RESIDUAL_COMPONENT_SUM | PROFILE_INTEGRAL_AND_RADIUS_COMPUTED_NONCLAIM |
| forbidden_orbital_GM_Ttotal_control | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | FAILED_FORBIDDEN_SOURCE | FAILED_CIRCULAR_SOURCE_PROFILE |
| counterfactual_solar_mass_profile | 1.988409870698051e+30 | 0.000000000000000e+00 | RESIDUAL_COMPONENT_SUM | PROFILE_COUNTERFACTUAL_SMOKE_PASS_NONCLAIM |

## rhoH Runner Output

| density_id | rho_H_integral_kg | H_tau_bulk_kg | M0_kg | epsilon_abs | M_lower_kg | runner_status |
| --- | --- | --- | --- | --- | --- | --- |
| physical_controlled_profile_values_missing | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | BLOCKED_MISSING_RHOH_NUMERIC_INTEGRAL |
| controlled_uniform_partial_zero_model | 1.000000000000000e+00 | 1.000000000000000e+00 | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | BLOCKED_MISSING_RHOH_RESIDUAL_RADIUS |
| private_uniform_dust_full_zero_model | 1.000000000000000e+00 | 1.000000000000000e+00 | 1.000000000000000e+00 | 0.000000000000000e+00 | 1.000000000000000e+00 | RHOH_SELF_DENOMINATOR_EXACT_PRIVATE_NONCLAIM |
| controlled_matter_EM_finite_bound_smoke | 3.000000000000000e+30 | 3.000000000000000e+30 | 3.000000000000000e+30 | 3.314016451163419e-03 | 2.990057950646509e+30 | RHOH_PARENT_INTEGRAL_INTERVAL_COMPUTED_NONCLAIM |
| forbidden_orbital_GM_Ttotal_control | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | BLOCKED_MISSING_RHOH_NUMERIC_INTEGRAL |
| counterfactual_solar_mass_profile | 1.988409870698051e+30 | 1.988409870698051e+30 | 1.988409870698051e+30 | 0.000000000000000e+00 | 1.988409870698051e+30 | RHOH_COUNTERFACTUAL_SMOKE_PASS_NONCLAIM |

## Chain Score

| profile_id | profile_runner_status | rhoh_runner_status | density_runner_status | parent_runner_status | source_runner_status | open_runner_status |
| --- | --- | --- | --- | --- | --- | --- |
| physical_controlled_profile_values_missing | BLOCKED_MISSING_SOURCE_PROFILE_COMPONENTS | BLOCKED_MISSING_RHOH_NUMERIC_INTEGRAL | BLOCKED_MISSING_DENSITY_CURRENT_COMPONENTS | BLOCKED_MISSING_PARENT_CHARGE_COMPONENTS | BLOCKED_MISSING_HTAU_OR_HREF | BLOCKED_MISSING_MHDRESS |
| controlled_uniform_partial_zero_model | PROFILE_INTEGRAL_COMPUTED_RESIDUALS_MISSING_NONCLAIM | BLOCKED_MISSING_RHOH_RESIDUAL_RADIUS | BLOCKED_MISSING_DENSITY_CURRENT_COMPONENTS | BLOCKED_MISSING_PARENT_CHARGE_COMPONENTS | BLOCKED_MISSING_HTAU_OR_HREF | BLOCKED_MISSING_MHDRESS |
| private_uniform_dust_full_zero_model | PROFILE_INTEGRAL_AND_RADIUS_EXACT_PRIVATE_NONCLAIM | RHOH_SELF_DENOMINATOR_EXACT_PRIVATE_NONCLAIM | DENSITY_CURRENT_EXACT_COMPUTED_NONCLAIM | PARENT_CHARGE_EXACT_COMPUTED_NONCLAIM | MHDRESS_COMPUTED_NONCLAIM | RUNNER_NUMERIC_FAIL_OR_TOLERANCE_MISSING_NONCLAIM |
| controlled_matter_EM_finite_bound_smoke | PROFILE_INTEGRAL_AND_RADIUS_COMPUTED_NONCLAIM | RHOH_PARENT_INTEGRAL_INTERVAL_COMPUTED_NONCLAIM | DENSITY_CURRENT_INTERVAL_COMPUTED_NONCLAIM | PARENT_CHARGE_INTERVAL_COMPUTED_NONCLAIM | MHDRESS_COMPUTED_NONCLAIM | RUNNER_NUMERIC_FAIL_OR_TOLERANCE_MISSING_NONCLAIM |
| forbidden_orbital_GM_Ttotal_control | FAILED_CIRCULAR_SOURCE_PROFILE | BLOCKED_MISSING_RHOH_NUMERIC_INTEGRAL | BLOCKED_MISSING_DENSITY_CURRENT_COMPONENTS | BLOCKED_MISSING_PARENT_CHARGE_COMPONENTS | BLOCKED_MISSING_HTAU_OR_HREF | BLOCKED_MISSING_MHDRESS |
| counterfactual_solar_mass_profile | PROFILE_COUNTERFACTUAL_SMOKE_PASS_NONCLAIM | RHOH_COUNTERFACTUAL_SMOKE_PASS_NONCLAIM | DENSITY_CURRENT_COUNTERFACTUAL_SMOKE_PASS_NONCLAIM | PARENT_CHARGE_COUNTERFACTUAL_SMOKE_PASS_NONCLAIM | MHDRESS_COUNTERFACTUAL_SMOKE_PASS_NONCLAIM | RUNNER_SMOKE_PASS_NONCLAIM |

## Route Selection

| route_id | route | selection_status |
| --- | --- | --- |
| RT4787_0_missing_residuals | close or bound R_eq/B_zero/boundary/nonHilbert/projector/domain for controlled source | SELECTED_NEXT |
| RT4787_1_testbench | promote the controlled source into a local testbench once residuals close | SELECTED_NEXT_PARALLEL |
| RT4787_2_physical_values | replace unit/smoke density with source-backed physical density and volume rows | SELECTED_NEXT_PARALLEL |

## Conclusion

The profile-value blocker is no longer abstract. A controlled `T_total(n,n)` source can be computed from local density/energy/volume rows and passed into the chain. The remaining failure is the same six residual components identified by 4786: `R_eq`, `B_zero`, boundary, non-Hilbert owner gap, projector commutator and domain shadow.

## Next Target

`4788-Y5-R2FR-close-Req-Bzero-boundary-projector-domain-or-controlled-source-testbench.md`
