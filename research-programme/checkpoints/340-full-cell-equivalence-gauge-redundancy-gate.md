# 340 - Full Cell Equivalence Gauge-Redundancy Gate

Private derivation checkpoint. This is not a public cosmology, CMB, local-GR, PPN, perturbation-theory, or unified-field claim.

## Purpose

Checkpoint 339 left the hinge:

```text
full cell equivalence must be gauge redundancy,
not merely a useful symmetry or averaging rule.
```

This checkpoint tests what is required to make that statement true.

Short answer:

```text
label symmetry alone is not enough.
```

A parent action can be fully cell-symmetric and still describe either:

```text
gauge-equivalent labels,
```

or:

```text
physically distinct but symmetric species.
```

The amplitude route needs the first interpretation.

## Machine Artifact

Script:

```text
scripts/full_cell_equivalence_gauge_redundancy_gate.py
```

Run:

```text
runs/20260601-203000-full-cell-equivalence-gauge-redundancy-gate
```

Status:

```text
full_cell_equivalence_gauge_route_sharpened_but_not_parent_derived
```

Claim ceiling:

```text
gauge_redundancy_gate_no_unconditional_epsilonH_Bmem_or_parent_action_promotion
```

## Finite Witness

The verifier uses the label-symmetric action:

```text
S_parent[h] = 1/2 sum_i (h_i - 1)^2.
```

Under an active/inactive cell swap:

```text
delta S_parent = 0.
```

So the parent witness is genuinely label-symmetric.

But this does not by itself prove gauge redundancy. It could still be a global symmetry among physical cell species.

That is the key distinction.

## Readout Test

For the uniform parent solution:

```text
h_i = 1,
```

the fixed active readout is safe:

```text
epsilon_H = 1.
```

For a nonuniform active-perturbed state:

```text
h_active = 1.0061980866083466,
h_inactive = 1,
```

a fixed active readout changes under an active/inactive swap:

```text
1.0061980866083466 -> 1.0030990433041733.
```

So:

```text
fixed P_active readout is not gauge-invariant on general states.
```

If labels are gauge, the active readout must therefore be:

```text
source-at-zero,
orbit-averaged,
or relationally dressed to a reference frame.
```

## Relational Readout

A relational readout can be invariant if the reference mask transforms with the state.

The verifier confirms:

```text
relational readout before transformation = relational readout after transformation.
```

This is promising, but dangerous:

```text
if the reference mask is only observer/source dressing, the route is safe;
if the reference mask is a physical material marker, the counterterm returns.
```

That is now the precise fork.

## Action Hazard

The verifier tests three action cases.

| Action case | Delta under active/inactive swap | Result |
|---|---:|---|
| parent label-symmetric action | 0 | invariant |
| fixed `P_active` physical action | `-3.841627760456552e-05` | breaks full equivalence |
| transforming marker covariant action | 0 | formally invariant |

The third case is the hazard:

```text
a transforming material marker can keep formal gauge covariance while still making the active mark physical.
```

So the parent theory must forbid not just:

```text
fixed P_active,
```

but also:

```text
physical marker fields or boundary defects whose background is P_active.
```

## Interpretation Audit

| Interpretation | Counterterm status | `epsilon_H` status |
|---|---|---|
| gauge label redundancy | forbidden if no material marker exists | conditional theorem |
| global symmetry of physical species | allowed once active sector is selected | closure/fitted |
| gauge-fixed representative | forbidden only if gauge fixing is not new EFT data | conditional theorem |
| relational boundary reference | forbidden if no variational backreaction | conditional theorem |
| material marker/boundary defect | allowed | closure/fitted |

The desired route is:

```text
gauge label redundancy + relational/source readout.
```

The dangerous route is:

```text
global symmetry or material marker.
```

## Gauge-Redundancy Contract

The exact contract is now:

| Condition | Requirement | Status |
|---|---|---|
| `G1` | cell labels are arbitrary enumeration labels, not physical species | not yet parent-derived |
| `G2` | physical state space is the `S27` quotient | not yet parent-derived |
| `G3` | bulk action descends to the quotient | conditional from Ward route |
| `G4` | gauge fixing is not a new EFT stage | open |
| `G5` | relational readout is not a material marker | open |
| `G6` | effective action respects parent quotient | open |

This is the cleanest current form of the theorem burden.

## Gate Results

| Gate | Result |
|---|---|
| source paths exist | pass |
| parent witness action is label-symmetric | pass |
| label symmetry alone proves gauge redundancy | fail |
| uniform parent solution readout is safe | pass |
| fixed active readout is not gauge-invariant for nonuniform states | pass |
| relational reference readout is invariant | pass |
| fixed `P_active` action breaks full cell equivalence | pass |
| transforming marker keeps formal invariance | pass |
| parent theory proves no material marker | fail |
| physical state-space quotient parent-derived | fail |
| effective corrections descend to quotient | fail |
| `epsilon_H` parent-derived unconditionally | fail |
| `B_mem` parent promotion allowed | fail |
| gauge-redundancy contract available | pass |

## What This Means

The route is not dead. It is now exact:

```text
derive the 27-cell structure as indistinguishable parent labels,
then quotient by S27,
then allow P_active only as source-at-zero or relational observer readout,
then forbid material marker/boundary defect terms.
```

If that can be done, the counterterm is not legal in the physical bulk action.

But if the cells are physical sectors, or if the active rank-2 mark is a physical marker, the amplitude is not derived.

## Standing

The fair status is:

```text
full cell equivalence as gauge redundancy is a precise parent-action contract.
```

Not:

```text
full cell equivalence as gauge redundancy is derived.
```

So:

```text
epsilon_H = 1
```

remains conditionally derived, and:

```text
B_mem = 2/27
```

remains the locked empirical lead/theorem target.

## Next Derivation Target

Next:

```text
derive_indistinguishable_cell_quotient_from_parent_action_or_freeze_epsilonH_as_closure.
```

Acceptance rule:

```text
The parent action must say why the 27 cells are bookkeeping copies of one parent structure,
not physical species or material subchannels.
```

Possible route:

```text
cells are basis choices in an internal finite fibre,
the parent action depends only on symmetric trace/orbit data,
physical configuration space is the quotient by basis relabeling,
active readout is a relational observer/source insertion,
and no marker field exists in the physical action.
```

If this can be established, the amplitude route keeps moving.

If it cannot, freeze:

```text
epsilon_H
```

as explicit closure/fitted and stop promoting `B_mem=2/27` as parent-derived.
