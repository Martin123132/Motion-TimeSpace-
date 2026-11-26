# Normal energy, surrounding material and the finite-radius Newton comparison

## Which quantity is being compared

Use the **existing** common-metric evolution in normal proper time λ, unit lapse and zero shift. Write the centre-to-centre dimensionless volume factor as V=exp(ℓ+2β), so that the spatial volume element is r²V dr dΩ. The shell radius is a comoving coordinate; it is the clock, not the coordinate sphere, that stays physically fixed. Subscript 2 denotes the coefficient of P₂; a tangential vector coefficient multiplies ∂θP₂. Only first angular order around the spherical host is retained. Products retain the host to the same order as the original solver.

For a quadrupolar mass perturbation outside the detector, the Newton Poisson contribution is +∫ d₂ dr/(5r). Define M[a,b]=∫[a,b] (VE)₂ dr/(5r), with E the **normal energy**. Its relativistic counterpart for this test is the evolving **source moment** q A⁻³ M, using the launch normalization, not a claim that the relativistic tidal tensor equals a flat-space Poisson integral. A=a/a_launch is read on the original proper clock, q=(c/c★)² and the geometric duration is √q times the saved physical duration. The output is the change from each state's own launch, then signed host minus host-free, wave minus cold. The Hubble factor and length normalization are not fitted. No independently imposed exterior harmonic is inferred from this moment.

## Flux and work from the matter equations

Project ∇μ Tᵘᵛ=0 on the unit normal, with extrinsic-curvature sign ∂λ log V=−K. Then

    ∂λ(√γ E) = −∂i(√γ jⁱ) + √γ Kᵢⱼ Sⁱʲ .

Writing jᵣ,jθ in the retained orthonormal frame and using the radial/tangential coframe tilt v₂ gives

    ∂λ [r² V E]₂ = −∂r F + H_ang + H_p + H_s
    F     = r² [exp(2β) jᵣ]₂
    H_ang = 6 r V₀ (exp(−β₀) jθ₂ − v₂ exp(−ℓ₀) jᵣ₀)
    H_p   = r² [V K p]₂
    H_s   = (3/2) r² [V Aᵣ Bᵣ]₂ .

Here p=tr S/3, Aᵣ is the radial traceless extrinsic curvature and Bᵣ is the radial traceless orthonormal spatial stress. The factor 6 is −ΔΩ P₂/P₂; the shear contraction factor is 1+2(−1/2)²=3/2. Mixed radial/tangential traceless products of two purely quadrupolar quantities would be second order. Neglecting ∂λV would spuriously leave a K E source; keeping V cancels it. The prescribed environment contributes its actual pressure and spatial traceless stress; its E and j are the **locally evolved** fields, not a replacement from the incoming density interpolation. Work in a single branch need not vanish when the matched contrast is small.

With φ=1/(5r³), integration of this equation on [a,b] gives positive entering face φ(a)F(a), negative leaving face −φ(b)F(b), radial bulk ∫φ'F, angular transport ∫φH_ang, pressure work ∫φH_p and shear work ∫φH_s. The sign of entering at a=6 is therefore opposite to its sign in the interior energy budget. Finally

    Δ(A⁻³ M) = A_final⁻³ ΔM + (A_final⁻³−1) M_launch .

This is why nonzero dilution of the initial perturbation is included even if the net surface flux is small. For a time-integrated *individual face* on the proper clock, use A(t)⁻³ inside the integral in both models; do not confuse it with the preceding endpoint decomposition.

## Actual material terms

- Dust: for coordinate particle number n, P=exp(−ℓ)∂r u and γ=√(1+P²), E=ρ nγ/V, jᵣ=ρ nP/V and p=ρ nP²/(3Vγ). Its Bᵣ=2p at the retained angular order. jθ₂=(ρ n/V)₀ exp(−β₀) u₂/r.
- Canonical wave: let L+iθ be its complex logarithmic amplitude/phase in the rotating frame, Π=z+K/(2μ)−i, and G=exp(−ℓ)∂r(L+iθ). With ρw=ρ exp(2L), E=ρw(1+|Π|²+|G|²/μ²)/2, jᵣ=−ρw Re(Π*G)/μ, p=ρw(|Π|²−1−|G|²/(3μ²))/2 and Bᵣ=2ρw |G|²/(3μ²). Use the corresponding angular phase and amplitude gradient in jθ. The incident trace and anisotropy are not duplicated here.
- Compute energy increments from differences of coordinates, not subtraction of nearly equal total energies. For instance δγ=(2P+δP)δP/(γ_new+γ_old); δ(VE_other)=V_new δE_other+V_old expm1(δ log V) E_other, with the angular product rule. The wave amplitude and normal momentum use the same divided differences. A regular analytic free spherical Klein–Gordon mode independently checks energy, flux and the sign of the retarded evolution: δω=√(μ²+k²)−μ, δE₂/ρ=(2+δω/μ)j₂(kr)cos(δωt), jᵣ₂/ρ=−kj₂'(kr)sin(δωt)/μ. A uniform expanding radiation control instead tests nonzero pressure work and no transport.

## Why the 6 Mpc wall had to move

The historical method reflects phase values at its outer wall. Its derivative at that very face is **exactly zero**. This kills the dust potential gradient and the wave logarithmic gradient used for material flux, although it does not delete all environmental current. The saved central curvature detector was far inside that wall: the duration permits only about 0.041 comoving Mpc of light travel at q=32. The old wall was not a physical measurement of surrounding mass transfer.

The face-to-cell derivative is a difference of an effective face primitive: for original weights a=(75/64,−25/384,3/640), Gᵢ=Σⱼ aⱼ Σₖ₌₋ⱼ…ⱼ Fᵢ₊ₖ; DᵢF=(Gᵢ₊₁−Gᵢ)/Δr. The wall's odd continuation in this derivative gives G_wall=(Σaⱼ)F_wall, not F_wall for nonzero physical flux. Internally the faces telescope. Integrate the exact discrete weak form first and then reassign the difference between cell-weighted and physical face terms to radial bulk. Changing the face rule in the diagnostics alone cannot restore material that never flowed in the saved evolution. The different dust and wave discretizations are not assumed to conserve this diagnostic identically: endpoint versus transport error is tested.

We therefore evolved the same launch on overlapping annuli with 6 Mpc strictly **inside**. The fast 2iμ normal oscillation and its triangular coupling to the logarithmic wave are integrated by an exponential fourth-order update; this is a second evolution algorithm, checked by a forced complex oscillator and against the stored interior histories. A wider annulus tests the influence of the artificial ends. All 22 fields in each expanded packet are tested against the corresponding saved fields on the overlap. Far-shell comparisons use both the reflected far end and a separate one-sided linear numerical continuation of cell and face values; neither is promoted to a measured physical exterior.

## A bound on the saved experiment, not on arbitrary cosmologies

For each nonoverlapping shell and time quarter, subtract independently calculated Newton and relativistic entering face, leaving face, radial bulk and angular terms. Add the two relativistic stress-work terms and the launch dilution difference. A bound must also include integration error. For each individual GR host, control, matter species group and epoch, calculate its **own** finite density increment minus its **own** integrated flux+work. Do likewise for the independent Newton ring integrals. Include their absolute errors **before** wave–cold and signed–zero subtraction. For the quarter-wise bound use the absolute differences of cumulative terms at consecutive quarter endpoints; sum over shells, quarters and components. Triangle inequality bounds the finite output without relying on fortuitous cancellation of these numerical residuals across the two theories. All ppm denominators are the absolute secular Newton detector change at the same elapsed fraction, on each original aperture, never the static curvature. The result does not bound a peak between samples, omitted orders of the sky harmonics, arbitrary incoming fields or the continuum discretization error. Grid, time and boundary comparisons test those specified numerical choices separately.

The spatial Hamiltonian constraint also contains extrinsic and intrinsic geometry. With γᵢⱼ=ψ⁴ γ̃ᵢⱼ the exact scalar relation in the retained 8πG units is 8 Δ̃ψ=ψ R̃−ψ⁵(2E−2K²/3+AᵢⱼAⁱʲ). A density moment measured here supplies only one input to this relation. Computing the remaining metric divergence, curvature and extrinsic terms, together with the independent homogeneous tidal boundary datum, is the route from this test to a constrained metric prediction.

## First direct geometry check, at launch

The retained initial metric is conformally flat: ψ=1+χ, K=−3H, AᵢⱼAⁱʲ=3Bᵣ²/2 in the orthonormal frame. Thus S_eff=ψ⁵(E−3H²+3Bᵣ²/4) sources −4Δψ. For its ℓ=2 coefficient u, (u'/r+3u/r²)'=(Δ₂u)/r. The effective-source exterior moment is exactly −4/5 times the difference of this surface combination at the two radii. The growing harmonic b r² gives a nonzero constant 5b at both ends; the decaying r⁻³ mode gives zero. Neither can be determined by treating the volume integral as two separate boundary values.

We evaluated the source from the independent energy, normal momentum, metric and shear in each launch packet. Direct point derivatives on opposite sides of an element junction need not agree. For a flux trace recover the derivative in just **one** adjacent element of the saved metric using a linear test v equal to one at the cut and zero at the other end:

    [r² u' v] = ∫ (r² u' v' + 6 u v − r² S_eff,2 v/4) dr .

The right-hand side uses the metric inside this one cell and its local physical source, not the integral over the shell to be predicted. Evaluate from either side where available and compare with independent source quadrature over all intervening elements. At the exterior endpoint only the inner cell exists. This check concerns the static matched launch observable; its relative ppm is not ppm of the several-orders-smaller secular change. At later times R̃ and Δ̃−Δ₀ need not vanish. In the general case the effective source for −4Δ₀ψ acquires −ψR̃/2 and +4(Δ̃−Δ₀)ψ in addition to ψ⁵(E−K²/3+A²/2).
