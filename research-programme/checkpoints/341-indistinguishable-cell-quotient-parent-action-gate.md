# 341 - Indistinguishable-Cell Quotient Parent-Action Gate

Private derivation checkpoint. This is not a public cosmology, CMB, local-GR, PPN, perturbation-theory, or unified-field claim.

## Purpose

Checkpoint 340 left the parent-action burden:

```text
the 27 cells must be bookkeeping copies of one parent structure,
not physical species or material subchannels.
```

This checkpoint tests the most direct route:

```text
the parent configuration space is the quotient R^27 / S27.
```

Short answer:

```text
the quotient route is mathematically clean,
but not yet parent-derived.
```

If the parent variable is an unlabelled orbit, multiset, spectrum, or basis-free finite-fibre object, the amplitude route survives.

If the parent variable is a labelled 27-component species vector, or if the configuration space is extended by a physical active marker, the counterterm returns.

## Machine Artifact

Script:

```text
scripts/indistinguishable_cell_quotient_parent_action_gate.py
```

Run:

```text
runs/20260601-204500-indistinguishable-cell-quotient-parent-action-gate
```

Status:

```text
indistinguishable_cell_quotient_template_constructed_parent_variable_origin_open
```

Claim ceiling:

```text
quotient_parent_action_gate_no_unconditional_epsilonH_Bmem_or_parent_action_promotion
```

## Orbit Function Test

The verifier tests a nonuniform state and its active/inactive relabeling.

Good quotient observables are constant on the orbit:

```text
trace average,
sorted spectrum,
power-sum/trace invariants.
```

These all pass.

Bad bulk observables are not constant on the orbit:

```text
fixed active average,
fixed active q_trace.
```

For the fixed active average:

```text
1.00464856495626 -> 1.0007747608260433
```

under an active/inactive swap.

So:

```text
fixed P_active is not a function on R^27 / S27.
```

That is exactly what we need if `P_active` is to be excluded from the physical bulk action.

## Relational Readout

The relational readout passes if the reference mask transforms with the state:

```text
state + reference mask
```

as an extended pair.

This gives an invariant readout:

```text
1.00464856495626.
```

But the old danger remains:

```text
if the reference is observer/source dressing, it is safe;
if the reference is a material marker, it reopens the counterterm.
```

So relational readout is a route, not a finished proof.

## Same Formula Trap

The verifier compares two cases:

```text
class action on quotient,
symmetric labelled-species action.
```

They can use the same formula:

```text
S_parent[h] = 1/2 sum_i (h_i - 1)^2.
```

Both are invariant under relabeling.

But they do not mean the same physics.

In the quotient case:

```text
h and permutation(h) are the same physical state.
```

In the labelled-species case:

```text
h and permutation(h) are different physical states related by a global symmetry.
```

Therefore:

```text
the formula alone does not derive gauge redundancy.
```

The parent variable/state-space definition must do the work.

## Marker Extension Hazard

A fixed active spurion breaks the state quotient:

```text
-0.012428586950922053 vs -0.012380566603916345.
```

But a covariant material marker:

```text
(state, marker) / S27
```

can descend to an extended quotient while still carrying active physical data.

That means:

```text
quotienting alone is not enough.
```

The parent theory must specifically forbid:

```text
marker/background variables whose value is P_active.
```

## Route Audit

| Route | Configuration space | Counterterm status | `epsilon_H` status |
|---|---|---|---|
| labelled species | `R^27` | allowed after active selection | closure/fitted |
| quotient orbit | `R^27 / S27` | forbidden in bulk action | conditional theorem |
| basis finite fibre | operator modulo basis relabeling | forbidden unless marker added | conditional theorem |
| material marker | `(state, marker) / S27` | allowed | closure/fitted |

The desired route is:

```text
quotient orbit or basis finite fibre.
```

The dangerous route is:

```text
labelled species or material marker.
```

## Quotient Parent-Action Contract

The exact contract is now:

| Condition | Requirement | Status |
|---|---|---|
| `Q1` | parent variables are unlabelled orbits/multisets/basis-free fibre objects | not yet parent-derived |
| `Q2` | action is a trace/spectrum/orbit class function | conditional template verified |
| `Q3` | observables are class functions or zero-source insertions | conditional template verified |
| `Q4` | no marker/background extension exists | open |
| `Q5` | relational readout has no backreaction | open |
| `Q6` | effective action remains a class function | open |

This is the best version of the quotient route so far.

## Gate Results

| Gate | Result |
|---|---|
| source paths exist | pass |
| trace and spectrum are orbit functions | pass |
| fixed active readout is not a quotient function | pass |
| relational readout is an extended quotient function | pass |
| class action descends to quotient | pass |
| same symmetric formula selects quotient over species | fail |
| fixed active spurion breaks state quotient | pass |
| covariant material marker descends to extended quotient | pass |
| parent variables prove unlabelled orbit space | fail |
| parent theory proves no marker extension | fail |
| effective action proven class function | fail |
| `epsilon_H` parent-derived unconditionally | fail |
| `B_mem` parent promotion allowed | fail |
| quotient parent-action contract available | pass |

## What This Means

This checkpoint does not kill the derivation route.

It says the next parent-action statement must be:

```text
the 27 cells are basis labels in an internal finite fibre,
not 27 physical components.
```

Then:

```text
physical variables are trace/spectrum/orbit data,
fixed P_active is not a bulk observable,
P_active can only enter as source-at-zero or relational observer dressing,
and lambda_mem P_active is not a legal bulk counterterm.
```

But if the theory cannot justify the finite-fibre/basis-label interpretation, then the amplitude is closure.

## Standing

The fair status is:

```text
indistinguishable-cell quotient is a precise theorem template.
```

Not:

```text
indistinguishable-cell quotient is derived.
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
derive_parent_finite_fibre_basis_relabeling_or_freeze_epsilonH_as_closure.
```

Acceptance rule:

```text
The parent action must define the 27-cell structure as a basis choice in a finite internal fibre,
with physical action and corrections depending only on basis-invariant trace/orbit data.
```

If this can be stated, the amplitude route keeps going.

If it cannot, freeze:

```text
epsilon_H
```

as explicit closure/fitted and stop promoting `B_mem=2/27` as parent-derived.
