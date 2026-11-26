# Gas correction closed on the saved histories; the remaining target is a radial change in the tide

19 November 2026 · Private · Existing couplings, occupations, signed bands and 2 × 10⁻⁵ numerical tolerance

## What the gas actually does
Integrated the atomic and molecular gas against the full azimuthal satellite field at **17,158 distinct source times** across the six simulated LMC histories, including the already defined finer L2M11 grid. Both ordinary foregrounds reuse those samples; they are not 34,316 independent events. Changing only the projected gas drive moves the present relative centroid **0.00090–0.00121 pc** in vector norm. The corrected separations are **2.719–18.676 pc**; no signed sky band changes. Most of the correction comes from HI. The largest sky change is 1.04 × 10⁻⁷ in units of 10⁻¹⁰ m/s². Static NFW gets the same acceleration-reference correction without inventing a halo wake.

Even without using the phases, the integrated absolute force correction on the represented histories is at most **0.000217 km/s**. The positive coupled response then limits its possible centroid effect to **0.012 pc**. This is not an extrapolation from the present-day force error. Signed cancellations in the actual time evolution further reduce the effect.

Spatial and time checks are separate: 36 gas-component comparisons against the uncompressed vertical quadrature (plus other convergence probes); frozen, genuinely off-grid numbers checked at one time in **each of 912 archive intervals**; an independent final convolution with the original spatial force and wall readouts. Largest frozen off-grid discrepancy in the mean ordinary correction is 1.90 × 10⁻⁶ (km/s)²/kpc. Highest-resolution nested time checks on the final **total** centroid vector differ by at most 7.64 × 10⁻⁶ relative. The small **increment alone** changes by up to 3.84% in the time comparisons: do not quote its fine digits as equally precise. There is no rigorous continuum quadrature-error certificate between all sampled physical times.

## What the data require beyond this correction
Compare vertical gravity evaluated 1.5 kpc above and below the same point in the plane. Their difference divided by 3 kpc gives the mean vertical compression K. This difference cancels a uniform acceleration exactly, regardless of where the origin is placed. All numbers in the table are in 10⁻¹⁰ m/s² per kpc.

| Cylindrical radius | Envelope from the original north/south bands | Corrected MTS | Matched static NFW |
|---|---:|---:|---:|
| 6.0 kpc | 0.735–0.909 | 0.545–0.570 | 0.613–0.636 |
| 8.3 kpc | 0.390–0.502 | 0.354–0.361 | 0.371–0.377 |

These are the retained force bands from [Lim et al., Figure 9](https://arxiv.org/html/2305.13358v3#S3.F9), projected conservatively as component intervals, and the spread across two prepared grounds and six orbits. The paper reconstructs accelerations from tracer phase space with an approximate equilibrium condition. The table is not a joint confidence interval, a likelihood or a new independent survey. See TIDAL-READOUT.svg.

On **every MTS history**, the minimum extra vertical compression at 6 kpc exceeds the maximum allowed extra compression at 8.3 kpc by **0.02346–0.04113** in the same units. Thus even an arbitrary uniform acceleration **plus an arbitrary constant tidal tensor** cannot close both bands on these prepared backgrounds. A smooth repair must have a radial gradient somewhere between the probes of magnitude at least **0.0102–0.0179** in those units per kpc, falling outward. The associated necessary change in mean weak-field tidal curvature is 8.46 × 10⁻⁴⁹ to 1.49 × 10⁻⁴⁸ m⁻². This is a metric-shape target, not a claim to have measured a third derivative directly.

We subjected NFW to exactly the same test. It too underpredicts vertical compression at both radii, but for it the two allowed *correction* intervals overlap: some uniform-plus-constant symmetric tidal field is compatible with all eight components in each case. That is a feasibility statement, not an observed extra tide or a fit to promote. A uniform acceleration **alone** works for neither model. A diagnostic allowing both an arbitrary uniform field and independently adjustable spherical radial pulls at the two radii is feasible for both; the more restrictive data statement above should not be generalized to all possible additional sources.

The vertical tide includes horizontal force divergence as well as density. Under the additional assumption that the correction to horizontal divergence is equal at both radii, the MTS contrast corresponds to a lower bound of **4.0–7.0 solar masses/pc²** on the extra inner column relative to the extra outer column (depending on ground and orbit). We did **not** add or fit such a sheet. DERIVATION.md gives the field identity and sign convention.

## Could a different wave phase rescue the present source?
We also allowed the represented linear waves to cooperate freely at conservative source-energy ceilings, not merely at their actual final phases. The signed force required is at least **3.15 times** the combined m=0,1,2 support, **3.06 times** even with relaxed north/south consistency. The m=1 part is bounded on its retained finite basis. See MODE-BUDGET.md for the inverse-mass energy metric, its source and domain qualifications, and the control that removes each actual signal before testing a replacement.

**Next physics step:** use the retained mass densities and gravitational potential to separate the missing vertical compression into a column-density requirement and a horizontal-divergence requirement at both radii. Keep the wave and ordinary matter contributions distinct, with the same NFW comparison; do not spend another pass tuning the small hydrogen correction. Such a decomposition can say which parent stress or preparation needs changing, something a new fitted acceleration constant cannot do.
