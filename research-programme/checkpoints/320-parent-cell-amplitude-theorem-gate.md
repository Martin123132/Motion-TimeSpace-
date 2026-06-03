# 320 — Parent-Cell Amplitude Theorem Gate

Private derivation checkpoint. This is not a public amplitude, CMB, local-GR, or unified-field claim.

## Purpose

Checkpoint 319 made the locked branch harder to dismiss:

```text
B_mem = 2/27,
p = 3,
u3 = 1/4
```

survives the first symmetric split robustness pass well. That raises the value of the amplitude target.

This checkpoint asks the hard theory question again:

```text
Can 2/27 now be derived from the parent cell/action structure?
```

Short answer:

```text
conditional theorem schema: yes
parent derivation in current corpus: no
```

So we have sharpened the exact theorem contract, not won the promotion.

## Machine Artifact

Script:

```text
scripts/parent_cell_amplitude_theorem_gate.py
```

Run:

```text
runs/20260601-131500-parent-cell-amplitude-theorem-gate
```

Status:

```text
parent_cell_amplitude_conditional_schema_but_not_parent_derived
```

Claim ceiling:

```text
conditional_parent_cell_schema_no_Bmem_amplitude_promotion
```

## Conditional Theorem

The clean parent-cell theorem would be:

```text
B_mem = kappa_mem Tr(P_active) / dim(V_cell).
```

If the parent action proves:

```text
V_cell = V_M tensor V_T tensor V_S,
dim(V_M)=dim(V_T)=dim(V_S)=3,
dim(V_cell)=27,
P_active^2=P_active,
rank(P_active)=2,
kappa_mem=1,
```

then:

```text
B_mem = 1 * 2/27 = 2/27.
```

That is not numerology. It is a real algebraic route.

But it is conditional on clauses that are not all derived.

## Clause Audit

| Clause | Requirement | Current status |
|---|---|---|
| `C1` | `dim(V_cell)=27` from a `3x3x3` motion-time-space cell | partial |
| `C2` | normalized cell trace `Tr(P_active)/dim(V_cell)` | partial |
| `C3` | idempotent projector `P_active^2=P_active` | partial |
| `C4` | active projector rank `2` | partial |
| `C5` | `kappa_mem=1` with no rescalable prefactor | fail |
| `C6` | same channel is locally PPN-silent | partial |

The exact gate result is:

| Gate | Status |
|---|---|
| source paths exist | pass |
| `dim27` parent-derived | fail |
| normalized trace parent-derived | fail |
| projector parent-derived | fail |
| rank-2 parent-derived | fail |
| `kappa_mem=1` parent-derived | fail |
| local silence parent-derived | fail |
| conditional theorem schema valid | pass |
| amplitude promotion allowed | fail |

## What Was Actually Derived

The following implication is now clean:

```text
3x3x3 parent cell
+ normalized cell trace
+ rank-2 active screen projector
+ unit normalization
=> B_mem = 2/27.
```

This is useful because it tells us exactly what a future parent action must produce.

It also tells us what cannot be claimed yet.

## Why Rank Two Is Tempting But Not Owned

The best rank-two story is:

```text
no-clock FLRW memory activates the two transverse/screen directions.
```

That would naturally give:

```text
rank(P_active)=2.
```

Then, with a `27`-dimensional parent cell and unit normalized trace:

```text
B_mem=2/27.
```

But FLRW scalar symmetry alone does not force this. Other ranks are still logically available:

| Route | Rank | Amplitude if `dim=27`, `kappa=1` | Status |
|---|---:|---:|---|
| scalar trace channel | `1` | `1/27` | not excluded by FLRW scalar symmetry alone |
| transverse screen channel | `2` | `2/27` | lead theorem target |
| full spatial channel | `3` | `1/9` | not excluded without local silence/trace subtraction |
| traceless symmetric spatial channel | `5` | `5/27` | not minimal FLRW background |

Therefore:

```text
rank two is physically promising,
but not parent-derived.
```

## Why Kappa Still Blocks Promotion

Even if we get:

```text
dim(V_cell)=27,
rank(P_active)=2,
```

the amplitude is still:

```text
B_mem = kappa_mem * 2/27.
```

Checkpoint 317 already proved the hard no-go:

```text
S_mem -> lambda S_mem
```

leaves the diffeomorphism Ward identity and FLRW continuity structure intact.

So ordinary conservation cannot fix:

```text
kappa_mem=1.
```

That still needs a genuinely non-homogeneous normalization mechanism:

```text
trace anomaly,
index theorem,
flux quantization,
boundary charge unit,
or parent measure normalization.
```

Without that, `kappa_mem=1` is still a clean closure, not a theorem.

## Current Verdict

This is a better position than before, but still not a promotion.

The branch now has:

```text
shape route: conditionally derived
LCDM limit: derived
split robustness: strengthened
2/27 algebraic parent-cell target: sharpened
amplitude theorem: still incomplete
```

Boxing readout:

```text
This is not a knockout.
But we have found the exact punch combination:
27-dimensional cell, rank-two screen projector, unit normalization.
The missing part is proving the glove is regulation weight, not choosing it.
```

## Decision

Decision:

```text
parent_cell_amplitude_conditional_schema_but_not_parent_derived
```

Meaning:

```text
B_mem=2/27 is now a sharper theorem target:
rank-two over twenty-seven with unit normalization.
But the current parent theory does not yet force rank two or kappa_mem=1.
```

Allowed language:

```text
The locked 2/27 branch is empirically strengthened and has a precise conditional parent-cell theorem schema.
```

Forbidden language:

```text
MTS derives B_mem=2/27 from the parent action.
```

## Next Target

There are now only two honest derivation routes:

1. Derive `rank(P_active)=2` from a no-clock/transverse-screen projector produced by the parent action.
2. Derive `kappa_mem=1` from a non-homogeneous normalization theorem.

The more promising next attempt is rank first:

```text
construct P_active as a parent projector,
prove P_active^2=P_active,
prove Tr(P_active)=2,
and prove it is FLRW-active but locally PPN-silent.
```

If that fails, `2/27` remains a locked empirical closure and the next pressure should move to external `Hz`, growth, CMB bridge, and local-GR compatibility tests.

## Output Files

```text
runs/20260601-131500-parent-cell-amplitude-theorem-gate/results/source_register.csv
runs/20260601-131500-parent-cell-amplitude-theorem-gate/results/theorem_clauses.csv
runs/20260601-131500-parent-cell-amplitude-theorem-gate/results/amplitude_family.csv
runs/20260601-131500-parent-cell-amplitude-theorem-gate/results/rank_route_ledger.csv
runs/20260601-131500-parent-cell-amplitude-theorem-gate/results/kappa_degeneracy.csv
runs/20260601-131500-parent-cell-amplitude-theorem-gate/results/conditional_theorem.csv
runs/20260601-131500-parent-cell-amplitude-theorem-gate/results/gate_results.csv
runs/20260601-131500-parent-cell-amplitude-theorem-gate/results/decision.csv
```
