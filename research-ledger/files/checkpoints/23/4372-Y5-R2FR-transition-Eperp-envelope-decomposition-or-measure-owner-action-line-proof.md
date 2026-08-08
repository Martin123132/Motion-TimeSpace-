# 4372: E_perp envelope decomposition or measure-owner action-line proof

Marker: `PPC4161_TRANSITION_EPERP_ENVELOPE_DECOMPOSITION_OR_MEASURE_OWNER_ACTION_LINE_PROOF_4372`

## What changed

- Decomposed `E_perp` into `E_measure + E_mass + E_transition + E_Xi + E_T`.
- Mapped the 4371 geometry gate onto the component sum.
- Wrote the exact conditional action-line proof for `E_measure=0`.
- Kept the proof unsigned because measure/Jacobian/hbar/source-prefactor clauses are not parent-certified.

## Decision row

| decision_id | decision | summary | next_target |
| --- | --- | --- | --- |
| DEC4372_0 | EPERP_COMPONENT_ENVELOPE_DECOMPOSITION_DERIVED_MEASURE_OWNER_ACTION_LINE_CONDITIONAL_NONCLAIM | 4372 decomposes E_perp into a no-cancellation component envelope: E_measure, E_mass, E_transition, E_Xi and E_T. The Newton/source gate from 4370/4371 now scores the sum, not a foggy single parameter. The measure-owner action-line proof is sharpened: one q-basic species-blind measure with no hbar/Jacobian/field-normalization/source-prefactor slot would set E_measure=0, but 4361/1606 keep the needed clauses unsigned. Even if E_measure closed, E_mass, E_transition, E_Xi and E_T would still need zero/bound rows. No local-GR/Newton/PPN claim fires. | 4373-Y5-R2FR-transition-first-Eperp-component-zero-or-bound-measure-source-mass.md |

## Next target

| next_id | target | question | preferred_route | alternate_route | avoid |
| --- | --- | --- | --- | --- | --- |
| NT4372_0 | 4373-Y5-R2FR-transition-first-Eperp-component-zero-or-bound-measure-source-mass.md | Can the first E_perp component be zeroed or bounded, starting with E_measure or E_mass? | try to parent-sign E_measure via the action-line measure owner clauses | derive/source an E_mass same-worldtube source-mass mismatch bound | treating the component decomposition as a numeric bound |
