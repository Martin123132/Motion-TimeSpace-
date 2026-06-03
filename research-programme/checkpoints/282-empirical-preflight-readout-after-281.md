# 282 - Empirical Preflight Readout After 281

Private empirical-readiness checkpoint. This is not a public local-GR, CMB, BAO, or unified-field claim.

## Purpose

Checkpoint 281 generated the empirical closure-test design.

This checkpoint actually runs the first safe preflights:

```text
T1 local proxy bound preflight
T2 SN+BAO schema dry-run
T3 fixed-vs-kappa dry-run
```

No empirical scores are generated here.

## Machine Artifact

Script:

```text
scripts/empirical_preflight_readout_after_281.py
```

Run:

```text
runs/20260601-000104-empirical-preflight-readout-after-281
```

Status:

```text
empirical_preflights_run_local_proxy_passed_cosmo_schema_blocked_by_BAO_manifest
```

Claim ceiling:

```text
dryrun_and_proxy_preflight_only_no_empirical_support_claim
```

## T1 - Local Proxy Bound Preflight

Run:

```text
runs/20260601-000100-local-bound-preflight-and-baseline-comparison
```

Readout:

```text
local_bound_preflight_dryrun_ranked_no_PPN_promotion
```

Key machine fields:

```text
compact_base_proxy_failures = 0
worst_base_q_proxy_ratio = 0.6768420886270882
tightest_coefficient_case = earth_GPS_shell
tightest_coefficient_residual = gamma_minus_1
tightest_coefficient_budget = 1.057945159147665
promotion_allowed = false
```

Interpretation:

```text
local proxy stack is ready for prioritization,
but it is not an official PPN/local-GR pass.
```

## T2 - Generic SN+BAO Schema Dry-Run

Run:

```text
runs/20260601-093239-cosmo-SN-BAO-closure-dryrun
```

Readout:

```text
dry_run_incomplete_missing_or_unvalidated_data
```

Blocker:

```text
BAO_distance_data_not_validated
```

Interpretation:

```text
do not run or interpret the generic SN+BAO short smoke yet.
```

Required fix:

```text
provide explicit --sn-data, --sn-cov, --bao-data, and --bao-cov paths
or add a local data manifest that maps the existing BAO files to the runner schema.
```

## T3 - Fixed-vs-Kappa SN+BAO Dry-Run

Run:

```text
runs/20260601-000101-fixed-vs-kappa-free-SN-BAO-dryrun-runner
```

Readout:

```text
fixed_vs_kappa_SN_BAO_dryrun_passed_no_scores_generated
```

Key machine fields:

```text
SN_rows_template = 1701
BAO_DR2_rows_template = 13
n_eff_template = 1714
kappa_AIC_tax_delta_chi2 = 2
kappa_BIC_tax_delta_chi2 = 7.446585
scores_generated = false
promotion_allowed = false
```

Interpretation:

```text
this is the cleanest near-term route to a short smoke,
because the dry-run contract is already complete.
```

But:

```text
no score has been generated yet.
```

## Gate Results

| Gate | Result |
|---|---|
| local proxy preflight completed | pass |
| local proxy headroom exists | warn / proxy only |
| SN+BAO schema ready | fail |
| fixed-vs-kappa dry-run ready | pass |
| empirical support claim allowed | fail |

So the project is now in a better testing position:

```text
one local proxy preflight passed,
one cosmology schema route is blocked by BAO manifest,
one cosmology dry-run route is ready for short smoke.
```

## Decision

Next practical choice:

```text
repair BAO data manifest,
or run fixed-vs-kappa short smoke first.
```

Recommended:

```text
repair/confirm BAO manifest before the generic runner,
but the fixed-vs-kappa short smoke is a valid near-term test if its built-in template assumptions are accepted.
```

## Output Files

```text
runs/20260601-000104-empirical-preflight-readout-after-281/results/source_register.csv
runs/20260601-000104-empirical-preflight-readout-after-281/results/dryrun_status_matrix.csv
runs/20260601-000104-empirical-preflight-readout-after-281/results/gate_results.csv
runs/20260601-000104-empirical-preflight-readout-after-281/results/blockers.csv
runs/20260601-000104-empirical-preflight-readout-after-281/results/next_actions.csv
runs/20260601-000104-empirical-preflight-readout-after-281/results/decision.csv
```

## Next Step

Best next implementation target:

```text
283 - BAO Data Manifest Repair or Fixed-vs-Kappa Short Smoke
```

If choosing BAO repair:

```text
identify local SN/BAO files,
write manifest,
rerun generic SN+BAO dry-run.
```

If choosing short smoke:

```text
run fixed_vs_kappa_cosmology_runner.py --phase short-smoke,
then inspect convergence, prior edges, residuals, and AIC/BIC against LCDM/wCDM/CPL.
```

