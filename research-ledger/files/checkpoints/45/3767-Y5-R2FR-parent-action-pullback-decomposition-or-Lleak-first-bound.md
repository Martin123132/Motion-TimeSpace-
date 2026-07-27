# 3767 - Parent Action Pullback Decomposition Or L_leak First Bound

## Status

`PARENT_ACTION_PULLBACK_DECOMPOSITION_DERIVED_LLEAK_BASIS_AND_BOUND_EMITTED_NOT_ZERO`.

3767 derives the exact fibre-homotopy decomposition L_parent=q_obs^*L_red+dB+L_leak. It does not prove L_leak=0 for the current MTS branch; instead it names the live leak operators and gives an epsilon_L bound that propagates into delta_frame_source and local-GR residuals.

## Result In Plain Terms

This checkpoint turns the parent-action gap into an exact decomposition. Along the vertical fibre of `q_obs`, the difference between the real parent action and the reduced observed action is split into a boundary term plus `L_leak`. If `L_leak=0` and the boundary is silent, 3766 gives the kernel-null certificate. If not, `L_leak` is the residual object to bound.

## Pullback Decomposition
- `PAD3767_0_fibre_path` `EXACT_LOCAL_FIBRE_SETUP`: Let Q=q_obs(Phi), choose a local section sigma(Q), and write a vertical path Phi_lambda=sigma(Q)+lambda zeta^A E_A with E_A in ker(Dq_obs). Identity: `Dq_obs[d Phi_lambda/dlambda]=0 along the path.`
- `PAD3767_1_homotopy_identity` `EXACT_ACTION_IDENTITY`: L_parent(Phi)-L_parent(sigma(Q)) = integral_0^1 zeta^A partial_A L_parent(Phi_lambda) dlambda. Identity: `This is the fundamental theorem of calculus on the vertical fibre.`
- `PAD3767_2_total_derivative_split` `DEFINITION_WITH_UNIQUE_RESIDUAL_AFTER_BOUNDARY_CHOICE`: Split partial_A L_parent(Phi_lambda)=d b_A(Phi_lambda)+r_A(Phi_lambda). Identity: `b_A is the boundary/improvement part; r_A is the non-exact bulk vertical residue.`
- `PAD3767_3_pullback_decomposition` `EXACT_DECOMPOSITION`: Define L_red(Q):=L_parent(sigma(Q)), B:=integral_0^1 zeta^A b_A(Phi_lambda)dlambda, and L_leak:=integral_0^1 zeta^A r_A(Phi_lambda)dlambda. Identity: `Then L_parent=q_obs^*L_red+dB+L_leak.`
- `PAD3767_4_zero_condition` `EXACT_ZERO_CONDITION`: L_leak=0 iff every vertical derivative of L_parent is a total derivative with silent local boundary/support. Identity: `r_A=0 and int_boundary B=0 for all E_A in ker(Dq_obs).`
- `PAD3767_5_kernel_consequence` `EXACT_CONDITIONAL_CONSEQUENCE`: If L_leak=0, source/readout descent holds, and the boundary is silent, 3766 gives i_EA Omega_parent=0, Lie_EA S_src=0, and Lie_EA r_s=0. Identity: `L_parent=q_obs^*L_red+dB is the missing premise of KNT3766_2.`
- `PAD3767_6_failure_bound` `RESIDUAL_BOUND_INTERFACE`: If L_leak != 0, define epsilon_L:=||L_leak||_U/||L_red||_U and propagate it into epsilon_Omega, epsilon_src, and delta_frame_source bounds. Identity: `delta_frame_source <= C_L epsilon_L + C_boundary epsilon_boundary + C_readout max_s epsilon_readout_s.`

## L_leak Operator Basis
- `LOB3767_0_topological_bulk` `L_leak_top`: integral_0^1 zeta^A r_A^top(Phi_lambda) dlambda Feeds: `Gdot, radial hair, PPN beta, source conservation`.
- `LOB3767_1_kappa_EH_coefficient` `L_leak_kappa`: -(partial_A ln kappa_*) zeta^A L_EH plus higher vertical orders Feeds: `Gdot, Newtonian GM calibration, PPN gamma/beta`.
- `LOB3767_2_shadow_metric_frame` `L_leak_shadow_g`: (delta L_EH/dg_eff_ab) Delta g_shadow_ab + source-frame analogues Feeds: `single observed frame, light bending, clocks, WEP`.
- `LOB3767_3_source_action` `L_leak_src`: zeta^A J_A^src with J_A^src:=delta S_src/dzeta^A Feeds: `WEP, EM stress, source universality, PPN source projection`.
- `LOB3767_4_constants_markers` `L_leak_theta`: zeta^A sum_i (partial L_src/partial theta_i) partial_A theta_i Feeds: `WEP, clocks, alpha_fs drift, calibrated source coupling`.
- `LOB3767_5_auxiliary_range` `L_leak_aux`: kinetic/mass/source terms for chi that are not algebraically eliminated, heavy/decoupled, or quotient-silent Feeds: `R10 fifth-force, radial hair, PPN, orbital systems`.
- `LOB3767_6_boundary_support` `L_leak_boundary`: dB with int_boundary B != 0 or source-support variation not quotient-owned Feeds: `Gdot, radial hair, source conservation, H_tau/H_ref`.
- `LOB3767_7_readout_postprocessing` `L_leak_readout`: post-action readout weights W_s(Phi) not expressible as F_s(q_obs) Feeds: `Delta q_s vector, preferred frame, local calibration`.

## Vertical Variation Audit
- `VAA3767_0_EH_pullback` pass=`False`: Einstein-Hilbert local operator from 3763 ansatz. Residual: `L_leak_kappa and L_leak_shadow_g remain live`.
- `VAA3767_1_source_action` pass=`False`: same-source action term from 3763/3764. Residual: `L_leak_src and L_leak_theta remain live`.
- `VAA3767_2_auxiliary_silence` pass=`False`: S_aux[chi;g_eff] branch. Residual: `L_leak_aux remains live`.
- `VAA3767_3_topological_sector` pass=`False`: S_top[MTS]. Residual: `L_leak_top remains live`.
- `VAA3767_4_boundary_support` pass=`False`: source support and boundary class. Residual: `L_leak_boundary remains live`.
- `VAA3767_5_readout_layer` pass=`False`: sector readouts after variation. Residual: `L_leak_readout and Delta q_s remain live`.

## Bound Interface
- `LBI3767_0_total_action_leak` `epsilon_L`: epsilon_L <= epsilon_top + epsilon_kappa + epsilon_shadow_g + epsilon_src + epsilon_theta + epsilon_aux + epsilon_boundary + epsilon_readout Inputs: requires each operator coefficient or proof of zero.
- `LBI3767_1_kappa_EH_leak` `epsilon_kappa`: contributes |delta G/G|, Newtonian source calibration drift, and EH coefficient variation Inputs: prove kappa_* q_obs-owned or bound from Gdot/PPN/orbital rows.
- `LBI3767_2_shadow_frame_leak` `epsilon_shadow_g`: contributes frame split, gamma, clocks, and light/matter mismatch Inputs: prove single frame descent or bound from PPN/clock/preferred-frame tests.
- `LBI3767_3_source_leak` `epsilon_src`: contributes WEP/source universality and EM stress split Inputs: prove source action descent or bound with composition/EM/apparatus sensitivities.
- `LBI3767_4_constants_markers` `epsilon_theta`: contributes mass, charge, clock, alpha, and material dependence Inputs: prove theta superselection or create coefficient rows b_mass,b_alpha,b_clock,b_material.
- `LBI3767_5_aux_range` `epsilon_aux`: contributes R10 alpha(lambda), radial hair, and PPN extra-channel terms Inputs: prove chi heavy/algebraic/gauge or use R10/PPN/radial bounds.
- `LBI3767_6_boundary_support` `epsilon_boundary`: contributes side flux, source conservation, radial hair, H_tau/H_ref Inputs: prove compact boundary silence or bound flux/current terms.
- `LBI3767_7_frame_propagation` `delta_frame_source`: delta_frame_source <= C_L epsilon_L + C_readout max_s epsilon_readout_s + C_boundary epsilon_boundary Inputs: requires C_L,C_readout,C_boundary or conservative normalized unit coefficients for smoke tests.

## Claim Gates
- `CG3767_0_sources` pass=`True`: all 3767 source paths exist - path hygiene
- `CG3767_1_decomposition_identity` pass=`True`: L_parent=q_obs^*L_red+dB+L_leak identity emitted - fibre homotopy decomposition exists
- `CG3767_2_operator_basis` pass=`True`: L_leak operator basis emitted - leak channels are named
- `CG3767_3_bound_interface` pass=`True`: epsilon_L and delta_frame_source bound emitted - failure is boundable
- `CG3767_4_pullback_signed` pass=`False`: current MTS parent action signs L_leak=0 - blocked by live kappa/source/topological/aux/boundary/readout residuals
- `CG3767_5_kernel_claim` pass=`False`: q_obs kernel-null claim allowed - blocked until CG3767_4 plus source/readout descent pass
- `CG3767_6_local_gr_claim` pass=`False`: local GR/Newton branch claim allowed - blocked until L_leak coefficients vanish or are below all local bounds

## Decisions
- `DEC3767_0`: The parent-action problem is now reduced to an exact identity plus named leak operators. Action: stop treating the coupling gap as a single mystery; attack the L_leak coefficients one by one.
- `DEC3767_1`: The easiest first zero target is the EH coefficient: if kappa_* is q_obs-owned, the EH coefficient does not leak along ker(Dq_obs). Action: make kappa/EH coefficient the next derivation target.
- `DEC3767_2`: The most dangerous non-geometric leak remains source constants and material markers. Action: keep L_leak_theta and L_leak_src live until superselection or coefficient bounds are written.
- `DEC3767_3`: If no coefficient can be proved zero, the project still has a disciplined empirical route. Action: fill epsilon_i coefficients and compare against Gdot, WEP, PPN, R10, clock, and orbital constraints.

## Next Target
- `3768-Y5-R2FR-kappa-EH-coefficient-quotient-zero-or-Gdot-PPN-bound.md`: prove the EH coupling coefficient kappa_* is q_obs-owned/superselected so L_leak_kappa=0, or turn Lie_EA ln kappa_* into the first numeric residual coefficient bounded by Gdot, Newtonian calibration, and PPN constraints

## Validation
- `sources_exist` `PASS`: all 3767 source paths exist
- `generated_csvs_parse` `PASS`: all generated 3767 csvs parse
- `decomposition_identity` `PASS`: pullback decomposition identity emitted
- `zero_condition` `PASS`: L_leak zero condition emitted
- `operator_basis` `PASS`: at least eight L_leak operators emitted
- `vertical_audit_nonclaim` `PASS`: current branch audit leaves residuals live
- `bound_interface` `PASS`: epsilon_L to delta_frame_source bound emitted
- `coefficients_missing` `PASS`: bound rows remain nonclaim without coefficients
- `claim_gates_closed` `PASS`: kernel/local-GR claims remain closed
- `next_target` `PASS`: 3768 kappa/EH coefficient target emitted
- `no_formalization_leak` `PASS`: no 3767 files written to formalization-workbench
