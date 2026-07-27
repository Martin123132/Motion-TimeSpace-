# 3755 — Global Kappa Superselection Or Coupling Residual Vector

## Status

`BIANCHI_KAPPA_LEMMA_DERIVED_SUPERSELECTION_UNSIGNED_RESIDUAL_VECTOR_EMITTED`.

This checkpoint separates the honest theorem from the claim. Bianchi can force derivative-silent coupling only under same-frame, separately conserved, arbitrary-source conditions; otherwise the kappa exchange term is physical and must be scored.

## Kappa Theorem Rows
- `KT3755_0_configuration_split` `SIGNATURE_REQUIRED_NOT_SOURCED`: Superselection signature — would give delta_local kappa_eff=0 and no local Euler equation for kappa
- `KT3755_1_global_parameter` `EXACT_IF_K_GLOBAL`: Global coupling derivative silence — kills Gdot/source/range/frame coupling derivatives
- `KT3755_2_bianchi_arbitrary_source` `EXACT_CONDITIONAL_THEOREM`: Bianchi arbitrary-source lemma — can prove derivative silence if same-frame separate conservation and arbitrary-source premises are signed
- `KT3755_3_exchange_fallback` `NO_OVERCLAIM_COUNTERBRANCH`: Bianchi exchange fallback — activates delta_kappa_source and q_exchange rows
- `KT3755_4_source_blindness` `EXACT_IF_K_GLOBAL_SOURCE_BLIND`: Species/source-label silence — kills active-gravitational-source composition dependence from kappa itself
- `KT3755_5_range_blindness` `EXACT_IF_NOT_LOCAL_FIELD`: Range/radius silence — kills kappa-owned R10/radial coupling hair; other mu_extra range channels remain separate
- `KT3755_6_constant_offset` `ANTI_OVERCLAIM_POLICY`: Absolute G policy — allows GR-like Newton limit without claiming measured G is derived

## Superselection Clauses
- `SC3755_0_factorization` `UNSIGNED_PARENT_SIGNATURE`: Q_parent = Q_dyn x K_global -> derive from parent action/category or retain scalar-kappa residuals
- `SC3755_1_no_local_variation` `PASS_IF_SC3755_0_SIGNED`: delta_local kappa_eff = 0 -> blocks scalar-tensor local force
- `SC3755_2_trivial_MTS_action` `PASS_IF_K_GLOBAL_TRIVIAL`: partial_Z/IQ/C/D kappa_eff = 0 -> blocks domain/range/preferred-location coupling hair
- `SC3755_3_no_species_label` `PASS_IF_K_GLOBAL_SOURCE_BLIND`: partial_A/source kappa_eff = 0 -> blocks kappa contribution to eta_source_AB
- `SC3755_4_no_range_time_radial` `PASS_IF_K_GLOBAL_NOT_LOCAL_FIELD`: partial_t,r,lambda kappa_eff = 0 -> blocks local Gdot/R10 from kappa
- `SC3755_5_bianchi_same_frame` `CONDITIONAL_UNSIGNED`: nabla T_obs=0 for arbitrary same-frame matter -> backup theorem, not replacement for parent signature
- `SC3755_6_exchange_owned` `OPEN`: q_exchange=0 or mapped -> delta_kappa_source row remains live if not signed

## Coupling Residual Vector
- `KRV3755_0_Gdot` `MISSING_DTLN_KAPPA_EFF_OR_SUPERSELECTION_ZERO`: `dln_Geff_dt` arena `LLR/Gdot` bound `9.6e-15 yr^-1`
- `KRV3755_1_species_source` `MISSING_SOURCE_BLIND_KAPPA_OR_ETA_SOURCE_VALUE`: `eta_source_AB` arena `MICROSCOPE/WEP` bound `2.8e-15 dimensionless`
- `KRV3755_2_range` `MISSING_NO_RANGE_THEOREM_OR_ALPHA_LAMBDA_CURVE`: `alpha(lambda)` arena `R10 inverse-square` bound `alpha(lambda) range-dependent`
- `KRV3755_3_radial` `MISSING_RADIAL_PROFILE_OR_NO_RADIAL_HAIR_THEOREM`: `partial_r_ln_mu_obs` arena `orbital/R10/radial source profile` bound `zero_or_mapped_bound inverse_length_or_dimensionless_envelope`
- `KRV3755_4_delta_kappa_exchange` `MISSING_ARENA_PROJECTION_OR_DERIVED_ZERO_EXCHANGE`: `delta_kappa_source` arena `PPN/R10/local exchange` bound `same-frame theorem or explicit exchange coefficient projected_force_density_or_dimensionless_normalized_residual`
- `KRV3755_5_frame` `MISSING_SAME_FRAME_SOURCE_THEOREM_OR_FRAME_RESIDUAL`: `delta_frame_source` arena `WEP/clock/preferred-frame` bound `zero_or_row_locks dimensionless`
- `KRV3755_6_gamma` `MISSING_FULL_PPN_VECTOR_PROJECTION`: `gamma_minus_1` arena `Cassini/Shapiro` bound `2.3e-05 dimensionless`
- `KRV3755_7_beta` `MISSING_SECOND_ORDER_SOURCE_THEOREM_OR_VALUE`: `delta_beta_source` arena `PPN beta` bound `7.8e-05 dimensionless`

## Claim Gates
- `CG3755_0_sources` pass=`True`: all 3755 source paths exist — path hygiene
- `CG3755_1_superselection_signature` pass=`False`: parent K_global signature sourced — contract exists but parent action has not signed it
- `CG3755_2_bianchi_lemma` pass=`True`: Bianchi arbitrary-source lemma written — conditional theorem recorded
- `CG3755_3_same_frame_conservation` pass=`False`: same-frame separate conservation signed — still conditional
- `CG3755_4_exchange_zero` pass=`False`: kappa exchange owners zero/mapped — delta_kappa_source remains live
- `CG3755_5_derivative_silence` pass=`False`: all local derivatives of G_eff vanish by proof — requires CG3755_1 or 3+4
- `CG3755_6_residual_vector` pass=`True`: coupling residual vector emitted — Gdot/WEP/R10/radial/frame/gamma/beta rows
- `CG3755_7_newton_claim` pass=`False`: Newton source calibration claim allowed — constant coupling and mu_extra still open
- `CG3755_8_local_gr_claim` pass=`False`: local GR/PPN claim allowed — second-order and full residual vector still open

## Decisions
- `DEC3755_0_theorem_status` `BIANCHI_LEMMA_DERIVED_PARENT_SUPERSELECTION_UNSIGNED`: 3755 derives the conditional Bianchi route to nabla kappa=0, but parent K_global superselection is not signed by the corpus.
- `DEC3755_1_residual_status` `COUPLING_RESIDUAL_VECTOR_EMITTED`: Failed kappa premises now activate Gdot, WEP/source charge, R10 alpha(lambda), radial hair, frame, gamma, and beta rows.
- `DEC3755_2_best_next` `NO_FLUX_EXCHANGE_OR_EXECUTABLE_RUNNER`: The next highest-leverage target is either proving q_exchange/Phi_side vanish or building the residual runner that scores the emitted rows.
- `DEC3755_3_G_policy` `DO_NOT_CLAIM_NUMERICAL_G`: Even if kappa is derivative-silent, absolute G remains a calibration unless parent normalization predicts it.

## Next Target
- `3756-Y5-R2FR-no-flux-projected-exchange-or-coupling-runner.md`: prove Phi_side=0 and Pi_M q_exchange=0 for the source-charge Ward balance, or create a dry-run coupling residual runner over the 3755 Gdot/WEP/R10/radial/frame/gamma/beta rows

## Source Register
- `SRC3755_0_3754_next` exists=`True`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3754_NEXT_TARGET.csv`
- `SRC3755_1_3754_poisson` exists=`True`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3754_POISSON_CALIBRATION_ROWS.csv`
- `SRC3755_2_3754_residuals` exists=`True`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3754_COUPLING_RESIDUAL_ROWS.csv`
- `SRC3755_3_3754_gates` exists=`True`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3754_CLAIM_GATES.csv`
- `SRC3755_4_global_contract` exists=`True`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_global_coupling_superselection_CONTRACT.csv`
- `SRC3755_5_constant_gm_attempt` exists=`True`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_CONSTANT_GM_ZERO_THEOREM_ATTEMPT.csv`
- `SRC3755_6_constant_gm_bounds` exists=`True`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_CONSTANT_GM_RESIDUAL_BOUND_MATRIX.csv`
- `SRC3755_7_delta_kappa` exists=`True`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_delta_kappa_source_exchange_residual.csv`
- `SRC3755_8_pg_map` exists=`True`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_PG_calibration_residual_MAP.csv`
- `SRC3755_9_newton_bounds` exists=`True`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3530_NEWTON_PPN_BOUND_ROWS.csv`
