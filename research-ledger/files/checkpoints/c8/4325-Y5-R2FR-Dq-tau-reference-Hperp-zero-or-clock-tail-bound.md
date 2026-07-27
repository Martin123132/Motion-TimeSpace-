# 4325 - Dq tau-reference Hperp zero or clock-tail bound

## Verdict

- Lifted `Dq_tau[Hperp]=0` inside the one-parent tau/surface/frame/reference branch.
- Retained clock/reference tails for post-fit or split-frame branches.
- Simplified the source-readout row by removing `L_xi epsilon_tau` only in the locked branch.
- Next target is boundary/projector/domain leakage.

## Main Formulas
| formula_id | name | formula | status |
| --- | --- | --- | --- |
| F4325_0_zero | tau/reference Hperp zero | single parent tau+surface+coframe+reference lock => Dq_tau[Hperp]=0 => epsilon_tau=0 | CONDITIONAL_ZERO_DERIVED |
| F4325_1_clock_tail | clock/reference fallback | epsilon_tau <= R_tau_split + R_surface_motion + R_frame_coframe + R_clock_readout + R_orbital_readout + R_units + R_ref_fit + R_boundary_normal | BOUND_READY_VALUES_MISSING |
| F4325_2_source_readout_simplified | 4324 source-readout row after tau zero | epsilon_source_readout <= (L_T L_mg + L_g)epsilon_geom + L_Sigma epsilon_boundary_projector + Xi_src_hidden | STANDARD_BRANCH_SIMPLIFICATION |
| F4325_3_EDq_update | EDq component update | E_Dq,Hperp^2 := sum_{i!=tau} w_i epsilon_i^2 in the locked tau branch; otherwise add w_tau epsilon_tau^2 | NONCLAIM_HANDOFF |
| F4325_4_Nsrc_handoff | source-support handoff | N_src_nonHilbert <= \|\|U_B\|\|_inf(C_S C_perp E_Dq,Hperp + \|\|R_src_readout\|\|), with tau contribution removed only in locked branch | NONCLAIM_HANDOFF |

## Tail Firewall
| tail_id | symbol | status |
| --- | --- | --- |
| CT4325_0_tau_split | R_tau_split | MISSING_ZERO_OR_BOUND |
| CT4325_1_surface | R_surface_motion | MISSING_ZERO_OR_BOUND |
| CT4325_2_frame | R_frame_coframe | MISSING_ZERO_OR_BOUND |
| CT4325_3_clock | R_clock_readout | MISSING_ZERO_OR_BOUND |
| CT4325_4_orbit | R_orbital_readout | MISSING_ZERO_OR_BOUND |
| CT4325_5_units | R_units | MISSING_ZERO_OR_BOUND |
| CT4325_6_ref_fit | R_ref_fit | MISSING_ZERO_OR_BOUND |
| CT4325_7_boundary_normal | R_boundary_normal | ROUTE_TO_BOUNDARY_PROJECTOR |

## Decision
| decision_id | result | reason | next_action |
| --- | --- | --- | --- |
| DEC4325_0 | TAU_REFERENCE_HPERP_ZERO_LIFTED_FOR_SINGLE_PARENT_TIME_FRAME_BRANCH_CLOCK_TAIL_BOUND_RETAINED_NONCLAIM | 4216 gives a clean single-parent tau/surface/frame lock; lifted to Hperp it closes Dq_tau only inside that locked branch, with post-fit clock/reference tails retained. | 4326-Y5-R2FR-Dq-boundary-projector-Hperp-zero-or-domain-tail-bound.md |

## Next Target
| next_target_id | next_target | preferred_route | fallback_route |
| --- | --- | --- | --- |
| NT4325_0 | 4326-Y5-R2FR-Dq-boundary-projector-Hperp-zero-or-domain-tail-bound.md | prove source worldtube, projector, domain, surface normal and readout boundary are q-owned/fixed before variation | retain epsilon_boundary_projector <= projector commutator + domain wall + boundary normal/corner residuals |
