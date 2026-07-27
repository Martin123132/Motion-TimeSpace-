# 4783 - Real parent density-current source row or Href zero certificate

Marker: `PPC4161_REAL_PARENT_DENSITY_CURRENT_SOURCE_ROW_OR_HREF_ZERO_CERTIFICATE_4783`
Generated: `2026-07-08T04:44:38+00:00`
Decision: `HREF_ZERO_CERTIFICATE_RUNNER_INSTALLED_PRIVATE_REFERENCE_ZERO_NARROWS_PHYSICAL_BLOCKER_TO_RHOH_M0_RESIDUALS_NONCLAIM`

## Result

4783 closes one side of the 4782 source slot in the only safe way: `H_ref=0` is accepted only for a fixed source-blind reference selected before source/radius/frame/readout scoring.

```text
H_ref = 0
D_source H_ref = D_readout H_ref = D_frame H_ref = 0
d_field(delta H_ref)=0
```

That narrows the physical blocker. It does not supply the real `rho_H` integral, `M0`, `epsilon_abs`, or residual-radius values.

## Href Theorem Rows

| theorem_id | statement | meaning |
| --- | --- | --- |
| HRT4783_0_anchor | H_ref=0 is legal only if the zero anchor is selected before source/readout scoring | blocks post-fit cancellation |
| HRT4783_1_source_blind | D_source H_ref=D_readout H_ref=D_frame H_ref=0 | removes reference laundering inside the selected branch |
| HRT4783_2_qbasic | H_ref=Hbar_ref(q(Phi)) and v in ker(Dq) => D_v H_ref=0 | source-blind quotient reference clause |
| HRT4783_3_curl | H_ref fixed => d_field(delta H_ref)=0 => I_ref=0 | reference curl term closes conditionally |
| HRT4783_4_bound | \|H_ref\| <= \|H_ref_anchor\|+sum \|Delta_ref_i\| | fallback if any zero clause is unsigned |

## Href Runner Output

| reference_id | H_ref_kg | H_ref_abs_bound_kg | epsilon_Href_abs | runner_status |
| --- | --- | --- | --- | --- |
| physical_missing_href_certificate | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | BLOCKED_MISSING_HREF_ANCHOR |
| private_source_blind_Href_zero_certificate | 0.000000000000000e+00 | 0.000000000000000e+00 | 0.000000000000000e+00 | HREF_ZERO_CERTIFIED_PRIVATE_NONCLAIM |
| finite_Href_bound_smoke_nonclaim | 0.000000000000000e+00 | 3.976819741396102e+28 | 2.000000000000000e-02 | HREF_BOUND_COMPUTED_NONCLAIM |
| counterfactual_Href_zero_smoke | 0.000000000000000e+00 | 0.000000000000000e+00 | 0.000000000000000e+00 | HREF_COUNTERFACTUAL_ZERO_SMOKE_PASS_NONCLAIM |
| forbidden_postfit_reference_control | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | FAILED_CIRCULAR_POSTFIT_REFERENCE |

## Density Runner Output

| density_id | H_tau_bulk_kg | H_ref_kg | M_lower_kg | Delta_H_abs_kg | runner_status |
| --- | --- | --- | --- | --- | --- |
| physical_missing_density_with_private_Href_zero | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | BLOCKED_MISSING_DENSITY_CURRENT_COMPONENTS |
| counterfactual_density_with_Href_zero | 1.988409870698051e+30 | 0.000000000000000e+00 | 1.988409870698051e+30 | 0.000000000000000e+00 | DENSITY_CURRENT_COUNTERFACTUAL_SMOKE_PASS_NONCLAIM |

## Chain Score

| reference_id | density_id | href_runner_status | density_runner_status | parent_runner_status | source_runner_status | open_runner_status |
| --- | --- | --- | --- | --- | --- | --- |
| private_source_blind_Href_zero_certificate | physical_missing_density_with_private_Href_zero | HREF_ZERO_CERTIFIED_PRIVATE_NONCLAIM | BLOCKED_MISSING_DENSITY_CURRENT_COMPONENTS | BLOCKED_MISSING_PARENT_CHARGE_COMPONENTS | BLOCKED_MISSING_HTAU_OR_HREF | BLOCKED_MISSING_MHDRESS |
| counterfactual_Href_zero_smoke | counterfactual_density_with_Href_zero | HREF_COUNTERFACTUAL_ZERO_SMOKE_PASS_NONCLAIM | DENSITY_CURRENT_COUNTERFACTUAL_SMOKE_PASS_NONCLAIM | PARENT_CHARGE_COUNTERFACTUAL_SMOKE_PASS_NONCLAIM | MHDRESS_COUNTERFACTUAL_SMOKE_PASS_NONCLAIM | RUNNER_SMOKE_PASS_NONCLAIM |

## Route Selection

| route_id | route | selection_status |
| --- | --- | --- |
| RT4783_0_rhoH | fill real parent/local-packet rho_H integral on W_H | SELECTED_NEXT |
| RT4783_1_M0 | source-backed M0 and epsilon_abs for positive M_lower | SELECTED_NEXT_PARALLEL |
| RT4783_2_radius | fill R_eq/B_zero/boundary/open-EM/projector/domain/kappa residual radius | SELECTED_NEXT_PARALLEL |

## Conclusion

The private/fixed `H_ref=0` branch is now executable and anti-circular. The live source-mass blocker is reduced to the genuinely physical inputs: real `rho_H dV_H`, source-backed `M0/epsilon_abs`, and finite residual-radius rows.

## Next Target

`4784-Y5-R2FR-real-rhoH-parent-density-integral-or-M0-source-backed-row.md`
