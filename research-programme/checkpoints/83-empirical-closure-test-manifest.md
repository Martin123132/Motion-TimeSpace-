# 83 - Empirical Closure Test Manifest

Private checkpoint. This is not a public claim.

## 1. Trigger

Checkpoint 82 found:

```text
amplitude_gate_status =
no_amplitude_fully_parent_derived
```

and required:

```text
Every future empirical test must say which factors are fixed, fitted, ablated, bounded, or diagnostic.
Baselines must be tested fairly where comparable.
No closure result is treated as field-theory proof.
```

This checkpoint turns that into a test manifest.

## 2. Short Verdict

```text
empirical_manifest_status =
test_contract_ready_not_yet_executed
```

Primary next test:

```text
cosmo_background_SN_BAO_short_smoke
```

Claim ceiling:

```text
closure_testing_only
```

Plain English:

```text
We are now allowed to test closures,
but every test must declare its amplitude freedoms and fair baselines.
```

## 3. Test Arenas

| Test ID | Arena | MTS variant | Baselines | Claim ceiling |
|---|---|---|---|---|
| `cosmo_background_SN_BAO` | cosmology background | C2 `p=3`, `u3=1/4`, fitted `B_mem` | `LambdaCDM`, `wCDM`, `CPL` | closure performance only |
| `cosmo_growth_CMB_distance_proxy` | growth/distance | regularized memory closure | same calibration freedom baselines | closure stress test only |
| `galaxy_rotation_reference` | galaxy dynamics | labelled galaxy closure only | Newtonian baryonic, implemented empirical baselines, MOND-style if fair | empirical pillar only |
| `local_PPN_residual_bound` | local gravity | `A_loc/q_loc` bound only | GR PPN | constraint only |
| `EM_time_extension_preflight` | EM/time | no unified claim before units/equations audit | Maxwell/SR/standard clocks | preflight only |

This keeps galaxy work as one empirical pillar, not the whole theory.

## 4. Amplitude Policy

| Factor | Default policy | Required ablation | Failure flag |
|---|---|---|---|
| `p=3` | fixed primary | fitted `p` | fixed `p` materially worse without theory gain |
| `u3=1/4` | fixed primary | fitted `u3` and inherited C2 `u3` | quarter lock breaks under splits/refits |
| `B_mem/b_mem` | fitted with explicit priors | wide/narrow priors, zero-memory, split fits | prior edge or split instability |
| `C_coh` | diagnostic only | `C_coh` off/nonselector closure | hidden selector dependence |
| `A_loc/q_loc` | bound only | GR limit with residual set to zero | needs nonzero local residual to fit |

The most dangerous item remains:

```text
B_mem / b_mem
```

It must never be frozen silently.

## 5. Baseline Fairness Rules

| Rule | Requirement |
|---|---|
| same data splits | MTS and baselines use identical train/holdout/jackknife splits |
| same nuisance freedom | do not give one side extra nuisance freedom without accounting for it |
| same calibration branch | no-SH0ES or calibration-free branches must be comparable |
| symmetric failure reporting | if MTS and baseline both fail a jackknife, flag pipeline/data sensitivity |
| no claims from edge hits | prior-edge best fits are unstable, not evidence |

This directly fixes the earlier worry:

```text
If a test breaks MTS, check whether it also breaks the baseline.
```

Otherwise the test might be measuring the pipeline, not the theory.

## 6. Required Output Artifacts

Every quantitative run must produce:

| Artifact | Required contents |
|---|---|
| `fit_summary.csv` | model, arena, chi2, dof, AIC, BIC, convergence, prior-edge flag, claim ceiling |
| `amplitude_policy.csv` | factor, fixed/fitted/ablated status, prior, best fit, split variation |
| `baseline_comparison.csv` | same-data, same-nuisance, same-calibration checks, delta chi2/AIC/BIC |
| `residuals.csv` | observed, predicted, residual, model, observable coordinate |
| `status.json` | readout, stable evidence flag, failures, next action |

No run is allowed to be just:

```text
it looks better.
```

It needs audit outputs.

## 7. First Test Contract

First short smoke target:

```text
cosmo_background_SN_BAO
```

Primary MTS closure:

```text
F(N)=1-exp[-(N/(1/4))^3]
B_mem fitted with explicit priors
```

Required ablations:

```text
fitted p
fitted u3
B_mem = 0
wide/narrow B_mem priors
```

Required baselines:

```text
LambdaCDM
wCDM
CPL
```

Required diagnostics:

```text
chi2
AIC
BIC
residuals
prior-edge table
data-split stability
```

Claim ceiling:

```text
closure_performance_only
```

## 8. What This Does Not Claim

This manifest does not claim:

```text
MTS beats GR.
MTS derives local GR.
MTS has a fundamental scalar action.
MTS has parent-derived amplitude normalization.
```

It claims only:

```text
The next empirical tests can now be run without hiding amplitude freedom or unfair baseline handling.
```

That is a real upgrade.

## 9. Run Artifact

Script:

```text
research-programme\scripts\empirical_closure_test_manifest.py
```

Run directory:

```text
research-programme\runs\20260531-121628-empirical-closure-test-manifest
```

Generated tables:

```text
source_checkpoint_register.csv
test_manifest.csv
amplitude_policy.csv
baseline_fairness.csv
output_contract.csv
decision.csv
```

Status readout:

```text
empirical_closure_manifest_ready_not_executed
```

## 10. Next Target

Create:

```text
84-closure-test-runner-design.md
```

or implement the first short runner if the needed local data/script path is clear.

Acceptance:

```text
Dry-run first.
No long execution without script/log/status output.
No result is allowed to skip amplitude policy, baseline comparison, residuals, and prior-edge diagnostics.
```
