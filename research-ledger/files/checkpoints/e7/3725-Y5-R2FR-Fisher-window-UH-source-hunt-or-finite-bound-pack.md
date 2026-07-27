# 3725 — Fisher Window / U_H Source Hunt or Finite Bound Pack

## Status
- `SOURCE_HUNT_NO_CLAIM_FINITE_SCORE_GRAM_ROUTE_READY`
- The hunt found no claim-ready `Theta_min`, `iota_min`, `iota_max`, `U_H`, or correction-loss row.
- The useful advance is the score-Gram route: `I_AB=<Y_A,Y_B>_0`, so `iota_min=lambda_min(G_Y)` and `iota_max=lambda_max(G_Y)` or a trace ceiling.
- This keeps the mean branch alive without smuggling a local screening pass.

## Source Adjudication
- `ADJ3725_0_theta_min` `SYMBOLIC_ONLY` — Theta_min: 3708/3724 give Theta_H/T_eff symbols but no parent-owned positive numeric/unit lower bound. Next: derive scale from parent KL/Legendre action or keep finite row.
- `ADJ3725_1_iota_min` `FORMULA_ONLY` — iota_min: 3708 defines Fisher lower/eigenvalue language, but no coercivity proof for active score directions. Next: derive Gram lower bound or retain missing invertibility row.
- `ADJ3725_2_iota_max` `MISSING_NEW_INPUT` — iota_max: 3724 shows this is mandatory for mean branch; corpus has lambda_max patterns in other sectors but no Fisher ceiling. Next: derive score-norm ceiling Trace(I)<=Y2_max.
- `ADJ3725_3_UH` `MISSING` — U_H/u_min: No same-basis unit map from Fisher Hessian to local m^-2 operator was found. Next: construct U_H from field metric/residual projection or keep blocked.
- `ADJ3725_4_DeltaM_mean` `MISSING` — DeltaM_mean: No source-owned mismatch between response-doublet M_Z and Theta_H I^{-1} exists. Next: retain finite operator mismatch row.
- `ADJ3725_5_R_loss` `PARTIAL_SYMBOLIC` — R_loss: Domain/source/boundary loss rows exist in neighbouring branches but no mean-branch combined bound is sourced. Next: assemble R_loss from domain/source/boundary rows if available.
- `ADJ3725_6_verdict` `NOT_CLAIM_READY` — mean branch source pack: No required input is currently source-owned enough to score Xi_loc. Next: advance to finite score-Gram/U_H owner route.

## Score-Gram Route
- `GRAM3725_0_score_gram` `DERIVED_ROUTE`: `I_AB=<Y_A,Y_B>_0` | Fisher matrix is a Gram matrix of score variables in the p_0 bath inner product.
- `GRAM3725_1_ceiling_trace` `DERIVED_BOUND`: `iota_max <= Tr(I)=sum_A ||Y_A||_0^2` | finite score norms give the Fisher ceiling required by the mean branch.
- `GRAM3725_2_ceiling_uniform` `DERIVED_BOUND`: `If ||Y_A||_0 <= Y_max and dim K_act=N, then iota_max <= N Y_max^2` | coarse but sourceable ceiling when only per-component score bounds exist.
- `GRAM3725_3_floor_coercivity` `COERCIVITY_TARGET`: `iota_min = inf_{||a||=1}<a^A Y_A,a^B Y_B>_0` | invertibility requires no active response direction has zero score.
- `GRAM3725_4_finite_matrix` `RUNNER_READY_CONCEPT`: `For finite active basis, compute eigenvalues of G_Y=(<Y_A,Y_B>_0)` | turns iota_min/iota_max into an eigenvalue problem rather than vibes.

## Finite Bound Pack
- `FP3725_0_theta_min` `Theta_min`: positive lower KL/Legendre scale | MISSING_PARENT_SOURCE | impact: feeds numerator of Xi_loc
- `FP3725_1_iota_min` `iota_min`: lambda_min(G_Y) | MISSING_SCORE_GRAM | impact: needed for I^{-1} to exist
- `FP3725_2_iota_max` `iota_max`: lambda_max(G_Y) or trace ceiling | MISSING_SCORE_GRAM_OR_TRACE_BOUND | impact: controls mean-branch gap floor
- `FP3725_3_u_min` `u_min`: smallest singular/coercivity value of U_H | MISSING_UNIT_MAP | impact: maps abstract Hessian to local operator
- `FP3725_4_DeltaM_mean` `||DeltaM_mean||`: operator mismatch norm | MISSING_OPERATOR_MATCH_BOUND | impact: subtracts from gap
- `FP3725_5_R_loss` `R_loss`: R_domain+R_source+R_boundary+even correction losses | MISSING_COMBINED_LOSS_BOUND | impact: subtracts from gap
- `FP3725_6_R_U` `R_U`: unit-map/projection remainder | MISSING_UNIT_REMAINDER_BOUND | impact: subtracts after local conversion
- `FP3725_7_Xi_loc` `Xi_loc`: u_min^2*(Theta_min/iota_max-DeltaM_mean-R_loss)-R_U | BLOCKED_SYMBOLIC | impact: only scoreable when all upstream rows are finite

## Decisions
- `DEC3725_0_no_claim` `NO_MEAN_BRANCH_INPUTS_SOURCE_OWNED` | The source hunt did not find claim-ready Theta/Fisher-window/U_H/correction inputs.
- `DEC3725_1_real_progress` `FINITE_GRAM_ROUTE_SELECTED` | iota_min and iota_max can be turned into a score-Gram eigenvalue problem, which is concrete and testable.
- `DEC3725_2_ceiling_priority` `IOTA_MAX_IS_NOW_FIRST_MEAN_BRANCH_TARGET` | Without iota_max the mean-branch lower gap cannot be computed even if iota_min exists.
- `DEC3725_3_next` `ADVANCE_TO_SCORE_GRAM_COHERCIVITY_RUNNER` | Next target should define the active score basis Y_A and produce a Gram/eigenvalue schema or theorem-zero demotion.

## Claim Gates
- `CG3725_0_score_basis` `BLOCKED` | active score variables Y_A and bath inner product are parent-owned
- `CG3725_1_gram` `BLOCKED` | G_Y matrix or theorem bounds provide iota_min and iota_max
- `CG3725_2_theta` `BLOCKED` | Theta_min source-owned with units
- `CG3725_3_UH` `BLOCKED` | U_H and u_min source-owned with local units
- `CG3725_4_losses` `BLOCKED` | DeltaM_mean, R_loss, and R_U finite or theorem-zero
- `CG3725_5_Xi` `BLOCKED` | Xi_loc positive and scoreable
- `CG3725_6_claim` `BLOCKED` | local screening claim allowed

## Source Register
- `doc_3724`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3724-Y5-R2FR-mean-branch-gap-floor-unit-map-owner.md`
- `next_3724`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3724_NEXT_TARGET.csv`
- `law_3724`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3724_MEAN_GAP_LAW_ROWS.csv`
- `input_3724`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3724_REQUIRED_INPUT_ROWS.csv`
- `fisher_3708`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3708_FISHER_GAP_DERIVATION_ROWS.csv`
- `doc_3253`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3253-Y5-R2FR-parent-ordinary-sector-action-signature-or-C_Tw-component-current-norm-intake-under-AX1090.md`
- `doc_2281`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2281-Y5-R2FR-q-stiffness-parent-sector-or-no-go.md`

## Automated Hit Rows
- See `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3725_AUTOMATED_HIT_ROWS.csv`.

## Next Target
- `3726-Y5-R2FR-score-Gram-coercivity-runner-or-symbolic-window-lock.md`
- Objective: define the score basis and Gram matrix schema, or lock the Fisher window as symbolic.

## Validation
- See `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_3725_VALIDATION.csv`.
