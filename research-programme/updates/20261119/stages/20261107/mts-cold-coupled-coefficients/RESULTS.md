# Cold relative-phase coefficients — verified 2026-11-08

## Advance
The retained coupled relative-scalar/matter/metric generator now evaluates on the saved cold background, rather than only the early resolved background. It uses the saved scalar state and clock, derived canonical scalar equations, native matter/thermal coefficients and the original G192 hierarchy. Both baseline/MTS and GR/spatial-Poisson controls pass.

No new perturbation initial condition, late microscopic phase, fitted coefficient, bank, physical grid or tolerance was introduced.

## Evidence
- 768 MTS phase-coefficient points: 256 at each of the three inherited wavelengths, with baseline controls.
- Three saved cold epochs, three independent phase angles, both models and both gravity branches: 324 full G192 vector checks.
- Nine midpoint phase predictions frozen before evaluation.
- Five exact symbolic identities: scalar density/current derivatives, two gauge-column cancellations and carrier-rate cancellation.
- Algebra gate 1e-10; numerical gate 2e-5, unchanged.

Final audit: audit/result.json. Largest residuals:
| Check | Maximum |
|---|---:|
| Independent canonical/native heavy rows, absolute coefficient | 5.177234e-7 |
| Independent endpoint heavy rows, absolute coefficient | 4.370256e-7 |
| Frozen midpoint matrix prediction, absolute entry | 3.725290e-9 |
| Native full-core/vector relative error | 6.781411e-13 |
| Native G192 tail relative error | 8.907650e-16 |
| Independent inverse-map derivative, absolute entry | 1.036353e-5 |
| Physical-clock mean refinement, absolute entry | 1.303852e-8 |
| Periodic primitive refinement, absolute entry | 1.939501e-18 |

The derivative check is the closest to its gate. It passes but is not a rigorous continuum error bound. A relative full-vector residual is not the same metric as an absolute individual coefficient residual; both are reported.

## Physical content
At the cold midpoint, mu=am/H is approximately 2.822798e8 and the heavy self-gravity coefficient b=rho_h/(2H²) is approximately 0.6330844.
The pressure contribution alpha²/4 is 1.541873e-5, 2.466996e-4 and 3.947194e-3 at half/balanced/double k respectively. The leading W–delta entry is alpha²/4-b: pressure and attractive gravity both remain, rather than imposing pressureless behavior.

The physical-clock means retain the other matter and metric feedback. These matrix entries are not new observations or a fitted growth prediction.
The cold window is a=[0.36273334952836184,0.46575884027469494], selected previously from kinematics, not from these comparison results.

## What was fixed
The original scan failed with a spurious coefficient residual of 244.62.
We traced and repaired separate numerical issues:
1. Large carrier/gauge terms canceled only after rounding. The coordinate derivative was simplified exactly and independently checked with 70-digit arithmetic.
2. The source-owned Fermi background and native thermal representation differed at about 1e-13 in H at the midpoint. Native comparisons now use a consistent native H/enthalpy, with a separately gated representation shift and the unchanged saved scalar/clock state.
3. Native scalar stress derivatives expanded canceling oscillator terms. The isolated native API now evaluates the exactly derived D'=-H(D+3P)-kQ-kzv² and Q'=-2HQ+kP instead.
4. A one-ulp endpoint overshoot was replaced by the exact saved endpoint. Six passing early controls from that attempt were reused, not rerun.

These are algebraic/representation repairs, not relaxed tolerances. Failed and diagnostic attempts remain in place; see DEVELOPMENT-FILES.md. Original libraries and checkpoints are unchanged.

## Retained uncertainty and next calculation
At the midpoint the saved heavy-background budget includes a clock error of about 0.0170831 Mpc in conformal units, H error about 1.53753e-10 Mpc^-1 and heavy-density log width about 3.18218e-6. These are retained, not replaced by the much smaller code-comparison residuals.

Next: derive/evaluate the cold primitive drift D_sigma Q f and controlled remainder
E=(I+Q)^-1[BQ-Q Bbar-D_sigma Q f], include background-replacement uncertainty and endpoint maps, then transport the original early preparation through matched GR/spatial-Poisson evolution. No reset late adiabatic mode.

## Locations
- DERIVATION.md: equations, adapter and precision reasoning.
- half/cold-midpoint-02, balanced/cold-midpoint-02, double/cold-midpoint-02: accepted phase banks, generators and means.
- half/independent-02, balanced/independent-02, double/independent-02: accepted independent controls and frozen predictions.
- half/qualification-03/result.json: final adapter qualification.
- summary/identities-01/result.json: exact identities.
- build-canonical-stress/build-result.json: accepted native binary and immutable input hashes.
- audit/result.json: final independent recomputation and integrity checks.
- compiler-cleanup.json and CLEANUP.json: exact task-process cleanup receipts.
- closeout.json: artifact manifest and checksums.

All work remains local. No GitHub action. No unrelated process was stopped.
