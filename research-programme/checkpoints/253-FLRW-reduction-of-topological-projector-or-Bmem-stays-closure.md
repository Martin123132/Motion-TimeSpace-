# 253 - FLRW Reduction of Topological Projector or Bmem Stays Closure

Private derivation checkpoint. This is not a cosmology support claim, CMB
claim, local-GR claim, or derivation of `B_mem = 2/27`.

## 1. Trigger

Checkpoint 252 gave N5 a conditional parent-action route:

```text
P_D is a metric-independent relative/topological chain projector.
```

That is good locally only if it is not a local-only repair. The same `P_D`
must also reduce to the FLRW memory projection.

## 2. Machine Artifact

Script:

```text
scripts/FLRW_reduction_of_topological_projector_or_Bmem_stays_closure.py
```

Run:

```text
runs/20260601-000070-FLRW-reduction-of-topological-projector-or-Bmem-stays-closure
```

Command:

```text
python scripts/FLRW_reduction_of_topological_projector_or_Bmem_stays_closure.py --timestamp 20260601-000070
```

Status:

```text
FLRW_topological_projector_reduction_derives_shape_conditionally_Bmem_2over27_rank_fraction_target_not_parent_derived
```

Claim ceiling:

```text
FLRW_shape_contract_only_Bmem_2over27_stays_closure_theorem_target
```

## 3. FLRW Reduction Chain

The same-projector route can be written cleanly:

```text
P_D local exterior -> metric-independent topological no-bulk-stress projector
P_D FLRW sector    -> homogeneous/isotropic coherent memory projector
```

On FLRW, any owned spatial coherent-load tensor has the symmetry form:

```text
Q^i_j = X_FLRW delta^i_j.
```

If the parent invariant is:

```text
I_M = det(Q),
```

then:

```text
I_M|FLRW = X_FLRW^3.
```

So the cubic activation shape remains conditionally derivable from the same
kind of structure. That is a real gain.

## 4. What Still Does Not Derive

The amplitude does not come out for free.

A topological projector can naturally give a rank fraction:

```text
B_mem = kappa_mem Tr(P_active) / dim(V_cell).
```

To get:

```text
B_mem = 2/27,
```

the parent theory must prove:

```text
dim(V_cell) = 27,
rank(P_active) = 2,
kappa_mem = 1.
```

Right now none of those three is parent-derived.

## 5. Rank-Fraction Target

The strongest honest theorem target is:

```text
V_cell has 3^3 topological/domain memory states,
P_active selects exactly 2 FLRW exchange modes,
the stress-exchange normalization is unity.
```

Then:

```text
Tr(P_active) / dim(V_cell) = 2 / 27.
```

This would be excellent if derived. But if we choose `27` and `2` because the
number is attractive, that is just numerology wearing a tie.

## 6. Empirical Note

The fixed-branch empirical corridor from the older private runs was:

```text
B_mem = 0.074533 to 0.153378.
```

The target is:

```text
2/27 = 0.074074.
```

That is interesting because it sits just under the lower fixed-branch corridor.
It is not evidence and not a derivation. It is a clue worth attacking, nothing
more.

## 7. Current Verdict

What improved:

```text
the same P_D skeleton can conditionally own the FLRW cubic shape route.
```

What did not improve enough:

```text
B_mem = 2/27 is not parent-derived.
```

The correct status is:

```text
p=3 shape: conditional route survives,
u3=1/4: conditional no-clock cell route survives,
B_mem=2/27: closure theorem-target only.
```

## 8. Claim Policy

Allowed:

```text
same-projector FLRW shape route is conditionally coherent.
```

Forbidden:

```text
B_mem = 2/27 is derived,
MTS passes cosmology,
MTS passes CMB,
local GR and cosmology are fully unified.
```

Allowed:

```text
2/27 is now a sharp theorem target: rank-27, rank-2, unity-normalization.
```

## 9. Decision

Decision:

```text
FLRW_topological_projector_reduction_derives_shape_conditionally_Bmem_2over27_rank_fraction_target_not_parent_derived
```

Meaning:

```text
we got the FLRW shape bridge to line up with the local topological projector
route, but the amplitude still has to earn its passport.
```

This is a “won the round on footwork, no knockout” result.

## 10. Next Target

Next:

```text
254-rank-27-rank-2-cell-theorem-or-Bmem-closure-lock.md
```

Purpose:

```text
try to derive the rank-27/rank-2/unity-normalization theorem. If it fails,
lock B_mem = 2/27 as an explicit empirical closure target until a real stress
normalization theorem exists.
```
