> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# The two Einstein evolutions recover the same finite-speed tidal response

**Result:** On the original q=64 signed-cloud test, all **64/64** comparisons pass the previous 20-ppm tolerance with the analytic launch metric carried into evolution. These are 2 formulations × 2 environments × 2 proper aperture widths × 4 clock times × 2 curvature readouts on **one** preparation family. They are not 64 observations. The largest same-detector difference between the two evolved formulations fell from **215.79 to 0.716 ppm** of the matched Newton increment. This separates a numerical representation error from a physically predicted, sign-changing signal.

| Central q=64 contrast | Maximum absolute difference, ppm of the full Newton change |
|---|---:|
| Actual tide vs unchanged longitudinal + retarded transverse stress | 6.693 |
| Ricci vs Gauss readouts of one evolution | 4.809 |
| Same readout, two Einstein evolution forms | 0.716 |
| Time refinement, 4 to 8 | 2.595 |
| Spatial refinement, 160 to 200 cells/Mpc (same time step) | 2.609 |
| Central outer radius, 3 to 4 Mpc (same time and space steps) | 0 at the recorded precision |

Times and positions are those of the precursor: four fractions of 273.43 years on a fixed proper aperture, with normalized widths 0.15 and 0.30. Parameters and the numerical acceptance gate were not adjusted. [All signed comparisons and gates](evidence-001.zip) (archive member: `all-controls.csv`) · finite-speed signal against pure Newton (not bundled here).

**The gravitational signal survives the repair.** At the full time the curved tidal change differs from the independently evolved pure Newton tide by **59.34–65.14 ppm in magnitude**. The previously calculated transverse material-stress term has the opposite sign for the two environments and is about 59–60 ppm there. Adding it to *pure Newton* leaves at most **6.65 ppm** at that time, without using the longitudinal exterior reconstruction as the comparator or fitting a coefficient. This identifies the leading finite-speed difference on this short clock. It is not a measurement of a universal correction or of a galaxy's occupation.

**Where the discrepancy came from.** Replaying the old ADM evolutions with only the new detector changes their late narrow splits from −79.783/+226.267 to −79.769/+226.211 ppm (positive/negative host). Evolving the corrected derivatives but reading them with the old detector gives +1.351/−4.753 ppm. Updating both gives **+1.365/−4.809 ppm**. Thus changing how one reads the same histories does not produce the improvement; changing the geometric derivatives in the field evolution does. The original constrained-trace formulation was already inside tolerance, and some of its individual errors increased slightly. Nothing was subtracted from a measured late constraint. ADM crossed replay (not bundled here) · retained formulation crossed replay (not bundled here).

**What the prospective test did and did not predict.** The earlier analytic-curvature launch estimates were below 1.66 ppm in absolute value. The actual time-dependent split was small against the 20-ppm gate but not universally below 1.66 ppm. The largest error against the frozen signed estimate was **4.60 ppm**, for negative-host narrow ADM at full time (−0.218 forecast vs −4.809 measured). The initial-only approximation is not a sub-ppm prediction. Frozen signed values (not bundled here) · [primary comparisons](evidence-001.zip) (archive member: `primary-comparison.csv`).

**Independent controls.** Exact inhomogeneous LTB dust plus a spatial coordinate quadrupole: both endpoint channels in both evolutions reproduce the proper monopole change to 0.00064 ppm and introduce less than 0.163 ppm of angular leakage relative to that nonzero change. A distinct finite scalar mode added to the reference passes the analytic spatial-curvature, ADM trace-acceleration and decimal tidal-difference checks (relative error below 1.14×10⁻¹²). All six physical Green references reproduce the original metric at the saved source nodes to relative 4.0×10⁻¹⁶; doubling the integral order changes the reference/derivatives by less than 3.2×10⁻¹⁵ in the tested maximum-norm comparisons. Those numbers are checks on numerical representation, not error bars on alleged fundamental physics. [Dust](evidence-001.zip) (archive member: `dust-control.csv`) · non-reference scalar perturbation (not bundled here) · physical launches (not bundled here) · analytic multipoles (not bundled here).

**Restart:** derivation (not bundled here), [local replay and packet layout](REPLAY.md), 48 four-epoch restart packets and checksums (not bundled here). The earlier LMC density-to-force result (not bundled here) concerns different inputs and is unchanged.

**Next discriminating test:** change the contraction parameter, not another detail of the q=64 detector. Use q=128 on the same 144-Mpc formation and physical clock, freeze the independent Newton plus *finite-travel* transverse-stress prediction, then build the matching positive/negative/zero Green preparations and test both evolution forms. Compare with q=64 and previously exposed q≤32, including the wider aperture and the Newton-only null. The retarded kernel must be evaluated at the new propagation time rather than assuming a 1/q or quadratic-in-time trend. A failure there would constrain how far this mechanism extends; keep the 20-ppm gate and the original state preparation.

