# 169 - No-Clock Lead Official Likelihood Refresh Plan

Private empirical planning checkpoint. This is not a public claim.

## 1. Trigger

Checkpoint 168 kept the pair-ruler half-kernel in the sidecar lane:

```text
half_kernel_contract_constructed_parent_ownership_not_proven
```

So the main empirical work now returns to the lead branch:

```text
MTS_2over27_no_clock_u3quarter
```

The task is not to make a bigger claim. The task is to make the next empirical
round harder to dismiss:

```text
same data,
same nuisance rules,
same priors,
same jackknifes,
same edge flags,
same punches for LCDM/wCDM/CPL.
```

## 2. Machine Artifact

Script:

```text
scripts/no_clock_lead_official_likelihood_refresh_plan.py
```

Run:

```text
runs/20260531-235959-no-clock-lead-official-likelihood-refresh-plan
```

Generated:

```text
source_register.csv
local_asset_audit.csv
official_source_targets.csv
refresh_stage_ladder.csv
branch_matrix.csv
baseline_fairness_contract.csv
artifact_contract.csv
dry_run_command_queue.csv
acceptance_gates.csv
decision.csv
status.json
```

Status:

```text
no_clock_lead_official_refresh_plan_locked
```

Claim ceiling:

```text
no_clock_official_likelihood_refresh_plan_no_theory_or_CMB_promotion
```

## 3. Current Source State

Local source audit:

```text
audited assets = 33
missing        = 0
hash failures  = 0
```

This means the current local source files are internally hash-locked against
the existing manifests.

It does not mean:

```text
full official likelihood wrapper implemented.
```

It means:

```text
the next source refresh can start from a clean local manifest rather than a
mystery pile of files.
```

## 4. Official Source Targets

| arena | source target | current local status | role |
|---|---|---|---|
| SN | Pantheon+SH0ES DataRelease | local hash-locked | primary SN full-covariance source |
| BAO | DESI DR2 products | local Cobaya mirror hash-locked | primary BAO target, official/mirror equivalence must be recorded |
| BAO | Cobaya `bao_data` DESI DR2 | local hash-locked | machine-readable mirror |
| BAO release sensitivity | DESI DR1/2024 BAO | local hash-locked | comparator only |
| H(z) | CC32 + Moresco CC15 | source-locked in checkpoint 145 | independent chronometer check |
| growth/RSD | SDSS/eBOSS DR16 likelihoods | source-locked in checkpoint 146 | growth/RSD covariance and ELG grid |
| CMB | Planck 2018 distance priors | diagnostic only | no promotion source |

External target URLs recorded in the machine output include:

```text
https://github.com/PantheonPlusSH0ES/DataRelease
https://data.desi.lbl.gov/doc/papers/dr2/
https://github.com/CobayaSampler/bao_data/tree/master/desi_bao_dr2
https://cluster.difa.unibo.it/astro/CC_data/
https://svn.sdss.org/public/data/eboss/DR16cosmo/tags/v1_0_1/likelihoods/
https://arxiv.org/abs/1808.05724
```

## 5. Lead Branch Matrix

The next scorecard should include:

| branch | role | rule |
|---|---|---|
| `LCDM` | baseline | same rows, nuisance freedoms, priors, and jackknifes |
| `wCDM` | baseline | same tests; edge hits demote evidence |
| `CPL` | flexible baseline | same tests; parameter penalty reported |
| `MTS_2over27_no_clock_u3quarter` | lead branch | `B_mem=2/27`, `u3=1/4`, no clock, no pair projection |
| `MTS_Bmem_zero` | negative control | checks that the effect is really from the frozen memory term |
| `MTS_pair_ruler_half_kernel` | frozen sidecar | excluded from lead refresh unless explicitly sidecar-labelled |

This prevents the two biggest failure modes:

```text
accidentally letting the pair-ruler sidecar rescue the lead branch;
accidentally letting baselines avoid the punches MTS has to take.
```

## 6. Refresh Stage Ladder

| stage | name | exit condition |
|---:|---|---|
| 0 | source manifest refresh | all required files hash-locked or explicitly deferred |
| 1 | schema/covariance preflight | rows, covariances, conventions, and positive-definite checks pass |
| 2 | single-arena reproduction | existing score signs reproduce or discrepancies are isolated |
| 3 | baseline-fair joint refresh | `chi2/AIC/BIC`, residuals, edge flags, and jackknifes written |
| 4 | official wrapper upgrade | wrapper dependency/reproducibility logs exist |
| 5 | long-run workflow | `runs/<timestamp>/log.txt`, `status.json`, and `DONE/FAILED` marker written |

The discipline is:

```text
do not jump straight to a big fit until the source-lock and reproduction gates pass.
```

## 7. Baseline Fairness Contract

Every future official-refresh runner must enforce:

| rule | evidence required |
|---|---|
| same rows and covariances | `row_manifest.csv`, `covariance_manifest.csv` |
| same nuisance freedom | `nuisance_policy.csv` |
| same priors and edge flags | `prior_edge_table.csv` |
| same jackknifes and splits | `jackknife_scorecard.csv` |
| draw threshold honesty | `baseline_comparisons.csv` |
| claim ceiling | `status.json` |

Hard rule:

```text
if a jackknife is a punch, everybody gets punched.
```

## 8. Planned Dry-Run Queue

The planner writes the future command queue but does not run the long jobs yet.

| step | label | status |
|---:|---|---|
| 1 | source refresh dry-run | planned next script |
| 2 | source refresh hash-lock | planned next script |
| 3 | single-arena reproduction | after source lock |
| 4 | baseline-fair refresh | long run from VS Code workflow |
| 5 | sidecar exclusion check | guardrail |

The next concrete script should be:

```text
scripts/no_clock_official_source_refresh.py
```

Its job is source-locking, schema/covariance preflight, and dry-run command
generation only.

## 9. Acceptance Gates

| gate | status | evidence |
|---|---|---|
| local assets hash-locked | pass | `missing=0`; `hash_fail=0`; `audited_assets=33` |
| official source targets named | pass | SN, BAO, H(z), growth/RSD, and CMB diagnostic targets listed |
| no-clock lead only | pass | pair-ruler sidecar excluded from lead scoring |
| baseline fairness contract | pass | same tests required for LCDM/wCDM/CPL/MTS |
| dry-run before long run | pass | command queue requires source-lock first |
| claim ceiling preserved | pass | no theory/CMB/local-GR/parent-action promotion |

## 10. Decision

Decision:

```text
no_clock_lead_official_refresh_plan_locked
```

Meaning:

```text
The local cosmology assets are clean enough to plan the official refresh.
The lead branch is no-clock MTS only.
The pair-ruler half-kernel stays frozen sidecar.
LCDM/wCDM/CPL must take the same punches.
No public/theory/CMB/local-GR promotion is made.
```

Boxing-card readout:

```text
We are not looking for a haymaker here.
We are setting up the clean judges' card:
same gloves, same ring, same rounds, same score sheet.
If MTS stays level or slightly ahead under that, that is exactly the kind of
win a field-theory challenger needs before the title fight.
```

## 11. Next Target

Create:

```text
170-no-clock-official-source-refresh-runner.md
```

and:

```text
scripts/no_clock_official_source_refresh.py
```

Task:

```text
implement the source-refresh/hash-lock/preflight runner for Pantheon+,
DESI BAO, CC H(z), and SDSS/eBOSS growth assets before any new fitting.
```

Pass condition:

```text
the runner writes source_hash_lock.csv, row_manifest.csv,
covariance_manifest.csv, branch_manifest.csv, dry-run commands, and status.json
without scoring a model.
```

Fail condition:

```text
new fits begin before source-lock, schema, covariance, and baseline-fairness
contracts are proven.
```
