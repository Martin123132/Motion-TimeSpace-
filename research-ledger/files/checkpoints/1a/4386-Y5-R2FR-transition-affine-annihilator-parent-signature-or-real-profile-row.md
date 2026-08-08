# 4386: affine annihilator parent signature or real profile row

Marker: `PPC4161_TRANSITION_AFFINE_ANNIHILATOR_PARENT_SIGNATURE_OR_REAL_PROFILE_ROW_4386`

## What changed

- Derived the double-divergence improvement route `rho_top-rho_H=partial_i partial_j S^{ij}`.
- Proved why it kills affine tests under boundary silence.
- Kept the single-divergence/superpotential shortcut rejected.
- Added synthetic smoke showing double-difference affine silence versus single-difference first-moment leakage.

## Decision

| decision_id | decision | summary | next_target | why_next |
| --- | --- | --- | --- | --- |
| DEC4386_0 | DOUBLE_DIVERGENCE_IMPROVEMENT_ROUTE_DERIVED_SINGLE_DIVERGENCE_REJECTED_PARENT_UNSIGNED_NONCLAIM | 4386 finds the cleanest mechanism so far for the affine-annihilator gap: if the topological/Hilbert residual density is a parent-owned double divergence partial_i partial_j S^{ij}, then it kills constants and linear test functions whenever the affine boundary pairings vanish. This is strictly stronger than generic divergence/superpotential language and avoids the previously rejected shortcut: a single divergence can have zero total charge but nonzero first moment. The synthetic smoke confirms this boundary: a second-difference profile has B_top/R=0, while a first-difference counterexample has nonzero B_top/R. The route is not claimed, because current files do not birth-certify S^{ij} as the actual rho_top-rho_H owner or prove the required boundary silence. | 4387-Y5-R2FR-transition-double-divergence-improvement-parent-owner-or-boundary-row.md | The next useful attack is a parent birth certificate for S^{ij} or a real boundary/profile row; not another generic superpotential sweep. |

## Next target

| next_id | target | question | preferred_route | fallback_route | avoid |
| --- | --- | --- | --- | --- | --- |
| NT4386_0 | 4387-Y5-R2FR-transition-double-divergence-improvement-parent-owner-or-boundary-row.md | Can the parent action identify rho_top-rho_H as a double-divergence improvement with silent affine boundary pairings, or must we fill boundary/profile rows? | derive S^{ij} from a parent stress-improvement/topological density birth certificate tied to rho_top-rho_H before readout. | create source-backed boundary-pairing rows BP4386_0/BP4386_1 or import a real profile through the affine runner. | generic superpotential claims, single-divergence shortcuts, total-charge-only arguments, synthetic smoke promotion, or post-readout profile recentering. |
