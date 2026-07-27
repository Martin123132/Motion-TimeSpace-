# 3181 - Exterior Hessian Tidal Footprint Or Metric Null Bound Under AX1090

Private checkpoint. This is not a local-GR claim, Newtonian-limit claim, PPN pass, clock pass, orbital pass, or public-facing result.

## Result

3180 gave a conditional projected-moment win, but left the exterior tensor footprint open.

The exterior tracefree Hessian carrier is:

```text
phi_ext = C r^-3 P2(a.n).
```

Choose `a=z`, so:

```text
phi_ext = C(3z^2-r^2)/(2r^5).
```

For the projected 3179 operator:

```text
D2[F] = (2/5)F'' + 2F'/r + 6F/(5r^2),
```

the exterior branch does vanish:

```text
D2[C r^-3] = 0.
```

But the full Hessian does not vanish.

Since the exterior branch is harmonic:

```text
K_L^{ij} = 2 partial_i partial_j phi_ext,
delta_ij K_L^{ij} = 0.
```

The tensor norm is:

```text
K_L^{ij}K^L_ij
  = 18 C^2 r^-10 (45 mu^4 - 10 mu^2 + 13),
mu := cos(theta).
```

Therefore:

```text
<K_L:K_L>_Omega = 336 C^2 r^-10,
K_rms = 4 sqrt(21)|C| r^-5.
```

So the goblin verdict is blunt:

```text
D2 zero is not metric silence.
```

## STF Basis Projection

With:

```text
Y_a^{ij} = a^i a^j - delta^{ij}/3,
```

the constant STF-basis projection is:

```text
Y_a:K_L = 3C r^-5(35 mu^4 - 30 mu^2 + 3).
```

Its angular mean vanishes:

```text
<Y_a:K_L>_Omega = 0.
```

But its RMS does not:

```text
<P_Y[K_L]^2>_Omega = 144 C^2 r^-10.
```

That slice is:

```text
144/336 = 3/7
```

of the full angular norm. So a scalar projected-moment bound alone is not enough to control the full exterior tidal tensor.

## What This Means

This is a real derivation, not a missing-list loop.

The attractive branch:

```text
F = C r^-3 outside the source
```

does have:

```text
D2 = 0,
```

which explains why the 3180 projected source moment can close cleanly.

But local GR is not protected by that alone, because the exterior Hessian has a nonzero tensor footprint falling like:

```text
r^-5.
```

That is good news and bad news:

- good: the leak is sharply quantified;
- bad: it cannot be waved away by the projected `D2=0` result.

## Metric-Null Gate

To keep the tracefree Hessian route alive as a derived local-GR branch, one of these must be proven:

```text
delta g_public[K_L_ext] = 0,
```

or:

```text
K_L_ext is gauge/exact/improvement-silent in the parent action,
```

or:

```text
the public metric only reads the D2 scalar source and not the full tracefree exterior Hessian.
```

No such theorem is parent-signed yet.

## Bound Route

If metric-null fails, the bounded route must introduce a source-owned response coefficient:

```text
mu_tidal,
```

and an arena transfer bound:

```text
tau_tidal.
```

At normalized exterior radius `x=1`, the nonclaim template is:

```text
A_tidal_surface
  = 4 sqrt(21)|s_K2 kappa_STF c_ext mu_tidal|,
```

so:

```text
|s_K2 kappa_STF c_ext mu_tidal|
  <= tau_tidal/(4 sqrt(21)).
```

This is only a template until `mu_tidal`, `tau_tidal`, source geometry, and the arena transfer kernel are source-owned.

## Decision

3181 moves the work forward by replacing a vague leakage warning with an exact footprint:

```text
<K_L:K_L>_Omega = 336 C^2 r^-10.
```

The local-GR branch is not dead, but the next fork is strict:

```text
prove metric-null / improvement silence,
or derive a real tidal response bound.
```

Next target:

```text
3182-Y5-R2FR-metric-readout-of-tracefree-Hessian-carrier-or-tidal-response-coefficient-under-AX1090
```
