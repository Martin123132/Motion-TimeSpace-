# Reciprocal Charge Source Neutrality

## 1. Purpose

This file follows:

```text
05-reciprocity-theorem-attempt.md
```

The question is:

```text
Can the reciprocal hair charge Q_R be killed by source matching or matter
coupling, so that T^2 S = 1 is actually derived?
```

Short answer:

```text
only conditionally.
```

The clean route is:

```text
source reciprocal neutrality.
```

But that source neutrality is not yet parent-derived.

## 2. Machine Run

Implemented:

```text
scripts/reciprocal_charge_source_neutrality.py
```

Successful run:

```text
runs/20260530-224822-reciprocal-charge-source-neutrality/status.json
```

Readout:

```text
reciprocal_charge_neutrality_conditional_not_parent_derived
```

Next target:

```text
07-nonpropagating-reciprocity-constraint.md
```

## 3. Source Matching

The exterior theorem attempt gave:

```text
J_R = 0 -> W R_AB' = Q_R.
```

At a source boundary, variation gives:

```text
delta S_boundary = [W R_AB' + Pi_R] delta R_AB|_surface.
```

Therefore:

```text
Q_R = -Pi_R.
```

Here:

```text
Pi_R = source reciprocal momentum/charge.
```

So:

```text
Pi_R = 0 -> Q_R = 0 -> R_AB = 0 -> AB = 1.
```

This would derive reciprocal routing.

## 4. Conditional Neutrality Routes

Routes that kill `Q_R`:

```text
clock-only load coupling:
source couples to A=T^2 and L, not independently to R_AB;

natural Neumann surface:
free source-boundary variation gives W R_AB'=0;

nonpropagating constraint:
R_AB is not a scalar hair mode at all.
```

Routes that do not kill `Q_R`:

```text
fixed source R_AB boundary;
anisotropic/radial routing stress source;
any hidden fitted reciprocal source.
```

## 5. PPN Danger

If reciprocal hair survives, write:

```text
R_AB = q_R L
L = 2GM/(rc^2).
```

Then weak-field routing gives approximately:

```text
gamma - 1 ~= q_R.
```

Using the internal conservative gate:

```text
|gamma - 1| <= 1e-5
```

requires:

```text
|q_R| <= 1e-5.
```

So a nonzero reciprocal charge is not a harmless detail.

Either it is exactly forbidden, or it becomes a tightly bounded local PPN
residual.

## 6. Gate Verdict

Passes:

```text
source 05 complete;
source matching formula;
Q_R=0 if source is reciprocal-neutral.
```

Fails:

```text
source neutrality parent-derived;
nonzero Q_R PPN safety;
promotion to main workbench.
```

Status:

```text
reciprocity remains conditional;
Q_R neutrality is the missing source theorem.
```

## 7. Next Target

Create:

```text
07-nonpropagating-reciprocity-constraint.md
```

Purpose:

```text
test the cleaner route where R_AB is not a propagating hair field but a
constraint mode. If successful, AB=1 can be structural rather than source-tuned.
```
