# 3610 - parent pi/vq certificate or Zq/Jq extraction

## Verdict
3610 turns the post-3609 fork into a concrete MTS object.

`pi_MTS` is now written over actual MTS symbols: public geometry/coframe, tau, matter/constants, boundary class, coupling slots, projector/readout maps, plus excluded `q_private` and the local silence multiplet `Y_loc`.

The no-pole certificate still does not close because `Dpi[v_q]=0` is unsigned component-by-component.  But the fallback is much sharper than a blank bound row:

`M_q^2 = n_q^A H_AB n_q^B`, `Z_q = xi_q^2 n_q^A H_AB n_q^B`, therefore `lambda_q = sqrt(Z_q/M_q^2) = xi_q`.

So if `q` is physical, its range is not arbitrary in this branch; it is the parent smoothing/correlation length `xi_q`.  That is the next derivation target.

## pi_MTS Symbol Map
- `PI3610_0_pi_definition` / `pi_MTS candidate`: CONCRETE_CANDIDATE_CONSTRUCTED_NOT_PARENT_SIGNED - This is the single pi target needed by 3609; it is still a candidate because parent derivation from motion/time/space primitives is unsigned.
- `PI3610_1_q_gobs` / `q(Phi); g_obs; observed coframe`: BEST_ANCHOR_CONDITIONAL_QAP_UNSIGNED - This is the least suspicious anchor: public geometry survives; private representative data should not.
- `PI3610_2_Gamma_Khat_qloc` / `Gamma_eff; K_hat; q_loc^nu`: WARD_EXACT_ROUTE_IDENTIFIED_NOT_SIGNED - They can vanish only if the exact Ward/boundary pair and P_loc projection commute on the same branch.
- `PI3610_3_Ploc_PiM` / `P_loc; Pi_M`: CONDITIONAL_ZERO_FROM_CHARGE_OWNER - No fitted GM/source projector can be used to prove Newton; this must be parent-owned.
- `PI3610_4_chiD_Qcoh_memory_flow` / `chi_D; Qcoh; memory; flow`: DOUBLE_ZERO_ROUTE_CONDITIONAL - This route can kill local hair without individual tuning, but positivity and factorization are not signed.
- `PI3610_5_EM_Maxwell` / `EM Hodge/Maxwell/Poynting residuals`: VISIBLE_STACK_COMPATIBLE_BOUND_ROWS_RETAINED - The EM part fits the shared visible-geometry route but does not yet close hidden EM stress couplings.
- `PI3610_6_kappa_G` / `kappa_eff; G_eff`: CALIBRATED_CONSTANT_NOT_MTS_DERIVED - This keeps Newton's constant as a coupling/integration datum unless a deeper parent route derives it.
- `PI3610_7_q_private` / `q_private`: CANDIDATE_VERTICAL_UNSIGNED - This is the exact q deletion target; it is not allowed to hide Weyl, matter, boundary or readout tails.
- `PI3610_8_source_coordinates` / `M_H_ref; sigma^a`: ANTI_TAUTOLOGY_GUARD_ACTIVE - Including source coordinates directly in pi would smuggle the Newton/source answer into the premises.

## Dpi[v_q] Certificate
- `DPI3610_0_target` / `v_q = partial/partial q_private at fixed reduced fields`: DEFINITIONAL_TARGET - This is the concrete version of the 3609 certificate.
- `DPI3610_1_geometry` / `D g_obs[v_q], D e_obs[v_q]`: CONDITIONAL_ZERO_NOT_PARENT_SIGNED - Hidden frame re-entry would make q physical and reopen PPN/WEP/clock rows.
- `DPI3610_2_tau_clock` / `D tau_obs[v_q], D clock standards[v_q]`: CONDITIONAL_ZERO_NOT_PARENT_SIGNED - Clock/time route remains important because it can reintroduce local force through readout.
- `DPI3610_3_matter_constants` / `D(Psi,theta,c_vis,masses,charges)[v_q]`: CONDITIONAL_ZERO_NOT_PARENT_SIGNED - This is the J_q matter/marker source leg.
- `DPI3610_4_boundary` / `D beta0[v_q], D B_ref[v_q], D H_ref[v_q]`: CONDITIONAL_ZERO_NOT_PARENT_SIGNED - This is the boundary/source-worldtube leg of J_q.
- `DPI3610_5_coefficients` / `D(kappa,G,alpha_EM,source weights)[v_q]`: CONDITIONAL_ZERO_NOT_PARENT_SIGNED - Without this, q deletion can be faked while constants drift.
- `DPI3610_6_projectors` / `D(P_loc,Pi_M,domain/readout kernels)[v_q]`: CONDITIONAL_ZERO_NOT_PARENT_SIGNED - If projectors move, q leaks through source normalization even when equations look GR-like.
- `DPI3610_7_Yloc` / `D Y_loc[v_q]`: FORK_ROW - This separates quotient representative q from physical silent multiplet Y_loc.
- `DPI3610_8_verdict` / `pi_MTS/v_q certificate`: NOT_CERTIFIED_CURRENT_CORPUS - Proceed to conditional Z_q/J_q extraction rather than claiming q deletion.

## Zq/Jq Extraction
- `EX3610_0_Mq2` / `M_q^2`: CONDITIONAL_FORMULA_IMPORTED - `M_q^2 = n_q^A H_AB n_q^B`
- `EX3610_1_Zq` / `Z_q`: CONDITIONAL_FORMULA_IMPORTED - `Z_q = xi_q^2 n_q^A H_AB n_q^B`
- `EX3610_2_lambda` / `lambda_q`: EXACT_CONDITIONAL_RATIO - `lambda_q = sqrt(Z_q/M_q^2) = xi_q`
- `EX3610_3_Lq` / `L_q`: OPERATOR_SHAPE_FILLED_CONDITIONAL - `L_q = -Z_q Delta_branch + M_q^2 + B_q^bdry`
- `EX3610_4_Jq_definition` / `J_q`: DEFINITION_SHARPENED - `J_q[eta] := delta_eta S_nonq projected onto the q equation`
- `EX3610_5_Jq_descent_zero` / `J_q zero theorem`: EXACT_CONDITIONAL_NOT_ACTIVE - `delta_vq F_i=0 if F_i=Fbar_i(Obs(Phi),psi) and v_q in ker(DObs)`
- `EX3610_6_Jq_components` / `J_q^abs`: SCHEMA_READY_VALUES_MISSING - `J_q^abs = sum_i ||J_q^i||_* over matter, frame, marker, body, boundary, projector, memory, source-normalization and curvature components`
- `EX3610_7_q_source_vector` / `E_q`: NORMAL_FORM_ACCEPTED_NONCLAIM - `E_q = L_q q + B_qRic R_Ricci + B_qW C_Weyl + C_qT T_H + epsilon_q_source sigma_source + Q_q_body delta_body + Pi_q delta_boundary + tail_q`
- `EX3610_8_residual_bound` / `q residual bound`: BOUND_LAW_READY_NUMBERS_MISSING - `||P_arena q|| <= ||P_arena L_q^{-1}|| (||J_q^abs|| + |B_qW| ||C_Weyl|| + |D_qWeyl2| ||C^2|| + boundary tails)`

## Decision Gates
- `DEC3610_0_pi_map` / `pi_MTS concrete map`: BUILT_NOT_SIGNED - Actual MTS symbols are placed into quotient base, derived residual, local silence multiplet, visible stress and coupling slots.
- `DEC3610_1_dpi_vq` / `Dpi[v_q] certificate`: FAIL_CURRENT_CERTIFICATION - The required component zeros are now explicit, but none is parent-signed across geometry, clocks, matter, boundary, constants and projectors.
- `DEC3610_2_Zq` / `Z_q/M_q/lambda extraction`: CONDITIONAL_FORMULA_ADVANCED - The fallback is upgraded from blank placeholders to M_q^2=n_q H n_q, Z_q=xi_q^2 n_q H n_q, lambda_q=xi_q.
- `DEC3610_3_Jq` / `J_q extraction`: COMPONENT_ENVELOPE_READY_VALUES_MISSING - The J_q source problem is an absolute component vector, not an undifferentiated coupling mystery.
- `DEC3610_4_next` / `next best attack`: SELECT_XI_OR_JQ_FIRST_COMPONENT - Either derive/source xi_q and the positive Hessian branch, or attack the highest-pressure J_q components: matter/constants and body/boundary.

## Status
- `PI_MTS_MAP_BUILT_VQ_UNSIGNED_ZQ_JQ_CONDITIONAL_EXTRACTION_ADVANCED`: 3610 builds a concrete pi_MTS candidate over actual MTS symbols and upgrades the physical-q fallback: M_q^2=n_q^A H_AB n_q^B, Z_q=xi_q^2 n_q^A H_AB n_q^B, and lambda_q=xi_q under the positive Hessian branch.
- Decision: do not claim q deletion; Dpi[v_q] remains unsigned componentwise. Treat q as either a future quotient representative or a physical residual with a now-sharper Hessian/source envelope.
- Framework progress: The next testable/derivable bottleneck is no longer abstract q ownership; it is xi_q/positive-Hessian ownership plus the absolute J_q component vector.
- Still missing: parent pi signature, Dpi[v_q] component zeros, xi_q source, positive H_AB, boundary/domain conditions, J_q component zero/bound values and arena projections

## Validation
- `VAL3610_0_sources_exist`: PASS (all required 3610 source paths exist)
- `VAL3610_1_needles_found`: PASS (all selected 3610 source anchors found)
- `VAL3610_2_outputs_exist`: PASS (all pre-validation 3610 csv outputs written)
- `VAL3610_3_csv_parse`: PASS (source_register:17; parent_pi_symbol_map:9; dpi_vq_certificate:9; zq_jq_extraction_rows:9; decision_gates:5; status:1; next_target:1; canonical_status:1)
- `VAL3610_4_actual_MTS_symbols_mapped`: PASS (actual MTS symbols are placed in the pi/kernel map)
- `VAL3610_5_dpi_certificate_not_falsely_signed`: PASS (Dpi[v_q] certificate remains unclaimed)
- `VAL3610_6_Zq_Jq_rows_extracted`: PASS (Zq/Mq/lambda and Jq extraction rows present)
- `VAL3610_7_lambda_equals_xi_recorded`: PASS (lambda_q=xi_q conditional ratio recorded)
- `VAL3610_8_no_claim_flags`: PASS (all generated physics rows remain nonclaim)
- `VAL3610_9_next_target_selected`: PASS (3611 xi_q/Hessian or Jq component target selected)
- `VAL3610_10_formalization_workbench_untouched`: PASS (no 3610 checkpoint output appears in formalization-workbench outside package/venv noise)

## Next Target
- `NEXT3610_0` -> `3611-Y5-R2FR-xi-q-positive-Hessian-source-or-Jq-first-component-bound.md`
- Objective: try to derive/source xi_q and the positive Hessian branch that makes lambda_q=xi_q; if that cannot close, immediately fill the first J_q component bound for matter/constants or body/boundary
- Success gate: must produce either an owned xi_q/H_AB row or a theorem-zero/source-backed bound for at least one leading J_q component; no new target-only ledger
