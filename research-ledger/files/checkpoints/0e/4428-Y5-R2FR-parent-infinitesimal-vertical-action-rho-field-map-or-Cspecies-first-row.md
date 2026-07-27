# 4428 - parent infinitesimal vertical action rho field map or C_species first row

Marker: `PPC4161_PARENT_INFINITESIMAL_VERTICAL_ACTION_RHO_FIELD_MAP_OR_CSPECIES_FIRST_ROW_4428`

Private checkpoint generated at `2026-07-04T08:30:53+00:00`.

## What changed

- Wrote an explicit `rho` field-map split instead of just saying "missing action".
- Proved the useful negative/positive result: `rho_diff` is genuine gauge structure, but only a subdistribution, not the hidden MTS kernel.
- Identified the exact missing object: internal `rho_hid` acting on hidden/residual/projector/source-support fields while keeping observed/source/readout data fixed.
- Staged both `C_species=DERIVED_ZERO` and the real 3543 Ti/Pt inequality as nonclaim fallback interfaces.

## Decision

| decision_id | decision | summary | next_target | valid_for_claim | public_claim |
| --- | --- | --- | --- | --- | --- |
| DEC4428_0 | RHO_DIFFEO_IS_ONLY_GAUGE_SUBDISTRIBUTION_HIDDEN_RHO_COMPONENTS_UNMAPPED_CSPECIES_ZERO_AND_BOUND_INTERFACES_STAGED | 4428 separates the easy gauge action from the hard hidden action. The diffeomorphism/local-Lorentz rho is legitimate as a coordinate/frame gauge subdistribution, but it cannot span the hidden MTS kernel. The required internal rho_hid must act on Z/phi/domain/memory/projector/Gamma-Khat/boundary/tau while keeping q, source/readout, theta markers and compact charges fixed. Existing maps do not supply that. The fallback is now sharper: either prove C_species=DERIVED_ZERO from label-forgetting/total-Hilbert-source ownership, or map MTS coefficients into the real 3543 Ti/Pt inequality. | 4429-Y5-R2FR-hidden-rho-internal-shift-from-parent-constraint-or-Cspecies-zero-theorem.md | False | False |

## Next target

| next_id | target | objective | derive_first | fallback | avoid | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| NT4428_0 | 4429-Y5-R2FR-hidden-rho-internal-shift-from-parent-constraint-or-Cspecies-zero-theorem.md | Construct the internal hidden rho_hid as a parent constraint/representative shift, or prove C_species=DERIVED_ZERO from source-label forgetting. | try rho_hid(s)[Z,phi,chi_D,m,Pi_M,Gamma,Khat,B_edge,tau] with e_obs/source/readout/theta/boundary charge fixed, then test Dq(rho_hid)=0 and Im(rho_hid)=hidden kernel. | prove the parent total-Hilbert-source/no-source-weight theorem for C_species=DERIVED_ZERO, or map MTS coefficients into the 3543 Ti/Pt D_mhat/D_e inequality. | pretending diffeomorphism gauge spans hidden MTS fibres; leaving boundary/tau/source/readout components implicit; converting a bound into a parent coefficient. | False |
