# Relative Boundary Current Construction Attempt

## 1. Purpose

This file follows:

```text
70-Ccoh-variation-and-boundary-current-audit.md
```

Checkpoint 70 found:

```text
C_coh can be constant-safe in ideal local/FLRW bulk branches, but varying
boundaries and perturbations require an explicit exchange current.
```

This checkpoint attempts to construct that current.

Short answer:

```text
a formal relative current can be written, but it is not parent-derived yet.
```

So this is a mathematical narrowing, not a promotion.

## 2. Machine Run

Implemented:

```text
scripts/relative_boundary_current_construction_attempt.py
```

Successful run:

```text
runs/20260531-113439-relative-boundary-current-construction-attempt/status.json
```

Readout:

```text
formal_current_constructed_not_parent_derived
```

Generated:

```text
runs/20260531-113439-relative-boundary-current-construction-attempt/results/source_checkpoint_register.csv
runs/20260531-113439-relative-boundary-current-construction-attempt/results/construction_chain.csv
runs/20260531-113439-relative-boundary-current-construction-attempt/results/closure_tests.csv
runs/20260531-113439-relative-boundary-current-construction-attempt/results/stress_safety_ledger.csv
runs/20260531-113439-relative-boundary-current-construction-attempt/results/gate_results.csv
runs/20260531-113439-relative-boundary-current-construction-attempt/results/decision.csv
```

## 3. Formal Construction

Use a relative pair:

```text
J_rel = (j_3, b_2) in C^3(D, boundary D).
```

The relative differential is:

```text
d_rel(j_3,b_2) =
(
  d j_3,
  i_star j_3 - d_boundary b_2
).
```

Closure requires:

```text
d j_3 = 0
```

in the bulk and:

```text
i_star j_3 = d_boundary b_2
```

on the boundary.

Interpretation:

```text
j_3 = coherent scalar memory 3-current
b_2 = boundary primitive/exchange current
```

This gives a clean mathematical object for the missing exchange current.

## 4. Local and FLRW Classes

Stationary bound local domain:

```text
j_3 = 0 or exact
b_2 = 0 or exact
[J_rel] = 0
```

So the relative class is trivial.

Coherent FLRW domain:

```text
integral_D j_3 nonzero
d ln V_D/dtau = 3H
I_M = det(Q_coh)
```

So the relative class can be nontrivial.

This matches the earlier contract:

```text
stationary bound domains -> trivial relative memory class
coherent FLRW expansion -> nontrivial expansion class
```

## 5. Stress Safety

The safe route is:

```text
metric_independent_topological_pair
```

Meaning:

```text
J_rel is topological/constrained bookkeeping, not a physical wall with surface
energy.
```

The dangerous route is:

```text
boundary_surface_stress
```

because it can become:

```text
PPN-sized local wall stress.
```

Rejected:

```text
arbitrary_boundary_counterterm
```

because that is just the old rescue knob wearing a cloak and humming Latin.

## 6. What This Fixes

It fixes the language of the missing object.

Instead of saying:

```text
some boundary current cancels the C_coh variation
```

we can now say:

```text
find a closed relative pair (j_3,b_2) such that local stationary classes are
trivial and FLRW expansion classes are nontrivial.
```

That is sharper and testable.

## 7. What Still Fails

Gate result:

```text
relative_pair_written              pass
local_trivial_class_possible       pass conditional
FLRW_nontrivial_class_possible     pass contract
PPN_surface_stress_avoided         pass conditional
parent_action_derives_Jrel         fail
amplitude_normalization_derived    fail
perturbation_current_resolved      open
local_GR_promoted                  fail
support_claim_allowed              fail
```

So the formal current is not enough.

The big missing sentence is:

```text
the parent action forces d_rel J_rel = 0 and selects the physical
representative.
```

Without that, the relative pair can still become a renamed boundary assumption.

## 8. Decision

Decision:

```text
relative_boundary_current_status =
formal_current_constructed_not_parent_derived
```

Meaning:

```text
closed relative pair can encode trivial local and nontrivial FLRW classes;
PPN danger is avoided only if it is topological/exact bookkeeping;
no parent action forces it yet.
```

Decision:

```text
local_GR_route_status =
boundary_current_formal_but_unpromoted
```

This is still movement. The problem has been squeezed into a very precise
corner:

```text
derive the action/topological owner of J_rel.
```

## 9. Next Target

Create:

```text
72-relative-current-action-owner-attempt.md
```

Purpose:

```text
attempt an action/topological term whose variation gives d_rel J_rel = 0
rather than merely imposing the desired current.
```

Pass condition:

```text
the action derives the closed relative pair, keeps local classes trivial,
preserves FLRW expansion class, and avoids physical PPN wall stress.
```

Fail condition:

```text
the action just restates d_rel J_rel = 0 as a multiplier constraint with no
physical selection rule.
```
