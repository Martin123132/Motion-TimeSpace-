# 3991 - Source-Weight Real Bound Or PPN Beta-Source Evaluator

Timestamp: `2026-07-01T18:09:59+00:00`

## Result

This checkpoint imports a real observable bound without pretending it is already an MTS coupling bound.

The source-backed MICROSCOPE Ti/Pt row gives `|eta_TiPt| <= 2.7e-15`.

For the source-weight branch the honest statement is:

`|P_WEP_source_weight| = |Delta_w_TiPt * tau_WEP| <= eta_bound_abs`.

That is real evidence, but it is only a product anchor until the parent `tau_WEP`, material/source contrast, and readout kernel are derived or sourced.

## PPN Beta Evaluator

The evaluator now covers three branches:

- theorem-zero branch: `B_source=A_source^2` gives `delta_beta_source=0` conditionally;
- 3990 envelope branch: `delta_beta_source_abs <= |R_matter_descent| + epsilon_no_hom + epsilon_action_line + epsilon_readout + |epsilon_SN|`;
- WEP transfer branch: `delta_beta_source_abs <= |K_beta_from_WEP| eta_bound / |tau_WEP material_contrast| + |epsilon_SN|`.

The real WEP branch correctly blocks because the transfer denominator is missing. The toy WEP projection passes only as a unit test, not as evidence.

## Evaluator Results

- `CASE3991_0_parent_theorem_zero`: status `CONDITIONAL_THEOREM_ZERO_PARENT_UNSIGNED`, delta_beta `0`, passes=True, claim=False
- `CASE3991_1_real_WEP_anchor_projection_blocked`: status `REAL_WEP_BOUND_PRESENT_TRANSFER_DENOMINATOR_MISSING`, delta_beta `MISSING`, passes=False, claim=False
- `CASE3991_2_WEP_transfer_toy_projection`: status `TOY_PROJECTION_ONLY_NOT_EVIDENCE`, delta_beta `2.7e-15`, passes=True, claim=False
- `CASE3991_3_3990_small_envelope_smoke`: status `NUMERIC_SMOKE_ONLY_NOT_EVIDENCE`, delta_beta `9.8333330416e-06`, passes=True, claim=False
- `CASE3991_4_missing_parent_rows`: status `MISSING_3990_ENVELOPE_INPUT`, delta_beta `MISSING`, passes=False, claim=False

## Current Residual Meaning

The source-coupling gap has been narrowed again: it is now specifically the projection denominator from a real WEP observable into the MTS source-weight basis, or else the parent no-Hom theorem-zero.

## Source Register

`13/13` source needles found.
- `SRC3991_00_3990_next`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3990_NEXT_TARGET.csv` needle `NEXT3990_0` found=True
- `SRC3991_01_3990_bound`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3990_SOURCE_WEIGHT_BOUND_ROWS.csv` needle `SWB3990_6_beta` found=True
- `SRC3991_02_3990_schema`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3990_FIRST_REAL_SOURCE_WEIGHT_BOUND_SCHEMA.csv` needle `SWS3990_1` found=True
- `SRC3991_03_WEP_real_bound`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1934_WEP_SOURCE_WEIGHT_BOUND_ROW.csv` needle `WEP1934_0_MICROSCOPE_TiPt_eta` found=True
- `SRC3991_04_WEP_smoke`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1934_WEP_SOURCE_WEIGHT_NONCLAIM_SMOKE_ROW.csv` needle `SMOKE1934_0_MTS_WEP_source_weight_placeholder` found=True
- `SRC3991_05_R10_deltaW`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1476_DELTA_W_SOURCE_WEIGHT_INPUT_ROW_NONCLAIM.csv` needle `DW1476_0_delta_w_A` found=True
- `SRC3991_06_1887_template`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1887_SOURCE_WEIGHT_VECTOR_TEMPLATE_NONCLAIM.csv` needle `FSV1887_PPN_BETA_SOURCE_NONCLAIM` found=True
- `SRC3991_07_2514_beta`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_NO_SHADOW_2514_FINITE_BETA_SOURCE_VECTOR.csv` needle `DBETA2514_0_source` found=True
- `SRC3991_08_2631_ppn`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_NO_SHADOW_PPN_VECTOR_2631_FULL_PPN_VECTOR_LEDGER.csv` needle `PPNV2631_4_wR` found=True
- `SRC3991_09_3917_beta`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3917_DELTA_BETA_SOURCE_FILL_ROWS.csv` needle `BET3917_2_fallback` found=True
- `SRC3991_10_3919_lock`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3919_BETA_SOURCE_LOCK_DERIVATION.csv` needle `BETA3919_4_source_zero` found=True
- `SRC3991_11_1224_product`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1224_SOURCE_WEIGHT_PRODUCT_LAW.csv` needle `PROD1224_0_source_weight` found=True
- `SRC3991_12_1477_rules`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1477_CI_SOURCE_WEIGHT_EVALUATOR_RULES_V2.csv` needle `EVR1477_2_no_bound_inversion` found=True

## Next Target

`3992-Y5-R2FR-parent-source-weight-projection-or-WEP-tau-denominator.md`

Derive/source the `tau_WEP` denominator and material/source contrast, or parent-sign the no-Hom zero directly.
