# 4171 - Hamiltonian Source Charge To Poisson/Gauss/Newton Readout

Timestamp UTC: `2026-07-03T01:44:38+00:00`  
Branch: `MTS_R2FR_Y5_HAMILTONIAN_SOURCE_CHARGE_TO_POISSON_GAUSS_NEWTON_4171`  
Decision: `PPC4161_TK_HQN_DERIVES_FIRST_ORDER_POISSON_GAUSS_NEWTON_READOUT_PRIVATE_PACKET_FULL_PPN_REMAINS`

## Move Made
4170 glued the Hamiltonian source charge:

```text
Q_M = M_H^dress[W_H;tau].
```

4171 derives the weak-field Newton readout from that same charge:

```text
G_00^lin = 2 nabla^2 Phi_N/c^2
T_00 = rho_H c^2
kappa_eff = 8*pi G_N/c^4.
```

Therefore:

```text
nabla^2 Phi_N = 4*pi G_N rho_H.
```

## Gauss And Acceleration
The compact source charge is:

```text
int_W rho_H dV = M_H^dress[W_H;tau].
```

Thus:

```text
int_S grad Phi_N dot dS = 4*pi G_N M_H^dress.
```

For the exterior monopole/spherical case, or leading far-field compact-source term:

```text
Phi_N = -G_N M_H^dress/r,
a = -grad Phi_N,
a_r = -G_N M_H^dress/r^2.
```

## Anti-Circularity
No observed orbital `GM`, fitted acceleration, or measured numerical `G_N` is used to define the charge. Orbits are downstream tests now.

## What Remains
This is first-order Newtonian recovery inside a private branch. It does not close full PPN:

```text
Delta_PPN = gamma-1, beta-1, alpha_i, zeta_i, xi.
```

## Next Target
`4172-Y5-R2FR-PPC4161-full-PPN-readout-gamma-beta-alpha-xi-zeta.md`

## Outputs
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4171_SOURCE_REGISTER.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4171_WEAK_FIELD_READOUT.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4171_POISSON_GAUSS_DERIVATION.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4171_ORBITAL_ACCELERATION_READOUT.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4171_RESIDUAL_CLOSE_OR_REACTIVATE.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4171_REMAINING_PPN_EMPIRICAL_GATES.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4171_BRANCH_DECISION.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4171_CLAIM_FIREWALL.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4171_STATUS.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4171_NEXT_TARGET.csv`
