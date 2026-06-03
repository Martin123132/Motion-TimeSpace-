# Cell-Current Origin Attempt

## 1. Purpose

This file follows:

```text
10-observer-map-symplectic-contract.md
```

The question is:

```text
Can a conserved radial observer-cell current derive R_AB=0, closing the
lambda-origin gate without inserting a closure axiom?
```

Short answer:

```text
not by ordinary current conservation. A conserved current gives a reciprocal
charge Q_R; it does not prove the charge is zero.
```

## 2. Machine Run

Implemented:

```text
scripts/cell_current_origin_attempt.py
```

Successful run:

```text
runs/20260530-230553-cell-current-origin-attempt/status.json
```

Readout:

```text
cell_current_origin_no_charge_obstruction
```

Next target:

```text
12-gauge-noether-origin-audit.md
```

## 3. Current Equation

The natural conserved reciprocal-cell current has the form:

```text
partial_r(W partial_r R_AB) = 0.
```

Therefore:

```text
W partial_r R_AB = Q_R.
```

For the natural spherical exterior weight:

```text
W = r^2
```

the exterior solution is:

```text
R_AB = R_infinity - Q_R/r.
```

With asymptotic reciprocity:

```text
R_infinity = 0
```

we still get:

```text
R_AB = -Q_R/r.
```

So asymptotic flatness does not kill the reciprocal charge.

## 4. Why This Fails As A Derivation

The target is:

```text
R_AB = 0.
```

But current conservation gives only:

```text
Q_R = constant.
```

It does not give:

```text
Q_R = 0.
```

That missing zero-charge theorem is exactly the old obstruction in a cleaner
language.

If `Q_R` is nonzero, the local route carries exterior reciprocal hair. In weak
field language this behaves like a `gamma-1` residual, so it is dangerous for
solar-system tests.

## 5. Routes Audited

Rejected or demoted:

```text
gradient_cell_current:
conserves Q_R but permits hair.

cell_number_continuity:
conserves integrated cell number but does not fix R_AB.

Noether current for cell scaling:
gives a Ward identity, not R_AB=0.

algebraic cell current:
forces R_AB=0 only by renaming the constraint.
```

Best possible route still open:

```text
topological_zero_charge:
Q_R = integral rho_R = 0 by source representation.
```

But that theorem is not currently derived.

## 6. Gate Verdict

Passes:

```text
source 10 complete;
cell-current equation written;
hair solution identified;
nonpropagating constraint remains available as a closure.
```

Fails:

```text
asymptotic boundary kills hair;
conservation alone derives R_AB=0;
no-charge theorem;
promotion to main workbench.
```

Status:

```text
ordinary cell-current conservation does not close the lambda-origin gate.
```

## 7. Current Best Position

The local GR branch is now boxed in properly:

```text
If R_AB=0 is imposed as a nonpropagating constraint, p=1 follows cleanly.

If R_AB is treated as a conserved-current field, it generically carries Q_R hair.

Therefore the branch either needs a true gauge/Noether origin that forbids
Q_R, or it must remain an explicit closure.
```

This is not a dead end, but it is not a derivation yet.

## 8. Next Target

Create:

```text
12-gauge-noether-origin-audit.md
```

Purpose:

```text
test whether a genuine observer-splitting gauge symmetry or Noether identity
can forbid Q_R without importing GR. If not, demote the local route to a
closure-only GR limit and move to empirical/field-action tests elsewhere.
```
