# Fixed-background matter interface: results

16 November 2026. The narrow interface test is complete. Previous research,
including the 33 cosmological reports through epoch2924, is unchanged.

## What advances

The retained quark/lepton representation and neutral real bath now have an
explicit small operator-interface implementation, not just a compatibility
table. Three deterministic 4D lattice fixtures pass under strong local gauge
transformations. The corrected replay reads exactly the original saved
fixtures and reproduces all panel and aggregate results exactly.

| Test | Observed result |
|---|---:|
| Maximum tested operator/projector/kinetic/Yukawa identity residual | 3.38812e-15 |
| Frozen identity threshold | 1e-10 |
| Minimum measured Wilson-kernel gap across fixtures/multiplets | 0.995825 |
| Maximum faithful plaquette deviation | 0.0255922 |
| Engineering plaquette guard | 0.1 |
| Maximum baseline action-sum gauge residual | 4.17659e-16 |
| Maximum neutral-bath-plus-matter action-sum residual | 2.61169e-16 |
| Independent free Fourier-spectrum relative error | 1.02501e-15 |

There are115 checks per fixture (345 total), plus the independent Fourier and
center-defect controls. This count is implementation coverage, not345
independent physical predictions. The operator/kernel "gap" is not a
particle or interacting Yang–Mills mass gap.

Baseline and MTS here mean the two synthetic fixed-geometry interfaces
described in METHOD.md, NOT reruns or new fits of the cosmological histories.
Their dimensionless fixture coefficients do not calibrate any physical input.

## Failure controls give real information

1. Wrong uc hypercharge gives0.0541–0.2376 Yukawa discrepancy; wrong color
   conjugation gives0.1085–0.3104. Both are well above the frozen1e-6
   detection floor.
2. Keeping the old projector while changing the gauge fields gives
   0.5363–0.5601 projected-field errors. Projector covariance must be carried
   through the matter implementation, not merely asserted for the links.
3. A single center-valued link produces faithful plaquette deviation1,
   while its SU(5)-image deviation is3.88578e-16. Thus the image-only
   criterion would accept a defect that our q=1 faithful guard rejects.
   This is an explicit reason to preserve the global-group distinction.
4. Rotating one allowed fermion basis vector changes the reduced determinant
   phase by the chosen0.37 radians while preserving its magnitude. Operator
   covariance alone has not supplied the compensating integration-measure
   phase. No such current is implemented in this stage.
5. The intentionally unstable bath has eigenvalue-0.0980712 after the
   representation repair; it is correctly rejected.

## A caught implementation error, preserved

The original root result.json is FALSE. All three initial panels failed the
unstable-bath negative control. Integer storage had truncated the intended
off-diagonal couplings0.4 and0.25 and the small unstable diagonal to zero.
This also made the original positive bath fixture wrong. The independent
failure control exposed what the shared edge/matrix action check could not.

The sole physics-arithmetic repair is an explicitly floating-point bath mass
matrix. The exact same cached inputs and unchanged parameters/thresholds were
replayed. Two additional guards check that the fractional couplings survive
and that det(M2)=prod(Omega_j^2) times its Schur complement. The corrected
positive bath has Schur complement1.9341667, smallest mass eigenvalue1.8420353,
and determinant29.0125. These are synthetic fixture values only.

REPAIR.md explains the output-path adaptation and cached-input reuse.
The old code, logs, panel reports, fixtures and failed status remain intact.
Authoritative status: float-bath-repair/result.json; identical replay:
float-bath-repair/replay-result.json. No cosmological implementation was
altered by this local prototype repair.

## Scientific interpretation

The test supports using the already adopted matter content with the selected
neutral bath at a fixed flat Euclidean regulator level. The derivation of
the transformation laws is in METHOD.md. It does not turn the original motion
field into a new electrically charged field, infer SM particle choices,
or substitute a different cosmology.

This is an operator and coefficient-tensor test. The holomorphic Yukawa
tensors have been checked using commuting probes of their multilinear
coefficients; the full Grassmann integration, independent barred-field
conjugate terms, measure-current phase, global-loop transport and continuum
construction are distinct tasks. The prior external-theorem assumption stays
explicit. The numeric plaquette guard is an engineering choice, not a
certified numerical admissibility threshold for Craig's theorem.

## Next bounded step

Finish this small interface by defining the independent barred Yukawa terms
and deriving/testing its gauge-current Ward identity under a local variation.
Keep the measure Jacobian separate from the classical action identity.
Then decide how that verified interface informs the retained common-metric
stress coupling before any larger lattice calculation. Do not turn this into
a replacement-framework project or automatically extend the cosmological
window: epoch2924 is still the completed preselected horizon.

No GitHub, handoff, subagents, new datasets or continuing workers. Goal stays
paused; subsequent work needs Martin's next manual instruction.
