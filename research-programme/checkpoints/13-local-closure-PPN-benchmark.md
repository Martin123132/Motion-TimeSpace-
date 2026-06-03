# Local Closure PPN Benchmark

## 1. Purpose

This file follows:

```text
12-gauge-noether-origin-audit.md
```

The question is:

```text
If local reciprocity is closure-only, what exactly does the honest closure
benchmark pass, and what does it not prove?
```

Short answer:

```text
the closure is a valid local GR control baseline, not a parent derivation.
```

## 2. Machine Run

Implemented:

```text
scripts/local_closure_ppn_benchmark.py
```

Successful run:

```text
runs/20260530-231158-local-closure-PPN-benchmark/status.json
```

Readout:

```text
local_closure_ppn_benchmark_valid_control_not_derivation
```

Next target:

```text
14-closure-deviation-PPN-sensitivity.md
```

## 3. Explicit Closure Assumptions

The benchmark assumes:

```text
T^2 = 1 - L
R_AB = ln(T^2 S) = 0
S = 1/T^2
Q_R = 0
angular sector = r^2 dOmega^2
universal matter coupling to the same observer coframe
```

Therefore:

```text
S = 1/(1-L)
p = 1.
```

This is the GR-like local exterior lane.

But the assumptions are not all derived. In particular:

```text
R_AB=0 and Q_R=0 are closure assumptions in this branch.
```

## 4. Benchmark Numbers

Under the closure:

```text
gamma = 1
beta = 1
GPS satellite-minus-ground = 38.60879935757566 microseconds/day
solar limb light bending = 1.7512432813682448 arcsec
solar Shapiro scale = 119.4750358485562 microseconds
Mercury perihelion = 42.98201260912118 arcsec/century
```

These match the GR control lane because the closure has made the local exterior
Schwarzschild-equivalent.

That is useful, but it is not a new local prediction.

## 5. Claim Separation

Allowed claim:

```text
If MTS imposes R_AB=0 as a local closure, the local solar-system benchmark
reduces to the GR exterior control lane.
```

Not allowed:

```text
MTS derives local GR from motion-load alone.
```

Not allowed:

```text
The closure is empirical evidence for the parent theory.
```

The closure is a control baseline. It is what future deviations or parent
actions must beat.

## 6. Sensitivity Warning

If reciprocal hair leaves:

```text
R_AB approx q_R L
```

then:

```text
gamma approx 1 + q_R.
```

So even small nonzero `q_R` acts directly like a local PPN residual.

That is why the next step is to quantify deviation sensitivity rather than
pretend the closure has solved the parent problem.

## 7. Gate Verdict

Passes:

```text
source 12 complete;
closure assumptions explicit;
gamma passes under closure;
closure not mislabeled as derivation.
```

Conditional pass:

```text
beta passes if exact areal Schwarzschild completion is accepted as the benchmark.
```

Fails:

```text
novel local prediction;
promotion to main workbench as derived GR.
```

Status:

```text
valid local control baseline;
not a fundamental derivation.
```

## 8. Next Target

Create:

```text
14-closure-deviation-PPN-sensitivity.md
```

Purpose:

```text
quantify how q_R, beta drift, matter-coupling drift, or residual R_AB hair
would show up in local observables, so the closure can become a falsifiable
deviation budget rather than a handwave.
```
