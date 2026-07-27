# 3331 - PPN weak-potential normalization and C_metric bound under AX1090

Run UTC: `2026-06-27T21:04:19.944753+00:00`

## Verdict

3331 does move the PPN branch forward. It does not merely say that a coefficient is missing.

The local PPN residual has two separable pieces:

`C_PPN(lambda) <= A_PPN(q_U,gauge) C_metric(lambda)`.

`A_PPN` is the weak-field/gauge/observable normalization. `C_metric` is the actual MTS metric operator response before PPN normalization.

The weak-potential denominator is

`q_U = |U|/c^2 = G_N M/(r c^2)`

in the calibrated local source frame. This means a tiny raw metric residual can become non-tiny in PPN units because gamma-like slots scale as `q_U^-1` and beta-like slots can scale as `q_U^-2`.

The derived safe maps are

`|delta gamma| <= (H_s^(1)+H_00^(1))/(2 q_U) + epsilon_gauge + epsilon_readout + epsilon_source`,

and

`|delta beta| <= H_00^(2)/(2 q_U^2) + a_beta1 H_00^(1)/q_U + epsilon_gauge + epsilon_readout + epsilon_source`.

So the clean route is not to fight source calibration. The clean route is to declare measured-G/Newtonian closure, project out pure gauge and GM-redefinition modes, then test only the residual physical metric pieces.

The metric response is now factorized as

`C_metric(lambda) = ||Pi_PPN G_PPN W_PPN||^2 ||D_metric S_ell H_pi(lambda) S_ell^dagger D_metric^dagger|| N_source`,

with conservative upper bound

`C_metric <= P_PPN^2 G_fix^2 W_src^2 D_readout^2 S_band^2 H_band(lambda) N_source`.

No PPN/local-GR claim follows. The result is stronger than a missing-input note because it gives the exact slots that must be bounded next.

## Source Register

- `SRC3331_0_3330_doc`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3330-Y5-R2FR-PPN-response-coefficient-and-local-floor-bound-under-AX1090.md` exists=true parse_ok=true role=handoff requiring A_PPN(q_U,gauge) and C_metric
- `SRC3331_1_3330_response`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3330_PPN_RESPONSE_COEFFICIENT.csv` exists=true parse_ok=true role=C_PPN decomposition into A_PPN and C_metric
- `SRC3331_2_3330_inputs`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3330_REQUIRED_INPUTS.csv` exists=true parse_ok=true role=required q_U, gauge, C_metric, and floor inputs
- `SRC3331_3_3322_Ci`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3322_CI_RESPONSE_GATE.csv` exists=true parse_ok=true role=generic C_i projection-propagator-source split
- `SRC3331_4_3328_budget`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3328_RESIDUAL_BUDGET_FORMULAS.csv` exists=true parse_ok=true role=master local residual budget
- `SRC3331_5_PPN_gamma_2053`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2053_PPN_GAMMA_WEAK_FIELD_DERIVATION.csv` exists=true parse_ok=true role=existing weak-field areal PPN gamma bridge
- `SRC3331_6_PPN_observable_3098`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3098_PPN_OBSERVABLE_BOUND.csv` exists=true parse_ok=true role=older PPN observable-bound context
- `SRC3331_7_PPN_GM_gauge_3058`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3058_PPN_GM_ABSORPTION_AND_GAUGE_GATE.csv` exists=true parse_ok=true role=GM absorption and PPN gauge caution

## Weak-Field Normalization

- `WF3331_0_metric_ansatz`: object=PPN weak-field metric; formula=g_00 = -1 + 2 U/c^2 - 2 beta U^2/c^4 + h_00^MTS + O(c^-6); g_ij = (1 + 2 gamma U/c^2) delta_ij + h_ij^MTS + O(c^-4); derivation=PPN observables compare dimensionless metric residuals against powers of q_U=|U|/c^2, so raw h_munu amplitudes cannot be judged without the weak-potential denominator; guard=sign convention is irrelevant for the bound because absolute residual amplitudes are used; status=ANSATZ_FIXED; valid_for_claim=false
- `WF3331_1_qU_definition`: object=weak-potential denominator; formula=q_U := |U|/c^2 = G_N M/(r c^2) in the calibrated local source frame; derivation=after measured-G closure the Newtonian slot defines the source mass used by PPN comparisons; residual first-order metric amplitudes are divided by q_U; guard=if the source mass/GM calibration is not fixed, first-order residuals can be hidden by mass redefinition and the PPN map is not scoreable; status=NORMALIZATION_DERIVED; valid_for_claim=false
- `WF3331_2_gamma_map`: object=PPN gamma residual; formula=|delta gamma| <= (H_s^(1)+H_00^(1))/(2 q_U) + epsilon_gauge + epsilon_readout + epsilon_source; derivation=write h_s^(1)=spatial isotropic first-order residual and h_00^(1)=time first-order residual after Newtonian calibration; gamma is the spatial potential coefficient relative to the calibrated time potential coefficient; guard=pure gauge pieces and GM absorption must be projected out before H_s^(1), H_00^(1) are called physical; status=GAMMA_BOUND_DERIVED; valid_for_claim=false
- `WF3331_3_beta_map`: object=PPN beta residual; formula=|delta beta| <= H_00^(2)/(2 q_U^2) + a_beta1 H_00^(1)/q_U + epsilon_gauge + epsilon_readout + epsilon_source; derivation=beta is a second-order time-metric coefficient, so an actual second-order residual is normalized by q_U^2; unresolved first-order leakage contaminates beta through source-calibration cross terms; guard=beta is not clean unless the first-order Newtonian slot is fixed or explicitly absorbed into measured GM; status=BETA_BOUND_DERIVED_WITH_FIRST_ORDER_GUARD; valid_for_claim=false
- `WF3331_4_preferred_frame_map`: object=non-isotropic PPN residuals; formula=|alpha_PF| <= A_PF H_T/q_U + epsilon_gauge + epsilon_frame; derivation=anisotropic or velocity-frame residual metric pieces enter preferred-frame/preferred-location PPN slots once projected into the standard PPN gauge; guard=if H_T is pure gauge or outside the PPN frame convention it must not be counted as a physical preferred-frame coefficient; status=PREFERRED_FRAME_BOUND_TEMPLATE; valid_for_claim=false

## A_PPN Bound

- `APPN3331_0_gamma`: coefficient=A_gamma(q_U,gauge); formula=A_gamma <= a_gamma/q_U + a_gauge + a_readout + a_source; meaning=linear first-order metric residuals are amplified by the inverse weak potential in gamma-like observables; status=SYMBOLIC_BOUND_DERIVED; valid_for_claim=false
- `APPN3331_1_beta`: coefficient=A_beta(q_U,gauge); formula=A_beta <= a_beta2/q_U^2 + a_beta1/q_U + a_gauge + a_readout + a_source; meaning=second-order time residuals carry a q_U^-2 denominator, with q_U^-1 contamination if first-order source calibration is not closed; status=SYMBOLIC_BOUND_DERIVED; valid_for_claim=false
- `APPN3331_2_vector_tensor`: coefficient=A_vector_tensor(q_U,gauge); formula=A_vector_tensor <= max(a_PF/q_U, a_aniso/q_U) + a_gauge + a_frame; meaning=anisotropic, vector, or frame-dependent metric residuals must be projected into the standard PPN gauge before comparison; status=BOUND_TEMPLATE; valid_for_claim=false
- `APPN3331_3_master`: coefficient=A_PPN(q_U,gauge); formula=A_PPN(q_U,gauge) := max(A_gamma, A_beta, A_vector_tensor, A_gauge_residual); meaning=the worst normalized PPN slot sets the safe response multiplier for C_metric; status=MASTER_APPN_BOUND; valid_for_claim=false
- `APPN3331_4_clean_branch`: coefficient=A_PPN_clean; formula=if H_00^(1) is fully absorbed into measured GM and gauge/readout residuals vanish, A_gamma~O(q_U^-1) and beta is controlled only by genuine H_00^(2)/q_U^2; meaning=this is the least-scrutinized clean route: do not count mass calibration or gauge artifacts as MTS physics; status=CONDITIONAL_CLEAN_BRANCH; valid_for_claim=false

## C_metric Bound

- `CMET3331_0_operator_definition`: quantity=C_metric(lambda); formula=C_metric(lambda) = ||Pi_PPN G_PPN W_PPN||^2 ||D_metric S_ell H_pi(lambda) S_ell^dagger D_metric^dagger|| N_source; derivation=specializes the 3322 C_i response coefficient to gauge-fixed weak-field metric components before q_U normalization; needed_input=Pi_PPN, G_PPN, W_PPN, D_metric, S_ell, H_pi, N_source; status=OPERATOR_BOUND_FORMULA; valid_for_claim=false
- `CMET3331_1_factor_bound`: quantity=factorized upper bound; formula=C_metric <= P_PPN^2 G_fix^2 W_src^2 D_readout^2 S_band^2 H_band(lambda) N_source; derivation=submultiplicativity turns the metric response into individually auditable projection, gauge-fixing, source-window, derivative-readout, smoothing, propagator, and source-normalization factors; needed_input=finite or numeric upper bound for every factor; status=CONSERVATIVE_FACTOR_BOUND; valid_for_claim=false
- `CMET3331_2_bandlimited_green`: quantity=H_band(lambda); formula=H_band(lambda) := sup_{k in PPN band} ||(Z_pi k^2 + M_pi^2)^-1|| or the parent Hessian inverse projected into the PPN band; derivation=a finite parent Hessian gap gives a finite metric response; without Z_pi/M_pi^2 or an equivalent Hessian spectrum the response remains symbolic; needed_input=Z_pi, M_pi^2, band convention, parent Hessian spectrum; status=PROPAGATOR_SLOT_IDENTIFIED; valid_for_claim=false
- `CMET3331_3_source_normalization`: quantity=N_source; formula=N_source is fixed by measured-G closure/Poisson normalization, not by a hidden re-fit inside C_metric; derivation=the local GR branch uses measured G_N to normalize the Newtonian slot; any extra MTS source response must be residual after that calibration; needed_input=source mass convention, GM absorption rule, measured-G closure declaration; status=SOURCE_CALIBRATION_GUARD; valid_for_claim=false
- `CMET3331_4_gauge_projector`: quantity=G_PPN; formula=G_PPN removes pure gauge, coordinate, and GM-redefinition modes before PPN scoring; derivation=PPN residuals are physical only after the metric is in the same observational gauge/frame as the comparator; needed_input=gauge-fixing projector or equivalent invariant observable map; status=GAUGE_GUARD_REQUIRED; valid_for_claim=false

## C_PPN Composition

- `CPPN3331_0_master`: formula=C_PPN(lambda) <= A_PPN(q_U,gauge) C_metric(lambda); meaning=PPN response is the product of weak-potential/gauge normalization and the underlying MTS metric operator response; status=COMPOSITION_DERIVED; valid_for_claim=false
- `CPPN3331_1_tree_residual`: formula=R_tree_PPN <= A_PPN(q_U,gauge) C_metric(lambda_PPN) epsilon_eff_PPN(lambda_PPN)^2; meaning=the first-gradient tree channel is now normalized into PPN units; status=TREE_CHANNEL_COMPOSED; valid_for_claim=false
- `CPPN3331_2_full_budget`: formula=R_PPN <= |R_Gamma_PPN| + A_PPN C_metric epsilon_eff_PPN^2 + epsilon_composite_PPN + epsilon_direct_PPN + epsilon_G_closure_PPN; meaning=full no-cancellation PPN residual budget after 3331; status=FULL_BUDGET_COMPOSED; valid_for_claim=false
- `CPPN3331_3_no_claim_rule`: formula=No PPN/local-GR claim unless A_PPN, C_metric, epsilon_eff, Gamma, composite, direct, and G-closure floors are all source-bounded below a real PPN threshold B_PPN; meaning=3331 narrows the map but does not supply numerical source-grade bounds; status=NO_CLAIM_RULE; valid_for_claim=false

## Required Inputs

- `REQ3331_0_qU_arena`: quantity=q_U=|U|/c^2 for each PPN arena; needed_for=A_gamma, A_beta, A_vector_tensor; current_status=FORMULA_DERIVED_NUMERIC_VALUES_NOT_SOURCED; priority=high; valid_for_claim=false
- `REQ3331_1_gauge_projector`: quantity=G_PPN gauge/invariant observable projector; needed_for=remove pure gauge and GM-absorption modes before scoring h_munu; current_status=STRUCTURAL_REQUIREMENT_DEFINED; priority=high; valid_for_claim=false
- `REQ3331_2_metric_projection`: quantity=Pi_PPN and W_PPN; needed_for=C_metric operator norm; current_status=FACTOR_IDENTIFIED_NUMERIC_BOUND_MISSING; priority=high; valid_for_claim=false
- `REQ3331_3_parent_hessian`: quantity=H_pi(lambda), Z_pi, M_pi^2 or equivalent Hessian spectrum; needed_for=finite metric Green/operator response; current_status=PARENT_NUMERIC_BOUND_MISSING; priority=high; valid_for_claim=false
- `REQ3331_4_source_normalization`: quantity=N_source after measured-G closure and GM absorption; needed_for=prevent Newtonian mass calibration being double-counted as MTS residual; current_status=CLOSURE_CONVENTION_REQUIRED; priority=high; valid_for_claim=false
- `REQ3331_5_real_threshold`: quantity=B_PPN real observational threshold vector; needed_for=claim-grade comparison; current_status=NOT_ATTEMPTED_IN_3331; priority=medium; valid_for_claim=false

## Promotion Gates

- `GATE3331_0_A_PPN_symbolic`: claim=A_PPN(q_U,gauge) is no longer a free placeholder; passed=true; reason=gamma, beta, and anisotropic PPN slots now carry explicit q_U denominators and gauge/source caveats; valid_for_claim=false
- `GATE3331_1_Cmetric_factorized`: claim=C_metric is factorized into auditable operator pieces; passed=true; reason=projection, gauge, source-window, derivative-readout, smoothing, Green/Hessian, and source-normalization factors are separated; valid_for_claim=false
- `GATE3331_2_CPPN_composed`: claim=C_PPN composition is formula-ready; passed=true; reason=C_PPN <= A_PPN C_metric and the tree residual budget are written explicitly; valid_for_claim=false
- `GATE3331_3_A_PPN_numeric`: claim=A_PPN has claim-grade numeric arena bounds; passed=false; reason=q_U values, gauge projector, and threshold vector are not sourced here; valid_for_claim=false
- `GATE3331_4_Cmetric_numeric`: claim=C_metric has claim-grade numeric operator bound; passed=false; reason=parent Hessian spectrum and metric projection norms are not numeric/source-owned; valid_for_claim=false
- `GATE3331_5_PPN_claim`: claim=PPN/local-GR pass is claim-ready; passed=false; reason=3331 derives the map, not the numeric floors and observational threshold comparison; valid_for_claim=false

## Decision Ledger

- `DEC3331_0`: question=Did 3331 move beyond a missing-input ledger?; answer=yes, structurally; reason=it derives the q_U normalization law for PPN gamma/beta slots and turns C_metric into a factorized operator norm; next_action=specialize epsilon_eff_PPN and floor terms using the new A_PPN C_metric composition; valid_for_claim=false
- `DEC3331_1`: question=Is the cleanest route still local GR closure?; answer=yes; reason=source-calibrated measured-G closure lets GM absorption handle the Newtonian slot while MTS residuals are tested only after gauge/source projection; next_action=keep direct psi-matter/psi-EM vertices excluded unless a parent action forces them; valid_for_claim=false
- `DEC3331_2`: question=Can PPN be claimed now?; answer=no; reason=A_PPN and C_metric are derivation-ready but not numeric/source-bounded; floors remain explicit; next_action=derive or bound epsilon_eff_PPN, epsilon_composite_PPN, and R_Gamma_PPN under this normalization; valid_for_claim=false

## Next Target

- `3332-Y5-R2FR-PPN-epsilon-eff-and-floor-specialization-under-AX1090.md`: target_script=scripts/Y5_R2FR_3332_PPN_epsilon_eff_and_floor_specialization.py; objective=specialize epsilon_eff_PPN, epsilon_composite_PPN, R_Gamma_PPN, epsilon_direct_PPN, and epsilon_G_closure_PPN inside the 3331 normalized PPN budget; must_include=T_grad(lambda_PPN); q_U-normalized C_PPN; Gamma proxy versus general Gamma bound; composite CLT/spectral/contact floors; direct vertex silence; no PPN claim; fallback_if_failed=retain full no-cancellation PPN residual vector and move to sourcing real PPN threshold rows only after floor terms are separated; valid_for_claim=false

## Test Notes

- This checkpoint is private and nonclaim.
- It sharpens the PPN branch by deriving the weak-potential denominators instead of treating `C_PPN` as a loose knob.
- It keeps measured-G closure explicit and blocks any hidden source-mass redefinition from masquerading as an MTS prediction.
- It does not use or claim real PPN observational bounds.
- `formalization-workbench` is not modified.
