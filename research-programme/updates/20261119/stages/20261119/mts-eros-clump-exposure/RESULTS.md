# EROS-2: the choice of monitored stars can change even the sign of the lensing shift

**What is new.** We coupled the retained common-metric point-lens calculation to actual EROS catalog star positions and colors. We recovered a discrepancy between two published ways of selecting the sources, propagated both, and constructed two explicit distance assignments that no red-clump mean or variance measurement can distinguish. They predict opposite signed changes in microlensing optical depth. There was no event fit, mass adjustment, or extra MTS coupling.

## Which stars and times?

- [Hamadache et al., 2006, original paper](https://www.aanda.org/articles/aa/pdf/2006/28/aa4893-06.pdf), [versioned vector figure source](https://arxiv.org/src/astro-ph/0601510v2). The 66 field labels of Fig. 1 sum to **6,830,000** stars, versus **5,569,216** in the published all-field latitude row. The excess of 1,260,784 exceeds even one whole unit of 10,000 per field. This does not diagnose the cause or invalidate the survey; it rules out substituting these labels for final weights. The five latitude counts sum to 5,562,460; keep the 6,756 difference unallocated. The reported denominator is 6.62 billion star-days: about 1,189 days per star, not the entire elapsed survey.
- From [the collaboration's observation and object catalogs (II/390)](https://cdsarc.cds.unistra.fr/viz-bin/cat/II/390) and [data-release paper](https://doi.org/10.1051/0004-6361/202557321), all 66 fields are identified; 2,058 of 2,112 potential CCD quarters have modern object catalog entries. The old analysis reports 2,063 retained after rejecting 46 of 2,109 reconstructed quarters. The two sets are not demonstrated identical. Reference-image positions are not the old acceptance bits.
- The lower panel of Fig. 5 contains 1,199 ordinary points for the central longitude strip (the highlighted symbol is not an extra population). Figure ordinates yield approximately 4.546 million stars. An order-preserving registration to the upper latitude sequence and modern CCD layout identifies 1,179 unique slots even after widening the sky tolerance to half a degree; 1,151 also have actual catalog footprints. On those, the plotted and independent archive-center latitudes differ by at most 0.022 degrees. These are reconstructed spatial labels, not released source IDs. Do not extrapolate this strip to 66 fields.
- Using archived paired images and the published 8.5-day cadence rule gives **859–1,600 days** across ordinary CCD fields; the stricter paired/six-chip/distinct-night convention gives **856–1,600**. For CCD 2 the first four seasons are explicitly omitted. On just the 1,179 registered plotted slots, the reconstructed count-times-season sums are 5.662 and 5.613 billion star-days. Neither is claimed to be its share of the published exposure: the accepted-star list, historical image quality flags and original time accounting are not identified. We did not renormalize them.
- EROS uses the event sum of crossing time divided by CCD efficiency, with prefactor π/(2 × 0.75), divided by the sum of monitored times; the published depth refers to a physical impact parameter below one. The 400-day ceiling, pre-day-900 100-day restriction, observing seasons, and sampling requirements matter. Five days is the lower end of the reported **detected** times, not an independently established sharp efficiency step. A physical timescale-restricted depth cannot exceed unrestricted depth for the same stars/impact convention; this is not a deterministic bound on a noisy measured estimator. Do not multiply the efficiency into the corrected depth a second time.

## Testing the selection itself

The Fig. 3 magnitude axis increases downward. In deviations from its cross, both prescriptions require |ΔR| < 1 and |ΔC| < 0.25, where C=B−R. The printed third condition is **ΔR > −4ΔC−1**; the polygon actually drawn enforces **ΔR < 4ΔC+1**. They remove opposite blue corners. Of 9,458 plotted marks, the two rules retain 1,819 and 1,674, with 229 differing memberships. The conservative coordinate-rounding intervals do not overlap.

We retrieved all **20,922 distinct archive IDs** in cg6104l (field 610, CCD 4). It is the second lettered quarter: a pilot counterpart to the paper's “quarter 2”, not proof of an identical reduction. Matching only identifier prefixes and celestial coordinates of the paper's 120 positional anchors to modern quarter rectangles supported the usual numeral→letter rule in 100, disagreed in 17, and gave no unique matching rectangle in three; no duration, residual or event selection was used in this check. Fig. 3 is not itself a complete archive source list.

| Same fixed cross, cg6104l | Printed | Drawn | Membership differs |
|---|---:|---:|---:|
| Reference magnitudes | 4,070 | 3,760 | 520 |
| Median magnitudes | 4,071 | 3,759 | 522 |

With reference magnitudes the digitization/photometry rounding counts are 4,064–4,081 versus 3,751–3,771. These ranges describe rounding, not total systematic errors. We did not pick the rule that got closer to a preferred prediction.

## Propagating through the retained light and gravity model

Both smooth backgrounds (MTS and spherical NFW control) have exactly the same compact stellar disk/remnant input. The spherical-versus-bar alternatives **below describe the central stars**, not different halo models. Values are ideal dimensionless optical depths in units of 10⁻⁶, for this pilot, not all-sky or duration-selected fits.

| Reference-photometry source assignment | Spherical, printed / drawn | Bar, printed / drawn |
|---|---:|---:|
| Same local external clump moments, Gaussian modulus conditional on sky only | 0.6990 / 0.6992 | 0.9321 / 0.9326 |
| All differential reddening-corrected brightness assigned to distance | 1.0068 / 0.8161 | 1.4482 / 1.1433 |

In the first row, 3,686 / 3,408 stars have unique positive-variance [OGLE-III distance cells](https://ftp.astrouw.edu.pl/ogle/ogle3/ext/blg/README.txt); 384 / 352 are missing. In the second row the independently tabulated cell at the quarter center anchors all stars, but a common intrinsic brightness and a fixed extinction law are **assumptions**. The inferred means are 8.58 / 8.07 kpc. Across the 12 directly matched cells, the optical brightness variance is **3.98–9.68 times** the independent clump distance-modulus variance. Interpreting it all as depth is not consistent with transferring those moments to this union, and neither transfer is guaranteed.

**A constructive result.** On the same 3,783 distinct matched stars we kept even the *entire multiset of distances* fixed within each cell and changed only which stars occupy the far side. Both assignments reproduce the external modulus mean and variance. In the barred foreground the printed-minus-drawn difference was **+0.0691 × 10⁻⁶** in one case and **−0.0698 × 10⁻⁶** in the other. The spherical foreground gives **+0.0394 and −0.0399 × 10⁻⁶**. The annular living-star response also reverses sign. These are possible assignments, not bounds or claims about actual star locations. This shows why getting a better mean distance alone cannot resolve this particular test.

**A result that does not require assigning individual distances.** From positivity of the retained stellar density we bounded every allowed ray and source distance over a padded survey footprint. For arbitrarily distant sources the entire-footprint ceilings are 17.06 and 64.86 × 10⁻⁶ (spherical/bar, rounded here; use CSV for the bounds). A conditional count/exposure envelope reduces them to 11.48 and 35.50 × 10⁻⁶. If every source is no farther than 8 kpc the latter become 0.892 and 1.542 × 10⁻⁶; the distance ceiling is a hypothesis, not an observation. These are deliberately one-sided limits, not point predictions, and do not justify a preference for either halo.

The original paper's aggregate depth and portions of its outcome table were visible while locating the estimator; this is not a blind study. Neither results nor residuals entered the code, no survey score was calculated, and no source parameters were fitted. See DERIVATION.md, verification.json and NEXT.md.
