# 3708 Y5 R2FR u1 Parent Relaxation Functional Origin Or Local Mass Gap Closure

Private checkpoint. No GitHub action. No public claim.

## Status

- `U1_RECAST_AS_FISHER_GAP_PRODUCT_R10_SCORE_GATE_CONNECTED_NONCLAIM`
- 3708 stitches the existing 3698-3700 derivation chain to the 3707 score gate. The clean local mass gap is Xi_H=T_eff*iota_H-R_loss, with lambda_H=Xi_H^-1/2 and alpha_eff_clean=0.5*P_N/Xi_H^2. At the official 38.6 um anchor, clean Xi_H=6.711589572874e+08 m^-2 and P_N_max_eta10=8.108178227049e+17 m^-4. The tightest private candidate row has lambda=578.549278 um, Xi_H=2.987578239966e+06 m^-2, and P_N_max_eta10=3.782222325794e+10 m^-4.

## Main Result

- The old question `where does u_1 come from?` is now sharpened into a Fisher-gap product.
- Define `iota_H := lambda_min(G_H^-1/2 I_H^perp G_H^-1/2)` and `R_loss:=R_domain+R_source_slope-lambda_min_corr`.
- Then `Xi_H := mu_H^2 = T_eff*iota_H - R_loss`, `lambda_H=Xi_H^-1/2`, and the clean aligned branch has `u_1=Xi_H/2`.
- The R10 score becomes `alpha_eff_clean=0.5*P_N/Xi_H^2`, hence `P_N <= 2*(1-eta)*alpha_bound_R10(Xi_H^-1/2)*Xi_H^2`.
- This is progress because `lambda_H` is no longer a free range parameter if `T_eff`, `I_H^perp`, and correction losses are parent-filled.
- It remains nonclaim because those parent rows, `P_N`, `eta`, and the reviewed curve are not filled.
- `valid_for_claim=false`: this is a private derivation/score contract, not a local-GR/R10/PPN/EM pass.

## Numeric Consequences

- Official anchor: `lambda=38.6 um`, `Xi_H_clean=6.711589572874e+08 m^-2`, `u1_clean=3.355794786437e+08 m^-2`, `P_N_max_eta10=8.108178227049e+17 m^-4`.
- Tightest private candidate row: `lambda=578.549278 um`, `Xi_H_clean=2.987578239966e+06 m^-2`, `P_N_max_eta10=3.782222325794e+10 m^-4`.
- Gap score rows generated: `67`.

## Derivation Chain

- `FGD3708_0_parent_bath` `CONDITIONAL_PARENT_CONSTRUCTION_FROM_3698_3699`: p_z(xi|X_B,q)=p_0 exp[z^A Y_A^perp-W(z;X_B,q)]
- `FGD3708_1_fisher_entropy` `DERIVED_IF_P0_YA_DEFINED`: D_KL(p_z||p_0)=0.5 I_AB^perp z^A z^B+O(z^3)
- `FGD3708_2_free_energy_to_u1` `STRUCTURAL_DERIVATION_NONCLAIM_UNITS_MISSING`: Delta F_cg=T_eff D_KL; u_1_parent=0.5*T_eff*lambda_min(G_H^-1/2 I_H^perp G_H^-1/2)
- `FGD3708_3_corrected_gap` `GAP_VARIABLE_DEFINED`: Xi_H := mu_H^2 = T_eff*iota_H - R_loss, with iota_H=lambda_min(G_H^-1/2 I_H^perp G_H^-1/2) and R_loss=R_domain+R_source_slope-lambda_min_corr
- `FGD3708_4_R10_rewrite` `EXECUTABLE_NONCLAIM_SCORE_REWRITE`: alpha_eff_clean=0.5*P_N/Xi_H^2; require P_N <= 2*(1-eta)*alpha_bound_R10(Xi_H^-1/2)*Xi_H^2
- `FGD3708_5_second_order_bridge` `LOCAL_ARENA_GATE_REWRITTEN`: epsilon_i <= 0.5*rho_i*((C_H||J_y+B_y||/Xi_H)^2+B_edge^2+B_boundary^2)+epsilon_edge+epsilon_proj+epsilon_boundary

## Parent Contract Rows

- `PCI3708_0_p0` `p_0(xi|X_B,q)`: `MISSING_PARENT_BATH_ROW` | source normalized local bath/reference distribution
- `PCI3708_1_Yperp` `Y_A^perp`: `MISSING_PARENT_LEAKAGE_OBSERVABLES` | parent leakage observables after Fisher projection against resolved matter/EM/Poynting/Newton/clock scores
- `PCI3708_2_IH` `I_H^perp`: `MISSING_NUMERIC_FISHER_MATRIX` | Fisher covariance positive on horizontal leakage modes after vertical nulls removed
- `PCI3708_3_Teff` `T_eff`: `MISSING_TEMPERATURE_UNITS_ROW` | effective free-energy/action conversion scale with units matching local mass-gap convention
- `PCI3708_4_Rloss` `R_loss`: `MISSING_CORRECTION_BOUND` | domain/source-slope/correction loss term in Xi_H=T_eff*iota_H-R_loss
- `PCI3708_5_PN` `P_N`: `MISSING_SOURCE_PRODUCT` | K_N*rho_Newton*C_H^2||J_y+B_y||^2 source product
- `PCI3708_6_eta` `eta_boundary+eta_edge`: `MISSING_BOUNDARY_EDGE_SOURCE_VALUE` | boundary/edge theorem-zero or finite source budget
- `PCI3708_7_rho_i` `rho_i residual tensors`: `MISSING_PARENT_RESIDUAL_TENSORS` | second-order local observable tensors for PPN, Newton, EM/Poynting, clocks, WEP, orbits
- `PCI3708_8_curve` `alpha_bound_R10(lambda)`: `CANDIDATE_CURVE_ONLY` | reviewed or official R10 bound curve

## Local Arena Gates

- `LAG3708_0_R10` `short-range Newton/R10`: alpha_eff_clean=0.5*P_N/Xi_H^2 + alpha_boundary_edge
- `LAG3708_1_PPN` `PPN/local metric`: S_PPN <= 0.5*rho_PPN*(C_HJ/Xi_H)^2 + K_Kperp||Kperp||/N_PPN + K_q||q_loc||/N_PPN
- `LAG3708_2_EM` `Maxwell/EM/Poynting stress`: epsilon_EM <= 0.5*rho_EM*(C_HJ/Xi_H)^2 + alpha_source_leak + current_normalization_error
- `LAG3708_3_clock` `precision clocks/time`: |delta nu/nu| <= 0.5*rho_clock*(C_HJ/Xi_H)^2 + clock_projection_error
- `LAG3708_4_WEP` `WEP/species`: eta_species <= 0.5||rho_species_a-rho_species_b||*(C_HJ/Xi_H)^2 + species_projection_error
- `LAG3708_5_orbital` `orbital dynamics`: delta_orbit <= K_orbit*0.5*rho_Newton*z0^2*exp(-2r*sqrt(Xi_H))*(1+r*sqrt(Xi_H))^2 + boundary

## Decisions

- `DEC3708_0_u1_route_promoted_to_fisher_gap_contract`: `BEST_CURRENT_DERIVATION_ROUTE_NONCLAIM` | Treat u_1/local screening as a Fisher-gap product Xi_H=T_eff*iota_H-R_loss, not as a free Yukawa mass.
- `DEC3708_1_R10_reduced_to_two_parent_products`: `EXECUTABLE_SCORE_FORM_NONCLAIM` | For R10, the local branch now needs only Fisher gap Xi_H and source product P_N plus eta/curve review.
- `DEC3708_2_anchor_requirement`: `ANCHOR_REQUIREMENT_RECORDED` | Official alpha=1 anchor requires clean Xi_H=6.711589572874e+08 m^-2 and P_N_max_eta10=8.108178227049e+17 m^-4.
- `DEC3708_3_candidate_tightest_requirement`: `PRIVATE_SMOKE_REQUIREMENT_RECORDED` | Tightest private candidate curve row is lambda=578.549278 um, Xi_H=2.987578239966e+06 m^-2, P_N_max_eta10=3.782222325794e+10 m^-4.
- `DEC3708_4_next_target`: `ADVANCE_TO_SOURCE_PRODUCT_FILL` | Next work should source or derive the first Xi_H and P_N rows, starting with R10 because its score gate is now shortest.

## Claim Gates

- `CG3708_0_p0_Y`: `BLOCKED` | p_0 and Y_A^perp are parent-defined and quotient-null
- `CG3708_1_fisher_gap`: `BLOCKED` | I_H^perp, T_eff and R_loss produce a positive sourced Xi_H
- `CG3708_2_source_product`: `BLOCKED` | P_N is parent-derived or bounded from K_N, rho_Newton, C_H and J_y+B_y
- `CG3708_3_eta_boundary`: `BLOCKED` | eta_boundary+eta_edge is theorem-zero or finite source value
- `CG3708_4_R10_curve`: `BLOCKED` | R10 alpha_bound(lambda) is official/reviewed
- `CG3708_5_residual_tensors`: `BLOCKED` | rho_i residual tensors are sourced for PPN, EM/Poynting, clock, WEP and orbital arenas
- `CG3708_6_public`: `BLOCKED` | local GR/Newton/Maxwell/R10 public claim allowed

## Source Register

- `doc_3698`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3698-Y5-R2FR-parent-entropy-free-energy-object-or-u1-closure-runner.md`
- `rec_3698`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3698_RELATIVE_ENTROPY_CONSTRUCTION_ROWS.csv`
- `fisher_3698`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3698_FISHER_ALIGNMENT_ROWS.csv`
- `u1_3698`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3698_U1_CLOSURE_RUNNER_ROWS.csv`
- `doc_3699`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3699-Y5-R2FR-parent-bath-observable-map-and-source-silence-fill.md`
- `bath_3699`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3699_BATH_DISTRIBUTION_ROWS.csv`
- `projection_3699`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3699_QUOTIENT_PROJECTION_ROWS.csv`
- `source_gates_3699`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3699_SOURCE_GATE_ROWS.csv`
- `doc_3700`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3700-Y5-R2FR-second-order-source-residual-vector-and-local-test-runner.md`
- `tensor_3700`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3700_RESIDUAL_TENSOR_ROWS.csv`
- `arena_3700`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3700_ARENA_RUNNER_ROWS.csv`
- `doc_3701`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3701-Y5-R2FR-local-test-source-row-acquisition-and-residual-matrix.md`
- `missing_3701`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3701_MISSING_MTS_INPUT_ROWS.csv`
- `ready_3701`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3701_SCORE_READINESS_ROWS.csv`
- `doc_3707`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3707-Y5-R2FR-PN-lambdaH-parent-source-product-origin-or-R10-score-gate.md`
- `score_3707`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3707_R10_SCORE_GATE_ROWS.csv`
- `anchor_3707`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3707_OFFICIAL_ANCHOR_SCORE_ROWS.csv`
- `input_3707`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3707_PARENT_INPUT_AUDIT_ROWS.csv`

## Next Target

- `3709-Y5-R2FR-Fisher-gap-and-PN-parent-source-row-fill-or-closure-demotion.md`
- Objective: try to source or derive the first numeric/symbolic parent rows for Xi_H=T_eff*iota_H-R_loss and P_N; if not possible, demote the local mass-gap route to explicit closure while preserving the R10/PPN/EM score gates
