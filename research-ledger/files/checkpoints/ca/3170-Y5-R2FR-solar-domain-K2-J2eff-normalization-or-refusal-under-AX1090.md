# 3170 - Solar-Domain K2 J2eff Normalization or Refusal under AX1090

Private checkpoint. This follows 3169 by auditing the shortcut:

```text
J2_eff := K_2 C_K2_unit.
```

The shortcut is not the correct public metric normalization.

## Metric Normalization

3159 used the weak-field public metric projection:

```text
g00 = -(1 + 2 Phi/c^2) + O(Phi^2)
gij =  (1 - 2 Phi/c^2) delta_ij + O(Phi^2).
```

For an exterior solar quadrupole:

```text
Phi_J2 = (GM/r) J2 (R_s/r)^2 P2(cos theta).
```

Therefore the public metric-component `P2` amplitude is:

```text
A_metric(r) = 2 GM/(c^2 r) J2 (R_s/r)^2.
```

Writing:

```text
rho = r/R_s
epsilon_sun_surface = GM_sun/(c^2 R_s),
```

this becomes:

```text
A_metric(r) = 2 epsilon_sun_surface J2 rho^-3.
```

So:

```text
J2_eff = A_metric rho^3 / (2 epsilon_sun_surface).
```

If:

```text
A_metric = K_2 C_K2_unit,
```

then the corrected transfer is:

```text
J2_eff = K_2 C_K2_unit rho^3 / (2 epsilon_sun_surface).
```

At the solar surface `rho=1`:

```text
epsilon_sun_surface = 2.122502570145357e-6
2 epsilon_sun_surface = 4.245005140290714e-6.
```

Thus:

```text
J2_eff(K2=1) = 8.465870449421527e-19.
```

This is the corrected normalization.

## 3169 Shortcut Audit

3169 used:

```text
J2_eff = K_2 C_K2_unit.
```

That missed:

```text
1/(2 epsilon_sun_surface).
```

Numerically:

```text
1/(2 epsilon_sun_surface) = 2.355709750522272e5.
```

So the 3169 shortcut made `J2_eff` too small by about `2.36e5` for a solar-surface exterior `J2` profile.

Equivalently, the corrected solar-surface `K_2` bounds are tighter than the 3169 shortcut bounds by:

```text
2 epsilon_sun_surface = 4.245005140290714e-6.
```

This is a real tightening, not a claim.

## Corrected Surface Bounds

Using:

```text
C_K2_unit = 3.593766357482964e-24
```

and assuming `K2*C_K2_unit` is the solar-surface public metric `P2` amplitude with standard exterior `J2` radial profile:

| source/proxy | J2_eff bound | A_metric surface bound | corrected K2 bound | ratio to internal AX1090 cap |
|---|---:|---:|---:|---:|
| Zschocke-Klioner adopted solar scale | 2.0e-7 | 8.490010280581428e-13 | 2.362426890357931e11 | 1.421882677315318e-9 |
| Rozelot total high scale | 2.32e-7 | 9.848411925474457e-13 | 2.740415192815201e11 | 1.649383905685770e-9 |
| Rozelot half-range proxy | 3.3e-8 | 1.400851696295935e-13 | 3.898004369090586e10 | 2.346106417570276e-10 |

The half-range row is still only a rough pressure proxy, not a covariance.

## Corrected Shapiro Length

Zschocke-Klioner gives:

```text
c delta_tau_Q <= 3 J2 GM_sun/c^2.
```

After the corrected map, for `K2=1`:

```text
c delta_tau_Q(K2=1) <=
3 (GM_sun/c^2) C_K2_unit / (2 epsilon_sun_surface)
= 3.750274882351347e-15 m.
```

This remains tiny for the natural owner case.

## What Is Still Not Derived

The corrected formula only applies if:

```text
K_2 C_K2_unit
```

is the solar-surface public metric `P2` amplitude with the same exterior `J2` radial profile:

```text
r^-3.
```

If the MTS residual lives at a different evaluation radius or in a different radial profile, the conversion carries:

```text
rho^3
```

or a different profile-transfer functional.

So the live blocker is now:

```text
profile/source-domain owner for K_2 C_K2_unit.
```

## Claim State

3170 claims:

```text
3169's J2_eff shortcut was missing the weak-field metric normalization factor.
```

3170 also gives the corrected conditional solar-surface transfer.

3170 does not claim:

- solar-domain transfer;
- local-GR recovery;
- PPN safety;
- Shapiro safety;
- light-bending safety;
- `K_2 C_K2_unit` is a solar exterior `J2` profile;
- the half-range proxy is a formal statistical bound.

Every generated row remains:

```text
valid_for_claim=false.
```

## Runner Artifacts

| artifact | path |
|---|---|
| runner | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\scripts\Y5_R2FR_3170_solar_domain_K2_J2eff_normalization_or_refusal.py` |
| inputs | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3170_INPUTS.csv` |
| constant source register | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3170_CONSTANT_SOURCE_REGISTER.csv` |
| normalization derivation | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3170_SOLAR_J2_NORMALIZATION_DERIVATION.csv` |
| shortcut audit | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3170_3169_SHORTCUT_AUDIT.csv` |
| corrected bounds | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3170_CORRECTED_J2EFF_K2_BOUNDS.csv` |
| decision | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3170_DECISION.csv` |
| validation | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3170_VALIDATION.csv` |

## Decision

3170 promotes the next target to:

```text
3171-Y5-R2FR-K2-radial-profile-owner-or-J2-transfer-demotion-under-AX1090.
```

Best next attack:

```text
derive whether K_2 C_K2_unit is actually a solar exterior J2-profile metric amplitude,
including the radial profile and evaluation radius.
```

If that fails, the equivalent-J2 channel must stay transfer-only and cannot be used as a local-GR or Shapiro safety claim.
