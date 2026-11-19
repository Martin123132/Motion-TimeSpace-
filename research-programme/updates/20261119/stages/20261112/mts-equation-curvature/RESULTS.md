# Equation-derived pressure curvature — paired short-interval test

## Advance

Obtained the missing curvature directly from the retained coupled equations, including metric/rest evolution, scalar self-gravity, actual native clock, massive neutrinos and differentiated background representation defects. No pressure coefficient is fitted. The original preparation is replayed only to acquire missing derivative readouts at its original 902 nodes; no new late-time evolution was run.

The weighted heavy source curvature (density, current, pressure) is

    (0.00786109143877699, 0.0000908248542441416, 0.0003277139150291484).

Unlike the old 6/8-knot estimates, this coefficient is not a difference of sampled source-rate arrays. An independent implementation of the folded A'/self-gravity/rest formula agrees with primitive differentiation. Source values, reconstructed constraints, native field RHS, background spline derivatives and original full-preparation parity pass their unchanged gates. See the two prediction-freeze files and operator-validation.json for the individually labelled checks.

## Frozen predictions against the existing checked history

Original numerical gate: 2e-5; algebra gate: 1e-10. No parameter, grid, preparation or tolerance changes. Predictions were frozen before loading the existing target readout. Earlier exposure of these data is explicit; this is numerical validation, not a new observational holdout.

| Branch / prediction | Density maximum relative residual | Current | Pressure | Verdict including working allowances |
|---|---:|---:|---:|---|
| Cold, first order | 1.9161e-10 | exactly zero | exactly zero | all eight intervals pass |
| Cold, quadratic | 3.4471e-10 | exactly zero | exactly zero | all eight intervals pass |
| Heavy, first order | 8.2347e-6 | 6.8628e-8 | 1.6713e-5 | all eight intervals pass |
| Heavy, quadratic | 1.0415e-7 | 5.9329e-8 | 4.6102e-5 | density/current pass; pressure fails full span |

The quadratic heavy prediction passes the first five consecutive intervals (through elapsed conformal time 0.006165128273863729), then pressure fails at intervals 6–8. Full-span elapsed time is 0.009863972062959192. Those are measured pass/fail locations, not a certified maximum applicability interval. Quadratic density error is about 79 times smaller than first order, but that does not override the pressure failure. Pressure residual plus working allowances is 4.7343e-5; first-order pressure retains a passing 1.7955e-5.

The working allowance includes the previous checked-history budget, initial recapture discrepancy, first-rate replay discrepancy propagated in time, and observed summation roundoff. It is not a rigorous mathematical error bound or a complete uncertainty model. No additional free uncertainty was introduced to obtain a pass.

## Meaning and next step

The previous coefficient-estimation instability is replaced by a directly derived local coefficient, but a constant-curvature expansion is not accurate across all eight intervals. About 65% of its initial pressure curvature is an explicit derivative of the retained background representation defect. This is a concrete sensitivity, not proof that interpolation explains all the discrepancy. The fixed original-node partition and rejected full-span result remain saved.

DERIVATION.md obtains an exact integration-by-parts form that carries these defect terms through time without differentiating them or deleting them. Next evaluate that form, freeze its prediction, and test both branches with the original bank and gates. Preserve the already passing first-order result.

No fits, GitHub, coordinator exchange, galaxy edits or other-chat process changes. Goal remains paused. Final seal and cleanup receipt record validation and exact task-worker exit checks; no worker is intended to continue beyond this stage.
