# 3723 — Natural vs Mean Coordinate Operator Match Owner

## Status
- `MEAN_COORDINATE_DEFAULT_SELECTED_NONCLAIM_NATURAL_BRANCH_RETAINED`
- 3708 z becomes `eta` here: it is the natural/exponential-family parameter.
- Response-doublet `Z=(R_+-R_-)/2` defaults to the mean/residual coordinate `m`, so the default operator is `Theta_H I^{-1}`.
- `Theta_H I` is retained only if `Z=eta` is parent-signed.

## Main Result
- Natural-to-mean map: `m_A=partial_A W=I_AB eta^B+O(eta^2)`.
- If `Z=eta`, then `M_Z=Theta_H I`.
- If `Z=m`, then `M_Z=Theta_H I^{-1}`.
- Current corpus leans to `Z=m` because response-doublet `Z` is written as a local residual amplitude, but this remains nonclaim until the parent signs the coordinate type.

## Notation Reset
- `NOT3723_0_eta` `eta^A`: natural/exponential-family source parameter | p_eta=p_0 exp[eta^A Y_A-W(eta)]
- `NOT3723_1_m` `m_A`: mean/response coordinate | m_A=E_eta[Y_A]-E_0[Y_A]=partial_A W(eta)
- `NOT3723_2_Z` `Z^A`: response-doublet physical residual coordinate | Z^A=(R_+^A-R_-^A)/2
- `NOT3723_3_local_map` `Z=L_m m or Z=L_eta eta`: coordinate owner map | must be parent-signed before choosing I or I^{-1}

## Evidence
- `EVID3723_0_3708_eta` `SUPPORTS_NATURAL_PARAMETER_FOR_3708_Z`: 3708 uses p_z=p_0 exp[zY-W] | This is natural-parameter form; rename that coordinate eta to avoid confusion.
- `EVID3723_1_517_Z` `SUPPORTS_MEAN_DEFAULT_FOR_RESPONSE_Z`: 517 defines Z=(R_+-R_-)/2 as a residual doublet coordinate | This looks like a physical/mean residual amplitude, not a conjugate source multiplier.
- `EVID3723_2_contract_lock` `SUPPORTS_MEAN_DEFAULT_BUT_UNSIGNED`: 516 requires Z^A=Y_loc^A through PPN/local order | If Z is locked to local observable residuals, mean-coordinate interpretation is the less smuggly default.
- `EVID3723_3_no_parent_choice` `CLAIM_BLOCKER`: No current row proves Z=eta rather than Z=m or Z=L eta | Therefore no local screening claim can use either Hessian branch without a retained mismatch.

## Coordinate Theorems
- `CTH3723_0_eta_to_m` `DERIVED`: `m_A=partial_A W(eta)=I_AB eta^B+O(eta^2)` | local mean and natural coordinates are related by the Fisher matrix
- `CTH3723_1_natural_operator` `CONDITIONAL_BRANCH`: `If Z=eta, then Psi=0.5 Theta_H I_AB Z^A Z^B+O(Z^3)` | M_Z=Theta_H I
- `CTH3723_2_mean_operator` `CONDITIONAL_BRANCH_SELECTED_AS_DEFAULT`: `If Z=m, then Psi=Theta_H W_star(Z)=0.5 Theta_H (I^{-1})^{AB} Z_A Z_B+O(Z^3)` | M_Z=Theta_H I^{-1}
- `CTH3723_3_general_map` `DERIVED_BOUND_BRANCH`: `If Z=L eta+O(eta^2), then M_Z=Theta_H L^{-T} I L^{-1}` | keeps arbitrary coordinate maps explicit
- `CTH3723_4_default_rule` `DEFAULT_SELECTION_NONCLAIM`: `Because response-doublet Z is written as residual amplitude, default internal route is mean branch unless parent signs Z=eta` | this is a discipline rule, not a claim

## Operator Pack
- `PACK3723_0_default_mean` `M_Z,default`: `Theta_H I^{-1} + DeltaM_mean` | DEFAULT_NONCLAIM
- `PACK3723_1_natural_alt` `M_Z,natural`: `Theta_H I + DeltaM_nat` | ALTERNATE_BRANCH_BLOCKED
- `PACK3723_2_general` `M_Z,general`: `Theta_H L^{-T} I L^{-1}+DeltaM_L` | GENERAL_BOUND_BRANCH
- `PACK3723_3_gap_default` `Xi_H,default`: `lambda_min(Theta_H I^{-1})-||DeltaM_mean||-R_loss` | BOUND_FORM_NONCLAIM
- `PACK3723_4_gap_guard` `no_claim_guard`: `do not use lambda_min(Theta_H I) for response Z unless Z=eta` | ACTIVE_GUARD

## Decisions
- `DEC3723_0_notation_reset` `RENAME_3708_Z_TO_ETA_IN_THIS_BRANCH` | The exponential-family coordinate is natural parameter eta; response-doublet Z should not inherit that name silently.
- `DEC3723_1_default_mean` `MEAN_COORDINATE_DEFAULT_SELECTED_NONCLAIM` | Response-doublet Z is a residual amplitude, so the least-smuggly internal default is Z=m and M=Theta I^{-1}.
- `DEC3723_2_natural_not_rejected` `NATURAL_BRANCH_RETAINED_IF_PARENT_SIGNS_Z_EQUALS_ETA` | If later parent text proves Z is a conjugate bath-source parameter, switch to M=Theta I.
- `DEC3723_3_next` `ADVANCE_TO_MEAN_BRANCH_GAP_FLOOR_AND_UNIT_MAP_OWNER` | Next target should source-own I^{-1}, Theta_H, U_H, and DeltaM_mean or keep the default branch nonclaim.

## Claim Gates
- `CG3723_0_coordinate_type` `BLOCKED` | Z=m default or Z=eta alternative is parent-signed
- `CG3723_1_I_inverse` `BLOCKED` | I is positive/invertible on active quotient-fibre subspace
- `CG3723_2_theta` `BLOCKED` | Theta_H positive and unit-owned
- `CG3723_3_UH` `BLOCKED` | U_H maps M_Z to local m^-2/operator units
- `CG3723_4_DeltaM` `BLOCKED` | DeltaM_mean/natural/general is theorem-zero or bounded
- `CG3723_5_boundary` `BLOCKED` | R_loss/F_loss/QK_loss are closed or finite
- `CG3723_6_claim` `BLOCKED` | local gap/screening claim allowed

## Source Register
- `doc_3722`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3722-Y5-R2FR-KL-Legendre-effective-action-sign-owner-or-free-energy-demotion.md`
- `next_3722`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3722_NEXT_TARGET.csv`
- `coord_3722`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3722_COORDINATE_CHOICE_ROWS.csv`
- `opm_3722`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3722_OPERATOR_MATCH_ROWS.csv`
- `kll_3722`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3722_KL_LEGENDRE_THEOREM_ROWS.csv`
- `fisher_3708`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3708_FISHER_GAP_DERIVATION_ROWS.csv`
- `doublet_517`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_RESPONSE_DOUBLET_ACTION_VARIATION.csv`
- `doublet_contract_516`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_RESPONSE_DOUBLET_ACTION_CONTRACT.csv`

## Next Target
- `3724-Y5-R2FR-mean-branch-gap-floor-unit-map-owner.md`
- Objective: source-own or bound the mean-branch gap floor and unit map.

## Validation
- See `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_3723_VALIDATION.csv`.
