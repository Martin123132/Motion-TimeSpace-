# 3640 Y5 R2FR parent source-normalization Ward identity or beta common bound fill

**Status:** 3640 derives the parent Ward/source-normalization form for beta_common and splits the residual into beta_q, beta_boundary, beta_source, beta_projection, and beta_calibration. The parent-zero theorem is still unsigned, but the live branch now has explicit inverted bound formulas for R10, PPN, Gdot/clock, radial/orbital, source-WEP null guard, and clock common-mode channels.

**Claim ceiling:** no local-GR/Newton, PPN, R10, Gdot, clock, or source-normalization pass is allowed from 3640.

## Actual derivation

Vary the parent action along the normalized common source direction `X_N`. On shell, the bulk Euler terms drop out, leaving a boundary/source/readout/calibration Ward charge. Therefore the exact local source coupling is not a single mystery number but

`beta_common = X_N ln mu_obs_common = beta_q + beta_boundary + beta_source + beta_projection + beta_calibration`.

If `X_N` is a genuine parent gauge/vertical generator, `mu_obs_common` descends through `q`, and the boundary, source current, projector, and calibration charge are silent, then the Ward identity gives `beta_common=0`. That would be the clean local-GR/Newton route: calibrated source strength is a quotient/gauge charge.

## Why it is not claimed yet

The corpus signs the algebraic form of the route but not the parent zero of all five residual pieces. So `beta_common=0` remains unclaimed. No WEP result can close it, because common-mode coupling lies in the WEP null direction.

## Ward derivation rows

- `W3640_0_parent_variation`: DERIVED_VARIATION_FORM — delta_X S_parent = integral(E_Phi delta_X Phi + E_psi delta_X psi) + integral_boundary Theta(Phi,delta_X Phi) + delta_X S_source + delta_X S_counterterm
- `W3640_1_noether_charge`: CONDITIONAL_WARD_ZERO — delta_X Q_mu = delta_X Q_boundary + delta_X Q_source + delta_X Q_projection + delta_X Q_calibration
- `W3640_2_beta_common_identity`: EXACT_RESIDUAL_SPLIT — beta_common = X_N ln mu_obs_common = beta_q + beta_boundary + beta_source + beta_projection + beta_calibration
- `W3640_3_newton_gr_reduction_gate`: LOCAL_GR_NEWTON_GATE_SHARPENED — mu_obs(r,t,A) = constant_mu + O(beta_common residuals); local GR/Newton source limit requires d_t mu_obs = d_r mu_obs = Delta_A mu_obs = alpha_common(lambda) = PPN_common = 0 or below bounds
- `W3640_4_verdict`: WARD_ZERO_UNSIGNED_BOUND_INVERSION_REQUIRED — current evidence signs the algebraic Ward form, not the parent zero of all residual pieces

## Residual pieces

- `beta_q`: X_N ln mu_bar(q(Phi)) | zero rule: zero if mu_obs_common=mu_bar(q(Phi)) and Dq(X_N)=0
- `beta_boundary`: X_N ln Q_boundary | zero rule: zero if boundary charge is invariant under X_N
- `beta_source`: X_N ln Q_source | zero rule: zero if active source current has no X_N representative dependence
- `beta_projection`: X_N ln Q_projection | zero rule: zero if local-to-observable projector commutes with quotient map
- `beta_calibration`: X_N ln Q_calibration | zero rule: zero if common scale shift is pure convention with no observable derivatives

## Bound inversions

- `R10_short_range`: `|beta_common| <= sqrt(|alpha_bound(lambda)| M_X^2/(|K_X tau_R10(lambda)|)) for beta_S=beta_T=beta_common`.
- `PPN_local_GR`: `|beta_common| <= sqrt(|Delta_PPN_limit|/|C_PPN|) when derivative terms vanish or are separately bounded`.
- `Gdot_clock`: `|beta_common| <= (|dln_mu_dt|_limit + |explicit_t residuals|)/|Xdot_N|`.
- `orbital_radial`: `|beta_common| <= (|partial_r ln mu|_limit + |explicit_r residuals|)/|partial_r X_N|`.
- `source_WEP_null_guard`: `no beta_common bound follows from differential eta alone`.
- `clock_common_mode`: `|beta_common| <= (|clock_common_limit| + non_mu_terms)/|S_mu Xdot_N|`.

## Claim gates

- `G3640_0_no_axiom`: ENFORCED — beta_common=0 may not be asserted as a plateau/closure axiom
- `G3640_1_termwise_or_identity`: ENFORCED — beta_q + beta_boundary + beta_source + beta_projection + beta_calibration cannot be cancelled by tuning
- `G3640_2_local_gr_newton`: ACTIVE — local GR/Newton source recovery requires source-normalization silence, not only WEP silence

## Next target

`3641-Y5-R2FR-beta-bound-input-prioritizer-and-first-numeric-fill.md` via `scripts/Y5_R2FR_3641_beta_bound_input_prioritizer_and_first_numeric_fill.py`.

## Sources

- `next_3639`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3639_NEXT_TARGET.csv` exists=True needle_found=True
- `proof_3639`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3639_COMMON_BETA_ZERO_PROOF_AUDIT.csv` exists=True needle_found=True
- `identity_3639`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3639_COMMON_BETA_IDENTITY.csv` exists=True needle_found=True
- `observables_3639`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3639_COMMON_BETA_OBSERVABLE_ROWS.csv` exists=True needle_found=True
- `source_runner_3639`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3639_SOURCE_NORMALIZATION_RUNNER_ROWS.csv` exists=True needle_found=True
- `constant_gm_gate`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_CONSTANT_GM_DERIVATIVE_HAIR_GATE.csv` exists=True needle_found=True
- `global_superselection`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_global_coupling_superselection_CONTRACT.csv` exists=True needle_found=True
- `species_contract`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_no_species_source_charge_CONTRACT.csv` exists=True needle_found=True
- `frame_marker_1028`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1028-Y5-R10-frame-marker-coupling-bound-input-pack-or-no-marker-theorem.md` exists=True needle_found=True
