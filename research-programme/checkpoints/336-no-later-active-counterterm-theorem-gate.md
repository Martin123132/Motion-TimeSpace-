# 336 - No-Later Active Counterterm Theorem Gate

Private derivation checkpoint. This is not a public cosmology, CMB, local-GR, PPN, perturbation-theory, or unified-field claim.

## Purpose

Checkpoint 335 narrowed the amplitude problem to one exact question:

```text
why is there no later active counterterm after P_active exists?
```

This checkpoint tries to derive that rule.

Short answer:

```text
the rule is not derived from residual symmetry, topology, trace normalization,
gauge quotient, first-class closure, or technical naturalness.
```

But the attempt is not wasted. It identifies the exact parent-action contract that would be sufficient:

```text
exact parent pullback:
only reduced terms that lift to full-cell-equivalence invariants before projection are allowed.
```

So the route has not collapsed, but the missing theorem is now extremely sharp.

## Machine Artifact

Script:

```text
scripts/no_later_active_counterterm_theorem_gate.py
```

Run:

```text
runs/20260601-193000-no-later-active-counterterm-theorem-gate
```

Status:

```text
no_later_active_counterterm_not_derived_exact_parent_pullback_contract_identified
```

Claim ceiling:

```text
counterterm_gate_no_epsilonH_Bmem_or_parent_action_promotion
```

## Core Algebra

The desired identity-current branch is:

```text
H_parent = I_cell
q_trace = Tr(P_active I_cell)/27 = 2/27
epsilon_H = 1
```

The active counterterm branch is:

```text
H_parent = I_cell + delta P_active
```

with:

```text
delta = 0.0061980866083466
epsilon_H = 1.0061980866083466
q_trace_effective = 0.07453319160061828
```

This is important because that effective trace is the same scale as the corrected DR2 fitted diagnostic branch, not random numerical noise.

The counterterm has:

```text
residual commutator = 0
full-equivalence commutator = 0.008765418142286879
```

So:

```text
full cell equivalence forbids the counterterm before projection,
but residual projector-preserving symmetry allows it after projection.
```

That is the fork.

## Trace Normalization Test

A tempting escape is:

```text
fix the full trace.
```

The verifier tests the compensated current:

```text
H_parent = I_cell + delta P_active - delta * 2/25 * (I_cell - P_active).
```

This keeps:

```text
Tr(H_parent)/27 = 1
```

but still gives:

```text
epsilon_H = 1.0061980866083466.
```

Therefore global trace normalization is not enough. It can hide the active shift in the inactive block.

## Route Audit

| Route | Result | Status |
|---|---|---|
| residual projector-preserving symmetry | `lambda_mem P_active` is invariant | fail |
| full cell equivalence same-stage | forbids `P_active`, but also forbids the physical projector | fail as full derivation |
| topological rank index | fixes support count, not weight | fail |
| total trace normalization | active and inactive blocks compensate | fail |
| gauge quotient | changes projected amplitude, so not pure gauge | fail |
| first-class closure | rescaling-blind unless parent normalization is owned | fail |
| technical naturalness | stability is not exact selection | fail |
| exact parent pullback | sufficient if imposed | conditional contract |

## No-Go Lemma

Once the active projector is physically available, the residual invariant algebra contains:

```text
span(P_active, I_cell - P_active).
```

Therefore a reduced action respecting only the residual symmetry can contain:

```text
lambda_mem P_active.
```

That means:

```text
no later active counterterm
```

cannot be derived from residual symmetry alone.

It must come from a stronger parent statement.

## Conditional Positive Theorem

There is a clean conditional theorem:

```text
If every reduced operator must be the pullback/projection of a full-cell-equivalence invariant,
then lambda_mem P_active is forbidden.
```

Reason:

```text
I_cell lifts to the full stage.
P_active does not lift to the full-cell-equivalence stage because it distinguishes active from inactive cells.
```

Under that exact-pullback contract:

```text
H_parent = I_cell
Tr(P_active H_parent)/27 = 2/27
epsilon_H = 1.
```

This is the best current derivation route.

But it is still conditional because the parent action has not yet proved:

```text
the reduced theory is an exact quotient/readout, not a Wilsonian EFT with all residual invariants.
```

## Gate Results

| Gate | Result |
|---|---|
| source paths exist | pass |
| residual symmetry forbids lambda | fail |
| full equivalence forbids lambda same-stage | pass |
| topological rank fixes weight | fail |
| total trace normalization fixes active weight | fail |
| gauge quotient removes lambda | fail |
| exact parent pullback sufficient if imposed | pass |
| exact parent pullback parent-derived | fail |
| no later active counterterm parent-derived | fail |
| `epsilon_H` parent-derived | fail |
| closure contract available | pass |

## What This Means

This is not a death blow. It is a discipline lock.

The amplitude branch now has two honest options:

```text
Option A:
derive the exact parent-pullback selection rule.

Option B:
keep epsilon_H as an explicit closure/fitted coupling while B_mem=2/27 remains a theorem target.
```

The theory should not claim:

```text
B_mem = 2/27 is parent-derived.
```

The fair claim is:

```text
B_mem = 2/27 is the locked empirical lead branch,
and a conditional exact-parent-pullback route can explain why epsilon_H=1,
but the parent selection rule is not yet derived.
```

## Next Derivation Target

Next:

```text
derive_parent_exact_pullback_selection_rule_or_keep_epsilonH_as_closure.
```

Acceptance rule:

```text
The parent action must prove that projection is an exact readout/quotient
and not a new reduced EFT stage where all residual invariants may be added.
```

If that is derived, the amplitude route becomes much stronger:

```text
full cell equivalence
=> identity parent Hamiltonian current
=> exact pullback/readout projection
=> no later lambda_mem P_active
=> epsilon_H = 1
=> B_mem = 2/27, provided H_star = H0 and rank/dim stay locked.
```

If not, the amplitude remains an empirical closure with a very good target value, not a theorem.
