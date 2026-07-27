# 3726 — Score-Gram Coercivity Runner or Symbolic Window Lock

## Status
- `SCORE_GRAM_SCHEMA_READY_CURRENT_WINDOW_SYMBOLIC`
- This checkpoint installs a finite score-Gram schema for `G_Y=<Y_A,Y_B>_0` and runner logic for `iota_min/iota_max`.
- Current runner status: `BLOCKED_SYMBOLIC_WINDOW` because placeholder score/matrix rows are not parent-owned.
- No local screening claim is allowed from placeholder Gram rows.

## Main Result
- If a real finite active score basis is supplied, the runner computes the Fisher eigenvalue window.
- `iota_min=lambda_min(G_Y)` gives invertibility for the mean branch.
- `iota_max=lambda_max(G_Y)` supplies the Fisher ceiling required by the `Theta_min/iota_max` gap law.
- If matrix rows are missing, nonsymmetric, or non-positive, the window remains symbolic.

## Theorem Rows
- `THM3726_0_finite_gram` `DERIVED_SCHEMA`: Given finite active score basis Y_A and bath inner product <.,.>_0, define G_Y,AB=<Y_A,Y_B>_0. | finite Fisher matrix is a Gram matrix
- `THM3726_1_eigen_window` `DERIVED_SCHEMA`: If G_Y is symmetric positive definite, iota_min=lambda_min(G_Y), iota_max=lambda_max(G_Y). | gives invertibility and mean-branch Fisher ceiling
- `THM3726_2_trace_ceiling` `DERIVED_BOUND`: iota_max <= Tr(G_Y)=sum_A ||Y_A||_0^2. | safe ceiling if exact eigenvalue runner is unavailable
- `THM3726_3_mean_gap_feed` `DERIVED_LINK`: Xi_loc <=/>= uses iota_max in denominator: Xi_loc >= u_min^2*(Theta_min/iota_max-DeltaM-R_loss)-R_U. | Gram window feeds 3724 gap law
- `THM3726_4_refusal` `ANTI_SMUGGLING_GUARD`: If any score, inner product, matrix value, symmetry, or positivity clause is missing, Fisher window stays symbolic. | no local screening promotion from placeholders

## Runner Status
- `RUN3726_0_score_gram` `BLOCKED_SYMBOLIC_WINDOW`: executable=False symmetry_ok=False positive_definite=False missing=`Y0:Y0;Y0:Y1;Y1:Y0;Y1:Y1`

## Decisions
- `DEC3726_0_runner_schema_ready` `SCORE_GRAM_RUNNER_SCHEMA_READY` | Future real score matrices can now produce iota_min/iota_max without changing the theory contract.
- `DEC3726_1_current_blocked` `CURRENT_WINDOW_LOCKED_SYMBOLIC` | The generated template contains placeholders, so no mean-branch gap value or screening claim is allowed.
- `DEC3726_2_next` `ADVANCE_TO_UH_UNIT_MAP_SCHEMA` | Once the Fisher window has a runner shell, the next orthogonal missing piece is U_H/local operator unit conversion.

## Claim Gates
- `CG3726_0_score_basis` `BLOCKED` | all active score functions Y_A parent-owned
- `CG3726_1_inner_product` `BLOCKED` | bath measure/inner product <.,.>_0 source-owned
- `CG3726_2_matrix` `BLOCKED` | G_Y matrix entries numeric and parent-owned
- `CG3726_3_spd` `BLOCKED` | G_Y symmetric positive definite on active subspace
- `CG3726_4_window` `BLOCKED` | iota_min/iota_max computed or theorem-bounded
- `CG3726_5_local_gap` `BLOCKED` | Fisher window inserted into Xi_loc with U_H and losses
- `CG3726_6_claim` `BLOCKED` | local screening claim allowed

## Output Files
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3726_SCORE_BASIS_TEMPLATE.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3726_GRAM_MATRIX_TEMPLATE.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3726_GRAM_RUNNER_STATUS.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_3726_VALIDATION.csv`

## Next Target
- `3727-Y5-R2FR-UH-local-unit-map-schema-or-symbolic-operator-lock.md`
- Objective: define the local unit/operator map `U_H`, coercivity `u_min`, and unit remainder `R_U`.
