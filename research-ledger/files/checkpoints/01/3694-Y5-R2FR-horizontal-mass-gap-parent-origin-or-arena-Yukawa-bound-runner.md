# 3694 - Horizontal mass-gap parent origin or arena Yukawa bound runner

Private checkpoint. No GitHub action. No local-GR/Newton/R10/PPN/EM claim.

## Status
- `PARENT_MASS_GAP_FORMULA_DERIVED_BUT_UNSIGNED_YUKAWA_BOUND_RUNNER_STAGED`
- The parent-origin formula for the horizontal mass gap is now explicit, including Schur/domain/source-slope corrections. It is not claimable yet, so the local branch is routed through nonclaim Yukawa/arena rows until G_H, M_eff,H, mu_H, alpha_A and arena projections are sourced.

## Parent Mass-Gap Derivation
- The horizontal local-GR route needs a real `mu_H`, not a verbal plateau.
- Parent formula: `M_H,IJ = H_I^A [nabla_A nabla_B Gamma_eff + nabla_A nabla_B U_resp + nabla_A nabla_B U_src] H_J^B |_{Z=0}`.
- Kinetic metric: `G_H,IJ = H_I^A G_AB H_J^B`.
- Effective matrix with mixing/domain corrections: `M_eff,H = M_HH - M_HV M_VV^+ M_VH + M_boundary + M_domain + M_connection`.
- Gap definition: `mu_H^2 := lambda_min(G_H^{-1/2} M_eff,H G_H^{-1/2}) - R_domain - R_source_slope`.
- Claim condition: `mu_H^2>0` and `ell_H=1/mu_H` short enough for every local arena.

## Yukawa Runner
- Because the parent-owned numeric gap is not yet supplied, local testing must use nonclaim Yukawa rows.
- Master local form: `lambda_H=ell_H=1/mu_H`, `alpha_A=K_A (||M_y||+||N_Dq||||Dq_H||) C_H ||J_y+B_y||/N_A`.
- Arena residual: `residual_A(r)=|alpha_A| exp(-r/lambda_H)(1+r/lambda_H)+R_edge_A+R_proj_A`.
- R10/Newton gate: `abs(alpha_N(lambda_H)) <= alpha_bound_R10(lambda_H)` only after a real bound curve and `K_N` source normalization are wired in.

## Newton Constant Note
- GR does not derive the numerical value of `G_N`; it calibrates it as the Einstein-Hilbert/source coupling normalization.
- MTS can try to derive `G_N` from its source coupling, but until that exists the fair rule is: calibrate the GR/Newton fixed point once, then test only residual deviations.

## Parent Gap Rows
- `PMG3694_0_parent_potential`: horizontal Hessian source | `FORMULA_DERIVED_PARENT_POTENTIAL_UNSIGNED` | M_H,IJ = H_I^A [nabla_A nabla_B Gamma_eff + nabla_A nabla_B U_resp + nabla_A nabla_B U_src] H_J^B |_{Z=0}
- `PMG3694_1_metric_weight`: kinetic metric | `FORMULA_DERIVED_GH_POSITIVITY_UNSIGNED` | G_H,IJ = H_I^A G_AB H_J^B
- `PMG3694_2_effective_matrix`: Schur-corrected mass matrix | `EFFECTIVE_MATRIX_FORM_DERIVED_NUMERIC_INPUTS_MISSING` | M_eff,H = M_HH - M_HV M_VV^+ M_VH + M_boundary + M_domain + M_connection
- `PMG3694_3_gap_definition`: mass gap | `MASS_GAP_DEFINITION_DERIVED_VALUE_MISSING` | mu_H^2 := lambda_min(G_H^{-1/2} M_eff,H G_H^{-1/2}) - R_domain - R_source_slope
- `PMG3694_4_environment`: environmental screening derivative | `ENVIRONMENTAL_ROUTE_FORMAL_NOT_SIGNED` | d mu_H^2/d rho = lambda_min' [G_H^{-1/2}(partial_rho M_eff,H - mu_H^2 partial_rho G_H)G_H^{-1/2}]
- `PMG3694_5_verdict`: parent mass-gap verdict | `PARENT_MASS_GAP_NOT_CLAIMED_YUKAWA_RUNNER_REQUIRED` | mu_H^2(local)>0 and ell_H(local)=1/mu_H small enough for every local arena

## Yukawa/Arena Runner Rows
- `YBR3694_0_master`: all local arenas | `NONCLAIM_SCHEMA_READY_VALUES_MISSING` | lambda_H=ell_H=1/mu_H; alpha_A=K_A (||M_y||+||N_Dq||||Dq_H||) C_H ||J_y+B_y||/N_A
- `YBR3694_1_R10_Newton`: Newton/R10 | `NONCLAIM_NEEDS_REAL_BOUND_CURVE_AND_KN` | pass_if abs(alpha_N(lambda_H)) <= alpha_bound_R10(lambda_H)
- `YBR3694_2_PPN`: PPN | `NONCLAIM_NEEDS_PPN_PROJECTION` | pass_if A_PPN <= epsilon_PPN with A_PPN=C_PPN residual_A(r_solar)
- `YBR3694_3_clocks_WEP`: clocks/WEP/Gdot | `NONCLAIM_NEEDS_CLOCK_WEP_SENSITIVITIES` | pass_if K_clock residual_A + K_species residual_A + K_Gdot residual_A <= epsilon_clock/WEP/Gdot
- `YBR3694_4_EM`: Maxwell/EM stress | `NONCLAIM_NEEDS_EM_STRESS_SOURCE_ROWS` | pass_if ||Delta T_EM||/||T_EM|| and |Delta alpha_fs/alpha_fs| stay below arena tolerances
- `YBR3694_5_orbital`: orbital/ephemeris | `NONCLAIM_NEEDS_ORBITAL_KERNEL_ROWS` | pass_if |delta a_r/a_N| + |delta dot_omega|/dot_omega_bound <= epsilon_orbital

## Calibration Rows
- `CAL3694_0_Newton_G`: Newton constant calibration | `CALIBRATION_LAW_STAGED_NOT_DERIVED` | MTS route: G_N = K_GR[theta0,G_H,M_eff,H,J_mass] at the GR/Newton fixed point, then local residuals are deviations around that calibrated value.
- `CAL3694_1_equal_baseline`: fair comparison rule | `BASELINE_RULE_RECORDED` | This keeps tests fair: constants may be fitted once, but extra horizontal residuals must still pass PPN/R10/clock/WEP/orbital constraints.

## Decisions
- `DEC3694_0`: `YUKAWA_RUNNER_SELECTED` - Formula for mu_H exists, but source-owned G_H, M_eff,H and environmental terms are not yet supplied.
- `DEC3694_1`: `NEXT_PARENT_HESSIAN_TARGET` - Next derive the parent Hessian/kinetic metric from the MTS scalar/action spine, while keeping all local arena rows nonclaim.
- `DEC3694_2`: `NO_FAKE_G_DERIVATION` - Treat G_N as a calibrated fixed-point normalization unless MTS derives it from parent source coupling.

## Claim Gates
- `CG3694_0_muH`: `BLOCKED` - mu_H numeric/local/environmental value missing
- `CG3694_1_yukawa`: `BLOCKED` - alpha/lambda predictions not sourced
- `CG3694_2_R10`: `BLOCKED` - real R10 alpha_bound(lambda) and K_N not both wired to this branch
- `CG3694_3_EM`: `BLOCKED` - EM stress/charge-current normalization not sourced
- `CG3694_4_local_GR`: `BLOCKED` - local GR not claimed until every arena residual passes against calibrated baselines
- `CG3694_5_public`: `BLOCKED` - private checkpoint; no GitHub/public claim

## Source Register
- `handoff_3693`: exists=True, needle_found=True, path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3693_NEXT_TARGET.csv`
- `operator_3693`: exists=True, needle_found=True, path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3693_HORIZONTAL_OPERATOR_ROWS.csv`
- `suppression_3693`: exists=True, needle_found=True, path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3693_LOCAL_SUPPRESSION_LAW_ROWS.csv`
- `arena_3693`: exists=True, needle_found=True, path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3693_ARENA_SUPPRESSION_GATES.csv`
- `split_3693`: exists=True, needle_found=True, path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3693_VERTICAL_HORIZONTAL_SPLIT_THEOREM_ROWS.csv`
- `clean_action_3686`: exists=True, needle_found=True, path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3686-Y5-R2FR-GK-q_loc-action-existence-Helmholtz-or-RGK-action-bound-row.md`
- `helmholtz_3687`: exists=True, needle_found=True, path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3687-Y5-R2FR-clean-response-action-Helmholtz-matrix-or-DeltaK-bound-row.md`
- `green_3690`: exists=True, needle_found=True, path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3690-Y5-R2FR-canonical-source-coupling-JA-zero-theorem-or-Green-profile-bound.md`

## Next Target
- `3695-Y5-R2FR-parent-Hessian-kinetic-metric-source-extraction-for-muH.md`
- Objective: extract or construct the parent scalar/action Hessian and kinetic metric that define G_H and M_eff,H; if absent, make an explicit closure assumption row instead of claiming local screening
