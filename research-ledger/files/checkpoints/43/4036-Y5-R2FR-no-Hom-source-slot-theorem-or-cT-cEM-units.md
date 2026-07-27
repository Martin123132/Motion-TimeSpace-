# 4036 - No-Hom Source Slot Theorem Or cT cEM Units

- Timestamp: `2026-07-01T23:13:47+00:00`
- Status: `private_nonclaim_checkpoint`
- Scope: `post-checkpoint-work` only; no `formalization-workbench` edits.
- Source needles found: `10/10`.

## What Actually Moved

4036 stops treating the coupling problem as a vague missing piece. It gives the exact conditional theorem:

If the ordinary matter and EM actions factor only through the observed quotient stack `Qvis=q(Phi)`, with fixed representation labels and no pre-variation source/readout marker, then hidden/source-slot objects have no parent morphism into the matter or EM action scalar.

In that typed packet, the direct vertices

- `Z*T_H`;
- `Z*F_EM^2`;

are not legal monomials. Therefore direct `c_T` and ordinary direct `c_EM` are zero inside that packet.

## Proof Skeleton

Write

`S_ord[Phi,psi]=Sbar_ord[Qvis(Phi),psi,theta,A_obs(Qvis)]`.

Then along a hidden/source-slot variation `v_Z`,

`delta_Z S_ord = <delta Sbar_ord/dQvis, DQvis[v_Z]> + <E_psi,delta_Z psi> + boundary`.

If `DQvis[v_Z]=0`, matter is on-shell/gauge-lifted, labels are fixed, and the boundary class is fixed, the bulk variation vanishes. A `Z*T_H` term would have produced a nonzero `T_H` contribution, so it is excluded by typing, not by hope.

The same argument applies to EM only if Maxwell has one observed Hodge/normalization owner. If a hidden multiplier `f(Z)F_EM^2` is allowed, `c_EM` is real and must be bounded.

## Fallback Units

If the packet is rejected:

- `F=Gamma_eff-Gamma0` has dimension `L^-2` for dimensionless `u`.
- `T_H` and normalized EM action/stress scalars have dimension `L^-4` in natural units.
- Therefore `c_T` and normalized `c_EM` have dimension `L^2 = mass^-2`.
- In SI energy-density convention, the comparison unit is `m/J`; `G/c^4` is the GR scale.

## Current Verdict

- Current evaluator result: `NO_HOM_THEOREM_DERIVED_CONDITIONAL_PARENT_UNSIGNED`.
- Claim result: `NO_PUBLIC_LOCAL_GR_CLAIM_FROM_4036`.
- Real progress: the missing coupling fork is now exact: either sign the typed parent packet or score finite `c_T,c_EM` bounds.

## Next Target

- `4037-Y5-R2FR-minimal-parent-packet-signature-or-cT-cEM-bound-smoke.md`
- `scripts/Y5_R2FR_4037_minimal_parent_packet_signature_or_cT_cEM_bound_smoke.py`
