# 3130 - Binding Boundary Suppression or Profile Fill under AX1090

Private checkpoint. This follows 3129 by attacking the surface/binding source pressure channel directly.

## Problem

3129 found:

```text
Q_surface_binding_Earth = -0.01211918219995745
```

with:

```text
|Q_surface_binding_Earth delta_J| = 8.526876722826009e-15.
```

The current WEP-set `DeltaC` threshold is:

```text
0.003979617773650001.
```

So the raw surface/binding coefficient is too large unless it is:

```text
boundary-common-mode zero,
calibrated,
profile-weighted down,
or projected silent.
```

## Boundary Exactness Route

If the surface/binding term is an exact boundary partition term:

```text
C_surf[B] = integral_{partial W_B} B_surf,
```

and source plus calibration use the same fixed Hilbert-stress worldtube functional, then:

```text
C_surf[S] - C_surf[cal] = 0
```

for the common mode. This would give:

```text
DeltaC_Scal,surf = 0.
```

That is the clean route to local GR/Newton source recovery for this channel. It is not currently signed because the same-boundary/common-worldtube/calibration theorem is missing.

## Finite Suppression Bound

If the surface/binding channel survives with residual factor `rho_surf`, then:

```text
DeltaC_Scal,surf = rho_surf Q_surface_binding_Earth.
```

To fit under the current WEP-set threshold:

```text
|rho_surf| <= 0.3283734585378189.
```

Equivalently, the source/calibration/profile construction must suppress at least:

```text
1 - 0.3283734585378189 = 0.6716265414621811.
```

This is the exact cap. It is not absurdly tiny, but it is definitely not something we can hand-wave.

## L1 Envelope

For the no-cancellation bulk L1 envelope:

```text
Q_bulk_abs_L1 = 0.013810442886708322.
```

The required residual factor is:

```text
|rho_L1| <= 0.2881600399274763.
```

This is a hazard envelope, not a prediction.

## Profile Guard

3130 preserves the 2125 refusal:

```text
bulk Earth vector != MICROSCOPE/orbit/profile/worldtube source vector.
```

So no source-GM, WEP, PPN, or local-GR claim follows from the bulk numbers.

## Status

All rows remain:

```text
claim_allowed = false.
```

The surface/binding branch has now been reduced to a precise fork:

```text
prove boundary exactness/common-worldtube cancellation,
```

or:

```text
derive a profile/calibration residual factor rho_surf <= 0.3283734585378189.
```

## Runner Artifacts

| artifact | path |
|---|---|
| input rows | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3130_BINDING_BOUNDARY_SUPPRESSION_INPUTS.csv` |
| output rows | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3130_BINDING_BOUNDARY_SUPPRESSION_OUTPUT.csv` |
| validation | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3130_VALIDATION.csv` |
| gate | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3130_BINDING_BOUNDARY_SUPPRESSION_GATE.csv` |
| runner | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\scripts\Y5_R2FR_3130_binding_boundary_suppression.py` |

## Next Target

3131 should attempt the zero route first:

```text
surface/binding term is boundary-exact and same-worldtube calibrated
=> rho_surf = 0.
```

If that fails, fill a real profile/worldtube `rho_surf` row and test whether it lands below:

```text
0.3283734585378189.
```
