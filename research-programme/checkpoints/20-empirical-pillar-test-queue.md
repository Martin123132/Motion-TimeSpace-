# Empirical Pillar Test Queue

## 1. Purpose

This file follows:

```text
19-constrained-parent-action-skeleton.md
```

The question is:

```text
How should empirical testing resume without turning the closure benchmark into
an overclaim?
```

Short answer:

```text
the empirical queue is ready, but it authorizes no claim yet. First target is a
cosmology parent-bridge audit, not a long blind run.
```

## 2. Machine Run

Implemented:

```text
scripts/empirical_pillar_test_queue.py
```

Successful run:

```text
runs/20260530-233654-empirical-pillar-test-queue/status.json
```

Readout:

```text
empirical_pillar_test_queue_ready_no_claims
```

Next target:

```text
21-cosmology-parent-bridge-audit.md
```

## 3. Pillar Priority

Priority order:

```text
1. local_PPN_clocks:
screening-ready using the stage 13-16 gate runner.

2. cosmology:
ready for robustness return, but parent bridge is open.

3. galaxies:
separate repo/thread; empirical pillar only.

4. EM_time:
needs variable/action mapping before numerical tests.

5. orbital_systems:
partly ready through local PPN sensitivity.

6. particle_quantum:
not ready until parent matter action is explicit.
```

## 4. Claim Ladder

All future evidence must be labeled:

```text
L0_control:
closure/control benchmark reproduces known limit.

L1_screened:
candidate branch survives published-bound screening.

L2_fit:
candidate improves a dataset under a specified likelihood.

L3_robust:
signal survives priors, splits, jackknives, and baselines.

L4_derived:
parameter follows from parent action.

L5_unified:
same parent action explains multiple pillars.
```

This ladder prevents:

```text
a fitted closure parameter being relabeled as derived;
a single empirical success being relabeled as unified theory;
a baseline failure being ignored while MTS is punished.
```

## 5. Next Runs

The next actionable runs are:

```text
local_branch_screening:
use scripts/local_bounds_gate_runner.py for any proposed local branch.

cosmology_bridge_audit:
create 21-cosmology-parent-bridge-audit.md.

cosmology_robustness_return:
only after bridge audit and prior/split rules are fixed.

EM_time_variable_map:
map variables and couplings before numerical tests.

galaxy_pillar_interface:
do not modify galaxy repo here; export only shared variables/action hooks.
```

## 6. Risk Register

High-risk failure modes:

```text
phenomenology_without_parent:
cosmology/galaxy parameters float without action origin.

closure_as_derivation:
local R_AB=0 gets mislabeled as proven.

baseline_asymmetry:
MTS is jackknifed harder than competitors without reporting baseline failures.

prior_edge_signal:
cosmology preference depends on edge-hitting priors.

repo_scope_contamination:
galaxy work and unified-field work get mixed too early.
```

## 7. Gate Verdict

Passes:

```text
source 19 complete;
all major pillars listed;
claim ladder defined;
next runs prioritized.
```

Fails:

```text
empirical claim allowed now;
main workbench mutation allowed.
```

Status:

```text
ready for disciplined next runs;
no claim authorized.
```

## 8. Next Target

Create:

```text
21-cosmology-parent-bridge-audit.md
```

Purpose:

```text
map cosmology variables and fitted parameters onto the parent-action skeleton
before any long cosmology robustness run, so we know what is derived,
postulated, or merely phenomenological.
```
