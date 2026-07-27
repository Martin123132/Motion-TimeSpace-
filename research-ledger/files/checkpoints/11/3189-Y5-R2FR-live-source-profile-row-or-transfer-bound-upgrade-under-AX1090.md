# 3189 - Live Source Profile Row Or Transfer Bound Upgrade Under AX1090

Private checkpoint. This is not a local-GR claim, Newtonian-limit claim, PPN pass, solar-J2 pass, clock pass, orbital pass, or public-facing result.

## Result

3189 replaces the sharp shell idealization with finite smooth source profiles.

Use a `C2` smoothstep transition:

```text
F = x^2                         for x <= 1-w,
F = (1-S)x^2 + S x^-3            for 1-w < x < 1+w,
F = x^-3                        for x >= 1+w,
S(t)=6t^5-15t^4+10t^3.
```

The tested widths are:

```text
w = 0.02, 0.05, 0.10, 0.20, 0.40, 0.70.
```

All preserve the boundary identity:

```text
I4_D2 = -4/5,
c_ext = 1.
```

The absolute profile norms land in the range:

```text
N4_D2 ≈ 3.40 to 4.46.
```

## Margin

The tight current pressure condition is:

```text
|s_K2 kappa_STF| N4_D2 <= 1.949002184545292e11.
```

For the smooth profiles above, this means:

```text
|s_K2 kappa_STF| ~ 1      passes easily,
|s_K2 kappa_STF| ~ 1e9    passes,
|s_K2 kappa_STF| ~ 1e12   fails the tight proxy.
```

So the branch is not numerically fragile for order-one to large-but-not-astronomical coupling products. It only gets into trouble for enormous coupling/profile products or a much tighter future transfer bound.

## Still Missing

This does not prove local GR.

The remaining gates are:

- parent action must select/derive the profile width or profile class;
- `s_K2 kappa_STF` must be source-owned;
- tensor leakage beyond the scalar projected profile must remain bounded/null;
- the current bound is still a public `P2` pressure proxy, not a full PPN/orbital covariance transfer.

## Decision

This is a useful concrete step:

```text
we now have live smooth source-profile rows with finite N4_D2.
```

Next target:

```text
3190-Y5-R2FR-parent-profile-selection-or-PPN-transfer-upgrade-under-AX1090
```
