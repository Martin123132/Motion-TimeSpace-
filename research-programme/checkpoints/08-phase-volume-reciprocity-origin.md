# Phase-Volume Reciprocity Origin

## 1. Purpose

This file follows:

```text
07-nonpropagating-reciprocity-constraint.md
```

The question is:

```text
Can phase-volume balance justify lambda_R ln(T^2 S) as a parent constraint,
rather than an inserted GR lock?
```

Short answer:

```text
it motivates the constraint, but does not fully derive it.
```

## 2. Machine Run

Implemented:

```text
scripts/phase_volume_reciprocity_origin.py
```

Successful run:

```text
runs/20260530-225432-phase-volume-reciprocity-origin/status.json
```

Readout:

```text
phase_volume_reciprocity_motivated_not_parent_derived
```

Next target:

```text
09-hamiltonian-radial-cell-derivation.md
```

## 3. Key Result

The phase-volume candidate that works is:

```text
T sqrt(S) = 1.
```

This is equivalent to:

```text
T^2 S = 1.
```

Therefore:

```text
S = 1/T^2.
```

With:

```text
T^2 = 1 - L
```

we get:

```text
S = 1/(1-L)
p = 1.
```

So radial clock-routing phase-cell preservation selects the GR lane.

## 4. Important Negative Result

Generic volume preservation does not work.

Examples:

```text
T S = 1 -> p = 1/2
T S^(3/2) = 1 -> p = 1/3
generic four-volume preservation -> p = 1/3 locally
```

So we cannot say:

```text
volume preservation gives GR.
```

The only successful candidate is specifically:

```text
radial t-r clock-routing cell preservation.
```

That specificity is the remaining burden.

## 5. Current Interpretation

The route now has a coherent story:

```text
load reduces clock capacity;
local radial propagation carries the compensating routing capacity;
the t-r phase cell is preserved;
therefore T sqrt(S)=1;
therefore T^2S=1 and p=1.
```

But the bold step is:

```text
the t-r phase cell is preserved.
```

That is still a candidate principle, not a parent theorem.

## 6. Gate Verdict

Passes:

```text
source 07 complete;
radial phase cell selects p=1;
generic volume principles are rejected.
```

Fails:

```text
radial cell origin derived;
lambda_R parent origin;
promotion to main workbench.
```

Status:

```text
phase-volume balance motivates the route;
Hamiltonian or null propagation structure must derive the radial cell.
```

## 7. Next Target

Create:

```text
09-hamiltonian-radial-cell-derivation.md
```

Purpose:

```text
attempt to derive the radial t-r phase-cell constraint from the local mass-shell
or Hamiltonian structure, rather than postulating it.
```
