# 4374: same-worldtube source-mass owner or E_mass bound

Marker: `PPC4161_TRANSITION_SAME_WORLDTUBE_SOURCE_MASS_OWNER_OR_EMASS_BOUND_4374`

## What changed

- Proved that equal integrated source mass is not enough to set `E_mass=0`.
- Promoted the clean zero target to pointwise/profile Hilbert density ownership: `rho_eff(y)=rho_H(y)` on `W_H`.
- Split `E_mass` into eight no-cancellation residual channels.
- Connected the residual sum to the existing `K_N(s)` exterior Newton support gate.

## Decision

| decision_id | decision | summary | next_target | why_next |
| --- | --- | --- | --- | --- |
| DEC4374_0 | SAME_TOTAL_MASS_NOT_ENOUGH_DENSITY_PROFILE_OWNER_OR_EMASS_BOUND_REQUIRED_NONCLAIM | 4374 tightens the mass-owner route. The existing 186/187/194 and 4354 chain is genuinely strong for the integrated monopole: it gives a non-circular Hamiltonian/Hilbert source mass and calibrated G_cal. But E_mass was defined as a profile/transverse source mismatch, so equal total mass is not enough. A zero-monopole density redistribution can leave E_mass nonzero and still perturb exterior fields through support/multipole geometry. Therefore the clean zero route now requires pointwise/profile Hilbert density ownership on the same worldtube before readout. If that is not signed, E_mass must be scored by the no-cancellation sum E_profile+E_PiH+E_I+E_ref+E_tau+E_boundary+E_transition+E_readout. | 4375-Y5-R2FR-transition-density-profile-owner-or-Emass-numeric-source-bound.md | the new key object is E_profile; closing it would turn the private source-mass bridge into a much stronger local-GR/Newton branch. |

## Next target

| next_id | target | question | preferred_route | alternate_route | avoid |
| --- | --- | --- | --- | --- | --- |
| NT4374_0 | 4375-Y5-R2FR-transition-density-profile-owner-or-Emass-numeric-source-bound.md | Can MTS parent-sign rho_eff(y)=rho_H(y) on W_H, or must E_profile become a finite source-density row? | derive density-profile ownership from Hilbert T00/source measure descent before readout | source or bound E_profile and score the full E_mass residual sum with K_N(s) | claiming E_mass=0 from integrated mass equality alone |
