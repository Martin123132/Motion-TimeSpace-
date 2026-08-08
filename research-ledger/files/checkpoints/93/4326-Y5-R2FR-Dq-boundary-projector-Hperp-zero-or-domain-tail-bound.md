# 4326 - Dq boundary-projector Hperp zero or domain-tail bound

## Verdict

- Lifted `Dq_boundary_projector[Hperp]=0` inside the q-basic no-flux domain branch.
- Retained domain/projector/radiative/source-crossing tails outside that branch.
- Simplified source-readout to geometry plus `Xi_src_hidden`.
- Next target is geometry/no-shadow.

## Main Formulas
| formula_id | name | formula | status |
| --- | --- | --- | --- |
| F4326_0_zero | boundary/projector Hperp zero | q-basic projector + q-owned/fixed domain + no wall/denominator + differentiability-owned no-flux boundary => Dq_boundary_projector[Hperp]=0 => epsilon_boundary_projector=0 | CONDITIONAL_ZERO_DERIVED |
| F4326_1_domain_tail | domain/projector fallback | epsilon_boundary_projector <= R_P_metric + R_domain + R_Hodge_readout + R_wall + R_denominator + R_source_readout + R_diff_owner + R_corner_edge + R_rad_flux + R_source_crossing + R_memory_pullback + R_improvement | BOUND_READY_VALUES_MISSING |
| F4326_2_source_readout_simplified | 4325 source-readout row after boundary/projector zero | epsilon_source_readout <= (L_T L_mg + L_g)epsilon_geom + Xi_src_hidden | STANDARD_BRANCH_SIMPLIFICATION |
| F4326_3_EDq_update | EDq component update | E_Dq,Hperp^2 := sum_{i!=tau,boundary_projector} w_i epsilon_i^2 in the locked no-flux branch; otherwise include w_boundary epsilon_boundary_projector^2 | NONCLAIM_HANDOFF |
| F4326_4_Nsrc_handoff | source-support handoff | N_src_nonHilbert <= \|\|U_B\|\|_inf(C_S C_perp E_Dq,Hperp + \|\|R_src_readout\|\|), with boundary contribution removed only in the q-basic no-flux branch | NONCLAIM_HANDOFF |

## Tail Firewall
| tail_id | symbol | status |
| --- | --- | --- |
| DT4326_0_metric | R_P_metric | MISSING_ZERO_OR_BOUND |
| DT4326_1_domain | R_domain | MISSING_ZERO_OR_BOUND |
| DT4326_2_hodge | R_Hodge_readout | MISSING_ZERO_OR_BOUND |
| DT4326_3_wall | R_wall | MISSING_ZERO_OR_BOUND |
| DT4326_4_denominator | R_denominator | MISSING_ZERO_OR_BOUND |
| DT4326_5_source_readout | R_source_readout | MISSING_ZERO_OR_BOUND |
| DT4326_6_diff | R_diff_owner | MISSING_ZERO_OR_BOUND |
| DT4326_7_corner | R_corner_edge | MISSING_ZERO_OR_BOUND |
| DT4326_8_rad | R_rad_flux | ROUTE_AS_BOUNDARY_FLUX |
| DT4326_9_crossing | R_source_crossing | MISSING_ZERO_OR_BOUND |
| DT4326_10_memory | R_memory_pullback | MISSING_ZERO_OR_BOUND |
| DT4326_11_improvement | R_improvement | MISSING_ZERO_OR_BOUND |

## Decision
| decision_id | result | reason | next_action |
| --- | --- | --- | --- |
| DEC4326_0 | BOUNDARY_PROJECTOR_HPERP_ZERO_LIFTED_FOR_QBASIC_NOFLUX_DOMAIN_BRANCH_DOMAIN_TAIL_BOUND_RETAINED_NONCLAIM | 4214/4217/4176 give a clean q-basic no-flux projector/domain zero route, but domain, wall, radiation and source-crossing tails are retained outside that branch. | 4327-Y5-R2FR-Dq-geometry-no-shadow-or-epsilon-geom-profile-reduction.md |

## Next Target
| next_target_id | next_target | preferred_route | fallback_route |
| --- | --- | --- | --- |
| NT4326_0 | 4327-Y5-R2FR-Dq-geometry-no-shadow-or-epsilon-geom-profile-reduction.md | parent-sign observed coframe/metric/Hodge/no-shadow descent for Hperp | retain epsilon_geom <= epsilon_Oloc+epsilon_coframe+epsilon_projector+epsilon_wall+epsilon_Hodge_geom and route to finite local tests |
