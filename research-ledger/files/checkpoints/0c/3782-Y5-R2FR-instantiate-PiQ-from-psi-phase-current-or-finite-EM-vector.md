# 3782 - Instantiate Pi_Q from psi Phase Current or Finite EM Vector

## Status

`PIQ_NOT_INSTANTIATED_CURRENT_CORPUS_NONCIRCULARITY_CONTRACT_AND_FINITE_EM_VECTOR_EMITTED`.

The current corpus motivates phase/flow but does not yet supply a non-circular q_obs-owned Pi_Q. A real scalar psi gives no U(1) phase; a covariant current containing A is circular. Finite EM residual rows are retained.

## Result In Plain Terms

3782 tries to fill `Pi_Q` from the actual MTS material. The result is useful but strict: the present core EFT uses a real scalar `psi`, so it does not yet provide a compact U(1) phase. A free complex phase current gives `Pi_Q=dtheta_Q`, which makes `A` pure gauge and `F=0`. A covariant charged current gives `Pi_Q=dtheta_Q-q_*A`, but that already contains `A`, so it is circular if used to derive `A`. Therefore `Pi_Q` is not yet instantiated; the finite EM residual vector stays live.

## psi / Phase Source Audit
- `PSA3782_0_eft_real_psi` `REAL_SCALAR_NO_U1_PHASE`: core EFT psi field. Evidence: the effective-field document defines the microscopic motion field as psi: R^4 -> R and builds geometry from <partial_mu psi partial_nu psi>. Consequence: cannot directly supply theta_Q or compact U(1) phase without extra structure
- `PSA3782_1_pgf_flow_psi` `FLOW_SCALAR_NOT_U1_CONNECTION`: PGF / contradiction-flow Psi. Evidence: motion-timespace-research treats Psi as scalar local tension/divergence of flow with damping/inertial PGF terms. Consequence: useful motivation for Pi_Q, but no one-form transformation law is present
- `PSA3782_2_alpha_phase_language` `NORMALIZATION_ROUTE_NOT_CONNECTION`: fine-structure alpha / EM phase sampling. Evidence: alpha notes describe EM phase/coupling as curvature-memory bandwidth or resolution effect. Consequence: feeds Z_EM/alpha, not A/F q_obs basicness
- `PSA3782_3_yang_mills_A` `GAUGE_FIELD_PRESENT_BUT_NOT_DERIVED_FROM_PSI`: Yang-Mills gauge potential A_mu. Evidence: Yang-Mills file imports a gauge potential and field strength for a gauge theory analogy. Consequence: cannot instantiate Pi_Q unless a parent map from psi/flow to A or Pi_Q is supplied
- `PSA3782_4_motion_flow` `MOTIVATING_FLOW_LANGUAGE`: momentum as motion-field flow. Evidence: relativity notes identify momentum as motion-field flow with resistance. Consequence: candidate source for Pi_Q, but lacks charge unit, U(1) fibre, and current owner

## Pi_Q Candidate Tests
- `PQT3782_0_real_gradient` `FAILS_NONTRIVIAL_MAXWELL_CURVATURE`: Pi_Q = d f(psi). Test: dPi_Q=0 away from singularities, so A=q_*^-1(dtheta_Q-df) is pure gauge or undefined. Next: could be a gauge/clock scalar, not ordinary EM
- `PQT3782_1_complex_phase_promote` `SUPPORTS_PHASE_LABEL_ONLY`: psi = rho exp(i theta_Q), Pi_Q^0=dtheta_Q. Test: A_obs=0 and F_obs=0 if Pi_Q=dtheta_Q. Next: needs independent Pi_Q flow one-form, not just phase gradient
- `PQT3782_2_noether_current_free` `FAILS_NONZERO_EM`: J_phase = Im(psi^* dpsi)=rho^2 dtheta_Q; Pi_Q=J_phase/rho^2. Test: Pi_Q=dtheta_Q, so it still gives zero connection curvature. Next: not enough for Maxwell unless defects/topology are separately owned
- `PQT3782_3_covariant_current` `CIRCULAR_IF_USED_TO_DERIVE_A`: J_Q = rho^2(dtheta_Q-q_* A_obs). Test: using this to define Pi_Q already assumes A_obs, so it is circular as an EM derivation. Next: allowed only after A_obs is independently derived
- `PQT3782_4_mts_flow_oneform` `BEST_ROUTE_NOT_FILLED`: Pi_Q = F_flow[psi,g_eff,tau_obs]. Test: this would work if F_flow has U(1) transformation law, q_obs descent, fixed q_*, source current, and regularity. Next: next target should try to construct this exact F_flow
- `PQT3782_5_poynting_hodge` `PROMISING_BUT_CIRCULAR_UNLESS_PARENT_HODGE_FLOW_EXISTS`: Pi_Q from Hodge/Poynting/background energy-flow. Test: requires already-descended Maxwell/Hodge structure; otherwise it imports EM to derive EM. Next: can become finite flux/source residual if not parent-owned
- `PQT3782_6_alpha_bandwidth` `ZEM_ONLY_NOT_PIQ`: Pi_Q from curvature-memory bandwidth l_max/Gamma_G. Test: affects coupling normalization Z_EM/alpha, not the EM connection one-form. Next: keep under beta_Z,A/lambda_A not A/F basicness

## Non-Circularity Contract
- `NCC3782_0_parent_U1` `MISSING_PARENT_U1_BUNDLE`: theta_Q is a parent S^1 fibre coordinate, not a post-readout label. Why: without this, phase is a scalar convention rather than gauge structure
- `NCC3782_1_non_circular_PiQ` `MISSING_NONCIRCULAR_FLOW_ONEFORM`: Pi_Q[psi] is constructed without A_obs and without Maxwell equations. Why: otherwise the route defines A using A
- `NCC3782_2_qobs_descent` `MISSING_PIQ_VERTICAL_SILENCE`: Lie_EA Pi_Q=0 for every E_A in ker(Dq_obs). Why: this is the direct R_A=0 input from 3781
- `NCC3782_3_fixed_qstar` `MISSING_CHARGE_UNIT_SUPERSELECTION`: beta_q,A=Lie_EA ln q_*=0. Why: otherwise charge-unit drift reopens R_A and dR_A
- `NCC3782_4_current_owner` `MISSING_SAME_SOURCE_WARD_OWNER`: same source action owns J_Q and gives a Ward identity. Why: needed to put EM stress into the total Hilbert source
- `NCC3782_5_node_regularization` `MISSING_PSI_NODE_DEFECT_RULE`: rho=|psi| is nonzero or defects/nodes have a declared source/topological owner. Why: phase current J/rho^2 is singular at nodes
- `NCC3782_6_ZEM_owner` `MISSING_ZEM_ALPHA_OWNER`: Z_EM/N_Q/lambda_A are fixed or bounded independently of A/F readout. Why: prevents a gauge-readout success from overclaiming alpha_EM

## Finite EM Vector
- `FEV3782_0_Pi_vertical` `epsilon_Pi_vertical`: ||Lie_EA Pi_Q||/||Pi_Q|| <= `MISSING_NONCIRCULAR_PIQ_MAP` `dimensionless`. Arena: A/F q_obs basicness
- `FEV3782_1_dPi_vertical` `epsilon_dPi_vertical`: ||d(Lie_EA Pi_Q)||/||dPi_Q|| <= `MISSING_DPIQ_VERTICAL_SILENCE` `dimensionless`. Arena: F_obs leakage; EM stress
- `FEV3782_2_beta_q` `beta_q,A`: Lie_EA ln q_* <= `MISSING_QSTAR_OWNER` `dimensionless`. Arena: charge-unit drift
- `FEV3782_3_node_defect` `epsilon_node`: defect/node contribution to dPi_Q or Wilson phase <= `MISSING_PSI_NODE_DEFECT_RULE` `dimensionless_or_flux_units`. Arena: topological/phase EM residue
- `FEV3782_4_beta_Z` `beta_Z,A`: Lie_EA ln Z_EM <= `MISSING_ZEM_NORM_OWNER` `dimensionless`. Arena: WEP; clocks; PPN; Gdot
- `FEV3782_5_lambda_A` `lambda_A`: allowed observed Maxwell pullback counterterm <= `MISSING_PRIMITIVE_ONLY_OPERATOR_BASIS` `action_coefficient`. Arena: unique F2; alpha_EM
- `FEV3782_6_current` `epsilon_J_Q`: ||nabla_a J_Q^a|| + ||J_Q-J_qobs|| <= `MISSING_SAME_SOURCE_CURRENT_OWNER` `current_norm`. Arena: Hilbert stress/source coupling
- `FEV3782_7_WEP` `eta_EM_AB`: C_Pi epsilon_Pi + C_Z epsilon_ZEM + C_J epsilon_J_Q + C_node epsilon_node <= `2.8e-15` `dimensionless`. Arena: WEP
- `FEV3782_8_PPN_gamma` `delta_gamma_EM`: C_F epsilon_dPi + C_g epsilon_EM_shadow_metric + C_q Delta_q_EM <= `2.3e-05` `dimensionless`. Arena: PPN gamma
- `FEV3782_9_Gdot` `dln_Geff_dt_EM`: |d_t beta_Z| + |d_t beta_q| + |d_t epsilon_dPi| + source exchange <= `9.6e-15` `yr^-1`. Arena: Gdot

## Claim Gates
- `CG3782_0_sources` pass=`True` claim_allowed=`False`: all source paths exist. Details: source register resolves
- `CG3782_1_real_psi_guard` pass=`True` claim_allowed=`False`: real-scalar psi guard emitted. Details: main EFT psi is not yet U(1) phase
- `CG3782_2_circularity_guard` pass=`True` claim_allowed=`False`: covariant-current circularity guard emitted. Details: do not derive A from a current already containing A
- `CG3782_3_non_circular_contract` pass=`True` claim_allowed=`False`: Pi_Q non-circularity contract emitted. Details: exact clauses listed
- `CG3782_4_PiQ_instantiated` pass=`False` claim_allowed=`False`: Pi_Q successfully instantiated. Details: no candidate currently passes all parent clauses
- `CG3782_5_finite_vector_nonclaim` pass=`True` claim_allowed=`False`: finite EM vector remains nonclaim. Details: missing Pi_Q/q*/Z/current/node inputs retained
- `CG3782_6_EM_local_GR_claim` pass=`False` claim_allowed=`False`: EM/local-GR promotion claim allowed. Details: blocked until non-circular Pi_Q, q*, Z_EM, lambda_A, current, and node clauses close

## Decisions
- `DEC3782_0_main_result`: Pi_Q is not yet instantiated from the current corpus. Action: The main psi field is real/scalar in the EFT source, and phase/current language is not yet a parent U(1) bundle map.
- `DEC3782_1_best_route`: Do not abandon the route: build the missing parent object explicitly. Action: The least-cheaty next step is a parent U(1)-bundle upgrade or proof that an existing complex psi sector already supplies it.
- `DEC3782_2_no_circularity`: A covariant matter current cannot be used to derive A if it already contains A. Action: Use it only after A/Pi_Q is independently supplied, or keep it as a finite residual.
- `DEC3782_3_alpha_guard`: Alpha/Z_EM remains separate from A/F readout. Action: Even a successful Pi_Q will still need N_Q/Z_EM/lambda_A owner work before EM-lock.

## Next Target
- `3783-Y5-R2FR-parent-U1-bundle-upgrade-or-PiQ-finite-bound-runner.md`: Try the minimal parent U(1)-bundle upgrade: promote or identify psi=rho exp(i theta_Q), define a non-circular Pi_Q flow one-form, handle nodes/Wilson sectors, and test q_obs descent; if this is not parent-owned, keep the finite EM vector as the local route.

## Validation
- `sources_exist` `PASS`: every cited source path exists
- `csv_outputs_parse` `PASS`: all generated CSV outputs exist and parse
- `doc_written` `PASS`: 3782 markdown document written
- `real_psi_guard` `PASS`: real psi guard emitted
- `candidate_tests` `PASS`: Pi_Q candidate tests emitted
- `noncircularity_contract` `PASS`: non-circularity contract emitted
- `finite_vector` `PASS`: finite EM vector emitted
- `claim_gate_closed` `PASS`: EM/local-GR claim gate remains closed
- `next_target` `PASS`: 3783 parent U(1) target emitted
- `formalization_clean` `PASS`: no 3782 files written under formalization-workbench
