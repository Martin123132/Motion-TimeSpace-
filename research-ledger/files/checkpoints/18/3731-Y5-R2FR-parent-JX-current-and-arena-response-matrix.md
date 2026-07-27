# 3731 - Parent J_X Current and Arena Response Matrix

## Status
- `JX_AND_RESPONSE_MATRIX_CONTRACT_READY_VALUES_MISSING`
- Parent source current: `delta_X S_parent = int sqrt(|g_obs|) J_X delta X + int_boundary Theta_X`.
- Arena response norm: `beta_A^2=lambda_max(G_H^{-1/2} B_A^T W_A B_A G_H^{-1/2})`.
- These formulas feed `sigma_A` and `beta_A` into the 3729 response inequality, but no local-GR/Newton/Maxwell claim is allowed yet.

## Parent Current Components
- `JXC3731_0_variational_definition` `total_parent_current`: delta_X S_parent = int_M sqrt(|g_obs|) J_X delta X + int_boundary Theta_X | missing: MISSING_PARENT_ACTION_DENSITY_AND_X_DIRECTION
- `JXC3731_1_visible_geometry` `J_geom`: J_geom = 1/2 T_matter^{mu nu} H^X_{mu nu}; H^X_{mu nu}:=partial_X g^matter_{mu nu}|branch | missing: MISSING_HX_OR_NO_SHADOW_FRAME_THEOREM
- `JXC3731_2_disformal_frame` `J_dis`: J_dis = 1/2 T^{mu nu} D^X_{mu nu}, with D^X_{mu nu}=partial_X(B_g U_mu U_nu + extra frame slots) | missing: MISSING_DISFORMAL_ABSENCE_OR_BOUND
- `JXC3731_3_marker_constants` `J_marker`: J_marker = sum_I (partial_X theta_I) partial L_matter/partial theta_I | missing: MISSING_NO_MARKER_THEOREM_OR_BOUNDS
- `JXC3731_4_connection_nonHilbert` `J_connection_nonH`: J_connection_nonH = delta_X S_nonHilbert + delta_X S_connection + source-support/domain terms | missing: MISSING_SOURCE_ACTION_AND_DOMAIN_BOUND
- `JXC3731_5_boundary` `J_boundary`: J_boundary = div Theta_X plus corner/support flux projected into arena A | missing: MISSING_BOUNDARY_FLUX_ZERO_OR_BOUND
- `JXC3731_6_EM_Hodge_Poynting` `J_EM`: J_EM = 1/4 (partial_X chi^{mu nu rho sigma}) F_{mu nu}F_{rho sigma} + 1/2 T_EM^{mu nu} H^X_{mu nu} + tail_EM | missing: MISSING_PARENT_HODGE_CONSTITUTIVE_RULE

## Sigma Projection Rows
- `R10_short_range`: sigma_R10 <= |K_X^R10 beta_source beta_test| + |tail_R10| | missing: K_X^R10,beta_source,beta_test,profile,tail
- `PPN_solar_system`: sigma_PPN <= |c_g C_geom| + |b_dis C_dis| + |tail_PPN| | missing: c_g,b_dis,weak-field profile,gauge,tail
- `clock_redshift`: sigma_clock <= sum_I |b_I C_clock,I| + |c_g C_geom_clock| + |tail_clock| | missing: marker constants, clock material sensitivities, frame coupling, tail
- `orbital_dynamics`: sigma_orbit <= |Delta_GM| + |source_support| + |boundary| + |tail_orbit| | missing: measured-GM calibration, support, boundary, source-normalization
- `EM_Poynting_waves`: sigma_EM <= |delta_X chi| ||F^2|| + |H^X:T_EM|/2 + |tail_EM| | missing: Hodge/constitutive variation, EM stress projection, tail
- `Newton_limit`: sigma_Newton <= |Delta_rho_Poisson| + |Delta_G| + |boundary_Newton| | missing: Poisson source, G calibration, boundary and left-hand Newton limit

## Response Matrix Rows
- `R10_short_range`: domain `h_X radial/profile coefficients` -> observable `alpha(lambda) or torque harmonic residuals` with `beta_A^2=lambda_max(G_H^{-1/2} B_A^T W_A B_A G_H^{-1/2})`
- `PPN_solar_system`: domain `weak-field metric/source perturbation coefficients` -> observable `gamma-1,beta-1,preferred-frame residual vector` with `beta_A^2=lambda_max(G_H^{-1/2} B_A^T W_A B_A G_H^{-1/2})`
- `clock_redshift`: domain `local frame/time/material marker perturbation coefficients` -> observable `fractional frequency/redshift residuals` with `beta_A^2=lambda_max(G_H^{-1/2} B_A^T W_A B_A G_H^{-1/2})`
- `orbital_dynamics`: domain `potential/acceleration/source-normalization perturbation coefficients` -> observable `range,timing,perihelion,acceleration residual vector` with `beta_A^2=lambda_max(G_H^{-1/2} B_A^T W_A B_A G_H^{-1/2})`
- `EM_Poynting_waves`: domain `Hodge/constitutive/stress perturbation coefficients` -> observable `Poynting theorem, Maxwell stress, wave-speed/polarization residuals` with `beta_A^2=lambda_max(G_H^{-1/2} B_A^T W_A B_A G_H^{-1/2})`
- `Newton_limit`: domain `Poisson potential/source perturbation coefficients` -> observable `acceleration and potential residuals` with `beta_A^2=lambda_max(G_H^{-1/2} B_A^T W_A B_A G_H^{-1/2})`

## Theorem Rows
- `THM3731_0_JX_variational_identity` `DERIVED_IDENTITY`: For any local branch coordinate X, delta_X S_parent = int sqrt(|g|) J_X delta X + boundary terms. | This is the parent-owned definition of the coupling source; it replaces fitted coupling talk with a variational object.
- `THM3731_1_matter_frame_current` `DERIVED_CONDITIONAL`: If matter sees g_m(X), then J_geom = 1/2 T^{mu nu} partial_X g^m_{mu nu}; quotient descent sets this to zero only if partial_X g_m=0 by parent theorem. | This is the exact fork between closure-zero and finite common coupling.
- `THM3731_2_response_matrix_norm` `DERIVED_OPERATOR_NORM`: With domain Gram G_H and observable weight W_A, beta_A^2=lambda_max(G_H^{-1/2} B_A^T W_A B_A G_H^{-1/2}). | This makes beta_A computable once the arena readout map is written.
- `THM3731_3_EM_constitutive_current` `ROUTE_OPEN_CONTRACT`: EM/Poynting residuals require delta_X chi, H^X:T_EM, and tail_EM; ordinary Poynting balance is recovered only if those terms vanish or are bounded. | This keeps Maxwell/EM stress derivable rather than assumed.
- `THM3731_4_no_claim_gate` `ANTI_OVERCLAIM`: A symbolic J_X and symbolic beta_A cannot pass 3729; both need numeric/source-owned rows or theorem-zero certificates. | Prevents smuggling closure assumptions into local-GR/Newton/Maxwell claims.

## Decisions
- `DEC3731_0_contract_closed` `JX_AND_BETA_CONTRACT_READY` | The parent-current and arena-response sides now have exact formulas feeding 3729.
- `DEC3731_1_no_numeric_claim` `NO_ARENA_SCORE_YET` | Current rows lack parent-owned H^X, chi_X, marker derivatives, B_A, W_A, and G_H matrices.
- `DEC3731_2_best_next` `SPECIALIZE_ONE_ARENA_NEXT` | The next leap is to pick the least slippery arena and write its B_A/W_A plus source-current specialization; Newton/PPN is the cleanest GR bridge, EM/Poynting is the parallel Maxwell bridge.

## Claim Gates
- `CG3731_0_sources` `PASS_NONCLAIM` | source trail exists
- `CG3731_1_JX_identity` `PASS_NONCLAIM` | variational J_X identity written
- `CG3731_2_HX` `BLOCKED` | H^X or quotient-zero/no-shadow theorem missing
- `CG3731_3_EM_chi` `BLOCKED` | delta_X chi/Hodge/constitutive rule missing
- `CG3731_4_markers` `BLOCKED` | marker constants theorem-zero or bounds missing
- `CG3731_5_Bmatrix` `BLOCKED` | B_A/W_A/G_H response matrices missing
- `CG3731_6_3729_feed` `BLOCKED` | no numeric sigma_A or beta_A can feed 3729 yet
- `CG3731_7_claim` `BLOCKED` | no local-GR/Newton/Maxwell/PPN/R10 claim allowed

## Next Target
- `3732-Y5-R2FR-first-arena-response-specialization-Newton-PPN-and-EM.md`
- Objective: specialize the `J_X/B_A/W_A` contract into Newton/PPN and EM/Poynting first-arena response matrices.
