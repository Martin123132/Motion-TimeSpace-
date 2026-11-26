> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# Isolating the photon stress over a finite exposure

21 November 2026. Local extension of the [sealed launch result](../mts-unprojected-maxwell-metric/RESULTS.md). Two mirror placements, the same equal-width finite Maxwell pulses, original common action and thresholds; no sky fit or external coupling value. **A single positive Gaussian aperture can suppress both unwanted tides over a short, nonzero exposure while retaining the displayed Weyl–photon response.** The width/centre are calculated before testing, not fitted to the tidal readings. Each aperture is stationary during its exposure.

## What the metric does after launch

Let T=c_light Δt/L, with time average uniform from launch to T. Write the differential spatial stress as S_ij, in turn ordinary, the Weyl–photon improvement per c_W/L², or the reduced spin-two improvement per (4κa_C+d)/L². The dimensionless tidal readings below multiply those respective coefficients, with a common κAB source normalization. They are not three physical accelerations of comparable expected magnitude. The preparations have identical scalar density (also for these differential derivative sources by reflection), trace-free stress, vanishing initial differential momentum and no added homogeneous metric data. These conditions matter.

For h solving (∂t²−Δ)h_ab=2κ S_ab with zero differential data, geodesic deviation is −R_0y0z. For the mean over a Gaussian centred at X and over the exposure, the exact metric readout is

    mean tide/κ = ⟨∂t h_yz(T) − ∂y h_0z(T) − ∂z h_0y(T)⟩ /(2κT).

Here h_00=0 for the difference; this is not a formula for a generic sourced metric. Using conservation, ∂t S_0i=∂j S_ji, the independent launch-slice forecast uses B[S]=ΔS_yz−∂y∂j S_jz−∂z∂j S_jy. At even degree 2n the derivative of the tide/κ is the 2n-th derivative of S_yz plus the sum of Δ^(n−1−j) B[∂t^(2j)S(0)] for j=0,…,n−1. Divide by (2n+1)! for the coefficient of the exposure average. The Schwartz-class electric data give polynomial-times-Gaussian jets by Maxwell evolution; no time-step fitting enters.

On the positive launch aperture (width .455090 L per axis, centre 1.681793 L), the frozen leading laws are:

    ordinary = −0.2551906574 T² + O(T⁴)
    W        = +0.7655719721 − 1.786334602 T² + O(T⁴)
    D        = −0.01813584163 T² − 0.6463577968 T⁴ + O(T⁶).

The quartic D coefficient is large compared with its quadratic coefficient. At T=.16 the exact D reading is −0.00087658; keeping the spatial metric term alone would instead give +0.00363628. Momentum changes the sign. The order-eight forecast on the fixed aperture exceeds 2×10⁻⁸ for all three columns at .32; the independent quadratures there agree. Do not conflate Taylor truncation with quadrature error.

**Independent calculation.** Reconstruct the real Maxwell fields from the spherical-wave Cauchy solution, take their time derivatives analytically, and derive the W source by varying a test metric (not the forecast's source projection). For radius d=T−t the 3D retarded propagator is d times a spherical average. Its convolution with the Gaussian is the launch Gaussian times exp(−d²/(2p²)) sinhc(d|x−X|/p²). Differentiate that kernel for h′_yz and the two momentum gradients, integrate over the source time, then divide by T. This is not an expansion in T and does not replace momentum with the stress divergence. Both signs were evaluated separately. The fine spatial refinement moved a mean by ≤1.37×10⁻¹⁴; changing time quadrature by ≤1.59×10⁻¹². The coarsest ordinary launch residual 5.26×10⁻¹² missed the 10⁻¹² launch gate, and was not promoted. Independent plane-wave checks test all kernel derivatives through third order. Exposure coefficients (not bundled here) · retarded readings (not bundled here) · [error by order](evidence-001.zip) (archive member: `fixed-window-errors.csv`).

## Predict the aperture rather than assume a perfect instantaneous measurement

Put s=T², u=1/(1+2p²), h=(uX)². Factor the common nonzero √h u^(3/2) exp(−h/u) from all three columns. At s=0 the ordinary coefficient is 2(h−2u); on h=2u the D coefficient is 8(2u²−1). Their Jacobian determinant in variables (h,u) at u=1/√2 is 64u, nonzero. Smoothness of these Gaussian averages and the retarded initial-value solution gives a locally unique pair h(s),u(s); W remains nonzero by continuity. This is a local existence result, not a claim about unlimited exposures. Successive powers of s are obtained by solving a two-by-two **linear** equation at each order with that same Jacobian. Predicting an observing configuration is not adding a free action parameter. Frozen geometry (not bundled here) · coefficients of the geometry (not bundled here).

Positive side, twelfth-order preparation, independent retarded result; sign reverses on the negative side:

| T | p | X | ordinary | W | D | both nuisance readings within 2×10⁻⁸? |
|---:|---:|---:|---:|---:|---:|:---|
| .12 | .464532 | 1.703653 | −7.08×10⁻¹⁴ | +.707806 | +7.00×10⁻¹³ | yes |
| .24 | .494356 | 1.773674 | −7.70×10⁻¹⁰ | +.556059 | +1.12×10⁻⁸ | yes |
| .32 | .527836 | 1.853895 | −2.56×10⁻⁸ | +.428839 | +5.79×10⁻⁷ | **no** |

Eighth-order geometry passes only .12. Both orders and all misses are retained. The largest change between independently refined geometry-test integrations was 2.32×10⁻¹². These response residuals are not bounds on Wilson coefficients or evidence of a detection. Decisions (not bundled here).

**Timing requirement.** At the .24 geometry the ordinary slope for an error in actual duration, keeping the prepared aperture fixed, is −0.09618423 per dimensionless T. The two symmetric finite differences agree with the analytic derivative on extrapolation. Dividing by the W gain, an absolute timing error δT can imitate about 0.172975 δT in c_W/L², before width/placement error, residual baseline, uncertain D, detector response or noise. This is not immunity to clock errors. Signed sensitivities (not bundled here).

**Alternative with fixed hardware.** A signed combination of the original aperture at .04, .08 and .16, with weights (+1.86081997,−.58441738,+.02981038) from the launch forecast alone, gives numerical responses (−1.03×10⁻¹², +0.999999999987, +3.20×10⁻¹¹). Equal absolute input errors can be amplified by up to 2.476 in this one combination. The full three-column inverse is poorly conditioned (~28,140); do not describe all three parameters as well determined. Repeated cumulative exposures have correlated noise. [Raw check](evidence-001.zip) (archive member: `three-window-test.csv`).

## A cross-check facing an external observable

The same coefficient controls photon propagation through tidal curvature. A direct action variation, checked independently against a weak Schwarzschild metric, gives a per-mode squared-speed slope of magnitude 24 in c_W GM/(c_light²r³) for a tangential ray. **The historical timing coefficient in checkpoint 4945 uses 12 for the corresponding dispersion slope.** A speed shift versus a squared-speed shift must not be interchanged. Comparing both primary sources confirms the mismatch between printed dispersion formulas for the stated full-index convention. No new astrophysical limit has been inferred. [Normalization derivation, primary sources and fixed-endpoint prediction](OPTICAL-MATCH.md).

**Next:** put this action-derived propagation law through a fixed-emitter/fixed-receiver ray calculation at the saved binary geometry, then compare with historical timing assumptions before converting a residual into a bound. This is a path to testing the **same** coefficient on the sky, rather than adding another synthetic detection claim. Full matching, including the finite QCD contribution, remains a distinct input. [Reproduction](REPLAY.md).
