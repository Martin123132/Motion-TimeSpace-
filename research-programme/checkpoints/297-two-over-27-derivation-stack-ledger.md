# 297 - Two-Over-27 Derivation Stack Ledger

Private checkpoint ledger. This is not a public cosmology, local-GR, CMB, or parent-field-theory claim.

## Purpose

The branch has now accumulated enough conditional structure that another narrow derivation stab would be less useful than a brutal ledger.

This checkpoint answers:

```text
what exactly is derived,
what is conditional,
what is closure,
and what must be done before B_mem=2/27 can be promoted?
```

Short answer:

```text
2/27 is now a serious theorem target,
not a random fitted number.
```

But:

```text
2/27 is still not parent-derived.
```

## The Conditional Chain

The best current stack is:

```text
B3 coherent domain
  -> relative index on End(TSigma_D)
  -> k=9

SO(3) scalar projection
  -> Pi_iso(Q)=(Tr Q/3)I
  -> trace factor 1/3

axis-to-scalar projector rank defect
  -> Delta n = Tr(P_axis)-Tr(P_iso)
  -> Delta n = 3-1 = 2

positive coarse-graining semigroup
  -> P_axis -> P_iso
  -> physical arrow 3 -> 1
```

Then:

```text
B_mem = Delta n/(3*k)
      = 2/(3*9)
      = 2/27.
```

This is the strongest version of the amplitude story so far.

It is conditional at several links.

## Stack Status

| Stack item | Current status | Blocker |
|---|---|---|
| `B_mem=2/27` empirical target | locked empirical closure | not parent-derived |
| stress/hazard equations | partial support | homogeneous in `B_mem` |
| boundary current `J_B` | formal support | no `Q_*` or endpoint law |
| `k=9` relative index | conditional pass | requires B3 coherent domain |
| B3 domain topology | conditional contract | not selected by parent action |
| trace partition `1/3` | conditional pass | Ward stress coupling missing |
| endpoint gap `Delta n=2` | conditional pass | early axis endpoint not parent-owned |
| arrow `3 -> 1` | conditional pass | positive parent time not derived |
| open parent sector | contract only | not in current parent action |
| full amplitude chain | conditional only | too many upstream conditions |
| local silence | fail/unproven | no `q_loc`/PPN proof |
| stable empirical evidence | not yet | current cosmology is mixed short-smoke |

## What Is Actually Won

The branch has improved in a real way.

Before this stack:

```text
2/27 looked like an empirical closure with suggestive algebra.
```

After this stack:

```text
2/27 has a coherent derivation-shaped scaffold:
index level,
trace projection,
projector rank defect,
semigroup arrow.
```

That matters.

It means the theory target is now precise enough to attack.

It also means we can stop kidding ourselves about which pieces are proven.

## What Is Not Won

The following claims are not allowed:

```text
B_mem=2/27 is derived from the parent action.
MTS has derived local GR.
MTS has stable cosmological evidence from current short-smoke runs.
The CMB bridge is solved.
The open/Onsager arrow is already part of the parent theory.
```

The allowed claim is:

```text
B_mem=2/27 is a locked empirical closure with a nontrivial conditional derivation stack.
```

That is the honest label.

## Promotion Gates

| Gate | Result | Meaning |
|---|---|---|
| source paths exist | pass | ledger traceable |
| `B_mem` parent-derived | fail | no amplitude promotion |
| conditional chain exists | pass | theorem target is sharp |
| reversible parent sufficient | fail | open/coarse-graining structure needed |
| local GR safe | fail | no local `q_loc` result |
| stable empirical evidence allowed | fail | no public evidence claim |
| closure contract written | pass | branch can be used safely internally |

## Closure Contract

Allowed:

```text
B_mem=2/27 is a locked empirical closure with a detailed conditional derivation stack.
```

Forbidden:

```text
B_mem=2/27 has been derived from the parent action.
```

Allowed:

```text
k=9 has a conditional relative-index origin if the coherent domain is B3-like.
```

Forbidden:

```text
k=9 is unconditionally derived.
```

Allowed:

```text
Delta n=2 has a clean projector-rank interpretation.
```

Forbidden:

```text
the physical endpoint arrow is fully parent-derived.
```

Allowed:

```text
short-smoke cosmology keeps the fixed branch worth testing.
```

Forbidden:

```text
MTS has stable cosmological evidence from current runs.
```

## Decision

Decision:

```text
two_over_27_stack_ledger_closure_contract_not_parent_derivation
```

Meaning:

```text
the 2/27 branch is now disciplined enough to keep,
but not derived enough to promote.
```

What improved:

```text
the exact derivation targets are now named and ordered.
```

What did not improve:

```text
the parent action still lacks B3 topology selection,
open positive time,
Ward trace stress coupling,
and local silence.
```

Boxing-score version:

```text
This is not a knockout.
But it is no longer shadowboxing either.
The combo is real: index, trace, rank defect, arrow.
Now the corner knows exactly which punches still need legal footing.
```

## Machine Artifacts

Script:

```text
scripts/two_over_27_derivation_stack_ledger.py
```

Run:

```text
runs/20260601-000120-two-over-27-derivation-stack-ledger
```

Output files:

```text
runs/20260601-000120-two-over-27-derivation-stack-ledger/results/source_register.csv
runs/20260601-000120-two-over-27-derivation-stack-ledger/results/derivation_stack.csv
runs/20260601-000120-two-over-27-derivation-stack-ledger/results/dependency_graph.csv
runs/20260601-000120-two-over-27-derivation-stack-ledger/results/promotion_gates.csv
runs/20260601-000120-two-over-27-derivation-stack-ledger/results/closure_contract.csv
runs/20260601-000120-two-over-27-derivation-stack-ledger/results/next_targets.csv
runs/20260601-000120-two-over-27-derivation-stack-ledger/results/decision.csv
```

## Next Step

Best theory next:

```text
construct the explicit open-boundary/influence parent sector.
```

It must include:

```text
q_r, q_a, N>=0, Gamma>=0,
Ward trace coupling,
and local silence clauses.
```

Best empirical next:

```text
move beyond 250-SN diagonal short smoke
to full covariance or independent non-SN holdout.
```

Recommended sequence:

```text
open-boundary parent sector first,
then local silence,
then stronger empirical run.
```

Reason:

```text
the amplitude route is now limited more by parent theory debt than by another small smoke fit.
```
