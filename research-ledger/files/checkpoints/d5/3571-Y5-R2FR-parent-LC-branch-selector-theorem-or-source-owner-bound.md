# 3571 - Parent LC branch selector theorem or source-owner bound

## Verdict
3571 reduces the parent LC selector to an exact finite product gate: `B_LC_selector = product_s I_s`.  Every active sector must either exclude `Gamma_ind/omega_ind` by argument-domain exhaustion or carry an explicit bound.  This is the no-smuggling rule in theorem form.

The selector is not public yet.  The live blockers are now narrow and named: projector/domain reentry, boundary/source-owner flux, `H_ref/M_H` reference lock, Poynting/collar flux, GM transfer, and clock/light/orbit downstream certificates.  Crucially, Poynting is not ignored: it is kept as Hilbert/Noether source energy or as `epsilon_Poynting_worldtube` if boundary flux survives.

## Generated outputs
- `source_register`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3571_SOURCE_REGISTER.csv`
- `selector_theorem`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3571_BLC_SELECTOR_THEOREM.csv`
- `sector_product_matrix`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3571_BLC_SECTOR_PRODUCT_MATRIX.csv`
- `leakage_bound_rows`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3571_SOURCE_OWNER_LEAKAGE_BOUND_ROWS.csv`
- `activation_gates`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3571_ACTIVATION_GATES.csv`
- `decision_ledger`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3571_DECISION_LEDGER.csv`
- `status`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3571_STATUS.csv`
- `next_target`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3571_NEXT_TARGET.csv`
- `canonical_status`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_parent_LC_branch_selector_status.csv`
- `validation`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_3571_VALIDATION.csv`

## Selector theorem
- `BLC3571_0_exact_product_gate`: B_LC_selector = product_s I_s, where I_s=1 only when sector s has no independent Gamma_ind/omega_ind action slot and no downstream source-current reentry. (DERIVED_PRODUCT_GATE)
- `BLC3571_1_variable_absence`: If Arg(S_s) excludes Gamma_ind, then delta S_s/delta Gamma_ind=0 in the reduced field domain. (EXACT_MATH)
- `BLC3571_2_coframe_owned_spin`: omega_spin=omega_LC[e_obs] routes spin variation through the coframe/Hilbert equation, not an independent torsion equation. (EXACT_IF_PARENT_SPIN_SIGNATURE_SELECTED)
- `BLC3571_3_same_frame_EM`: A_Q,F_Q,*_obs(e_obs) have no affine Gamma slot; Poynting energy belongs in J_H/H_tau or in an explicit collar-flux residual. (DERIVED_CONDITIONAL_PUBLIC_HODGE_AND_FLUX_BOUND_OPEN)
- `BLC3571_4_readout_no_reentry`: Clock/light/orbit/R10/PPN readouts do not source Gamma if they are downstream functors of solved e_obs,A_Q,J_H,M_H,tau,theta and do not define extra source-labelled currents. (CONDITIONAL_CONTRACT)
- `BLC3571_5_public_selector_result`: The parent LC selector is mathematically reduced to a finite product gate, but the public product is not 1 because projector/domain, boundary/source-owner, GM/reference and Poynting/collar clauses are not parent-signed. (PARTIAL_THEOREM_PUBLIC_CLAIM_BLOCKED)

## Sector product gates
- `SELP3571_0_matter` `I_matter`: CONDITIONAL_SUPPORTED_PRIVATE (parent action/spurion exclusion still private)
- `SELP3571_1_spin` `I_spin`: CONDITIONAL_SUPPORTED_PRIVATE (metric-affine counterbranch not parent-excluded publicly)
- `SELP3571_2_EM` `I_EM`: PARTIAL_SUPPORTED (scalar lambda_A/alpha owner and boundary flux norms open)
- `SELP3571_3_source` `I_source`: PRIVATE_CONDITIONAL (support/reference/projector and finite-source boundary open)
- `SELP3571_4_projector` `I_projector`: LIVE_WEAK_LINK (delta_Gamma Pi_M operator norm or theorem missing)
- `SELP3571_5_clocks` `I_clock`: UNSIGNED_READOUT_SLOT (clock protocol argument list not parent-signed)
- `SELP3571_6_light` `I_light`: PARTIAL_READOUT_SLOT (Shapiro/ray/detector downstream proof not signed)
- `SELP3571_7_orbit` `I_orbit`: UNSIGNED_READOUT_SLOT (test-body limit and GM transfer not parent-signed)
- `SELP3571_8_boundary` `I_boundary`: LIVE_PRIMARY_LEAK (boundary flux, H_ref/M_H, owner current not parent-derived)
- `SELP3571_9_total` `B_LC_selector`: FALSE_PUBLICLY_CURRENTLY (one live leak is enough to keep public selector false)

## Leakage bounds
- `LEAK3571_0_projector_comm` `epsilon_projector_comm`: ||delta_Gamma Pi_M|| * ||J_H|| / abs(M_H_ref) (COUNTERMODEL_ACTIVE_BOUND_REQUIRED)
- `LEAK3571_1_boundary_flux` `epsilon_boundary_flux`: abs(int_partialSigma n_i K_owner^{i0} dS) / abs(M_H_ref) (BOUND_ROW_FORMULA_DERIVED_INPUTS_MISSING)
- `LEAK3571_2_MHref_reference` `epsilon_MHref`: abs(delta_Gamma(H_tau-H_ref)) / abs(M_H_ref) (REFERENCE_LOCK_UNSIGNED)
- `LEAK3571_3_Poynting_worldtube` `epsilon_Poynting_worldtube`: mu0^-1 ||E_T||_L2(B)||B_T||_L2(B)/abs(M_H_ref) + collar_flux/abs(M_H_ref) (PLACED_BUT_INPUT_NORMS_MISSING)
- `LEAK3571_4_GM_transfer` `epsilon_GM_transfer`: abs(delta_Gamma(G_ref M_H)+delta_cal GM_obs)/abs(G_ref M_H) (GM_TRANSFER_UNSIGNED)
- `LEAK3571_5_total_selector_tail` `epsilon_selector_leak`: epsilon_projector_comm + epsilon_boundary_flux + epsilon_MHref + epsilon_Poynting_worldtube + epsilon_GM_transfer + clock/light/orbit readout tails (EXECUTABLE_SYMBOLIC_NONCLAIM)

## Activation gates
- `GATE3571_0_sources`: PASS (all required 3571 source paths exist)
- `GATE3571_1_product_gate`: PASS_CONDITIONAL (exact product/no-cancellation selector theorem derived)
- `GATE3571_2_matter_spin`: PASS_PRIVATE_NOT_PUBLIC (ordinary/coframe spin clauses are written but not public parent selector)
- `GATE3571_3_projector`: FAIL_CURRENT_PUBLIC_CLAIM (delta_Gamma Pi_M theorem/operator norm missing)
- `GATE3571_4_boundary_source_owner`: FAIL_CURRENT_PUBLIC_CLAIM (boundary flux, H_ref/M_H and owner current not parent-derived)
- `GATE3571_5_poynting_flux`: FAIL_NUMERIC_BOUND_READY_ONLY (formula retained; E/B/collar norms missing)
- `GATE3571_6_public_BLC`: FAIL_CURRENT_PUBLIC_CLAIM (product gate has live non-signed factors)
- `GATE3571_7_axial_consequence`: FAIL_CURRENT_PUBLIC_CLAIM (axial zero remains private until B_LC is public or leaks are bounded)

## Decisions
- `DEC3571_0_selector_reduction`: treat B_LC as a finite product gate -> future work attacks named leak rows instead of restarting the torsion discussion
- `DEC3571_1_poynting_kept`: keep Poynting as source-owner/boundary flux, not axial torsion -> EM stress remains in the GR source route while its boundary leakage gets a bound formula
- `DEC3571_2_next_target`: attack projector naturality first -> 3572 should try to prove delta_Gamma Pi_M=0 or source its operator norm

## Status
- `BLC_SELECTOR_REDUCED_TO_PRODUCT_GATE_AND_LEAKAGE_BOUND_LEDGER`: B_LC_selector=product_s I_s exact no-cancellation gate; axial C_A=0 follows if all I_s=1, otherwise selector leakage is bounded by projector, boundary, H_ref, Poynting and GM-transfer rows.

## Validation
- `VAL3571_0_sources_exist`: PASS (all required 3571 source paths exist)
- `VAL3571_1_required_needles_found`: PASS (all selected selector/leak source needles found)
- `VAL3571_2_outputs_exist`: PASS (all pre-validation 3571 output files written)
- `VAL3571_3_csv_parse`: PASS (source_register:16; selector_theorem:6; sector_product_matrix:10; leakage_bound_rows:6; activation_gates:8; decision_ledger:3; status:1; next_target:1; canonical_status:1)
- `VAL3571_4_product_gate_present`: PASS (B_LC product gate theorem present)
- `VAL3571_5_sector_matrix_present`: PASS (sector product matrix includes total selector)
- `VAL3571_6_leak_bounds_present`: PASS (key leakage bound formulas present)
- `VAL3571_7_public_claim_blocked`: PASS (public B_LC selector remains blocked)
- `VAL3571_8_projector_next_selected`: PASS (projector naturality selected as next target)
- `VAL3571_9_no_claim_flags`: PASS (all generated physics rows remain nonclaim)
- `VAL3571_10_generated_source_paths_exist`: PASS (every generated row source_path exists)
- `VAL3571_11_formalization_workbench_untouched`: PASS (no 3571 checkpoint output appears in formalization-workbench)

## Next target
- `3572-Y5-R2FR-projector-naturality-deltaGammaPi-zero-or-operator-norm.md`
- Objective: try to prove Pi_M is q/e_obs/tau-natural so delta_Gamma Pi_M=0; if not, create a source-backed operator-norm row for epsilon_projector_comm
