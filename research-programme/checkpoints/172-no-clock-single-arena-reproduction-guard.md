# 172 - No-Clock Single-Arena Reproduction Guard

Private scorer checkpoint. This is not a public claim.

## 1. Trigger

Checkpoint 171 proved the official-refresh scorer can read the source-refresh
manifests without smuggling in the pair-ruler sidecar or producing hidden fit
scores.

This checkpoint adds the next narrow mode:

```text
--mode reproduce --assert-no-sidecar
```

It reproduces exactly one known empirical arena before any broader official
refresh is allowed:

```text
BAO-only DESI DR2 and DESI DR1 locked 2/27 branch test.
```

This is deliberately not SN, H(z), growth, CMB, or full combined likelihood.

## 2. Machine Artifact

Script:

```text
scripts/no_clock_official_likelihood_refresh.py
```

Reproduction scorer reused:

```text
scripts/locked_2over27_BAO_only_release_test.py
```

Run:

```text
runs/20260531-235959-no-clock-single-arena-reproduction-guard
```

Command:

```text
python scripts/no_clock_official_likelihood_refresh.py --mode reproduce --assert-no-sidecar --timestamp 20260531-235959 --source-run runs/20260531-235959-no-clock-official-source-refresh --max-iter 180 --reference-tolerance 1e-8
```

Status:

```text
no_clock_single_arena_BAO_reproduction_passed
```

Claim ceiling:

```text
single_arena_BAO_reproduction_no_full_refresh_or_theory_promotion
```

## 3. What Was Scored

Arena:

```text
BAO-only
```

Releases:

| release | rows |
|---|---:|
| DESI DR2 primary | 18 |
| DESI DR1 primary | 12 |

Models:

| model | role |
|---|---|
| `LCDM` | baseline |
| `wCDM` | baseline |
| `CPL` | baseline |
| `MTS_locked_2over27` | no-clock lead alias for `MTS_2over27_no_clock_u3quarter` |
| `MTS_Bmem_zero` | negative control |
| `MTS_fitted_Bmem_diagnostic` | diagnostic only |

The pair-ruler half-kernel sidecar was not scored.

## 4. Gate Results

All reproduction gates passed:

| gate | status |
|---|---|
| manifest guard passed | pass |
| arena is BAO-only | pass |
| required models scored | pass |
| sidecar absent | pass |
| locked branch fixed `B_mem = 2/27` | pass |
| locked branch not prior-edge | pass |
| all models converged | pass |
| prior edges reported for all models | pass |
| reference delta reproduced | pass |
| full refresh not run | pass |
| claim ceiling preserved | pass |
| BAO release loads pass | pass |

Failure count:

```text
failed_gates = 0
```

## 5. Reproduced Reference Deltas

The previous BAO-only locked-branch result was reproduced exactly within the
`1e-8` tolerance:

| release | comparison | reproduced `ΔBIC` |
|---|---|---:|
| DESI DR2 primary | locked 2/27 vs LCDM | -2.108368627321081 |
| DESI DR1 primary | locked 2/27 vs LCDM | -0.8483738675035859 |

Readout:

```text
The no-clock locked 2/27 branch remains competitive on BAO-only information
criteria in both DR2 and DR1, using the same fitted-baseline machinery.
```

## 6. Baseline Fairness Readout

The same BAO-only reproduction compares the locked branch against `LCDM`,
`wCDM`, and `CPL`:

| release | reference | `Δχ²` | `ΔAIC` | `ΔBIC` |
|---|---|---:|---:|---:|
| DESI DR2 primary | LCDM | -2.108368627321081 | -2.108368627321081 | -2.108368627321081 |
| DESI DR2 primary | wCDM | -0.8784013279999279 | -2.878401327999928 | -3.4433506854614677 |
| DESI DR2 primary | CPL | 2.3030470252785333 | -1.6969529747214658 | -2.826851689644542 |
| DESI DR1 primary | LCDM | -0.8483738675035877 | -0.8483738675035877 | -0.8483738675035859 |
| DESI DR1 primary | wCDM | -0.8127377954532999 | -2.8127377954533 | -3.2976444452413 |
| DESI DR1 primary | CPL | 1.9220830724920805 | -2.0779169275079195 | -3.0477302270839175 |

Important nuance:

```text
CPL can reduce chi2 relative to the locked branch, but pays parameter cost.
The locked branch wins AIC/BIC in this BAO-only arena.
```

That is the Mayweather-style result: not a knockout, but clean scoring on this
round.

## 7. Prior-Edge Discipline

The locked branch:

```text
prior_edge_flag = False
```

The reproduction table reports two prior-edge flags overall. They belong to the
flexible baseline/diagnostic side of the fit discipline, not to the locked
2/27 branch.

This matters because the same prior-edge police now apply to everyone:

```text
MTS does not get to ignore edge pressure,
but LCDM extensions do not get to hide it either.
```

## 8. What This Does Not Prove

This checkpoint does not prove:

```text
the full official likelihood,
a CMB pass,
the local GR branch,
the parent action,
or a derived value of B_mem = 2/27.
```

It only proves:

```text
the new official-refresh runner can reproduce a known BAO-only result,
with baselines present, sidecar excluded, prior edges reported, and no full
refresh claim being made.
```

## 9. Decision

Decision:

```text
no_clock_single_arena_BAO_reproduction_passed
```

Meaning:

```text
The lead no-clock branch has survived the first official-refresh reproduction
gate. The hit is not hype; it is reproducible in this narrow arena. But the
title belt still requires expansion to SN+BAO, then H(z)/growth, and eventually
a disciplined CMB/perturbation bridge.
```

## 10. Next Target

Create:

```text
173-no-clock-SN-BAO-reproduction-guard.md
```

Extend:

```text
scripts/no_clock_official_likelihood_refresh.py
```

Next task:

```text
Add a second reproduction mode for the existing SN+BAO no-clock/locked branch
pipeline, keeping the same baseline fairness, prior-edge, no-sidecar, and
claim-ceiling rules.
```
