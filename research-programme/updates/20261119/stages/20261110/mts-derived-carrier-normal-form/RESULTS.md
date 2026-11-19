# Derived sound coefficient and explicit metric-coupled carrier operator

Private retained-parent result, 2026-11-10. Previous turn was verified progress. This stage completes the next derivation rather than rerunning the preceding live integration. Original field action, bank, background, masses, wavelength, output grids, source extraction and tolerances remain unchanged. No fit or observation has been added.

## New constructive results

- The exact frozen quadratic-field normal form has slow frequency omega-mu and fast frequency omega+mu. Its slow density/current obey d'=-k*q and q'=k*c_s^2*d, deriving the retained coefficient c_s^2=k^2/(omega+mu)^2.
- A regular two-coordinate inverse retains the physical phase without dividing by a field or velocity zero. Its energy-scaled map is a scaled orthogonal reflection. The fast source pieces are determined by these same two coordinates and background, not new free modes.
- Expansion, live metric force and background representation terms are derived explicitly. The source pair closes using current quantities without needing H' or z'. Its exact coupled operator includes the inherited heavy self-gravity and rest-source forcing.
- An analytic frozen-phase operator average exposes a nonzero self-gravity correlation, -E*(omega-mu)/(8H*omega*beta) times the identity. Independent 32/64-angle controls verify it. This is a mathematical phase-average control, not an assumed cosmological population or a completed averaged propagator.

DERIVATION.md contains the equations and units. The existing implemented WD/WQ route remains intact; this stage has not changed the live integrator to the new pair.

## Paired verification

Twenty-two exact symbolic identities establish the normal form and its restored equations; three further identities establish the limited phase-average metric coupling. Saved-packet verification checks 47 comparisons, with 57 further operator/coupling/phase-control comparisons. They all pass. These counts are algebraic and numerical verification, not independent observations.

The calculation uses both the original 902-node extraction and the completed 65-node live continuation. Baseline is the actual retained CDM source; its source equation and metric feedback pass, with no heavy oscillator invented. MTS exact stress reconstruction, inverse, native field equations, evolving normal-form rates, saved boundary coordinates and full coupled metric operator pass the unchanged algebra gate 1e-10. Inputs are hash-checked; no physical calculation was restarted.

## What the original extraction actually retains

The heavy sound coefficient ranges from 2.16547e-4 to 2.22847e-4 over the extraction and from 2.16112e-4 to 2.16547e-4 over the live window.

Using the original signed weights, the normalized pressure splits as follows:

| Derived contribution | Value |
| --- | ---: |
| Original c0^2 times projected slow density | -2.253496542838865e-4 |
| Coefficient-history correction | +5.502609595449409e-12 |
| Projected fast pressure | +3.434082413594254e-7 |
| Reassembled pressure | -2.250062405399175e-4 |
| Independently retained physical pressure | -2.250062405402447e-4 |

The fast density projection is only 7.81666e-11, but the fast current projection is 3.69900e-5 and its pressure contribution is 3.43408e-7. Small fast density alone does not license dropping the other stresses. Ignoring fast pressure gives a 0.152624% pressure-relative discrepancy; the existing late pressure formula on the physical projected sources gives 0.156965%. These diagnostics use the retained 2e-5 relative numerical gate; they do not replace the separate historical mode-normalized pressure test or imply an observational exclusion.

For a fairer rate comparison than instantaneous oscillations, project BOTH the exact rates and the late-operator rates through the same original weights. The remaining density/current differences are respectively 0.0792205% and 0.0685098%, larger than this numerical gate. The derived residual contributions are:

| Projected rate contribution | Density | Current |
| --- | ---: | ---: |
| Expansion mismatch | -8.65739e-6 | -2.32297e-7 |
| Explicit phase term | -6.80855e-6 | -2.11403e-10 |
| Metric-coupling remainder | -2.14567e-5 | +1.10980e-6 |
| Representation defects | -7.19243e-9 | -8.84739e-11 |
| Total | -3.69298e-5 | +8.77200e-7 |

The additional fixed-center operator-history terms are only 6.31571e-13 and -1.54939e-11 here. Restoring all derived terms reconstructs the projected rates at the algebra gate. No correction was fitted against the discrepancy.

Instantaneous late-only comparisons have much larger oscillatory discrepancies (about 85% density and 60% current when normalized to peak exact rates). Those are retained in analysis.json but are NOT used as a rejection of an averaged model. The projected checks above are still fixed-functional tests, not a new late cosmological evolution or a full history error bound.

## Interpretation and next calculation

We now have an equation-derived origin for the retained frozen sound coefficient, an exact source/readout map, and explicit expansion/gravity terms that a proper reduction must carry. The result does not require a new field, arbitrary cutoff or adjustable galaxy coupling. It narrows the next calculation to the phase-dependent operator correction, including metric correlations, rather than another search for an unspecified coefficient.

Next derive the first controlled phase correction using the actual phase speed and retained operator, then test its propagator/source error against the saved histories and signed extraction. Keep the current exact pair as reference. A uniform phase average alone is not enough to identify the real evolving ensemble, and no local/galactic occupation has been selected by this algebra. See NEXT.md.

Everything remains private. No native rebuild, source download, Galaxy edit, GitHub, browser, relay, timer or subagent. closeout.json and CLEANUP-VERIFIED.json record the final artifact hashes and task-process exits after sealing.
