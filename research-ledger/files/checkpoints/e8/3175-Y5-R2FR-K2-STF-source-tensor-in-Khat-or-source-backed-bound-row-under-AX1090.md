# 3175 — K2 STF Source Tensor In Khat Or Source-Backed Bound Row Under AX1090

Private checkpoint. This is not a local-GR claim, Newtonian-limit claim, PPN pass, solar J2 score, or public-facing result.

## Result

3174 reduced the live coupling problem to:

```text
S_K2 = delta K_MTS^{mu nu} / delta(K_2 C_K2_unit).
```

For the solar J2 / tracefree channel, the needed object is sharper:

```text
S_K2_STF
  = P_STF,l2[delta K_MTS^{mu nu}/delta sigma_K2]|_0,

sigma_K2 := K_2 C_K2_unit.
```

Using the trace/tensor split:

```text
K_MTS^{mu nu}
  = -Gamma_eff g^{mu nu}
  + K_hat^{mu nu},
```

this becomes:

```text
S_K2_STF
  = P_l2[delta K_hat^{mu nu}/delta sigma_K2]|_0.
```

So yes: the exact target tensor is now defined.

But no: current `K_2` does not instantiate it.

## Why `K_2` Alone Fails

3164 defines:

```text
K_2 := |W_2 M_Lambda|.
```

That is a scalar magnitude.

A tracefree public quadrupole source needs more than magnitude:

```text
signed amplitude;
axis/orientation;
STF tensor basis;
radial/source support;
units converting sigma_K2 into L^-2 source curvature;
conservation/divergence balance.
```

The basic spatial STF basis would be:

```text
Y_STF^{ij}(a)
  = a^i a^j - delta^{ij}/3,
```

with:

```text
delta_ij Y_STF^{ij} = 0.
```

But `K_2` as an absolute value cannot tell us the sign, the axis `a^i`, or the source profile.

## Conditional Source Tensor

If the parent theory later supplies the missing signed data, the source tensor can be written:

```text
delta K_hat_STF^{ij}(x)
  = sigma_K2 A_STF R_K2(r)
    (a^i a^j - delta^{ij}/3).
```

Then:

```text
S_K2_STF^{ij}
  = A_STF R_K2(r)
    (a^i a^j - delta^{ij}/3).
```

This would feed the 3174 effective metric equation:

```text
L_eff[h] = S_K2_STF sigma_K2
```

inside the compact source, and:

```text
L_eff[h] = 0
```

outside the source.

Then the exterior branch uses the 3172 result:

```text
f_2(r) proportional to r^-3.
```

So the exterior Green/radial part is not the live issue anymore. The live issue is the source tensor.

## Conservation Guard

A tracefree tensor source is not automatically safe.

It creates a source-balance residual:

```text
q_K2^nu
  := -nabla_mu(delta K_hat_STF^{mu nu})
     + trace/exchange companions.
```

To claim local safety, the parent theory must prove:

```text
q_K2^nu = 0
```

or supply a boundary theorem, or bound the residual in PPN/source-normalization arenas.

This links 3175 back to the older 1010 guardrail:

```text
Gamma/Khat action existence and q_loc zero remain unproved.
```

## What Is Now Missing

| Object | Meaning | Status |
| --- | --- | --- |
| `s_K2` | signed `W_2 M_Lambda` before absolute value | missing |
| `Y_STF^{mu nu}` | parent-owned tracefree tensor basis/orientation | missing |
| `R_K2(r)` | radial/source kernel with units | missing |
| `delta K_hat_STF` | embedding of K2 lane into Khat | missing |
| `q_K2^nu` | conservation/source-balance residual | missing/bounded route needed |

## Source-Ready Nonclaim Rows

3175 stages nonclaim rows for:

```text
S_K2_STF;
Upsilon_J2_source_moment;
q_K2^nu;
direct STF/PPN comparator.
```

All remain:

```text
valid_for_claim = false.
```

They are not bureaucracy. They are the exact inputs needed to turn the coupling from a phrase into a testable object.

## Decision

The derivation attempt partially succeeds:

```text
S_K2_STF is exactly defined as a projected functional derivative.
```

But current MTS artifacts do not instantiate it:

```text
K_2 is an unsigned scalar magnitude, not a source tensor.
```

Next target:

```text
3176-Y5-R2FR-signed-K2-STF-basis-owner-or-source-moment-bound-under-AX1090.
```

That target should try to derive a signed STF basis/source moment from `Wbar`, `M_Lambda`, `Khat`, or source-domain geometry. If it cannot, keep the route as source-backed nonclaim bounds.

## Generated Artifacts

```text
source-intake/mts_residuals/P8_Y5_R2FR_3175_INPUTS.csv
source-intake/mts_residuals/P8_Y5_R2FR_3175_STF_SOURCE_TENSOR_DERIVATION.csv
source-intake/mts_residuals/P8_Y5_R2FR_3175_K2_SCALAR_TO_TENSOR_AUDIT.csv
source-intake/mts_residuals/P8_Y5_R2FR_3175_STF_SOURCE_CONTRACT.csv
source-intake/mts_residuals/P8_Y5_R2FR_3175_SOURCE_READY_BOUND_ROWS.csv
source-intake/mts_residuals/P8_Y5_R2FR_3175_DECISION.csv
source-intake/mts_residuals/P8_Y5_R2FR_3175_VALIDATION.csv
```
