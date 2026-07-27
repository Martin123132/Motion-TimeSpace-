# 4370: epsilon_Gsrc coefficient bound or Xi owner edge proof

Marker: `PPC4161_TRANSITION_EPSILON_GSRC_COEFFICIENT_BOUND_OR_XI_OWNER_EDGE_PROOF_4370`

## What changed

- Used `int_W rho_H epsilon_Gsrc_perp dV=0` to derive a sharper zero-monopole far-field gate.
- Converted the Newton/source-normalization obstruction to `E_perp <= delta_N/K_N(s)`.
- Added geometry factors for representative `R/r` values.
- Audited the owner-edge zero route and kept it unsigned.

## Decision row

| decision_id | decision | summary | next_target |
| --- | --- | --- | --- |
| DEC4370_0 | EPSILON_GSRC_MONOPOLE_SUBTRACTED_BOUND_GATE_DERIVED_XI_OWNER_EDGE_UNSIGNED_NONCLAIM | 4370 turns epsilon_Gsrc_perp into a sharper coefficient-bound problem. Because the common monopole is subtracted, the far-field source-normalization residual has a zero-monopole geometry factor. For s=R/r, the safe Newton acceleration gate is K_N(s)=min((1-s)^-2, 2s(1-s)^-3), requiring E_perp<=delta_N/K_N(s). The owner-edge route was checked against 4361/1606/4178 and remains unsigned: the measure edge, current/readout edge, same-source-mass edge and no-reentry package do not activate epsilon_Gsrc_perp=0 now. No public local-GR/Newton/PPN claim fires. | 4371-Y5-R2FR-transition-source-worldtube-support-bound-or-measure-owner-edge-proof.md |

## Next target

| next_id | target | question | preferred_route | alternate_zero_route | avoid |
| --- | --- | --- | --- | --- | --- |
| NT4370_0 | 4371-Y5-R2FR-transition-source-worldtube-support-bound-or-measure-owner-edge-proof.md | Can we supply source/worldtube support parameters for the epsilon_Gsrc gate, or prove the measure-owner edge that sets the envelope to zero? | derive/source R/r and E_perp inputs for the Newton/source-normalization gate | try a concrete species-blind measure/Jacobian owner proof | calling the symbolic K_N(s) gate a local-GR pass |
