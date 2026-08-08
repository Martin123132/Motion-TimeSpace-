# 4389: curvature improvement action adoption or real boundary pairing row

Marker: `PPC4161_TRANSITION_CURVATURE_IMPROVEMENT_ACTION_ADOPTION_OR_REAL_BOUNDARY_PAIRING_ROW_4389`

## What changed

- Derived the full adoption payload for `S_U`.
- Rejected density-only / pure `00` closure.
- Added `curvature_improvement_adoption_gate.py`.
- Kept `S_U` as a construction route, not a local-GR claim.

## Decision

| decision_id | decision | summary | next_target | why_next |
| --- | --- | --- | --- | --- |
| DEC4389_0 | CURVATURE_ACTION_ADOPTION_PAYLOAD_DERIVED_PURE_00_CLOSURE_REJECTED_ADOPTION_GATE_BUILT_NONCLAIM | 4389 tests the curvature-improvement action as a real adoption candidate. The key result is a no-pure-00 theorem: S_U cannot honestly be used only to fix rho_top-rho_H/B_top while ignoring the rest of its Hilbert tensor. Adopting S_U brings momentum, pressure/anisotropy, curvature, boundary, and conservation payloads. The adoption gate therefore requires residual identity, parent U owner, Riemann symmetries, owned metric variation, pre-readout lock, affine boundary pass, curvature bound, pressure/aniso bound, Ward conservation, and visible EM non-double-counting. The current template closes only the EM guard; all other adoption clauses remain open. Therefore S_U remains a promising construction route, not a claim. | 4390-Y5-R2FR-transition-U-action-owner-construction-or-pressure-curvature-bound-row.md | The next useful work is to construct U/action ownership directly or bound the pressure/curvature payload; broad source-hunting has already failed. |

## Next target

| next_id | target | question | preferred_route | fallback_route | avoid |
| --- | --- | --- | --- | --- | --- |
| NT4389_0 | 4390-Y5-R2FR-transition-U-action-owner-construction-or-pressure-curvature-bound-row.md | Can U/action ownership be constructed without hidden pressure/curvature payload, or must those payloads become bound rows? | construct a parent U/Phi sector with Riemann symmetries, residual identity, Ward conservation, and controlled pressure/curvature projections. | fill source-backed bounds for pressure/aniso, curvature remainder, boundary pairings, or import real profiles. | using S_U as a density-only fix, treating phiR/Khat shapes as adoption, or ignoring Bianchi/stress payload. |
