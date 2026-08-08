# 3127 - Hilbert EM Weight Measure and Poynting Guard under AX1090

Private checkpoint. This follows 3126 by deriving the body/source weighting measure needed to turn the `C_J` tensor into material, source-GM, and calibration coefficients.

The point is simple: if the coupling is real before Maxwell/Hilbert variation, then the weights are not arbitrary fitting knobs. They must come from the EM Hilbert stress energy of the body or source.

## Hilbert Stress Measure

Use the standard EM Hilbert stress block:

```text
T_EM^{mu nu}
  = Z_Q (F^{mu lambda}F^nu_lambda - 1/4 g^{mu nu}F^2).
```

On a stationary source slice:

```text
E_EM[B]
  = integral_{Sigma_B} N T_EM^{mu nu} n_mu xi_nu dSigma.
```

Then:

```text
f_EM,B^ADM = E_EM[B] / M_ADM[B].
```

This is conditional on a signed ADM split, a specified source worldtube, and no unresolved boundary flux.

## Pair Weight Measure

For a quasi-static bound-field decomposition:

```text
U_AB^B = 1/2 integral rho_A G_B rho_B,
```

and:

```text
w_AB^B = U_AB^B / sum_CD U_CD^B.
```

With the 3126 pair kernel:

```text
K_AB = kappa_A + kappa_B - zeta_Q,
```

the body EM coefficient is:

```text
C_J,B^EM = sum_AB w_AB^B K_AB.
```

The ADM/source coefficient is:

```text
C_J,B^ADM = f_EM,B^ADM C_J,B^EM + C_relax,B.
```

This is the missing bridge shape. It says exactly where the weights must come from.

## Reductions Recovered

The one-channel material smoke limit is:

```text
C_J,B = q_alpha,B (2 tau_EM - zeta_Q) + C_relax,B.
```

For the 3122 TA6V/PtRh10 row, 3127 reproduces:

```text
Delta C_J = -0.003979617773650001
|delta_J| <= 7.035851579866459e-13.
```

The homogeneous source-GM limit is:

```text
C_J,S^ADM = f_EM,S^ADM (2 tau_EM,S - zeta_Q) + C_relax,S.
```

For `zeta_Q=0`, this recovers the 3121 bridge:

```text
C_J,S^ADM = 2 tau_EM,S f_EM,S^ADM + C_relax,S.
```

## Poynting Guard

This is where the EM/wave intuition matters. The static source coefficient cannot silently eat radiative energy flow.

The energy balance is:

```text
dE_EM/dt
  = - surface_integral S dot dA - integral J dot E dV.
```

So:

```text
static ADM/source coefficient
```

requires:

```text
zero net unresolved Poynting flux,
or an explicitly averaged periodic/radiative balance.
```

If MTS wants to use EM waves or Poynting flow as a background-field clue, that is allowed as a branch, but it must be derived as a flux/readout coefficient, not smuggled into the static `GM` coefficient.

## What 3127 Improves

3127 reduces the coupling gap to concrete objects:

```text
w_AB^B from Hilbert EM stress,
f_EM,B^ADM from ADM mass split,
C_relax,B from non-EM relaxation/stress response,
C_J,cal^ADM from the calibration body/reference,
Poynting flux condition for dynamic EM.
```

This is a real narrowing. WEP, source-GM, calibration, and radiative EM now share one weight-measure grammar.

## Current Status

The result remains nonclaim:

```text
claim_allowed = false
```

because the actual body/source weights are not filled yet, and the parent action still has not signed or forbidden the `c_A(y), Z_Q(y)` slots.

## Runner Artifacts

| artifact | path |
|---|---|
| input rows | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3127_HILBERT_EM_WEIGHT_MEASURE_INPUTS.csv` |
| output rows | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3127_HILBERT_EM_WEIGHT_MEASURE_OUTPUT.csv` |
| validation | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3127_VALIDATION.csv` |
| gate | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3127_HILBERT_EM_WEIGHT_MEASURE_GATE.csv` |
| runner | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\scripts\Y5_R2FR_3127_Hilbert_EM_weight_measure.py` |

## Next Target

3128 should attempt the first source-calibration kernel fill:

```text
C_J,S^ADM - C_J,cal^ADM
```

from Hilbert-stress weights. If that cannot be filled, the clean alternative is to attack the parent zero proof:

```text
c_A(y), Z_Q(y) forbidden or calibration-only.
```

That is the next decisive fork.
