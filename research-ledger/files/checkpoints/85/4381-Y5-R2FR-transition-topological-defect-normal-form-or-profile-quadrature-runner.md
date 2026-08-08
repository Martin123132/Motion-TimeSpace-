# 4381: topological defect normal form or profile quadrature runner

Marker: `PPC4161_TRANSITION_TOPOLOGICAL_DEFECT_NORMAL_FORM_OR_PROFILE_QUADRATURE_RUNNER_4381`

## What changed

- Wrote the normal-form theorem bundle for the topological defect route.
- Added `profile_topological_moment_quadrature.py`, a reusable l<=2 moment runner.
- Generated synthetic smoke input/output to verify radial zero-monopole silence and shifted-profile dipole detection.
- Kept all rows nonclaim until a parent normal form or real source profile is supplied.

## Decision

| decision_id | decision | summary | next_target | why_next |
| --- | --- | --- | --- | --- |
| DEC4381_0 | NORMAL_FORM_THEOREMS_SHARPENED_PROFILE_QUADRATURE_RUNNER_BUILT_AND_SMOKE_TESTED_NONCLAIM | 4381 turns the 4380 fork into two executable routes. The proof route is now a normal-form theorem bundle: direct radial zero-monopole defect, common-center isotropy plus charge equality, or Laplacian boundary-silent defect. The fallback route is now a real CSV quadrature runner for l<=2 spherical moments using the 4378 E_l^top conventions. Smoke tests show the runner kills a radial zero-monopole shell and detects a dipole from separately centered equal-monopole profiles. Current MTS parent normal form and real profile inputs remain missing, so all claim gates stay false. | 4382-Y5-R2FR-transition-topological-profile-source-acquisition-or-parent-normal-form-signature.md | We can now either sign a parent normal form or feed a real rho_H/rho_top profile into the runner; no more vibes-only moment rows. |

## Next target

| next_id | target | question | preferred_route | fallback_route | avoid |
| --- | --- | --- | --- | --- | --- |
| NT4381_0 | 4382-Y5-R2FR-transition-topological-profile-source-acquisition-or-parent-normal-form-signature.md | Can a real parent normal-form signature or a real source profile be supplied for delta rho_top? | prove raw topological defect is radial zero-monopole/common-center isotropic/laplacian-null from parent source construction. | ingest first real rho_H/rho_top profile or conservative analytic envelope and run profile_topological_moment_quadrature.py. | using synthetic smoke output, old q_loc surrogates, total charge, metric-nullity or post-hoc centering as evidence. |
