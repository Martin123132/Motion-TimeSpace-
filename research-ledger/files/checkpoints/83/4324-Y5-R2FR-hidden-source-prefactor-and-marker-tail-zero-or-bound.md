# 4324 - hidden source-prefactor and marker-tail zero or bound

## Verdict

- Did not fake the no-hidden-slot theorem; 4304 says it is not globally parent-signed.
- Derived the master hidden source-coupling budget `Xi_src_hidden`.
- Isolated hidden source tails inside the matter and source-readout formulas.
- Set next target to the tau/reference clock row.

## Master Budget
| formula_id | name | formula | status |
| --- | --- | --- | --- |
| F4324_0_master_tail | hidden source-prefactor master budget | Xi_src_hidden := epsilon_matter_hidden + epsilon_SR_hidden + R_marker_source_label + R_hidden_weights + R_source_normalization + delta_w_EM + R_no_direct_m_charge + R_environment_selector | DERIVED_MASTER_BUDGET |
| F4324_1_tail_bound | source-label derivative fallback | Xi_src_hidden <= C_w\|\|D_Hperp ln w_A\|\| + C_norm\|\|D_Hperp ln N_src\|\| + C_mark\|\|D_Hperp theta_src\|\| + C_op\|\|D_Hperp O_hidden\|\| + C_EM\|\|delta_w_EM\|\| + C_inner\|\|Q_m^H\|\| + C_env\|\|D_Hperp sigma_env\|\| | BOUND_READY_VALUES_MISSING |
| F4324_2_zero | no-hidden-slot zero | if source-label forgetting/no-hidden-slot theorem is parent-signed, then Xi_src_hidden=0 | CONDITIONAL_ZERO_ROUTE_NOT_PARENT_SIGNED |

## Reduced Dependencies
| formula_id | name | formula | status |
| --- | --- | --- | --- |
| F4324_3_matter_substitution | 4323 matter row with hidden tail isolated | epsilon_matter <= L_mg epsilon_geom + epsilon_matter_hidden <= L_mg epsilon_geom + Xi_src_hidden | REDUCED_DEPENDENCY_HANDOFF |
| F4324_4_source_readout_substitution | 4323 source-readout row with hidden tails isolated | epsilon_source_readout <= (L_T L_mg + L_g)epsilon_geom + L_Sigma epsilon_boundary_projector + L_xi epsilon_tau + Xi_src_hidden | REDUCED_DEPENDENCY_HANDOFF |

## Decision
| decision_id | result | reason | next_action |
| --- | --- | --- | --- |
| DEC4324_0 | NO_HIDDEN_SLOT_NOT_PARENT_SIGNED_SOURCE_PREFACTOR_MASTER_TAIL_BOUND_DERIVED_NONCLAIM | The corpus has a clean no-hidden-slot zero route but 4304 explicitly does not parent-sign it globally, so hidden source-prefactor/marker tails become the master coupling budget Xi_src_hidden. | 4325-Y5-R2FR-Dq-tau-reference-Hperp-zero-or-clock-tail-bound.md |

## Next Target
| next_target_id | next_target | preferred_route | fallback_route |
| --- | --- | --- | --- |
| NT4324_0 | 4325-Y5-R2FR-Dq-tau-reference-Hperp-zero-or-clock-tail-bound.md | prove local tau/reference normal is q-owned/fixed before variation and has no hidden clock-standard leg | retain epsilon_tau <= clock/reference Jacobian tail plus boundary/normal residual |
