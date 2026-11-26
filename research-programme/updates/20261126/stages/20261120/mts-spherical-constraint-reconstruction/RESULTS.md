> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# One predicted spatial contrast, and a separate test of motion in time

20 November 2026 · Local calculation, no fitted parameters. Tests the retained Einstein-limit equations on MTS formation data. The two branches are the cold control and the massive coherent-wave branch. Early and late are two already saved epochs, not independent cosmological observations.

## Recovering the frozen prediction

The preceding calculation predicted a signed contrast of V−U at 100, 200 and 350 comoving kpc from radial stress and the Newtonian field gradient. Here V comes from the nonlinear spatial and momentum constraints, and U comes separately from preserving the chosen shear-free slicing. We did not set either equal to the forecast. Relative differences in the primary, finest constraint calculation:

| Preparation | Scale factor | Frozen contrast | Reconstructed | Relative difference (ppm) |
|---|---:|---:|---:|---:|
| Cold, early | 0.65 | +2.511411e−12 | +2.511397e−12 | −5.61 |
| Cold, late | 0.925159 | +1.990824e−12 | +1.990808e−12 | −8.29 |
| Wave, early | 0.65 | +5.031227e−13 | +5.031189e−13 | −7.63 |
| Wave, late | 0.925159 | +1.284505e−12 | +1.284506e−12 | +0.74 |

All four recover the forecast inside the original 20 ppm target. Changing the sampled core radii or the box from 24 to 12 Mpc changes this contrast by less than 0.2 ppm relative to the corresponding reference; changing between the two wave initial-data lifts by up to 2.2 ppm. Correcting the wave origin separately gives −7.68 and +0.38 ppm against the forecast on the finest tested wave grid. Those origin tests use the archived short-history readout rather than the independent direct-lapse integration in the table.

The constraints required a spatially varying normal expansion because the matter has radial momentum. The mass obtained from the geometry independently agrees with the integrated material energy and radial current: worst relative mass difference 1.77e−13; error measured against the much smaller current term itself 3.91e−6 or less. Analytic expanding, vacuum and charged exterior controls include Maxwell tension and the extremal cancellation. This is a consistency test inside the retained gravity limit, not a new Galactic mass measurement. See [equations and assumptions](DERIVATION.md).

## Does the spatial metric move at its predicted rate?

Before advancing matter, store the rate required by the local expansion and lapse. Then advance matter for a short interval, reconstruct the constraints slice by slice, and measure the rate from two potential differences. The target is 2e−5 of the larger of the predicted rate, measured rate and the Hubble-times-span scale. It is not a percentage of an arbitrarily small rate.

- **Cold.** Newtonian motion passed its Newtonian control but missed the early relativistic inner span (2.75e−5). The common metric fixes both the marginal change of radial speed and the force; neither is a free coefficient. On the identical initial mass elements with the same midpoint rule, projection and eight steps, Newtonian motion on the relativistic test gives +2.71e−5; the derived geodesic motion gives +1.48e−7. The second span gives +1.03e−5 and −1.16e−6 respectively. The full live table (not bundled here) includes late, doubled-label, and Newtonian-potential checks; its signed residual and finite-stencil differences are published even when outside tolerance. Naive pointwise acceleration at mass-element ends was not reliably accurate: these runs integrate across the folded elements with their original masses.
- **Wave.** A large native late discrepancy (up to 0.332 on the fixed scale) was mostly a false signal from spreading the unused origin cache into a finite central volume. Restoring the limit of the represented sine wave gives 8.77e−4 on the native late inner span. The remaining off-grid phase kick has a spurious density-rate contribution of 6.49e−13 there on the native grid, below 4e−19 two refinements later. On that refined wave grid both spans at both epochs meet the original test; worst relativistic residual 1.12e−5. These are evolutions of the *saved envelope*, not full relativistic scalar evolutions.
- **What follows from the scalar action itself.** We derived the evolution of the independent field and its densitized conjugate quadrature and applied both equations, including the mass and background-expansion terms, at each saved epoch. Across two shell spans and both admissible lifts, the instantaneous volume rate agrees with independently evaluated boundary current to at worst 4.01e−9 on the flux scale. This checks a quadratic phase-pair Wronskian, not electric charge or a new exact particle symmetry. The result makes a finite wave-evolution test possible without resetting a wave quadrature at every step.

Across both cold epochs, both spans and both label resolutions, **all eight** geodesic rate checks meet the 20 ppm target. The largest error is 1.235 ppm on the prescribed scale. Doubling the labels (and, at the early epoch only, doubling time resolution) keeps every rate inside 0.75 ppm. This comparison does not separate those two refinements at the early epoch.

## Light and the matching boundary

The two-clock experiment uses two null trajectories arriving at one event, not just a value of the potential on one slice. A check using two neighbouring emissions agrees with the integrated pulse-spacing factor within 8.1e−18 absolute. The compensated three-radius contrast is robust; not every two-clock difference is. For the late wave, the net change from the Newtonian two-clock result on the inner arm is +7.22e−15 in the 24-Mpc box and −3.20e−14 in the 12-Mpc box on the same regular-origin grid. Do not predict its sign without an exterior matching condition. The central radial dust caustics also need an explicit core treatment; regularity of the unmodified streams was not assumed.

**Next physical test:** evolve both canonical wave quadratures and the positive-mass streams through the same short interval, with common metric feedback and unchanged shell flux, temporal and optical checks. First distinguish the time discretization error of the fast mass oscillation from physical departures from the envelope. Keep the two initial-data lifts visible instead of selecting the one giving smaller residuals. For the separate galaxy question, [the saved crossed-foreground test](../mts-foreground-occupation-cross/RESULTS.md) already isolates ordinary disk and bulge from wave occupation; no reason to rerun it in lieu of this dynamical test.

[Material and light derivations](MATERIAL-AND-LIGHT.md) · independent wave flux (not bundled here) · forecast and quadrature checks (not bundled here) · all time tests on original histories (not bundled here) · [replay](REPLAY.md).
