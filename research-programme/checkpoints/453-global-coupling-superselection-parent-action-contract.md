# 453 - Global Coupling Superselection Parent Action Contract

Private P8/R4/R9/R10/R11 coupling checkpoint. This is not a public Einstein-Hilbert, measured-GM, Newtonian-limit, PPN, fifth-force, local-GR, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 452 showed that `G_eff=kappa_eff c^4/(8 pi)` is harmless only if `kappa_eff` is constant and universal.

This checkpoint writes the exact parent-action contract needed to make `kappa_eff` a true global/superselection coupling rather than a local MTS scalar hidden inside source normalization.

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/global_coupling_superselection_parent_action_contract.py` |
| Run directory | `runs\20260602-164500-global-coupling-superselection-parent-action-contract` |
| Status | `global_coupling_superselection_parent_action_contract_written_exact_parent_options_kappa_global_not_parent_derived_Gdot_source_range_rows_retained_no_Newton_or_local_GR_pass` |
| Claim ceiling | `global_coupling_superselection_contract_only_no_measured_GM_Newton_PPN_or_local_GR_pass` |
| Contract | `source-intake\mts_residuals\P8_global_coupling_superselection_CONTRACT.csv` |
| Next target | `454-PiM-parent-symplectic-projector-algebra-attempt.md` |

## 3. Source Register

| source_file | exists | role |
| --- | --- | --- |
| 452-constant-universal-Geff-kappa-identity-attempt.md | True | immediate constant G_eff/kappa identity attempt and CU0-CU8 contract |
| source-intake/mts_residuals/P8_constant_universal_Geff_kappa_CONTRACT.csv | True | constant universal G_eff/kappa contract feeding this superselection gate |
| 448-constant-sector-universality-theorem-attempt.md | True | constant-sector superselection pattern and quotient-invariance warning |
| source-intake/mts_residuals/P8_constant_sector_universality_CONTRACT.csv | True | constant-sector contract showing trivial MTS action requirements |
| 402-EH-source-normalization-parent-pair.md | True | same-frame EH/source normalization and G_eff algebra |
| 424-same-frame-EH-source-Poisson-reduction-gate.md | True | Poisson reduction gate requiring same-frame constant kappa |
| 451-mass-flux-projector-Euler-calibration-attempt.md | True | mass-flux closure attempt showing measured-GM still needs constant coupling |
| 260-C3-unit-stress-normalization-parent-action-attempt.md | True | older unit/stress normalization caveat against typing constants into the action |
| 255-memory-stress-exchange-normalization-or-kappa-mem-free.md | True | kappa_mem analogy and warning not to confuse cosmological memory normalization with local kappa_eff |
| runs/20260602-101500-Ward-Bianchi-exchange-owner-for-Poisson-source/results/Ward_identity_chain.csv | True | Bianchi/Ward chain exposing T_obs grad kappa_eff exchange term |
| runs/20260602-101500-Ward-Bianchi-exchange-owner-for-Poisson-source/results/source_residual_decomposition.csv | True | delta_kappa_source residual mapping |
| runs/20260601-191500-universal-matter-coupling-theorem-attempt/results/matter_action_contract.csv | True | single observed geometry and matter constants contract |
| runs/20260601-191500-universal-matter-coupling-theorem-attempt/results/forbidden_vertices.csv | True | forbidden matter-memory/source vertices |
| runs/20260601-000057-universal-coupling-parent-contract-or-local-bound-data-runner/results/universal_coupling_contract.csv | True | universal coupling and constants-not-memory-fields contract |
| runs/20260602-150000-source-owner-current-parent-action-contract/results/parent_action_blocks.csv | True | source-owner parent-action blocks and coupling/source-normalization requirements |

## 4. Theorem Statement

| part | statement | mathematical_form | status |
| --- | --- | --- | --- |
| conditional_superselection_contract | If the parent configuration space factorizes into dynamical fields times a global coupling sector, kappa_eff belongs only to the global sector, and all MTS selectors, matter labels, source labels, range labels, frames, and local variations act trivially on that sector, then d kappa_eff=0 and G_eff is constant and universal. | Q_parent=Q_dyn x K_global; kappa_eff in K_global; delta_local kappa_eff=0; L_xi kappa_eff=0; partial_{Z,A,lambda,r,t,frame} kappa_eff=0 => dG_eff=0 | valid_conditional_route |
| exact_parent_action_contract | A future parent action must state whether kappa_eff is a non-varied sector label, a topological/integration constant with a derived zero-gradient equation, or a local scalar/source-normalization field. The first two can keep Newton alive; the last reopens scalar-tensor and source residual branches. | kappa_eff notin Gamma(local scalar bundle) OR E_A3: d kappa_eff=0; otherwise q_loc contains kappa_eff^-1 P_loc[T_obs nabla kappa_eff] | contract_written_not_parent_derived |
| no_derivation_warning | Declaring kappa_eff global is a legitimate theory-sector premise, but it is not yet a derivation from MTS primitives. The corpus currently has repeated requirements for constant kappa_eff, not a completed superselection proof. | CU1/GS1 remain not_parent_derived | blocks_overclaim |
| Bianchi_arbitrary_source_route | Bianchi can force local gradients of kappa_eff to vanish only under the stronger premise that the same-frame matter stress is separately conserved for arbitrary local sources and there are no hidden exchange owners. With exchange sectors retained, Bianchi maps gradients into residuals instead of killing them. | nabla_mu T_obs^{mu nu}=0 for arbitrary T_obs and nabla E_EH=0 => T_obs^{mu nu} nabla_mu kappa_eff=0 => nabla kappa_eff=0; with exchange, term remains in q_loc | conditional_only |
| scalar_branch_fallback | If kappa_eff is allowed to depend on MTS invariants, local memory, species/source labels, radius, range, or frame, it is no longer a Newton constant. It becomes an executable residual branch that must be derived zero or bounded. | kappa_eff=kappa0 F(Z,I_Q,C_D,A,lambda,r,t,frame) => R1/R4/R9/R10/R11 active | retained_fallback |

## 5. Parent Options

| option | mechanism | mathematical_form | what_it_closes | cost_or_warning | current_status |
| --- | --- | --- | --- | --- | --- |
| P0_superselection_parameter | kappa_eff is a non-dynamical global coupling labeling a theory sector. | kappa_eff in K_global; not varied by compact-support local variations | local d kappa_eff, Gdot, source/range/radial running if all MTS actions are trivial | closure-level unless the parent explains why K_global is part of the configuration category | sufficient_as_explicit_premise_not_derived |
| P1_topological_zero_form | derive kappa_eff as a closed zero-form or integration constant using a motivated topological pair. | delta A_3 gives d kappa_eff=0 on connected local domains | spacetime gradients without adding scalar force if kappa_eff has no kinetic/local matter vertex | needs actual parent topological sector and boundary policy; otherwise it is a dressed constraint | promising_future_parent_route_not_in_corpus |
| P2_Lagrange_zero_gradient | insert a constraint field imposing d kappa_eff=0. | S_constraint=int Lambda^mu partial_mu kappa_eff | formal local gradients | ad hoc unless Lambda has gauge/topological origin; variation may add unowned stress | not_acceptable_as_bare_patch |
| P3_Bianchi_for_arbitrary_sources | use same-frame Bianchi identity plus separately conserved arbitrary matter stress to force gradients to zero. | T_obs^{mu nu} nabla_mu kappa_eff=0 for arbitrary T_obs => nabla kappa_eff=0 | local spacetime gradients of kappa_eff | fails when hidden exchange, non-EH divergence, boundary flux, or nonmetric matter exchange remains active | conditional_narrow_route |
| P4_units_calibration | treat a constant rescaling of kappa_eff as measured-G calibration. | kappa_eff=kappa0 constant; G_measured absorbs kappa0 | absolute value overclaim only | does not derive constancy and does not predict numerical G | policy_only |
| P5_scalar_field_branch | allow kappa_eff to be a local scalar or MTS function and carry it as a residual branch. | kappa_eff=kappa0 F(Z,I_Q,C_D,A,lambda,r,t) | nothing automatically | becomes scalar-tensor/source-normalization physics with Gdot, fifth-force, and source-charge locks | retained_fallback_if_P0_P1_P3_fail |

## 6. Superselection Contract

The global-coupling superselection contract has been written to `source-intake\mts_residuals\P8_global_coupling_superselection_CONTRACT.csv`.

| contract_id | required_identity | mathematical_form | closes_component | affected_rows | current_status | evidence_needed | fallback_if_missing |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GS0_configuration_factorization | the parent configuration category splits dynamical MTS/local fields from a global coupling sector | Q_parent=Q_dyn x K_global with kappa_eff in K_global | local-field interpretation of kappa_eff | R4;R9;R10;R11 | not_parent_derived | parent action or categorical statement showing K_global is not a local scalar bundle | kappa_eff remains a possible local source-normalization field |
| GS1_kappa_not_local_field | kappa_eff is not varied by compact-support local variations and has no local Euler-Lagrange equation | delta_local kappa_eff=0; kappa_eff notin Gamma(E_local) | local gradient, local scalar force, scalar-tensor leakage | R3;R4;R9;R10;R11 | not_parent_derived | superselection or topological zero-form derivation | retain scalar-kappa branch and PPN/fifth-force locks |
| GS2_trivial_MTS_action_on_kappa | MTS selectors, memory variables, quotient invariants, projector/domain data, and material markers act trivially on kappa_eff | L_xi kappa_eff=0 and partial_Z kappa_eff=partial_IQ kappa_eff=partial_C kappa_eff=partial_D kappa_eff=0 | memory/domain/projector dependence of G_eff | R5;R6;R7;R8;R9;R10;R11 | not_parent_derived | parent symmetry/no-extension theorem forbidding kappa_eff(Z,I_Q,C_D,D_boundary) | Gdot, domain, and fifth-force residual rows remain active |
| GS3_no_species_marker_source_label | kappa_eff carries no species, composition, source-owner, preparation-marker, or material label | partial_A kappa_eff=partial_m kappa_eff=partial_source kappa_eff=0 | composition-dependent active gravitational source charge | R1;R4;R9;R11 | not_parent_derived | source-current Ward universality plus kappa superselection | R1 source charge and measured-GM residuals remain active |
| GS4_no_range_radial_time_dependence | kappa_eff has no radius, finite-range, clock-time, epoch, or local boundary dependence in the local branch | partial_r kappa_eff=partial_lambda kappa_eff=partial_t kappa_eff=partial_boundary kappa_eff=0 | Gdot, radial G, Yukawa/range hair, preferred-location coupling | R3;R4;R7;R8;R9;R10;R11 | not_parent_derived | superselection/topological constant route plus boundary no-hair theorem | execute Gdot, alpha(lambda), radial-source, and boundary residual bounds |
| GS5_Bianchi_arbitrary_source_consistency | Bianchi is used only in a same-frame, separately conserved, arbitrary-source branch or else grad kappa is retained as exchange | if nabla T_obs=0 for arbitrary T_obs then nabla kappa_eff=0; otherwise q_loc includes kappa_eff^-1 P_loc[T_obs nabla kappa_eff] | Bianchi overclaim and hidden exchange ambiguity | R0;R3;R4;R7;R9;R10;R11 | conditional_only | same-frame conservation theorem with all exchange owners absent, or explicit residual coefficient | delta_kappa_source row remains in the exchange ledger |
| GS6_constant_offset_policy | a global constant offset in kappa_eff is calibration only unless the parent action predicts its absolute normalization | delta kappa_eff/kappa_eff=constant_global with all derivatives zero | false prediction of numerical G | R4;R9;R11 | policy_written_not_parent_normalization | absolute coupling normalization theorem if predicting G itself | claim only derivative/source silence, not the numerical value of G |
| GS7_scalar_branch_fallback | if any dependence survives, it is promoted to an executable residual branch rather than hidden inside measured GM | dln_Geff_dt, partial_A ln G_eff, partial_r ln G_eff, alpha(lambda), delta_kappa_source | nothing; keeps falsifiable residuals visible | R1;R3;R4;R7;R8;R9;R10;R11 | fallback_policy_only | numeric coefficients, priors, and bound comparison for any nonzero branch | no measured-GM, Newton, PPN, or local-GR claim |
| GS8_evaluator_mapping | failed GS rows activate the local residual evaluator and empirical locks | GS failure -> residual_vector[R1,R4,R9,R10,R11] active | silent loss of failed assumptions | R1;R4;R9;R10;R11 | not_yet_executable | machine-readable mapping from GS0-GS7 to local-bound residual evaluator | manual gate discipline required before any local-GR claim |

## 7. Counterexamples

| counterexample | construction | why_it_fails | required_blocker | affected_contracts |
| --- | --- | --- | --- | --- |
| typed_constant_in_action | write kappa_eff as a symbol in S_EH but never state whether it is global, varied, or derived | notation does not decide ontology; a typed constant can hide a local field assumption | configuration-factorization statement or topological zero-form derivation | GS0;GS1;GS6 |
| bare_lambda_dk_constraint | add Lambda^mu partial_mu kappa_eff only to force d kappa_eff=0 | without gauge/topological origin it is an inserted plateau axiom with possible unowned stress | motivated topological pair, boundary conditions, and Ward ledger ownership | GS1;GS5 |
| kappa_of_memory | kappa_eff=kappa0 F(Z_memory,I_Q,C_D) | cosmological or memory success leaks into local Gdot/source normalization | trivial MTS action on K_global or local memory no-hair theorem | GS2;GS4;GS7 |
| kappa_of_species | kappa_A=kappa0(1+epsilon_A) or kappa_eff(A,m) | composition-dependent active source coupling survives one observed coframe | source-current Ward universality plus species-blind kappa sector | GS3;GS7 |
| kappa_of_range_or_radius | G_eff(r,lambda)=G0[1+alpha exp(-r/lambda)] | Newton inverse-square and local PPN limits gain fifth-force/radial-hair residuals | range/radial derivative theorem or executable alpha(lambda) bound | GS4;GS7 |
| conformal_frame_kappa | kappa_eff is constant in one frame but matter clocks and EH operator use different frames | constant coupling can be a frame artefact rather than a measured-G statement | same observed coframe and source-normalization theorem | GS0;GS5;GS6 |
| Bianchi_with_hidden_exchange | use Bianchi to set grad kappa_eff=0 while non-EH, boundary, projector, or nonmetric exchange terms remain active | Bianchi then owns exchange; it does not erase the exchange residual | all exchange owners theorem-zero or explicit residual mapping | GS5;GS8 |
| constant_offset_value_claim | treat kappa_eff=kappa0 constant as a prediction of the measured numerical value of G | constant offset is calibration unless the parent fixes absolute normalization | absolute coupling normalization theorem | GS6 |

## 8. Gate Tests

| gate | pass_condition | current_result | evidence |
| --- | --- | --- | --- |
| contract_makes_global_status_explicit | kappa_eff global/superselection status is a named parent-action requirement | pass | GS0 and GS1 written |
| topological_route_not_overclaimed | topological zero-form route is treated as possible future derivation, not current corpus result | pass | P1 status is promising_future_parent_route_not_in_corpus |
| Bianchi_not_used_as_magic | Bianchi only kills grad kappa under arbitrary separately conserved same-frame matter stress | pass | GS5 and Bianchi_arbitrary_source_route |
| constant_offset_not_prediction | constant kappa offset is calibration without absolute normalization | pass | GS6 written |
| global_coupling_parent_derived | corpus derives why kappa_eff cannot be local or MTS-dependent | fail | P0/P1/P3 are not established in the parent corpus |
| all_local_dependencies_forbidden | MTS, species, source, range, radius, time, and frame dependencies are theorem-forbidden | fail | GS2-GS4 remain not_parent_derived |
| Newton_or_local_GR_promoted | constant coupling plus measured-GM plus PPN rows are theorem-zero or empirically scored | fail | this is a parent contract only |

## 9. Theorem Status

| claim | status | evidence |
| --- | --- | --- |
| exact global-coupling parent-action contract written | pass | GS0-GS8 define the required parent identities and fallbacks |
| safe superselection route identified | pass_conditional | P0 is sufficient if explicitly adopted as a global sector premise |
| possible derivation route identified | pass_conditional | P1 topological zero-form/integration-constant route could derive d kappa_eff=0 if built into the parent theory |
| Bianchi route bounded | pass | Bianchi arbitrary-source branch is distinguished from hidden-exchange branch |
| global kappa parent-derived from current MTS corpus | fail | no completed parent superselection or topological derivation exists in cited sources |
| scalar/source residual branch eliminated | fail | if kappa_eff depends on MTS/source/range/frame data, R1/R4/R9/R10/R11 remain active |
| Newton/PPN/local-GR promoted | fail | constant-coupling superselection contract only |

## 10. Gate Results

| gate | status | evidence |
| --- | --- | --- |
| source_paths_exist | pass | all cited source paths exist |
| contract_schema_matches | pass | global coupling superselection contract columns match schema |
| theorem_statement_written | pass | 5 theorem rows |
| parent_options_written | pass | 6 parent options |
| counterexamples_written | pass | 8 counterexamples |
| contract_written | pass | source-intake\mts_residuals\P8_global_coupling_superselection_CONTRACT.csv |
| Bianchi_not_used_as_magic | pass | same-frame arbitrary-source route separated from retained exchange route |
| constant_offset_not_prediction | pass | GS6 calibration policy recorded |
| scalar_branch_retained | pass | P5 and GS7 retain kappa_eff local-dependence fallback |
| global_coupling_parent_derived | fail | no completed parent superselection/topological derivation exists in cited sources |
| MTS_invariant_dependence_forbidden | fail | GS2 remains not_parent_derived |
| species_source_blind_kappa_derived | fail | GS3 remains not_parent_derived |
| range_radial_time_running_zero | fail | GS4 remains not_parent_derived |
| residual_evaluator_mapping_executable | fail | GS8 mapping is contract-only |
| Newtonian_reduction_promoted | fail | global-coupling contract only |
| local_GR_promoted | fail | P8 and PPN rows remain retained |
| claim_ceiling_enforced | pass | global_coupling_superselection_contract_only_no_measured_GM_Newton_PPN_or_local_GR_pass |

## 11. Decision

The exact contract is now clear. MTS can keep a constant universal G_eff in the local branch if kappa_eff is an explicit global/superselection coupling, or if a future parent action derives it as a topological/integration constant with d kappa_eff=0 and no local matter/source/range/frame dependence. The current corpus does not yet derive either route. Therefore the honest status is conditional-superselection-or-closure: adopt kappa_eff as a global sector premise for the local GR branch, or keep scalar/source-normalization residuals active. This checkpoint does not promote measured-GM, Newton, PPN, or local GR.

Practical read: this is not grim, but it is not magic either. The clean boxing-footwork version is to carry `kappa_eff` as a declared global sector label for the local GR branch, while refusing to claim the numerical value of `G`. The more ambitious derivation route is a topological zero-form/integration-constant parent sector. If neither is adopted, then `kappa_eff` is a local scalar/source-normalization residual and the local GR branch does not pass yet.

## 12. Next Queue

| rank | target | why_next |
| --- | --- | --- |
| 1 | 454-PiM-parent-symplectic-projector-algebra-attempt.md | constant coupling can be carried as a clean superselection premise while mass-flux closure still needs actual Pi_M projector algebra |
| 2 | map GS0-GS8 into P8/R9/R10 residual evaluator | failed global-coupling identities should automatically activate Gdot/source/range/local-bound rows |
| 3 | parent topological zero-form kappa route | if we want derivation rather than closure, this is the sharpest future path for d kappa_eff=0 |
