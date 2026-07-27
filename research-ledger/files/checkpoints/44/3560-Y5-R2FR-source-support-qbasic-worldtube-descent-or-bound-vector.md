# 3560 - Source-support q-basic worldtube descent or bound vector

## Verdict
3560 derives the worldtube/support route in the clean form: if the Hilbert source density `rho_H dV_H` is q-basic, the support is regular, `M_H_ref` is q-basic, and the residual direction is genuinely vertical (`Dq(v_X)=0`), then `W_source`, the shape coordinates `sigma^a`, and `Y=(M_H_ref,sigma^a)` descend through `q`.

That gives the wanted zero route: `D_X W_source=0`, `D_X sigma^a=0`, `A_X=dY(v_X)=0`, hence `Delta_W=C_domain=C_shape=C_M=0` on the preferred 3559 `Pi_M^H` branch.

Still not a local-GR claim. The newly exposed boss is sharper: prove `rho_H dV_H` is q-basic and the support boundary is regular, or bound those failures.

## Exact support lemma
`rho_H dV_H=rhobar_H(q(Phi))` and `Dq(v_X)=0` imply `D_X(rho_H dV_H)=0`.

For a regular support class, unchanged density means unchanged support. For shape moments, Reynolds transport gives a bulk term plus a boundary term; both vanish only when the integrand is q-basic and the support boundary has no birth/death or leakage event.

## What moved
- The worldtube is now tied to the Hilbert density support, not an arbitrary fitted domain.
- `C_shape` and `C_domain` have a real zero route through q-basic support descent.
- A new honest regularity gate appears: boundary birth/death or source-shell layers must be zero or bounded.
- Poynting/EM is handled consistently: stationary minimal EM stress is in `rho_H`; radiative/nonminimal leakage is `E_EM_flux`.
- Next target is the Hilbert density owner: prove or bound `rho_H dV_H` q-basicness.

## Generated outputs
- `source_register`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3560_SOURCE_REGISTER.csv`
- `support_qbasic_theorem`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3560_SOURCE_SUPPORT_QBASIC_THEOREM.csv`
- `support_clause_audit`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3560_SUPPORT_CLAUSE_AUDIT.csv`
- `support_residual_decomposition`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3560_SUPPORT_RESIDUAL_DECOMPOSITION.csv`
- `bound_vector`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3560_BOUND_VECTOR.csv`
- `decision_ledger`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3560_DECISION_LEDGER.csv`
- `status`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3560_STATUS.csv`
- `next_target`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3560_NEXT_TARGET.csv`
- `canonical_status`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_source_support_qbasic_worldtube_status.csv`
- `validation`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_3560_VALIDATION.csv`

## Theorem rows
- `SWT3560_0_support_functor_definition`: Define rho_H[tau,e_obs]=n_mu tau_nu T_H^{mu nu} and W_source:=closure(supp(rho_H dV_H)) on the same e_obs/tau branch before readout.
- `SWT3560_1_qbasic_support_lemma`: If rho_H dV_H is q-basic and the support has a stable regular boundary class, then W_source descends through q; for v_X in ker(Dq), D_X W_source=0.
- `SWT3560_2_Reynolds_shape_moment_zero`: For sigma^a=I^a[W_source,rho_H,e_obs,tau]/M_H_ref, D_X sigma^a=0 if I^a, rho_H dV_H and M_H_ref are q-basic and W_source is vertically fixed.
- `SWT3560_3_Y_qbasic_bundle_theorem`: If M_H_ref is q-basic and the support/shape coordinates sigma^a are q-basic, then Y=(M_H_ref,sigma^a)=Ybar(q(Phi)); for v_X in ker(Dq), A_X=dY(v_X)=0.
- `SWT3560_4_failure_decomposition`: If the support theorem does not fire, D_X Y decomposes into E_rho_qbasic + E_boundary_birth + E_Dq + E_tau_eobs + E_Href + E_readout_mask + E_EM_flux.
- `SWT3560_5_local_closure_consequence`: With 3559 Pi_M^H adoption plus SWT3560_1 through SWT3560_3, Delta_W=C_domain=C_shape=C_M=0. The remaining local closure gates are Pi_M^H dJ_extra, A_parent and side flux.

## Clause audit
- `SCL3560_0_rho_H_qbasic`: rho_H dV_H descends through q from same matter+EM Hilbert variation -> UNSIGNED
- `SCL3560_1_regular_support`: support boundary is compact, regular and has no vertical birth/death event -> NEW_REGULARITY_PREMISE_UNSIGNED
- `SCL3560_2_no_readout_mask`: no fitted/source-specific domain mask enters W_source -> GUARD_ACTIVE_NOT_THEOREM
- `SCL3560_3_MHref_qbasic`: M_H_ref=H_tau-H_ref descends through q -> CONDITIONAL_UNSIGNED
- `SCL3560_4_actual_vertical_basis`: actual residual directions satisfy Dq(v_X)=0 -> MISSING_ACTUAL_QMAP_AND_BASIS
- `SCL3560_5_same_frame_tau_eobs`: same tau/e_obs branch feeds source density, support, charge and readout -> CONDITIONAL_UNSIGNED
- `SCL3560_6_EM_stress_dressing`: stationary minimal EM stress included in T_H; nonstationary/nonminimal flux retained -> CONDITIONAL_DRESSING_RULE

## Residual decomposition
- `SRD3560_0_E_rho_qbasic` `E_rho_qbasic`: LIVE_UNSIGNED (D_X(rho_H dV_H) not forced to zero)
- `SRD3560_1_E_boundary_birth` `E_boundary_birth`: LIVE_UNSIGNED (support boundary births, deaths, discontinuities or distributional layers)
- `SRD3560_2_E_Dq_source` `Dq(v_X)`: LIVE_UNSIGNED (residual direction is not proven vertical for the actual q map)
- `SRD3560_3_E_tau_eobs` `Delta_tau+Delta_eobs`: LIVE_UNSIGNED (source density and support not evaluated on same frame as readout)
- `SRD3560_4_E_Href` `D_X H_ref`: LIVE_UNSIGNED (reference selector drift contaminates M_H_ref)
- `SRD3560_5_E_readout_mask` `Delta_mask`: LIVE_UNSIGNED (domain/support chosen after readout or arena fit)
- `SRD3560_6_E_EM_flux` `Phi_EM_rad;epsilon_EM_extra`: LIVE_UNSIGNED (nonstationary or nonminimal EM/Poynting leakage outside T_H)
- `SRD3560_7_Delta_support_total` `Delta_W+C_domain+C_shape+C_frame`: BOUND_VECTOR_REQUIRED_IF_THEOREM_UNSIGNED (total source-support drift after 3559 Pi_M^H adoption)

## Bound rows
- `BF3560_0_E_rho_qbasic` `E_rho_qbasic`: MISSING_JH_QBASIC_OWNER_OR_BOUND
- `BF3560_1_E_boundary_birth` `E_boundary_birth`: MISSING_REGULAR_SUPPORT_CERTIFICATE_OR_BOUND
- `BF3560_2_E_Dq_source` `E_Dq_source`: MISSING_ACTUAL_QMAP_VERTICAL_BASIS
- `BF3560_3_E_tau_eobs` `Delta_tau;Delta_eobs;C_frame`: MISSING_SAME_FRAME_SOURCE_SUPPORT_LOCK_OR_BOUND
- `BF3560_4_E_Href` `D_X H_ref`: MISSING_HREF_SOURCE_BLINDNESS_OR_BOUND
- `BF3560_5_E_readout_mask` `Delta_mask`: MISSING_NO_READOUT_MASK_THEOREM_OR_BOUND
- `BF3560_6_E_EM_flux` `Phi_EM_rad;epsilon_EM_extra`: MISSING_STATIONARY_MINIMAL_EM_ZERO_OR_FLUX_BOUND
- `BF3560_7_Delta_support_total` `Delta_W+C_domain+C_shape+C_frame`: NONCLAIM_SUM_OF_ROWS_UNTIL_ALL_COMPONENTS_ZERO_OR_NUMERIC

## Decision ledger
- `DEC3560_0`: The source-support descent lemma exists. If the Hilbert density is q-basic and its support is regular, the worldtube support descends too. This is an actual derivation route, not just a missing-label audit.
- `DEC3560_1`: The new hard premise is rho_H q-basicness plus regular support. The support problem has been pushed back to the source-density owner and boundary regularity, which is a sharper target than generic coupling.
- `DEC3560_2`: Poynting/EM stress stays inside the same rule. Stationary minimal EM energy is part of the Hilbert density support; radiative or nonminimal Poynting leakage is not ignored and becomes E_EM_flux.
- `DEC3560_3`: Next target should prove or bound rho_H q-basicness. Without the Hilbert source density owner, the worldtube theorem cannot go live even though the support lemma is mathematically clean.

## Next target
- `3561-Y5-R2FR-Hilbert-source-density-qbasic-owner-or-bound.md`
- Objective: try to prove rho_H dV_H is q-basic from the same matter+EM Hilbert functor with no source-only weights, or fill E_rho_qbasic, prevariation_weight, nonHilbert_bypass and EM_flux bound rows
