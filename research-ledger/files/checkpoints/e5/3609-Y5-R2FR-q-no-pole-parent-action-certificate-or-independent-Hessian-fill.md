# 3609 - q no-pole parent-action certificate or independent Hessian fill

## Verdict
3609 makes the fork honest and mathematical.

The no-pole side is no longer hand-waving: if `S=Sbar∘pi`, `v_q in ker(Dpi)`, and the reduced equations hold, then

`D^2(Sbar∘pi)[v_q,w]=D^2Sbar[Dpi(v_q),Dpi(w)] + DSbar[D^2pi(v_q,w)] = 0`

for every physical direction `w`.  Therefore the `q` row/column is not part of the physical Hessian on the quotient, and q-basic observables contain no physical `G_q` pole.

But the current MTS corpus does not yet sign the parent `pi`, actual `v_q in ker(Dpi)`, first-class degree count, matter/coefficient/readout descent, and boundary silence on one branch.  So this is a proved conditional theorem, not a local-GR claim.

If that certificate cannot be built, the alternative is now explicit: treat `q` as physical and fill `Z_q`, `M_q^2`, `lambda_q`, `J_q`, boundary, coefficient, and `P_arena` rows.

## No-Pole Hessian Proof
- `QNP3609_0_setup` / `parent quotient setup`: DEFINITIONAL_SETUP - This fixes the branch where q can be deleted instead of bounded.
- `QNP3609_1_first_variation` / `vertical first variation`: PROVED_CONDITIONALLY - A vertical representative direction cannot source the parent equations if the action descends through pi.
- `QNP3609_2_hessian_row` / `on-shell Hessian row`: PROVED_CONDITIONALLY_WITH_ONSHELL_CAVEAT - This is the actual no-pole algebra: the q row is zero before inversion, provided reduced equations and quotient descent are both true.
- `QNP3609_3_schur_complement` / `physical propagator after quotient`: PROVED_CONDITIONALLY - Gauge-fixing may add an auxiliary inverse in the representative sector, but q-basic readouts have zero coupling to it.
- `QNP3609_4_matter_boundary` / `source and boundary silence`: PROVED_CONDITIONALLY - This is what removes J_q, boundary tails and P_arena leakage rather than merely setting a coefficient to zero.
- `QNP3609_5_failure_modes` / `when no-pole proof fails`: EXACT_COUNTERCONDITION - This prevents deleting q by words: any non-descending row reactivates Z_q, M_q^2, J_q and P_arena.
- `QNP3609_6_current_application` / `current MTS application`: THEOREM_PROVED_CERTIFICATE_UNSIGNED - Use the theorem as the target certificate; do not claim q deletion yet.

## Parent Certificate
- `QCERT3609_0_parent_pi` / `parent quotient object pi`: UNSIGNED - P8_EM and 2486 provide candidate quotient language, not a parent-owned single pi.
- `QCERT3609_1_vertical_generator` / `v_q in ker(Dpi)`: UNSIGNED - 3604 marks v_q as highest priority but not certified; R_AB is rejected under current observer map.
- `QCERT3609_2_first_class_degree_count` / `first-class/removed degree count`: UNSIGNED - No current row owns the symplectic/constraint package for q deletion.
- `QCERT3609_3_action_descent` / `parent action descent`: PARTIAL_CONDITIONAL - QAP gives conditional normal-form progress, but parent action/object-language exhaustion remains unsigned.
- `QCERT3609_4_matter_descent` / `ordinary matter descent`: UNSIGNED - 2486 proves the chain-rule gate but source prefactors/constants owner remain open.
- `QCERT3609_5_coefficient_descent` / `visible constants/couplings descent`: UNSIGNED - Coefficient descent theorem is exact conditional but not parent-signed for every visible coefficient.
- `QCERT3609_6_readout_boundary_descent` / `readout and boundary silence`: UNSIGNED - Readout-order guard exists; boundary/reference/projector silence remains open.
- `QCERT3609_7_local_GR_compatibility` / `local GR reduction compatibility`: PARTIAL_MAP_ONLY - 3534 maps MTS variables into a local-EH quotient kernel but does not yet parent-own the double-zero origin.
- `QCERT3609_8_activation` / `activate q no-pole deletion`: NOT_ACTIVATED - The no-pole theorem is proven conditionally, but the MTS parent certificate is not signed.

## Independent Hessian Fill
- `QHESS3609_0_Zq` / `Z_q`: REQUIRED_IF_Q_NOT_DELETED - Z_q := coefficient of (1/2) sqrt(-g) h_q^{mu nu} nabla_mu q nabla_nu q in delta_q^2 S_parent after branch normalization.
- `QHESS3609_1_Mq2` / `M_q^2`: REQUIRED_IF_Q_NOT_DELETED - M_q^2 := second derivative of the effective q potential plus branch curvature-mass terms in the same normalization as Z_q.
- `QHESS3609_2_lambda` / `lambda_q`: DERIVED_FORMULA_INPUTS_MISSING - lambda_q=sqrt(Z_q/M_q^2) for positive massive branch; if M_q^2=0, replace by massless domain/no-hair boundary theorem.
- `QHESS3609_3_domain` / `D(L_q)`: REQUIRED_IF_Q_NOT_DELETED - D(L_q) is the local function space, support class and regularity class on which L_q is inverted.
- `QHESS3609_4_boundary_operator` / `B_q^bdry`: REQUIRED_IF_Q_NOT_DELETED - Boundary variation terms define the self-adjoint extension or finite boundary/source-tail rows of L_q.
- `QHESS3609_5_Jq` / `J_q`: REQUIRED_IF_Q_NOT_DELETED - J_q := -delta S_parent/delta q excluding the declared Weyl forcing terms; includes matter, source, boundary and readout residues.
- `QHESS3609_6_BqWeyl` / `B_qWeyl`: REQUIRED_FOR_LINEAR_ROUTE - B_qWeyl is the parent coefficient of a linear q-Weyl forcing channel; zero only follows from quotient/no-spurion certificate.
- `QHESS3609_7_DqWeyl2` / `D_qWeyl2`: REQUIRED_FOR_QUADRATIC_GUARD - D_qWeyl2 is the parent coefficient of q C_abcd C^abcd or the no-higher-curvature theorem-zero switch.
- `QHESS3609_8_Parena` / `P_arena[q]`: REQUIRED_FOR_ANY_TEST - P_arena maps q(r) or q[x] into R10 alpha(lambda), PPN gamma/beta/alpha_i, clocks, orbital precession or source-GM residuals.
- `QHESS3609_9_runner_law` / `finite q residual law`: FORMULA_READY_INPUTS_MISSING - ||P_arena q|| <= ||P_arena G_q|| (|B_qWeyl| ||P*C|| + |D_qWeyl2| ||C^2|| + ||J_q|| + ||bdry||).

## Decision Gates
- `QDEC3609_0_math_theorem` / `conditional no-pole theorem`: PASS_CONDITIONAL - The Hessian proof is complete: quotient descent plus on-shell reduced equations delete the q row from physical propagators.
- `QDEC3609_1_mts_certificate` / `MTS parent certificate`: FAIL_CURRENT - pi, v_q, first-class degree count, descent and boundary/readout silence are not all signed on one branch.
- `QDEC3609_2_delete_route` / `delete q operator`: NOT_ACTIVATED - Do not delete G_q from B_qWeyl/D_qWeyl2 runners yet.
- `QDEC3609_3_bound_route` / `independent Hessian route`: FORMULAS_FILLED_NOT_NUMERIC - The exact rows needed for Z_q, M_q^2, lambda, domain, boundary, J_q, coefficients and P_arena are now defined.
- `QDEC3609_4_next_route` / `next best attack`: SELECTED_PARENT_PI_OR_ZQ - Either construct the single parent pi/v_q certificate from actual MTS symbols, or extract Z_q and J_q from the parent action candidate.

## Status
- `NO_POLE_THEOREM_PROVED_CONDITIONALLY_MTS_CERTIFICATE_UNSIGNED_HESSIAN_ROWS_FILLED`: 3609 proves the exact parent-action no-pole lemma at Hessian level: for S=Sbar∘pi, v_q in ker(Dpi), and on-shell reduced equations, the q Hessian row/column vanish and q-basic observables contain no physical q pole.
- Decision: do not claim q deletion for MTS yet; the theorem is real but pi/v_q/descent/boundary certificate rows are unsigned. If this certificate cannot be built, use the independent Hessian fill rows to bound q as physical.
- Framework progress: The fork is now mathematically clean: either q is a quotient representative and disappears from physical local GR, or q is a physical residual with explicit Z_q/M_q/J_q/P_arena rows.
- Still missing: parent-owned pi, actual v_q in ker(Dpi), first-class degree count, action/matter/coefficient/readout/boundary descent, or numeric/source-backed Hessian rows

## Validation
- `VAL3609_0_sources_exist`: PASS (all required 3609 source paths exist)
- `VAL3609_1_needles_found`: PASS (all selected 3609 source anchors found)
- `VAL3609_2_outputs_exist`: PASS (all pre-validation 3609 csv outputs written)
- `VAL3609_3_csv_parse`: PASS (source_register:14; no_pole_hessian_proof:7; parent_action_certificate:9; independent_hessian_fill_rows:10; decision_gates:5; status:1; next_target:1; canonical_status:1)
- `VAL3609_4_hessian_proof_present`: PASS (on-shell Hessian row no-pole proof is present)
- `VAL3609_5_certificate_complete`: PASS (all no-pole parent certificate clauses represented)
- `VAL3609_6_hessian_rows_filled`: PASS (independent q Hessian fill rows present)
- `VAL3609_7_no_deletion_claim`: PASS (q no-pole deletion remains unactivated for current MTS)
- `VAL3609_8_no_claim_flags`: PASS (all generated physics rows remain nonclaim)
- `VAL3609_9_next_target_selected`: PASS (3610 pi/vq certificate or Zq/Jq extraction target selected)
- `VAL3609_10_formalization_workbench_untouched`: PASS (no 3609 checkpoint output appears in formalization-workbench outside package/venv noise)

## Next Target
- `NEXT3609_0` -> `3610-Y5-R2FR-parent-pi-vq-certificate-or-Zq-Jq-extraction.md`
- Objective: attempt the concrete parent pi/v_q certificate from actual MTS symbols; if any clause fails, immediately extract or bound Z_q and J_q from the parent action candidate instead of producing another target ledger
- Success gate: must either sign pi and v_q in ker(Dpi) with descent clauses, or produce source-backed/nonclaim numeric-ready rows for Z_q and J_q
