# 3142 - EM/Poynting q-Basic Sector under AX1090

Private checkpoint. This follows 3141 by taking the selected tactical fork:

```text
EM/Poynting q-basic sector theorem:
parent T_Q/gauge norm + no independent F_Q^2 + Hilbert stress/current owner.
```

## Result

3142 derives the clean conditional readout:

```text
owned q-basic Maxwell sector
=> Maxwell equations
=> Hilbert EM stress tensor
=> observed Poynting flux.
```

Assume:

```text
L_EM = q^*(-1/4 Z_Q mu_obs F_Q^{mu nu}F^Q_mu nu) + dB_EM,
```

where:

```text
Z_Q = C_P N_Q
```

is fixed by parent/representation data, and no extra observed-sector kinetic coefficient is legal:

```text
lambda_A F_Q^2,
f_X(Xhat)F_Q^2,
delta_lambda_rad F_Q^2,
readout-regenerated F_Q^2.
```

Then for:

```text
v in ker(Dq),
```

the EM kinetic coefficient is vertically silent:

```text
Lie_v Z_Q = 0.
```

If `hbar`, `c`, and the alpha readout are quotient-fixed or fixed representation data too, then:

```text
b_alpha = Lie_v ln alpha_EM = 0.
```

## Poynting Readout

The Poynting vector is not an extra axiom in this branch.

Metric variation of the owned Maxwell sector gives:

```text
T_EM^{mu nu}
= Z_Q(
    F^{mu rho}F^nu_rho
    - 1/4 g_obs^{mu nu} F^2
  ).
```

In an observed tetrad:

```text
S^i = -T_EM^i_0.
```

Equivalently this is the usual observed `E x H` flux once the same `Z_Q` convention is used.

So the physical statement is:

```text
the Poynting vector is the observed energy-flux component
of the Hilbert stress tensor of the q-owned Maxwell sector.
```

This is exactly the disciplined version of the intuition that EM energy flux is working on the background/readout field.

## What Actually Closes

The following conditional theorem is exact:

| clause | result |
|---|---|
| q-basic Maxwell sector | EM stress depends only on `Q_obs`/fixed representation data |
| fixed `T_Q` and `N_Q` | EM kinetic normalization is parent-owned |
| no extra `F_Q^2` slot | alpha has no independent hidden-visible coefficient |
| same current owner | `J_Q=delta S_matter/delta A_Q` |
| Hilbert variation | standard EM stress tensor follows |
| observed tetrad readout | Poynting flux follows as `-T^i_0` |

So if the EM sector ownership signs, we get:

```text
b_alpha = 0
Delta_T_EM = 0
Poynting readout owned
```

without inserting Poynting by hand.

## What Still Does Not Close

The current corpus does not yet parent-sign the EM sector.

The live blockers are:

| blocker | status |
|---|---|
| parent `T_Q` object | partial template only |
| fixed charge lattice/base unit | integer labels partial, base unit unsigned |
| fixed gauge norm/level `N_Q` | not parent-signed |
| no independent `lambda_A F_Q^2` | not derived |
| no hidden `f_X(Xhat)F_Q^2` | not derived |
| same current owner | not parent-signed |
| readout/radiative closure | unsigned |

Therefore:

```text
b_alpha=0 is not claimed.
```

and:

```text
EM/Poynting/local-GR/WEP/R10 claims remain blocked.
```

## Finite Residual If The Zero Route Fails

If the EM sector is not q-basic, the finite residual is no longer vague.

Define:

```text
Z_EM,total
= C_P N_Q
  + lambda_A
  + f_X(Xhat)
  + delta_lambda_rad
  + readout terms.
```

Then:

```text
zeta_EM = Lie_v ln Z_EM,total.
```

This is the honest finite branch behind:

```text
b_alpha_EM,
Delta_T_EM,
beta_source_alpha.
```

Those are now explicit residual rows, not philosophical worries.

| residual | meaning |
|---|---|
| `b_alpha_EM` | vertical alpha derivative from EM kinetic/readout sector |
| `zeta_EM` | vertical derivative of total EM kinetic coefficient |
| `Delta_T_EM` | non-q-basic correction to EM stress/Poynting readout |
| `beta_source_alpha` | source/test EM current normalization residual |

No clock/WEP/R10 transfer is allowed until the corresponding `tau`, source/test, material, and projection factors are real.

## Claim Gate

| gate | status |
|---|---|
| EM q-basic to Maxwell stress/Poynting | `pass_conditional_theorem` |
| parent `T_Q`, norm, no-extra-`F^2`, current, readout signed | `fail_for_claim` |
| `b_alpha` zero or finite prediction | `not_claim_ready` |
| clock/WEP/R10 alpha transfer | `not_claim_ready` |

## Why This Matters

This is a useful step because it connects three things that were floating separately:

```text
charge/alpha,
Poynting flux,
EM stress-energy.
```

They now sit in one exact fork:

```text
owned q-basic Maxwell sector
```

or:

```text
finite zeta_EM residual branch.
```

That is good theory hygiene. It means we are not trying to “explain Poynting” with words. We either derive it from Hilbert variation of an owned EM sector, or we carry the missing ownership as an explicit finite coefficient.

## Runner Artifacts

| artifact | path |
|---|---|
| inputs | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3142_INPUTS.csv` |
| EM q-basic theorem | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3142_EM_QBASIC_THEOREM.csv` |
| Poynting/stress readout | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3142_POYNTING_STRESS_READOUT.csv` |
| zero/residual rows | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3142_EM_ZERO_OR_RESIDUAL_ROW.csv` |
| gate | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3142_GATE.csv` |
| decision | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3142_DECISION.csv` |
| validation | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3142_VALIDATION.csv` |
| runner | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\scripts\Y5_R2FR_3142_em_poynting_qbasic_sector.py` |

## Next Target

The zero route is now sharpened enough that repeating it immediately would probably be circling.

The next best target is:

```text
3143:
fill the first finite alpha/EM product input,
or prove the same-current owner needed for beta_source_alpha=0.
```

Two acceptable routes:

```text
Route A:
finite zeta_EM/b_alpha product row with clock/WEP/R10 projection requirements.
```

or:

```text
Route B:
same T_Q current owner theorem,
J_Q = delta S_matter / delta A_Q,
with no q_A(Xhat) or c_A current weights.
```

Route A gets us closer to testing. Route B gets us closer to derivation. The better next move depends on whether we want the next session to be data-facing or proof-facing.
