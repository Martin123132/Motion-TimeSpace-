# 4321 - Dq source-readout factorization zero or Rsrc epsilon row

## Verdict

- Removed the independent standard-branch source-readout leg using the 4266 Hilbert/ADM theorem.
- Did **not** claim blanket `Dq_source_readout[Hperp]=0`.
- Derived the honest dependency bound for `epsilon_source_readout`.
- Kept `R_src_readout` tails and `Dq_coeff` coupling drift explicit.

## Main Bound
| formula_id | name | formula | status |
| --- | --- | --- | --- |
| F4321_1_epsilon_source_readout | dependency bound | epsilon_source_readout <= L_T epsilon_matter + L_g epsilon_geom + L_Sigma epsilon_boundary_projector + L_xi epsilon_tau + L_theta epsilon_theta_marker + epsilon_SR_hidden | BOUND_DERIVED_VALUES_MISSING |
| F4321_2_Rsrc | explicit readout residual | \|\|R_src_readout\|\| <= R_hidden_weights + R_post_readout + R_projector_comm + R_worldtube_selector | BOUND_DERIVED_VALUES_MISSING |
| F4321_4_Nsrc_substitution | 4319 substitution | N_src_nonHilbert <= \|\|U_B\|\|_inf(C_S C_perp sqrt(sum_{i!=SR} w_i epsilon_i^2 + w_SR epsilon_source_readout^2)+\|\|R_src_readout\|\|) | NONCLAIM_HANDOFF |

## Residual Ledger
| residual_id | residual | status | owner_note |
| --- | --- | --- | --- |
| Rsrc_hidden_weights | hidden source/species weights w_A(Phi) | MISSING_ZERO_OR_BOUND | not Dq_coeff unless it multiplies kappa_cal |
| Rsrc_post_readout | post-readout transfer tail | MISSING_ZERO_OR_BOUND | post-solution q-natural readout zeros it |
| Rsrc_projector_comm | source-readout projector commutator | MISSING_ZERO_OR_BOUND | can move to boundary/projector if q-owned |
| Rsrc_worldtube_selector | worldtube/collar selector reentry | MISSING_ZERO_OR_BOUND | owned by boundary/domain if not zero |
| Rsrc_coeff_excluded | delta kappa_cal Q_src | RETAINED_IN_DQ_COEFF | explicit no-double-count row |

## Decision
| decision_id | result | reason | next_action |
| --- | --- | --- | --- |
| DEC4321_0 | SOURCE_READOUT_INDEPENDENT_LEG_REMOVED_DEPENDENCY_BOUND_DERIVED_RSRC_RESIDUAL_RETAINED_NONCLAIM | The standard Hilbert/ADM source-readout theorem removes an independent source-readout slot, but Hperp closure now depends on matter, geometry, boundary/projector, tau, theta and explicit Rsrc tails. | 4322-Y5-R2FR-Dq-matter-descent-lift-or-geometry-theta-bound-row.md |

## Next Target
| next_target_id | next_target | preferred_route | fallback_route |
| --- | --- | --- | --- |
| NT4321_0 | 4322-Y5-R2FR-Dq-matter-descent-lift-or-geometry-theta-bound-row.md | derive delta_Hperp S_matter through g_obs(q) and theta_obs(q), with no direct hidden matter slot | write epsilon_matter <= L_mg epsilon_geom + L_mtheta epsilon_theta_marker + epsilon_matter_hidden as a nonclaim row |
