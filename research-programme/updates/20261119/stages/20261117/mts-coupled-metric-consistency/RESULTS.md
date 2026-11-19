# Common-metric pressure consistency: completed test

Date: 2026-11-17. Private work; no GitHub action. Authority: metric-result.json, control-identity-result.json, verification.json and closeout.json. Read DERIVATION.md together with DIMENSIONAL-CLARIFICATION.md.

## What advanced

The previously accepted coupled background, perturbations and surrounding species now have a direct common-metric consistency test. Density/current-derived metric time derivatives agree with the independent spatial-pressure equations within the unchanged numerical allowance. Both the cold baseline and MTS are checked, including photons, baryons, massless/massive neutrinos and the retained scalar fields.

This verifies the effect of the PREVIOUS stage's coherent evolution. It does not introduce a fitted pressure correction, a new action or a new empirical success. The standard Einstein/conservation identities are not presented as new mathematics.

## Quantitative result

Values below are maximum raw residual plus measured32/64 refinement, divided by norms frozen from934 ORIGINAL states before corrected evolution. The acceptance threshold is2e-5. Norms follow the same rule for both cases; these are numerical consistency diagnostics, not goodness-of-fit comparisons.

| Equation | Baseline interpolated | Baseline coherent | MTS interpolated | MTS coherent |
|---|---:|---:|---:|---:|
| Background balance | 5.16640e-12 | 2.15036e-14 | 1.57906e-3 | 6.95487e-14 |
| Density balance | 4.08366e-8 | 4.08362e-8 | 5.51437e-6 | 3.55926e-8 |
| Current balance | 1.44975e-12 | 4.82305e-16 | 2.78203e-6 | 5.11882e-16 |
| Spatial trace / pressure | 4.49210e-8 | 4.49203e-8 | 8.66611e-4 | 4.57294e-8 |
| Spatial shear | 4.49210e-8 | 4.49203e-8 | 8.80807e-4 | 4.64773e-8 |

The old interpolated MTS background, trace and shear fail; the coherent evolution passes. The MTS spatial mismatch falls by approximately19,000-fold. Its worst corrected equation residual is about430 times below the unchanged numerical allowance. Baseline spatial residuals were already below the allowance and remain there. Algebraic constraint and eta consistency checks also pass.

The residual left in the coherent histories is dominated by the retained massive-neutrino finite-momentum/background approximation, not the old scalar interpolation contact. At the worst trace point, baseline actual1.79615214e-10 versus predicted neutrino1.79615145e-10; MTS actual8.29792791e-11 versus predicted neutrino8.29792597e-11, in native Mpc^-1 trace units. Across the window, removing just that independently predicted contribution leaves maximum trace discrepancies7.16e-17 /4.85e-17 respectively, including baryon thermal approximation and rounding. This diagnostic subtraction is NOT used to pass the raw physical gate.

## Control qualification: not an all-tests-pass report

The original strict aggregate metric_stage_passed remains FALSE. It additionally demanded that every deliberately omitted term fail the broad2e-5 physical gate. Baseline pressure omission gives1.1674e-5 and therefore does NOT fail that gate. This control is too insensitive to establish baseline pressure necessity by itself.

The separate, explicitly post-result supplement uses the ALREADY EXISTING1e-10 contact-identity gate, with the same frozen norms and cached packets. Correct identities pass. Omitting pressure gives1.17187e-5 baseline /8.75041e-3 MTS and is detected by that stricter equation-accounting test. Omitting anisotropic stress is detected as well. No threshold, physical residual, initial aggregate flag or previous failed result is rewritten. See CONTROL-INTERPRETATION.md.

Thus BOTH physical metric checks pass, while the weak baseline broad-budget pressure control remains honestly inconclusive. The post-result supplement is not represented as preregistered evidence.

## Reuse and preservation

- Original33x902 query grid,934-state native capture, single matched initial state, k=5 Mpc^-1, bank, parameters, masses, grids and tolerance values unchanged.
- Every original accepted output array reproduces exactly:22 arrays in each of four runs,88 exact comparisons. New metric diagnostics are extra readouts, not changed dynamics.
- Full matched preparation-pressure budget remains4.44654810e-9 versus5.07616242e-9, or87.5966% of its cap. This includes the initial preparation and uncertainty estimates, NOT only the small subsequent increment.
- The previous three tiny-baseline response-relative failures and four earlier background-relative failures remain recorded and unresolved. This stage does not convert them to convergence.
- All390 previous sealed artifacts and1057 frozen source paths verified unchanged.
- Sixteen symbolic identities, three symbolic omission controls, eleven dimensional checks and both38-check readout preflights pass. New76 identity/readout checks per case and all refinement checks pass. Cached result and supplementary-control replays are exact.
- Initial preflight failures from computing nearly cancelling scalar B+P are retained; using exact primitive v^2 repairs only that representation.
- The frozen derivation's dimensional prose error is explicitly corrected in DIMENSIONAL-CLARIFICATION.md; equations and results were unaffected.

## Scope and next use

These are the retained flat linear scalar equations in one saved cosmological mode and interval, with explicit thermo/hierarchy approximation contacts. Measured step differences are error estimates, not rigorous global bounds. No quantum measure, new observational fit, new galactic occupation, or new growth/lensing forecast is inferred.

The new packets preserve metric/stress diagnostics and the previous source/work arrays. They are NOT complete corrected native-state restart files. A later extension must explicitly preserve the full state, background correction and work accumulators rather than pretending selected readouts are sufficient.

The next useful step is to carry the now-consistent source into the saved radiation/gas response and quantify its effect on the existing predicted output, retaining the full preparation uncertainty. Do not spend another stage repeating these passing same-window metric tests or removing a harmless approximation solely to manufacture more passed checks.

## Cleanup

One numerical worker/thread at a time. All154 recorded worker/compiler identities verified exited; native owners released and temporary drive mapping removed. No bytecode, server, browser, subagent, continuing numerical worker, publication, scheduler change or other-chat process action. The foreground verification command also completed. The broader owner goal remains active; this completed stage leaves no background job.

