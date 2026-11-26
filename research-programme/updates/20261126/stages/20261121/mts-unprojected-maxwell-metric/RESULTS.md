> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# A finite launch measurement isolates the curvature–photon response

21 November 2026. Local calculation on the retained zero-local-motion-source branch. **The new result is a spatial readout, not a measured coupling:** one equal-width pair of finite Maxwell pulses admits a positive Gaussian aperture where the ordinary Einstein–Maxwell cross-tide and the displayed reduced curvature-squared contribution both vanish at launch. The Weyl–photon response does not. The negative and positive centres can be read separately or differenced. The conclusion concerns one signed tidal component of the pulse contrast, not vanishing total gravity.

## From the parent to the measured component

Checkpoint 4947 (not bundled here) supplies the common metric coupling κ, Einstein and Maxwell terms and effective curvature terms. No new coupling was chosen to match either dust or light. Use lengths in pulse widths L, times in L/c; take the leading order in metric perturbations (quadratic in prepared Maxwell amplitude) and first order in the effective coefficients. Keep the differential constraint-satisfying launch data, no freely added tensor wave, and the detector in the original metric frame.

Two individually physical Maxwell preparations add/subtract a poloidal field on a toroidal field. Their densities agree while their stress and oblique momentum differ. Generating the fields in real space, we drove the unconstrained-by-projection harmonic and synchronous metric evolutions and took derivatives of the resulting metrics. Spatial constraint data were imposed at launch, not reapplied to repair the evolved readings. Both formulations reproduce the individual Poisson dust tide with the same κ, and agree on the four-dimensional linear Riemann tensor to 4.30×10⁻¹¹ in the adopted units. The dust residual is at most 1.28×10⁻¹¹. For the equal-width equatorial mode kL=1, the differential tide is initially +16/51 of the magnitude of the matched dust longitudinal tide, and becomes −0.51940 at t=2L/c although instantaneous tensor stress is still positive. These are Fourier amplitude comparisons, not collocated dust and radiation.

Swapping to two different fixed-energy widths changes oblique momentum from cubic to linear at early times, with opposite slopes at wide versus narrow widths. Deleting only differential momentum can pass the simple tensor test but fails the oblique momentum constraint. [Signed targets](evidence-001.zip) (archive member: `signed-forecast-comparisons.csv`) · complete paired metric checks (not bundled here) · broken-source control (not bundled here). No fit to astrophysical observations is involved.

## A finite detector, not a single spatial Fourier mode

At launch the equal-width pair has matching energy, zero momentum and identical minimal metric data. In the differential derivative sources the scalar density is also zero (an axisymmetric reflection-odd scalar cannot be nonzero); the launch momenta vanish by time-reversal symmetry of the electric preparation. For these data the initial off-diagonal tidal acceleration in parallel Cartesian frames is κ times the differential yz source. This is why a finite spatial average of that source is a tidal readout **at launch**; it is not a general instantaneous stress-to-tide rule. Away from launch one must propagate the metric. The localized readout is an average over an ensemble on the background slice, not a model of a single rigid extended instrument.

Let p be the Gaussian standard deviation **per coordinate** in units L and X its centre on the positive x axis. Define u=1/(1+2p²). In units of the common κAB factor the ordinary launch tide is

    Q(p,X) = 2 u^(3/2) exp(−u X²) uX [(uX)²−2u].

This follows by averaging 2x(x²+y²−2)exp(−r²) over the Gaussian. Choose X²=2/u; the same normalized positive aperture then gives the two leading response coefficients

    W = 8√2 exp(−2) u²,     D = W(2u²−1).
    δA_yz / (κAB) = (c_W/L²) W + [(4κa_C+d)/L²] D.

Here W is the displayed Weyl–photon term; D is the reduced spin-two curvature term, degenerate in this response with a possible Ricci–photon matching coefficient d (d=0 in the displayed action). The derivation varies the action before evaluating the real fields; its independent check differentiates correlation functions with derivatives transferred to the Gaussian. See [action and normalization](ACTION-MATCHING.md), exact real-space identities (not bundled here) and three nonspecial apertures (not bundled here).

**Double null:** p=√[(√2−1)/2]=0.45508986, X=√(2√2)=1.68179283. Now Q=D=0 exactly in these equations and W=4√2 exp(−2)=0.7655719721. At −X the sign reverses. Independent integration at both centres gave ordinary residuals below 2×10⁻¹⁶ and gravity residuals below 2×10⁻¹⁰; the largest discrepancy from any of the six analytic values was 4.18×10⁻¹⁰. Orders 26/36 and halved time stencil passed the unchanged checks. These residuals are numerical errors, not upper bounds on nature's coupling. [Prespecified checks](FINITE-NULL-DESIGN.md) · six raw readings (not bundled here).

**Registration matters.** At the positive null the ordinary slope is S=8 exp(−2)u^(7/2)=0.32188. A shared x translation of both Gaussian centres by ε contaminates their oriented half-difference at second, not first, order: −10 X exp(−2)u^(9/2) ε². The half-sum instead monitors Sε at first order. Halving ε from .01 to .005 reduced the measured ordinary leakage by a factor of 3.99982. A *separation* error or a common *width* error does not cancel: independent offsets of .001 in half-separation or width gave ordinary leakage of +3.21×10⁻⁴ or −3.48×10⁻⁴. Instrumental tolerances, shot noise, finite exposure and the value of c_W are not determined here. Offset controls (not bundled here).

## Independent dynamical check

For the complementary Fourier experiment the ordinary launch zero is reached by a different pulse width at each of kL=.5,1,2. Two distinct critical scales distinguish W and D algebraically. The corrected differential metrics were evolved using full Cartesian field products and an off-shell action variation; their tidal, metric, stress and current readouts were compared with separately frozen momentum-space predictions. A further test uses **only two synthetic launch readings per coefficient scenario** to reconstruct the two amplitudes, then predicts the other observables through t=2L/c. For the simulated mixture (+.3,−.12) the two amplitudes return as +.30000000000094 and −.11999999999894. All 3,234 remaining readings pass the original per-channel tolerances (worst fine-grid absolute difference 1.44×10⁻¹⁰). These are correlated predictions of a linear effective model, not independent data points or a physical coefficient measurement. Synthetic calibration (not bundled here) · transfer and worst-case input-error gains (not bundled here).

## What failed and what to do next

Direct second differences of the original coarse dense time interpolation missed the 2×10⁻⁸ Einstein threshold for the two synchronous light preparations at kL=2, t=.08 (4.45×10⁻⁸). Local integration of metric increments around the same epochs resolved the derivatives without changing the thresholds or discarding those rows. A coarse narrow-pulse source quadrature also missed its target; the next two quadrature orders agreed. An initial dust index mistakenly included broken-current controls; the [original indexing diagnostic](evidence-001.zip) (archive member: `precheck-control-index.csv`) is retained, and the accepted dust test uses only the true dust trajectories.

**Next parent test:** compute the ordinary, W and D *time-dependent finite-aperture tidal acceleration* for this same double-null preparation, not another ideal mode. Predict the leading exposure-time leakage before comparing with a retarded real-space metric solution; use both signs and the already tested registration controls. The separation here acts on the displayed leading operators, not all possible local effective interactions. It establishes neither an anomalous value relative to conventional physics nor a galaxy occupation. The LMC signed force result (not bundled here) remains a separate sky test.
