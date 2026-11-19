# Selected-segment integration result — 2026-11-09

## What moved forward
The identified heavy scalar background-flow contribution is now tested using integration aligned with its saved DOP853 polynomial segments. All four selected MTS segments pass the unchanged numerical comparison, with the physical background, source bank, preparation, histories, grids and tolerances preserved. We did not set a flow residual to zero or replace a background derivative by the field equation.

This isolates a practical repair route: integrate the same identified contribution accurately, then add it back to the rest of the existing source. A separate saved-data calculation shows that the remainder's quadrature changes are already below the fixed threshold for the four previously flagged MTS combinations. That is a feasibility result, not permission to discard the contribution.

## Frozen scope and numerical results
- MTS: segments2697,2749,2802,2854;132nodes. Four of158segments, covering **1.5317814154904217%** of this original source cell's N-length (first/last are clipped).
- Baseline: both segments26,27;66nodes, covering the entire same baseline source cell.
-198source nodes total;four old endpoint packets reused,194new point evaluations. No physical history integration, new compiler, subagent or GitHub action.
-9/17/33nested nodes per segment, fixed before source evaluation; two metric branches and Pi/delta_massless outputs.
-Current-history, phase-history, phase/current cross and both adjoint controls remain explicit.
-Fixed gates: algebra1e-10, numerical2e-5. The numerical figures below are divided by the **original whole-cell conditional source budget**, not by the small segment contribution.

| Model / isolated part | Largest 17−9 change / budget | Largest 33−17 change / budget | Largest summed numerical indicator / budget | Segment/branch/channel checks |
|---|---:|---:|---:|---:|
| MTS native conservative part |1.0556269409917747e-8|2.4796012295324976e-10|3.5033186376686603e-10|16/16|
| MTS heavy flow |1.615988949962867e-10|5.0414159919863906e-11|5.103243809808887e-11|16/16|
| MTS slow flow |3.5496155138108397e-38|5.2208135708334e-38|5.739813255612914e-38|16/16|
| MTS residual |1.767624282055694e-10|8.292170096464796e-11|2.6568231062975577e-10|16/16|
| Baseline native conservative part |9.946055891464586e-5|6.742333831053775e-5|6.742333870352151e-5|6/8|
| Baseline slow flow |1.2737405992959868e-30|1.4896488664602063e-30|1.4896489588418205e-30|8/8|
| Baseline heavy flow (absent field) |0|0|0|8/8|
| Baseline residual |2.4438349280601405e-6|1.2323841622515074e-6|1.2323841624207833e-6|8/8|

These are measured refinement/control indicators, not rigorous continuum bounds or independent observations. Tiny terms need not exhibit monotonic relative contraction. The baseline's two failures are Poisson-spatial Pi conservative contributions in segments26and27; they remain flagged. The largest baseline numerical indicator is2.548459526256143e-19 of the existing physical reference scale. This tiny absolute scale does not turn a failed relative criterion into a pass.

## Derived composite route
The source identity permits
```
I_hybrid = Q_old(S - S_heavy_flow) + Q_segment(S_heavy_flow).
```
The heavy-flow term MUST be added back over all158segments before any candidate can replace the old integral. Existing native approximations and the remaining source coordinates remain intact.

Independent90-digit contraction of the old full-grid remainder gives these quadrature changes / original budget:

| Branch | Pi | delta_massless |
|---|---:|---:|
| GR |−5.267973544781917e-6|−3.511605634661774e-6|
| Poisson-spatial |−3.2216699200149435e-6|−2.142807918655891e-6|

Each is below2e-5. This identifies a bounded job with an explicit success criterion; it does not yet test the sum with a fully integrated heavy-flow term or settle other error terms. For baseline the heavy term is identically absent, so this identity makes no improvement to its old full-cell flags.

## Arithmetic repair and independent checks
The original freeze's floating midpoint slightly changed the interval represented by its moment equations. The independent exact-interval check found a maximum moment error3.0032406005027055e-10, above the algebra gate. Before using any weights in final integration, a separate immutable supplement derived weights from the exact binary endpoints and the **same frozen nodes**. No source outcomes enter the weights. The independent90-digit Legendre moment residual is now<=8.695616576309867e-16. Original weights remain recorded, unused in final projection; this is not a tolerance relaxation.

-The native alternating polynomial derivative agrees with an independently expanded power polynomial to<=1.7001138745596743e-16 in its stated normalized scale.
-Independent90-digit scalar-flow arithmetic covers3168field cases; values agree when rounded to binary64. This is an arithmetic check on saved native inputs.
-The18-point probe's independent forward/transpose observable-map error is<=9.520991011826685e-16. Full-audit forward_map_error=0 is an unperformed full-map-test placeholder; the actual map check was the probe, not all198points.
-All4752stored mapped component cases have their branch/current/observable binding checked.
-Independent90-digit quadrature summation agrees within3.669570390563365e-14 relative to the resulting integral.
-All nine numerical workers exited0. Exact cleanup and artifact seal are recorded separately; no other chat's processes were stopped.

## What remains authoritative
Old completed stages and source packets are untouched. Original full-cell MTS16/20 and baseline0/20source-case status is not promoted by this selected-segment diagnostic. This test covers the balanced family and original source8->12 only. Read NEXT.md for the full-cell calculation and controls needed next.

## Evidence
Within this folder: DERIVATION.md; RECOVERY.md; balanced/freeze-01/result.json; balanced/exact-weights-01/result.json; probe-audit/result.json; full-audit/result.json; balanced/projection-01/result.json; integration-audit/result.json; balanced/composite-feasibility-01/result.json; per-point receipts; CLEANUP.json; closeout.json.

Inherited authoritative inputs are recorded with absolute paths and hashes in these receipts. Immediate parent: ../mts-direct-monopole-metric-source-20261109, seal d4dfc5819407839480dff54a01b96e9fc6fa48de172858e067fa66c4ca8e98c3.

