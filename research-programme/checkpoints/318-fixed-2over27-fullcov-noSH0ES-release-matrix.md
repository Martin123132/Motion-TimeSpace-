# 318 - Fixed 2/27 Full-Cov No-SH0ES Release Matrix

Private empirical checkpoint. This is not a public cosmology, CMB, local-GR, or parent-field-theory claim.

## Purpose

Checkpoints 316 and 317 narrowed the theory situation:

```text
FLRW shape/source/LCDM limit: improved.
kappa_mem=1: not derived.
B_mem=2/27: still closure/theorem target.
```

So the next empirical question is clean:

```text
If we do not fit the memory amplitude at all,
does the strict fixed B_mem=2/27 branch survive the same full-cov no-SH0ES DR2/DR1 matrix?
```

This checkpoint runs exactly that.

## Model Contract

Data:

```text
Pantheon+ full covariance,
mb-corr observable,
calibrators excluded,
DESI DR2 BAO release,
DESI DR1 BAO release.
```

Models:

```text
LCDM,
wCDM,
CPL with the same wide CPL priors as checkpoint 315,
MTS_fixed_2over27_no_clock,
MTS_kappa_free_no_clock,
MTS_Bmem_zero.
```

Strict branch:

```text
p = 3,
u3 = 1/4,
B_mem = 2/27,
kappa_mem = 1 by closure only.
```

No amplitude is fitted in the strict branch.

## Core Result

| Comparator | DR2 delta chi2 | DR2 delta AIC | DR2 delta BIC | DR1 delta chi2 | DR1 delta AIC | DR1 delta BIC |
|---|---:|---:|---:|---:|---:|---:|
| fixed 2/27 vs LCDM | -5.259467 | -5.259467 | -5.259467 | -3.618758 | -3.618758 | -3.618758 |
| fixed 2/27 vs wCDM | -0.169009 | -2.169009 | -7.569630 | -0.381424 | -2.381424 | -7.781433 |
| fixed 2/27 vs CPL | +0.167728 | -3.832272 | -14.633514 | +0.382537 | -3.617463 | -14.417482 |

Sign convention:

```text
negative delta = fixed 2/27 is better than the named baseline.
positive delta = baseline is better.
```

Readout:

```text
fixed 2/27 beats LCDM, wCDM, and CPL by AIC/BIC in both DR2 and DR1.
```

Against CPL, the fixed branch loses raw chi2 by a tiny amount, but wins after parameter penalties.

## Kappa Test

Kappa-free asks whether the data require an extra amplitude:

| Release | fixed chi2 | kappa-free chi2 | raw chi2 gain | delta AIC kappa-fixed | delta BIC kappa-fixed | kappa promoted |
|---|---:|---:|---:|---:|---:|---:|
| DR2 | 1465.268406 | 1465.268214 | 0.000192 | +1.999808 | +7.400429 | no |
| DR1 | 1468.962326 | 1468.962042 | 0.000284 | +1.999716 | +7.399726 | no |

The fitted kappa values are:

| Release | fitted `B_mem` | implied `kappa_mem` |
|---|---:|---:|
| DR2 | 0.074533 | 1.006198 |
| DR1 | 0.073418 | 0.991149 |

So the amplitude-fitted branch lands close to `2/27`, but does not pay for its extra freedom.

## Control Check

`MTS_Bmem_zero` exactly collapses onto LCDM in both releases.

That means:

```text
the memory term is the scoring difference,
not a bookkeeping difference in the pipeline.
```

## Residual Readout

The strict fixed branch improves the BAO residual RMS relative to LCDM:

| Release | LCDM BAO RMS | fixed 2/27 BAO RMS |
|---|---:|---:|
| DR2 | 0.307391 | 0.265384 |
| DR1 | 0.574738 | 0.516446 |

SN residual RMS is also slightly lower than LCDM:

| Release | LCDM SN RMS | fixed 2/27 SN RMS |
|---|---:|---:|
| DR2 | 0.163504 | 0.163050 |
| DR1 | 0.163373 | 0.163064 |

Residual plots were written for SN and BAO in both releases.

## Gates

| Gate | Result | Meaning |
|---|---:|---|
| source paths exist | pass | all source artifacts exist |
| all models converged | pass | every branch converged |
| no prior-edge flags | pass | no fitted parameter sits on a prior edge |
| fixed beats LCDM AIC/BIC both releases | pass | strict branch beats LCDM with equal parameter count |
| fixed beats wCDM AIC/BIC both releases | pass | strict branch beats wCDM with fewer parameters |
| fixed beats CPL AIC/BIC both releases | pass | strict branch beats CPL after penalty |
| kappa-free not promoted | pass | amplitude freedom does not pay AIC/BIC tax |
| Bmem parent derived | fail | deliberate fail: 2/27 is still closure/theorem target |
| stable evidence allowed | fail | diagnostic matrix only |

## Interpretation

This is the strongest clean late-time background score so far.

Why:

```text
the strict branch has the same parameter count as LCDM,
uses no fitted memory amplitude,
survives DR2 and DR1,
beats LCDM/wCDM/CPL by AIC/BIC,
and the kappa-free hand is not needed.
```

But the claim ceiling remains strict:

```text
this does not derive B_mem,
does not pass CMB,
does not derive local GR,
does not finish the parent field theory.
```

Boxing translation:

```text
This is the cleanest round MTS has won on the cards so far.
Not a knockout.
Not a title belt.
But it is absolutely not grim.
```

## Decision

Decision:

```text
fixed_2over27_fullcov_noSH0ES_DR1_DR2_matrix_scored_no_parent_claim
```

Claim ceiling:

```text
fixed_2over27_late_time_background_score_only_no_parent_CMB_or_local_GR_promotion
```

Readout:

```text
strict_fixed_2over27_survives_DR1_DR2_fullcov_noSH0ES_matrix
```

## Next Target

Before stronger empirical language:

```text
symmetric jackknife / split tests,
external H(z) and growth holdouts,
then only after that revisit CMB bridge readiness.
```

Theory-side:

```text
only a nonhomogeneous trace-anomaly/index/scale-lock theorem can promote kappa_mem=1.
```

## Machine Artifacts

Script:

```text
scripts/fixed_2over27_fullcov_noSH0ES_release_matrix.py
```

Run:

```text
runs/20260601-000145-fixed-2over27-fullcov-noSH0ES-release-matrix
```

Output files:

```text
runs/20260601-000145-fixed-2over27-fullcov-noSH0ES-release-matrix/results/source_register.csv
runs/20260601-000145-fixed-2over27-fullcov-noSH0ES-release-matrix/results/release_config.csv
runs/20260601-000145-fixed-2over27-fullcov-noSH0ES-release-matrix/results/fit_summary.csv
runs/20260601-000145-fixed-2over27-fullcov-noSH0ES-release-matrix/results/baseline_comparison.csv
runs/20260601-000145-fixed-2over27-fullcov-noSH0ES-release-matrix/results/fixed_vs_kappa.csv
runs/20260601-000145-fixed-2over27-fullcov-noSH0ES-release-matrix/results/prior_edge_table.csv
runs/20260601-000145-fixed-2over27-fullcov-noSH0ES-release-matrix/results/residual_summary.csv
runs/20260601-000145-fixed-2over27-fullcov-noSH0ES-release-matrix/results/release_stability.csv
runs/20260601-000145-fixed-2over27-fullcov-noSH0ES-release-matrix/results/plot_manifest.csv
runs/20260601-000145-fixed-2over27-fullcov-noSH0ES-release-matrix/results/gate_results.csv
runs/20260601-000145-fixed-2over27-fullcov-noSH0ES-release-matrix/results/decision.csv
```
