# 304 - Epsilon-Loc Beta Guard Update

Private local-bound checkpoint. This is not a public local-GR, PPN, cosmology, CMB, or parent-field-theory claim.

## Purpose

Checkpoint 303 showed:

```text
beta_eff = B/A^2
c_beta = b1 - 2a1.
```

For a linear-only local trace leak:

```text
c_beta = -2.
```

Therefore the checkpoint-301 guard:

```text
c_beta = 1
```

was too soft.

This checkpoint updates the `epsilon_loc` runner so:

```text
|c_beta| = 2
```

unless:

```text
exact selector silence holds,
or the parent proves B=A^2.
```

## Runner Patch

Patched:

```text
scripts/epsilon_loc_local_bound_runner.py
```

Updated coefficient policies:

| Policy | Old `c_beta` | New `c_beta` | Meaning |
|---|---:|---:|---|
| `scalar_metric_proxy` | 1 | 2 | conservative beta guard |
| `common_mode_contract` | 1 | 2 | gamma zero, beta still guarded |
| `direct_matter_stress_test` | 1 | 2 | harsh fail probe |
| `exact_silence` | irrelevant | irrelevant | coefficients do not matter if `epsilon_loc=0` |

Also added:

```text
local_beta_guard2_bounded_common_mode
```

as a nonzero leakage case that passes the stronger beta guard.

## Updated Results

Exact silence still passes:

```text
local_bath_absent_exact
local_relative_class_trivial_exact
```

Small leakage still has a bounded path:

```text
local_tiny_selector_scalar_proxy
local_beta_guard2_bounded_common_mode
```

The old near-edge common-mode case now fails:

```text
local_beta_edge_common_mode -> beta_minus_1 fail
```

That is the intended behaviour.

The runner is stricter now.

## Gates

| Gate | Result | Meaning |
|---|---|---|
| source paths exist | pass | runner traceable |
| epsilon runner constructed | pass | selector faces quantitative gate |
| exact silence cases pass | pass | `sigma_D=0` gives zero residual |
| proxy bounded case exists | pass | nonzero leakage can still pass |
| beta guard 2 active | pass | checkpoint-303 risk represented |
| failure probes fail | pass | no rubber-stamping |
| official PPN claim allowed | fail | proxy/manifest only |
| local GR promoted | fail | selector and coefficients not parent-derived |
| `B_mem` parent-derived | fail | amplitude unchanged |

## Decision

Decision:

```text
epsilon_loc_local_bound_runner_beta_guard_2_ready_no_local_GR_promotion
```

Meaning:

```text
the local proxy runner now treats beta conservatively enough for linear-only trace leakage.
```

What improved:

```text
the beta guard now matches the checkpoint-303 second-order analysis.
```

What did not improve:

```text
this is still not an official PPN proof,
and local GR is not promoted.
```

Boxing-score version:

```text
We tightened the gloves.
Beta no longer gets a soft touch:
if the second punch is not parent-owned, the guard doubles.
```

## Machine Artifacts

Updated script:

```text
scripts/epsilon_loc_local_bound_runner.py
```

Run:

```text
runs/20260601-000127-epsilon-loc-local-bound-runner
```

Output files:

```text
runs/20260601-000127-epsilon-loc-local-bound-runner/results/source_register.csv
runs/20260601-000127-epsilon-loc-local-bound-runner/results/bound_manifest_proxy.csv
runs/20260601-000127-epsilon-loc-local-bound-runner/results/coefficient_policies.csv
runs/20260601-000127-epsilon-loc-local-bound-runner/results/candidate_domains.csv
runs/20260601-000127-epsilon-loc-local-bound-runner/results/epsilon_results.csv
runs/20260601-000127-epsilon-loc-local-bound-runner/results/residual_channel_results.csv
runs/20260601-000127-epsilon-loc-local-bound-runner/results/case_summary.csv
runs/20260601-000127-epsilon-loc-local-bound-runner/results/promotion_gates.csv
runs/20260601-000127-epsilon-loc-local-bound-runner/results/decision.csv
```

## Next Step

The next local blocker is now:

```text
fifth-force gradient behaviour.
```

Build a runner for:

```text
grad(Lambda_D Tr(P_iso q_r))
```

and test whether nonzero `epsilon_loc` creates a local force,
or whether only exact selector silence is safe.
