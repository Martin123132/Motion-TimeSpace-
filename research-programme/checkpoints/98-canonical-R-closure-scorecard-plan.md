# 98 - Canonical R Closure Scorecard Plan

Private checkpoint. This is not a public claim.

## 1. Trigger

Checkpoint 97 demoted:

```text
a_F = 1
```

to:

```text
explicit canonical closure for empirical testing.
```

This checkpoint turns that demotion into a fair empirical scorecard plan.

## 2. Short Verdict

```text
scorecard_plan_status =
canonical_R_closure_scorecard_plan_written
```

```text
runs_started =
false
```

```text
promotion_allowed =
false
```

Plain English:

```text
The branch is now testable without pretending the amplitude is derived. The existing runner model MTS_fixed_p3_u3quarter is the numerical proxy for canonical_R_closure, provided every result is labelled as empirical closure only.
```

Boxing-score version:

```text
We are back on the cards. No fake belt, no stolen round: clean scoring, fair opponents, and the amplitude debt written on the gloves.
```

## 3. Machine Artifact

Script:

```text
research-programme\scripts\canonical_R_closure_scorecard_plan.py
```

Run:

```text
research-programme\runs\20260531-135654-canonical-R-closure-scorecard-plan
```

Generated:

```text
source_checkpoint_register.csv
canonical_branch_policy.csv
fair_retest_matrix.csv
scorecard_rules.csv
dry_run_and_fit_commands.csv
claim_language_guardrails.csv
acceptance_gates.csv
decision.csv
status.json
```

Status:

```text
canonical_R_closure_scorecard_plan_written
```

## 4. Branch Alias

The empirical branch label is:

```text
canonical_R_closure
```

The current numerical runner model is:

```text
MTS_fixed_p3_u3quarter
```

The alias is valid only with this claim ceiling:

```text
empirical_closure_scorecard_only
```

Fixed or conditionally fixed choices:

```text
p = 3
u3 = 1/4
eta = 1
a_F = 1
```

Fitted quantities:

```text
Omega_m
B_mem
SN nuisance offset/calibration
```

Closure debt:

```text
a_F=1 is canonical convention;
R unit scale is not parent-derived;
DeltaR is read from fitted B_mem;
B_mem remains fitted amplitude.
```

## 5. Retest Matrix

| Test | Priority | SN | Covariance | Rows | BAO | Purpose |
|---|---:|---|---|---|---|---|
| `T0_dry_run_shape_check` | 0 | no-SH0ES `mb-corr` | full | full | DR2 | data/config preflight |
| `T1_clean_primary_fullcov` | 1 | no-SH0ES `mb-corr` | full | full | DR2 | main scorecard |
| `T2_clean_primary_with_ablations` | 2 | no-SH0ES `mb-corr` | full | full | DR2 | fixed branch vs shape rescue |
| `T3_diagonal_covariance_sensitivity` | 3 | no-SH0ES `mb-corr` | diagonal | full | DR2 | covariance sensitivity |
| `T4_small_sample_reproduction` | 4 | no-SH0ES `mb-corr` | full | 250 | DR2 | old short-smoke reproduction |
| `T5_SH0ES_pressure_branch` | 5 | SH0ES `mu-sh0es` | diagonal | 250 | DR2 | local-H0 pressure stress |
| `T6_BAO_release_sensitivity` | 6 | no-SH0ES `mb-corr` | full | 250 | DR1 | BAO release sensitivity |

Primary empirical branch:

```text
T1_clean_primary_fullcov
```

Reason:

```text
no-SH0ES full-sample full-covariance DR2 is the cleanest background scorecard.
```

## 6. Scorecard Rules

The branch must always be scored against:

```text
fitted LCDM
fitted wCDM
fitted CPL
```

Report:

```text
Delta chi2
Delta AIC
Delta BIC
prior-edge flags
convergence flags
```

Rules:

| Rule | Requirement |
|---|---|
| primary baselines | score against fitted `LCDM`, `wCDM`, and `CPL` |
| information criteria | report chi2, AIC, and BIC deltas |
| edge flags | MTS edge hit blocks stable-evidence language |
| baseline flags | baseline edge hits are recorded too |
| full covariance | no-SH0ES full-covariance full sample is primary |
| amplitude ceiling | `B_mem -> DeltaR=3B_mem` is bookkeeping only |
| close rounds | draws and narrow points rounds keep the branch alive if edge-free |

## 7. Claim Guardrails

Allowed:

```text
canonical_R_closure is an edge-free labelled closure branch if the fit converges away from priors.
```

Forbidden:

```text
canonical_R_closure is a derived field-theory prediction.
```

Allowed:

```text
B_mem can be translated to DeltaR=3B_mem under eta=1,a_F=1 for theorem-target bookkeeping.
```

Forbidden:

```text
MTS predicts DeltaR or B_mem from the parent action.
```

Allowed:

```text
AIC/BIC wins over wCDM/CPL can be called clean/style points wins if edge-free.
```

Forbidden:

```text
MTS has beaten cosmology.
```

## 8. Acceptance Gates

| Gate | Required result | Blocks if failed |
|---|---|---|
| `data_shapes_pass` | dry-run passes for primary branch | yes |
| `primary_models_converge` | `LCDM`, `wCDM`, `CPL`, canonical branch, and zero-memory control converge | yes |
| `canonical_branch_non_edge` | canonical branch has no prior-edge flag | yes |
| `scorecard_complete` | deltas reported against all three baselines | yes |
| `amplitude_debt_label_present` | all prose says fitted amplitude/closure | yes |
| `future_theory_target_recorded` | `B_mem` translated to `DeltaR` only as target | no |

## 9. Dry-Run and Fit Commands

Dry-run first:

```powershell
& "research-programme\.venv-score\Scripts\python.exe" "research-programme\scripts\cosmo_SN_BAO_closure_runner.py" --phase dry-run --sn-observable mb-corr --sn-covariance-mode full --sn-max-rows 0 --bao-label DESI_DR2_primary
```

Primary full-covariance fit:

```powershell
& "research-programme\.venv-score\Scripts\python.exe" "research-programme\scripts\cosmo_SN_BAO_closure_runner.py" --phase short-smoke --sn-observable mb-corr --sn-covariance-mode full --sn-max-rows 0 --bao-label DESI_DR2_primary --max-iter 120
```

Primary full-covariance ablations:

```powershell
& "research-programme\.venv-score\Scripts\python.exe" "research-programme\scripts\cosmo_SN_BAO_closure_runner.py" --phase short-smoke --sn-observable mb-corr --sn-covariance-mode full --sn-max-rows 0 --bao-label DESI_DR2_primary --include-mts-ablations --max-iter 120
```

These commands were generated but not run.

## 10. Decision

Decision:

```text
next_work_status =
canonical_R_closure_scorecard_plan_written
```

Decision:

```text
primary_empirical_branch =
no_SH0ES_full_sample_full_covariance_DR2
```

Decision:

```text
branch_alias =
MTS_fixed_p3_u3quarter numeric model is canonical_R_closure when claim ceiling is enforced.
```

Decision:

```text
claim_ceiling =
empirical_closure_scorecard_only
```

## 11. Next Target

Create:

```text
99-canonical-R-closure-dryrun-readiness.md
```

Purpose:

```text
run T0 dry-run only, confirm data shapes and command safety, then decide whether to launch the longer primary full-covariance fit.
```

Do not start the long fit until:

```text
T0 dry-run passes;
the expected runtime/output path is clear;
and the result will write a new run directory instead of overwriting old evidence.
```
