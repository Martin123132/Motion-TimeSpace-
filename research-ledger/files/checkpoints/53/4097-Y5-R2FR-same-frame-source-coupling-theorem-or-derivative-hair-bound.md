# 4097 - Same-Frame Source Coupling Theorem Or Derivative-Hair Bound

## Purpose

4096 reduced `Y5_source_normalization` to a concrete source-coupling problem. 4097 assembles the exact first-order Newton contract: one observed frame, one calibrated `G_ref/kappa_ref`, one Hilbert source, and one closed projected mass current.

- Decision: `SAME_FRAME_SOURCE_COUPLING_THEOREM_ASSEMBLED_FIRST_ORDER_NEWTON_DERIVED_CONDITIONALLY_DERIVATIVE_HAIR_VECTOR_RETAINED_NONCLAIM`
- Public Newton/source-coupling claim: `false`
- Public local-GR/PPN claim: `false`

## Conditional Derivation

If the parent action signs

```text
S_loc = (c^4/(16 pi G_ref)) int sqrt(-g_obs) R[g_obs] + S_matter[psi,A,g_obs] + S_silent
T_H^{mu nu} = -(2/sqrt(-g_obs)) delta S_matter / delta g_obs_{mu nu}
d(Pi_M J_H) = -Pi_M dJ_extra + [d,Pi_M]J_H + A_parent = 0
kappa_ref = 8 pi G_ref / c^4
```

then the weak-field `00` equation gives

```text
G_00^(1)=2 nabla^2 Phi_N/c^2,   T_00=rho_H c^2
=> nabla^2 Phi_N = 4 pi G_ref rho_H
=> U = G_ref M_H/r,   a = -grad U
```

That is the right GR-style target: the numerical value of `G_ref` is calibrated, but its universal role is derived.

## What Still Blocks A Claim

- `Pi_M J_H` closure is not parent-signed.
- the Hamiltonian/Gauss boundary charge is not yet proved to be the same object as the projected Hilbert mass.
- worldtube/support/reference data are not yet locked before readout.
- derivative hair (`Gdot`, radial/range hair, species source charge, frame split, extra monopoles) remains active.
- first-order Newton does not by itself close `gamma`, `beta`, `zeta`, R11, or EM/Poynting stress ownership.

## Bound Route

Every failure mode has a retained row: `dln_Geff_dt`, `dln_MH_dt`, `partial_r_ln_Geff`, `partial_r_ln_MH`, `eta_source_AB`, `delta_frame_source`, `epsilon_mu`, and second-order PPN source tails.

## Next Target

`4098-Y5-R2FR-PiM-Hamiltonian-Gauss-source-mass-identity-or-radial-hair-bound.md` should attack the sharpest remaining source-coupling obstruction: proving the projected Hilbert mass is the same closed source object as the Hamiltonian/Gauss mass.

## Outputs

- `P8_Y5_R2FR_4097_SOURCE_REGISTER.csv`
- `P8_Y5_R2FR_4097_SAME_FRAME_SOURCE_COUPLING_THEOREM.csv`
- `P8_Y5_R2FR_4097_NEWTON_CHAIN_GATE.csv`
- `P8_Y5_R2FR_4097_OBSTRUCTION_TO_BOUND.csv`
- `P8_Y5_R2FR_4097_DERIVATIVE_HAIR_BOUND_VECTOR.csv`
- `P8_Y5_R2FR_4097_NEWTON_PPN_DECISION.csv`
- `P8_Y5_R2FR_4097_DECISION_GATE.csv`
- `P8_Y5_R2FR_4097_CLAIM_GATE.csv`
- `P8_Y5_R2FR_4097_NEXT_TARGET.csv`
- `P8_Y5_R2FR_4097_STATUS.csv`
- `P8_Y5_BRR545_4097_VALIDATION.csv`
