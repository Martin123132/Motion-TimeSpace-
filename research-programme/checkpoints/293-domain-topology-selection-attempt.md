# 293 - Domain Topology Selection Attempt

Private derivation checkpoint. This is not a public cosmology, local-GR, CMB, or parent-field-theory claim.

## Purpose

Checkpoint 292 found a real conditional foothold:

```text
if the coherent memory domain is a single contractible 3-cell,
then the relative End(TSigma_D) index has magnitude 9.
```

This checkpoint asks:

```text
can the parent theory force that domain topology?
```

Short answer:

```text
not yet.
```

But the condition can be made mathematically sharp.

## Conditional Theorem

Let `D` be a compact connected oriented spatial 3-domain.

If:

```text
1. partial D is a single connected isotropic boundary,
2. partial D is S2-like,
3. D has no H1 or H2 harmonic cycle sectors,
4. D has no hidden irreducible/prime interior factor,
```

then `D` is a B3-like coherent cell.

For that cell:

```text
chi(D,partial D)=-1.
```

Then checkpoint 292 applies:

```text
index(D,End(TSigma_D),rel)=9*(-1)=-9,
```

so:

```text
|index|=9.
```

That is the clean topology theorem target.

## Why The Assumptions Are Not Random

The assumptions are not arbitrary decoration.

They map onto physical requirements:

| Assumption | Physics meaning | Status |
|---|---|---|
| compact connected oriented 3-domain | coherent spatial cell exists | reasonable background |
| single connected boundary | one memory interface | not derived |
| `S2` isotropic boundary | scalar FLRW symmetry | conditional |
| no `H1/H2` cycles | no internal vector/cavity memory modes | not derived |
| irreducible interior | no hidden topological defect | not derived |

This is better than simply saying:

```text
assume a ball.
```

It says exactly what the theory must prove to earn the ball.

## Topology Sensitivity

The relative-index result is very topology-sensitive:

| Candidate domain | Boundary | Cycle content | Relative index with rank 9 | Verdict |
|---|---|---|---:|---|
| `B3` contractible cell | `S2` | none | -9 | target |
| solid torus | `T2` | one handle | 0 | rejected |
| spherical shell | `S2 union S2` | cavity mode | -18 | rejected |
| closed 3-domain | none | no relative boundary | 0 | rejected |

So:

```text
the k=9 index is not generic.
```

It belongs to:

```text
a single S2-boundary, no-cycle coherent 3-cell.
```

That is good because it is restrictive.

It is also bad because the restriction must be derived.

## Attempted Parent Routes

| Route | What it can derive | Failure |
|---|---|---|
| FLRW symmetry only | `S2`-like isotropic boundary | not single boundary/no cycles |
| harmonic-mode penalty | zero active harmonic amplitudes | topology itself can remain nontrivial |
| domain-complexity penalty | minimal B3 topology | closure unless parent-owned |
| relative-current admissibility | B3-like admissible class | still needs derivation |
| local-silence same rule | possible local safety bridge | representative selection missing |

The strongest non-cheating route is:

```text
relative-current admissibility.
```

It would say:

```text
the scalar FLRW memory branch only admits domains with one top relative class
and no lower harmonic classes.
```

That would pick the B3-like topology without inserting `B3` directly.

But right now it is a contract, not a theorem.

## Important No-Go

A local differential equation on a fixed domain usually does not change topology.

So a parent field equation alone is unlikely to derive:

```text
D = B3.
```

To derive it, the parent framework needs one of:

```text
1. an admissible-domain principle,
2. a free-boundary/domain-sum measure,
3. a topological sector penalty derived from the action,
4. an anomaly/Ward cancellation that kills H1/H2 sectors.
```

Without one of those, domain topology is a superselection choice.

That means:

```text
B3 is not parent-derived yet.
```

## Gates

| Gate | Result | Meaning |
|---|---|---|
| source paths exist | pass | audit traceable |
| conditional B3 theorem formulated | pass | exact target written |
| FLRW symmetry selects `S2` boundary | conditional pass | scalar symmetry helps |
| single boundary component derived | fail | shell/cavity domains not forbidden |
| no-cycle rule derived | fail | `H1/H2` sectors not parent-killed |
| B3 domain derived | fail | k=9 remains conditional |
| `B_mem` derived | fail | amplitude still needs period and endpoint law |

## Decision

Decision:

```text
coherent_domain_topology_selection_conditional_not_parent_derived
```

Meaning:

```text
we can state the exact topology theorem needed for the k=9 index route,
but we cannot yet derive the theorem from the parent action.
```

What improved:

```text
the ball/cell assumption is no longer vague.
```

It is now:

```text
single S2 boundary
+ no H1/H2 cycle sectors
+ irreducible interior.
```

What did not improve:

```text
the parent action still has not selected that topology.
```

Boxing-score version:

```text
We found the exact footwork drill:
one clean S2 boundary, no handles, no cavity.
But the coach has not yet proved why the fighter must use that stance.
Good form. Not yet a mandatory rule.
```

## Machine Artifacts

Script:

```text
scripts/domain_topology_selection_attempt.py
```

Run:

```text
runs/20260601-000116-domain-topology-selection-attempt
```

Output files:

```text
runs/20260601-000116-domain-topology-selection-attempt/results/source_register.csv
runs/20260601-000116-domain-topology-selection-attempt/results/topology_candidates.csv
runs/20260601-000116-domain-topology-selection-attempt/results/conditional_theorem_assumptions.csv
runs/20260601-000116-domain-topology-selection-attempt/results/variational_routes.csv
runs/20260601-000116-domain-topology-selection-attempt/results/gate_results.csv
runs/20260601-000116-domain-topology-selection-attempt/results/decision.csv
```

## Next Step

The domain route is now pinned but not promoted.

Best next derivation target:

```text
derive the endpoint occupancy/arrow law:
n_early=3 -> n_today=1.
```

Reason:

```text
even if the B3 topology theorem is later supplied,
B_mem still does not follow without the endpoint law.
```

The honest target is:

```text
find a parent variational or Ward rule that gives Delta n = 2
without inserting the polynomial roots by hand.
```
