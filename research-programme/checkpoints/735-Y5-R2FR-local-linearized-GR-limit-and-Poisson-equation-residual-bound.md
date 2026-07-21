# 4719 - Local Linearized GR Limit and Poisson Equation Residual Bound

Generated: `2026-07-07T21:38:04+00:00`

## Purpose

This checkpoint rebases the older 4171/4172/4278 Newton/PPN branch onto the newer 4718 coupling owner law:

`G_eff = lambda_D/(8*pi*M_EH^2)`.

The aim is to derive the weak-field bridge rather than merely assert that MTS should reduce to GR.

## Main Derivation

Start from:

`M_EH^2 G_mu_nu[g_eff] = lambda_D T_mu_nu + R_mu_nu^local`

Define:

`kappa_eff = lambda_D/M_EH^2 = 8*pi*G_eff/c^4`

and:

`E_mu_nu = R_mu_nu^local/M_EH^2`.

Then:

`G_mu_nu = kappa_eff T_mu_nu + E_mu_nu`.

In harmonic gauge with `g_eff=eta+h`, the EH block gives:

`G_mu_nu^(1) = -1/2 box bar_h_mu_nu`.

For a static slow source:

`T_00 = rho c^2`, `g_00=-(1+2 Phi_N/c^2)`, and `G_00^(1)=2 nabla^2 Phi_N/c^2`.

Therefore:

`nabla^2 Phi_N = 4*pi*G_eff*rho + (c^2/2)E_00`.

That is the clean local Newton bridge in the current MTS language.

## What This Actually Buys

This is a forward step:

- `G` is no longer an unowned mystery knob in this branch; it is the ratio `lambda_D/M_EH^2`.
- Newton's Poisson equation follows if the EH principal block and source signature are signed.
- The residual is explicit: `(c^2/2)E_00` plus source, boundary, multipole, drift, and non-EH tails.
- Poisson alone still does not prove full local GR; the PPN vector is retained separately.

## Linearized Rows

- `LFE4719_0_parent_field_equation`: G_mu_nu=kappa_eff T_mu_nu+E_mu_nu. Status: `derived_from_4718_signature`.
- `LFE4719_1_linearized_harmonic_gauge`: box bar_h_mu_nu=-2 kappa_eff T_mu_nu-2 E_mu_nu plus higher-order/non-EH terms. Status: `standard_EH_linear_identity_rebased`.
- `LFE4719_2_static_slow_source`: 2 nabla^2 Phi_N/c^2=kappa_eff rho c^2+E_00. Status: `Poisson_parent_equation`.
- `LFE4719_3_Poisson_equation_with_residual`: nabla^2 Phi_N=4*pi*G_eff*rho+(c^2/2)E_00. Status: `derived_conditionally`.
- `LFE4719_4_Gauss_orbit_readout`: a=-grad Phi_N and a_r=-G_eff M_H/r^2 plus residual force. Status: `orbital_readout_conditional`.

## Poisson Bounds

- `PB4719_0_absolute_source_residual` / `Delta_Poisson_abs`: `|Delta(nabla^2 Phi_N)| <= (c^2/2)|E_00| + 4*pi*G_eff*rho*|delta_source| + |Delta_Lambda| + |Delta_boundary|`
- `PB4719_1_fractional_density_region` / `epsilon_N_density`: `epsilon_N <= |E_00|/(kappa_eff rho c^2) + |delta_source| + |Delta_Lambda|/(4*pi*G_eff rho) + |Delta_boundary|/(4*pi*G_eff rho)`
- `PB4719_2_exterior_force_residual` / `epsilon_a_exterior`: `|Delta a_r|/|G_eff M_H/r^2| <= |int E_00 dV|/(kappa_eff M_H c^2) + |delta_M_H|/M_H + |multipoles|/(M_H r^l) + |boundary_flux|/(G_eff M_H)`
- `PB4719_3_common_G_drift` / `dotG_eff_over_G_eff`: `D_tau ln G_eff = D_tau ln lambda_D - D_tau ln M_EH^2`

## PPN Residual Vector

- `PPNV4719_0_gamma` / `gamma_minus_1`: `gamma-1 = Pi_gamma[E_ij^TF, c_D, c_R2/M_R, c_Gamma, Delta_Hodge_light, boundary_TF]`
- `PPNV4719_1_beta` / `beta_minus_1`: `beta-1 = Pi_beta[E_00^(2), nonlinear_EH_coefficient_error, delta_kappa, binding_stress_double_count]`
- `PPNV4719_2_preferred_frame` / `alpha1_alpha2_alpha3_xi`: `||alpha_xi|| <= Pi_vec[vector/torsion slots, q-frame drift, anisotropic projector, external memory gradient, boundary momentum flux]`
- `PPNV4719_3_conservation` / `zeta1_zeta2_zeta3_zeta4`: `||zeta|| <= Pi_zeta[div E_mu_nu, source_prefactor_delta_w, EM/Poynting owner defects, boundary/source exchange]`
- `PPNV4719_4_Gdot` / `Gdot_over_G`: `Gdot/G = D_tau ln(lambda_D/M_EH^2) + readout_tau_tail`

## Closure Gates

- `RCG4719_0_EH_principal_block` / `E_EH_closure`: passed=False; q-basic metric sector has EH principal block through 2PN.
- `RCG4719_1_same_source_charge` / `delta_source`: passed=False; rho is the same Hamiltonian/Hilbert source charge before orbital readout.
- `RCG4719_2_source_prefactor_zero` / `delta_w, Delta_kappa, q_A`: passed=False; 4717 parent signature is signed or finite kernels are filled.
- `RCG4719_3_boundary_projection_silence` / `boundary_flux, multipoles, local projector tails`: passed=False; compact source/no-flux collar or explicit exterior multipole bound.
- `RCG4719_4_common_G_stationarity` / `D_tau ln(lambda_D/M_EH^2)`: passed=False; common matter scale and metric kinetic scale are constants or linked by parent identity.

## Source Register

- `SRC4719_0`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4718_COMMON_G_NORMALIZATION_OWNER_ROWS.csv`; exists=True; needle_found=True; role=Current common-coupling owner law G_eff=lambda_D/(8*pi*M_EH^2).
- `SRC4719_1`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4718_COMMON_G_NORMALIZATION_OWNER_ROWS.csv`; exists=True; needle_found=True; role=4718 target that asked for a Poisson residual bound.
- `SRC4719_2`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4718_LOCAL_GR_NEWTON_RESIDUAL_ROWS.csv`; exists=True; needle_found=True; role=Residual envelope that 4719 refines into normalized Poisson/PPN rows.
- `SRC4719_3`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4171_WEAK_FIELD_READOUT.csv`; exists=True; needle_found=True; role=Older weak-field identity G_00^lin=2 nabla^2 Phi_N/c^2.
- `SRC4719_4`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4171_POISSON_GAUSS_DERIVATION.csv`; exists=True; needle_found=True; role=Older Poisson/Gauss/Newton readout to be rebased onto lambda_D/M_EH^2.
- `SRC4719_5`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4171_ORBITAL_ACCELERATION_READOUT.csv`; exists=True; needle_found=True; role=Slow-orbit Newtonian acceleration readout after the Poisson equation.
- `SRC4719_6`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4172_PPN_GAUGE_AND_ASSUMPTIONS.csv`; exists=True; needle_found=True; role=PPN metric convention for g00 and beta.
- `SRC4719_7`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4172_PPN_VECTOR_DERIVATION.csv`; exists=True; needle_found=True; role=Full private PPN residual vector including coupling drift.
- `SRC4719_8`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4278_LEFT_HAND_EH_NEWTON_DERIVATION.csv`; exists=True; needle_found=True; role=Left-hand EH/Newton gate assembling conditional Poisson readout.
- `SRC4719_9`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4278_RESIDUAL_EFT_COEFFICIENT_MAP.csv`; exists=True; needle_found=True; role=Non-EH residual coefficient map that must be bounded if not zero.
- `SRC4719_10`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\MTS_local_residual_predictions_TEMPLATE.csv`; exists=True; needle_found=True; role=Local residual prediction template warning that Poisson alone does not prove gamma.
- `SRC4719_11`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4717_DELTAW_KERNEL_FIRST_ROWS.csv`; exists=True; needle_found=True; role=Source-prefactor contribution to the PPN residual vector.

## Decision

`LINEARIZED_GR_POISSON_BRIDGE_DERIVED_CONDITIONALLY_RESIDUAL_VECTOR_EXPLICIT_NONCLAIM`

## Next Target

`4720-Y5-R2FR-EH-reduction-parent-signature-or-nonEH-operator-coefficient-matrix.md`
