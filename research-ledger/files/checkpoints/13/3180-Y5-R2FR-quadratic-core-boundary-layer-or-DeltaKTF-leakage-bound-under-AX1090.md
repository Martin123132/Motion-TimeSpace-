# 3180 - Quadratic Core Boundary Layer Or DeltaKTF Leakage Bound Under AX1090

Private checkpoint. This is not a local-GR claim, Newtonian-limit claim, PPN pass, solar J2 score, or public-facing result.

## Result

3179 found that the tracefree Hessian candidate has the projected K2 operator:

```text
D2[F]
  = (2/5)F'' + 2F'/r + 6F/(5r^2).
```

3180 tests the natural profile picture:

```text
quadratic core: F_in = A r^2,
exterior branch: F_out = C r^-3.
```

Value matching at `r=R_b` gives:

```text
C = A R_b^5.
```

But derivative matching fails:

```text
F'_in(R_b)  =  2A R_b,
F'_out(R_b) = -3A R_b,
[F']        = -5A R_b.
```

So a nontrivial quadratic core cannot be glued directly to an exterior `r^-3` branch as a smooth `C1` profile. It needs either:

```text
a shell/boundary source,
or a finite transition layer,
or a parent-owned matching theorem.
```

No free smooth glue. The goblin stamps this one in red ink.

## Projected Moment Win

There is still a useful derivation.

For:

```text
D2[F] = (2/5)F'' + 2F'/r + 6F/(5r^2),
```

integration by parts gives:

```text
integral_a^b D2[F] r^4 dr
  = (2/5)[r^4F' + r^3F]_a^b.
```

Therefore, for a regular origin and exterior:

```text
F -> C r^-3,
```

the projected moment is fixed:

```text
integral_0^infty D2[F] r^4 dr
  = -4C/5.
```

In dimensionless form:

```text
I4_D2 = -4 c_ext/5.
```

If, and only if, the tracefree Hessian route is parent-adopted and the tensor leakage is zero/bounded:

```text
M2_K2^proj
  = -(kappa_STF/5) I4_D2
  = (4/25) kappa_STF c_ext.
```

This is a real projected-kernel result. It is not a full tensor/local-GR result.

## Sharp Shell Check

For the sharp value-matched profile:

```text
[F'] = -5A R_b.
```

So:

```text
F''_shell = [F'] delta(r-R_b),
```

and:

```text
D2_shell
  = (2/5)[F']delta(r-R_b)
  = -2A R_b delta(r-R_b).
```

The core contributes:

```text
integral_0^Rb 6A r^4 dr
  = 6A R_b^5/5.
```

The shell contributes:

```text
-2A R_b^5.
```

Total:

```text
6A R_b^5/5 - 2A R_b^5
  = -4A R_b^5/5
  = -4C/5.
```

This matches the boundary identity.

## Product-Bound Recast

3177 gave:

```text
|s_K2 M2_K2| <= B_product.
```

With the conditional projected Hessian result:

```text
M2_K2^proj = (4/25)kappa_STF c_ext,
```

the gate becomes:

```text
|s_K2 kappa_STF c_ext|
  <= (25/4)B_product.
```

The tightest carried row gives:

```text
|s_K2 kappa_STF c_ext|
  <= 2.436252730681616e11.
```

Again: nonclaim, parent-and-leakage gated.

## The Remaining Problem

The projected moment is not the whole tensor.

3179 already showed the full Hessian contains extra tensor-harmonic pieces when:

```text
B'(r) != 0,
B(r) := (3/2)F(r)/r^2.
```

A finite transition layer necessarily has:

```text
B'(r) != 0.
```

The exterior harmonic branch also satisfies:

```text
D2[C r^-3] = 0,
```

but that only kills the pure projected source moment. The full Hessian of an exterior l=2 harmonic field can still have a tidal tensor footprint. So the next live object is:

```text
K_perp_layer/exterior,
DeltaK_TF,
metric response of K_L.
```

These must be:

```text
parent-zero,
metric-null,
or explicitly bounded against local tests.
```

## Decision

3180 gives a mixed but useful result:

```text
projected source moment closes conditionally,
full tensor leakage remains open.
```

The route is not dead. It is sharper:

```text
either prove the Hessian carrier is metric-null / leakage-silent,
or use DeltaK_TF leakage bounds.
```

Next target:

```text
3181-Y5-R2FR-exterior-Hessian-tidal-footprint-or-metric-null-bound-under-AX1090.
```

That target should attack the exterior/full-Hessian tensor footprint directly. If it is not metric-null, it becomes a local STF/tidal residual bound rather than a local-GR derivation.

## Generated Artifacts

```text
source-intake/mts_residuals/P8_Y5_R2FR_3180_INPUTS.csv
source-intake/mts_residuals/P8_Y5_R2FR_3180_CORE_EXTERIOR_MATCHING_NO_GO.csv
source-intake/mts_residuals/P8_Y5_R2FR_3180_PROJECTED_MOMENT_IDENTITY.csv
source-intake/mts_residuals/P8_Y5_R2FR_3180_SHELL_TRANSITION_LEDGER.csv
source-intake/mts_residuals/P8_Y5_R2FR_3180_PRODUCT_BOUND_RECAST.csv
source-intake/mts_residuals/P8_Y5_R2FR_3180_DELTAKTF_LEAKAGE_REQUIREMENTS.csv
source-intake/mts_residuals/P8_Y5_R2FR_3180_DECISION.csv
source-intake/mts_residuals/P8_Y5_R2FR_3180_VALIDATION.csv
```
