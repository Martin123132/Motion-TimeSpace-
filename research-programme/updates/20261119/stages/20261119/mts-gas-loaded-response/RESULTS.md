# What happened when gas was allowed to gravitate inside the wave?

**The gas strengthens the wave's off-plane response. The observed off-plane force is stronger still.** For both stellar source reconstructions, both unchanged physical models fall below the magnitude of the Gaia-inferred polar force at the two frozen positions that the published study covers. This is useful evidence about a shared foreground, not a unique failure or success of one dark sector.

## The part we can attribute to the wave

No new coupling, stellar normalization, rotation radius or gas parameter was chosen for this primary experiment. Both models share the prior stellar source, bulge and compact gravity, and the same atomic and molecular gas from McMillan's Table 1. The spherical halo has the same 16-kpc scale. For each of the two alternately normalized APOGEE reconstructions, the wave was re-solved first at the saved occupation and then with one amplitude recalibrated to the same exposed outer speed. The masses below are inherited occupancy labels (see numerical convention below).

| R=8.3 kpc, z=1.5 kpc unless noted | Catalogue stellar masses | Local-column stellar source |
|---|---:|---:|
| Wave-only T: stars only → gas, fixed occupation → gas, matched occupation | −11.01 → −18.76 → **−16.99** | −12.12 → −20.27 → **−18.38** |
| Outer speed: stars only → direct gas only → gas, fixed occupation (km/s) | 224.03 → 229.76 → **232.05** | 224.03 → 229.76 → **232.36** |
| Gas-loaded matched wave mass (10¹¹ solar masses) | 1.896 | 1.983 |
| Matched local slope, wave / NFW (km/s/kpc) | +2.58 / −1.00 | +4.78 / +0.82 |
| Matched total vertical gravity, wave / NFW | −1675 / −1700 | −1633 / −1682 |
| Frozen three-position wave excess, before → after matching with gas | +0.285 → **+0.159** | +0.221 → **+0.056** |

T = g_z+(z/R)g_in, in (km/s)²/kpc. The direct gas-only contribution at a position is exactly the same for both theories. The extended wave also *rearranges* in the new potential: adding gas only at the final force readout misses that contribution. A matched spherical halo itself has identically zero T. At the single near-Sun point the wave is only 2.7% of the ordinary-source T; the three-position wave residual is 0.98% / 0.34% of the absolute common signal after cancelling the two stellar templates. It is not a practical gas-insensitive measurement.

The exposed rotation-curve diagnostics are still mixed. With the catalogue masses, mean-bin RMSE (km/s) is 9.80 / 8.44 on the other 11 Cepheid bins and 12.78 / 15.93 on the 38 older giant bins (wave / NFW). With local-column normalization the corresponding numbers are 17.05 / 12.78 and 16.00 / 16.45. Comparing at identical inputs matters more here than declaring a winner. The older local red-clump vertical determinations differ from the matched MTS prediction by 0.60–1.33 quoted widths across the two reconstructions and tracers.

## A second dataset actually measures this component

The polar acceleration in [Lim et al., Gaia DR3, Fig. 9](https://arxiv.org/html/2305.13358v3) is directly proportional to T. We froze the model predictions before extracting the reported values. Using the published spherical radius instead of the cylindrical radius and the correct sign, the northern slice at z=+1.5 kpc gives:

| Cylindrical radius (kpc) | Gaia plot, central [outer band] | Catalogue wave / spherical halo | Column wave / spherical halo |
|---|---:|---:|---:|
| 6.0 | 0.671 [0.573, 0.769] | 0.437 / 0.428 | 0.417 / 0.409 |
| 8.3 | 0.301 [0.238, 0.365] | 0.204 / 0.199 | 0.222 / 0.216 |

Units: 10⁻¹⁰ m/s². The corresponding southern central values are −0.675 and −0.301. **All four primary predictions miss the published outer polar band on both sides at both radii.** These are pointwise figure bands, not sixteen independent observations or a joint exclusion probability. The small numerical differences between the parent grids do not explain the gap. For the catalogue-mass MTS case the radial acceleration at R=6 *does* agree within the inner bands; the problem is not a universal scaling error on every acceleration component. At R=8.3 its radial acceleration is too weak in magnitude on both sides. The R=12 site is outside the study volume. No measured three-point statistic is available from these curves.

In cylindrical terms, the reflection-symmetric part of the *extra vertical force needed in the north* for MTS is approximately −694 and −399 (km/s)²/kpc at 6 and 8.3 kpc for the catalogue case; −993 and −441 for the column case. A spherically symmetric force added at readout cannot fix the polar discrepancy. Do not infer the missing density uniquely from this fact. Other geometry, response of the wave, stellar mass, gas structure, selection, departures from equilibrium and calibration can all matter. The Gaia inference uses stellar phase-space equilibrium, not direct test-body accelerometry. Its overlap with earlier tracers has not been certified absent.

## An independent clue, and a trap

A local Solar-neighbourhood census ([McKee, Parravano & Hollenbach, Table 1](https://arxiv.org/pdf/1509.05334)) gives a total stellar column of **33.4±3** solar masses/pc², compared with **21.79 / 25.06** for the two local reconstructions integrated through the adopted cylinder. The census includes brown dwarfs and remnants and is not a perfect population match. This was explored *after* identifying the polar discrepancy; do not describe the follow-up as blind.

For a spherical halo the polar gravity comes from the ordinary nonspherical sources only. Holding the gas and stellar shapes fixed, the four outer Gaia polar bands have a common allowed stellar amplitude interval of **1.44–2.04** (catalogue) or **1.54–2.09** (column). These intersections are descriptive, not parameter likelihoods. Normalizing to **local counts only** gives factors **1.53 / 1.33**. The former gets the spherical catalogue control inside all four angular bands without using any of their values to set that factor; the latter misses the inner-Galaxy angular bands. This is a *polar-component control only*. Neither a full spherical acceleration fit nor an MTS prediction on the newly normalized disk is being claimed.

The same census puts **31.2±3** inside |z|≤1.1 kpc. With only the total column normalized, the templates put 26.64 / 27.06 there. Squeezing all stellar heights by 0.509 / 0.534 matches both central columns, but then predicts midplane stellar densities **0.065 / 0.063** solar masses/pc³ against the census central **0.043**. Matching total column and midplane instead gives height factors 0.770 / 0.788 and inner columns 28.72 / 28.92. No joint covariance or total midplane error is assumed; this is a central-value inconsistency in a *particular family of shapes*, not a statistically certified failure of the census or the APOGEE populations. Do not pick a thickness because it makes the rotation or angular score look good.

## What advanced on the parent side

- In the retained Newtonian limit we derived and checked a nontrivial matter–wave stress identity. The downward mutual force on the gas and on the wave above the plane equals the gravitational stress transmitted across the plane, including the tail to infinity. For the fine catalogue matched state, the atomic-associated and molecular-associated tractions are 1.297×10¹³ and 3.296×10¹² solar masses (km/s)²/kpc. Independent energy integrals with source and receiver swapped agree within 10⁻⁹ relative on the fine integration; the nonzero half-space force balance closes within **1.5×10⁻⁷** relative.
- The frozen response includes a reciprocal energy curvature between H I and H₂. In the catalogue case the fixed-occupation susceptibility matrix per original wave mass, in (km/s)² per pair of dimensionless gas amplitudes, is approximately [[−35.55,−9.74],[−9.74,−2.78]]. Its negative eigenvalues describe relaxation in these two driven directions. Cross symmetry and finite combined perturbations were checked; this is not a universal stability proof.
- The mutual-energy calculation caught a **30.24 ppm solar-mass convention difference** between the retained wave-unit conversion and the nominal solar GM used by the external Newton field. The ratio follows independently from the constants; using a common mass unit restores energy/Poisson agreement without adjusting any coupling or acceleration. Both original numbers are preserved.
- The fine residual potential agrees with the independent rings within 0.29 ppm across tested positions. All 70 small-response comparisons (including envelope energy and energy curvature) pass the 20-ppm criterion, worst error below 0.069 ppm. The tiny three-position excess is less resolved: final independent-box differences are about 145 / 799 ppm. Preserve these and the smaller-grid misses; do not report 20-ppm accuracy for every observable. See resolution-checks.csv.

No parameter was tuned on the new angular outcomes. No new public release, other chat, or changes to the earlier source/solver checkpoints.
