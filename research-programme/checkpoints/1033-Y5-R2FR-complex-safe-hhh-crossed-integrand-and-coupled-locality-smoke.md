# 5017 — complex-safe hhh crossed integrand and coupled locality smoke

## Exact implementation gain

The sourced five-point KLT sum is now reimplemented with complex Mandelstam invariants throughout. The previous physical implementation converted the momentum kernel to `float(real)` and therefore could not legally be used on the crossed sheets. At a physical point the new kernel agrees with checkpoint 5010 to relative residual `0.000e+00`; its exact soft coefficient agrees to `0.000e+00`.

For every phase-space point the code evaluates the correlated cyclic combination

```text
C_hhh(z)=D_hhh(z)+[-(1-z)/2]^3 D_hhh((3+z)/(1-z))
                   +[-(1+z)/2]^3 D_hhh(-(3-z)/(1+z)).
```

No direct-channel Legendre continuation and no fitted cancellation coefficient is used.

| z | Re C_hhh/G^3 | RQMC error | Im C_hhh/G^3 |
|---:|---:|---:|---:|
| -0.6 | -1.5922422 | 0.48 | 0.431 |
| -0.3 | -3.0506859 | 0.22 | -0.488 |
| 0 | -3.6320624 | 0.31 | 1.84e-10 |
| 0.3 | -3.0506559 | 0.22 | 0.488 |
| 0.6 | -1.5922108 | 0.48 | -0.431 |

## First full coupled smoke

The scalar, completed `hh`, graph-complete `phi phi h`, complex-safe `hhh`, and sourced `D1 ReF1` pieces are now present in one crossing-complete numerical object:

```text
M_full=2(C_phi+C_hh+C_phiphih+C_hhh)+(203/10)F1.
```

After removing the best local `c(1-z^2)` component:

| z | full smoke master | nonlocal residual | combined RQMC error |
|---:|---:|---:|---:|
| -0.6 | 199.10065 | 91.298582 | 72 |
| -0.3 | 144.25819 | -9.0228784 | 1.4e+02 |
| 0 | 68.222158 | -100.21858 | 1.1e+02 |
| 0.3 | 144.12095 | -9.1601215 | 1.4e+02 |
| 0.6 | 198.94897 | 91.146901 | 72 |

The maximum residual significance is `1.26` sigma. This is a smoke diagnostic, not a locality verdict: checkpoint 5016's isolated crossed `hh` estimator still has large variance, and the crossed-sheet pole prescription has not yet been stabilized analytically.

## Status

- Complex-safe graph-complete `2phi+3h` KLT kernel: **implemented and physically cross-checked**.
- Exact `hhh` soft coefficient and plus integrand: **cross-checked against checkpoint 5010**.
- Correlated full cyclic `hhh` estimator: **executed**.
- First all-sector crossing-complete locality smoke: **executed**.
- Precision crossing locality, numeric UV coefficient, local GR, and full MTS: **not claimed**.

Next: stabilize the common crossed-sheet prescription at the integrand level, preferably by combining the `hh` hard term with the `hhh` soft sector before numerical integration, then rerun the same full-master residual without changing its normalization.
