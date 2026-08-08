# 3574 - Topological mass-current origin or Meff drift source row

## Verdict
3574 gets a real step forward, not just another missing-list: a closed topological mass current is easy to write, but the exact obstruction is now named.

`J_M^top := Q_M omega_M^top + dB_M` gives `dJ_M^top=0` if the parent action owns `Q_M`, `omega_M^top`, and the exterior class.  The decisive equality is

`Pi_M J_H = J_M^top + dB_zero + R_eq`.

Therefore, in the closed-topological branch, `d(Pi_M J_H)=dR_eq`.  So topological closure only becomes Hilbert/Newton source closure if `R_eq=0` or at least has zero annulus and compact-boundary flux.  Current corpus does not prove that.

This is not a dead end.  It sharpens the coupling hunt: the missing object is the same-source glue `Q_M = integral_W J_H[tau] = B_xi/G_ref`, with boundary, Poynting/wave, extra-sector, and calibration terms either zero or source-bounded.

## Generated outputs
- `source_register`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3574_SOURCE_REGISTER.csv`
- `topological_origin`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3574_TOPOLOGICAL_MASS_CURRENT_ORIGIN_ATTEMPT.csv`
- `equality_gate`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3574_JMTOP_EQUALS_PIMJH_GATE.csv`
- `drift_source_rows`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3574_MEFF_DRIFT_SOURCE_ROWS.csv`
- `activation_gates`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3574_ACTIVATION_GATES.csv`
- `decision_ledger`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3574_DECISION_LEDGER.csv`
- `status`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3574_STATUS.csv`
- `next_target`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3574_NEXT_TARGET.csv`
- `canonical_status`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_topological_mass_current_status.csv`
- `validation`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_3574_VALIDATION.csv`

## Topological current origin
- `TOP3574_0_candidate_current`: J_M^top := Q_M omega_M^top + dB_M, with d omega_M^top=0, dQ_M=0 in the exterior, and d^2B_M=0. (FORMAL_CLOSED_CURRENT_AVAILABLE)
- `TOP3574_1_parent_domain_selector`: The S2/worldtube class linking the compact source must be selected before readout and not by fitted orbital GM. (NOT_PARENT_SIGNED)
- `TOP3574_2_same_source_charge`: Q_M must be defined from the same observed-frame Hilbert source worldtube as J_H, not introduced as an independent cohomology label. (KEY_BLOCKER_NOT_DERIVED)
- `TOP3574_3_first_class_origin`: A_M or Lambda_M may impose J_M^top-Pi_M J_H-dB_zero=0 only if its constraint is first-class/topological before Newton fitting. (CLOSURE_ONLY_IF_NOT_INDEPENDENT)
- `TOP3574_4_boundary_silence`: The exact term dB_zero and owner currents must have zero compact-boundary mass flux or a declared universal constant calibration. (FAIL_OPEN)
- `TOP3574_5_exchange_silence`: Pi_M dJ_extra must vanish for hidden, domain, non-EH, memory, range, Poynting, boundary, and source-owner flux channels. (NOT_DERIVED)
- `TOP3574_6_calibration_guard`: Even after closure, Q_M or int_S Pi_M J_H must reduce to EH/Poisson/Gauss/orbital mass with constant universal G_ref. (NOT_PARENT_DERIVED)

## Equality gate
- `EQ3574_0_decomposition` `R_eq`: Pi_M J_H = J_M^top + dB_zero + R_eq (EXACT_DEFINITION)
- `EQ3574_1_closure_implication` `dR_eq`: d(Pi_M J_H)=dJ_M^top + dR_eq = dR_eq when dJ_M^top=0 (DERIVED_IF_R_EQ_ZERO)
- `EQ3574_2_wrong_object_test` `epsilon_Req_annulus`: J_M^top closed but R_eq != 0 (FAILS_LOCAL_NEWTON_SOURCE)
- `EQ3574_3_worldtube_glue_route` `Z_worldtube_source_glue`: Q_M := integral_W J_H[tau] and J_M^top := PD(W_source) Q_M before readout (PROMISING_CONDITIONAL_NOT_SIGNED)
- `EQ3574_4_hamiltonian_route` `Delta_cal`: B_xi/G_ref = Q_M = M_eff[Pi_M J_H] (DOWNSTREAM_NOT_DERIVED)
- `EQ3574_5_poynting_flux_guard` `epsilon_Poynting_worldtube`: epsilon_Poynting_worldtube enters R_eq or mu_extra unless its compact source-worldtube flux is zero or bounded. (BOUND_ROW_PRESENT_INPUTS_MISSING)
- `EQ3574_6_verdict` `Z_top_to_Hilbert`: Z_top_to_Hilbert := Z_closed_top * Z_same_source * Z_domain * Z_boundary * Z_exchange = 0 in the current corpus (EQUALITY_NOT_CLAIMED)

## Drift/source rows
- `MEFF3574_0_R_eq_annulus` `epsilon_Req_annulus`: epsilon_Req_annulus := |int_A dR_eq|/|M_eff| with Pi_M J_H=J_M^top+dB_zero+R_eq (FORMULA_READY_PARENT_INTEGRAL_MISSING)
- `MEFF3574_1_B_zero_flux` `epsilon_Bzero_flux`: epsilon_Bzero_flux := |int_boundary dB_zero|/|M_eff| (FORMULA_READY_BOUNDARY_INPUT_MISSING)
- `MEFF3574_2_source_worldtube_glue` `epsilon_Wsource_glue`: epsilon_Wsource_glue := |Q_M - integral_W J_H[tau]|/|M_eff| (FORMULA_READY_SOURCE_MEASURE_MISSING)
- `MEFF3574_3_Poynting_worldtube` `epsilon_Poynting_worldtube`: epsilon_Poynting_worldtube := |int_W Pi_M dJ_Poynting|/|M_eff| or bounded by source-worldtube collar flux norm (BOUND_FORMULA_READY_INPUTS_MISSING)
- `MEFF3574_4_dlnMeff_dt` `dln_Meff_dt`: dln_Meff_dt = D_t ln int_S Pi_M J_H = D_t ln int_S (J_M^top+dB_zero+R_eq) (LIVE_FROM_3573_REFINED_BY_REQ)
- `MEFF3574_5_partial_r_ln_mu_obs` `partial_r_ln_mu_obs`: partial_r ln mu_obs = partial_r ln G_eff + partial_r ln M_eff[R_eq,B_zero,J_extra] + partial_r ln(1+epsilon_mu) (LIVE_FROM_3573_REFINED_BY_REQ)
- `MEFF3574_6_Delta_cal` `Delta_cal`: Delta_cal := M_eff[Pi_M J_H] - M_Gauss_orbital (CALIBRATION_GATE_STILL_OPEN)

## Activation gates
- `GATE3574_0_sources`: PASS (all required 3574 source paths exist)
- `GATE3574_1_closed_topological_current`: PASS_FORMULA_NONCLAIM (dJ_M^top=0 follows for closed parent topological data, but physical source identity is separate)
- `GATE3574_2_same_source_charge`: FAIL_CURRENT_CLAIM (Q_M is not parent-signed as the same source-worldtube Hilbert charge)
- `GATE3574_3_equality_residual`: FAIL_CURRENT_CLAIM (Pi_M J_H=J_M^top+dB_zero+R_eq is written, but R_eq=0 is not derived)
- `GATE3574_4_boundary_exchange`: FAIL_CURRENT_CLAIM (B_zero, extra channels, and Poynting worldtube flux are unbounded or unsigned)
- `GATE3574_5_drift_rows`: PASS_NONCLAIM (R_eq/B_zero/worldtube/Poynting/dlnMeff rows generated as non-claim source inputs)
- `GATE3574_6_Newton_claim`: FAIL_CURRENT_CLAIM (constant G_ref and Poisson/Gauss/orbital calibration are still downstream gates)
- `GATE3574_7_local_GR_claim`: FAIL_CURRENT_CLAIM (no PPN/local-GR promotion follows from a closed wrong object)

## Decisions
- `DEC3574_0_topological_current_kept`: keep the topological current as a real candidate, not a discarded route -> It remains useful if future parent action defines Q_M from the same Hilbert source worldtube.
- `DEC3574_1_no_wrong_object_promotion`: do not promote J_M^top closure to Newton/source closure -> R_eq is now the named failure variable rather than a vague missing coupling.
- `DEC3574_2_Poynting_retained`: retain Poynting/wave flux as a source-owner residual -> This widens the search instead of trying once and calling it dead.
- `DEC3574_3_next_target`: next derive R_eq=0 through source-worldtube/Hamiltonian glue or start filling residual rows -> 3575 should attack the source-worldtube/Hamiltonian glue chain directly, then fall back to numeric/source rows if it fails.

## Status
- `TOPOLOGICAL_CURRENT_FORMAL_CLOSURE_FOUND_EQUALITY_NOT_CLAIMED_REQ_ROWS_ACTIVE`: A closed topological mass current can be written, and the exact decomposition Pi_M J_H=J_M^top+dB_zero+R_eq shows precisely what must vanish for topological closure to become Hilbert/source closure.

## Validation
- `VAL3574_0_sources_exist`: PASS (all required 3574 source paths exist)
- `VAL3574_1_required_needles_found`: PASS (all selected 3574 source-current needles found)
- `VAL3574_2_outputs_exist`: PASS (all pre-validation 3574 output files written)
- `VAL3574_3_csv_parse`: PASS (source_register:25; topological_origin:7; equality_gate:7; drift_source_rows:7; activation_gates:8; decision_ledger:4; status:1; next_target:1; canonical_status:1)
- `VAL3574_4_closed_top_current_present`: PASS (formal closed topological current row present)
- `VAL3574_5_Req_decomposition_present`: PASS (R_eq decomposition present)
- `VAL3574_6_closure_implication_present`: PASS (d(Pi_M J_H)=dR_eq implication present)
- `VAL3574_7_residual_rows_present`: PASS (R_eq/boundary/Poynting/Meff residual rows present)
- `VAL3574_8_equality_not_claimed`: PASS (R_eq zero remains unclaimed)
- `VAL3574_9_next_target_selected`: PASS (source-worldtube/Hamiltonian glue next target selected)
- `VAL3574_10_no_claim_flags`: PASS (all generated physics rows remain nonclaim)
- `VAL3574_11_generated_source_paths_exist`: PASS (every generated row source_path exists)
- `VAL3574_12_formalization_workbench_untouched`: PASS (no 3574 checkpoint output appears in formalization-workbench)

## Next target
- `3575-Y5-R2FR-Req-zero-source-worldtube-Hamiltonian-glue-or-residual-fill.md`
- Objective: try to prove R_eq=0 by deriving the same-object chain Q_M=integral_W J_H[tau]=B_xi/G_ref in one parent branch; if not, fill source-backed R_eq/B_zero/Poynting/Meff drift rows
