# 3167 - Pi Gamma K2 Shapiro Projection Kernel or Unit Smoke Only under AX1090

Private checkpoint. This follows 3166 by attacking the missing `Pi_gamma,K2` kernel instead of leaving it as a placeholder.

## Key Distinction

3165 mapped the `K_2` lane into a spatial-curvature residual component:

```text
Delta_gamma_K2 = Pi_gamma,K2 K_2 C_K2_unit.
```

But this line hides an important distinction:

```text
spatial-index trace != spherical-harmonic monopole.
```

The Cassini `gamma-1` result is a scalar PPN monopole readout. The current `K_2` lane is an angular `l=2` lane built from:

```text
P2(cos theta).
```

So the first projection question is not whether the spatial residual is a trace. The first question is whether the `l=2` residual leaks into the `l=0` scalar PPN gamma estimator.

## Monopole Projection

The exact angular average is:

```text
<P2>_S2 = (1/2) int_-1^1 P2(x) dx = 0.
```

Therefore:

```text
Pi_gamma,K2_l0 = <Y00,P2>/<Y00,Y00> = 0
```

provided the residual is a pure `l=2` mode and the gamma readout is the scalar monopole PPN coefficient.

This is the useful result:

```text
pure l=2 K_2 does not directly shift scalar gamma-1.
```

## What This Does Not Prove

This does not prove PPN safety.

The quadrupole residual can still produce:

```text
anisotropic Shapiro delay;
anisotropic light bending;
source-domain quadrupole leakage;
fit/covariance leakage into the scalar gamma estimator.
```

So 3167 moves the danger. It does not erase it.

The scalar Cassini gate from 3166 now becomes a leakage/mixing gate:

```text
Pi_gamma,K2 = M20_Cassini Pi_quad,K2.
```

For a pure orthogonal `l=2` mode:

```text
M20_Cassini = 0.
```

For the worst diagnostic used in 3166:

```text
M20_Cassini = 1.
```

## Mixing Gate

3166 found:

```text
C_K2_unit = 3.593766357482964e-24
gamma_abs_bound = 6.7e-5
K2_unit_projection_bound = 1.864339340271583e19.
```

3167 reinterprets this as:

```text
K_2 <= 1.864339340271583e19 / |M20_Cassini|.
```

If `M20_Cassini=1`, this reproduces the 3166 unit-projection diagnostic.

If `M20_Cassini=0`, scalar Cassini `gamma-1` gives no direct bound on pure `K_2`; the test must be moved to the quadrupole Shapiro/light-bending kernel.

The inherited internal cap was:

```text
K_2 <= 1.661478072732744e20.
```

If someone tried to saturate that internal cap, scalar-gamma leakage would need:

```text
|M20_Cassini| <= 1.122096867161887e-1.
```

This is not difficult if the mode is genuinely orthogonal. But it is not a claim until the Cassini fit/readout covariance or a clean orthogonality theorem is sourced.

## Source-Domain Guard

There is a second trap.

The recent `K_2` cap was built from an Earth/source-domain `l=2` lane. Cassini is a Solar-conjunction Shapiro experiment.

Therefore:

```text
Earth-domain K2 cap -> Solar Shapiro K2 amplitude
```

is not automatic.

Before using Cassini as a direct empirical `K_2` bound, the framework needs either:

```text
1. a source-domain transfer/universality theorem; or
2. a separate solar-domain K_2 construction; or
3. an arena-specific quadrupole Shapiro kernel.
```

## Claim State

3167 does claim the conditional mathematical sorting rule:

```text
pure l=2 has zero scalar-monopole gamma projection.
```

3167 does not claim:

- PPN safety;
- Shapiro safety;
- light-bending safety;
- local-GR recovery;
- source-domain universality;
- quadrupole residual suppression;
- Cassini fit/covariance orthogonality.

Every generated row remains:

```text
valid_for_claim=false.
```

## Runner Artifacts

| artifact | path |
|---|---|
| runner | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\scripts\Y5_R2FR_3167_Pi_gamma_K2_Shapiro_projection_kernel.py` |
| inputs | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3167_INPUTS.csv` |
| Shapiro projection derivation | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3167_SHAPIRO_PROJECTION_DERIVATION.csv` |
| mixing gate | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3167_MIXING_GATE.csv` |
| source-domain compatibility | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3167_SOURCE_DOMAIN_COMPATIBILITY.csv` |
| decision | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3167_DECISION.csv` |
| validation | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3167_VALIDATION.csv` |

## Decision

3167 promotes the next target to:

```text
3168-Y5-R2FR-anisotropic-Shapiro-quadrupole-kernel-or-source-transfer-contract-under-AX1090.
```

Best next attack:

```text
derive the quadrupole Shapiro/light-bending kernel for a pure P2 residual,
or derive the source-domain transfer law that lets the Earth l=2 K2 lane be
compared to Solar-system Shapiro data.
```

This is a genuine improvement over 3166: the scalar Cassini gamma gate is no longer treated as the whole story. The correct target is now the anisotropic projection kernel.
