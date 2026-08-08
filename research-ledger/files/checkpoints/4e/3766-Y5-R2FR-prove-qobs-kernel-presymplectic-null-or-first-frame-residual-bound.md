# 3766 - Prove q_obs Kernel Presymplectic Null Or First Frame Residual Bound

## Status

`KERNEL_NULL_THEOREM_DERIVED_CONDITIONALLY_FRAME_RESIDUAL_BOUND_EMITTED_NOT_PARENT_SIGNED`.

3766 derives the exact covariant phase-space condition under which ker(Dq_obs) is presymplectic-null, matter-invisible, boundary-silent, and readout-silent. The current MTS branch does not yet sign the parent action pullback/symplectic/source/boundary clauses, so local GR is not claimed. The fallback is now a concrete delta_frame_source bound in terms of vertical leakage norms.

## Result In Plain Terms

The clean route is now exact: if the parent local action is a pullback through `q_obs` up to a boundary term, and the source/readout sectors also descend through `q_obs`, then every vertical direction in `ker(Dq_obs)` is gauge/null/matter-invisible. That would make the 3764 single-frame/same-source theorem live.

The current corpus does not yet sign the parent action pullback or the symplectic calculation, so this is not a local-GR claim. The fallback is stronger than before: the failure is now bounded by named vertical leakage norms rather than left as an undefined coupling gap.

## Kernel-Null Theorem
- `KNT3766_0_vertical_split` `EXACT_LOCAL_FIBRE_IDENTITY`: Choose a local section sigma of q_obs and vertical coordinates zeta^A so Phi=sigma(Q)+zeta^A E_A with Q=q_obs(Phi). Identity: `Dq_obs[E_A]=0 by construction; E_A span ker(Dq_obs).`
- `KNT3766_1_pullback_action` `EXACT_CONDITIONAL_ACTION_THEOREM`: If L_parent(Phi)=q_obs^* L_red(Q)+dB(Q,zeta) and S_src(Phi,psi,A,theta)=Sbar_src(q_obs(Phi),psi,A,theta), then vertical bulk variations vanish. Identity: `delta_EA L_parent=d(delta_EA B), delta_EA S_src=0.`
- `KNT3766_2_presymplectic_contraction` `EXACT_CONDITIONAL_PRESYMPLECTIC_THEOREM`: For L_parent=q_obs^*L_red+dB, the covariant symplectic current obeys i_EA Omega_parent=0 in the bulk and i_EA Theta_parent=dB_EA up to the same boundary term. Identity: `Theta_parent=q_obs^*Theta_red+delta B, so Omega_parent=q_obs^*Omega_red; contracting with E_A gives zero because Dq_obs[E_A]=0.`
- `KNT3766_3_boundary_silence` `EXACT_CONDITIONAL_BOUNDARY_THEOREM`: For compact local variations or quotient-owned boundary/support data, the surface integral of B_EA vanishes. Identity: `int_boundary B_EA=0 implies no side flux, no boundary owner current, and no radial leakage from the vertical sector.`
- `KNT3766_4_matter_invisibility` `EXACT_CONDITIONAL_SOURCE_THEOREM`: If S_src=Sbar_src(q_obs(Phi),psi,A,theta) and Lie_EA theta=0, then Lie_EA S_src=0 for matter, EM, binding, apparatus, and interaction terms. Identity: `Lie_EA S_src=(delta Sbar/dQ)Dq_obs[E_A]+sum_i(partial Sbar/partial theta_i)Lie_EA theta_i=0.`
- `KNT3766_5_readout_zero` `EXACT_CONDITIONAL_READOUT_THEOREM`: If every sector readout r_s factors as F_s o q_obs, then Lie_EA r_s=0 and Delta q_s=0 for matter, EM, light, clocks, orbital/source, boundary/current, and range sectors. Identity: `Lie_EA r_s=DF_s[Dq_obs[E_A]]=0.`
- `KNT3766_6_kernel_null_result` `EXACT_CONDITIONAL_KERNEL_CERTIFICATE`: Under KNT3766_1 through KNT3766_5, ker(Dq_obs) is presymplectic-null, matter-invisible, boundary-silent, and readout-silent. Identity: `i_EA Omega_parent=0; Lie_EA S_src=0; Lie_EA r_s=0; int_boundary B_EA=0.`

## Proof Attempt Against Current Branch
- `KPA3766_0_candidate_qobs` pass=`True`: q_obs candidate exists. Evidence: 3765 writes q_obs_candidate and Q_obs tuple.
- `KPA3766_1_vertical_split` pass=`True`: local fibre split Phi=sigma(Q)+zeta^A E_A with Dq_obs[E_A]=0. Evidence: can be introduced locally as differential geometry of the candidate map.
- `KPA3766_2_parent_pullback_action` pass=`False`: L_parent=q_obs^*L_red+dB plus no local vertical leakage. Evidence: 3763 action ansatz and 3633 theorem support the target form, but no parent-owned pullback proof is present.
- `KPA3766_3_presymplectic_null` pass=`False`: i_EA Omega_parent=0 and i_EA Theta_parent=dB_EA. Evidence: derived conditionally in KNT3766_2; current corpus still lacks Omega_parent calculation.
- `KPA3766_4_boundary_silence` pass=`False`: int_boundary B_EA=0 for compact local/source support. Evidence: 3756-3758 keep side flux and exchange as live gates.
- `KPA3766_5_source_descent` pass=`False`: S_src=Sbar_src(q_obs,psi,A,theta) and Lie_EA theta=0. Evidence: 3764/3646 provide the theorem but not parent-signed constants/material-marker descent.
- `KPA3766_6_sector_readout_descent` pass=`False`: all r_s=F_s o q_obs. Evidence: 3765 sector residual map exists; factorization is not signed for all sectors.
- `KPA3766_7_kernel_certificate_verdict` pass=`False`: ker(Dq_obs) proof live for MTS local-GR branch. Evidence: requires KPA3766_2 through KPA3766_6.

## Vertical Leakage Norms
- `VLN3766_0_action_leak` `epsilon_L`: sup_A ||delta_EA L_parent - dB_EA||_U / ||L_red||_U Meaning: bulk parent action dependence on vertical variables.
- `VLN3766_1_symplectic_leak` `epsilon_Omega`: sup_A ||i_EA Omega_parent||_U / ||Omega_red||_U Meaning: physical phase-space charge in the q_obs kernel.
- `VLN3766_2_boundary_leak` `epsilon_boundary`: sup_A |int_boundary B_EA| / E_U Meaning: compact-support, side-flux, or boundary-owner visibility.
- `VLN3766_3_source_leak` `epsilon_src`: sup_A |Lie_EA S_src| / |S_src| Meaning: matter, EM, binding, apparatus, or interaction dependence on vertical variables.
- `VLN3766_4_constant_marker_leak` `epsilon_theta`: sup_A,i |Lie_EA theta_i| / |theta_i| Meaning: mass, charge, clock-ratio, material-marker, or calibration dependence outside q_obs.
- `VLN3766_5_readout_leak` `epsilon_readout_s`: sup_A ||Lie_EA r_s|| / ||r_s|| for each sector s Meaning: sector readout mismatch Delta q_s.
- `VLN3766_6_range_hair_leak` `epsilon_range`: sup_A (|alpha_A(lambda)| + |hair_A(r)|) Meaning: finite-range or exterior radial hair carried by vertical variables.

## First Frame Residual Bound
- `FRB3766_0_sector_path_bound` `Delta q_s`: |Delta q_s| <= integral_0^1 ||D r_s[E_A]|| |d zeta^A/dlambda| dlambda Inputs: requires sector sensitivity ||D r_s[E_A]|| and vertical amplitude |zeta^A|.
- `FRB3766_1_lipschitz_bound` `Delta q_s`: |Delta q_s| <= sum_A L_{sA} |zeta^A| Inputs: requires L_{sA} from parent readout map or empirical residual model.
- `FRB3766_2_frame_summary_bound` `delta_frame_source`: delta_frame_source <= w_m|Delta q_matter|+w_EM|Delta q_EM|+w_l|Delta q_light|+w_c|Delta q_clock|+w_o|Delta q_orbit_source| Inputs: requires sector weights from target observable or conservative w_s=1 discipline.
- `FRB3766_3_kernel_leak_bound` `delta_frame_source`: delta_frame_source <= C_Omega epsilon_Omega + C_src epsilon_src + C_theta epsilon_theta + C_boundary epsilon_boundary + C_readout max_s epsilon_readout_s Inputs: requires constants C_i from parent linearization or empirical calibration.
- `FRB3766_4_ppn_gamma_bound` `abs(gamma-1)_frame`: abs(gamma-1)_frame <= C_gamma_frame delta_frame_source + C_gamma_range epsilon_range + C_gamma_EH delta_EH Inputs: requires C_gamma coefficients and PPN observable mapping.
- `FRB3766_5_wep_bound` `eta_source_AB`: eta_source_AB <= C_AB^m |Delta q_matter| + C_AB^theta epsilon_theta + C_AB^EM |Delta q_EM| + C_AB^boundary epsilon_boundary Inputs: requires composition sensitivities and material constants.
- `FRB3766_6_newton_gm_bound` `delta_mu_obs`: |delta mu_obs| <= |Delta q_orbit_source| + epsilon_boundary + epsilon_src Inputs: requires source monopole map and boundary/current denominator coefficients.

## Claim Gates
- `CG3766_0_sources` pass=`True`: all 3766 source paths exist - path hygiene
- `CG3766_1_kernel_theorem_emitted` pass=`True`: kernel-null theorem emitted - exact conditional proof exists
- `CG3766_2_proof_live_for_MTS` pass=`False`: kernel-null proof live for current MTS parent branch - blocked by unsigned parent action/symplectic/source/boundary clauses
- `CG3766_3_leakage_norms_emitted` pass=`True`: vertical leakage norms emitted - first measurable/boundable residual interface exists
- `CG3766_4_frame_bound_emitted` pass=`True`: first frame residual bound emitted - failure branch is now a bound formula rather than a vague gap
- `CG3766_5_single_frame_claim` pass=`False`: single observed frame claim allowed - blocked until CG3766_2 passes or residual bounds are filled below tests
- `CG3766_6_local_gr_claim` pass=`False`: local GR/Newton/PPN claim allowed - blocked until kernel proof plus local EH/no-range/global-kappa gates close

## Decisions
- `DEC3766_0`: The exact mathematical route to a live q_obs kernel proof is now written as a covariant phase-space theorem. Action: do not relitigate the target; attack the missing parent action pullback and Omega_parent calculation.
- `DEC3766_1`: The current MTS corpus still does not sign the proof because the parent action/symplectic/source/boundary clauses are not explicit enough. Action: keep local GR unclaimed.
- `DEC3766_2`: If the proof remains unsigned, the first fallback is no longer a vague closure label: delta_frame_source has a bound in terms of vertical leakage norms. Action: next fill or derive epsilon_L, epsilon_Omega, epsilon_src, epsilon_theta, epsilon_boundary, and epsilon_readout_s.
- `DEC3766_3`: The highest-value next derivation is the parent action pullback decomposition L_parent=q_obs^*L_red+dB+L_leak. Action: try to force all non-q_obs terms into L_leak and either prove L_leak=0 or make it the first numeric residual object.

## Next Target
- `3767-Y5-R2FR-parent-action-pullback-decomposition-or-Lleak-first-bound.md`: decompose the local parent action as L_parent=q_obs^*L_red+dB+L_leak, then either prove L_leak=0 for the q_obs kernel or promote L_leak into the first source-ready residual coefficient set

## Validation
- `sources_exist` `PASS`: all 3766 source paths exist
- `generated_csvs_parse` `PASS`: all generated 3766 csvs parse
- `kernel_result` `PASS`: kernel-null result theorem emitted
- `proof_attempt_closed` `PASS`: live MTS proof remains blocked rather than claimed
- `leakage_norms` `PASS`: at least seven vertical leakage norms emitted
- `frame_bound` `PASS`: first frame residual bound emitted
- `numeric_status_nonclaim` `PASS`: frame-bound rows remain nonclaim without coefficients
- `claim_gates_closed` `PASS`: single-frame/local-GR claims remain closed
- `next_target` `PASS`: 3767 parent action pullback target emitted
- `no_formalization_leak` `PASS`: no 3766 files written to formalization-workbench
