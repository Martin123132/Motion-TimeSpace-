# 5006 - Chi massless integrand identity and reduced-limit repair

**Checkpoint marker:** `MTS_5006_CHI_MASSLESS_INTEGRAND_IDENTITY_AND_REDUCED_LIMIT_REPAIR`  
**Date:** 2026-07-14  
**Claim status:** private one-loop amplitude correction.

## Exact source comparison

The 5000 strict-four-dimensional covariant cut is pointwise identical to Chi's published two-helicity trace numerator. At each of five independent rational loop directions,

```text
N_5000 = (625/64) conjugate[N_Chi],
residual = 0.
```

The conjugation is only the opposite external-helicity phase convention. The normalization is global and fixed by the same box normalization already used in 5000.

## Correction to the old interpretation

The direct massless integrand reduces to

```text
A_s^hh(D=4) = (t + u)*(t**6 - t**5*u + t**4*u**2 - t**3*u**3 + t**2*u**4 - t*u**5 + u**6)/16.
```

Checkpoint 4991 instead set `M=0` in coefficients that had already been reduced in a basis containing both a massless triangle, a massive triangle, and massive boxes. It obtained

```text
A_s^hh(naive reduced M->0) = -(t + u)*(t**6 - t**5*u + t**4*u**2 - t**3*u**3 + t**2*u**4 - t*u**5 + u**6)/16.
```

Their difference is

```text
Delta_limit = (t + u)*(t**6 - t**5*u + t**4*u**2 - t**3*u**3 + t**2*u**4 - t*u**5 + u**6)/8.
```

Because the unintegrated massless cuts agree pointwise, this difference cannot be an FDH-versus-HV scheme effect at `D=4`. It is a non-commuting limit: the finite-mass master basis degenerates when `M->0`, and lower-topology pieces must be transformed before the limit is taken. The 4991 `strict massless FDH triangle` label and the 4999 `epsilon^0 scheme shift` label are therefore retired. The 5004 selected strict-D4 value is reinforced.

This also blocks a tempting shortcut: the finite-mass Chi ancillary cannot determine the massless rational remainder by direct substitution. `R_rat(t,u)` still requires factorization or a genuinely D-dimensional massless calculation.
