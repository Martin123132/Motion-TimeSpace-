# 335 — Two-Stage Identity-Then-Project Ordering Gate

Private derivation checkpoint. This is not a public cosmology, CMB, local-GR, PPN, perturbation-theory, or unified-field claim.

## Purpose

Checkpoint 334 left one viable route for deriving:

```text
epsilon_H = 1.
```

That route was:

```text
identity first,
project second.
```

This checkpoint asks whether that ordering can be made into a theorem, or whether it still leaves a post-projection active-block coupling.

Short answer:

```text
the clean ordering template works,
but a post-projection lambda counterterm reopens the amplitude.
```

So the ordering theorem is still not derived.

The next hard lock is:

```text
no later active counterterm.
```

## Machine Artifact

Script:

```text
scripts/two_stage_identity_then_project_ordering_gate.py
```

Run:

```text
runs/20260601-191500-two-stage-identity-then-project-ordering-gate
```

Status:

```text
two_stage_identity_then_project_template_conditional_post_projection_lambda_not_forbidden
```

Claim ceiling:

```text
ordering_template_only_no_epsilonH_Bmem_or_parent_action_promotion
```

## Ordering Cases

The verifier tests four cases.

| Case | `epsilon_H` | Full-equivalence projector commutator | Residual commutator | Readout |
|---|---:|---:|---:|---|
| project first under full cell equivalence | 1.0000000000 | 1.4142135624 | 0 | fails projector invariance |
| identity then project, no counterterm | 1.0000000000 | 1.4142135624 | 0 | conditional template pass |
| identity then project plus lambda counterterm | 1.0061980866 | 1.4142135624 | 0 | lambda reopens amplitude |
| active-only inserted after identity | 1.0000000000 | 1.4142135624 | 0 | imposition, not inheritance |

The important case is:

```text
identity_then_project_no_counterterm.
```

It gives:

```text
epsilon_H = 1.
```

But the equally important counterexample is:

```text
identity_then_project_plus_lambda_counterterm.
```

After projection, the residual projector-preserving algebra allows:

```text
lambda_mem P_active H_parent.
```

That shifts:

```text
epsilon_H = 1.0061980866
```

while remaining residual-invariant.

So:

```text
identity first
```

is not enough unless the parent action also forbids:

```text
lambda_mem P_active H_parent
```

after projection.

## What The Template Proves

The clean two-stage template says:

1. Full cell equivalence acts before projection.
2. The parent Hamiltonian current is fixed as:

```text
H_parent = H_scale I_cell.
```

3. The active projector is derived later as a reduction/observable:

```text
P_active.
```

4. The memory trace is:

```text
Tr(P_active H_parent)/27 = H_scale 2/27.
```

5. Therefore:

```text
epsilon_H = 1.
```

This is a valid conditional theorem template.

It is not yet a parent theorem because the ordering and no-counterterm rule are not derived.

## No-Go Result

There are now four explicit no-gos:

```text
same-stage no-go:
  full cell equivalence and nontrivial P_active cannot both be exact same-stage symmetries.

post-projection counterterm no-go:
  after P_active exists, lambda_mem P_active is invariant under the residual projector-preserving algebra.

active-only not inheritance:
  H_parent=P_active H_scale gets the trace right by inserting the desired block.

ordering is dynamical, not notational:
  the word “then” must be a parent variational or constraint statement, not prose order.
```

This last one is the key.

We cannot just write:

```text
identity first, project second.
```

We need the action to enforce that order.

## Gate Results

| Gate | Result |
|---|---|
| source paths exist | pass |
| identity-then-project template gives unit epsilon | pass |
| project-first same-stage fails | pass |
| post-projection lambda counterexample | pass |
| post-projection lambda residual invariant | pass |
| ordering parent-derived | fail |
| no later active counterterm parent-derived | fail |
| `epsilon_H` parent-derived | fail |
| `B_mem=2/27` parent promotion | fail |

## What This Wins

This checkpoint gives the strongest current route:

```text
full cell equivalence before reduction
=> identity Hamiltonian current
=> active projection
=> epsilon_H=1.
```

That is real structure.

But it also shows exactly why this is not enough:

```text
the reduced theory can still add lambda_mem P_active.
```

So the theorem burden has moved from:

```text
why identity coupling?
```

to:

```text
why no later active counterterm?
```

That is narrower and better.

## What It Does Not Decide

This checkpoint does not derive:

```text
epsilon_H = 1,
B_mem = 2/27,
H_star = H0,
dim(V_cell)=27,
rank(P_active)=2,
local GR,
PPN silence,
CMB safety,
MTS perturbations.
```

It also does not demote the locked branch.

The fair standing is:

```text
the amplitude derivation route is alive as a conditional two-stage template,
but parent ownership now requires a no-later-active-counterterm theorem.
```

## Next Derivation Target

Next:

```text
derive_or_demote_no_later_active_counterterm_theorem.
```

Acceptance rule:

```text
The parent action must forbid lambda_mem P_active H_parent after projection
without simply setting lambda_mem=1.
```

Possible routes:

```text
renormalization/technical-naturalness is not enough;
residual gauge quotient must remove the invariant, not just allow it;
first-class constraint must have a parent origin;
topological index must fix weight, not only rank.
```

If this cannot be done, the honest status becomes:

```text
epsilon_H is an explicit closure/fitted coupling,
and B_mem=2/27 remains a strong empirical theorem target rather than a derived amplitude.
```
