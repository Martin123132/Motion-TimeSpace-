# 4384: parent center functional proof or real profile import

Marker: `PPC4161_TRANSITION_PARENT_CENTER_FUNCTIONAL_PROOF_OR_REAL_PROFILE_IMPORT_4384`

## What changed

- Proved the Hilbert center is conditionally parent-owned by the Hamiltonian/Hilbert source chain.
- Reduced the remaining topological center obstruction to the exact first-moment residual `B_top`.
- Added `topological_profile_import_validator.py` for real profile imports.
- Confirmed synthetic smoke rows are rejected as claim inputs.

## Decision

| decision_id | decision | summary | next_target | why_next |
| --- | --- | --- | --- | --- |
| DEC4384_0 | HILBERT_CENTER_PARENT_OWNED_CONDITIONALLY_TOPOLOGICAL_FIRST_MOMENT_REMAINS_OPEN_IMPORT_VALIDATOR_BUILT_NONCLAIM | 4384 partially proves the parent-center route: the Hilbert center c_H is conditionally parent-owned by the existing Hamiltonian/Hilbert worldtube chain, but the topological center is not signed. The remaining obstruction is sharpened to an exact first-moment residual B_top=M_H^{-1} int y(rho_top-rho_H)dV. With equal monopoles, b=\|\|B_top\|\|, so b=0 is equivalent to vector first-moment silence, not full profile equality. 4384 also adds a real-profile import validator that rejects synthetic/smoke/placeholder inputs before the center-lock and quadrature runners can be promoted. | 4385-Y5-R2FR-transition-topological-first-moment-zero-proof-or-real-profile-import.md | The next least-circular route is now first-moment zero: prove B_top=0 from topological density ownership or import a real profile. |

## Next target

| next_id | target | question | preferred_route | fallback_route | avoid |
| --- | --- | --- | --- | --- | --- |
| NT4384_0 | 4385-Y5-R2FR-transition-topological-first-moment-zero-proof-or-real-profile-import.md | Can B_top=M_H^{-1} int y(rho_top-rho_H)dV be proved zero, or can real profile rows be imported? | derive topological first-moment silence from parent profile-density ownership, radial/Laplacian representative, or boundary first-moment cancellation. | validate/import real rho_H/rho_top profile rows, then run center-lock and profile-quadrature runners. | using synthetic smoke, total charge, post-readout centering, metric-nullity or same-worldtube charge as first-moment proof. |
