# 170 - No-Clock Official Source Refresh Runner

Private prefit/source-lock checkpoint. This is not a public claim.

## 1. Trigger

Checkpoint 169 said the next empirical move must not start with a fit. It must
start with the source files:

```text
source hashes,
row manifests,
covariance manifests,
branch manifests,
nuisance rules,
dry-run commands.
```

This checkpoint implements that runner.

No model has been scored here.

## 2. Machine Artifact

Script:

```text
scripts/no_clock_official_source_refresh.py
```

Run:

```text
runs/20260531-235959-no-clock-official-source-refresh
```

Generated:

```text
source_register.csv
source_hash_lock.csv
row_manifest.csv
covariance_manifest.csv
branch_manifest.csv
nuisance_policy.csv
dry_run_command_queue.csv
preflight_gates.csv
decision.csv
status.json
DONE.txt
```

Status:

```text
no_clock_official_source_refresh_preflight_passed
```

Claim ceiling:

```text
source_refresh_preflight_only_no_model_scoring_or_theory_promotion
```

## 3. What Was Checked

The runner audits the current local official/source-locked assets:

| check | result |
|---|---:|
| source hash rows | `43` |
| expected hash mismatches | `0` |
| recorded current hashes without expected upstream hash | `10` |
| row manifest rows | `1819` |
| covariance manifest rows | `18` |
| covariance failures | `0` |
| failed gates | `0` |

The `recorded_no_expected_hash` rows are the cosmic-chronometer local products
whose source state is handled by the previous CC source-lock/row-lock work.
They are not treated as official release hash failures.

## 4. Row Manifest

Rows are now explicitly manifest before any fit:

| arena | rows |
|---|---:|
| SN | `1701` |
| BAO | `25` |
| H(z) | `47` |
| growth/RSD | `30` |
| CMB diagnostic | `16` |

Important row policies:

```text
Pantheon+ calibrators are flagged for no-SH0ES shape handling.
DESI DR2 is the primary BAO release.
DESI DR1/2024 remains a release-sensitivity comparator.
CC32 is diagonal sensitivity only.
CC15 BC03 is the covariance primary chronometer branch.
SDSS/eBOSS BAO-plus and full-shape-only are kept separate.
ELG remains grid-likelihood/parser-required, not a Gaussian shortcut.
Planck distance priors remain diagnostic only.
```

This is exactly the prefit guardrail we needed.

## 5. Covariance Manifest

Covariance checks passed for:

```text
Pantheon+ STAT+SYS full covariance
Pantheon+ STATONLY full covariance
DESI DR2 BAO covariance
DESI DR1/2024 BAO covariance
CC15 BC03 covariance variants
SDSS/eBOSS growth/RSD covariance files
Planck distance-prior long-form covariance diagnostic
```

The SN covariance symmetry tolerance was treated numerically, not ideologically:

```text
max symmetry deviation ~ 3e-8
```

That is retained as acceptable finite-precision source formatting, not a
physical covariance failure.

## 6. Branch Manifest

The lead-refresh branch policy is now machine-readable:

| branch | role | included in lead refresh |
|---|---|---|
| `LCDM` | baseline | yes |
| `wCDM` | baseline | yes |
| `CPL` | baseline | yes |
| `MTS_2over27_no_clock_u3quarter` | lead branch | yes |
| `MTS_Bmem_zero` | negative control | yes |
| `MTS_pair_ruler_half_kernel` | frozen sidecar | no |

This is the key guardrail:

```text
the sidecar cannot silently rescue the lead branch.
```

## 7. Nuisance Policy

The runner also writes:

```text
nuisance_policy.csv
```

Required next-step rules:

```text
SN offset / absolute magnitude must be profiled identically.
BAO alpha / rd convention must be shared.
H0 or expansion-scale treatment must be symmetric.
sigma8_0 profiling must be shared in GR-proxy growth tests.
prior-edge hits demote evidence for every branch, including baselines.
```

So if a future fit is close, the scorecard is not allowed to hide behind
asymmetric nuisance treatment.

## 8. Gates

| gate | status | evidence |
|---|---|---|
| source files exist | pass | `missing=0` |
| expected hashes match | pass | `hash_mismatches=0` |
| required row manifests present | pass | `total_rows=1819` |
| covariance preflight | pass | `covariance_failures=0` |
| sidecar excluded from lead refresh | pass | pair-ruler half-kernel `included_in_lead_refresh=no` |
| no model scoring | pass | no `chi2/AIC/BIC` scoring run |
| claim ceiling preserved | pass | source preflight only |

## 9. Decision

Decision:

```text
no_clock_official_source_refresh_preflight_passed
```

Meaning:

```text
The source-lock/schema/covariance/branch guardrail is ready.
No-clock MTS remains the empirical lead branch.
LCDM/wCDM/CPL are present as fair baselines.
MTS_Bmem_zero is present as a negative control.
The pair-ruler half-kernel is explicitly excluded from lead scoring.
No model fit or theory promotion is made here.
```

Boxing-card readout:

```text
The ring inspection passes.
The gloves are weighed.
The judges' score sheet is printed.
Nobody has thrown a punch yet.
```

## 10. Next Target

Create:

```text
171-no-clock-manifest-only-fit-guard.md
```

and:

```text
scripts/no_clock_official_likelihood_refresh.py
```

First mode only:

```text
--mode manifest-only --assert-no-sidecar
```

Task:

```text
build the scorer guard that refuses to run if the row, covariance, branch,
nuisance, prior-edge, and sidecar-exclusion contracts are not present.
```

Pass condition:

```text
the scorer can generate a manifest-only run and explicitly refuse scoring if
the source-refresh artifacts are missing or inconsistent.
```

Fail condition:

```text
the next script jumps directly into fitting without proving the prefit contract.
```
