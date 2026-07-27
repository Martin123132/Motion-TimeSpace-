# 3771 - Constants/Material Marker Leak Zero Or Clock/WEP/Alpha Bound

## Status

`CONSTANT_MARKER_ZERO_THEOREM_DERIVED_UNIT_CHEAT_REJECTED_BOUNDS_WIRED_NOT_PARENT_SIGNED`.

3771 derives the exact constants/material-marker leak operator and its conditional zero theorem. It separates harmless unit/common-scale gauge from physical dimensionless constant and material-label leakage, wires WEP/clock/R10/PPN/Gdot/Newton bound interfaces, and keeps all claims closed because parent superselection, material-marker descent, clock projection, R10 material charges, and Newton active/passive source normalization are not signed.

## Result In Plain Terms

This checkpoint attacks the coupling obstruction directly. If physical constants, masses, charges, clock markers, and material labels are fixed labels of the `q_obs` branch, then the hidden fibre cannot change them and `L_leak_theta=0`. If they can wiggle, the wiggle is no longer vague: it is a named vector of `b_alpha`, `b_mu`, material, binding, clock, and source-normalization coefficients that feeds WEP, clocks, R10, PPN, Gdot, and Newtonian GM.

## Constants/Marker Theorem
- `CMT3771_0_theta_split` `EXACT_SPLIT`: Split theta into dimensionless physical constants c_I, material or representation labels m_A, binding/response coefficients b_A, and pure unit/common-scale conventions u. Derivation: Only dimensionless readouts and source-normalized combinations can be physical; a unit convention alone cannot create or remove an observable force.
- `CMT3771_1_theta_leak_operator` `EXACT_OPERATOR`: For E_A in ker(Dq_obs), define theta_{I,A}:=Lie_EA theta_I and L_leak_theta=zeta^A sum_I (partial L_src/partial theta_I) theta_{I,A}+O(zeta^2). Derivation: This is the constants/material-marker component of the 3767 action-leak basis.
- `CMT3771_2_conditional_zero` `EXACT_CONDITIONAL_ZERO_THEOREM`: If every physical theta_I is q_obs-owned or superselected, Lie_EA theta_I=0 for all E_A in ker(Dq_obs), hence L_leak_theta=0. Derivation: Substitute theta_{I,A}=0 into the operator definition.
- `CMT3771_3_common_unit_mode` `UNIT_GAUGE_CONDITION`: A common unit rescaling is quotient-gauge only when all rods, clocks, source normalization, and kappa calibration descend through the same q_obs class. Derivation: Dimensionless ratios cancel the common mode; Newtonian GM and absolute G do not cancel unless source calibration is also signed.
- `CMT3771_4_clock_projection` `CLOCK_BOUND_INTERFACE`: Clock ratios see only sensitivity-weighted dimensionless constant leakage: delta ln(nu_a/nu_b)=sum_I Delta K_I^{ab} delta ln theta_I plus readout-frame terms. Derivation: Frequency units cancel; sensitivity differences survive.
- `CMT3771_5_WEP_projection` `WEP_BOUND_INTERFACE`: Composition tests see differential material response: eta_AB <= sum_I |Delta Q_I^{AB}| |b_I| tau_WEP plus EM/binding/source-current residuals. Derivation: Universal common coupling cancels in eta_AB; composition-dependent constants and binding fractions do not.
- `CMT3771_6_alpha_R10_projection` `R10_ALPHA_BOUND_INTERFACE`: Short-range rows see alpha_X(lambda_X) from material charges Qbar_source/test built from alpha, mass, nuclear, and clock-marker coefficients. Derivation: A finite range mediator with nonzero material charge must be compared to alpha_bound(lambda).
- `CMT3771_7_Newton_source_projection` `NEWTON_SOURCE_INTERFACE`: Newtonian mechanics requires the same source mass/charge normalization in inertial, passive, and active roles; theta common modes are safe only after this equality is signed. Derivation: Otherwise delta ln mu_obs receives source-normalization and binding-marker leakage.

## Zero Proof Attempt
- `CZA3771_0_operator_identified` pass=`True`: L_leak_theta is present in the 3767 leak basis. Evidence: P8_Y5_R2FR_3767_LLEAK_OPERATOR_BASIS.csv:LOB3767_4_constants_markers.
- `CZA3771_1_source_gate_requires_theta_silence` pass=`True`: 3770 source descent requires constants/material markers silent. Evidence: P8_Y5_R2FR_3770_SOURCE_ACTION_ZERO_ATTEMPT.csv:SZA3770_4_constants_markers_silent.
- `CZA3771_2_unit_cheat_removed` pass=`True`: dimensionful unit rescaling is not counted as physical proof. Evidence: 3771 unit-gauge audit splits common unit mode from dimensionless constants.
- `CZA3771_3_dimensionless_constants_superselected` pass=`False`: alpha_EM, mass ratios, charge ratios, and nuclear response coefficients are q_obs-owned or superselected. Evidence: current corpus has schemas and gates, but no parent superselection derivation.
- `CZA3771_4_material_labels_superselected` pass=`False`: material/species labels and binding fractions are fixed representation or boundary labels invisible to ker(Dq_obs). Evidence: current corpus has WEP/EM source budgets, but no parent material-label descent proof.
- `CZA3771_5_clock_markers_superselected` pass=`False`: clock transition response coefficients are q_obs-owned or source-backed constants. Evidence: clock product/source rows remain nonclaim or missing projection inputs.
- `CZA3771_6_newton_source_common_mode_closed` pass=`False`: common mass/source normalization is harmless for Newtonian GM. Evidence: 3770 still marks Newton active/passive source projection missing.
- `CZA3771_7_verdict` pass=`False`: L_leak_theta=0 for current MTS local branch. Evidence: conditional theorem exists, but parent superselection/material-marker/source-normalization proofs are unsigned.

## Unit Gauge Audit
- `UGA3771_0_dimensionful_mass_scale` `unit_gauge_candidate`: common dimensionful mass/energy scale. Rule: cancels in dimensionless clock and WEP ratios only if all rods/clocks/source normalization co-descend. Requirement: Newton GM and absolute G calibration still need a source-normalization owner.
- `UGA3771_1_alpha_EM` `physical_dimensionless_constant`: fine-structure constant alpha_EM. Rule: cannot be removed by units; clocks, spectra, WEP binding, and R10 material charges can see it. Requirement: requires b_alpha=0 theorem or sourced b_alpha bound.
- `UGA3771_2_mass_ratios` `physical_dimensionless_constant`: dimensionless mass ratios such as m_e/m_p. Rule: cannot be removed by units; clock and matter responses can see it. Requirement: requires b_mu=0 theorem or sourced b_mu bound.
- `UGA3771_3_charge_quantization` `superselection_candidate`: charge ratios and gauge representation labels. Rule: safe only if gauge representation labels are fixed across q_obs fibres. Requirement: requires parent gauge/representation descent proof.
- `UGA3771_4_material_identity` `boundary_or_representation_candidate`: material species labels and binding fractions. Rule: safe only if material labels are not dynamical vertical fields. Requirement: requires material worldtube/source action descent proof.
- `UGA3771_5_clock_transition_markers` `readout_marker_candidate`: clock transition sensitivities and apparatus markers. Rule: safe only if apparatus/readout model descends through q_obs. Requirement: requires clock readout kernel and sensitivity source closure.

## Residual Coefficients
- `CMC3771_0_total_theta` `epsilon_theta`: sup_A,I |zeta^A Lie_EA theta_I| after unit-gauge quotient Value: `MISSING_PARENT_THETA_SUPERSELECTION`.
- `CMC3771_1_b_alpha` `b_alpha`: E_A ln alpha_EM times zeta^A or local driver amplitude Value: `MISSING_B_ALPHA_OR_PARENT_ZERO_THEOREM`.
- `CMC3771_2_b_mu` `b_mu`: E_A ln(m_e/m_p) times zeta^A or local driver amplitude Value: `MISSING_B_MU_OR_PARENT_ZERO_THEOREM`.
- `CMC3771_3_b_mA` `b_mA`: species/material mass response after removing pure common unit mode Value: `MISSING_MATERIAL_MASS_MARKER_DESCENT`.
- `CMC3771_4_b_nuc` `b_nuc`: nuclear/binding response not captured by alpha or simple mass ratios Value: `MISSING_NUCLEAR_BINDING_RESPONSE`.
- `CMC3771_5_b_charge` `b_charge`: vertical derivative of charge/gauge representation labels or charge ratios Value: `MISSING_GAUGE_REPRESENTATION_DESCENT`.
- `CMC3771_6_b_clock` `b_clock_i`: vertical derivative of clock transition/readout marker after alpha/mass/nuclear projection Value: `MISSING_CLOCK_MARKER_DESCENT`.
- `CMC3771_7_b_material_label` `b_material_label`: vertical derivative of material labels, composition fractions, or test-body identity markers Value: `MISSING_MATERIAL_LABEL_SUPERSELECTION`.
- `CMC3771_8_b_source_norm` `b_source_norm`: vertical derivative of source normalization common mode after observable calibration Value: `MISSING_NEWTON_SOURCE_NORMALIZATION_OWNER`.

## Bound Budget
- `CBB3771_0_WEP_theta` `eta_theta_AB`: eta_theta_AB <= sum_I |DeltaQ_I^AB| |b_I| tau_WEP + source/EM residuals <= `2.8e-15` `dimensionless`. Source: P8_Y5_R2FR_3759_WEP_BOUND_EVALUATION.csv:WB3759_2_max_allowed_residual.
- `CBB3771_1_EM_binding_WEP` `eta_EM_theta_AB`: eta_EM_theta_AB <= |Delta_AB f_EM||b_alpha| + |Delta_AB b_bind| + EM source residuals <= `2.8e-15` `dimensionless`. Source: P8_Y5_R2FR_3760_EM_SOURCE_RESIDUAL_BUDGET.csv:EMR3760_0_WEP_EM_binding.
- `CBB3771_2_clock_ratio` `delta_ln_clock_ratio`: delta ln(nu_a/nu_b)=sum_I DeltaK_I^ab b_I dX + readout residual <= `MISSING_CLOCK_PRODUCT_BOUND_SOURCE_OR_PROJECTION` `fractional_frequency_or_yr^-1`. Source: P8_Y5_PARENT_QLOC_1805_ALPHA_MASS_CLOCK_BOUND_MATRIX.csv:BM1805_0_alpha_clock.
- `CBB3771_3_clock_redshift` `alpha_clock_redshift`: alpha_clock_redshift=P_clock[b_clock_i,metric_readout_residual,source potential map] <= `MISSING_CLOCK_REDSHIFT_PROJECTION` `dimensionless`. Source: P8_Y5_PARENT_QLOC_1805_ALPHA_MASS_CLOCK_BOUND_MATRIX.csv:BM1805_1_clock_redshift.
- `CBB3771_4_R10_alpha` `alpha_X(lambda_X)`: alpha_X(lambda_X) ~ K_X Qbar_source Qbar_test/(4*pi*Z_X*G_obs) <= `MISSING_R10_FULL_CURVE_AND_MATERIAL_CHARGES` `range-dependent`. Source: P8_Y5_PARENT_QLOC_1805_ALPHA_MASS_CLOCK_BOUND_MATRIX.csv:BM1805_3_R10_yukawa.
- `CBB3771_5_gamma_theta` `delta_gamma_theta`: delta_gamma_theta <= C_gamma_theta epsilon_theta + C_gamma_src epsilon_src <= `2.3e-05` `dimensionless`. Source: P8_Y5_R2FR_3761_GAMMA_BETA_BOUND_EVALUATION.csv:PGB3761_0_gamma_conditional_zero.
- `CBB3771_6_beta_theta` `delta_beta_theta`: delta_beta_theta <= C_beta_theta epsilon_theta + C_beta_bind b_nuc + C_beta_src epsilon_src <= `7.8e-05` `dimensionless`. Source: P8_Y5_R2FR_3761_GAMMA_BETA_BOUND_EVALUATION.csv:PGB3761_1_beta_conditional_zero.
- `CBB3771_7_Gdot_theta` `dln_Geff_dt_theta`: dln_Geff_dt_theta <= |d_t epsilon_theta| + |d_t b_source_norm| + kappa/source calibration residuals <= `9.6e-15` `yr^-1`. Source: P8_Y5_R2FR_3768_KAPPA_BOUND_BUDGET.csv:KBB3768_0_Gdot_total.
- `CBB3771_8_Newton_source_norm` `delta_ln_mu_obs_theta`: delta ln mu_obs|_theta <= C_mu_theta epsilon_theta + b_source_norm + binding/source residuals <= `MISSING_NEWTON_ACTIVE_PASSIVE_SOURCE_PROJECTION` `dimensionless`. Source: P8_Y5_R2FR_3770_SOURCE_ACTION_BOUND_BUDGET.csv:SAB3770_6_Newton_source.

## Claim Gates
- `CG3771_0_sources` pass=`True`: all 3771 source paths exist - path hygiene
- `CG3771_1_theta_zero_theorem` pass=`True`: constant/material-marker conditional zero theorem emitted - zero route exists
- `CG3771_2_unit_cheat_removed` pass=`True`: dimensionful-unit escape is explicitly rejected - dimensionless observables only
- `CG3771_3_current_zero_signed` pass=`False`: current branch signs L_leak_theta=0 - blocked by unsigned superselection/material/source-normalization proofs
- `CG3771_4_coefficients_named` pass=`True`: constant/material residual coefficient rows emitted - b_alpha, b_mu, material, clock, and source-normalization rows named
- `CG3771_5_numeric_bound_envelopes` pass=`True`: WEP/PPN/Gdot envelopes emitted - source-backed external envelopes are wired
- `CG3771_6_missing_rows_nonclaim` pass=`True`: clock/R10/Newton rows remain explicit blockers - no claim with missing projection inputs
- `CG3771_7_constants_material_claim` pass=`False`: constants/material-marker closure claim allowed - blocked until zero proof or all coefficients are sourced and below bounds
- `CG3771_8_local_gr_claim` pass=`False`: local GR/Newton claim allowed - blocked by Newton active/passive source projection and remaining leak gates

## Decisions
- `DEC3771_0`: The constants/material-marker problem is not generic vibes; it is exactly L_leak_theta=zeta^A sum_I (partial L_src/partial theta_I) Lie_EA theta_I. Action: treat theta leakage as a vertical derivative problem.
- `DEC3771_1`: A pure unit/common-scale mode is not a physical force in dimensionless readouts, but it is not enough to close Newtonian GM. Action: do not use unit rescaling to claim absolute G or source mass derivation.
- `DEC3771_2`: The clean derivation route is superselection or q_obs-ownership of alpha, mass ratios, charge/gauge labels, material labels, binding fractions, and clock markers. Action: hunt for parent-action clauses that make Lie_EA theta_I=0.
- `DEC3771_3`: If zero proof fails, the empirical route is now specified: b_alpha, b_mu, b_mA, b_nuc, b_charge, b_clock, b_material_label, and b_source_norm must be sourced or bounded. Action: do not claim clock/WEP/R10/Newton pass while these rows are placeholders.
- `DEC3771_4`: The next highest-value leap is Newtonian active/passive/inertial source normalization, because local GR is not meaningful until the same source charge gives Newtonian GM. Action: attack source Hamiltonian normalization next.

## Next Target
- `3772-Y5-R2FR-source-Hamiltonian-normalization-or-Newton-active-passive-GM-bound.md`: prove the local matter/source Hamiltonian gives the same inertial, passive, and active source charge in the q_obs branch, or emit a Newtonian GM/source-normalization residual bound

## Validation
- `sources_exist` `PASS`: all 3771 source paths exist
- `generated_csvs_parse` `PASS`: all generated 3771 csvs parse
- `theta_zero_theorem` `PASS`: constant/material-marker zero theorem emitted
- `theta_leak_operator` `PASS`: L_leak_theta operator emitted
- `unit_cheat_rejected` `PASS`: dimensionful unit rescaling is not accepted as proof
- `zero_not_claimed` `PASS`: current branch keeps L_leak_theta zero unsigned
- `coefficient_rows` `PASS`: at least nine constants/material coefficient rows emitted
- `numeric_bound_envelopes` `PASS`: WEP/PPN/Gdot numeric envelopes emitted
- `missing_rows_nonclaim` `PASS`: clock/R10/Newton blockers remain explicit
- `claim_gates_closed` `PASS`: constants/local-GR claims remain closed
- `next_target` `PASS`: 3772 Newton source-normalization target emitted
- `no_formalization_leak` `PASS`: no 3771 files written to formalization-workbench
