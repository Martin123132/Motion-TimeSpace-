# 85 - Cosmology SN+BAO Closure Runner Dry-Run

Private checkpoint. This is not a public claim.

## 1. Trigger

Checkpoint 84 required:

```text
scripts/cosmo_SN_BAO_closure_runner.py
```

with:

```text
--phase dry-run
```

and no scoring.

The dry-run had to validate:

```text
data-path state;
model matrix;
amplitude policy;
baseline fairness rules;
output directory creation.
```

## 2. Short Verdict

```text
cosmo_SN_BAO_dryrun_status =
passed_after_schema_tightening
```

```text
scores_written =
false
```

```text
stable_evidence_allowed =
false
```

Plain English:

```text
The dry-run wrapper now exists and validates local SN plus DESI BAO candidate data,
but it still makes no physics/fit claim.
```

## 3. Important Correction

The first dry-run was too gullible.

It initially accepted readable config/status files as possible data candidates.

That was fixed before this checkpoint was accepted:

```text
candidate data now requires schema-compatible SN or BAO columns;
DESI BAO mean vectors require paired covariance validation.
```

This matters because it prevents a fake dry-run pass.

## 4. Final Dry-Run Artifact

Script:

```text
research-programme\scripts\cosmo_SN_BAO_closure_runner.py
```

Run directory:

```text
research-programme\runs\20260531-122858-cosmo-SN-BAO-closure-dryrun
```

Status readout:

```text
dry_run_pass_data_candidates_validated
```

## 5. Data Validation

Validated SN candidate:

```text
[local-formalization-workbench]\data\cosmology\pantheon_plus\Pantheon+SH0ES.dat
```

Rows:

```text
1701
```

Validated BAO candidates:

```text
[local-formalization-workbench]\data\cosmology\desi_dr1_bao\desi_2024_gaussian_bao_ALL_GCcomb_mean.txt
```

with paired covariance:

```text
[local-formalization-workbench]\data\cosmology\desi_dr1_bao\desi_2024_gaussian_bao_ALL_GCcomb_cov.txt
```

and:

```text
[local-formalization-workbench]\data\cosmology\desi_dr2_bao\desi_gaussian_bao_ALL_GCcomb_mean.txt
```

with paired covariance:

```text
[local-formalization-workbench]\data\cosmology\desi_dr2_bao\desi_gaussian_bao_ALL_GCcomb_cov.txt
```

This is enough for a next dry-run with explicit paths, then a short smoke.

## 6. Model Matrix Frozen

The dry-run froze seven branches:

| Model | Role | Claim ceiling |
|---|---|---|
| `LCDM` | baseline | baseline |
| `wCDM` | baseline | baseline |
| `CPL` | baseline | baseline |
| `MTS_fixed_p3_u3quarter` | primary closure | closure performance only |
| `MTS_fitted_p` | ablation | closure ablation only |
| `MTS_fitted_u3` | ablation | closure ablation only |
| `MTS_Bmem_zero` | negative control | control |

No local-GR or field-theory claim is allowed from this runner.

## 7. Outputs Created

The dry-run wrote:

```text
status.json
run_config.json
results/model_matrix.csv
results/amplitude_policy.csv
results/baseline_fairness.csv
results/data_schema_report.csv
results/output_contract.csv
```

It did not write:

```text
fit_summary.csv
baseline_comparison.csv
residuals.csv
prior_edge_table.csv
```

because those belong to the short-smoke scoring phase.

## 8. Next Gate

Next target:

```text
86-cosmo-SN-BAO-short-smoke-contract.md
```

Purpose:

```text
Implement or specify the short-smoke scoring phase using explicit SN and BAO paths, low iteration caps, and the required audit outputs.
```

Acceptance before scoring:

```text
rerun dry-run with explicit --sn-data and --bao-data paths;
freeze whether DR1 or DR2 BAO is primary;
write fit_summary, baseline_comparison, residuals, and prior_edge_table;
do not call any result field-theory evidence.
```
