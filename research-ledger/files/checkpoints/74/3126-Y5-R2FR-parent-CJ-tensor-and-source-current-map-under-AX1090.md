# 3126 - Parent `C_J` Tensor and Source-Current Map under AX1090

Private checkpoint. This is the direct follow-up to 3125. Instead of writing one more "the coupling is missing" note, 3126 derives the algebraic coefficient map that a future parent action has to either sign or forbid.

## Result

Assume the selected 3124 branch is real: the current insertion occurs before Maxwell solve and Hilbert variation. The minimal local action slot is:

```text
S[A,g,Psi;y] =
  integral sqrt(-g) [
    -1/4 Z_Q(y) F_{mu nu}F^{mu nu}
    + sum_A c_A(y) A_Q,mu J_A^mu
    + L_matter(Psi_A,e,n_A)
  ].
```

Define:

```text
kappa_A = d ln c_A / dJ
zeta_Q  = d ln Z_Q / dJ.
```

Variation gives:

```text
nabla_mu(Z_Q F^{mu nu}) = sum_A c_A J_A^nu.
```

For a quasi-static EM pair:

```text
U_AB^EM proportional to c_A c_B / Z_Q,
```

so the derived pair kernel is:

```text
K_AB = kappa_A + kappa_B - zeta_Q.
```

This is the coupling map. It is not yet a parent claim, but it is no longer just a missing box.

## Body Coefficient

For a material body `B`, define EM pair weights:

```text
sum_AB w_AB^B = 1
```

over the body's EM binding/self-energy decomposition. Then:

```text
C_J,B^EM = sum_AB w_AB^B K_AB
         = sum_AB w_AB^B (kappa_A + kappa_B - zeta_Q).
```

The one-channel Coulomb smoke limit used in 3122 is:

```text
C_J,B = q_alpha,B (2 tau_EM - zeta_Q) + C_relax,B.
```

For `zeta_Q=0`, `tau_EM=1`, `C_relax=0`, this reproduces the 3122 material pair:

```text
Delta C_J(TA6V - PtRh10) = -0.003979617773650001
|delta_J| <= 7.035851579866459e-13.
```

## Source-GM Coefficient

For a gravitating source:

```text
C_J,S^ADM = f_EM,S^ADM C_J,S^EM + C_relax,S^ADM.
```

In the homogeneous limit:

```text
kappa_A = kappa_B = tau_EM,S
zeta_Q = 0
C_J,S^EM = 2 tau_EM,S
```

so:

```text
C_J,S^ADM = 2 tau_EM,S f_EM,S^ADM + C_relax,S,
```

which is exactly the 3121 source-GM bridge kernel.

The observable source-GM law remains:

```text
Delta(GM)_S / (GM)_S
  = [C_J,S^ADM - C_J,cal^ADM] delta_J.
```

## What This Actually Improves

3126 turns the coupling problem into a finite list of mathematical objects:

```text
c_A(y) or its ban,
Z_Q(y) or its ban,
w_AB^B body EM pair weights,
f_EM,S^ADM source EM mass fraction,
C_relax terms,
calibration kernel C_J,cal^ADM.
```

That is a leap forward: source-GM, WEP, R10, and EM stress now share one coefficient tensor map instead of separate symbolic gaps.

## What Still Is Not Claimed

No local-GR, WEP, R10, source-GM, or Maxwell-extension pass is claimed. The map is conditional on the parent action slot. The current status is:

```text
conditional_derived_map_not_parent_signed
claim_allowed = false
```

The alternative route remains:

```text
prove no-c_A/no-Z_Q/current-owner zero
```

which would kill `delta_J` instead of bounding it.

## Runner Artifacts

| artifact | path |
|---|---|
| input rows | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3126_CJ_TENSOR_MAP_INPUTS.csv` |
| output rows | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3126_CJ_TENSOR_MAP_OUTPUT.csv` |
| validation | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3126_VALIDATION.csv` |
| gate | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3126_CJ_TENSOR_MAP_GATE.csv` |
| runner | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\scripts\Y5_R2FR_3126_CJ_tensor_source_map.py` |

## Next Target

3127 should derive the body/source weighting measure from Hilbert EM stress:

```text
w_AB^B and f_EM,S^ADM
```

or prove that the parent action forbids the slots:

```text
c_A(y), Z_Q(y).
```

That is the shortest path from "coupling gap" to an actual GR/Newton/EM reduction gate.
