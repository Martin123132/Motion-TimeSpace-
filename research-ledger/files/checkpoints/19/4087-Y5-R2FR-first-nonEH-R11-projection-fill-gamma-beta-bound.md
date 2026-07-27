# 4087 - First Non-EH R11 Projection Fill Gamma Beta Bound

- Timestamp: `2026-07-02T04:06:13+00:00`
- Status: `private_nonclaim_checkpoint`
- Decision: `FIRST_R11_R2_SCALAR_MODE_BOUND_FILLED_GAMMA_EXACT_BETA_ASYMPTOTIC_LOCAL_GR_STILL_NONCLAIM`
- Public local-GR/R11 pass claim: `false`
- GitHub action: `false`

## Result

4087 fills the first live non-EH/R11 family instead of merely pointing at it.

Selected family:

```text
R2_fR_scalar_mode
f(R) subset: f(R)=R+mu R^2
m_R^2 = 1/(6 mu)
lambda_R = 1/m_R
```

The scalar mode is allowed only if it is absent, parent double-zeroed, or short-ranged enough.

## Gamma Derivation

For the standard metric `f(R)` scalar normalization:

```text
y = exp(-b/lambda_R)
gamma_R2(b) = (3-y)/(3+y)
|gamma-1| = 2y/(3+y)
```

Using the 4085 Cassini bound:

```text
B_gamma = 2.300000e-05
y <= 3 B_gamma/(2-B_gamma) = 3.450040e-05
b/lambda_R >= 10.274540
```

With Cassini closest approach `b = 1.6 R_sun`:

```text
lambda_R <= 1.557247e-01 R_sun
lambda_R <= 7.241928e-04 AU
```

## Beta Derivation

The available quadratic-gravity 2PN result gives, in the scalar/f(R) limit:

```text
G_eff^2 beta - 1
  ~= (1/3) x exp(-x) ln(2x)
    + ((9 gamma_E - 4)/27) x exp(-x)

G_eff = 1 + exp(-x)/3
x = b/lambda_R
```

Solving against the 4085 beta bound:

```text
B_beta = 8.000000e-05
b/lambda_R >= 11.960837
lambda_R <= 1.337699e-01 R_sun
lambda_R <= 6.220925e-04 AU
```

In this template the beta asymptotic bound is stricter than the gamma-only bound.

## Combined Bound

```text
b/lambda_R >= 11.960837
lambda_R <= 1.337699e-01 R_sun
lambda_R <= 9.306372e+07 m
lambda_R <= 6.220925e-04 AU
m_R >= 1.607478e+03 AU^-1
mu <= 1.443476e+15 m^2
```

Interpretation:

```text
long-range R2/f(R) scalar -> local GR fails
short-range enough scalar -> may survive this one family gate
parent double-zero/absence -> cleaner than bounding
```

## What This Does Not Claim

This is not an MTS local-GR pass. It is a filled bound template for one non-EH family under standard `f(R)=R+mu R^2` normalization.

To promote it, MTS must either:

```text
map c_R2 to mu and prove the bound
or prove C_i(X0)=0, dC_i(X0)=0, mass-gap, and readout silence
```

## Decision

```text
first R11 family bound = filled
gamma condition = exact for standard f(R) scalar Yukawa
beta condition = asymptotic 2PN bound template
local GR claim = still false
next = map actual MTS c_R2 or fill Ricci/Weyl spin-2 slip projection
```

## Sources

- Chiba, Smith and Erickcek, *Solar System constraints to general f(R) gravity*.
- Zhu and Li, *Parameterized post-Newtonian analysis of quadratic gravity and solar system constraints*.
- 4085 PPN bound table and 4086 non-EH projection formulas.

## Next

```text
4088-Y5-R2FR-map-MTS-cR2-normalization-or-Ricci-Weyl-spin2-slip-bound.md
```
