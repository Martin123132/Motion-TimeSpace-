# 3582 — Phi anchor zero boundary condition or first finite flux row

## Verdict
3582 makes a real forward move: the Poynting anchor is not left as a vague missing object.  On the stationary asymptotic public-EM branch, choose the anchor surface at infinity:

`Phi_infty[K] = lim_{R->infty} int_{S_R} T_EM^{mu nu} K_mu n_nu dA = lim_{R->infty} int_{S_R} n.(E x H) dA`.

For a compact stationary Maxwell source with no transverse radiative `O(R^-1)` field, `E=O(R^-2)` and `B=O(R^-3)`, so `n.(E x H)=O(R^-5)` and the surface integral is `O(R^-3)->0`.  Therefore `Phi_anchor_abs=0` is conditionally filled for this no-radiation boundary branch.

This is not a local-GR claim.  It closes the Poynting-specific anchor slot only; the same-package geometry owner remains live: `tau_obs`, `S_in/S_out`, compact no-crossing worldtube support, EM gauge/corners, and regulator seams.

## Theorem rows
- `PAZ3582_0_anchor_definition`: Phi_infty[K] := lim_{R->infty} int_{S_R} T_EM^{mu nu} K_mu n_nu dA = lim_{R->infty} int_{S_R} n.(E x H) dA (ANCHOR_OBJECT_DEFINED)
- `PAZ3582_1_stationary_falloff_clause`: E = Q rhat/(4 pi epsilon0 R^2)+O(R^-3), B = O(R^-3), and no transverse radiative O(R^-1) fields (STANDARD_PUBLIC_EM_ASYMPTOTIC_INPUT)
- `PAZ3582_2_zero_flux_estimate`: n.(E x H)=O(R^-5), dA=O(R^2), hence Phi_infty=O(R^-3)->0 (DERIVED_CONDITIONAL_PUBLIC_EM_ZERO)
- `PAZ3582_3_transport_into_annulus`: If 3580 transport clauses close on the same P_ann, Phi_anchor=Phi_infty=0 propagates to S_out and S_in. (ANCHOR_SLOT_FILLED_CONDITIONALLY)
- `PAZ3582_4_radiation_escape_clause`: If O(R^-1) radiative fields, incoming waves, external driving, or non-stationary sources are present, Phi_infty need not vanish and FAR3581_0 must be a finite measured/source-backed row. (FINITE_ROW_REQUIRED_IF_BOUNDARY_FAILS)
- `PAZ3582_5_scope_guard`: Phi_anchor=0 does not prove the MTS EM coupling normalization, fine-structure constant, Newtonian limit, PPN pass, or local GR. (NO_OVERCLAIM_GUARD)

## Clause audit
- `PAC3582_0_anchor_surface` `Z_anchor_surface`: PASS_CONDITIONAL_PUBLIC_EM — Anchor is at infinity, not an arbitrary interior surface.
- `PAC3582_1_stationary_source` `Z_stationary_source`: PASS_IF_3580_TAU_WORLDLINE_CLAUSES_CLOSE — This still depends on the same tau/worldtube ownership package.
- `PAC3582_2_asymptotic_flat_falloff` `Z_asymptotic_falloff`: PASS_CONDITIONAL_PUBLIC_EM — This is a standard exterior boundary condition, not a new fitted MTS parameter.
- `PAC3582_3_no_radiative_1overR` `Z_no_radiative_1overR`: PASS_BY_BOUNDARY_BRANCH_SELECTION — If this fails, the finite-flux row is mandatory.
- `PAC3582_4_radial_flux_estimate` `Z_radial_flux_zero`: PASS_DERIVED — This is the actual proof step: O(R^-5) times O(R^2) tends to zero.
- `PAC3582_5_same_package_transport` `Z_same_Pann_transport`: MISSING_SAME_PACKAGE_OWNER_FOR_PUBLIC_CLAIM — 3582 fills the anchor; it does not yet prove every 3581 package object is parent-owned.
- `PAC3582_6_anchor_result` `Z_anchor`: PASS_CONDITIONAL_PUBLIC_EM_ZERO_ANCHOR — This closes the Poynting-specific anchor row conditionally, while keeping the full MTS/local-GR switch false.

## Bound rows
- `PAB3582_0_Phi_infty` `Phi_infty`: 0 [W in SI or geometrized Killing-energy/time] (DERIVED_ZERO_UNDER_STATIONARY_ASYMPTOTIC_FALLOFF)
- `PAB3582_1_Phi_anchor_abs` `Phi_anchor_abs`: 0 [same as Phi_infty] (FILLED_CONDITIONALLY_REPLACES_FAR3581_0_ON_THIS_BRANCH)
- `PAB3582_2_R_ann_abs_reduced` `R_ann_abs`: MISSING_GEOMETRY_OWNER_RESIDUALS [mixed residual bound units] (PHI_ANCHOR_TERM_REMOVED_ONLY_IF_3582_BRANCH_CONDITIONS_HOLD)
- `PAB3582_3_I_matter_EM_flux_reduced` `I_matter_EM_flux`: MISSING_REMAINING_RESIDUAL_VALUES [H_tau source contribution units] (HTAU_FEED_READY_WITH_ANCHOR_ZERO_NONCLAIM)
- `PAB3582_4_finite_escape` `Phi_anchor_abs`: MISSING_NUMERIC_FINITE_FLUX [W or geometrized Killing-energy/time] (REQUIRED_IF_NO_RADIATION_BOUNDARY_REJECTED)

## Gates
- `GATE3582_0_sources`: PASS (all source paths and selected anchors exist)
- `GATE3582_1_asymptotic_anchor`: PASS_CONDITIONAL_PUBLIC_EM (Phi_infty=0 follows from stationary finite-source Maxwell falloff with no O(R^-1) radiative field)
- `GATE3582_2_anchor_slot`: PASS_CONDITIONAL_PUBLIC_EM_ZERO_ANCHOR (FAR3581_0 is filled by a theorem-zero on the asymptotic no-radiation branch)
- `GATE3582_3_full_3581_switch`: FAIL_CURRENT_CLAIM (Z_tau, Z_surface, Z_worldtube, Z_gauge, and Z_no_seams remain unsigned)
- `GATE3582_4_local_GR`: FAIL_CURRENT_CLAIM (anchor zero is one public EM boundary condition, not a derivation of local GR/Newton)
- `GATE3582_5_finite_escape`: PASS_GUARD (radiative/external branches are routed to a finite Phi_anchor row instead of being forced to zero)

## Status
- `PHI_ANCHOR_ZERO_DERIVED_CONDITIONALLY_PUBLIC_EM_LOCAL_BRANCH_STILL_BLOCKED`: The Poynting-specific anchor is no longer a pure missing row: on a stationary asymptotically flat public Maxwell branch with finite compact source and no O(R^-1) radiative field, Phi_infty=0 because n.(E x H)=O(R^-5) and the sphere area is O(R^2). This conditionally fills Phi_anchor_abs=0 for the 3581 package.
- Still missing: same-P_ann parent ownership of tau_obs, S_in/S_out, compact no-crossing worldtube support, EM gauge/corner silence, regulator seam ledger, and parent-owned EM normalization/charge-current coupling

## Validation
- `VAL3582_0_sources_exist`: PASS (all required 3582 source paths exist)
- `VAL3582_1_required_needles_found`: PASS (all selected 3582 anchors found)
- `VAL3582_2_outputs_exist`: PASS (all pre-validation 3582 output files written)
- `VAL3582_3_csv_parse`: PASS (source_register:11; anchor_theorem:6; anchor_clauses:7; bound_rows:5; activation_gates:6; status:1; next_target:1; canonical_status:1)
- `VAL3582_4_zero_theorem_present`: PASS (asymptotic zero theorem row present)
- `VAL3582_5_anchor_clause_promoted_conditionally`: PASS (Z_anchor conditionally promoted)
- `VAL3582_6_phi_anchor_value_zero`: PASS (Phi_anchor_abs zero row present)
- `VAL3582_7_full_switch_still_blocked`: PASS (full 3581 switch remains blocked)
- `VAL3582_8_no_claim_flags`: PASS (all generated physics rows remain nonclaim)
- `VAL3582_9_finite_escape_present`: PASS (finite-flux escape row present)
- `VAL3582_10_next_target_selected`: PASS (same-Pann geometry next target selected)
- `VAL3582_11_generated_source_paths_exist`: PASS (every generated row source_path exists)
- `VAL3582_12_formalization_workbench_untouched`: PASS (no 3582 checkpoint output appears in formalization-workbench)

## Next target
- `NEXT3582_0` -> `3583-Y5-R2FR-same-Pann-tau-surface-worldtube-owner-or-residual-stack.md`
- Objective: try to parent-own the same stationary package geometry: tau_obs, S_in/S_out, and compact no-crossing worldtube support, now that the Poynting anchor itself has a conditional public EM zero
