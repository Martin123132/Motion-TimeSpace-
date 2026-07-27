# 3722 — KL/Legendre Effective Action Sign Owner or Free-Energy Demotion

## Status
- `KL_LEGENDRE_SIGN_DERIVED_RAW_FREE_ENERGY_DEMOTED_COORDINATE_FORK_OPEN`
- Positive sign is valid for `Psi_KL=Theta_H D_KL` or the Legendre dual, if the parent action owns that effective action and `Theta_H>0`.
- Raw `-Theta log Z` is demoted as a gap source unless a separate convexity theorem is supplied.
- New fork: if `Z` is a natural bath coordinate then `M=Theta I`; if `Z` is a mean/response coordinate then `M=Theta I^{-1}`.

## Main Result
- Exponential-family route: `D_KL(p_z||p_0)=0.5 I_AB z^A z^B+O(z^3)` gives a positive Hessian in natural coordinates.
- Legendre route: `W_star(m)=sup_z(z*m-W)` gives Hessian `I^{-1}` in mean coordinates.
- Raw free-energy route: `partial_AB F_raw=<A_AB>-(1/Theta)Cov(A_A,A_B)`, so it is not automatically a stable local gap.
- Therefore the local operator match cannot be claimed until the theory chooses natural, mean, or mixed coordinate geometry.

## KL/Legendre Theorems
- `KLL3722_0_exponential_family` `THEOREM_TEMPLATE`: `p_z=p_0 exp[z^A Y_A-W(z)] with W(z)=log E_0 exp[z^A Y_A]` | normalization makes W the cumulant generator
- `KLL3722_1_zero_score` `DERIVED`: `If E_0[Y_A]=0, then partial_A W|0=0 and I_AB=partial_A partial_B W|0=E_0[Y_A Y_B]` | Fisher matrix is positive semidefinite
- `KLL3722_2_natural_KL` `DERIVED`: `D_KL(p_z||p_0)=z^A partial_A W-W=0.5 I_AB z^A z^B+O(z^3)` | natural-parameter coordinate has Hessian I_AB
- `KLL3722_3_mean_legendre` `DERIVED_IF_I_INVERTIBLE`: `m_A:=partial_A W; W_star(m)=sup_z[z^A m_A-W(z)]` | mean-response coordinate has Hessian partial_m partial_m W_star|0=I^{-1} on identifiable subspace
- `KLL3722_4_positive_action` `DERIVED_CONDITIONAL`: `Psi_KL=Theta_H D_KL or Theta_H W_star is positive if Theta_H>0 and I has a positive floor` | this is the legitimate sign-owner route
- `KLL3722_5_parent_owner_clause` `REQUIRED_BEFORE_CLAIM`: `Parent action must contain the information-projection/Legendre penalty as an effective action term, not merely a raw partition function` | prevents importing entropy sign by notation

## Raw Free-Energy Audit
- `RAW3722_0_raw_partition` `NOT_A_GAP_SOURCE_BY_ITSELF`: `F_raw(z)=-Theta log integral exp[-A(z,xi)/Theta] dmu` | not equivalent to Theta D_KL unless the variational/Legendre construction is supplied
- `RAW3722_1_hessian` `SIGN_INDEFINITE`: `partial_AB F_raw=<A_AB>-(1/Theta)Cov(A_A,A_B)` | covariance term has the sign opposite to a naive positive stiffness
- `RAW3722_2_dominance_condition` `MISSING_DOMINANCE_THEOREM`: `<A_AB> must dominate (1/Theta)Cov(A_A,A_B) for raw F to be convex` | this would be a separate parent theorem, not automatic Fisher positivity
- `RAW3722_3_demote_if_no_owner` `DEMOTION_RULE`: `If parent only owns raw F_raw and not Psi_KL/Legendre convexity, keep M_AB independent` | prevents false local screening gap

## Coordinate Choice
- `COORD3722_0_natural_branch` `UNSIGNED_BRANCH`: Z=z natural parameter -> M_AB should match Theta_H I_AB plus DeltaM_map | best if response doublet changes the bath weights/sources directly
- `COORD3722_1_mean_branch` `UNSIGNED_BRANCH`: Z=m=E_z[Y]-E_0[Y] mean response -> M_AB should match Theta_H (I^{-1})_AB plus DeltaM_map | best if response doublet is the observed/mean residual amplitude
- `COORD3722_2_mixed_branch` `FINITE_MAP_ROW_REQUIRED`: Z=L z + O(z^2) -> M_Z=Theta_H L^{-T} I L^{-1} plus correction terms | most general local coordinate map; needs Jacobian L and units
- `COORD3722_3_no_choice_no_claim` `ACTIVE_GUARD`: coordinate type unresolved -> both M=Theta I and M=Theta I^{-1} are unsafe as claims | forces M_AB to remain independent nonclaim coefficient

## Operator Matches
- `OPM3722_0_natural_bound` `natural`: DeltaM_nat:=M_AB-Theta_H I_AB | Xi_H >= lambda_min(Theta_H I)-||DeltaM_nat||-R_loss
- `OPM3722_1_mean_bound` `mean`: DeltaM_mean:=M_AB-Theta_H I^{-1}_AB | Xi_H >= lambda_min(Theta_H I^{-1})-||DeltaM_mean||-R_loss
- `OPM3722_2_general_jacobian` `mixed`: DeltaM_L:=M_Z-Theta_H L^{-T} I L^{-1} | Xi_H >= lambda_min(Theta_H L^{-T} I L^{-1})-||DeltaM_L||-R_loss
- `OPM3722_3_response_gap` `independent`: M_AB remains parent response-doublet coefficient | Xi_H >= lambda_min(M_AB)-R_loss if M_AB positive is separately proved

## Demotion Rules
- `DEM3722_0_KL_owner_missing` `NONCLAIM_DEMOTION_RULE`: Parent variational principle does not explicitly own Psi_KL or W_star -> Do not use Fisher positivity as local screening evidence; retain M_AB.
- `DEM3722_1_coordinate_missing` `NONCLAIM_DEMOTION_RULE`: Natural vs mean coordinate not selected -> Do not choose M=Theta I or M=Theta I^{-1}; retain coordinate-map residual DeltaM_L.
- `DEM3722_2_units_missing` `NONCLAIM_DEMOTION_RULE`: Theta_H, I_H, G_H/U_H units not locked -> Do not compare Xi_H to R10/PPN/clock/orbit scales.
- `DEM3722_3_boundary_missing` `NONCLAIM_DEMOTION_RULE`: J_Z/B_Z and boundary corrections not theorem-zero -> Keep F_loss/QK_loss/R_loss active.

## Decisions
- `DEC3722_0_sign_route` `KL_LEGENDRE_SIGN_ROUTE_IS_VALID_CONDITIONAL` | The positive sign is mathematically clean for Theta_H D_KL or the Legendre dual, assuming Theta_H>0 and identifiable Fisher directions.
- `DEC3722_1_raw_route` `RAW_FREE_ENERGY_ROUTE_DEMOTED` | Raw -Theta log Z is sign-indefinite unless a separate convexity/dominance theorem is supplied.
- `DEC3722_2_coordinate_fork` `NATURAL_VS_MEAN_COORDINATE_IS_NOW_THE_MAIN_FORK` | Response-doublet Z may be a natural bath-source coordinate or a mean residual coordinate, changing M from Theta I to Theta I^{-1}.
- `DEC3722_3_next` `ADVANCE_TO_COORDINATE_TYPE_AND_OPERATOR_MATCH_OWNER` | Next target should decide whether Z is natural, mean, or mixed, then write the correct M_AB match and retained mismatch row.

## Claim Gates
- `CG3722_0_KL_owner` `BLOCKED` | parent action owns Psi_KL=Theta_H D_KL or W_star
- `CG3722_1_theta` `BLOCKED` | Theta_H positive and unit-normalized
- `CG3722_2_coordinate` `BLOCKED` | Z coordinate type is natural, mean, or mixed with Jacobian
- `CG3722_3_operator` `BLOCKED` | M_AB match uses the correct I/I^{-1}/Jacobian branch
- `CG3722_4_identifiability` `BLOCKED` | Fisher floor positive on active local subspace
- `CG3722_5_boundary` `BLOCKED` | boundary/source correction budget closed or finite
- `CG3722_6_claim` `BLOCKED` | local gap/screening claim allowed

## Source Register
- `doc_3721`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3721-Y5-R2FR-response-doublet-to-Gibbs-bath-parity-map-or-demotion.md`
- `next_3721`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3721_NEXT_TARGET.csv`
- `theorem_3721`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3721_BRIDGE_THEOREM_ROWS.csv`
- `audit_3721`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3721_CURRENT_BRIDGE_AUDIT_ROWS.csv`
- `coeff_3721`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3721_RETAINED_COEFFICIENT_ROWS.csv`
- `fisher_3708`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3708_FISHER_GAP_DERIVATION_ROWS.csv`
- `doublet_517`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_RESPONSE_DOUBLET_ACTION_VARIATION.csv`

## Next Target
- `3723-Y5-R2FR-natural-vs-mean-coordinate-operator-match-owner.md`
- Objective: choose or bound the coordinate type before using the Fisher gap in local screening.

## Validation
- See `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_3722_VALIDATION.csv`.
