# 258 - Fixed vs Kappa-Free SN+BAO Short-Smoke Implementation

Private implementation checkpoint. This is a same-data, same-nuisance
SN+BAO short-smoke score of the strict fixed `B_mem=2/27` branch against the
one-extra-parameter `kappa_mem` ablation.

It is not a parent-action derivation, CMB result, growth result, local-GR
result, or public claim.

## 1. Trigger

Checkpoint 257 froze the rule:

```text
MTS_fixed_2over27_no_clock is the strict lead closure.
MTS_kappa_free_no_clock is allowed only as a penalized amplitude ablation.
```

The next honest move was to score them on the same SN+BAO split and ask whether
the free amplitude actually earns its extra parameter.

## 2. Machine Artifact

Script:

```text
scripts/fixed_vs_kappa_cosmology_runner.py
```

Dry-run validation:

```text
runs/20260601-000075-fixed-vs-kappa-free-SN-BAO-dryrun-runner
```

Short-smoke run:

```text
runs/20260601-000076-fixed-vs-kappa-free-SN-BAO-short-smoke-implementation
```

Command:

```text
python scripts/fixed_vs_kappa_cosmology_runner.py --phase short-smoke --arena SN-BAO-T7 --timestamp 20260601-000076 --max-iter 120
```

Status:

```text
fixed_vs_kappa_SN_BAO_short_smoke_scored
```

Claim ceiling:

```text
SN_BAO_short_smoke_only_no_parent_or_CMB_promotion
```

## 3. Data and Model Contract

The scored arena uses:

```text
Pantheon+SH0ES with full covariance, mb-corr observable, calibrators excluded:
  SN rows = 1624

DESI DR2 BAO Gaussian mean/covariance:
  BAO rows = 13

n_eff = 1637
```

Models scored:

```text
LCDM
wCDM
CPL
MTS_fixed_2over27_no_clock
MTS_kappa_free_no_clock
MTS_Bmem_zero
```

The MTS fixed branch has:

```text
p = 3
u3 = 1/4
B_mem = 2/27 = 0.074074074074
kappa_mem = 1 fixed by closure only
```

The kappa branch has:

```text
p = 3
u3 = 1/4
B_mem = kappa_mem (2/27)
kappa_mem fitted
```

## 4. Fit Summary

```text
LCDM:
  chi2 = 1470.527872679
  AIC  = 1476.527872679
  BIC  = 1492.729734411
  k    = 3

wCDM:
  chi2 = 1465.437415073
  AIC  = 1473.437415073
  BIC  = 1495.039897383
  k    = 4

CPL:
  chi2 = 1465.100678197
  AIC  = 1475.100678197
  BIC  = 1502.103781084
  k    = 5

MTS_fixed_2over27_no_clock:
  chi2 = 1465.268405801
  AIC  = 1471.268405801
  BIC  = 1487.470267533
  k    = 3

MTS_kappa_free_no_clock:
  chi2 = 1465.268214007
  AIC  = 1473.268214007
  BIC  = 1494.870696316
  k    = 4

MTS_Bmem_zero:
  chi2 = 1470.527872679
  AIC  = 1476.527872679
  BIC  = 1492.729734411
  k    = 3
```

All fitted models converged. No prior-edge flags were hit.

## 5. Fixed vs Kappa Readout

The kappa branch fits:

```text
B_mem = 0.074533191601
kappa_mem = 1.006198086608
```

Against fixed `B_mem=2/27`, it improves raw chi2 by only:

```text
Delta chi2 = 0.000191793823
```

But the extra parameter must pay:

```text
AIC tax: Delta chi2 > 2
BIC tax: Delta chi2 > 7.400620577
```

It does not pay either tax.

Decision:

```text
kappa_free_improves_raw_chi2_but_not_information_criteria
```

So the kappa branch is not promoted. The strict fixed `2/27` branch remains the
cleaner lead branch for this SN+BAO short-smoke.

## 6. Fair Baseline Readout

The strict fixed branch compared to the baselines:

```text
vs LCDM:
  Delta chi2 = -5.259466878
  Delta AIC  = -5.259466878
  Delta BIC  = -5.259466878

vs wCDM:
  Delta chi2 = -0.169009272
  Delta AIC  = -2.169009272
  Delta BIC  = -7.569629850

vs CPL:
  Delta chi2 = +0.167727604
  Delta AIC  = -3.832272396
  Delta BIC  = -14.633513551
```

This is exactly the kind of result the programme should be looking for:

```text
not a knockout,
but a clean scorecard win on parsimony while staying in the round on chi2.
```

Still, this remains a late-time background test only.

## 7. Diagnostics Written

The short-smoke writes:

```text
fit_summary.csv
baseline_comparison.csv
fixed_vs_kappa_penalty.csv
prior_edge_table.csv
implementation_gates.csv
residual_summary.csv
bao_residuals.csv
plot_register.csv
SN_residuals_fixed_vs_kappa.svg
BAO_residuals_fixed_vs_kappa.svg
decision.csv
status.json
```

`matplotlib` is not installed in the scoring environment, so the runner writes
SVG residual plots directly as a dependency-free fallback.

## 8. Gates

Passed:

```text
data_shapes_pass
all_models_converged
no_prior_edge_flags
fixed_branch_competitive_with_baselines
```

Failed by design:

```text
kappa_parameter_tax_paid
```

Meaning:

```text
kappa-free is a useful ablation, but not a better theory branch here.
```

## 9. Decision

Decision:

```text
fixed_2over27_survives_short_smoke_kappa_not_promoted
```

Allowed:

```text
The fixed 2/27 no-clock branch is empirically competitive on this SN+BAO
short-smoke and beats the kappa-free ablation after AIC/BIC accounting.
```

Forbidden:

```text
B_mem is derived,
the parent action is complete,
CMB/growth/local-GR are solved,
MTS is promoted as a final theory.
```

## 10. Next Target

The next derivation target is not another amplitude fit.

It is:

```text
derive or reject the memory-stress normalization route that would make
kappa_mem = 1 a theorem rather than a closure.
```

If that route fails, the fixed `2/27` branch remains a disciplined empirical
closure. If it succeeds, the branch starts looking much more like field theory
than curve fitting.
