# 3597 - EM/Poynting Hilbert source accounting or bound

## Verdict
3597 derives the clean conditional accounting law: EM stress, Poynting flux, and binding energy may enter the source branch exactly once if they are all owned by the same observed Hilbert variation before `Pi_M` and before readout.

This is progress, not a claim.  The Poynting vector now has a precise role: it is the exterior flux term in the dressed source balance.  If that flux is not zero or explicitly included, the local source charge has time/boundary hair and cannot be promoted to a Newton/PPN/local-GR result.

## Once-Only Theorem Gate
- `EMT3597_0_target`: TARGET_IMPORTED - Prove that EM stress, Poynting flux, and binding energy enter J_H_total exactly once in the source-measure branch, or retain epsilon_EM_once and Phi_EM_rad bounds.
- `EMT3597_1_visible_Maxwell_Hilbert_stress`: CONDITIONAL_STRESS_DERIVED - For S_EM=-1/4 integral sqrt(-g_obs) w_EM F_ab F^ab, variation before readout gives T_EM^{mu nu}=w_EM(F^{mu alpha}F^nu_alpha-1/4 g_obs^{mu nu}F^2) in the chosen sign convention.
- `EMT3597_2_Poynting_balance`: CONDITIONAL_BALANCE_DERIVED - D_tau E_EM[V] + integral_boundary S_Poynting dot n dA = - integral_V J dot E + improvement/boundary terms.
- `EMT3597_3_no_omission`: POYNTING_FLUX_EXPLICIT_GUARD - If Phi_EM_rad is nonzero, the local source charge has time/boundary hair unless Phi_EM_rad is included in M_source^dress or bounded over the stated window.
- `EMT3597_4_no_double_count`: DOUBLE_COUNT_GUARD - EM binding energy cannot be counted once inside dressed matter mass and again as an independent topological/source charge.
- `EMT3597_5_same_owner_requirements`: OWNER_PREMISES_LISTED - The same q/e_obs/tau branch must own the EM Hodge star, charge/current normalization, Maxwell action scale, Hilbert variation, Pi_M projection, and readout ordering.
- `EMT3597_6_conditional_theorem`: CONDITIONAL_ZERO_THEOREM_DERIVED - If Delta_Hodge_EM=0, w_EM=1, C_XF2=0, C_JQ=0, C_EM_readout=0, Delta_J_total=0, Pi_M is parent-fixed, exact improvements are boundary-silent, and Phi_EM_rad is zero or explicitly included, then epsilon_EM_once=0.
- `EMT3597_7_current_MTS_verdict`: BOUND_BRANCH_ACTIVE_NO_CLAIM - Current MTS has a viable accounting law but not a parent-signed EM once-only proof: Delta_Hodge_EM, w_EM, C_XF2, C_JQ, Phi_EM_rad, C_EM_readout, Delta_J_total, and exact-improvement silence remain active nonclaim rows.

## Residual Decomposition
- `EMR3597_0_total` / `R_EM_once_total`: ACTIVE_NONCLAIM - Pi_M[J_H_total - J_matter - J_EM - J_Poynting - J_binding - dB_impr]
- `EMR3597_1_Hodge` / `R_Delta_Hodge_EM`: OPEN_PARENT_SIGNATURE_REQUIRED - Delta_Hodge_EM = *_EM - *_obs[e_obs(q)] or chi_EM - chi_obs
- `EMR3597_2_wEM` / `R_w_EM`: OPEN_NORMALIZATION_REQUIRED - w_EM - 1
- `EMR3597_3_XF2` / `R_C_XF2`: OPEN_OPERATOR_DOMAIN_REQUIRED - C_XF2 hidden-visible F^2/F*F operator
- `EMR3597_4_CJQ` / `R_C_JQ`: OPEN_CHARGE_CURRENT_OWNER_REQUIRED - C_JQ charge/current normalization drift
- `EMR3597_5_PhiEM` / `R_Phi_EM_rad`: OPEN_FLUX_ZERO_OR_BOUND_REQUIRED - Phi_EM_rad = integral_boundary S_Poynting dot n dA
- `EMR3597_6_readout` / `R_C_EM_readout`: OPEN_READOUT_CLOSURE_REQUIRED - C_EM_readout effective post-reduction EM coefficient
- `EMR3597_7_DeltaJ` / `R_Delta_J_total`: OPEN_CURRENT_CLOSURE_REQUIRED - dJ_H_total - 0 = Delta_nonEH + Delta_frame + Delta_extra + Delta_boundary + Delta_radiative
- `EMR3597_8_double_count` / `R_EM_double_count`: OPEN_ANTI_TAUTOLOGY_GUARD - M_matter^dress + M_EM^separate - M_source^dress[J_H_total]
- `EMR3597_9_improvement` / `R_dB_improvement`: OPEN_BOUNDARY_SILENCE_REQUIRED - integral_boundary dB_impr or stress improvement flux
- `EMR3597_10_calibration_downstream` / `R_Gauss_orbital_calibration`: DOWNSTREAM_OPEN - M_source^dress[J_H_total] - M_Gauss_orbital

## Bound Rows
- `EMB3597_0_epsilon_EM_once` / `epsilon_EM_once`: BOUND_REQUIRED_CRITICAL - abs(Pi_M[J_H_total-J_matter-J_EM-J_Poynting-J_binding-dB_impr])/abs(M_H_ref)
- `EMB3597_1_epsilon_Hodge_EM` / `epsilon_Hodge_EM`: BOUND_REQUIRED - norm(*_EM-*_obs[e_obs(q)]) or norm(chi_EM-chi_obs)
- `EMB3597_2_epsilon_w_EM` / `epsilon_w_EM`: BOUND_REQUIRED - abs(w_EM-1)
- `EMB3597_3_epsilon_XF2` / `epsilon_XF2`: BOUND_REQUIRED - norm(C_XF2) with declared operator normalization
- `EMB3597_4_epsilon_CJQ` / `epsilon_CJQ`: BOUND_REQUIRED - abs(C_JQ)
- `EMB3597_5_epsilon_Phi_EM_rad` / `epsilon_Phi_EM_rad`: BOUND_REQUIRED_CRITICAL - abs(integral_boundary S_Poynting dot n dA)/(abs(G_ref M_H) over stated window)
- `EMB3597_6_epsilon_EM_readout` / `epsilon_EM_readout`: BOUND_REQUIRED - norm(C_EM_readout)
- `EMB3597_7_epsilon_Delta_J_total` / `epsilon_Delta_J_total`: BOUND_REQUIRED - norm(dJ_H_total)
- `EMB3597_8_epsilon_EM_double_count` / `epsilon_EM_double_count`: BOUND_REQUIRED - abs(M_matter^dress+M_EM^separate-M_source^dress[J_H_total])/abs(M_H_ref)
- `EMB3597_9_epsilon_dB_impr` / `epsilon_dB_impr`: BOUND_REQUIRED - abs(integral_boundary dB_impr)/abs(M_H_ref)
- `EMB3597_10_epsilon_EM_source_total` / `epsilon_EM_source_total`: TOTAL_BOUND_BRANCH_ACTIVE - sum of epsilon_EM_once, epsilon_Hodge_EM, epsilon_w_EM, epsilon_XF2, epsilon_CJQ, epsilon_Phi_EM_rad, epsilon_EM_readout, epsilon_Delta_J_total, epsilon_EM_double_count, epsilon_dB_impr

## Promotion Gates
- `PROM3597_0_conditional_theorem`: PASS_CONDITIONAL_THEOREM - epsilon_EM_once is zero only under the full listed same-owner premises
- `PROM3597_1_Poynting_visible`: PASS_GUARD - Phi_EM_rad is an explicit source/boundary term, not a hidden afterthought
- `PROM3597_2_EM_once_claim`: FAIL_CURRENT_CLAIM - Hodge, action normalization, current normalization, hidden XF2, readout, current closure and flux rows remain unsigned
- `PROM3597_3_no_double_count`: PASS_NONCLAIM_GUARD - the single dressed-source functional is required before any orbital mass readout
- `PROM3597_4_bound_pack`: PASS_NONCLAIM - rows are source-ready but not numeric/score-ready
- `PROM3597_5_no_Newton_claim`: PASS_GUARD - Gauss/orbital calibration remains downstream even if EM once-only closes

## Status
- `EM_POYNTING_ONCE_THEOREM_CONDITIONAL_BOUND_BRANCH_ACTIVE`: 3597 converts the coupling worry into a precise source-accounting theorem: EM stress, Poynting flux and binding energy can be included exactly once if they are varied in the same observed Hilbert source branch before Pi_M and before readout, with flux/boundary terms either zero or explicitly retained.
- Decision: keep the conditional theorem, retain all EM once-only rows as nonclaim bounds, and move next to calibrating the dressed Hilbert source against Gauss/orbital measured GM
- Still missing: parent-signed observed EM Hodge/coframe, w_EM=1 normalization, C_XF2=0 operator exclusion, C_JQ charge-current normalization, Phi_EM_rad zero or sourced flux bound, C_EM_readout=0 closure, total Hilbert current closure, exact-improvement boundary silence, and Gauss/orbital calibration

## Validation
- `VAL3597_0_sources_exist`: PASS (all required 3597 source paths exist)
- `VAL3597_1_needles_found`: PASS (all selected 3597 source anchors found)
- `VAL3597_2_outputs_exist`: PASS (all pre-validation 3597 csv output files written)
- `VAL3597_3_csv_parse`: PASS (source_register:19; em_once_theorem:8; residuals:11; bound_rows:11; promotion_gates:6; status:1; next_target:1; canonical_status:1)
- `VAL3597_4_conditional_theorem_present`: PASS (EM once-only conditional theorem row present)
- `VAL3597_5_Poynting_flux_explicit`: PASS (Poynting flux bound row is explicit)
- `VAL3597_6_EM_once_input_active`: PASS (epsilon_EM_once remains active until all owner premises close)
- `VAL3597_7_claim_blocked`: PASS (current EM/Poynting once-only claim is blocked)
- `VAL3597_8_no_claim_flags`: PASS (all generated physics rows remain nonclaim)
- `VAL3597_9_no_local_gr_claim`: PASS (Newton/PPN/local-GR claim guard is active)
- `VAL3597_10_double_count_guard`: PASS (double-count guard row present)
- `VAL3597_11_next_target_selected`: PASS (3598 Gauss/orbital calibration target selected)
- `VAL3597_12_generated_source_paths_exist`: PASS (every generated row source_path exists)
- `VAL3597_13_formalization_workbench_untouched`: PASS (no 3597 checkpoint output appears in formalization-workbench)

## Next target
- `NEXT3597_0` -> `3598-Y5-R2FR-Gauss-orbital-calibration-or-Delta-cal-bound.md`
- Objective: connect the dressed Hilbert source charge M_source^dress[W;tau]=ell_M(Pi_M J_H_total) to Poisson/Gauss/orbital measured GM, or retain Delta_cal/partial_r_ln_mu_obs/dln_Geff_dt bounds
