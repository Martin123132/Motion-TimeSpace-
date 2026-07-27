# 3781 - Construct EM Connection from MTS Flow or Bound R_A and beta_Z

## Status

`PHASE_FLOW_CONNECTION_ROUTE_DERIVED_A_F_CONDITIONAL_ZEM_ALPHA_STILL_UNSIGNED`.

A_obs=q_*^{-1}(dtheta_Q-Pi_Q) gives an exact route to R_A=0 if Pi_Q and q_* are q_obs-owned; Z_EM/alpha still requires an independent norm/operator/current owner.

## Result In Plain Terms

3781 finds the clean constructive route for the EM readout. If MTS supplies a U(1) phase `theta_Q`, a q_obs-owned phase-flow one-form `Pi_Q`, and a fixed charge unit `q_*`, then `A_obs=q_*^{-1}(dtheta_Q-Pi_Q)`. Along hidden q_obs fibres, the only non-gauge residue is `R_A=-q_*^{-1}Lie_EA Pi_Q-beta_q,A A_obs`. So `Pi_Q` vertical silence and fixed `q_*` give `R_A=0` and `dR_A=0`. That is real progress. But `Z_EM`/alpha still needs an independent norm/operator/current owner; compact U(1) alone does not fix the Maxwell kinetic coefficient.

## Phase-Flow Connection Theorem
- `PFC3781_0_parent_data` `SETUP`: Assume a parent U(1)-phase variable theta_Q, a phase-flow one-form Pi_Q, and a charge unit q_*. Meaning: This is the minimal constructive EM connection package.
- `PFC3781_1_connection_definition` `EXACT_CONNECTION_ANSATZ`: Define A_obs := q_*^{-1}(d theta_Q - Pi_Q). Meaning: Under theta_Q -> theta_Q + q_* chi, A_obs -> A_obs + d chi if Pi_Q is gauge invariant.
- `PFC3781_2_vertical_variation` `EXACT_RESIDUE_FORMULA`: For E_A in ker(Dq_obs), Lie_EA A_obs = d(Lie_EA theta_Q/q_*) - q_*^{-1} Lie_EA Pi_Q - beta_q,A A_obs. Meaning: The non-gauge residue is R_A = -q_*^{-1} Lie_EA Pi_Q - beta_q,A A_obs.
- `PFC3781_3_zero_condition` `EXACT_CONDITIONAL_ZERO_PROOF`: If Lie_EA Pi_Q=0 and beta_q,A=0, then Lie_EA A_obs=d(Lie_EA theta_Q/q_*), hence R_A=0. Meaning: This closes the 3780 A-basicness branch without pretending a physical residue is gauge.
- `PFC3781_4_curvature` `EXACT_F_BASICNESS_ROUTE`: F_obs=dA_obs=-q_*^{-1} dPi_Q when q_* is fixed, so Lie_EA F_obs=-q_*^{-1} d(Lie_EA Pi_Q)-beta_q,A F_obs. Meaning: If Pi_Q and q_* are vertical-silent, F is q_obs-basic.
- `PFC3781_5_current_Ward` `CONDITIONAL_WARD_ROUTE`: Gauge symmetry of theta_Q with the same source action gives the Ward identity nabla_a J_Q^a=0 and makes R_A couple only to a genuine current-descent failure. Meaning: This connects the EM readout route to same-source Hilbert stress.
- `PFC3781_6_ZEM_owner` `CONDITIONAL_ZEM_ZERO_ROUTE_WITH_GUARD`: If Z_EM = C_Q N_Q with C_Q and the charge-generator norm N_Q q_obs-owned or superselected, then beta_Z,A=Lie_EA ln Z_EM=0. Meaning: This is the extra owner needed for the Maxwell kinetic normalization.
- `PFC3781_7_no_go_guard` `NO_OVERCLAIM_GUARD`: Phase-flow construction can close A/F readout but cannot by itself prove unique F^2 or alpha_EM; 1398-1400 keep lambda_A and alpha_EM finite unless the operator/norm/current owner is signed. Meaning: No local-GR or EM-lock claim follows from compact U(1) alone.

## Parent Input Audit
- `PFI3781_0_theta_Q` `MOTIVATED_NOT_PARENT_SIGNED`: parent U(1) phase theta_Q. Evidence: suggested by MTS phase/psi/gauge material, not formalized as a q_obs bundle coordinate. Next: define S^1 phase field and transformation law
- `PFI3781_1_Pi_Q` `MISSING_EXPLICIT_PARENT_MAP`: phase-flow one-form Pi_Q. Evidence: MTS has flow/phase/current language, but no unique q_obs-owned Pi_Q map is currently supplied. Next: construct Pi_Q from psi phase/current or mark residual
- `PFI3781_2_q_star` `MISSING_FIXED_CHARGE_UNIT_OWNER`: fixed charge unit q_*. Evidence: compact U(1) supports a charge lattice only after a base unit exists. Next: parent-own q_* or keep beta_q,A residual
- `PFI3781_3_N_Q` `MISSING_ZEM_NORM_OWNER`: charge-generator norm or kinetic normalization N_Q. Evidence: 1399/1400 say compact U(1) does not fix the continuous Maxwell kinetic coefficient. Next: derive N_Q from parent metric/topological level/spectral owner or bound alpha_EM
- `PFI3781_4_no_pullback_lambda` `NOT_EXCLUDED`: no standalone observed Maxwell pullback counterterm lambda_A. Evidence: 1398 gives a no-go for locality/gauge/diffeomorphism-only exclusion. Next: needs primitive-only operator basis or finite lambda_A vector
- `PFI3781_5_same_source_current` `MISSING_CURRENT_OWNER`: same q_obs source action owns J_Q. Evidence: 3779/3780 require Ward/current descent but current corpus has not signed it. Next: connect phase-flow current to total Hilbert source
- `PFI3781_6_local_patch` `MISSING_LOCAL_COHOMOLOGY_CERTIFICATE`: local contractible patch or Wilson silence. Evidence: 3780 allows local simplification but parent document has not declared the patch/cohomology guard. Next: declare H^1(U)=0 for local PPN/Newton patch or bound Wilson terms

## Residual Formulas
- `RBF3781_0_RA` `R_A`: -q_*^{-1} Lie_EA Pi_Q - beta_q,A A_obs. Meaning: non-gauge vertical EM potential residue. Zero condition: zero iff Pi_Q and q_* are vertical-silent
- `RBF3781_1_dRA` `dR_A`: -q_*^{-1} d(Lie_EA Pi_Q) - beta_q,A F_obs - d(beta_q,A) wedge A_obs. Meaning: vertical EM field-strength leakage. Zero condition: zero iff Pi_Q/q_* are silent and beta_q,A is zero/constant-silent
- `RBF3781_2_beta_q` `beta_q,A`: Lie_EA ln q_*. Meaning: charge-unit leakage along hidden fibre. Zero condition: feeds A/F residue and alpha normalization
- `RBF3781_3_beta_Z` `beta_Z,A`: Lie_EA ln Z_EM = Lie_EA ln C_Q + Lie_EA ln N_Q. Meaning: Maxwell kinetic/alpha_EM leakage. Zero condition: zero only from q_obs/superselected normalization owner
- `RBF3781_4_lambda_A` `lambda_A`: coefficient of allowed observed Maxwell pullback counterterm. Meaning: unique F2 failure from 1398/1400. Zero condition: finite residual unless primitive-only operator basis forbids it
- `RBF3781_5_R_EM_local` `R_EM_local`: (R_A,dR_A,beta_q,A,beta_Z,A,lambda_A,current_owner,Wilson). Meaning: joined local EM residual vector. Zero condition: must be zeroed or bounded before local-GR EM promotion

## Z_EM / Alpha Guard
- `ZOG3781_0_compact_U1` `SUPPORT_ONLY`: compact U(1) phase/charge lattice helps: helps define charge labels and gauge orbit; does not do: does not fix continuous Maxwell kinetic coefficient N_Q or alpha_EM
- `ZOG3781_1_phase_flow_connection` `A_F_ROUTE_ONLY`: A_obs=q_*^{-1}(d theta_Q-Pi_Q) helps: can close q_obs A/F readout if Pi_Q and q_* descend; does not do: does not prove Z_EM or exclude lambda_A F^2
- `ZOG3781_2_norm_owner` `PROMISING_BUT_UNSIGNED`: Z_EM=C_Q N_Q helps: would close beta_Z,A if C_Q,N_Q are q_obs-owned/superselected; does not do: current corpus has no fixed N_Q owner
- `ZOG3781_3_no_counterterm_guard` `REQUIRES_STRONG_PARENT_SELECTION_RULE`: primitive-only/no-pullback operator basis helps: would exclude standalone lambda_A; does not do: 1398 says ordinary locality/gauge/diffeomorphism do not exclude it
- `ZOG3781_4_finite_alpha_route` `FALLBACK_NONCLAIM`: finite alpha_EM residual vector helps: honest fallback if norm owner is not derived; does not do: requires clock/WEP/R10/PPN source-backed projections

## Local EM Residual Vector
- `ELR3781_0_epsilon_A_perp` `epsilon_A_perp`: ||R_A||/||A_obs|| with R_A=-q_*^{-1}Lie_EA Pi_Q-beta_q,A A_obs <= `MISSING_PI_Q_AND_QSTAR_VERTICAL_SILENCE` `dimensionless_or_field_norm`. Arena: gauge/current; EM readout
- `ELR3781_1_epsilon_F_vertical` `epsilon_F_vertical`: ||dR_A||/||F_obs|| <= `MISSING_DPI_Q_VERTICAL_SILENCE` `dimensionless`. Arena: EM stress; PPN; Newton GM
- `ELR3781_2_beta_q` `beta_q,A`: Lie_EA ln q_* <= `MISSING_CHARGE_UNIT_SUPERSELECTION` `dimensionless`. Arena: charge normalization; alpha_EM
- `ELR3781_3_beta_Z` `beta_Z,A`: Lie_EA ln Z_EM <= `MISSING_ZEM_NORM_OWNER` `dimensionless`. Arena: WEP; clocks; Gdot; PPN
- `ELR3781_4_lambda_A` `lambda_A`: standalone observed Maxwell pullback coefficient <= `MISSING_PRIMITIVE_ONLY_OPERATOR_BASIS` `declared_action_units`. Arena: unique F2; alpha_EM
- `ELR3781_5_current_owner` `epsilon_J_Q`: ||nabla_a J_Q^a|| + ||J_Q-J_qobs|| <= `MISSING_SAME_SOURCE_WARD_OWNER` `current_norm`. Arena: same-source Hilbert stress
- `ELR3781_6_Wilson` `epsilon_Wilson`: max_C |int_C R_A|/Phi0 <= `MISSING_LOCAL_COHOMOLOGY_OR_BOUNDARY_SILENCE` `dimensionless`. Arena: phase; quantum/EM readout
- `ELR3781_7_WEP` `eta_EM_AB`: C_A epsilon_A_perp + C_F epsilon_F_vertical + C_Z epsilon_ZEM + C_J epsilon_J_Q <= `2.8e-15` `dimensionless`. Arena: WEP envelope
- `ELR3781_8_gamma` `delta_gamma_EM`: C_g epsilon_EM_shadow_metric + C_F epsilon_F_vertical + C_q Delta_q_EM <= `2.3e-05` `dimensionless`. Arena: PPN gamma envelope
- `ELR3781_9_Gdot` `dln_Geff_dt_EM`: |d_t ln Z_EM| + |d_t beta_q| + |d_t epsilon_F_vertical| + source exchange <= `9.6e-15` `yr^-1`. Arena: Gdot envelope

## Claim Gates
- `CG3781_0_sources` pass=`True` claim_allowed=`False`: all source paths exist. Details: source register resolves
- `CG3781_1_theorem` pass=`True` claim_allowed=`False`: phase-flow connection theorem emitted. Details: A=q^-1(dtheta-Pi) route derived
- `CG3781_2_residue_formula` pass=`True` claim_allowed=`False`: R_A and beta residual formulas emitted. Details: R_A=-q^-1 Lie Pi - beta_q A
- `CG3781_3_zem_guard` pass=`True` claim_allowed=`False`: Z_EM/alpha no-overclaim guard emitted. Details: compact U(1) not enough for alpha
- `CG3781_4_inputs_parent_signed` pass=`False` claim_allowed=`False`: phase-flow inputs parent-signed. Details: theta_Q/Pi_Q/q*/N_Q/current/Wilson clauses unsigned
- `CG3781_5_finite_vector_nonclaim` pass=`True` claim_allowed=`False`: finite local EM vector remains nonclaim. Details: missing parent/source inputs retained
- `CG3781_6_EM_promotion` pass=`False` claim_allowed=`False`: EM promoted to descended local-GR Hilbert stress. Details: blocked until A/F route and Z_EM/unique-F2/current clauses close

## Decisions
- `DEC3781_0_best_news`: A/F basicness has a constructive route. Action: If `Pi_Q` is q_obs-owned and `q_*` is fixed, then `R_A=0` and `dR_A=0` follow exactly.
- `DEC3781_1_hard_wall`: Z_EM/alpha is still a separate owner problem. Action: Do not let a successful phase-flow connection imply a fixed Maxwell kinetic coefficient.
- `DEC3781_2_less_scrutinized_route`: The least-cheaty route is to derive the U(1) bundle connection first, then derive or bound the kinetic normalization second. Action: This separates gauge/readout success from alpha_EM overclaim.
- `DEC3781_3_next`: Instantiate `Pi_Q` from actual MTS `psi` phase/current/flow objects. Action: Build the `psi` phase-current source map and test whether it is q_obs-owned or only a finite residual.

## Next Target
- `3782-Y5-R2FR-instantiate-PiQ-from-psi-phase-current-or-finite-EM-vector.md`: Try to define Pi_Q from the actual MTS psi/phase/current/flow corpus and prove it is q_obs-owned; if not, wire Lie_EA Pi_Q, beta_q,A, beta_Z,A, and lambda_A into the finite EM local residual vector.

## Validation
- `sources_exist` `PASS`: every cited source path exists
- `csv_outputs_parse` `PASS`: all generated CSV outputs exist and parse
- `doc_written` `PASS`: 3781 markdown document written
- `connection_theorem` `PASS`: phase-flow connection theorem emitted
- `ra_formula` `PASS`: R_A residual formula emitted
- `dRA_formula` `PASS`: dR_A residual formula emitted
- `zem_guard` `PASS`: Z_EM/alpha guard emitted
- `nonclaim_vector` `PASS`: finite EM local vector remains nonclaim
- `claim_gate_closed` `PASS`: EM promotion claim gate remains closed
- `next_target` `PASS`: 3782 Pi_Q instantiation target emitted
- `formalization_clean` `PASS`: no 3781 files written under formalization-workbench
