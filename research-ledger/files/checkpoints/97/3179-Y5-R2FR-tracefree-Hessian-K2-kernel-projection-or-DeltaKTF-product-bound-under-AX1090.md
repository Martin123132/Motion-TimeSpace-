# 3179 - Tracefree Hessian K2 Kernel Projection Or DeltaKTF Product Bound Under AX1090

Private checkpoint. This is not a local-GR claim, Newtonian-limit claim, PPN pass, solar J2 score, or public-facing result.

## Result

3178 normalized the unknown source moment:

```text
M2_K2 = -(kappa_STF/5) I4[hat_R].
```

3179 tests the best current `K_hat` candidate: the tracefree Hessian/improvement route.

Use:

```text
K_L^{mu nu}
  = 2 nabla^mu nabla^nu phi
    - (1/2)g^{mu nu}Box phi.
```

For an axisymmetric scalar l=2 carrier:

```text
phi(r,n) = F(r)P2(a.n)
         = (3/2)F(r)Y_a^{ij}n_i n_j.
```

Write:

```text
phi = B(r)Y_a^{ij}x_i x_j,
B(r) := (3/2)F(r)/r^2.
```

Then the angular-averaged pure `Y_a^{ij}` projection of the spatial tracefree Hessian candidate is:

```text
P_Y[K_L]^{ij}
  = D2[F](r)Y_a^{ij},
```

with:

```text
D2[F]
  = (2/5)F'' + 2F'/r + 6F/(5r^2).
```

That is a real derivation: the candidate K2 source-kernel projection is now explicit.

## Checks

For the source-free exterior l=2 profile:

```text
F_ext = C r^-3,
```

the operator gives:

```text
D2[F_ext] = 0.
```

Good: this matches the 3172 result that the exterior `r^-3` branch is source-free.

For a quadratic core:

```text
F_core = A r^2,
```

the operator gives:

```text
D2[F_core] = 6A.
```

So a pure constant `Y_a^{ij}` kernel is possible in a special quadratic-core region.

## The Catch

The full Hessian is not generally just:

```text
R(r)Y_a^{ij}.
```

The Cartesian Hessian contains:

```text
partial_i partial_j[B Y_ab x_a x_b]
  = B'' n_i n_j S
    + (B'/r)(delta_ij - n_i n_j)S
    + 2rB'(n_iY_j+n_jY_i)
    + 2B Y_ij,
```

where:

```text
S := Y_ab x_a x_b.
```

The extra tensor-harmonic pieces vanish pointwise only if:

```text
B'(r)=0,
```

equivalently:

```text
d(F/r^2)/dr = 0.
```

So the simple 3175 source ansatz:

```text
delta K_hat_STF^{ij} = R_K2(r)Y_a^{ij}
```

is exact for the Hessian candidate only when:

```text
F(r) = A r^2
```

on the region being modeled.

That is useful but restrictive. A compact source has to transition from a quadratic core to an exterior `r^-3` profile, and that transition creates boundary-layer or tensor-harmonic leakage unless the parent theory owns or cancels it.

## Bound Form

If the tracefree Hessian route is parent-adopted and the leakage is zero or bounded, then:

```text
I4[hat_R]
  -> integral_0^eta D2[hat_F](x)x^4 dx.
```

The 3178 gate carries through:

```text
|s_K2 kappa_STF I4[hat_R]| <= 5 B_product.
```

But because `K_L` is not yet live `K_hat`, and because the non-pure leakage is not zeroed, this remains a nonclaim product-bound component.

## Decision

3179 is a genuine step forward:

```text
D2[F] = (2/5)F'' + 2F'/r + 6F/(5r^2)
```

is the explicit tracefree-Hessian K2 projection.

But it also finds the next obstruction:

```text
the Hessian route is not generically a pure R(r)Y_ij source.
```

Therefore the next target is:

```text
3180-Y5-R2FR-quadratic-core-boundary-layer-or-DeltaKTF-leakage-bound-under-AX1090.
```

That target should test whether the quadratic-core plus exterior `r^-3` profile can be matched with a parent-owned boundary layer. If not, the leakage becomes an explicit `DeltaK_TF` product-bound row.

## Generated Artifacts

```text
source-intake/mts_residuals/P8_Y5_R2FR_3179_INPUTS.csv
source-intake/mts_residuals/P8_Y5_R2FR_3179_HESSIAN_PROJECTION_DERIVATION.csv
source-intake/mts_residuals/P8_Y5_R2FR_3179_PURE_KERNEL_CONDITION.csv
source-intake/mts_residuals/P8_Y5_R2FR_3179_TRACEFREE_LEAKAGE_AUDIT.csv
source-intake/mts_residuals/P8_Y5_R2FR_3179_PRODUCT_BOUND_CARRY_FORWARD.csv
source-intake/mts_residuals/P8_Y5_R2FR_3179_DECISION.csv
source-intake/mts_residuals/P8_Y5_R2FR_3179_VALIDATION.csv
```
