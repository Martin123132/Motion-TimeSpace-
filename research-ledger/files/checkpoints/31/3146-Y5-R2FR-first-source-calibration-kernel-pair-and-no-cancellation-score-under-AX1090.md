# 3146 - First Source/Calibration Kernel Pair and No-Cancellation Score under AX1090

Private checkpoint. This follows 3145:

```text
Delta ln(GM)_obs,J
= epsilon_J_before [K_GM_J[S;u_S] - K_GM_J[cal;u_cal]].
```

3146 stages the first explicit source/calibration kernel-pair rows in that language, using the earlier 3128-3133 source-calibration and profile-weighting work.

## Result

The first usable finite kernel-pair ledger is now:

| branch | coefficient | status |
|---|---:|---|
| common-mode source/calibration | `0 if theorem signed` | exact conditional zero, not signed |
| Earth bulk Coulomb smoke | `3.382521373501744e-03` | below WEP-set coefficient threshold, nonclaim |
| Earth raw surface/binding smoke | `-1.211918219995745e-02` | above threshold pressure channel |
| profile/worldtube binding delta smoke | `-1.000360742326654e-03` signed, `1.000360742326654e-03` absolute | below threshold alone, nonclaim |

The important new score is the combination.

Under strict no-cancellation:

```text
|DeltaK_coulomb| + |DeltaK_profile|
= 4.382882115828398e-03.
```

The WEP-set coefficient threshold from the current `delta_J` envelope is:

```text
3.979617773650001e-03.
```

So the absolute combination is slightly over:

```text
predicted eta = 3.083730805901969e-15
WEP eta bound = 2.8e-15.
```

That is not catastrophic, but it is a real pressure row.

## Signed vs Absolute

If the smoke signs are allowed, the combined coefficient is:

```text
3.382521373501744e-03 - 1.000360742326654e-03
= 2.382160631175090e-03.
```

Then:

```text
predicted eta = 1.676052864034894e-15,
```

which is below the current bound.

But this is not a claim because sign-cancellation is not allowed until the parent-to-DD map, source profile, calibration reference, and readout convention are signed.

So the branch does not need a miracle. It needs one of:

```text
common-mode source/calibration zero,
signed orthogonality/cancellation from parent geometry,
or stronger physical profile suppression.
```

## Tightened rho Requirement

The old standalone surface/binding cap was:

```text
|rho_surf| <= 0.3283734585378189.
```

But once the Coulomb channel is carried at the same time under absolute no-cancellation, the remaining binding/profile budget tightens to:

```text
|rho_surface_remaining| <= 0.04926870396835468.
```

The current two-layer smoke profile has:

```text
rho_profile_worldtube = 0.0825435846925518.
```

So the profile smoke is:

```text
below the old standalone surface cap,
above the tighter combined absolute budget.
```

This is the useful lesson of 3146.

## Interpretation

This is not a local-GR failure and not a local-GR pass.

It says:

```text
the selected finite current/source branch is close enough that calibration/profile geometry matters,
but not safe enough under absolute no-cancellation with the current smoke profile.
```

That is a better state than "missing coefficient." We now know the branch lives or dies on a specific sign/profile/common-mode theorem.

## Gates

| gate | status |
|---|---|
| first `K_source - K_cal` pair exists | `pass_nonclaim` |
| common-mode zero theorem | `fail_for_claim` |
| absolute no-cancellation combo below threshold | `fail_for_claim_pressure` |
| signed combo allowed | `fail_for_claim` |
| real PREM/worldtube profile imported | `fail_for_claim` |

## Runner Artifacts

| artifact | path |
|---|---|
| inputs | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3146_INPUTS.csv` |
| kernel pairs | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3146_SOURCE_CALIBRATION_KERNEL_PAIR.csv` |
| combination score | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3146_NO_CANCELLATION_COMBO_SCORE.csv` |
| gates | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3146_GATES.csv` |
| decision | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3146_DECISION.csv` |
| validation | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3146_VALIDATION.csv` |
| runner | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\scripts\Y5_R2FR_3146_first_source_calibration_kernel_pair.py` |

## Decision

3146 selects the next fork:

```text
3147:
prove signed orthogonality/common-mode calibration for the Coulomb and surface/profile channels,
or replace the two-layer smoke profile with a real source/worldtube profile and check whether
rho_profile <= 0.04926870396835468.
```

That is the current shortest route toward a derived local-GR/Newton source branch.
