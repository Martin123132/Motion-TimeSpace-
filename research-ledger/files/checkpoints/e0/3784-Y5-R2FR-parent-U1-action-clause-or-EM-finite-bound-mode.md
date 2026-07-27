# 3784 - Parent U(1) Action Clause or EM Finite-Bound Mode

## Status

`PARENT_U1_ACTION_GRAMMAR_WRITTEN_BQ_OWNER_STILL_UNSIGNED`.

3784 takes the leap from missing-list to an actual parent U(1) action grammar. It conditionally derives Ward/Maxwell descent, but the non-circular MTS flow one-form B_Q is still the live gap.

## Result In Plain Terms

3784 writes the actual parent-action fork. If we allow a parent U(1) bundle with a primitive one-form `Pi_Q`, then `A_obs=q_*^{-1}(dtheta_Q-Pi_Q)` is not vague coupling talk: varying `theta_Q` gives current conservation, varying `Pi_Q` gives the Maxwell equation, and varying `g_eff` gives the Maxwell Hilbert stress. The catch is honest and sharp: unless `Pi_Q` is built from a non-circular MTS flow operator `B_Q[Phi_MTS,Psi_Q]`, this is a viable parent extension rather than a derivation from the current real-scalar corpus.

## Parent U(1) Action Clause
- `U1A3784_0_field_space` `MINIMAL_PARENT_EXTENSION_CLAUSE`: statement: Extend the parent field space by Phi_U1=(Phi_MTS,P_Q -> M,theta_Q,Pi_Q,q_*,N_Q,D_Q), where P_Q is a principal U(1) bundle, theta_Q is local fibre phase, Pi_Q is a gauge-invariant parent one-form, q_* is the charge unit, N_Q fixes generator norm, and D_Q stores node/defect data.; derivation_role: names the smallest objects that make the 3781/3783 connection theorem precise
- `U1A3784_1_readout` `EXACT_READOUT_DEFINITION`: statement: A_obs=q_*^{-1}(dtheta_Q-Pi_Q), F_obs=dA_obs=-q_*^{-1}dPi_Q-beta_q wedge A_obs plus defect terms; for fixed q_* and no defects this reduces to F_obs=-q_*^{-1}dPi_Q.; derivation_role: turns EM readout into a connection reconstruction, not an independent inserted A_mu
- `U1A3784_2_parent_lagrangian` `CONDITIONAL_ACTION_GRAMMAR`: statement: S_U1=int sqrt(-g_eff)[-(Z_Pi/(4 q_*^2)) H_ab H^ab + A_obs_a J_Q^a + L_Q(rho_Q,D_a rho_Q,theta_Q,Pi_Q;Phi_MTS) + L_constraint(Pi_Q-B_Q[Phi_MTS,Psi_Q])]+S_defect[D_Q], with H=dPi_Q.; derivation_role: the smallest action grammar that can vary to Maxwell form while exposing the possible smuggle point B_Q
- `U1A3784_3_no_smuggle` `NONCIRCULARITY_CONTRACT`: statement: B_Q must be built from MTS flow primitives before A_obs/F_obs/Maxwell equations are defined; if B_Q is absent or arbitrary, Pi_Q is an added EM field and the route is parent-extension mode, not derived-from-current-MTS mode.; derivation_role: prevents the action from hiding Maxwell inside new notation
- `U1A3784_4_normalization` `ALPHA_OWNER_CLAUSE`: statement: Z_EM=Z_Pi/q_*^2=C_Q N_Q must be q_obs-owned, superselected, or separately bounded; the U(1) bundle fixes compact charge labels but not the continuous Maxwell kinetic normalization.; derivation_role: keeps alpha_EM honest instead of claiming compact U(1) automatically derives it
- `U1A3784_5_same_source` `WARD_SOURCE_CLAUSE`: statement: J_Q must be varied inside the same q_obs-descended total source action as EM stress, so div(T_EM+T_charged+T_binding)=0 follows from one source sector rather than from matched bookkeeping.; derivation_role: connects EM to Pi_M_total and the Newton/PPN source programme

## Variation And Maxwell Descent
- `VAR3784_0_gauge_transform` `EXACT_CONDITIONAL`: result: A_obs transforms as a U(1) connection if theta_Q -> theta_Q+q_* lambda and Pi_Q is gauge-invariant.; calculation: A_obs' = q_*^{-1}(dtheta_Q+q_*dlambda-Pi_Q)=A_obs+dlambda; therefore F_obs is gauge invariant.
- `VAR3784_1_theta_variation` `EXACT_CONDITIONAL`: result: theta_Q variation gives current conservation when the action depends on theta_Q through A_obs and q_obs-descended source terms.; calculation: delta_theta A_obs=q_*^{-1}d(delta theta); delta S=int sqrt(-g) J_Q^a q_*^{-1} nabla_a delta theta = -int sqrt(-g) q_*^{-1}(nabla_a J_Q^a)delta theta + boundary.
- `VAR3784_2_piq_variation` `EXACT_WITH_RESIDUALS`: result: Pi_Q variation gives the Maxwell equation for A_obs if the parent kinetic term is -(Z_Pi/(4q_*^2))|dPi_Q|^2 and source coupling is A_obs dot J_Q.; calculation: delta_Pi A_obs=-q_*^{-1}delta Pi, delta_Pi F_obs=-q_*^{-1}d delta Pi, so the Euler equation is nabla_b(Z_EM F_obs^{ba})=J_Q^a plus B_Q/constraint/defect residuals.
- `VAR3784_3_stress_descent` `EXACT_CONDITIONAL`: result: Metric variation supplies the Maxwell Hilbert stress with normalization Z_EM only if the kinetic term uses the same g_eff and descends through the same q_obs quotient.; calculation: T_EM^{ab}=Z_EM(F^a_c F^{bc}-1/4 g_eff^{ab}F^2); any separate metric, Z_EM vertical drift, or source split re-enters the residual vector.
- `VAR3784_4_vertical_variation` `EXACT_ZERO_OR_BOUND`: result: The local vertical EM obstruction vanishes only under Pi_Q, q_*, Z_EM, current, and defect q_obs descent.; calculation: Lie_EA A_obs=d(Lie_EA theta_Q/q_*)-q_*^{-1}Lie_EA Pi_Q-beta_q,A A_obs; hence R_A=-q_*^{-1}Lie_EA Pi_Q-beta_q,A A_obs, beta_Z,A=Lie_EA ln Z_EM.

## Noncircularity And Flow Owner Tests
- `NCT3784_0_no_A_in_BQ` `UNSIGNED`: requirement: B_Q[Phi_MTS,Psi_Q] contains no A_obs, F_obs, Maxwell equation, Lorentz force, or EM stress as an input.; verdict: blocks derived claim; otherwise Pi_Q is renamed EM
- `NCT3784_1_flow_origin` `PROMISING_UNFILLED`: requirement: B_Q is computed from owned MTS flow primitives such as normalized phase-flow, vorticity, connection on node bundle, or pre-EM Poynting-like stress flow.; verdict: best constructive fork is vorticity/defect flow, but parent operator is not yet written
- `NCT3784_2_no_pure_gradient` `PASSED_AS_GUARD_NOT_AS_CONSTRUCTION`: requirement: dPi_Q must be nonzero away from defects without defining Pi_Q=dtheta_Q or df(psi).; verdict: pure-gradient routes rejected; need primitive one-form or defect curvature
- `NCT3784_3_same_source` `UNSIGNED`: requirement: J_Q, charged matter, EM stress, and binding stress arise from the same source action used by Pi_M_total.; verdict: blocks Newton/PPN promotion until source action is explicit
- `NCT3784_4_normalization` `UNSIGNED`: requirement: q_*, N_Q, and Z_Pi are fixed by parent units/superselection or empirical finite-bound rows, not tuned after data.; verdict: blocks alpha_EM claim; leaves finite-bound mode active

## q_obs Zero Conditions
- `ZC3784_0_PiQ_descent` `MISSING_PARENT_FLOW_OWNER`: zero_condition: Lie_EA Pi_Q=0; residual_if_unsigned: epsilon_Pi_vertical and epsilon_dPi_vertical
- `ZC3784_1_charge_unit` `MISSING_CHARGE_UNIT_SUPERSELECTION`: zero_condition: Lie_EA ln q_*=0; residual_if_unsigned: beta_q,A
- `ZC3784_2_ZEM` `MISSING_ZEM_OWNER`: zero_condition: Lie_EA ln Z_EM=0; residual_if_unsigned: beta_Z,A
- `ZC3784_3_lambda` `MISSING_OPERATOR_BASIS_PROOF`: zero_condition: lambda_A=0 through primitive-only/no-observed-pullback operator basis; residual_if_unsigned: lambda_A
- `ZC3784_4_defects` `MISSING_DEFECT_WILSON_CERTIFICATE`: zero_condition: D_Q and Wilson cycles are q_obs-owned or vanish on the local patch; residual_if_unsigned: epsilon_node
- `ZC3784_5_current` `MISSING_SAME_SOURCE_ACTION`: zero_condition: J_Q descends from the same q_obs total source action; residual_if_unsigned: epsilon_J_Q and EM/source WEP-PPN rows

## EM Finite-Bound Mode
- `epsilon_Pi_vertical`: meaning: vertical change of primitive Pi_Q; arena: A/F readout; numeric_value: MISSING_EPSILON_PI_VERTICAL; action_if_not_zeroed: source_or_bound_before_claim
- `epsilon_dPi_vertical`: meaning: vertical change of dPi_Q/F; arena: EM stress and PPN; numeric_value: MISSING_EPSILON_DPI_VERTICAL; action_if_not_zeroed: source_or_bound_before_claim
- `beta_q,A`: meaning: vertical drift of charge unit; arena: charge units and alpha; numeric_value: MISSING_BETA_Q,A; action_if_not_zeroed: source_or_bound_before_claim
- `epsilon_node`: meaning: node/Wilson/defect residue; arena: topology and local patch; numeric_value: MISSING_EPSILON_NODE; action_if_not_zeroed: source_or_bound_before_claim
- `beta_Z,A`: meaning: vertical drift of Maxwell normalization; arena: WEP, clocks, Gdot, PPN; numeric_value: MISSING_BETA_Z,A; action_if_not_zeroed: source_or_bound_before_claim
- `lambda_A`: meaning: observed Maxwell pullback counterterm; arena: operator basis and alpha; numeric_value: MISSING_LAMBDA_A; action_if_not_zeroed: source_or_bound_before_claim
- `epsilon_J_Q`: meaning: same-source charged-current failure; arena: Hilbert source and Newton/PPN; numeric_value: MISSING_EPSILON_J_Q; action_if_not_zeroed: source_or_bound_before_claim

## Claim Gates
- `CG3784_0_sources`: pass: True; claim_allowed: False; details: all source paths resolve
- `CG3784_1_action_clause`: pass: True; claim_allowed: False; details: minimal parent U1 action grammar written
- `CG3784_2_variation`: pass: True; claim_allowed: False; details: theta and Pi_Q variations give Ward/Maxwell equations conditionally
- `CG3784_3_non_circular_BQ`: pass: False; claim_allowed: False; details: B_Q MTS-flow operator remains unsigned
- `CG3784_4_zero_conditions`: pass: False; claim_allowed: False; details: Pi_Q, q_*, Z_EM, lambda_A, defects, and J_Q descent remain open
- `CG3784_5_finite_mode`: pass: True; claim_allowed: False; details: finite EM residual rows retained
- `CG3784_6_local_GR_EM_claim`: pass: False; claim_allowed: False; details: not claimable until B_Q and zero conditions are parent-signed or bounded

## Decisions
- `DEC3784_0_actual_progress`: decision: The U(1) route can be made into a real parent action clause.; action: Keep it as a viable parent-extension branch rather than treating EM as pure hand closure.
- `DEC3784_1_key_gap`: decision: The only honest derivation gap is now B_Q: the parent-owned MTS flow one-form that is not A/F in disguise.; action: Next target should attempt B_Q from vorticity, node/defect flow, or pre-EM stress/Poynting geometry.
- `DEC3784_2_no_claim`: decision: Do not claim local-GR/EM closure from the action grammar alone.; action: Use finite-bound mode if B_Q cannot be built.

## Next Target
- `3785-Y5-R2FR-derive-BQ-flow-one-form-from-vorticity-defects-or-demote-EM.md`: target_script: scripts/Y5_R2FR_3785_derive_BQ_flow_one_form_from_vorticity_defects_or_demote_EM.py; objective: Try to construct the non-circular B_Q[Phi_MTS,Psi_Q] one-form from MTS flow/vorticity/node-defect/Poynting geometry; if no owned one-form exists, formally demote EM readout to finite-bound parent-extension mode.

## Validation
- `sources_exist` `PASS`: detail: every cited source path exists
- `csv_outputs_parse` `PASS`: detail: all generated CSV outputs exist and parse
- `doc_written` `PASS`: detail: 3784 markdown document written
- `action_clause` `PASS`: detail: parent U1 action clause emitted
- `variation_derivation` `PASS`: detail: theta/Pi_Q/metric/vertical variation rows emitted
- `noncircularity_guard` `PASS`: detail: B_Q no-A/F guard emitted
- `zero_conditions` `PASS`: detail: q_obs zero-or-bound conditions emitted
- `finite_mode` `PASS`: detail: finite EM mode rows stay nonclaim
- `claim_gate_closed` `PASS`: detail: EM/local-GR claim gate remains closed
- `next_target` `PASS`: detail: 3785 B_Q construction target emitted
- `formalization_clean` `PASS`: detail: no 3784 files written under formalization-workbench
