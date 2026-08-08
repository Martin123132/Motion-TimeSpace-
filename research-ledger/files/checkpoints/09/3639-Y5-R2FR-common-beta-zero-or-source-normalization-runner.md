# 3639 Y5 R2FR common beta zero or source normalization runner

**Status:** 3639 tried the common-beta zero proof. The exact quotient route and pure-calibration route are now written, but neither is parent-signed, so beta_common remains live. The useful advance is that beta_common is no longer a vague missing coupling: it is mapped into R10, PPN, Gdot/clock, radial/orbital, and source-normalization equations.

**Claim ceiling:** no local-GR/Newton, PPN, R10, Gdot, clock, or source-normalization pass is allowed from 3639.

## Main result

The useful theorem is conditional and exact: if `mu_obs_common = mu_bar(q(Phi))` and `X_N in ker(Dq)`, then `beta_common = X_N[ln mu_obs_common] = 0`. A second exact route exists if a parent scale/source Ward identity makes `delta ln G_eff + delta ln M_eff + delta ln(1+epsilon_mu) = 0` as a symmetry, not a tune.

The current parent corpus does not sign either route. Therefore `beta_common` stays live, but it has been moved out of the fog: it now has explicit R10, PPN, Gdot/clock, radial/orbital, and source-normalization maps.

## Exact identity

- `beta_common`: beta_common = X_N[ln mu_obs_common] = X_N[ln G_eff] + X_N[ln M_eff] + X_N[ln(1+epsilon_mu)] [EXACT_DECOMPOSITION_NO_ZERO_CLAIM]
- `dot_mu_over_mu`: d ln mu_obs_common/dt = beta_common * dX_N/dt + explicit_t[ln G_eff M_eff(1+epsilon_mu)] [REQUIRES_XDOT_OR_PARENT_ZERO]
- `partial_r_ln_mu`: partial_r ln mu_obs_common = beta_common * partial_r X_N + explicit_r[ln G_eff M_eff(1+epsilon_mu)] [REQUIRES_PROFILE_OR_PARENT_ZERO]
- `eta_source_AB`: eta_source_AB sees Delta beta_AB, not beta_common; beta_common lies in the WEP null direction. [WEP_CANNOT_CLOSE_COMMON_MODE]

## Proof audit

- `CB3639_0_definition`: DERIVED_IDENTITY — beta_common := X_N[ln mu_obs] for the species-blind part of mu_obs.
- `CB3639_1_quotient_zero_route`: CONDITIONAL_ZERO_NOT_PARENT_SIGNED — If mu_obs = mu_bar(q(Phi)) and X_N in ker(Dq), then beta_common = X_N[ln mu_bar(q(Phi))] = 0.
- `CB3639_2_unit_gauge_route`: CONDITIONAL_ZERO_NOT_PARENT_SIGNED — A common source scaling is unobservable only if it is pure calibration gauge.
- `CB3639_3_scalar_tensor_guard`: COMMON_MODE_NOT_WEP_ERASED — Universal coupling can pass WEP but still fail PPN/R10/Gdot.
- `CB3639_4_verdict`: ZERO_PROOF_UNSIGNED_OBSERVABLE_RUNNER_FILLED — The common-beta zero proof cannot be claimed from the current parent corpus.

## Observable maps

- `R10_short_range`: `alpha_common(lambda)` via `alpha_common(lambda) = K_X * beta_common_source * beta_common_test * tau_R10(lambda) / M_X^2`.
- `PPN_local_GR`: `PPN_residual_vector_common` via `Delta_PPN_common ~ (gamma-1, beta_PPN-1, alpha_i, zeta_i) sourced at leading order by beta_common^2 and derivatives of beta_common`.
- `Gdot_clock`: `dln_mu_obs_dt` via `dln_mu_obs_dt = beta_common * Xdot_N + explicit_t residuals`.
- `orbital_radial`: `radial_source_hair` via `a_r = -mu_obs(r)/r^2 with partial_r ln mu_obs = beta_common partial_r X_N + explicit_r residuals`.
- `source_normalization`: `calibration_null_or_physical_beta` via `beta_common is gauge only if delta ln mu_obs_common is a parent-owned calibration transformation with zero derivatives in observables`.

## Source-normalization runner

- `SNR3639_0_calibrated_mu`: ACTIVE_FORK — mu_obs_common := G_eff M_eff(1+epsilon_mu)
- `SNR3639_1_no_cancellation`: NO_TUNED_CANCELLATION_ALLOWED — X_N ln G_eff + X_N ln M_eff + X_N ln(1+epsilon_mu) = 0
- `SNR3639_2_common_wEP_guard`: WEP_NOT_SUFFICIENT — Delta beta_AB = 0 while beta_common != 0 is allowed

## Decision

- `DEC3639_0_zero_not_claimed`: ZERO_PROOF_UNSIGNED — Do not claim beta_common=0 from the current corpus.
- `DEC3639_1_runner_filled`: OBSERVABLE_RUNNER_FILLED — Keep beta_common as a source-normalization residual with explicit arena equations.
- `DEC3639_2_next`: WARD_IDENTITY_NEXT — Next target is the parent source-normalization Ward identity.

## Next target

`3640-Y5-R2FR-parent-source-normalization-ward-identity-or-beta-common-bound-fill.md` via `scripts/Y5_R2FR_3640_parent_source_normalization_ward_identity_or_beta_common_bound_fill.py`.

## Sources

- `handoff_3638`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3638_NEXT_TARGET.csv` exists=True needle_found=True
- `component_pack_3638`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3638_BETAX_COMPONENT_PACK.csv` exists=True needle_found=True
- `eta_update_3638`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3638_ETA_SOURCE_AB_COMPONENT_UPDATE.csv` exists=True needle_found=True
- `constant_gm_gate`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_CONSTANT_GM_DERIVATIVE_HAIR_GATE.csv` exists=True needle_found=True
- `constant_gm_species`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_CONSTANT_GM_DERIVATIVE_HAIR_GATE.csv` exists=True needle_found=True
- `global_superselection`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_global_coupling_superselection_CONTRACT.csv` exists=True needle_found=True
- `no_species_contract`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_no_species_source_charge_CONTRACT.csv` exists=True needle_found=True
- `source_bound_1027`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1027-Y5-R10-qbarXT-source-zero-or-bounded-coupling-row.md` exists=True needle_found=True
- `frame_marker_1028`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1028-Y5-R10-frame-marker-coupling-bound-input-pack-or-no-marker-theorem.md` exists=True needle_found=True
