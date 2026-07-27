# 3992 - Parent Source-Weight Projection Or WEP Tau Denominator

Timestamp: `2026-07-01T18:16:43+00:00`

## Result

This checkpoint attacks the WEP denominator rather than relabelling it missing.

Two things now separate cleanly:

1. the readout-normalized effective WEP contrast; and
2. the raw MTS parent source-weight coefficient.

## Exact Effective Bound

For `a_A=g_N(1+epsilon_A)` and `a_B=g_N(1+epsilon_B)`,

`eta_AB = 2(epsilon_A-epsilon_B)/(2+epsilon_A+epsilon_B)`.

Defining `Delta_w_eff_TiPt` as the source component already in the MICROSCOPE Eotvos readout convention gives

`|Delta_w_eff_TiPt| <= 2.700000000000e-15`.

This is a real effective-observable bound. It is not a raw MTS coupling claim.

## Numeric DD Proxy Denominator

Using the existing DD proxy Earth/source vector and MICROSCOPE material rows:

`dot(Q_Earth_DD, DeltaQ_TA6V_minus_PtRh10) = -2.211577647525e-04`.

With `0.98 <= tau_readout_X <= 1.02`, this gives `|tau_DD_proxy| >= 2.167346094575e-04`.

If, and only if, a future parent map proves `K_parent_to_DD=1` in this compressed channel, the proxy coefficient smoke bound would be `|C_DD_proxy| <= 1.245763197100e-11`.

That last line is deliberately nonclaim: the parent-to-DD/source-response map is the live missing object.

## Evaluator Results

- `CASE3992_0_effective_contrast_bound`: status `REAL_EFFECTIVE_CONTRAST_BOUND_NONCLAIM`, tau `1.000000000000e+00`, coeff_bound `2.700000000000e-15`, claim=False
- `CASE3992_1_DD_proxy_denominator`: status `NUMERIC_PROXY_ONLY_PARENT_MAP_MISSING`, tau `2.167346094575e-04`, coeff_bound `1.245763197100e-11`, claim=False
- `CASE3992_2_raw_MTS_projection_missing`: status `MISSING_PARENT_BASIS_AND_OFFICIAL_PROJECTION`, tau `MISSING`, coeff_bound `MISSING`, claim=False
- `CASE3992_3_no_Hom_zero_conditional`: status `CONDITIONAL_NO_HOM_ZERO_PARENT_UNSIGNED`, tau `not_required_if_Delta_w_zero`, coeff_bound `0`, claim=False

## Current Closure Gate

The WEP side is no longer just missing. It now has an exact effective observable bound and a numeric DD proxy denominator. The remaining hard gate is the parent map from MTS source-weight residuals into that response basis, or the no-Hom theorem-zero.

## Source Register

`15/15` source needles found.
- `SRC3992_00_3991_next`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3991_NEXT_TARGET.csv` needle `NEXT3991_0` found=True
- `SRC3992_01_3991_anchor`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3991_REAL_SOURCE_WEIGHT_BOUND_ANCHORS.csv` needle `ANCH3991_0_WEP_MICROSCOPE_product` found=True
- `SRC3992_02_3463_tau_derivation`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3463_WEP_TAU_PROJECTION_DERIVATION.csv` needle `TAU3463_1_direct_linear_limit` found=True
- `SRC3992_03_3366_packet`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3366_TAU_WEP_EXECUTION_PACKET.csv` needle `TAU3366_0_executable_formula` found=True
- `SRC3992_04_3262_factor`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3262_TAU_WEP_FACTORIZATION.csv` needle `TAU3262_1_readout_X` found=True
- `SRC3992_05_3262_readout_lines`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3262_MICROSCOPE_READOUT_FACTOR_EVIDENCE.csv` needle `MRF3262_1_x_readout` found=True
- `SRC3992_06_3263_channel`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3263_MICROSCOPE_EP_CHANNEL_EVIDENCE.csv` needle `MCH3263_5_eta_identification` found=True
- `SRC3992_07_3260_bound_inputs`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3260_MICROSCOPE_DD_BOUND_INPUTS.csv` needle `BIN3260_4_eta_reported_level` found=True
- `SRC3992_08_3473_material`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3473_FULL_DD_MATERIAL_ROWS.csv` needle `MAT3473_MICROSCOPE_TA6V` found=True
- `SRC3992_09_3482_earth`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3482_EARTH_FULL_DD_SOURCE_VECTOR_NONCLAIM.csv` needle `EARTH3482_0_bulk_full_DD_four_charge` found=True
- `SRC3992_10_3481_normalizer`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3481_WEP_SHARED_EARTH_NORMALIZER_ROWS_NONCLAIM.csv` needle `WEN3481_0_MATRIX3473_0_MICROSCOPE_TA6V_minus_PtRh10` found=True
- `SRC3992_11_3544_source_leg`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3544_MICROSCOPE_SOURCE_LEG_INTAKE.csv` needle `SL3544_0_compressed_D_definition` found=True
- `SRC3992_12_3364_owner`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3364_WEP_PROJECTION_OWNER_AUDIT.csv` needle `WEP3364_4_tau_product` found=True
- `SRC3992_13_1420_checklist`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1420_WEP_SOURCE_PROJECTION_ACQUISITION_CHECKLIST.csv` needle `WAC1420_0_source_worldtube_profile` found=True
- `SRC3992_14_3991_results`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3991_PPN_BETA_SOURCE_EVALUATOR_RESULTS.csv` needle `CASE3991_1_real_WEP_anchor_projection_blocked` found=True

## Next Target

`3993-Y5-R2FR-DD-proxy-to-parent-basis-map-or-source-weight-zero.md`

Derive the parent-to-DD/source-response map, or prove the no-Hom source-weight zero.
