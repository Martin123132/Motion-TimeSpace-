# 4786 - Source-profile physical values or parent zero-profile certificate

Marker: `PPC4161_SOURCE_PROFILE_PHYSICAL_VALUES_OR_PARENT_ZERO_PROFILE_CERTIFICATE_4786`
Generated: `2026-07-08T05:13:19+00:00`
Decision: `RESIDUAL_ZERO_CERTIFICATE_RUNNER_INSTALLED_PARTIAL_ZERO_DOES_NOT_UNLOCK_PROFILE_REAL_PHYSICAL_SOURCE_PROFILE_STILL_MISSING_NONCLAIM`

## Result

4786 tries the zero-certificate path before demanding new data. Each residual component must be independently zero-certified or bounded:

```text
Delta_H_abs = |R_eq|+|B_zero|+|boundary_flux|+|open_EM|
            + |nonEM_owner_gap|+|projector_comm|+|domain_shadow|+|kappa_drift|.
```

Partial success is retained but does not unlock the chain. In the current physical attempt, fixed-EM/open-EM and kappa drift can be routed to existing private/conditional zero packets, but `R_eq`, `B_zero`, boundary, non-Hilbert owner gap, projector and domain components remain unclosed in the same parent branch.

## Zero-Certificate Law

| law_id | rule | meaning |
| --- | --- | --- |
| ZPL4786_0_same_branch | all zero components must live in the same parent/source-profile branch | prevents mixing private EM zero with unrelated boundary assumptions |
| ZPL4786_1_exact_or_bound | each residual component is either zero-certified, numerically bounded, or explicitly missing | no silent closure of the residual radius |
| ZPL4786_2_partial_blocks | a partial zero certificate does not unlock rho_H/M_lower | profile integral plus missing residual components still blocks |
| ZPL4786_3_openEM_kappa | fixed EM/Poynting and private kappa drift can zero their own components only inside their signed branch | keeps useful partial progress without overclaiming |
| ZPL4786_4_firewall | post-fit residual cancellation cannot be used as a zero certificate | blocks fitted-GM/readout laundering |

## Residual Zero Aggregate

| certificate_id | Delta_H_abs_kg | zero_component_count | bound_component_count | missing_component_count | failed_component_count | runner_status |
| --- | --- | --- | --- | --- | --- | --- |
| physical_partial_parent_zero_attempt | MISSING_NUMERIC_VALUE | 2 | 0 | 6 | 0 | RESIDUAL_ZERO_CERTIFICATE_PARTIAL_BLOCKED |
| private_full_zero_certificate_control | 0.000000000000000e+00 | 8 | 0 | 0 | 0 | RESIDUAL_ZERO_CERTIFICATE_PRIVATE_NONCLAIM |
| finite_residual_bound_smoke_nonclaim | 9.942049353490256e+27 | 0 | 8 | 0 | 0 | RESIDUAL_RADIUS_BOUND_COMPUTED_NONCLAIM |
| forbidden_postfit_zero_control | MISSING_NUMERIC_VALUE | 0 | 0 | 0 | 8 | FAILED_RESIDUAL_ZERO_CERTIFICATE |
| counterfactual_full_zero_certificate | 0.000000000000000e+00 | 8 | 0 | 0 | 0 | RESIDUAL_ZERO_COUNTERFACTUAL_SMOKE_PASS_NONCLAIM |

## Profile Runner Output

| profile_id | rho_H_integral_kg | Delta_H_abs_kg | residual_radius_mode | runner_status |
| --- | --- | --- | --- | --- |
| physical_profile_values_missing_partial_zero_certificate | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | NOT_COMPUTED_WITHOUT_PROFILE | BLOCKED_MISSING_SOURCE_PROFILE_COMPONENTS |
| profile_with_partial_zero_mass_smoke_nonclaim | 1.000000000000000e+00 | MISSING_NUMERIC_VALUE | MISSING_R_eq_abs_kg;B_zero_abs_kg;boundary_flux_abs_kg;nonEM_owner_gap_abs_kg;projector_comm_abs_kg;domain_shadow_abs_kg | PROFILE_INTEGRAL_COMPUTED_RESIDUALS_MISSING_NONCLAIM |
| private_unit_profile_parent_zero_certificate | 1.000000000000000e+00 | 0.000000000000000e+00 | RESIDUAL_COMPONENT_SUM | PROFILE_INTEGRAL_AND_RADIUS_EXACT_PRIVATE_NONCLAIM |
| finite_bound_profile_from_certificate_smoke | 1.988409870698051e+30 | 9.942049353490256e+27 | RESIDUAL_COMPONENT_SUM | PROFILE_INTEGRAL_AND_RADIUS_COMPUTED_NONCLAIM |
| forbidden_postfit_zero_profile_control | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | FAILED_FORBIDDEN_SOURCE | FAILED_CIRCULAR_SOURCE_PROFILE |
| counterfactual_profile_zero_certificate | 1.988409870698051e+30 | 0.000000000000000e+00 | RESIDUAL_COMPONENT_SUM | PROFILE_COUNTERFACTUAL_SMOKE_PASS_NONCLAIM |

## rhoH Runner Output

| density_id | rho_H_integral_kg | H_tau_bulk_kg | M0_kg | epsilon_abs | M_lower_kg | runner_status |
| --- | --- | --- | --- | --- | --- | --- |
| physical_profile_values_missing_partial_zero_certificate | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | BLOCKED_MISSING_RHOH_NUMERIC_INTEGRAL |
| profile_with_partial_zero_mass_smoke_nonclaim | 1.000000000000000e+00 | 1.000000000000000e+00 | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | BLOCKED_MISSING_RHOH_RESIDUAL_RADIUS |
| private_unit_profile_parent_zero_certificate | 1.000000000000000e+00 | 1.000000000000000e+00 | 1.000000000000000e+00 | 0.000000000000000e+00 | 1.000000000000000e+00 | RHOH_SELF_DENOMINATOR_EXACT_PRIVATE_NONCLAIM |
| finite_bound_profile_from_certificate_smoke | 1.988409870698051e+30 | 1.988409870698051e+30 | 1.988409870698051e+30 | 5.000000000000000e-03 | 1.978467821344561e+30 | RHOH_PARENT_INTEGRAL_INTERVAL_COMPUTED_NONCLAIM |
| forbidden_postfit_zero_profile_control | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | BLOCKED_MISSING_RHOH_NUMERIC_INTEGRAL |
| counterfactual_profile_zero_certificate | 1.988409870698051e+30 | 1.988409870698051e+30 | 1.988409870698051e+30 | 0.000000000000000e+00 | 1.988409870698051e+30 | RHOH_COUNTERFACTUAL_SMOKE_PASS_NONCLAIM |

## Chain Score

| profile_id | profile_runner_status | rhoh_runner_status | density_runner_status | parent_runner_status | source_runner_status | open_runner_status |
| --- | --- | --- | --- | --- | --- | --- |
| physical_profile_values_missing_partial_zero_certificate | BLOCKED_MISSING_SOURCE_PROFILE_COMPONENTS | BLOCKED_MISSING_RHOH_NUMERIC_INTEGRAL | BLOCKED_MISSING_DENSITY_CURRENT_COMPONENTS | BLOCKED_MISSING_PARENT_CHARGE_COMPONENTS | BLOCKED_MISSING_HTAU_OR_HREF | BLOCKED_MISSING_MHDRESS |
| profile_with_partial_zero_mass_smoke_nonclaim | PROFILE_INTEGRAL_COMPUTED_RESIDUALS_MISSING_NONCLAIM | BLOCKED_MISSING_RHOH_RESIDUAL_RADIUS | BLOCKED_MISSING_DENSITY_CURRENT_COMPONENTS | BLOCKED_MISSING_PARENT_CHARGE_COMPONENTS | BLOCKED_MISSING_HTAU_OR_HREF | BLOCKED_MISSING_MHDRESS |
| private_unit_profile_parent_zero_certificate | PROFILE_INTEGRAL_AND_RADIUS_EXACT_PRIVATE_NONCLAIM | RHOH_SELF_DENOMINATOR_EXACT_PRIVATE_NONCLAIM | DENSITY_CURRENT_EXACT_COMPUTED_NONCLAIM | PARENT_CHARGE_EXACT_COMPUTED_NONCLAIM | MHDRESS_COMPUTED_NONCLAIM | RUNNER_NUMERIC_FAIL_OR_TOLERANCE_MISSING_NONCLAIM |
| finite_bound_profile_from_certificate_smoke | PROFILE_INTEGRAL_AND_RADIUS_COMPUTED_NONCLAIM | RHOH_PARENT_INTEGRAL_INTERVAL_COMPUTED_NONCLAIM | DENSITY_CURRENT_INTERVAL_COMPUTED_NONCLAIM | PARENT_CHARGE_INTERVAL_COMPUTED_NONCLAIM | MHDRESS_COMPUTED_NONCLAIM | RUNNER_NUMERIC_PASS_NONCLAIM |
| forbidden_postfit_zero_profile_control | FAILED_CIRCULAR_SOURCE_PROFILE | BLOCKED_MISSING_RHOH_NUMERIC_INTEGRAL | BLOCKED_MISSING_DENSITY_CURRENT_COMPONENTS | BLOCKED_MISSING_PARENT_CHARGE_COMPONENTS | BLOCKED_MISSING_HTAU_OR_HREF | BLOCKED_MISSING_MHDRESS |
| counterfactual_profile_zero_certificate | PROFILE_COUNTERFACTUAL_SMOKE_PASS_NONCLAIM | RHOH_COUNTERFACTUAL_SMOKE_PASS_NONCLAIM | DENSITY_CURRENT_COUNTERFACTUAL_SMOKE_PASS_NONCLAIM | PARENT_CHARGE_COUNTERFACTUAL_SMOKE_PASS_NONCLAIM | MHDRESS_COUNTERFACTUAL_SMOKE_PASS_NONCLAIM | RUNNER_SMOKE_PASS_NONCLAIM |

## Route Selection

| route_id | route | selection_status |
| --- | --- | --- |
| RT4786_0_physical_profile | fill a controlled physical T_total(n,n) profile row | SELECTED_NEXT |
| RT4786_1_complete_zero | try to close R_eq/B_zero/boundary/nonEM/projector/domain residual zeros in the same branch | SELECTED_NEXT_PARALLEL |
| RT4786_2_numeric_bounds | if zeros fail, source numerical bounds for the missing residual components | SELECTED_NEXT_PARALLEL |

## Conclusion

The branch did move: residual closure is now component-wise executable, and partial zero results cannot masquerade as a full local-GR source certificate. The next best target is a controlled physical `T_total(n,n)` profile row, while continuing to attack the unclosed residual components.

## Next Target

`4787-Y5-R2FR-physical-Ttotal-profile-row-or-minimal-controlled-source-model.md`
