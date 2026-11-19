# Collisionless angular transport with nonlinear gravitational feedback

Use the same equal-sided p,q,K=p+q, μ=p̂·q̂=−1/2, CDM-synchronous chart and perturbative amplitudes as the sealed early-counterflow calculation. No 1/2 in front of the whole second-order field. A cosine input and a sine flux are Re[b exp(ikx)] with b real and negative imaginary respectively. Taking a product at K gives half the sum of its two ordered products. Only the scalar about K is required for energy and longitudinal current; we azimuthally project *after* applying the crossed angular operator. Averaging each parent distribution before crossing it gives an incorrect source. For linear metric and massive momentum conventions see [Ma & Bertschinger](https://arxiv.org/abs/astro-ph/9506072); for second-order tetrad radiative transfer and polarization see [Pitrou](https://arxiv.org/abs/0809.3036). The following implementation and the numerical MTS results are local, not results taken from either paper.

## Null and massive geodesics

Write γ=exp(s) for the spatial metric after removing a². For a first-order scalar with axis p̂, s=A p̂p̂ᵀ+B I, A=−2D+6η, B=−2η, A'=2t, B'=−2(t+D')/3. D is the synchronous CDM linear density; t=kσ is its shear amplitude (inverse Mpc). Local tetrad momentum length Q in units of the present neutrino temperature is comoving; E=sqrt(Q²+(am/T₀)²), v=Q/E. Let n be its unit tetrad direction, P=I−nnᵀ. To the order needed,
```
dxⁱ/dτ=v[(I−s/2)n]ⁱ ;    (ln Q)'=−nᵀs'n/2
n'=(P/2){v ∇(nᵀsn)−[s'+v(n·∇)s]n}        (linear direction field).
```
The symmetric tetrad contraction exp(−s/2) γ' exp(−s/2)=s' through second order. Homogeneous momentum redshift has already been factored out. With f=f_FD+G F, G=−Q df_FD/dQ, ℓ=d ln G/d ln Q=1−Q tanh(Q/2), each incoming scalar obeys
```
F'+ikvξ F=−(A'ξ²+B')/2, ξ=n·q̂,
FlnQ'+ikvξ FlnQ=−ikv(1−v²)ξ F.
```
For exactly massless species use bolometric brightness divided by four in place of F, ℓ=−4 and FlnQ=0; the −4 follows by integrating by parts in Q. For the generated scalar set u=n·K̂, w=n·p̂=u−ξ, and write angle brackets below for the azimuthal average at fixed u. For equal inputs the two ordered products have the same azimuthal projection. Their summed source is
```
S = (ikv/2)⟨(A μ w+B ξ) F⟩
  + (1/2)⟨(A' w²+B')(ℓ F+FlnQ)⟩
  − (1/2)⟨(μ−wξ)(ikv B−A'w) ∂ξF⟩ .
F₂'+ikvu F₂ = C₂'/3 − t₂(u²−1/3) + S .
```
Terms are respectively the perturbed streaming speed/direction in coordinate space, gravitational redshift of the existing distribution, and angular deflection. Keeping only a density and pressure is not equivalent. Incoming angular polynomials and their derivatives are evaluated at ξ, not at u. Different azimuths and polar orders were checked. For the massive species use weights Q² E G dQ / ∫Q²E f_FD dQ for the fractional density, an additional v for flux and (1+v²)/2 for the active trace entering Raychaudhuri. No negative-momentum extrapolation. The native a⁴ρν ratio between early times and today fixes m/T₀=356.59353 using the thermal integral; a third scale factor was reserved for checking that conversion. Setting only transport mass to zero while keeping background weights/other histories fixed isolates the mass correction to streaming; it is not a refitted cosmology.

## Close the scalar shear without imposing its value

The exact momentum constraint on the same synchronous slices is ∇ⱼTʲᵢ−∂ᵢ tr T=−8πG a² Jᵢ, with T=γ⁻¹γ'/2 and Jᵢ the normal momentum with its spatial index down (scale-factor convention of the native solver). This T is the expansion tensor, not matter stress. The scalar shear is t₂=(3/4)(K̂K̂−I/3):s₂'. The commutator in T has zero crossed scalar for these equal inputs. The quadratic connection gives, with b=K̂·p̂=1/2,
```
G/k=b D[μ t−(D'+t)/3]+(b/2)[A(t μ²−(D'+t)/3)−B D'] .
t₂ = −C₂' + 3[8πG a² J_K + G]/(2k).
```
In J_K combine the covariant acoustic momentum, k(f₀'f₂+f₁'f₁/2) in the native gravitational units, and the streaming species. Convert a streaming species' orthonormal longitudinal sine momentum to the coordinate covector: add (A μ+B) times its *incoming* flux divided by four. Not doing this amounts to changing the metric coupling at quadratic order. The same massive/relativistic energy and stress source enters C₂''; the shear cannot be computed with one momentum and the energy with a different distribution. The subdominant rolling scalar's second-order stress is not provided on this window; photon–baryon tight-coupling errors are distinct from angular resolution.

## Regular scalar beginning and independent constraint

Use the preceding regular adiabatic Gaussian branch. Write x=kτ, C₁=x²/4, C₂=c x² with c=−3/16; no decaying, entropy or primordial anisotropic mode. In radiation domination the linear shear t/(kx)=t₁=−5/(15+4f), where f is the relativistic free-streaming fraction. The incoming real distribution divided by x² is Y=1/12−t₁(ξ²−1/3)/2; its imaginary part divided by x³ is −ξY/3. The second-order even coefficient is Y₂=c/3−t₂₀(u²−1/3)/2. Its odd coefficient is [−uY₂+Im(S/(kx²))]/3 using the regular first mode. Solve the *same momentum constraint* at order kx for t₂₀, including the incoming-index lowering, the quadratic spatial connection, and the adiabatic acoustic dipole P₂=c x³/9. This gives t₁≈−0.30057 and t₂₀≈+0.16907. Changing the physical initial fraction, shape, or branch would change these numbers. At the earliest time the thermal particles are ultrarelativistic for the populated momenta. Finite-start error is independently tested.

Check with an equation not used to evolve density. For the scalar log metric parameter η₂ integrate 3η₂'=C₂'+t₂. The spatial Ricci coefficient on the triangle is
```
R₂=k²(3D²/8−9Dη/4−45η²/8−4η₂).
R₂−4ℋ C₂'+2D'²/3−(μ²−1/3)t² = 16πG a² δE₂ .
```
The geometric polynomial is computed from the quadratic Christoffel terms and the exp(s) inverse. Its initial constant is fixed by the primordial pulled-back R₂/k²=−3, not by setting the diagnostic residual to zero. Use **energy** on the right, not the active trace E+S. Another check integrates the independent massless energy equation with the native first flux and its quadrupole inferred from its linear Euler equation. These checks are diagnostics on a partial matter model; neither is interpreted as proof of a nonlinear junction.

## Scattering and continuation beyond this window

For the linear finite-opacity control, F_l are intensity moments, G_l the Stokes-Q moments relative to the Fourier axis. Both stream with k[l F_(l−1)−(l+1)F_(l+1)]/(2l+1). For positive conformal opacity κ, the collision gain is isotropic in F₀, adds 4v_b/3 to the F₁ target, and has polarized targets (F₂,G₀,G₂)=(U/10,U/2,U/10), U=F₂+G₀+G₂. Include metric sources 4D'/3 and 8t/15 in F₀ and F₂, drag 3κ(qγ−4v_b/3)/(4R_b) on baryons with R_b=3ρ_b/(4ρ_γ), and native thermal sound speed. Compare with the independent native solver, whose tight expansion is related in the opaque limit. The diagnostic diffusion integral follows [Hu & Sugiyama](https://arxiv.org/abs/astro-ph/9510117); no damping exponent is inserted into any calculated photon transfer.

For a cold-electron Thomson collision, incident bolometric polarization tensor H(n) is transverse to n. Let S=I−nnᵀ, V the electron velocity, Γ its boost, d=Γ(1−V·n), n_e the aberrated direction. The spatial screen transformation from the lab to the **electron rest** tetrad is U=[I+Γ² VVᵀ/(1+Γ)+Γ n_e Vᵀ]S. The rest-frame bolometric tensor gains d⁴ and solid angle gains d⁻². Transforming the gain and loss back gives per proper electron opacity:
```
C_lab(n)=(3/2)d⁻³ Uᵀ⟨ d² U H Uᵀ ⟩ U − d H .
```
Full scalar couplings come from Taylor expanding this expression, including the electron-density perturbation multiplying the *linear* collision. The implementation checks the quadratic expansion against the exact finite-speed equation, a boosted equilibrium, and four-force orthogonality. Two independent native first waves then generate cosine/sine multipoles of intensity and polarization (through l=6) at eight times. Density was set to the baryon perturbation for these samples; the separate derivative with respect to a common additional ionization perturbation is supplied, not silently set to a measured value. The electron-velocity perturbation here is orthonormal; second-order baryon covariant momentum must be converted before supplying a linear-in-V₂ contribution. The angular source alone is not the full quadratic propagation: include spatial transport, redshift, polarization-basis transport, reciprocal baryon drag and the electron-density history. Recoil/frequency redistribution and thermal Compton effects are outside this bolometric elastic limit.
