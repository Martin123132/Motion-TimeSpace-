# 4323 - Dq theta-marker Hperp zero lift or marker-tail bound

## Verdict

- Lifted the 4264 theta-marker zero to `Dq_theta_marker[Hperp]=0` inside the standard calibrated q-basic branch.
- Kept marker/source-label/environment tails explicit outside that branch.
- Simplified the 4322 matter row and 4321 source-readout row by deleting the theta term.
- No numerical-constant or local-GR claim fires.

## Simplified Formulas
| formula_id | name | formula | status |
| --- | --- | --- | --- |
| F4323_0_zero | standard theta zero | D_Hperp theta_obs=0 => Dq_theta_marker[Hperp]=0 => epsilon_theta_marker=0 | CONDITIONAL_ZERO_DERIVED |
| F4323_2_matter_simplified | 4322 matter row after theta zero | epsilon_matter <= L_mg epsilon_geom + epsilon_matter_hidden | STANDARD_BRANCH_SIMPLIFICATION |
| F4323_3_source_readout_simplified | 4321 source-readout row after theta zero and matter substitution | epsilon_source_readout <= (L_T L_mg + L_g)epsilon_geom + L_Sigma epsilon_boundary_projector + L_xi epsilon_tau + L_T epsilon_matter_hidden + epsilon_SR_hidden | STANDARD_BRANCH_SIMPLIFICATION |

## Tail Firewall
| tail_id | tail | status |
| --- | --- | --- |
| MT4323_0_mass_label | m_A(Phi) | MISSING_ZERO_OR_BOUND_OUTSIDE_STANDARD_BRANCH |
| MT4323_1_charge_label | charge labels(Phi) or alpha_EM(Phi) | MISSING_ZERO_OR_BOUND_OUTSIDE_STANDARD_BRANCH |
| MT4323_2_clock_standard | clock standards(Phi), hbar(Phi), c(Phi) | MISSING_ZERO_OR_BOUND_OUTSIDE_STANDARD_BRANCH |
| MT4323_3_material_label | material labels(Phi) | MISSING_ZERO_OR_BOUND_OUTSIDE_STANDARD_BRANCH |
| MT4323_4_source_normalization | source normalization(Phi) | ROUTE_TO_HIDDEN_SOURCE_PREFACTOR_OR_RSRC |
| MT4323_5_environment_selector | environment selectors(Phi) | ROUTE_TO_SELECTOR_OR_BOUNDARY |

## Decision
| decision_id | result | reason | next_action |
| --- | --- | --- | --- |
| DEC4323_0 | THETA_MARKER_HPERP_ZERO_LIFTED_FOR_STANDARD_CALIBRATED_BRANCH_MARKER_TAIL_BOUND_RETAINED_NONCLAIM | The calibrated q-basic theta row is fixed before variation, so the Hperp theta-marker component closes in the standard branch; marker/source-label tails remain explicit outside that branch. | 4324-Y5-R2FR-hidden-source-prefactor-and-marker-tail-zero-or-bound.md |

## Next Target
| next_target_id | next_target | preferred_route | fallback_route |
| --- | --- | --- | --- |
| NT4323_0 | 4324-Y5-R2FR-hidden-source-prefactor-and-marker-tail-zero-or-bound.md | prove source-label forgetting/no-hidden-slot theorem for w_A(Phi), source normalization and marker tails | retain epsilon_matter_hidden, epsilon_SR_hidden and R_marker/source-prefactor rows with no-cancellation bounds |
