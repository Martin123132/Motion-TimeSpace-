# Can light weigh the same inner stellar mass that enters the force test?

**Yes, conditionally.** We have a paired numerical prediction for the same change of stellar mass, with the gravitational coupling inherited from the parent and nothing fitted to microlensing. The OGLE sightlines do probe 4–7 kpc. Their full optical depths do not, on their own, tell us how much mass sits there. This is a sensitivity result, not an observation of extra mass.

## What reaches the telescope

We used [OGLE-IV survey geometry and image-calibrated counts](https://www.astrouw.edu.pl/ogle/ogle4/microlensing_maps/): 697 subfields in 22 geometry-selected fields, representing 187,383,429 tabulated monitored-source counts (not an independence or unique-star claim). For 291 centers, representing 111,273,824 counts, the [OGLE-III red-clump catalogue](https://ftp.astrouw.edu.pl/ogle/ogle3/ext/blg/) supplied a unique containing cell with usable source-distance moments. There were 368 centers outside, 37 ambiguous and one with nonpositive variance. No photometric or lensing residual selected those cases.

These are **predictions**, in units of one millionth of ideal optical depth. The compact living-star plus remnant populations are identical in total mass between the spherical and bar central-geometry controls.

| Source assumption | Annulus / total, spherical centre | Annulus / total, bar centre |
|---|---:|---:|
| All sources at 6 kpc (geometry control) | 0.173 / 0.257 | 0.173 / 0.253 |
| At 8 kpc | 0.213 / 0.598 | 0.213 / 0.715 |
| At 10 kpc | 0.237 / 1.491 | 0.237 / 2.366 |
| Gaussian in measured red-clump modulus, matched footprint | 0.219 / 0.749 | 0.219 / 0.983 |

For the last line, **29.2% or 22.3%** of the predicted depth comes from 4–7 kpc. Replacing the spherical excess by a mass-preserving bar barely changes that annular numerator but changes total depth by 31%. The bar uses an independently published *red-clump shape* [Cao et al.](https://arxiv.org/abs/1303.6430); transferring it to mass is conditional. The all-source and matched-footprint rows do not have the same sky coverage.

## A prediction shared by two different observations

The retained living disk contains 5.45913 billion solar masses at 4–7 kpc. A local change of that mass has the following derivatives per **one billion solar masses** with the same spatial profile. This unit expresses a slope; no billion-solar-mass addition was fitted or asserted.

| Response on the shared ordinary matter | Ground MTS | Spherical NFW control |
|---|---:|---:|
| Inner SEGUE mean vertical-force equivalent, outer speed kept fixed | +5.324 | +5.137 |
| Same, dark mass/amplitude held fixed | +5.728 | +5.349 |
| Ideal lensing depth increment, red-clump moment bound | (3.179–3.218) × 10⁻⁸ | same |

The force unit is solar masses/pc² in `|K_z|/(2πG)`, not directly measured surface mass. The dynamical average uses the identical 14 inner [SEGUE populations](https://arxiv.org/abs/1309.0809) from the previous test. On the matched MTS branch this corresponds to **(5.97–6.04) × 10⁻⁹** in ideal depth per unit of that force change; for NFW **(6.19–6.26) × 10⁻⁹**. Holding either dark component fixed instead gives different slopes, as expected. A smooth MTS wave and a smooth NFW halo are not counted as individual stellar lenses. No MTS versus NFW ranking follows from the equality of the optical numerator.

The optical interval allows *any* positive source-distance distribution with the tabulated red-clump mean and variance at each unique sightline, at fixed lens profile and N21 angular weights. The degree of freedom being bounded is the shape in distance, **not** the identity of the source population. The annular living-disk depth at present mass is 0.173565–0.175650 millionths. Varying both reported moments in their individual printed-error rectangles gives 0.171979–0.177136; weighting instead by the local red-clump surface density times the inferred CCD area gives 0.176889–0.182280 including the same rectangles. These conditional weights sample the CCD centers, not an exact mask intersection. None of these ranges is an observational error bar for OGLE-IV. Diffuse gas, brown-dwarf incompleteness, stellar-evolution uncertainty, compact binaries and distance-dependent extinction of faint sources have not been swept into a fitted mass.

**Why not score table 7?** [Mróz et al.](https://arxiv.org/html/1906.02210) report a source-magnitude-selected, duration-limited result. The source-count table is not an all-source distance distribution. The finite event window also matters: a one-solar-mass point lens 4 kpc away toward an 8-kpc source has a 4.04-AU Einstein radius and must move faster than 23.3 km/s transversely for its event timescale to fall below 300 days. We did not download or score table 7. The attainable foreground ambiguity is real: two positive compact-mass arrangements with *all versus none* of their added lenses in the target annulus give identical depths for every source behind both, yet differing depths for sources between the lenses. See distance-null-control.csv.

**Numerical and physics checks.** All 5,346 low/high total-depth pairs agree to 2.53×10⁻⁸ relative or better. All 172 total dynamical slopes pass the original 2×10⁻⁵ scaled criterion, and signed nonlinear tests down to ±1/256 confirm the MTS slope. The small induced-force component alone did not pass at the first refinement (worst 1.98×10⁻⁴). Changing the ordinary-source mesh at fixed wave state barely moved it; increasing radial wave resolution did. Its final 512/40 to 640/40 difference is at most 8.84×10⁻⁶ scaled. The failed earlier comparisons remain in resolution.csv. Direct ring mass, angular Poisson monopole and finite-response normalization are checked independently.

During the light derivation we also found a genuine factor-of-two mismatch in the linear polarization split in checkpoint 4931. The retained Maxwell action and its exact optical factors agree with each other, and independent ray integration confirms the corrected weak-deflection magnitude. At the example 4.04-AU impact the conditional parent contribution is only 1.59×10⁻⁹⁴ of GR bending; the electron term is 2.11×10⁻⁵³. Neither is an upper bound on unspecified operators. See LIGHT-COUPLING.md; the sealed historical file is untouched.

**Decision:** use a source- and exposure-matched measurement of compact-lens depth to test this foreground. A change of central geometry without matching source selection can imitate a much larger change in total optical depth than the annular signal. Do not infer a new stellar mass by dividing the full SEGUE shortfall by a local tangent.
