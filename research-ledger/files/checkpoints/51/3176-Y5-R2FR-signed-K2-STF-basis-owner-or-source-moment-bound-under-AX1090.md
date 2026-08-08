# 3176 - Signed K2 STF Basis Owner Or Source-Moment Bound Under AX1090

Private checkpoint. This is not a local-GR claim, Newtonian-limit claim, PPN pass, solar J2 score, or public-facing result.

## Result

3175 left the K2 local branch blocked because:

```text
K_2 := |W_2 M_Lambda|
```

is an unsigned scalar magnitude, while a public quadrupole/local tracefree source needs a signed STF tensor.

3176 gets a real partial win:

```text
the missing angular STF basis is derivable.
```

For the 3164 one-dimensional l=2 lane:

```text
e2(n) := P2(cos theta),
```

let `a^i` be the unit axis of the boundary chart and `n^i` the unit radial vector, so:

```text
cos theta = a_i n^i.
```

Define:

```text
Y_a^{ij} := a^i a^j - delta^{ij}/3.
```

Then:

```text
delta_ij Y_a^{ij} = 0,
```

and:

```text
Y_a^{ij} n_i n_j
  = (a.n)^2 - 1/3
  = (2/3) P2(a.n).
```

Therefore:

```text
P2(a.n) = (3/2) Y_a^{ij} n_i n_j.
```

So the scalar `P2` lane can be lifted into a canonical axisymmetric spatial STF angular basis. This part is not hand-waving; it is an exact identity.

## Signed Boundary Lift

The correct signed quantity is not `K_2`, but:

```text
s_K2 := W_2 M_Lambda.
```

The absolute lane is only:

```text
K_2 = |s_K2|.
```

So the signed source normalization should be:

```text
sigma_K2_signed := s_K2 C_K2_unit.
```

Using the derived STF identity, a signed boundary l=2 profile can be written:

```text
delta z_boundary(n)
  = s_K2 C_K2_unit P2(a.n)
```

as:

```text
T_K2^{ij}|_boundary
  = (3/2) s_K2 C_K2_unit Y_a^{ij},
```

because:

```text
T_K2^{ij} n_i n_j
  = s_K2 C_K2_unit P2(a.n).
```

This closes the angular-normalization problem.

## What It Does Not Close

The above does not yet supply a compact parent source tensor inside `K_hat`.

The needed interior/source object is still:

```text
delta K_hat_STF^{ij}(x)
  = (3/2) s_K2 C_K2_unit R_K2(r) Y_a^{ij}
```

with:

```text
R_K2(r)      = parent-owned radial/source kernel,
M2_K2        = Green/source moment of R_K2(r) Y_a^{ij},
q_K2^nu      = conservation/source-balance residual.
```

The 3173/3174 extractor then becomes:

```text
Upsilon_J2
  = P_surf,l2 L_eff^{-1}
      [(3/2) s_K2 C_K2_unit R_K2(r) Y_a^{ij}]
```

or, after source-moment compression:

```text
Upsilon_J2_pred = s_K2 C_K2_unit M2_K2.
```

For bounds only:

```text
|Upsilon_J2_pred|
  <= K_2 C_K2_unit |M2_K2|.
```

This is useful because it separates prediction from envelope:

```text
prediction needs s_K2,
bound/envelope may use K_2.
```

## Claim Gate

The angular STF basis is now derived, but the branch still cannot claim a local-GR/J2/PPN pass until the parent supplies:

| object | status |
| --- | --- |
| `s_K2 = W_2 M_Lambda` | missing signed parent owner |
| `a^i` as parent source axis | public chart axis exists; parent/source ownership conditional |
| `R_K2(r)` | missing radial/source kernel and units |
| `M2_K2` | missing Green/source moment |
| `q_K2^nu` | missing conservation/source-balance closure or bound |

So 3176 improves the situation, but it does not finish the coupling problem.

## Decision

The previous bottleneck:

```text
K_2 is scalar, not tensor.
```

has been narrowed:

```text
the scalar l=2 angular lane has an exact STF tensor lift.
```

The new live bottleneck is sharper:

```text
derive or source the signed compact-source moment M2_K2 and conservation balance.
```

Next target:

```text
3177-Y5-R2FR-K2-source-moment-normalization-or-direct-STF-comparator-bound-under-AX1090.
```

That target should try to derive `M2_K2` from the parent source geometry or, if that fails, build a direct STF comparator/bound row without claiming local GR.

## Generated Artifacts

```text
source-intake/mts_residuals/P8_Y5_R2FR_3176_INPUTS.csv
source-intake/mts_residuals/P8_Y5_R2FR_3176_STF_BASIS_DERIVATION.csv
source-intake/mts_residuals/P8_Y5_R2FR_3176_SIGNED_AMPLITUDE_AUDIT.csv
source-intake/mts_residuals/P8_Y5_R2FR_3176_SOURCE_MOMENT_CONTRACT.csv
source-intake/mts_residuals/P8_Y5_R2FR_3176_BOUND_ROW_TEMPLATE.csv
source-intake/mts_residuals/P8_Y5_R2FR_3176_DECISION.csv
source-intake/mts_residuals/P8_Y5_R2FR_3176_VALIDATION.csv
```
