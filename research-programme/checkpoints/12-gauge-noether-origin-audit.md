# Gauge-Noether Origin Audit

## 1. Purpose

This file follows:

```text
11-cell-current-origin-attempt.md
```

The question is:

```text
Can a genuine observer-splitting gauge symmetry or Noether identity forbid
Q_R and derive R_AB=0 without importing GR?
```

Short answer:

```text
not in the current scaffold. The local reciprocity route must be treated as a
closure benchmark unless a new constrained parent action is introduced.
```

## 2. Machine Run

Implemented:

```text
scripts/gauge_noether_origin_audit.py
```

Successful run:

```text
runs/20260530-230810-gauge-noether-origin-audit/status.json
```

Readout:

```text
gauge_noether_origin_not_derived_closure_only
```

Next target:

```text
13-local-closure-PPN-benchmark.md
```

## 3. Gauge Routes Tested

Rejected:

```text
radial coordinate gauge:
areal radius already fixes r through r^2 dOmega^2, so AB=1 is not free
coordinate gauge.

cell-scale gauge:
T and S are observable clock/routing factors in this scaffold, so changing
T sqrt(S) changes local observables unless a new matter map is built.

reciprocal split gauge:
T -> exp(sigma)T and sqrt(S)->exp(-sigma)sqrt(S) leaves T sqrt(S) unchanged,
so it cannot impose R_AB=0.

Noether identity:
a symmetry identity relates equations of motion; it does not set R_AB=0 unless
one equation is already a constraint equation.
```

Still possible in principle:

```text
first-class parent constraint:
R_AB could be eliminated in a full constrained Hamiltonian parent theory.
```

But that parent theory is not present here.

## 4. Coordinate Warning

In the areal radial scaffold:

```text
ds^2 = -T^2 c^2 dt^2 + S dr^2 + r^2 dOmega^2
```

the coordinate `r` is tied to sphere area:

```text
area = 4 pi r^2.
```

So using radial coordinate freedom to set:

```text
T^2 S = 1
```

would be a hidden import unless a new gauge-invariant observer theory is written.

In GR, `AB=1` in the Schwarzschild exterior follows from the vacuum equations.
That cannot be used as a premise for MTS.

## 5. Noether Warning

A Noether identity has the schematic form:

```text
sum_i E_i delta phi_i + divergence = 0.
```

This is an identity among equations of motion.

It is not the same as:

```text
delta lambda_R S = R_AB = 0.
```

So Noether structure can explain a constraint only after the parent action has
a genuine constrained variable or first-class constraint.

It cannot replace that derivation.

## 6. Gate Verdict

Passes:

```text
source 11 complete;
closure route remains available;
first-class constraint remains possible in principle.
```

Fails:

```text
radial coordinate gauge derives AB=1;
cell-scale gauge available in current scaffold;
Noether identity derives R_AB=0;
promotion to main workbench as derived GR.
```

Status:

```text
local reciprocity is closure-only, not parent-derived.
```

## 7. Meaning For The Programme

This is not a catastrophe.

It means the local branch has been disciplined:

```text
R_AB=0 is allowed as a benchmark closure that reproduces the GR-like local
lane, but it cannot be advertised as derived from motion-load alone.
```

That is still useful because it gives a strict target for any future parent
action:

```text
beat the closure by deriving R_AB=0, no Q_R hair, beta=1, conservation, and
universal matter coupling.
```

## 8. Next Target

Create:

```text
13-local-closure-PPN-benchmark.md
```

Purpose:

```text
formalize the honest closure benchmark: assume R_AB=0 explicitly, compute the
local PPN/solar-system pass conditions, and separate what is tested from what
is derived.
```
