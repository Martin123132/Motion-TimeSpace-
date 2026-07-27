# 3575 - R_eq zero from source-worldtube/Hamiltonian glue or residual fill

## Verdict
3575 gets a real coupling foothold.  The old independent topological route can conserve the wrong object, but the Hilbert-identity single-charge branch gives a conditional theorem:

`Pi_M = Pi_M^H`, `Pi_M^H J_H = J_H`, and `J_M^top` is chosen as the exterior representative of the same Hilbert worldtube charge.

Then the exterior periods match, so `Pi_M^H J_H - J_M^top=dC`; choosing `B_zero=C` gives `Pi_M^H J_H=J_M^top+dB_zero` and `R_eq=0` at flux/cohomology level.  Therefore `epsilon_Req_annulus=0` in that branch.

This is not yet a public Newton/local-GR claim.  It still needs parent activation, `H_tau/H_ref` reference lock, zero compact boundary flux, Poynting/extra-mass silence or bounds, and measured-GM calibration.  But it is no longer just 'missing coupling' fog: the best coupling route is now a single explicit branch selector.

## Generated outputs
- `source_register`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3575_SOURCE_REGISTER.csv`
- `single_charge_theorem`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3575_SINGLE_CHARGE_THEOREM.csv`
- `Req_zero_derivation`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3575_REQ_ZERO_DERIVATION.csv`
- `branch_selector`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3575_BRANCH_SELECTOR_AND_RESIDUAL_ENVELOPE.csv`
- `Hamiltonian_GM_gates`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3575_HAMILTONIAN_GM_GLUE_GATES.csv`
- `residual_fill_rows`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3575_RESIDUAL_FILL_ROWS.csv`
- `activation_gates`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3575_ACTIVATION_GATES.csv`
- `decision_ledger`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3575_DECISION_LEDGER.csv`
- `status`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3575_STATUS.csv`
- `next_target`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3575_NEXT_TARGET.csv`
- `canonical_status`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_single_charge_Req_status.csv`
- `validation`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_3575_VALIDATION.csv`

## Single-charge theorem
- `SCT3575_0_single_source_current`: J_H[tau] := -T^mu_nu[e_obs,Psi] tau^nu epsilon_mu, with W_source := closure(supp J_H[tau]) (CONDITIONAL_DEFINITION_FROM_HILBERT_WORLDTUBE_BRANCH)
- `SCT3575_1_identity_PiM`: Pi_M := Pi_M^H on the Hilbert mass-current complex, so Pi_M J_H = J_H and [d,Pi_M]J_H=0 (EXACT_CONDITIONAL_THEOREM)
- `SCT3575_2_same_worldtube_top_class`: Q_H[tau] := integral_{Sigma cap W_source} J_H[tau]; choose [J_M^top] as the linking cohomology class with period Q_H[tau] (CONDITIONAL_CLASS_DEFINITION)
- `SCT3575_3_period_zero_difference`: [Pi_M^H J_H - J_M^top] has zero periods on every linking S2 in the exterior annulus (DERIVED_IF_SINGLE_LINKING_CLASS_AND_NO_HARMONIC_REMAINDER)
- `SCT3575_4_Req_zero_flux`: Pi_M^H J_H = J_M^top + dB_zero with R_eq=0 at the flux/cohomology level (EXACT_CONDITIONAL_FLUX_THEOREM)
- `SCT3575_5_Hamiltonian_charge_lock`: M_H := H_tau[S_outer]-H_ref = integral_{Sigma cap W_source} J_H[tau] and mu_obs=G_ref M_H (DOWNSTREAM_CONDITIONAL_NOT_SIGNED)
- `SCT3575_6_Newton_first_order_transfer`: PC3400_0..6 plus no retained rows imply Delta_Newton_v_coupled=0 (PARTIAL_INPUT_TO_3399_NOT_FULL_PROMOTION)
- `SCT3575_7_PPN_guard`: A same-object source charge does not by itself prove beta, gamma, preferred-frame silence, R10, or clock/orbital residuals (GUARDRAIL_RETAINED)

## R_eq derivation
- `REQ3575_0_start`: R_eq := Pi_M J_H - J_M^top - dB_zero (EXACT)
- `REQ3575_1_identity_branch`: Pi_M=Pi_M^H => Pi_M J_H=J_H and [d,Pi_M]J_H=0 (EXACT_IF_BRANCH_ADOPTED)
- `REQ3575_2_same_periods`: integral_S Pi_M^H J_H = Q_H[tau] = integral_S J_M^top for every allowed linking surface S (DERIVED_IF_WORLD_TUBE_SOURCE_MEASURE_LOCKED)
- `REQ3575_3_exact_difference`: d(Pi_M^H J_H-J_M^top)=0 and all periods vanish => Pi_M^H J_H-J_M^top=dC (DERIVED_IF_TOPOLOGY_SELECTOR_CLEAN)
- `REQ3575_4_absorb_C`: Pi_M^H J_H=J_M^top+dB_zero and R_eq=0 (CONDITIONAL_REQ_ZERO)
- `REQ3575_5_flux_result`: int_A d(Pi_M^H J_H)=int_A dR_eq=0 (EXACT_CONDITIONAL_FLUX_CLOSURE)
- `REQ3575_6_exchange_exception`: Pi_M dJ_extra, Poynting collar flux, boundary/reference flux, or non-EH charge re-enters as R_eq_eff (RETAINED_EXCEPTION)
- `REQ3575_7_verdict`: R_eq=0 is derivable for the Hilbert-identity single-charge branch at flux/cohomology level; current MTS has not yet parent-activated all branch clauses (CONDITIONAL_THEOREM_NOT_CURRENT_CLAIM)

## Branch selector
- `BSC3575_0_selector` `B_single_charge`: B_SC := I_same_JH * I_PiM_identity * I_same_worldtube_period * I_no_harmonic_remainder * I_Bzero_zero_flux * I_no_extra_exchange (SELECTOR_DEFINED_NONCLAIM)
- `BSC3575_1_Req_flux` `epsilon_Req_annulus`: epsilon_Req_annulus = (1-B_SC) * epsilon_Req_input (CONDITIONAL_ZERO_OR_INPUT)
- `BSC3575_2_commutator` `I_commutator`: I_commutator = (1-B_PiM_identity) * I_commutator_topological (CONDITIONAL_ZERO_OR_INPUT)
- `BSC3575_3_projector_stress` `T_PiM_projector`: T_PiM_projector = 0 in identity/inclusion branch; retained for Hodge/DeWitt/domain/readout projectors (CONDITIONAL_ZERO_OR_INPUT)
- `BSC3575_4_mass_envelope` `epsilon_M_total`: epsilon_M_total <= epsilon_Req_annulus + epsilon_Bzero_flux + epsilon_Wsource_glue + epsilon_Poynting_worldtube + epsilon_extra_mass + epsilon_Href_lock + epsilon_cal (EXECUTABLE_ENVELOPE_NONCLAIM)
- `BSC3575_5_Newton_product` `Delta_Newton_v_coupled`: Delta_Newton_v_coupled=(1+delta_KC)(1+epsilon_M_total)(1+delta_kappa)(1+delta_ellJ)-1 (USES_3399_PRODUCT_LAW)

## Hamiltonian/GM gates
- `HGM3575_0_tau_lock`: tau_source=tau_H=tau_clock=tau_orbit (PARTIAL_OPEN)
- `HGM3575_1_Htau_integrability`: delta H_tau finite and field-space curl zero after boundary/reference conditions (PARTIAL_EH_ONLY_EXTRA_CURLS_OPEN)
- `HGM3575_2_Href_lock`: H_ref fixed before source/orbit comparison and derivative-silent (OPEN)
- `HGM3575_3_same_source_measure`: M_source[W] := H_tau[S_outer]-H_ref = integral_{Sigma cap W_source} J_H[tau] (CONDITIONAL_DEFINITION_REQUIRED)
- `HGM3575_4_constant_Gref`: kappa_MTS=8*pi*G_ref/c^4 with no source/species/range/frame labels (CAN_SIGN_AS_PARENT_CONSTANT_NOT_SI_DERIVATION)
- `HGM3575_5_Poisson_Gauss`: B_xi/G_ref=M_eff[Pi_M J_H] and weak-field Poisson/Gauss/orbital readout agree (CONDITIONAL_NOT_PARENT_DERIVED)
- `HGM3575_6_no_extra_mass`: Q_nonEH+Q_PiM+Q_boundary+Q_domain+Q_memory+Q_range+Q_delta_kappa+Q_Poynting=0 or retained (FAIL_OPEN_RETAIN_ROWS)

## Residual rows
- `RF3575_0_epsilon_Req_input` `epsilon_Req_input`: |int_A dR_eq|/|M_eff| for non-single-charge branches (MISSING_NUMERIC_OR_ZERO_THEOREM)
- `RF3575_1_epsilon_Bzero_flux` `epsilon_Bzero_flux`: |int_boundary dB_zero|/|M_eff| (MISSING_BOUNDARY_REFERENCE_INPUT)
- `RF3575_2_epsilon_Wsource_glue` `epsilon_Wsource_glue`: |Q_M-integral_W J_H[tau]|/|M_eff| (ZERO_IN_SINGLE_CHARGE_BRANCH_ELSE_MISSING_INPUT)
- `RF3575_3_epsilon_Poynting_worldtube` `epsilon_Poynting_worldtube`: |int_W Pi_M dJ_Poynting|/|M_eff| or collar-flux bound (BOUND_FORMULA_READY_INPUTS_MISSING)
- `RF3575_4_epsilon_Href_lock` `epsilon_Href_lock`: |D_X H_ref|/|M_eff| or field-space curl/reference mismatch envelope (MISSING_REFERENCE_FUNCTIONAL)
- `RF3575_5_epsilon_extra_mass` `epsilon_extra_mass`: |Q_nonEH+Q_boundary+Q_domain+Q_memory+Q_range+Q_delta_kappa|/|M_eff| (MISSING_ZERO_CERTIFICATES_OR_BOUNDS)
- `RF3575_6_epsilon_cal` `epsilon_cal`: |M_eff[Pi_M J_H]-M_Gauss_orbital|/|M_eff| (CALIBRATION_GATE_OPEN)
- `RF3575_7_dlnMeff_dt` `dln_Meff_dt`: D_t ln int_S Pi_M J_H; zero in B_SC branch only after H_ref/extra/Poynting silence (LIVE_DERIVATIVE_ROW)
- `RF3575_8_partial_r_ln_mu_obs` `partial_r_ln_mu_obs`: partial_r ln G_eff + partial_r ln M_eff + partial_r ln(1+epsilon_M_total) (LIVE_RADIAL_ROW)

## Activation gates
- `GATE3575_0_sources`: PASS (all required 3575 source paths exist)
- `GATE3575_1_identity_PiM`: PASS_CONDITIONAL (3426 gives exact commutator/projector-stress zero if parent adopts Pi_M^H)
- `GATE3575_2_Req_flux_zero`: PASS_CONDITIONAL (same-worldtube periods plus identity Pi_M imply R_eq=0 at flux/cohomology level)
- `GATE3575_3_parent_activation`: FAIL_CURRENT_CLAIM (the current corpus has not adopted all B_SC clauses in one parent branch)
- `GATE3575_4_boundary_reference`: FAIL_CURRENT_CLAIM (reference and compact-boundary flux remain open)
- `GATE3575_5_poynting_extra`: FAIL_CURRENT_CLAIM (Poynting/exchange/no-extra-mass rows remain unfilled)
- `GATE3575_6_Newton`: PARTIAL_NOT_PROMOTED (R_eq piece can close conditionally; kappa/ell_J/v-ratio/Href/no-extra-mass still decide the full product)
- `GATE3575_7_local_GR`: FAIL_CURRENT_CLAIM (PPN beta/gamma/preferred-frame and R10/clock/orbital rows remain downstream)

## Decisions
- `DEC3575_0_adopt_best_route`: prefer Hilbert identity/inclusion Pi_M over independent topological Pi_M for local source coupling -> Old topological Pi_M is kept only as a demoted/bounded branch.
- `DEC3575_1_Req_progress`: count R_eq flux-zero as conditionally derived, not merely missing -> Future work should sign/adopt the branch or fill the named residual rows; do not re-audit generic topology.
- `DEC3575_2_G_constant_note`: do not try to derive the SI value of Newton's constant here -> This prevents wasting effort on deriving the numerical value of G while still blocking cheating by variable G.
- `DEC3575_3_next_target`: write the adoption packet for PC3400_3 and PC3400_4 or fill the first residual rows -> 3576 should attempt the parent adoption patch for the single-charge source branch.

## Status
- `REQ_FLUX_ZERO_CONDITIONAL_THEOREM_DERIVED_FOR_HILBERT_IDENTITY_BRANCH_NOT_PROMOTED`: If Pi_M is the Hilbert identity/inclusion and J_M^top is the exterior representative of the same Hilbert worldtube charge, then R_eq can be set to zero at flux/cohomology level and epsilon_Req_annulus=0.

## Validation
- `VAL3575_0_sources_exist`: PASS (all required 3575 source paths exist)
- `VAL3575_1_required_needles_found`: PASS (all selected 3575 same-object/source-coupling needles found)
- `VAL3575_2_outputs_exist`: PASS (all pre-validation 3575 output files written)
- `VAL3575_3_csv_parse`: PASS (source_register:28; single_charge_theorem:8; Req_zero_derivation:8; branch_selector:6; Hamiltonian_GM_gates:7; residual_fill_rows:9; activation_gates:8; decision_ledger:4; status:1; next_target:1; canonical_status:1)
- `VAL3575_4_identity_theorem_present`: PASS (Hilbert identity/inclusion Pi_M theorem present)
- `VAL3575_5_Req_zero_flux_present`: PASS (conditional R_eq zero row present)
- `VAL3575_6_selector_present`: PASS (single-charge selector present)
- `VAL3575_7_residual_envelope_present`: PASS (epsilon_M no-cancellation envelope present)
- `VAL3575_8_residual_rows_present`: PASS (first residual fill rows present)
- `VAL3575_9_parent_not_promoted`: PASS (parent activation remains unclaimed)
- `VAL3575_10_next_target_selected`: PASS (PC3400_3/4 adoption next target selected)
- `VAL3575_11_no_claim_flags`: PASS (all generated physics rows remain nonclaim)
- `VAL3575_12_generated_source_paths_exist`: PASS (every generated row source_path exists)
- `VAL3575_13_formalization_workbench_untouched`: PASS (no 3575 checkpoint output appears in formalization-workbench)

## Next target
- `3576-Y5-R2FR-PC3400-3-4-single-charge-parent-adoption-or-first-residual-fill.md`
- Objective: attempt to write a parent adoption packet for the Hilbert-identity single-charge branch that signs PC3400_3 and narrows PC3400_4; if not, fill first source-backed epsilon_Href/epsilon_extra/Poynting residual rows
