# 3908 - Measured Gstar Derivative Zero Gates or Bound Runner

Generated: `2026-07-01T09:50:28+00:00`

## Result

3908 turns the measured-`G_*` policy into an executable derivative gate.

No-cancellation rule:

`total_residual <= sum_i |component_i|; no fitted cancellation is credited unless a parent identity is signed`

Core bound branches:

- `B_Gdot = |d_t ln C_*| + |d_t ln M_eff| + |d_t epsilon_mu/(1+epsilon_mu)| + |d_t ln Z_Poisson| + |d_t ln Z_frame| <= 9.6e-15 yr^-1`
- `B_WEP = |Delta_AB ln kappa_eff| + |Delta_AB ln Xi| + |Delta_AB ln Z_frame| + |Delta_AB exchange| <= 2.8e-15`
- `B_R10(lambda) = alpha_predicted(lambda) <= alpha_bound(lambda) with sourced full-curve/arena projection rows`
- `B_product = |z_G| + |z_w| + |z_ellJ| + |z_Rframe| + |z_extra| + |epsilon_Gref_match|`

Verdict: measured `G_*` is acceptable only if every derivative/source/range gate is theorem-zero or bounded. Current state is not claim-ready, but it is now scoreable: time, radial, species, range, frame and product-factor residuals have explicit zero routes and fallback formulas.

## Gstar Derivative Zero Route Matrix

| gate_id | symbol | zero_route | source_theorem | fallback_formula | status |
| --- | --- | --- | --- | --- | --- |
| ZR3908_0_time | dln_Gstar_dt | G_* is a global/topological zero-form or q-global constant with no local time label | GST3880_0_target; GDOT3881_0_conditional_zero | B_Gdot = |d_t ln C_*| + |d_t ln M_eff| + |d_t epsilon_mu/(1+epsilon_mu)| + |d_t ln Z_Poisson| + |d_t ln Z_frame| <= 9.6e-15 yr^-1 | ZERO_CONDITIONAL_BOUND_ROUTE_ACTIVE |
| ZR3908_1_radial | partial_r_ln_Gstar | kappa/source charge/Poisson calibration/extra fields are constant outside compact source | RRF3762_2_no_radial_hair | |partial_r ln kappa_eff| + |partial_r ln C_M| + |partial_r ln Z_Poisson| + |partial_r ln Z_extra| | ZERO_CONDITIONAL_PROFILE_ROUTE_ACTIVE |
| ZR3908_2_species | partial_A_ln_Gstar | source functor forgets material/species labels and universal kappa/source action is parent-owned | WB3759_0_conditional_zero; SC3/C5 contracts | B_WEP = |Delta_AB ln kappa_eff| + |Delta_AB ln Xi| + |Delta_AB ln Z_frame| + |Delta_AB exchange| <= 2.8e-15 | ZERO_CONDITIONAL_WEP_BOUND_ROUTE_ACTIVE |
| ZR3908_3_range | alpha_Gstar_lambda | no unscreened finite-range mediator outside the EH metric/coframe and same total source | RRF3762_0_no_range_mediator | B_R10(lambda) = alpha_predicted(lambda) <= alpha_bound(lambda) with sourced full-curve/arena projection rows | ZERO_CONDITIONAL_R10_CURVE_ROUTE_ACTIVE |
| ZR3908_4_frame | partial_frame_ln_Gstar | same observed coframe/tau/source/orbit/clock branch is fixed before readout | RRF3762_4_single_observed_frame; FSM3764_2_frame | |delta_clock_frame| + |delta_light_cone| + |delta_source_frame| + |delta_preferred_frame| | ZERO_CONDITIONAL_FRAME_BOUND_ROUTE_ACTIVE |
| ZR3908_5_product | Dln_Z_product | z_G=z_w=z_ellJ=z_Rframe=z_extra=0 independently or by parent identity | GPL3600_1_product_identity; GPL3600_8_conditional_product_lock_theorem | B_product = |z_G| + |z_w| + |z_ellJ| + |z_Rframe| + |z_extra| + |epsilon_Gref_match| | ZERO_CONDITIONAL_PRODUCT_BOUND_ROUTE_ACTIVE |

## Gstar Derivative Bound Runner

| runner_id | observable | formula | required_inputs | runner_status |
| --- | --- | --- | --- | --- |
| RUN3908_0_absolute_sum | all derivative gates | total_residual <= sum_i |component_i|; no fitted cancellation is credited unless a parent identity is signed | component theorem-zero flags or source-backed numeric bounds | EXECUTABLE_FORMULA_READY_INPUTS_MISSING |
| RUN3908_1_Gdot | Gdot_over_G | B_Gdot = |d_t ln C_*| + |d_t ln M_eff| + |d_t epsilon_mu/(1+epsilon_mu)| + |d_t ln Z_Poisson| + |d_t ln Z_frame| <= 9.6e-15 yr^-1 | d_t ln C_*, d_t ln M_eff, d_t epsilon_mu, d_t ln Z_Poisson, d_t ln Z_frame | BOUND_READY_NUMERIC_COMPONENTS_MISSING |
| RUN3908_2_WEP | eta_source_AB | B_WEP = |Delta_AB ln kappa_eff| + |Delta_AB ln Xi| + |Delta_AB ln Z_frame| + |Delta_AB exchange| <= 2.8e-15 | Delta_AB ln kappa_eff, Delta_AB ln Xi, Delta_AB ln Z_frame, Delta_AB exchange | BOUND_READY_NUMERIC_COMPONENTS_MISSING |
| RUN3908_3_R10 | alpha(lambda) | B_R10(lambda) = alpha_predicted(lambda) <= alpha_bound(lambda) with sourced full-curve/arena projection rows | source-backed alpha_predicted(lambda), lambda rows, real alpha_bound(lambda), projection provenance | BOUND_CURVE_READY_PROJECTION_INPUTS_MISSING |
| RUN3908_4_radial_frame_product | radial/frame/product residual vector | |partial_r ln mu_obs| + |delta_frame_source| + B_product = |z_G| + |z_w| + |z_ellJ| + |z_Rframe| + |z_extra| + |epsilon_Gref_match| | radial profile, frame split, z_G/z_w/z_ellJ/z_Rframe/z_extra, Gref match | VECTOR_BOUND_READY_INPUTS_MISSING |

## Observable Budget Targets

| budget_id | observable | target_or_bound | units | acceptance_rule | status |
| --- | --- | --- | --- | --- | --- |
| BUD3908_0_Gdot | Gdot_over_G | 9.6e-15 | yr^-1 | absolute component sum <= bound and all components sourced or theorem-zero | TARGET_READY_COMPONENTS_MISSING |
| BUD3908_1_WEP | eta_source_AB | 2.8e-15 | dimensionless | composition residual absolute sum <= bound and source material mapping exists | TARGET_READY_COMPONENTS_MISSING |
| BUD3908_2_R10 | alpha(lambda) | alpha_bound(lambda) | dimensionless curve | each alpha_predicted(lambda) row <= real sourced bound row without placeholder coefficients | CURVE_TARGET_READY_PROJECTION_ROWS_MISSING |
| BUD3908_3_frame | delta_frame_source | PPN/clock/orbital row locks | dimensionless or arena-specific | single-frame theorem signed or every frame component has arena bound | TARGET_INTERFACE_READY_COMPONENTS_MISSING |
| BUD3908_4_product | Dln_Z_product | zero or arena budget inherited from Gdot/WEP/R10/PPN | per-channel derivative units | every product factor independently zero-owned or numerically bounded; no cancellation | TARGET_INTERFACE_READY_COMPONENTS_MISSING |

## Local-GR Claim Gate

| gate_id | gate | result | status | claim_allowed |
| --- | --- | --- | --- | --- |
| GATE3908_0_zero_route | all derivative zero routes parent-signed | not currently true; routes are conditional | BLOCKED_PARENT_SIGNATURES | False |
| GATE3908_1_bound_route | fallback numeric bound route | formulas exist, but component values/provenance are missing | BLOCKED_NUMERIC_COMPONENTS | False |
| GATE3908_2_measured_G_policy | measured G_* allowed | allowed only if derivative/source/range gates pass | POLICY_READY_NOT_CLAIM_READY | False |
| GATE3908_3_local_GR_Newton | local GR/Newton promotion | blocked until zero or bound route closes for all six derivative gates | BLOCKED_NO_CLAIM | False |

## Source Register

Resolved `13/13` source rows.

| source_id | path | needle_found | role |
| --- | --- | --- | --- |
| SRC3908_00_next | source-intake\mts_residuals\P8_Y5_R2FR_3907_NEXT_TARGET.csv | True | 3907 selected derivative gate target |
| SRC3908_01_policy | source-intake\mts_residuals\P8_Y5_R2FR_3907_MEASURED_COUPLING_POLICY_RUNNER.csv | True | measured Gstar derivative policy |
| SRC3908_02_gates | source-intake\mts_residuals\P8_Y5_R2FR_3907_GSTAR_DERIVATIVE_ZERO_GATES.csv | True | 3907 derivative gates |
| SRC3908_03_residuals | source-intake\mts_residuals\P8_Y5_R2FR_3906_NON_EH_AND_GSTAR_RESIDUAL_ROWS.csv | True | 3906 residual vector |
| SRC3908_04_silence | source-intake\mts_residuals\P8_Y5_R2FR_3880_GEFF_DERIVATIVE_SILENCE_THEOREM.csv | True | Geff derivative silence theorem |
| SRC3908_05_gdot_fallback | source-intake\mts_residuals\P8_Y5_R2FR_3881_GDOT_FALLBACK_BOUND_ROWS.csv | True | Gdot fallback absolute-sum bound |
| SRC3908_06_gdot_eval | source-intake\mts_residuals\P8_Y5_R2FR_3758_GDOT_BOUND_EVALUATION.csv | True | Gdot numeric target |
| SRC3908_07_wep_eval | source-intake\mts_residuals\P8_Y5_R2FR_3759_WEP_BOUND_EVALUATION.csv | True | WEP/source coupling target |
| SRC3908_08_rrf_locks | source-intake\mts_residuals\P8_Y5_R2FR_3762_RANGE_RADIAL_FRAME_LOCKS.csv | True | range/radial/frame lock theorem routes |
| SRC3908_09_rrf_budget | source-intake\mts_residuals\P8_Y5_R2FR_3762_RANGE_RADIAL_FRAME_RESIDUAL_BUDGET.csv | True | range/radial/frame residual budgets |
| SRC3908_10_frame | source-intake\mts_residuals\P8_Y5_R2FR_3764_FRAME_SOURCE_DESCENT_MATRIX.csv | True | frame source descent matrix |
| SRC3908_11_product_theorem | source-intake\mts_residuals\P8_Y5_R2FR_3600_GEFF_PRODUCT_LOCK_THEOREM.csv | True | G_eff product lock theorem |
| SRC3908_12_product_bounds | source-intake\mts_residuals\P8_Y5_R2FR_3600_GEFF_PRODUCT_BOUND_ROWS.csv | True | G_eff product bound rows |

## Next Target

| next_id | target_checkpoint | objective | why_next |
| --- | --- | --- | --- |
| NEXT3908_0 | 3909-Y5-R2FR-first-measured-Gstar-component-fill-Gdot-or-WEP.md | fill the first real measured-Gstar component branch: either Gdot component rows from stationary/topological zero-form route, or WEP/source-species rows from source-label forgetting | 3908 makes the derivative gates executable; the next real move is to close one component family rather than keep broad matrices open |

## Bottom Line

This is the practical local-test interface for a measured `G_*` branch:

1. If all derivative gates are parent-zero, local `G_*` is clean.
2. If not, the gates become quantitative residual rows.
3. No local-GR/Newton claim is allowed until either route closes.

The next best move is not another broad audit. It is to close one component family first: `Gdot` or WEP/source-species.
