# 3172 — Public Metric Radial Green Owner Or J2 Channel Closure Under AX1090

Private checkpoint. This is not a public claim, not a local-GR pass, and not a solar-system bound result.

## Result

The exterior public `r^-3` quadrupole radial profile can be derived cleanly, but only inside the already-public weak-field/Laplace channel.

That closes one mathematical clause conditionally:

```text
if an MTS residual is already proven to enter the exterior public l=2 metric potential,
then asymptotic flatness forces the exterior radial profile to be r^-3.
```

It does not close the MTS coupling/projection clause:

```text
K_2 C_K2_unit != A_metric_solar_surface
```

until the parent exterior operator and public metric projection are signed.

## Public Green Derivation

For a source-free exterior scalar/public weak-field quadrupole channel, assume:

```text
nabla^2[f_l(r) P_l(cos theta)] = 0.
```

Separating variables gives:

```text
r^2 f_l'' + 2 r f_l' - l(l+1) f_l = 0.
```

The power-law solutions are:

```text
f_l(r) = a r^l + b r^(-l-1).
```

For `l=2`:

```text
f_2(r) = a r^2 + b r^-3.
```

For an isolated solar-system exterior field, asymptotic flatness removes the growing branch:

```text
a = 0,
f_2(r) = b r^-3.
```

So, if an already-owned public surface metric amplitude exists,

```text
A_metric(r) = A_surface (R_s/r)^3.
```

## What This Actually Buys

This is useful because 3171 listed the exterior radial Green profile as one of the missing owner clauses. The profile itself is no longer mysterious in the public channel.

But this is not enough to score MTS against solar J2, Shapiro, PPN, clocks, or orbital tests. The hard missing object is now sharper:

```text
Upsilon_J2 = Pi_J2_metric * T_source * G_ext_l2_surface.
```

Where:

```text
Pi_J2_metric
```

is the parent-to-public metric projection;

```text
T_source
```

is the source-domain transfer/universality map;

```text
G_ext_l2_surface
```

is the exterior radial Green normalization, equal to `1` only if the amplitude is already defined at the solar surface.

## Guardrail

Do not set:

```text
Pi_J2_metric = 1
```

or:

```text
T_source = 1
```

by convenience. Those are parent-owned claims, not harmless conventions.

Therefore the correct current contract remains:

```text
A_metric_solar_surface
= Upsilon_J2 K_2 C_K2_unit.
```

and:

```text
J2_eff
= Upsilon_J2 K_2 C_K2_unit / (2 epsilon_sun_surface).
```

The 3170 half-range pressure row becomes:

```text
K_2 <= 3.898004369090586e10 / |Upsilon_J2|.
```

No direct score is allowed while `Upsilon_J2` is missing.

## Channel Status

| Clause | Status | Meaning |
| --- | --- | --- |
| Exterior public `r^-3` profile | conditional math pass | public Laplace/weak-field channel gives it |
| Parent exterior operator match | missing | need MTS linearized exterior equation |
| `Pi_J2_metric` | missing | need map from residual to public metric perturbation |
| `T_source` | missing | need solar-source transfer or universality theorem |
| `Upsilon_J2` | missing | composite transfer kernel not owned |
| Direct J2/PPN scoring | blocked | no local-GR claim |

## Decision

The J2 route is not dead, but the bottleneck is no longer the radial profile. The bottleneck is the coupling/projection:

```text
does the parent MTS residual actually enter the exterior public l=2 metric channel?
```

Next target:

```text
3173-Y5-R2FR-parent-exterior-operator-match-or-PiJ2metric-source-row-under-AX1090.
```

Try derivation first. If it fails, build a source-ready nonclaim row for `Pi_J2_metric`/`T_source` rather than pretending the channel is closed.

## Generated Artifacts

```text
source-intake/mts_residuals/P8_Y5_R2FR_3172_INPUTS.csv
source-intake/mts_residuals/P8_Y5_R2FR_3172_GREEN_OWNER_ATTEMPT.csv
source-intake/mts_residuals/P8_Y5_R2FR_3172_CHANNEL_STATUS.csv
source-intake/mts_residuals/P8_Y5_R2FR_3172_CLOSURE_CONTRACT.csv
source-intake/mts_residuals/P8_Y5_R2FR_3172_DECISION.csv
source-intake/mts_residuals/P8_Y5_R2FR_3172_VALIDATION.csv
```
