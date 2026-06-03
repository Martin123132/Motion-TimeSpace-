# 284 - Generic BAO Manifest Repair Readout

Private empirical-readiness checkpoint. This is not a public cosmology, CMB, local-GR, or parent-field-theory claim.

## Purpose

Checkpoint 282 found:

```text
generic SN+BAO dry-run blocked by BAO_distance_data_not_validated.
```

But checkpoint 283 proved the fixed-vs-kappa runner already had valid local paths for:

```text
Pantheon+ / SH0ES SN
DESI DR2 BAO mean + covariance
DESI DR1 BAO mean + covariance
```

This checkpoint repairs the generic runner so it can find those same validated files before falling into source-intake grid files.

## Code Change

Patched:

```text
scripts/cosmo_SN_BAO_closure_runner.py
```

Change:

```text
candidate_files()
```

now prioritizes known formalization-workbench files:

```text
formalization-workbench/data/cosmology/pantheon_plus/Pantheon+SH0ES.dat
formalization-workbench/data/cosmology/desi_dr2_bao/desi_gaussian_bao_ALL_GCcomb_mean.txt
formalization-workbench/data/cosmology/desi_dr1_bao/desi_2024_gaussian_bao_ALL_GCcomb_mean.txt
```

before scanning broader `post-checkpoint-work/source-intake`.

That fixes the actual failure mode:

```text
source-intake BAO grid likelihood files were being considered before the validated DESI mean/cov pairs.
```

## Machine Artifact

Readout script:

```text
scripts/generic_BAO_manifest_repair_readout.py
```

Run:

```text
runs/20260601-000107-generic-BAO-manifest-repair-readout
```

Status:

```text
generic_SN_BAO_runner_BAO_manifest_repaired_dryrun_passes_no_scores
```

Claim ceiling:

```text
schema_repair_and_dryrun_only_no_empirical_support_claim
```

## Before / After

Before repair:

```text
runs/20260601-093239-cosmo-SN-BAO-closure-dryrun
readout = dry_run_incomplete_missing_or_unvalidated_data
failure = BAO_distance_data_not_validated
```

Explicit-path validation:

```text
runs/20260601-094538-cosmo-SN-BAO-closure-dryrun
readout = dry_run_pass_data_candidates_validated
data_ready_for_short_smoke = true
```

After patch, auto-discovery validation:

```text
runs/20260601-094657-cosmo-SN-BAO-closure-dryrun
readout = dry_run_pass_data_candidates_validated
data_ready_for_short_smoke = true
```

## Schema Readout

Auto-discovery now validates:

```text
SN_shape:
Pantheon+SH0ES.dat
rows = 1701
schema_status = schema_valid
```

```text
BAO_distances:
desi_gaussian_bao_ALL_GCcomb_mean.txt
rows = 13
schema_status = schema_valid
paired covariance validated
```

```text
BAO_distances:
desi_2024_gaussian_bao_ALL_GCcomb_mean.txt
rows = 12
schema_status = schema_valid
paired covariance validated
```

Source-intake eBOSS grid files may still appear as schema mismatches, but they are no longer blocking because the validated DESI BAO candidates are seen first.

## Gate Results

| Gate | Result |
|---|---|
| pre-repair failure reproduced | pass |
| explicit DESI DR2 paths validate | pass |
| auto-discovery prioritizes DESI | pass |
| scores generated | fail / no |
| short-smoke ready | pass |

So the generic SN+BAO pipeline is now ready for controlled short-smoke and robustness work.

## What This Does and Does Not Mean

Allowed:

```text
generic SN+BAO schema blocker is repaired.
validated local Pantheon+/DESI paths are wired into discovery.
generic short-smoke / no-SH0ES / DESI release robustness can be attempted.
```

Not allowed:

```text
new empirical support claim.
CMB claim.
parent-action claim.
local-GR claim.
```

No scores were generated in this checkpoint.

## Output Files

```text
runs/20260601-000107-generic-BAO-manifest-repair-readout/results/source_register.csv
runs/20260601-000107-generic-BAO-manifest-repair-readout/results/run_status_matrix.csv
runs/20260601-000107-generic-BAO-manifest-repair-readout/results/schema_readout.csv
runs/20260601-000107-generic-BAO-manifest-repair-readout/results/gate_results.csv
runs/20260601-000107-generic-BAO-manifest-repair-readout/results/next_actions.csv
runs/20260601-000107-generic-BAO-manifest-repair-readout/results/decision.csv
```

## Next Step

Now allowed:

```text
generic SN+BAO short smoke
no-SH0ES shape branch
DESI DR1 vs DR2 release robustness
```

Recommended next:

```text
run generic SN+BAO short smoke first,
then no-SH0ES,
then DESI release robustness.
```

