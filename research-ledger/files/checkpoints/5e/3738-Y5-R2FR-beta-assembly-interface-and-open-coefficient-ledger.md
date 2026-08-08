# 3738 - Beta Assembly Interface and Open Coefficient Ledger

## Status
- `BETA_ASSEMBLY_INTERFACE_DERIVED_VALUES_MISSING`
- `beta_NP` and `beta_EM` now have both exact matrix contracts and conservative diagonal bound formulas.
- This is a forward step: the response machinery is assembled into a plug-in scoring interface, but numeric claims remain blocked.

## Exact Matrix Contracts
- `FORM3738_0_exact_NP` `beta_NP`: beta_NP^2=lambda_max(G_NP^{-1/2} B_NP^T W_NP B_NP G_NP^{-1/2}) | requirements: finite B_NP, positive-definite G_NP, positive-semidefinite W_NP
- `FORM3738_2_exact_EM` `beta_EM`: beta_EM^2=lambda_max(G_EM^{-1/2} B_EM^T W_EM B_EM G_EM^{-1/2}) | requirements: finite B_EM, positive-definite G_EM, positive-semidefinite W_EM

## Conservative Diagonal Bounds
- `FORM3738_1_diag_bound_NP` `beta_NP`: beta_NP_diag^2 <= w_y_accel*(C_grad^2/g_h_phi + C_boundary_projection^2/g_h_bdy) + w_y_poisson*(C_lap^2/g_h_phi + (4*pi*rho_eff_norm)^2/g_h_GM + C_boundary_projection^2/g_h_bdy) + w_y_gamma*Phi0_inv^2*(1/g_h_phi + 1/g_h_psi) + w_y_beta*C_beta_2PN^2/g_h_phi + w_y_pref*C_preferred_frame^2/g_h_pref
- `FORM3738_3_diag_bound_EM` `beta_EM`: beta_EM_diag^2 <= w_y_poynting*(C_poynting_chi^2/g_h_chi + C_JdotE^2/g_h_Jem + C_EM_tail_projection^2/g_h_EM_tail) + w_y_stress*(C_TEM_frame^2/g_h_frame + C_EM_tail_projection^2/g_h_EM_tail) + w_y_wave*(C_wave_chi^2/g_h_chi + C_EM_tail_projection^2/g_h_EM_tail) + w_y_pol*(C_birefringence^2/g_h_chi + C_EM_tail_projection^2/g_h_EM_tail) + w_y_charge*(C_charge_marker^2/g_h_alpha + C_EM_tail_projection^2/g_h_EM_tail)

## Atomic Bound Terms
- `NP001` `beta_NP` `y_accel` <- `h_phi` via `C_grad`: `w_y_accel*C_grad^2/g_h_phi`
- `NP002` `beta_NP` `y_accel` <- `h_bdy` via `C_boundary_projection`: `w_y_accel*C_boundary_projection^2/g_h_bdy`
- `NP003` `beta_NP` `y_poisson` <- `h_phi` via `C_lap`: `w_y_poisson*C_lap^2/g_h_phi`
- `NP004` `beta_NP` `y_poisson` <- `h_GM` via `4*pi*rho_eff_norm`: `w_y_poisson*(4*pi*rho_eff_norm)^2/g_h_GM`
- `NP005` `beta_NP` `y_poisson` <- `h_bdy` via `C_boundary_projection`: `w_y_poisson*C_boundary_projection^2/g_h_bdy`
- `NP006` `beta_NP` `y_gamma` <- `h_phi` via `Phi0_inv`: `w_y_gamma*Phi0_inv^2/g_h_phi`
- `NP007` `beta_NP` `y_gamma` <- `h_psi` via `Phi0_inv`: `w_y_gamma*Phi0_inv^2/g_h_psi`
- `NP008` `beta_NP` `y_beta` <- `h_phi` via `C_beta_2PN`: `w_y_beta*C_beta_2PN^2/g_h_phi`
- `NP009` `beta_NP` `y_pref` <- `h_pref` via `C_preferred_frame`: `w_y_pref*C_preferred_frame^2/g_h_pref`
- `EM001` `beta_EM` `y_poynting` <- `h_chi` via `C_poynting_chi`: `w_y_poynting*C_poynting_chi^2/g_h_chi`
- `EM002` `beta_EM` `y_poynting` <- `h_Jem` via `C_JdotE`: `w_y_poynting*C_JdotE^2/g_h_Jem`
- `EM003` `beta_EM` `y_poynting` <- `h_EM_tail` via `C_EM_tail_projection`: `w_y_poynting*C_EM_tail_projection^2/g_h_EM_tail`
- `EM004` `beta_EM` `y_stress` <- `h_frame` via `C_TEM_frame`: `w_y_stress*C_TEM_frame^2/g_h_frame`
- `EM005` `beta_EM` `y_stress` <- `h_EM_tail` via `C_EM_tail_projection`: `w_y_stress*C_EM_tail_projection^2/g_h_EM_tail`
- `EM006` `beta_EM` `y_wave` <- `h_chi` via `C_wave_chi`: `w_y_wave*C_wave_chi^2/g_h_chi`
- `EM007` `beta_EM` `y_wave` <- `h_EM_tail` via `C_EM_tail_projection`: `w_y_wave*C_EM_tail_projection^2/g_h_EM_tail`
- `EM008` `beta_EM` `y_pol` <- `h_chi` via `C_birefringence`: `w_y_pol*C_birefringence^2/g_h_chi`
- `EM009` `beta_EM` `y_pol` <- `h_EM_tail` via `C_EM_tail_projection`: `w_y_pol*C_EM_tail_projection^2/g_h_EM_tail`
- `EM010` `beta_EM` `y_charge` <- `h_alpha` via `C_charge_marker`: `w_y_charge*C_charge_marker^2/g_h_alpha`
- `EM011` `beta_EM` `y_charge` <- `h_EM_tail` via `C_EM_tail_projection`: `w_y_charge*C_EM_tail_projection^2/g_h_EM_tail`

## Open Input Ledger Summary
- response coefficients open: 14
- domain Gram entries open: 10
- observable weight entries open: 10
- highest-priority theoretical blockers: `C_beta_2PN`, `Phi0_inv`, `G_N`/measured-G normalization, and the local Gram/weight choices.

## Theorem Rows
- `THM3738_0_exact_operator_norm` `DERIVED_FROM_3735`: Once B, G, and W are finite and signed, beta is the spectral norm of the weighted response operator. | This is the exact bridge from local residual rows to a scalar beta score.
- `THM3738_1_diagonal_envelope` `DERIVED_CONSERVATIVE_BOUND`: For diagonal positive G/W, Cauchy gives beta^2 <= sum_y w_y sum_j C_yj^2/g_j without using cancellation. | This gives a safe smoke-run formula before full covariance structure is owned.
- `THM3738_2_NP_split` `DERIVED_ASSEMBLY`: The Newton/PPN diagonal envelope splits gamma into h_phi and h_psi and duplicates boundary response into acceleration and Poisson. | This prevents hiding the gamma denominator or boundary projection in one vague coefficient.
- `THM3738_3_EM_tail_split` `DERIVED_ASSEMBLY`: The EM diagonal envelope propagates the retained tail into Poynting, stress, wave, polarization, and charge rows. | This prevents falsely declaring Maxwell recovery while keeping hidden EM tails.
- `THM3738_4_claim_gate` `ANTI_OVERCLAIM`: No beta_NP or beta_EM number is claimable until all coefficients, Gram entries, and weights are numeric/source-owned or theorem-owned. | The checkpoint builds the machine; it does not claim a local-GR or Maxwell pass.

## Decisions
- `DEC3738_0_progress` `BETA_ASSEMBLY_INTERFACE_DERIVED` | The work now has exact and conservative formulas that turn response rows into beta_NP/beta_EM once inputs are supplied.
- `DEC3738_1_not_vibes` `MISSING_INPUTS_ARE_EXECUTION_BLOCKERS_NOT_AUDIT_VIBES` | The open ledger is tied to formula terms, so each missing item has a direct role in the future runner.
- `DEC3738_2_next` `NEXT_ATTACK_2PN_BETA_AND_GN_NORMALIZATION` | The least-circular leap toward GR/Newton reduction is deriving the parent 2PN beta map and deciding whether G_N is emergent or calibrated.

## Next Target
- `3739-Y5-R2FR-parent-2PN-beta-map-and-GN-normalization.md`
- Objective: derive or bound the parent weak-field expansion through 2PN beta and state whether Newton's constant is an emergent coupling, a calibration constant, or a blocked parent input
