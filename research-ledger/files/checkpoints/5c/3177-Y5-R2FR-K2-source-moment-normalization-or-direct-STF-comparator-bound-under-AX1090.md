# 3177 - K2 Source-Moment Normalization Or Direct STF Comparator Bound Under AX1090

Private checkpoint. This is not a local-GR claim, Newtonian-limit claim, PPN pass, solar J2 score, or public-facing result.

## Result

3176 closed the angular problem:

```text
P2(a.n) = (3/2) Y_a^{ij} n_i n_j.
```

3177 pushes the next piece: the compact-source moment.

If the 3174 effective local metric equation can be reduced in the public l=2 scalar channel to:

```text
nabla^2 [u_2(r) P2(a.n)] = S_2(r) P2(a.n),
```

with:

```text
S_2(r) = kappa_STF s_K2 C_K2_unit R_K2(r),
```

then the l=2 radial equation is:

```text
(1/r^2)(r^2 u_2')' - 6 u_2/r^2 = S_2(r).
```

For a compact source inside `R_src`, asymptotic flatness gives:

```text
u_2(r > R_src)
  = -(1/5) r^-3 integral_0^Rsrc S_2(r') r'^4 dr'.
```

So the source moment can be compressed as:

```text
A_surface
  = s_K2 C_K2_unit M2_K2,
```

where:

```text
M2_K2
  := - kappa_STF/(5 R_b^3)
       integral_0^Rsrc R_K2(r') r'^4 dr'.
```

That is progress: `M2_K2` is no longer vague. It is a precise Green/source-moment object.

## What Is Still Missing

The formula is exact inside the reduced public Green channel, but not yet instantiated by the parent theory because these objects remain unsigned:

| object | status |
| --- | --- |
| `kappa_STF` | missing signed projection from `delta K_hat_STF` into public l=2 metric equation |
| `R_K2(r)` | missing parent-owned compact radial/source kernel and units |
| `s_K2` | missing signed `W_2 M_Lambda` owner |
| `q_K2^nu` | missing conservation/source-balance theorem or residual bound |

So the J2/local branch is not closed, but the gate is now sharper:

```text
|s_K2 M2_K2| <= A_surface_bound / C_K2_unit.
```

## Direct Product Bound

Using the existing 3170 corrected solar-surface public metric amplitude rows, 3177 converts the bound from a fake-looking `K2` claim into a cleaner product bound:

```text
|s_K2 M2_K2| <= A_metric_bound_surface / C_K2_unit.
```

This is not a pass. It is a nonclaim product constraint.

Interpretation:

```text
if M2_K2 is later derived,
this immediately becomes a bound on |s_K2|;

if s_K2 is later derived,
this immediately becomes a bound on |M2_K2|;

if both are derived,
the local J2/STF branch becomes testable.
```

## Why This Is Better Than Circling

The earlier blocker was:

```text
source moment missing.
```

3177 replaces that with:

```text
M2_K2 = - kappa_STF/(5 R_b^3) integral R_K2(r) r^4 dr.
```

That is a concrete target. The hunt is now for:

```text
kappa_STF,
R_K2(r),
source-balance q_K2^nu.
```

## Decision

The source-moment route is viable as a formal branch, but not claimable yet.

Next target:

```text
3178-Y5-R2FR-Khat-source-kernel-normalization-or-STF-product-bound-gate-under-AX1090.
```

That target should attack `kappa_STF` and `R_K2(r)` directly from the `K_hat`/parent source structure. If the parent route cannot supply them, the correct fallback is a direct STF product-bound gate using `|s_K2 M2_K2|`, not a claimed `K_2` pass.

## Generated Artifacts

```text
source-intake/mts_residuals/P8_Y5_R2FR_3177_INPUTS.csv
source-intake/mts_residuals/P8_Y5_R2FR_3177_GREEN_SOURCE_MOMENT_DERIVATION.csv
source-intake/mts_residuals/P8_Y5_R2FR_3177_M2_NORMALIZATION_CONTRACT.csv
source-intake/mts_residuals/P8_Y5_R2FR_3177_PRODUCT_BOUND_FROM_3170.csv
source-intake/mts_residuals/P8_Y5_R2FR_3177_DIRECT_STF_COMPARATOR_TEMPLATE.csv
source-intake/mts_residuals/P8_Y5_R2FR_3177_DECISION.csv
source-intake/mts_residuals/P8_Y5_R2FR_3177_VALIDATION.csv
```
