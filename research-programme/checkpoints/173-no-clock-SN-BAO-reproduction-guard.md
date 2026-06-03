# 173 - No-Clock SN+BAO Reproduction Guard

Private scorer checkpoint. This is not a public claim.

## 1. Trigger

Checkpoint 172 reproduced the BAO-only locked `2/27` result through the new
official-refresh runner.

This checkpoint expands one step:

```text
--mode reproduce --arena SN-BAO-T7 --assert-no-sidecar
```

It reproduces the existing SN+BAO locked-amplitude matrix without turning it
into a new full official likelihood.

## 2. Machine Artifact

Script:

```text
scripts/no_clock_official_likelihood_refresh.py
```

Reproduction scorer reused:

```text
scripts/canonical_R_two_ninth_T7_robustness.py
```

Fixed-amplitude helper reused:

```text
scripts/canonical_R_fixed_amplitude_scout.py
```

Run:

```text
runs/20260531-235959-no-clock-SN-BAO-reproduction-guard
```

Command:

```text
python scripts/no_clock_official_likelihood_refresh.py --mode reproduce --arena SN-BAO-T7 --assert-no-sidecar --timestamp 20260531-235959 --source-run runs/20260531-235959-no-clock-official-source-refresh --reference-tolerance 1e-8
```

Status:

```text
no_clock_SN_BAO_locked_2over27_reproduction_passed
```

Claim ceiling:

```text
SN_BAO_locked_2over27_reproduction_no_full_refresh_or_theory_promotion
```

## 3. What Was Scored

Lead branch:

```text
MTS_2over27_no_clock_u3quarter
```

Implementation alias:

```text
two_ninth_boundary_charge / MTS_locked_2over27
```

Fixed values:

```text
B_mem = 2/27
p = 3
u3 = 1/4
```

Fitted cosmological parameter:

```text
Omega_m
```

Nuisance treatment:

```text
same SN offset and BAO alpha machinery as the baseline source runs.
```

The pair-ruler sidecar was not scored.

## 4. Branch Matrix

| branch | SN rows | SN covariance | SN observable | BAO |
|---|---:|---|---|---|
| `T1_primary_fullcov_DR2` | 1624 | full | `mb-corr` | DESI DR2 |
| `T3_diagonal_fullsample_DR2` | 1624 | diagonal | `mb-corr` | DESI DR2 |
| `T4_small_fullcov_DR2` | 250 | full | `mb-corr` | DESI DR2 |
| `T5_SH0ES_pressure` | 250 | diagonal | `mu-sh0es` | DESI DR2 |
| `T5_matched_control` | 250 | diagonal | `mb-corr` | DESI DR2 |
| `T6_small_fullcov_DR1` | 250 | full | `mb-corr` | DESI DR1 |

This matrix is still SN+BAO only:

```text
no H(z),
no growth,
no CMB,
no perturbation calculation,
no local-GR derivation.
```

## 5. Gate Results

All reproduction gates passed:

| gate | status |
|---|---|
| manifest guard passed | pass |
| arena is SN+BAO locked matrix | pass |
| source branch artifacts present | pass |
| required branches scored | pass |
| sidecar absent | pass |
| locked branch fixed `B_mem = 2/27` | pass |
| locked branch not prior-edge | pass |
| all locked branches converged | pass |
| all branch gates pass | pass |
| prior edges reported for locked and baselines | pass |
| reference delta reproduced | pass |
| full refresh not run | pass |
| claim ceiling preserved | pass |

Failure count:

```text
failed_gates = 0
```

## 6. Reproduced Reference Deltas

The previous T7 locked-amplitude SN+BAO matrix was reproduced exactly within
the `1e-8` tolerance:

| branch | reproduced `ΔBIC` vs LCDM |
|---|---:|
| `T1_primary_fullcov_DR2` | -5.259466877748764 |
| `T3_diagonal_fullsample_DR2` | -7.956849125466192 |
| `T4_small_fullcov_DR2` | -2.1121258573889463 |
| `T5_SH0ES_pressure` | -2.1071017912585432 |
| `T5_matched_control` | -2.107119040036963 |
| `T6_small_fullcov_DR1` | -0.8525455130148885 |

Readout:

```text
The locked 2/27 no-clock branch reproduces the existing SN+BAO matrix and
remains competitive or better than LCDM by information criteria in all six
tested branches.
```

## 7. Flexible Baseline Fairness

The branch also keeps the Mayweather-style scorecard against flexible baselines:

| branch | vs `wCDM` `ΔBIC` | vs `CPL` `ΔBIC` | vs fitted-MTS `Δχ²` |
|---|---:|---:|---:|
| `T1_primary_fullcov_DR2` | -7.569629849695502 | -14.633513551191527 | 0.00019179382275069656 |
| `T3_diagonal_fullsample_DR2` | -8.221046547824244 | -15.251950176001401 | 0.4880379293573469 |
| `T4_small_fullcov_DR2` | -6.424944212530647 | -8.682036101051608 | 0.5428663481910974 |
| `T5_SH0ES_pressure` | -6.462100367075607 | -8.96018804576704 | 0.5385098663872299 |
| `T5_matched_control` | -6.461992143748915 | -8.95956992352626 | 0.5385246951522049 |
| `T6_small_fullcov_DR1` | -6.375718903084817 | -9.064805443647288 | 0.2843589124615278 |

Interpretation:

```text
The locked branch is not always the raw-chi2 minimum against every flexible
model, but it pays fewer parameters and wins the AIC/BIC card in this matrix.
```

That is exactly the fair-comparison logic: if flexible baselines throw extra
parameter haymakers, the scorecard still has to charge them for the swing.

## 8. Prior-Edge Discipline

The locked branch:

```text
locked Omega_m prior-edge flags = 0
```

Total reported prior rows:

```text
84
```

Flagged source-run prior edges:

```text
8
```

The flagged edges occur in flexible source-run branches, mainly `CPL.wa` and
some fitted-`u3` diagnostic rows. They do not belong to the locked `2/27`
branch.

This is important, because the guard now records edge pressure symmetrically:

```text
MTS does not get a free pass,
but flexible baselines and diagnostics do not get invisibility cloaks either.
```

## 9. What This Does Not Prove

This checkpoint does not prove:

```text
the final official likelihood,
independent prediction of B_mem = 2/27,
a CMB or growth pass,
the perturbation theory,
the local GR/PPN branch,
or the parent action.
```

It proves only:

```text
the official-refresh runner can reproduce the existing SN+BAO locked 2/27
matrix, with source artifacts present, baselines included, sidecar excluded,
prior edges recorded, and no full-refresh claim made.
```

## 10. Decision

Decision:

```text
no_clock_SN_BAO_locked_2over27_reproduction_passed
```

Boxing-card readout:

```text
This is a clean six-round technical scorecard, not a knockout.
The locked no-clock branch slips the flexible-baseline parameter tax and lands
enough clean counters to stay genuinely interesting.
```

## 11. Next Target

Create:

```text
174-no-clock-Hz-growth-reproduction-readiness.md
```

Next task:

```text
Before a broader official refresh, audit which existing H(z), growth/RSD, and
non-CMB holdout runs are clean enough to reproduce under the same guard
machinery, and which ones must remain diagnostic only.
```
