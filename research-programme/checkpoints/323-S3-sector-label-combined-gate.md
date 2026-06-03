# 323 — `S3` Symmetry and `S_D` Sector-Label Combined Gate

Private derivation checkpoint. This is not a public amplitude, local-GR, CMB, or unified-field claim.

## Purpose

Checkpoint 322 improved the rank-one motion/time projectors:

```text
P_M = S3 singlet,
P_T = S3 singlet.
```

That removes arbitrary basis-slot picking.

This checkpoint asks the next sharper question:

```text
Can the S3 singlet also replace the ordinary/MTS sector label S_D?
```

Short answer:

```text
No.
```

`S3` helps the rank-one cell projector, but it cannot by itself distinguish MTS memory from ordinary coherent local baths.

## Machine Artifact

Script:

```text
scripts/S3_sector_label_combined_gate.py
```

Run:

```text
runs/20260601-141500-S3-sector-label-combined-gate
```

Status:

```text
S3_singlet_block_structure_conditional_SD_still_independent
```

Claim ceiling:

```text
conditional_S3_block_and_SD_support_no_local_GR_or_Bmem_promotion
```

## What `S3` Does Own Conditionally

If the parent cell kernel commutes with `S3`, then the singlet and doublet sectors block-diagonalize.

The artifact checks:

| Kernel | `S3` commutator | Singlet/doublet cross norm | Readout |
|---|---:|---:|---|
| `S3` invariant non-degenerate | `0` | near `0` | block diagonal |
| `S3` invariant degenerate | `0` | near `0` | block diagonal |
| generic `S3` breaking | nonzero | nonzero | cross terms allowed |

So the clean theorem is:

```text
[K_cell,S3]=0
=> singlet/doublet cross block vanishes.
```

That is a real conditional theorem.

It helps justify:

```text
P_singlet
```

as the coherent rank-one projector.

## Why `S3` Cannot Replace `S_D`

The artifact tests possible sources:

| Source | Pure singlet? | Problem |
|---|---:|---|
| FLRW MTS equal memory | yes | desired target |
| ordinary isotropic EM bath | yes | leakage danger |
| ordinary isotropic thermal bath | yes | leakage danger |
| anisotropic local shear | no | mostly doublet |
| generic local environment | mixed | has singlet part |

This is the key result:

```text
ordinary coherent baths can also be S3 singlets.
```

Therefore:

```text
P_singlet != P_MTS.
```

If we used only `S3` singlet selection, ordinary isotropic local stress/bath data could falsely activate the same memory channel.

So the sector label remains independent:

```text
S_D != P_singlet.
```

## What `S_D` Still Must Do

Checkpoint 311 remains the best sector-label route:

```text
A_D = C_D^\dagger C_D,
S_D = support(A_D).
```

where:

```text
C_D = P_rel P_IR P_coh
```

or an equivalent parent-owned MTS activity map.

The combined gate verifies:

| Test | Result |
|---|---|
| `A_D` positive | pass conditional |
| `S_D^2=S_D` | pass conditional |
| block kernel with `[K,S_D]=0` has zero ordinary/MTS cross block | pass conditional |
| sector-mixing kernel reintroduces ordinary/MTS cross terms | pass |

So the logic is now:

```text
S3 selects coherent cell singlets.
S_D selects the MTS boundary/memory sector.
Both are needed.
```

## Gate Results

| Gate | Status |
|---|---|
| source paths exist | pass |
| `S3` invariant kernel block-diagonalizes | pass |
| `S3` breaking kernel allows cross terms | pass |
| ordinary coherent bath singlet leakage exists | pass |
| `S3` singlet is not `S_D` | pass |
| `S_D` support label can be written | pass |
| block kernel is safe if commuting | pass |
| sector-mixing counterexample exists | pass |
| parent `C_D` derived | fail |
| parent kernel commutation derived | fail |
| amplitude promotion allowed | fail |

## Current Best Structure

The clean branch now has this layered form:

```text
P_active =
S_D
P_singlet,M
P_singlet,T
P_screen
```

with roles:

| Factor | Role | Status |
|---|---|---|
| `P_singlet,M` | coherent rank-one motion/load channel | conditional `S3` theorem |
| `P_singlet,T` | coherent rank-one no-clock/history channel | conditional `S3` theorem |
| `P_screen` | transverse spatial rank two | conditional screen-bundle theorem |
| `S_D` | kills ordinary bath leakage | conditional support-label theorem |
| `kappa_mem` | unit amplitude normalization | not derived |

Then:

```text
Tr(P_singlet,M tensor P_singlet,T tensor P_screen)/27 = 2/27.
```

But this only becomes a parent prediction if `S_D`, local silence, and `kappa_mem=1` are also parent-derived.

## Decision

Decision:

```text
S3_singlet_block_structure_conditional_SD_still_independent
```

Meaning:

```text
S3 is useful for the rank-one cell projectors.
S3 does not solve the ordinary/MTS bath separation problem.
S_D remains necessary and conditional.
```

Allowed language:

```text
MTS has a conditional layered projector schema: S3 singlets for coherent cell rank, plus an independent MTS sector label S_D to remove ordinary bath leakage.
```

Forbidden language:

```text
S3 symmetry derives the full MTS projector or B_mem=2/27.
```

## Boxing Readout

This was a good round, but not a knockout.

`S3` gives us cleaner footwork:

```text
rank-one by symmetry, not by slot picking.
```

But it does not block ordinary coherent body shots:

```text
ordinary isotropic baths can stand in the same singlet lane.
```

So we need the defensive guard:

```text
S_D = support(A_D).
```

And that guard is still not born from the parent action.

## Next Target

At this point the remaining parent derivation target is very narrow:

```text
derive C_D and [K_boundary,A_D]=0,
or stop squeezing this local/projector route and pivot to external empirical pressure.
```

Concrete theorem target:

```text
C_D = P_rel P_IR P_coh is parent-derived,
A_D = C_D^\dagger C_D is a parent activity/charge operator,
[K_boundary,A_D]=0 follows from the parent boundary action,
C_D B_ord = 0 for ordinary coherent baths,
C_D B_FLRW != 0 for cosmological memory.
```

If that cannot be derived, the current projector branch should remain:

```text
disciplined closure / theorem target,
not derived local GR,
not derived B_mem.
```

## Output Files

```text
runs/20260601-141500-S3-sector-label-combined-gate/results/source_register.csv
runs/20260601-141500-S3-sector-label-combined-gate/results/S3_kernel_decomposition.csv
runs/20260601-141500-S3-sector-label-combined-gate/results/singlet_leakage_tests.csv
runs/20260601-141500-S3-sector-label-combined-gate/results/SD_support_block_kernel.csv
runs/20260601-141500-S3-sector-label-combined-gate/results/theorem_clauses.csv
runs/20260601-141500-S3-sector-label-combined-gate/results/gate_results.csv
runs/20260601-141500-S3-sector-label-combined-gate/results/decision.csv
```
