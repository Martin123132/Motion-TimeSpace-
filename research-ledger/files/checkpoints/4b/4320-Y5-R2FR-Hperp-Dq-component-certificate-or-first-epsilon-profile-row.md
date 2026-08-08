# 4320 - Hperp Dq component certificate or first epsilon profile row

## Verdict

- Ranked the eight `Dq_i[Hperp]` component gates.
- Picked `Dq_source_readout[Hperp]` as the next target because it controls both `E_Dq,Hperp` and `R_src_readout`.
- Kept geometry second, using the existing `epsilon_geom` five-piece profile rather than re-circling it.
- No local-GR/Newton claim fires.

## Dq Component Status
| rank | component | status | fallback_epsilon_row | feeds |
| --- | --- | --- | --- | --- |
| 1 | Dq_source_readout[Hperp] | PRIMARY_NEXT_TARGET | epsilon_source_readout >= \|\|Dq_source_readout[Hperp]\|\| and R_src_readout finite or zero | E_Dq,Hperp and explicit R_src_readout |
| 2 | Dq_geom[Hperp] | MATURE_EPSILON_PROFILE_ROUTE | epsilon_geom <= epsilon_Oloc+epsilon_coframe+epsilon_projector+epsilon_wall+epsilon_Hodge_geom | E_Dq,Hperp |
| 3 | Dq_EM[Hperp] | EM_HODGE_ROUTE_AVAILABLE | epsilon_EM >= \|\|Dq_EM[Hperp]\|\| with EM/Hodge residual envelope | E_Dq,Hperp |
| 4 | Dq_tau[Hperp] | REFERENCE_TIME_ROUTE_OPEN | epsilon_tau >= \|\|Dq_tau[Hperp]\|\| | E_Dq,Hperp and clock arena |
| 5 | Dq_matter[Hperp] | MATTER_DESCENT_ROUTE_OPEN | epsilon_matter >= \|\|Dq_matter[Hperp]\|\| | E_Dq,Hperp and source equality |
| 6 | Dq_boundary_projector[Hperp] | BOUNDARY_DOMAIN_ROUTE_OPEN | epsilon_boundary_projector >= \|\|Dq_boundary_projector[Hperp]\|\| | E_Dq,Hperp and N_boundary_domain |
| 7 | Dq_theta_marker[Hperp] | MARKER_SELECTOR_ROUTE_OPEN | epsilon_theta_marker >= \|\|Dq_theta_marker[Hperp]\|\| | E_Dq,Hperp and selector drift |
| 8 | Dq_coeff[Hperp] | COEFFICIENT_DESCENT_ROUTE_OPEN | epsilon_coeff >= \|\|Dq_coeff[Hperp]\|\| | E_Dq,Hperp and coefficient naturalness |

## Source Readout Schema
| symbol | requirement | status |
| --- | --- | --- |
| source_factor_q_certificate | source/readout functional factors as S_bar[q(Phi),Psi,theta] | MISSING_PARENT_SIGNATURE |
| source_label_Hperp_leg | no Hperp representative source-label leg survives quotient stripping | MISSING_PARENT_SIGNATURE |
| readout_projector_commutator | \|\|[P_readout,Dq]Hperp\|\| or theorem-zero equivalent | MISSING_BOUND_OR_ZERO |
| epsilon_source_readout | epsilon_source_readout >= \|\|Dq_source_readout[Hperp]\|\| | MISSING_VALUE |
| R_src_readout | explicit residual in S_cg_nonHilbert = S_A Hperp^A + R_src_readout | MISSING_VALUE |
| U_B_scope | U_B belongs to the local branch being scored and is not a transition-shell shortcut | MISSING_SCOPE_CERTIFICATE |

## Formulas
| formula_id | name | formula | status |
| --- | --- | --- | --- |
| F4320_0_EDq | combined Hperp Dq defect | E_Dq,Hperp^2 := sum_i w_i epsilon_i^2, epsilon_i >= \|\|Dq_i[Hperp]\|\| | FORMULA_READY_VALUES_MISSING |
| F4320_1_Nsrc | source-support finite row | N_src_nonHilbert <= \|\|U_B\|\|_inf(C_S C_perp E_Dq,Hperp + \|\|R_src_readout\|\|) | BOUND_READY_SOURCE_READOUT_INPUTS_MISSING |
| F4320_2_source_readout_zero | source/readout deletion condition | if Dq_source_readout[Hperp]=0 and R_src_readout=0, remove epsilon_source_readout and R_src_readout from the 4319 source row | CONDITIONAL_ZERO_ROUTE |
| F4320_3_geometry_import | geometry profile import | epsilon_geom <= epsilon_Oloc+epsilon_coframe+epsilon_projector+epsilon_wall+epsilon_Hodge_geom | PROFILE_READY_VALUES_MISSING |
| F4320_4_Nrest_handoff | canonical residual handoff | N_rest_nonEM^canon = N_src_nonHilbert + N_drift_selector + N_history_transition + N_boundary_domain + N_N | HANDOFF_READY_NO_CLAIM |

## Decision
| decision_id | result | reason | next_action |
| --- | --- | --- | --- |
| DEC4320_0 | DQ_COMPONENTS_CLASSIFIED_SOURCE_READOUT_AND_GEOMETRY_PRIORITIZED_EPSILON_PROFILE_ROUTE_STAGED_NONCLAIM | Dq_source_readout[Hperp] is the highest-leverage component because it feeds both E_Dq,Hperp and explicit R_src_readout; geometry is mature but still blocked by A_MF/no-shadow. | 4321-Y5-R2FR-Dq-source-readout-factorization-zero-or-Rsrc-epsilon-row.md |

## Next Target
| next_target_id | next_target | preferred_route | fallback_route |
| --- | --- | --- | --- |
| NT4320_0 | 4321-Y5-R2FR-Dq-source-readout-factorization-zero-or-Rsrc-epsilon-row.md | prove source/readout factors through q and has no Hperp source-label leg | write nonclaim epsilon_source_readout and R_src_readout bound rows with parent/source paths |
