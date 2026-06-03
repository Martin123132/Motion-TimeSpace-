# 294 - Endpoint Occupancy Arrow Law Attempt

Private derivation checkpoint. This is not a public cosmology, local-GR, CMB, or parent-field-theory claim.

## Purpose

The current amplitude chain is:

```text
B_mem = (n_early-n_today)/(3*k).
```

Checkpoints 292 and 293 made `k=9` conditional on a relative-index route.

The remaining endpoint target is:

```text
n_early=3
n_today=1
Delta n=2
```

This checkpoint asks:

```text
can the endpoint integers be derived without inserting roots by hand?
```

Short answer:

```text
Delta n=2 can be conditionally derived as a projector rank defect.
```

But:

```text
the arrow 3 -> 1 is not yet parent-owned.
```

## Projector Interpretation

Work inside the diagonal spatial axis-load sector:

```text
A = span{E_11,E_22,E_33} inside End(TSigma_D).
```

The resolved axis-load endpoint is:

```text
P_axis = I_A.
```

Therefore:

```text
n_early = Tr(P_axis)=3.
```

The scalar FLRW trace endpoint is the SO(3)-invariant trace projector:

```text
P_iso = (1/3) 11^T,
```

equivalently:

```text
Q -> (Tr Q/3) I.
```

Therefore:

```text
n_today = Tr(P_iso)=1.
```

So:

```text
Delta n = Tr(P_axis)-Tr(P_iso)=3-1=2.
```

This is the cleanest endpoint derivation found so far.

It does not use the built-to-order polynomial:

```text
V(n)=n(n-1)(n-3).
```

That polynomial remains rejected if inserted by hand.

## Representation Meaning

The full spatial endomorphism sector decomposes schematically as:

```text
End(R^3) = trace scalar + antisymmetric vector + symmetric traceless shear
```

with dimensions:

```text
9 = 1 + 3 + 5.
```

The FLRW scalar branch keeps only:

```text
trace scalar, dimension 1.
```

The endpoint law used here is narrower:

```text
three resolved diagonal axis occupancies collapse to one scalar trace occupancy.
```

That gives:

```text
3 -> 1.
```

So the endpoint integers now have a representation-theoretic meaning:

```text
3 = resolved spatial-axis rank,
1 = scalar trace-projector rank.
```

## Amplitude Chain

If the previous conditional results are accepted:

```text
k=9
trace partition=3
Delta n=2
```

then:

```text
B_mem = Delta n/(3*k)
      = 2/(3*9)
      = 2/27.
```

This is the first time the full number has a clean conditional chain:

```text
B3 relative index -> k=9
SO(3) trace projection -> factor 1/3
axis-to-scalar projector defect -> Delta n=2
```

But the word conditional is doing real work.

## Arrow Problem

The projector algebra gives:

```text
3 and 1.
```

It does not by itself give:

```text
3 -> 1.
```

Possible arrow routes:

| Route | Derives | Failure |
|---|---|---|
| SO(3) projection only | `Delta n=2` | no time direction |
| coarse-graining semigroup | resolved-to-scalar direction | semigroup not parent-derived |
| anisotropy penalty | scalar endpoint stable | does not make rank jump topological |
| Ward trace selection | trace couples to FLRW stress | early axis endpoint still needed |
| built endpoint potential | roots 1 and 3 | circular if inserted |

The best parent contract is:

```text
a Ward/trace action where only scalar trace charge couples to FLRW stress,
plus a parent time/coarse-graining law that maps resolved axis occupancy to scalar occupancy.
```

Until that is derived:

```text
the arrow remains closure.
```

## Gates

| Gate | Result | Meaning |
|---|---|---|
| source paths exist | pass | audit traceable |
| endpoint projectors defined | pass | `P_axis` and `P_iso` are exact |
| `Delta n` derived | conditional pass | `Tr(P_axis)-Tr(P_iso)=2` |
| SO(3) trace projection unique | pass | scalar FLRW endpoint is clean |
| early axis endpoint parent-owned | fail | `P_axis` not action-selected yet |
| arrow parent-owned | fail | `3 -> 1` not dynamically derived |
| `B_mem` derived | fail | conditional chain only |
| local silence derived | fail | no local-GR/PPN promotion |

## Decision

Decision:

```text
endpoint_occupancy_delta_n2_conditionally_derived_arrow_not_parent_owned
```

Meaning:

```text
the endpoint integer gap Delta n=2 now has a clean projector-rank derivation,
but the irreversible endpoint arrow is not yet owned by the parent theory.
```

What improved:

```text
n=3 and n=1 are no longer arbitrary roots.
```

They can be read as:

```text
Tr(P_axis)=3,
Tr(P_iso)=1.
```

What did not improve:

```text
the parent action still has not proved why the physical path runs from P_axis to P_iso.
```

So:

```text
B_mem=2/27 remains a locked empirical closure/theorem target,
not a completed derivation.
```

Boxing-score version:

```text
We finally made the 3 and the 1 throw real punches:
rank three axis load into rank one scalar trace.
But the bell that sends the fight from 3 to 1 has not rung yet.
Good counter. Still no stoppage.
```

## Machine Artifacts

Script:

```text
scripts/endpoint_occupancy_arrow_attempt.py
```

Run:

```text
runs/20260601-000117-endpoint-occupancy-arrow-attempt
```

Output files:

```text
runs/20260601-000117-endpoint-occupancy-arrow-attempt/results/source_register.csv
runs/20260601-000117-endpoint-occupancy-arrow-attempt/results/projector_algebra.csv
runs/20260601-000117-endpoint-occupancy-arrow-attempt/results/representation_decomposition.csv
runs/20260601-000117-endpoint-occupancy-arrow-attempt/results/arrow_routes.csv
runs/20260601-000117-endpoint-occupancy-arrow-attempt/results/amplitude_chain.csv
runs/20260601-000117-endpoint-occupancy-arrow-attempt/results/gate_results.csv
runs/20260601-000117-endpoint-occupancy-arrow-attempt/results/decision.csv
```

## Next Step

The next exact target is now:

```text
derive the arrow from parent time/coarse-graining/Ward trace action.
```

The sharp contract is:

```text
parent dynamics must make P_axis -> P_iso monotone,
without inserting the endpoint roots or amplitude by hand.
```

If that fails:

```text
the full 2/27 chain remains an elegant conditional closure,
not a fundamental derivation.
```
