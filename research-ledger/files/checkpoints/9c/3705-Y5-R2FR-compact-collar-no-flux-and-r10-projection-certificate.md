# 3705 Y5 R2FR Compact Collar No-Flux And R10 Projection Certificate

Private checkpoint. No GitHub action. No public claim.

## Status

- `R10_PROJECTION_ZERO_SIGNED_PRIVATE_BRANCH_COLLAR_THEOREM_STAGED_EDGE_BOUNDARY_OPEN`
- 3705 branch-signs alpha_proj=0 for the private R2FR R10 branch and rewrites alpha_nuisance as collar/edge-only. Generated 67 reduced budget rows with eta_proj=0. Boundary/edge zeros are mathematically sufficient under a compact no-flux collar, but not parent-signed yet.

## Main Result

- `alpha_proj=0` is now branch-signed for the private R2FR R10 branch.
- Reason: the resolved Fisher basis already includes Newton/GR calibration; first-order leakage is projected out, and second-order Newton/R10 leakage is owned by `rho_Newton/P_N`.
- The reduced nuisance is `alpha_boundary_edge := 0.5*K_N*rho_Newton*(B_edge^2+B_boundary^2)+alpha_edge`.
- The reduced R10 gate is `0.5*P_N*lambda_H^4 + alpha_boundary_edge <= alpha_bound_R10(lambda_H)`.
- The compact collar/no-flux theorem is mathematically sufficient for `B_boundary=B_edge=alpha_edge=0`, but it is not parent-signed yet.
- `valid_for_claim=false`: this removes a private nuisance knob; it does not claim local Newton/R10 recovery.

## Projection Certificate

- `RPC3705_0_resolved_basis`: `SOURCE_CONFIRMED` | passed=True | R10/Newton fixed-point calibration is represented by resolved score C_N including kappa_GR
- `RPC3705_1_projection_operator`: `SOURCE_CONFIRMED` | passed=True | leakage scores are Fisher-projected against all resolved C_i before entering local tests
- `RPC3705_2_first_order_Newton_silence`: `SOURCE_CONFIRMED` | passed=True | partial_z kappa_GR|_0=0 and first-order Newton/R10 readout leakage is forbidden
- `RPC3705_3_second_order_owner`: `BRANCH_DEFINITION_CONFIRMED` | passed=True | remaining Newton/R10 leakage is counted only through rho_Newton/P_N, not alpha_proj
- `RPC3705_4_certificate`: `BRANCH_SIGNED_NONPUBLIC` | passed=True | alpha_proj=0 inside the private R2FR local R10 branch

## Collar Theorem

- `CCT3705_0_domain`: `mathematically_sufficient` parent_signed=False | choose compact collar Omega_c with source/readout support strictly inside its interior
- `CCT3705_1_boundary_condition`: `mathematically_sufficient` parent_signed=False | horizontal variations obey y|partialOmega_c=0 or natural n_mu G_H^{mu nu}D_nu y=0
- `CCT3705_2_no_incoming_flux`: `mathematically_sufficient` parent_signed=False | no incoming horizontal response flux through partialOmega_c
- `CCT3705_3_cutoff_support`: `mathematically_sufficient` parent_signed=False | cutoff derivative support is disjoint from source and R10 readout support
- `CCT3705_4_same_readout`: `mathematically_sufficient` parent_signed=False | R10/Newton readout operator is identical on the interior and collar overlap
- `CCT3705_5_parent_signature_gap`: `parent_signature_missing` parent_signed=False | parent action/boundary sector must own CCT3705_0 through CCT3705_4

## Zero Verdicts

- `ZV3705_0_alpha_proj`: `ZERO_IN_PRIVATE_BRANCH` | alpha_proj | alpha_proj=0 follows from the resolved Fisher quotient branch definition; any Newton/R10 leakage is in P_N.
- `ZV3705_1_B_boundary`: `ZERO_IF_COLLAR_PARENT_SIGNED_ELSE_BUDGET` | B_boundary | compact fixed/no-flux collar kills it mathematically, but parent boundary ownership is not yet signed.
- `ZV3705_2_B_edge`: `ZERO_IF_SUPPORT_COLLAR_PARENT_SIGNED_ELSE_BUDGET` | B_edge | support separation kills it mathematically, but the collar/support contract is not yet parent-signed.
- `ZV3705_3_alpha_edge`: `ZERO_IF_SAME_READOUT_PARENT_SIGNED_ELSE_BUDGET` | alpha_edge | same readout on collar overlap kills it mathematically, but the readout identity is not yet parent-signed.
- `ZV3705_4_reduced_nuisance`: `alpha_nuisance = 0.5*K_N*rho_Newton*(B_edge^2+B_boundary^2)+alpha_edge` | alpha_nuisance_reduced | projection nuisance is removed; only collar/boundary/edge nuisance remains.

## Eta Components

- `ETA3705_0_projection`: `eta_proj` = `0` | BRANCH_SIGNED_NONPUBLIC
- `ETA3705_1_boundary`: `eta_boundary` = `MISSING_FINITE_BOUND_OR_PARENT_ZERO` | OPEN
- `ETA3705_2_edge`: `eta_edge` = `MISSING_FINITE_BOUND_OR_PARENT_ZERO` | OPEN
- `ETA3705_3_total`: `eta_R10` = `eta_boundary + eta_edge` | REDUCED_BUDGET_SCHEMA

## Reduced Budget Rows

- Reduced candidate rows generated: `67`.
- Tightest eta_boundary+eta_edge=0.1 row: `lambda=578.549278 um`, `P_N_max=3.782222325794e+10 m^-4`.

## Decisions

- `DEC3705_0`: `PROJECTION_ZERO_ADVANCES` | Projection nuisance is removed from the private R10 branch. | The resolved Fisher basis already owns Newton/GR calibration and routes residual force leakage through rho_Newton/P_N; alpha_proj is not a second knob.
- `DEC3705_1`: `COLLAR_THEOREM_STAGED_NOT_CLAIMED` | The collar theorem is mathematically sufficient but not parent-signed. | Boundary/edge zero requires parent-owned compact collar, no-flux or fixed boundary data, support separation, and same readout; 1010 says boundary ownership is still open.
- `DEC3705_2`: `BUDGET_REDUCED` | The R10 nuisance budget is reduced from three components to two. | eta_proj=0; only eta_boundary and eta_edge remain, and they must be zero-proved or finite-bounded.

## Claim Gates

- `CG3705_0_projection`: `PASS_PRIVATE_NONPUBLIC` | alpha_proj=0 in the private branch
- `CG3705_1_parent_collar`: `BLOCKED` | parent action/boundary sector signs compact collar and no-flux/fixed-boundary conditions
- `CG3705_2_edge_support`: `BLOCKED` | source/readout support separation and same readout operator are parent-signed
- `CG3705_3_budget`: `BLOCKED` | eta_boundary+eta_edge is zero or finite and <1
- `CG3705_4_R10_score`: `BLOCKED` | P_N and lambda_H are parent-sourced and scored with eta_proj=0
- `CG3705_5_public`: `BLOCKED` | public R10/local-Newton claim allowed

## Source Register

- `doc_3704`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3704-Y5-R2FR-alpha-nuisance-zero-or-budget-boundary-projection-cleanup.md`
- `theorem_3704`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3704_NUISANCE_ZERO_THEOREM_CONTRACT_ROWS.csv`
- `terms_3704`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3704_NUISANCE_TERM_VERDICT_ROWS.csv`
- `budget_3704`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3704_ALPHA_NUISANCE_BUDGET_ROWS.csv`
- `projection_3699`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3699_QUOTIENT_PROJECTION_ROWS.csv`
- `source_gate_3699`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3699_SOURCE_GATE_ROWS.csv`
- `suppression_3693`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3693_LOCAL_SUPPRESSION_LAW_ROWS.csv`
- `yukawa_3694`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3694_YUKAWA_ARENA_BOUND_RUNNER_ROWS.csv`
- `q_loc_1010`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1010-Y5-R10-Gamma-Khat-action-existence-Helmholtz-or-q_loc-residual-retention.md`

## Next Target

- `3706-Y5-R2FR-parent-boundary-action-collar-signature-or-edge-budget-bound.md`
- Objective: try to derive the compact collar/no-flux boundary condition from the parent action boundary term; if not, produce finite eta_boundary and eta_edge bound rows
