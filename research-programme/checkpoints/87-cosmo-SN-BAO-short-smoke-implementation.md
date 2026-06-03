# 87 - Cosmology SN+BAO Short-Smoke Implementation

Private checkpoint. This is not a public claim.

## 1. Trigger

Checkpoint 86 froze the short-smoke contract:

```text
run explicit dry-run first;
then run a short smoke only if explicit paths validate;
write all required artifacts;
do not make a field-theory claim from the result.
```

This checkpoint records the first implemented scoring pass.

## 2. Short Verdict

```text
short_smoke_status =
implemented_and_scored_but_unstable
```

```text
scores_written =
true
```

```text
stable_evidence_allowed =
false
```

Plain English:

```text
The runner now scores SN+BAO against fair baselines, and the first usable short smoke gives a reviewable signal, but it is not evidence because a baseline prior edge is hit.
```

## 3. Implemented Runner Capability

Extended:

```text
research-programme\scripts\cosmo_SN_BAO_closure_runner.py
```

with:

- `--phase short-smoke`;
- Pantheon+ whitespace-table parsing;
- DESI BAO mean/covariance parsing;
- shared analytic SN magnitude-offset nuisance;
- shared analytic BAO scale nuisance;
- fitted `LCDM`, `wCDM`, `CPL`, `MTS_fixed_p3_u3quarter`, and `MTS_Bmem_zero`;
- `fit_summary.csv`, `baseline_comparison.csv`, `residuals.csv`, `prior_edge_table.csv`, `amplitude_policy.csv`, and `status.json`;
- fast background distance integration by grid/interpolation rather than one quadrature call per datum.

No scoring artifact is written outside `post-checkpoint-work`.

## 4. Explicit Dry-Run Gate

Dry-run artifact:

```text
research-programme\runs\20260531-123839-cosmo-SN-BAO-closure-dryrun
```

Readout:

```text
dry_run_pass_data_candidates_validated
```

The explicit data gate passed before scoring.

## 5. Latest Short-Smoke Run

Run artifact:

```text
research-programme\runs\20260531-124544-cosmo-SN-BAO-short-smoke
```

Status:

```text
short_smoke_scores_written_unstable
```

Failure flags:

```text
prior_edge_flags_present
```

Data validated:

| Dataset | Rows | Status |
|---|---:|---|
| Pantheon+ SN shape table | 1701 | schema valid |
| DESI DR2 BAO mean vector | 13 | schema valid with paired covariance |

Scored sample:

```text
SN rows used = 250
BAO rows used = 13
total residual rows written = 1315
```

## 6. Fit Summary

| Model | chi2 total | AIC | BIC | Converged | Prior edge | Claim ceiling |
|---|---:|---:|---:|---:|---:|---|
| `LCDM` | 130.308367 | 136.308367 | 147.024829 | yes | no | baseline |
| `wCDM` | 129.091212 | 137.091212 | 151.379828 | yes | no | baseline |
| `CPL` | 126.017145 | 136.017145 | 153.877915 | yes | yes | baseline |
| `MTS_fixed_p3_u3quarter` | 127.662755 | 135.662755 | 149.951372 | yes | no | closure performance only |
| `MTS_Bmem_zero` | 130.308367 | 136.308367 | 147.024829 | yes | no | control |

The zero-memory control collapses to `LCDM`, which is a useful sanity check.

## 7. Prior-Edge Finding

The prior-edge issue is not from the primary fixed-MTS branch:

| Model | Parameter | Best fit | Prior | Edge flag |
|---|---|---:|---|---:|
| `CPL` | `wa` | -2.0 | [-2.0, 2.0] | yes |
| `MTS_fixed_p3_u3quarter` | `B_mem` | 0.138740 | [-1.0, 1.0] | no |

This is still enough to block stable-evidence language, because a fair baseline is trying to run off the allowed space.

## 8. Baseline Comparisons

Primary fixed-MTS branch:

| Reference | Delta chi2 | Delta AIC | Delta BIC | Readout |
|---|---:|---:|---:|---|
| `LCDM` | -2.645612 | -0.645612 | +2.926542 | small chi2/AIC improvement, BIC penalty |
| `wCDM` | -1.428456 | -1.428456 | -1.428456 | small improvement |
| `CPL` | +1.645610 | -0.354390 | -3.926544 | worse chi2 than CPL, lower AIC/BIC because fewer parameters |

This is interesting enough to keep testing, but not clean enough to promote.

## 9. Amplitude Policy Result

| Factor | Treatment | Best fit | Edge flag | Role |
|---|---|---:|---:|---|
| `p=3` | fixed primary | fixed | no | fixed-vs-fitted-p ablation still required |
| `u3=1/4` | fixed primary | fixed | no | fixed-vs-fitted-u3 ablation still required |
| `B_mem/b_mem` | fitted with explicit prior | 0.138740 | no | dangerous amplitude |
| `Ccoh` | diagnostic only | not scored | not scored | local selector off |
| `A_loc/q_loc` | bound only | not scored | not scored | local residual constraint |

## 10. Interpretation Gate

Allowed statement:

```text
The short-smoke implementation is now working, all required CSVs are written, the primary fixed-MTS branch converges without its own prior edge, and the result is worth robustness follow-up.
```

Forbidden statement:

```text
MTS is preferred by SN+BAO.
```

Reason:

```text
CPL hits wa = -2.0, the run uses a short sampled SN subset, and p/u3 ablations have not been run.
```

## 11. Next Target

Create:

```text
88-cosmo-SN-BAO-prior-edge-review.md
```

and run a stability review that does only:

1. widen/narrow the CPL `wa` prior;
2. repeat the same short smoke with identical data/nuisance rules;
3. add `MTS_fitted_p` and `MTS_fitted_u3` only if runtime stays manageable;
4. keep the output private and explicitly unstable unless the edge behavior disappears.

Acceptance:

```text
no MTS preference claim unless LCDM/wCDM/CPL baselines are stable under the same priors, same data, and same nuisance treatment.
```
