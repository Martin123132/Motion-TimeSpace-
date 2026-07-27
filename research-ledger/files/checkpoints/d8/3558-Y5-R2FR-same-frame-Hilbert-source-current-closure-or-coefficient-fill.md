# 3558 - Same-frame Hilbert source-current closure or coefficient fill

## Verdict
3558 gets the source-current problem into its sharp form. The closure theorem is exact: if the same observed coframe/time/source branch defines the Hilbert current, `Pi_M` is the Hilbert mass-current identity/inclusion chainmap, extra currents have zero mass projection, and boundary/worldtube/frame data are fixed before readout, then `d(Pi_M J_H)=0` and the first-order Newton source charge is stable.

But the current MTS branch has not signed all those clauses. The honest status is conditional theorem plus coefficient rows, not a local-GR claim.

## Exact obstruction
`d(Pi_M J_H) = -Pi_M dJ_extra + [d,Pi_M]J_H + A_parent`.

So the live boss fight is not vague coupling anymore. It is three concrete terms: projected extra-current, Pi_M commutator, and parent anomaly/multiplier.

## What moved
- The cleanest `Pi_M` route is now selected: Hilbert identity/inclusion, not a new topological projector with extra stress.
- Ordinary stationary EM stress is dressed into `M_H`; only nonminimal or radiative Poynting leakage remains as `mu_extra`.
- First-order Newton is reachable if the Hilbert current closure and Gauss/orbital readout clauses are parent-signed.
- Full local GR still needs PPN source stability after that.

## Generated outputs
- `source_register`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3558_SOURCE_REGISTER.csv`
- `closure_theorem`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3558_HILBERT_CURRENT_CLOSURE_THEOREM.csv`
- `clause_audit`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3558_CLOSURE_CLAUSE_AUDIT.csv`
- `obstruction_map`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3558_OBSTRUCTION_RESIDUAL_MAP.csv`
- `coefficient_fill`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3558_COEFFICIENT_FILL_ROWS.csv`
- `decision_ledger`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3558_DECISION_LEDGER.csv`
- `status`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3558_STATUS.csv`
- `next_target`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3558_NEXT_TARGET.csv`
- `canonical_status`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_same_frame_Hilbert_source_current_closure_status.csv`
- `validation`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_3558_VALIDATION.csv`

## Key theorem rows
- `HC3558_0_same_frame_Hilbert_current_definition`: If matter descends through a single observed coframe e_obs=q(Phi) before readout, the active ordinary source current is J_H[tau]=T_H^{mu nu}[e_obs] n_mu tau_nu dSigma, with T_H from the variational derivative of S_matter[e_obs].
- `HC3558_1_projected_flux_obstruction_identity`: For any defined mass projector Pi_M, d(Pi_M J_H)= -Pi_M dJ_extra + [d,Pi_M]J_H + A_parent.
- `HC3558_2_closure_sufficient_conditions`: If Pi_M dJ_extra=0, [d,Pi_M]J_H=0, A_parent=0, tau/e_obs/source support are fixed, and the exterior is source-free/stationary, then d(Pi_M J_H)=0 and linked-surface M_eff is time/radius independent.
- `HC3558_3_Hilbert_identity_PiM_route`: The cleanest Pi_M option is not an independent topological/Hodge projector: take Pi_M as the identity/inclusion on the Hilbert mass-current object after the source branch is defined. Then [d,Pi_M]J_H=0 by construction, provided the source object is fixed before readout.
- `HC3558_4_Poynting_dressing_rule`: Ordinary stationary Maxwell field energy belongs inside the dressed Hilbert source charge M_H; only nonminimal EM coupling, radiative Poynting leakage, or background cross-terms remain as mu_extra coefficients.
- `HC3558_5_Newton_first_order_corollary`: If HC3558_0 through HC3558_4 are signed and G_N is constant, the local first-order Newton source branch follows: nabla^2 Phi=4*pi*G_N rho_H and a_r=-G_N M_H/r^2 up to explicitly retained PPN/operator residuals.

## Clause audit
- `CL3558_0_same_frame`: same observed coframe/time generator -> CONDITIONAL_NOT_PARENT_DERIVED
- `CL3558_1_Hilbert_current`: Hilbert current from same matter action -> EXACT_CONDITIONAL_NOT_PARENT_FORCED
- `CL3558_2_PiM_chainmap`: Pi_M identity/inclusion or fixed chain map -> BEST_ROUTE_CONDITIONAL_UNSIGNED
- `CL3558_3_extra_mass_silence`: extra currents have no mass projection -> NOT_PARENT_DERIVED
- `CL3558_4_parent_anomaly_zero`: no parent anomaly/multiplier term -> NOT_SATISFIED
- `CL3558_5_worldtube_support`: source support and linking surfaces fixed before readout -> WORLDTUBE_REFERENCE_UNSIGNED
- `CL3558_6_stationary_no_flux`: stationary local exterior/no side flux -> RETAINED_FLUX_COEFFICIENT_REQUIRED
- `CL3558_7_Gauss_orbital_readout`: closed charge calibrates to inverse-square orbit -> NOT_DERIVED
- `CL3558_8_PPN_stability`: source charge stable through PPN -> NOT_DERIVED

## Coefficient fill rows
- `CF3558_0_sigma_Gdot` `sigma_Gdot`: MISSING_PARENT_COEFFICIENT_OR_DERIVED_ZERO
- `CF3558_1_eta_source_AB` `eta_source_AB`: MISSING_SELECTOR_BLIND_THEOREM_OR_ETA_SOURCE_VECTOR
- `CF3558_2_radial_profile` `partial_r_ln_mu_obs;epsilon_radial_MH(r)`: MISSING_GAUSS_NOHAIR_THEOREM_OR_PROFILE
- `CF3558_3_frame_split` `delta_frame_source`: MISSING_SAME_FRAME_SOURCE_THEOREM_OR_DELTA_FRAME
- `CF3558_4_mu_extra` `mu_extra_boundary_bulk_domain/(G_N M_H)`: MISSING_ZERO_THEOREM_OR_CHANNEL_VECTOR_VALUES
- `CF3558_5_PiM_commutator` `Delta_PiM;C_M;C_shape`: MISSING_HILBERT_IDENTITY_PIM_ADOPTION_OR_CHAINMAP_PROOF
- `CF3558_6_EM_flux` `epsilon_EM_extra;Phi_EM_rad`: CONDITIONAL_ZERO_IF_MINIMAL_STATIONARY_ELSE_MISSING_FLUX_COEFFICIENT
- `CF3558_7_PPN_source` `delta_beta_source;gamma_minus_1`: MISSING_SECOND_ORDER_SOURCE_PPN_VECTOR

## Decision ledger
- `DEC3558_0`: Same-frame Hilbert current closure is derivable in principle. The exact theorem is not a plateau axiom: it follows from a variational Hilbert current, Pi_M chainmap/identity, zero extra mass current, zero anomaly, and fixed worldtube/frame data.
- `DEC3558_1`: Current MTS still fails live source-current closure. Pi_M dJ_extra, [d,Pi_M]J_H, A_parent, boundary symplectic flux, worldtube/reference selectors, frame/species source split, and PPN stability are not all parent-signed.
- `DEC3558_2`: Poynting intuition is integrated rather than ignored. Stationary minimal EM stress is part of the dressed Hilbert source; nonstationary or nonminimal Poynting/cross-term leakage remains an explicit coefficient row.
- `DEC3558_3`: Next target is parent adoption of the Hilbert identity/inclusion Pi_M plus q-basic source support. That route attacks the largest obstruction [d,Pi_M]J_H without introducing new topological projector stress.

## Next target
- `3559-Y5-R2FR-Hilbert-identity-PiM-chainmap-source-support-adoption-or-bound.md`
- Objective: try to parent-sign Pi_M as the Hilbert mass-current identity/inclusion chainmap with q-basic source support and fixed tau/e_obs; if not, fill Delta_PiM, C_M, C_shape, C_domain, C_frame and source-support coefficient rows
