# The ordinary disk changes the prediction more than the satellite wake

**Result.** The model now makes signed, observer-to-source acceleration forecasts for 26 real binary-pulsar directions. More importantly, we found and tested a physical inconsistency in how the denser reference state could have been used. That state was an *upper envelope* constructed by allocating the outer circular speed to the wave alone. It cannot simply be installed as the actual wave in a model which also contains the ordinary Galactic disk.

## A fixed-mass test, not a new fit

We solved the stationary wave and Poisson equations again with the same particle pole, occupations, central ordinary cloud and a specified ordinary disk and bulge. No timing or rotation residual was used to choose a new mass. The wave contracts in both cases. Speeds below are equatorial circular speeds, not spherical enclosed-mass estimates.

| At 17.58 kpc (km/s) | Denser reference | Illustrative diffuse |
|---|---:|---:|
| Original isolated wave alone | 224.03 | 97.20 |
| Old wave with disk/bulge added only at readout | 259.11 | 162.47 |
| Wave alone after solving in disk/bulge gravity | 252.25 | 165.15 |
| **New stationary total** (wave, disk, bulge, compact cloud) | **283.87** | **210.30** |
| Fixed smooth NFW + same ordinary reference, approximately | 200.57 | 200.57 |

The already-exposed [Cepheid bin](https://arxiv.org/html/2512.21780v1#S3.T1) has central speed 224.03 km/s and tabulated bootstrap error 1.91 km/s; that is not a complete systematic error. The ordinary reference leaves only **182.32 km/s of wave circular speed** at this radius when the forces add. The denser composite overshoots the central value by 59.84 km/s; the diffuse one undershoots by 13.73 km/s. The diffuse result is not a match merely because it is closer. Nor does one fixed disk or one radial bin reject every possible occupation or mixed state. The smooth baseline likewise undershoots this bin. No mass has been readjusted to turn these comparisons into wins.

The rms radii shrink from 15.51 to **10.93 kpc** and from 29.10 to **15.34 kpc**, while the final rms vertical-to-in-plane axis ratios are about 0.982 and 0.980. Mild flattening is not the same as negligible radial contraction. The change in predicted *static wave* acceleration on the pulsar directions has median magnitude about 0.220 / 0.164 mm/s per year, versus about 0.0011 / 0.0013 for the *satellite-driven wave change* on the old backgrounds. These are separately computed quantities, **not** an updated prediction for the satellite wake on the disk-loaded backgrounds.

**How each source enters.** Differentiating the coupled equations, including the wave's own rearrangement, gives the following *local* change in the total outer circular speed for a 1% increase:

| Parameter varied alone | Denser | Diffuse |
|---|---:|---:|
| Ordinary disk+bulge normalization | +0.41 km/s | +0.65 km/s |
| Conserved wave mass at fixed particle pole | +1.38 km/s | +0.92 km/s |

These are derivatives, not error bars, a global mass law, or fitted coefficients. Independent nonlinear neighboring equilibria reproduce the extrapolated energy, chemical-potential and speed-squared derivatives to better than 10⁻⁹ in relative terms within each tested discretization. Different starts on the same grid, a larger domain, a direct midplane Newton integral and the virial identity were checked. The earlier diffuse coarse virial misses remain in the ledger. Arbitrary non-axisymmetric or long-term stability is not established by a stationary calculation.

## The observational interface

Use all 26 entries in the [published v3 binary-pulsar sample](https://github.com/thomasdonlon/Empirical_Model_MSP_Spindown_Accels/tree/6cb4e31f6b2e732f5973b024634507c2e4f59988/v3), their Galactic coordinates and their curated distances. Only geometry columns were extracted. At the Sun the model predicts the difference of the source and observer accelerations **along the sightline**, not the magnitude of an invisible halo displacement. The old forced wave, its rigid translation and its internal deformation are separately tabulated; disk, bulge, compact material and direct LMC are common within each comparison. The static smooth halo reference has no satellite-induced internal response. It is a control, not a calculation of how a live collisionless halo responds.

For the released host origin, the largest nominal forced-wave excursion among the 26 is toward **B1913+16**: **−0.01255 / −0.00894 mm/s per year** for denser / diffuse. A negative sign means a change toward the observer relative to the unforced field. Median absolute changes are 0.00112 / 0.00133. Re-registering both endpoints relative to the compact material center changes individual driven readouts by up to 0.00378 / 0.000095 mm/s per year. Each source was sampled at 17 distances from d−σ to d+σ. The reported range is a sampled geometric sensitivity, not a probability interval or a timing measurement.

The off-center solver recovers the earlier centered shell vector within 0.003 ppm; its independent Newton integral agrees on the differential field vectors within 1.52 ppm. One tiny near-cancelling sightline originally missed the 20-ppm relative tolerance (26.1 ppm, absolute 2.47×10⁻¹⁰ mm/s per year). Evaluating the spectral radial modes directly instead of interpolating removes that miss; exact radial predictions also cover the whole distance grid. The inherited angular/domain changes still move the combined forced sightline vectors by up to 68 ppm, above the original 20-ppm target. The two independent field readouts can agree more closely than two different evolutions. Solar registration, the adopted [ordinary mass model](https://docs.galpy.org/en/v1.3.0/reference/potential.html), and the wave preparation matter more for interpretation than these digits.

**Use the right files.** `sightlines-exact-angular24-cap.csv` / `sightlines-exact-angular28-diff.csv` are the finite, original-background forecasts. `diskbox-cap-timing.csv` / `diskbox-diff-timing.csv` are the disk-loaded **stationary** forecasts with the common ordinary foreground, direct satellite excluded in both stationary models. All sightline acceleration columns are in mm/s per Julian year except the explicitly labeled fractional period rate in s⁻¹. No timing outcomes, fits, catalogue ranking, or evidence ratios. See `DERIVATION.md` for equations, `NEXT.md` for the decision and `REPLAY.md` for provenance and reruns.
