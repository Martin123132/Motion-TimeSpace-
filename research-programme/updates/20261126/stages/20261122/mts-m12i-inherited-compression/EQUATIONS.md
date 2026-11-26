> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# Formation-derived compression: which part of the early state changes the late fraction?

Dates are a₀=0.003 (and separately the logarithmic interval midpoint), aᵢ=0.01 and a𝒇=0.05. Lengths are comoving Mpc. Conformal time η, peculiar velocity with c=1, H the physical expansion in inverse Mpc; dot denotes d/dη. All reported drifts are percentage **points of the host-normalized patch share**; currents and density states are not fitted or calibrated on a stream.

## Retarded solution, including both matching endpoints
Let X=(D₂, −aθ₂/B) over all species, B=aᵢ²Hᵢ at **the same** aᵢ in all runs. The previous equations (not bundled here) give X′=A X+S with prime=d/d ln a. G(b,a) is its homogeneous propagator, normalized to the identity at equal epochs. Source S contains quadratic numbers and velocities on the actual realization (continuity and advection), and for the wave the expansion of the quantum stress. The common Poisson potential is solved from *all* species including the induced D₂, never imported from the cold cosmology for the heavy run.

For each species write X=K+Z. K consists of ½ ∂ᵢ∂ⱼ(sᵢsⱼ) and −a/B times the divergence of −(s·∇)v, with s(k)=ikD₁/k² on uniform-mass labels. Z consists of −div s₂ and −a div(dot s₂)/B. Then, identically in this approximation,

    Zᵢ = G(i,0) Z₀ + G(i,0) K₀ + ∫ G(i,t) S(t) d ln a − Kᵢ .

Dropping either K₀ or the subtraction at i misidentifies ordinary motion as new dynamical compression. Z₀ and an additional forced solution for omitted stresses are not known to be zero. Benchmarks quote the displayed particular terms, without an inferred value for a homogeneous mode. The second-order contribution to the *change* of the inner fraction between i and f is ⟨W, e[G(f,i)−I]Zᵢ⟩. Here e reads target-minus-same-metric-CDM density, W is 100 times the label fraction times the difference of the patch and host mean windows, and ⟨ , ⟩ is the real Fourier product with conjugate partners counted. The subtraction of I compares the same hypothesis at both dates. Geometry, linear number ratio and normalization terms were already evaluated in the later-stage control; they are not counted again.

## An independent calculation from the force on a moving element
Write x(q)=q+s+s₂ in uniform mass labels. An Eulerian acceleration F evaluated at this point contributes F₂+(s·∇)F₁. Consequently the force-divergence source for Z's scaled velocity is
    −[k²Ψ₂[K] + δ_wave k⁴ K_density/(4a²m²)
      + δ_wave div F_Q,quadratic[D₁] + div((s·∇)F₁)]/(HB).
The rest of the linear response to Z, including self-gravity and dispersive pressure, is in A. In this reduced number chart the equation for the displacement density −div s₂ has *no quadratic forcing from a velocity product*: that product has already been removed into K. k²Ψ₂[K]=−Σ C K_density/(2a). The pressure divergence is ∇²[−D₁∇²D₁/2−|∇D₁|²/4]/(2a²m²), not a new wave mass or coupling.

For irrotational F₁ with T=div F₁ and Pᵢⱼ acting in Fourier space as kᵢkⱼ/k²,
    div((s·∇)F₁)=s·∇T − Σ (PᵢⱼD₁)(PᵢⱼT).
The other product used in this calculation is K_density=(D₁²+Σ(PᵢⱼD₁)²)/2 − s·∇D₁. This is a different numerical construction from the Fourier double divergence in the Eulerian route. In pressureless single dust, T=−C D₁/(2a). The s·∇ terms cancel **pointwise** and the scaled forcing becomes C [D₁²−Σ(PᵢⱼD₁)²]/(4aHB), the second displacement invariant. Testing the kernel on actual three-dimensional phases and the resulting growth with the inherited cold-simulation solution checks signs, time normalization and the moving-label transformation. It is not a prescription for a growing wave.

Three successive forcings isolate distinct effects: (1) matter-only linear Poisson plus leading scalar wave pressure; (2) add the difference between the native *linear* lapse and matter-only Poisson, sampled on each displacement; (3) add the remaining species acceleration inferred from H d(aθ₁)/d ln a. For (3) the archived θ₁ is not an independent observation: near agreement with the Eulerian route tests consistency, not data fit. The last route also allows the retained linear species forces to differ from the leading NR expression. None supplies second-order intrinsic photon, gas, metric, or scalar stress. The linear native density is volume-corrected energy density; finite-pressure continuity is not exactly a number pushforward. Interpolation and differentiation errors can appear in closure even if the continuum calculation is consistent.

## Keeping approximate modes separate
The intersection of the existing branch screens requires (aH/k)² and [x/(sqrt(1+x²)+1)]² below 2e−5 with x=k/(am). Both scales are assessed from a₀ to f for **inputs and outputs** using the retained test mass; k=0 is conserved and removed. H is largest in conformal units at a₀ here; the larger of both backgrounds is used. The screened-input calculation recomputes both members of each quadratic pair, rather than masking a previously generated result and calling its inputs screened. Output-only removal and the cross terms containing an excluded input can therefore be separated exactly. This is not a bound on primordial modes absent from the original seed or on pressure/metric effects not represented by those two scale tests.

## Unknown boundary and omitted common gravitational source
In addition to the propagated incoming Z₀, a missing common second-order lapse ΔΨ₂ adds source −k²ΔΨ₂/(BH) to all scaled divergences. Define U=−2a k²ΔΨ₂/Σ C, a dimensionless density-equivalent field (not an extra measured matter density). At time t the dual kernel before windowing is
    b(k,t)=Σ_C/(2aBH) Σ_over_velocity_channels [ e(G(f,i)−I) G(i,t) ]_velocity .
For a time-independent spatial pattern U the gain is ||W ∫b dt_log||. For arbitrary U with norm defined as box rms, averaged in *squared norm over ln a*, it is sqrt(Δln a ∫ ||W b||² dt_log). A pre-start perturbation of joint density/scaled-velocity box rms has gain ||W e(G(f,i)−I)G(i,0)||. The Cauchy–Schwarz bounds are sharp for unconstrained fields with these norms and Fourier support; neither tells us the size or correlations nature supplies. In dust the common-force projection vanishes for the differential observable, even though each species accelerates; in the heavy branch pressure allows a response. General species-specific second-order stresses are separate source terms and **not** bounded by this common-lapse number.
