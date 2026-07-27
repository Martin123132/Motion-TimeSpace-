# 3613 - EM Hodge normalization or PiM/Htau source denominator

## Verdict
3613 takes a real bite out of the EM/Poynting residual: `Delta_Hodge_EM` is now an explicit component bound, and the pure conformal piece is removed from the 4D Maxwell two-form Hodge mismatch.

`||Delta_Hodge_EM|| <= ||Delta_chi_principal|| + ||Delta_chi_skewon|| + L||d theta_EM|| + |C_Hodge_hidden| + |C_Hodge_readout| + |Delta_orientation_flux|`

The important guard is just as sharp: pure conformal scale is zero only for the Maxwell Hodge/cone piece.  It is still alive in clocks, source mass, alpha/charge normalization, and Newton calibration.  So this is progress, not a local-GR or Maxwell pass.

## Delta Hodge Bound
- `DHB3613_0_target` / `Delta_Hodge_EM`: TARGET_IMPORTED - `Delta_Hodge_EM := *_EM - *_obs[e_obs(q)] or chi_EM - chi(g_obs)`
- `DHB3613_1_component_bound` / `Delta_Hodge_EM aggregate bound`: SOURCE_BOUND_FILLED_NONCLAIM - `||Delta_Hodge_EM|| <= ||Delta_chi_principal|| + ||Delta_chi_skewon|| + L||d theta_EM|| + |C_Hodge_hidden| + |C_Hodge_readout| + |Delta_orientation_flux|`
- `DHB3613_2_principal` / `Delta_chi_principal`: RETAINED_COMPONENT_BOUND_REQUIRED - `Delta_chi_principal := chi_EM_principal - chi(g_obs)`
- `DHB3613_3_skewon` / `Delta_chi_skewon`: RETAINED_COMPONENT_BOUND_REQUIRED - `B_skewon := ||chi_EM_skewon||`
- `DHB3613_4_axion_gradient` / `Delta_chi_axion_gradient`: RETAINED_COMPONENT_BOUND_REQUIRED - `B_axion := L||d theta_EM||`
- `DHB3613_5_hidden_readout_orientation` / `hidden/readout/orientation Hodge tails`: RETAINED_TAIL_BOUND_REQUIRED - `B_tail := |C_Hodge_hidden| + |C_Hodge_readout| + |Delta_orientation_flux|`

## Conformal Subtheorem
- `CHS3613_0_theorem` / `pure conformal Hodge invariance`: MATHEMATICAL_SUBTHEOREM - In four spacetime dimensions, the Hodge star on two-forms is invariant under g -> Omega^2 g.
- `CHS3613_1_delta_hodge_effect` / `Delta_conformal_scale removal from Hodge cone`: SUBCOMPONENT_THEOREM_ZERO_FOR_HODGE_ONLY - A pure conformal factor does not belong in the Delta_Hodge_EM cone/2-form Hodge mismatch after the 4D Maxwell restriction.
- `CHS3613_2_no_overclaim` / `source/clock scale caveat`: RETAINED_SCALE_GATE - The same conformal freedom can still affect clocks, volumes, masses, alpha normalization, charge/current scale or Newton source calibration.
- `CHS3613_3_reconstruction` / `nonbirefringence only reconstructs conformal metric`: DERIVED_OBSTRUCTION_RETAINED - Fresnel/nonbirefringence can recover a conformal metric class, not the full source metric and normalization.

## EM Normalization
- `ENB3613_0_local_alpha_baseline` / `alpha_EM local branch`: CALIBRATED_CONSTANT_BASELINE_NONCLAIM - alpha may be carried as a calibrated universal local constant for the GR/Newton route without pretending it is derived.
- `ENB3613_1_CXF2_branch` / `C_XF2`: BOUND_BRANCH_RETAINED - nonzero hidden F^2 branch remains a scoreable residual and cannot be hidden inside source mass.
- `ENB3613_2_lambda_branch` / `D_vq ln lambda_A`: BOUND_BRANCH_RETAINED - Maxwell kinetic normalization is closed only on the calibrated branch; otherwise its vertical derivative is a force/clock/source residual.
- `ENB3613_3_current_branch` / `D_vq ln g_J`: OWNER_UNSIGNED_RETAINED - charge/current normalization must share the same owner as A_Q and F_Q^2 before EM stress and Lorentz force are comparable.

## PiM / Htau Fallback
- `PHTF3613_0_total` / `R_PiM_plus_R_Htau`: EXACT_DECOMPOSITION_IMPORTED - `R_PiM+R_Htau = C_M+C_shape+C_curl+C_domain+C_ref+C_frame+C_units`
- `PHTF3613_1_bound` / `PiM/Htau no-cancellation bound`: BOUND_FALLBACK_READY_VALUES_MISSING - `|R_PiM+R_Htau| <= |C_M|+|C_shape|+|C_curl|+|C_domain|+|C_ref|+|C_frame|+|C_units|`
- `PHTF3613_2_priority` / `Newton source denominator`: NEXT_PRESSURE_POINT_IF_HODGE_STALLS - `mu_obs=G_ref M_H_ref(1+epsilon_mu), not M_H_ref:=mu_obs/G_ref`

## Decision Gates
- `DEC3613_0_Delta_Hodge` / `Delta_Hodge_EM`: ADVANCED - Aggregate bound filled; pure conformal piece removed from the 4D two-form Hodge mismatch and reclassified as scale/source residual.
- `DEC3613_1_conformal` / `Delta_conformal_scale`: SUBTHEOREM_ZERO_FOR_HODGE_ONLY - Conformal light-cone agreement is useful but does not fix clocks, source mass, alpha, charge/current, or Newton normalization.
- `DEC3613_2_normalization` / `D_vq ln lambda_A / C_XF2`: RETAINED - Calibrated local alpha is allowed as baseline; any nonzero hidden F2 or kinetic drift branch remains scoreable.
- `DEC3613_3_PiM_Htau` / `Pi_M/H_tau source denominator`: FALLBACK_READY - If EM Hodge subcomponents cannot be parent-signed next, the denominator route has a ready no-cancellation component bound.
- `DEC3613_4_claim_guard` / `local-GR/Newton/Maxwell claim`: BLOCKED_FOR_CLAIM_NOT_FOR_WORK - No claim follows until the remaining Hodge components, normalization branch, and source denominator are theorem-zero or numeric/source-backed.
- `DEC3613_5_next` / `next best attack`: SELECT_PRINCIPAL_HODGE_OR_PIM_HTAU_CURL - Either attack Delta_chi_principal with empirical/parent bounds, or attack C_curl in Pi_M/H_tau because it is the Hamiltonian integrability core.

## Status
- `DELTA_HODGE_BOUND_FILLED_CONFORMAL_HODGE_SUBTERM_ZEROED_SCALE_RETAINED`: 3613 fills a source-backed aggregate Delta_Hodge_EM bound, proves the pure conformal piece is zero for the 4D two-form Maxwell Hodge operator, reclassifies conformal scale as a clock/source/normalization residual, keeps EM kinetic/C_XF2 branches nonclaim, and imports Pi_M/H_tau as the fallback Newton-source denominator bound.

## Validation
- `VAL3613_0_sources_exist`: PASS (all required 3613 source paths exist)
- `VAL3613_1_needles_found`: PASS (all selected 3613 source anchors found)
- `VAL3613_2_outputs_exist`: PASS (all pre-validation 3613 csv outputs written)
- `VAL3613_3_csv_parse`: PASS (source_register:16; delta_hodge_bound:6; conformal_subtheorem:4; em_normalization_branch:4; pim_htau_fallback:3; decision_gates:6; status:1; next_target:1; canonical_status:1)
- `VAL3613_4_delta_hodge_bound_filled`: PASS (Delta_Hodge_EM aggregate source-bound filled)
- `VAL3613_5_conformal_zero_hodge_only`: PASS (pure conformal term zeroed only for 4D Maxwell Hodge)
- `VAL3613_6_scale_retained`: PASS (conformal scale retained for clock/source/normalization)
- `VAL3613_7_normalization_branch_retained`: PASS (C_XF2 / kinetic branch remains nonclaim bound branch)
- `VAL3613_8_pim_htau_fallback_ready`: PASS (Pi_M/H_tau fallback no-cancellation bound imported)
- `VAL3613_9_no_claim_flags`: PASS (all generated rows remain nonclaim)
- `VAL3613_10_next_target_selected`: PASS (3614 target selected from concrete residual branches)
- `VAL3613_11_status_ok`: PASS (canonical status matches 3613 verdict)
- `VAL3613_12_formalization_workbench_untouched`: PASS (no 3613 checkpoint output appears in formalization-workbench outside package/venv noise)

## Next Target
- `NEXT3613_0` -> `3614-Y5-R2FR-principal-Hodge-bound-or-Htau-curl-integrability.md`
- Objective: try to source-bound or theorem-zero Delta_chi_principal using the constitutive/light-cone branch; if that does not close, attack C_curl in Pi_M/H_tau via Hamiltonian integrability and boundary symplectic flux
- Success gate: must produce a sourced nonclaim bound or theorem-zero for Delta_chi_principal, or a sourced nonclaim bound/theorem-zero for C_curl; do not write another generic coupling ledger
- Reason: 3613 removes the conformal Hodge decoy and leaves principal Hodge shape or H_tau curl as the next sharp pressure points.
