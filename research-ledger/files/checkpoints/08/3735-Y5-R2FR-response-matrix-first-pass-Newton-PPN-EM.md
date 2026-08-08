# 3735 - Response Matrix First Pass: Newton/PPN and EM

## Status
- `RESPONSE_MATRIX_CONTRACT_READY_VALUES_MISSING`
- `beta_NP` and `beta_EM` now have finite `B/G/W` matrix contracts.
- All entries remain placeholders, so this is a computability scaffold, not evidence.

## Norm Contracts
- `NORM3735_NP` `Newton_PPN_bridge`: beta_NP^2=lambda_max(G_NP^{-1/2} B_NP^T W_NP B_NP G_NP^{-1/2})
- `NORM3735_EM` `EM_Poynting_bridge`: beta_EM^2=lambda_max(G_EM^{-1/2} B_EM^T W_EM B_EM G_EM^{-1/2})

## Basis Summary
- `Newton_PPN_bridge` domain_dim=5 obs_dim=5 domain=`h_phi;h_psi;h_GM;h_pref;h_bdy` observable=`y_accel;y_poisson;y_gamma;y_beta;y_pref`
- `EM_Poynting_bridge` domain_dim=5 obs_dim=5 domain=`h_chi;h_frame;h_Jem;h_alpha;h_EM_tail` observable=`y_poynting;y_stress;y_wave;y_pol;y_charge`

## B Entries
- `BME3735_B3732_NP_accel_phi` `B_NP` `y_accel` <- `h_phi` via `grad_operator_norm_C_grad`
- `BME3735_B3732_NP_poisson_phi` `B_NP` `y_poisson` <- `h_phi` via `laplacian_operator_norm_C_lap`
- `BME3735_B3732_NP_poisson_gm` `B_NP` `y_poisson` <- `h_GM` via `4pi_rho_norm_C_GM`
- `BME3735_B3732_NP_gamma_phipsi` `B_NP` `y_gamma` <- `h_phi;h_psi` via `C_gamma_metric_ratio`
- `BME3735_B3732_NP_beta_phi` `B_NP` `y_beta` <- `h_phi` via `C_beta_second_order`
- `BME3735_B3732_NP_pref_pref` `B_NP` `y_pref` <- `h_pref` via `C_preferred_frame`
- `BME3735_B3732_NP_boundary` `B_NP` `y_accel;y_poisson` <- `h_bdy` via `C_boundary_projection`
- `BME3735_B3732_EM_poynting_chi` `B_EM` `y_poynting` <- `h_chi` via `C_poynting_chi_derivative`
- `BME3735_B3732_EM_poynting_current` `B_EM` `y_poynting` <- `h_Jem` via `C_JdotE`
- `BME3735_B3732_EM_stress_frame` `B_EM` `y_stress` <- `h_frame` via `C_TEM_frame`
- `BME3735_B3732_EM_wave_chi` `B_EM` `y_wave` <- `h_chi` via `C_wave_constitutive`
- `BME3735_B3732_EM_pol_chi` `B_EM` `y_pol` <- `h_chi` via `C_birefringence`
- `BME3735_B3732_EM_charge_marker` `B_EM` `y_charge` <- `h_alpha` via `C_charge_marker`
- `BME3735_B3732_EM_tail` `B_EM` `y_poynting;y_stress;y_wave;y_pol;y_charge` <- `h_EM_tail` via `C_EM_tail_projection`

## Positivity Gates
- `PG3735_0_GNP` `BLOCKED_PLACEHOLDER_VALUES`: G_NP positive definite | all domain Gram eigenvalues positive or diagonal entries positive in diagonal approximation
- `PG3735_1_WNP` `BLOCKED_PLACEHOLDER_VALUES`: W_NP positive semidefinite | observable weights/covariance inverse nonnegative with finite bounds
- `PG3735_2_BNP` `BLOCKED_PLACEHOLDER_VALUES`: B_NP finite | all response entries finite and source-owned/theorem-owned
- `PG3735_3_GEM` `BLOCKED_PLACEHOLDER_VALUES`: G_EM positive definite | all domain Gram eigenvalues positive or diagonal entries positive in diagonal approximation
- `PG3735_4_WEM` `BLOCKED_PLACEHOLDER_VALUES`: W_EM positive semidefinite | observable weights/covariance inverse nonnegative with finite bounds
- `PG3735_5_BEM` `BLOCKED_PLACEHOLDER_VALUES`: B_EM finite | all response entries finite and source-owned/theorem-owned

## Runner Rows
- `RUN3735_Newton_PPN_bridge` `BLOCKED_MISSING_RESPONSE_MATRIX_ENTRIES` missing_count=17
- `RUN3735_EM_Poynting_bridge` `BLOCKED_MISSING_RESPONSE_MATRIX_ENTRIES` missing_count=17

## Decisions
- `DEC3735_0_beta_contract_ready` `BETA_RESPONSE_MATRIX_CONTRACT_READY` | beta_NP and beta_EM now have finite-basis matrix contracts rather than loose symbols.
- `DEC3735_1_blocked_correctly` `RESPONSE_MATRICES_BLOCKED_BY_PLACEHOLDERS` | No beta score is allowed until B/G/W entries are source-owned or theorem-owned.
- `DEC3735_2_next` `NEXT_DERIVE_NEWTON_PPN_MATRIX_COEFFICIENTS` | The GR/Newton route should attack B_NP first because acceleration, Poisson, gamma, and beta are the cleanest local-reduction observables.

## Next Target
- `3736-Y5-R2FR-Newton-PPN-response-coefficients-from-weak-field-limit.md`
- Objective: derive the Newton/PPN response coefficients in `B_NP` from weak-field metric and Poisson relations.
