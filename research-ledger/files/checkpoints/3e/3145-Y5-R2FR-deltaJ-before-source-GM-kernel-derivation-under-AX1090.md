# 3145 - `delta_J_before` Source-GM Kernel Derivation under AX1090

Private checkpoint. This follows the 3144 decision:

```text
the no-cA/no-wA grammar theorem is not parent-signed,
so carry the before-variation finite current/source branch.
```

3145 takes that branch seriously and derives the source-GM projection kernel instead of merely saying the kernel is missing.

## Result

Represent the selected 3144 branch as:

```text
J_Q -> J_Q + epsilon_J_before u_J(x) J_Q
```

before Maxwell solve and Hilbert variation.

On the fixed public Maxwell background used in 3142 and 3121:

```text
L_A[delta A_Q] = delta J_Q,
delta F_Q = d(delta A_Q) = G_F[epsilon_J_before u_J J_Q].
```

Holding the public metric/coframe, Hodge owner, and EM kinetic normalization fixed, the Hilbert Maxwell stress varies as:

```text
delta T_EM^{mu nu}
= Z_EM(
    delta F^mu_a F^{nu a}
  + F^mu_a delta F^{nu a}
  - 1/2 g^{mu nu} F_ab delta F^{ab}
  ).
```

The source-GM kernel is therefore:

```text
K_GM_J[S;u]
= (1/M_H,S) Int_S xi_nu delta T_EM^{mu nu}[u] dSigma_mu
  + K_relax,S[u]
  + K_boundary,S[u].
```

The observable source-GM residual is not the raw kernel. It is calibration-subtracted:

```text
Delta ln(GM)_obs,J
= epsilon_J_before [K_GM_J[S;u_S] - K_GM_J[cal;u_cal]].
```

That is the 3145 advance.

## What This Means Physically

This gives a clean middle position:

```text
current coupling can alter raw source stress,
but a universal/common-mode current normalization is not automatically observable.
```

So MTS does not instantly fail local GR because a hidden current normalization exists. It fails only if a calibration-subtracted, time-dependent, source-dependent, composition-dependent, or metric-shape residual survives the local bounds.

That is the right boxing-match rule: do not call a knockdown when the punch was absorbed by calibration, but do not hide a real differential residual either.

## Limits

### Constant Source Profile

If:

```text
u_J = 1,
fixed public Hodge/Z_EM,
stationary weak field,
no relaxation,
no boundary/support tail,
```

then:

```text
delta F = epsilon_J_before F,
delta T_EM = 2 epsilon_J_before T_EM.
```

So:

```text
K_GM_J[S] = 2 f_EM,S^H.
```

This recovers the 3121 leading bridge as a limit of the more exact Frechet kernel.

### Weighted Source Profile

If `u_J` varies over the source support:

```text
K_GM_J[S]
= 2 f_EM,S^H <u_J>_EM,S
  + K_nonlocal,S
  + K_relax,S
  + K_boundary,S.
```

This is where the hard work now lives: source profile, EM stress weighting, relaxation, and boundary/support convention.

### Common-Mode Calibration Silence

If source and calibration share the same kernel:

```text
K_GM_J[S;u_S] = K_GM_J[cal;u_cal],
```

then:

```text
Delta ln(GM)_obs,J = 0.
```

So a raw current normalization is not automatically an observable Newton/GR violation.

### Differential Residual

If the source and calibration kernels differ:

```text
Delta K_GM_J != 0,
```

then:

```text
Delta ln(GM)_obs,J = epsilon_J_before Delta K_GM_J.
```

That is the actual branch that can hit orbital dynamics, source normalization, clocks, or PPN after the relevant projection kernels are supplied.

## Local-GR Gate

The finite branch is locally harmless only if one of these closes:

```text
epsilon_J_before = 0,
```

or:

```text
K_GM_J[S;u_S] - K_GM_J[cal;u_cal] = 0,
```

or:

```text
|Pi_local epsilon_J_before Delta K_GM_J| <= local bound
```

without using fitted orbital `GM` as a circular proof input.

This is important: 3145 does not prove local GR yet, but it gives the correct bridge for proving or bounding it.

## PPN and WEP Separation

`DeltaGM_J` alone is not a PPN prediction.

PPN needs the metric-shape projection:

```text
Delta_PPN_J
= Pi_PPN G_metric[delta T_EM[u_S] - delta T_EM[cal]] epsilon_J_before.
```

Likewise, a pure source `GM` rescaling cancels from a leading Eotvos ratio. WEP needs test-body gravitational/inertial mismatch or source-test product legs. This keeps the theory from cheating by treating every local bound as the same bound.

## What Is Still Missing

The derivation now supplies the kernel form. It does not supply numeric claim rows.

Still needed:

| object | missing input |
|---|---|
| `epsilon_J_before` | parent coefficient, bound, or zero theorem |
| `K_GM_J[S;u_S]` | source profile, EM stress fraction, support/worldtube, relaxation, boundary convention |
| `K_GM_J[cal;u_cal]` | same-frame calibration reference |
| `Delta_PPN_J` | metric Green operator and PPN projection |
| `d_ln_GM_dt_J` | time profile for coefficient and kernels |

## Runner Artifacts

| artifact | path |
|---|---|
| inputs | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3145_INPUTS.csv` |
| kernel derivation | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3145_DELTAJ_BEFORE_GM_KERNEL.csv` |
| limit reductions | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3145_LIMIT_REDUCTIONS.csv` |
| observability gates | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3145_OBSERVABILITY_GATES.csv` |
| residual vector | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3145_RESIDUAL_VECTOR.csv` |
| decision | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3145_DECISION.csv` |
| validation | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3145_VALIDATION.csv` |
| runner | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\scripts\Y5_R2FR_3145_deltaJ_before_source_GM_kernel_derivation.py` |

## Decision

3145 replaces:

```text
MISSING_DELTAJ_TO_SOURCE_GM_KERNEL
```

with:

```text
Delta ln(GM)_obs,J
= epsilon_J_before [K_GM_J[S;u_S] - K_GM_J[cal;u_cal]].
```

No public/local-GR claim follows yet.

The next useful target is:

```text
3146:
fill or derive the first source/calibration kernel pair
K_GM_J[S;u_S], K_GM_J[cal;u_cal],
probably starting with a clean Earth/Sun/lab-calibration convention.
```

If the kernel pair is common-mode, the branch may be locally silent. If it is differential, the finite residual becomes scoreable.
