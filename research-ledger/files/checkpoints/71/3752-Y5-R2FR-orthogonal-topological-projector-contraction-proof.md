# 3752 — Orthogonal/Topological Projector Contraction Proof

## Status

`ORTHOGONAL_CONTRACTION_PROVED_METRIC_SILENCE_CONDITIONAL`.

This checkpoint proves one piece rather than circling it: a parent-orthogonal projector is contractive. It also blocks the tempting mistake: Hodge/DeWitt orthogonality does not by itself make the projector metric-stress silent.

## Theorem Core
- `THM3752_0_setup` `definition`: Parent Hilbert bundle split — sets the norm in which a contraction statement has meaning
- `THM3752_1_orthogonal_projector` `hypothesis`: Orthogonal projection hypotheses — rules out an oblique projector with arbitrarily large norm
- `THM3752_2_contraction` `exact_theorem`: Contraction proof — therefore ||Pi_M||_{P->P}<=1, with equality unless Pi_M=0
- `THM3752_3_metric_silence` `exact_conditional_theorem`: Metric-independent topological projector — kills bulk projector metric stress only in the parent-owned topological branch
- `THM3752_4_topological_rank_one_norm` `exact_bound`: Topological rank-one bound — topological silence does not automatically give contraction unless the parent norm fixes the dual normalization
- `THM3752_5_hodge_caveat` `counterbranch`: Hodge or DeWitt orthogonality caveat — orthogonal is not the same as metric-stress silent
- `THM3752_6_local_leak_consequence` `conditional_reduction`: Local leak consequence — advances H_op by reducing one factor without claiming full local GR

## Branch Matrix
- `BR3752_0_parent_topological_orthogonal` `BEST_ROUTE_CONDITIONAL`: Pi_M parent-owned, metric-independent, orthogonal/dual-normalized -> ||Pi_M||<=1 and delta_g Pi_M=0
- `BR3752_1_parent_topological_oblique` `BOUND_ROUTE`: Pi_M parent-owned and metric-independent but not orthogonal/dual-normalized -> delta_g Pi_M=0 but ||Pi_M||<=||omega_M||||ell_M||
- `BR3752_2_hodge_orthogonal` `METRIC_STRESS_ROUTE`: Pi_M orthogonal under Hodge/DeWitt/e_obs metric-dependent inner product -> ||Pi_M||<=1 in that metric but delta_g Pi_M remains live
- `BR3752_3_affine_transport_or_mask` `REJECT_OR_BOUND`: Pi_M uses Gamma_ind transport, fitted masks, collars, or empirical selectors before variation -> neither contraction nor metric silence is claimable

## Reduced H_op Interface
- Imported cap: `H_op <= 5.468734671794e+12`.
- `RHOP3752_0_if_parent_signed` `CONDITIONAL_NOT_CLAIM`: `C_pair * 1 * 1 * PPN_response_norm` requires `PPN_response_norm <= 5.468734671794e+12`.
- `RHOP3752_1_if_top_oblique` `BOUND_ROUTE`: `C_pair * ||omega_M||||ell_M|| * 1 * PPN_response_norm` requires `C_pair*||omega_M||||ell_M||*PPN_response_norm <= 5.468734671794e+12`.
- `RHOP3752_2_if_hodge_metric` `ACTIVE_STRESS_ROUTE`: `C_pair * (1 + C_spec||delta_g A_P||/gap_P) * PPN_response_norm` requires `full product must be <= 5.468734671794e+12`.

## Fallback Bounds
- `FB3752_0_metric_projector_stress` `SOURCE_VALUES_MISSING`: `epsilon_Pi_g <= C_pair * ||delta_g Pi_M||_op * ||J_H||_* / M_H_ref`
- `FB3752_1_spectral_projector_derivative` `DERIVED_BOUND_VALUES_MISSING`: `if Pi_M is a spectral projector of A_P(g), ||delta_g Pi_M||_op <= C_spec * ||delta_g A_P||_op / gap_P`
- `FB3752_2_topological_oblique_norm` `DERIVED_BOUND_VALUES_MISSING`: `||Pi_top|| <= ||omega_M||_P ||ell_M||_{P,*}`
- `FB3752_3_domain_motion` `SOURCE_VALUES_MISSING`: `epsilon_Pi_D <= C_Pi_D * ||D_D Pi_M||_op * ||delta D|| * ||J_H||_* / M_H_ref`
- `FB3752_4_boundary_flux` `SOURCE_VALUES_MISSING`: `epsilon_boundary <= |Phi_D| / M_H_ref`
- `FB3752_5_total_absolute` `ABSOLUTE_SUM_GUARD`: `epsilon_projector_abs <= |epsilon_Pi_g|+|epsilon_Pi_D|+|epsilon_boundary|+|epsilon_transition|`
- `FB3752_6_cap_interface` `NONCLAIM_CAP_INTERFACE`: `fallback product must remain below 5.468734671794e+12 after inserting finite projector-stress factors`

## Decisions
- `DEC3752_0_progress` `ORTHOGONAL_CONTRACTION_DERIVED`: The projector norm part is no longer a vague missing coefficient: if Pi_M is parent-orthogonal, ||Pi_M||<=1 follows exactly.
- `DEC3752_1_key_warning` `ORTHOGONAL_NOT_ENOUGH_FOR_METRIC_SILENCE`: If the projector is Hodge/DeWitt metric-built, delta_g Pi_M remains active even though the instantaneous norm is contractive.
- `DEC3752_2_best_route` `PARENT_TOPOLOGICAL_DUAL_NORMALIZED_PROJECTOR`: The least-scrutiny route is to make Pi_M a parent-owned topological/relative-charge projector with fixed dual normalization.
- `DEC3752_3_fallback` `SPECTRAL_PROJECTOR_DERIVATIVE_BOUND`: If metric-built projection is unavoidable, use the spectral-gap derivative bound and feed it into the absolute PPN/source residual vector.

## Claim Gates
- `CG3752_0_sources` pass=`True`: all 3752 source paths exist — path hygiene
- `CG3752_1_contraction_theorem` pass=`True`: orthogonal projector contraction derived — ||Pi_M||<=1 proof recorded
- `CG3752_2_metric_silence_conditional` pass=`True`: metric silence theorem recorded — requires parent-owned topological branch
- `CG3752_3_hodge_caveat` pass=`True`: Hodge/DeWitt caveat retained — prevents false local-GR closure
- `CG3752_4_fallback_bounds` pass=`True`: metric-stress fallback bounds emitted — if topology route fails
- `CG3752_5_parent_signature` pass=`False`: parent topology/norm signature is sourced — still not signed by parent action
- `CG3752_6_parallel_split` pass=`False`: parallel split A_ML=A_LM=0 is sourced — 3747 remains conditional
- `CG3752_7_local_claim` pass=`False`: local GR/Newton/PPN claim allowed — 3752 is proof progress plus bound interface only

## Next Target
- `3753-Y5-R2FR-parent-topological-charge-projector-action-signature.md`: write the exact parent-action signature that makes Pi_M a metric-independent, dual-normalized topological charge projector before variation, or route to the spectral-gap metric-stress bound

## Source Register
- `SRC3752_0_next` exists=`True`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3751_NEXT_TARGET.csv`
- `SRC3752_1_factor_lanes` exists=`True`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3751_HOP_FACTOR_LANES.csv`
- `SRC3752_2_zero_route` exists=`True`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3751_ZERO_ROUTE_CLAUSES.csv`
- `SRC3752_3_projector_variation_contract` exists=`True`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_PiM_projector_variation_stress_CONTRACT.csv`
- `SRC3752_4_topological_naturality` exists=`True`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3498_PROJECTOR_NATURALITY_THEOREM.csv`
- `SRC3752_5_gamma_naturality` exists=`True`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3572_PROJECTOR_NATURALITY_PROOF.csv`
- `SRC3752_6_parallel_zero` exists=`True`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3747_PARALLEL_PROJECTOR_ZERO_THEOREM.csv`
- `SRC3752_7_domain_bounds` exists=`True`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3431_DOMAIN_PROJECTOR_OPERATOR_BOUND_PACK.csv`
- `SRC3752_8_leak_formulas` exists=`True`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3748_PROJECTOR_LEAK_BOUND_FORMULAS.csv`
- `SRC3752_9_cap` exists=`True`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3750_HIDDEN_OPERATOR_NORM_CAPS.csv`
