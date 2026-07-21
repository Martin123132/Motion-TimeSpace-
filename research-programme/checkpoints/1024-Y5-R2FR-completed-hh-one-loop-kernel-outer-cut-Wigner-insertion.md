# 5008 - Completed hh one-loop kernel outer-cut Wigner insertion

**Checkpoint marker:** `MTS_5008_COMPLETED_HH_KERNEL_OUTER_CUT_WIGNER_INSERTION`  
**Date:** 2026-07-14  
**Claim status:** private amplitude derivation; not a full-MTS, local-GR, or complete two-loop claim.

## What is now inserted

Checkpoint 5007 proved that the finite rational remainder of the minimal massless Einstein-scalar opposite-helicity one-loop amplitude is zero. The 5005 hard kernel is therefore no longer a representative: it is the completed one-loop kernel for this declared sector. In the physical `s=1`, `t=-x`, `u=x-1` channel, its endpoint data are

```text
H(0)=H(1)=pi^2/16,
H'(0)=-5 pi^2/16,
H'(1)=+5 pi^2/16.
```

The unique crossing-even quadratic matching those four endpoint data is

```text
H_soft(x) = (pi^2/16)[1-5x(1-x)].
```

This is uniqueness only inside the minimal quadratic endpoint-subtraction class. Terms of order `x^2(1-x)^2` are integrable finite reallocations and are not silently declared absent. With `H_reg=H-H_soft`,

```text
lim_(x->0,1) H_reg/[x^2(1-x)^2] = 7 pi^2/16.
```

Thus both double and simple endpoint jets are removed, while crossing is preserved exactly.

## Exact helicity tower

For an external scalar pair and an intermediate `h+ h-` pair, the direct channel uses

```text
d^J_{0,4}(1-2x) = sqrt((J-4)!/(J+4)!) P_J^4(1-2x),  J>=4.
```

The tree partial wave is not merely tabulated. Four integrations by parts give

```text
a_J = 12 sqrt((J-4)!/(J+4)!)  for even J>=4,
a_J = 0                         for odd J.
```

The boundary term gives `48[1+(-1)^J]`; the remaining degree-two bulk polynomial is orthogonal to `P_J` for `J>=4`. Every hard coefficient is then evaluated exactly from beta-function derivatives for `1`, `log x`, `log(1-x)`, their squares, and their product. The generator is exact for arbitrary requested even `J`; this checkpoint materializes `J=4,...,40`.

The first five products `a_J h_J^reg` are

```text
J=4  : (1279249 + 3332000 pi^2)/526848000
J=6  : (3989437 + 28106400 pi^2)/71124480000
J=8  : (4675265713 + 57501813600 pi^2)/852000145920000
J=10 : (39809226503 + 736900164000 pi^2)/41596540457472000
J=12 : (499769479399 + 12825154742400 pi^2)/2139250652098560000
```

## Direct-cut normalization

Using `M1_hh M0*=kappa^6 F/(4stu)`, `kappa^2=32piG`, the restored one-loop factor `(4pi)^-2`, two-body phase space, the identical-state factor, both opposite-helicity assignments, and both one-loop placements gives

```text
D_hh,s^reg(z)
 = -(64/pi) sum_(J even>=4) (2J+1) a_J h_J^reg P_J(z).
```

The factor is exactly twice the already normalized scalar-cut factor `-32/pi`, as required by the two opposite-helicity assignments. Through `J=40`, the weighted partial sum is `0.6532457290649558` and the reduced-cut coefficient is `-13.30781271479766`. The last-pair falloff and tail estimate in the JSON are convergence diagnostics, not rigorous bounds.

## Why the full UV number is not yet legal

The direct hh channel has no `J=0` or `J=2` support. Crossing does not make it disappear: crossing a mode with `J>=4` produces rational channel denominators. For example, the `J=4` and `J=6` crossing sums are non-polynomial even though the full sums are crossing symmetric. Splitting each into a polynomial quotient and remainder is not crossing covariant.

Therefore an hh-only local UV projection is not well-defined. Those nonlocal pieces must be combined with the mixed `hhh` and `phi-phi-h` three-particle cuts before the local `J=0,2` projector is applied. This is a derived coupling requirement, not another unspecified missing-input ledger.

## Result

- Completed one-loop opposite-helicity kernel inserted into the outer two-particle cut: **yes**.
- Minimal endpoint jets and exact helicity tower: **closed**.
- Direct hh normalization: **closed as `-64/pi`**.
- Crossing-complete hh-only local UV subtotal: **forbidden as a standalone object**.
- Full outer cut: **open only on the coupled three-particle completion and final local projection**.

Next: derive the mixed `hhh` and `phi-phi-h` cut integrands in this normalization, combine all three cut classes before any polynomial projection, and test exact cancellation of the crossed nonlocal denominators.
