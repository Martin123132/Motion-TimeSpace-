# 3186 - Source-Owned PH Amplitude Or Slip Transfer Bound Under AX1090

Private checkpoint. This is not a local-GR claim, Newtonian-limit claim, PPN pass, solar-J2 pass, clock pass, orbital pass, or public-facing result.

## Result

3185 explained the `chi_H` scale:

```text
chi_H = 2 C_K2_unit / 25.
```

3186 turns that into the actual source-amplitude fork.

With:

```text
Sigma_H = chi_H P_H,
P_H := s_K2 kappa_STF c_ext,
```

the current slip pressure bound becomes:

```text
|P_H| <= A_metric_bound / (2 chi_H).
```

But because:

```text
chi_H = 2 C_K2_unit / 25,
```

this is:

```text
|P_H| <= (25/4) A_metric_bound / C_K2_unit.
```

That is exactly the 3180 scalar recast bound.

## What This Means

The local branch is not facing an extra hidden penalty from the slip readout, provided the 3177/3180/3183 normalizations are the same public `P2` normalization.

The tightest current pressure allows:

```text
|P_H| <= 3.898004369090586e10
```

on the half-range proxy row.

If:

```text
P_H ~ 1,
```

then:

```text
A_slip = 2 chi_H = 5.750026171972743e-25,
```

which is far below the current pressure proxy.

So the true question is no longer:

```text
how can chi_H be tiny?
```

It is:

```text
what is P_H?
```

## Source-Owner Gaps

The product:

```text
P_H = s_K2 kappa_STF c_ext
```

is still not source-owned.

The live missing pieces are:

- `s_K2`: signed basis/magnitude from parent boundary basis;
- `kappa_STF`: coupling/source-moment coefficient from parent variation;
- `c_ext`: exterior coefficient from compact source profile and matching layer;
- `DeltaK_TF`: tensor leakage beyond scalar `D2`;
- transfer: accepted PPN/orbital/light-time map, not just pressure proxy.

## Decision

3186 improves the status:

```text
the scary chi_H factor is explained,
and order-one P_H would be locally safe under current pressure.
```

But no claim is made, because `P_H` could be much larger than order one unless the source profile is derived.

Next target:

```text
3187-Y5-R2FR-kappaSTF-cExt-source-profile-estimator-or-parent-zero-under-AX1090
```
