> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# The four-pion threshold: a derived stress norm and a photon data check

**21 November 2026 · Local checkpoint.** The real-photon matching calculation now has an explicit leading-order stress coupling to all four-pion charge configurations. Four pions need both phase space *and orbital motion* to carry spin two: the squared stress norm rises as the **11/2 power** of the excess energy. Its coefficient was derived on paper and recovered by an independent relativistic phase-space integration. Nothing was fitted to the angular data.

| Pair energy | Four-pion / two-pion stress amplitude norm, both at tree level | Tree four-pion norm / reconstructed two-pion norm |
|---|---:|---:|
| 0.60 GeV | 0.0000591 | 0.0000453 |
| 0.70 GeV | 0.00124 | 0.000846 |
| 0.80 GeV | 0.00418 | 0.00248 |

These are **norm ratios, not percentages of the mixed photon–gravity signal**. [Full calculation](STRESS.md) · numbers and numerical refinements (not bundled here). At 0.8 GeV the tree calculation is a low-energy estimate without a higher-order uncertainty, not a rigorous upper bound.

**The matching result.** From 0.540 GeV to the equal-mass four-pion threshold (0.5582816 GeV), the additional signed contribution to −F₃(0) is **+6.97 × 10⁻⁶ GeV⁻²** in the retained elastic reconstruction. Above threshold, continuing *only* the old channel gives **+5.75 × 10⁻⁵ GeV⁻²** up to 0.800 GeV; this second number is a **reference**, not an inclusive result. We did not extrapolate the Dai–Pennington low-energy magnitude array past its support. Separate windows and controls (not bundled here).

**What could reverse the sign?** Unitarity bounds the sine of the relative two-pion production phase by the product of the four-to-two photon and stress norm ratios. Using the mixed-order stress estimate at 0.8 GeV, reaching a 90° relative phase there would require a photon amplitude norm ratio of at least **404**. This identifies a quantitative test; it is not evidence that the actual photon norm is below it. It also leaves changes in the magnitudes and any independent contact term separate. [Derivation, failure control and data coverage](UNITARITY.md).

**What faced observations.** We tested 12 charged Mark II and 136 neutral Belle angular bins, using the published acceptances, no new fit and no invented charge-channel decomposition. Both calculations use identical one-loop chiral spectator waves; one replaces only the isoscalar helicity-zero D wave with the frozen dispersion calculation. In the two charged energy bins, the replacement predicts 127.1 and 107.0 nb versus 100.7 and 87.3 nb observed. For example, in the first neutral bin it gives **10.54 nb versus 4.52 nb** observed; the unchanged one-loop control gives 10.78 nb. The neutral excess grows to roughly fourfold in the last bin. The D-wave replacement alone cannot repair the discrepancy. These are comparisons of absolute central rates, not covariance-weighted significances. They probe the **combined** photon amplitudes; they do not isolate the sign of the gravitational product. [Angular predictions and inputs](ANGULAR.md) · [angular rows](evidence-001.zip) (archive member: `angular-comparison.csv`) · aperture rates and rate-independent shapes (not bundled here).

**Next local calculation:** gauge the same leading pion action and compute the actual two-real-photon → four-pion amplitude with its sign. Include both photon orderings, insertions on different charged legs and the two-photon contact on a charged leg. Require a Ward-identity zero for **each** photon (with a deliberate missing-contact failure), the charged two-pion Born normalization, and Bose/flavor controls. Project the equal-helicity spin-two component or integrate it directly against the stress tensor. This supplies the missing photon numerator and the direct four-pion cut as a theory estimate rather than assuming it vanishes. Rescattering corrections to the two-pion magnitudes, and calibration of the ordinary photon S wave, remain distinct.
