# 3165 - K2 Local Residual Vector and PPN/Clock/Orbital Gate under AX1090

Private checkpoint. This follows 3164 by turning the closure lane:

```text
K_2 := |W_2 M_Lambda|
```

into an actual local residual-vector interface.

## Per-Unit K2 Coefficient

From 3161 and 3159:

```text
||Lambda||_hat(M_Lambda=1) = 2.386903626527921e-12
A_public_full_shell        = 1.505618541755115e-12.
```

Therefore the per-unit `K_2` local `l=2` coefficient is:

```text
C_K2_unit
= ||Lambda||_hat(M_Lambda=1) * A_public_full_shell
= 3.593766357482964e-24.
```

The induced coefficient is:

```text
C_K2 = K_2 C_K2_unit.
```

## Internal AX1090 Gate

The inherited internal cap is:

```text
5.970964001482571e-4.
```

So:

```text
K_2 <= 5.970964001482571e-4 / 3.593766357482964e-24
```

which gives:

```text
K_2 <= 1.661478072732744e20.
```

This reproduces the 3164 closure cap.

## Projection-Owner Smoke Case

If later the parent theory signs:

```text
W_2 = 1
```

and:

```text
M_Lambda = 1,
```

then:

```text
K_2 = 1.
```

The residual coefficient would be:

```text
C_K2 = 3.593766357482964e-24.
```

Relative to the internal AX1090 cap:

```text
C_K2 / cap = 6.018737270214063e-21.
```

This is extremely small. It is still not a claim because both parent-owner clauses are unsigned.

## Residual Vector

The `K_2` lane now feeds:

```text
Delta_i = Pi_i,K2 * K_2 * C_K2_unit.
```

The mapped components are:

| component | arena | formula |
|---|---|---|
| `gamma_minus_1` | Shapiro/light bending/spatial curvature | `Delta_gamma_K2 = Pi_gamma_K2 K_2 C_K2_unit` |
| `beta_minus_1` | perihelion/nonlinear superposition/clocks | `Delta_beta_K2 = Pi_beta_K2 K_2 C_K2_unit` |
| `alpha2_or_xi_anisotropy` | preferred location/domain anisotropy | `Delta_aniso_K2 = Pi_aniso_K2 K_2 C_K2_unit` |
| `alpha1_alpha2_vector` | preferred-frame/vector readout | `Delta_vector_K2 = Pi_vector_K2 K_2 C_K2_unit` |
| `zeta_conservation` | Bianchi/Ward/source exchange | `Delta_zeta_K2 = Pi_zeta_K2 K_2 C_K2_unit + exchange terms` |
| `clock_redshift` | local clock/readout | `Delta_clock_K2 = Pi_clock_K2 K_2 C_K2_unit` |
| `orbital_acceleration_precession` | orbit/perihelion/radial acceleration | `Delta_orbit_K2 = Pi_orbit_K2 K_2 C_K2_unit` |

The `Pi` kernels are not fit knobs. They are projection/readout kernels fixed by the public PPN gauge, clock convention, orbital observable, and source-domain readout.

## Gate Form

For any empirical observable `i`:

```text
|Pi_i,K2| K_2 C_K2_unit <= bound_i.
```

Equivalently:

```text
K_2 <= bound_i / (|Pi_i,K2| C_K2_unit).
```

This is the exact first empirical gate shape.

## What Is Not Claimed

3165 does not claim:

- local closure;
- local-GR recovery;
- PPN safety;
- clock safety;
- orbital safety;
- WEP;
- R10;
- Maxwell recovery;
- Newtonian recovery.

The empirical gates are blocked because the checkpoint has not sourced:

```text
Pi_gamma_K2,
Pi_beta_K2,
Pi_clock_K2,
Pi_orbit_K2,
Pi_zeta_K2,
empirical bounds in the same readout convention.
```

Every generated row remains:

```text
valid_for_claim=false.
```

## Runner Artifacts

| artifact | path |
|---|---|
| runner | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\scripts\Y5_R2FR_3165_K2_local_residual_vector_and_PPN_clock_orbital_gate.py` |
| inputs | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3165_INPUTS.csv` |
| unit coefficient | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3165_K2_UNIT_RESIDUAL_COEFFICIENT.csv` |
| residual vector | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3165_K2_LOCAL_RESIDUAL_VECTOR.csv` |
| gates | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3165_PPN_CLOCK_ORBITAL_GATES.csv` |
| decision | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3165_DECISION.csv` |
| validation | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3165_VALIDATION.csv` |

## Decision

3165 promotes the next target to:

```text
3166-Y5-R2FR-first-K2-empirical-projection-gate-source-intake-under-AX1090.
```

Best next attack:

```text
source the first empirical projection gate,
preferably gamma/Shapiro or orbital precession,
and compute a real K_2 bound from data/source-backed kernels.
```

This is the first point where the local closure lane is ready to touch empirical bounds without hiding the missing parent derivation.
