# 3152 - Kernel Closedness Chain Rule or First Norm Factor Bound under AX1090

Private checkpoint. This follows 3151:

```text
derive d_S Wbar = 0 under fixed B_class and parent kernel geometry,
or source the first real derivative/Poynting norm rows below the caps.
```

## Actual Derivation

3152 does not assume `d_S(W)=0`. It derives the exact place where that condition can come from.

Restrict the weighted-Stokes kernel to the boundary surface:

```text
W|S = z_S^* Wbar
```

where:

```text
z_S := (B_class, lambda, epsilon, xi, mu_obs, reference)|S.
```

Then the surface chain rule gives:

```text
d_S W = (D_z Wbar) o d_S z_S.
```

Equivalently, for every tangent vector `tau in T(S)`:

```text
d_S W[tau] = D_z Wbar[z_S](d_S z_S[tau]).
```

This is the useful leap: the old fog term `||d_S(W)||` splits into:

```text
kernel sensitivity:       L_W := ||D_z Wbar||_op
boundary-data drift:      B_z := ||d_S z_S||_*
boundary primitive size:  ||Lambda||_*
```

so the finite route becomes:

```text
||d_S W||_* ||Lambda||_* <= L_W B_z ||Lambda||_*.
```

## Two Honest Zero Routes

The chain rule gives two legitimate ways to zero the derivative term.

### Route A - Boundary Level Set

If the parent action proves the boundary surface is a level set of every kernel-relevant datum:

```text
d_S z_S = 0
```

then:

```text
d_S W = 0.
```

This is attractive because it zeros the term without needing a numeric primitive bound.

### Route B - Kernel Annihilator

If the kernel can see the boundary data but is blind to the allowed tangential variations:

```text
D_z Wbar | Im(d_S z_S) = 0
```

then:

```text
d_S W = 0.
```

This is the more flexible route because it does not require the boundary data to be completely constant. It only requires the parent kernel to annihilate the dangerous tangent directions.

## Why This Matters

3151 showed:

```text
B_class fixed before readout does not imply d_S(W)=0.
```

3152 now shows the missing extra condition exactly:

```text
B_class fixed is only enough if it also gives d_S z_S=0,
or if Wbar annihilates Im(d_S z_S).
```

So the next derivation is not vague. We must prove one of:

```text
d_S z_S = 0
```

or:

```text
D_z Wbar | Im(d_S z_S) = 0.
```

If neither closes, we must source:

```text
L_W, B_z, ||Lambda||_*.
```

## Current Caps

The single-survivor derivative cap remains:

```text
L_W B_z ||Lambda||_* <= 5.970964001482571e-04
```

with eta cap:

```text
4.201081650315690e-16.
```

The six-way diagnostic cap remains:

```text
L_W B_z ||Lambda||_* <= 9.951606669137618e-05
```

with eta cap:

```text
7.001802750526150e-17.
```

## Poynting Side Branch

The Poynting term also has a clean zero route, but only under the public-Maxwell interpretation:

```text
n_i S_EM^i|partialW = 0
```

with a fixed integration worldtube and no EM radiation/constitutive residual crossing the boundary.

This uses the 3105/3116 result: Poynting is either public Hilbert EM stress or an explicit residual. It is not a hidden extra source we can spend twice.

The Poynting cap remains:

```text
|Int_partialW S_EM . dA dt| / M_H <= 5.970964001482571e-04
```

or:

```text
<= 9.951606669137618e-05
```

under equal diagnostic splitting.

## Gate Status

| gate | status | reason |
|---|---|---|
| chain-rule split written | `pass_nonclaim` | exact identity `d_S W = (D_z Wbar) o d_S z_S` |
| boundary level-set route | `fail_for_claim` | parent has not signed `d_S z_S=0` |
| kernel annihilator route | `fail_for_claim` | parent has not supplied `D_z Wbar` tangent annihilator |
| finite factor route | `fail_for_claim` | `L_W`, `B_z`, and `||Lambda||` are still missing |
| Poynting stationary route | `not_claim_ready` | public stress route exists, no-radiation worldtube is unsigned |

## What Changed

This is progress, not just a missing-ledger step.

Before 3152, the missing object was:

```text
||d_S(W)|| ||Lambda||.
```

After 3152, the missing object is:

```text
L_W B_z ||Lambda||_*.
```

That is better because each factor has a different physical meaning:

| factor | meaning | best way to attack |
|---|---|---|
| `L_W` | how sensitive the kernel is to boundary data | derive kernel annihilator or source operator norm |
| `B_z` | how much boundary data drifts along `S` | prove source-support/level-set condition |
| `||Lambda||` | size of the primitive surface piece | derive boundary primitive norm or zero condition |

## Runner Artifacts

| artifact | path |
|---|---|
| inputs | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3152_INPUTS.csv` |
| derivation | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3152_KERNEL_CLOSEDNESS_DERIVATION.csv` |
| gates | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3152_ANNIHILATOR_GATE_STATUS.csv` |
| factor rows | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3152_DERIVATIVE_NORM_FACTORIZATION.csv` |
| scorecard | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3152_BOUND_SCORECARD.csv` |
| next target | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3152_NEXT_TARGET.csv` |
| validation | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3152_VALIDATION.csv` |
| runner | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\scripts\Y5_R2FR_3152_kernel_closedness_chain_rule_or_first_norm_factor_bound.py` |

## Decision

3152 does not promote local closure, local-GR recovery, WEP, R10, PPN, clock, orbital, Maxwell, or Newton claims.

It does promote the next attack from:

```text
somehow prove d_S(W)=0
```

to:

```text
3153:
prove d_S z_S=0 from local vacuum/source support,
or prove D_z Wbar annihilates Im(d_S z_S) from quotient symmetry,
or source L_W, B_z, ||Lambda|| and Poynting flux below the caps.
```
