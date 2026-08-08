# 3161 - Bexact Source Bound or Wbar Sensitivity Interface under AX1090

Private checkpoint. This follows 3160 by trying to fill:

```text
B_exact := ||d_S Lambda||_L2
```

for the first local source-domain, instead of leaving it as another placeholder.

## Setup

3160 derived:

```text
C_Hodge_hat = 1/sqrt(2)
```

for a general zero-mean primitive on the round first-domain sphere.

3161 now uses the fact that the first source-domain perturbations are `l=2` boundary profiles:

```text
Lambda(theta) = A P2(cos theta).
```

This is conditional. It assumes the parent exact primitive `Lambda` pulls back to the public metric-component `l=2` boundary profile. That parent map is not yet signed.

## Exact l=2 Identities

Using the unnormalised geodesy convention:

```text
P2(cos theta) = (3 cos^2 theta - 1)/2,
```

we have:

```text
integral_S2 P2^2 dOmega = 4 pi/5.
```

and:

```text
integral_S2 |grad_Omega P2|^2 dOmega = l(l+1) 4 pi/(2l+1) = 24 pi/5
```

for:

```text
l = 2.
```

Therefore for:

```text
Lambda(theta) = A P2(cos theta),
```

the normalized primitive norm is:

```text
||Lambda||_hat = ||Lambda||_L2/R = |A| sqrt(4 pi/5),
```

and the exact boundary norm is:

```text
B_exact = ||d_S Lambda||_L2 = |A| sqrt(24 pi/5).
```

For a pure `l=2` profile, the sharper mode-specific constant is:

```text
C_Hodge_l2 = 1/sqrt(6) = 0.4082482904638631.
```

## Earth J2 Result

From 3159, the conservative full-shell Earth J2 metric amplitude is:

```text
A_J2 = 1.505618541755115e-12.
```

Therefore:

```text
||Lambda_J2||_hat = 2.386903626527921e-12
B_exact_J2        = 5.846695950192112e-12
```

Using the general 3160 Hodge constant gives:

```text
L_W_phys <= 9.592548125449111e19.
```

Using the exact `l=2` Hodge constant gives:

```text
L_W_phys <= 1.661478072732745e20.
```

The `l=2` row is less restrictive because the mode-specific Hodge constant is sharper than the general zero-mean sphere bound.

## Tide Results

The same `l=2` interface gives:

```text
B_exact_Sun+Moon = 4.427851730645259e-16
L_W_phys <= 2.896873249711743e28        l=2 constant
```

The tide rows are much looser than the Earth J2 row in this first-domain smoke.

## Meaning

3161 removes another fog variable conditionally.

If the parent exact primitive is the public `l=2` metric boundary profile, then `B_exact` is not unknown for the first domain. It is:

```text
B_exact_J2 = 5.846695950192112e-12.
```

The local product obstruction then becomes a cap on:

```text
L_W_phys.
```

For the tightest first-domain row:

```text
L_W_phys <= 1.661478072732745e20
```

using the exact `l=2` mode constant.

This is not numerically fatal. But it is not a local-GR proof because the parent map is still unsigned:

```text
public metric l=2 boundary profile -> parent exact primitive Lambda.
```

## Claim State

No claim is promoted.

3161 does not claim:

- local closure;
- local-GR recovery;
- WEP;
- R10;
- PPN safety;
- clock safety;
- orbital safety;
- Maxwell recovery;
- Newtonian recovery.

Every generated row remains:

```text
valid_for_claim=false.
```

## Runner Artifacts

| artifact | path |
|---|---|
| runner | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\scripts\Y5_R2FR_3161_Bexact_source_bound_or_Wbar_sensitivity_interface.py` |
| inputs | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3161_INPUTS.csv` |
| l2 identities | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3161_L2_MODE_IDENTITIES.csv` |
| Bexact rows | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3161_BEXACT_SOURCE_BOUND_ROWS.csv` |
| gates | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3161_GATE_STATUS.csv` |
| decision | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3161_DECISION.csv` |
| validation | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3161_VALIDATION.csv` |

## Decision

3161 promotes the next target to:

```text
3162-Y5-R2FR-parent-Lambda-map-for-public-l2-boundary-profile-under-AX1090.
```

Best next attack:

```text
derive the parent map from the public l=2 metric boundary profile to the exact primitive Lambda.
```

If that map passes, then `L_W_phys` is the last local product factor. If it fails, these Bexact rows remain source-domain smoke/interface rows only, and the local branch must keep an explicit closure parameter.
