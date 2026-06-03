# 315 - Full-Cov No-SH0ES Score Readout

Private empirical checkpoint. This is not a public cosmology, CMB, local-GR, galaxy, or parent-field-theory claim.

## Purpose

Checkpoint 314 said the full-covariance no-SH0ES branch was score-ready.

This checkpoint runs the short-smoke score for:

```text
Pantheon+ full covariance,
mb-corr shape branch,
calibrator-excluded no-SH0ES branch,
DESI DR2 and DESI DR1 release split,
LCDM / wCDM / CPL / MTS fixed / B_mem=0 control.
```

The point is not to declare victory.

The point is to ask whether the current no-clock MTS closure stays in the fight when local-H0 calibration pressure is removed.

## Score Result

| Comparator | DESI DR2 Result | DESI DR1 Result | Readout |
|---|---:|---:|---|
| MTS fixed vs LCDM, delta chi2 | -5.260 | -3.619 | MTS improves raw fit |
| MTS fixed vs LCDM, delta AIC | -3.260 | -1.619 | MTS wins AIC |
| MTS fixed vs LCDM, delta BIC | +2.141 | +3.781 | LCDM still wins BIC |
| MTS fixed vs wCDM, delta BIC | -0.169 | -0.382 | MTS slightly wins same-k comparison |
| MTS fixed vs CPL, delta BIC | -7.233 | -7.018 | MTS wins penalty-adjusted comparison |

Sign convention:

```text
negative delta = MTS fixed is better than the named baseline.
positive delta = baseline is better.
```

## Prior Edges

All score branches converged.

No prior-edge flags were raised.

The fitted memory amplitude was:

| Branch | B_mem |
|---|---:|
| DESI DR2 full-cov no-SH0ES | 0.074533 |
| DESI DR1 full-cov no-SH0ES | 0.073418 |

Release shift:

```text
-1.50 percent
```

That is useful because the branch did not survive by slamming into a prior wall.

## Control Check

The `MTS_Bmem_zero` branch collapses numerically onto LCDM in both releases.

That is exactly what we want from a negative control:

```text
the memory term is doing the extra work,
not a bookkeeping difference in the runner.
```

## Claim Gates

| Gate | Result | Meaning |
|---|---:|---|
| score paths exist | pass | all score/readout sources exist |
| scores written | pass | both score runs wrote fit summaries |
| all models converged | pass | LCDM, wCDM, CPL, and MTS branches converged |
| no prior-edge flags | pass | best fits are not boundary artifacts |
| MTS beats LCDM chi2 | pass | raw fit improves in both releases |
| MTS beats LCDM AIC | pass | AIC improves in both releases |
| MTS beats LCDM BIC | fail | LCDM still wins BIC penalty in both releases |
| MTS beats wCDM same-k | pass | MTS slightly beats wCDM with equal parameter count |
| MTS beats CPL AIC/BIC | pass | MTS beats CPL after parameter penalties |
| B_mem release stability | pass | B_mem shifts by less than 5 percent |
| stable evidence allowed | fail | short-smoke cannot support stable evidence language |

## Interpretation

This is not grim.

It is also not a knockout.

The clean readout is:

```text
MTS fixed is competitive under full-cov no-SH0ES.
It beats wCDM narrowly with equal parameter count.
It beats CPL by information criteria.
It improves LCDM raw chi2 and AIC.
It does not beat LCDM by BIC.
```

Boxing-card version:

```text
This is a Mayweather round, not a Tyson round.
MTS slipped the local-H0 pressure punch,
landed clean counters on wCDM/CPL,
but LCDM still stole the BIC card with fewer parameters.
```

## Derivation Consequence

This result makes the FLRW memory projection worth deriving, not claiming.

The next theory contract is now sharper:

```text
derive the sign,
derive the amplitude scale,
derive why the no-clock p=3, u3=1/4 branch exists,
prove B_mem -> 0 is the LCDM/background-GR limit,
or demote the branch to an empirical closure only.
```

The important fact is:

```text
B_mem is nonzero,
stable across DR2/DR1,
and not edge-driven.
```

So the derivation target is alive.

The evidence claim is not.

## Decision

Decision:

```text
MTS_fixed_survives_fullcov_noSH0ES_short_smoke_as_competitive_diagnostic_not_LCDM_BIC_win
```

Claim ceiling:

```text
short_smoke_late_time_background_diagnostic_only_no_stable_evidence_or_theory_promotion
```

Next action:

```text
derive or reject the FLRW memory projection amplitude contract,
then run the symmetric robustness matrix.
```

## Machine Artifacts

Script:

```text
scripts/fullcov_noSH0ES_score_readout.py
```

Score runs:

```text
runs/20260601-000140-cosmo-SN-BAO-short-smoke
runs/20260601-000141-cosmo-SN-BAO-short-smoke
```

Readout run:

```text
runs/20260601-000142-fullcov-noSH0ES-score-readout
```

Output files:

```text
runs/20260601-000142-fullcov-noSH0ES-score-readout/results/source_register.csv
runs/20260601-000142-fullcov-noSH0ES-score-readout/results/score_summary.csv
runs/20260601-000142-fullcov-noSH0ES-score-readout/results/MTS_fixed_vs_baselines.csv
runs/20260601-000142-fullcov-noSH0ES-score-readout/results/release_stability.csv
runs/20260601-000142-fullcov-noSH0ES-score-readout/results/prior_edge_audit.csv
runs/20260601-000142-fullcov-noSH0ES-score-readout/results/information_criteria_ruling.csv
runs/20260601-000142-fullcov-noSH0ES-score-readout/results/claim_gates.csv
runs/20260601-000142-fullcov-noSH0ES-score-readout/results/residual_plot_manifest.csv
runs/20260601-000142-fullcov-noSH0ES-score-readout/results/derivation_targets.csv
runs/20260601-000142-fullcov-noSH0ES-score-readout/results/decision.csv
```

Residual plots:

```text
runs/20260601-000142-fullcov-noSH0ES-score-readout/results/plots/DESI_DR2_fullcov_noSH0ES_SN_residuals.svg
runs/20260601-000142-fullcov-noSH0ES-score-readout/results/plots/DESI_DR2_fullcov_noSH0ES_BAO_residuals.svg
runs/20260601-000142-fullcov-noSH0ES-score-readout/results/plots/DESI_DR1_fullcov_noSH0ES_SN_residuals.svg
runs/20260601-000142-fullcov-noSH0ES-score-readout/results/plots/DESI_DR1_fullcov_noSH0ES_BAO_residuals.svg
```
