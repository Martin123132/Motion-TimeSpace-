# 5264 — Occupation-separated Laurent residue and boundary completion

## Purpose

Checkpoint 5263 reached generation 9 with intact topology, closure, and R96/R128/R512 convergence, but one E040 residue row failed the finite-window log-slope gate.
The failure occurred because the dynamic winding boundary forced the real-axis fit radius below the pole's imaginary displacement. This checkpoint separates two logically distinct objects: the analytic Laurent residue of the bare component and the integer contour-occupation multiplier.

## Derived local rule

For an active owner channel `D_X(z)` and component `F_X(z)`, define `N_X(z)=D_X(z)F_X(z)`. If `D_X(z_X)=0`, `D'_X(z_X) != 0`, `N_X` is analytic and `N_X(z_X) != 0`, then the pole is simple and `Res(F_X,z_X)=N_X(z_X)/D'_X(z_X)`.
The dynamic winding multiplier is held constant while fitting this analytic local object. It is then used only as the independently certified contour occupation. The real integration patch remains capped inside the dynamic interval, so the continuation does not smear a winding step across the real contour.

## Numerical gates

- Minimum complex-pole coverage ratio: `1.25`.
- Minimum nested certifying fits: `2`.
- Nested residue relative-spread limit: `0.0005`.
- Root normalized-residual limit: `1e-08`.
- Derivative relative-residual limit: `5e-05`.
- Root-refinement shift-ratio limit: `0.001`.
- Dynamic patch margin factor: `0.8`.

## Result

- Validation passed: `True`.
- Completed generation: `10`.
- Total certified nodes: `27`.
- Maximum parent-to-repaired physical shift: `6.415778242136025e-06`.
- All boundary stopping gates passed: `True`.
- Formalization-workbench modified files: `0`.
- Decision: `ADOPT_OCCUPATION_SEPARATED_LAURENT_RESIDUE__HANDOFF_TO_OUTER_COEFFICIENT_REASSEMBLY`.

## Claim boundary

This checkpoint certifies the targeted topology-boundary location budget and the local residue treatment used in that calculation. It does not by itself establish the numeric UV coefficient, local GR, or the full MTS theory.
