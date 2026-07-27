# 3602 - PiM/Htau subdenominator lock or component bound

## Verdict
3602 gets a real theorem out of the fog: `R_PiM + R_Htau = C_M + C_shape + C_curl + C_domain + C_ref + C_frame + C_units`.

The best zero route is not a plateau axiom.  It is a chain-rule mechanism: make the source coordinates `Y=(M_H_ref,sigma^a)` descend through the parent quotient and prove the residual direction is vertical.  Then `A_X=dYbar(Dq(v_X))=0`, so the mass/shape connection terms `C_M` and `C_shape` vanish before fitting.

The full PiM/Htau zero remains conditional because `C_curl`, support/domain, reference, frame, and unit silence are not yet parent-signed.  No Newton, PPN, R10, orbital, clock, or local-GR claim is promoted.

## PiM/Htau Theorem Gate
- `PHT3602_0_target`: TARGET_IMPORTED - Try to prove R_PiM+R_Htau=0, or keep each Pi_M/H_tau subdenominator component as an explicit bound term.
- `PHT3602_1_exact_decomposition`: EXACT_COMPONENT_DECOMPOSITION - R_PiM + R_Htau = C_M + C_shape + C_curl + C_domain + C_ref + C_frame + C_units.
- `PHT3602_2_source_coordinate_connection`: EXACT_DEFINITION - Let Y(Phi)=(M_H_ref(Phi), sigma^a(Phi)) and A_X^I := D_X Y^I.  Then C_M and C_shape are the mass/shape connection pieces induced by A_X.
- `PHT3602_3_quotient_zero_theorem`: CONDITIONAL_ZERO_THEOREM_DERIVED - If Y=Ybar(q(Phi)) and v_X in ker(Dq), then A_X^I=dYbar^I(Dq(v_X))=0, hence C_M=C_shape=0.
- `PHT3602_4_Htau_integrability_zero`: CONDITIONAL_ZERO_ROUTE_NOT_SIGNED - C_curl=0 if the parent L_X/theta/omega/tau/surface branch is fixed and the H_tau symplectic boundary term is exact, zero, or separately bounded.
- `PHT3602_5_domain_reference_frame_units_zero`: CONDITIONAL_ZERO_ROUTE_NOT_SIGNED - C_domain=C_ref=C_frame=C_units=0 only if W_source, H_ref, tau/coframe/surface readout, and denominator units are parent-selected before measured GM or clock/orbit readout.
- `PHT3602_6_subdenominator_theorem`: CONDITIONAL_ZERO_THEOREM_DERIVED - If A_X=0, C_curl=0, and the domain/reference/frame/unit clauses are all parent-silent, then R_PiM+R_Htau=0.
- `PHT3602_7_current_MTS_verdict`: BOUND_BRANCH_ACTIVE_NO_CLAIM - Current MTS has the conditional mechanism, but not the live signatures for q-basic Y, actual vertical v_X, H_tau integrability, fixed support/reference/frame, or source-unit silence.
- `PHT3602_8_best_next_move`: NEXT_TARGET_SELECTED - The least hand-wavy route is to prove source-coordinate q-basicity first: Y=(M_H_ref,sigma^a)=Ybar(q(Phi)) and Dq(v_X)=0.

## Component Residuals
- `PHTR3602_0_total` / `R_PiM_plus_R_Htau`: ACTIVE_NONCLAIM_EXACT_DECOMPOSITION - C_M+C_shape+C_curl+C_domain+C_ref+C_frame+C_units
- `PHTR3602_1_C_M` / `C_M`: OPEN_SOURCE_MASS_CONNECTION_ZERO_REQUIRED - -(partial_M A_X^M) partial_M(H_tau-H_ref)/(Pi_M H_tau)
- `PHTR3602_2_C_shape` / `C_shape`: OPEN_SOURCE_SHAPE_CONNECTION_ZERO_REQUIRED - -(partial_M A_X^a) partial_a(H_tau-H_ref)/(Pi_M H_tau)
- `PHTR3602_3_C_curl` / `C_curl`: OPEN_HTAU_INTEGRABILITY_REQUIRED - Pi_M^H(curl(delta H_tau))/(Pi_M H_tau)
- `PHTR3602_4_C_domain` / `C_domain`: OPEN_SUPPORT_DOMAIN_LOCK_REQUIRED - normalized D_X(W_source, Sigma, Hodge, linked surfaces)
- `PHTR3602_5_C_ref` / `C_ref`: OPEN_SOURCE_BLIND_REFERENCE_REQUIRED - -([D_X,Pi_M]H_ref + Pi_M D_X H_ref)/(Pi_M H_tau)
- `PHTR3602_6_C_frame` / `C_frame`: OPEN_FRAME_READOUT_LOCK_REQUIRED - D_X ln(tau, e_obs, Sigma, readout frame mismatch)
- `PHTR3602_7_C_units` / `C_units`: OPEN_DENOMINATOR_UNIT_LOCK_REQUIRED - D_X ln(Pi_M H_tau denominator units)
- `PHTR3602_8_A_X` / `A_X_source_connection`: CONDITIONAL_ZERO_NOT_LIVE - A_X^I=D_X Y^I=dYbar^I(Dq(v_X)) when Y is q-basic
- `PHTR3602_9_qbasic_Y` / `qbasic_Y`: OPEN_QBASIC_CERTIFICATE_REQUIRED - Y(Phi)=(M_H_ref,sigma^a)=Ybar(q(Phi))
- `PHTR3602_10_vertical_vX` / `vertical_vX`: OPEN_VERTICAL_BASIS_REQUIRED - Dq(v_X)=0
- `PHTR3602_11_PiM_chainmap` / `PiM_chainmap`: PARTIAL_CHAINMAP_OPEN_SUPPORT - [d,Pi_M^H]J_H^M=0 on fixed C_H^M plus fixed support
- `PHTR3602_12_MHref_tau_surface` / `Delta_MHref_tau_surface_total`: OPEN_MHREF_LOCK_REQUIRED - tau/coframe/surface/integrability/M_H_ref denominator lock residual

## Component Bound Rows
- `PHTB3602_0_total` / `R_PiM_plus_R_Htau`: BOUND_REQUIRED_CRITICAL - C_M+C_shape+C_curl+C_domain+C_ref+C_frame+C_units
- `PHTB3602_1_C_M` / `C_M`: BOUND_REQUIRED_CRITICAL - -(partial_M A_X^M) partial_M(H_tau-H_ref)/(Pi_M H_tau)
- `PHTB3602_2_C_shape` / `C_shape`: BOUND_REQUIRED_CRITICAL - -(partial_M A_X^a) partial_a(H_tau-H_ref)/(Pi_M H_tau)
- `PHTB3602_3_C_curl` / `C_curl`: BOUND_REQUIRED_CRITICAL - Pi_M^H(curl(delta H_tau))/(Pi_M H_tau)
- `PHTB3602_4_C_domain` / `C_domain`: BOUND_REQUIRED - normalized D_X(W_source, Sigma, Hodge, linked surfaces)
- `PHTB3602_5_C_ref` / `C_ref`: BOUND_REQUIRED - -([D_X,Pi_M]H_ref + Pi_M D_X H_ref)/(Pi_M H_tau)
- `PHTB3602_6_C_frame` / `C_frame`: BOUND_REQUIRED - D_X ln(tau, e_obs, Sigma, readout frame mismatch)
- `PHTB3602_7_C_units` / `C_units`: BOUND_REQUIRED - D_X ln(Pi_M H_tau denominator units)
- `PHTB3602_8_A_X` / `A_X_source_connection`: BOUND_REQUIRED_CRITICAL - A_X^I=D_XY^I
- `PHTB3602_9_qbasic_MHref` / `qbasic_MHref`: BOUND_REQUIRED - M_H_ref(Phi)=Mbar_H_ref(q(Phi))
- `PHTB3602_10_qbasic_sigma` / `qbasic_sigma`: BOUND_REQUIRED - sigma^a(Phi)=sigmabar^a(q(Phi))
- `PHTB3602_11_vertical_vX` / `vertical_vX`: BOUND_REQUIRED - Dq(v_X)=0
- `PHTB3602_12_total_no_cancellation` / `epsilon_PiM_Htau_total`: TOTAL_BOUND_BRANCH_ACTIVE - norm(C_M,C_shape,C_curl,C_domain,C_ref,C_frame,C_units)

## Promotion Gates
- `PROM3602_0_exact_decomposition`: PASS_EXACT_IDENTITY - R_PiM+R_Htau is split into C_M,C_shape,C_curl,C_domain,C_ref,C_frame,C_units
- `PROM3602_1_qbasic_zero_route`: PASS_CONDITIONAL_THEOREM - Y=Ybar(q(Phi)) and Dq(v_X)=0 imply A_X=0 and C_M=C_shape=0
- `PROM3602_2_subdenominator_zero_theorem`: PASS_CONDITIONAL_THEOREM - all seven C_i components zero imply R_PiM+R_Htau=0
- `PROM3602_3_current_PiM_Htau_claim`: FAIL_CURRENT_CLAIM - q-basic source coordinates, vertical basis, H_tau curl, support, reference, frame and units are not jointly parent-signed
- `PROM3602_4_current_Newton_GR_claim`: FAIL_CURRENT_CLAIM - the subdenominator is not live-zero, so no local-GR/Newton claim follows from 3602
- `PROM3602_5_no_measured_GM_laundering`: PASS_GUARD - M_H_ref, H_ref, W_source, Pi_M and units must be fixed before orbital GM/readout
- `PROM3602_6_bound_pack`: PASS_NONCLAIM - component rows are source-ready but not numeric/score-ready
- `PROM3602_7_next_target`: PASS_ROUTE_SELECTED - attack source-coordinate q-basicity and vertical-basis certificate before further numeric bounds

## Status
- `PIM_HTAU_SUBDENOMINATOR_CONDITIONAL_ZERO_THEOREM_BOUND_BRANCH_ACTIVE`: 3602 derives the exact local theorem for the Pi_M/H_tau subdenominator: R_PiM+R_Htau=0 if source-coordinate q-basicity, actual verticality, H_tau integrability, support/domain, source-blind reference, same-frame readout, and denominator-unit silence all hold.
- Decision: keep the theorem as a conditional win, keep all seven C_i components as nonclaim bound rows, and move next to source-coordinate q-basicity because it kills C_M and C_shape by chain rule rather than by numeric fitting
- Still missing: Y=(M_H_ref,sigma^a) q-basic descent, Dq(v_X)=0 vertical basis certificate, H_tau curl zero/exactness, W_source support descent, source-blind H_ref selector, same-frame tau/coframe/surface readout lock, and denominator unit lock

## Validation
- `VAL3602_0_sources_exist`: PASS (all required 3602 source paths exist)
- `VAL3602_1_needles_found`: PASS (all selected 3602 source anchors found)
- `VAL3602_2_outputs_exist`: PASS (all pre-validation 3602 csv output files written)
- `VAL3602_3_csv_parse`: PASS (source_register:18; subdenominator_theorem:9; component_residuals:13; component_bounds:13; promotion_gates:8; status:1; next_target:1; canonical_status:1)
- `VAL3602_4_exact_decomposition_present`: PASS (PiM/Htau exact component decomposition row present)
- `VAL3602_5_component_bounds_present`: PASS (all seven C_i component bound rows present)
- `VAL3602_6_qbasic_route_present`: PASS (source-coordinate q-basic zero theorem present)
- `VAL3602_7_claims_blocked`: PASS (PiM/Htau and Newton/GR claims are blocked)
- `VAL3602_8_no_laundering_guard`: PASS (measured-GM/source denominator laundering guard present)
- `VAL3602_9_no_claim_flags`: PASS (all generated physics rows remain nonclaim)
- `VAL3602_10_next_target_selected`: PASS (3603 source-coordinate q-basicity target selected)
- `VAL3602_11_generated_source_paths_exist`: PASS (every generated row source_path exists)
- `VAL3602_12_formalization_workbench_untouched`: PASS (no 3602 checkpoint output appears in formalization-workbench outside package/venv noise)

## Next target
- `NEXT3602_0` -> `3603-Y5-R2FR-source-coordinate-qbasicity-or-AX-connection-bound.md`
- Objective: try to prove Y=(M_H_ref,sigma^a) is q-basic and v_X is vertical so A_X=0; if not, retain A_X^M, A_X^a, partial_M A_X^M and partial_M A_X^a as source-connection bound inputs
