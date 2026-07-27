# 4781 - Htau/Href parent charge evaluation or reference bound

Marker: `PPC4161_HTAU_HREF_PARENT_CHARGE_EVALUATION_OR_REFERENCE_BOUND_4781`
Generated: `2026-07-08T04:29:20+00:00`
Decision: `PARENT_CHARGE_EVALUATOR_AND_NO_CANCELLATION_BOUND_INTERFACE_INSTALLED_REAL_ROW_BLOCKS_COUNTERFACTUAL_SMOKES_NONCLAIM`

## Result

4781 turns the live 4780 blocker into an executable parent-charge interface. The exact source mass is still:

```text
M_H^dress[W_H;tau,e_obs] = H_tau[S_link;tau,e_obs] - H_ref[Sigma_ref;tau,e_obs].
```

But now the branch has a strict evaluation rule:

```text
delta H_tau[S] = int_S(delta Q_tau - i_tau theta_total(delta))
I_tau,S = d_field alpha_tau,S = int_S i_tau omega_total + I_ref + I_tau + I_corner.
```

If the curl/residual terms vanish and `H_ref` is fixed source-blind before readout, the parent charge is exact. If not, the legal fallback is an interval:

```text
M_H^dress in [H_tau_center - H_ref - Delta_H_abs,
              H_tau_center - H_ref + Delta_H_abs]
epsilon_Hcharge <= Delta_H_abs/M_lower.
```

No row may use observed orbital `GM/G_cal` to define `H_tau`, `H_ref`, `M_lower`, or `M_H^dress`.

## Parent Charge Theorem Rows

| theorem_id | formula | status |
| --- | --- | --- |
| PCT4781_0_variational_charge | delta H_tau[S]=int_S(delta Q_tau-i_tau theta_total(delta)) | definition/imported from 4211/4212 |
| PCT4781_1_integrability | I_tau,S=d_field alpha_tau,S=int_S i_tau omega_total+I_ref+I_tau+I_corner | operator derived; full zero still conditional |
| PCT4781_2_reference | H_ref=Hbar_ref(q(Phi)) selected before readout | conditional zero or bound |
| PCT4781_3_bound | M_H^dress in [H0-H_ref-Delta_H_abs, H0-H_ref+Delta_H_abs] | new executable bound interface |
| PCT4781_4_positive_lower | epsilon_Hcharge <= Delta_H_abs/M_lower, M_lower=M_EH(1-epsilon_abs)>0 | positive guard retained |

## Bound Law

| law_id | symbol | formula |
| --- | --- | --- |
| CBL4781_0_center | H_tau_center | H_tau_bulk+H_tau_surface |
| CBL4781_1_radius | Delta_H_abs | abs(H_tau_curl)+abs(H_tau_flux)+abs(H_tau_sector)+abs(H_tau_surface_residual)+abs(H_ref_drift)+abs(H_ref_selector) |
| CBL4781_2_interval_low | M_low | H_tau_center-H_ref-Delta_H_abs |
| CBL4781_3_interval_high | M_high | H_tau_center-H_ref+Delta_H_abs |
| CBL4781_4_normalized | epsilon_Hcharge | Delta_H_abs/M_lower |
| CBL4781_5_exact_zero | exact pass | Delta_H_abs=0 and M_low>0 |

## Parent Runner Output

| charge_id | M_H_dress_center_kg | M_H_dress_low_kg | M_H_dress_high_kg | epsilon_Hcharge_abs | runner_status |
| --- | --- | --- | --- | --- | --- |
| private_selector_missing_parent_charge_components | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | BLOCKED_MISSING_PARENT_CHARGE_COMPONENTS |
| private_parent_charge_interval_smoke_nonclaim | 1.988409870698051e+30 | 1.948641673284090e+30 | 2.028178068112012e+30 | 2.222222222222222e-02 | PARENT_CHARGE_INTERVAL_COMPUTED_NONCLAIM |
| counterfactual_parent_charge_equals_comparator | 1.988409870698051e+30 | 1.988409870698051e+30 | 1.988409870698051e+30 | 0.000000000000000e+00 | PARENT_CHARGE_COUNTERFACTUAL_SMOKE_PASS_NONCLAIM |
| forbidden_orbital_GM_as_parent_charge_control | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | FAILED_CIRCULAR_PARENT_CHARGE_SOURCE |

## Chain Score

| charge_id | parent_runner_status | source_runner_status | open_runner_status |
| --- | --- | --- | --- |
| private_selector_missing_parent_charge_components | BLOCKED_MISSING_PARENT_CHARGE_COMPONENTS | BLOCKED_MISSING_HTAU_OR_HREF | BLOCKED_MISSING_MHDRESS |
| private_parent_charge_interval_smoke_nonclaim | PARENT_CHARGE_INTERVAL_COMPUTED_NONCLAIM | BLOCKED_MISSING_HTAU_OR_HREF | BLOCKED_MISSING_MHDRESS |
| counterfactual_parent_charge_equals_comparator | PARENT_CHARGE_COUNTERFACTUAL_SMOKE_PASS_NONCLAIM | MHDRESS_COUNTERFACTUAL_SMOKE_PASS_NONCLAIM | RUNNER_SMOKE_PASS_NONCLAIM |
| forbidden_orbital_GM_as_parent_charge_control | FAILED_CIRCULAR_PARENT_CHARGE_SOURCE | BLOCKED_MISSING_HTAU_OR_HREF | BLOCKED_MISSING_MHDRESS |

## Route Selection

| route_id | route | selection_status |
| --- | --- | --- |
| RT4781_0_density_current | fill H_tau_bulk from parent density/current integral on W_H | SELECTED_NEXT |
| RT4781_1_reference | derive H_ref=0 or fixed source-blind reference value in the same branch | SELECTED_NEXT_PARALLEL |
| RT4781_2_Mlower | source or derive positive M_lower=M_EH(1-epsilon_abs) | SELECTED_NEXT_PARALLEL |
| RT4781_3_residual_radius | fill curl/flux/sector/reference residual radius components | SELECTED_NEXT_PARALLEL |

## Conclusion

This is a forward move but not a public local-GR/Newton claim. The real row blocks until the parent supplies one of:

1. a source-backed `H_tau_bulk` density/current integral plus fixed `H_ref`;
2. a theorem-zero residual radius with positive `M_lower`;
3. or finite residual components strong enough to bound `epsilon_Hcharge`.

## Next Target

`4782-Y5-R2FR-parent-Htau-density-current-first-source-row-or-Mlower-bound-fill.md`
