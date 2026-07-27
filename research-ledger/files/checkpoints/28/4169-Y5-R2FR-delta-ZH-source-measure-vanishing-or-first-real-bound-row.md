# 4169 - Delta-ZH Source-Measure Vanishing Or First Real Bound Row

Timestamp UTC: `2026-07-03T01:30:49+00:00`  
Branch: `MTS_R2FR_Y5_DELTA_ZH_SOURCE_MEASURE_DESCENT_4169`  
Decision: `PPC4161_TK_H_HILBERT_SOURCE_DESCENT_CLOSES_DELTA_ZH_PRIVATE_PACKET_MASS_READOUT_GLUE_REMAINS`

## Move Made
4168 reduced the coupling residual to:

```text
R_A^G = D_A delta_ZH.
```

4169 takes the derivation route first and defines the private PPC4161-TK-H branch:

```text
PPC4161-TK-H := PPC4161-TK + H_src.
```

The source clause is:

```text
S_src = S_matter[psi,g_obs,theta]
      + S_EM[A,g_obs]
      + S_binding[psi,A,g_obs]
      + int dB_impr
      + S_rest^top/zero.
```

No independent species/source weights `w_A` are admitted.

## Variational Derivation
The same action defines the local Hilbert source:

```text
T_H^munu = -2/sqrt(-g_obs) delta S_src/delta g_obs_munu.
```

The parent-to-Hilbert source split was:

```text
T_parent^H = Z_H T_H + T_leak,
Z_H = Z_0 exp(delta_ZH).
```

But under `H_src`:

```text
T_parent^H = Z_0 T_H,
T_leak = 0,
delta_ZH = 0.
```

The EM/Poynting sector is included in `T_H`; it is not a separate source multiplier.

## Coupling Residual
Using the 4168 topological kappa lock:

```text
D_A ln kappa_* = 0
```

the private packet coupling residual becomes:

```text
R_A^G = D_A ln kappa_* + D_A delta_ZH = 0.
```

## Important Guard
This closes the local coupling multiplier leak only inside PPC4161-TK-H. It does not close:

- Hilbert source charge to worldtube/orbital measured mass;
- Pi_M/H_tau/readout glue;
- full PPN;
- numerical `G_N`;
- global MTS adoption.

## Next Target
`4170-Y5-R2FR-Hilbert-source-charge-to-worldtube-mass-readout-glue.md`

## Outputs
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4169_SOURCE_REGISTER.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4169_HILBERT_SOURCE_DESCENT_ACTION.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4169_VARIATIONAL_SOURCE_MEASURE_PROOF.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4169_DELTA_ZH_CHANNEL_CLOSURE.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4169_REMAINING_MASS_READOUT_AND_PPN_GATES.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4169_BOUND_FALLBACK_ROWS.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4169_BRANCH_DECISION.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4169_CLAIM_FIREWALL.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4169_STATUS.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4169_NEXT_TARGET.csv`
