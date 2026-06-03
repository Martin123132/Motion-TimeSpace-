# Reciprocal Routing Parent Origin

## 1. Purpose

This file follows:

```text
02-motion-load-local-GR-reduction.md
```

The question is:

```text
Can T^2 S = 1 be derived from a parent principle rather than inserted as the
hidden p=1 dial?
```

Short answer:

```text
not yet.
```

The reciprocity condition is algebraically powerful and physically plausible,
but the parent origin is still incomplete.

## 2. Machine Run

Implemented:

```text
scripts/reciprocal_routing_parent_origin.py
```

Successful run:

```text
runs/20260530-223810-reciprocal-routing-parent-origin/status.json
```

Readout:

```text
reciprocal_routing_parent_origin_partial_not_derived
```

Next target:

```text
04-vacuum-reciprocity-action-contract.md
```

## 3. Algebraic Result

The motion-load route has:

```text
T^2 = 1 - L
S_p = (1-L)^(-p)
```

Therefore:

```text
T^2 S_p = (1-L)^(1-p).
```

For exact reciprocity over variable load `L`:

```text
T^2 S_p = 1
```

requires:

```text
p = 1.
```

This is a real simplification.

The local GR routing dial is not arbitrary if reciprocity is derived.

## 4. Candidate Parent Origins

The scan found five possible origins:

```text
motion-capacity reciprocity;
determinant balance;
vacuum stress balance;
null-cone preservation;
Hamiltonian dual metric.
```

The strongest route is:

```text
vacuum stress balance + Hamiltonian duality.
```

Reason:

```text
in a static areal metric ds^2=-A dt^2+B dr^2+r^2dOmega^2,
G^t_t = G^r_r implies (A B)' = 0,
and asymptotic flatness gives A B = 1.
```

With:

```text
A = T^2
B = S
```

this gives:

```text
T^2 S = 1.
```

## 5. Why This Is Not Yet A Full Derivation

The strongest route still leans on a GR-like exterior stress-balance equation.

That is useful, but dangerous:

```text
if MTS simply imports G^t_t = G^r_r, then it has rephrased GR rather than
derived the GR limit from motion-load.
```

So the missing parent theorem is:

```text
the MTS/motion-load action must imply the vacuum radial stress balance or an
equivalent Hamiltonian duality that forces A B = 1.
```

Until that is done:

```text
p=1 is conditionally derived from reciprocity;
reciprocity itself is not parent-derived.
```

## 6. Gate Verdict

Passes:

```text
source 02 complete;
algebra forces p=1 from exact reciprocity;
plausible parent routes identified.
```

Fails:

```text
non-GR parent derivation;
promotion to main workbench.
```

Status:

```text
reciprocity = theorem target, not completed theorem.
```

## 7. Next Target

Create:

```text
04-vacuum-reciprocity-action-contract.md
```

Purpose:

```text
write the exact action/stress theorem that must derive AB=1 or T^2S=1 from
motion-load variables without smuggling in Einstein's exterior equations.
```
