# 257 - Fixed vs Kappa-Free SN+BAO Dryrun Runner

Private runner checkpoint. This adds a dry-run wrapper only. It does not fit
SN, BAO, CMB, growth, or any other data, and it does not create a new empirical
score.

## 1. Trigger

Checkpoint 256 froze the fair test manifest:

```text
fixed 2/27 = strict lead closure,
kappa_mem = penalized ablation.
```

The next safe move is not a long fit. It is a dry-run runner that refuses to
score until branch definitions, data schemas, parameter counts, and output
contracts are locked.

## 2. Machine Artifact

Script:

```text
scripts/fixed_vs_kappa_cosmology_runner.py
```

Run:

```text
runs/20260601-000074-fixed-vs-kappa-free-SN-BAO-dryrun-runner
```

Command:

```text
python scripts/fixed_vs_kappa_cosmology_runner.py --phase dry-run --arena SN-BAO-T7 --timestamp 20260601-000074
```

Status:

```text
fixed_vs_kappa_SN_BAO_dryrun_passed_no_scores_generated
```

Claim ceiling:

```text
dryrun_schema_and_model_contract_only_no_fit_or_claim
```

## 3. What The Dry Run Checks

The runner checks:

```text
source files exist,
SN row template,
BAO mean/covariance shape,
fixed and kappa branch contracts,
model parameter matrix,
kappa AIC/BIC tax template.
```

It writes:

```text
data_schema_report.csv
branch_contract.csv
model_parameter_matrix.csv
fixed_vs_kappa_penalty_template.csv
preflight_gates.csv
command_plan.csv
```

## 4. Branch Contract

The dry-run branch split is:

```text
MTS_fixed_2over27_no_clock:
  B_mem = 2/27,
  kappa_mem = 1 by closure,
  free amplitude count = 0.
```

and:

```text
MTS_kappa_free_no_clock:
  B_mem = kappa_mem (2/27),
  kappa_mem fitted,
  free amplitude count = 1.
```

The runner also keeps:

```text
MTS_Bmem_zero
```

as a negative control.

## 5. Parameter Penalty

Using the dry-run row template, the kappa branch gets:

```text
Delta k = 1.
```

So future score phases must require:

```text
Delta chi2 > 2
```

for AIC preference, and:

```text
Delta chi2 > ln(n_eff)
```

for BIC preference.

The dry run computes the actual `n_eff` template from the current SN+BAO files.

## 6. Score Refusal

This runner is deliberately not a scoring runner yet.

If used honestly, it should be followed by a separate implementation checkpoint
for the short-smoke score phase.

That keeps the pipeline from doing the classic bad science shuffle:

```text
fit first,
define the rules after.
```

## 7. Claim Policy

Allowed:

```text
the fixed/kappa SN+BAO dry-run contract is ready.
```

Forbidden:

```text
new empirical support,
kappa promotion,
B_mem derivation,
CMB/growth/local-GR claims.
```

## 8. Decision

Decision:

```text
fixed_vs_kappa_SN_BAO_dryrun_passed_no_scores_generated
```

Meaning:

```text
the gloves, ring, and judges' scorecards are set up. No punches have been
counted yet.
```

## 9. Next Target

Next:

```text
258-fixed-vs-kappa-free-SN-BAO-short-smoke-implementation.md
```

Purpose:

```text
implement the short-smoke scoring phase against the frozen dry-run contract,
then compare fixed 2/27, kappa-free, and baselines with explicit AIC/BIC
penalty accounting.
```
