# 3702 Y5 R2FR R10 Bound Curve Digitizer And MTS Alpha-Lambda Binder

Private checkpoint. No GitHub action. No public claim.

## Status

- `R10_CANDIDATE_CURVE_DIGITIZED_FROM_VECTOR_FIGURE_MTS_ALPHA_LAMBDA_BINDER_SCHEMA_READY_NONCLAIM`
- 3702 extracted a private candidate R10 alpha_bound(lambda) lower envelope from arXiv fig5b1.pdf. The selected component crosses alpha=1 at 38.583 micrometer, matching the official 38.6 micrometer anchor. The curve is useful for nonclaim smoke tests only; claims require an official supplemental table or manual-reviewed digitization plus numeric MTS alpha_eff/lambda_H rows.

## Main Result

- Pulled and inspected the arXiv source package for Lee et al. 2020 / PRL 124, 101101.
- The TeX confirms 66 tested `lambda` values from `5 micrometer` to `9 mm`, but says signed `alpha` constraints are in Supplemental Material.
- The arXiv source package contains `fig5b1.pdf` but no machine-readable alpha-lambda table.
- A private vector digitization candidate was extracted from `fig5b1.pdf`; it crosses `alpha=1` at `38.583346 micrometer`, matching the official `38.6 micrometer` anchor.
- The digitized curve is `valid_for_claim=false`; it is only for smoke-testing schema and rough private intuition until manually reviewed or replaced by an official table.

## Extraction Rows

- `EXT3702_0_axis_calibration`: `medium_for_private_digitization` | x_major_1e-5_m=2102.79; x_major_1e-4_m=3361.06; y_logalpha_minus3=775.344; y_logalpha_6=3835.29
- `EXT3702_1_curve_component`: `candidate_curve_manual_review_required` | crossing=38.583346 micrometer; official anchor=38.6 micrometer; abs error=0.016654 micrometer
- `EXT3702_2_limitations`: `blocker_precisely_named` | TeX says positive and negative alpha constraints are in Supplemental Material, but extracted arXiv source package contains PDFs and no machine-readable alpha-lambda table.

## Curve Rows

- Candidate rows: `66`
- Official anchor row: `38.600000 micrometer`, `alpha=1`, `valid_for_claim=false`

## MTS Binder Rows

- `MTSR10_3702_0_lambda`: `MISSING_MUH_VALUE` | lambda_H = 1/mu_H
- `MTSR10_3702_1_alpha`: `MISSING_ALPHA_VALUE` | alpha_eff = K_N * 0.5*rho_Newton*z0^2 + alpha_edge + alpha_proj
- `MTSR10_3702_2_score`: `SCHEMA_READY_VALUES_MISSING` | pass_if abs(alpha_eff(lambda_H)) <= alpha_bound_R10(lambda_H)
- `MTSR10_3702_3_anchor_only`: `ANCHOR_ONLY_SMOKE` | if lambda_H >= 38.6 micrometer then gravitational-strength alpha_eff~1 branch is disfavored by Lee2020 anchor

## Smoke Rows

- `SMOKE3702_0_curve_candidate`: score_ready=True claim=false | 66 candidate curve rows plus official alpha=1 anchor at 38.600000 micrometer | blocker: manual review and/or official supplemental alpha table required for claims
- `SMOKE3702_1_mts_binding`: score_ready=False claim=false | binder schema exists but no numeric rho_Newton, z2_bound, mu_H, K_N, alpha_edge, or alpha_proj | blocker: MTS-side numeric rows missing

## Decisions

- `DEC3702_0`: `CURVE_CANDIDATE_ADVANCES` | R10 figure digitization candidate exists. | Vector extraction from fig5b1 reproduces the official alpha=1 crossing at 38.58 micrometer.
- `DEC3702_1`: `CLAIM_BLOCKED` | Do not treat the candidate curve as claim evidence. | The paper says the signed alpha constraints are in Supplemental Material; no machine-readable official table was found in the arXiv source package.
- `DEC3702_2`: `MTS_SIDE_MISSING` | MTS R10 binder is schema-ready but not numerically score-ready. | lambda_H and alpha_eff remain symbolic until mu_H/rho_Newton/z2_bound/K_N are sourced.

## Claim Gates

- `CG3702_0_official_curve`: `BLOCKED` | official full alpha_bound(lambda) table or manually reviewed digitization
- `CG3702_1_mts_lambda`: `BLOCKED` | numeric lambda_H=1/mu_H sourced from parent mass-gap rows
- `CG3702_2_mts_alpha`: `BLOCKED` | numeric alpha_eff from rho_Newton, z2_bound, K_N, edge, projection terms
- `CG3702_3_score`: `BLOCKED` | abs(alpha_eff(lambda_H)) <= alpha_bound_R10(lambda_H) evaluated
- `CG3702_4_public`: `BLOCKED` | public R10/local-Newton claim allowed

## Source Register

- `handoff_3701`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3701_NEXT_TARGET.csv`
- `source_rows_3701`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3701_LOCAL_TEST_SOURCE_ROWS.csv`
- `matrix_3701`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3701_RESIDUAL_MATRIX_ROWS.csv`
- `arxiv_tex_2002_11761`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\r10\arxiv_2002_11761_source\FB_ISL_pdf.tex`
- `arxiv_fig5b1_pdf`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\r10\arxiv_2002_11761_source\fig5b1.pdf`
- `arxiv_source_archive`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\r10\arxiv_2002_11761_source.tar.gz`

## Next Target

- `3703-Y5-R2FR-MTS-rho-Newton-z2bound-muH-numeric-or-symbolic-bound.md`
- Objective: try to derive or bound the MTS-side R10 inputs rho_Newton, z2_bound, mu_H/lambda_H, K_N, alpha_edge, and alpha_proj from the Fisher/source-silence chain
