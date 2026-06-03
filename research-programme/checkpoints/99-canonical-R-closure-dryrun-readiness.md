# 99 — Canonical R Closure Dry-Run Readiness

## Verdict

`T0_dry_run_passed_primary_fit_not_started`.

The primary no-SH0ES full-covariance DESI DR2 scorecard branch is now ready for a proper `T1_clean_primary_fullcov` short-smoke run when compute time is available. No fit, model score, or evidence claim was generated in this pass.

## Important correction

The first T0 command at `runs/20260531-140113-cosmo-SN-BAO-closure-dryrun` passed candidate data discovery, but it did not preserve the exact branch settings in `run_config.json`. That was too loose for a serious checkpoint.

The runner was tightened so dry-runs now record the requested SN observable, covariance mode, sample size, calibrator policy, BAO label, and explicit data/covariance paths. The authoritative T0 is therefore:

`runs/20260531-140441-cosmo-SN-BAO-closure-dryrun`.

## Strict T0 command

```powershell
& "research-programme\.venv-score\Scripts\python.exe" "research-programme\scripts\cosmo_SN_BAO_closure_runner.py" --phase dry-run --sn-observable mb-corr --sn-covariance-mode full --sn-max-rows 0 --bao-label DESI_DR2_primary --sn-data "[local-formalization-workbench]\data\cosmology\pantheon_plus\Pantheon+SH0ES.dat" --sn-cov "[local-formalization-workbench]\data\cosmology\pantheon_plus\Pantheon+SH0ES_STAT+SYS.cov" --bao-data "[local-formalization-workbench]\data\cosmology\desi_dr2_bao\desi_gaussian_bao_ALL_GCcomb_mean.txt" --bao-cov "[local-formalization-workbench]\data\cosmology\desi_dr2_bao\desi_gaussian_bao_ALL_GCcomb_cov.txt"
```

## Frozen branch

| Setting | Value |
|---|---|
| SN observable | `mb-corr` |
| SN covariance | `full` |
| SN rows | `full` |
| Calibrators | excluded |
| BAO branch | `DESI_DR2_primary` |
| Scores written | `False` |
| Stable evidence allowed | `False` |

## Data shape gates

| Dataset | Path | Rows | Status |
|---|---:|---:|---|
| SN shape | `formalization-workbench/data/cosmology/pantheon_plus/Pantheon+SH0ES.dat` | 1701 | `schema_valid` |
| SN covariance | `formalization-workbench/data/cosmology/pantheon_plus/Pantheon+SH0ES_STAT+SYS.cov` | 1701 | `schema_valid` |
| BAO mean | `formalization-workbench/data/cosmology/desi_dr2_bao/desi_gaussian_bao_ALL_GCcomb_mean.txt` | 13 | `schema_valid` |
| BAO covariance | `formalization-workbench/data/cosmology/desi_dr2_bao/desi_gaussian_bao_ALL_GCcomb_cov.txt` | 13 | `schema_valid` |

## Readiness ledger

Readiness run:

`runs/20260531-140637-canonical-R-closure-dryrun-readiness`.

Outputs:

- `source_checkpoint_register.csv`
- `dryrun_artifact_register.csv`
- `data_shape_checks.csv`
- `command_safety_checks.csv`
- `readiness_gates.csv`
- `decision.csv`
- `status.json`

All blocking readiness gates passed: sources exist, dry-run artifacts match the no-score contract, data shapes pass, command branch is frozen, the status permits a next smoke run, and the required model matrix is declared.

## Claim ceiling

This branch remains `empirical_closure_scorecard_only`.

`MTS_fixed_p3_u3quarter` may be treated as `canonical_R_closure` only under that ceiling. It is not yet a derived field-theory prediction because `a_F=1`, the `R` normalization, the endpoint amplitude, and `B_mem` ownership remain closure debts.

## Next target

The next empirical step is `T1_clean_primary_fullcov`: run the no-SH0ES, full-sample, full-covariance, DESI DR2 short-smoke with fitted `LCDM`, `wCDM`, `CPL`, `canonical_R_closure`, and the `B_mem=0` control.

Suggested command, not yet run here:

```powershell
& "research-programme\.venv-score\Scripts\python.exe" "research-programme\scripts\cosmo_SN_BAO_closure_runner.py" --phase short-smoke --sn-observable mb-corr --sn-covariance-mode full --sn-max-rows 0 --bao-label DESI_DR2_primary --sn-data "[local-formalization-workbench]\data\cosmology\pantheon_plus\Pantheon+SH0ES.dat" --sn-cov "[local-formalization-workbench]\data\cosmology\pantheon_plus\Pantheon+SH0ES_STAT+SYS.cov" --bao-data "[local-formalization-workbench]\data\cosmology\desi_dr2_bao\desi_gaussian_bao_ALL_GCcomb_mean.txt" --bao-cov "[local-formalization-workbench]\data\cosmology\desi_dr2_bao\desi_gaussian_bao_ALL_GCcomb_cov.txt" --max-iter 120
```

Scorecard rule: a clean draw or narrow points result keeps MTS alive if it is edge-free and symmetric against the baselines. Edge hits, convergence failures, or a `B_mem=0` tie mean the closure is not carrying independent physical signal.
