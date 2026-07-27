# 5123 — physical hhh angular-first branch and crossed-remainder audit

## Result

This checkpoint makes a physics calculation rather than another missing-input
ledger.  The physical `hhh` cut is no longer inferred from the unstable
`epsilon -> 0` five-point rows.  At each fixed physical scattering angle it
performs the internal angular average first, subtracts the independently
derived checkpoint-5019 endpoint only after that average, and then evaluates

```text
D_hhh(z)/G^3 = -(2/pi) integral_0^1 dx [G(x,z)-G(0,z)]/x.
```

This is the ordering required by checkpoint 5014.  It never uses the rejected
pointwise soft-endpoint subtraction.  Identical outgoing-scalar exchange gives
the integrated identity `D_hhh(z)=D_hhh(-z)`; paired angles are therefore
symmetrized before use.

| physical `z` | angular-first `D_hhh/G^3` | RQMC SE |
|---:|---:|---:|
| -0.6 | -0.03557017332 | 0.000207 |
| -0.3 | -0.0005238131103 | 8.34e-05 |
| +0.0 | 0.02285665832 | 0.000141 |
| +0.3 | -0.0005238131103 | 8.34e-05 |
| +0.6 | -0.03557017332 | 0.000207 |

The physical branch passes the angular-power, Gauss-order, real-sheet and
identical-scalar-evenness gates.  Its contribution to the local-shape
coefficient has standard error `7.32786e-05`.

## What this changes

Replacing only the five physical `epsilon` rows leaves the crossed rows
untouched.  The hybrid local coefficient is

```text
a_hhh = -173.329279771
        + i 16.0531136937,
SE_real = 102.952,
SE_imag = 32.8284.
```

The crossed contribution alone has local-shape standard error
`102.952`.  It dominates the physical error
by orders of magnitude.  The candidate `K_mu` remains
`740.94152 + i -128.42491`
with real/imaginary errors
`824/263`.
It is therefore **not a coefficient measurement**.

## Cog criterion

The governing MTS requirement is now explicit.  The same parent dynamics must
leave the successful local GR/Newton cogs—Mercury, clocks, local lensing and
laboratory gravity—turning as before, while deriving a controlled activation
that supplies the missing galactic response.  No manual regime switch or
equation retuning is permitted.  This calculation supports that discipline:
the ordinary physical branch is controlled, while the unclosed crossed
analytic continuation is isolated instead of being absorbed into a coupling.

## Decision

- Physical real-sheet `hhh` finite cut at the five audit angles: **controlled smoke**.
- Exact endpoint and normalization: **source locked**.
- Old physical `epsilon` extrapolation as coefficient evidence: **replaced**.
- Crossed finite-`x` upper-boundary values: **still variance dominant**.
- Numeric UV coefficient, source coupling, local GR/Newton and full MTS: **not claimed**.

Next: combine the three crossed channel terms at the finite-`x` integrand and
residue level before outer averaging.  The aim is cancellation-before-sampling,
not another independent control bank or deletion of the large events.
