# 3736 - Newton/PPN Response Coefficients from Weak-Field Limit

## Status
- `B_NP_SHAPES_SHARPENED_NUMERIC_VALUES_MISSING`
- Newton/PPN `B_NP` entries now have weak-field coefficient formulas.
- `beta_NP` remains blocked because operator norms, gauge normalization, and the 2PN beta map are not source-owned.

## Coefficient Rows
- `BNP3736_0_accel_phi` `BME3735_B3732_NP_accel_phi`: delta a = -grad(delta Phi), so ||y_accel|| <= C_grad ||h_phi|| -> `C_grad` | status `DERIVED_SHAPE_COEFFICIENT_MISSING_NORM`
- `BNP3736_1_poisson_phi` `BME3735_B3732_NP_poisson_phi`: delta R_Poisson = nabla^2(delta Phi), so ||y_poisson|| <= C_lap ||h_phi|| -> `C_lap` | status `DERIVED_SHAPE_COEFFICIENT_MISSING_NORM`
- `BNP3736_2_poisson_gm` `BME3735_B3732_NP_poisson_gm`: measured-GM/source normalization contributes |4*pi*rho_eff| |h_GM| to the Poisson residual -> `4*pi*rho_eff_norm` | status `DERIVED_SHAPE_COEFFICIENT_MISSING_SOURCE_NORM`
- `BNP3736_3_gamma_phipsi` `BME3735_B3732_NP_gamma_phipsi`: for weak fields gamma≈Psi/Phi, delta(gamma-1)≈(h_psi-h_phi)/Phi0 after gauge/background normalization -> `Phi0_inv acting on h_psi-h_phi` | status `CONDITIONAL_WEAK_FIELD_FORMULA`
- `BNP3736_4_beta_phi` `BME3735_B3732_NP_beta_phi`: beta-1 is second-order weak-field response; coefficient needs the parent 2PN metric-potential map -> `C_beta_2PN` | status `FORMULA_TARGET_SECOND_ORDER_NOT_DERIVED`
- `BNP3736_5_pref_pref` `BME3735_B3732_NP_pref_pref`: preferred-frame residual is linear in the retained disformal/preferred-frame coordinate -> `C_preferred_frame` | status `CONDITIONAL_LINEAR_RESPONSE`
- `BNP3736_6_boundary` `BME3735_B3732_NP_boundary`: boundary/support perturbations project into acceleration and Poisson residuals through C_boundary_projection -> `C_boundary_projection` | status `BOUND_SCHEMA_READY_VALUES_MISSING`

## Required Inputs
- `C_grad` = `MISSING_GRAD_OPERATOR_NORM` | gradient norm from potential basis to acceleration residual
- `C_lap` = `MISSING_LAPLACIAN_OPERATOR_NORM` | Laplacian norm from potential basis to Poisson residual
- `rho_eff_norm` = `MISSING_RHO_EFF_NORM` | effective source density norm for measured-GM calibration
- `Phi0_inv` = `MISSING_PHI0_INVERSE_OR_SAFE_NORMALIZATION` | safe weak-field normalization for gamma response
- `C_beta_2PN` = `MISSING_2PN_BETA_COEFFICIENT` | second-order beta response coefficient
- `C_preferred_frame` = `MISSING_PREFERRED_FRAME_COEFFICIENT` | preferred-frame response coefficient
- `C_boundary_projection` = `MISSING_BOUNDARY_PROJECTION_NORM` | boundary/support projection norm

## Theorem Rows
- `THM3736_0_Newton_accel` `DERIVED_WEAK_FIELD_SHAPE`: Newtonian local acceleration residual is the gradient response of the potential perturbation: delta a=-grad delta Phi. | This derives the y_accel<-h_phi B_NP entry shape.
- `THM3736_1_Poisson` `DERIVED_WEAK_FIELD_SHAPE`: Poisson residual is nabla^2 delta Phi minus measured-source normalization terms. | This derives y_poisson<-h_phi and y_poisson<-h_GM entry shapes.
- `THM3736_2_gamma` `CONDITIONAL_WEAK_FIELD_SHAPE`: In a fixed weak-field gauge with nonzero background potential scale, gamma response is controlled by h_psi-h_phi. | This derives the gamma row conditionally and exposes the gauge/Phi0 dependency.
- `THM3736_3_beta` `ANTI_OVERCLAIM`: PPN beta is 2PN/second-order and cannot be derived from the first-order Newtonian potential row alone. | This prevents falsely promoting beta from a 1PN scaffold.
- `THM3736_4_claim_gate` `ANTI_SMUGGLING`: B_NP shapes are sharper but not numeric/source-owned; beta_NP remains blocked in 3735. | Shape derivation is progress, not an empirical or local-GR pass.

## Decisions
- `DEC3736_0_progress` `B_NP_WEAK_FIELD_SHAPES_SHARPENED` | The Newton/PPN response matrix is no longer anonymous: acceleration, Poisson, gamma, preferred-frame, and boundary rows have weak-field formulas.
- `DEC3736_1_beta_block` `BETA_REQUIRES_2PN_PARENT_MAP` | PPN beta is explicitly held back until the second-order parent weak-field expansion is derived.
- `DEC3736_2_next` `NEXT_DO_EM_MATRIX_OR_2PN_BETA` | The best continuation is either EM/Poynting B_EM coefficient derivation, or a focused 2PN beta parent expansion.

## Next Target
- `3737-Y5-R2FR-EM-Poynting-response-coefficients-from-Hodge-Maxwell.md`
- Objective: derive the EM/Poynting `B_EM` response entries from Hodge/constitutive Maxwell identities.
