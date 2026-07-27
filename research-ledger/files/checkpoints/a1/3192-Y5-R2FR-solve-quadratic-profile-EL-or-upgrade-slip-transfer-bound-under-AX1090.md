# 3192 - Solve Quadratic Profile EL Or Upgrade Slip Transfer Bound Under AX1090

Private checkpoint. This is not a local-GR claim, Newtonian-limit claim, PPN pass, solar-J2 pass, clock pass, orbital pass, or public-facing result.

## Result

This checkpoint does not just record a missing parent input. It solves the toy quadratic profile equation introduced in 3191.

For:

```text
J[F] = integral x^4 (D2[F])^2 dx
```

with:

```text
D2[F]=(2/5)F''+2F'/x+6F/(5x^2),
```

the Euler-Lagrange equation is:

```text
D2^dagger[x^4D2[F]]=0,
```

where:

```text
D2^dagger[u]=(2/5)u''-(2u/x)'+6u/(5x^2).
```

For a power law:

```text
D2^dagger[x^4D2[x^p]]=(4/25)p(p-2)(p+1)(p+3)x^p.
```

So the exact interior stationary transition family is:

```text
F_EL(x)=A+B x^2+C/x+D/x^3.
```

The constants are fixed by matching `F` and `F'` to:

```text
F=x^2 at x=1-w,
F=x^-3 at x=1+w.
```

## What Changed

The previous smoothstep profile was useful, but it was not a stationary profile of the quadratic toy parent functional.

At the 3190 selected width:

```text
w = 0.435
```

the smoothstep row has:

```text
N4_D2 = 3.392613563564943,
trimmed EL residual L2 = 420.6894109506566.
```

The exact interior EL profile at the same width has:

```text
N4_D2 = 1.174307819436789,
improvement factor = 2.889032592146136.
```

So the pressure/source envelope improves materially:

```text
|P_H| <= 1.467884774295986 |s_K2 kappa_STF|
```

instead of:

```text
|P_H| <= 4.240766954456179 |s_K2 kappa_STF|.
```

## Boundary Gate

The catch is not the interior equation. The catch is regularity at the joins.

The same-width exact EL row keeps a finite but nonzero curvature jump:

```text
max |Delta F''| = 5.519741898178943.
```

The best balanced jump row in the scan is:

```text
w = 0.623,
N4_D2 = 1.093472635691388,
max |Delta F''| = 1.567214003023483.
```

The minimum-`N4_D2` row pushes the transition very wide:

```text
w = 0.950,
N4_D2 = 0.9696291000650621,
max |Delta F''| = 413.2059465989288.
```

That is not acceptable as a clean local-GR proof unless a parent boundary condition or boundary layer makes the jump physical.

## Decision

This is genuine progress.

The profile problem is now narrowed to:

```text
interior profile solved,
boundary regularity not solved.
```

The next derivation target is:

```text
3193-Y5-R2FR-parent-boundary-regularity-or-natural-boundary-layer-under-AX1090
```

## Generated Evidence

- `source-intake/mts_residuals/P8_Y5_R2FR_3192_INPUTS.csv`
- `source-intake/mts_residuals/P8_Y5_R2FR_3192_EL_OPERATOR_DERIVATION.csv`
- `source-intake/mts_residuals/P8_Y5_R2FR_3192_SMOOTHSTEP_EL_RESIDUAL_SCAN.csv`
- `source-intake/mts_residuals/P8_Y5_R2FR_3192_EL_STATIONARY_TRANSITION_SCAN.csv`
- `source-intake/mts_residuals/P8_Y5_R2FR_3192_EL_STATIONARY_SELECTION.csv`
- `source-intake/mts_residuals/P8_Y5_R2FR_3192_PROFILE_DECISION.csv`
- `source-intake/mts_residuals/P8_Y5_R2FR_3192_VALIDATION.csv`

Validation passed and all rows remain `valid_for_claim=false`.
