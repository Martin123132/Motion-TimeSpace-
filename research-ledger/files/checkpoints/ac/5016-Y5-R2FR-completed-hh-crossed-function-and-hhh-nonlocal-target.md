# 5016 — completed hh crossed function and hhh nonlocal target

## Result

The exact checkpoint-5008 two-particle tower has now been reconstructed as an angular integral rather than analytically continuing a divergent Legendre series. The sourced four-point KLT tree supplies the spin-four phase, while the completed regular kernel is

```text
K(c)=[H(x)-H_soft(x)]/[x^2(1-x)^2],  x=(1-c)/2.
```

At physical angles the direct integral is checked against the exact `J<=40` tower. The same `z-i0` sheet derived in checkpoint 5015 then gives the crossed values.

| z | Re cyclic D_hh/G^3 | RQMC error |
|---:|---:|---:|
| -0.6 | 97.258267 | 36 |
| -0.3 | 68.915344 | 71 |
| 0 | 30.461346 | 53 |
| 0.3 | 68.915181 | 71 |
| 0.6 | 97.24277 | 36 |

## Coupled target

The known real master before `hhh` is now an actual function:

```text
M_known=2(C_phi+C_hh+C_pph)+(203/10)F1.
```

The last sign follows from `D1 ReF1=-(203/10)F1`. Removing the best local `c(1-z^2)` component leaves a nonlocal residual. Since `hhh` enters as `2 C_hhh`, its required nonlocal component is exactly minus one half of that residual on the sampled grid.

| z | known master without hhh | required hhh nonlocal D/G^3 |
|---:|---:|---:|
| -0.6 | 202.28514 | -45.174924 |
| -0.3 | 150.35956 | 4.3992132 |
| 0 | 75.486282 | 49.706304 |
| 0.3 | 150.22226 | 4.4678647 |
| 0.6 | 202.13339 | -45.099052 |

This is not the rejected checkpoint-5013 mode-by-mode target. It is a crossing-complete functional target, defined only modulo the genuinely local `stu` coefficient.

## Status

- Four-point KLT phase and completed hard kernel: **inserted and checked**.
- Direct `hh` integral versus exact tower: **executed**.
- Crossed `hh` function: **constructed without Legendre continuation**.
- Known master nonlocal residual and `hhh` target: **derived**.
- Independent graph-complete `hhh` crossed calculation: **next active calculation**.
- Combined locality, numeric `K_mu/K_ang`, exact local GR, and full MTS: **not claimed**.

Next: evaluate the graph-complete five-point KLT `hhh` plus distribution at these same direct and crossed angles, and compare its nonlocal component with the target above before fitting any local coefficient.
