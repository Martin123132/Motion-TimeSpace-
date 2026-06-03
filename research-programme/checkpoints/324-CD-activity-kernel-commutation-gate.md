# 324 — `C_D` Activity and Kernel-Commutation Gate

Private derivation checkpoint. This is not a public local-GR, PPN, amplitude, CMB, or unified-field claim.

## Purpose

Checkpoint 323 narrowed the remaining projector problem to:

```text
derive C_D and [K_boundary,A_D]=0,
```

where:

```text
A_D = C_D^\dagger C_D,
S_D = support(A_D).
```

This checkpoint asks the exact remaining question:

```text
Can C_D = P_rel P_IR P_coh and kernel commutation be parent-derived now?
```

Short answer:

```text
conditional algebra: yes
parent derivation: no
base C_D is insufficient without an MTS-specific channel
```

## Machine Artifact

Script:

```text
scripts/CD_activity_kernel_commutation_gate.py
```

Run:

```text
runs/20260601-143000-CD-activity-kernel-commutation-gate
```

Status:

```text
CD_activity_and_kernel_commutation_conditional_parent_origin_not_derived
```

Claim ceiling:

```text
conditional_CD_activity_gate_no_local_GR_or_Bmem_promotion
```

## Base Activity Filter

The base candidate is:

```text
C_base = P_rel P_IR P_coh.
```

It means:

| Factor | Keeps |
|---|---|
| `P_coh` | coherent scalar/domain content |
| `P_IR` | low-frequency / IR boundary content |
| `P_rel` | non-exact relative boundary-current content |

This is a real filter, but not enough.

The toy boundary basis shows:

| State | `C_base` | `C_MTS` |
|---|---:|---:|
| ordinary coherent IR relative | passes | killed |
| MTS coherent IR relative | passes | passes |
| edge/horizon coherent IR relative | passes | killed |

So:

```text
C_base = P_rel P_IR P_coh
```

still leaks an ordinary coherent IR relative bath.

That is the exact problem checkpoint 323 warned about.

## Required Repair

The repaired conditional filter is:

```text
C_MTS = P_MTS P_rel P_IR P_coh.
```

With `P_MTS` supplied, the artifact verifies:

```text
ordinary coherent IR relative bath -> killed
MTS coherent IR relative -> retained
```

But this is only useful if:

```text
P_MTS
```

or an equivalent channel-specific activity map is parent-derived.

If `P_MTS` is inserted by hand, the local/projector branch remains closure-level.

## Activity Operator and Sector Label

For supplied `C_D`, define:

```text
A_D = C_D^\dagger C_D.
```

The artifact verifies:

| Operator | `A_D` positive? | `S_D` idempotent? | Support |
|---|---:|---:|---|
| `C_base` | yes | yes | ordinary + MTS + edge coherent IR relative |
| `C_MTS` | yes | yes | MTS coherent IR relative only |

So the support-label theorem remains valid:

```text
S_D = support(A_D)
```

is a threshold-free projector.

But the support is only physically correct if the input `C_D` is physically correct.

## Kernel-Commutation Gate

The block split is safe if:

```text
[K_boundary,A_D]=0
```

or equivalently:

```text
[K_boundary,S_D]=0.
```

The artifact verifies:

| Kernel | Commutation | Cross terms |
|---|---:|---|
| block-diagonal by sector | pass | none |
| `K=f(A_D)` | pass | none |
| ordinary/MTS mixing kernel | fail | ordinary/MTS cross term |
| MTS/edge mixing kernel | fail | MTS/edge cross term |

So:

```text
K=f(A_D)
```

would be a clean theorem route.

But a generic boundary kernel can mix the support and kernel of `A_D`.

Therefore:

```text
[K_boundary,A_D]=0
```

must be derived from the parent boundary action. It cannot be assumed after the fact.

## Gate Results

| Gate | Status |
|---|---|
| source paths exist | pass |
| `C_base=P_rel P_IR P_coh` is a valid projector | pass |
| ordinary leakage through `C_base` detected | pass |
| `C_MTS` kills ordinary leakage if supplied | pass |
| `A_D` positive for `C_MTS` | pass |
| `S_D=support(A_D)` idempotent | pass |
| `K=f(A_D)` commutes with `A_D` | pass |
| generic kernel mixing counterexample | pass |
| edge/horizon mixing counterexample | pass |
| parent `C_D` derived | fail |
| parent kernel commutation derived | fail |
| lifted `J_C` parent-derived | fail |
| local-GR or `B_mem` promotion allowed | fail |

## What This Decides

The remaining local/projector route is now almost completely fenced.

We have:

```text
S3 singlet for rank-one coherent cell channels,
screen bundle for rank-two spatial factor,
S_D = support(A_D) as threshold-free sector label,
C_MTS as the correct activity filter if P_MTS is supplied,
K=f(A_D) as a clean commutation route if parent-owned.
```

But we do not have:

```text
parent derivation of P_MTS or C_D,
parent derivation of [K_boundary,A_D]=0,
parent derivation of lifted J_C,
parent derivation of local GR,
parent derivation of B_mem=2/27.
```

## Decision

Decision:

```text
CD_activity_and_kernel_commutation_conditional_parent_origin_not_derived
```

Meaning:

```text
The correct C_D/S_D/K_boundary algebra is now explicit.
The base activity filter leaks ordinary coherent baths.
The repaired filter works only if a parent MTS channel projector is supplied.
Kernel commutation works only if the boundary action is block/functional in A_D.
```

Allowed language:

```text
MTS has a precise conditional activity-operator route for the ordinary/MTS sector split.
```

Forbidden language:

```text
MTS derives local GR or B_mem=2/27 from the projector branch.
```

## Boxing Readout

This is the bell for this local/projector round.

We did not get knocked out, but we also did not win the title.

We found the exact defensive shell:

```text
S3 singlet + screen bundle + S_D support label + parent C_D + commuting K_boundary.
```

But the two punches that would make it a theorem are still missing:

```text
derive C_D,
derive [K_boundary,A_D]=0.
```

Without those, the branch is disciplined closure/theorem target.

## Next Target

Unless a genuinely new parent action supplies `C_D`, the best next move is no longer another local projector derivation.

Next default:

```text
park the local/projector branch as conditional,
then move to external empirical pressure:
Hz, growth, CMB bridge, and official/full-likelihood wrappers.
```

The local theorem target remains written:

```text
derive a lifted 3-form / holonomy / boundary-class current J_C
such that C_D follows from parent variables,
A_D = C_D^\dagger C_D,
[K_boundary,A_D]=0,
C_D B_ord = 0,
C_D B_FLRW != 0.
```

But it should not be used as derived support until that theorem exists.

## Output Files

```text
runs/20260601-143000-CD-activity-kernel-commutation-gate/results/source_register.csv
runs/20260601-143000-CD-activity-kernel-commutation-gate/results/boundary_basis.csv
runs/20260601-143000-CD-activity-kernel-commutation-gate/results/CD_projector_algebra.csv
runs/20260601-143000-CD-activity-kernel-commutation-gate/results/ordinary_leakage_tests.csv
runs/20260601-143000-CD-activity-kernel-commutation-gate/results/activity_support.csv
runs/20260601-143000-CD-activity-kernel-commutation-gate/results/kernel_commutation.csv
runs/20260601-143000-CD-activity-kernel-commutation-gate/results/theorem_clauses.csv
runs/20260601-143000-CD-activity-kernel-commutation-gate/results/gate_results.csv
runs/20260601-143000-CD-activity-kernel-commutation-gate/results/decision.csv
```
