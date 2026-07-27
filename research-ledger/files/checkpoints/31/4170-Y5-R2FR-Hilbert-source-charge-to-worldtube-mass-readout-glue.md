# 4170 - Hilbert Source Charge To Worldtube Mass Readout Glue

Timestamp UTC: `2026-07-03T01:38:46+00:00`  
Branch: `MTS_R2FR_Y5_HILBERT_HAMILTONIAN_WORLDTUBE_MASS_GLUE_4170`  
Decision: `PPC4161_TK_HQ_ADOPTS_HAMILTONIAN_MASS_CHARGE_MAP_SO_PIM_HTAU_WORLDTUBE_GLUE_CLOSES_PRIVATE_PACKET`

## Move Made
4169 closed the local source multiplier leak but left the source charge readout open. 4170 defines the private charge-glued branch:

```text
PPC4161-TK-HQ := PPC4161-TK-H + H_Q.
```

The adopted Hamiltonian/worldtube glue is:

```text
W_H = closure(supp J_H_total)
delta H_tau[S] = int_S(delta Q_tau - i_tau theta_total)
M_H^dress[W_H;tau] = H_tau[S_link] - H_ref
ell_M(Pi_M^H J_H_total) := M_H^dress[W_H;tau].
```

`Pi_M` is therefore not a late topological/readout mask. It is the Hamiltonian mass-charge map of the same Hilbert current and same worldtube.

## Noether Closure
The local packet current obeys:

```text
J_tau = theta_total(Phi,L_tau Phi) - i_tau L_total
J_tau = dQ_tau + C_tau.
```

In the compact source-free exterior collar:

```text
C_tau = F_symp = F_boundary = F_extra = 0.
```

So:

```text
H_tau[S2] - H_tau[S1] = 0
```

for any two linking surfaces enclosing `W_H`.

## Same-Charge Result
Inside PPC4161-TK-HQ:

```text
Q_M = ell_M(Pi_M^H J_H_total)
Q_M = H_tau[S_link] - H_ref
Q_M = M_H^dress[W_H;tau].
```

This closes the private `Pi_M/H_tau/worldtube` same-charge glue.

## Anti-Circularity
No orbital `GM`, fitted acceleration, or measured `G_N` is used in the definition. Orbital data only becomes a test after the weak-field Newton/Gauss readout is derived.

## Still Open
This does not yet prove:

- `nabla^2 Phi_N = 4*pi G_N rho_H`;
- `a_r = -G_N M_H^dress/r^2`;
- full PPN;
- numerical `G_N`;
- global MTS adoption.

## Next Target
`4171-Y5-R2FR-Hamiltonian-source-charge-to-Poisson-Gauss-Newton-readout.md`

## Outputs
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4170_SOURCE_REGISTER.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4170_HAMILTONIAN_BRANCH_ADOPTION.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4170_NOETHER_RADIAL_GLUE.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4170_SAME_OBJECT_IDENTITY.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4170_RESIDUAL_CLOSE_OR_REACTIVATE.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4170_REMAINING_NEWTON_PPN_GATES.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4170_BRANCH_DECISION.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4170_CLAIM_FIREWALL.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4170_STATUS.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4170_NEXT_TARGET.csv`
