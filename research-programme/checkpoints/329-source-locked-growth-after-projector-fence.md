# 329 — Source-Locked Growth After Projector Fence

Private empirical checkpoint. This is not a public perturbation-theory, local-GR, PPN, CMB, cosmology, amplitude, or unified-field claim.

## Purpose

Checkpoints 327–328 fenced the local/projector branch:

```text
J_C can conditionally own the cubic FLRW hazard,
P_top has a conditional relative-cohomology route,
P_MTS still requires a parent sector charge.
```

So the next honest move is not to squeeze the same projector lock again.

This checkpoint refreshes the independent growth/RSD pressure test:

```text
Does locked B_mem=2/27 survive source-locked SDSS/eBOSS growth covariance
when baselines receive the same jackknife treatment?
```

Short answer:

```text
yes, as a conditional GR-proxy growth stress test.
```

But:

```text
MTS perturbations are still not derived.
```

## Machine Artifact

Script:

```text
scripts/source_locked_growth_covariance_holdout.py
```

Run:

```text
runs/20260601-170000-source-locked-growth-covariance-holdout
```

Fetched source intake:

```text
source-intake/sdss_eboss_dr16/20260601-170000
```

Status:

```text
growth_covariance_source_locked_primary_preferred_or_draw
```

Claim ceiling:

```text
source_locked_growth_covariance_holdout_no_perturbation_promotion
```

## Source Lock

The runner re-fetched the SDSS/eBOSS DR16 likelihood files listed in the local source manifest.

Hash-lock result:

```text
fetched_files = 19
failures = 0
```

All fetched files matched:

```text
manifest hash,
local hash.
```

This is important because the result is not relying on a stale or silently changed local copy.

## Fairness Contract

All scored branches use the same stress rule:

```text
locked B_mem = 2/27,
fixed late-time no-CMB background from BAO+H(z),
shared fitted sigma8_0 only,
same model set,
same covariance branches,
same jackknifes.
```

Models:

```text
LCDM,
wCDM,
CPL,
MTS_locked_2over27,
MTS_Bmem_zero.
```

The growth equation is still the GR background-growth proxy:

```text
D'' + [2 + d ln H / d ln a] D' - 3 Omega_m(a) D / 2 = 0.
```

So this is a disciplined stress test, not a derived MTS perturbation equation.

## Primary DR2 Result

Primary branch:

```text
DR2_noCMB_primary
primary_BAO_plus_all_samples
score_mode = all
```

Fit snapshot:

| Model | chi2 | BIC | sigma8_0 | source edge |
|---|---:|---:|---:|---:|
| `LCDM` | 16.7602715513 | 19.3993288810 | 0.8688417012 | false |
| `wCDM` | 13.9145029041 | 16.5535602337 | 0.8873719885 | false |
| `CPL` | 13.9639611223 | 16.6030184519 | 0.8777006500 | true |
| `MTS_locked_2over27` | 14.4567012710 | 17.0957586006 | 0.8823631714 | false |
| `MTS_Bmem_zero` | 16.7602715513 | 19.3993288810 | 0.8688417012 | false |

Locked MTS versus `LCDM`:

```text
Delta chi2 = -2.3035702803557125
Delta AIC  = -2.3035702803557108
Delta BIC  = -2.3035702803557143
readout    = locked_preferred
```

Locked MTS versus zero-memory control:

```text
Delta chi2 = -2.3035702803557125
```

So the nonzero locked memory term is doing measurable work in the primary covariance branch.

## RSD-Only and Full-Shape Checks

The primary all-row result is not treated as pure growth-amplitude proof.

RSD-only:

```text
DR2 primary BAO-plus f_sigma8-only vs LCDM:
Delta chi2 = -0.3346859767476644
readout = competitive_draw
```

Alternative full-shape-only compression:

```text
all rows Delta chi2 vs LCDM = -0.21779048907627363
RSD-only Delta chi2 vs LCDM = -0.30412137705544495
readout = competitive_draw
```

This means:

```text
the primary advantage is geometry-plus-growth,
while pure RSD and alternative compression keep MTS in the pack.
```

That is still a useful survival result.

## DR1 Sensitivity

DR1 no-CMB release sensitivity:

```text
primary BAO-plus all rows Delta chi2 vs LCDM = -2.5501137065853374
primary BAO-plus f_sigma8-only Delta chi2 vs LCDM = -0.322321378588037
```

Readout:

```text
all rows = locked preferred,
f_sigma8-only = competitive draw.
```

This matters because DR1 weakened the no-CMB BAO+H(z) near-win, but the growth covariance route does not collapse under DR1.

## Jackknife Card

All jackknives are scored against `LCDM` with the same `sigma8_0` nuisance rule.

| Background | File set | Mode | Preferred | Draw | Disfavored | Delta range |
|---|---|---|---:|---:|---:|---|
| DR2 | BAO-plus | all | 2 | 2 | 0 | -2.314 to -0.732 |
| DR2 | BAO-plus | fs8-only | 0 | 4 | 0 | -0.339 to -0.026 |
| DR2 | full-shape-only | all | 0 | 3 | 0 | -0.498 to +1.174 |
| DR2 | full-shape-only | fs8-only | 0 | 3 | 0 | -0.314 to +0.041 |
| DR1 | BAO-plus | all | 2 | 2 | 0 | -2.434 to -0.847 |
| DR1 | BAO-plus | fs8-only | 0 | 4 | 0 | -0.325 to -0.029 |
| DR1 | full-shape-only | all | 0 | 3 | 0 | -0.528 to +1.002 |
| DR1 | full-shape-only | fs8-only | 0 | 3 | 0 | -0.300 to +0.037 |

Jackknife verdict:

```text
8 groups,
0 failing groups.
```

This directly answers the fairness issue:

```text
MTS was not singled out for jackknifes;
the baselines took the same leave-one-sample-out punches.
```

## Controls and Gates

Controls:

```text
MTS_Bmem_zero reproduced LCDM in every branch.
control rows passing = 36.
```

Machine gates:

| Gate | Status |
|---|---|
| source fetch hash lock | pass |
| covariance schema | pass |
| frozen `B_mem` no refit | pass |
| same-test retest baselines | pass |
| primary growth not disfavored | pass |
| jackknife no hard loss | pass |
| do not combine alternative compressions | pass |
| theory promotion | fail |

The theory-promotion gate must fail, because:

```text
no MTS perturbation action is derived,
no local-GR theorem is derived,
no CMB bridge is derived.
```

## Interpretation

This is a strong internal empirical result for the locked late-time closure branch.

Allowed language:

```text
The locked 2/27 branch survives source-locked SDSS/eBOSS growth covariance
stress tests under a shared sigma8_0 GR-proxy growth treatment.
```

Stronger private/internal language:

```text
The branch now has a coherent late-time empirical survival pattern across
SN+BAO, BAO-only, BAO+H(z), H(z), and source-locked growth covariance.
```

Forbidden language:

```text
MTS derives perturbations.
MTS passes CMB.
MTS derives local GR.
MTS is a completed unified theory.
```

## Boxing Readout

This was a clean Mayweather round.

On primary BAO+FS:

```text
MTS nicks the round from LCDM.
```

On RSD-only and full-shape-only:

```text
MTS stays in the pack.
```

On jackknifes:

```text
MTS does not get dropped.
```

That is exactly the standard we set: not a knockout, but disciplined survival under fair scoring.

## Decision

Decision:

```text
growth_covariance_source_locked_primary_preferred_or_draw
```

Meaning:

```text
do not demote the locked late-time branch;
do not promote it to derived perturbation theory;
use growth survival as another empirical theorem target.
```

## Next Target

The empirical branch has now earned a harder likelihood task.

Next options:

```text
1. Build an ELG grid-likelihood parser.
2. Build an official/full-likelihood SN+BAO+growth wrapper.
```

Default recommendation:

```text
official/full-likelihood wrapper first,
ELG grid parser second,
unless the next turn is explicitly derivation-focused.
```

Reason:

```text
the theory side is fenced cleanly;
the empirical side now needs fewer proxies and more official likelihood structure.
```

## Output Files

```text
runs/20260601-170000-source-locked-growth-covariance-holdout/status.json
runs/20260601-170000-source-locked-growth-covariance-holdout/results/source_register.csv
runs/20260601-170000-source-locked-growth-covariance-holdout/results/fetch_hash_lock.csv
runs/20260601-170000-source-locked-growth-covariance-holdout/results/data_schema.csv
runs/20260601-170000-source-locked-growth-covariance-holdout/results/branch_manifest.csv
runs/20260601-170000-source-locked-growth-covariance-holdout/results/fit_summary.csv
runs/20260601-170000-source-locked-growth-covariance-holdout/results/baseline_comparisons.csv
runs/20260601-170000-source-locked-growth-covariance-holdout/results/control_reproduction.csv
runs/20260601-170000-source-locked-growth-covariance-holdout/results/jackknife_scorecard.csv
runs/20260601-170000-source-locked-growth-covariance-holdout/results/residuals.csv
runs/20260601-170000-source-locked-growth-covariance-holdout/results/gate_results.csv
runs/20260601-170000-source-locked-growth-covariance-holdout/results/decision.csv
```
