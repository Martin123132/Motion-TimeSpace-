# Exact cold coupled phase derivatives — verified 2026-11-08

## What moved forward

The complete metric and physical-coordinate-map derivatives are now calculated directly from the retained source equations. This removes the fourth-order numerical slow derivatives from the new coupled generator without changing the cold background, baseline, matter bank, grids, initial preparation or tolerances.

The second derivative of the finite-source quadrature defect is derived explicitly, including the previously detected tiny normalization differences. This closes the additional derivative needed by the spatial-Poisson branch. The full GR momentum identity and its inherited baryon-pressure term remain intact.

A second advance is an exact, cancellation-factored coupled generator. With metric readout L, injection F, free generator G, periodic map T, physical affine map W and physical forward map S,

    A = T^-1(G T-T_N) + T^-1[(G W-W_N+F)L-W(L_N+L G+L F L)]S.

This is algebraically equal to the direct physical pullback R(G+FL)S+R_N S. It cancels the leading rapid micromotion before assembling the full matrix, while keeping all matter/metric coupling. DERIVATION.md supplies the derivation and assumptions.

## Checks with the original gates

Both saved baseline and MTS are checked at the three inherited wavelengths, three saved cold epochs and both gravity branches. ALGEBRA=1e-10 and GATE=2e-5 are unchanged.

- 54 native model/phase cases, covering 108 gravity-branch comparisons. Largest coupled-generator difference: 3.275091e-9 absolute, 5.714819e-13 relative. The separate native scalar conversion residual is at most 4.339689e-7, also below its existing gate.
- Exact slow metric derivatives agree with the saved fourth-order derivatives within 1.533332e-9 relative. Slow plus phase derivatives reproduce the total derivative within 4.720006e-16 relative; the small slow derivative is tested separately rather than hidden beneath the fast phase term.
- 108 saved-point direct/factored comparisons: largest absolute discrepancy 3.773649e-13; physical inverse-map identity residual at most 1.629563e-16.
- Four exact symbolic finite-Fermi identities and 90 independent source-derivative checks. There are 36 independent 70-digit metric/map fixtures, using unsimplified momentum equations, direct map inversion, complex-step refinement and independently inverted thermal interpolation. The audit counts 32,832 value/rate entry comparisons, including both step sizes.
- 24 direct/factored high-precision generator comparisons, including baseline controls. Largest discrepancy from the 70-digit reference: 1.818990e-12 absolute, 3.054240e-16 relative.
- 1,536 branch/node cancellation comparisons on the original 256-node midpoint phase grids. Worst relative discrepancy 3.154159e-16.

These are equation/implementation checks, not observational significance or measured cosmological precision. The tiny high-precision derivative residuals do not certify the underlying thermal continuum or global integration error.

## Saved phase result preserved

The midpoint generator, time-weighted phase mean and zero-mean periodic primitive were recomputed using the new exact jets and factored cancellation. Against the saved result, the largest relative changes are:

| Quantity | Relative difference |
| --- | ---: |
| phase-grid generator | 2.576252e-13 |
| time-weighted mean | 2.574725e-13 |
| periodic primitive | 3.143566e-13 |

The baseline remains exactly phase-independent in these tests. Periodic closure/derivative residuals are at most 2.131877e-12 relative, below the original algebra gate.

The physical mean's midpoint logarithmic norm remains approximately 0.0641–0.06491 across the six wavelength/branch cases. The sampled periodic primitive Frobenius norm is about 5.574e-9. These are midpoint/sampled diagnostics, not newly asserted whole-history bounds or observational percentages.

## Reuse and provenance

- `source_laws.py`, `tangent.py`: retained source laws and directional differentiation.
- `coupled_jets.py`, `stable_coupled.py`: direct and cancellation-factored physical generators.
- `half`, `balanced`, `double` / `jets-01`: frozen predictions and native tests.
- `stable-validation` and `independent-validation-02`: accepted algebra and 70-digit checks.
- Each wave family / `average-01`: retained midpoint mean, periodic primitive, baseline control and phase bank.
- `audit/result.json`: accepted source hashes, counts, extrema and gate checks.
- `EXECUTION-NOTE.md`: two preserved validation/diagnostic implementation failures and the narrowly scoped repair. Neither changes a physics formula or tolerance.
- `CLEANUP.json`, `closeout.json`: worker cleanup and artifact integrity receipt, produced after acceptance.

Only the inherited core plus first two massive-tail levels are used for the new coupled coefficient comparison; the already-qualified full G192 free source and its envelope are reused. Native UFA/full hierarchy choices and the saved thermal source remain explicit. No new data fit, late initial mode, action substitution, GitHub action or heavy-background rerun occurs here.

## Next physical calculation

Use the factored formula to propagate the inherited background/clock uncertainty through the COMPLETE coupled generator. Its exact directional derivatives now supply the previously numerical part of that calculation. Keep the shared-variable cancellations, combine with the existing physical logarithmic-norm and averaging-remainder control, then transport the original early preparation through the cold interval with both physical endpoint maps. Carry source replacement, phase averaging and global integration errors as separate contributions.
