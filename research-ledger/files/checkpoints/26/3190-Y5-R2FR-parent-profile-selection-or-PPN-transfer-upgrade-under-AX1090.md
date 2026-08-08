# 3190 - Parent Profile Selection Or PPN Transfer Upgrade Under AX1090

Private checkpoint. This is not a local-GR claim, Newtonian-limit claim, PPN pass, solar-J2 pass, clock pass, orbital pass, or public-facing result.

## Result

3189 built live smooth source-profile rows.

3190 scans the transition width in the same `C2` smoothstep family:

```text
0.020 <= w <= 0.800.
```

The selection criterion is:

```text
minimize N4_D2
```

subject to:

```text
I4_D2 = -4/5,
c_ext = 1.
```

The nonclaim minimum in this family is:

```text
w = 0.435,
N4_D2 = 3.392613563564943.
```

## Coupling Margin

The tight current pressure condition is:

```text
|s_K2 kappa_STF| N4_D2 <= 1.949002184545292e11.
```

For the selected profile:

```text
|s_K2 kappa_STF| <= 5.744839923640726e10.
```

So the selected smooth profile is numerically comfortable for order-one coupling products, but still not parent-owned.

## Remaining Fork

This leaves two honest routes:

```text
derive the parent profile equation,
```

or:

```text
upgrade the pressure proxy to a real PPN/orbital/light-time transfer bound.
```

The min-`N4` profile is useful as a candidate, not a derivation.

## Decision

The best next target is:

```text
3191-Y5-R2FR-selected-profile-transfer-runner-or-parent-action-profile-equation-under-AX1090
```
