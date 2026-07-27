# 3734 - H^X/chi Bound Interface to Newton/PPN and EM

## Status
- `HX_CHI_BOUND_INTERFACE_READY_CURRENTLY_BLOCKED`
- `Hbar_X` now feeds a fillable `sigma_NP` row for the Newton/PPN bridge.
- `Chibar_total` and `Hbar_X` now feed a fillable `sigma_EM` row for the EM/Poynting bridge.
- The interface is still blocked because all values and response matrices are placeholders.

## Sigma Formulas
- `FORM3734_NP_sigma` `Newton_PPN_bridge`: sigma_NP = C_NP_H*Hbar_X*T_norm_NP + Delta_GM + boundary_NP + tail_NP
- `FORM3734_EM_sigma` `EM_Poynting_bridge`: sigma_EM = C_EM_chi*Chibar_total*F2_norm + C_EM_frame*Hbar_X*T_EM_norm + C_EM_J*delta_J_EM + b_alpha_C_alpha + tail_EM

## Sigma Inputs
- `Newton_PPN_bridge` `Hbar_X` = `MISSING_HBAR_X` | frame/metric variation envelope from 3733
- `Newton_PPN_bridge` `T_norm_NP` = `MISSING_T_NORM_NP` | ordinary/source stress norm in local Newton/PPN arena
- `Newton_PPN_bridge` `C_NP_H` = `MISSING_C_NP_H` | projection coefficient from Hbar_X*T_norm into Newton/PPN source residual
- `Newton_PPN_bridge` `Delta_GM` = `MISSING_DELTA_GM` | measured-GM/source-normalization residual
- `Newton_PPN_bridge` `boundary_NP` = `MISSING_BOUNDARY_NP` | Newton/PPN boundary/support residual
- `Newton_PPN_bridge` `tail_NP` = `MISSING_TAIL_NP` | other retained Newton/PPN source tails
- `EM_Poynting_bridge` `Chibar_total` = `MISSING_CHIBAR_TOTAL` | total Hodge/constitutive variation envelope from 3733
- `EM_Poynting_bridge` `F2_norm` = `MISSING_F2_NORM` | local EM field-strength squared norm
- `EM_Poynting_bridge` `C_EM_chi` = `MISSING_C_EM_CHI` | projection from Chibar_total*F2_norm into EM residual
- `EM_Poynting_bridge` `Hbar_X` = `MISSING_HBAR_X` | frame/metric variation entering EM stress
- `EM_Poynting_bridge` `T_EM_norm` = `MISSING_T_EM_NORM` | Maxwell stress norm
- `EM_Poynting_bridge` `C_EM_frame` = `MISSING_C_EM_FRAME` | projection from Hbar_X*T_EM into EM stress residual
- `EM_Poynting_bridge` `delta_J_EM` = `MISSING_DELTA_J_EM` | electric source-current/readout perturbation
- `EM_Poynting_bridge` `C_EM_J` = `MISSING_C_EM_J` | projection from current perturbation to Poynting residual
- `EM_Poynting_bridge` `b_alpha_C_alpha` = `MISSING_B_ALPHA_C_ALPHA` | charge/fine-structure marker contribution
- `EM_Poynting_bridge` `tail_EM` = `MISSING_TAIL_EM` | other retained EM tails

## Beta Links
- `BETA3734_NP`: beta_NP^2=lambda_max(G_NP^{-1/2} B_NP^T W_NP B_NP G_NP^{-1/2}) | status: MISSING_B_NP_W_NP_G_NP_NUMERIC_OR_THEOREM
- `BETA3734_EM`: beta_EM^2=lambda_max(G_EM^{-1/2} B_EM^T W_EM B_EM G_EM^{-1/2}) | status: MISSING_B_EM_W_EM_G_EM_NUMERIC_OR_THEOREM

## 3729 Fill Contracts
- `FILL3734_NP` `Newton_PPN_bridge`: sigma_A=sigma_NP from RUN3734_Newton_PPN_bridge; beta_A=beta_NP from BETA3734_NP; ell_A, epsilon_A, bound_A still required by 3729
- `FILL3734_EM` `EM_Poynting_bridge`: sigma_A=sigma_EM from RUN3734_EM_Poynting_bridge; beta_A=beta_EM from BETA3734_EM; ell_A, epsilon_A, bound_A still required by 3729

## Theorem Rows
- `THM3734_0_NP_sigma_interface` `DERIVED_INTERFACE`: Hbar_X plus source stress/G calibration/boundary tails determine a compressed sigma_NP input row. | Turns the H^X bound into a Newton/PPN source residual interface.
- `THM3734_1_EM_sigma_interface` `DERIVED_INTERFACE`: Chibar_total and Hbar_X plus EM field/current/marker/tail norms determine a compressed sigma_EM input row. | Turns the Hodge/H^X bound into a Maxwell/Poynting source residual interface.
- `THM3734_2_beta_separation` `ANTI_SMUGGLING`: sigma_A source bounds and beta_A response norms remain separate until 3729 combines them. | Prevents hiding source uncertainty inside response coefficients.
- `THM3734_3_nonclaim` `ANTI_OVERCLAIM`: All interface rows stay nonclaim until every input is numeric/source-owned or theorem-zero. | The interface is a socket for future derivations, not a pass.

## Decisions
- `DEC3734_0_interface_ready` `HX_CHI_TO_SIGMA_INTERFACE_READY` | Hbar_X and Chibar_total now have fillable paths into Newton/PPN and EM/Poynting sigma rows.
- `DEC3734_1_still_blocked` `VALUES_AND_RESPONSE_MATRICES_MISSING` | The interface is structurally ready but cannot score until source-owned input values and beta matrices exist.
- `DEC3734_2_next` `NEXT_ATTACK_RESPONSE_MATRICES_OR_PARENT_ZERO` | Best next move is either derive Hbar_X/Chibar_total theorem-zero, or build B_NP/B_EM numeric/theorem response matrices.

## Next Target
- `3735-Y5-R2FR-response-matrix-first-pass-Newton-PPN-EM.md`
- Objective: build the first `B_NP/W_NP/G_NP` and `B_EM/W_EM/G_EM` response-matrix contracts so `beta_NP` and `beta_EM` can become computable.
