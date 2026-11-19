# What the EROS infrared and parallax counterparts actually constrain

**Selection:** the observer's original clump procedure supports the *drawn* boundary. **Distance:** the disputed sets differ strongly in near-infrared brightness, but the data do not establish a distance ordering for the full groups. **Gravity:** two well-matched, image-screened stars are in front of the entire 4–7 kpc stellar annulus under our explicit astrometric error model. Increasing compact mass there cannot lens those two sources. These statements use different evidence.

## Recovering the original selection

[Hamadache's 2004 thesis](https://publication-theses.unistra.fr/public/theses_doctorat/2004/HAMADACHE_Clarisse_2004.pdf), pp. 103–104, Fig. 6.4 and equations 6.7–6.9, labels the red magnitude as *positive* 2.5 log(red flux) relative to the clump; color is positive 2.5 log(red/blue flux). In calibrated coordinates the first offset is −ΔR while the second is Δ(B−R). Therefore the thesis inequality is **ΔR < 4Δ(B−R)+1**, the sloping edge in Fig. 3 of the [2006 paper](https://www.aanda.org/articles/aa/pdf/2006/28/aa4893-06.pdf), not the inequality obtained by applying the printed magnitude formula directly in calibrated coordinates. This is evidence for a historical implementation, not a claim to have the final survey source list.

The two-percent random reference-star subsample in thesis Tables 6.1–6.2 has 144,800 clump candidates in 66 fields. Multiplication by 50 gives 7,240,000, then the thesis's 23% overlapping-margin adjustment gives a field sum of **5,574,780**, 0.100% above the eventual 5,569,216. This reconciles the scale without asserting these are exact per-field journal counts or that every individual star has the same probability of duplication. The separate digitized Fig. 1 gross count is not an interchangeable normalization. The thesis used one 1,704-day duration, not the journal's total source-days.

Tables 4.1–4.2 recover field production end months: one in July 2001, 20 in May 2002, 40 in October 2002 and five in November 2002. Reapplying the retained cadence test to the archive, the six calendar/cadence choices yield 6.512–6.920 billion source-days at equal one-eighth short-chip occupancy. End-of-month/six-chip nights happens to give **6.62290** versus the published **6.62**. It is not a recovered mask. In 27 fields with all 32 Fig. 5 quarters registered, the short chip contains 8.86–11.51% of digitized sources. Those fields supply 43.06% of the end-of-month/six-chip CCD exposure difference; using their measured proxy fractions would require the other fields to average **14.25%** rather than the measured subset's **10.40%** to hit the stated total. No missing field was given that fraction as a measurement.

## Same optical IDs, independent infrared and astrometric readouts

Subset | Original IDs | Stable VVV counterpart | Clean infrared | Quality Gaia parallax
---|---:|---:|---:|---:
Printed-only | 415 | 344 | 185 | 172
Drawn-only | 105 | 88 | 30 | 58
Both | 3,655 | 3,442 | 2,368 | 2,403

All 20,922 original stars compete for matches, not just selected stars. [VVV PSF photometry](https://doi.org/10.1051/0004-6361/201935730), [VIRAC2 astrometry](https://www.eso.org/qi/catalog/show/424), [Gaia DR3](https://gea.esac.esa.int/archive/) and the [EROS archive](https://cdsarc.cds.unistra.fr/viz-bin/cat/II/390) were matched by position and epoch under the frozen protocol. At ±5 arcsec offsets there were still 655–703 Gaia and 1,087–1,171 VIRAC matches, versus 14,251 and 16,754 at the true coordinates across the quarter. These are chance-match diagnostics, not per-star false-match probabilities. The optical quarter boundary need not include every potential competitor. Source blending is not removed by astrometric registration.

- The median extinction-corrected K magnitude of printed-only stars is **1.2605 mag fainter** than drawn-only stars after the primary cuts (4×4 sky-block interval 1.060–1.354; alternative extinction slopes 1.261–1.262). If the two samples had the same characteristic absolute magnitude, that flux contrast would correspond to a distance ratio of 1.79. Equal intrinsic luminosity and representative completeness are not established.
- For the two exclusive groups, the corrected Gaia difference of **mean signed parallaxes** is −0.0533 mas (block interval −0.1349 to +0.0092). Six-parameter-only: −0.0111 (−0.0665 to +0.0440); no five-parameter-only comparison exists. VIRAC gives −0.4063 mas; even on the same eligible IDs its differential is 0.2895 mas more negative than Gaia's. The additional distance-canceling statistic π·10^[0.2(K₀−13)] gives opposite directions for the two catalogs. Do not invert a noisy group mean, treat luminosity as known, pool the catalogs as independent, or extrapolate the clean subset to the unmeasured stars. VIRAC is Gaia-referenced and shares VVV images with the PSF photometry.

## A direct prediction for the same mass that produces the vertical force

For a nonnegative compact foreground on a fixed ray, the ideal optical depth is proportional to the integral of ρ(D) D max(1−Dπ,0). It decreases with geometric parallax π. Right in front of the near edge the annular contribution is **exactly zero**, irrespective of how the annulus mass is normalized. With correct IDs, Gaussian random errors of at most 1.5 times catalog uncertainties and per-star absolute bias ≤0.05 mas, simultaneous 95% intervals on all 2,633 quality Gaia stars give three foregrounds. Two also pass the extra Gaia image-quality screen. Both belong to *both* optical cuts:

Star | Upper source distance | First possible annulus lens distance
---|---:|---:
cg6104l11414 | 0.868 kpc | 1.124 kpc
cg6104l31652 | 0.953 kpc | 1.124 kpc

Both have tight Gaia and VIRAC matches. The third has 37% multi-peak Gaia image windows, so its position alone is insufficient assurance. The separate test of two artificial, histogram-preserving source assignments finds six nearer-than-both source IDs, only one of which passes the extra image screen. The two clean annular zeros are **not** those witness exclusions. See `foreground-tipping-points.csv` for the bias and error inflation at which each zero ceases to be assured (one change at a time). These checks cannot exclude an unresolved blend in a historical EROS aperture.

For the 3,760 drawn-pilot IDs, including unconstrained distances on unmatched stars, the conditional ideal-depth derivative is **[4.76×10⁻¹⁰, 7.30×10⁻⁸] per additional billion solar masses** distributed like the existing annular living disk. Its paired inner vertical-force derivatives at fixed outer speed remain +5.324 for ground MTS and +5.137 for the spherical NFW control, in solar masses/pc² of force equivalent per billion. The optical coupling acts on the same ordinary stellar lenses in both; these derivatives are not a fitted or allowed mass increment. The printed-minus-drawn optical interval crosses zero. Dropping the Gaussian assumption, the prechosen supporting-line lower bound allowing arbitrary error correlations is zero; a separate precision-only design admits no stars. The stronger bounds are conditional, not distribution-free.

## How much the survey geometry alone buys

We bounded the positive stellar density on padded angular footprints for all 66 fields, independently of the quarter's astrometry. The reported total exposure is rounded: the retained 6.615–6.625 billion range is optimized over **all** saturation breakpoints plus both endpoints, and checked independently by linear programming. See `survey-exposure-certified.csv` (108 field-calendar/chip/depth cases). The older endpoint-only diagnostic `survey-exposure-envelopes.csv` has an overgeneral column label; its endpoints happen to attain the maximum in these data, but are not a valid method in general.

Across the 12 timing and chip scenarios, the all-distance ceilings on the ideal annular depth for the *existing* disk are (7.24–7.49)×10⁻⁷. Putting a ceiling of 8 kpc on all source distances would instead give (2.16–2.20)×10⁻⁷. The latter is an assumption, not a measurement. These are ceilings on weighted integrals conditional on the field footprints, historical weight model and foreground; not observed event depths or competing halo scores. We have not reconstructed individual 2006 event-duration acceptance, all source days, radial mass covariance or a formation-derived dark population. The highest-value next test is therefore on **how much independently measured stellar mass can be moved**, not on picking the chip scenario closest to the published exposure.
