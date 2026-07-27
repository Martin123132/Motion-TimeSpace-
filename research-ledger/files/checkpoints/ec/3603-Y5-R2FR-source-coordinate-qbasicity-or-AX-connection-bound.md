# 3603 - source-coordinate q-basicity or A_X connection bound

## Verdict
3603 fuses the scattered source-coordinate work into one sharp law: `A_X=dY(v_X)=dYbar(Dq(v_X))+E_Y`, with `Y=(M_H_ref,sigma^a)`.

This is the leap we wanted: if `Y` is q-basic and `v_X` is genuinely vertical, then `A_X=0`; therefore `partial_M A_X^M=partial_M A_X^a=0`, so `C_M` and `C_shape` die by chain rule rather than by a fitted plateau or calibration trick.

The live corpus still cannot claim that zero, because the actual `Dq` matrix/residual basis is not certified.  The nonzero branch is now a usable bound law: `||A_X|| <= ||dYbar|| ||Dq(v_X)|| + ||E_MHref|| + ||E_sigma||`.

## Source-Coordinate Theorem Gate
- `AX3603_0_target`: TARGET_IMPORTED - Prove Y=(M_H_ref,sigma^a) is q-basic and v_X is vertical so A_X=0, or retain A_X and its M-derivatives as source-connection bounds.
- `AX3603_1_qbasic_criterion`: EXACT_DIFFERENTIAL_CRITERION - For connected q-fibres, Y descends as Y=Ybar(q(Phi)) iff dY annihilates ker(Dq) and is compatible across quotient branches.
- `AX3603_2_AX_connection_identity`: EXACT_CHAIN_RULE_IDENTITY - A_X^I:=D_XY^I=dY^I(v_X). If Y is q-basic, A_X^I=dYbar^I(Dq(v_X)).
- `AX3603_3_bundle_zero_theorem`: CONDITIONAL_ZERO_THEOREM_DERIVED - If M_H_ref and sigma^a are q-basic and Dq(v_X)=0, then A_X=0, hence partial_M A_X^M=partial_M A_X^a=0 and C_M=C_shape=0.
- `AX3603_4_MHref_descent_route`: CONDITIONAL_ZERO_ROUTE_NOT_LIVE - M_H_ref=H_tau-H_ref is q-basic if H_tau and H_ref are q-basic on the same tau/coframe/surface/reference/unit branch.
- `AX3603_5_shape_reynolds_route`: EXACT_REYNOLDS_TRANSPORT_LAW - For sigma^a=I^a/M_H_ref with I^a=int_W s^a rho_H dV_H, D_X sigma^a=(D_XI^a-sigma^a D_XM_H_ref)/M_H_ref.
- `AX3603_6_nonzero_bound_law`: EXACT_BOUND_LAW_NONCLAIM - If the theorem does not fire, ||A_X|| is bounded by a horizontal Dq leak plus E_MHref+E_sigma: ||A_X|| <= ||dYbar|| ||Dq(v_X)|| + ||E_MHref|| + ||E_sigma||.
- `AX3603_7_current_MTS_verdict`: BOUND_BRANCH_ACTIVE_NO_CLAIM - Current MTS has the conditional source-coordinate bundle theorem, but it does not yet own the actual Dq matrix, vertical basis, H_tau q-basicness, Hilbert-density q-basicness, regular support, or no-source-only Hom clauses.
- `AX3603_8_best_next_move`: NEXT_TARGET_SELECTED - Close or bound the actual q-map vertical basis: fill Dq(v_X) entries for each candidate residual direction before trying to claim any q-basic source-coordinate zero.

## A_X Obstruction Law
- `AXR3603_0_A_X_total` / `A_X_source_connection`: ACTIVE_NONCLAIM_EXACT_CHAIN_RULE - A_X=dY(v_X)=dYbar(Dq(v_X))+E_Y
- `AXR3603_1_Dq_vX` / `Dq_vX`: OPEN_VERTICAL_BASIS_REQUIRED - Dq(v_X)
- `AXR3603_2_A_XM` / `A_XM`: OPEN_MHREF_QBASIC_REQUIRED - D_X M_H_ref = D_XH_tau-D_XH_ref+E_branch_units
- `AXR3603_3_A_Xshape` / `A_Xshape`: OPEN_SHAPE_QBASIC_REQUIRED - D_X sigma^a=(D_XI^a-sigma^a D_XM_H_ref)/M_H_ref
- `AXR3603_4_E_Htau` / `E_Htau_qbasic`: OPEN_HTAU_QBASIC_REQUIRED - D_XH_tau - dHbar_tau(Dq(v_X))
- `AXR3603_5_E_Href` / `E_Href_qbasic`: OPEN_REFERENCE_BRANCH_REQUIRED - D_XH_ref - dHbar_ref(Dq(v_X))
- `AXR3603_6_E_rho` / `E_rho_qbasic`: OPEN_DENSITY_QBASIC_REQUIRED - D_X(rho_H dV_H)-d rhobar_H(Dq(v_X))
- `AXR3603_7_E_noHom` / `E_source_weight`: OPEN_NO_SOURCE_ONLY_HOM_REQUIRED - relative active source prefactor/source-marker/readout-mask terms
- `AXR3603_8_E_boundary` / `E_boundary_birth`: OPEN_SUPPORT_REGULARITY_REQUIRED - int_boundary s^a rho_H v_boundary dS plus zero-crossing/birth-death events
- `AXR3603_9_E_tau_frame` / `E_tau_frame`: OPEN_FRAME_LOCK_REQUIRED - D_X(tau,e_obs,Sigma,readout frame mismatch)
- `AXR3603_10_E_readout_mask` / `E_readout_mask`: OPEN_NO_READOUT_MASK_REQUIRED - D_X W_source post-readout mask or fitted source-domain selector
- `AXR3603_11_E_EM_flux` / `E_EM_flux`: OPEN_EM_FLUX_SILENCE_OR_BOUND_REQUIRED - nonstationary or non-q-basic EM/Poynting flux contribution to rho_H/support
- `AXR3603_12_partial_M_AXM` / `partial_M_A_XM`: OPEN_MASS_FLATNESS_DERIVATIVE_REQUIRED - partial_M(D_XM_H_ref)
- `AXR3603_13_partial_M_AXshape` / `partial_M_A_Xshape`: OPEN_SHAPE_FLATNESS_DERIVATIVE_REQUIRED - partial_M(D_X sigma^a)

## A_X Bound Rows
- `AXB3603_0_A_X_total` / `A_X_source_connection`: BOUND_REQUIRED_CRITICAL - ||A_X|| <= ||dYbar|| ||Dq(v_X)|| + ||E_MHref|| + ||E_sigma||
- `AXB3603_1_Dq_vX` / `Dq_vX`: BOUND_REQUIRED_CRITICAL - Dq(v_X)
- `AXB3603_2_A_XM` / `A_XM`: BOUND_REQUIRED_CRITICAL - D_XH_tau-D_XH_ref+E_branch_units
- `AXB3603_3_A_Xshape` / `A_Xshape`: BOUND_REQUIRED_CRITICAL - (D_XI^a-sigma^a D_XM_H_ref)/M_H_ref
- `AXB3603_4_E_MHref` / `E_MHref`: BOUND_REQUIRED - E_Htau+E_Href+E_tau_branch+E_ref_branch+E_units
- `AXB3603_5_E_sigma` / `E_sigma`: BOUND_REQUIRED - E_rho+E_boundary_birth+E_tau_frame+E_readout_mask+E_EM_flux+E_MHref_denom
- `AXB3603_6_E_rho` / `E_rho_qbasic`: BOUND_REQUIRED - D_X(rho_H dV_H)-d rhobar_H(Dq(v_X))
- `AXB3603_7_E_source_weight` / `E_source_weight`: BOUND_REQUIRED - relative source prefactor/source-marker/readout-mask source density terms
- `AXB3603_8_E_boundary` / `E_boundary_birth`: BOUND_REQUIRED - int_boundary s^a rho_H v_boundary dS + support birth/death events
- `AXB3603_9_E_EM_flux` / `E_EM_flux`: BOUND_REQUIRED - nonstationary/non-q-basic EM flux through source support
- `AXB3603_10_partial_M_AXM` / `partial_M_A_XM`: BOUND_REQUIRED_CRITICAL - partial_M(D_XM_H_ref)
- `AXB3603_11_partial_M_AXshape` / `partial_M_A_Xshape`: BOUND_REQUIRED_CRITICAL - partial_M(D_X sigma^a)
- `AXB3603_12_C_M_Cshape_transfer` / `C_M_plus_C_shape`: TOTAL_BOUND_BRANCH_ACTIVE - C_M+C_shape from partial_M A_XM and partial_M A_Xshape

## Promotion Gates
- `PROM3603_0_chain_rule_identity`: PASS_EXACT_IDENTITY - A_X=dY(v_X), and q-basic Y gives A_X=dYbar(Dq(v_X))
- `PROM3603_1_bundle_zero_theorem`: PASS_CONDITIONAL_THEOREM - q-basic M_H_ref and sigma^a plus Dq(v_X)=0 kill A_X, C_M and C_shape
- `PROM3603_2_reynolds_shape_law`: PASS_EXACT_IDENTITY - D_X sigma^a=(D_XI^a-sigma^a D_XM_H_ref)/M_H_ref isolates support/density/boundary leakage
- `PROM3603_3_current_AX_zero_claim`: FAIL_CURRENT_CLAIM - actual Dq matrix, vertical basis, M_H_ref q-basicness, density q-basicness and regular support are not jointly parent-signed
- `PROM3603_4_current_CM_Cshape_claim`: FAIL_CURRENT_CLAIM - partial_M A_XM and partial_M A_Xshape have no live zero or numeric bound yet
- `PROM3603_5_anti_tautology_guard`: PASS_GUARD - Y is a target derived observable; including M_H_ref or sigma^a as primitive q components would be circular
- `PROM3603_6_no_measured_GM_laundering`: PASS_GUARD - M_H_ref and sigma^a must be fixed by parent charge/support, not by orbit/R10/PPN fits
- `PROM3603_7_bound_pack`: PASS_NONCLAIM - A_X, Dq leak, MHref leakage, shape leakage and derivative rows are source-ready but not score-ready
- `PROM3603_8_next_target`: PASS_ROUTE_SELECTED - fill the actual q-map vertical matrix or retain Dq leak bounds

## Status
- `SOURCE_COORDINATE_QBASIC_AX_THEOREM_DERIVED_DQ_MATRIX_NEXT`: 3603 fuses the scattered q-basic results into one source-coordinate connection law: A_X=dY(v_X)=dYbar(Dq(v_X))+E_Y, with exact zero if Y=(M_H_ref,sigma^a) is q-basic and v_X is truly vertical. The shape component now has a Reynolds transport formula, not a mystery coupling.
- Decision: retain A_X, A_XM, A_Xshape, Dq_vX, E_MHref, E_sigma and partial_M derivative rows as nonclaim bounds; move next to the actual Dq vertical-basis matrix because every q-basic theorem depends on it
- Still missing: actual q-map matrix entries, certified residual basis, Dq(v_X)=0 or norm bounds, H_tau/H_ref q-basic same-branch lock, Hilbert-density q-basic owner, no-source-only Hom theorem, support regularity, same-frame/readout lock, EM flux silence and derivative bounds for partial_M A_X

## Validation
- `VAL3603_0_sources_exist`: PASS (all required 3603 source paths exist)
- `VAL3603_1_needles_found`: PASS (all selected 3603 source anchors found)
- `VAL3603_2_outputs_exist`: PASS (all pre-validation 3603 csv output files written)
- `VAL3603_3_csv_parse`: PASS (source_register:21; qbasic_ax_theorem:9; ax_obstruction_law:14; ax_bound_rows:13; promotion_gates:9; status:1; next_target:1; canonical_status:1)
- `VAL3603_4_chain_rule_present`: PASS (A_X chain-rule identity present)
- `VAL3603_5_bundle_zero_present`: PASS (source-coordinate bundle zero theorem present)
- `VAL3603_6_reynolds_law_present`: PASS (shape Reynolds transport law present)
- `VAL3603_7_bound_rows_present`: PASS (critical A_X and derivative bound rows present)
- `VAL3603_8_claims_blocked`: PASS (A_X and C_M/C_shape claims are blocked)
- `VAL3603_9_no_tautology_guard`: PASS (anti-tautology guard present)
- `VAL3603_10_no_claim_flags`: PASS (all generated physics rows remain nonclaim)
- `VAL3603_11_next_target_selected`: PASS (3604 Dq vertical-basis target selected)
- `VAL3603_12_generated_source_paths_exist`: PASS (every generated row source_path exists)
- `VAL3603_13_formalization_workbench_untouched`: PASS (no 3603 checkpoint output appears in formalization-workbench outside package/venv noise)

## Next target
- `NEXT3603_0` -> `3604-Y5-R2FR-actual-qmap-vertical-basis-or-Dq-leak-bound.md`
- Objective: try to construct the actual q-map/Dq matrix and certify which residual directions satisfy Dq(v_X)=0; if not, retain Dq leak bounds for v_q, v_memory, v_coeff, v_boundary and rejected v_RAB directions
