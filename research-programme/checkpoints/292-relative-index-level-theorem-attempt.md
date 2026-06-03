# 292 - Relative Index Level Theorem Attempt

Private derivation checkpoint. This is not a public cosmology, local-GR, CMB, or parent-field-theory claim.

## Purpose

Checkpoint 288 left the cleanest exact target:

```text
construct an explicit differential complex on End(TSigma_D)
whose relative index/period level is 9.
```

This checkpoint attempts that construction.

The question is:

```text
can k=9 be more than component counting?
```

Short answer:

```text
yes, conditionally.
```

But:

```text
this still does not derive B_mem=2/27.
```

## Construction

Take a coherent spatial domain:

```text
D = compact oriented 3-domain with boundary partial D.
```

Use the spatial load/coframe endomorphism bundle:

```text
E_D = End(TSigma_D).
```

Because the spatial tangent bundle is rank three:

```text
rank(E_D)=3*3=9.
```

Construct the relative de Rham complex:

```text
0 -> Omega^0(D,E_D)
  -> Omega^1(D,E_D)
  -> Omega^2(D,E_D)
  -> Omega^3(D,E_D)
  -> 0
```

with relative boundary conditions.

For a flat/admissible coefficient connection:

```text
index(D,E_D,rel)=rank(E_D)*chi(D,partial D).
```

This is the key improvement over the previous rank-counting language.

It is now an index statement.

## Contractible Cell Result

For a single coherent contractible 3-cell:

```text
chi(D)=1
chi(partial D)=chi(S2)=2
chi(D,partial D)=-1
```

Therefore:

```text
index(D,E_D,rel)=9*(-1)=-9.
```

So the level magnitude is:

```text
|index|=9.
```

That means:

```text
k=9 can be conditionally derived
from a relative index theorem
if the parent theory selects a single contractible coherent 3-cell.
```

This is a real gain.

It is not the whole amplitude.

## Topology Sensitivity

The result is topology-sensitive:

| Domain | Boundary | chi(D,partial D) | index | Result |
|---|---|---:|---:|---|
| contractible 3-cell | `S2` | -1 | -9 | conditional k=9 |
| solid torus | `T2` | 0 | 0 | wrong |
| spherical shell | `S2 union S2` | -2 | -18 | wrong |
| closed 3-domain | none | 0 | 0 | no relative source |

So this checkpoint does not let us say:

```text
k=9 is automatic.
```

It lets us say:

```text
k=9 follows from a very specific coherent-domain topology:
one contractible 3-cell with relative boundary conditions.
```

The missing theorem is now sharper:

```text
derive that domain topology from the parent action.
```

## Period And Trace Chain

The conditional chain is:

```text
relative index on End(TSigma_D) -> |index|=9.
```

Then one wants:

```text
Q_* = 1/9.
```

But the index alone only says:

```text
there are nine relative load channels.
```

It does not force the scalar charge to be the average over those channels.

That still needs a Ward/trace rule:

```text
q_scalar = (1/9) Tr_End(q).
```

The trace partition has a cleaner route:

```text
Pi_iso(Q)=(Tr Q/3) I.
```

This is the unique SO(3)-equivariant isotropic projection of a spatial endomorphism.

So the one-third factor is conditionally derivable from isotropic spatial projection.

The full target chain is:

```text
B_mem = (n_early-n_today)/(3*9).
```

If:

```text
n_early=3
n_today=1
```

then:

```text
B_mem=2/27.
```

But the endpoint occupancy law is still not derived.

## What Improved

Before this checkpoint:

```text
k=9 was mostly rank/component language.
```

After this checkpoint:

```text
k=9 has a conditional relative-index derivation.
```

The derivation is:

```text
E_D=End(TSigma_D),
rank(E_D)=9,
chi(D,partial D)=-1 for a coherent 3-cell,
therefore index=-9.
```

That is a better foundation.

It is the first clean mathematical route where the number 9 is not just fitted or hand-picked.

## What Still Fails

The following are still missing:

| Missing theorem | Status | Why it matters |
|---|---|---|
| domain topology selection | fail | other topologies do not give k=9 |
| normalized period denominator | fail | index counts channels but does not force `Q_*=1/9` |
| endpoint occupancies | fail | need `3 -> 1` |
| endpoint arrow | fail | parent dynamics must select the direction |
| local silence | fail | index does not make local source periods vanish |

Therefore:

```text
B_mem=2/27 remains a locked empirical closure/theorem target.
```

and:

```text
local GR is not promoted.
```

## Gates

| Gate | Result | Meaning |
|---|---|---|
| source paths exist | pass | audit traceable |
| relative complex constructed | conditional pass | real index route exists |
| contractible cell gives level 9 | conditional pass | `index=-9` |
| domain topology derived | fail | parent action has not selected the cell |
| period denominator derived | fail | normalized trace still needed |
| trace partition from SO(3) | conditional pass | `Pi_iso(Q)=(Tr Q/3)I` |
| endpoint law derived | fail | `n=3 -> 1` not owned |
| local silence derived | fail | no local-GR/PPN promotion |
| `B_mem` derived | fail | locked closure retained |

## Decision

Decision:

```text
relative_index_level_derives_conditional_k9_not_full_Bmem
```

Meaning:

```text
we have upgraded k=9 from a naked rank target to a conditional relative-index theorem.
```

The theorem is:

```text
if coherent memory domains are single contractible 3-cells,
then the relative index of the End(TSigma_D) complex has magnitude 9.
```

The amplitude is not derived because:

```text
domain topology,
period normalization,
endpoint occupancies,
endpoint arrow,
and local silence
remain unproved.
```

Boxing-score version:

```text
We did not win the belt,
but we finally landed a proper clean counter:
the nine is now an index target, not just "look, 3x3".
Still no knockout until the endpoint law walks into the ring.
```

## Machine Artifacts

Script:

```text
scripts/relative_index_level_attempt.py
```

Run:

```text
runs/20260601-000115-relative-index-level-attempt
```

Output files:

```text
runs/20260601-000115-relative-index-level-attempt/results/source_register.csv
runs/20260601-000115-relative-index-level-attempt/results/complex_construction.csv
runs/20260601-000115-relative-index-level-attempt/results/domain_index_sensitivity.csv
runs/20260601-000115-relative-index-level-attempt/results/period_and_trace_chain.csv
runs/20260601-000115-relative-index-level-attempt/results/endpoint_blockers.csv
runs/20260601-000115-relative-index-level-attempt/results/gate_results.csv
runs/20260601-000115-relative-index-level-attempt/results/decision.csv
```

## Next Step

The next derivation fork is now precise:

```text
derive the coherent-domain topology selection,
or derive the endpoint occupancy/arrow law.
```

Best next theory target:

```text
try to derive why the coherent FLRW memory domain must be a single contractible 3-cell.
```

Reason:

```text
without that topology theorem, the index route is conditional.
```

If that fails:

```text
the k=9 route remains a strong closure contract,
not a parent-derived amplitude.
```
