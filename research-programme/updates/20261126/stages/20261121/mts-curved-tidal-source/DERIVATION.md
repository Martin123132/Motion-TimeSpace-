> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# Which radial tide does a driven curved tensor produce?

**Conventions.** The retained local evolution uses unit lapse, zero shift, signature −+++, mixed extrinsic curvature Kⁱⱼ=−(γ⁻¹∂tγ)ⁱⱼ/2, and sources in geometric Einstein-equation units (κ already absorbed). Angular quantities below are the coefficients of the quadrupole, first order in angular perturbations about the *evolving spherical* solution. This does not linearize away the monopole. A dot holds the comoving coordinate r fixed; a prime holds time fixed and differentiates proper radius ρ. On each time slice dρ=A(t,r)dr and the area radius is B(t,r). Do not commute those derivatives. The general Gauss and Ricci equations are standard GR, not new MTS couplings; see [Gourgoulhon, §§3–4](https://arxiv.org/abs/gr-qc/0703035). The reduction and checks below relate them to the retained fields.

**Spatial force from the shape of the two-spheres.** Let a=B′/B, let L and b be the perturbations of the radial and angular log scale, and let the radial-angular metric component be B v D_A Y in proper radial coordinates. The trace-free angular metric coefficient d multiplies D_A D_B Y+3Ω_AB Y. In the saved r chart the physical v here is exp(b₀−ℓ₀) times the stored tilt. The unperturbed two-sphere mean curvature is 2a; its perturbation is jY with j=2b′−2aL+6v/B. This follows by differentiating the area element along the radial unit normal, including its angular shift (ΔΩY=−6Y). The radial Ricci equation and the contracted two-sphere Gauss equation then give, suppressing Y,

    δRic_nn = −(∂ρ+2a)j + 2a′L + 6L/B²
    δR₃ = (8b+12d)/B² + 2δRic_nn − 2aj .

Here the term 6L/B² is the angular Laplacian of the radial lapse with its minus sign. At first order radial-normal and radial mixed diagonal contractions agree on a spherical background.

**Driven time evolution.** The mixed-index ADM equation gives the following equation for the actual radial logarithmic metric amplitude, with τ=tr K, σ=(Kʳᵣ)TF, π=(Sʳᵣ)TF and S=tr S:

    L̈ = −δRic_nn − δ[τ(τ/3+σ)] + δ[ε/2 − S/6 + π].

For the instantaneous spatial transverse-traceless (TT) completion at fixed L, b=−L/2 and v=BL′/3+B′L. Then j_TT=L′+4aL. Substituting, the spatial acceleration for this part is

    −δRic_nn(TT) = L″ + 6aL′ − [6(1−B′²)/B² − 2B″/B] L.

The *rest* of the actual spatial acceleration is exactly +(∂ρ+2a)(j−j_TT). It vanishes for that completion but is not assigned zero on the measured fields. This is an instantaneous decomposition; TT need not evolve as an autonomous sector on a time-dependent material background. In flat space, with no other shape, extrinsic or matter source, the earlier L″+6L′/r law follows. No extra coupling or fitted radiation amplitude.

**Geodesic tide versus electric Weyl curvature.** Put M=(K²)ʳᵣTF=2τσ/3+σ²/2 through the retained angular order. Radial trace-free geodesic deviation in this experiment has sign opposite to Rⁱ₀ⱼ₀. The detector field and electric Weyl curvature obey

    T = −(Rʳ₀ᵣ₀)TF = −σ̇+M = −(Ric₃ʳᵣ)TF − τσ + M + π,
    Eʳᵣ = −T + π/2 .

Products here mean monopole products and their full quadrupole linearization; they are not products of quadrupoles. These equalities distinguish a time observer built from the physical shear from a spatial reader built from metric derivatives and anisotropic stress. Injecting the total Riemann tide into a Weyl forecast without the last π term would be incorrect. A perfect isotropic stress has π=0 but can still drive the radial scale via the preceding amplitude equation.

**Independent sign, matter and curvature controls.** We evaluate the full four-dimensional metric, not the evolution RHS, at signed rational perturbations of a time-dependent curved geometry with positive Einstein energy density. Metric first and second derivatives give the four-dimensional Riemann tensor and Einstein stress; an independent three-dimensional contraction gives Ric_nn and the spatial scalar. Centred signs at two amplitudes for both a TT and a non-TT deformation test five nonzero coefficients (including Weyl and anisotropic stress). These are sourced manufactured geometries, not claims that MTS prepared them. [Controls](evidence-001.zip) (archive member: `spacetime-controls.csv`).

**Retained-source check.** The numerical calculation uses the original physical densities, pressures, cold species, wave gradients and incident stresses. The full acceleration and each of its above contributions are recorded separately on the six saved trajectories and their matched references. The aperture calculation uses the original optical path variation and moving proper windows, not a coordinate-radius average. Riemann and Weyl here are classical observables of the retained common metric; no quantum assumption is imported.
