# 279 - Representative Selection / Boundary Polarization No-Go

Private derivation checkpoint. This is not a public local-GR, CMB, BAO, or unified-field claim.

## Purpose

Checkpoint 278 restricted admissible boundary variations using a relative current:

```text
delta_eta Q_rel[D] = 0.
```

That helped, but did not select the physical representative:

```text
which local class is trivial?
which FLRW class is nonzero?
which boundary primitive b_2 is physical?
```

This checkpoint tests the obvious next move:

```text
boundary polarization Pi(C_coh)
```

and asks whether it is derived or just a selector function.

## Machine Artifact

Script:

```text
scripts/representative_selection_boundary_polarization_no_go.py
```

Run:

```text
runs/20260601-000097-representative-selection-boundary-polarization-no-go
```

Status:

```text
boundary_polarization_endpoint_constraints_underselect_representative_selection_not_derived
```

Claim ceiling:

```text
polarization_no_go_for_parent_promotion_local_branch_remains_effective_closure
```

## Polarization Route

The attractive schematic action is:

```text
S =
integral B wedge F[A]
+ integral_boundaryD Pi(C_coh) wedge b_2.
```

The hoped-for branch logic is:

```text
C_coh = 0 -> Pi(0)=0 -> local trivial representative
C_coh = 1 -> Pi(1)!=0 -> FLRW expansion representative
```

This is elegant.

But elegance is not derivation.

## Endpoint Constraints

The minimum constraints are:

```text
Pi(0) = 0
Pi(1) = 1
```

For local and FLRW first-order safety, one might also demand:

```text
Pi'(0) = 0
Pi'(1) = 0
```

and monotonicity:

```text
0 <= Pi(C) <= 1.
```

These constraints do not select a unique function.

Examples:

```text
Pi(C) = C
Pi(C) = 3C^2 - 2C^3
Pi(C) = 10C^3 - 15C^4 + 6C^5
```

all satisfy different reasonable subsets of the requirements.

There are infinitely many more.

## No-Go Result

Endpoint behaviour underselects `Pi`.

Regularity underselects `Pi`.

Monotonicity underselects `Pi`.

Threshold/sigmoid versions add:

```text
C_*
w
```

which are new selector scales unless derived.

And any action term:

```text
Pi(C_coh) b_2
```

reopens:

```text
delta Pi = Pi'(C_coh) delta C_coh
```

so the boundary/Bianchi exchange problem comes back unless a parent current equation absorbs it.

Therefore:

```text
Pi(C_coh) can encode the desired representative,
but it does not derive it.
```

## What Remains Live

The only non-closure route is:

```text
topological quantization / discrete class projector
```

meaning:

```text
Pi is not a chosen smooth function;
Pi is forced by the relative class sector itself.
```

But that requires the missing theorem:

```text
the parent action selects the physical relative class / representative.
```

So this is not dead, but the smooth polarization route cannot be promoted.

## Decision

This closes the current local-branch derivation attempt cleanly:

```text
fixed-D Q_coh projection: derived
free-boundary Euler equation: derived but degenerate
relative-current admissibility: sharpened
boundary polarization representative selection: not derived
```

So the local branch status is:

```text
disciplined effective closure / theorem target,
not derived local GR.
```

That is not a failure of the whole programme. It is a useful piece of discipline:

```text
we now know exactly where the derivation stops.
```

## Output Files

```text
runs/20260601-000097-representative-selection-boundary-polarization-no-go/results/source_register.csv
runs/20260601-000097-representative-selection-boundary-polarization-no-go/results/endpoint_constraints.csv
runs/20260601-000097-representative-selection-boundary-polarization-no-go/results/polarization_candidates.csv
runs/20260601-000097-representative-selection-boundary-polarization-no-go/results/no_go_tests.csv
runs/20260601-000097-representative-selection-boundary-polarization-no-go/results/branch_impact.csv
runs/20260601-000097-representative-selection-boundary-polarization-no-go/results/route_policy.csv
runs/20260601-000097-representative-selection-boundary-polarization-no-go/results/decision.csv
```

## Next Step

Next target:

```text
280 - Local Branch Status Ledger and Empirical Closure Pivot
```

Purpose:

```text
separate derived, conditional, closure, and failed pieces,
then define the empirical tests that can be run honestly without pretending local GR has been derived.
```

Recommended stance:

```text
continue derivation only through topological quantization;
test smooth polarization / projected-matter metric only as labelled closure.
```

