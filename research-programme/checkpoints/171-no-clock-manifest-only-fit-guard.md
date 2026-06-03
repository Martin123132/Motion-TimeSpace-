# 171 - No-Clock Manifest-Only Fit Guard

Private scorer-guard checkpoint. This is not a public claim.

## 1. Trigger

Checkpoint 170 passed the source-refresh preflight:

```text
no_clock_official_source_refresh_preflight_passed
```

The next risk is obvious:

```text
starting a fit before the scorer itself proves it is respecting the source,
row, covariance, branch, nuisance, prior-edge, and sidecar-exclusion contracts.
```

This checkpoint implements the first mode of the future scorer:

```text
--mode manifest-only --assert-no-sidecar
```

It does not fit models.

## 2. Machine Artifact

Script:

```text
scripts/no_clock_official_likelihood_refresh.py
```

Run:

```text
runs/20260531-235959-no-clock-manifest-only-fit-guard
```

Command:

```text
python scripts/no_clock_official_likelihood_refresh.py --mode manifest-only --assert-no-sidecar --timestamp 20260531-235959 --source-run runs/20260531-235959-no-clock-official-source-refresh
```

Generated:

```text
source_register.csv
source_artifact_contract.csv
source_status_guard.csv
source_hash_guard.csv
row_contract_guard.csv
covariance_contract_guard.csv
branch_contract_guard.csv
nuisance_contract_guard.csv
prior_edge_contract.csv
scoring_refusal_policy.csv
guard_gates.csv
decision.csv
status.json
DONE.txt
```

Status:

```text
no_clock_manifest_only_fit_guard_passed
```

Claim ceiling:

```text
manifest_only_guard_no_model_scoring_or_theory_promotion
```

## 3. What The Guard Proves

The guard checks that the source-refresh run has:

```text
passed status,
DONE marker,
no model scoring,
sidecar excluded,
required artifacts present,
clean source hashes,
row contracts,
covariance contracts,
branch contracts,
nuisance contracts.
```

It then writes the missing pre-score contract:

```text
prior_edge_contract.csv
```

This is not a fitted prior-edge table. It is the mandatory contract saying:

```text
when scoring begins, every included branch must write branch, parameter,
best_fit, lower_bound, upper_bound, edge_distance, and edge_flag.
```

So flexible baselines do not get a free pass if they hit an edge, and MTS does
not get to ignore edge pressure either.

## 4. Guard Results

All guard gates passed:

| gate | status |
|---|---|
| source run status | pass |
| source artifacts present | pass |
| source hashes clean | pass |
| row contracts present | pass |
| covariance contracts pass | pass |
| branch contracts pass | pass |
| nuisance contracts present | pass |
| prior-edge contract written | pass |
| mode is manifest-only | pass |
| no model scoring | pass |
| claim ceiling preserved | pass |

Failure count:

```text
failed_gates = 0
```

## 5. Branch Guard

The guard requires:

| branch | required policy | result |
|---|---|---|
| `LCDM` | included | pass |
| `wCDM` | included | pass |
| `CPL` | included | pass |
| `MTS_2over27_no_clock_u3quarter` | included | pass |
| `MTS_Bmem_zero` | included | pass |
| `MTS_pair_ruler_half_kernel` | excluded | pass |

This matters because it blocks a quiet failure mode:

```text
using the pair-ruler sidecar to improve the lead no-clock branch.
```

The sidecar is still useful physics work, but it is not allowed into this
empirical lead refresh.

## 6. Refusal Policy

The script currently allows only:

```text
manifest-only
```

It explicitly refuses:

```text
reproduce
full-refresh
```

until the manifest-only guard exists and passes.

That is intentional. It prevents the next file from becoming a sneaky fit script
before the contracts are stable.

## 7. Decision

Decision:

```text
no_clock_manifest_only_fit_guard_passed
```

Meaning:

```text
The future official-likelihood scorer now has a working entry guard.
It reads the checkpoint-170 source-refresh run.
It refuses non-manifest scoring modes for now.
It proves the lead branch and baselines are present.
It proves the sidecar is excluded.
It writes the prior-edge contract required before any fit.
No chi2/AIC/BIC score is produced.
No theory/CMB/local-GR/parent-action promotion is made.
```

Boxing-card readout:

```text
The bouncer is now on the door.
Nobody gets into the scoring room unless the paperwork is clean,
and the sidecar is not sneaking in through the kitchen.
```

## 8. Next Target

Create:

```text
172-no-clock-single-arena-reproduction-guard.md
```

Extend:

```text
scripts/no_clock_official_likelihood_refresh.py
```

Next mode:

```text
--mode reproduce
```

Task:

```text
implement single-arena reproduction only, starting with SN+BAO or BAO-only,
and require the same branch/nuisance/edge contracts before producing any score.
```

Pass condition:

```text
the scorer reproduces an existing known score sign without changing source files
or including the sidecar.
```

Fail condition:

```text
the scorer runs a new joint/full refresh before reproducing at least one existing
arena and proving the scorecard plumbing is sane.
```
