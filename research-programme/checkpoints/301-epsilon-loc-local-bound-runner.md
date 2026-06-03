# 301 - Epsilon-Loc Local-Bound Runner

Private local-bound checkpoint. This is not a public local-GR, PPN, cosmology, CMB, or parent-field-theory claim.

## Purpose

Checkpoint 300 left the next concrete task:

```text
build the local-bound runner for epsilon_loc.
```

The local residual contract is:

```text
epsilon_loc = |sigma_D Lambda_open Tr(P_iso q_r)|.
```

This runner tests whether:

```text
sigma_D=0 exactly,
```

or whether the residual must face PPN-style proxy bounds.

## Runner Definition

The selector is:

```text
sigma_D = b_D c_D / (b_D c_D + mu_*^2).
```

with exact-zero handling:

```text
b_D c_D = 0 => sigma_D=0.
```

Then:

```text
epsilon_loc = |sigma_D Lambda_open trace_charge|.
```

The runner maps this into residual channels:

```text
delta_channel = C_channel epsilon_loc.
```

The coefficient policies are deliberately labelled as proxy/contract-level:

| Policy | Meaning |
|---|---|
| `scalar_metric_proxy` | conservative proxy for gamma/beta, no direct clock/matter |
| `common_mode_contract` | checkpoint-227 common-mode contract, beta still active |
| `direct_matter_stress_test` | harsh fail probe for WEP/direct matter coupling |
| `exact_silence` | coefficients irrelevant if `epsilon_loc=0` |

## What Passed

Exact silence passes:

```text
local_bath_absent_exact
local_relative_class_trivial_exact
```

because:

```text
sigma_D=0,
epsilon_loc=0.
```

Small nonzero selectors can pass proxy bounds:

```text
local_tiny_selector_scalar_proxy
local_beta_edge_common_mode
```

That means the gate can distinguish:

```text
exact silence,
bounded leakage,
and unacceptable leakage.
```

## What Failed

Deliberate failure probes fail:

```text
local_proxy_fail
direct_matter_tiny_fail_probe
```

This is important.

The runner is not rubber-stamping MTS.

The direct matter case fails because:

```text
MICROSCOPE/WEP-style proxy bounds are brutally tight
if the open sector creates composition-dependent coupling.
```

So the theory still strongly wants:

```text
universal metric coupling,
no direct matter coupling,
or exact selector silence.
```

## Gates

| Gate | Result | Meaning |
|---|---|---|
| source paths exist | pass | runner traceable |
| epsilon runner constructed | pass | selector now faces a quantitative gate |
| exact silence cases pass | pass | `sigma_D=0` gives zero residual |
| proxy bounded case exists | pass | nonzero leakage can be bounded |
| failure probes fail | pass | runner catches bad branches |
| official PPN claim allowed | fail | coefficients/bounds still proxy-level |
| local GR promoted | fail | selector and coefficients not parent-derived |
| `B_mem` parent-derived | fail | runner does not derive amplitude |

## Decision

Decision:

```text
epsilon_loc_local_bound_runner_ready_exact_silence_passes_proxy_bounds_no_local_GR_promotion
```

Meaning:

```text
local silence and bounded leakage can now be tested mechanically,
but the result is still a proxy gate, not a local-GR proof.
```

What improved:

```text
the local branch now has a quantitative failure gate.
```

What did not improve:

```text
the required selector theorem and parent PPN coefficients remain missing.
```

So:

```text
local GR remains unpromoted.
```

Boxing-score version:

```text
We built the scale.
Now the local branch has to make weight.
Some cuts pass, some fail, and no one gets to claim the belt from the weigh-in.
```

## Machine Artifacts

Script:

```text
scripts/epsilon_loc_local_bound_runner.py
```

Run:

```text
runs/20260601-000124-epsilon-loc-local-bound-runner
```

Output files:

```text
runs/20260601-000124-epsilon-loc-local-bound-runner/results/source_register.csv
runs/20260601-000124-epsilon-loc-local-bound-runner/results/bound_manifest_proxy.csv
runs/20260601-000124-epsilon-loc-local-bound-runner/results/coefficient_policies.csv
runs/20260601-000124-epsilon-loc-local-bound-runner/results/candidate_domains.csv
runs/20260601-000124-epsilon-loc-local-bound-runner/results/epsilon_results.csv
runs/20260601-000124-epsilon-loc-local-bound-runner/results/residual_channel_results.csv
runs/20260601-000124-epsilon-loc-local-bound-runner/results/case_summary.csv
runs/20260601-000124-epsilon-loc-local-bound-runner/results/promotion_gates.csv
runs/20260601-000124-epsilon-loc-local-bound-runner/results/decision.csv
```

## Next Step

The local gate now says what the theory must supply:

```text
derive sigma_D=0 exactly for local domains,
or derive parent coefficients C_channel and show epsilon_loc stays below official bounds.
```

Best next move:

```text
either derive/import the parent coefficient map for epsilon_loc,
or pivot back to stronger empirical holdout testing while local GR remains conditional.
```
