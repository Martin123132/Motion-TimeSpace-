# 3187 - kappaSTF cExt Source Profile Estimator Or Parent Zero Under AX1090

Private checkpoint. This is not a local-GR claim, Newtonian-limit claim, PPN pass, solar-J2 pass, clock pass, orbital pass, or public-facing result.

## Result

3186 made the live object:

```text
P_H = s_K2 kappa_STF c_ext.
```

3187 turns `c_ext` into a source-profile estimator.

From 3180:

```text
I4_D2 := integral_0^infty D2[F](x) x^4 dx = -4 c_ext/5.
```

Therefore:

```text
c_ext = -5 I4_D2/4.
```

So:

```text
P_H = -(5/4) s_K2 kappa_STF I4_D2.
```

This is the useful estimator. Once `s_K2 kappa_STF` and the projected source profile are parent-owned, `P_H` becomes computable.

## Absolute Envelope

For a conservative profile bound, define:

```text
N4_D2 := integral |D2[F](x)| x^4 dx.
```

Then:

```text
|P_H| <= (5/4)|s_K2 kappa_STF| N4_D2.
```

Given a pressure ceiling `B_PH`, the sufficient pass condition is:

```text
|s_K2 kappa_STF| N4_D2 <= (4/5) B_PH.
```

This is now an executable profile/coupling gate, not just a symbol list.

## Sharp Shell Calibration

For the normalized quadratic-core plus sharp-shell calibration:

```text
F_in = a2 x^2,
F_out = c_ext x^-3.
```

Value matching gives:

```text
c_ext = a2.
```

The signed projected source moment is:

```text
I4_D2 = 6a2/5 - 2a2 = -4a2/5.
```

The absolute projected-source norm is:

```text
N4_D2 = |6a2/5| + |2a2| = 16|a2|/5.
```

So the signed-to-absolute ratio is:

```text
1/4.
```

And:

```text
P_H = s_K2 kappa_STF a2.
```

## Margin Smoke

Using the current tightest pressure:

```text
|P_H| <= 2.436252730681616e11,
```

the illustrative source products behave as:

```text
P_H = 1      passes by ~2.4e11 margin,
P_H = 1e6   passes,
P_H = 1e9   passes,
P_H = 1e11  passes,
P_H = 1e12  fails the tight proxy.
```

This is not a claim, because `P_H` is not source-owned yet. But it tells us the scale of the next fight.

## Parent Zero Routes

The projected branch is zero if:

```text
s_K2 kappa_STF I4_D2 = 0.
```

The viable zero routes are:

- parent source symmetry kills the STF component;
- `c_ext=0`, equivalently `I4_D2=0`;
- parent variation gives `s_K2 kappa_STF=0`.

But:

```text
core/shell cancellation cannot hide a fixed nonzero c_ext,
```

because the boundary identity fixes:

```text
I4_D2 = -4c_ext/5.
```

## Decision

3187 gives the next working object:

```text
I4_D2 and N4_D2 of the parent source profile.
```

If the source profile is order-one in this normalized estimator, the local pressure problem is mild. If the source product is huge, it must be bounded or zeroed.

Next target:

```text
3188-Y5-R2FR-PH-source-profile-prior-grid-or-parent-coupling-zero-under-AX1090
```
