# 5021 — global-azimuth Feynman-contour nested hhh smoke

## Actual advance

The five-dimensional crossed integral is no longer sampled blindly across its pole. Write the two original azimuths as

```text
phi_global = phi_soft,
delta      = phi_decay-phi_soft.
```

The Jacobian is one. At fixed soft energy, two polar cosines and `delta`, the full internal three-body event is rotated through `phi_global`. The complex-safe KLT product is then integrated deterministically around that complete azimuth before any Sobol averaging. For crossed `q`, the code evaluates the ordinary unit circle at `q+i epsilon`; the pole is displaced by the Feynman boundary value instead of being hit by real-sphere QMC.

The periodic trapezoid at `64` and `128` nodes agrees at the fixed crossed controls to maximum residual `6.577e+00`. The same nested contour reproduces the independently derived checkpoint-5019 soft endpoint on both a physical point and `q=3+0.08i`; its maximum relative residual is `0.992`.

## First finite-x boundary smoke

The remaining four variables are integrated with `4` scrambled Sobol seeds and `2^5` points per seed. Four upper-boundary epsilon values are extrapolated independently per seed. A linear-quadratic intercept is compared with an even-polynomial intercept; their difference remains a continuation-model systematic. The maximum relative model systematic is `4.97`.

| physical z | corrected cyclic hhh | nonlocal part | required 5018 target | smoke error |
|---:|---:|---:|---:|---:|
| -0.6 | -8.671621 | -4.29961 | 28.71095 | 40 |
| -0.3 | -3.925392 | 2.291061 | -9.009423 | 1 |
| +0.0 | -5.497497 | 1.33377 | -20.45383 | 0.73 |
| +0.3 | -3.925392 | 2.291061 | -8.940934 | 1 |
| +0.6 | -8.671621 | -4.29961 | 28.77132 | 40 |

The corrected nonlocal vector has correlation `-0.950363` with the independently constructed target and relative L2 mismatch `1.142`. These are diagnostics, not a fit and not yet a locality verdict.

## Status

- Exact global-azimuth coordinate reduction: **implemented**.
- Crossed poles displaced with `q+i epsilon` before deterministic azimuth integration: **implemented**.
- Physical and crossed soft-endpoint check against the exact resolvent: **passed**.
- First finite-`x`, all-crossed-argument hhh boundary smoke: **executed**.
- Precision epsilon limit and final coupled locality: **open**.
- Numeric UV invariant, local GR and full MTS: **not claimed**.

Next: increase the remaining-variable power, add one smaller epsilon with adaptive azimuth nodes, and require the extrapolated cyclic nonlocal vector to stabilize under both epsilon-window and `x0/x_floor` changes before a locality decision.
