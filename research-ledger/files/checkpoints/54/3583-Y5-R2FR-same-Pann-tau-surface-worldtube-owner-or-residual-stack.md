# 3583 — same-Pann tau/surface/worldtube owner or residual stack

## Verdict
3583 turns the remaining same-annulus geometry problem into one precise object: `E_stat=(D_ext,K,r,W_source,Sigma_tau,S_in,S_out,Phi_infty)`.  If the parent theory owns `E_stat` before readout, then the previously separate blockers `Z_tau`, `Z_same_tau`, `Z_surface`, `Z_worldtube`, and `Z_no_seams` close together on the same `P_ann` branch.

This is a forward reduction, not a claim.  `E_stat` is not yet derived from the MTS parent action or quotient map.  With the `3582` asymptotic anchor carried forward, the annulus residual narrows to:

`R_ann_abs = C_EM_surface_gauge_abs + epsilon_Estat`.

So the Poynting/local-EM branch is now mainly blocked by two things: parent ownership of `E_stat`, and the EM gauge/corner term.

## Domain theorem rows
- `SPD3583_0_Estat_object`: E_stat := (D_ext, K=tau_obs, r, W_source, Sigma_tau, S_in, S_out, Phi_infty) (CERTIFICATE_OBJECT_DEFINED)
- `SPD3583_1_tau_from_Estat`: L_K g_obs=0, K(r)=0, K|infty normalized once => nabla_(mu tau_nu)=0 and tau_source=tau_boundary=tau_readout (DERIVED_IF_ESTAT_PARENT_SIGNED)
- `SPD3583_2_surfaces_from_Estat`: S_R := Sigma_tau cap {r=R}; boundary(D_stat)=S_out union (-S_in) with no time caps (DERIVED_IF_ESTAT_PARENT_SIGNED)
- `SPD3583_3_worldtube_from_Estat`: closure(supp J_H[tau]) subset int(S_in), L_K W_source=0, and A_ext cap W_source=empty => J_cross=0 in the annulus (DERIVED_IF_ESTAT_PARENT_SIGNED)
- `SPD3583_4_seams_from_Estat`: D_stat is one smooth K-invariant annulus with no cutoff, excision, smoothing, patch, or reference seam => B_corner_flux=0 (DERIVED_IF_ESTAT_REGULARITY_SIGNED)
- `SPD3583_5_residual_collapse`: Phi_anchor_abs=0 from 3582 and E_stat=>Delta_tau_surface_abs=Delta_surface_owner_abs=J_cross_EM_abs=B_corner_flux_abs=0 (GEOMETRY_STACK_COLLAPSES_CONDITIONALLY)
- `SPD3583_6_live_blocker`: Z_Estat is not yet parent-derived from the MTS action or quotient map (MISSING_PARENT_STATIONARY_EXTERIOR_DOMAIN_THEOREM)

## Geometry clause audit
- `GCA3583_0_Estat` `Z_Estat`: MISSING_PARENT_STATIONARY_EXTERIOR_DOMAIN_OWNER — This is now the single hard geometry owner, not five independent assumptions.
- `GCA3583_1_tau` `Z_tau`: PASS_IF_ESTAT_SIGNED — Follows from L_K g_obs=0 inside the same exterior domain.
- `GCA3583_2_same_tau` `Z_same_tau`: PASS_IF_ESTAT_ASYMPTOTIC_NORMALIZATION_SIGNED — A single K normalized at the branch boundary prevents tau swapping.
- `GCA3583_3_surface` `Z_surface`: PASS_IF_ESTAT_REGULAR_LEVEL_SETS_SIGNED — Actual-surface equivalence is inherited from one domain object.
- `GCA3583_4_worldtube` `Z_worldtube`: PASS_IF_ESTAT_COMPACT_INVARIANT_SUPPORT_SIGNED — No support in the annulus means no crossing current term.
- `GCA3583_5_no_seams` `Z_no_seams`: PASS_IF_ESTAT_SMOOTH_SINGLE_ANNULUS_SIGNED — Otherwise B_corner_flux_abs must stay finite and sourced.
- `GCA3583_6_anchor` `Z_anchor`: PASS_FROM_3582_CONDITIONAL — The anchor is no longer the live geometry blocker.
- `GCA3583_7_gauge` `Z_gauge`: MISSING_EM_GAUGE_CORNER_CERTIFICATE — Still separate from E_stat unless a later closed-surface/exact-form theorem removes it.
- `GCA3583_8_activation` `Z_Poynting`: FAIL_CURRENT_CLAIM_ESTAT_AND_GAUGE_UNSIGNED — With 3582 and 3583, the branch is narrowed but not claim-grade.

## Residual stack
- `GRS3583_0_Phi_anchor_abs` `Phi_anchor_abs`: 0 (ZERO_IF_3582_BRANCH_CONDITIONS_HOLD)
- `GRS3583_1_Delta_tau_surface_abs` `Delta_tau_surface_abs`: 0 if Z_Estat, else epsilon_Killing + epsilon_same_tau (CONDITIONAL_ZERO_OR_FINITE_ESTAT_RESIDUAL)
- `GRS3583_2_Delta_surface_owner_abs` `Delta_surface_owner_abs`: 0 if Z_Estat, else epsilon_surface_equivalence (CONDITIONAL_ZERO_OR_FINITE_ESTAT_RESIDUAL)
- `GRS3583_3_J_cross_EM_abs` `J_cross_EM_abs`: 0 if Z_Estat, else epsilon_crossing_flux (CONDITIONAL_ZERO_OR_FINITE_ESTAT_RESIDUAL)
- `GRS3583_4_B_corner_flux_abs` `B_corner_flux_abs`: 0 if Z_Estat smooth single-annulus, else epsilon_seam_flux (CONDITIONAL_ZERO_OR_FINITE_ESTAT_RESIDUAL)
- `GRS3583_5_C_EM_surface_gauge_abs` `C_EM_surface_gauge_abs`: MISSING_EM_GAUGE_CORNER_VALUE_OR_ZERO_THEOREM (STILL_LIVE_NON_GEOMETRY_RESIDUAL)
- `GRS3583_6_Estat_residual_norm` `epsilon_Estat`: epsilon_Killing + epsilon_same_tau + epsilon_surface_equivalence + epsilon_crossing_flux + epsilon_seam_flux (NO_CANCELLATION_GEOMETRY_STACK)
- `GRS3583_7_R_ann_abs_after_3583` `R_ann_abs`: C_EM_surface_gauge_abs + epsilon_Estat (REDUCED_RESIDUAL_STACK_NONCLAIM)

## Gates
- `GATE3583_0_sources`: PASS (all source paths and selected anchors exist)
- `GATE3583_1_Estat_reducer`: PASS_CONDITIONAL_THEOREM (one E_stat certificate implies tau, same-tau, surfaces, worldtube no-crossing, and no seams)
- `GATE3583_2_anchor_carried`: PASS_CONDITIONAL_PUBLIC_EM_ZERO_ANCHOR (Phi_anchor_abs=0 is carried from 3582 and not reopened)
- `GATE3583_3_geometry_claim`: FAIL_CURRENT_CLAIM (E_stat has not yet been derived from the parent MTS action or quotient map)
- `GATE3583_4_gauge_corner`: FAIL_CURRENT_CLAIM (C_EM_surface_gauge_abs remains unsigned or unbounded)
- `GATE3583_5_local_GR`: FAIL_CURRENT_CLAIM (local GR/Newton still requires parent action, coupling normalization, denominator positivity, and PPN residual closure)

## Status
- `SAME_PANN_GEOMETRY_REDUCED_TO_SINGLE_ESTAT_OWNER_NOT_PARENT_SIGNED`: The tau/surface/worldtube/no-seam blockers are no longer independent loose assumptions. A single stationary exterior-domain certificate E_stat=(D_ext,K,r,W_source,Sigma_tau,S_in,S_out,Phi_infty) would imply Z_tau, Z_same_tau, Z_surface, Z_worldtube, and Z_no_seams on the same P_ann branch. With the 3582 Phi_anchor zero carried forward, R_ann_abs reduces to C_EM_surface_gauge_abs + epsilon_Estat.
- Still missing: parent derivation of E_stat from the MTS action/quotient map, EM gauge/corner silence or finite value, source coupling normalization, positive same-frame denominator, and PPN/local-GR residual closure

## Validation
- `VAL3583_0_sources_exist`: PASS (all required 3583 source paths exist)
- `VAL3583_1_required_needles_found`: PASS (all selected 3583 anchors found)
- `VAL3583_2_outputs_exist`: PASS (all pre-validation 3583 output files written)
- `VAL3583_3_csv_parse`: PASS (source_register:14; domain_theorem:7; geometry_clauses:9; residual_stack:8; activation_gates:6; status:1; next_target:1; canonical_status:1)
- `VAL3583_4_Estat_object_present`: PASS (E_stat object theorem row present)
- `VAL3583_5_geometry_reducer_present`: PASS (geometry residual collapse row present)
- `VAL3583_6_clause_symbols_present`: PASS (all 3583 clause symbols present)
- `VAL3583_7_anchor_not_reopened`: PASS (3582 anchor zero carried forward)
- `VAL3583_8_reduced_stack_present`: PASS (reduced R_ann stack present)
- `VAL3583_9_full_claim_blocked`: PASS (geometry claim remains blocked until parent E_stat is signed)
- `VAL3583_10_no_claim_flags`: PASS (all generated physics rows remain nonclaim)
- `VAL3583_11_next_target_selected`: PASS (parent E_stat next target selected)
- `VAL3583_12_generated_source_paths_exist`: PASS (every generated row source_path exists)
- `VAL3583_13_formalization_workbench_untouched`: PASS (no 3583 checkpoint output appears in formalization-workbench)

## Next target
- `NEXT3583_0` -> `3584-Y5-R2FR-parent-Estat-stationary-exterior-domain-theorem-or-epsilon-stack.md`
- Objective: try to derive E_stat from the parent MTS action/quotient map as the local stationary exterior branch, or define the finite epsilon_Estat stack with measurable/source-backed terms
