# 179 - PPC4048 Local Parent Packet Candidate

- Drafted: `2026-07-02T00:32:52+00:00`
- Status: `private_candidate_integration_draft`
- Claim status: `not_public_local_GR_claim`
- Intended formal location: `formalization-workbench/179-PPC4048-local-parent-packet-candidate.md`

## Purpose

This draft records the strongest current local-GR repair packet without erasing the older caveats.

The packet is not a declaration that MTS already derives local GR. It is a candidate parent-action contract: if the full corpus adopts it, the selected compact local PPN/Newton branch closes; if any clause is rejected, the corresponding fallback score row must be filled with no cancellation credit.

## Candidate Packet

The local parent branch is:

`Q_parent^loc = Q_dyn^loc x K_G x Q_aux`,

with `q:Q_dyn^loc -> Met_obs`, `V=ker(Dq)`, `kappa_* in K_G`, and `T_local K_G=0`.

Through the local required PPN order:

`S_loc^{<=2PN}=S_EH[g_obs;kappa_*]+S_matter[psi,g_obs,theta]+S_EM[A,g_obs]+S_binding+dB_proper+S_top+S_aux^{double-zero}+S_vert^{Dq=0}`.

Allowed extra local operators are only:

- exact/proper boundary terms;
- topological terms;
- vertical-only terms annihilated by the observed quotient/readout;
- auxiliary double-zero sectors with no linear local PPN source;
- open-system memory terms whose compact local retarded/reset projection is zero.

## Conditional Local Limit

If the packet is adopted as one parent branch, then in the compact stationary local branch:

- `nabla^2 Phi = 4*pi*G_ref*rho_H`;
- `gamma=1`;
- `beta=1`;
- `alpha_i=0`;
- `xi=0`;
- `zeta_i=0`;
- `Gdot/G=0`;
- `Delta_cZ_selected=0`;
- `Delta_cnorm_selected=0`.

This is a conditional local-GR/PPN zero vector under the packet, not a public theorem of the whole MTS corpus.

## Explicit Non-Claims

- This does not predict the numerical value of Newton's constant.
- This does not derive global Maxwell electromagnetism.
- This does not erase cosmology, galaxy, or open-memory sectors.
- This does not make old closure-only files automatically obsolete.
- This does not allow a public local-GR claim until adoption is verified or fallback score rows pass.

## Remaining Formal Weak Links

1. The closed local parent action is not yet in the formal corpus.
2. `q_loc/Khat` projector silence remains the primary formal blocker.
3. The `K_G` superselection/no-Hom coupling branch must be formalized.
4. The Hilbert/H_tau/Pi_M same-source charge map must be formalized.
5. Local standard-EM sourcing must remain separate from global Maxwell recovery.

## Adoption Rule

The packet may be promoted only if every clause is either:

- matched to an existing formal corpus source;
- inserted as an explicit new parent clause;
- or demoted to a named fallback scorer row.

No hidden closure assumption is allowed.
