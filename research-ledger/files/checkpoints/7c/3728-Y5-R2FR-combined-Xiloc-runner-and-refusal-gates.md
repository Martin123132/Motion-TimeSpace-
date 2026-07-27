# 3728 — Combined Xi_loc Runner and Refusal Gates

## Status
- `COMBINED_XILOC_RUNNER_READY_CURRENTLY_BLOCKED`
- Combined formula: `Xi_loc=u_min^2*(Theta_min/iota_max-DeltaM_mean-R_loss)-R_U`, with `iota_min>0` required for invertibility.
- Current runner status: `BLOCKED_MISSING_OR_NONPOSITIVE_XILOC`.
- This is a runner contract, not a local-GR/Newton/R10 claim.

## Main Result
- The mean-branch local gap is now a single product/gate object.
- Missing inputs generate refusal rows instead of silently passing.
- A future positive `Xi_loc` must still be consumed by arena response maps before any empirical statement.

## Runner
- `RUN3728_0_Xiloc` `BLOCKED_MISSING_OR_NONPOSITIVE_XILOC`: executable=False positive_gap=False missing=`Theta_min;iota_min;iota_max;u_min;DeltaM_mean;R_loss;R_U`

## Refusals
- `REF3728_missing_Theta_min` `Theta_min`: missing numeric source-owned input | fix: provide source-owned numeric Theta_min row with units and parent path
- `REF3728_missing_iota_min` `iota_min`: missing numeric source-owned input | fix: provide source-owned numeric iota_min row with units and parent path
- `REF3728_missing_iota_max` `iota_max`: missing numeric source-owned input | fix: provide source-owned numeric iota_max row with units and parent path
- `REF3728_missing_u_min` `u_min`: missing numeric source-owned input | fix: provide source-owned numeric u_min row with units and parent path
- `REF3728_missing_DeltaM_mean` `DeltaM_mean`: missing numeric source-owned input | fix: provide source-owned numeric DeltaM_mean row with units and parent path
- `REF3728_missing_R_loss` `R_loss`: missing numeric source-owned input | fix: provide source-owned numeric R_loss row with units and parent path
- `REF3728_missing_R_U` `R_U`: missing numeric source-owned input | fix: provide source-owned numeric R_U row with units and parent path

## Theorem Rows
- `THM3728_0_combined_law` `DERIVED_RUNNER_FORM`: Xi_loc=u_min^2*(Theta_min/iota_max-DeltaM_mean-R_loss)-R_U | combines 3724 mean-branch gap with 3726 Fisher window and 3727 U_H map
- `THM3728_1_invertibility_gate` `DERIVED_GATE`: iota_min>0 is required even though iota_max controls the lower mean gap | separates inverse existence from gap floor
- `THM3728_2_positive_gate` `ANTI_OVERCLAIM`: Xi_loc>0 is necessary but not sufficient for local-GR/Newton/PPN claim | local response and source coupling gates still consume the gap
- `THM3728_3_refusal_gate` `ANTI_SMUGGLING_GUARD`: Any missing/non-source-owned factor blocks scoring | prevents symbolic product from becoming a hidden pass

## Decisions
- `DEC3728_0_runner_ready` `COMBINED_XILOC_RUNNER_READY` | The full mean-branch local gap product now has one executable/refusal-safe runner contract.
- `DEC3728_1_current_blocked` `CURRENT_XILOC_BLOCKED_BY_MISSING_FACTORS` | Current inputs are placeholders, so Xi_loc remains unscoreable and no local screening claim is allowed.
- `DEC3728_2_next` `ADVANCE_TO_RESPONSE_ARENA_MAP` | Next target should map a future positive Xi_loc into R10/PPN/clock/orbit residual gates without assuming local-GR recovery.

## Claim Gates
- `CG3728_0_theta` `BLOCKED` | Theta_min numeric/source-owned
- `CG3728_1_fisher` `BLOCKED` | iota_min and iota_max numeric/source-owned from score-Gram runner
- `CG3728_2_UH` `BLOCKED` | u_min and R_U numeric/source-owned from U_H runner
- `CG3728_3_losses` `BLOCKED` | DeltaM_mean and R_loss numeric/source-owned or theorem-zero
- `CG3728_4_Xi` `BLOCKED` | Xi_loc computed positive
- `CG3728_5_arena` `BLOCKED` | positive Xi_loc mapped into R10/PPN/clock/orbit/EM residual arenas
- `CG3728_6_claim` `BLOCKED` | local-GR/Newton screening claim allowed

## Next Target
- `3729-Y5-R2FR-Xiloc-to-local-arena-response-map.md`
- Objective: write the response-map contract from future `Xi_loc` into R10/PPN/clock/orbit/EM/Newton residual arenas.
