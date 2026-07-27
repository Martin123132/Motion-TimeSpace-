# 3147 - Signed Orthogonality/Common-Mode Gate under AX1090

Private checkpoint. This follows 3146, which exposed the live fork:

```text
absolute no-cancellation: slightly over threshold,
signed smoke sum: below threshold,
but signed cancellation is not yet legal.
```

3147 derives the exact contract for when the signed route is allowed.

## Result

Signed addition is legal only if the Coulomb and surface/profile channels are components of one parent-owned linear source functional:

```text
DeltaK_total = L_parent[P_C q_C + P_S q_S],
```

with:

```text
fixed oriented basis,
parent-owned source pairing,
no post-readout sign choice,
no fitted cancellation,
no hidden/direct source spurion re-entry.
```

Equivalently, one of these parent identities must be signed:

```text
common-mode:
K_GM_J[S;u_C,u_S] = K_GM_J[cal;u_C,u_S],
```

or:

```text
orthogonal projection:
Pi_local P_surface q_surface = 0,
```

or:

```text
oriented linear identity:
DeltaK_total = DeltaK_C + DeltaK_S
with signs fixed by the parent map before fitting.
```

Without one of those identities, the active gate remains:

```text
score_abs = |DeltaK_C| + |DeltaK_S|.
```

## Current Score

The absolute fallback remains active:

```text
|DeltaK_C| + |DeltaK_S|
= 4.382882115828398e-03,
threshold = 3.979617773650001e-03.
```

At the current `delta_J` smoke envelope:

```text
eta_abs = 3.083730805901969e-15,
eta_bound = 2.8e-15.
```

So the active nonclaim pressure row is:

```text
eta excess = 2.837308059019689e-16.
```

That is close, but it is still over.

## Signed Route

If the parent orientation/sign identity is later signed, the smoke signs give:

```text
|DeltaK_signed|
= 2.382160631175090e-03,
```

and:

```text
eta_signed = 1.676052864034894e-15,
```

which is below the current bound.

But 3147 does not claim this pass, because the parent-to-DD map, physical profile, readout projection, common worldtube, and spurion exclusion gates are not signed.

## Profile Route

The tightened profile target after carrying the Coulomb channel is:

```text
rho_profile <= 0.04926870396835468.
```

The current two-layer smoke row is:

```text
rho_profile = 0.0825435846925518.
```

So:

```text
rho_profile / rho_required = 1.675363569174102.
```

The profile only needs to improve by a factor of about `1.68`, but it must be a real profile/worldtube row, not a two-layer smoke row.

## Gates

| gate | status | meaning |
|---|---|---|
| parent-to-DD oriented map | `fail_for_claim` | signed basis/orientation is not derived |
| PREM/equivalent worldtube profile | `fail_for_claim` | current profile is smoke |
| official/parent readout projection | `fail_for_claim` | profile vector is not a physical local readout |
| same source/calibration worldtube | `fail_for_claim` | common-mode zero is still only conditional |
| no `J_spurion` / `J_direct` re-entry | `fail_for_claim` | 3134 still carries leakage heads |
| absolute no-cancellation fallback | `active` | active score remains the pressure row |

## Parent Contract

To use the signed route, a future parent action must supply:

1. an oriented parent-to-DD/source basis map;
2. a source Hilbert/symplectic pairing proving common-mode equality, orthogonality, or fixed destructive orientation;
3. a physical profile/worldtube vector or a long-range theorem;
4. no source-only spurion/direct vertex re-entry.

If any of these are missing, the signed smoke pass stays private/nonclaim.

## Runner Artifacts

| artifact | path |
|---|---|
| inputs | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3147_INPUTS.csv` |
| theorem shapes | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3147_SIGNED_CANCELLATION_THEOREM.csv` |
| gate status | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3147_GATE_STATUS.csv` |
| scorecard | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3147_SIGNED_VS_ABSOLUTE_SCORECARD.csv` |
| parent contract | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3147_PARENT_CONTRACT.csv` |
| decision | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3147_DECISION.csv` |
| validation | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3147_VALIDATION.csv` |
| runner | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\scripts\Y5_R2FR_3147_signed_orthogonality_common_mode_gate.py` |

## Decision

The signed route is mathematically viable but not yet legal.

So 3147 keeps the active status as:

```text
absolute no-cancellation pressure row retained.
```

Next target:

```text
3148:
try to prove Pi_local P_surface = 0 or K_source = K_cal from Hilbert/worldtube geometry.
```

If that fails, the fallback is data-facing:

```text
replace the two-layer smoke profile with PREM/shell/worldtube profile
and test whether rho_profile <= 0.04926870396835468.
```
