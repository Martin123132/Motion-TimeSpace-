# 3646 Y5 R2FR matter coupling descent or first beta source row

**Status:** 3646 proves the matter-coupling zero route as an exact conditional chain-rule theorem, rejects current claim status because parent signatures are missing, and creates first R2FR beta/source rows with absolute no-cancellation guards.

**Claim ceiling:** no coupling-zero, beta-zero, local-GR/Newton, R10, PPN, clock, orbital, or WEP pass is claimed.

## Theorem attempt

The clean route is exact but conditional:

`S_matter=Sbar_m[Obs(q(Phi)),Psi,theta_A]`, `v_X in ker(Dq)`, `DObs(Dq[v_X])=0`, and `Lie_vX theta_A=0` imply `J_X^matter=0` and `beta_i=0`, provided there is no hidden conformal/disformal matter frame or material marker depending on `X_N`.

This is useful because it says exactly what must be derived; it is not a closure axiom.

## Theorem rows
- `MDT3646_0_statement`: EXACT_CHAIN_RULE_THEOREM_PREMISES_UNSIGNED — If every hypothesis holds in the same parent branch, delta_vX S_matter=0, J_X^matter=0, beta_i=0, and qbar_XT=0.
- `MDT3646_1_metric_frame_part`: MATH_PASS_NEEDS_PARENT_OBS_SIGNATURE — The Hilbert stress channel gives no J_X^matter contribution from geometry under quotient descent.
- `MDT3646_2_constants_marker_part`: COUNTERMODEL_CLASS_IDENTIFIED — If alpha_EM(X), masses, clock ratios, material labels, or binding fractions carry X_N dependence, beta_i is nonzero even with quotient geometry.
- `MDT3646_3_shadow_frame_part`: LIVE_COUNTERMODEL_OR_BOUND_ROW — Universal coupling is not automatically safe; it tends to enter finite exchange as beta_s beta_t or c_g^2.
- `MDT3646_4_fallback_beta_definition`: BETA_FALLBACK_DERIVED — |beta_i| is bounded by an absolute component envelope; no cancellation between unknown components is credited.

## Clause audit
- `MDC3646_0_q_kernel`: `v_X in ker(Dq)` — MISSING_PARENT_Q_KERNEL_FOR_ACTUAL_XN
- `MDC3646_1_obs_geometry`: `Obs_g/Obs_e factor through q` — MISSING_OBS_GEOMETRY_PARENT_SIGNATURE
- `MDC3646_2_matter_functor`: `S_matter=Sbar_m[Obs(q(Phi)),Psi,theta]` — MISSING_PARENT_MATTER_FUNCTOR
- `MDC3646_3_no_shadow_frame`: `no A_g(X), B_dis(X), or hidden matter frame` — MISSING_NO_SHADOW_FRAME_THEOREM_OR_COEFFICIENTS
- `MDC3646_4_no_marker_constants`: `Lie_vX theta_A=0 for masses, alpha_EM, clocks, materials` — MISSING_NO_MARKER_THEOREM_OR_COEFFICIENTS
- `MDC3646_5_hidden_source_silence`: `no hidden/source/domain support in ordinary body action` — MISSING_HIDDEN_SOURCE_SILENCE
- `MDC3646_6_projector_readout`: `calibration/readout fixed before X variation` — MISSING_PROJECTOR_READOUT_SIGNATURE
- `MDC3646_7_same_branch`: `all clauses close in one parent branch` — MISSING_SINGLE_PARENT_BRANCH_CERTIFICATE

## First beta/source rows
- `BETA3646_0_theorem_zero`: `beta_i_zero` — MISSING_PARENT_THEOREM_CERTIFICATE
- `BETA3646_1_geom_shadow`: `beta_geom_shadow` — MISSING_FRAME_LEAK_ZERO_OR_NUMERIC_BOUND
- `BETA3646_2_constants_marker`: `beta_marker` — MISSING_NO_MARKER_THEOREM_OR_NUMERIC_BOUNDS
- `BETA3646_3_binding_material`: `beta_binding` — MISSING_MATERIAL_SENSITIVITY_ROWS
- `BETA3646_4_nonH_source`: `beta_nonH` — MISSING_HIDDEN_SOURCE_ZERO_OR_NUMERIC_BOUND
- `BETA3646_5_projector_readout`: `beta_projector` — MISSING_PROJECTOR_READOUT_BOUND
- `BETA3646_6_abs_total`: `beta_s_abs;beta_t_abs` — SCHEMA_READY_VALUES_MISSING
- `BETA3646_7_product_guard`: `abs_beta_product` — CLAIM_BLOCKED

## Material schema
- `body_id`: REQUIRED — source/test body or material row id
- `role`: REQUIRED — which beta leg the row fills
- `material_or_body_class`: REQUIRED_MISSING_VALUES — material/body composition class; no generic beta without material/readout declaration
- `S_A;S_alpha;S_clock;f_binding`: REQUIRED_MISSING_VALUES — composition/constant sensitivity vector
- `c_g;b_dis;b_A;b_alpha;b_clock;q_nonH`: REQUIRED_MISSING_VALUES — MTS-side coupling coefficients or theorem-zero certificates
- `beta_geom_shadow;beta_marker;beta_binding;beta_nonH;beta_projector`: REQUIRED_MISSING_VALUES — component beta values/bounds
- `source_paths`: REQUIRED_FOR_ANY_CLAIM — source for every sensitivity, coefficient, and theorem-zero certificate
- `absolute_no_cancellation`: REQUIRED_TRUE — components add by absolute envelope, not cancellation

## Decisions
- `DEC3646_0_theorem_attempt`: THEOREM_SHAPE_EXACT — The matter-coupling zero theorem is mathematically clean by chain rule.
- `DEC3646_1_current_verdict`: PARENT_SIGNATURE_UNSIGNED — It is not a current MTS claim because observed geometry, matter functor, no-shadow frame, no-marker constants, hidden source silence, and projector readout are not signed in one parent branch.
- `DEC3646_2_fallback`: BETA_ROWS_CREATED_NOT_SCORE_READY — First beta/source rows are created as nonclaim rows; they make coupling testable instead of hand-waved.
- `DEC3646_3_best_next`: OBS_FRAME_NO_SHADOW_OR_COEFFICIENTS_NEXT — Attack no-shadow observed frame first, because a universal A_g(X) or disformal matter frame can mimic WEP safety while still sourcing finite exchange.

## Next target

`3647-Y5-R2FR-observed-frame-no-shadow-theorem-or-cg-bdis-coefficient-row.md` via `scripts/Y5_R2FR_3647_observed_frame_no_shadow_theorem_or_cg_bdis_coefficient_row.py`.

## Sources
- `next_3645`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3645_NEXT_TARGET.csv` exists=True needle_found=True
- `jx_3645`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3645_JX_VARIATION_DERIVATION.csv` exists=True needle_found=True
- `obs_637`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_637_OBS_FUNCTOR_DERIVATION.csv` exists=True needle_found=True
- `qmap_637`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_637_QUOTIENT_MAP_DERIVATION.csv` exists=True needle_found=True
- `qvx_1023`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1023-Y5-R10-q-vX-action-descent-certificate-or-scalar-nohair-demotion.md` exists=True needle_found=True
- `qbar_1027`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1027-Y5-R10-qbarXT-source-zero-or-bounded-coupling-row.md` exists=True needle_found=True
- `matter_pullback_1044`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1044-Y5-R10-matter-pullback-JX-zero-or-qbarXT-bound-row.md` exists=True needle_found=True
- `matter_functor_1045`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1045-Y5-R10-parent-matter-functor-descent-signature-or-qbar-component-fill.md` exists=True needle_found=True
- `no_shadow_1046`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1046-Y5-R10-no-shadow-frame-constant-marker-theorem-or-qbar-marker-coefficients.md` exists=True needle_found=True
- `beta_1036`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1036_BETA_SOURCE_TEST_DERIVATION.csv` exists=True needle_found=True
- `bounded_beta_1037`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1037_BOUNDED_BETA_SOURCE_TEST_TEMPLATE.csv` exists=True needle_found=True
