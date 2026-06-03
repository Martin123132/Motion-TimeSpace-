# 322 — `S3` Singlet Motion/Time Projector Gate

Private derivation checkpoint. This is not a public amplitude, local-GR, CMB, or unified-field claim.

## Purpose

Checkpoint 321 showed that the full-cell rank-two amplitude route needs:

```text
P_active = P_M tensor P_T tensor P_screen,
rank(P_M)=1,
rank(P_T)=1,
rank(P_screen)=2.
```

The weak point was that `P_M` and `P_T` looked like chosen basis slots.

This checkpoint asks:

```text
Can the rank-one motion/time projectors be made symmetry-selected rather than hand-selected?
```

Short answer:

```text
yes, conditionally: use the unique S3 singlet projector in each 3-state sector.
no, as a parent theorem: the parent S3 symmetry and no-clock singlet source are not derived yet.
```

This is a real improvement because it removes the arbitrary-basis smell from the rank-one factors.

## Machine Artifact

Script:

```text
scripts/singlet_motion_time_projector_gate.py
```

Run:

```text
runs/20260601-140000-singlet-motion-time-projector-gate
```

Status:

```text
singlet_motion_time_projectors_constructed_conditionally_not_parent_derived
```

Claim ceiling:

```text
conditional_S3_singlet_projectors_no_Bmem_or_local_GR_promotion
```

## Construction

For a three-state sector with permutation group `S3`, define:

```text
P_singlet = (1/|S3|) sum_{g in S3} g.
```

This is the group-average projector onto the coherent equal-load vector:

```text
(1,1,1).
```

The artifact verifies:

| Object | Trace | Rank | Idempotent | Commutes with `S3` |
|---|---:|---:|---:|---:|
| `P_singlet` | `1` | `1` | yes | yes |
| `P_doublet` | `2` | `2` | yes | yes |
| `P_screen` | `2` | `2` | yes | no, because it requires a normal/screen bundle |

So `P_singlet` is not just another arbitrary axis projector. It is the unique coherent channel selected by permutation symmetry.

## Full Cell Lift

Use:

```text
P_M = P_singlet on the motion/load sector,
P_T = P_singlet on the time/history sector,
P_screen = h - n n on the spatial sector.
```

Then:

```text
P_active = P_singlet,M tensor P_singlet,T tensor P_screen.
```

The full 27-dimensional lift gives:

| Object | Dimension | Trace | Rank | Normalized trace |
|---|---:|---:|---:|---:|
| `P_active_singlet` | `27` | `2` | `2` | `2/27` |
| old axis-basis active projector | `27` | `2` | `2` | `2/27` |
| motion-doublet contamination | `27` | `4` | `4` | `4/27` |

The value is the same as the old axis construction, but now the rank-one factors are symmetry singlets rather than picked basis axes.

That is a better theorem target.

## Source Test

The artifact checks source vectors:

| Source | `S3` invariant? | Singlet readout |
|---|---:|---|
| coherent equal load `(1,1,1)` | yes | pure singlet |
| basis-axis load `(1,0,0)` | no | contains doublet |
| tracefree difference `(1,-1,0)` | no | pure/nonzero doublet |
| generic load `(1,2,4)` | no | contains doublet |

So the singlet route naturally says:

```text
FLRW coherent equal-load memory can excite the singlet;
generic local/source data contains doublet or symmetry-breaking content.
```

That is promising for separation, but not enough for local safety. Ordinary baths still need the `P_MTS` / sector-superselection projector from checkpoints 309–310.

## Gate Results

| Gate | Status |
|---|---|
| source paths exist | pass |
| `P_singlet^2=P_singlet` | pass |
| `rank(P_singlet)=1` | pass |
| `P_singlet` commutes with all `S3` permutations | pass |
| coherent FLRW source is pure singlet | pass |
| generic sources are not pure singlet | pass |
| full lift has rank two | pass |
| full lift gives `2/27` | pass |
| basis choice removed | pass |
| parent `S3` symmetry derived | fail |
| no-clock singlet parent-derived | fail |
| ordinary-bath superselection parent-derived | fail |
| amplitude promotion allowed | fail |

## What This Wins

This is the cleanest rank-one motion/time result so far:

```text
rank-one is no longer "choose slot 1";
rank-one is "project onto the S3 coherent singlet".
```

That makes the full amplitude route:

```text
B_mem = kappa_mem Tr(P_singlet,M tensor P_singlet,T tensor P_screen) / 27
      = kappa_mem * 2/27.
```

So if a parent action later proves:

```text
S3 cell symmetry,
FLRW equal-load singlet source,
screen-bundle projection,
kappa_mem=1,
ordinary/MTS sector superselection,
```

then the `2/27` amplitude follows without a fitted amplitude knob.

## What Still Fails

The parent action has not yet proved:

```text
the 3-state sectors really carry S3 symmetry,
the no-clock time/history sector is the S3 singlet,
ordinary local baths cannot source the same singlet channel,
the screen bundle is parent-owned,
kappa_mem=1.
```

The crucial difference is that the theorem target is now much sharper.

Earlier:

```text
pick a rank-one motion slot and rank-one time slot.
```

Now:

```text
derive S3 symmetry and project to the coherent singlet.
```

That is a much more respectable field-theory contract.

## Decision

Decision:

```text
singlet_motion_time_projectors_constructed_conditionally_not_parent_derived
```

Meaning:

```text
The rank-one motion/time projectors can be constructed as unique S3 singlet projectors.
This removes arbitrary basis-slot picking.
But the parent action still has to derive the S3 symmetry, no-clock singlet source, and ordinary/MTS sector split.
```

Allowed language:

```text
MTS has a conditional S3-singlet route for the rank-one motion/time projectors needed by the 2/27 amplitude schema.
```

Forbidden language:

```text
MTS derives B_mem=2/27.
```

## Next Target

The next derivation target is now narrow:

```text
derive or reject parent S3 cell symmetry and the sector label S_D.
```

The clean theorem route would be:

```text
K_cell commutes with S3_M x S3_T,
FLRW memory source lies in the singlet-singlet sector,
ordinary local baths lie outside the MTS boundary sector or are killed by S_D,
[K_boundary,S_D]=0,
screen bundle supplies the spatial rank-two factor.
```

If that route fails, the rank-two amplitude branch remains a disciplined closure, and the sensible next move is external empirical pressure: `Hz`, growth, CMB bridge, and local-GR compatibility tests.

## Output Files

```text
runs/20260601-140000-singlet-motion-time-projector-gate/results/source_register.csv
runs/20260601-140000-singlet-motion-time-projector-gate/results/S3_projector_algebra.csv
runs/20260601-140000-singlet-motion-time-projector-gate/results/full_cell_lift.csv
runs/20260601-140000-singlet-motion-time-projector-gate/results/invariant_source_tests.csv
runs/20260601-140000-singlet-motion-time-projector-gate/results/theorem_clauses.csv
runs/20260601-140000-singlet-motion-time-projector-gate/results/gate_results.csv
runs/20260601-140000-singlet-motion-time-projector-gate/results/decision.csv
```
