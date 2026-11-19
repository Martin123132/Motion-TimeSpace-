# A local tidal source bound valid on either side of the Compton crossover

The question is what is induced by an ordinary weak field, as distinct from how much stress was already present. Use the same prepared particular solution, homogeneous carrier and static Fourier lapse as LOCAL-FORCED-RESPONSE.md. Let w=m²/K² and θ=mt+θ₀. Without any cycle average,

    δρ / (ρ₀Ψ) = −(1+4w) + cos(2θ)
    δp / (ρ₀Ψ) = −1 + (1+4w) cos(2θ).

At the level of the standard Einstein trace-reversed equation on the common-metric branch, R_hat0hat0 from a material sector is 4πG(ρ+Σp) in c=1 units. This is a source attribution in a local orthonormal frame, not the full Riemann tensor. In particular gradient energies cancel in the active trace of the minimally coupled real scalar even before linearizing: ρ+Σp=2(∂_hat0 h)²−m²h². Its *induced* part on the static forced branch has the contrast

    δ(ρ+Σp) / (ρ₀ Ψ) = −4(1+w) + 4(1+3w) cos(2θ).

This recovers more than a time average. The mean coefficient is −4(1+w), the peak absolute coefficient is bounded by 8+16w at **every phase**. Phase mixing is not required for the second statement. To evaluate the independent numerical control, solve the original KG equation on a finite weak static metric in one periodic spatial direction; measure the cosine Fourier coefficient of the full proper stress at 257 times. Check both the constant and twice-carrier frequency pieces, two phases, two metric amplitudes and K/m=0.25, 1, 4. local-tidal-controls.csv uses the predicted coefficients, not a fit.

Restore c, physical wavenumber K and rest-mass density ρ_mass. Normalize against the **applied Fourier tidal scale** c² K² |Ψ|, not the local Ricci tensor of vacuum GR (which can vanish). The phase-uniform induced contribution to |c² δR_hat0hat0| divided by that scale is at most

    [4πG ρ_mass/(c²K²)] [8+16(mc/ℏK)²].

For the stationary *mean* substitute 4+4(mc/ℏK)². The coefficient per unit supplied density is tabulated in SI, with K=2π divided by the stated physical wavelength. Thus the induced trace is suppressed relative to applied tidal scale as K⁻⁴ in the long-wave, gradient-dominated material-response term, crossing to K⁻² (not K⁻⁴) for K much larger than the inverse Compton length. A linearized solution is required: |Ψ| and 2w|Ψ| must both be small. These powers are transfer coefficients, not a real-space law for the force of the Sun or a PPN residual vector.

Why this distinction matters: the undriven populated carrier already contributes ρ₀[1−3cos(2θ)] to the active trace. Free waves or boundaries can add more, and changing the metric in Einstein's equations can contribute at the same order as an induced material term. The bound above intentionally does not discard any of those from a total gravity test. It computes the source derivative conditional on fixed homogeneous occupation and a stated preparation. No local density, halo mass, representative phase or gravitational constant was obtained by fitting. The next genuinely relativistic test is to include the metric response and the carrier's free state consistently, then compare a physical tidal observable (including Weyl) for the same ordinary source, rather than treating this Ricci coefficient as the whole local-GR prediction.

Prior art: the parent action is the retained real-pole subfamily, not an invented fluid. Coherently oscillating scalars, scale-dependent pressure and the relation to cold matter have established antecedents, e.g. [Hwang & Noh (2009)](https://arxiv.org/abs/0902.4738). The preceding parent handoff also cites [Khmelnitsky & Rubakov](https://arxiv.org/abs/1309.5888) on the background oscillating potential. What is being checked here is a forced, phase-resolved source for this retained pole and a separate test of its preparation and regime, not a discovery of scalar dark matter or a general solution of Einstein–Klein–Gordon.

