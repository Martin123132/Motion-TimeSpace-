# Reconstructed sources now continue with live gravity

Private retained-framework result, 10 November 2026. This completes the saved live-continuation target and derives the physical remainder needed for the next averaged-carrier step. No action, mass, coupling, abundance, bank, output grid or tolerance changed.

## Actual dynamical test

The preceding stage reconstructed the physical scalar/CDM block from the original projected sources and their earlier history. Here that endpoint starts an independent evolution of the constrained phase variables AND all other active native species, with the metric computed from their current state. The RHS does not consume future metric/species histories. All other initial coordinates and native caches are preserved. The comparison start is the directly captured endpoint.

Both baseline and MTS pass for both starts and both internal step limits. The original 4253 native outputs remain exact; the 65-output continuation spans original indices2892..2956, after the 902-node extraction, with its endpoint shared. The captured next regime is coherent and fixed, not the old late averaged selector. Existing phase/native interfaces were reused without rebuilding the library.

| Fine continuation, worst componentwise difference | Baseline | MTS |
|---|---:|---:|
| Reconstructed start versus original native state |1.37022e-14|1.78319e-11|
| Reconstructed start versus original native observables |1.32068e-13|5.55713e-11|
| Reconstructed start versus original native derivatives |3.26439e-12|2.92526e-9|
| Reconstructed versus captured-start state |1.16142e-14|1.60451e-11|

All are below the unchanged2e-5 numerical gate; exact algebra uses1e-10. MTS maximum derivative discrepancy falls from4.08137e-8 at step128 to2.92526e-9 at step256. Baseline is already at rounding-sensitive levels, so monotonic convergence is not claimed there. All9 selected cache values are checked; approximate-neutrino memory activation remains outside this fixed-regime test. These are equation/restart consistency errors, not observational precision or a new fit.

7,422 component comparisons are independently recomputed; these are correlated numerical checks, not thousands of distinct physical predictions. Four symbolic source/carrier identities pass. Bidirectional metric/phase feedback, zero/sign controls, unchanged-source hashes and native owner release pass. Seed scaling uses only the initial state and initial RHS, not future reference peaks.

## What the old averaged carrier needs

For the same instantaneous coherent sources/background, the difference from the retained two-moment late equations is derived exactly in DERIVATION.md. It contains pressure phase, phase-dependent gravitational work and finite background-representation terms. In particular the gravitational term is proportional to beta*v², not automatically one.

On this saved heavy interval beta*v² ranges from0.0004432034 to1.9999273922. Substituting exact pressure into the averaged equations still leaves a44.4144% density-rate discrepancy, normalized to the coherent rate peak. Supplying the full derived remainder reduces the density-rate identity difference to2.04589e-13 and current-rate difference to3.15589e-16. These percentages concern instantaneous coherent equations: they do NOT reject a properly averaged approximation. The uncorrected and pressure-only comparisons remain explicitly failed in validation.json rather than being relabelled successes.

The coherent pressure itself oscillates strongly. The previous finite-window pressure relation must not be substituted as a universal instantaneous law. Nor does evolving this coherent state mean an independently selected positive ensemble or galaxy occupation has been derived. The old late solver also has an averaged background and selector1; its background/source transfer still needs explicit treatment.

## A derived route to controlling the extra term

With J=beta*b*v, E=beta*(v²+mu²*b²)/2 and F=beta*(E_f*v+E_b*b),

    beta*v²-1 = (E-1) + J'/2 + (2H-r)*J/2 - F/2.

Its accumulated gravitational work therefore splits into an explicit endpoint term plus normalization, changing-metric, expansion and representation integrals. This is a product-rule/integration-by-parts result, not random-phase averaging or a fitted closure. Three additional symbolic identities and the paired pointwise decomposition checks pass. E lies between0.9994372392 and1.0005640368 in the heavy interval even though beta*v² ranges nearly0..2. That gives a concrete fast-phase structure to control rather than treating it as an arbitrary missing coefficient.

The endpoint contribution alone is0.0014787908 in the retained normalized source units on this interval; it is NOT the whole accumulated work. The history integrals have not yet been evaluated in this boundary decomposition. The next task is to calculate/bound them jointly with pressure memory using the saved work and original extraction.

## Precision note and preservation

The original work-boundary.json displayed tiny slow-field kinetic factors as zero because its range used `(beta*v*v-1)+1`. No evolution or heavy result depended on that display. The original script/receipt are preserved. check_work_readout.py evaluates the unshifted factor and verifies its decomposition with50-digit arithmetic on the same saved inputs. Accepted corrected ranges are in work-boundary-readout-precision.json: slow factors are approximately7.24e-23..7.29e-23, not physically zero. The heavy range is unchanged. All three higher-precision checks pass the same algebra gate.

Everything stays local. No Galaxy modifications, GitHub, browser, relay, timer, subagents, native build or background worker left running. Exact release/exit receipts accompany the sealed checkpoint. Full project goal remains active.
