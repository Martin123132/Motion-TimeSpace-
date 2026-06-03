# 310 - Ordinary/MTS Sector Split Attempt

Private derivation checkpoint. This is not a public local-GR, PPN, cosmology, galaxy, CMB, or parent-field-theory claim.

## Purpose

Checkpoint 309 reduced the `P_MTS` problem to the ordinary/MTS sector split:

```text
<B_ord, B_MTS>_D = 0
```

or equivalently:

```text
K_boundary =
[
  K_ord      0
  0          K_MTS
].
```

This checkpoint asks:

```text
can that block split be derived rather than imposed?
```

Short answer:

```text
there is a clean conditional superselection lemma,
but the parent sector label is not derived yet.
```

## Boundary Sector Decomposition

Let the boundary data space be:

```text
H_B(D) = H_ord ⊕ H_MTS ⊕ H_edge.
```

Where:

```text
H_ord  = ordinary EM/matter/environmental boundary operators,
H_MTS  = coherent IR relative memory boundary channel,
H_edge = horizons, galaxies/clusters, and mixed time-dependent domains.
```

The needed parent object is a self-adjoint sector label:

```text
S_D.
```

With:

```text
S_D u = 0      for u in H_ord,
S_D v = v      for v in H_MTS.
```

Then:

```text
P_ord = 1 - S_D,
P_MTS = S_D
```

on the clean two-sector subspace.

## Conditional Superselection Lemma

Assume the boundary kinetic kernel obeys:

```text
[K_boundary, S_D] = 0.
```

Then for:

```text
u in H_ord,
v in H_MTS,
```

we have:

```text
<u, K_boundary v>
= <u, S_D K_boundary v>
= <S_D u, K_boundary v>
= 0.
```

Therefore:

```text
<H_ord, K_boundary H_MTS> = 0.
```

So:

```text
K_cross = 0.
```

This is the exact theorem route for:

```text
P_ord_perp.
```

It is not hand-wavy.

But it depends on the parent action deriving `S_D` and `[K_boundary,S_D]=0`.

## Important Subtlety

Gauge invariance alone is not enough.

Ordinary EM/matter stress can be:

```text
gauge-invariant,
neutral,
and gravitationally active.
```

So the argument:

```text
"ordinary baths are gauge stuff, MTS is memory stuff, so they cannot mix"
```

fails.

The correct separation must be:

```text
ordinary matter still couples universally through g_eff,
but ordinary bath data does not directly enter rho_MTS or sigma_D.
```

So the action must look schematically like:

```text
S = S_grav[g_eff, MTS]
  + S_matter[psi_m, g_eff]
  + S_boundary[B_ord, B_MTS]
```

with:

```text
S_boundary cross block = 0
```

by a parent sector symmetry or superselection rule.

## What Was Derived

| Result | Status |
|---|---|
| sector-split theorem target `H_B=H_ord⊕H_MTS⊕H_edge` | pass |
| block-kernel lemma from `[K,S]=0` | conditional pass |
| ordinary metric coupling preserved through `g_eff` | conditional pass |
| EM-stress gauge-neutral counterexample identified | pass as danger |
| parent sector label `S_D` | fail |
| parent block kernel `K_cross=0` | fail |

## No-Go Checks

| Claim | Result | Reason |
|---|---|---|
| gauge invariance alone forbids mixing | fail | EM/matter stress can be gauge-neutral |
| relative cohomology alone removes all ordinary baths | partial | it kills memory class, not generic stress spectra |
| universal metric coupling equals MTS boundary mixing | fail | ordinary matter must still gravitate |
| block diagonal kernel can be imposed after variation | fail | external projector / hidden Bianchi stress |
| split covers horizons and galaxies automatically | fail | those remain edge/domain branches |

## Promotion Gates

| Gate | Result | Meaning |
|---|---|---|
| source paths exist | pass | attempt traceable |
| sector decomposition written | pass | ordinary/MTS split is well-posed |
| block-kernel lemma proved | conditional pass | cross block vanishes if parent owns `S_D` |
| ordinary GR metric coupling preserved | conditional pass | projector need not delete gravity |
| gauge-neutral stress counterexample closed | fail | gauge slogans alone do not work |
| sector label parent-derived | fail | `S_D` is not action-owned |
| block kernel parent-derived | fail | `K_cross=0` not derived |
| Bianchi-safe split parent-closed | conditional pass | possible only with stress ledger |
| selector parent-derived | fail | `sigma_D` still a theorem target |
| local GR promoted | fail | no PPN/local-GR promotion |
| `B_mem` parent-derived | fail | `2/27` remains empirical closure/theorem target |

## Decision

Decision:

```text
ordinary_MTS_sector_split_conditional_superselection_lemma_cross_kernel_not_parent_derived
```

Claim ceiling:

```text
conditional_sector_split_no_Pord_parent_derivation_no_local_GR_or_selector_promotion
```

Meaning:

```text
we can derive the split if the parent supplies a sector label S_D
and a boundary kernel commuting with it;
we cannot yet derive that label or kernel.
```

Boxing-score version:

```text
We found the legal defensive move:
make ordinary and MTS boundary modes different weight classes.
Then the cross punch is illegal by the rules.
But we still need the parent action to write the rules,
not the corner shouting them from the stool.
```

## Next Step

There are two honest moves now.

Theory move:

```text
derive S_D.
```

Required contract:

```text
S_D = S_D(parent boundary variables, relative class, ordinary charges),
S_D^† = S_D,
[K_boundary,S_D]=0,
S_D H_ord = 0,
S_D H_MTS = H_MTS.
```

Empirical move:

```text
pivot back to holdout testing with the local branch labelled conditional.
```

My recommendation:

```text
one more theorem checkpoint for S_D/block-kernel origin,
then pivot to empirical holdouts if it remains conditional.
```

Reason:

```text
the derivation route is now very narrow;
if S_D does not appear naturally,
more local derivation attempts will start circling the same closure.
```

## Machine Artifacts

Script:

```text
scripts/ordinary_MTS_sector_split_attempt.py
```

Run:

```text
runs/20260601-000133-ordinary-MTS-sector-split-attempt
```

Output files:

```text
runs/20260601-000133-ordinary-MTS-sector-split-attempt/results/source_register.csv
runs/20260601-000133-ordinary-MTS-sector-split-attempt/results/sector_decomposition.csv
runs/20260601-000133-ordinary-MTS-sector-split-attempt/results/block_kernel_theorem.csv
runs/20260601-000133-ordinary-MTS-sector-split-attempt/results/mixing_risk_tests.csv
runs/20260601-000133-ordinary-MTS-sector-split-attempt/results/no_go_tests.csv
runs/20260601-000133-ordinary-MTS-sector-split-attempt/results/promotion_gates.csv
runs/20260601-000133-ordinary-MTS-sector-split-attempt/results/next_targets.csv
runs/20260601-000133-ordinary-MTS-sector-split-attempt/results/decision.csv
```
