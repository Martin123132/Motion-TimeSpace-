# 4387: double-divergence improvement parent owner or boundary row

Marker: `PPC4161_TRANSITION_DOUBLE_DIVERGENCE_IMPROVEMENT_PARENT_OWNER_OR_BOUNDARY_ROW_4387`

## What changed

- Derived the covariant improvement owner shape `Delta T = nabla nabla U`.
- Mapped its weak-static density projection to the `S^{ij}` double divergence from 4386.
- Audited the birth-certificate clauses and kept them unsigned.
- Added `double_divergence_boundary_gate.py` for future source-backed affine boundary rows.

## Decision

| decision_id | decision | summary | next_target | why_next |
| --- | --- | --- | --- | --- |
| DEC4387_0 | COVARIANT_IMPROVEMENT_OWNER_SHAPE_DERIVED_BIRTH_CERTIFICATE_FAILS_BOUNDARY_GATE_BUILT_NONCLAIM | 4387 derives the covariant owner shape behind the 4386 double-divergence mechanism. A Hilbert/Noether stress improvement has leading local form Delta T^{mu nu}=nabla_alpha nabla_beta U^{mu alpha nu beta}; in the weak-static Newtonian source limit this gives Delta rho=c^{-2}partial_i partial_j U^{0i0j}. That would birth the S^{ij} required by 4386 if and only if the parent action identifies rho_top-rho_H with that improvement before readout and the affine boundary pairings vanish. Existing dB_impr notation and the old Khat improvement route support the mathematical species but do not birth-certify the actual topological residual. So 4387 builds a boundary-pairing gate for source-backed rows and keeps the route nonclaim. | 4388-Y5-R2FR-transition-improvement-birth-certificate-source-hunt-or-boundary-row-fill.md | The next real move is either source-hunt the U/S birth certificate or fill source-backed boundary-pairing rows; generic improvement language is no longer enough. |

## Next target

| next_id | target | question | preferred_route | fallback_route | avoid |
| --- | --- | --- | --- | --- | --- |
| NT4387_0 | 4388-Y5-R2FR-transition-improvement-birth-certificate-source-hunt-or-boundary-row-fill.md | Can a source file birth-certify U/S as the actual rho_top-rho_H owner, or can source-backed boundary pairings be filled? | search/derive a parent action clause where the topological/Hilbert residual is exactly the Newtonian density projection of an improvement superpotential. | fill real boundary-pairing rows for constant and linear affine tests, or import a real profile through the affine runner. | claiming from dB_impr notation alone, old Khat improvement shape alone, generic superpotential words, synthetic boundary smoke, or total charge. |
