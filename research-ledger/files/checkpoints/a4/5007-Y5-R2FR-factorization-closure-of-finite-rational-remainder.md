# 5007 - Factorization closure of the finite rational remainder

**Checkpoint marker:** `MTS_5007_FACTORIZATION_CLOSURE_OF_FINITE_RATIONAL_REMAINDER`  
**Date:** 2026-07-14  
**Claim status:** private amplitude theorem for the minimal massless Einstein-scalar opposite-helicity channel; not a local-GR or full-MTS claim.

## Result

Checkpoint 5006 proves that the strict massless covariant cut is pointwise the published Chi cut. Checkpoint 5005 then leaves one finite cut-free object, `R_rat(t,u)`. This checkpoint closes it:

```text
R_rat(t,u) = 0.
```

This is not the choice of a minimal representative. It follows from the complete rational factorization basis at this order.

## Three-point obstruction

For a square-bracket three-point monomial `[12]^a [23]^b [31]^c`, little-group covariance fixes all three exponents. For `(phi,phi,h+)` it gives

```text
(a,b,c) = ('-2', '2', '2'),  spinor dimension = 2.
```

The tree coupling is `kappa` and needs dimension two, so this is the ordinary minimal vertex. A one-loop three-point vertex carries `kappa^3` and needs dimension four. The only possible extra dimension-two Lorentz scalar is a three-point Mandelstam invariant, and all such invariants vanish. Therefore the on-shell `phi-phi-h` one-loop vertex is zero.

The mixed-helicity `h+h-h` or `h-h+h` vertex has the same dimension-two result and its one-loop correction vanishes for the same reason. The exceptional all-plus graviton monomial instead has dimension 6; at `kappa^3` it requires an inverse `K^2`. This is precisely the sourced nonstandard one-loop all-plus vertex. It cannot occur here because the only all-graviton factorization side contains the external `h+` and `h-` pair.

## Four-point rational basis

Write the rational amplitude as

```text
M_rat/kappa^4 = Q^4 f(s,t,u),  [f] = mass_dimension_-4.
```

With only ordinary physical simple poles,

```text
f = a/(s t) + b/(s u) + c/(t u).
```

Crossing sets `a=b`, and `s+t+u=0` gives

```text
1/(s t) + 1/(s u) = -1/(t u).
```

Hence the entire ordinary-pole space is one-dimensional:

```text
M_rat/kappa^4 = C Q^4/(t u) = C t^3 u^3/Qbar^4,
Q Qbar = t u.
```

Its `t` and `u` residues require the one-loop `phi-phi-h` vertex just proved zero, so `C=0`. Double poles are absent because neither an all-plus graviton channel nor a singular scalar-graviton three-point vertex is available.

A pole-free remainder would have to be a local spinor polynomial. Opposite graviton helicities require at least `Q^4`, of spinor dimension eight, while a `kappa^4` four-point amplitude permits only dimension four. The sourced scalar-gravity basis independently places the first `C_L C_R phi^2 D^4` contact at operator dimension ten. No local remainder exists at this order.

## Consequence

The minimal massless Einstein-scalar opposite-helicity one-loop kernel is now complete in the normalization fixed by checkpoints 5004-5006: poles, finite logarithms, pi-squared terms, and the rational sector are all fixed. The next calculation is to insert this completed one-loop kernel into the outer cut rather than reopen its internal reduction.
