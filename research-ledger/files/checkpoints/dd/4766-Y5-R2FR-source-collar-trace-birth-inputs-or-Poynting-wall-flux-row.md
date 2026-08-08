# 4766: Source-Collar Trace/Birth Inputs or Poynting Wall Flux Row

Generated: `2026-07-08T02:51:41+00:00`

Marker: `PPC4161_SOURCE_COLLAR_SUPPORT_INVARIANCE_OR_POYNTING_WALL_FLUX_ROW_4766`

## Result

4766 finds a cleaner route than hammering zero trace directly.

- If the Hilbert source measure `mu_H=rho_H dV_H` is exactly q-basic as a Radon measure, then along a vertical fibre `mu_H(Phi_s)=mu_H(Phi_0)`.
- If the source worldtube is selected before readout as `W_H=closure(supp mu_H)`, measure equality implies support equality.
- Therefore `V_n_bound=0` and `mu_birth_TV=0` on that strict branch, so `Q_edge_shell_abs=0` without needing `rho_H_trace_norm=0`.
- This is not claimed yet: the parent source-qbasic measure/support selector signature is still unsigned.
- Poynting is not ignored: Hilbert-owned stationary EM is counted once in `T_total`; open/radiative wall flux remains an explicit boundary row.

## Support Invariance Theorem

| theorem_id | object | statement | status |
| --- | --- | --- | --- |
| SIT4766_0_measure_object | mu_H | mu_H := rho_H dV_H is the parent Hilbert source measure, including ordinary matter, binding, pressure and Hilbert-owned EM stress. | OBJECT_DEFINED |
| SIT4766_1_exact_qbasic_measure | mu_H(q(Phi)) | If mu_H=mu_bar[q(Phi)] and v is vertical, then along any vertical path Phi_s with q(Phi_s)=q(Phi_0), mu_H(Phi_s)=mu_H(Phi_0) as a Radon measure. | CONDITIONAL_THEOREM_DERIVED_PARENT_UNSIGNED |
| SIT4766_2_support_invariance | W_H=closure(supp mu_H) | Exact equality of Radon measures implies supp(mu_H(Phi_s))=supp(mu_H(Phi_0)); therefore W_H is invariant when selected before readout. | SUPPORT_INVARIANCE_DERIVED_CONDITIONAL |
| SIT4766_3_no_birth_death | mu_birth_TV | If the measure is exactly constant on the vertical fibre, no distributional source layer is born or killed. | NO_BIRTH_DERIVED_CONDITIONAL |
| SIT4766_4_trace_bypass | rho_H_trace_norm | The Reynolds shell product contains rho_H_trace_norm V_n_bound; if V_n_bound=0 and mu_birth_TV=0, shell zero does not require proving rho_H_trace_norm=0. | TRACE_ZERO_NO_LONGER_PRIMARY_ON_STRICT_BRANCH |
| SIT4766_5_poynting_escape | Phi_wall_Poynting_abs | Radiative/open Poynting flux can change the energy crossing a collar; that is not erased by support invariance and must be routed to the boundary flux row. | POYNTING_RETAINED_AS_BOUNDARY_ROW |

## Trace/Birth Gate Update

| row_id | quantity | new_rule | status |
| --- | --- | --- | --- |
| TBG4766_0_previous_trace_route | rho_H_trace_norm=0 | still sufficient | OPTIONAL_SUFFICIENT_ROUTE |
| TBG4766_1_support_velocity | V_n_bound=0 | follows from exact q-basic Hilbert source measure and W_H=closure(supp mu_H) | DERIVED_CONDITIONAL |
| TBG4766_2_birth_shell | mu_birth_TV=0 | follows from exact source measure equality along the vertical fibre | DERIVED_CONDITIONAL |
| TBG4766_3_shell_result | Q_edge_shell_abs=0 | rho_H_trace_norm*0 + 0 = 0 for finite trace/test/kernel ceilings | CONDITIONAL_ZERO_ROUTE_SHARPENED |
| TBG4766_4_fallback | Q_edge_shell_abs | Q_edge_shell_abs <= W_lambda_edge_max Phi_edge (rho_H_trace_norm V_n_bound + mu_birth_TV) | BOUND_ROUTE_RETAINED |

## Qedge Shell Closure Update

| update_id | formula_or_rule | status |
| --- | --- | --- |
| QEU4766_0_shell_term | Q_edge_shell = int_partialW phi_edge W_lambda rho_H_tr V_n dSigma + <phi_edge W_lambda, mu_birth> | UNCHANGED_OBJECT |
| QEU4766_1_support_zero | V_n_bound=0 and mu_birth_TV=0 if mu_H is exact q-basic and W_H=closure(supp mu_H) before readout | NEW_ZERO_ROUTE |
| QEU4766_2_boundary_not_shell | Q_edge_abs <= Q_edge_shell_abs + Q_edge_boundary_abs | BOUNDARY_RETAINED |
| QEU4766_3_claim_status | Q_edge_shell_abs=0 is not claimed yet | NONCLAIM |

## Poynting Wall Flux Row

| row_id | quantity | formula_or_zero_condition | status |
| --- | --- | --- | --- |
| PWF4766_0_owner | Poynting stress ownership | S_i=-T_EM(n,e_i) on the public observed-Hodge Maxwell branch | EXACT_IDENTITY_CONDITIONAL |
| PWF4766_1_stationary_zero | Phi_wall_Poynting=0 | stationary isolated source collar, time_avg(dU_EM/dt)=0, time_avg(int_W J.E dV)=0, no incoming/background/apparatus flux | CONDITIONAL_LOCAL_ZERO_NOT_GLOBAL |
| PWF4766_2_wall_flux_bound | Phi_wall_Poynting_abs | \|Phi_wall_Poynting\| <= \|dU_EM/dt\| + \|int_W J.E dV\| + \|Phi_incoming\| + \|Phi_apparatus\| | BOUND_TEMPLATE_READY_VALUES_MISSING |
| PWF4766_3_Qedge_boundary_insert | Q_edge_boundary_abs | \|Q_edge_boundary\| includes \|F_rad\| and Phi_wall_Poynting_abs where EM radiation crosses the collar | BOUNDARY_INSERT_READY_NONNUMERIC |

## Parent Source-Qbasic Signature Pack

| signature_id | quantity_or_clause | requirement | current_status |
| --- | --- | --- | --- |
| PSQ4766_0_source_action | S_src=Sbar_src[q(Phi),Psi,A,theta] | parent source action descends through q before variation | MISSING_PARENT_SIGNATURE |
| PSQ4766_1_measure_equality | mu_H(Phi_s)=mu_H(Phi_0) | Radon measure equality on vertical fibres, including EM stress owner | MISSING_PARENT_SIGNATURE |
| PSQ4766_2_support_selector | W_H=closure(supp mu_H) | support/collar selected before readout from the parent measure, not a residual threshold | MISSING_SELECTOR_SIGNATURE |
| PSQ4766_3_same_branch | tau_*,e_*,W_H,Pi_M,M_H_ref all same branch | no split frames or post-fit source conventions | MISSING_BRANCH_SIGNATURE |
| PSQ4766_4_poynting_clause | public Hodge or explicit wall flux | Poynting is either Hilbert-owned/stationary or bounded as Phi_wall_Poynting_abs | MISSING_POYNTING_BRANCH_SIGNATURE |
| PSQ4766_5_promotion_gate | Q_edge_shell_abs=0 | claim-ready only if PSQ4766_0..4 are signed and no MISSING markers remain | CLAIM_BLOCKED |

## QbarXH Product Update

| update_id | formula_or_rule | status |
| --- | --- | --- |
| QBU4766_0_support_zero_product | If exact q-basic mu_H and pre-readout W_H hold, then Q_edge_shell_abs=0 via V_n_bound=0 and mu_birth_TV=0. | CONDITIONAL_INSERT |
| QBU4766_1_open_product | \|Qbar_XH\| <= [P_M_bound(\|Q_bulk\| + Q_edge_boundary_abs + \|Q_shadow\|) + \|E_PiM_comm\|]/[M_0(1-epsilon_abs)] when Q_edge_shell_abs=0. | PRODUCT_SIMPLIFIED_CONDITIONAL_NONCLAIM |
| QBU4766_2_poynting_boundary | Q_edge_boundary_abs retains Phi_wall_Poynting_abs or F_rad_abs on open/radiative collars. | POYNTING_VISIBLE |

## Route Selection

| route_id | route | payoff | selection_status |
| --- | --- | --- | --- |
| ROUTE4766_0_trace_direct | prove rho_H_trace_norm=0 | valid but harder; not needed if support invariance closes V_n and birth | DEPRIORITIZED |
| ROUTE4766_1_support_invariance | prove exact q-basic measure implies fixed support/no birth | cleanest derivation route; built in this checkpoint | ATTEMPTED_CONDITIONAL |
| ROUTE4766_2_parent_signature | source action/measure/support selector signature | next target because it can promote the support-invariance theorem | SELECTED_NEXT |
| ROUTE4766_3_poynting_wall_bound | stationary zero or finite Poynting wall flux row | parallel EM/boundary branch if source collar is open or radiative | PARALLEL_REQUIRED |
| ROUTE4766_4_denominator_pack | M0 epsilon PiM Ecomm | still mandatory before local scoring | PARALLEL_REQUIRED |

## Promotion Gates

| gate_id | rule | enforced_effect |
| --- | --- | --- |
| PG4766_0_no_trace_overfocus | Do not require zero trace if support invariance proves V_n_bound=0 and mu_birth_TV=0. | permits cleaner proof route |
| PG4766_1_no_measure_slogan | Do not claim support invariance from infinitesimal prose; require exact q-basic Radon measure equality or a bound. | blocks soft closure |
| PG4766_2_no_threshold_support | W_H must be closure(supp mu_H), not a fitted threshold/readout mask. | blocks circular source collar |
| PG4766_3_no_poynting_erasure | Open/radiative Poynting wall flux must remain explicit. | blocks hiding EM flux in shell zero |
| PG4766_4_no_local_score | No local-GR/Newton/R10/PPN/WEP/clock/orbital/Maxwell claim from 4766. | keeps checkpoint private/nonclaim |

## Decision

`SOURCE_SUPPORT_INVARIANCE_LEMMA_DERIVED_CONDITIONAL_QBASIC_MEASURE_UNSIGNED_POYNTING_WALL_FLUX_RETAINED_NONCLAIM`

## Next Target

`4767-Y5-R2FR-parent-source-qbasic-signature-or-Poynting-wall-numeric-bound.md`
