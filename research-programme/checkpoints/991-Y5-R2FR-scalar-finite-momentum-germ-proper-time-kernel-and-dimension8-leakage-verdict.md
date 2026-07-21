# 4975 - Scalar finite-momentum germ, proper-time kernel, and dimension-eight leakage verdict

Marker: `MTS_4975_SCALAR_FINITE_MOMENTUM_GERM_AND_PT_KERNEL`

Formal marker: `PPC4161_SCALAR_FINITE_MOMENTUM_GERM_4975`.

## Decision

The free-scalar third response has now been carried one order beyond the
local Weyl-cubic coefficient. The common external-momentum Taylor germ is
evaluated through `q^8` for the same twelve traceful off-shell geometries
used by the independently validated rank-eight `q^6` quotient.

The control closes exactly:

```text
q6 quotient residual       = 9.073324633292171e-16
q6 recovered coefficient   = 2.094105151343174e-7
q6 exact coefficient       = 2.0941051513379998e-7
relative coefficient error = 2.4706903190008234e-12.
```

The first symmetric form-factor dressing does not close at `q^8`. Its
relative response leakage is

```text
0.030214084796217903.
```

That number is unchanged between angular orders eight and ten: the full
`q^8` response-vector difference is `4.4543e-15` and the projected-estimator
difference is `2.4951e-13`. It is therefore not a quadrature failure.

The apparent projected coefficient is also not stable under source removal.
Leave-one-geometry values range from

```text
-2.2660076373437794e-6 to +1.3421671685426887e-6,
```

including sign changes and a maximum relative shift of `5.2147`. The
least-squares value `5.376402133326893e-7` is retained only as a diagnostic
channel estimator. It is not promoted to a Weyl-cubic form-factor
derivative.

This is a useful rejection rather than another missing-input declaration.
The `q^6` baseline passes in the identical pipeline at machine precision,
the `q^8` result is quadrature converged, and its exact mass homogeneity is
independently recovered. The failed object is specifically the assumption
that one sigma-one dressing of the `q^6` quotient spans all third-response
dimension-eight operators.

## 1. Finite-momentum Taylor observable

Scale all three external momenta by one parameter `t` while preserving
momentum closure:

```text
q_i -> t q_i,
W_123(t;m)=sum_n t^n W_123,n(m).
```

The determinant response retains the complete `1+3+2` topology from
checkpoint 4974. The `n=6` and `n=8` coefficients are ultraviolet finite and
are evaluated directly by recursive propagator Taylor algebra before loop
integration. No subtraction of separately divergent amplitudes is used.

For a permutation-symmetric first derivative of a cubic form factor, the
only degree-one scalar in the three external virtualities is

```text
sigma1=q1^2+q2^2+q3^2.
```

If the first derivative merely dressed the retained `q^6` quotient, its
response matrix would be

```text
M8,C3=diag(sigma1) M6.
```

Because every sampled `sigma1` is positive, this matrix has the same
rank-eight right nullspace as `M6`. The Ricci-flat `C3` functional annihilates
that nullspace to `1.2490e-15`, so the diagnostic channel is quotient
invariant inside this restricted image.

The measured response is not inside that image. The converged `3.0214%`
orthogonal component proves that the scalar determinant contains additional
dimension-eight third-response tensors. These include the allowed
four-derivative quadratic-curvature and two-derivative cubic-curvature
classes; they cannot be discarded by calling the calculation a `C3` form
factor.

## 2. Baseline-controlled rejection

The same integration, contacts, source ensemble, and quotient code recover
the known heat-kernel `a6` coefficient. This matters for interpretation:

```text
q6 residual  ~ 9e-16  -> pipeline and local quotient pass;
q8 residual  ~ 3e-2   -> restricted dimension-eight image fails.
```

The angular-order comparison changes the `q^8` vector by only `4.45e-15`.
Consequently the failure is not blamed on MTS, the scalar determinant, or
the numerical machinery in general. It identifies exactly which theoretical
truncation must be enlarged.

## 3. Exact mass homogeneity

After the continuum change of variables `p=m l`, the coefficient of order
`n` obeys

```text
W_123,n(m)=m^(4-n) W_123,n(1).
```

The executable spot-checks three independent geometries at `m=1` and `m=2`
and obtains zero floating-point residual for both orders. Therefore

```text
q6 coefficient ~ m^-2,
q8 response    ~ m^-4.
```

This scaling applies to the complete `q^8` response vector, including its
component outside the restricted `C3` image.

## 4. Proper-time kernel through q8

For a homogeneous Taylor coefficient

```text
a_n(M^2)=A_n (M^2)^(2-n/2),
```

the checkpoint-4974 proper-time `m=3` operator gives

```text
K_n(k)=(3k^2)^3 partial_(M^2)^3 a_n(M^2)
       evaluated at M^2=m^2+3k^2.
```

Writing `x=3k^2/m^2`, its normalized form is

```text
K_n/a_n(m^2)
 =p(p-1)(p-2)x^3/(1+x)^(3-p),
p=2-n/2.
```

The two calculated profiles are

```text
K6/a6  =-6 x^3/(1+x)^4,
K8/a8  =-24 x^3/(1+x)^5.
```

Their positive ultraviolet-to-infrared weights integrate exactly to one.
The cumulative fractions are

```text
F6(x)=x^3/(1+x)^3,
F8(x)=x^3(x+4)/(1+x)^4.
```

The `q^8` magnitude peaks at `x=3/2` with value `-2592/3125`; half its
integrated coefficient is accumulated by `x=1.5925033174107472`. Thus the
proper-time profile of every homogeneous `q^8` response component is known
even though its complete operator decomposition is not yet known.

## 5. Massless-limit ceiling

The local coefficients diverge as `m^-2` and `m^-4`. A finite-order Taylor
germ therefore has no uniform `m -> 0` limit at fixed external momentum.
The physical logarithm cannot be extracted by setting `m=0` in these rows.
It requires either the full momentum-dependent response or a source-complete
dimension-eight-and-higher reconstruction followed by controlled resummation.

## 6. Current status

```text
free-scalar q6 determinant quotient          = exact control pass;
free-scalar q8 response                      = calculated and converged;
q8 mass scaling                              = exact m^-4;
q8 PT-m3 profile and integral                = exact;
sigma1-dressed q6 image                      = rejected as incomplete;
diagnostic q8 C3-channel estimator           = leave-one unstable;
unique C3 form-factor derivative             = not identified;
massless physical logarithm                  = not inferred;
interacting motion third response            = open;
graviton/ghost third response                = open;
exact all-operator compact GR                = false;
full MTS                                     = false.
```

## 7. Next calculation

Checkpoint 4976 must build the complete local dimension-eight third-response
quotient rather than fit the leaked vector. It should include at least the
four-derivative quadratic-curvature and two-derivative cubic-curvature
classes, generate enough independent off-shell geometries to establish its
rank, and recover the free-scalar `a8` response. Only then may the component
associated with a derivative of the `C3` form factor be tested for
nullspace invariance and leave-one stability.

No GitHub action or public claim is authorized.

## Outputs

- `post-checkpoint-work/scripts/Y5_R2FR_4975_scalar_finite_momentum_germ_and_PT_kernel.py`
- `post-checkpoint-work/source-intake/functional_rg/4975/C3_scalar_q6_q8_Taylor_responses.csv`
- `post-checkpoint-work/source-intake/functional_rg/4975/C3_scalar_q6_q8_quotient_projection.csv`
- `post-checkpoint-work/source-intake/functional_rg/4975/C3_scalar_q8_leave_one_geometry.csv`
- `post-checkpoint-work/source-intake/functional_rg/4975/C3_scalar_mass_homogeneity.csv`
- `post-checkpoint-work/source-intake/functional_rg/4975/C3_scalar_PT_m3_q6_q8_kernel.csv`
- `post-checkpoint-work/source-intake/functional_rg/4975/C3_scalar_finite_momentum_germ_gate.csv`
- `post-checkpoint-work/source-intake/functional_rg/4975/C3_scalar_finite_momentum_germ_and_PT_kernel_results.json`

The runner passes `8/8` internal gates. The independent validator passes
`22/22`; validation CSV SHA256 is
`defa054feb409c92caf7157adb070895a32bce12ff848af9afa06be95e10d6e1`.
