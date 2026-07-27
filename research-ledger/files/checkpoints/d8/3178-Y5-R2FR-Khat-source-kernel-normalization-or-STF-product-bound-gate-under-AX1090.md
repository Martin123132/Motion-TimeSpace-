# 3178 - Khat Source-Kernel Normalization Or STF Product-Bound Gate Under AX1090

Private checkpoint. This is not a local-GR claim, Newtonian-limit claim, PPN pass, solar J2 score, or public-facing result.

## Result

3177 reduced the local STF/J2 coupling problem to:

```text
M2_K2
  = - kappa_STF/(5 R_b^3)
      integral_0^Rsrc R_K2(r) r^4 dr.
```

3178 asks whether the current corpus can source `kappa_STF` or `R_K2(r)` from `K_hat`.

Verdict:

```text
No live source-owned K_hat source kernel is found.
```

The best current candidate remains the tracefree Hessian/improvement route:

```text
K_L^{mu nu}
  = 2 nabla^mu nabla^nu phi
    - (1/2) g^{mu nu} Box phi.
```

That route is mathematically real and exactly tracefree in four dimensions, but 3067 still refuses to promote it as live MTS `K_hat` because the parent action, coefficient/sign, `phi` owner, boundary convention, current-symbol match, and metric-response safety are not source-signed.

So 3178 does not close `R_K2`. It does something still useful: it normalizes the unknown source kernel so the unknown becomes a clean product-bound object.

## Source-Kernel Extractor

From 3176:

```text
Y_a^{ij} := a^i a^j - delta^{ij}/3,
Y_a:Y_a = 2/3,
P2(a.n) = (3/2)Y_a^{ij}n_i n_j.
```

If a parent source later supplies `delta K_hat_STF^{ij}`, the radial kernel is extractable by projection:

```text
R_K2(r)
  := [Y_{a,ij} delta K_hat_STF^{ij}(r)]
      /[(3/2) s_K2 C_K2_unit (Y_a:Y_a)].
```

Equivalently:

```text
R_K2(r)
  = [Y_{a,ij} delta K_hat_STF^{ij}(r)]
      /[s_K2 C_K2_unit],
```

because:

```text
(3/2)(Y_a:Y_a) = 1.
```

That is a tidy little win: the STF projection normalization cancels exactly.

But it still requires `delta K_hat_STF` to be live and parent-owned. Current files do not give that.

## Dimensionless Kernel

Since the public weak-field source equation has:

```text
nabla^2 u_2 = S_2,
```

the source side has units:

```text
[S_2] = L^-2.
```

If:

```text
S_2(r)
  = kappa_STF s_K2 C_K2_unit R_K2(r),
```

and `kappa_STF` is treated as dimensionless, then:

```text
[R_K2] = L^-2.
```

Set:

```text
x := r/R_b,
eta := R_src/R_b,
R_K2(r) := R_b^-2 hat_R_K2(x).
```

Then:

```text
M2_K2
  = -(kappa_STF/5)
      integral_0^eta hat_R_K2(x) x^4 dx.
```

Define the dimensionless fourth moment:

```text
I4[hat_R]
  := integral_0^eta hat_R_K2(x) x^4 dx.
```

So:

```text
M2_K2 = -(kappa_STF/5) I4[hat_R].
```

This is the clean 3178 result.

## Product-Bound Gate

3177 gave:

```text
|s_K2 M2_K2| <= B_product.
```

Using the 3178 normalization:

```text
|s_K2 kappa_STF I4[hat_R]| <= 5 B_product.
```

So the unknowns are now organized as:

```text
signed amplitude    s_K2,
operator projection kappa_STF,
source shape        I4[hat_R].
```

This is not a claim, but it is a better gate:

```text
the experiment constrains the product of the amplitude, operator projection, and source shape.
```

The tightest carried 3170/3177 row gives:

```text
|s_K2 M2_K2| <= 3.898004369090585e10,
```

equivalently:

```text
|s_K2 kappa_STF I4[hat_R]| <= 1.949002184545293e11.
```

## Tracefree Route Status

The tracefree Hessian route remains the best mathematical throat:

```text
K_L^{mu nu}
  = 2 nabla^mu nabla^nu phi
    - (1/2)g^{mu nu}Box phi.
```

But current evidence still says:

| clause | status |
| --- | --- |
| live `K_hat = K_L` adoption | not signed |
| parent action coefficient/sign | missing |
| `phi` owner/source equation | missing |
| boundary/Green/projector silence | missing |
| curved Ricci/source-balance residual | retained |
| metric-response safety | missing |

So:

```text
R_K2^cand(r)
  = [Y_{a,ij} K_L^{ij}(r)]/[s_K2 C_K2_unit]
```

is allowed only as a candidate projection, not as the live MTS source kernel.

## Decision

3178 does not derive local GR. It does not close the parent coupling.

It does sharpen the problem:

```text
M2_K2 = -(kappa_STF/5) I4[hat_R],
```

and:

```text
|s_K2 kappa_STF I4[hat_R]| <= 5 B_product.
```

Next target:

```text
3179-Y5-R2FR-tracefree-Hessian-K2-kernel-projection-or-DeltaKTF-product-bound-under-AX1090.
```

That target should attempt the tracefree Hessian projection explicitly. If the parent route still cannot adopt `K_L` as live `K_hat`, it should demote the route to a `DeltaK_TF` product-bound component instead of pretending `R_K2` is sourced.

## Generated Artifacts

```text
source-intake/mts_residuals/P8_Y5_R2FR_3178_INPUTS.csv
source-intake/mts_residuals/P8_Y5_R2FR_3178_KERNEL_EXTRACTION_DERIVATION.csv
source-intake/mts_residuals/P8_Y5_R2FR_3178_TRACEFREE_KHAT_ROUTE_AUDIT.csv
source-intake/mts_residuals/P8_Y5_R2FR_3178_DIMENSIONLESS_MOMENT_NORMALIZATION.csv
source-intake/mts_residuals/P8_Y5_R2FR_3178_STF_PRODUCT_BOUND_GATE.csv
source-intake/mts_residuals/P8_Y5_R2FR_3178_DECISION.csv
source-intake/mts_residuals/P8_Y5_R2FR_3178_VALIDATION.csv
```
