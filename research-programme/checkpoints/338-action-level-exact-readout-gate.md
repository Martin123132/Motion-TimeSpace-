# 338 - Action-Level Exact Readout Gate

Private derivation checkpoint. This is not a public cosmology, CMB, local-GR, PPN, perturbation-theory, or unified-field claim.

## Purpose

Checkpoint 337 proved the algebraic conditional:

```text
full parent pullback + trace normalization + exact readout
=> epsilon_H = 1
=> q_trace = 2/27.
```

This checkpoint asks the next harder question:

```text
can the action itself justify exact readout?
```

Short answer:

```text
only conditionally.
```

The action-level route works if:

```text
P_active is a post-variation observable/source-at-zero readout,
not a physical spurion or boundary tensor inside the action.
```

If `P_active` is allowed into the physical action, the counterterm comes back.

## Machine Artifact

Script:

```text
scripts/action_level_exact_readout_gate.py
```

Run:

```text
runs/20260601-200000-action-level-exact-readout-gate
```

Status:

```text
action_level_exact_readout_contract_constructed_Pactive_probe_premise_open
```

Claim ceiling:

```text
action_readout_contract_no_unconditional_epsilonH_Bmem_or_parent_action_promotion
```

## Finite Action Witness

The verifier uses a finite-cell variational witness:

```text
S_parent[h] = 1/2 sum_i (h_i - 1)^2
```

with full cell symmetry before projection.

If the action is varied first:

```text
h_i = 1 for all cells.
```

Then applying the active readout gives:

```text
epsilon_H = average_active(h_i) = 1,
q_trace = 2/27.
```

So the exact-readout branch works.

## Source Versus Spurion

The critical distinction is:

```text
source-at-zero != physical spurion.
```

If `P_active` is only a generating source:

```text
S[J] = S_parent + J O_active,
```

and physical equations are evaluated at:

```text
J = 0,
```

then the source lets us compute the observable without changing the background:

```text
epsilon_H = 1.
```

But if the same term is a physical coupling in the action:

```text
S_physical = S_parent + J O_active,
```

with:

```text
J = 0.0061980866083466,
```

then the active sector shifts:

```text
epsilon_H = 1.0061980866083466.
```

That is the counterterm returning through the action door.

## Trace Compensation Still Fails

The verifier also tests the usual escape:

```text
keep the total trace fixed.
```

A compensated physical spurion can keep:

```text
Tr(H_parent)/27 = 1
```

while still giving:

```text
epsilon_H = 1.0061980866083466.
```

So global normalization still does not remove the active-block freedom.

## Action Contract

The exact-readout branch now has a concrete action-level contract:

| Condition | Requirement | Status |
|---|---|---|
| `A1` | vary `S_parent` before projection | contract constructed |
| `A2` | `P_active` is observable/probe, not action spurion | not yet parent-derived |
| `A3` | no independent `S_reduced[P_active]` | not yet parent-derived |
| `A4` | effective corrections are parent pullbacks | open |
| `A5` | active mark is boundary/readout label, not material defect | open |
| `A6` | readout is subtrace of the same lapse/Hamiltonian current | open |

This is good progress because it pins down exactly what must be proved.

## Fork Audit

There are now four branches.

| Fork | Counterterm status | `epsilon_H` status |
|---|---|---|
| strict parent observable readout | forbidden by construction | conditional theorem |
| boundary/defect action | allowed | closure or fitted |
| Wilsonian effective reduction | allowed | closure or fitted |
| constrained effective pullback | forbidden if Ward/constraint identity exists | possible theorem |

The branch we want is the first or fourth.

The dangerous branches are the second and third.

## Gate Results

| Gate | Result |
|---|---|
| source paths exist | pass |
| post-variation observable readout gives `epsilon_H=1` | pass |
| post-variation observable readout gives `q_trace=2/27` | pass |
| source-at-zero does not shift background | pass |
| physical `P_active` spurion shifts `epsilon_H` | pass |
| trace-compensated spurion still shifts `epsilon_H` | pass |
| action-level exact readout sufficient | pass |
| parent action currently proves `P_active` probe not spurion | fail |
| effective corrections proven parent pullback | fail |
| `epsilon_H` parent-derived unconditionally | fail |
| `B_mem` parent promotion allowed | fail |
| closure contract available | pass |

## What This Means

The action-level route is alive, but only with a strict interpretation:

```text
P_active is not a field,
not a coupling,
not a symmetry-breaking material tensor,
and not part of an independent reduced action.
```

It is:

```text
a post-variation readout/source-at-zero observable.
```

Under that interpretation:

```text
lambda_mem P_active
```

is not allowed in the physical action because `P_active` is not available as an action-building object.

But if `P_active` is a real boundary/defect object inside the action, the counterterm is legal and the amplitude is not derived.

## Standing

The fair status is now:

```text
epsilon_H = 1 is conditionally derived under strict parent-observable readout.
```

Not:

```text
epsilon_H = 1 is unconditionally parent-derived.
```

And:

```text
B_mem = 2/27
```

remains the locked empirical lead/theorem target, not a fully derived parent amplitude.

## Next Derivation Target

Next:

```text
derive_Pactive_as_boundary_observable_not_action_spurion_or_freeze_epsilonH_as_closure.
```

Acceptance rule:

```text
The parent action must explain why the active rank-2 mark is a readout/boundary observable
rather than a physical spurion that permits active-local action terms.
```

The most promising route is a Ward/constraint statement:

```text
P_active may couple only to a source used to differentiate observables at J=0,
while all physical action terms must remain parent-pullback invariants.
```

If we can prove that, the amplitude branch becomes a serious conditional theorem.

If not, we should freeze:

```text
epsilon_H
```

as an explicit closure/fitted coupling and stop trying to promote `B_mem=2/27` as parent-derived.
