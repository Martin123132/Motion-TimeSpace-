# 288 - k=9 Ward / Index Level Attempt

Private derivation checkpoint. This is not a public field-theory, CMB, local-GR, or amplitude-prediction claim.

## Purpose

Checkpoint 287 made the amplitude problem integer-level precise:

```text
R_today = 1/9
R_early = 1/3
DeltaR = 2/9
B_mem = 2/27
```

with minimal integer data:

```text
k = 9
n_today = 1
n_early = 3
delta_n = 2.
```

This checkpoint asks:

```text
Can k=9 be derived as a Ward/index level rather than component counting?
```

Short verdict:

```text
Not yet.
```

The cleanest target is real:

```text
k=9 as rank End(TSigma_D) = 3 x 3.
```

But:

```text
rank is not a Ward identity.
```

It does not by itself define:

```text
Q_*,
integral periods,
endpoint occupancies,
endpoint arrow,
or B_mem = DeltaR/3.
```

## Machine Artifact

Script:

```text
scripts/k9_Ward_index_level_attempt.py
```

Run:

```text
runs/20260601-000111-k9-Ward-index-level-attempt
```

Status:

```text
k9_Ward_index_level_not_derived_rank9_bundle_target_retained
```

Claim ceiling:

```text
k9_theorem_target_only_no_Bmem_or_parent_promotion
```

## Candidate Routes

| Candidate | What it gives | Why it fails as derivation |
|---|---|---|
| `rank End(TSigma)=3x3=9` | natural nine-slot lattice for `Q^i_j` | rank is component counting unless periods are parent-defined |
| `dim GL(3)=9` | full spatial deformation channel | FLRW branch uses trace/isotropic line |
| `dim so(3)=3` | rotational gauge sector | wrong level and mostly gauge |
| `27/3=9` | connects determinant `p=3` to trace partition | post-hoc unless variation yields it |
| BF/Chern-Simons level | integral periods | level is free unless anomaly/Ward cancellation fixes `9` |
| Euler/signature index | genuine if index equals `9` | no explicit bundle/operator/index exists |

So the best theorem target is:

```text
E_D = End(TSigma_D),
rank(E_D) = 9,
and the parent action must make the relative charge periods live in (1/9)Z.
```

That would be meaningful.

But we have not derived it.

## Rank-9 Bundle Tests

| Test | Status | Blocker |
|---|---|---|
| parent bundle defined | partial | `Q^i_j` exists conditionally, but charge lattice not selected |
| integral period structure | fail | `Q_*` remains free |
| isotropic projection compatibility | open | FLRW trace line may collapse denominator to `1` or `3` |
| endpoint occupancy selection | fail | no dynamics selects `n=1,3` |
| endpoint arrow | fail | no theorem selects `3 -> 1` |
| trace partition | conditional | `B_mem=DeltaR/3` still needs Ward coupling |

This matters because `9` is tempting.

It is not worthless numerology:

```text
Q^i_j really is a spatial endomorphism object.
```

But it is also not yet physics:

```text
no parent action has turned those nine slots into a normalized charge unit.
```

## What A Real Index Theorem Must Provide

To promote `k=9`, we would need all of:

| Requirement | Must exist |
|---|---|
| operator / complex | parent differential complex whose index counts the relative charge level |
| bundle choice | complex acts on spatial load/coframe endomorphism bundle |
| index value | `index(E_D)=9` or effective period denominator `9` |
| boundary condition | local bound domains trivial, FLRW domains nontrivial |
| Ward trace coupling | variation maps level charge into stress with one-third trace partition |

None of those are currently derived.

So:

```text
k=9 remains a sharp theorem target, not a theorem.
```

## Endpoint Occupancy Law

Even if `k=9` were derived, the endpoint law still has to select:

```text
n_today = 1
n_early = 3.
```

Attempted laws:

| Law | Status | Reason |
|---|---|---|
| endpoint quadratic `27R^2-12R+1=0` | formal target | coefficients not parent-produced |
| occupancy potential `V(n)=n(n-1)(n-3)` | rejected if inserted | built-to-order polynomial |
| monotone charge relaxation | open | no entropy/event law |
| rank drop `3 -> 1` | motivation only | not a variational theorem |

This kills a subtle cheat:

```text
deriving k=9 alone would still not derive 2/27.
```

You also need:

```text
n=3 -> n=1,
and B_mem=(3-1)/(3*9).
```

## Gates

| Gate | Result | Meaning |
|---|---|---|
| source paths exist | pass | audit traceable |
| rank-9 natural target | pass as target | `End(TSigma)` has rank 9 |
| rank-9 derives charge lattice | fail | rank does not define periods or `Q_*` |
| Ward/index theorem exists | fail | no operator/complex/anomaly cancellation |
| endpoint occupancies derived | fail | `n=1,3` are target occupancies only |
| trace partition derived | fail | `B_mem=DeltaR/3` conditional |
| local silence derived | fail | local trivial class conditional |
| `B_mem` derived | fail | all required pieces remain unproven |

## Decision

Decision:

```text
k9_Ward_index_level_not_derived_rank9_bundle_target_retained
```

Meaning:

```text
rank End(TSigma)=9 is the best non-circular k=9 target,
but it is not a Ward/index derivation.
```

What improved:

```text
we now know exactly what k=9 would have to mean:
an integral relative charge lattice on the spatial load/coframe endomorphism bundle.
```

What did not improve:

```text
B_mem=2/27 remains locked empirical closure.
local GR remains unpromoted.
parent field theory remains incomplete.
```

Boxing-score version:

```text
We found the right gym door: the nine-slot spatial endomorphism bundle.
But we have not found the coach with the key: the Ward/index theorem.
No key, no title shot.
```

## Output Files

```text
runs/20260601-000111-k9-Ward-index-level-attempt/results/source_register.csv
runs/20260601-000111-k9-Ward-index-level-attempt/results/candidate_k9_routes.csv
runs/20260601-000111-k9-Ward-index-level-attempt/results/rank9_bundle_tests.csv
runs/20260601-000111-k9-Ward-index-level-attempt/results/index_theorem_requirements.csv
runs/20260601-000111-k9-Ward-index-level-attempt/results/endpoint_occupancy_law.csv
runs/20260601-000111-k9-Ward-index-level-attempt/results/noncircularity_tests.csv
runs/20260601-000111-k9-Ward-index-level-attempt/results/gate_results.csv
runs/20260601-000111-k9-Ward-index-level-attempt/results/decision.csv
```

## Next Step

At this point the derivation branch has done its job for this round:

```text
it narrowed the amplitude problem to an exact but unproven k=9 Ward/index theorem.
```

Recommended next:

```text
return to empirical robustness: run the no-SH0ES shape branch,
then DESI DR1/DR2 fixed-branch comparison.
```

Reason:

```text
the theory route is now fenced cleanly.
The fastest way to improve the whole framework is to test whether the locked/fixed branch survives calibration pressure removal.
```

If the theory route is continued instead, the next exact target is:

```text
construct an explicit differential complex on End(TSigma_D)
whose relative index/period level is 9.
```
