# 256 - Fixed 2over27 vs Kappa-Free Cosmology Test Manifest

Private empirical-test checkpoint. This creates a fair test contract only. It
does not run a new fit, does not claim CMB support, and does not promote
`B_mem = 2/27` to a parent-derived amplitude.

## 1. Trigger

Checkpoint 255 showed:

```text
B_mem = kappa_mem (2/27)
```

with `kappa_mem` not fixed by Bianchi, topology, or rank arithmetic.

So the next empirical question is:

```text
does the strict fixed 2/27 branch survive,
and if kappa_mem is freed, does it improve enough to pay the parameter tax?
```

## 2. Machine Artifact

Script:

```text
scripts/fixed_2over27_vs_kappa_free_cosmology_test_manifest.py
```

Run:

```text
runs/20260601-000073-fixed-2over27-vs-kappa-free-cosmology-test-manifest
```

Command:

```text
python scripts/fixed_2over27_vs_kappa_free_cosmology_test_manifest.py --timestamp 20260601-000073
```

Status:

```text
fixed_2over27_vs_kappa_free_cosmology_manifest_written_no_scores_or_claims
```

Claim ceiling:

```text
test_manifest_only_no_new_empirical_or_theory_promotion
```

## 3. Branches

The strict lead branch is:

```text
MTS_fixed_2over27_no_clock:
  p = 3,
  u3 = 1/4,
  B_mem = 2/27,
  no global clock,
  no pair-ruler sidecar.
```

The ablation branch is:

```text
MTS_kappa_free_no_clock:
  p = 3,
  u3 = 1/4,
  B_mem = kappa_mem (2/27),
  kappa_mem fitted.
```

The second branch is not more fundamental. It is one extra amplitude hand in
the ring, so the judges charge it.

## 4. Parameter-Tax Rule

Against the fixed branch, `kappa_mem` adds:

```text
Delta k = 1.
```

Therefore the kappa branch must improve raw `chi2` by:

```text
more than 2
```

to beat AIC, and by:

```text
more than ln(n_eff)
```

to beat BIC.

If it does not pay that tax, the strict fixed `2/27` branch remains the cleaner
lead branch even if kappa improves raw residuals slightly.

## 5. Required Arenas

The manifest covers:

| arena | claim ceiling |
|---|---|
| SN+BAO T7 reproduction | late-time closure only |
| no-SH0ES SN+BAO | late-time closure only |
| BAO-only DR1/DR2 | BAO distance closure only |
| BAO+H(z), no CMB | late-time closure only |
| growth `f_sigma8` proxy | effective perturbation proxy only |
| CMB profiled/mock readiness | CMB diagnostic only |

No CMB/public-support claim can come from this manifest.

## 6. Fairness Rules

Every model must use:

```text
same rows,
same covariance,
same calibration branch,
same nuisance policy,
same convergence rules,
same prior-edge reporting.
```

Baselines are not invisible. If `LCDM`, `wCDM`, or `CPL` also fail a jackknife
or split, that is a data/pipeline warning, not an automatic MTS loss.

Likewise, MTS gets no free pass. Prior-edge or convergence failures block
stable-evidence language.

## 7. Outputs Required From Future Runs

Future actual runners must emit:

```text
fit_summary.csv
fixed_vs_kappa_penalty.csv
baseline_comparison.csv
residuals.csv
status.json
```

The key artifact is:

```text
fixed_vs_kappa_penalty.csv
```

because it forces the question:

```text
did kappa_mem actually pay for itself?
```

## 8. Claim Policy

Allowed:

```text
fixed 2/27 is the strict lead test branch.
```

Allowed:

```text
kappa-free is a phenomenological ablation.
```

Forbidden:

```text
kappa-free evidence is parent-amplitude evidence,
profiled/compressed CMB diagnostics are a CMB pass,
fixed 2/27 is now derived.
```

## 9. Decision

Decision:

```text
fixed_2over27_vs_kappa_free_cosmology_manifest_written_no_scores_or_claims
```

Meaning:

```text
the next empirical round is now pre-registered: fixed 2/27 keeps the clean
lead-branch gloves; kappa_mem may enter only as a penalized ablation.
```

Boxing translation:

```text
if kappa wants to join the fight, it has to win the round clearly, not just
nick a flashy exchange.
```

## 10. Next Target

Next:

```text
257-fixed-vs-kappa-free-SN-BAO-dryrun-runner.md
```

Purpose:

```text
implement the dry-run runner first: schema check, model matrix, parameter
counts, command plan, and refusal to score until the fixed/kappa branch
definitions are frozen.
```
