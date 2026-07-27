# 3704 Y5 R2FR Alpha-Nuisance Zero Or Budget Boundary Projection Cleanup

Private checkpoint. No GitHub action. No public claim.

## Status

- `ALPHA_NUISANCE_SPLIT_INTO_PROJECTION_ZERO_CONTRACT_AND_EDGE_BOUNDARY_BUDGET_RUNNER`
- 3704 converts alpha_nuisance into a precise branch contract: alpha_proj can be zeroed only by a resolved Newton/R10 quotient certificate; edge and boundary terms require compact collar/no-flux theorems or explicit eta_R10 budgets. Generated 67 budget rows from the 3703 product curve.

## Main Result

- 3703 left `alpha_nuisance` as the local R10 obstruction.
- 3704 splits it into three distinct responsibilities: projection leakage, boundary leakage, and edge/collar leakage.
- The projection term has a real zero route: if the R10/Newton readout is part of the Fisher-resolved quotient basis, `alpha_proj=0`; its second-order leakage is then already counted in `rho_Newton/P_N`.
- Boundary and edge terms do not get a free pass: they require a compact fixed/no-flux collar theorem or finite `eta_R10` budgets.
- The clean zero branch is `alpha_nuisance=0`, which reduces R10 to `0.5*P_N*lambda_H^4 <= alpha_bound_R10(lambda_H)`.
- The budget branch is `alpha_nuisance <= eta_R10*alpha_bound_R10(lambda_H)`, giving `P_N <= 2*(1-eta_R10)*alpha_bound_R10(lambda_H)/lambda_H^4`.
- `valid_for_claim=false` throughout: this is a branch contract and budget runner, not a local-Newton claim.

## Zero Contract

- `NZT3704_0_decomposition`: `DERIVED_INPUT` | alpha_nuisance | 0.5*K_N*rho_Newton*(B_edge^2+B_boundary^2)+alpha_edge+alpha_proj
- `NZT3704_1_projection_zero`: `CONDITIONAL_ZERO_THEOREM` | alpha_proj=0 | R10/Newton readout O_N is in the Fisher-resolved basis C_i and uses the same quotient q/P_loc as the GR/Newton fixed point
- `NZT3704_2_boundary_zero`: `CONDITIONAL_ZERO_THEOREM_UNSIGNED` | B_boundary=0 | local R10 branch is posed on a compact collar domain with fixed quotient data, y|partialOmega=0 or natural n.G_H Dy=0, and no incoming horizontal flux
- `NZT3704_3_edge_zero`: `CONDITIONAL_ZERO_THEOREM_UNSIGNED` | B_edge=0 and alpha_edge=0 | source support lies strictly inside the collar, cutoff derivatives do not overlap horizontal response support, and the readout operator is the same on the interior and collar
- `NZT3704_4_full_zero`: `CONDITIONAL_BRANCH_CONTRACT` | alpha_nuisance=0 | NZT3704_1, NZT3704_2, and NZT3704_3 all hold simultaneously
- `NZT3704_5_budget_fallback`: `BUDGET_THEOREM` | alpha_nuisance <= eta_R10*alpha_bound_R10(lambda_H), 0<=eta_R10<1 | if any zero clause is unsigned or finite, allocate a sourced absolute budget rather than claiming zero

## Term Verdicts

- `TERM3704_0_alpha_proj`: `conditionallly_zero_if_resolved_Newton_R10_basis_complete` | alpha_proj | Fisher projection already includes kappa_GR/Newton coupling; any remaining R10 Newton second-order leakage belongs in rho_Newton/P_N, not an extra projection knob.
- `TERM3704_1_B_boundary`: `not_zero_without_no_flux_or_fixed_boundary_contract` | B_boundary | 1010 still marks boundary no-flux unsigned; therefore boundary leakage cannot be deleted by rhetoric.
- `TERM3704_2_B_edge`: `not_zero_without_collar_support_contract` | B_edge | 3693/3694 keep R_edge explicit; it can vanish for compact support/collar geometry but is not yet parent-signed.
- `TERM3704_3_alpha_edge`: `not_zero_without_same_readout_operator_contract` | alpha_edge | edge readout mismatch is separate from the bulk P_N product and must not be hidden inside rho_Newton.

## Budget Rows

- Candidate budget rows generated: `67`.
- Tightest eta10 row: `lambda=578.549278 um`, `P_N_max_eta10=3.782222325794e+10 m^-4`.
- All budget rows are private/nonclaim because `eta_R10`, `P_N`, and `lambda_H` are not parent-sourced yet.

## Decisions

- `DEC3704_0`: `PROJECTION_BRANCH_SHARPENED` | Alpha projection is no longer allowed to float as an independent knob. | If R10/Newton readout is in the resolved Fisher quotient basis, alpha_proj=0; otherwise the branch must declare an explicit eta_proj budget.
- `DEC3704_1`: `ZERO_PROOF_INCOMPLETE` | Boundary and edge zeros are plausible but not currently parent-signed. | The archive still keeps boundary no-flux and R_edge/R_proj terms explicit, so deleting them would be a closure assumption.
- `DEC3704_2`: `BUDGET_RUNNER_READY` | R10 can still be scored privately through an eta_R10 budget. | For any sourced eta_R10<1, the product gate becomes P_N <= 2*(1-eta_R10)*alpha_bound/lambda_H^4.

## Claim Gates

- `CG3704_0_projection`: `BLOCKED` | R10/Newton readout and P_loc certified inside the Fisher-resolved quotient basis
- `CG3704_1_boundary`: `BLOCKED` | compact fixed/no-flux collar proves B_boundary=0 or finite eta_boundary is sourced
- `CG3704_2_edge`: `BLOCKED` | support/collar/readout theorem proves B_edge=alpha_edge=0 or finite eta_edge is sourced
- `CG3704_3_eta`: `BLOCKED` | eta_R10 components are zero or finite absolute-summed sourced budgets with eta_R10<1
- `CG3704_4_score`: `BLOCKED` | P_N/lambda_H are parent-sourced and scored against the selected eta_R10 row
- `CG3704_5_public`: `BLOCKED` | public R10/local-Newton claim allowed

## Source Register

- `doc_3703`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3703-Y5-R2FR-MTS-rho-Newton-z2bound-muH-numeric-or-symbolic-bound.md`
- `product_3703`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3703_R10_PRODUCT_BOUND_ROWS.csv`
- `missing_3703`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3703_MISSING_PARENT_INPUT_ROWS.csv`
- `projection_3699`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3699_QUOTIENT_PROJECTION_ROWS.csv`
- `source_gate_3699`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3699_SOURCE_GATE_ROWS.csv`
- `suppression_3693`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3693_LOCAL_SUPPRESSION_LAW_ROWS.csv`
- `yukawa_3694`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3694_YUKAWA_ARENA_BOUND_RUNNER_ROWS.csv`
- `q_loc_1010`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1010-Y5-R10-Gamma-Khat-action-existence-Helmholtz-or-q_loc-residual-retention.md`

## Next Target

- `3705-Y5-R2FR-compact-collar-no-flux-and-r10-projection-certificate.md`
- Objective: try to parent-sign the two remaining zero clauses: R10/Newton projection completeness and compact collar no-flux/edge silence
