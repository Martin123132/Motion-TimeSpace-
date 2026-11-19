# Derived phase drift closes the original projected-rate discrepancy

Private result, 2026-11-10. Previous goal turn was verified progress. This stage derives the actual phase flow and a first near-identity correction, including the inherited self-gravity and changing-background contribution. No physical parameter, observation, bank, output grid, cutoff or acceptance gate changes. Coefficients and checks were frozen before evaluating their performance.

## Main result

Under the ORIGINAL 902-node signed extraction, the new first correction gives:

| Normal-source rate | Reference | Corrected prediction | Relative discrepancy |
| --- | ---: | ---: | ---: |
| Density | 0.046616511250787925 | 0.04661656524774686 | 1.15832e-6 |
| Current | -0.0012804009259109953 | -0.0012804005997838108 | 2.54707e-7 |

Both pass the unchanged 2e-5 numerical gate. These are about 1.16 and 0.25 parts per million in projected RATES, not observational accuracies or independently evolved final-state errors. The prior uncorrected projected-rate discrepancies were 7.92205e-4 and 6.85098e-4.

The correction is not a fitted residual. It follows from the harmonic operator, its matrix commutators, the actual phase speed and background energy/Friedmann drift. The exact remainder remains explicit.

## Why the changing background matters

The actual phase speed differs from mu by up to 5.78531e-4 fractionally in the extraction and 5.63871e-4 in the live interval. The zero-mean phase correction has a sufficient frozen-phase inverse bound at most 0.0537071; the actual transform condition number stays below 1.039504.

The projected comparison distinguishes the ingredients:

| Candidate, with transformed rest response | Density relative discrepancy | Current relative discrepancy |
| --- | ---: | ---: |
| Mean operator with micromotion | 1.56688e-6 | 9.12118e-4 |
| Plus fixed-parameter commutator only | 1.45754e-3 | 8.50321e-4 |
| Plus derived phase/parameter drift | 1.15832e-6 | 2.54707e-7 |

The commutator alone is not a complete physical correction. The separately derived changing-background term is essential here. Removing the rest-response compensation degrades the projected errors to 1.16430e-5 and 1.57608e-5: those still pass this particular gate, so they are NOT labelled failed, but their degradation and the missing exact term remain recorded.

## Remaining pointwise error

The first approximation does not pass the stricter point-by-point rate test. With the same normalization as the exact normal-source history:

| Window | Density discrepancy | Current discrepancy |
| --- | ---: | ---: |
| Original extraction | 8.36050e-4 | 2.57210e-4 |
| Short live history, native derivative | 8.02849e-4 | 2.35160e-4 |

This is a residual oscillatory/evolution error, not hidden by the projected pass. Whether its signed effects stay small through actual evolution is the next calculation. No whole-history or new late-model pass is claimed from rates alone.

## Independent numerical and mathematical checks

- Fourteen exact phase/amplitude/energy/harmonic identities pass. Independent primitive-field matrices reproduce the harmonic operator, including metric self-gravity.
- Frozen 32/64-angle tests verify the commutator and background-drift averages separately. They are labelled mathematical controls, not a physical ensemble.
- At all six prescribed window locations (five unique locations), the first commutator-corrected one-period fundamental matrix has normalized errors from 1.81e-8 to 4.59e-8. The bare mean has errors from 4.29e-5 to 1.05e-4; micromotion without the commutator also fails that 2e-5 control gate. The two integration step sizes agree. These controls have fixed parameters/rest source, not a live cosmological background.
- Exact coordinate inverse and transformed-equation checks pass at 1e-10. Twenty-one additional reconstruction/metric-derivative robustness comparisons pass. The two complex derivative precisions and retained metric-derivative variants do not change the projected conclusion.
- Both original windows retain the genuine CDM baseline, whose unchanged source equation passes. No fictitious heavy phase is assigned to the control.

## Scope and next step

The saved-history comparison includes the actual rest-source derivative and its coordinate compensation. It does not propagate a new coupled rest-species state. The derived first generator must now face a finite-window propagation/defect-response test and then the current-state full coupling, retaining the actual late background/selector and matching normalization.

All earlier checkpoints and physical implementations remain intact. No new native build, fit, download, Galaxy edit, public upload, browser, relay, timer or subagent. The only numerical integration here is the small explicitly frozen periodic control. Final source/artifact hashes and worker exits are recorded in closeout.json and CLEANUP-VERIFIED.json.
