# 3169 - STF Shapiro Source Bound or Solar-Domain K2 Transfer under AX1090

Private checkpoint. This follows 3168 by sourcing the first real STF/quadrupole comparator hook instead of continuing to borrow scalar Cassini `gamma`.

## Source Hooks

3168 left:

```text
K_2 <= epsilon_quad / (|Pi_quad_LOS| C_K2_unit)
```

with `epsilon_quad` missing.

3169 finds a usable external source hook through the standard solar quadrupole channel.

Recorded sources:

| source | role | URL |
|---|---|---|
| Zschocke & Klioner 2009 | primary formula source for quadrupole time-delay scale | `https://arxiv.org/abs/0907.4318` |
| Rozelot et al. 2022 | solar `J2` range summary | `https://arxiv.org/abs/2208.06779` |
| Kopeikin & Makarov 2007 | supporting STF/multipole light-deflection theory | `https://arxiv.org/abs/0712.0417` |

The Zschocke-Klioner source gives the strict upper-bound scale:

```text
c delta_tau_Q <= 3 J2 GM/c^2.
```

For the Sun with:

```text
J2 = 2e-7
GM_sun/c^2 = 1476 m
```

this gives:

```text
c delta_tau_Q <= 8.856e-4 m
```

which is the stated `~0.89 mm` solar quadrupole Shapiro scale.

## Equivalent-J2 Transfer

Define a conditional solar quadrupole-equivalent amplitude:

```text
J2_eff := K_2 C_K2_unit.
```

This is not automatically true. It requires the MTS `K_2` radial profile and source-domain normalization to match the solar exterior quadrupole convention.

If that transfer is later derived, then:

```text
c delta_tau_Q_MTS <= 3 GM_sun/c^2 K_2 C_K2_unit.
```

Using:

```text
C_K2_unit = 3.593766357482964e-24
```

the `K_2=1` equivalent solar quadrupole is:

```text
J2_eff(K2=1) = 3.593766357482964e-24.
```

The corresponding Shapiro length scale is:

```text
c delta_tau_Q(K2=1) <= 1.591318742933377e-20 m.
```

So the natural owner case remains tiny.

## Conditional Bounds

Under the transfer condition:

```text
J2_eff = K_2 C_K2_unit,
```

the equivalent `K_2` caps are:

| bound source | J2_eff bound | K2 equivalent bound | ratio to internal AX1090 cap |
|---|---:|---:|---:|
| Zschocke-Klioner solar scale | 2.0e-7 | 5.565192060512189e16 | 3.349542887050409e-4 |
| Rozelot high total scale | 2.32e-7 | 6.455622790194139e16 | 3.885469748978475e-4 |
| Rozelot half-range pressure proxy | 3.3e-8 | 9.182566899845112e15 | 5.526745763633175e-5 |

The half-range row is not a formal covariance. It is only a rough anomaly pressure proxy.

Still, this is important: if MTS `K_2` really maps into solar `J2_eff`, the quadrupole/STF channel pressures `K_2` far more strongly than the internal AX1090 cap and far more strongly than the borrowed scalar-gamma smoke scale.

## Transfer Blocker

The claim-blocking issue is now precise:

```text
K2_solar = T_source K2_earth
```

or:

```text
J2_eff = K_2 C_K2_unit.
```

Current status:

```text
T_source = MISSING_PARENT_SOURCE_DOMAIN_UNIVERSALITY.
```

So the equivalent-J2 row is a real gate shape, not a pass.

## Claim State

3169 does claim:

```text
if J2_eff = K_2 C_K2_unit, then solar quadrupole literature gives concrete K_2 pressure rows.
```

3169 does not claim:

- local-GR recovery;
- PPN safety;
- Shapiro safety;
- light-bending safety;
- solar-domain transfer;
- `J2_eff = K_2 C_K2_unit`;
- a Cassini quadrupole pass;
- that the Rozelot half-range is a formal statistical bound.

Every generated row remains:

```text
valid_for_claim=false.
```

## Runner Artifacts

| artifact | path |
|---|---|
| runner | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\scripts\Y5_R2FR_3169_STF_Shapiro_source_bound_or_solar_domain_K2_transfer.py` |
| inputs | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3169_INPUTS.csv` |
| source register | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3169_STF_SOURCE_REGISTER.csv` |
| transfer | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3169_SOLAR_J2_EQUIVALENT_TRANSFER.csv` |
| equivalent-J2 bounds | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3169_EQUIVALENT_J2_K2_BOUNDS.csv` |
| decision | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3169_DECISION.csv` |
| validation | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3169_VALIDATION.csv` |

## Decision

3169 promotes the next target to:

```text
3170-Y5-R2FR-solar-domain-K2-J2eff-normalization-or-refusal-under-AX1090.
```

Best next attack:

```text
derive J2_eff = K_2 C_K2_unit from the metric/source-domain side,
or refuse equivalent-J2 scoring and keep the quadrupole gate as transfer-only.
```

This is no longer just an empirical-source hunt. The empirical pressure exists; the next question is whether MTS owns the normalization that lets the pressure touch `K_2`.
