# 4385: topological first-moment zero proof or real profile import

Marker: `PPC4161_TRANSITION_TOPOLOGICAL_FIRST_MOMENT_ZERO_PROOF_OR_REAL_PROFILE_IMPORT_4385`

## What changed

- Derived the finite affine condition for `B_top=0`: annihilate `1,x,y,z`.
- Proved radial/inversion-even zero-monopole and affine Laplacian-boundary routes.
- Rejected generic exact divergence as insufficient for first-moment silence.
- Added `topological_affine_first_moment_gate.py` and smoke-tested it on locked vs shifted profiles.

## Decision

| decision_id | decision | summary | next_target | why_next |
| --- | --- | --- | --- | --- |
| DEC4385_0 | AFFINE_FIRST_MOMENT_THEOREM_DERIVED_PARENT_SIGNATURE_UNSIGNED_RUNNER_BUILT_NONCLAIM | 4385 proves the minimal first-moment law for the separated-center branch. Full distributional profile equality is not required to kill b; it is enough for the residual density operator D_top-H to annihilate the four-dimensional affine test space {1,x,y,z}. Radial or inversion-even zero-monopole defects are exact sufficient conditions, and the Laplacian route only needs Green boundary silence for the same affine tests. A generic exact divergence is rejected as insufficient. The parent signature remains unsigned, so 4385 adds an affine first-moment runner that computes Delta_M, B_top and B_top/R from profile rows and verifies the existing smoke profiles: locked rows give zero, shifted equal-monopole rows are detected. | 4386-Y5-R2FR-transition-affine-annihilator-parent-signature-or-real-profile-row.md | The least-circular next move is to parent-sign the affine annihilator or feed one real profile row through the validator and affine runner. |

## Next target

| next_id | target | question | preferred_route | fallback_route | avoid |
| --- | --- | --- | --- | --- | --- |
| NT4385_0 | 4386-Y5-R2FR-transition-affine-annihilator-parent-signature-or-real-profile-row.md | Can the parent action sign D_top-H in Ann(Aff_1(W_H)), or can a first real rho_H/rho_top profile row be imported? | derive the affine annihilator from parent translation/no-marker/source-center symmetry or Laplacian affine boundary silence. | import one real source-backed profile through the validator, then compute Delta_M and B_top/R with topological_affine_first_moment_gate.py. | requiring full profile equality when only center lock is being tested; or claiming from total charge, generic exact divergence, synthetic smoke, or post-readout recentering. |
