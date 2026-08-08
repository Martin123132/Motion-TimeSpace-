# 3952 - GK Helmholtz Khat Metric-Response Test Or DeltaK Bound

Timestamp: `2026-07-01T14:10:22+00:00`

## Result

3952 turns the Khat question into a genuine pass/fail variational test.

Define the Helmholtz obstruction:

`H_GK[h,k] := integral_D (h_mu_nu delta_k K_hat^mu_nu - k_mu_nu delta_h K_hat^mu_nu) dV`

modulo boundary exact terms.

If `K_hat` is defined by a parent scalar density,

`K_metric^mu_nu[Gamma_eff] := 2/sqrt(-g) delta(sqrt(-g) Gamma_eff)/delta g_mu_nu`

then `H_GK=0` by equality of mixed second variations. That branch is mathematically coherent.

## Current MTS Verdict

The current MTS branch is not promoted because the actual current `K_hat` tensor/density pair is still not supplied in a computable form.

So the exact split is:

`K_hat_current^mu_nu = K_metric^mu_nu[Gamma_eff] + Delta_K^mu_nu`.

This gives the sharpened local residual identity:

`q_loc^nu = -P_loc(E_A nabla^nu Z^A + R_boundary^nu + R_source^nu + nabla_mu Delta_K^mu_nu)`.

That is the important movement: any non-response part must now appear as `nabla_mu Delta_K^mu_nu`, not as an unspecified closure gap.

## Bound Fallback

The value-ready mismatch channel is:

`epsilon_GK_metric_response_mismatch := E_DeltaK/E_pos`

with

`E_DeltaK := int_D |Delta_K_mu_nu u^mu u^nu| dV + L_D int_D |nabla_mu Delta_K^mu_nu| dV`.

No public/local-GR claim follows until `Delta_K=0` is derived or this channel gets sourced values.

## Source Register

- Source rows found: `13/13`
- Register: `source-intake\mts_residuals\P8_Y5_R2FR_3952_SOURCE_REGISTER.csv`
- Validation: `source-intake\mts_residuals\P8_Y5_BRR545_3952_VALIDATION.csv`

## Generated Tables

- `source-intake\mts_residuals\P8_Y5_R2FR_3952_HELMHOLTZ_KHAT_TEST.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_3952_DELTAK_QLOC_BOUND.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_3952_DECISION_GATE.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_3952_CLAIM_GATE.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_3952_NEXT_TARGET.csv`

## Next Target

`3953-Y5-R2FR-minimal-Gamma-density-variation-and-Khat-current-comparison.md`
