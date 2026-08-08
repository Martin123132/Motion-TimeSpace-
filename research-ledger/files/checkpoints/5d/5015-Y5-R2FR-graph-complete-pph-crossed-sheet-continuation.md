# 5015 — graph-complete pph crossed-sheet continuation

## Result

Checkpoint 5014 supplied a legal direct-channel object but locality requires its complete cyclic crossing. That continuation is now executable.

For real `|z|>1`, the two choices of

```text
p_out=(1, +/-sqrt(1-z^2), 0, z)
```

give complex-conjugate tree products. Their real part is therefore branch independent. The positive transverse square root matches the exact checkpoint-5012 endpoint evaluated on `z-i0`: `log(1-z)` takes `+i pi` for `z>1`, while `log(1+z)` takes `-i pi` for `z<-1`.

The continued direct function is combined as

```text
C_pph(z)=d(z)+[-(1-z)/2]^3 d((3+z)/(1-z))
               +[-(1+z)/2]^3 d(-(3-z)/(1+z)).
```

| z | Re cyclic D_pph/G^3 | RQMC error | Im diagnostic |
|---:|---:|---:|---:|
| -0.6 | -4.2435295 | 0.26 | 7.82 |
| -0.3 | -5.1022709 | 0.037 | 5.78 |
| 0 | -5.1427831 | 0.31 | 3.31e-13 |
| 0.3 | -5.1707595 | 0.049 | -5.78 |
| 0.6 | -4.3039036 | 0.26 | -7.82 |

The `pph` sector alone does not fit `c(1-z^2)`; the maximum residual is `0.627946`. That is expected and is retained rather than subtracted or tuned: locality is a condition on `hh+hhh+pph+D1`, not on `pph` by itself.

## Status

- Crossed-sheet branch pair and real-part prescription: **derived and checked**.
- Exact complex soft endpoint on the same sheet: **inserted**.
- Direct and cyclic graph-complete `pph` functions: **computed**.
- `pph`-only nonlocal component: **measured and retained for coupled cancellation**.
- Completed `hh` and graph-complete `hhh` crossed functions: **next active calculation**.
- Combined locality, numeric `K_mu/K_ang`, exact local GR, and full MTS: **not claimed**.

Next: reconstruct the completed checkpoint-5008 `hh` cut as a crossed function in this same `z-i0` convention, then add `hhh` before applying any local projection.
