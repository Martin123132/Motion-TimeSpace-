# 3601 - ellJ source-current normalization zero or bound

## Verdict
3601 turns `ell_J` from a vague denominator into an exact component law: `z_ellJ = R_md + R_Ward + R_PiM + R_Htau + R_ref + R_W + R_frame + R_units`.

This is a real narrowing.  `ell_J` can be zero only if the full source-current chain is parent-owned before readout; it cannot be defined from measured orbital `GM` after the fact.

## ellJ Theorem Gate
- `ELJ3601_0_target`: TARGET_IMPORTED - Prove z_ellJ=D_X ln ell_J=0 by closing matter descent, Ward projection, Pi_M/H_tau, reference, support, frame and unit factors, or retain component bounds.
- `ELJ3601_1_exact_decomposition`: EXACT_DECOMPOSITION - z_ellJ[X] = R_md + R_Ward + R_PiM + R_Htau + R_ref + R_W + R_frame + R_units.
- `ELJ3601_2_matter_descent`: CONDITIONAL_ZERO_ROUTE_NOT_SIGNED - R_md=0 if S_matter descends as Sbar[q(Phi),psi,theta] with no source-only weight, hidden representative marker, or direct X/Z matter vertex.
- `ELJ3601_3_Ward_projection`: CONDITIONAL_ZERO_ROUTE_NOT_SIGNED - R_Ward=0 if the on-shell Hilbert/Ward current is conserved before Pi_M and readout, and all boundary/non-Hilbert tails are exact, zero, or retained separately.
- `ELJ3601_4_PiM_Htau_square`: EXACT_SUBDECOMPOSITION - R_PiM+R_Htau = C_M + C_shape + C_curl + C_domain + C_ref + C_frame + C_units.
- `ELJ3601_5_source_connection_zero_route`: CONDITIONAL_ZERO_ROUTE_NOT_SIGNED - C_M=C_shape=0 if the source coordinates Y=(M_H_ref,sigma^a) are q-basic and the residual direction v_X is vertical; then the source-branch connection A_X vanishes.
- `ELJ3601_6_reference_support_frame_units`: CONDITIONAL_ZERO_ROUTE_NOT_SIGNED - R_ref, R_W, R_frame and R_units vanish only if H_ref is source-blind, W_source=closure(supp J_H[tau]), one observed frame/tau/surface branch is fixed, and ell_J/C_source units are selected before measured GM.
- `ELJ3601_7_conditional_theorem`: CONDITIONAL_ZERO_THEOREM_DERIVED - If R_md=R_Ward=R_PiM=R_Htau=R_ref=R_W=R_frame=R_units=0 by one parent source-current chain, then z_ellJ=0 and the ell_J factor in the effective coupling product is source-silent.
- `ELJ3601_8_current_MTS_verdict`: BOUND_BRANCH_ACTIVE_NO_CLAIM - Current MTS has the exact ell_J decomposition and conditional theorem, but matter descent, Ward projection, Pi_M/H_tau, reference, support, frame and unit factors are not jointly parent-signed.

## ellJ Residuals
- `ELJR3601_0_total` / `z_ellJ`: ACTIVE_NONCLAIM - D_X ln ell_J
- `ELJR3601_1_R_md` / `R_md`: OPEN_MATTER_DESCENT_REQUIRED - D_X ln(delta S_matter/delta e_obs)-D_X ln(delta Sbar[q(Phi)]/delta e_obs)
- `ELJR3601_2_R_Ward` / `R_Ward`: OPEN_WARD_PROJECTION_REQUIRED - normalized failure of nabla_mu T_H^{mu nu}=0 to imply d(Pi_M J_H)=0
- `ELJR3601_3_R_PiM` / `R_PiM`: OPEN_PROJECTOR_LOCK_REQUIRED - ([D_X,Pi_M^H]J_H + Pi_M^H[D_X,J_H] - D_X Pi_M^H[J_H]) / Pi_M^H[J_H]
- `ELJR3601_4_R_Htau` / `R_Htau`: OPEN_HTAU_INTEGRABILITY_REQUIRED - normalized curl(delta H_tau) = normalized integral_S i_tau omega_total plus exact/boundary terms
- `ELJR3601_5_R_ref` / `R_ref`: OPEN_REFERENCE_LOCK_REQUIRED - D_X H_ref/(H_tau-H_ref)
- `ELJR3601_6_R_W` / `R_W`: OPEN_SUPPORT_SELECTOR_REQUIRED - D_X ln int_Wsource rho_H dV_H - D_X ln int_closure(supp J_H[tau]) rho_H dV_H
- `ELJR3601_7_R_frame` / `R_frame`: OPEN_FRAME_LOCK_REQUIRED - D_X ln(source readout frame)-D_X ln(parent H_tau frame)
- `ELJR3601_8_R_units` / `R_units`: OPEN_UNIT_LOCK_REQUIRED - D_X ln C_source + D_X ln hidden ell_J unit convention
- `ELJR3601_9_R_PiM_plus_R_Htau` / `R_PiM_plus_R_Htau`: OPEN_SUBDENOMINATOR_REQUIRED - C_M+C_shape+C_curl+C_domain+C_ref+C_frame+C_units
- `ELJR3601_10_A_source_connection` / `A_X_source_connection`: OPEN_SOURCE_CONNECTION_REQUIRED - A_X^M,A_X^a from D_X Y(Phi) with Y=(M_H_ref,sigma^a)
- `ELJR3601_11_MHref_units` / `Delta_MHref_tau_surface_total`: OPEN_MHREF_DENOMINATOR_REQUIRED - tau/coframe/surface/integrability/M_H_ref denominator lock residual

## Bound Rows
- `ELJB3601_0_z_ellJ` / `z_ellJ`: BOUND_REQUIRED_CRITICAL - D_X ln ell_J = R_md+R_Ward+R_PiM+R_Htau+R_ref+R_W+R_frame+R_units
- `ELJB3601_1_R_md` / `R_md`: BOUND_REQUIRED - matter descent/source-only multiplier residual
- `ELJB3601_2_R_Ward` / `R_Ward`: BOUND_REQUIRED - Ward conservation to projected source flux residual
- `ELJB3601_3_R_PiM` / `R_PiM`: BOUND_REQUIRED_CRITICAL - Pi_M/source-current commutator residual
- `ELJB3601_4_R_Htau` / `R_Htau`: BOUND_REQUIRED_CRITICAL - H_tau curl/integrability residual
- `ELJB3601_5_R_ref` / `R_ref`: BOUND_REQUIRED - D_X H_ref/(H_tau-H_ref)
- `ELJB3601_6_R_W` / `R_W`: BOUND_REQUIRED - worldtube support/domain selector drift
- `ELJB3601_7_R_frame` / `R_frame`: BOUND_REQUIRED - source frame/readout mismatch
- `ELJB3601_8_R_units` / `R_units`: BOUND_REQUIRED - D_X ln C_source + D_X ln hidden ell_J unit convention
- `ELJB3601_9_R_PiM_plus_R_Htau` / `R_PiM_plus_R_Htau`: BOUND_REQUIRED_CRITICAL - C_M+C_shape+C_curl+C_domain+C_ref+C_frame+C_units
- `ELJB3601_10_C_M_C_shape` / `C_M_plus_C_shape`: BOUND_REQUIRED - mass/shape source-branch connection curvature terms
- `ELJB3601_11_ellJ_total` / `epsilon_ellJ_total`: TOTAL_BOUND_BRANCH_ACTIVE - norm of active R_md,R_Ward,R_PiM,R_Htau,R_ref,R_W,R_frame,R_units and subdenominator components

## Promotion Gates
- `PROM3601_0_ellJ_decomposition`: PASS_EXACT_IDENTITY - z_ellJ splits into eight source-current owner components
- `PROM3601_1_conditional_theorem`: PASS_CONDITIONAL_THEOREM - z_ellJ=0 follows if all components close by one parent source-current chain
- `PROM3601_2_ellJ_claim`: FAIL_CURRENT_CLAIM - matter descent, Ward, Pi_M/H_tau, reference, support, frame and units are not jointly signed
- `PROM3601_3_PiM_Htau_claim`: FAIL_CURRENT_CLAIM - R_PiM+R_Htau remains the core open algebraic subproblem
- `PROM3601_4_no_measured_GM_laundering`: PASS_GUARD - ell_J, H_ref, M_H_ref and C_source cannot be defined from orbital GM after the fact
- `PROM3601_5_bound_pack`: PASS_NONCLAIM - rows are source-ready but not numeric/score-ready
- `PROM3601_6_no_Newton_or_GR_claim`: PASS_GUARD - ell_J source-current normalization is not promoted

## Status
- `ELLJ_SOURCE_CURRENT_NORMALIZATION_DECOMPOSED_PIM_HTAU_NEXT`: 3601 turns ell_J into an exact source-current owner decomposition: z_ellJ=R_md+R_Ward+R_PiM+R_Htau+R_ref+R_W+R_frame+R_units. The conditional theorem is clear, but current MTS has not parent-signed the component zeros.
- Decision: retain the ell_J theorem as conditional, keep z_ellJ and all components as active nonclaim rows, and attack R_PiM+R_Htau next because it is the largest algebraic subdenominator
- Still missing: matter descent grammar, Ward-to-projected-flux closure, Pi_M parent chainmap/commutator zero, H_tau integrability, source-blind H_ref, worldtube support selector, same frame/tau/readout lock, source-unit lock, and source-coordinate q-basic certificate

## Validation
- `VAL3601_0_sources_exist`: PASS (all required 3601 source paths exist)
- `VAL3601_1_needles_found`: PASS (all selected 3601 source anchors found)
- `VAL3601_2_outputs_exist`: PASS (all pre-validation 3601 csv output files written)
- `VAL3601_3_csv_parse`: PASS (source_register:20; ellj_theorem:9; residuals:12; bound_rows:12; promotion_gates:7; status:1; next_target:1; canonical_status:1)
- `VAL3601_4_decomposition_present`: PASS (ellJ exact decomposition row present)
- `VAL3601_5_component_bounds_present`: PASS (ellJ component bound rows present)
- `VAL3601_6_claims_blocked`: PASS (ellJ and PiM/Htau claims are blocked)
- `VAL3601_7_no_laundering_guard`: PASS (measured-GM laundering guard present)
- `VAL3601_8_no_claim_flags`: PASS (all generated physics rows remain nonclaim)
- `VAL3601_9_no_Newton_GR_claim`: PASS (Newton/PPN/local-GR claim guard is active)
- `VAL3601_10_next_target_selected`: PASS (3602 PiM/Htau target selected)
- `VAL3601_11_generated_source_paths_exist`: PASS (every generated row source_path exists)
- `VAL3601_12_formalization_workbench_untouched`: PASS (no 3601 checkpoint output appears in formalization-workbench outside package/venv noise)

## Next target
- `NEXT3601_0` -> `3602-Y5-R2FR-PiM-Htau-subdenominator-lock-or-component-bound.md`
- Objective: try to prove R_PiM+R_Htau=0 by closing source-coordinate q-basicity, Pi_M chainmap/commutator, H_tau integrability curl, reference, domain, frame and unit terms, or retain C_M/C_shape/C_curl/C_domain/C_ref/C_frame/C_units bounds
