# 3732 - First Arena Response Specialization: Newton/PPN and EM

## Status
- `FIRST_ARENA_SPECIALIZATION_READY_VALUES_MISSING`
- `Newton_PPN_bridge` tests local GR/Newton through acceleration, Poisson, PPN gamma/beta, and preferred-frame residuals.
- `EM_Poynting_bridge` tests Maxwell/EM stress through Poynting, stress, wave, polarization, and charge-continuity residuals.
- Current specialization is claim-blocked until `H^X`, `partial_X chi`, source tails, and response entries are theorem-zero or numeric/source-owned.

## Basis Rows
- `Newton_PPN_bridge` `domain` `h_phi`: Poisson potential perturbation delta Phi
- `Newton_PPN_bridge` `domain` `h_psi`: space-curvature potential perturbation delta Psi
- `Newton_PPN_bridge` `domain` `h_GM`: measured-GM/source-normalization perturbation
- `Newton_PPN_bridge` `domain` `h_pref`: preferred-frame/disformal perturbation coordinate
- `Newton_PPN_bridge` `domain` `h_bdy`: boundary/support/local-domain residual coordinate
- `Newton_PPN_bridge` `observable` `y_accel`: local acceleration residual delta a + grad delta Phi
- `Newton_PPN_bridge` `observable` `y_poisson`: Poisson residual nabla^2 Phi - 4 pi G rho_eff
- `Newton_PPN_bridge` `observable` `y_gamma`: PPN gamma minus one
- `Newton_PPN_bridge` `observable` `y_beta`: PPN beta minus one
- `Newton_PPN_bridge` `observable` `y_pref`: preferred-frame residual vector
- `EM_Poynting_bridge` `domain` `h_chi`: Hodge/constitutive perturbation delta chi
- `EM_Poynting_bridge` `domain` `h_frame`: metric/frame perturbation H^X entering EM stress
- `EM_Poynting_bridge` `domain` `h_Jem`: electric source-current/readout perturbation
- `EM_Poynting_bridge` `domain` `h_alpha`: charge/fine-structure/material marker perturbation
- `EM_Poynting_bridge` `domain` `h_EM_tail`: boundary/non-Hilbert/material tail residual
- `EM_Poynting_bridge` `observable` `y_poynting`: Poynting theorem residual partial_t u + div S + J dot E
- `EM_Poynting_bridge` `observable` `y_stress`: Maxwell stress-divergence/momentum-balance residual
- `EM_Poynting_bridge` `observable` `y_wave`: wave-speed/dispersion residual
- `EM_Poynting_bridge` `observable` `y_pol`: polarization/birefringence residual
- `EM_Poynting_bridge` `observable` `y_charge`: charge/current continuity residual

## Response Entries
- `B3732_NP_accel_phi` `y_accel` <- `h_phi` via `grad_operator_norm_C_grad` | maps potential perturbation to acceleration residual
- `B3732_NP_poisson_phi` `y_poisson` <- `h_phi` via `laplacian_operator_norm_C_lap` | maps potential perturbation to Poisson residual
- `B3732_NP_poisson_gm` `y_poisson` <- `h_GM` via `4pi_rho_norm_C_GM` | maps measured-G/source normalization into Poisson residual
- `B3732_NP_gamma_phipsi` `y_gamma` <- `h_phi;h_psi` via `C_gamma_metric_ratio` | maps two-potential relation to gamma-1
- `B3732_NP_beta_phi` `y_beta` <- `h_phi` via `C_beta_second_order` | maps second-order potential response to beta-1
- `B3732_NP_pref_pref` `y_pref` <- `h_pref` via `C_preferred_frame` | maps disformal/preferred-frame branch to PPN preferred-frame residual
- `B3732_NP_boundary` `y_accel;y_poisson` <- `h_bdy` via `C_boundary_projection` | maps boundary/support tail into Newton/PPN residuals
- `B3732_EM_poynting_chi` `y_poynting` <- `h_chi` via `C_poynting_chi_derivative` | maps constitutive/Hodge perturbation to Poynting theorem residual
- `B3732_EM_poynting_current` `y_poynting` <- `h_Jem` via `C_JdotE` | maps source-current perturbation to J dot E residual
- `B3732_EM_stress_frame` `y_stress` <- `h_frame` via `C_TEM_frame` | maps frame perturbation into Maxwell stress residual
- `B3732_EM_wave_chi` `y_wave` <- `h_chi` via `C_wave_constitutive` | maps constitutive perturbation into wave speed/dispersion residual
- `B3732_EM_pol_chi` `y_pol` <- `h_chi` via `C_birefringence` | maps anisotropic constitutive perturbation into polarization residual
- `B3732_EM_charge_marker` `y_charge` <- `h_alpha` via `C_charge_marker` | maps charge/fine-structure marker perturbation into continuity/readout residual
- `B3732_EM_tail` `y_poynting;y_stress;y_wave;y_pol;y_charge` <- `h_EM_tail` via `C_EM_tail_projection` | maps retained EM tail into all EM observables

## Sigma Specializations
- `SIG3732_NP`: sigma_NP <= C_trace|c_g| ||T|| + C_dis|b_dis| ||T_UU|| + |Delta_GM| + |boundary_NP| + |tail_NP| | missing: c_g,b_dis,T,T_UU,Delta_GM,boundary_NP,tail_NP
- `SIG3732_EM`: sigma_EM <= C_chi||partial_X chi|| ||F^2|| + C_frame||H^X:T_EM|| + C_J||delta_X J_EM|| + |b_alpha C_alpha| + |tail_EM| | missing: partial_X_chi,H^X,T_EM,delta_X_J_EM,b_alpha,tail_EM

## Theorem Rows
- `THM3732_0_Newton_PPN_basis` `DERIVED_BASIS_CONTRACT`: Newton/PPN recovery can be tested by y_NP=(acceleration residual, Poisson residual, gamma-1, beta-1, preferred-frame residual). | This converts local GR/Newton reduction into observable residual basis rows rather than a verbal target.
- `THM3732_1_Newton_PPN_matrix` `DERIVED_RESPONSE_CONTRACT`: beta_NP^2=lambda_max(G_NP^{-1/2} B_NP^T W_NP B_NP G_NP^{-1/2}). | A PPN/Newton pass needs B_NP/W_NP/G_NP entries, not just a positive Xi_loc.
- `THM3732_2_EM_Poynting_basis` `DERIVED_BASIS_CONTRACT`: EM recovery can be tested by y_EM=(Poynting residual, Maxwell-stress residual, wave residual, polarization residual, charge-continuity residual). | This turns Maxwell/EM stress into a gateable arena parallel to Newton/PPN.
- `THM3732_3_EM_Poynting_matrix` `DERIVED_RESPONSE_CONTRACT`: beta_EM^2=lambda_max(G_EM^{-1/2} B_EM^T W_EM B_EM G_EM^{-1/2}). | Poynting intuition becomes a matrix norm plus source-current bound, not an assumed background field success.
- `THM3732_4_zero_conditions` `ANTI_OVERCLAIM`: Newton/PPN and EM residuals vanish only if the corresponding sigma bridge is theorem-zero and beta is finite, or if the 3729 residual bound beats a sourced bound_A. | This is the no-smuggling rule for GR/Newton/Maxwell recovery.

## Decisions
- `DEC3732_0_Newton_PPN_bridge` Newton/PPN is now the primary local-GR reduction bridge. | It directly tests acceleration, Poisson, gamma, beta, and preferred-frame residuals.
- `DEC3732_1_EM_bridge` EM/Poynting is retained as the Maxwell-stress bridge. | It tests Poynting balance, Maxwell stress, waves, polarization, and charge continuity.
- `DEC3732_2_next` Next derive zero-or-bound clauses for H^X and partial_X chi. | Those two quantities are common bottlenecks: H^X feeds matter/PPN/Newton/EM stress, while partial_X chi controls the Maxwell/Hodge route.

## Next Target
- `3733-Y5-R2FR-HX-and-Hodge-variation-zero-or-bound.md`
- Objective: derive or bound `H^X=partial_X g_matter` and `partial_X chi`, because those are the common coefficients behind Newton/PPN and EM/Poynting recovery.
