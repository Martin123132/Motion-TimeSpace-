# 3573 - PiM flux closure: Ward/Euler or Meff drift bound

## Verdict
3573 writes the Newton-source fork cleanly.  The required closure is `d(Pi_M J_H)=0`, equivalently `M_eff(S2)-M_eff(S1)=int_annulus d(Pi_M J_H)`.  Ward conservation, a topological current, or an Euler constraint could close it, but none is parent-derived yet.

So Newton/source calibration is not claimed.  The fallback rows are now explicit: `dln_Meff_dt`, `partial_r_ln_mu_obs`, `Delta_flux`, `Delta_cal`, `mu_extra`, `dln_Geff_dt`, and `alpha(lambda)`.  This prevents fitted-G sleight of hand: if flux closure fails, it becomes Gdot/radial/fifth-force/source-hair data.

## Generated outputs
- `source_register`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3573_SOURCE_REGISTER.csv`
- `closure_fork`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3573_PIM_FLUX_CLOSURE_FORK.csv`
- `drift_bound_rows`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3573_MEFF_DRIFT_RADIAL_BOUND_ROWS.csv`
- `activation_gates`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3573_ACTIVATION_GATES.csv`
- `decision_ledger`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3573_DECISION_LEDGER.csv`
- `status`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3573_STATUS.csv`
- `next_target`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3573_NEXT_TARGET.csv`
- `canonical_status`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PiM_flux_closure_status.csv`
- `validation`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_3573_VALIDATION.csv`

## Closure fork
- `FLUX3573_0_target`: J_M := Pi_M J_H must be a parent-owned mass-channel current and satisfy dJ_M=d(Pi_M J_H)=0 in the compact local exterior. (TARGET_DEFINED)
- `FLUX3573_1_ward_route`: If the local exterior supplies an observed stationary/asymptotic time generator xi and J_M^mu=T_H^{mu nu}xi_nu, then nabla_mu T_H^{mu nu}=0 plus L_xi g_obs=0 gives dJ_M=0. (EXACT_IF_STATIONARY_HAMILTONIAN_OWNER_SIGNED)
- `FLUX3573_2_topological_route`: If a parent topological/closed-form mass current J_M^top exists and equals Pi_M J_H on shell, then d(Pi_M J_H)=dJ_M^top=0. (PROMISING_NOT_IN_CORPUS)
- `FLUX3573_3_euler_route`: If a parent-owned lambda_M or equivalent source-normalization equation has an independent gauge/topological/Ward origin, its Euler equation may impose d(Pi_M J_H)=0. (EXACT_IF_NO_AD_HOC_MULTIPLIER_PROVED)
- `FLUX3573_4_flux_difference_law`: M_eff(S_2)-M_eff(S_1)=int_{S2xI} d(Pi_M J_H). (DERIVED_STOKES_BOUND_BACKBONE)
- `FLUX3573_5_measured_GM_warning`: Even if d(Pi_M J_H)=0, Newton needs M_eff=(4 pi G_ref)^-1 int_S2 Pi_M J_H and mu_obs=G_ref M_eff with constant G_ref and no mu_extra. (SCOPE_GUARD)
- `FLUX3573_6_verdict`: The exact closure routes are now written, but none are parent-derived in the current corpus; dln_Meff_dt and partial_r_ln_mu_obs stay retained as executable source-normalization residuals. (CLOSURE_NOT_CLAIMED_BOUND_ROWS_ACTIVE)

## Drift and radial rows
- `DRIFT3573_0_dlnMeff_dt` `dln_Meff_dt`: dln_Meff_dt := (1/M_eff) dM_eff/dt, with M_eff=int_S Pi_M J_H (MISSING_THEOREM_OR_NUMERIC_VALUE)
- `DRIFT3573_1_partial_r_ln_mu_obs` `partial_r_ln_mu_obs`: partial_r ln mu_obs = partial_r ln G_eff + partial_r ln M_eff + partial_r ln(1+epsilon_mu) (MISSING_THEOREM_OR_PROFILE)
- `DRIFT3573_2_Delta_flux` `Delta_flux`: Delta_flux := abs(int_annulus d(Pi_M J_H)) / abs(M_eff) (FORMULA_READY_INPUT_INTEGRAL_MISSING)
- `DRIFT3573_3_Delta_cal` `Delta_cal`: Delta_cal := M_eff[Pi_M J_H] - M_Gauss_orbital (CALIBRATION_GATE_OPEN)
- `DRIFT3573_4_mu_extra` `mu_extra_boundary_bulk_domain`: epsilon_mu := mu_extra/(G_eff M_eff); mu_obs=G_eff M_eff(1+epsilon_mu) (CENTRAL_MU_EXTRA_VECTOR_UNFILLED)
- `DRIFT3573_5_dlnGeff_dt` `dln_Geff_dt`: dln mu_obs/dt = dln_Geff_dt + dln_Meff_dt + dln(1+epsilon_mu)/dt (SEPARATE_COUPLING_SUPERSELECTION_OPEN)
- `DRIFT3573_6_alpha_lambda` `alpha(lambda)`: finite-range residual curve if no radial/range no-hair theorem exists (R10_CURVE_OR_NO_RANGE_THEOREM_MISSING)
- `DRIFT3573_7_total_source_drift` `D_X_ln_mu_obs`: D_X ln mu_obs = D_X ln G_eff + D_X ln M_eff + D_X ln(1+epsilon_mu) (EXECUTABLE_IDENTITY_NONCLAIM)

## Activation gates
- `GATE3573_0_sources`: PASS (all required 3573 source paths exist)
- `GATE3573_1_closure_identity`: PASS_FORMULA (Stokes/annulus law converts closure failure into residual rows)
- `GATE3573_2_ward_route`: FAIL_CURRENT_CLAIM (stationary/Hamiltonian mass generator and same-frame current not parent-derived)
- `GATE3573_3_topological_route`: FAIL_CURRENT_CLAIM (promising route exists but no parent current equal to Pi_M J_H is in corpus)
- `GATE3573_4_euler_route`: FAIL_CURRENT_CLAIM (no non-ad-hoc multiplier/source-normalization Euler origin)
- `GATE3573_5_drift_rows`: PASS_NONCLAIM (dln_Meff_dt and partial_r_ln_mu_obs rows generated with units and source links)
- `GATE3573_6_Newton_claim`: FAIL_CURRENT_CLAIM (closed calibrated mass flux and measured-GM equality remain open)
- `GATE3573_7_local_GR_claim`: FAIL_CURRENT_CLAIM (second-order PPN/source stability deferred until first-order source rows close)

## Decisions
- `DEC3573_0_no_Ward_shortcut`: do not count Ward conservation alone as d(Pi_M J_H)=0 -> prevents smuggling Newton source conservation from general covariance alone
- `DEC3573_1_drift_rows_live`: retain dln_Meff_dt and partial_r_ln_mu_obs as first-class rows -> keeps testing path alive instead of burying source calibration in fitted GM
- `DEC3573_2_next_target`: try topological mass-current origin next -> 3574 should construct or reject J_M^top=Pi_M J_H; if rejected, fill dln_Meff_dt/radial source rows numerically or from bounds

## Status
- `PIM_FLUX_CLOSURE_FORK_DERIVED_MEFF_DRIFT_ROWS_ACTIVE`: M_eff(S2)-M_eff(S1)=int_annulus d(Pi_M J_H) and dln_Meff_dt/partial_r_ln_mu_obs residual rows are explicit; Ward/topological/Euler closure routes are named but not parent-derived.

## Validation
- `VAL3573_0_sources_exist`: PASS (all required 3573 source paths exist)
- `VAL3573_1_required_needles_found`: PASS (all selected mass-flux source needles found)
- `VAL3573_2_outputs_exist`: PASS (all pre-validation 3573 output files written)
- `VAL3573_3_csv_parse`: PASS (source_register:15; closure_fork:7; drift_bound_rows:8; activation_gates:8; decision_ledger:3; status:1; next_target:1; canonical_status:1)
- `VAL3573_4_flux_law_present`: PASS (annulus flux law present)
- `VAL3573_5_ward_euler_routes_present`: PASS (Ward/topological/Euler closure routes present)
- `VAL3573_6_drift_rows_present`: PASS (Meff drift/radial/flux residual rows present)
- `VAL3573_7_Newton_claim_blocked`: PASS (Newton claim remains blocked)
- `VAL3573_8_next_topological_target_selected`: PASS (topological mass-current target selected)
- `VAL3573_9_no_claim_flags`: PASS (all generated physics rows remain nonclaim)
- `VAL3573_10_generated_source_paths_exist`: PASS (every generated row source_path exists)
- `VAL3573_11_formalization_workbench_untouched`: PASS (no 3573 checkpoint output appears in formalization-workbench)

## Next target
- `3574-Y5-R2FR-topological-mass-current-origin-or-Meff-drift-source-row.md`
- Objective: try to construct a parent-owned closed topological mass current J_M^top and prove J_M^top=Pi_M J_H on shell; if not, source the dln_Meff_dt/partial_r residual rows
