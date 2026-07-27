# 4547 - Local static residual vector projection to PPN/Gdot/R10 or first numeric U-bound row

Generated: `2026-07-06T10:13:19.332934+00:00`  
Marker: `PPC4161_LOCAL_STATIC_RESIDUAL_VECTOR_PROJECTION_TO_PPN_GDOT_R10_OR_FIRST_NUMERIC_UBOUND_ROW_4547`  
Decision: `STATIC_RESIDUAL_PROJECTION_CONTRACT_AND_EPSILON_U_BOUND_ROWS_WRITTEN_NUMERIC_INPUTS_MISSING_NONCLAIM`  
Claim: `L-389` remains private, conditional and nonclaim.

## What Moved

4546 gave the static residual envelope:

```text
B_static := C_H A_1 epsilon_U^2
          + D_m C_lap_m epsilon_U^2/L_B^2
          + B_boundary_static
          + O(epsilon_U^3).
```

4547 turns that into arena pass rows. The shared rule is:

```text
Delta O_a = K_a B_static
```

with one shared source/profile object; no PPN/R10/Gdot retuning is allowed.

For a static channel, the generic pass inequality is:

```text
|K_a B_static| <= B_a.
```

Equivalently, if the boundary piece is separately zero/bounded:

```text
epsilon_U <= sqrt((B_a - B_boundary,a)
                  / (K_a (C_H A_1 + D_m C_lap_m/L_B^2))).
```

This is not a claim because `epsilon_U`, the coefficient products, boundary amplitudes and arena kernels are not filled. But it is now a scorer-shaped object. The tightest symbolic rows are `alpha3`, `xi`, `R10`, and the Gdot derivative caveat.

## Static Residual Vector

| vector_id | symbol | definition | source | meaning | numeric_value | units | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SV4547_0_B_static | B_static | B_static := C_H A_1 epsilon_U^2 + D_m C_lap_m epsilon_U^2/L_B^2 + B_boundary_static + O(epsilon_U^3) | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4546_STATIC_JRES_BUDGET.csv | shared local static residual envelope after 4545 derivative silence | missing | source/profile norm units before arena projection | False |
| SV4547_1_source_piece | B_src | B_src := C_H A_1 epsilon_U^2 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4546_UB2_STATIC_BOUND_THEOREM.csv | source leakage contribution from P_loc[U_B S_cg] | missing | same as B_static | False |
| SV4547_2_mL_piece | B_mL | B_mL := D_m C_lap_m epsilon_U^2/L_B^2 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4546_ML_HOMOGENEITY_BOUND.csv | spatial/laplacian attractor inhomogeneity contribution | missing | same as B_static | False |
| SV4547_3_boundary_piece | B_boundary_static | B_boundary_static := \|\|P_loc boundary_in_static\|\| | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4546_INPUT_REQUIREMENTS.csv | retained trace/shear/vector boundary amplitude after derivative silence | missing | same as B_static after projection | False |


## Arena Projection Contract

| projection_id | arena | observable | effective_product | bound | units | projection_formula | required_kernel_or_proof | shared_profile_policy | numeric_ready | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AP4547_02_xi | PPN | xi | C_Gamma_metric | 4.0000000000000002e-09 | dimensionless | Delta_xi = K_xi^scalar B_static | K_xi scalar/metric projection | same B_static/source profile for all arenas; no retuning | False | False |
| AP4547_05_alpha3 | PPN_conservation | alpha3 | C_Gamma_vector | 3.9999999999999998e-20 | dimensionless | Delta_alpha3 = K_alpha3^vec B_boundary/vector_static + K_alpha3^src B_src | K_alpha3 vector/flux projection; no scalar cancellation | same B_static/source profile for all arenas; no retuning | False | False |
| AP4547_08_zeta3 | PPN_conservation | zeta3 | C_Gamma_stress | 1e-08 | dimensionless | Delta_zeta3 = K_zeta3^stress B_static | K_zeta3 stress-conservation projection | same B_static/source profile for all arenas; no retuning | False | False |
| AP4547_10_Gdot | clock_orbital | Gdot_over_G | C_Gamma_Gdot | 2.42e-14 | yr^-1 | Delta_Gdot/G_static = J_Gdot^t D_t B_static; 4545 makes derivative channel conditionally zero, so static B_static does not by itself create Gdot. | J_Gdot^t and proof D_t B_static=0 | same B_static/source profile for all arenas; no retuning | False | False |
| AP4547_11_R10 | short_range_gravity | alpha_Yukawa_at_lambda_38p6um | C_Gamma_R10 | 1 | dimensionless | alpha_MTS(lambda) = K_R10(lambda) B_static(lambda) | K_R10(lambda) curve and B_static radial/range profile | same B_static/source profile for all arenas; no retuning | False | False |
| AP4547_14_orbit_combo | orbital | ((2+2gamma-beta)/3)-1 | C_Gamma_metric | 4.6666666666666672e-05 | dimensionless | Delta_((2+2gamma-beta)/3)-1 = K_((2+2gamma-beta)/3)-1^scalar B_static | K_((2+2gamma-beta)/3)-1 scalar/metric projection | same B_static/source profile for all arenas; no retuning | False | False |


## Pass Inequality Rows

| pass_id | observable | bound | units | pass_inequality | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| PI4547_xi | xi | 4.0000000000000002e-09 | dimensionless | \|Delta_xi\| <= 4.0000000000000002e-09 dimensionless | formula_ready_inputs_missing | False |
| PI4547_alpha3 | alpha3 | 3.9999999999999998e-20 | dimensionless | \|Delta_alpha3\| <= 3.9999999999999998e-20 dimensionless | formula_ready_inputs_missing | False |
| PI4547_zeta3 | zeta3 | 1e-08 | dimensionless | \|Delta_zeta3\| <= 1e-08 dimensionless | formula_ready_inputs_missing | False |
| PI4547_Gdot_over_G | Gdot_over_G | 2.42e-14 | yr^-1 | If D_t B_static=0, static contribution to Gdot is zero; otherwise \|J_Gdot^t D_t B_static\| <= 2.42e-14 yr^-1. | formula_ready_inputs_missing | False |
| PI4547_alpha_Yukawa_at_lambda_38p6um | alpha_Yukawa_at_lambda_38p6um | 1 | dimensionless | For every lambda in the tested curve, \|K_R10(lambda) B_static(lambda)\| <= alpha_bound(lambda); anchor alpha<=1 is smoke only. | formula_ready_inputs_missing | False |
| PI4547_2+2gamma-beta_3-1 | ((2+2gamma-beta)/3)-1 | 4.6666666666666672e-05 | dimensionless | \|Delta_((2+2gamma-beta)/3)-1\| <= 4.6666666666666672e-05 dimensionless | formula_ready_inputs_missing | False |


## Epsilon_U Bound Rows

| row_id | observable | target_bound | bound_units | kernel | epsilon_U_bound_formula | missing_inputs | note | numeric_value | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EUB4547_alpha3 | alpha3 | 4e-20 | dimensionless | K_alpha3 | epsilon_U <= sqrt((4e-20 - B_boundary_alpha3) / (K_alpha3 * (C_H A_1 + D_m C_lap_m/L_B^2))) when numerator positive. | kernel, B_boundary_channel, C_H A_1, D_m C_lap_m/L_B^2, local domain/range | hardest vector/flux PPN lock | missing | False |
| EUB4547_xi | xi | 4e-09 | dimensionless | K_xi | epsilon_U <= sqrt((4e-09 - B_boundary_xi) / (K_xi * (C_H A_1 + D_m C_lap_m/L_B^2))) when numerator positive. | kernel, B_boundary_channel, C_H A_1, D_m C_lap_m/L_B^2, local domain/range | preferred-location/static anisotropy lock | missing | False |
| EUB4547_R10_alpha_anchor | R10_alpha_anchor | 1 | dimensionless | K_R10(lambda) | epsilon_U <= sqrt((1 - B_boundary_R10_alpha_anchor) / (K_R10(lambda) * (C_H A_1 + D_m C_lap_m/L_B^2))) when numerator positive. | kernel, B_boundary_channel, C_H A_1, D_m C_lap_m/L_B^2, local domain/range | short-range fifth-force anchor only; full curve still required | missing | False |
| EUB4547_Gdot_static_derivative | Gdot_static_derivative | 2.42e-14 | yr^-1 | J_Gdot^t D_t | If D_t B_static is not theorem-zero, require \|J_Gdot^t D_t B_static\| <= 2.42e-14 yr^-1; no epsilon_U-only bound exists without a time-variation model. | kernel, B_boundary_channel, C_H A_1, D_m C_lap_m/L_B^2, local domain/range | only if static envelope drifts; 4545 aims to zero this | missing | False |


## Gdot/R10 Interface Decision

| interface_id | channel | 4547_decision | current_status | next_input | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| IF4547_0_Gdot | Gdot | static B_static does not automatically source Gdot; Gdot needs D_t B_static or derivative hair | conditionally_quiet_from_4545_but_not_full_local_GR | D_t B_static theorem-zero or numeric derivative row in yr^-1 | False |
| IF4547_1_R10 | R10 | static radial/range part of B_static can source alpha(lambda); anchor alpha<=1 is not a full curve pass | curve_kernel_missing | K_R10(lambda), B_static(lambda), alpha_bound(lambda) curve | False |
| IF4547_2_PPN | PPN | static B_static maps to scalar, vector, stress and anisotropy rows through separate kernels; alpha3 and xi are the tightest locks | projection_kernels_missing | K_alpha3, K_xi, K_zeta3, K_orbit_combo, no-cancellation policy | False |


## Input Acquisition Queue

| queue_id | input | why_first | source_or_method | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| ACQ4547_0_epsilon_U | epsilon_U = sup_Dloc U_B | sets every U_B^2 static residual scale | evaluate B_env/Pi_B on chosen local exterior domain or derive parent local-range bound | missing | False |
| ACQ4547_1_CHA1 | C_H A_1 | source leakage coefficient in B_src | parent leakage-coordinate norm plus source-map first derivative norm | missing | False |
| ACQ4547_2_mL_lap | D_m C_lap_m/L_B^2 | spatial attractor homogeneity coefficient in B_mL | D_m, far-local gradient length, laplacian regularity constants | missing | False |
| ACQ4547_3_boundary_static | B_boundary_channel | alpha3/xi can be dominated by retained boundary vector/shear pieces | theorem-zero boundary nohair certificate or numeric product row | missing | False |
| ACQ4547_4_projection_kernel | K_channel | converts B_static norm into observable residual units | shared worldtube/profile projection into PPN/R10/Gdot kernels | missing | False |


## Claim Gates

| claim_gate_id | gate | status | meaning | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| CG4547_0_projection_contract | static residual projection contract | PASS_FORMULA_NONCLAIM | B_static has been mapped to PPN/Gdot/R10 inequality rows | False | False |
| CG4547_1_numeric_bounds | epsilon_U and coefficient numeric rows | BLOCKED_INPUTS_MISSING | epsilon_U, C_H A_1, D_m C_lap_m/L_B^2, boundary_static and kernels are not filled | False | False |
| CG4547_2_R10 | R10/fifth-force pass | BLOCKED_CURVE_KERNEL_MISSING | single alpha<=1 anchor is smoke only; full lambda curve needed | False | False |
| CG4547_3_local_GR | local GR/Newton/PPN | BLOCKED_NONCLAIM_PROJECTION_STAGE | projection equations exist, but no channel has score-ready values | False | False |


## Decision

| decision_id | decision | meaning | next_action | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| DEC4547_0 | STATIC_RESIDUAL_PROJECTION_CONTRACT_AND_EPSILON_U_BOUND_ROWS_WRITTEN_NUMERIC_INPUTS_MISSING_NONCLAIM | 4547 converts the 4546 static residual envelope into arena-specific pass inequalities and epsilon_U bound formulas. This moves the branch toward actual scoring without inventing constants or retuning profiles per arena. | 4548-Y5-R2FR-fill-first-epsilonU-local-range-row-or-static-bound-runner-smoke.md | False | False |


## Next Target

| next_id | target | objective | derive_first | fallback | avoid | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| NT4547_0 | 4548-Y5-R2FR-fill-first-epsilonU-local-range-row-or-static-bound-runner-smoke.md | fill the first epsilon_U/local-range row or run a symbolic static-bound smoke runner over the projection table | derive or evaluate epsilon_U=sup_Dloc U_B on a named local exterior domain with source path | keep epsilon_U symbolic and run schema-only pass/fail smoke using ACQ4547 queue | turning alpha3/R10 anchors into claims without kernels and curve data | False |


## Status

| timestamp_utc | branch_id | checkpoint_id | result | static_projection_contract_written | pass_inequality_rows_written | epsilon_U_bound_rows_written | numeric_epsilon_U_available | projection_kernels_available | R10_curve_ready | public_local_GR_claim_allowed | next_target | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-07-06T10:13:19.148586+00:00 | MTS_R2FR_Y5_STATIC_RESIDUAL_PROJECTION_4547 | 4547 | STATIC_RESIDUAL_PROJECTION_CONTRACT_AND_EPSILON_U_BOUND_ROWS_WRITTEN_NUMERIC_INPUTS_MISSING_NONCLAIM | True | True | True | False | False | False | False | 4548-Y5-R2FR-fill-first-epsilonU-local-range-row-or-static-bound-runner-smoke.md | False | False |


## Source Register

| checkpoint | source_id | label | path | exists | needle | needle_found | role | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4547 | SRC4547_00_4546_status | 4546 status | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4546_STATUS.csv | True | STATIC_SOURCE_AND_ML_HOMOGENEITY_EXACT_ZERO_CONDITIONAL_UB2_BOUND_IMPORTED_ACTIVE_NONCLAIM | True | imports current static residual state | False |
| 4547 | SRC4547_01_4546_static_budget | 4546 static Jres budget | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4546_STATIC_JRES_BUDGET.csv | True | SJ4546_0_static_budget | True | defines the shared B_static envelope | False |
| 4547 | SRC4547_02_4546_requirements | 4546 input requirements | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4546_INPUT_REQUIREMENTS.csv | True | REQ4546_4_worldtube_profile | True | keeps shared source profile/no-retuning requirement | False |
| 4547 | SRC4547_03_4188_runner | 4188 product-bound runner | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4188_CGAMMA_PRODUCT_BOUND_RUNNER.csv | True | RUN4188_B4173_11_R10 | True | imports PPN/Gdot/R10 local threshold rows | False |
| 4547 | SRC4547_04_4542_strictest | 4542 strictest cGamma bounds | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4542_STRICTEST_CGAMMA_PRODUCT_BOUNDS.csv | True | B4542_CGamma_vector | True | imports strict alpha3/xi/Gdot/R10 locks | False |
| 4547 | SRC4547_05_template | local residual prediction template | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\MTS_local_residual_predictions_TEMPLATE.csv | True | R10_fifth_force | True | maps residual vector rows to local observables | False |
| 4547 | SRC4547_06_alpha3_template | alpha3 numeric template | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_ALPHA3_NUMERIC_PRODUCT_INPUT_TEMPLATE.csv | True | A3_BOUNDARY_NUMERIC_OR_ZERO | True | keeps ultratight alpha3 row as individual channel gate | False |
| 4547 | SRC4547_07_constant_GM_gate | constant GM derivative/range gate | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_CONSTANT_GM_DERIVATIVE_HAIR_GATE.csv | True | CGM4_range_dependence | True | separates Gdot time drift from radial/range/R10 hair | False |
| 4547 | SRC4547_08_worldtube_gate | 2224 worldtube profile gate | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2224_WORLDTUBE_PROFILE_GATE.csv | True | one compact profile should feed all local arenas | True | forbids per-arena source-profile retuning | False |
| 4547 | SRC4547_09_4546_UB2 | 4546 U_B2 theorem | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4546_UB2_STATIC_BOUND_THEOREM.csv | True | UB24546_1_linear_silence | True | imports U_B2 source leakage formula | False |


## Validation

| validation_id | status | detail |
| --- | --- | --- |
| VAL4547_00_sources | PASS | all source paths exist and needles found |
| VAL4547_01_static_vector | PASS | shared B_static envelope is defined |
| VAL4547_02_projection_rows | PASS | PPN/Gdot/R10 projection rows are present |
| VAL4547_03_pass_inequalities | PASS | R10 curve and Gdot lock inequalities are explicit |
| VAL4547_04_epsilon_bounds | PASS | epsilon_U bound formulas include alpha3 and Gdot caveat |
| VAL4547_05_interfaces | PASS | R10 interface keeps curve requirement |
| VAL4547_06_acquisition_queue | PASS | first numeric acquisition queue is explicit and nonclaim |
| VAL4547_07_claim_firewall | PASS | no local GR/Newton/PPN claim from projection table |
| VAL4547_08_csv_parse | PASS | all generated CSV files parse and have rows |
| VAL4547_09_pycache_absent | PASS | scripts __pycache__ absent after cleanup |
| VAL4547_OVERALL | PASS | 4547 static residual projection and epsilon_U bound rows |

