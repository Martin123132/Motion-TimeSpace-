# Native background time derivative: experiment completed

2026-11-09. This stage follows the common-frame background source, retaining the existing action, initial preparation, fullG192, three wave families, baseline/MTS and both metric branches. No observation, parameter, bank, physical grid or tolerance was changed.

## Mathematical progress

Derived the complete moving-frame source derivative
    E_N=T^-1(DeltaF)_N T+[E,T^-1 T_N],
and its distinct observable derivative. The commutator was retained in the implementation. The tests use fixed retained vectors (the saved left-end carried mode plus four seeded probes), not a newly evolved current history. Local native equation derivatives use fourth-order centered stencils at h,h/2,h/4 with equation-integrated phase stencils and unchanged DOP853 tolerances.

Also derived the cancellation-safe heavy-amplitude difference directly from the native equation. Common carrier and conjugate constant terms cancel algebraically. SCALE-REPRESENTATION.md generalizes this identity to the two slightly different represented scale factors rather than forcing them equal. The audit checks both individual native heavy equations using the CDM continuity reconstruction and their differences on all saved stencil/center packets. This is a useful identity, but it does not solve the remaining derivative precision problem.

## Frozen prediction outcome

Predictions were written before the held-out source worker started. The original source index2 was not used to set endpoint values or slopes. It is held out only from this new interpolation test, not from previous theory work or observations.

The MTS phase advances28.506438457954573 radians across the endpoint cell. A cubic between those endpoints is an explicit tested hypothesis, not an adequate phase representation by assumption.

| Family | Source-relative error at interior point, finest derivative | Readout-source relative error | Source error at tiny independent offset |
|---|---:|---:|---:|
| half MTS |0.7469101390 |0.0130663072 |1.9463648883e-5 |
| balanced MTS |0.1594770894 |0.0259950882 |1.2663521903e-5 |
| double MTS |0.3638700483 |0.4319425700 |4.7691419444e-6 |

These are maxima over both branches and all five fixed probes using frozen endpoint-source scales. They are not percentage errors in observed cosmology. All three derivative versions fail the full-cell source and readout interpolation tests at the unchanged2e-5 source-relative gate. Small-offset source tests pass for MTS, but they do not establish derivative convergence or justify interpolation across many oscillations.

The successive derivative-step changes affect the whole-cell source prediction by0.06635 then0.03473 (half),0.005481 then0.003028 (balanced), and0.002701 then0.001312 (double), on the same source scales. The wide-cell failure remains in every tested version; these differences are empirical controls, not rigorous error bounds.

For the carried left-end vector only, the readout prediction discrepancies are4.002e-7,8.879e-7 and7.404e-8 on the earlier physical output scales. That is a different normalization from source-relative interpolation accuracy and is not a propagated-trajectory test.

## Precision result: retain the failure, do not fit around it

The native time derivative has not converged at2e-5. Maximum finest-level step changes for the original MTS source derivative across the two endpoints are0.07640,0.04630 and0.007809. The cancellation-safe heavy component leaves corresponding maxima0.07647,0.04633 and0.007828. It therefore does not materially repair the observed derivative sensitivity; other components, numerical background representation and/or thermal-knot behavior remain possible contributors. This experiment does not isolate a unique cause.

The stable identity is retained as useful algebra, not advertised as a successful precision fix. No frozen prediction was overwritten or post-hoc rescored as pre-test evidence.

## Baseline control

The baseline is checked through the identical endpoint, derivative-step and target procedure. Its background difference is extremely small, as established in the preceding stage. Strict relative derivative/source tests fail; no artificial zero or relaxed gate is imposed.

Some baseline endpoint readout differences are exactly zero at stored precision. Dividing tiny residuals by the defensive1e-80 denominator produces huge finite ratios (~1e63–1e64); these are undefined-in-practice relative measurements, not physical explosions. The carried-vector readout discrepancies on the existing physical scales are at most1.248e-15 in this experiment. The audit records zero endpoint scales and the physical-scale diagnostic separately.

## Coverage, repairs and preservation

audit/result.json passed the reproducibility and bookkeeping checks; it explicitly reports all_interpolation_checks_pass=false and derivative_convergence_proven=false.

Coverage:6 model/family cases,12 endpoints,96 stencil packets,12 held-out/local native packets and6 stable heavy-endpoint diagnostics. Original source seals, fixed predictions, phase controls, independent native-map construction, difference signs, finite-difference coefficients, Hermite predictions, error scales and failed-test flags were checked.

Three failed implementation attempts remain:
1. prepare-half-01: instantaneous context left a narrowed native time window; v2 restores exactly the original authorized window and retains the original domain checks.
2. test-half-01: stale report selector, caught before any held-out evaluation; v3 reads the already-frozen repaired report.
3. cancellation-half-01: exact scale-factor equality was false in an offset packet; the general unequal-scale identity retains that difference instead.

Completed packets were reused where applicable, with hash checks and native-center reproduction. See REPAIRS.md, READ-PATH-REPAIR.md and SCALE-REPRESENTATION.md. Thirteen bounded workers are accounted for:three failed attempts and ten successful runs including the audit. No compiler, subagents, apps, servers, GitHub or unrelated process intervention.

## Decision

Reject the wide-cell cubic as the transport representation. Do not require a high-accuracy numerical derivative of a small operator difference when the desired integral can be evaluated from the original operator values.

NEXT.md derives the phase-resolved variation-of-constants integral. The next calculation should evaluate that integral directly in a small original cell, with phase-resolution controls and the observable map carried consistently. This follows the measured dominant source rather than polishing the insignificant residual feedback.

