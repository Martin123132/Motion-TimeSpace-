# 4772: Boundary-Lift/Poynting Collar Zero or Denominator/Projector First Values

Generated: `2026-07-08T03:28:35+00:00`

Marker: `PPC4161_BOUNDARY_LIFT_POYNTING_COLLAR_ZERO_OR_DENOMINATOR_PROJECTOR_FIRST_VALUES_4772`

## Result

- 4772 derives a compact stationary isolated collar zero theorem for the remaining boundary numerator obstruction.
- The theorem is conditional/private: it is not yet an actual source-collar instance and not a local-GR/Newton claim.
- Under the collar contract:

```text
E_lift_boundary = 0
E_Poynting_wall = 0
E_boundary_flux = 0
E_boundary_total_4772 := |E_lift_boundary|+|E_Poynting_wall|+|E_boundary_flux| = 0.
```

- If the collar is open, radiative, nonstationary, apparatus-supported, or not fixed/exact/q-owned, the finite envelope must be used instead:

```text
E_boundary_total_4772_open <=
  |int_partialW Theta_m(delta_v psi)|
+ |dU_EM/dt| + |int_W J.E dV|
+ |Phi_incoming| + |Phi_apparatus|
+ |F_rad| + |B_Ham_corner| + |B_normal_momentum| + |B_app_support|.
```

## Compact Stationary Collar Zero Theorem

| theorem_id | quantity | value_or_rule | status |
| --- | --- | --- | --- |
| CCT4772_0_branch_selector | compact_stationary_isolated_same_Hodge_fixed_boundary_collar | branch_contract_written | CONDITIONAL_BRANCH_NOT_INSTANCE |
| CCT4772_1_lift_boundary_zero | E_lift_boundary | 0_private_if_CCT4772_0 | ZERO_CANDIDATE |
| CCT4772_2_poynting_zero | E_Poynting_wall | 0_private_if_CCT4772_0 | ZERO_CANDIDATE |
| CCT4772_3_boundary_flux_zero | E_boundary_flux | 0_private_if_CCT4772_0 | ZERO_CANDIDATE_CONDITIONAL |
| CCT4772_4_no_double_count | boundary channel placement | no_hidden_cancellation | ACCOUNTING_RULE |
| CCT4772_5_total | E_boundary_total_4772 | 0_private_collar_candidate | TOTAL_ZERO_CANDIDATE_NONCLAIM |

## Open-Collar Finite Envelope

| envelope_id | quantity | formula | status |
| --- | --- | --- | --- |
| OCE4772_0_lift | E_lift_boundary | \|int_partialW Theta_m(delta_v psi)\| | VALUE_NEEDED_IF_OPEN |
| OCE4772_1_poynting | E_Poynting_wall | \|dU_EM/dt\|+\|int_W J.E dV\|+\|Phi_incoming\|+\|Phi_apparatus\| | VALUE_NEEDED_IF_OPEN |
| OCE4772_2_hamiltonian_corner | E_boundary_flux | \|F_rad\|+\|B_Ham_corner\|+\|B_normal_momentum\|+\|B_app_support\| | VALUE_NEEDED_IF_OPEN |
| OCE4772_3_total | E_boundary_total_4772 | \|int_partialW Theta_m(delta_v psi)\|+\|dU_EM/dt\|+\|int_W J.E dV\|+\|Phi_incoming\|+\|Phi_apparatus\|+\|F_rad\|+\|B_Ham_corner\|+\|B_normal_momentum\|+\|B_app_support\| | FINITE_FALLBACK_TEMPLATE |
| OCE4772_4_score_policy | boundary score policy | zero candidate can be used only after a source collar instance signs CCT4772_0; otherwise use OCE4772_3 | POLICY_ROW |

## Qedge/Qbar Update

| update_id | rule | meaning | status |
| --- | --- | --- | --- |
| QQ4772_0_bulk_qbasic | E_bulk_source_qbasic_4771=0_private_conditional is retained. | bulk source-qbasic no longer blocks the private compact-collar branch | BULK_CLOSED_PRIVATE |
| QQ4772_1_shell_zero | Q_edge_shell_abs=0 if bulk qbasicity, pre-readout support, and no boundary lift birth/death hold. | compact collar branch supplies no boundary birth/death; open collar uses finite envelope | SHELL_ZERO_CONDITIONAL |
| QQ4772_2_boundary_zero | Q_edge_boundary_abs=0_private_collar_candidate if E_boundary_total_4772=0. | requires actual compact stationary isolated source-collar instance | BOUNDARY_ZERO_CANDIDATE |
| QQ4772_3_open_boundary | Q_edge_boundary_abs <= E_boundary_total_4772_open + other corner/shadow rows on open collars. | no cancellation; use finite envelope if branch is not signed | FINITE_FALLBACK |
| QQ4772_4_qbar_product | Qbar_XH score remains blocked by Q_shadow_abs, M_lower, P_M_bound and E_PiM_comm. | boundary progress is necessary but not enough for local-GR/Newton scoring | PRODUCT_BLOCKED |

## Local Scoring Gate Status

| gate_id | gate | needed_evidence | current_status | score_fires_now | status |
| --- | --- | --- | --- | --- | --- |
| SG4772_0_collar_instance | compact collar instance | must sign CCT4772_0 for the actual local source arena | not yet supplied | False | INSTANCE_MISSING |
| SG4772_1_boundary_total | E_boundary_total_4772 | zero candidate or finite source-backed envelope | conditional zero candidate plus finite template exists | False | CONDITIONAL_OR_VALUE_NEEDED |
| SG4772_2_shadow | Q_shadow_abs | no-shadow theorem or finite residual | not closed by collar theorem | False | MISSING |
| SG4772_3_denominator | M_lower=M_0(1-epsilon_abs)>0 | source-backed positive denominator | M_0 and epsilon_abs still missing values | False | MISSING |
| SG4772_4_projector | P_M_bound and E_PiM_comm | finite norm and zero/bounded commutator | projector first values still missing | False | MISSING |
| SG4772_5_qbar | Qbar_XH local score | collar instance, shadow, denominator and projector all closed | blocked by SG4772_0..4 | False | PRODUCT_BLOCKED |

## Route Selection

| route_id | route | payoff | selection_status |
| --- | --- | --- | --- |
| ROUTE4772_0_collar_instance | write the actual compact-collar source instance certificate | turns the zero candidate into a branch-specific usable gate, or rejects it cleanly | SELECTED_NEXT |
| ROUTE4772_1_shadow_denominator_projector | fill Q_shadow_abs, M_0, epsilon_abs, P_M_bound and E_PiM_comm | needed before any Qbar/local-GR score can fire even if collar zero holds | PARALLEL_HIGH_VALUE |
| ROUTE4772_2_open_collar_values | fill finite open-collar boundary envelope values | lets the branch be bounded instead of zero-assumed if compact collar fails | FALLBACK |
| ROUTE4772_3_public_parent | promote collar branch to public parent selector | would turn conditional private collar theorem into public MTS result | LONGER_ROUTE |

## Promotion Gates

| gate_id | rule | enforced_effect | claim_allowed |
| --- | --- | --- | --- |
| GATE4772_0_instance | Do not use E_boundary_total_4772=0 until an actual compact stationary isolated collar instance signs all CCT4772_0 clauses. | blocks branch smuggling | False |
| GATE4772_1_open_fallback | Open/radiative/nonstationary collars must use the finite envelope, not the zero candidate. | keeps waves and apparatus visible | False |
| GATE4772_2_no_double_count | Boundary lift, Poynting and Hamiltonian/corner flux cannot be double-counted or cancelled against each other unless one owner identity proves equivalence. | blocks fake no-cancellation algebra | False |
| GATE4772_3_qbar | Qbar/local-GR score cannot fire without shadow, denominator and projector gates. | blocks premature local-GR/Newton scoring | False |

## Decision

`COMPACT_STATIONARY_COLLAR_ZERO_THEOREM_DERIVED_CONDITIONAL_BOUNDARY_TOTAL_ZERO_CANDIDATE_OPEN_COLLAR_FINITE_ENVELOPE_RETAINED_QBAR_STILL_BLOCKED_BY_SHADOW_DENOMINATOR_PROJECTOR_NONCLAIM`

## Next Target

`4773-Y5-R2FR-collar-instance-certificate-or-shadow-denominator-projector-first-values.md`
