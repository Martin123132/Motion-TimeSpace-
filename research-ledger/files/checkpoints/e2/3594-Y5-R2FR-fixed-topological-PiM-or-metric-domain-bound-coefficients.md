# 3594 - Fixed-topological PiM or metric/domain bound coefficients

## Verdict
3594 gets a useful conditional theorem: a parent-selected fixed-topological `Pi_M` or identity subcomplex projector has no independent metric/domain projector stress.  That means `K_PiM_metric=K_PiM_domain=0` is mathematically legal inside that branch.

But it still does **not** prove source coupling, Newton, PPN, or local GR, because the fixed topological charge can still be the wrong conserved object unless it equals the Hilbert/source mass seen by local orbits.

## Theorem Attempt
- `FTP3594_0_target`: TARGET_IMPORTED - Try to prove delta_g Pi_M = D_D Pi_M = 0 by making Pi_M fixed-topological/identity, otherwise bound K_PiM_metric/domain.
- `FTP3594_1_topological_definition`: EXACT_DEFINITION_IF_PARENT_SELECTOR_EXISTS - Pi_top J := ell_M(J) omega_M_top, with d omega_M_top=0 and integral_S2 omega_M_top=1 on a parent-selected S2 class.
- `FTP3594_2_metric_zero`: DERIVED_CONDITIONAL_ZERO - delta_g Pi_top = 0
- `FTP3594_3_domain_isotopy_zero`: DERIVED_CONDITIONAL_EXACT_TERM - D_D Pi_top[delta D]J = ell_M(J) d alpha_D and integral_boundary d alpha_D = 0 when no support crosses the representative.
- `FTP3594_4_identity_branch`: DERIVED_CONDITIONAL_IDENTITY_ZERO - Pi_M = inclusion/identity on the Hilbert mass-current subcomplex implies delta Pi_M = 0 by definition.
- `FTP3594_5_wrong_object_obstruction`: MAIN_BLOCKER_RETAINED - dJ_M_top=0 does not imply Pi_M J_H = J_M_top.
- `FTP3594_6_em_poynting_guard`: RETAINED_EXPLICIT_GUARD - J_H must include matter, EM stress, Poynting flux and binding energy exactly once before Pi_M.
- `FTP3594_7_verdict`: CONDITIONAL_STRESS_ZERO_TOTAL_CLAIM_BLOCKED - K_PiM_metric=K_PiM_domain=0 only inside a parent-selected fixed-topological or identity Pi_M branch; current corpus does not certify the parent selector or Hilbert equality.

## Zero Audit
- `ZA3594_0_parent_selected_topology`: CONDITIONAL_OPEN - parent action fixes Sigma_ext and [S2] before readout
- `ZA3594_1_metric_independent_representative`: PASS_IF_TOPOLOGICAL_BRANCH - Pi_M uses closed topological representative, not Hodge/DeWitt
- `ZA3594_2_homology_preserving_domain`: CONDITIONAL_OPEN - domain motion is isotopy/exact and no source support crosses boundary
- `ZA3594_3_identity_subcomplex`: CONDITIONAL_OPEN - identity/inclusion projector on parent Hilbert mass subcomplex
- `ZA3594_4_hilbert_equality`: FAIL_CURRENT_BRANCH - topological or identity current equals projected Hilbert source
- `ZA3594_5_flux_calibration`: FAIL_CURRENT_BRANCH - closed current is calibrated to measured GM
- `ZA3594_6_em_poynting_once`: OPEN_RETAINED - EM/Poynting/binding source accounting is included once
- `ZA3594_7_total_local_gr`: FAIL_CURRENT_TOTAL - all local-GR projector/source gates pass

## Coefficient Rows
- `KMD3594_0_K_PiM_metric_topological` / `K_PiM_metric`: CONDITIONAL_ZERO_OR_BOUND_REQUIRED - ||delta_g Pi_M||_{J_H->M}
- `KMD3594_1_K_PiM_domain_topological` / `K_PiM_domain`: CONDITIONAL_ZERO_OR_BOUND_REQUIRED - ||D_D Pi_M||_{J_H->M}
- `KMD3594_2_K_PiM_Hodge_counterbranch` / `K_PiM_Hodge`: BOUND_REQUIRED_IF_USED - ||delta_g Pi_Hodge/DeWitt/Green||_{J_H->M}
- `KMD3594_3_K_PiM_support_crossing` / `K_PiM_support`: BOUND_REQUIRED_IF_USED - ||source support crossing/domain marker response||
- `KMD3594_4_epsilon_metric_domain` / `epsilon_PiM_metric_domain`: TOTAL_METRIC_DOMAIN_BOUND_BRANCH_ACTIVE - epsilon_PiM_metric + epsilon_PiM_domain <= (K_PiM_metric ||delta g|| + K_PiM_domain ||delta D||) ||J_H||/abs(M_H_ref) + epsilon_support

## Residual Update
- `ERU3594_0_gamma` / `epsilon_PiM_Gamma`: CARRIED_FROM_3593 - zero inside q/e_obs/tau-natural LC branch
- `ERU3594_1_metric_domain` / `epsilon_PiM_metric_domain`: PARTIAL_THEOREM_BOUND_BRANCH - conditional zero in fixed-topological/identity branch, otherwise K coefficient bound
- `ERU3594_2_parent_current` / `epsilon_PiM_parent`: OPEN_MAIN_BLOCKER - still requires Pi_M J_H = J_M^parent or topological-Hilbert equality
- `ERU3594_3_flux_calibration` / `epsilon_PiM_flux`: OPEN_MAIN_BLOCKER - still requires d(Pi_M J_H)=0 and measured GM calibration
- `ERU3594_4_em_poynting` / `epsilon_PiM_EM_accounting`: OPEN_RETAINED - retained until EM/Poynting/binding energy enters J_H_total once
- `ERU3594_5_total` / `epsilon_PiM`: NOT_SCORE_READY_TOTAL - metric/domain route sharpened but total source coupling remains not score-ready

## Promotion Gates
- `PROM3594_0_metric_domain_zero`: PASS_CONDITIONAL_BRANCH_ONLY - only if fixed-topological/identity parent selector is certified
- `PROM3594_1_total_DeltaPiM`: FAIL_CURRENT_CLAIM - wrong object, Hilbert equality, flux, calibration, EM accounting remain open
- `PROM3594_2_bound_rows`: PASS_NONCLAIM - rows are source-ready but not numeric/score-ready
- `PROM3594_3_no_multiplier_cheat`: PASS_GUARD - closure multiplier remains assumption unless independently owned
- `PROM3594_4_no_local_gr_claim`: PASS_GUARD - projector stress improved but source coupling not finished

## Status
- `FIXED_TOPOLOGICAL_PIM_STRESS_ZERO_CONDITIONAL_SOURCE_EQUALITY_BLOCKED`: 3594 derives the clean projector-stress route: if Pi_M is parent-selected fixed topological data, Pi_top J=ell_M(J) omega_M_top with closed normalized omega_M_top, then delta_g Pi_M=0 and homology-preserving domain variation is exact/boundary-silent. The identity subcomplex branch has the same projector-stress zero. Current MTS still lacks the parent selector and Hilbert/source equality, so the closed topological object may be the wrong conserved charge.
- Decision: use K_PiM_metric=K_PiM_domain=0 only as a conditional private branch; otherwise carry K_PiM_metric, K_PiM_domain, K_PiM_Hodge and K_PiM_support coefficient rows with no local-GR/Newton claim
- Still missing: parent-selected topology/domain, Pi_M J_H=J_M^parent or J_M_top+dB_zero, d(Pi_M J_H)=0, Poisson/Gauss/orbital calibration, EM/Poynting once-only Hilbert source accounting, numeric coefficient rows for non-topological branches

## Validation
- `VAL3594_0_sources_exist`: PASS (all required 3594 source paths exist)
- `VAL3594_1_needles_found`: PASS (all selected 3594 source anchors found)
- `VAL3594_2_outputs_exist`: PASS (all pre-validation 3594 csv output files written)
- `VAL3594_3_csv_parse`: PASS (source_register:20; theorem_attempt:8; zero_audit:8; coefficient_rows:5; residual_update:6; promotion_gates:5; status:1; next_target:1; canonical_status:1)
- `VAL3594_4_metric_zero_conditional`: PASS (metric projector zero theorem row present)
- `VAL3594_5_domain_exact_conditional`: PASS (domain isotopy exact-term row present)
- `VAL3594_6_wrong_object_blocked`: PASS (wrong-object/Hilbert equality blocker remains explicit)
- `VAL3594_7_coefficients_complete`: PASS (metric/domain coefficient rows complete)
- `VAL3594_8_residual_update_complete`: PASS (epsilon_PiM residual update includes main blockers)
- `VAL3594_9_no_claim_flags`: PASS (all generated physics rows remain nonclaim)
- `VAL3594_10_no_local_gr_claim`: PASS (Newton/PPN/local-GR claim guard is active)
- `VAL3594_11_next_target_selected`: PASS (3595 Hilbert-source/topological-charge glue target selected)
- `VAL3594_12_generated_source_paths_exist`: PASS (every generated row source_path exists)
- `VAL3594_13_formalization_workbench_untouched`: PASS (no 3594 checkpoint output appears in formalization-workbench)

## Next target
- `NEXT3594_0` -> `3595-Y5-R2FR-Hilbert-source-to-topological-charge-glue-or-wrong-object-bound.md`
- Objective: attack the conserved-wrong-object blocker: prove the fixed-topological/identity mass charge is the same Hilbert source charge measured by local orbits, or create explicit epsilon_PiM_parent/wrong-object bound rows
