# 4548 - Fill first epsilon_U local range row or static-bound runner smoke

Generated: `2026-07-06T10:13:19.810287+00:00`  
Marker: `PPC4161_FILL_FIRST_EPSILONU_LOCAL_RANGE_ROW_OR_STATIC_BOUND_RUNNER_SMOKE_4548`  
Decision: `EPSILON_U_LOGISTIC_RANGE_LAW_DERIVED_POINT_ANCHOR_EXTRACTED_DOMAIN_SUP_MISSING_STATIC_BOUND_SMOKE_READY_NONCLAIM`  
Claim: `L-390` remains private, conditional and nonclaim.

## What Moved

4548 does not just say "epsilon_U missing". It derives the exact range law from the existing switch:

```text
Pi_B = 1/(1 + exp[-(B_env-B_*)/Delta_B])
U_B  = 1 - Pi_B
     = 1/(1 + exp[(B_env-B_*)/Delta_B]).
```

Therefore, on any named local domain `D_loc` with `B_env(x) >= B_min` and `Delta_B>0`,

```text
epsilon_U(D_loc) := sup_Dloc U_B
                 <= 1/(1 + exp[(B_min-B_*)/Delta_B]).
```

For a far-local positive margin this gives the faster but weaker tail:

```text
epsilon_U(D_loc) <= exp[-(B_min-B_*)/Delta_B].
```

The existing Sun-1AU source-model row gives a useful point anchor, `U_B ~ 9.73e-14`, but that is not a domain supremum. The transition shell still has `U_B ~ 1/2`, so it cannot be smuggled into the far-local suppression branch.

## Range Law

| law_id | object | assumptions | derivation | result | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| LAW4548_0_exact_UB | U_B | Pi_B=(1+exp[-(B_env-B_*)/Delta_B])^-1; U_B=1-Pi_B; Delta_B>0. | U_B=1-Pi_B=(1+exp[(B_env-B_*)/Delta_B])^-1. | U_B(B_env) = 1/(1 + exp[(B_env-B_*)/Delta_B]) | derived_from_existing_logistic_switch | False |
| LAW4548_1_domain_sup | epsilon_U(D_loc) | D_loc has B_env(x)>=B_min for every x in D_loc; Delta_B>0. | U_B is monotone decreasing in B_env, so sup_Dloc U_B occurs at the smallest allowed B_env. | epsilon_U(D_loc) := sup_Dloc U_B <= 1/(1 + exp[(B_min-B_*)/Delta_B]) | derived_but_numeric_domain_inputs_missing | False |
| LAW4548_2_large_margin_tail | far-local exponential tail | B_min>B_* and Delta_B>0. | For y=(B_min-B_*)/Delta_B>0, 1/(1+e^y) <= e^-y. | epsilon_U(D_loc) <= exp[-(B_min-B_*)/Delta_B] | derived_useful_for_fast_screening_bounds | False |
| LAW4548_3_gradient_tail | gradient leakage | Delta_B>0 and \|nabla B_env\| <= 1/L_B on D_loc. | nabla U_B = -U_B(1-U_B)nabla B_env/Delta_B. | \|nabla U_B\| <= epsilon_U/(Delta_B L_B) | derived_for_static_bound_runner_inputs | False |


## Local Range Rows

| row_id | domain | range_condition | epsilon_U_candidate | numeric_value | units | source_path | extraction_method | missing_inputs | status | valid_for_claim | computed_from_logistic | B_env | B_star | Delta_B |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LR4548_0_far_local_domain_formula | Dloc_far_local := stationary compact local exterior excluding source support and excluding transition shell | B_env(x) >= B_min > B_* on the full tested domain | 1/(1 + exp[(B_min-B_*)/Delta_B]) | missing | dimensionless | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\runs\source_model_curvature_Lcg_20260527-211932\summary.csv | domain_sup_formula_not_numeric | B_min over a named local test domain; parent-owned B_*; parent-owned Delta_B; proof transition shell is excluded or separately quarantined | formula_ready_domain_sup_missing | False |  |  |  |  |
| LR4548_1_sun_1AU_point_anchor | single point anchor: source_model local_weak_field_point_mass_sun_1AU | point evaluation only, not a domain supremum | 9.7255536957163713e-14 | 9.7255536957163713e-14 | dimensionless | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\runs\source_model_curvature_Lcg_20260527-211932\summary.csv | source_model_point_anchor_not_supremum | domain supremum; real tested exterior definition; parent-owned threshold/width | numeric_point_anchor_nonclaim | False | missing | 1.5981105180940755e+01 | missing | missing |
| LR4548_2_transition_shell_warning | solar_transition_shell_point_mass | B_env approximately B_*, hence U_B approximately 1/2 | 0.5 | 0.5 | dimensionless | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\runs\source_model_curvature_Lcg_20260527-211932\summary.csv | anti_cheat_transition_warning | transition current PPN solver or routing theorem | not_usable_for_far_local_suppression_claim | False |  |  |  |  |


## Static Smoke Inputs

| input_id | symbol | meaning | candidate_source | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| SMI4548_0_epsilon_U | epsilon_U | sup_Dloc U_B | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4548_EPSILON_U_LOCAL_RANGE_ROW.csv | formula_ready_domain_sup_missing_point_anchor_available | False |
| SMI4548_1_S_static | S_static | C_H A_1 + D_m C_lap_m/L_B^2 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4547_INPUT_ACQUISITION_QUEUE.csv | symbolic_only_coefficient_products_missing | False |
| SMI4548_2_boundary | B_boundary,a | arena-specific retained static boundary/vector/shear amplitude | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4547_INPUT_ACQUISITION_QUEUE.csv | missing_zero_theorem_or_numeric_bound | False |
| SMI4548_3_kernel | K_a | arena projection kernel converting B_static to observable residual | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4547_ARENA_PROJECTION_CONTRACT.csv | missing_projection_kernel | False |


## Static Bound Smoke Runner

| smoke_id | observable | target_bound | bound_units | candidate_epsilon_source | candidate_epsilon_value | static_formula | epsilon_bound_formula | schema_status | numeric_blockers | claim_guard | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SMOKE4548_alpha3 | alpha3 | 4e-20 | dimensionless | LR4548_1_sun_1AU_point_anchor | 9.7255536957163713e-14 | \|Delta_alpha3\| <= \|K_alpha3\| * (S_static * epsilon_U^2 + B_boundary_alpha3) | epsilon_U <= sqrt((4e-20 - B_boundary_alpha3) / (K_alpha3 * (C_H A_1 + D_m C_lap_m/L_B^2))) when numerator positive. | schema_pass_numeric_blocked | domain epsilon_U sup; S_static; projection kernel; boundary amplitude | point anchor is not a domain sup; no kernels/coefficient products/boundary rows | False |
| SMOKE4548_xi | xi | 4e-09 | dimensionless | LR4548_1_sun_1AU_point_anchor | 9.7255536957163713e-14 | \|Delta_xi\| <= \|K_xi\| * (S_static * epsilon_U^2 + B_boundary_xi) | epsilon_U <= sqrt((4e-09 - B_boundary_xi) / (K_xi * (C_H A_1 + D_m C_lap_m/L_B^2))) when numerator positive. | schema_pass_numeric_blocked | domain epsilon_U sup; S_static; projection kernel; boundary amplitude | point anchor is not a domain sup; no kernels/coefficient products/boundary rows | False |
| SMOKE4548_R10_alpha_anchor | R10_alpha_anchor | 1 | dimensionless | LR4548_1_sun_1AU_point_anchor | 9.7255536957163713e-14 | \|Delta_R10_alpha_anchor\| <= \|K_R10(lambda)\| * (S_static * epsilon_U^2 + B_boundary_R10_alpha_anchor) | epsilon_U <= sqrt((1 - B_boundary_R10_alpha_anchor) / (K_R10(lambda) * (C_H A_1 + D_m C_lap_m/L_B^2))) when numerator positive. | schema_pass_numeric_blocked | domain epsilon_U sup; S_static; projection kernel; boundary amplitude | point anchor is not a domain sup; no kernels/coefficient products/boundary rows | False |
| SMOKE4548_Gdot_static_derivative | Gdot_static_derivative | 2.42e-14 | yr^-1 | LR4548_1_sun_1AU_point_anchor | 9.7255536957163713e-14 | No epsilon_U-only static amplitude pass: require theorem D_t B_static=0 or source J_Gdot^t D_t B_static bound. | not_applicable_without_time_variation_model | schema_pass_numeric_blocked | D_t B_static zero proof or time-variation kernel; boundary derivative terms | point anchor is not a domain sup; no kernels/coefficient products/boundary rows | False |


## Numeric Blockers

| blocker_id | symbol | needed_for | status | next_action | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| BLOCK4548_0_Dloc | D_loc | epsilon_U = sup_Dloc U_B | MISSING_NAMED_TEST_DOMAIN | define the exact local exterior domain for R10/PPN/clocks/orbits, with transition shell handling | False |
| BLOCK4548_1_Bmin | B_min | epsilon_U <= 1/(1+exp[(B_min-B_*)/Delta_B]) | MISSING_DOMAIN_INFIMUM | source or compute inf_Dloc B_env from the selected domain, not a single point | False |
| BLOCK4548_2_Bstar_DeltaB | B_*, Delta_B | logistic range numeric value | EXAMPLE_VALUES_ONLY_NOT_PARENT_DERIVED | derive threshold/width from parent coarse-graining law or freeze as explicit EFT inputs | False |
| BLOCK4548_3_Sstatic | S_static | B_static = S_static epsilon_U^2 + B_boundary + O(epsilon_U^3) | MISSING_COEFFICIENT_PRODUCTS | source C_H A_1 and D_m C_lap_m/L_B^2 or replace with parent zero theorem | False |
| BLOCK4548_4_Kernels | K_a | Delta O_a = K_a B_static | MISSING_ARENA_PROJECTION_KERNELS | derive or source first real PPN/R10 projection kernel row | False |
| BLOCK4548_5_Boundary | B_boundary,a | static PPN vector/shear and R10/channel residuals | MISSING_BOUNDARY_ZERO_OR_BOUND | prove boundary no-hair for retained static channels or add numeric amplitude rows | False |


## Claim Gates

| gate_id | condition | status | valid_for_claim |
| --- | --- | --- | --- |
| GATE4548_0_logistic_derivation | exact logistic epsilon_U law derived from existing Pi_B/U_B definitions | PASS | False |
| GATE4548_1_numeric_domain_sup | epsilon_U supplied as sup over named local domain | FAIL_MISSING_DOMAIN_SUP | False |
| GATE4548_2_static_runner_schema | static-bound runner rows parse for alpha3, xi, R10, and Gdot derivative caveat | PASS_SCHEMA_ONLY | False |
| GATE4548_3_no_claim_guard | no local-GR, R10, PPN, or Gdot pass claimed from point anchor/symbolic rows | PASS | False |


## Decision

| checkpoint | branch | decision | summary | claim_id | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| 4548 | MTS_R2FR_Y5_EPSILON_U_LOCAL_RANGE_AND_STATIC_SMOKE_4548 | EPSILON_U_LOGISTIC_RANGE_LAW_DERIVED_POINT_ANCHOR_EXTRACTED_DOMAIN_SUP_MISSING_STATIC_BOUND_SMOKE_READY_NONCLAIM | 4548 derives the exact epsilon_U logistic range law and extracts a source-model Sun-1AU U_B point anchor, but refuses to call it a domain supremum. The static-bound smoke runner is now executable/schema-clean and remains nonclaim until D_loc/B_min, S_static, kernels and boundary amplitudes are sourced. | L-390 | False |


## Next Target

| next_target | route | why | no_claim_guard | valid_for_claim |
| --- | --- | --- | --- | --- |
| 4549-Y5-R2FR-source-real-local-domain-Bmin-or-first-projection-kernel-row.md | best_forward_route | The next real leap is either a domain supremum B_min for epsilon_U or the first actual arena projection kernel; either turns the scorer from symbolic to numerically testable. | Do not use the Sun-1AU point anchor as a PPN/R10 pass. | False |


## Source Register

| checkpoint | source_id | label | path | exists | needle | needle_found | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4548 | SRC4548_00_var_audit_PiB | variable audit Pi_B/U_B | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\04-variable-audit.csv | True | Pi_B=1/{1+exp[-(B_env-B_*)/Delta_B]}; U_B=1-Pi_B | True | False |
| 4548 | SRC4548_01_var_audit_Benv | variable audit B_env | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\04-variable-audit.csv | True | B_env=ln(1+A_curv)-w_theta ln(1+E_theta) | True | False |
| 4548 | SRC4548_02_XB_doc_logistic | 85 X_B logistic definition | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\85-coarse-graining-invariants-XB.md | True | 1 / {1 + exp[-(B_env - B_*)/Delta_B]} | True | False |
| 4548 | SRC4548_03_XB_gate_values | 86 X_B gate rough threshold values | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\86-XB-invariant-gate.md | True | B_* = 1 | True | False |
| 4548 | SRC4548_04_source_model_logistic | 89 source model Pi_B definition | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\89-source-model-curvature-Lcg-test.md | True | 1 / {1 + exp[-(B_env - B_*) / Delta_B]} | True | False |
| 4548 | SRC4548_05_source_model_summary | source model local point anchor rows | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\runs\source_model_curvature_Lcg_20260527-211932\summary.csv | True | local_weak_field_point_mass_sun_1AU | True | False |
| 4548 | SRC4548_06_XB_summary | X_B summary screening rows | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\runs\XB_invariant_gate_20260527-204233\summary.csv | True | local_screening_target_conditional_pass | True | False |
| 4548 | SRC4548_07_trace_gate_summary | trace gate local U_B^2 row | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\runs\trace_suppression_closure_gate_20260527-214758\summary.csv | True | local_point_mass_universal_U2_pass | True | False |
| 4548 | SRC4548_08_trace_doc_caveat | trace gate parent-derived caveat | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\91-trace-suppression-closure-gate.md | True | U_B^2 is derived | True | False |
| 4548 | SRC4548_09_1975_requirements | 1975 epsilon_U requirement row | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1975_BOUND_CONSTANT_REQUIREMENTS.csv | True | epsilon_U | True | False |
| 4548 | SRC4548_10_1975_envelope | 1975 U_B suppression envelope | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1975_UB_SUPPRESSION_BOUND_ENVELOPE.csv | True | epsilon_U^2 | True | False |
| 4548 | SRC4548_11_4547_acquisition | 4547 acquisition queue | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4547_INPUT_ACQUISITION_QUEUE.csv | True | epsilon_U = sup_Dloc U_B | True | False |
| 4548 | SRC4548_12_4547_epsilon_bounds | 4547 epsilon bound rows | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4547_EPSILON_U_BOUND_ROWS.csv | True | EUB4547_alpha3 | True | False |
| 4548 | SRC4548_13_4547_projection | 4547 arena projection contract | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4547_ARENA_PROJECTION_CONTRACT.csv | True | same B_static/source profile for all arenas; no retuning | True | False |
| 4548 | SRC4548_14_4547_pass | 4547 pass inequalities | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4547_PASS_INEQUALITY_ROWS.csv | True | PI4547_alpha3 | True | False |


## Validation

| validation_id | status | detail |
| --- | --- | --- |
| VAL4548_00_sources | PASS | all source paths exist and needles found |
| VAL4548_01_logistic_law | PASS | exact U_B and domain-sup law rows present |
| VAL4548_02_local_range_nonclaim | PASS | local range keeps point anchor separate from domain sup |
| VAL4548_03_static_smoke_runner | PASS | static smoke rows include alpha3, xi, R10 and Gdot caveat; all nonclaim |
| VAL4548_04_claim_guards | PASS | claim gates do not promote local-GR/R10/PPN pass |
| VAL4548_05_csv_parse | PASS | all generated CSV files parse and have rows |
| VAL4548_06_docs_written | PASS | post and formal checkpoint docs written |
| VAL4548_07_pycache_absent | PASS | scripts __pycache__ absent after cleanup |
| VAL4548_OVERALL | PASS | 4548 epsilon_U local range law and static-bound smoke runner |

