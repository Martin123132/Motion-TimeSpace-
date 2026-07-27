# 4773: Collar Instance Certificate or Shadow/Denominator/Projector First Values

Generated: `2026-07-08T03:34:20+00:00`

Marker: `PPC4161_COLLAR_INSTANCE_CERTIFICATE_OR_SHADOW_DENOMINATOR_PROJECTOR_FIRST_VALUES_4773`

## Result

- 4773 certifies one private mathematical instance: `C_static_iso_private`, an ideal compact stationary isolated collar-selector branch.
- This is **not** a public/global theorem and not an empirical local-GR/Newton claim.
- Inside `C_static_iso_private` plus the private no-shadow selector:

```text
E_boundary_total_4773 = 0_private_C_static_iso
Q_edge_shell_abs = 0_private_C_static_iso
Q_edge_boundary_abs = 0_private_C_static_iso
Q_shadow_abs = 0_private_selector
Q_tot_XH_abs = 0_private_collar_selector.
```

- The hard remaining product gate is:

```text
Qbar_XH = (Pi_M Q_tot_XH + E_PiM_comm) / M_lower.
```

Even with `Q_tot_XH=0`, no score fires until `M_lower>0` and projector/commutator gates are certified.

## Collar Instance Certificate

| certificate_id | object | certificate_clause | status |
| --- | --- | --- | --- |
| CIC4773_0_instance | C_static_iso_private | ideal compact stationary isolated local source collar | SIGNED_PRIVATE_MATH_INSTANCE |
| CIC4773_1_worldtube | W_H | W_H=closure(supp mu_H) before readout with compact support separation | SIGNED_PRIVATE |
| CIC4773_2_stationary | stationary averaging window | time-averaged dU_EM/dt=0 and no collar time flow | SIGNED_FOR_INSTANCE |
| CIC4773_3_same_Hodge | same Maxwell-Hodge/current owner | EM stress is Hilbert-owned once and Poynting is either stress flux or explicit wall flux | SIGNED_PRIVATE |
| CIC4773_4_no_external_flux | incoming/apparatus/radiative flux | Phi_incoming=Phi_apparatus=F_rad=B_app_support=0 | SIGNED_FOR_INSTANCE |
| CIC4773_5_fixed_boundary | matter and Hamiltonian boundary | delta_v psi fixed/compact or exact/q-owned; B_Ham_corner and B_normal_momentum vanish | SIGNED_FOR_INSTANCE |
| CIC4773_6_no_double_count | boundary accounting | lift-boundary, Poynting and Hamiltonian/corner rows are disjoint or identified by owner before summing | SIGNED_ACCOUNTING |
| CIC4773_7_boundary_total | E_boundary_total_4773 | E_boundary_total_4772=0_private_collar_candidate becomes E_boundary_total_4773=0_private_C_static_iso | CERTIFIED_PRIVATE_IDEAL_INSTANCE_NONCLAIM |

## Shadow Import Certificate

| shadow_id | shadow_channel | private_value_or_formula | status |
| --- | --- | --- | --- |
| SIC4773_0_standard_interface | canonical frame/source shadow slot | Q_shadow_action=0_private_selector | PRIVATE_IMPORT |
| SIC4773_1_projector_shadow | source-map/projector shadow | Q_shadow_projector=0_private_selector | PRIVATE_IMPORT |
| SIC4773_2_source_shadow | independent source functional shadow | source_shadow=0_private_selector | PRIVATE_IMPORT_FROM_4431_CONTRACT |
| SIC4773_3_nonvariational_shadow | nonvariational shadow | Q_shadow_nonvariational=0_private_selector | PRIVATE_IMPORT |
| SIC4773_4_shadow_total | Q_shadow_abs | 0_private_selector | SHADOW_ZERO_PRIVATE_SELECTOR_NONCLAIM |

## Numerator Collapse Update

| update_id | quantity | private_value_or_formula | status |
| --- | --- | --- | --- |
| NU4773_0_bulk | Q_bulk_XH_abs | 0_private_selector | PRIVATE_ZERO |
| NU4773_1_edge_shell | Q_edge_shell_abs | 0_private_C_static_iso | PRIVATE_ZERO |
| NU4773_2_edge_boundary | Q_edge_boundary_abs | 0_private_C_static_iso | PRIVATE_ZERO |
| NU4773_3_edge_total | Q_edge_XH_abs | 0_private_C_static_iso | PRIVATE_ZERO |
| NU4773_4_shadow | Q_shadow_abs | 0_private_selector | PRIVATE_ZERO |
| NU4773_5_Qtot | Q_tot_XH_abs | 0_private_collar_selector | NUMERATOR_COLLAPSED_NONCLAIM |
| NU4773_6_open_fallback | Q_tot_XH_abs_open | \|Q_bulk\|+\|Q_edge_shell\|+E_boundary_total_4772_open+\|Q_shadow\| | FINITE_FALLBACK_RETAINED |

## Denominator/Projector Remaining Gate

| gate_id | quantity | formula_or_condition | current_status | status |
| --- | --- | --- | --- | --- |
| DG4773_0_projector_comm | E_PiM_comm | 0_private_if Pi_M is fixed/q-basic and selected before readout | conditional theorem from 4764 DL4764_3, not yet an empirical/source-backed row | CONDITIONAL_PROJECTOR_LOCK |
| DG4773_1_projector_norm | P_M_bound | finite if Pi_M is a fixed bounded projector on the chosen source norm | operator norm/value still not supplied | VALUE_OR_NORM_MISSING |
| DG4773_2_denominator | M_lower | M_0(1-epsilon_abs)>0 | requires M_0>0 and 0<=epsilon_abs<1 with same-frame units; source-backed values still missing | POSITIVE_LOCK_MISSING |
| DG4773_3_qbar_private | Qbar_XH | (P_M Q_tot + E_PiM_comm)/M_lower | with Q_tot=0 and E_PiM_comm=0, Qbar=0 only after M_lower>0 is certified | BLOCKED_BY_DENOMINATOR_POSITIVITY |
| DG4773_4_score_policy | local-GR/Newton score | do not score from numerator collapse alone | must next certify denominator/projector positivity or fill first source-backed values | PRODUCT_STILL_BLOCKED |

## Route Selection

| route_id | route | payoff | selection_status |
| --- | --- | --- | --- |
| ROUTE4773_0_denominator_projector | certify M_lower>0 and projector lock or fill first M_0/epsilon_abs/P_M_bound/E_PiM_comm rows | last hard product gate after private numerator collapse | SELECTED_NEXT |
| ROUTE4773_1_open_arena_values | fill finite open-collar and off-selector values | needed for radiative/lab/apparatus arenas that do not satisfy C_static_iso | PARALLEL |
| ROUTE4773_2_public_parent | promote private collar-selector instance to one public parent action selector | would turn private branch into public theorem rather than private local instance | LONGER_ROUTE |

## Promotion Gates

| gate_id | rule | enforced_effect | claim_allowed |
| --- | --- | --- | --- |
| GATE4773_0_private_scope | C_static_iso is a private ideal collar-selector instance, not a public/global MTS theorem. | prevents public overclaim | False |
| GATE4773_1_open_fallback | Open/radiative/nonstationary/apparatus arenas must use finite fallback rows. | prevents using static collar zero outside domain | False |
| GATE4773_2_shadow_scope | Q_shadow_abs=0 is private selector only; off-selector source-shadow countermodels remain active. | keeps shadow risk honest | False |
| GATE4773_3_denominator | Qbar/local-GR score cannot fire until M_lower>0 and projector/commutator gates are certified. | blocks numerator-only scoring | False |

## Decision

`PRIVATE_COMPACT_COLLAR_SELECTOR_INSTANCE_CERTIFIED_NUMERATOR_COLLAPSES_CONDITIONALLY_TO_ZERO_DENOMINATOR_PROJECTOR_POSITIVITY_STILL_BLOCKS_QBAR_SCORE_NONCLAIM`

## Next Target

`4774-Y5-R2FR-denominator-projector-positive-lock-or-first-source-backed-M0-epsilon-row.md`
