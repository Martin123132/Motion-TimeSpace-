# 3703 Y5 R2FR MTS Rho-Newton Z2bound Muh Numeric Or Symbolic Bound

Private checkpoint. No GitHub action. No public claim.

## Status

- `R10_MTS_SIDE_COMPRESSED_TO_PARENT_SOURCE_PRODUCT_GATE_NONCLAIM`
- 3703 derives alpha_eff(lambda_H) <= 0.5*P_N*lambda_H^4 + alpha_nuisance and converts the 3702 candidate curve into 67 private P_N bound rows. This is a real narrowing step: R10 now asks for parent-sourced P_N, lambda_H, and alpha_nuisance, not a scattered list of unrelated missing constants.

## Main Result

- This checkpoint stops the R10 branch from being a bag of missing symbols.
- Starting from 3700, `alpha_eff(lambda_H)=K_N * 0.5*rho_Newton*z0^2 + alpha_edge + alpha_proj`.
- Starting from the mass-gap amplitude bound, `z0^2 <= (C_H ||J_y+B_y||/mu_H^2)^2 + B_edge^2 + B_boundary^2`.
- With `lambda_H=1/mu_H`, the R10 prediction compresses to `alpha_eff(lambda_H) <= 0.5*P_N*lambda_H^4 + alpha_nuisance`.
- The parent source product is `P_N := K_N*rho_Newton*C_H^2||J_y+B_y||^2` with units `m^-4`.
- The visible nuisance term is `alpha_nuisance := 0.5*K_N*rho_Newton*(B_edge^2+B_boundary^2)+alpha_edge+alpha_proj`.
- Therefore R10 asks for `0.5*P_N*lambda_H^4 + alpha_nuisance <= alpha_bound_R10(lambda_H)`.
- If nuisance leakage is zero, the private curve gives `P_N <= 2*alpha_bound_R10(lambda_H)/lambda_H^4`.
- If nuisance leakage is budgeted, `alpha_nuisance <= eta_R10*alpha_bound_R10` gives `P_N <= 2*(1-eta_R10)*alpha_bound_R10/lambda_H^4`.

## Anchor Consequence

- `ANCH3703_0_alpha1_range`: If the branch behaves like gravitational-strength Yukawa alpha_eff~1, R10 demands lambda_H < 38.6 micrometer, equivalently mu_H > 2.59067e4 m^-1.
- At the official alpha=1 anchor, zero-nuisance `P_N_max = 9.009086918943e+17 m^-4`.

## Product-Bound Curve

- Candidate product-bound rows generated: `67`.
- Tightest zero-nuisance private row: `lambda=578.549278 um`, `log10(P_N_max)=10.623504544`.
- All rows remain `valid_for_claim=false` because the bound curve is still candidate/manual-review-only and MTS-side `P_N/lambda_H/alpha_nuisance` are not parent-sourced.

## Derivation Rows

- `DER3703_0_R10_arena`: `DERIVED_INPUT` | alpha_eff(lambda_H)=K_N * 0.5*rho_Newton*z0^2 + alpha_edge + alpha_proj | start from the already-derived second-order source-silence bridge
- `DER3703_1_amplitude`: `DERIVED_INPUT` | z0^2 <= (C_H ||J_y+B_y||/mu_H^2)^2 + B_edge^2 + B_boundary^2 | replace unsourced z0 by the mass-gap/source amplitude bound
- `DER3703_2_range`: `DERIVED_INPUT` | lambda_H = 1/mu_H | turn the mass gap into the R10 force range
- `DER3703_3_substitution`: `NEW_3703_RESULT` | alpha_eff(lambda_H) <= 0.5*K_N*rho_Newton*C_H^2||J_y+B_y||^2*lambda_H^4 + alpha_nuisance | this is the useful compression: R10 sees a lambda^4 source-product plus nuisance leakage
- `DER3703_4_parent_product`: `NEW_3703_RESULT` | P_N := K_N*rho_Newton*C_H^2||J_y+B_y||^2 | collapses K_N, rho_Newton, source norm, and horizontal Green constant into one parent-owned product with units m^-4
- `DER3703_5_nuisance`: `NEW_3703_RESULT` | alpha_nuisance := 0.5*K_N*rho_Newton*(B_edge^2+B_boundary^2) + alpha_edge + alpha_proj | keeps edge/projection/boundary leakage visible instead of hiding it inside P_N
- `DER3703_6_R10_gate`: `NEW_3703_RESULT` | 0.5*P_N*lambda_H^4 + alpha_nuisance <= alpha_bound_R10(lambda_H) | this is now the exact nonclaim local-Newton gate produced by the 3699-3702 chain
- `DER3703_7_product_bound`: `NEW_3703_RESULT` | P_N <= 2*(alpha_bound_R10(lambda_H)-alpha_nuisance)/lambda_H^4 | if alpha_nuisance is zero or separately bounded, the candidate R10 curve directly bounds the parent source product
- `DER3703_8_budget_fraction`: `NEW_3703_RESULT` | if alpha_nuisance <= eta_R10*alpha_bound_R10, then P_N <= 2*(1-eta_R10)*alpha_bound_R10/lambda_H^4 | gives a fair future scoring route without pretending nuisance leakage is absent

## Missing Parent Inputs

- `MISS3703_0_P_N`: `P_N` | K_N*rho_Newton*C_H^2||J_y+B_y||^2 | next: derive from parent source coupling, Fisher residual tensor, horizontal Green constant, and source norm
- `MISS3703_1_lambda_H`: `lambda_H` | 1/mu_H | next: derive mu_H from horizontal mass gap, Hessian/Fisher eigenvalue, or source-sector stability operator
- `MISS3703_2_alpha_nuisance`: `alpha_nuisance` | 0.5*K_N*rho_Newton*(B_edge^2+B_boundary^2)+alpha_edge+alpha_proj | next: prove zero by boundary/projection theorem or allocate a sourced eta_R10 budget
- `MISS3703_3_curve_review`: `alpha_bound_R10(lambda)` | candidate curve from fig5b1 | next: replace by official supplemental table or manually reviewed digitization before claims

## Smoke Rows

- `SMOKE3703_0_product_curve_schema`: score_ready=True claim=false | derived 67 P_N bound rows from the 3702 candidate R10 curve | blocker: candidate curve remains manual-review-only; MTS P_N/lambda_H/alpha_nuisance are not sourced
- `SMOKE3703_1_tightest_private_row`: score_ready=False claim=false | tightest zero-nuisance candidate row is lambda=578.549278 um with log10(P_N_max)=10.623504544 | blocker: cannot score until MTS predicts lambda_H and P_N independently
- `SMOKE3703_2_largest_private_row`: score_ready=False claim=false | loosest zero-nuisance candidate row is lambda=5.839634 um with log10(P_N_max)=27.239664168 | blocker: large allowed P_N at short range does not help unless mu_H places the branch there
- `SMOKE3703_3_anchor_muH`: score_ready=False claim=false | If the branch behaves like gravitational-strength Yukawa alpha_eff~1, R10 demands lambda_H < 38.6 micrometer, equivalently mu_H > 2.59067e4 m^-1. | blocker: anchor constrains gravitational-strength alpha_eff only; arbitrary alpha_eff needs full curve and MTS values

## Decisions

- `DEC3703_0`: `DERIVATION_ADVANCES` | R10 missing-input set is reduced to a source-product gate. | The chain now says exactly what must be true: 0.5*P_N*lambda_H^4 + alpha_nuisance must sit below the R10 bound curve.
- `DEC3703_1`: `CLAIM_BLOCKED` | Do not claim R10/local-Newton recovery. | P_N, lambda_H, and alpha_nuisance are still not parent-sourced, and the R10 curve is candidate-only.
- `DEC3703_2`: `NEXT_TARGET_SELECTED` | Next attack should be edge/projection/boundary cleanup before chasing more public data. | Without alpha_nuisance=0 or alpha_nuisance <= eta_R10 alpha_bound, no finite P_N result can be trusted.

## Claim Gates

- `CG3703_0_curve`: `BLOCKED` | official/reviewed alpha_bound_R10(lambda) curve
- `CG3703_1_parent_range`: `BLOCKED` | parent-derived numeric lambda_H=1/mu_H
- `CG3703_2_parent_product`: `BLOCKED` | parent-derived numeric or bounded P_N
- `CG3703_3_nuisance`: `BLOCKED` | alpha_nuisance proved zero or bounded by sourced eta_R10 budget
- `CG3703_4_score`: `BLOCKED` | 0.5*P_N*lambda_H^4+alpha_nuisance <= alpha_bound_R10(lambda_H) evaluated
- `CG3703_5_public`: `BLOCKED` | public R10/local-Newton claim allowed

## Source Register

- `curve_3702`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3702_R10_BOUND_CURVE_CANDIDATE.csv`
- `binder_3702`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3702_MTS_ALPHA_LAMBDA_BINDER_ROWS.csv`
- `arena_3700`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3700_ARENA_RUNNER_ROWS.csv`
- `tensor_3700`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3700_RESIDUAL_TENSOR_ROWS.csv`
- `residual_3699`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3699_RESIDUAL_BOUND_ROWS.csv`
- `doc_3700`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3700-Y5-R2FR-second-order-source-residual-vector-and-local-test-runner.md`
- `doc_3702`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3702-Y5-R2FR-R10-bound-curve-digitizer-and-MTS-alpha-lambda-binder.md`

## Next Target

- `3704-Y5-R2FR-alpha-nuisance-zero-or-budget-boundary-projection-cleanup.md`
- Objective: prove alpha_edge/alpha_proj/boundary terms vanish for the local R10 branch, or derive a sourced eta_R10 budget that leaves a finite P_N bound
