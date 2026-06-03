# 86 - Cosmology SN+BAO Short-Smoke Contract

Private checkpoint. This is not a public claim.

## 1. Trigger

Checkpoint 85 implemented:

```text
scripts/cosmo_SN_BAO_closure_runner.py --phase dry-run
```

and produced:

```text
dry_run_pass_data_candidates_validated
```

This checkpoint freezes the short-smoke scoring contract before any fits are allowed.

## 2. Short Verdict

```text
short_smoke_contract_status =
contract_ready_runner_scoring_not_implemented
```

```text
scores_written =
false
```

```text
claim_status =
no_scores_no_evidence_yet
```

Plain English:

```text
The scoring gate is now specified, but the scoring code has not run.
```

## 3. Frozen Data Choice

Primary SN:

```text
[local-formalization-workbench]\data\cosmology\pantheon_plus\Pantheon+SH0ES.dat
```

Primary BAO:

```text
[local-formalization-workbench]\data\cosmology\desi_dr2_bao\desi_gaussian_bao_ALL_GCcomb_mean.txt
```

with covariance:

```text
[local-formalization-workbench]\data\cosmology\desi_dr2_bao\desi_gaussian_bao_ALL_GCcomb_cov.txt
```

Robustness BAO:

```text
[local-formalization-workbench]\data\cosmology\desi_dr1_bao\desi_2024_gaussian_bao_ALL_GCcomb_mean.txt
```

with covariance:

```text
[local-formalization-workbench]\data\cosmology\desi_dr1_bao\desi_2024_gaussian_bao_ALL_GCcomb_cov.txt
```

DESI DR2 is primary. DESI DR1 is robustness only unless explicitly selected.

## 4. Required Phase Order

1. explicit dry-run with the exact SN and DR2 BAO paths;
2. short smoke with low iteration cap;
3. DR1 robustness only after the DR2 short smoke exists;
4. no robustness claim until both baseline and MTS branches are run under the same rules.

The explicit dry-run command must come first:

```text
python scripts/cosmo_SN_BAO_closure_runner.py --phase dry-run --sn-data <SN_PATH> --bao-data <BAO_DR2_MEAN>
```

Short-smoke scoring command design:

```text
python scripts/cosmo_SN_BAO_closure_runner.py --phase short-smoke --sn-data <SN_PATH> --bao-data <BAO_DR2_MEAN> --bao-cov <BAO_DR2_COV> --max-iter 200
```

The short-smoke phase is not implemented yet.

## 5. Required Models

| Model | Role | Required? | Claim ceiling |
|---|---|---:|---|
| `LCDM` | baseline | yes | baseline |
| `wCDM` | baseline | yes | baseline |
| `CPL` | baseline | yes | baseline |
| `MTS_fixed_p3_u3quarter` | primary closure | yes | closure performance only |
| `MTS_Bmem_zero` | negative control | yes | control |
| `MTS_fitted_p` | ablation | optional if runtime allows, otherwise next | ablation only |
| `MTS_fitted_u3` | ablation | optional if runtime allows, otherwise next | ablation only |

No MTS result is allowed without `LCDM`, `wCDM`, and `CPL` in the same run.

## 6. Prior and Edge Rules

| Parameter | Rule |
|---|---|
| `Omega_m` | finite prior, e.g. `0.05 <= Omega_m <= 0.6` |
| `B_mem/b_mem` | explicit finite prior in `run_config.json` before scoring |
| fitted `p` | ablation prior, e.g. `1 <= p <= 6` |
| fitted `u3` | ablation prior, e.g. `0.05 <= u3 <= 1.0` |
| SN offset/nuisance | same analytic or fitted treatment for every model |

Any prior-edge hit blocks stable-evidence language.

## 7. Required Outputs

Short-smoke scoring must write:

```text
fit_summary.csv
baseline_comparison.csv
residuals.csv
prior_edge_table.csv
amplitude_policy.csv
status.json
```

`fit_summary.csv` must include:

```text
model, chi2_SN, chi2_BAO, chi2_total, dof, k, n, AIC, BIC, convergence, prior_edge_flag, claim_ceiling
```

`baseline_comparison.csv` must include:

```text
same_data, same_nuisance, same_calibration, delta_chi2, delta_AIC, delta_BIC
```

## 8. Abort Conditions

Abort or mark unstable if:

- explicit data dry-run has not passed;
- BAO mean/covariance shapes mismatch;
- any required baseline is missing;
- SN nuisance treatment is asymmetric;
- prior-edge behavior is unreported;
- any result is described as field-theory proof.

This is closure testing only.

## 9. Run Artifact

Script:

```text
research-programme\scripts\cosmo_SN_BAO_short_smoke_contract.py
```

Run directory:

```text
research-programme\runs\20260531-123311-cosmo-SN-BAO-short-smoke-contract
```

Generated tables:

```text
source_checkpoint_register.csv
frozen_data.csv
fit_phases.csv
model_policy.csv
priors.csv
required_outputs.csv
abort_conditions.csv
decision.csv
```

Status readout:

```text
SN_BAO_short_smoke_contract_ready_no_scores
```

## 10. Next Target

Create:

```text
87-cosmo-SN-BAO-short-smoke-implementation.md
```

and extend:

```text
scripts/cosmo_SN_BAO_closure_runner.py
```

to support:

```text
--phase short-smoke
```

Acceptance:

```text
run explicit dry-run first;
then run a short smoke only if explicit paths validate;
write all required artifacts;
do not make a field-theory claim from the result.
```
