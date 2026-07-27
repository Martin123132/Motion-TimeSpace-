# 3762 — Range/Radial/Frame Residual Lock Or R10/PPN Bound

## Status

`RANGE_RADIAL_FRAME_ZERO_OR_BOUND_INTERFACES_DERIVED`.

3762 derives zero-or-bound interfaces for alpha(lambda), radial source hair, and frame/source split. The local-GR route now has explicit residual handling for Gdot, WEP, EM stress, gamma, beta, range, radial, and frame rows.

## Derivation

This checkpoint closes the last vague local-GR leak channels into explicit interfaces. A finite-range force, radial source hair, or hidden frame split would break the clean local GR route. Each now has a zero theorem route and a fallback residual formula.

The clean branch is: no extra finite-range mediator, no exterior radial hair, and one observed metric/coframe/time generator. The fallback branch is: executable `alpha(lambda)` curve, radial profile, and frame residual decomposition.

## Range/Radial/Frame Locks
- `RRF3762_0_no_range_mediator` `EXACT_CONDITIONAL_ZERO_THEOREM`: If the local branch has no unscreened propagating scalar/vector/tensor mediator outside the EH metric/coframe and same total source, then alpha(lambda)=0 for all finite lambda.
- `RRF3762_1_alpha_curve_fallback` `EXECUTABLE_BOUND_INTERFACE_REQUIRED`: If any finite-range mediator remains, R10 scoring requires table rows (lambda, alpha_predicted) compared against alpha_bound(lambda).
- `RRF3762_2_no_radial_hair` `EXACT_CONDITIONAL_ZERO_THEOREM`: If kappa_eff, source charge, Poisson calibration, and extra-field amplitudes are constant outside a compact local source, then partial_r ln mu_obs=0.
- `RRF3762_3_radial_profile_fallback` `PROFILE_BOUND_INTERFACE_REQUIRED`: If radial hair remains, score partial_r ln mu_obs by an explicit profile: partial_r ln mu_obs = partial_r ln kappa_eff + partial_r ln C_M + partial_r ln Z_Poisson + partial_r ln Z_extra.
- `RRF3762_4_single_observed_frame` `EXACT_CONDITIONAL_ZERO_THEOREM`: If matter, light, clocks, EM, and source readout all descend to one observed metric/coframe and one local time generator, then delta_frame_source=0.
- `RRF3762_5_frame_residual_fallback` `FRAME_BOUND_INTERFACE_REQUIRED`: If frame descent is unsigned, delta_frame_source must be decomposed into clock drift, light-cone split, source-frame split, and preferred-frame PPN residuals.

## Residual Budgets
- `RRF_BUD3762_0_alpha_lambda` `BOUND_CURVE_REQUIRED_NUMERIC_COMPONENTS_MISSING`: `alpha(lambda)` formula `sum_X |A_X|^2 |Q_X|^2 exp(-r/lambda_X) projected into alpha_predicted(lambda)` target `alpha_bound(lambda) range-dependent`
- `RRF_BUD3762_1_radial_hair` `PROFILE_BOUND_REQUIRED_NUMERIC_COMPONENTS_MISSING`: `partial_r_ln_mu_obs` formula `|partial_r ln kappa_eff| + |partial_r ln C_M| + |partial_r ln Z_Poisson| + |partial_r ln Z_extra|` target `zero_or_mapped_bound inverse_length_or_dimensionless_envelope`
- `RRF_BUD3762_2_frame_split` `FRAME_BOUND_REQUIRED_NUMERIC_COMPONENTS_MISSING`: `delta_frame_source` formula `|delta_clock_frame| + |delta_light_cone| + |delta_source_frame| + |delta_preferred_frame|` target `zero_or_row_locks dimensionless`

## Runner Patch
- `RUN3762_KRV3755_0_Gdot` `CONDITIONAL_ZERO_OR_RESIDUAL_BOUND_READY`: |d_t ln kappa_*| + |R_G| + |R_M| + |d_t ln Z_Poisson| + |d_t ln Z_frame| <= 9.6e-15 yr^-1; zero if all components vanish
- `RUN3762_KRV3755_1_species_source` `CONDITIONAL_ZERO_OR_EM_WEP_RESIDUAL_BOUND_READY`: |Delta_AB ln kappa_eff| + |Delta_AB ln Xi| + |Delta_AB ln Z_frame| + |Delta_AB exchange| + eta_EM_AB <= 2.8e-15; eta_EM_AB=0 if EM stress is same-source
- `RUN3762_KRV3755_2_range` `CONDITIONAL_ZERO_OR_R10_CURVE_BOUND_REQUIRED`: alpha(lambda)=0 if no unscreened finite-range mediator/hair is parent-signed; otherwise require executable alpha_predicted(lambda) curve against alpha_bound(lambda)
- `RUN3762_KRV3755_3_radial` `CONDITIONAL_ZERO_OR_RADIAL_PROFILE_BOUND_REQUIRED`: partial_r ln mu_obs=0 if no radial hair/source drift is parent-signed; otherwise |partial_r ln kappa_eff|+|partial_r ln C_M|+|partial_r ln Z_Poisson|+|partial_r ln Z_extra| must be mapped to bounds
- `RUN3762_KRV3755_4_delta_kappa_exchange` `BLOCKED_ZERO_OR_MAPPED_BOUND_REQUIRED`: 
- `RUN3762_KRV3755_5_frame` `CONDITIONAL_ZERO_OR_FRAME_BOUND_REQUIRED`: delta_frame_source=0 if matter/light/clocks/EM/source use one observed metric/coframe and time generator; otherwise decompose clock/light/source/preferred-frame residuals
- `RUN3762_KRV3755_6_gamma` `CONDITIONAL_PASS_UNSIGNED_LOCAL_EH_TOTAL_SOURCE_PREMISES`: gamma-1=0 if local EH + same observed metric + same total source are parent-signed; otherwise |Delta_EH_linear|+|Delta_source_projection|+|Delta_frame|+|delta_gamma_EM|+|delta_gamma_extra_field| <= 2.3e-05
- `RUN3762_KRV3755_7_beta` `CONDITIONAL_PASS_UNSIGNED_SECOND_ORDER_EH_TOTAL_SOURCE_PREMISES`: beta-1=0 if second-order EH self-coupling + same total source are parent-signed; otherwise |Delta_EH_second_order|+|Delta_source_nonlinear|+|Delta_frame2|+|delta_beta_EM|+|delta_beta_extra_field| <= 7.8e-05

## Local-GR Claim Matrix
- `CM3762_0_Gdot` `dln_Geff_dt`: conditionally scoreable from 3758 — blocker: parent kappa/no-flux signatures unsigned
- `CM3762_1_WEP` `eta_source_AB`: conditionally scoreable from 3759 — blocker: same-action/source-universality signatures unsigned
- `CM3762_2_EM` `eta_EM_AB/delta_gamma_EM/delta_beta_EM`: same-source or residual interface from 3760 — blocker: MTS EM descent unsigned
- `CM3762_3_gamma` `gamma_minus_1`: conditionally scoreable from 3761 — blocker: local EH/same-frame signatures unsigned
- `CM3762_4_beta` `beta_minus_1`: conditionally scoreable from 3761 — blocker: second-order EH/source signatures unsigned
- `CM3762_5_range` `alpha(lambda)`: zero-or-curve interface from 3762 — blocker: no-range mediator theorem or curve missing
- `CM3762_6_radial` `partial_r_ln_mu_obs`: zero-or-profile interface from 3762 — blocker: no-radial-hair theorem or profile missing
- `CM3762_7_frame` `delta_frame_source`: zero-or-frame-residual interface from 3762 — blocker: single observed frame theorem unsigned

## Claim Gates
- `CG3762_0_sources` pass=`True`: all 3762 source paths exist — path hygiene
- `CG3762_1_range_zero_or_curve` pass=`True`: range row has zero theorem or curve fallback — alpha(lambda) no longer vague
- `CG3762_2_radial_zero_or_profile` pass=`True`: radial row has no-hair or profile fallback — radial hair no longer vague
- `CG3762_3_frame_zero_or_bound` pass=`True`: frame row has single-frame or bound fallback — frame split no longer vague
- `CG3762_4_range_claim` pass=`False`: R10/range claim allowed — no-range parent theorem or curve data missing
- `CG3762_5_radial_claim` pass=`False`: radial/orbital source profile claim allowed — no-hair theorem or numeric profile missing
- `CG3762_6_frame_claim` pass=`False`: same-frame/preferred-frame claim allowed — single observed frame theorem or numeric rows missing
- `CG3762_7_local_gr_claim` pass=`False`: local GR claim allowed — parent signatures remain unsigned

## Decisions
- `DEC3762_0`: The local-GR residual stack is now fully routed: every open coupling/local row has either a conditional zero theorem or an explicit bound/profile fallback. Action: stop circling missingness; next select parent signatures to adopt or gather numeric residual components.
- `DEC3762_1`: The R10 range row is the least claim-ready because alpha(lambda) still needs a curve unless a no-range mediator theorem is parent-signed. Action: keep R10 nonclaim until no-range theorem or executable curve exists.
- `DEC3762_2`: The frame row is conceptually central: one observed metric/coframe/time generator simultaneously helps WEP, clocks, gamma/beta, and preferred-frame constraints. Action: make the single-observed-frame parent signature the next derivation target.

## Next Target
- `3763-Y5-R2FR-parent-signature-selection-single-frame-no-range-local-EH.md`: turn the zero-or-bound interfaces into a minimal parent-action signature set: local EH, same total source, single observed frame, global kappa, no finite-range mediator, and compact no-radial-hair

## Validation
- `sources_exist` `PASS`: all 3762 source paths exist
- `generated_csvs_parse` `PASS`: all generated 3762 csvs parse
- `range_lock` `PASS`: range zero-or-curve lock emitted
- `radial_lock` `PASS`: radial zero-or-profile lock emitted
- `frame_lock` `PASS`: frame zero-or-bound lock emitted
- `runner_patch_nonclaim` `PASS`: patched runner remains nonclaim
- `claim_matrix_complete` `PASS`: local-GR claim matrix covers eight observables
- `local_gr_not_claimed` `PASS`: local GR remains unclaimed
- `next_target` `PASS`: 3763 target emitted
- `no_formalization_leak` `PASS`: no 3762 files written to formalization-workbench
