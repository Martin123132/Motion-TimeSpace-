# 84 - Closure Test Runner Design

Private checkpoint. This is not a public claim.

## 1. Trigger

Checkpoint 83 created the empirical manifest and selected:

```text
cosmo_background_SN_BAO_short_smoke
```

with the rule:

```text
No result is allowed to skip amplitude policy, baseline comparison, residuals, and prior-edge diagnostics.
```

This checkpoint designs the runner before implementation.

## 2. Short Verdict

```text
closure_runner_design_status =
design_ready_runner_not_implemented
```

Next target:

```text
85-cosmo-SN-BAO-closure-runner-dryrun.md
```

Plain English:

```text
The first empirical runner should be a fresh audited wrapper, not a mutation of older growth/CMB scripts.
```

The next allowed execution is:

```text
dry_run_only
```

No scoring until schemas, amplitudes, baselines, and outputs are validated.

## 3. Runner Phases

| Phase | Purpose | Writes scores? |
|---|---|---:|
| dry-run manifest | validate data paths, schemas, model grid, amplitude policy, baseline parity, output directories | no |
| short smoke | fit minimal SN+BAO closure matrix with low iteration caps | yes |
| robustness matrix | wide/narrow priors, fitted `p/u3`, split tests, no-SH0ES branch | yes |
| promotion review | decide if any closure result is stable evidence | no |

Long robustness runs require:

```text
log.txt
status.json
COMPLETE.txt
```

No waiting around in the chat for hours.

## 4. Model Matrix

| Model | Role | Fixed factors | Fitted factors | Claim ceiling |
|---|---|---|---|---|
| `LCDM` | baseline | standard model form | `Omega_m`, nuisance/calibration | baseline |
| `wCDM` | baseline | constant-`w` form | `Omega_m`, `w`, nuisance/calibration | baseline |
| `CPL` | baseline | CPL form | `Omega_m`, `w0`, `wa`, nuisance/calibration | baseline |
| `MTS_fixed_p3_u3quarter` | primary closure | `p=3`, `u3=1/4` | `B_mem/b_mem`, `Omega_m`, nuisance/calibration | closure only |
| `MTS_fitted_p` | ablation | `u3=1/4` | `p`, `B_mem/b_mem`, `Omega_m`, nuisance/calibration | ablation only |
| `MTS_fitted_u3` | ablation | `p=3` | `u3`, `B_mem/b_mem`, `Omega_m`, nuisance/calibration | ablation only |
| `MTS_Bmem_zero` | negative control | `p=3`, `u3=1/4`, `B_mem=0` | `Omega_m`, nuisance/calibration | control |

The primary test is not allowed to hide behind a fitted transition shape.

## 5. Data Contracts

| Dataset | Dry-run requirement |
|---|---|
| SN shape | validate redshift/value/covariance or sigma/nuisance-offset columns |
| BAO distances | validate `z`, observable, value, covariance/sigma, survey tag |
| run config | freeze model grid, priors, fixed/fitted flags, baseline parity before scoring |

If data paths are missing, the runner must stop at dry-run and write a useful failure status.

## 6. Required Outputs

Every scoring run must produce:

```text
status.json
run_config.json
fit_summary.csv
amplitude_policy.csv
baseline_comparison.csv
residuals.csv
prior_edge_table.csv
```

Long runs additionally need:

```text
log.txt
COMPLETE.txt
```

`fit_summary.csv` must include:

```text
model, chi2, dof, k, n, AIC, BIC, convergence, prior_edge_flag, claim_ceiling
```

`baseline_comparison.csv` must include:

```text
same_data, same_nuisance, same_calibration, delta_chi2, delta_AIC, delta_BIC
```

## 7. Command Contract

Dry run:

```text
python scripts/cosmo_SN_BAO_closure_runner.py --phase dry-run --output-root runs
```

Short smoke:

```text
python scripts/cosmo_SN_BAO_closure_runner.py --phase short-smoke --max-iter 200 --output-root runs
```

Long robustness:

```text
python scripts/cosmo_SN_BAO_closure_runner.py --phase robustness --output-root runs *> runs/<timestamp>/log.txt
```

The long command is a design contract, not something to run yet.

## 8. Abort Conditions

The runner must abort or mark unstable if:

- data schemas fail;
- a model lacks a comparable baseline branch;
- `B_mem` hits a prior edge;
- residuals are not written;
- AIC/BIC cannot be computed with explicit `k` and `n`;
- MTS receives nuisance freedom that baselines do not receive;
- a closure result is described as field-theory proof.

This is the guardrail that keeps the test honest.

## 9. First Implementation Target

Create:

```text
scripts/cosmo_SN_BAO_closure_runner.py
```

First implementation should support:

```text
--phase dry-run
```

and write:

```text
status.json
run_config.json
amplitude_policy.csv
```

It should not score models yet.

Acceptance:

```text
dry-run validates data-path state, model matrix, amplitude policy, baseline fairness rules, and output directory creation.
```

## 10. Run Artifact

Script:

```text
research-programme\scripts\closure_test_runner_design.py
```

Run directory:

```text
research-programme\runs\20260531-122041-closure-test-runner-design
```

Generated tables:

```text
source_checkpoint_register.csv
runner_phases.csv
model_matrix.csv
data_contract.csv
output_artifacts.csv
command_contract.csv
decision.csv
```

Status readout:

```text
closure_runner_design_ready_runner_not_implemented
```

## 11. Next Target

Create:

```text
85-cosmo-SN-BAO-closure-runner-dryrun.md
```

and implement:

```text
scripts/cosmo_SN_BAO_closure_runner.py
```

dry-run mode only.

No fit claims yet.
