# 4322 - Dq matter descent lift or geometry theta bound row

## Verdict

- Removed `Dq_matter[Hperp]` as an independent mystery component in the standard branch.
- Derived `epsilon_matter <= L_mg epsilon_geom + L_mtheta epsilon_theta_marker + epsilon_matter_hidden`.
- Substituted the matter bound into the 4321 source-readout dependency row.
- Kept hidden matter/source-prefactor, EM and domain tails explicit.

## Main Formulas
| formula_id | name | formula | status |
| --- | --- | --- | --- |
| F4322_0_chain_rule | matter action chain rule | delta_Hperp S_matter = S_g delta_Hperp g_obs + S_theta delta_Hperp theta_obs + R_matter_hidden | DERIVED |
| F4322_1_epsilon_matter | matter dependency bound | epsilon_matter <= L_mg epsilon_geom + L_mtheta epsilon_theta_marker + epsilon_matter_hidden | BOUND_DERIVED_VALUES_MISSING |
| F4322_2_exact_zero | exact matter component zero | if epsilon_geom=epsilon_theta_marker=epsilon_matter_hidden=0, then Dq_matter[Hperp]=0 | CONDITIONAL_ZERO_ROUTE |
| F4322_3_source_readout_substitution | source-readout with matter substituted | epsilon_source_readout <= (L_T L_mg + L_g)epsilon_geom + (L_T L_mtheta + L_theta)epsilon_theta_marker + L_Sigma epsilon_boundary_projector + L_xi epsilon_tau + L_T epsilon_matter_hidden + epsilon_SR_hidden | REDUCED_DEPENDENCY_HANDOFF |
| F4322_4_Nsrc_handoff | 4319 source-support handoff | N_src_nonHilbert <= \|\|U_B\|\|_inf(C_S C_perp E_Dq,Hperp + \|\|R_src_readout\|\|), with epsilon_matter replaced by F4322_1 where used | NONCLAIM_HANDOFF |

## Component Update
| update_id | component | status | new_row |
| --- | --- | --- | --- |
| CU4322_0 | Dq_matter[Hperp] | INDEPENDENT_LEG_REMOVED_GEOMETRY_THETA_BOUND_RETAINED | epsilon_matter <= L_mg epsilon_geom + L_mtheta epsilon_theta_marker + epsilon_matter_hidden |
| CU4322_1 | Dq_source_readout[Hperp] | SOURCE_READOUT_DEPENDENCY_REDUCED | substitute epsilon_matter bound into 4321 source-readout formula |
| CU4322_2 | Dq_theta_marker[Hperp] | NEXT_TARGET | theta is the easiest remaining dependency because 4264 already adopted the standard q-basic row |

## Decision
| decision_id | result | reason | next_action |
| --- | --- | --- | --- |
| DEC4322_0 | MATTER_COMPONENT_INDEPENDENT_LEG_REMOVED_GEOMETRY_THETA_DEPENDENCY_BOUND_DERIVED_NONCLAIM | The 4265/4277 matter-domain theorem removes an independent matter component, but Hperp closure depends on observed geometry, theta markers and explicit hidden matter tails. | 4323-Y5-R2FR-Dq-theta-marker-Hperp-zero-lift-or-marker-tail-bound.md |

## Next Target
| next_target_id | next_target | preferred_route | fallback_route |
| --- | --- | --- | --- |
| NT4322_0 | 4323-Y5-R2FR-Dq-theta-marker-Hperp-zero-lift-or-marker-tail-bound.md | prove theta_obs is fixed before variation and has no hidden marker/source-label insertion for Hperp | retain epsilon_theta_marker <= marker Jacobian tail plus source-label/environment selector residuals |
