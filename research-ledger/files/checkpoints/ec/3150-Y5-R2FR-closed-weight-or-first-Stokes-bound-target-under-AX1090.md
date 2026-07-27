# 3150 - Closed Weight or First Stokes Bound Target under AX1090

Private checkpoint. This follows 3149:

```text
derive d_S(W)=0 from parent/source boundary class,
or fill the first finite bound term:
||d_S W|| ||Lambda|| or poynting_flux_abs.
```

3150 does both: it writes the closed-weight theorem contract and computes the first finite cap if the theorem remains unsigned.

## Closed-Weight Theorem Shape

The weighted-Stokes weight is the local source projector kernel restricted to the boundary class:

```text
W := W_local|S
   = q^* Wbar(B_class, lambda, epsilon, xi, mu_obs, reference).
```

The clean theorem is:

```text
D_S B_class = 0,
D_S lambda = 0,
D_S epsilon = 0,
D_S xi = 0,
D_S reference = 0
=> d_S(W) = 0.
```

If signed, this kills the kernel-derivative term:

```text
||d_S(W)|| ||Lambda|| = 0.
```

But it is not currently signed because the boundary class, kernel/range owner, reference/readout silence, and source variation class are not all fixed by one parent action clause.

## Bound Target

Since the Coulomb-only branch sits below the current WEP-set coefficient threshold, the remaining total unsigned surface budget after Coulomb is:

```text
5.970964001482571e-04
```

in coefficient units, corresponding to:

```text
4.201081650315690e-16
```

in the current eta envelope.

Against the raw surface/binding coefficient, that is:

```text
rho <= 4.926870396835468e-02.
```

So if the derivative term is the only surviving surface term, it must satisfy:

```text
||d_S(W)||_* ||Lambda||_* <= 5.970964001482571e-04.
```

If the six unsigned Stokes/flux terms share the budget equally as a diagnostic, the per-term cap is:

```text
9.951606669137618e-05
```

or:

```text
rho_i <= 8.211450661392446e-03.
```

The same cap applies to the Poynting flux term if it is the only survivor:

```text
|Int_partialW S_EM . dA dt| / M_H <= 5.970964001482571e-04.
```

## What This Means

This is no longer vague.

The first finite bound term must either be theorem-zero:

```text
d_S(W)=0
```

or numerically/source-backed below a known cap.

Closing only `d_S(W)=0` is not enough for a full pass, because corner, harmonic, residual, Poynting, reference, and readout terms are still active. But it removes one real obstruction from the surface-null theorem.

## Gates

| gate | status |
|---|---|
| same boundary class fixed before readout | `fail_for_claim` |
| kernel/range/epsilon owner fixed on `S` | `fail_for_claim` |
| reference/readout cannot move `W` | `fail_for_claim` |
| `d_S(W)=0` | `not_claim_ready` |
| derivative/flux bound targets staged | `pass_nonclaim` |

## Runner Artifacts

| artifact | path |
|---|---|
| inputs | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3150_INPUTS.csv` |
| theorem | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3150_CLOSED_WEIGHT_THEOREM.csv` |
| gates | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3150_CLOSED_WEIGHT_GATES.csv` |
| bound targets | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3150_FIRST_STOKES_BOUND_TARGETS.csv` |
| score impact | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3150_SCORE_IMPACT.csv` |
| decision | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3150_DECISION.csv` |
| validation | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3150_VALIDATION.csv` |
| runner | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\scripts\Y5_R2FR_3150_closed_weight_or_first_stokes_bound.py` |

## Decision

3150 does not promote the closed-weight theorem.

It does promote the target from fog to a concrete cap:

```text
||d_S(W)|| ||Lambda|| <= 5.970964001482571e-04
```

if it is the only remaining term, or:

```text
<= 9.951606669137618e-05
```

under equal diagnostic budget splitting.

Next target:

```text
3151:
derive boundary-class fixedness before readout,
or fill/source the first numeric derivative-bound input:
||d_S(W)|| and ||Lambda||.
```
