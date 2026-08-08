# 4782 - Parent Htau density-current first source row or Mlower bound fill

Marker: `PPC4161_PARENT_HTAU_DENSITY_CURRENT_FIRST_SOURCE_ROW_OR_MLOWER_BOUND_FILL_4782`
Generated: `2026-07-08T04:37:40+00:00`
Decision: `DENSITY_CURRENT_AND_MLOWER_RUNNER_INSTALLED_REAL_PARENT_DENSITY_BLOCKS_PRIVATE_AND_COUNTERFACTUAL_CONTROLS_PASS_NONCLAIM`

## Result

4782 takes the 4781 `H_tau_bulk` slot and gives it an executable density/current law:

```text
rho_H dV_H := c^-2 T_total(n,n) dV_eobs
H_tau_bulk = int_W rho_H dV_H + H_tau_surface_center
Delta_H_abs = |R_eq|+|B_zero|+|boundary_flux|+|open_EM|+|nonEM_owner_gap|
            + |projector_comm|+|domain_shadow|+|kappa_drift|
M_lower = M0*(1-epsilon_abs).
```

Poynting is not an extra hidden source here: it is counted once as Maxwell/Hilbert stress or as an explicit boundary/open-EM flux row.

## Density/Current Theorem Rows

| theorem_id | formula | meaning |
| --- | --- | --- |
| DCT4782_0_density | rho_H dV_H := c^-2 T_total(n,n)dV_eobs | parent Hilbert density integrand for H_tau_bulk |
| DCT4782_1_poynting_once | T_total = T_matter + T_EM + retained sectors | Poynting is counted once as Maxwell/Hilbert stress or boundary flux |
| DCT4782_2_current_tail | Delta_H_abs includes R_eq+B_zero+boundary+open_EM+nonEM+projector+domain+kappa tails | open source-current pieces become a no-cancellation radius |
| DCT4782_3_exact_branch | Delta_H_abs=0 and M_lower>0 | only this branch can feed exact H_tau/H_ref into M_Hdress |

## Mlower Law

| law_id | symbol | formula |
| --- | --- | --- |
| ML4782_0 | M0 | M0 := M_EH_private or source-backed positive Hilbert energy |
| ML4782_1 | epsilon_abs | sum_i \|Delta_i\|/M0 |
| ML4782_2 | M_lower | M_lower = M0*(1-epsilon_abs) |
| ML4782_3 | public row | M0 and epsilon_abs must be source-backed, not private/unit smoke |

## Density Runner Output

| density_id | H_tau_bulk_kg | M_lower_kg | Delta_H_abs_kg | epsilon_density_current_abs | runner_status |
| --- | --- | --- | --- | --- | --- |
| physical_missing_parent_density_current | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | BLOCKED_MISSING_DENSITY_CURRENT_COMPONENTS |
| private_unit_exact_density_current_control | 1.000000000000000e+00 | 1.000000000000000e+00 | 0.000000000000000e+00 | 0.000000000000000e+00 | DENSITY_CURRENT_EXACT_COMPUTED_NONCLAIM |
| finite_interval_density_current_smoke_nonclaim | 1.988409870698051e+30 | 1.789568883628246e+30 | 3.976819741396102e+28 | 2.222222222222222e-02 | DENSITY_CURRENT_INTERVAL_COMPUTED_NONCLAIM |
| counterfactual_density_current_equals_comparator | 1.988409870698051e+30 | 1.988409870698051e+30 | 0.000000000000000e+00 | 0.000000000000000e+00 | DENSITY_CURRENT_COUNTERFACTUAL_SMOKE_PASS_NONCLAIM |
| forbidden_observed_GM_density_control | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | FAILED_CIRCULAR_DENSITY_CURRENT_SOURCE |

## Chain Score

| density_id | density_runner_status | parent_runner_status | source_runner_status | open_runner_status |
| --- | --- | --- | --- | --- |
| physical_missing_parent_density_current | BLOCKED_MISSING_DENSITY_CURRENT_COMPONENTS | BLOCKED_MISSING_PARENT_CHARGE_COMPONENTS | BLOCKED_MISSING_HTAU_OR_HREF | BLOCKED_MISSING_MHDRESS |
| private_unit_exact_density_current_control | DENSITY_CURRENT_EXACT_COMPUTED_NONCLAIM | PARENT_CHARGE_EXACT_COMPUTED_NONCLAIM | BLOCKED_MISSING_HTAU_OR_HREF | BLOCKED_MISSING_MHDRESS |
| finite_interval_density_current_smoke_nonclaim | DENSITY_CURRENT_INTERVAL_COMPUTED_NONCLAIM | PARENT_CHARGE_INTERVAL_COMPUTED_NONCLAIM | BLOCKED_MISSING_HTAU_OR_HREF | BLOCKED_MISSING_MHDRESS |
| counterfactual_density_current_equals_comparator | DENSITY_CURRENT_COUNTERFACTUAL_SMOKE_PASS_NONCLAIM | PARENT_CHARGE_COUNTERFACTUAL_SMOKE_PASS_NONCLAIM | MHDRESS_COUNTERFACTUAL_SMOKE_PASS_NONCLAIM | RUNNER_SMOKE_PASS_NONCLAIM |
| forbidden_observed_GM_density_control | FAILED_CIRCULAR_DENSITY_CURRENT_SOURCE | BLOCKED_MISSING_PARENT_CHARGE_COMPONENTS | BLOCKED_MISSING_HTAU_OR_HREF | BLOCKED_MISSING_MHDRESS |

## Route Selection

| route_id | route | selection_status |
| --- | --- | --- |
| RT4782_0_real_density | fill first real rho_H integral from parent/local-packet density-current row | SELECTED_NEXT |
| RT4782_1_Href_zero | prove fixed source-blind H_ref=0 branch or source a reference value | SELECTED_NEXT_PARALLEL |
| RT4782_2_M0 | source M0 and epsilon_abs rather than unit/private Mlower | SELECTED_NEXT_PARALLEL |
| RT4782_3_residuals | source R_eq/B_zero/boundary/open-EM/projector/domain/kappa residual radius | SELECTED_NEXT_PARALLEL |

## Conclusion

The exact hole is no longer vague. To make the local Newton/GR source row physical, 4783 must supply a real parent/local-packet `rho_H` integral and a fixed source-blind `H_ref` value or zero certificate. `M0`, `epsilon_abs`, and the residual radius must be source-backed before any normalized claim.

## Next Target

`4783-Y5-R2FR-real-parent-density-current-source-row-or-Href-zero-certificate.md`
