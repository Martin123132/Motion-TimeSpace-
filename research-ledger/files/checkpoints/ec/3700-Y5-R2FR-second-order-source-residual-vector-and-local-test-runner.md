# 3700 Y5 R2FR Second-Order Source Residual Vector And Local Test Runner

Private checkpoint. No GitHub action. No public claim.

## Status

- `SECOND_ORDER_LOCAL_RESIDUAL_VECTOR_DERIVED_RUNNER_SCHEMA_READY_VALUES_MISSING`
- 3700 turns Fisher source silence into the local-test bridge: after first-order projection, each local observable has Delta O_i=0.5 z^A z^B R_iAB+O(|z|^3). With z bounded by the horizontal mass gap, every arena gets a pass inequality. The route is mathematically sharper and test-facing, but remains nonclaim until residual tensors, amplitude rows, PPN/R10/EM/clock/orbit normalizers, and boundary/Kperp terms are sourced.

## Main Result

- `3699` gives first-order source silence: `<C_i^0 Y_A^perp>_0=0`.
- Therefore each local observable starts as `Delta O_i(z)=0.5 z^A z^B R_iAB+O(|z|^3)`.
- Define `rho_i=||G_H^-1/2 R_i G_H^-1/2||_op/N_i` and `z2_bound=(C_H||J_y+B_y||/mu_H^2)^2+B_edge^2+B_boundary^2`.
- Master local gate: `epsilon_i^MTS <= 0.5 rho_i z2_bound + epsilon_edge_i + epsilon_proj_i + epsilon_boundary_i`.
- Yukawa/local-range gate squares the first-order kernel: `epsilon_i(r) <= 0.5 rho_i z0^2 exp(-2r/lambda_H)(1+r/lambda_H)^2 + ...`.

## Meaning

- This is good news structurally: if Fisher projection is exact, local violations are quadratic, not linear.
- It is not yet a pass: quadratic can still be far too large unless `rho_i`, `z2_bound`, `Kperp`, `q_loc`, and boundary terms are small for derived reasons.
- This runner treats GR/Maxwell/Newton as the local baseline and scores only residual deviations, which is the fair comparison route.

## Residual Tensor Rows

- `RT3700_0_first_order_zero`: `DERIVED_FROM_3699` | Fisher projection gives <C_i^0 Y_A^perp>_0=0, so partial_A<O_i>_0=0.
- `RT3700_1_second_derivative`: `RESIDUAL_TENSOR_DEFINED` | R_iAB := partial_A partial_B<O_i>_0 = <C_i^0 Y_A^perp Y_B^perp>_0 - <C_i^0>_0 I_AB^perp.
- `RT3700_2_dimensionless_norm`: `NORM_GATE_DEFINED` | rho_i := ||G_H^-1/2 R_i G_H^-1/2||_op / N_i.
- `RT3700_3_amplitude_bound`: `AMPLITUDE_BOUND_CONDITIONAL` | z2_bound := (C_H ||J_y+B_y||/mu_H^2)^2 + B_edge^2 + B_boundary^2.
- `RT3700_4_master_bound`: `MASTER_LOCAL_BOUND_DERIVED` | epsilon_i^MTS <= 0.5 rho_i z2_bound + epsilon_edge_i + epsilon_proj_i + epsilon_boundary_i.
- `RT3700_5_yukawa_kernel`: `SECOND_ORDER_YUKAWA_KERNEL_DERIVED` | epsilon_i^MTS(r) <= 0.5 rho_i z0^2 exp(-2r/lambda_H)(1+r/lambda_H)^2 + epsilon_edge_i + epsilon_proj_i.

## Arena Runner Rows

- `AR3700_0_PPN`: PPN/local metric | `NONCLAIM_RUNNER_SCHEMA_READY_VALUES_MISSING` | S_PPN <= 0.5 rho_PPN z2_bound + K_Kperp||Kperp||/N_PPN + K_q||q_loc||/N_PPN
- `AR3700_1_R10_Newton`: short-range Newton/R10 | `NONCLAIM_RUNNER_SCHEMA_READY_VALUES_MISSING` | alpha_eff(lambda_H)=K_N * 0.5 rho_Newton z0^2 + alpha_edge + alpha_proj
- `AR3700_2_clock`: precision clocks/time | `NONCLAIM_RUNNER_SCHEMA_READY_VALUES_MISSING` | |delta nu/nu| <= 0.5 rho_clock z2_bound + clock_projection_error
- `AR3700_3_EM`: Maxwell/EM/Poynting stress | `NONCLAIM_RUNNER_SCHEMA_READY_VALUES_MISSING` | EM residual <= 0.5 rho_EM z2_bound + alpha_source_leak + current_normalization_error
- `AR3700_4_orbital`: orbital dynamics | `NONCLAIM_RUNNER_SCHEMA_READY_VALUES_MISSING` | orbital residual <= K_orbit * 0.5 rho_Newton z0^2 exp(-2r/lambda_H)(1+r/lambda_H)^2 + boundary terms
- `AR3700_5_WEP_species`: WEP/species dependence | `NONCLAIM_RUNNER_SCHEMA_READY_VALUES_MISSING` | eta_species <= 0.5 ||rho_species_a-rho_species_b|| z2_bound + species_projection_error

## Break Modes

- `BM3700_0_source_projection_fail`: `HARD_FAIL_OR_REPROJECT` | If <C_i^0 Y_A^perp>_0 != 0 for any local observable, the local branch has first-order leakage and likely fails precision tests.
- `BM3700_1_large_second_order`: `NUMERIC_BOUND_FAIL` | If rho_i z2_bound exceeds arena tolerance, first-order silence is not enough and local GR/Maxwell/Newton recovery fails or needs a stronger mass gap.
- `BM3700_2_boundary_zero_modes`: `BOUNDARY_THEOREM_REQUIRED` | Hyperbolic incoming waves, Neumann-like zero modes, topology, or nonzero boundary data add B_boundary and reopen local PPN/clock gates.
- `BM3700_3_Kperp_tensor`: `TENSOR_GATE_REQUIRED` | Scalar source silence does not control tensor Kperp unless Kperp is exactly zero, cubic, or explicitly PPN-bounded.
- `BM3700_4_fitted_tolerance`: `ANTI_TUNING_GATE` | Choosing rho_i, z0, K_i, or alpha_eff from the local experimental budget is forbidden tuning.

## Decisions

- `DEC3700_0`: `BRIDGE_ADVANCES` | Use the second-order residual vector as the local-test bridge. | It converts the Fisher source-silence theorem into PPN/R10/clock/EM/orbital quantities without pretending values are known.
- `DEC3700_1`: `CLAIM_BLOCKED` | Do not claim local GR/Maxwell/Newton pass. | The structural bound is derived, but rho_i, z2_bound, Kperp, q_loc, boundary amplitudes, and real experimental normalizers remain unfilled.
- `DEC3700_2`: `SOURCE_ROWS_NEXT` | Next move should be numeric-source acquisition, not more names. | The runner now names exactly which rows must be sourced to score the branch.

## Claim Gates

- `CG3700_0_R_tensor`: `BLOCKED` | R_iAB residual tensors sourced/bounded for matter, PPN, Newton, EM/Poynting, clocks, orbits, WEP
- `CG3700_1_amplitude`: `BLOCKED` | z2_bound sourced from parent J_y, mu_H, C_H, edge, and boundary rows
- `CG3700_2_test_normalizers`: `BLOCKED` | epsilon_i and N_i sourced for each local arena
- `CG3700_3_R10_curve`: `BLOCKED` | real R10 alpha_bound(lambda) curve and lambda_H scoring implemented
- `CG3700_4_PPN_solver`: `BLOCKED` | PPN Green-function projection constants and Kperp/q_loc tensor terms bounded
- `CG3700_5_EM_coupling`: `BLOCKED` | Maxwell stress, Poynting flux, alpha_fs, charge/current residuals bounded
- `CG3700_6_public`: `BLOCKED` | public local-GR/Maxwell/Newton claim allowed

## Source Register

- `handoff_3699`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3699_NEXT_TARGET.csv`
- `residuals_3699`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3699_RESIDUAL_BOUND_ROWS.csv`
- `projection_3699`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3699_QUOTIENT_PROJECTION_ROWS.csv`
- `source_gates_3699`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3699_SOURCE_GATE_ROWS.csv`
- `suppression_3693`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3693_LOCAL_SUPPRESSION_LAW_ROWS.csv`
- `yukawa_3694`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3694_YUKAWA_ARENA_BOUND_RUNNER_ROWS.csv`
- `ppn_trace_90`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\90-Lcg-gradient-trace-bound.md`
- `parent_clock_newton_83`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\83-parent-equations-v1.md`
- `red_team_06`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\06-consistency-red-team.md`

## Next Target

- `3701-Y5-R2FR-local-test-source-row-acquisition-and-residual-matrix.md`
- Objective: create source-ready numeric/symbolic rows for rho_i, z2_bound, Kperp, q_loc, R10 alpha_bound(lambda), PPN normalizers, EM/Poynting residuals, clock and orbital tolerances
