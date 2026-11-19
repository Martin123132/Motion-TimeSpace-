# Cold analytic phase control — verified 2026-11-08

## What changed physically
The retained relative-phase, matter and metric equations now have an explicit rational phase representation. Their unsampled fast-phase tail can be bounded from the source equations, rather than guessed from a decaying FFT or a larger grid.

The source has degree-one stress/free-generator/injection terms and degree-two solved-metric numerators. The scalar/metric coordinate inverses remain explicit. Including their derivatives and the physical weight gives a common denominator of degree at most12 and numerator of degree at most15. The full retained G192 hierarchy remains present.

This is a derivation and qualification of the existing MTS branch, not a replacement theory or new fit. The original bank, physical grids and tolerances are unchanged.

## Uniform result on the saved cold window
Using the inherited background tube and positive-energy/positive-quadrature inequalities, all required inverse maps and the physical phase clock are pole-free on the complex annulus 1/16<=|exp(2i theta)|<=16 throughout the cold window a=[0.36273334952836184,0.46575884027469494].

The largest contraction bounds over all three wavelengths/branches are:
- Scalar periodic-map contraction:3.869485e-5.
- Normalized metric-denominator contraction:5.776654e-5.
- Closed metric-feedback contraction:8.996926e-9.
- Clock contraction:1.000653e-7.

Each is well below1. These are analytic tube bounds, not maxima of phase samples. They exclude singular coordinate/metric inverses in this domain; they are not a claim that gravity is negligible.

## Tested source and analytic truncation
All three inherited wavelengths are checked at both cold endpoints and the saved midpoint, for baseline and MTS, with GR and spatial-Poisson rows retained separately.

- 27 independent native MTS phase points, both gravity branches; predictions frozen first.
- 27 baseline phase-independence comparisons, exactly zero.
- 108 complex-phase branch fixtures check the analytic norm/inverse bounds.
- Seven exact symbolic identities check metric rearrangements, quotient differentiation and the affine source used in the bound.
- Independent denominator multiplication checks the degree15 numerator; worst forbidden-mode residual1.527121e-16 relative.

Across those coefficient states, the derived exact-arithmetic256-point generator interpolation tail bound is at most1.082e-139. This does NOT mean140-digit numerical precision: native arithmetic and source-jet accuracy are separate, much larger contributions. The point of the bound is to establish that unrepresented analytic phase harmonics are not the limiting error at these states.

The exact clock denominator is included in the mean quadrature ratio bound. Integrating sampled forcing has its own alias bound, rather than silently using the interpolation bound for the primitive itself. Corrected authoritative bounds are in audit/result.json.

## Numerical error checks — unchanged gates
- Saved midpoint generator agreement:2.452986e-15 relative.
- Saved clock mean agreement:3.054241e-16 relative.
- Saved periodic primitive agreement:4.045941e-13 relative.
- Held-out generator/native-adapter agreement:1.228052e-15 relative.
- Independent native scalar coefficient residual:3.379053e-7 absolute.
- Independent analytic continuation agrees on the real phase circle to2.300107e-16 relative.

The full generator's large streaming entries would make slow-jet refinement look artificially tiny. A separate direct jet test avoids that normalization:
- Background numerator derivative refinement:8.501702e-10 relative.
- Background denominator derivative refinement:3.444422e-6 relative (closest to the2e-5 gate).
- Energy-direction denominator derivative refinement:4.091236e-7 relative.
- Physical metric-rate refinement:2.542806e-14 relative.

All pass the original2e-5 numerical and1e-10 algebra gates applicable to their respective checks. Source finite-degree qualification is1.890361e-11 relative. No tolerance changes or failed worker attempts.

## What this makes possible next
The phase-control obstacle is now reduced to explicit source algebra and bounded inverses. Next use their sensitivity formulas to carry the saved slow-background tube and source-jet uncertainty into a uniform coefficient/remainder envelope over the cold interval. Endpoints and midpoint alone do not supply that envelope.

Then transport the retained original perturbation preparation with both physical endpoint maps, using the previous useful logarithmic norm rather than the very conservative analytic norm. Compare GR and spatial Poisson in a common physical frame; do not invent a late initial mode or identify the analytic tail with the total history error.

## Reproducibility and receipts
- DERIVATION.md: source degree, rational denominator, weighted Fourier bounds, whole-tube inverse bounds and sensitivity formulas.
- analytic_math.py: accepted source representation and corrected bounds.
- collect_analytic.py: frozen source/prediction construction and native/baseline qualification.
- check_analytic.py: independent symbolic, complex-phase, degree and hash audit.
- check_slow_jets.py: independently normalized derivative refinement.
- audit/result.json and jet-check/result.json: authoritative validation outputs.
- Each label/analytic-01/: source coefficients, frozen predictions and retained receipts.
- EXECUTION-NOTE.md and analytic_math_initial.py: exact imported source for the half-family worker; only the reporting bound changed while it ran. The final audit recomputes every bound from the accepted packets, and verifies operator construction is unchanged.
- CLEANUP.json and closeout.json: final process and artifact receipts.

Everything remains local. Prior checkpoints are intact. All owned numerical workers exit before sealing.
