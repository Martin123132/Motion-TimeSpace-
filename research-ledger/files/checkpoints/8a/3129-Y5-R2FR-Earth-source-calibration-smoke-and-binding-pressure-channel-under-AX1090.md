# 3129 - Earth Source-Calibration Smoke and Binding Pressure Channel under AX1090

Private checkpoint. This follows 3128 by attempting a first finite source/calibration row from existing source-weight data, without pretending bulk Earth composition is a valid profile/worldtube source.

## Source-Cal Kernel

3128 identified the exact object:

```text
DeltaC_Scal = C_J,S^ADM - C_J,cal^ADM.
```

3129 tests the first existing finite source-side data:

```text
EPB2125_0_bulk_DD_context
```

from the source-weight archive. This row is explicitly nonclaim:

```text
bulk Earth vector is not shell/profile/worldtube weighted
parent-to-DD/readout maps remain missing
```

but it is still useful as a smoke pressure test.

## Calibration Zero Route

The clean route is:

```text
C_J,S^ADM and C_J,cal^ADM are the same common-mode Hilbert-stress functional
=> DeltaC_Scal = 0.
```

This would be excellent for local GR/Newton recovery, but it is not signed. The existing source descent rows keep relative source residuals live unless `NoSourceOnlySpeciesSlot`, source-label forgetting, and readout no-reentry are proved.

## Earth Bulk Smoke Result

Using the one-channel Coulomb convention from 3122:

```text
DeltaC_Earth,alpha = 2 Q_alpha_Coulomb_Earth.
```

The source archive gives:

```text
Q_alpha_Coulomb_Earth = 0.001691260686750872
```

so:

```text
DeltaC_Earth,alpha = 0.003382521373501744.
```

With the current strict nonclaim envelope:

```text
|delta_J| <= 7.035851579866459e-13
```

this gives:

```text
|DeltaC_Earth,alpha delta_J| = 2.379891834968431e-15.
```

That is below the WEP-set coefficient threshold:

```text
0.003979617773650001.
```

So the Coulomb-only Earth bulk smoke channel is not the immediate killer. Good little counterpunch.

## Binding Pressure Channel

The same source row gives:

```text
Q_surface_binding_Earth = -0.01211918219995745.
```

At the same `delta_J` envelope:

```text
|Q_surface_binding_Earth delta_J| = 8.526876722826009e-15.
```

This is above the WEP-set threshold. The L1 bulk envelope:

```text
Q_bulk_abs_L1 = 0.013810442886708322
```

is also above threshold.

Therefore the finite source route has a sharp pressure point:

```text
surface/binding source channel.
```

It must be suppressed, calibrated, projected silent, profile-weighted down, or carried as the dangerous finite source channel.

## Refusal Guard

3129 does not claim:

```text
bulk Earth vector = MICROSCOPE profile/source worldtube vector.
```

The older source-weight ledger explicitly refuses that shortcut. This checkpoint preserves that refusal.

## Current Status

All rows remain:

```text
claim_allowed = false.
```

But the gap is no longer foggy. The next fight is not "coupling in general"; it is:

```text
Q_surface_binding / source-binding channel.
```

## Runner Artifacts

| artifact | path |
|---|---|
| input rows | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3129_EARTH_SOURCE_CAL_SMOKE_INPUTS.csv` |
| output rows | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3129_EARTH_SOURCE_CAL_SMOKE_OUTPUT.csv` |
| validation | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3129_VALIDATION.csv` |
| gate | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3129_EARTH_SOURCE_CAL_SMOKE_GATE.csv` |
| runner | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\scripts\Y5_R2FR_3129_Earth_source_calibration_smoke.py` |

## Next Target

3130 should target one of two routes:

```text
derive/suppress/calibrate/project-silent Q_surface_binding,
```

or:

```text
fill a profile/worldtube-weighted Earth/source vector so the smoke row can be replaced.
```

That is the sharpest next move toward the local GR/Newton source side.
