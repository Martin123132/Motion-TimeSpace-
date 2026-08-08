# 3577 - Htau/Href q-basic reference lock or source residual first fill

## Verdict
3577 narrows the source-denominator blocker.  In the private single-charge branch, `H_ref` is now treated as a parent-fixed reference selected before source/orbit/PPN readout, so `D_source H_ref=0` and the reference-laundering part of `epsilon_Href_lock` is internally zero.

But `H_tau` itself is not promoted.  The one-form route is exact only if `alpha_tau` is closed and `Theta_MTS/Q_tau^MTS/tau/surface/symplectic` data are parent-owned.  Those pieces are still retained.

The resulting first residual row is now sharper: `epsilon_Href_lock <= epsilon_Htau_curl + epsilon_tau_surface_frame + epsilon_symplectic_boundary + epsilon_MHref_qbasic`.  The positive denominator route is also explicit: `M_H_ref >= M_EH(1-epsilon_abs)>0`, but `M_EH` and `Delta_i` rows are still missing.

## Generated outputs
- `source_register`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3577_SOURCE_REGISTER.csv`
- `reference_lock`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3577_HREF_REFERENCE_LOCK.csv`
- `htau_qbasic`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3577_HTAU_QBASIC_REFERENCE_THEOREM.csv`
- `denominator_route`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3577_MHREF_POSITIVE_DENOMINATOR_ROUTE.csv`
- `epsilon_Href_rows`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3577_EPSILON_HREF_LOCK_ROWS.csv`
- `activation_gates`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3577_ACTIVATION_GATES.csv`
- `decision_ledger`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3577_DECISION_LEDGER.csv`
- `status`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3577_STATUS.csv`
- `next_target`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3577_NEXT_TARGET.csv`
- `canonical_status`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_Htau_Href_reference_lock_status.csv`
- `validation`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_3577_VALIDATION.csv`

## Reference lock
- `REF3577_0_fixed_reference_rule`: H_ref := H_tau[g_ref,e_ref,tau_ref,S_ref] where g_ref/e_ref/tau_ref/S_ref are selected by the parent branch before source/orbit/PPN scoring. (INTERNAL_CANDIDATE_SIGNED_REFERENCE_DERIVATIVE_SILENCE)
- `REF3577_1_no_GM_laundering`: partial_{GM_obs,M_fit,M_H_ref,kappa_A,composition_A} H_ref=0 (FORBIDDEN_INPUT_RULE_ADOPTED)
- `REF3577_2_surface_class`: S_outer, S_inner and S_ref remain in one fixed linked boundary class with no source/radius/orbit retuning. (INTERNAL_CANDIDATE_SIGNED_IF_SURFACE_CLASS_FIXED)
- `REF3577_3_reference_component`: epsilon_ref_source := |D_X H_ref|/M_H_ref_lower (CANDIDATE_ZERO_OR_RETAINED_ROW)

## Htau q-basic theorem
- `HTQ3577_0_alpha_definition`: alpha_tau(delta Phi)=int_S(delta Q_tau^MTS-i_tau Theta_MTS(delta Phi))-delta H_ref (EXACT_CONDITIONAL_DEFINITION)
- `HTQ3577_1_curl_law`: d_F alpha_tau=-int_S i_tau omega_MTS + C_tau + C_S + C_ref (DERIVED_ACCOUNTING_IDENTITY_REFERENCE_TERM_NARROWED)
- `HTQ3577_2_qbasic_theorem`: If alpha_tau is closed and all ingredients factor through q/e_obs/tau, then H_tau=Hbar_tau(q(Phi)). (EXACT_CONDITIONAL_THEOREM_NOT_LIVE)
- `HTQ3577_3_MHref_qbasic`: If H_tau=Hbar_tau(q(Phi)) and H_ref=Hbar_ref(q(Phi)), then M_H_ref=H_tau-H_ref descends through q. (EXACT_CONDITIONAL_THEOREM_NOT_LIVE)
- `HTQ3577_4_live_blocker`: H_ref derivative silence is internally signed; H_tau exactness/q-basicness and positive M_H_ref are not. (REFERENCE_LOCK_NARROWED_HTAU_DENOMINATOR_RETAINED)

## Denominator route
- `DEN3577_0_exact_MHref` `M_H_ref`: M_H_ref := G_ref^-1*(H_tau[S_outer]-H_ref) (DEFINITION_READY_VALUE_MISSING)
- `DEN3577_1_lower_bound` `M_H_ref_lower`: M_H_ref >= M_EH*(1-epsilon_abs), epsilon_abs=sum_i |Delta_i|/(G_ref*M_EH) (DERIVED_LOWER_BOUND_LAW_COMPONENTS_MISSING)
- `DEN3577_2_EH_comparator` `M_EH`: EH/Komar/ADM/Gauss reference mass in the same tau/coframe/source branch (SOURCE_BACKED_VALUE_MISSING)
- `DEN3577_3_epsilon_abs` `epsilon_abs`: epsilon_abs := (|Delta_H_curl|+|Delta_ref|+|Delta_tau_surface_frame|+|Delta_symp_boundary|+|Delta_extra|)/(G_ref*M_EH) (COMPONENT_ENVELOPE_NARROWED_NOT_FILLED)
- `DEN3577_4_acceptance` `denominator_acceptance`: Accept exact positive M_H_ref or source-backed M_H_ref_lower>0; reject orbital-GM denominator import. (ACCEPTANCE_RULE_ACTIVE)

## Epsilon Href rows
- `EHL3577_0_reference_zero` `epsilon_ref_source`: epsilon_ref_source := |D_X H_ref|/M_H_ref_lower = 0 in fixed-reference candidate branch (CANDIDATE_ZERO_INTERNAL_NONCLAIM)
- `EHL3577_1_Htau_curl` `epsilon_Htau_curl`: Delta_H_curl_bound/M_H_ref_lower, with Delta_H_curl_bound <= A_F sup_BF|-int_S i_tau omega_MTS + C_tau + C_S| (FORMULA_READY_COMPONENT_INPUTS_MISSING)
- `EHL3577_2_tau_surface_frame` `epsilon_tau_surface_frame`: (|C_tau|+|C_S|+|C_frame|)/M_H_ref_lower (MISSING_TAU_SURFACE_FRAME_LOCK_OR_BOUND)
- `EHL3577_3_symplectic_boundary` `epsilon_symplectic_boundary`: |int_S i_tau omega_extra + Delta_symp|/M_H_ref_lower (MISSING_SYMPLECTIC_BOUNDARY_ZERO_OR_BOUND)
- `EHL3577_4_qbasic_mass_leak` `epsilon_MHref_qbasic`: |D_X M_H_ref|/M_H_ref_lower <= (|D_X H_tau|+|D_X H_ref|)/M_H_ref_lower (NARROWED_TO_DX_HTAU_AFTER_REFERENCE_ZERO)
- `EHL3577_5_total` `epsilon_Href_lock`: epsilon_Href_lock <= epsilon_Htau_curl + epsilon_tau_surface_frame + epsilon_symplectic_boundary + epsilon_MHref_qbasic (FIRST_RETAINED_ROW_FORMULA_READY_VALUES_MISSING)

## Gates
- `GATE3577_0_sources`: PASS (all required 3577 source paths exist)
- `GATE3577_1_Href`: PASS_INTERNAL_CANDIDATE (source/readout derivative of H_ref is zero if the parent-fixed reference selector is adopted)
- `GATE3577_2_Htau`: FAIL_CURRENT_CLAIM (theta/Q_tau/curl/symplectic/tau/surface terms are not all zero-derived)
- `GATE3577_3_MHref_positive`: FAIL_CURRENT_CLAIM (lower-bound law exists but M_EH and Delta_i rows are unfilled)
- `GATE3577_4_epsilon_Href`: PASS_NONCLAIM (epsilon_Href_lock now has narrowed formula, units and components)
- `GATE3577_5_Newton`: PARTIAL_NOT_PROMOTED (source denominator blocker narrowed but not closed)
- `GATE3577_6_local_GR`: FAIL_CURRENT_CLAIM (PPN/R10/clock/orbital residual vector remains downstream)

## Decisions
- `DEC3577_0_reference_signed`: sign fixed-reference derivative silence internally -> Reference leakage is removed from epsilon_Href_lock in this private branch.
- `DEC3577_1_Htau_not_signed`: do not sign H_tau exactness yet -> H_tau terms stay in the residual envelope.
- `DEC3577_2_denominator_route`: use lower-bound route instead of orbital-GM import -> Next work should derive/fill M_EH and Delta_i rows rather than using fitted GM.
- `DEC3577_3_next_target`: attack H_tau curl/component vector next -> 3578 should derive or fill the H_tau curl component vector.

## Status
- `HREF_REFERENCE_DERIVATIVE_SILENCE_SIGNED_INTERNAL_HTAU_DENOMINATOR_RETAINED`: Fixed H_ref derivative silence is internally signed in the single-charge branch, so epsilon_Href_lock is narrowed to H_tau curl, tau/surface/frame, symplectic boundary and q-basic denominator leakage terms.

## Validation
- `VAL3577_0_sources_exist`: PASS (all required 3577 source paths exist)
- `VAL3577_1_required_needles_found`: PASS (all selected Htau/Href needles found)
- `VAL3577_2_outputs_exist`: PASS (all pre-validation 3577 output files written)
- `VAL3577_3_csv_parse`: PASS (source_register:23; reference_lock:4; htau_qbasic:5; denominator_route:5; epsilon_Href_rows:6; activation_gates:7; decision_ledger:4; status:1; next_target:1; canonical_status:1)
- `VAL3577_4_reference_zero_present`: PASS (fixed-reference derivative silence row present)
- `VAL3577_5_Htau_not_claimed`: PASS (H_tau denominator remains retained)
- `VAL3577_6_lower_bound_route_present`: PASS (positive denominator lower-bound route present)
- `VAL3577_7_epsilon_Href_formula_present`: PASS (epsilon_Href_lock narrowed formula present)
- `VAL3577_8_reference_gate_passes_only_internal`: PASS (H_ref pass is internal candidate only)
- `VAL3577_9_denominator_not_promoted`: PASS (positive denominator remains unclaimed)
- `VAL3577_10_next_target_selected`: PASS (Htau curl next target selected)
- `VAL3577_11_no_claim_flags`: PASS (all generated physics rows remain nonclaim)
- `VAL3577_12_generated_source_paths_exist`: PASS (every generated row source_path exists)
- `VAL3577_13_formalization_workbench_untouched`: PASS (no 3577 checkpoint output appears in formalization-workbench)

## Next target
- `3578-Y5-R2FR-Htau-curl-component-zero-or-first-bound-vector.md`
- Objective: derive H_tau field-space curl zero for the single-charge branch by extracting theta/Q_tau/symplectic/tau/surface components, or fill the first Delta_H_curl_bound component vector
