# 281 - Empirical Closure Test Design After Local Ledger

Private test-design checkpoint. This is not a public local-GR, CMB, BAO, or unified-field claim.

## Purpose

Checkpoint 280 ended the local derivation loop honestly:

```text
derived fixed-D projector;
domain and representative still closure/theorem targets;
testing allowed only under closure labels.
```

This checkpoint turns that into a concrete empirical test plan.

No model scores are generated here. This is the disciplined preflight that says:

```text
what to run,
what baselines get the same pressure,
what outputs must exist,
and what claims are forbidden.
```

## Machine Artifact

Script:

```text
scripts/empirical_closure_test_design_after_local_ledger.py
```

Run:

```text
runs/20260601-000099-empirical-closure-test-design-after-local-ledger
```

Status:

```text
empirical_closure_test_design_written_after_local_ledger_no_scores_generated
```

Claim ceiling:

```text
test_design_and_dryrun_commands_only_no_empirical_support_claim
```

## Closure Branches

The test plan separates four branches:

| Branch | Label | Claim ceiling |
|---|---|---|
| local projected `Q_coh` closure | explicit effective closure | closure viability only |
| cosmology no-clock `2/27` | empirical EFT closure | empirical closure score only |
| smooth `Pi(C_coh)` polarization | closure only / no promotion | do not use as derivation |
| topological representative selection | theorem target | derivation research only |

This prevents the old trap:

```text
good empirical behaviour != parent derivation.
```

## Test Manifest

Priority tests:

| Test | Arena | Purpose |
|---|---|---|
| `T1_local_proxy_bound_preflight` | local gravity proxy | check local residual bound stack |
| `T2_SN_BAO_dryrun_schema` | cosmology background | validate schema/model/baseline matrix before scoring |
| `T3_fixed_vs_kappa_SN_BAO_short_smoke` | cosmology background | compare fixed `2/27` against kappa-free and baselines |
| `T4_no_SH0ES_branch` | cosmology background | check dependence on local-H0 calibration pressure |
| `T5_domain_sensitivity_jackknife` | local/cosmology stability | test arbitrary-domain sensitivity fairly |
| `T6_official_CMB_preflight_repeat` | CMB | only readiness until official likelihood assets exist |

## Baseline Parity

The plan locks five fairness rules:

```text
same data / same splits
same calibration freedom where comparable
same jackknife pressure where meaningful
visible complexity penalty
edge hits are not evidence
```

That addresses the boxing-point properly:

```text
MTS should not be hammered by tests that the baselines are not also asked to survive.
```

But:

```text
if MTS gets extra freedom, the penalty must be visible.
```

Mayweather rules, not bar-fight rules.

## Dry-Run Commands

Generated command file:

```text
runs/20260601-000099-empirical-closure-test-design-after-local-ledger/results/run_dryruns.ps1
```

Commands are also registered in:

```text
runs/20260601-000099-empirical-closure-test-design-after-local-ledger/results/dry_run_commands.csv
```

Recommended first sequence:

```text
T1 local proxy bound preflight
T2 SN+BAO schema dry-run
T3 fixed-vs-kappa dry-run, then short smoke only if dry-run passes
```

No long computation is started in this checkpoint.

## Output Contract

Any empirical run must write:

```text
status.json
DONE.txt
source_register.csv
gate_results.csv
```

If scores exist, it must also write:

```text
baseline_comparison.csv
prior_edge_table.csv
residuals or plot_register
```

This prevents orphaned numbers from being interpreted without diagnostics.

## Decision

The empirical route is now ready to start safely.

Current allowed statement:

```text
The local branch is an explicitly labelled closure with testable residual gates.
The cosmology branch can be scored against LCDM/wCDM/CPL with fair baseline parity.
No score from this plan can prove a parent field theory by itself.
```

## Output Files

```text
runs/20260601-000099-empirical-closure-test-design-after-local-ledger/results/source_register.csv
runs/20260601-000099-empirical-closure-test-design-after-local-ledger/results/closure_branches.csv
runs/20260601-000099-empirical-closure-test-design-after-local-ledger/results/test_manifest.csv
runs/20260601-000099-empirical-closure-test-design-after-local-ledger/results/baseline_parity_rules.csv
runs/20260601-000099-empirical-closure-test-design-after-local-ledger/results/dry_run_commands.csv
runs/20260601-000099-empirical-closure-test-design-after-local-ledger/results/output_contract.csv
runs/20260601-000099-empirical-closure-test-design-after-local-ledger/results/decision.csv
runs/20260601-000099-empirical-closure-test-design-after-local-ledger/results/run_dryruns.ps1
```

## Next Step

Run the first dry-runs:

```text
T1_local_proxy_bound_preflight
T2_SN_BAO_dryrun_schema
T3_fixed_vs_kappa_SN_BAO_dryrun
```

Then only run the short smoke if:

```text
schemas pass,
baselines are present,
and failure labels are wired.
```

