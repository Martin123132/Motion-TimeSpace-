# The inner vertical-force deficit survives the stellar-height test

**Decision:** keep the measured-height perturbation as a control, not a repair. It changes the force but not nearly enough, and the mismatch also appears in another tracer survey. The parent field has a collective response to an asymmetric foreground; its strength for this particular source is now bounded, not fitted. A large odd occupation is not justified by this mechanism.

## The sky comparison

We used [Wu et al., Fig. 17](https://arxiv.org/abs/2604.24456) to change **where** the living thin stars lie in height without changing how much mass there is at each radius. We recovered 35 vector markers and their plotted error bars in each of seven panels. The pooled red-clump height at 6.379 kpc is 0.164 kpc (plotted range 0.140–0.187). These are tracer counts in a wedge, not all-sky gravitating mass measurements. Gas, remnants, central stellar excess and original wave parameters are unchanged.

At R=6 kpc, z=1.5 kpc, with the original 224.03 km/s outer speed, the MTS polar acceleration shifts from 0.42418 to **0.42349**, against the near allowed edge 0.57340; the spherical NFW control moves from 0.41569 to **0.41499**. Units are 10⁻¹⁰ m/s². The correction moves MTS by less than half a percent of the gap, away from the band. Alternative tracer normalizations, plotted endpoints and the sector average all give 0.42313–0.42362 on the matched ground branch. The sign is not that of an infinite sheet: the 5.5–6.5 kpc annuli more than cancel the opposite changes elsewhere. Direct nonaxisymmetric integration of the conditional wedge at the same site gives changes (inward, upward, azimuthal) = (−2.1753, +3.9443, +0.5176) (km/s)²/kpc. It is not a nonlinear all-harmonic wave prediction.

The inward radial **magnitude** is 1.65228 for ground MTS and 2.11139 for NFW versus 2.275–2.507. Full equal counter-rotation, rematched only at the outer speed, gives a polar 0.59035 but radial magnitude only 0.71230. Moving stars in height does not resolve the tradeoff.

### A second survey and a different force component

We then used all 43 published [Bovy & Rix SEGUE G-dwarf population force rows](https://arxiv.org/abs/1309.0809) at z=1.1 kpc; no parameters were adjusted. These are vertical forces divided by 2πG, expressed in solar masses/pc², **not** measured surface densities. Primary R0=8.122 kpc, preserving published R0−R; native 8 kpc retained separately. Individual printed errors are not a joint likelihood.

| Population-average force measure | Observed | Ground MTS | Spherical NFW | Fully counter-rotating MTS |
|---|---:|---:|---:|---:|
| 14 groups inside R=6.5 kpc | 183.65 | 97.20 | 110.28 | 90.45 |
| 29 outside | 92.33 | 68.58 | 73.32 | 65.16 |
| All 43 | 122.06 | 77.90 | 85.36 | 73.39 |
| All-group RMS error | — | 55.72 | 47.28 | 60.34 |
| Within one printed uncertainty, all / inner | — | 6 / 0 | 8 / 0 | 5 / 0 |

NFW is closer on this shared test, but **all three** undershoot all 14 inner estimates. The estimates are model-dependent dynamical inferences; distinct tracers do not establish statistically independent residuals, an untouched test history, or a significance from 43 independent draws. The inverse spherical test requires 2.230 times the printed SEGUE widths even with an otherwise free nondecreasing mass profile and the outer anchor. Adding the fixed Gaia radial bands requires 3.032 times. These widths are not sigma levels. The results are conditional on the adopted ordinary matter.

## What the same field can do

On the original stationary foreground the dipolar, mirror-even field response to the height perturbation gives a longest calculated collective period of **883.12 Myr**, compared to 489.51 Myr for the frozen-potential gap. The cosine centroid moves 0.0240 pc versus 0.00478 pc without self-gravitational feedback; sine 0.00442 versus 0.000893 pc. Rigid translation recovers 1.000000097 of the imposed shift; projected-state discrepancy is 1.72×10⁻⁶. This is a susceptibility and an eigenfrequency, not a detected oscillation. A different far-side completion consistent with exactly the same measured wedge gives zero odd drive.

The fine-basis sudden-switch energy is 9.48×10⁻⁸ (km/s)² per unit mass versus 5.39×10⁻⁸ on the coarse basis: **do not quote this tiny energy as precisely converged**. The represented spatial source norm rises from 8.1% to 79.9%. Instead we independently assembled the self-gravitating Hessian and verified a positive floor by shifted Cholesky on both the 768- and 6,144-dimensional spaces. Matrix actions agree with a separate operator to better than 2×10⁻¹⁵ on the tested vectors. The conservative whole-spatial-source ceiling is 3.58723×10⁻⁵ / 3.58733×10⁻⁵ (coarse/fine): about 3×10⁻⁵ relative difference, not 20-ppm convergence. On either space it is less than 1.44×10⁻⁷ of the 251.01 (km/s)² initial one-percent transfer energy scale.

Turning the same pattern does not automatically evade this result. The derived path-length bound requires the equivalent of **more than 420 full turns** at unit amplitude after one rise merely to reach the reference energy, even allowing perfect accumulation. As a positive control we intentionally rotate at exact fundamental resonance: after four periods the four resolved modes acquire 4.50×10⁻⁶ (km/s)², while the all-mode bound is 0.02450, still less than 0.01% of the reference. This does not forbid a stronger past source, a different shape or initially occupied modes, nor prove a nonlinear one-percent threshold. No elapsed formation time or pattern speed was inferred.

**Verification:** 2,810 cross-resolution comparisons pass the unchanged scaled 2×10⁻⁵ tolerance for the named force outputs and four periods (worst 3.96×10⁻⁶). These do not include the unconverged raw switch energy. The original source tables, component sums, group scores, normalization, translation, exterior moments, shifted-matrix floor, spherical-feasibility result and protected predecessor digests have separate checks. See DERIVATION.md, resolution-audit.csv and REPLAY.md. No new fit or galaxy-formation prescription. The next independent lever is the radial distribution of compact stellar mass, not the traced scale height; see NEXT.md.
