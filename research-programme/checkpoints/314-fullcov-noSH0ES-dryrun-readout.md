# 314 - Full-Cov No-SH0ES Dry-Run Readout

Private empirical checkpoint. This is not a public cosmology, CMB, local-GR, galaxy, or parent-field-theory claim.

## Purpose

Checkpoint 313 froze the official/full-likelihood-style SN+BAO wrapper contract.

This checkpoint actually runs the first safe gate:

```text
Pantheon+ full covariance,
mb-corr shape branch,
calibrator-excluded no-SH0ES branch,
DESI DR2 and DESI DR1 release split,
dry-run only.
```

No fitting score is produced here.

## Runner Fix

The SN+BAO runner now accepts fixed run timestamps:

```text
--timestamp
```

That makes the workflow reproducible and lets future long jobs write predictable run folders without Codex waiting around.

The command repair from checkpoint 313 is preserved:

```text
--include-calibrators exists,
--exclude-calibrators does not exist,
no-SH0ES remains the default calibrator-excluded branch.
```

## Dry-Run Results

| Branch | Phase | SN Covariance | SN Observable | SN Rows | Calibrators | BAO Rows | Ready For Score | Scores Written |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| DESI DR2 full-cov no-SH0ES | dry-run | full | mb-corr | 1701 | excluded | 13 | yes | no |
| DESI DR1 full-cov no-SH0ES | dry-run | full | mb-corr | 1701 | excluded | 12 | yes | no |

Both dry-runs returned:

```text
dry_run_pass_data_candidates_validated
```

## Score Readiness Gates

| Gate | Result | Meaning |
|---|---:|---|
| source paths exist | pass | all dry-run, preflight, runner, and readout sources exist |
| runner timestamp patch active | pass | fixed timestamps work and no nonexistent calibrator flag is used |
| DR2 dry-run ready | pass | DR2 full-cov no-SH0ES data candidates validate |
| DR1 dry-run ready | pass | DR1 full-cov no-SH0ES data candidates validate |
| full SN covariance schema | pass | Pantheon+ full covariance validates at 1701 x 1701 |
| BAO covariance schema | pass | DR2 and DR1 BAO covariance files validate |
| no scores written | pass | dry-run phase created no fit scores |
| baseline parity present | pass | LCDM, wCDM, CPL, and MTS branches share data/nuisance policy |
| stable evidence allowed | fail | deliberate fail: dry-run cannot support evidence language |
| score commands ready | pass | short-smoke commands are prepared but not executed here |

## Derivation Consequence

This does not derive the MTS memory term.

It does something narrower but important:

```text
it locks the empirical judge that the next derivation must face.
```

If the no-clock branch with fixed closure structure survives both DR2 and DR1 under full covariance and no local-H0 calibration pressure, then the FLRW memory projection remains worth deriving.

If it fails badly or only survives by edge-hitting, then the current FLRW closure is demoted before we spend more theory effort defending it.

## Decision

Decision:

```text
fullcov_noSH0ES_DR1_DR2_dryruns_pass_score_ready_no_scores_written
```

Claim ceiling:

```text
fullcov_noSH0ES_dryrun_only_no_scores_or_stable_evidence
```

Meaning:

```text
the ring is clean,
the judges are symmetric,
the gloves fit,
but the bell has not rung yet.
```

## Next Score Commands

Exact short-smoke commands are written to:

```text
runs/20260601-000139-fullcov-noSH0ES-dryrun-readout/results/next_score_commands.csv
```

The intended order is:

```text
1. DESI DR2 full-cov no-SH0ES short-smoke
2. DESI DR1 full-cov no-SH0ES short-smoke
```

The score rule remains:

```text
no stable evidence claim from edge-hitting,
no MTS-only punishment,
same data and nuisance policy for LCDM, wCDM, CPL, and MTS.
```

## Machine Artifacts

Script:

```text
scripts/fullcov_noSH0ES_dryrun_readout.py
```

Dry-runs:

```text
runs/20260601-000137-cosmo-SN-BAO-closure-dryrun
runs/20260601-000138-cosmo-SN-BAO-closure-dryrun
```

Readout run:

```text
runs/20260601-000139-fullcov-noSH0ES-dryrun-readout
```

Output files:

```text
runs/20260601-000139-fullcov-noSH0ES-dryrun-readout/results/source_register.csv
runs/20260601-000139-fullcov-noSH0ES-dryrun-readout/results/dryrun_status_summary.csv
runs/20260601-000139-fullcov-noSH0ES-dryrun-readout/results/schema_summary.csv
runs/20260601-000139-fullcov-noSH0ES-dryrun-readout/results/model_matrix_check.csv
runs/20260601-000139-fullcov-noSH0ES-dryrun-readout/results/baseline_fairness_check.csv
runs/20260601-000139-fullcov-noSH0ES-dryrun-readout/results/runner_patch_check.csv
runs/20260601-000139-fullcov-noSH0ES-dryrun-readout/results/score_readiness_gates.csv
runs/20260601-000139-fullcov-noSH0ES-dryrun-readout/results/next_score_commands.csv
runs/20260601-000139-fullcov-noSH0ES-dryrun-readout/results/decision.csv
```
