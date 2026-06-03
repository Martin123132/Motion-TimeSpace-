# Reciprocity Theorem Attempt

## 1. Purpose

This file follows:

```text
04-vacuum-reciprocity-action-contract.md
```

The question is:

```text
Does the reciprocal-strain action actually force T^2 S = 1 in local vacuum?
```

Short answer:

```text
only conditionally.
```

The theorem almost works, but it exposes a hidden obstruction:

```text
reciprocal charge Q_R.
```

## 2. Machine Run

Implemented:

```text
scripts/reciprocity_theorem_attempt.py
```

Successful run:

```text
runs/20260530-224448-reciprocity-theorem-attempt/status.json
```

Readout:

```text
reciprocity_theorem_conditional_no_hair_obstruction
```

Next target:

```text
06-reciprocal-charge-source-neutrality.md
```

## 3. Toy Parent Variation

Use the reciprocal-strain mode:

```text
R_AB = ln(A B) = ln(T^2 S).
```

Toy parent action:

```text
S_R = integral dr [0.5 W(r) (R_AB')^2 + J_R R_AB].
```

Variation gives:

```text
d/dr [W(r) R_AB'] = J_R.
```

In local vacuum:

```text
J_R = 0
```

so:

```text
W R_AB' = Q_R.
```

`Q_R` is a conserved reciprocal charge.

## 4. Conditional Success

If:

```text
Q_R = 0
```

then:

```text
R_AB' = 0.
```

With asymptotic flatness:

```text
R_AB(infinity) = 0
```

therefore:

```text
R_AB = 0
AB = 1
T^2 S = 1
p = 1.
```

So the theorem succeeds only if reciprocal charge neutrality is derived.

## 5. Obstruction

Asymptotic flatness alone does not kill `Q_R`.

For the natural spherical scaling:

```text
W ~ r^2
```

the exterior solution is:

```text
R_AB ~ Q_R/r.
```

This is:

```text
asymptotically flat;
finite-energy in the exterior;
nonzero unless Q_R = 0.
```

Therefore:

```text
finite exterior energy + infinity boundary are not enough.
```

The missing theorem is source matching:

```text
Q_R = integral J_R dr = 0
```

or an equivalent natural boundary condition:

```text
W R_AB' = 0
```

at the material/load surface.

## 6. Gate Verdict

Passes:

```text
source 04 complete;
toy action variation;
vacuum conserved charge;
conditional AB=1 if Q_R=0.
```

Fails:

```text
asymptotic-flatness no-hair;
reciprocal charge neutrality derived;
promotion to main workbench.
```

Status:

```text
reciprocity theorem = conditional;
hidden obstruction = Q_R reciprocal hair;
motion-load route = promising but not promoted.
```

## 7. Next Target

Create:

```text
06-reciprocal-charge-source-neutrality.md
```

Purpose:

```text
derive or reject Q_R=0 from source matching, matter coupling, boundary
variation, or an explicit no-reciprocal-charge principle.
```
