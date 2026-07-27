# 3128 - Source-Calibration Kernel Sensitivity Interface under AX1090

Private checkpoint. This follows 3127 by turning the Hilbert-stress source coefficient into a test-facing source/calibration kernel.

## Kernel Definition

The source-GM bridge is:

```text
Delta(GM)_S / (GM)_S
  = DeltaC_Scal delta_J.
```

where:

```text
DeltaC_Scal = C_J,S^ADM - C_J,cal^ADM.
```

Using the 3127 weight measure:

```text
C_J,S^ADM
  = f_EM,S^ADM sum_AB w_AB^S K_AB + C_relax,S.
```

Therefore:

```text
DeltaC_Scal
  = f_EM,S^ADM sum_AB w_AB^S K_AB
    + C_relax,S
    - C_J,cal^ADM.
```

This is the exact object that must be filled or killed.

## Sensitivity Interface

3125 gives the current strict nonclaim envelope:

```text
|delta_J| <= 7.035851579866459e-13.
```

For any static dimensionless observable with unit projection:

```text
|DeltaC_Scal| <= bound / |delta_J|.
```

This is not a claim, because the actual projection coefficients are not derived. It is a scale interface: it tells us whether a future source/calibration kernel would be dangerous, irrelevant, or testable.

## WEP Anchor Consistency

For the WEP material anchor:

```text
eta_bound / |delta_J| = 0.003979617773650001,
```

which reproduces the 3122 one-channel:

```text
|Delta C_J(TA6V - PtRh10)| = 0.003979617773650001.
```

So the interface is internally consistent.

## PPN and Clock Rows

The clock, gamma, and beta rows are only sensitivity rows. They do not score MTS because:

```text
K_clock,
K_gamma,
K_beta
```

are not derived.

The useful fact is that, under a unit projection assumption, these bounds are far weaker than the WEP material anchor. That means the immediate local danger remains WEP/material composition and source-calibration kernels, not raw PPN unless the projection coefficient is large.

## Gdot Row

`Gdot/G` is not converted into an absolute static `delta_J` bound. Its law is:

```text
|DeltaC_Scal d(delta_J)/dt + d(DeltaC_Scal)/dt delta_J|
  <= |Gdot/G|.
```

So it needs:

```text
d(delta_J)/dt,
d(DeltaC_Scal)/dt.
```

This keeps the time/profile branch honest.

## Current Status

3128 is still nonclaim:

```text
claim_allowed = false
```

but it moves the work from "coupling missing" to a precise fork:

```text
fill DeltaC_Scal from source/calibration Hilbert-stress weights
```

or:

```text
prove DeltaC_Scal = 0 by parent grammar/calibration.
```

## Runner Artifacts

| artifact | path |
|---|---|
| input rows | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3128_SOURCE_CAL_KERNEL_INPUTS.csv` |
| output rows | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3128_SOURCE_CAL_KERNEL_INTERFACE_OUTPUT.csv` |
| validation | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3128_VALIDATION.csv` |
| gate | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3128_SOURCE_CAL_KERNEL_GATE.csv` |
| runner | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\scripts\Y5_R2FR_3128_source_calibration_kernel_interface.py` |

## Next Target

3129 should attempt one of two decisive routes:

```text
source/calibration fill:
  Sun/Earth/lab C_J,S^ADM and C_J,cal^ADM from Hilbert-stress weights;

zero proof:
  c_A(y), Z_Q(y) reduce to common calibration mode, so DeltaC_Scal=0.
```

That is now the shortest path toward a real local GR/Newton reduction gate.
