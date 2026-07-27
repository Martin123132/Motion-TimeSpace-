# 3612 - Jq matter subcomponent zero or xi_q source input

## Verdict
3612 takes the first real bite out of `J_q^matter_bulk`: the EM/Poynting/binding leg is no longer a vague coupling hole.

The rule is now explicit.  Minimal bound EM fields and Poynting bookkeeping are inside the total Hilbert stress/source mass when the observed Hodge, current normalization, Maxwell action normalization, stationary boundary, and readout order are common-owner clauses.  If any of those clauses fail, the term is not waved away; it becomes an absolute residual vector.

`||J_q^EM/Poynting||_* <= C_EM,g||D_{v_q}e_obs|| + C_H||Delta_Hodge_EM|| + C_lambda|D_{v_q}ln lambda_A| + |Phi_EM_rad|/(G_ref M_H) + C_XF2|C_XF2| + C_readout|C_EM_readout| + C_NH||J_NH||`

No local-GR, Newton, Maxwell, R10, clock, or PPN claim follows yet.  But this is not circling: a named subcomponent has been converted into a theorem-zero-or-bound law.

## J_q Matter Subcomponent Attack
- `JQA3612_0_selected_subcomponent` / `J_readout_nonH_bound / EM-Poynting part of J_q^matter_bulk`: SELECTED_FOR_ATTACK - EM/Poynting/binding can either be inside total Hilbert stress or become a non-Hilbert/boundary flux residual
- `JQA3612_1_Hilbert_absorption` / `ordinary bound EM fields`: EXACT_CONDITIONAL_ZERO_ROUTE - minimal Maxwell fields varied on the observed geometry contribute to T_H and M_H; they are not an extra q-source
- `JQA3612_2_flux_residual` / `radiative/background Poynting flux`: BOUND_COMPONENT_RETAINED - net Poynting flux through the local exterior boundary is not killed by Hilbert absorption; it is a boundary/time-hair residual
- `JQA3612_3_Hodge_gate` / `EM Hodge/coframe mismatch`: ZERO_OR_BOUND_GATE_IMPORTED - Poynting only uses the same local geometry as gravity if *_EM=*_obs[e_obs(q)] or every constitutive mismatch is bounded
- `JQA3612_4_normalization_gate` / `Maxwell action normalization and alpha`: CALIBRATED_BASELINE_WITH_ACTIVE_BRANCH_BOUND - local baseline may carry alpha as a calibrated universal constant; nonzero C_XF2 must be scored, not hidden in the source mass
- `JQA3612_5_first_subcomponent_verdict` / `J_q^EM/Poynting sub-bound`: SUCCESS_GATE_FILLED_SOURCE_BOUND_NONCLAIM - EM/Poynting is now either conditionally zero inside total Hilbert stress or retained as an explicit no-cancellation residual vector

## EM / Poynting Closure
- `EPC3612_0_identity` / `Poynting is stress flux`: EXACT_STANDARD_IDENTITY_CONDITIONAL_ON_OBSERVED_HODGE - `S_Poynting^i = -h^i_mu T_EM^{mu nu} u_nu`
- `EPC3612_1_bound_fields` / `stationary bound EM fields`: CONDITIONAL_ZERO_INSIDE_MH - `Delta M_EM = integral_Sigma T_EM(u,u) dV_obs; no separate epsilon_EM_bound if same M_H denominator is used`
- `EPC3612_2_exchange` / `matter-EM Lorentz exchange`: CONDITIONAL_ZERO_IN_TOTAL_HILBERT_STRESS - `nabla_mu T_EM^{mu nu}=-F^{nu lambda}J_lambda; nabla_mu T_matter^{mu nu}=+F^{nu lambda}J_lambda`
- `EPC3612_3_radiative_flux` / `radiative/background flux`: RETAINED_BOUND_ROW - `B_EM_rad := |integral_boundary S_Poynting dot n dA|/(G_ref M_H)`
- `EPC3612_4_constitutive` / `Hodge/constitutive mismatch`: RETAINED_BOUND_ROW - `B_Hodge := C_H||*_EM-*_obs[e_obs(q)]|| plus principal/skewon/axion/hidden/readout sub-bounds`
- `EPC3612_5_action_scale` / `w_EM / C_XF2 normalization`: RETAINED_BOUND_ROW - `B_EM_norm := C_lambda|D_{v_q}ln lambda_A| + C_XF2|C_XF2|`
- `EPC3612_6_closure_rule` / `usable local branch rule`: EXACT_CONDITIONAL_RULE_NOT_CURRENT_CLAIM - `J_q^EM/Poynting=0 iff Delta_Hodge_EM=C_XF2=D_{v_q}ln lambda_A=Phi_EM_rad=C_EM_readout=J_NH=0 and D_{v_q}e_obs=0`

## Source-Weight Reduction
- `SWR3612_0_source_weight_slot` / `J_source_weight_bound`: THEOREM_STACK_IMPORTED_NOT_PARENT_SIGNED - source-only species weights are conditionally excluded by typed matter constructor plus connected density-line naturality
- `SWR3612_1_common_scale` / `w_common`: RECLASSIFIED_NOT_ZERO - a common action/source scale is not a composition source charge but can still drift G_eff/source calibration
- `SWR3612_2_prevariation_countermodel` / `prevariation_weight`: NO_GO_GUARD_RETAINED - Ward identities do not remove source weights that are already present in S_matter before variation
- `SWR3612_3_nonHilbert_bypass` / `nonHilbert_source_bypass`: PARALLEL_BOUND_GATE_RETAINED - ordinary matter functor descent does not kill independent non-Hilbert active source currents
- `SWR3612_4_product_lock` / `ell_J/source denominator`: DENOMINATOR_GATE_CONNECTED - source coupling cannot be judged from source weights alone; Pi_M, H_tau, frame and units sit in the same product gate

## xi_q Parallel Audit
- `XIP3612_0_parallel_xi_q` / `xi_q/H_AB source row`: NO_NEW_OWNER_FOUND - 3612 did not find a parent-owned xi_q, H_AB positivity, q-normal, self-adjoint domain, or boundary/no-flux source row beyond the 3611 contract.

## Decision Gates
- `DEC3612_0_em_poynting` / `EM/Poynting subcomponent`: ADVANCED - Poynting is either absorbed into total Hilbert stress under exact common-owner clauses or retained as explicit boundary/Hodge/normalization/readout residuals.
- `DEC3612_1_source_weight` / `source-weight subcomponent`: NARROWED - species source weights reduce to typed-domain, density-line and no-Hom signatures, while common-scale and non-Hilbert bypass remain active.
- `DEC3612_2_xi_q` / `xi_q/H_AB parallel route`: NO_PROGRESS_TO_OWNER - No new xi_q/H_AB source owner appears in the 3612 source sweep.
- `DEC3612_3_claim_guard` / `local-GR/Newton/Maxwell claim`: BLOCKED_FOR_CLAIM_NOT_FOR_WORK - No claim is allowed because the EM/Poynting zero clauses and source-weight grammar are conditional and not parent-signed together.
- `DEC3612_4_next` / `next best attack`: SELECT_HODGE_NORMALIZATION_OR_PIM_HTAU - Either prove/bound the EM Hodge/normalization terms inside the new bound, or attack Pi_M/H_tau because that is the source denominator heart.

## Status
- `JQ_MATTER_EM_POYNTING_SUBCOMPONENT_BOUND_FILLED_XI_OWNER_STILL_MISSING`: 3612 fills the EM/Poynting part of J_q^matter_bulk: minimal bound EM fields live inside total Hilbert stress under common-owner clauses; radiative flux, Hodge mismatch, EM normalization, hidden F2/readout and non-Hilbert bypass remain explicit absolute residuals. Source weights are narrowed to typed-domain/density-line/no-Hom signatures, while xi_q/H_AB remains unsigned.

## Validation
- `VAL3612_0_sources_exist`: PASS (all required 3612 source paths exist)
- `VAL3612_1_needles_found`: PASS (all selected 3612 source anchors found)
- `VAL3612_2_outputs_exist`: PASS (all pre-validation 3612 csv outputs written)
- `VAL3612_3_csv_parse`: PASS (source_register:15; subcomponent_attack:6; em_poynting_closure:7; source_weight_reduction:5; xi_parallel_audit:1; decision_gates:5; status:1; next_target:1; canonical_status:1)
- `VAL3612_4_em_bound_filled`: PASS (J_q^EM/Poynting absolute bound row filled)
- `VAL3612_5_hilbert_absorption_rule`: PASS (bound EM fields conditionally absorbed into M_H/T_H)
- `VAL3612_6_flux_retained`: PASS (radiative/background Poynting flux remains a retained residual)
- `VAL3612_7_source_weight_narrowed`: PASS (source-weight subcomponent narrowed by theorem stack)
- `VAL3612_8_xi_not_falsely_owned`: PASS (xi_q/H_AB owner not falsely claimed)
- `VAL3612_9_no_claim_flags`: PASS (all generated rows remain nonclaim)
- `VAL3612_10_next_target_selected`: PASS (3613 target selected from concrete residual vector)
- `VAL3612_11_status_ok`: PASS (canonical status matches 3612 verdict)
- `VAL3612_12_formalization_workbench_untouched`: PASS (no 3612 checkpoint output appears in formalization-workbench outside package/venv noise)

## Next Target
- `NEXT3612_0` -> `3613-Y5-R2FR-EM-Hodge-normalization-or-PiM-Htau-source-denominator.md`
- Objective: try to close or source-bound Delta_Hodge_EM and EM normalization terms inside J_q^EM/Poynting; if that stalls, attack Pi_M/H_tau source-denominator commutator because it controls Newtonian source mass
- Success gate: must theorem-zero or source-bound at least one of Delta_Hodge_EM, D_vq ln lambda_A, C_XF2, Phi_EM_rad, or one Pi_M/H_tau denominator obstruction; no generic missing-coupling ledger
- Reason: 3612 converts the Poynting worry into a concrete residual vector; 3613 should remove or bound one term in that vector.
