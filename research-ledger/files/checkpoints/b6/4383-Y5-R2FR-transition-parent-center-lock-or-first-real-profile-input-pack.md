# 4383: parent center lock or first real profile input pack

Marker: `PPC4161_TRANSITION_PARENT_CENTER_LOCK_OR_FIRST_REAL_PROFILE_INPUT_PACK_4383`

## What changed

- Derived the exact conditional parent-center-lock theorem: shared parent center before readout gives `b=0`.
- Built `topological_center_lock_input_runner.py` to compute `c_H`, `c_top`, `b/R`, and envelope scores.
- Smoke-tested centered and shifted profiles.
- Kept all outputs nonclaim until the parent signature or real profile inputs exist.

## Decision

| decision_id | decision | summary | next_target | why_next |
| --- | --- | --- | --- | --- |
| DEC4383_0 | PARENT_CENTER_LOCK_CONTRACT_DERIVED_INPUT_RUNNER_BUILT_AND_SMOKE_TESTED_REAL_VALUES_MISSING_NONCLAIM | 4383 derives the exact parent-center-lock contract: if Hilbert and topological profile representatives factor through one parent source-center functional before readout, then c_H=c_top and b=0, collapsing all 4382 center-offset envelope rows. The parent signature is not yet signed, so 4383 builds the fallback input runner. It computes c_H, c_top, b/R and all envelope scores from profile CSV rows. Synthetic smoke tests verify that identical centered profiles give b/R=0 while shifted equal-monopole profiles produce nonzero b/R and finite envelope scores. Real source inputs and delta_N values remain missing. | 4384-Y5-R2FR-transition-parent-center-functional-proof-or-real-profile-import.md | We now need either the actual parent center functional proof or the first real profile import; both have executable acceptance gates. |

## Next target

| next_id | target | question | preferred_route | fallback_route | avoid |
| --- | --- | --- | --- | --- | --- |
| NT4383_0 | 4384-Y5-R2FR-transition-parent-center-functional-proof-or-real-profile-import.md | Can the parent center functional c[P,W_H,J_H] be proved, or can real profile rows be imported? | prove the parent center functional and factorization lock from source-readout descent/Hilbert-topological profile ownership. | import first real profile CSV or conservative b/R value, then run topological_center_lock_input_runner.py and profile quadrature. | using synthetic smoke rows, coordinate recentering after readout, total charge, metric-nullity, or old q_loc surrogates. |
