# 339 - P_active Boundary-Observable Ward Gate

Private derivation checkpoint. This is not a public cosmology, CMB, local-GR, PPN, perturbation-theory, or unified-field claim.

## Purpose

Checkpoint 338 left the exact action-level burden:

```text
P_active must be a readout/source-at-zero observable,
not a physical action spurion.
```

This checkpoint tests the cleanest route:

```text
full cell equivalence as a Ward/gauge redundancy.
```

Short answer:

```text
the Ward route conditionally supports P_active as a readout,
but it is not yet an unconditional parent derivation.
```

If full cell equivalence is a gauge redundancy, fixed non-invariant `P_active` terms are forbidden in the physical bulk action. `P_active` can then appear only as a post-variation source/readout.

But if the theory allows a transforming material marker or a physical boundary defect whose background is `P_active`, the counterterm returns.

## Machine Artifact

Script:

```text
scripts/Pactive_boundary_observable_Ward_gate.py
```

Run:

```text
runs/20260601-201500-Pactive-boundary-observable-Ward-gate
```

Status:

```text
Pactive_probe_route_conditionally_supported_gauge_redundancy_and_no_material_defect_open
```

Claim ceiling:

```text
Ward_readout_gate_no_unconditional_epsilonH_Bmem_or_parent_action_promotion
```

## Ward Test

Use a rank-2 active mask:

```text
P_active = diag(1,1,0,...,0)
```

and a full-cell transformation that swaps one active and one inactive cell.

For a physical fixed active bulk term:

```text
J P_active
```

with:

```text
J = 0.0061980866083466,
```

the Ward norm is:

```text
0.00876541814228682.
```

So the fixed active term violates full cell gauge redundancy.

For a source-at-zero readout:

```text
J = 0,
```

the Ward norm is:

```text
0.
```

That is the safe branch: the source can define the observable but does not enter the physical equations.

## Orbit-Average Completion

The full-gauge orbit average of a rank-2 active mask is:

```text
P_average = (2/27) I_cell.
```

This is Ward-invariant:

```text
Ward norm = 0.
```

But it erases the active/inactive contrast.

After trace normalization:

```text
epsilon_H = 0.9999999999999998,
q_trace = 0.07407407407407406.
```

So the only bulk gauge-invariant completion of the active mark does not produce an active amplitude shift.

This is a useful result:

```text
bulk gauge invariance either forbids fixed P_active
or averages it into a uniform non-active term.
```

## Spurion Hazard

There is still an escape route for the counterterm.

If a marker field:

```text
m_i
```

transforms under the gauge action and is then physically fixed to:

```text
m_i = P_active,
```

then the action can be formally Ward-invariant while still containing a real active material mark.

That reopens:

```text
lambda_mem P_active.
```

So the parent theory must not merely say:

```text
the expression is gauge-covariant.
```

It must say:

```text
there is no material active marker/defect in the physical action.
```

That is the next hard requirement.

## Boundary-Readout Contract

The Ward/readout branch now has six conditions:

| Condition | Requirement | Status |
|---|---|---|
| `W1` | full cell equivalence is gauge redundancy | not yet parent-derived |
| `W2` | `P_active` enters only as external source at `J=0` | conditional contract |
| `W3` | no material marker field has background `P_active` | open |
| `W4` | boundary/readout insertion has no variational backreaction | open |
| `W5` | effective corrections satisfy parent Ward identity | open |
| `W6` | observable is relationally dressed to boundary/observer frame | open |

This is the most exact version of the amplitude route so far.

## Gate Results

| Gate | Result |
|---|---|
| source paths exist | pass |
| fixed `P_active` bulk term violates parent Ward identity | pass |
| source-at-zero restores physical Ward identity | pass |
| orbit average is parent-Ward invariant | pass |
| orbit average erases active amplitude shift | pass |
| fixed `P_active` spurion shifts active amplitude | pass |
| transforming material spurion reopens counterterm | pass |
| parent theory proves full cell equivalence is gauge | fail |
| parent theory proves no material marker/boundary defect | fail |
| effective corrections obey parent Ward identity | fail |
| `epsilon_H` parent-derived unconditionally | fail |
| `B_mem` parent promotion allowed | fail |
| Ward-readout contract available | pass |

## What This Means

This is the best route if we want to keep deriving rather than freezing:

```text
full cell equivalence is gauge,
physical bulk action is parent-Ward invariant,
P_active is only a readout/source-at-zero,
there is no material active marker,
effective corrections preserve the parent Ward identity.
```

Then:

```text
lambda_mem P_active
```

is not a legal physical action term.

But if any of these fail, especially the "no material marker" condition, the active counterterm is legal and:

```text
epsilon_H
```

must remain a closure/fitted coupling.

## Standing

The fair status is:

```text
P_active as readout is conditionally supported by a Ward/gauge route.
```

Not:

```text
P_active as readout is parent-derived.
```

And:

```text
B_mem = 2/27
```

remains the locked empirical lead/theorem target, not a fully derived parent amplitude.

## Next Derivation Target

Next:

```text
derive_full_cell_equivalence_as_gauge_redundancy_or_freeze_epsilonH_as_closure.
```

Acceptance rule:

```text
The parent action must identify full cell equivalence as redundancy of description,
not merely an approximate/global symmetry or convenient averaging rule.
```

If this can be derived, the route becomes:

```text
gauge cell equivalence
=> Ward-invariant physical action
=> fixed P_active forbidden in bulk dynamics
=> source-at-zero/boundary readout only
=> no lambda_mem P_active counterterm
=> epsilon_H = 1 conditionally
=> B_mem = 2/27 if H_star = H0 and rank/dim remain locked.
```

If not, the honest move is:

```text
freeze epsilon_H as closure/fitted,
keep 2/27 as empirical lead,
and stop promoting the amplitude as parent-derived.
```
