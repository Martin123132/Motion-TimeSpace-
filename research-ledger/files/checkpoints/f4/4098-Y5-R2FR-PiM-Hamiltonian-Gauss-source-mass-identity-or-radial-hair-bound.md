# 4098 - PiM/Hamiltonian/Gauss Source-Mass Identity Or Radial-Hair Bound

## Purpose

4097 showed first-order Newton follows if the same-frame Hilbert source mass is the same closed object as the Hamiltonian/Gauss mass. 4098 sharpens that identity.

- Decision: `PIMH_OPERATOR_IDENTITY_ADOPTED_HAMILTONIAN_GAUSS_MASS_IDENTITY_CONTRACT_BUILT_RADIAL_SOURCE_HAIR_BOUND_VECTOR_RETAINED`
- Public Newton/source-mass claim: `false`
- Public local-GR/PPN claim: `false`

## Forward Move

Adopt the clean 3559 branch:

```text
Pi_M^H = id/inclusion on C_H^M(W,e_obs,tau)
[d,Pi_M^H] J_H^M = 0
```

So the live obstruction is no longer a vague projector problem. It is the source-mass identity:

```text
M_H[S] := N_G int_S Pi_M^H J_H[tau]
B_tau/G_ref = M_H[Pi_M^H J_H]
delta B_tau = delta int_S Pi_M^H J_H
M_H(S2)-M_H(S1)=N_G int_A d(Pi_M^H J_H)
```

If this closes, `Phi_N=-G_ref M_H/r` and `a_r=-G_ref M_H/r^2` use the same mass denominator as the parent Hilbert source.

## What Still Blocks A Claim

- `rho_H dV_H` q-basicness is not parent-signed.
- source support regularity and no readout mask are unsigned.
- `M_H_ref=H_tau-H_ref` is not proved q-basic/source-blind.
- Hamiltonian boundary integrability/equality is a target identity, not yet derived.
- extra mass-channel currents `Pi_M^H dJ_extra` remain live.

## Bound Route

If the identity fails, the failure is observable radial/source hair: `Delta_Gauss`, `partial_r_ln_MH`, `E_rho_qbasic`, `delta_w_species`, `E_boundary_birth`, `epsilon_mu`, and EM/Poynting flux leakage.

## Next Target

`4099-Y5-R2FR-Hilbert-density-no-source-only-Hom-theorem-or-prefactor-bound.md` should attack the active-source-prefactor countermodel: forbid source-only weights or bound them.

## Outputs

- `P8_Y5_R2FR_4098_SOURCE_REGISTER.csv`
- `P8_Y5_R2FR_4098_SOURCE_MASS_IDENTITY_THEOREM.csv`
- `P8_Y5_R2FR_4098_IDENTITY_CLAUSE_AUDIT.csv`
- `P8_Y5_R2FR_4098_RADIAL_HAIR_DECOMPOSITION.csv`
- `P8_Y5_R2FR_4098_GAUSS_NEWTON_CONSEQUENCE.csv`
- `P8_Y5_R2FR_4098_BOUND_VECTOR.csv`
- `P8_Y5_R2FR_4098_DECISION_GATE.csv`
- `P8_Y5_R2FR_4098_CLAIM_GATE.csv`
- `P8_Y5_R2FR_4098_NEXT_TARGET.csv`
- `P8_Y5_R2FR_4098_STATUS.csv`
- `P8_Y5_BRR545_4098_VALIDATION.csv`
