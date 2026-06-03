# 321 — Rank-Two Screen Projector Gate

Private derivation checkpoint. This is not a public amplitude, local-GR, CMB, or unified-field claim.

## Purpose

Checkpoint 320 showed that the locked amplitude target needs:

```text
B_mem = kappa_mem Tr(P_active) / dim(V_cell),
dim(V_cell)=27,
Tr(P_active)=2,
kappa_mem=1.
```

This checkpoint asks:

```text
Can Tr(P_active)=2 be derived from a no-clock / transverse-screen projector?
```

Short answer:

```text
rank-two projector algebra: yes, conditionally
parent-derived rank two: no
amplitude promotion: no
```

The work is still useful because it catches a hidden trap.

## Machine Artifact

Script:

```text
scripts/rank_two_screen_projector_gate.py
```

Run:

```text
runs/20260601-132500-rank-two-screen-projector-gate
```

Status:

```text
rank_two_full_cell_projector_constructed_conditionally_not_parent_derived
```

Claim ceiling:

```text
conditional_rank_two_projector_no_Bmem_or_local_GR_promotion
```

## The Trap

A two-dimensional spatial screen projector by itself is not enough.

If we write:

```text
P_screen = h - n n
```

then in the three-dimensional spatial sector:

```text
Tr(P_screen)=2.
```

But the full parent cell target is:

```text
V_cell = V_M tensor V_T tensor V_S,
dim(V_cell)=3*3*3=27.
```

If we lift the spatial screen naively:

```text
I_M tensor I_T tensor P_screen,
```

then:

```text
rank = 3*3*2 = 18,
Tr/27 = 18/27 = 2/3.
```

That is not `2/27`.

So the correct full-cell construction must be:

```text
P_active = P_M tensor P_T tensor P_screen,
rank(P_M)=1,
rank(P_T)=1,
rank(P_screen)=2.
```

Then:

```text
rank(P_active)=1*1*2=2,
Tr(P_active)/27=2/27.
```

This is the first clean full-cell rank-two construction.

## Algebra Results

| Object | Dimension | Trace | Rank | Normalized trace |
|---|---:|---:|---:|---:|
| `P_M` | `3` | `1` | `1` | — |
| `P_T` | `3` | `1` | `1` | — |
| `P_screen` | `3` | `2` | `2` | — |
| `P_active` | `27` | `2` | `2` | `2/27` |
| bad spatial lift | `27` | `18` | `18` | `2/3` |
| scalar trace alternative | `27` | `1` | `1` | `1/27` |
| full spatial alternative | `27` | `3` | `3` | `1/9` |

All listed projectors are idempotent in the algebraic construction.

The lead conditional target is:

```text
P_active = P_M(rank 1) tensor P_T(rank 1) tensor P_screen(rank 2).
```

## FLRW Isotropy Check

A fixed screen normal `n` would break isotropy.

But the screen bundle can be angular averaged:

```text
<P_screen> = (2/3) I.
```

This keeps:

```text
Tr(<P_screen>) = 2.
```

and gives an isotropic FLRW tensor.

Important subtlety:

```text
<P_screen>
```

is not idempotent. The projector is fiberwise; the averaged FLRW tensor preserves the trace but not the projector property.

That is acceptable only if the parent theory supplies a screen-bundle measure. It is not acceptable as a standalone parent proof.

## Gate Results

| Gate | Status |
|---|---|
| source paths exist | pass |
| `P_active^2=P_active` | pass |
| `rank(P_active)=2` | pass |
| `Tr(P_active)/27=2/27` | pass |
| bad spatial lift rejected | pass |
| screen-bundle FLRW isotropy | pass |
| rank-one motion channel parent-derived | fail |
| rank-one time/no-clock channel parent-derived | fail |
| screen normal parent-derived | fail |
| screen-only local silence | fail |
| `kappa_mem=1` parent-derived | fail |
| amplitude promotion allowed | fail |

## What This Actually Wins

We now know the exact rank-two construction required:

```text
one coherent motion/load channel
one no-clock time/history channel
two transverse screen channels
```

That gives:

```text
1 * 1 * 2 = 2.
```

So `2/27` can be read as:

```text
two active channels out of the twenty-seven motion-time-space cell slots.
```

That is a much cleaner theorem target than generic component-counting.

## What Still Fails

The parent action has not yet proved:

```text
rank(P_M)=1,
rank(P_T)=1,
n or the screen bundle is generated before fitting,
ordinary local transverse baths are annihilated,
kappa_mem=1.
```

The local silence failure matters. A screen projector alone does not distinguish MTS memory from ordinary transverse EM/radiation/laboratory boundary data.

So it must still be combined with the earlier boundary projector contract:

```text
P_MTS = P_Ward P_coh P_IR P_rel P_ord_perp.
```

Without that, screen rank two would be locally dangerous.

## Decision

Decision:

```text
rank_two_full_cell_projector_constructed_conditionally_not_parent_derived
```

Meaning:

```text
The rank-two algebra is real if the parent theory supplies rank-one motion/time channels and a screen-bundle projector.
But those structures are not yet parent-derived, and the amplitude remains closure-level.
```

Allowed language:

```text
MTS has a conditional full-cell rank-two projector construction whose normalized trace is 2/27.
```

Forbidden language:

```text
MTS derives B_mem=2/27.
```

## Next Target

The next derivation attempt should not be another broad amplitude essay.

It should target the factor projectors:

```text
derive P_M and P_T as rank-one parent projectors,
or demote rank two to a screen-bundle closure.
```

The exact theorem target is:

```text
P_M^2=P_M, Tr(P_M)=1,
P_T^2=P_T, Tr(P_T)=1,
P_screen^2=P_screen, Tr(P_screen)=2,
[P_M,P_T]=[P_M,P_screen]=[P_T,P_screen]=0
```

on the tensor-product cell space, with the local boundary filters proving ordinary local baths do not activate the same channel.

## Output Files

```text
runs/20260601-132500-rank-two-screen-projector-gate/results/source_register.csv
runs/20260601-132500-rank-two-screen-projector-gate/results/projector_algebra.csv
runs/20260601-132500-rank-two-screen-projector-gate/results/angular_average.csv
runs/20260601-132500-rank-two-screen-projector-gate/results/lift_hazard_ledger.csv
runs/20260601-132500-rank-two-screen-projector-gate/results/theorem_clauses.csv
runs/20260601-132500-rank-two-screen-projector-gate/results/gate_results.csv
runs/20260601-132500-rank-two-screen-projector-gate/results/decision.csv
```
