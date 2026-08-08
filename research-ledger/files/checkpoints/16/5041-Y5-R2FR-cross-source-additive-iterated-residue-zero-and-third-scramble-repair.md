# 5041 Y5/R2FR cross-source additive iterated-residue zero and third-scramble repair

Marker: `MTS_5041_CROSS_SOURCE_ADDITIVE_ZERO_REPAIR`.

**Scope correction:** the proof and independent witness certify only the two
owned `direct:g1` families listed below. The original eight third-scramble
repairs remain valid. The former broad fourth-scramble extension is quarantined
by 5045 and replaced by the numerical restricted-scope recomputation in
5047-5048.

## Question

Eight third-scramble kernels were blocked by one required collision between an
owned `direct:g1` global pole and an unowned `subtraction:decay` global pole.
Double-precision nested contours did not converge. The question was whether the
associated causal iterated residue is nonzero or whether the instability is a
finite-node artefact.

## Exact local identity

Let `z` be the global azimuth variable, `q` the relative azimuth variable and
`q0` the cross-source collision. The finite-plus integrand has the source
decomposition

```text
I_plus(z,q) = I_D(z,q) + I_S(z,q),
I_D = direct/x_soft,
I_S = -subtraction/x_soft.
```

The causal local cycle follows the single owned direct pole `z_D(q)` and has
radius smaller than the distance to every other global pole. Therefore

```text
oint_C_D(q) dz/(2 pi i z) I_S(z,q) = 0,
oint_C_D(q) dz/(2 pi i z) I_D(z,q) = R_D(q).
```

The first equality is Cauchy's theorem: the subtraction pole is outside the
owned local disk. At `q0`, the collision group contains exactly one direct label
and one subtraction label. There is no same-component direct collision, so the
simple-pole residue `R_D(q)` is holomorphic through `q0`. The audited disks also
exclude `q=0` and `z=0`. Consequently

```text
Res_(q=q0) [R_D(q)/q] = 0,
Res_(q=q0) Res_(z=z_D(q)) [I_plus(z,q)/(z q)] = 0.
```

This statement uses the same global-first, relative-second causal order as the
production transport. It is not a claim that arbitrary same-source or
multiplicative pole pinches vanish.

## Independent numerical witness

`scripts/Y5_R2FR_5040_arbitrary_precision_cross_source_residue.py` ports the
full finite-plus integrand to arbitrary precision and separates the additive
source before the local Cauchy evaluation. Its generic-point values agree with
the production integrand within `3e-13` relative error.

At 70 decimal digits and 16 nodes on each contour, both collision branches give
the analytic trapezoid alias law:

```text
branch                 radius 0.1       radius 0.05      ratio
minus_v / minus_u      1.23821e-19      1.88935e-24      about 65536
plus_v  / plus_u       1.24304e-19      1.89120e-24      about 65536
expected                                                   2^16
```

This is a witness to the exact identity, not the reason the residue is zero.

## Repair result

`scripts/Y5_R2FR_5041_cross_source_additive_zero_repair.py` audits the source
decomposition, ownership, simple-pole condition, collision group, nonzero chart
coordinates and nested contour isolation before applying the identity. Original
jobs and kernels are retained under
`source-intake/functional_rg/5041/repairs/cross_source_additive_zero_v1/original`.

All eight candidates were recomputed from their original topologies:

```text
candidate jobs          = 8
repaired-converged       = 8
still open               = 0
live failed              = 0
live unconverged         = 0
terminal matrix jobs     = 333/378
production-clean seeds   = 3/4
```

The repair is hash-linked in every repaired job and kernel. It inserts an exact
zero correction only when every theorem guard passes.

## Corrected fourth-scramble completion

The old `scripts/Y5_R2FR_5041_theorem_guarded_5040_resume.py` extension produced
372 certificates outside the independently witnessed family and is no longer
an active result. Checkpoints 5047-5048 instead recompute the 45 fourth-scramble
jobs numerically. They give `378/378` terminal live jobs with zero failures,
zero unconverged rows, and zero fourth-scramble theorem substitutions.

The completed nested/sample-0 SD ratios are
`(0.935,0.657,0.632,0.759,0.673)`. Corresponding nested/equal-cost-independent
halfwidth ratios are `(1.780,1.251,1.203,1.445,1.281)`. Under the predeclared
worst-component rule the design decision is therefore
`SWITCH_TO_ADDITIONAL_INDEPENDENT_SCRAMBLES`.

## Boundary and next calculation

Matrix completion is not precision completion. Strict target equivalence and
imaginary-zero equivalence each fail 5/5 components; contraction is supported
for 3/5. No production `hhh`, local GR, Newton, Maxwell or full MTS claim follows.
The next step is to derive and pilot an unbiased independent-scramble control
variate or stratification from the already known endpoint/soft structure before
authorizing more expensive sampling.

Superseding markers: `MTS_5045_THEOREM_SCOPE_FALSIFICATION_AND_QUARANTINE`,
`MTS_5048_INTEGRATE_RESTRICTED_FOURTH_SCRAMBLE_AND_REAUDIT`.
