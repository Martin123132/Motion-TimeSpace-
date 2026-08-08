# 3724 — Mean-Branch Gap Floor and Unit Map Owner

## Status
- `MEAN_GAP_LAW_DERIVED_FISHER_CEILING_AND_UNIT_MAP_REQUIRED`
- Corrected mean-branch bound: `Xi_loc >= u_min^2*(Theta_min/iota_max-||DeltaM_mean||-R_loss)-R_U`.
- New discipline point: the mean branch needs a Fisher ceiling `iota_max`; `iota_min` gives invertibility but not the lower gap floor.
- No local screening claim follows until `Theta_H`, the Fisher eigenvalue window, `U_H`, and correction losses are parent-owned or bounded.

## Main Result
- For `M_Z=Theta_H I_H^{-1}`, `lambda_min(I_H^{-1})=1/lambda_max(I_H)`.
- Therefore the abstract mean gap is bounded by `Theta_min/iota_max`, not by `Theta_min/iota_min`.
- The local operator gap additionally needs unit-map coercivity: `U_H` contributes `u_min^2` and remainder `R_U`.

## Mean Gap Laws
- `MGL3724_0_active_subspace` `DOMAIN_CLAUSE`: `Work on active fibre subspace K_act after exact nulls/gauge directions are quotiented.` | required before I^{-1} exists
- `MGL3724_1_fisher_window` `DERIVED_REQUIREMENT`: `0 < iota_min <= lambda_min(I_H|K_act) and lambda_max(I_H|K_act) <= iota_max < infinity` | iota_min gives invertibility; iota_max gives a lower floor for I^{-1}
- `MGL3724_2_inverse_floor` `DERIVED_EXACT`: `lambda_min(I_H^{-1}|K_act)=1/lambda_max(I_H|K_act) >= 1/iota_max` | mean branch needs Fisher ceiling, not only Fisher floor
- `MGL3724_3_core_gap` `DERIVED_BOUND`: `lambda_min(Theta_H I_H^{-1}) >= Theta_min/iota_max if Theta_H>=Theta_min>0` | core mean-branch gap floor
- `MGL3724_4_correction_gap` `DERIVED_BOUND`: `lambda_min(M_Z,total) >= Theta_min/iota_max - ||DeltaM_mean|| - R_loss` | Weyl-safe correction bound before unit conversion
- `MGL3724_5_local_unit_gap` `DERIVED_BOUND`: `Xi_loc >= u_min^2*(Theta_min/iota_max - ||DeltaM_mean|| - R_loss) - R_U` | local m^-2/operator gap after U_H with coercivity u_min and unit-map remainder R_U

## Required Inputs
- `IN3724_0_theta_min` `Theta_min`: lower bound of positive KL/Legendre scale | action/operator scale | MISSING_PARENT_VALUE
- `IN3724_1_iota_min` `iota_min`: positive lower Fisher eigenvalue on K_act | score^2 units | MISSING_INVERTIBILITY_FLOOR
- `IN3724_2_iota_max` `iota_max`: finite upper Fisher eigenvalue on K_act | score^2 units | MISSING_FISHER_CEILING
- `IN3724_3_UH_umin` `u_min`: coercivity/smallest singular value of U_H local unit map | basis-to-local operator conversion | MISSING_UNIT_MAP_COERCIVITY
- `IN3724_4_DeltaM_mean` `||DeltaM_mean||`: operator mismatch between response doublet M_Z and Theta_H I^{-1} | same basis as M_Z | MISSING_MISMATCH_BOUND
- `IN3724_5_R_loss` `R_loss`: domain/source/boundary/even-correction loss | same basis as M_Z | MISSING_CORRECTION_BOUND
- `IN3724_6_R_U` `R_U`: unit-map remainder from non-isometric/projection conversion | local operator units | MISSING_UNIT_REMAINDER
- `IN3724_7_Xi_loc` `Xi_loc`: u_min^2*(Theta_min/iota_max-||DeltaM_mean||-R_loss)-R_U | m^-2/local operator units | SYMBOLIC_DERIVED_NOT_NUMERIC

## Correction Rows
- `COR3724_0_DeltaM_mean` `DeltaM_mean`: M_Z,total - Theta_H I^{-1} | operator mismatch; must be zero or bounded
- `COR3724_1_R_domain` `R_domain`: loss from finite local domain and gauge/null quotient | can reduce gap or spoil invertibility
- `COR3724_2_R_source` `R_source`: source-current or slope loss in active local branch | prevents treating bath stiffness as source-free
- `COR3724_3_R_boundary` `R_boundary`: boundary/symplectic/local collar remainder | same boundary debt as earlier F_loss/QK_loss
- `COR3724_4_R_U` `R_U`: unit-map/projection remainder | converts abstract Hessian to observed local operator

## Decisions
- `DEC3724_0_ceiling_needed` `FISHER_CEILING_ADDED_TO_MEAN_BRANCH` | For M=Theta I^{-1}, the smallest local gap is controlled by lambda_max(I), so iota_max is mandatory.
- `DEC3724_1_floor_still_needed` `FISHER_FLOOR_STILL_REQUIRED_FOR_INVERTIBILITY` | iota_min remains required so I^{-1} exists on the active subspace, but it is not the mean-branch gap floor.
- `DEC3724_2_unit_map_is_live` `UNIT_MAP_COERCIVITY_IS_A_REAL_GATE` | Even a positive abstract Hessian is not a local R10/PPN operator until U_H and its units are owned.
- `DEC3724_3_next` `ADVANCE_TO_FISHER_WINDOW_AND_UH_SOURCE_HUNT` | Next target should try to source-own theta_min, iota_min, iota_max, U_H, and correction losses from the parent corpus.

## Claim Gates
- `CG3724_0_Kact` `BLOCKED` | active fibre subspace K_act is parent-defined after null/gauge quotient
- `CG3724_1_I_window` `BLOCKED` | 0<iota_min and finite iota_max are parent-owned
- `CG3724_2_theta` `BLOCKED` | Theta_min positive with units
- `CG3724_3_UH` `BLOCKED` | U_H local unit map has coercivity u_min and units
- `CG3724_4_corrections` `BLOCKED` | DeltaM_mean, R_loss, and R_U are zero or finite sourced
- `CG3724_5_Xi_positive` `BLOCKED` | Xi_loc>0 in m^-2/local operator units
- `CG3724_6_claim` `BLOCKED` | mean-branch local screening claim allowed

## Source Register
- `doc_3723`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3723-Y5-R2FR-natural-vs-mean-coordinate-operator-match-owner.md`
- `next_3723`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3723_NEXT_TARGET.csv`
- `pack_3723`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3723_OPERATOR_PACK_ROWS.csv`
- `gates_3723`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3723_CLAIM_GATES.csv`
- `kll_3722`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3722_KL_LEGENDRE_THEOREM_ROWS.csv`
- `fisher_3708`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3708_FISHER_GAP_DERIVATION_ROWS.csv`

## Next Target
- `3725-Y5-R2FR-Fisher-window-UH-source-hunt-or-finite-bound-pack.md`
- Objective: source-own or explicitly retain `theta_min`, `iota_min`, `iota_max`, `u_min`, `DeltaM_mean`, `R_loss`, and `R_U`.

## Validation
- See `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_3724_VALIDATION.csv`.
