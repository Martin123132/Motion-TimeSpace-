# 5039 - completed four-scramble uncertainty and target audit

**Status: COMPLETE AS AN UNCERTAINTY AUDIT; neither an epsilon-zero result nor a fixed-target verdict is claimed.**

## Completed source matrix

The immutable 5037 matrix is now complete at `189/189` terminal jobs:

```text
expected jobs          = 189
exact imports          = 117
computed-converged     = 72
failed                 = 0
unconverged            = 0
paired outer scrambles = 4
```

The three finite A14 endpoint jobs at `epsilon=(0.08,0.04,0.02)` each have
their own two-floor certificate. Their maximum local double-residue magnitudes
are below `1.08e-14`; all one-sided and adjacent-sector limit residuals are
below `9.29e-9`. Six chart-origin-only rows close independently under v5. No
finite endpoint was classified as a chart root.

## Why the deterministic gate is insufficient

The complete mean regulator steps are

```text
full vector       : 14.0466 -> 11.1743
local coefficient :  4.2014 ->  2.5591
```

but two nonlocal mean components increase:

```text
z=-0.6 : 2.8141 -> 4.7299
z=+0.3 : 3.1232 -> 5.8098.
```

Those are norms of four-scramble sample means, not noiseless observables. A
raw increase is a valid warning, but it is not by itself evidence that the
regulator limit fails. The audit therefore tests the paired eventwise quantity

```text
delta_i = |N_i(0.02)-N_i(0.04)| - |N_i(0.04)-N_i(0.08)|
```

with a Student 95% interval, and the first-order scaling defect

```text
Q_i = [N_i(0.02)-N_i(0.04)]
    - 0.5 [N_i(0.04)-N_i(0.08)]
```

with a two-dimensional Hotelling diagnostic and all 16 exact sign flips.

## Convergence result

The two raw failures are not statistically resolved as noncontraction:

```text
z=-0.6 : delta 95% interval = [-5.169, +3.292]
z=+0.3 : delta 95% interval = [-7.486, +1.768].
```

The `z=+0.6` component supports contraction at 95%, with interval
`[-5.228,-0.029]`; the other four are unresolved. No component supports
noncontraction at 95%. Every complex first-order defect, including the local
coefficient defect, contains zero within its Hotelling 95% region. With only
four replicates, this is a non-rejection and not a proof of linear scaling.

## Fixed-target result

The untouched 5018 target was loaded after eventwise local projection and was
not fitted. All five real residual intervals contain zero:

```text
z=-0.6 : [-272.08, +391.15]
z=-0.3 : [ -56.07, +112.14]
z= 0.0 : [-228.15, +153.51]
z=+0.3 : [ -78.16, +120.95]
z=+0.6 : [-248.29, +105.29].
```

No component excludes the fixed target, but these intervals are far too wide
to establish agreement. Normal-approximate planning counts for resolving the
currently observed residuals are approximately `(48,14,40,33,10)` independent
replicates. These are planning diagnostics, not guaranteed stopping counts,
because the effect and variance estimates themselves come from four samples.

## Reflection result

Reflection was measured and never imposed. Neither odd component excludes the
fixed target at 95%:

```text
|z|=0.6 : odd residual interval [-19.69,+150.73]
|z|=0.3 : odd residual interval [-25.39, +32.02].
```

The large positive `|z|=0.6` point estimate remains a watch item, not a claim.

## Decision

The completed four-scramble calculation is neither a target match nor a
regulator failure. It establishes that outer variance, not inner quadrature or
endpoint topology, is now the limiting uncertainty. The predeclared minimum
of eight scrambles must not be treated as guaranteed precision: the next run
should use sequential stopping based on paired contraction, target-residual,
and odd-component intervals. Increasing points within each scramble should be
compared with merely adding one-point scrambles, because the present design is
effectively a very small RQMC population.

Outputs:

- `source-intake/functional_rg/5039/completed_matrix_uncertainty_audit.json`
- `source-intake/functional_rg/5039/contraction_uncertainty.csv`
- `source-intake/functional_rg/5039/fixed_target_uncertainty.csv`
- `source-intake/functional_rg/5039/reflection_uncertainty.csv`

No GitHub action was taken. No production `hhh`, local-GR, Newton, Maxwell, or
full-MTS claim follows from this numerical sector.

Marker: `MTS_5039_COMPLETED_MATRIX_UNCERTAINTY_AUDIT`.
