# What produces the signed deformation?

This calculation uses the retained nonrelativistic common-potential branch; it does not postulate an extra interaction for the wave. Length is comoving Mpc, c=1, conformal time η is in Mpc, conformal Hubble rate ℋ is inverse Mpc, and a is dimensionless. Dark wave, cold matter and baryons source the same Newtonian potential with the previously saved coefficients C_s. In this approximation baryons are pressureless. The cold control is a different retained background; changing the **initial target velocity** is a separate intervention on each background. A fixed number in a late Galactic state and the early cosmological ensemble below are not equivalent preparations.

## Shape transfer on a finite spherical preparation

Use number density in units of the background, n_s, and irrotational peculiar velocity ∇V_s. Set n_s=n_s0+d_s P₂ and V_s=V_s0+w_s P₂ to first order in the quadrupolar perturbation. Let L₂=∂ᵣ²+2∂ᵣ/r−6/r² and L₀=∂ᵣ²+2∂ᵣ/r. Compare two states differing **only in their target initial quadrupolar velocity**, with unchanged exterior drive. Subtracting their equations removes that drive; it does not remove their induced interior gravity. Writing subscripts r for radial derivatives and primes for time,

    d_s' = −n_s0 L₂w_s − n_s0,r w_s,r − V_s0,r d_s,r − d_s L₀V_s0,
    w_s' = −ℋ w_s − V_s0,r w_s,r − φ₂ + δ_sh Q₂,
    L₂φ₂ = Σ_s C_s d_s/(2a),
    4a²m² Q₂ = L₂d_h/n_h0 − d_h L₀n_h0/n_h0²
                − n_h0,r d_h,r/n_h0² + d_h n_h0,r²/n_h0³.

Here Q₂ is the quadrupolar variation of +(∇²√n)/(2a²m²√n). At initial a=.01 all d_s and the extra potential vanish; w_target alone is the signed donor-minus-recipient phase potential. The independently evolved spherical fields supply n_s0 and V_s0, not a fitted density template. The Poisson Green integral uses regular origin, vacuum continuation for the *difference* outside the box, and the actual inside and outside quadrupole of the evolved interior. For source f=Σ C_s d_s/(2a),

    φ₂(r) = −[r⁻³∫₀ʳ f(u)u⁴du + r²∫ᵣᴸ f(u)du/u]/5.

For axial minus equatorial material marker splitting ΔR at spherical marker B, ΔR'=V_s0,rr ΔR+(3/2)w_s,r. The cap comprising μ=cosθ from 1/2 to 1 and its southern mirror, in the code's angular normalization, has first-order number change 3/16 [∫₀ᴮ r²d_s dr + B²n_s0(2ΔR/3)]; sideways flux is (9/8)∫₀ᴮ n_s0 w_s dr per conformal time. The factor 3/16 also obtains for the single northern cap using a hemisphere-normalized measure; ratios and the flux use the same normalization. These are checks on material transport, not an inference that density stays constant inside a fixed radius.

The full path independently advances all angular fields on the live spherical preparation. At x=ln(a/a_i) a shape fraction F obeys F_x=v/ℋ and F_xx=g/ℋ²−(1+∂ₓlnℋ)F_x, with speed and force each divided by initial radius. The forecast uses native velocities and independently reconstructed shell forces, with one backward force derivative to obtain the cubic term. Root tests use archived, held-out displacement and speed (not the forecast coefficients), one root per aperture on the sampled interval, and the elapsed log-a interval from window 64 as denominator.

## When an initially invisible relative flow begins to gravitate

This second statement is for a **homogeneous** background with no perturbing exterior potential. For each k>0 define S=Σ C_s D_s, P=Σ C_s V_s, and Φ=−S/(2ak²). The retained Fourier equations give

    S'=k²P,   P'=−ℋP + C_tot S/(2ak²) − C_h k²D_h/(4a²m²),
    D_h'=k²V_h,   V_h'=−ℋV_h + S/(2ak²) − k²D_h/(4a²m²).

Start from D_s=0 and C_h V_hi+C_c V_ci=0 with all other V_si zero. This is an explicit test preparation, not a derived Galactic population. In the all-dust limit S=P=0 remains an exact solution; the individual streams still move. For finite wave mass, write ω²=k⁴/(4a²m²). Differentiating S″+ℋS′=C_tot S/(2a)−C_h ω²D_h gives S′=S″=0, S‴=−C_h ω²k²V_hi and S⁽⁴⁾=−6ℋ_i S‴ initially. Differentiating the 1/a in Poisson then gives

    Φ_i = Φ′_i = Φ″_i = 0,
    Φ‴_i = C_h k⁴ V_hi/(8a_i³m²),       Φ⁽⁴⁾_i = −10ℋ_i Φ‴_i,
    Φ(η_i+t) = Φ‴_i t³/6 [1 − (5/2)ℋ_i t + O(t²)].

This is a signed, dimensional prediction, not a fitted time exponent. Each mode projects to the quadrupole through the saved shear selector and j₂(kr), or to the comoving radial force coefficient through −k j₂′(kr). Do not infer physical acceleration in m/s² from that coefficient without returning to physical coordinates. V_hi=0, zero projection, or m→∞ removes the leading signal. Halving/doubling the mass is a diagnostic applied only to perturbative dispersion, with formation inputs fixed, not three self-consistent cosmologies. Summed equations were integrated without subtracting almost equal component potentials. Independent component evolution uses each species’ canonical momentum aV_s and retains both large cancelling terms.

The underlying scalar wave pressure is established physics ([Hu, Barkana & Gruzinov](https://doi.org/10.1103/PhysRevLett.85.1158)). The result tested here is its conditional current-to-common-potential coefficient and order of onset on the retained MTS preparation; it is not a discovery of wave pressure or a proof of relativistic decoupling.

## Why the homogeneous null need not survive in a host

In a stratified sphere an irrotational compensator for W(r)P₂ must satisfy both n_c V_c=−(C_h/C_c)n_h W from the angular current and n_c V_c,r=−(C_h/C_c)n_h W_r from the radial current for **pointwise** cancellation. These imply (n_h/n_c)_r W=0. Instead the finite control solves Σ C_s∫n_s∇δV_s·∇u=0 in the admitted radial basis. This is weak initial divergence cancellation, not a vanishing local flux vector. In the cold experiment the compensator is baryonic, not a second copy of the heavy wave.

For a continuum follow-up write J=Σ C_s n_s u_s, Π_ij=Σ C_s n_s u_si u_sj. At δn_s=0 and zero changed exterior tide, δΦ=δQ=0 initially. Continuity and summed momentum then give S″+ℋS′=∂ᵢ∂ⱼδΠ_ij initially, even before a wave-pressure acceleration has developed; here S is the real-space total Eulerian density perturbation weighted by C_s. Thus a velocity-stratified preparation can differ from homogeneous cubic onset. Disentangling this physical term from the finite taper/projection error in δJ is the next test, not an assumption that a homogeneous cancellation holds in a galaxy.
