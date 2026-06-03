# 283 - Fixed-vs-Kappa Short-Smoke Readout

Private empirical short-smoke checkpoint. This is not a public CMB, local-GR, or parent-field-theory claim.

## Purpose

Checkpoint 282 left two near-term paths:

```text
repair the generic BAO manifest,
or run the fixed-vs-kappa short smoke.
```

The fixed-vs-kappa dry-run had already passed, so this checkpoint runs the short smoke and audits:

```text
convergence,
prior edges,
residuals,
AIC/BIC against LCDM/wCDM/CPL,
and whether kappa-free earns its extra parameter.
```

## Machine Artifacts

Scoring run:

```text
runs/20260601-000105-fixed-vs-kappa-free-SN-BAO-short-smoke-implementation
```

Readout script:

```text
scripts/fixed_vs_kappa_short_smoke_readout_after_282.py
```

Readout run:

```text
runs/20260601-000106-fixed-vs-kappa-short-smoke-readout-after-282
```

Status:

```text
fixed_2over27_short_smoke_competitive_kappa_not_promoted_no_parent_claim
```

Claim ceiling:

```text
SN_BAO_short_smoke_closure_score_only_no_parent_CMB_or_local_GR_promotion
```

## Core Result

The fixed no-clock `2/27` branch is competitive in this SN+BAO short smoke.

Fit summary:

| Model | chi2 | AIC | BIC | Edge flag |
|---|---:|---:|---:|---|
| LCDM | 1470.5278726785464 | 1476.5278726785464 | 1492.7297344106598 | false |
| wCDM | 1465.437415073122 | 1473.437415073122 | 1495.0398973826066 | false |
| CPL | 1465.100678197247 | 1475.100678197247 | 1502.1037810841026 | false |
| MTS fixed `2/27` | 1465.2684058007974 | 1471.2684058007974 | 1487.4702675329108 | false |
| MTS kappa-free | 1465.2682140069749 | 1473.2682140069749 | 1494.8706963164593 | false |
| MTS `B_mem=0` | 1470.5278726785464 | 1476.5278726785464 | 1492.7297344106598 | false |

All models converged.

No prior-edge flags appeared.

## Baseline Comparison

For the fixed `2/27` branch:

```text
vs LCDM:
delta_chi2 = -5.2594668777489915
delta_AIC  = -5.2594668777489915
delta_BIC  = -5.2594668777489915
```

```text
vs wCDM:
delta_chi2 = -0.16900927232472895
delta_AIC  = -2.169009272324729
delta_BIC  = -7.56962984969573
```

```text
vs CPL:
delta_chi2 = 0.16772760355047467
delta_AIC  = -3.8322723964495253
delta_BIC  = -14.633513551191754
```

Interpretation:

```text
fixed 2/27 beats LCDM/wCDM/CPL by AIC/BIC in this short smoke.
```

Against CPL, MTS has slightly worse raw chi2 but fewer parameters, so AIC/BIC favour the fixed branch.

## Kappa-Free Test

Kappa-free result:

```text
kappa_best_Bmem = 0.07453319160061826
kappa_best_kappa_mem = 1.0061980866083466
fixed_Bmem = 0.07407407407407407
```

Raw improvement:

```text
delta_chi2_improvement = 0.0001917938225233229
```

Information penalty:

```text
AIC tax required = 2
BIC tax required = 7.400620577371135
```

Actual:

```text
delta_AIC_kappa_minus_fixed = 1.9998082061774767
delta_BIC_kappa_minus_fixed = 7.400428783548477
```

So:

```text
kappa-free is not promoted.
```

This is a useful result because the best kappa-free fit lands very close to the fixed `2/27` amplitude but does not pay for the extra freedom.

## Residual Diagnostics

Residual summary:

| Model | SN RMS | BAO RMS | BAO max abs |
|---|---:|---:|---:|
| LCDM | 0.16350415184714895 | 0.3073907160953857 | 0.6163580224315339 |
| wCDM | 0.16317090374680424 | 0.2783370969439023 | 0.6075498971135893 |
| CPL | 0.16323569877480504 | 0.2767145564621511 | 0.5910787764259346 |
| MTS fixed `2/27` | 0.16304950526203182 | 0.26538415276571037 | 0.5906962820493575 |
| MTS kappa-free | 0.16304852763466884 | 0.26517256323043437 | 0.5908203267981165 |
| MTS `B_mem=0` | 0.16350415184714895 | 0.3073907160953857 | 0.6163580224315339 |

Residual plots were written:

```text
runs/20260601-000105-fixed-vs-kappa-free-SN-BAO-short-smoke-implementation/results/SN_residuals_fixed_vs_kappa.svg
runs/20260601-000105-fixed-vs-kappa-free-SN-BAO-short-smoke-implementation/results/BAO_residuals_fixed_vs_kappa.svg
```

## What This Does and Does Not Mean

Allowed statement:

```text
In this same-data SN+BAO short smoke, the fixed no-clock 2/27 closure branch is competitive and kappa-free is not justified by AIC/BIC.
```

Not allowed:

```text
B_mem is derived.
MTS passes CMB.
MTS derives local GR.
MTS is a finished parent field theory.
```

This is a strong sparring round, not a title belt.

## Output Files

Short-smoke results:

```text
runs/20260601-000105-fixed-vs-kappa-free-SN-BAO-short-smoke-implementation/results/fit_summary.csv
runs/20260601-000105-fixed-vs-kappa-free-SN-BAO-short-smoke-implementation/results/baseline_comparison.csv
runs/20260601-000105-fixed-vs-kappa-free-SN-BAO-short-smoke-implementation/results/prior_edge_table.csv
runs/20260601-000105-fixed-vs-kappa-free-SN-BAO-short-smoke-implementation/results/residual_summary.csv
runs/20260601-000105-fixed-vs-kappa-free-SN-BAO-short-smoke-implementation/results/implementation_gates.csv
```

Readout results:

```text
runs/20260601-000106-fixed-vs-kappa-short-smoke-readout-after-282/results/source_register.csv
runs/20260601-000106-fixed-vs-kappa-short-smoke-readout-after-282/results/score_readout.csv
runs/20260601-000106-fixed-vs-kappa-short-smoke-readout-after-282/results/gate_results.csv
runs/20260601-000106-fixed-vs-kappa-short-smoke-readout-after-282/results/residual_readout.csv
runs/20260601-000106-fixed-vs-kappa-short-smoke-readout-after-282/results/next_actions.csv
runs/20260601-000106-fixed-vs-kappa-short-smoke-readout-after-282/results/decision.csv
```

## Next Step

Before stronger empirical language:

```text
repair the generic BAO manifest,
run no-SH0ES shape branch,
run split / BAO-release robustness,
and keep official CMB separate until official likelihood assets exist.
```

Theory-side next:

```text
derive or reject memory-stress normalization before making any amplitude claim.
```

