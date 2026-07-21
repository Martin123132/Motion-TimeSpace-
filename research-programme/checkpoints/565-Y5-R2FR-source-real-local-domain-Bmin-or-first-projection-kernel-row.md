# 4549 - Source real local-domain B_min or first projection-kernel row

Generated: `2026-07-06T10:13:20.350128+00:00`  
Marker: `PPC4161_SOURCE_REAL_LOCAL_DOMAIN_BMIN_OR_FIRST_PROJECTION_KERNEL_ROW_4549`  
Decision: `POINT_MASS_DOMAIN_BMIN_EPSILONU_ROWS_DERIVED_SOURCE_MODEL_NUMERIC_NONCLAIM_KERNELS_AND_COEFFICIENTS_STILL_MISSING`  
Claim: `L-391` remains private, conditional and nonclaim.

## What Moved

4548 derived the range law but only had a single Sun-1AU point anchor. 4549 turns that into actual finite source-model domain rows.

For the existing point-mass source model:

```text
C_abs = sqrt(48) G M_sun/(c^2 r^3)
K_B   = w_C C_abs + eta_H H_bg^2/c^2
G_K   = |d_r ln K_B|
L_cg  = (L_H^-2 + alpha_K G_K^2)^(-1/2)
A_curv = c L_cg w_C C_abs / H_bg
B_env = ln(1 + A_curv)
U_B   = 1/(1 + exp[(B_env-B_*)/Delta_B]).
```

If `B_env(r)` is monotone decreasing on `[r_in,r_out]`, then the domain infimum is the endpoint:

```text
B_min = B_env(r_out),  epsilon_U([r_in,r_out]) = U_B(r_out).
```

The first useful row is `D4549_0_inner_solar_1_to_30_AU`:

```text
r_out = 3.0000000000000000e+01 AU
B_min = 9.1788135114056022e+00
epsilon_U = 7.8699652128477737e-08
epsilon_U^2 = 6.1936352451434104e-15
```

That is real movement: `epsilon_U` is no longer only a missing symbol for this source-model domain. It is still not a PPN/R10/local-GR pass because `S_static`, `K_a`, and retained boundary amplitudes are not supplied.

## Point-Mass Domain Law

| law_id | object | assumptions | law | result | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| LAW4549_0_point_mass_source_model | Solar point-mass B_env(r) | Schwarzschild-vacuum proxy, E_theta=0, source model 89, default universal parameters b_*=1 and Delta_B=0.5. | C_abs=sqrt(48)GM/(c^2 r^3); K_B=w_C C_abs+eta_H H_bg^2/c^2; G_K=\|d_r ln K_B\|; L_cg=(L_H^-2+alpha_K G_K^2)^-1/2; A_curv=c L_cg w_C C_abs/H_bg; B_env=ln(1+A_curv). | If B_env is monotone non-increasing on [r_in,r_out], then B_min=B_env(r_out). | derived_from_existing_source_model | False |
| LAW4549_1_domain_epsilon | epsilon_U([r_in,r_out]) | B_env monotone non-increasing; r_out remains inside the quarantined transition radius. | epsilon_U = sup U_B = U_B(B_min) = 1/(1+exp[(B_min-B_*)/Delta_B]). | A named source-model domain now has numeric B_min and epsilon_U, but this is still a source-model row rather than a full PPN/R10 claim. | numeric_domain_row_ready_nonclaim | False |
| LAW4549_2_transition_guard | transition exclusion | Solar transition radius is solved by B_env(r_tr)=B_* in source model 89. | A local suppression domain must satisfy r_out << r_tr or carry a separate transition-current/routing proof. | Rows ending near r_tr are retained as warnings and not promoted. | anti_smuggling_guard | False |


## Local Domain B_min Rows

| domain_id | label | r_in_m | r_out_m | r_out_AU | r_transition_m | r_out_over_r_transition | r_out_definition | monotone_Benv_nonincreasing | B_min | B_star | Delta_B | margin_Bmin_minus_Bstar | epsilon_U_domain | epsilon_U_squared | epsilon_U_recomputed_from_Bmin | endpoint_A_curv | endpoint_Pi_B | endpoint_trace_warning | source_path | status | numeric_ready_for_smoke | valid_for_claim | claim_guard | warning |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| D4549_0_inner_solar_1_to_30_AU | inner source-model Solar exterior | 1.4959787070000000e+11 | 4.4879361210000000e+12 | 3.0000000000000000e+01 | 3.3700091957845725e+14 | 1.3317281527343615e-02 | 30 AU chosen finite inner-Solar source-model interval; not a planet-data claim | True | 9.1788135114056022e+00 | 1.0000000000000000e+00 | 5.0000000000000000e-01 | 8.1788135114056022e+00 | 7.8699652128477737e-08 | 6.1936352451434104e-15 | 7.8699652147728414e-08 | 9.6886492915331692e+03 | 9.9999992130034787e-01 | True | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\scripts\source_model_curvature_Lcg_test.py | source_model_domain_bound_strong_nonclaim | True | False | source-model domain row only; still needs PPN/R10 domain justification, S_static, K_a and boundary rows |  |
| D4549_1_outer_solar_1_to_100_AU | extended source-model Solar exterior | 1.4959787070000000e+11 | 1.4959787070000000e+13 | 1.0000000000000000e+02 | 3.3700091957845725e+14 | 4.4390938424478714e-02 | 100 AU conservative finite local exterior smoke interval; not a full PPN domain claim | True | 6.7719108545352888e+00 | 1.0000000000000000e+00 | 5.0000000000000000e-01 | 5.7719108545352888e+00 | 9.6956676641779538e-06 | 9.4005971454185979e-11 | 9.6956676641653025e-06 | 8.7197843602766432e+02 | 9.9999030433233582e-01 | True | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\scripts\source_model_curvature_Lcg_test.py | source_model_domain_bound_strong_nonclaim | True | False | source-model domain row only; still needs PPN/R10 domain justification, S_static, K_a and boundary rows |  |
| D4549_2_guarded_0p1_transition | ten-percent transition guard domain | 1.4959787070000000e+11 | 3.3700091957845727e+13 | 2.2527120072067794e+02 | 3.3700091957845725e+14 | 1.0000000000000001e-01 | r_out=0.1*r_transition using source-model transition solver | True | 5.1522979380901308e+00 | 1.0000000000000000e+00 | 5.0000000000000000e-01 | 4.1522979380901308e+00 | 2.4731611472994519e-04 | 6.1165260605115410e-08 | 2.4731611473007979e-04 | 1.7182818281923525e+02 | 9.9975268388527005e-01 | True | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\scripts\source_model_curvature_Lcg_test.py | source_model_domain_bound_strong_nonclaim | True | False | source-model domain row only; still needs PPN/R10 domain justification, S_static, K_a and boundary rows |  |
| D4549_3_half_transition_warning | half-transition warning domain | 1.4959787070000000e+11 | 1.6850045978922862e+14 | 1.1263560036033896e+03 | 3.3700091957845725e+14 | 5.0000000000000000e-01 | r_out=0.5*r_transition; included as warning because suppression weakens near transition | True | 2.0634553548874286e+00 | 1.0000000000000000e+00 | 5.0000000000000000e-01 | 1.0634553548874286e+00 | 1.0650862537518047e-01 | 1.1344087279310536e-02 | 1.0650862537518047e-01 | 6.8731273128331445e+00 | 8.9349137462481953e-01 | True | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\scripts\source_model_curvature_Lcg_test.py | source_model_domain_bound_numeric_but_transition_margin_warning | True | False | source-model domain row only; still needs PPN/R10 domain justification, S_static, K_a and boundary rows | near transition; do not use as local suppression proof |


## Static Bound With Domain epsilon_U

| update_id | observable | source_smoke_id | domain_epsilon_row | epsilon_U_domain | epsilon_U_squared | updated_static_formula | remaining_missing_inputs | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UPD4549_alpha3 | alpha3 | SMOKE4548_alpha3 | D4549_0_inner_solar_1_to_30_AU | 7.8699652128477737e-08 | 6.1936352451434104e-15 | Using D4549_0 source-model domain: \|Delta_alpha3\| <= \|K\|*(S_static*6.1936352451434104e-15 + B_boundary_alpha3) | S_static=C_H A_1 + D_m C_lap_m/L_B^2; K_a; B_boundary,a | domain_epsilon_inserted_coefficients_kernels_boundary_missing | False |
| UPD4549_xi | xi | SMOKE4548_xi | D4549_0_inner_solar_1_to_30_AU | 7.8699652128477737e-08 | 6.1936352451434104e-15 | Using D4549_0 source-model domain: \|Delta_xi\| <= \|K\|*(S_static*6.1936352451434104e-15 + B_boundary_xi) | S_static=C_H A_1 + D_m C_lap_m/L_B^2; K_a; B_boundary,a | domain_epsilon_inserted_coefficients_kernels_boundary_missing | False |
| UPD4549_R10_alpha_anchor | R10_alpha_anchor | SMOKE4548_R10_alpha_anchor | D4549_0_inner_solar_1_to_30_AU | 7.8699652128477737e-08 | 6.1936352451434104e-15 | Using D4549_0 source-model domain: \|Delta_R10_alpha_anchor\| <= \|K\|*(S_static*6.1936352451434104e-15 + B_boundary_R10_alpha_anchor) | S_static=C_H A_1 + D_m C_lap_m/L_B^2; K_a; B_boundary,a | domain_epsilon_inserted_coefficients_kernels_boundary_missing | False |
| UPD4549_Gdot_static_derivative | Gdot_static_derivative | SMOKE4548_Gdot_static_derivative | D4549_0_inner_solar_1_to_30_AU | 7.8699652128477737e-08 | 6.1936352451434104e-15 | No epsilon_U-only static-amplitude pass. 4545 derivative silence or time-variation kernel still required. | S_static=C_H A_1 + D_m C_lap_m/L_B^2; K_a; B_boundary,a | domain_epsilon_not_sufficient_for_time_derivative_channel | False |


## Remaining Blockers

| blocker_id | previous_status | new_status | what_changed | still_missing | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| BLOCK4549_0_Dloc_Bmin | MISSING_DOMAIN_INFIMUM | SOURCE_MODEL_NUMERIC_ROW_AVAILABLE_NONCLAIM | The point-mass source model now gives B_min and epsilon_U for named finite domains. | empirical/legal PPN/R10 domain adoption and transition-shell handling | False |
| BLOCK4549_1_Sstatic | MISSING_COEFFICIENT_PRODUCTS | STILL_MISSING | Domain epsilon can now be inserted into the formula. | C_H A_1 and D_m C_lap_m/L_B^2, or a parent zero theorem | False |
| BLOCK4549_2_Kernels | MISSING_ARENA_PROJECTION_KERNELS | STILL_MISSING | Projection formulas now have a candidate epsilon input. | K_alpha3, K_xi, K_R10(lambda), J_Gdot^t, orbital scalar kernel | False |
| BLOCK4549_3_Boundary | MISSING_BOUNDARY_ZERO_OR_BOUND | STILL_MISSING | Nothing in the domain epsilon row controls retained boundary/vector/shear channels. | static boundary amplitude zero theorem or finite rows | False |


## Claim Gates

| gate_id | condition | status | valid_for_claim |
| --- | --- | --- | --- |
| GATE4549_0_source_model_load | existing 89 source model script imported and evaluated without changing it | PASS | False |
| GATE4549_1_monotonicity | B_env monotone non-increasing on sampled point-mass domains | PASS | False |
| GATE4549_2_first_domain_numeric | first finite inner-Solar source-model domain has positive margin B_min>B_* and numeric epsilon_U | PASS | False |
| GATE4549_3_no_transition_smuggle | rows near transition are warnings/nonclaim, not local suppression passes | PASS | False |
| GATE4549_4_no_claim_until_kernels | no PPN/R10/Gdot/local-GR claim before S_static, K_a and boundary rows exist | PASS | False |


## Decision

| checkpoint | branch | decision | summary | claim_id | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| 4549 | MTS_R2FR_Y5_LOCAL_DOMAIN_BMIN_4549 | POINT_MASS_DOMAIN_BMIN_EPSILONU_ROWS_DERIVED_SOURCE_MODEL_NUMERIC_NONCLAIM_KERNELS_AND_COEFFICIENTS_STILL_MISSING | 4549 converts the 4548 epsilon_U law into named source-model point-mass domain rows. The inner 1-30 AU row supplies a numeric B_min and epsilon_U by monotonicity, but it remains nonclaim because projection kernels, S_static and boundary amplitudes are still absent. | L-391 | False |


## Next Target

| next_target | route | why | avoid | valid_for_claim |
| --- | --- | --- | --- | --- |
| 4550-Y5-R2FR-first-static-coefficient-product-bound-or-projection-kernel-row.md | best_forward_route | D_loc/B_min is no longer purely missing. The next real blocker is turning B_static into an observable: either fill S_static coefficient products or derive the first projection kernel row. | Do not celebrate the small epsilon_U^2 number as a pass until S_static, K_a and B_boundary are real. | False |


## Monotonicity Grid Preview

| domain_id | sample_index | radius_m | radius_AU | B_env | U_B | A_curv | Pi_B | trace_warning | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| D4549_0_inner_solar_1_to_30_AU | 0 | 1.4959787070000012e+11 | 1.0000000000000009e+00 | 1.5981105180940753e+01 | 9.7255536957163713e-14 | 8.7197843603264298e+06 | 9.9999999999990274e-01 | True | False |
| D4549_0_inner_solar_1_to_30_AU | 1 | 1.8503142370226550e+11 | 1.2368586720951604e+00 | 1.5555955568997078e+01 | 2.2737367544323206e-13 | 5.6998783675726317e+06 | 9.9999999999977263e-01 | True | False |
| D4549_0_inner_solar_1_to_30_AU | 2 | 2.2885772101626093e+11 | 1.5298193747370024e+00 | 1.5130805989243276e+01 | 5.3224091800530005e-13 | 3.7258505557622276e+06 | 9.9999999999946776e-01 | True | False |
| D4549_0_inner_solar_1_to_30_AU | 3 | 2.8306465691489795e+11 | 1.8921703603826625e+00 | 1.4705656458732513e+01 | 1.2456702336294256e-12 | 2.4354839644963611e+06 | 9.9999999999875433e-01 | True | False |
| D4549_0_inner_solar_1_to_30_AU | 4 | 3.5011097566883258e+11 | 2.3403473193207192e+00 | 1.4280507003572286e+01 | 2.9154456626656611e-12 | 1.5920075302546804e+06 | 9.9999999999708455e-01 | True | False |
| D4549_0_inner_solar_1_to_30_AU | 5 | 4.3303779645169293e+11 | 2.8946788776164909e+00 | 1.3855357663661499e+01 | 6.8229866201363620e-12 | 1.0406506523194702e+06 | 9.9999999999317701e-01 | True | False |
| D4549_0_inner_solar_1_to_30_AU | 6 | 5.3560655388625671e+11 | 3.5803086727106517e+00 | 1.3430208500074434e+01 | 1.5968337763183627e-11 | 6.8024413175995660e+05 | 9.9999999998403166e-01 | True | False |
| D4549_0_inner_solar_1_to_30_AU | 7 | 6.6246961100521765e+11 | 4.4283358306196643e+00 | 1.3005059606236934e+01 | 3.7371217231907394e-11 | 4.4465650193536148e+05 | 9.9999999996262878e-01 | True | False |
| D4549_0_inner_solar_1_to_30_AU | 8 | 8.1938128337131311e+11 | 5.4772255750516718e+00 | 1.2579911125045820e+01 | 8.7461593523130432e-11 | 2.9065947867836640e+05 | 9.9999999991253841e-01 | True | False |
| D4549_0_inner_solar_1_to_30_AU | 9 | 1.0134588460902664e+12 | 6.7745539515240329e+00 | 1.2154763275148410e+01 | 2.0468959860409086e-10 | 1.8999594558565106e+05 | 9.9999999979531040e-01 | True | False |
| D4549_0_inner_solar_1_to_30_AU | 10 | 1.2535053625983037e+12 | 8.3791658045190598e+00 | 1.1729616391000649e+01 | 4.7904191724512657e-10 | 1.2419501852469463e+05 | 9.9999999952095808e-01 | True | False |
| D4549_0_inner_solar_1_to_30_AU | 11 | 1.5504089782474993e+12 | 1.0363843890242611e+01 | 1.1304470984277255e+01 | 1.1211152006751490e-09 | 8.1182798816412818e+04 | 9.9999999887888480e-01 | True | False |
| ... | 56 additional rows in CSV | | | | | | | | |


## Source Register

| checkpoint | source_id | label | path | exists | needle | needle_found | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4549 | SRC4549_00_source_model_script | source model script formulas | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\scripts\source_model_curvature_Lcg_test.py | True | c_abs = math.sqrt(48.0) * G * mass_kg / (C * C * radius_m**3) | True | False |
| 4549 | SRC4549_01_source_model_lcg | source model L_cg rule | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\scripts\source_model_curvature_Lcg_test.py | True | return 1.0 / math.sqrt(1.0 / (l_h * l_h) + params.alpha_k * g_k * g_k) | True | False |
| 4549 | SRC4549_02_source_model_screening | source model B_env/Pi_B/U_B | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\scripts\source_model_curvature_Lcg_test.py | True | b_env = math.log1p(max(a_curv, 0.0)) - params.w_theta * math.log1p(max(e_theta, 0.0)) | True | False |
| 4549 | SRC4549_03_transition_solver | source model transition solver | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\scripts\source_model_curvature_Lcg_test.py | True | def find_solar_transition_radius(params: Parameters) -> float: | True | False |
| 4549 | SRC4549_04_source_model_doc | 89 documented point-mass source model | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\89-source-model-curvature-Lcg-test.md | True | C_abs = sqrt(48) G M_sun / (c^2 r^3) | True | False |
| 4549 | SRC4549_05_source_model_summary | source model summary rows | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\runs\source_model_curvature_Lcg_20260527-211932\summary.csv | True | solar_transition_shell_point_mass | True | False |
| 4549 | SRC4549_06_source_model_status | source model status parameters | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\runs\source_model_curvature_Lcg_20260527-211932\status.json | True | "b_star": 1.0 | True | False |
| 4549 | SRC4549_07_4548_range_law | 4548 epsilon_U range law | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\564-PPC4161-fill-first-epsilonU-local-range-row-or-static-bound-runner-smoke.md | True | epsilon_U(D_loc) := sup_Dloc U_B | True | False |
| 4549 | SRC4549_08_4548_range_csv | 4548 range law CSV | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4548_EPSILON_U_LOGISTIC_RANGE_LAW.csv | True | LAW4548_1_domain_sup | True | False |
| 4549 | SRC4549_09_4548_local_rows | 4548 local range rows | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4548_EPSILON_U_LOCAL_RANGE_ROW.csv | True | LR4548_1_sun_1AU_point_anchor | True | False |
| 4549 | SRC4549_10_4548_smoke | 4548 static smoke runner | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4548_STATIC_BOUND_SMOKE_RUNNER.csv | True | SMOKE4548_alpha3 | True | False |
| 4549 | SRC4549_11_4548_blockers | 4548 blockers | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4548_NUMERIC_BLOCKERS.csv | True | MISSING_DOMAIN_INFIMUM | True | False |


## Validation

| validation_id | status | detail |
| --- | --- | --- |
| VAL4549_00_sources | PASS | all source paths exist and needles found |
| VAL4549_01_law_rows | PASS | point-mass domain and epsilon laws present |
| VAL4549_02_domain_rows | PASS | domain rows have positive ranges, B_min and nonclaim epsilon_U |
| VAL4549_03_first_domain_bound | PASS | inner 1-30 AU source-model domain has strong positive screening margin |
| VAL4549_04_monotonicity_grid | PASS | monotonicity grid present and nonclaim |
| VAL4549_05_static_update | PASS | static smoke rows updated with domain epsilon and remain nonclaim |
| VAL4549_06_claim_gates | PASS | claim gates pass and retain nonclaim guard |
| VAL4549_07_csv_parse | PASS | all generated CSV files parse and have rows |
| VAL4549_08_docs_written | PASS | post and formal checkpoint docs written |
| VAL4549_09_pycache_absent | PASS | scripts __pycache__ absent after cleanup |
| VAL4549_OVERALL | PASS | 4549 local domain B_min and epsilon_U source-model bound |

