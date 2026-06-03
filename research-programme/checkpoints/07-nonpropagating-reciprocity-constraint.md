# Nonpropagating Reciprocity Constraint

## 1. Purpose

This file follows:

```text
06-reciprocal-charge-source-neutrality.md
```

The question is:

```text
Can reciprocal routing be made structural by preventing R_AB from becoming a
propagating hair field?
```

Short answer:

```text
yes algebraically, but the parent origin is still open.
```

This is the cleanest route found so far.

## 2. Machine Run

Implemented:

```text
scripts/nonpropagating_reciprocity_constraint.py
```

Successful run:

```text
runs/20260530-225112-nonpropagating-reciprocity-constraint/status.json
```

Readout:

```text
nonpropagating_reciprocity_constraint_clean_but_parent_origin_open
```

Next target:

```text
08-phase-volume-reciprocity-origin.md
```

## 3. Clean Constraint Route

Use:

```text
R_AB = ln(A B) = ln(T^2 S)
```

but do not give `R_AB` a kinetic exterior mode.

Instead use a constraint:

```text
S_constraint = integral lambda_R R_AB.
```

Variation with respect to `lambda_R` gives:

```text
R_AB = 0.
```

Therefore:

```text
AB = 1
T^2 S = 1
S = 1/T^2.
```

With:

```text
T^2 = 1 - L
```

this gives:

```text
S = 1/(1-L)
p = 1
gamma = 1.
```

## 4. Why This Beats The Hair Route

The old kinetic route:

```text
0.5 W (R_AB')^2 + J_R R_AB
```

creates:

```text
Q_R = W R_AB'
```

and therefore allows exterior reciprocal hair.

The nonpropagating route has:

```text
no R_AB kinetic term;
no conserved Q_R;
no reciprocal hair mode.
```

The reaction stress goes into:

```text
lambda_R
```

instead of becoming a new observable long-range field.

## 5. Still Not Promoted

This is not yet a full parent derivation.

The open question is:

```text
why does the parent motion-load action contain lambda_R ln(T^2 S)?
```

The best candidate interpretation is:

```text
local motion-capacity phase-volume balance.
```

In words:

```text
clock capacity lost to load is exactly reciprocally carried by spatial routing,
so the local clock-routing product is constrained rather than dynamically free.
```

But that sentence must become a theorem.

## 6. Gate Verdict

Passes:

```text
source 06 complete;
hair obstruction removed;
AB=1 from constraint;
p=1 recovered.
```

Fails:

```text
constraint parent origin;
promotion to main workbench.
```

Status:

```text
best route = hard constraint or phase-volume balance;
kinetic R_AB route = demoted;
motion-load route = cleaner but still in sandbox.
```

## 7. Next Target

Create:

```text
08-phase-volume-reciprocity-origin.md
```

Purpose:

```text
derive or reject the phase-volume principle that would justify
lambda_R ln(T^2 S) as a parent constraint rather than an inserted GR lock.
```
