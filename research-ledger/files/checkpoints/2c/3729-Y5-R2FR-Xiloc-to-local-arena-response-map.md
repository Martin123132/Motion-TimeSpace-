# 3729 - Xi_loc to Local Arena Response Map

## Status
- `RESPONSE_MAP_READY_CURRENTLY_BLOCKED_BY_XILOC_AND_ARENA_INPUTS`
- Main response law: `residual_bound_A=beta_A*sigma_A/(Xi_loc-ell_A)+epsilon_A`.
- Pass condition: `Xi_loc>ell_A` and `residual_bound_A<=bound_A`.
- This is a bridge from local coercivity to measurable arenas, not a claim that local GR/Newton/Maxwell has been recovered.

## Derived Contract
- Coercive local branch: `<h,Lh> >= Xi_loc||h||^2`.
- Arena nonlinear loss: `||N_A(h)|| <= ell_A||h||`.
- Source/coupling norm: `||source_A|| <= sigma_A`.
- Observable map norm: `||B_A|| <= beta_A`.
- Therefore `||residual_A|| <= beta_A*sigma_A/(Xi_loc-ell_A)+epsilon_A`, if `ell_A < Xi_loc`.

## Arena Rows
- `R10_short_range`: alpha(lambda) fifth-force residual | baseline: Newton inverse-square laboratory torsion response | status `RESPONSE_CONTRACT_READY_CURRENTLY_BLOCKED`
- `PPN_solar_system`: PPN residual vector including gamma-1, beta-1, preferred-frame terms | baseline: metric GR weak-field post-Newtonian limit | status `RESPONSE_CONTRACT_READY_CURRENTLY_BLOCKED`
- `clock_redshift`: fractional frequency/redshift residual | baseline: GR proper-time and gravitational redshift limit | status `RESPONSE_CONTRACT_READY_CURRENTLY_BLOCKED`
- `orbital_dynamics`: perihelion, range, timing, and acceleration residual vector | baseline: Newtonian plus GR weak-field orbital dynamics | status `RESPONSE_CONTRACT_READY_CURRENTLY_BLOCKED`
- `EM_Poynting_waves`: Maxwell stress, wave, and Poynting-balance residual | baseline: Maxwell vacuum/material energy-flux balance | status `RESPONSE_CONTRACT_READY_CURRENTLY_BLOCKED`
- `Newton_limit`: local acceleration and Poisson-potential residual | baseline: Newtonian mechanics recovered from the local weak-field branch | status `RESPONSE_CONTRACT_READY_CURRENTLY_BLOCKED`

## Runner Rows
- `R10_short_range` `BLOCKED_MISSING_XILOC_OR_ARENA_INPUTS` missing=`Xi_loc;sigma_A;beta_A;ell_A;epsilon_A;bound_A` predicted=``
- `PPN_solar_system` `BLOCKED_MISSING_XILOC_OR_ARENA_INPUTS` missing=`Xi_loc;sigma_A;beta_A;ell_A;epsilon_A;bound_A` predicted=``
- `clock_redshift` `BLOCKED_MISSING_XILOC_OR_ARENA_INPUTS` missing=`Xi_loc;sigma_A;beta_A;ell_A;epsilon_A;bound_A` predicted=``
- `orbital_dynamics` `BLOCKED_MISSING_XILOC_OR_ARENA_INPUTS` missing=`Xi_loc;sigma_A;beta_A;ell_A;epsilon_A;bound_A` predicted=``
- `EM_Poynting_waves` `BLOCKED_MISSING_XILOC_OR_ARENA_INPUTS` missing=`Xi_loc;sigma_A;beta_A;ell_A;epsilon_A;bound_A` predicted=``
- `Newton_limit` `BLOCKED_MISSING_XILOC_OR_ARENA_INPUTS` missing=`Xi_loc;sigma_A;beta_A;ell_A;epsilon_A;bound_A` predicted=``

## Theorem Rows
- `THM3729_0_coercive_response_bound` `DERIVED_CONTRACT`: If <h,Lh> >= Xi_loc||h||^2 and ||N_A(h)|| <= ell_A||h|| with ell_A < Xi_loc, then ||h_A|| <= sigma_A/(Xi_loc-ell_A). | Local coercivity converts source/coupling residual into a bounded local perturbation.
- `THM3729_1_observable_pushforward` `DERIVED_CONTRACT`: If ||B_A|| <= beta_A, then residual_bound_A=beta_A*sigma_A/(Xi_loc-ell_A)+epsilon_A. | Each empirical arena needs its own response norm and residual floor.
- `THM3729_2_no_claim_from_Xi_alone` `ANTI_OVERCLAIM`: Xi_loc>0 is not an arena pass without sigma_A, beta_A, ell_A, epsilon_A, and bound_A. | Stops a positive local gap from being smuggled into R10/PPN/clock/orbit/EM/Newton claims.
- `THM3729_3_EM_Poynting_is_an_arena` `ROUTE_OPEN_BLOCKED`: The Poynting/wave route enters as EM_Poynting_waves with the same response inequality, not as an assumed Maxwell recovery. | Keeps the user's background-field/Poynting idea alive but gateable.
- `THM3729_4_GR_Newton_bridge_is_residual_based` `DISCIPLINE_GATE`: Derived local GR/Newton recovery means bounded PPN/orbital/Newton residuals, not a declaration that the branch is GR. | Turns the GR reduction target into measurable residual inequalities.

## Decisions
- `DEC3729_0_response_map_ready` `RESPONSE_MAP_CONTRACT_READY` | A future positive Xi_loc now has a concrete path into R10, PPN, clocks, orbits, EM/Poynting, and Newton residual bounds.
- `DEC3729_1_current_blocked` `CURRENT_ARENAS_BLOCKED_BY_MISSING_XILOC_AND_COUPLINGS` | The runner refuses every arena because Xi_loc and arena coupling/source response rows are not numeric/source-owned.
- `DEC3729_2_next` `NEXT_ATTACK_COUPLING_SOURCE_NORMS` | The highest-leverage derivation is sigma_A and beta_A from matter coupling/descent, because those feed every local arena.

## Refusals
- Every arena is blocked until `Xi_loc`, `sigma_A`, `beta_A`, `ell_A`, `epsilon_A`, and `bound_A` are numeric/source-owned.
- The EM/Poynting route is retained as a proper response arena rather than being discarded or assumed.

## Next Target
- `3730-Y5-R2FR-coupling-source-norm-derivation-hunt.md`
- Objective: derive or source `sigma_A` and `beta_A` from matter coupling/descent, because that is the common bottleneck for R10/PPN/clocks/orbits/EM/Newton.
