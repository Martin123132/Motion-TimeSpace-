# 3591 - Source coupling GM calibration or residual contract

## Verdict
3591 writes the exact bridge MTS needs before it can say it has Newtonian mechanics rather than an EH-looking equation plus fitted `GM`.

If the transfer contract closes, `mu_obs=G_ref M_H`, `epsilon_mu=0`, and `a_r=-G_ref M_H/r^2`.  In the current corpus the contract is not parent-signed, so `epsilon_mu` must be propagated into Newton, PPN, R10, and local-GR tests.

## GM Transfer Contract
- `GMT3591_0_same_observed_frame` `same observed frame`: CONDITIONAL_NOT_PARENT_DERIVED - e_obs=e_matter=e_source=e_orbit and g_00=-1+2Phi/c^2 in that frame
- `GMT3591_1_EH_or_bounded_operator` `weak-field operator`: CONDITIONAL_EH_ONLY_NOT_PARENT_DERIVED - E_munu=G_munu+Lambda g_munu+R11_residual and nabla^2 Phi=(kappa_eff c^4/2)rho_H + R_operator
- `GMT3591_2_parent_Hilbert_source` `Hilbert source current`: NOT_PARENT_DERIVED - J_H and T_H are varied from the parent matter action before material labels/readout
- `GMT3591_3_Hamiltonian_equals_Hilbert_mass` `charge-current equality`: NOT_PARENT_DERIVED - B_xi/G_ref = M_H[Pi_M J_H] and delta B_xi = delta integral_S Pi_M J_H
- `GMT3591_4_closed_flux` `closed projected mass flux`: NOT_DERIVED_PROJECTOR_COMMUTATOR_OPEN - d(Pi_M J_H)=0, so M_H(S2)-M_H(S1)=0 in compact source-free exterior annuli
- `GMT3591_5_Gauss_orbital_calibration` `Gauss-to-orbit readout`: DOWNSTREAM_GATE_OPEN - nabla^2 Phi=4piG_ref rho_H and a_r=-G_ref M_H/r^2, so v^2 r=G_ref M_H
- `GMT3591_6_zero_extra_monopole` `extra source monopole silence`: RETAINED_RESIDUAL_REQUIRED - mu_extra=Delta_nonEH+Delta_symp+Delta_PiM+Delta_extra+Delta_frame+Delta_cal+Delta_PPN+Delta_GK=0 or bounded
- `GMT3591_7_constant_universal_Gref` `universal coupling`: NOT_PARENT_DERIVED - partial_t,r,A,lambda,frame G_ref=0 and G_ref=kappa_eff c^4/(8pi)
- `GMT3591_8_theorem_result_if_all_close` `Newton transfer theorem`: THEOREM_ROUTE_EXACT_BUT_NOT_ACTIVATED - all preceding rows close => mu_obs=G_ref M_H, epsilon_mu=0, a_r=-G_ref M_H/r^2, and no fitted-GM hiding

## Source Charge Audit
- `SCA3591_0_no_fitted_source_mask` `Pi_M owner`: MISSING_PARENT_PROJECTOR_ORIGIN - Pi_M must be parent-owned before readout; no post-fit GM mask or galaxy/source convention may define it
- `SCA3591_1_same_frame_worldtube` `worldtube source measure`: MISSING_SAME_FRAME_TAU_EOBS_LOCK - W_source and J_H must be computed from the same observed coframe/time generator used by orbit readout
- `SCA3591_2_action_measure_current_owner` `action/current owner`: LOCK_NOT_PROVED_CURRENT_CORPUS - ordinary matter weights, action measure, hbar, and source currents must descend from one parent owner
- `SCA3591_3_charge_current_equality` `Hamiltonian-Hilbert equality`: NOT_PARENT_DERIVED - B_xi/G_ref must equal M_H[Pi_M J_H] with projector variation accounted for
- `SCA3591_4_flux_closure` `closed exterior source flux`: NOT_DERIVED_PROJECTOR_COMMUTATOR_OPEN - d(Pi_M J_H)=0 or explicit residual d(Pi_M J_H) must be carried into radial/Gdot/source tests
- `SCA3591_5_no_extra_mass_projection` `extra monopole channels`: NOT_DERIVED_EXTRA_MASS_CHANNELS_ACTIVE - non-EH, GK, boundary, projector, domain, memory, range, frame, species and calibration monopoles must be zero or residual rows
- `SCA3591_6_second_order_stability` `PPN source stability`: NOT_DERIVED - same source charge must survive beta/gamma/preferred-frame order; Poisson-only success is insufficient for local GR
- `SCA3591_7_current_verdict` `GM source theorem`: RESIDUAL_CONTRACT_REQUIRED - GM transfer theorem is exact as a contract but not activated; residual propagation is mandatory

## Epsilon Mu Contract
- `EMU3591_0_epsilon_frame` `epsilon_frame`: MISSING_NUMERIC_OR_DERIVED_ZERO_FRAME_SPLIT - delta_frame_source
- `EMU3591_1_epsilon_current` `epsilon_current`: MISSING_CURRENT_OWNER_OR_NUMERIC_RESIDUAL - current_rescaling + qbar_source_weight
- `EMU3591_2_epsilon_flux` `epsilon_flux`: MISSING_FLUX_CLOSURE_OR_NUMERIC_RESIDUAL - dln_Meff_dt + partial_r_ln_mu_obs
- `EMU3591_3_epsilon_extra` `epsilon_extra`: MISSING_EXTRA_MONOPOLE_ZERO_OR_VECTOR - mu_extra_boundary_bulk_domain/(G_ref M_H)
- `EMU3591_4_epsilon_GK` `epsilon_GK_source`: MISSING_K_GK_MU_MAP_OR_ETA_CLOSURE - K_GK_mu * X_GK_residual
- `EMU3591_5_epsilon_operator` `epsilon_operator`: MISSING_EH_ONLY_OR_R11_VECTOR - R11/nonEH operator coefficient contribution to Poisson source coefficient
- `EMU3591_6_epsilon_calibration` `epsilon_calibration`: MISSING_CONSTANT_UNIVERSAL_GREF - delta_G_ref + absolute calibration offset
- `EMU3591_7_epsilon_PPN_source` `epsilon_PPN_source`: MISSING_SECOND_ORDER_SOURCE_VECTOR - delta_beta_source + preferred-frame/source PPN residuals
- `EMU3591_8_epsilon_mu_total` `epsilon_mu`: RESIDUAL_CONTRACT_READY_VALUES_MISSING - epsilon_frame + epsilon_current + epsilon_flux + epsilon_extra + epsilon_GK_source + epsilon_operator + epsilon_calibration + epsilon_PPN_source

## Newton And PPN Propagation
- `NPP3591_0_measured_mu` `mu_obs`: RESIDUAL_PROPAGATION_RULE - mu_obs := G_ref M_H * (1 + epsilon_mu)
- `NPP3591_1_Newton_acceleration` `a_r`: NONCLAIM_TESTABLE_FORM - a_r = -G_ref M_H/r^2 * (1 + epsilon_mu + epsilon_radial_profile + epsilon_operator_force)
- `NPP3591_2_Poisson_source` `Poisson residual`: NONCLAIM_TESTABLE_FORM - nabla^2 Phi = 4piG_ref rho_H + R_operator + R_source + R_boundary
- `NPP3591_3_PPN_vector` `PPN_source_vector`: RESIDUAL_VECTOR_REQUIRED - {gamma-1,beta-1,alpha_i,xi,zeta_i}_source receive explicit epsilon_mu/epsilon_GK/source residual contributions
- `NPP3591_4_R10_range` `alpha(lambda)`: R10_REMAINS_SEPARATE_SCORE_BRANCH - range-dependent source or GK/local hair must enter alpha(lambda), not a constant GM calibration
- `NPP3591_5_no_absorption_cheat` `GM calibration policy`: PASS_GUARD - constant universal calibration may set one overall G_ref only; derivatives/composition/range/profile residuals remain live

## Gates
- `GATE3591_0_sources`: PASS (all source paths and selected anchors exist)
- `GATE3591_1_transfer_contract`: PASS_CONTRACT_EXACT (GM/Newton transfer theorem requirements are explicitly enumerated)
- `GATE3591_2_parent_source_charge`: FAIL_CURRENT_CLAIM (parent Hilbert/Noether/Hamiltonian source charge is not derived)
- `GATE3591_3_GM_not_hidden`: PASS_GUARD (unclosed source coupling is propagated as epsilon_mu, not fitted GM)
- `GATE3591_4_Newton_claim`: FAIL_CURRENT_CLAIM (Newtonian mechanics is not claimed until epsilon_mu and operator residuals close)
- `GATE3591_5_PPN_claim`: FAIL_CURRENT_CLAIM (Poisson-only bridge cannot promote local GR without PPN/source stability)
- `GATE3591_6_next_pivot`: PASS (next target should attack the largest epsilon_mu component rather than re-loop GK)

## Status
- `GM_TRANSFER_CONTRACT_DERIVED_RESIDUAL_PROPAGATION_ACTIVE`: 3591 derives the exact source-coupling contract needed to turn an EH/weak-field branch into Newtonian measured GM: same frame, EH/Poisson operator, parent Hilbert source, Hamiltonian-Hilbert equality, closed flux, Gauss/orbital readout, zero extra monopole, and constant universal G_ref. The current corpus does not close those clauses, so epsilon_mu is introduced as the explicit measured-GM residual vector.
- Decision: do not claim Newton/local-GR from fitted GM; propagate epsilon_mu into Newton, PPN, R10, and source-normalization tests until the source charge theorem closes
- Still missing: parent matter/current owner, Pi_M origin, Hamiltonian-Hilbert equality, flux closure, worldtube/source measure glue, zero extra monopole, constant universal G_ref, second-order PPN source stability, numeric/source-backed epsilon_mu components

## Validation
- `VAL3591_0_sources_exist`: PASS (all required 3591 source paths exist)
- `VAL3591_1_required_needles_found`: PASS (all selected 3591 anchors found)
- `VAL3591_2_outputs_exist`: PASS (all pre-validation 3591 output files written)
- `VAL3591_3_csv_parse`: PASS (source_register:23; gm_transfer_contract:9; source_charge_audit:8; epsilon_mu_contract:9; newton_ppn_propagation:6; activation_gates:7; status:1; next_target:1; canonical_status:1)
- `VAL3591_4_GM_contract_complete`: PASS (all GM transfer contract rungs are present)
- `VAL3591_5_epsilon_mu_complete`: PASS (epsilon_mu residual vector is complete)
- `VAL3591_6_no_fitted_GM_guard`: PASS (unclosed source coupling is not hidden in fitted GM)
- `VAL3591_7_Newton_claim_blocked`: PASS (Newton claim remains blocked)
- `VAL3591_8_PPN_propagation_present`: PASS (PPN/source residual propagation row is present)
- `VAL3591_9_source_audit_blocks_GM`: PASS (source audit rows block GM claim until closed)
- `VAL3591_10_no_claim_flags`: PASS (all generated physics rows remain nonclaim)
- `VAL3591_11_next_target_selected`: PASS (3592 PiM-Hilbert target selected)
- `VAL3591_12_generated_source_paths_exist`: PASS (every generated row source_path exists)
- `VAL3591_13_formalization_workbench_untouched`: PASS (no 3591 checkpoint output appears in formalization-workbench)

## Next target
- `NEXT3591_0` -> `3592-Y5-R2FR-PiM-Hilbert-charge-equality-or-epsilon-mu-input-pack.md`
- Objective: attack the central source-coupling clause: derive Pi_M J_H equals the Hamiltonian/Hilbert mass charge, or build the first source-ready epsilon_mu input pack for measured-GM residuals
