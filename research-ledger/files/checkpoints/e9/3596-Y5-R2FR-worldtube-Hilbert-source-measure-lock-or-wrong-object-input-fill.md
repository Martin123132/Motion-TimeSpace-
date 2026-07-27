# 3596 - Worldtube Hilbert source measure lock or wrong-object input fill

## Verdict
3596 locks the only non-cheat definition: `Q_M` can stop being a wrong topological label only if it is defined as `ell_M(Pi_M J_H_total)=M_source^dress[W;tau]` before orbital readout.

This conditionally kills the independent-label failure, but not the whole source-coupling problem.  `H_tau` integrability, reference/source support, same frame/tau, extra-sector silence, and especially EM/Poynting/binding once-only accounting remain live.

## Source-Measure Lock
- `WSL3596_0_target`: TARGET_IMPORTED - Lock Q_M=ell_M(Pi_M J_H)=M_source[W] as a dressed Hilbert/Hamiltonian source measure, or retain epsilon_Qlabel/epsilon_worldtube/epsilon_EM_once.
- `WSL3596_1_dressed_definition`: DEFINITION_LOCK_CONDITIONAL - M_source^dress[W;tau] := H_tau[S_outer] - H_tau[S_ref]
- `WSL3596_2_Hilbert_source_scalar`: CONDITIONAL_Q_LABEL_ZERO - Q_M := ell_M(Pi_M J_H_total) := M_source^dress[W;tau]
- `WSL3596_3_constraint_bridge`: CONDITIONAL_PARENT_TRANSFER - delta H_tau = integral_W T_H,total(n,tau) + boundary/reference terms + Delta_nonEH + Delta_symp + Delta_extra + Delta_frame
- `WSL3596_4_EM_once`: OPEN_CRITICAL_GUARD - J_H_total = J_matter + J_EM + J_Poynting + J_binding + improvements_exact_zero
- `WSL3596_5_readout_order`: ANTI_TAUTOLOGY_GUARD - J_parent := delta S/delta e_obs and T_parent := delta S/delta g before readout; orbital GM cannot define Q_M.
- `WSL3596_6_conditional_lock_theorem`: CONDITIONAL_ZERO_THEOREM_DERIVED - If H_tau is parent integrable, tau/source frame/reference are fixed, Pi_M is fixed before variation, extra sectors have zero mass charge, and J_H_total includes EM/Poynting/binding once, then Q_M=ell_M(Pi_M J_H_total)=M_source^dress[W;tau].
- `WSL3596_7_current_MTS_verdict`: PARTIAL_LOCK_REMAINING_INPUTS_ACTIVE - The definition can be adopted as the only non-cheat branch, but current MTS has not parent-signed H_tau integrability, same source frame, extra-sector silence, EM once-only accounting, or Gauss/orbital calibration.

## Residual Decomposition
- `WMR3596_0_total` / `R_worldtube_total`: ACTIVE_NONCLAIM - M_source^dress[W;tau] - ell_M(Pi_M J_H_total)
- `WMR3596_1_Qlabel` / `R_Qlabel`: CONDITIONAL_ZERO_IF_DEFINITION_ADOPTED - Q_M - ell_M(Pi_M J_H_total)
- `WMR3596_2_Htau_integrability` / `R_Htau`: OPEN_BOUND_REQUIRED - curl(delta H_tau) or nonintegrable boundary symplectic term
- `WMR3596_3_reference` / `R_ref`: OPEN_BOUND_REQUIRED - D_X H_ref/(H_tau-H_ref)
- `WMR3596_4_worldtube_support` / `R_W`: OPEN_BOUND_REQUIRED - D_X ln W_source - D_X ln closure(supp J_H[tau])
- `WMR3596_5_frame_tau` / `R_frame_tau`: OPEN_FRAME_BLOCKER - source/readout frame or tau mismatch
- `WMR3596_6_extra_charge` / `R_extra_charge`: OPEN_MTS_TRANSFER_BLOCKER - Delta_nonEH + Delta_symp + Delta_extra + Delta_frame
- `WMR3596_7_EM_once` / `R_EM_once`: OPEN_CRITICAL_GUARD - Pi_M[J_H_total - J_matter - J_EM - J_Poynting - J_binding]
- `WMR3596_8_Gref_units` / `R_Gref_units`: OPEN_PRODUCT_LOCK - mismatch in G_ref, ell_J, action-line, or source units
- `WMR3596_9_calibration_downstream` / `R_calibration`: DOWNSTREAM_OPEN - M_source^dress - M_Gauss_orbital

## Input Rows
- `WIN3596_0_epsilon_Qlabel` / `epsilon_Qlabel`: CONDITIONAL_ZERO_BRANCH - abs(Q_M-ell_M(Pi_M J_H_total))/abs(M_H_ref)
- `WIN3596_1_epsilon_worldtube` / `epsilon_worldtube`: BOUND_REQUIRED - abs(M_source^dress[W;tau]-ell_M(Pi_M J_H_total))/abs(M_H_ref)
- `WIN3596_2_epsilon_Htau` / `epsilon_Htau_integrability`: BOUND_REQUIRED - abs(curl(delta H_tau))/abs(M_H_ref)
- `WIN3596_3_epsilon_ref` / `epsilon_reference_source_blind`: BOUND_REQUIRED - abs(D_X H_ref)/abs(H_tau-H_ref)
- `WIN3596_4_epsilon_W` / `epsilon_worldtube_support`: BOUND_REQUIRED - abs(D_X ln W_source - D_X ln closure(supp J_H[tau]))
- `WIN3596_5_epsilon_frame_tau` / `epsilon_frame_tau`: BOUND_REQUIRED - abs(R_frame_tau)
- `WIN3596_6_epsilon_EM_once` / `epsilon_EM_once`: BOUND_REQUIRED_CRITICAL - abs(Pi_M[J_H_total-J_matter-J_EM-J_Poynting-J_binding])/abs(M_H_ref)
- `WIN3596_7_epsilon_Gref_units` / `epsilon_Gref_units`: BOUND_REQUIRED - abs(R_Gref_units)
- `WIN3596_8_epsilon_source_measure_total` / `epsilon_source_measure_total`: TOTAL_BOUND_BRANCH_ACTIVE - sum of epsilon_Qlabel, epsilon_worldtube, epsilon_Htau, epsilon_ref, epsilon_W, epsilon_frame_tau, epsilon_EM_once, epsilon_Gref_units

## Promotion Gates
- `PROM3596_0_Qlabel`: PASS_CONDITIONAL_ZERO_BRANCH - zero only if Q_M is parent-defined as ell_M(Pi_M J_H_total)
- `PROM3596_1_worldtube_lock`: FAIL_CURRENT_CLAIM - H_tau/reference/support/frame/extra-sector premises remain open
- `PROM3596_2_EM_once`: FAIL_CURRENT_CLAIM - critical Poynting/source-accounting row remains open
- `PROM3596_3_bound_pack`: PASS_NONCLAIM - inputs are source-ready but not numeric/score-ready
- `PROM3596_4_no_Newton_claim`: PASS_GUARD - Gauss/orbital calibration remains downstream

## Status
- `QM_LABEL_CONDITIONALLY_ZERO_WORLDTUBE_EM_ONCE_INPUTS_ACTIVE`: 3596 locks the non-cheat definition: Q_M may be identified with ell_M(Pi_M J_H_total) only when M_source[W] is the dressed Hamiltonian/Noether source charge before orbital readout. This conditionally kills the independent topological-label failure, but current MTS still lacks parent-signed H_tau integrability, reference/source support, same frame/tau, extra-sector charge silence, and EM/Poynting/binding once-only accounting.
- Decision: adopt the dressed-source definition as the only viable branch, keep epsilon_worldtube and epsilon_EM_once active, and do not claim Newton/PPN/local-GR until Gauss/orbital calibration and EM source accounting are closed
- Still missing: H_tau integrability, H_ref source-blindness, worldtube support selector, same source frame/tau, extra-sector charge silence, EM/Poynting/binding once-only Hilbert source map, G_ref/ell_J units lock, Gauss/orbital calibration

## Validation
- `VAL3596_0_sources_exist`: PASS (all required 3596 source paths exist)
- `VAL3596_1_needles_found`: PASS (all selected 3596 source anchors found)
- `VAL3596_2_outputs_exist`: PASS (all pre-validation 3596 csv output files written)
- `VAL3596_3_csv_parse`: PASS (source_register:21; source_measure_lock:8; residual_decomposition:10; input_rows:9; promotion_gates:5; status:1; next_target:1; canonical_status:1)
- `VAL3596_4_definition_lock_present`: PASS (dressed source definition lock row present)
- `VAL3596_5_Qlabel_conditional_zero`: PASS (epsilon_Qlabel has conditional-zero branch)
- `VAL3596_6_worldtube_EM_inputs_active`: PASS (worldtube and EM once inputs are active)
- `VAL3596_7_EM_once_claim_blocked`: PASS (EM/Poynting once-only claim remains blocked)
- `VAL3596_8_no_claim_flags`: PASS (all generated physics rows remain nonclaim)
- `VAL3596_9_no_local_gr_claim`: PASS (measured-GM/Newton/PPN/local-GR claim guard is active)
- `VAL3596_10_next_target_selected`: PASS (3597 EM/Poynting source accounting target selected)
- `VAL3596_11_generated_source_paths_exist`: PASS (every generated row source_path exists)
- `VAL3596_12_formalization_workbench_untouched`: PASS (no 3596 checkpoint output appears in formalization-workbench)

## Next target
- `NEXT3596_0` -> `3597-Y5-R2FR-EM-Poynting-Hilbert-source-accounting-or-bound.md`
- Objective: prove that EM stress, Poynting flux, and binding energy enter J_H_total exactly once in the source-measure branch, or fill epsilon_EM_once/Phi_EM_rad/source-accounting bound rows
