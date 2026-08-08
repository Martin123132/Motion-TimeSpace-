# 3171 - K2 Radial Profile Owner or J2 Transfer Demotion under AX1090

Private checkpoint. This follows 3170 by asking whether the corrected solar `J2` pressure rows can actually score `K_2`.

The answer from the current artifacts is:

```text
not yet.
```

The reason is now precise: `K_2 C_K2_unit` is not currently derived as a solar exterior public metric `P2` amplitude.

## What K2 Currently Owns

3164 defined:

```text
K_2 := |W_2 M_Lambda|.
```

This is a scalar closure lane on the one-dimensional physical `l=2` boundary chart:

```text
delta z_phys = delta A P2(cos theta).
```

3165 then defined:

```text
C_K2_unit = ||Lambda||_hat(M_Lambda=1) A_public_full_shell.
```

Numerically:

```text
C_K2_unit = 3.593766357482964e-24.
```

So the currently owned object is:

```text
C_K2 = K_2 C_K2_unit.
```

But this is an internal residual coefficient assembled from an Earth-domain boundary norm and a public full-shell `l=2` amplitude. It is not automatically the public exterior metric amplitude of a solar quadrupole.

## Non-Identifiability Proof

Current artifacts permit the counterfamily:

```text
A_metric_solar(r)
= Upsilon_J2 K_2 C_K2_unit (R_s/r)^3 P2(cos theta),
```

with arbitrary:

```text
Upsilon_J2.
```

Different values of `Upsilon_J2` preserve the existing `K_2` bookkeeping but give different solar `J2_eff`.

Two limiting examples:

```text
Upsilon_J2 = 0
```

means nonzero `K_2` does not source the solar exterior `J2` channel.

```text
Upsilon_J2 = 1
```

recovers the 3170 corrected surface-pressure rows.

Because both are allowed by the currently written artifacts, the solar `J2` score is non-identifiable until the parent theory supplies the missing projection/radial/source map.

## Transfer Contract

Define the missing transfer kernel:

```text
A_metric_solar_surface
= Upsilon_J2 K_2 C_K2_unit.
```

Then the corrected solar `J2` map becomes:

```text
J2_eff =
Upsilon_J2 K_2 C_K2_unit / (2 epsilon_sun_surface).
```

For the 3170 half-range pressure proxy:

```text
K_2 <= 3.898004369090586e10 / |Upsilon_J2|.
```

This is a useful pressure row. It is not a score until `Upsilon_J2` is derived or source-backed.

## Required Owner Clauses

To turn the equivalent-`J2` gate into an actual empirical test, one branch must supply:

```text
1. parent Wbar/Lambda owner;
2. public metric injection Pi_J2_metric;
3. solar source-domain transfer or direct solar K2 construction;
4. exterior r^-3 radial Green profile;
5. evaluation-radius convention.
```

Without those, using the corrected `J2` bounds would still be a hidden closure assumption.

## Demotions

3171 demotes:

| target | new status |
|---|---|
| 3169 `J2_eff=K2*C_K2_unit` | wrong-normalization smoke only |
| 3170 corrected numeric bounds | `Upsilon_J2`-conditional transfer rows |
| local-GR/Shapiro safety from `J2` | still not claimed |

The corrected 3170 rows remain valuable because they show the pressure scale if the transfer closes. But they cannot be used as pass/fail evidence yet.

## Claim State

3171 claims:

```text
solar J2 scoring is non-identifiable from the current K2 artifacts.
```

3171 does not claim:

- local-GR recovery;
- PPN safety;
- Shapiro safety;
- light-bending safety;
- solar-domain transfer;
- `Upsilon_J2=0`;
- `Upsilon_J2=1`;
- a solar `J2` empirical score.

Every generated row remains:

```text
valid_for_claim=false.
```

## Runner Artifacts

| artifact | path |
|---|---|
| runner | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\scripts\Y5_R2FR_3171_K2_radial_profile_owner_or_J2_transfer_demotion.py` |
| inputs | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3171_INPUTS.csv` |
| profile owner audit | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3171_PROFILE_OWNER_AUDIT.csv` |
| non-identifiability proof | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3171_PROFILE_NONIDENTIFIABILITY_PROOF.csv` |
| Upsilon transfer contract | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3171_UPSILON_J2_TRANSFER_CONTRACT.csv` |
| scoring demotion | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3171_J2_SCORING_DEMOTION.csv` |
| decision | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3171_DECISION.csv` |
| validation | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3171_VALIDATION.csv` |

## Decision

3171 promotes the next target to:

```text
3172-Y5-R2FR-public-metric-radial-Green-owner-or-J2-channel-closure-under-AX1090.
```

Best next attack:

```text
derive Pi_J2_metric and the exterior r^-3 Green/radial profile from the parent equations,
or close the solar J2-equivalent channel as transfer-only.
```

This is the point where more external data is not the answer. The bottleneck is the parent metric/radial owner.
