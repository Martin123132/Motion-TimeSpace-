# 3756 — No-Flux / Projected Exchange Or Coupling Runner

## Status

`NO_FLUX_EXCHANGE_ZERO_CONDITIONAL_COUPLING_RUNNER_EMITTED`.

This checkpoint tries the theorem route first. It does not claim the source flux vanishes: it records the exact clauses needed and emits a dry-run runner for every live coupling residual.

## No-Flux Clauses
- `NF3756_0_balance_start` `DERIVED_BALANCE`: Delta ell_M(J_H) = -Phi_side + int_C Pi_M q_exchange — source charge conservation reduces to two terms
- `NF3756_1_side_flux_definition` `DEFINITION_READY`: Phi_side := int_side J_M through the worldtube/collar side boundary — if the side moves or carries flux, M_eff drift is physical
- `NF3756_2_topological_no_side_flux` `EXACT_CONDITIONAL_THEOREM`: Phi_side=0 if J_M is a closed topological current and the side boundary is homologous with no source crossing — not signed because worldtube/no-crossing theorem is not parent-derived
- `NF3756_3_owner_divergence_no_flux` `EXACT_CONDITIONAL_BOUNDARY_TEST`: int_boundary Pi_M nabla_mu K_owner^{mu0}=int_boundary Pi_M K_owner^{i0} n_i dS — current corpus marks this fail_open
- `NF3756_4_flux_bound` `BOUND_INTERFACE_READY`: |d ln M_eff/dt| <= (|Phi_side|+int|Pi_M q_exchange|)/(|ell_M(J_H)| Delta t) — feeds Gdot/radial/orbital residual rows

## Projected Exchange Clauses
- `EX3756_0_exchange_decomposition` `DECOMPOSITION_INTERFACE`: q_exchange = q_Hilbert_nonconservation + q_boundary + q_domain + q_memory + q_range + q_connection + q_kappa + q_retained — prevents treating all exchange as zero by naming channels
- `EX3756_1_projected_exchange_condition` `EXACT_CONDITIONAL_GATE`: Pi_M q_exchange=0 iff every Pi_M q_i=0 or the nonzero terms are mapped and bounded in the residual vector — Newton source calibration needs this, not just total Ward conservation
- `EX3756_2_kappa_exchange` `LIVE_FROM_3755`: Pi_M q_kappa = Pi_M[kappa_eff^-1 T_obs^{mu nu} nabla_mu kappa_eff] — otherwise activates delta_kappa_source
- `EX3756_3_boundary_domain_exchange` `UNSIGNED`: Pi_M(q_boundary+q_domain)=0 — otherwise activates mu_extra/radial/source residuals
- `EX3756_4_memory_range_exchange` `UNSIGNED`: Pi_M(q_memory+q_range)=0 — otherwise activates R10 alpha(lambda) and source-normalization rows
- `EX3756_5_verdict` `NOT_CLAIMED`: Pi_M q_exchange=0 is not proved in the current corpus — local Newton/local GR remain blocked

## Runner Spec
- `RS3756_0_schema`: residual_id,symbol,arena,bound_value,units,prediction_status,prediction_value,score_status — minimum runner columns
- `RS3756_1_numeric_rule`: numeric bound rows score only when prediction_value is finite numeric — abs(prediction_value)<=bound_value
- `RS3756_2_curve_rule`: alpha(lambda) rows require a curve/table with lambda and alpha_predicted columns — not scoreable from scalar placeholder
- `RS3756_3_symbolic_rule`: zero_or_mapped_bound rows require a theorem-zero source or explicit mapped residual — not scoreable from prose
- `RS3756_4_claim_rule`: valid_for_claim remains false unless source path exists, units are recognized, prediction is numeric/table-backed, and bound comparison passes — anti-smuggling rule
- `RS3756_5_no_cancellation`: sum/total rows use absolute components, not tuned cancellation — no-cancellation policy

## Dry-Run Runner Rows
- `RUN3756_KRV3755_0_Gdot` `BLOCKED_THEOREM_OR_NUMERIC_PREDICTION_REQUIRED`: `dln_Geff_dt` arena `LLR/Gdot` bound `9.6e-15 yr^-1`
- `RUN3756_KRV3755_1_species_source` `BLOCKED_PREDICTION_VALUE_MISSING`: `eta_source_AB` arena `MICROSCOPE/WEP` bound `2.8e-15 dimensionless`
- `RUN3756_KRV3755_2_range` `BLOCKED_ALPHA_LAMBDA_CURVE_REQUIRED`: `alpha(lambda)` arena `R10 inverse-square` bound `alpha(lambda) range-dependent`
- `RUN3756_KRV3755_3_radial` `BLOCKED_THEOREM_OR_NUMERIC_PREDICTION_REQUIRED`: `partial_r_ln_mu_obs` arena `orbital/R10/radial source profile` bound `zero_or_mapped_bound inverse_length_or_dimensionless_envelope`
- `RUN3756_KRV3755_4_delta_kappa_exchange` `BLOCKED_ZERO_OR_MAPPED_BOUND_REQUIRED`: `delta_kappa_source` arena `PPN/R10/local exchange` bound `same-frame theorem or explicit exchange coefficient projected_force_density_or_dimensionless_normalized_residual`
- `RUN3756_KRV3755_5_frame` `BLOCKED_THEOREM_OR_NUMERIC_PREDICTION_REQUIRED`: `delta_frame_source` arena `WEP/clock/preferred-frame` bound `zero_or_row_locks dimensionless`
- `RUN3756_KRV3755_6_gamma` `BLOCKED_PREDICTION_VALUE_MISSING`: `gamma_minus_1` arena `Cassini/Shapiro` bound `2.3e-05 dimensionless`
- `RUN3756_KRV3755_7_beta` `BLOCKED_THEOREM_OR_NUMERIC_PREDICTION_REQUIRED`: `delta_beta_source` arena `PPN beta` bound `7.8e-05 dimensionless`

## Claim Gates
- `CG3756_0_sources` pass=`True`: all 3756 source paths exist — path hygiene
- `CG3756_1_balance` pass=`True`: Ward flux balance imported — Delta ell_M = -Phi_side + int Pi_M q_exchange
- `CG3756_2_side_flux_zero` pass=`False`: Phi_side=0 fully proved — conditional only; boundary flux fail_open remains
- `CG3756_3_projected_exchange_zero` pass=`False`: Pi_M q_exchange=0 fully proved — channel-by-channel exchange zero not signed
- `CG3756_4_runner` pass=`True`: coupling dry-runner rows emitted — one row per 3755 residual
- `CG3756_5_runner_claim_ready` pass=`False`: any runner row claim-ready — predictions are missing/theorem-dependent
- `CG3756_6_newton_claim` pass=`False`: Newton source calibration claim allowed — no-flux/exchange and runner inputs incomplete
- `CG3756_7_local_gr_claim` pass=`False`: local GR/PPN claim allowed — PPN/source vector remains nonclaim

## Decisions
- `DEC3756_0_no_flux` `NO_FLUX_THEOREM_CONDITIONAL_NOT_SIGNED`: Phi_side=0 follows for a fixed topological worldtube with no side crossing, but current sources still mark boundary/owner flux as fail_open.
- `DEC3756_1_exchange` `PROJECTED_EXCHANGE_ZERO_NOT_PROVED`: Pi_M q_exchange=0 requires channel-by-channel silence; kappa, boundary, domain, memory, and range channels remain live.
- `DEC3756_2_runner` `COUPLING_DRY_RUNNER_EMITTED`: The 3755 residual vector is now machine-dry-runnable and blocks claims until theorem-zero or numeric/table predictions are supplied.
- `DEC3756_3_next` `FILL_FIRST_RUNNER_ROW_OR_PROVE_NO_FLUX`: Best next move is either prove the side-flux/exchange zero clauses or fill the first scoreable Gdot/WEP/R10 residual input.

## Next Target
- `3757-Y5-R2FR-first-coupling-runner-fill-or-side-flux-zero-proof.md`: fill the first scoreable coupling runner row, prioritizing Gdot or WEP/source-charge, or prove the side-flux/no-projected-exchange clauses that zero the same rows

## Source Register
- `SRC3756_0_3755_next` exists=`True`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3755_NEXT_TARGET.csv`
- `SRC3756_1_3755_residual_vector` exists=`True`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3755_COUPLING_RESIDUAL_VECTOR.csv`
- `SRC3756_2_3755_theorems` exists=`True`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3755_KAPPA_THEOREM_ROWS.csv`
- `SRC3756_3_3755_gates` exists=`True`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3755_CLAIM_GATES.csv`
- `SRC3756_4_3754_ward_flux` exists=`True`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3754_SOURCE_WARD_FLUX_LAW_ROWS.csv`
- `SRC3756_5_ward_owner` exists=`True`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Ward_source_owner_identity_CONTRACT.csv`
- `SRC3756_6_source_ward` exists=`True`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_source_current_Ward_universality_CONTRACT.csv`
- `SRC3756_7_flux_contract` exists=`True`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_PiM_flux_closure_Ward_topological_CONTRACT.csv`
- `SRC3756_8_flux_residual_map` exists=`True`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_SOURCE_MEASURE_MEFF_FLUX_RESIDUAL_MAP.csv`
- `SRC3756_9_constant_gm_bounds` exists=`True`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_CONSTANT_GM_RESIDUAL_BOUND_MATRIX.csv`
- `SRC3756_10_delta_kappa` exists=`True`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_delta_kappa_source_exchange_residual.csv`
