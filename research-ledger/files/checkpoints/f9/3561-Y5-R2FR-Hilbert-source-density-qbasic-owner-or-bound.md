# 3561 - Hilbert source density q-basic owner or bound

## Verdict
3561 derives the clean density-owner theorem: if the source action is one descended matter+EM Hilbert action `S_src=q^*Sbar_src[q(Phi),psi,theta]`, with fixed representation data, q-owned measure/coframe/time/EM coefficients, no source-only weights, no non-Hilbert bypass, and variation before readout, then `rho_H dV_H` is q-basic.

So for a true vertical residual direction `Dq(v_X)=0`, the density derivative vanishes: `D_X(rho_H dV_H)=0`. That is exactly the missing input needed by the 3560 worldtube/support lemma.

But it is not live yet. The surviving countermodel is simple and dangerous: `S_src=sum_A(1+epsilon_A(X))S_A` or `T_source=sum_A kappa_A(X)T_A`. Ordinary equations can look respectable while the active source density is still weighted. That has to be forbidden by parent grammar or bounded.

## Density theorem
`S_src=q^*Sbar_src` implies `T_H=Tbar_H(q(Phi),psi,theta)`; contracting with q-owned `n`, `tau` and `dSigma_H` gives `rho_H dV_H=rhobar_H(q(Phi),psi,theta)`.

The theorem fails exactly through named channels: source-only weights, hidden markers, non-Hilbert currents, non-q-owned EM coefficients, radiative Poynting flux, readout masks, or nonvertical `Dq(v_X)`.

## What moved
- The density bottleneck is now a precise pullback theorem, not a vague coupling complaint.
- The source-only species-weight countermodel is explicitly retained and cannot be waved away by Ward identities.
- EM/Poynting is split correctly: stationary q-basic Maxwell stress is in `rho_H`; radiative/nonminimal flux is a bound row.
- The next clean target is the no-source-only `Hom` theorem for active-source prefactors.

## Generated outputs
- `source_register`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3561_SOURCE_REGISTER.csv`
- `density_qbasic_theorem`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3561_HILBERT_DENSITY_QBASIC_THEOREM.csv`
- `density_clause_audit`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3561_DENSITY_CLAUSE_AUDIT.csv`
- `density_residual_decomposition`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3561_DENSITY_RESIDUAL_DECOMPOSITION.csv`
- `bound_vector`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3561_BOUND_VECTOR.csv`
- `decision_ledger`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3561_DECISION_LEDGER.csv`
- `status`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3561_STATUS.csv`
- `next_target`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3561_NEXT_TARGET.csv`
- `canonical_status`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_Hilbert_source_density_qbasic_status.csv`
- `validation`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_3561_VALIDATION.csv`

## Theorem rows
- `HDQ3561_0_density_definition`: Define rho_H dV_H := n_mu tau_nu T_H^{mu nu}[e_obs,A_obs,psi,theta] dSigma_H, with T_H from variation of the same matter+EM action before readout.
- `HDQ3561_1_pullback_density_theorem`: If S_matter+S_EM=q^*Sbar_src[q(Phi),psi,theta] with fixed representation data, no source-only weights, q-basic measure/coframe/time/EM coefficient, and variation-before-readout, then rho_H dV_H=rhobar_H(q(Phi),psi,theta).
- `HDQ3561_2_vertical_zero_corollary`: If rho_H dV_H=rhobar_H(q(Phi),psi,theta) and v_X is vertical with Dq(v_X)=0 while matter labels are fixed/gauge/on-shell, then D_X(rho_H dV_H)=0.
- `HDQ3561_3_source_weight_countermodel`: If S_src=sum_A(1+epsilon_A(X))S_A or T_source=sum_A kappa_A(X)T_A is legal before variation, then rho_H is not q-basic in general even when ordinary equations can look acceptable.
- `HDQ3561_4_EM_density_branch`: If the Maxwell sector is q-basic with fixed Z_Q and stationary/no-net-flux support, then the EM contribution to rho_H dV_H is q-basic; radiative or nonminimal Poynting leakage is an explicit E_EM_flux row.
- `HDQ3561_5_live_density_verdict`: The q-basic density theorem is mathematically clean but not live for current MTS because the parent has not signed the unique matter grammar, no-source-only Hom exclusion, non-Hilbert current silence, q-basic EM ownership, actual q-map verticality and boundary regularity together.

## Clause audit
- `HDC3561_0_single_source_action`: S_src=q^*Sbar_src[q(Phi),psi,theta] owns matter+EM source density -> TARGET_SHARP_NOT_PARENT_SIGNED
- `HDC3561_1_no_source_only_weights`: no w_A(X), kappa_A(X), hidden marker or source-only prefactor -> NOT_DERIVED_COUNTERMODEL_RETAINED
- `HDC3561_2_noHom_source_slot`: Hom(species/hidden/readout selector, active-source-prefactor) empty or common constant -> NOT_DERIVED
- `HDC3561_3_variation_before_readout`: T_H and J_H are functional derivatives before material projection/support fitting -> CONDITIONAL_WORKFLOW_CONTRACT
- `HDC3561_4_qbasic_EM`: Maxwell/Hodge sector has q-basic Z_Q and no extra F^2 counterterm -> CONDITIONAL_UNSIGNED
- `HDC3561_5_flux_guard`: stationary support has no unresolved Poynting/radiative boundary leakage -> CONDITIONAL_UNSIGNED
- `HDC3561_6_nonHilbert_silence`: non-Hilbert currents are exact improvements with zero exterior flux or explicit residuals -> RETAINED_PARALLEL_GATE
- `HDC3561_7_actual_vertical_basis`: actual residual directions satisfy Dq(v_X)=0 -> MISSING_ACTUAL_QMAP_AND_BASIS
- `HDC3561_8_boundary_regular_density`: rho_H support boundary has no hidden source shell/birth-death event -> UNSIGNED_FROM_3560

## Residual decomposition
- `HDR3561_0_E_action_pullback` `E_action_pullback`: LIVE_UNSIGNED (source action not proven to factor through q)
- `HDR3561_1_delta_w_species` `delta_w_species`: LIVE_COUNTERMODEL (relative species/action-density source weights)
- `HDR3561_2_kappa_A_source` `kappa_A_source`: LIVE_COUNTERMODEL (post-variation active-source coupling selector)
- `HDR3561_3_hidden_marker_source` `hidden_marker_source`: LIVE_UNSIGNED (hidden/domain/material marker feeding source coefficient)
- `HDR3561_4_nonHilbert_bypass` `nonHilbert_source_bypass`: LIVE_PARALLEL_GATE (active source current not generated by Hilbert variation)
- `HDR3561_5_EM_coefficient_drift` `D_X Z_Q;extra_F2`: LIVE_UNSIGNED (Maxwell/Hodge coefficient or extra F^2 term not q-owned)
- `HDR3561_6_EM_flux` `Phi_EM_rad;epsilon_EM_extra`: LIVE_UNSIGNED (radiative/nonminimal Poynting flux not part of stationary density)
- `HDR3561_7_readout_mask` `Delta_mask`: LIVE_GUARD (support/source density selected after readout)
- `HDR3561_8_E_rho_qbasic_total` `E_rho_qbasic`: BOUND_VECTOR_REQUIRED_IF_THEOREM_UNSIGNED (total vertical derivative of rho_H dV_H after all density-owner channels)

## Bound rows
- `BD3561_0_E_action_pullback` `E_action_pullback`: MISSING_PARENT_SOURCE_ACTION_PULLBACK_OR_BOUND
- `BD3561_1_delta_w_species` `delta_w_species`: MISSING_NO_SOURCE_ONLY_WEIGHT_THEOREM_OR_NUMERIC_EPSILON_A
- `BD3561_2_kappa_A_source` `kappa_A_source`: MISSING_SOURCE_LABEL_FORGETTING_OR_KAPPA_VECTOR
- `BD3561_3_hidden_marker_source` `hidden_marker_source`: MISSING_NOHOM_HIDDEN_MARKER_OR_BOUND
- `BD3561_4_nonHilbert_bypass` `nonHilbert_source_bypass`: MISSING_IMPROVEMENT_ZERO_FLUX_OR_NONHILBERT_BOUND
- `BD3561_5_EM_coefficient_drift` `D_X Z_Q;extra_F2`: MISSING_QBASIC_MAXWELL_OWNER_OR_COEFFICIENT_BOUND
- `BD3561_6_EM_flux` `Phi_EM_rad;epsilon_EM_extra`: MISSING_STATIONARY_FLUX_ZERO_OR_NUMERIC_FLUX_BOUND
- `BD3561_7_readout_mask` `Delta_mask`: MISSING_NO_READOUT_MASK_THEOREM_OR_BOUND
- `BD3561_8_E_rho_qbasic_total` `E_rho_qbasic`: NONCLAIM_SUM_OF_ROWS_UNTIL_ALL_COMPONENTS_ZERO_OR_NUMERIC

## Decision ledger
- `DEC3561_0`: The Hilbert density q-basic theorem is derived conditionally. One descended matter+EM Hilbert action with no source-only weights makes rho_H dV_H a q-basic density, so 3560 support descent can fire.
- `DEC3561_1`: The live obstruction is no-Hom/source-only grammar. The countermodel S_src=sum_A(1+epsilon_A(X))S_A survives unless the parent object language forbids relative active-source weights.
- `DEC3561_2`: EM/Poynting is included without double-counting. q-basic stationary Maxwell stress contributes to rho_H; radiative/nonminimal flux remains a separate E_EM_flux row.
- `DEC3561_3`: Next target should attack the no-source-only Hom theorem. If species/hidden/readout selectors cannot map to active-source prefactors, the density theorem becomes much closer to live.

## Next target
- `3562-Y5-R2FR-no-source-only-Hom-theorem-or-density-weight-bound.md`
- Objective: try to prove species labels, hidden markers and readout/worldtube selectors have no parent Hom into active-source prefactors except common constants; if not, fill delta_w_species, kappa_A_source, hidden_marker_source and Delta_mask bound rows
