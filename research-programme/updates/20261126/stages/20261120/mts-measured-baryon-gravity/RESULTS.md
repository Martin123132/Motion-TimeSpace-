> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# The LMC moves the wave inward, but does not supply the inner polar force

Local follow-through on the [original fixed-number derivation and its 192 same-band checks](../../20261119/mts-lmc-fixed-occupation-axisymmetric/RESULTS.md). Its offline verifier passed again: 227 local and 1,070 inherited files. In the original calculation 1.67–3.48 × 10⁸ M☉ transferred inward through the 6.185-kpc sphere, without repairing a signed force band. We then made **a new prediction on a differently prepared Milky Way**, without splicing in any response from the old background.

## What the new foreground puts at risk

The source was frozen before the force comparisons. We used all four mapped stellar/remnant populations, their measured local vertical profiles rather than two fitted layers, the same globally normalized stellar mass, the already-counted central excess once, nine paired inner HI/H2 measurements, and the local multiphase gas and brown-dwarf inventories. See [frozen protocol](PROTOCOL.md). The source gives 0.0832 M☉/pc³ in the plane, 41.64 M☉/pc² within ±1.1 kpc and 45.12 M☉/pc² integrated at R=8.3 kpc. None of the force bands was used to choose a mass. The empirical inputs are the [Lian stellar data](https://github.com/lianjianhui/Source-data-for-MW-mass-paper), [Marasco et al.](https://arxiv.org/abs/1707.00743) and [McKee et al.](https://arxiv.org/abs/1509.05334), from the saved local sources. Gas reconstructions use line profiles, hence this is not a blind test. Transporting local vertical profiles to other radii, spherical deprojection inside 4 kpc, gas continuation, mask and axisymmetry are assumptions. No mass was added for undocumented phases; their absence from the calculation is not evidence of zero true density.

We solved the same self-gravitating stationary equation on this new potential. The two inherited occupations give outer speeds **225.21 and 224.12 km/s** without refitting, rather than about 250 km/s on the simulation disk. Recalibrating to exactly 224.03 km/s at 17.58 kpc gives 2.1405 × 10¹¹ M☉, only 0.063% below the second saved population. This recovers the *old calibration* on the new source; it is not a new independent validation or a formation law.

## Six alternative histories, eight signed observables

For each prepared wave we drove the first-order, reflection-even axisymmetric sector with the six unchanged [archived LMC histories](https://zenodo.org/records/8015660). The perturbation is orthogonal to the ground; the density response is twice the real product of ground and perturbed wave. Inner mass can change while total occupation is conserved. [Equations and controls](RESPONSE-PROTOCOL.md). On these new grounds no old m=2 or other nonaxisymmetric response is included. The two direct-field frames are the original site-minus-point frame and the archive accelerating frame, not an inferred extended stellar-centre acceleration.

| Quantity | Two inherited occupations, six histories |
|---|---:|
| Wave mass moved inside 6.185 kpc | +1.666–3.450 × 10⁸ M☉ |
| Wave mass moved inside 8.434 kpc | +3.160–6.552 × 10⁸ M☉ |
| Added north inner radial acceleration | −0.01304 to −0.00642 |
| Added north inner polar acceleration | −0.000562 to −0.000208 |
| Inner north radial shortfall filled | 1.12–2.28% |
| Signed bands reached, MTS / matched static NFW | 2 of 8 / 2 of 8 |

Accelerations are in 10⁻¹⁰ m/s². Opposite changes outside each sphere cancel the inside transfer; integrated number defects stay below 1.6 × 10⁻¹⁷ of the total. The only bands reached are the two outer polar bands. This holds before and after the induced wave, in all six histories, either frame, and also in the separately outer-anchored preparation. The NFW control uses exactly the same ordinary mass, direct field and outer speed; it has no live halo wake. These are marginal diagnostic bands, not eight independent likelihood measurements.

**The angular requirement is sharper than a 2/8 count.** At 6 kpc, subtract the known ordinary and site-minus-point direct forces from the two polar intervals and reflect the southern residual into the north. Their intersection needs a north even dark polar force of **at least +0.1662 to +0.1671**, depending on history. On the two inherited populations the *whole* evolved dark component gives **+0.00828 to +0.00875**: about 5% of the needed minimum. The LMC increment actually decreases it. A spherical potential gives zero polar force for any radial normalization. In potential language, with μ=z/r, the required local angular slope is ∂Φ/∂μ = r² aθ/R in consistent units: at least about **3,270 (km/s)²** at the inner north probe. This is a local constraint on the sum of multipoles, not a fitted quadrupole. The outer polar intervals permit zero. See even-dark-requirement.csv and angular-potential-requirement.csv.

## Vertical-force cross-check

At R=8.5 kpc, the source adds **2.57 M☉/pc²** of actual ordinary column between 1 and 2 kpc, compared with 0.36 on the previous two-layer source. The anchored *stationary* MTS force equivalent increases only from **50.40 to 64.99**: +2.57 ordinary column +28.55 dark column −16.52 radial Poisson correction = **+14.60**. Matched NFW gives +16.03. The vertical force is not the mass column. An independent horizontal-divergence integral checks the identity to 0.0043 M☉/pc² in the fine runs.

Including the direct LMC tide and induced wave, north/south-symmetrized at the sampled meridian, gives **14.68–14.78 for outer-anchored MTS, 16.05–16.07 for matched NFW**, versus the [Bienaymé et al. RAVE](https://doi.org/10.1051/0004-6361/201424478) central difference **28.4** in those units. These are not tracer forward models or a significance calculation. The measured ordinary tail helps the column, but changed radial gravity offsets it. The LMC contribution is too small on these preparations.

## Accuracy and next test

Independent Newtonian ring quadrature split at the measured stellar-height knots gives stable forces; the full multipole-field check misses 2 × 10⁻⁵ relative at three vertical-force sites, so direct ring values, not the approximate multipole probe values, were used for the ordinary force readout and outer anchor. The wave Hamiltonian uses the full-space field projected into its angular basis. All 72 temporal refinements pass the inherited target. 55/72 coarser-to-finer combined spatial, field and trial-basis checks pass it. Largest relative difference of an induced component is 8.56 × 10⁻⁵; the largest difference of a **total** signed force is below 8 × 10⁻⁷ in sky units, with no changed decisions. This is not a rigorous infinite-domain error bound. Densities, individual bands and errors are retained.

**Next local test:** replace only the spherical deprojection of the already-counted central stellar excess with the independently sourced barred geometry, keeping the same mass, orientation constraints and outer reference. Bound how much of the required inner angular slope this redistribution can supply; compare both dark models before assigning missing angular gravity to new wave occupation. Recompute rather than import a bar response from a different ground. If none of the allowed geometry reaches the band, quantify the residual instead of tuning to it.
