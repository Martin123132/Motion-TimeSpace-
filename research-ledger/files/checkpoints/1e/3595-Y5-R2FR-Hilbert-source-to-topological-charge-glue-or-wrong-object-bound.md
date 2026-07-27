# 3595 - Hilbert source to topological charge glue or wrong-object bound

## Verdict
3595 gets the exact mathematical route on paper: a closed Hilbert mass current in a fixed `S2 x I` exterior decomposes into the normalized topological mass representative plus an exact term and any non-mass cohomology residue.

So the topological route can work **only if** `Q_M` is not an independent label: it must be `ell_M(Pi_M J_H)=M_source[W]` before orbital readout, with zero exact boundary flux and EM/Poynting/binding included once.

## Glue Theorem
- `HGT3595_0_target`: TARGET_IMPORTED - Prove Pi_M J_H = J_M_top + dB_zero, or retain epsilon_PiM_parent as a wrong-object residual.
- `HGT3595_1_deRham_decomposition`: CONDITIONAL_THEOREM_DERIVED - For a closed Hilbert mass 2-current J_M on E with H^2(E)=R[S2], J_M = ell_M(J_M) omega_M_top + dB + R_perp.
- `HGT3595_2_QM_not_independent`: MAIN_NO_CHEAT_CONDITION - Q_M := ell_M(Pi_M J_H) := integral_S Pi_M J_H := M_source[W] before orbital readout.
- `HGT3595_3_zero_boundary_exact_term`: CONDITIONAL_BOUNDARY_ZERO - Pi_M J_H - J_M_top = dB_zero and integral_boundary dB_zero = 0.
- `HGT3595_4_worldtube_dressed_source`: NECESSARY_DEFINITION_LOCK - M_source[W] := H_tau[S_outer] - H_tau[reference], not bare rest mass.
- `HGT3595_5_em_poynting_once`: RETAINED_EXPLICIT_GUARD - J_H_total = J_matter + J_EM + J_Poynting + J_binding, with no hidden double count.
- `HGT3595_6_conditional_glue_theorem`: CONDITIONAL_ZERO_THEOREM_DERIVED - If d(Pi_M J_H)=0, H^2(E)=R[S2], Q_M=ell_M(Pi_M J_H)=M_source[W], R_perp=0, integral_boundary dB_zero=0, and EM/Poynting are included once, then Pi_M J_H = J_M_top + dB_zero and epsilon_PiM_parent=0.
- `HGT3595_7_current_MTS_verdict`: THEOREM_CONDITIONAL_WRONG_OBJECT_BOUND_ACTIVE - Current MTS has the theorem form but not the parent-owned worldtube/source-measure lock; epsilon_wrong_object stays active.

## Wrong-Object Residuals
- `WOR3595_0_total` / `R_wrong`: ACTIVE_NONCLAIM - Pi_M J_H - J_M_top - dB_zero
- `WOR3595_1_Q_label` / `R_Qlabel`: MAIN_BLOCKER - (ell_M(Pi_M J_H)-Q_M) omega_M_top
- `WOR3595_2_cohomology` / `R_perp`: CONDITIONAL_ZERO_OR_BOUND - non-mass cohomology/harmonic component of Pi_M J_H
- `WOR3595_3_boundary_exact` / `R_Bzero`: OPEN_BOUNDARY_BLOCKER - dB_zero with nonzero compact linking-surface flux
- `WOR3595_4_worldtube_measure` / `R_worldtube`: OPEN_MAIN_BLOCKER - M_source[W] - ell_M(Pi_M J_H)
- `WOR3595_5_extra_exchange` / `R_extra_exchange`: OPEN_EXCHANGE_BLOCKER - Pi_M dJ_extra + hidden/domain/nonEH/memory/range exchange
- `WOR3595_6_frame_species` / `R_frame_species`: OPEN_FRAME_WEP_BLOCKER - same-source-frame/species mismatch in J_H
- `WOR3595_7_em_once` / `R_EM_once`: OPEN_EM_GUARD - missing or double-counted EM/Poynting/binding contribution in J_H_total
- `WOR3595_8_calibration` / `R_calibration`: DOWNSTREAM_OPEN - M_top/Hilbert charge differs from Gauss/orbital GM

## Bound Rows
- `WPB3595_0_epsilon_Qlabel` / `epsilon_Qlabel`: MISSING_QM_HILBERT_DEFINITION - abs(ell_M(Pi_M J_H)-Q_M)/abs(M_H_ref)
- `WPB3595_1_epsilon_Rperp` / `epsilon_Rperp`: 0 if H2(E)=R[S2] and no nonmass class; otherwise missing norm - ||R_perp||_M/abs(M_H_ref)
- `WPB3595_2_epsilon_Bzero` / `epsilon_Bzero`: MISSING_BOUNDARY_ZERO_OR_CONSTANT_CALIBRATION - abs(integral_boundary dB_zero)/abs(M_H_ref)
- `WPB3595_3_epsilon_worldtube` / `epsilon_worldtube`: MISSING_DRESSED_SOURCE_MEASURE_LOCK - abs(M_source[W]-ell_M(Pi_M J_H))/abs(M_H_ref)
- `WPB3595_4_epsilon_extra_exchange` / `epsilon_extra_exchange`: MISSING_ZERO_OR_NUMERIC_CHANNEL_BOUNDS - abs(int_A Pi_M dJ_extra)/abs(M_H_ref)
- `WPB3595_5_epsilon_frame_species` / `epsilon_frame_species`: MISSING_SAME_SOURCE_FRAME_THEOREM - abs(R_frame_species)/abs(M_H_ref)
- `WPB3595_6_epsilon_EM_once` / `epsilon_EM_once`: MISSING_ONCE_ONLY_EM_STRESS_ACCOUNTING - abs(Pi_M[J_H_total-J_matter-J_EM-J_Poynting-J_binding])/abs(M_H_ref)
- `WPB3595_7_epsilon_wrong_object_total` / `epsilon_PiM_parent_wrong_object`: NOT_SCORE_READY_TOTAL - epsilon_Qlabel+epsilon_Rperp+epsilon_Bzero+epsilon_worldtube+epsilon_extra_exchange+epsilon_frame_species+epsilon_EM_once

## Promotion Gates
- `PROM3595_0_conditional_glue`: PASS_CONDITIONAL_THEOREM - de Rham/topological route is explicit but premises are not parent-certified
- `PROM3595_1_wrong_object_zero`: FAIL_CURRENT_CLAIM - Q_M/worldtube/Hilbert source lock remains open
- `PROM3595_2_bound_pack`: PASS_NONCLAIM - residual rows are source-ready but not numeric/score-ready
- `PROM3595_3_EM_guard`: OPEN_GUARDED - cannot omit EM stress from the source charge
- `PROM3595_4_no_GM_Newton_claim`: PASS_GUARD - Gauss/orbital calibration and PPN readout remain downstream

## Status
- `CONDITIONAL_HILBERT_TO_TOPO_GLUE_DERIVED_WRONG_OBJECT_BOUND_ACTIVE`: 3595 derives the exact conditional glue route: in a fixed S2 x I exterior with closed Hilbert mass current and H2(E)=R[S2], Pi_M J_H decomposes as ell_M(Pi_M J_H) omega_M_top + dB + R_perp. If Q_M is defined from the same dressed Hilbert/worldtube source, R_perp=0, boundary exact flux is zero, and EM/Poynting/binding are included once, then the topological charge is not the wrong object and epsilon_PiM_parent can vanish.
- Decision: do not promote source coupling; retain epsilon_PiM_parent_wrong_object until Q_M=ell_M(Pi_M J_H)=M_source[W] is parent-signed and component residuals are zero or bounded
- Still missing: parent-owned Q_M Hilbert definition, dressed worldtube source measure, zero exact boundary flux, no extra-current projection, same source frame/species theorem, EM/Poynting once-only source accounting, Gauss/orbital calibration, PPN source stability

## Validation
- `VAL3595_0_sources_exist`: PASS (all required 3595 source paths exist)
- `VAL3595_1_needles_found`: PASS (all selected 3595 source anchors found)
- `VAL3595_2_outputs_exist`: PASS (all pre-validation 3595 csv output files written)
- `VAL3595_3_csv_parse`: PASS (source_register:20; glue_theorem:8; wrong_object_residuals:9; bound_rows:8; promotion_gates:5; status:1; next_target:1; canonical_status:1)
- `VAL3595_4_glue_theorem_present`: PASS (conditional Hilbert/topological glue theorem row present)
- `VAL3595_5_wrong_object_total_present`: PASS (wrong-object residual decomposition includes total R_wrong)
- `VAL3595_6_bound_pack_complete`: PASS (wrong-object bound pack includes all required components)
- `VAL3595_7_wrong_object_claim_blocked`: PASS (wrong-object zero claim remains blocked)
- `VAL3595_8_no_claim_flags`: PASS (all generated physics rows remain nonclaim)
- `VAL3595_9_no_local_gr_claim`: PASS (measured-GM/Newton/PPN/local-GR claim guard is active)
- `VAL3595_10_next_target_selected`: PASS (3596 worldtube source-measure lock target selected)
- `VAL3595_11_generated_source_paths_exist`: PASS (every generated row source_path exists)
- `VAL3595_12_formalization_workbench_untouched`: PASS (no 3595 checkpoint output appears in formalization-workbench)

## Next target
- `NEXT3595_0` -> `3596-Y5-R2FR-worldtube-Hilbert-source-measure-lock-or-wrong-object-input-fill.md`
- Objective: prove Q_M=ell_M(Pi_M J_H)=M_source[W] as a dressed Hilbert/Hamiltonian source measure including EM/Poynting/binding once, or fill source-ready epsilon_Qlabel/epsilon_worldtube/epsilon_EM_once rows
