# From polarized transport to the heavy-field stress at the matching surface

Conventions, action, mode normalization, initial regular solution, native units, Einstein constraints, massive momentum weights and boosted Thomson collision are those of ../mts-streaming-counterflow-20261118/EQUATIONS.md. Wavevectors p,q,K=p+q all have magnitude k=1.98095677855/Mpc; μ=p̂·q̂=−1/2; spatial amplitudes use the same cosine (density) and sine (current) convention and quadratic normalization. τ is conformal time in Mpc, primes d/dτ, H here is the conformal rate, m_a²=(a m_h)². Coefficients multiply products of primordial perturbation amplitudes. The metric is shared, not fitted per species. For the underlying radiative and gauge formalism see [Pitrou](https://arxiv.org/abs/0809.3036) and [Ma & Bertschinger](https://arxiv.org/abs/astro-ph/9506072). The mode reduction, calculated histories and comparisons here are ours.

## Finite-opacity evolution on both backgrounds

Let s=A p̂p̂ᵀ+B I be the incoming log spatial metric, A=−2D+6η, B=−2η, A'=2t, B'=−2(t+D')/3; D is the incoming CDM density and t its conformal shear amplitude. For n the photon direction, ξ=n·q̂, w=n·p̂. The scalar crossed geodesic source from an incoming intensity I(ξ) is
```
S[I]=(ik/2)(A μ w+Bξ)I−2(A'w²+B')I−[(μ−wξ)/2](ikB−A'w)∂ξI .
```
For the linear polarization Q the projected source is cos(2χ) S[Q] plus Q ξ(p̂·f)(f·L_K e)(ikB−A'w)/sqrt(1−ξ²), with e=(q̂−nξ)/sqrt(1−ξ²), f=n×q̂/sqrt(1−ξ²), L_K the difference of the two transverse polarization projectors about K. This extra term is the rotation of the incoming polarization analyzer as n changes; treating Q as intensity would miss it. Azimuthal averaging is done after crossing. screen_check.py transports a full screen tensor on independently displaced rays. photon_source.py constructs geometry and collision maps on incoming multipoles, not interpolants of the old sparse quadratic samples.

Use the prior exact rest-frame bolometric Thomson tensor to generate per-opacity collision moments, including electron density. To perturb the number of free electrons during local He++/He+ Saha exchange, f=nHe/nH, x=(x_e−1−f)/f, r=f x(1−x)/x_e. Varying charge conservation together with the Saha ratio gives δx_e/x_e=[r/(1+r)] [(3/2+χ/(k_B T)) δγ/4−δ_b], with χ the He+ ionization energy. The total opacity perturbation uses δ_b+δx_e/x_e. Only applied to this early interval with a blackbody temperature monopole and the native recombination plateaux. Not a nonlinear recombination prescription down to last scattering.

β₂ is log Eulerian baryon number; P_b is the covariant normal momentum coefficient in baryon-background units. Set l=(A μ+B)/4, v_e2=P_b−(β₁/2+l)v_b, j=4v_b/3−qγ. In addition to photon propagation, the baryons evolve as
```
β₂'=C₂'−kP_b+k v_b(β₁−5η/2),
P_b'=−H P_b+D'v_b/2−kv_b²/4
      −κ(ργ/ρb)[4v_e2/3−F₁₂ + (δ_e j+4δγ v_b/3−πγ(μ−1/3)v_b)/2 + l j].
```
The second formula comes from the electron rest-frame dipole and its covector transformation, independently of integrating the collision sky. F₁₂ is the generated orthonormal photon dipole. The photon monopole gains −κ μ v_b j from collision. Keep polarization gain, gravitational redshift, perturbed streaming and deflection. The optional thermal-gas check adds only the linearized k c_b² β₂ term. All runs keep the incoming native gas sound speed. Recoil, rest-frame heating and spectral distortions are not part of this cold bolometric branch.

Split the preceding tightly-coupled covariant momentum at x=kτ=10, independently at 20: P_b=P_combined−[4ργ/(3ρb+4ργ)]β₁v_b/6. Initialize F₀₂=4β₂/3+8β₁²/9−2μv_b²/3, F₁₂=4v_e2/3+8β₁v_b/9, F₂₂=(2/3)(3/4−μ)v_b² and generated polarization initially zero. This is a leading tight-coupling switch, not an exact finite-opacity initial condition. The two switch histories test its sensitivity. All five systems (CDM and scalar, photons, baryons, both neutrino populations) source the metric at every implicit Radau stage. The omitted subdominant rolling-scalar quadratic source is not reconstructed. Numerical solver details and options: evolution.py and the named run JSONs.

## Exact stress transfer on this triangle

Use W=a/ρ_match (the saved normalization). Write the retained canonical scalar as f₀,f₁,f₂. Define E₂=f₀'f₂'+m_a²f₀f₂+[f₁'²+(m_a²−μk²)f₁²]/2, L₂=f₀'f₂'−m_a²f₀f₂+[f₁'²−(m_a²−μk²)f₁²]/2, G=W k² f₁². Then
```
Y=W E₂,  Q=W k(f₀'f₂+f₁'f₁/2),  Q₁=W k f₀'f₁,
P=W L₂−μG/3,  S=W L₂−G/4,
Y'=−3H P−kQ+W(C₂'f₀'²+2D'f₀'f₁')−(5/2)kη Q₁,
Q'+H Q=k S + D'Q₁/2 .
```
P is the isotropic pressure and S the longitudinal stress; confusing them gives a different impulse. Derivation: differentiate the field products, insert the homogeneous and perturbed KG equations including f₂''+2H f₂'+(m_a²+k²)f₂=C₂'f₀'+D'f₁'−(5/2)k²η f₁, then collect the k²f₁² terms using μ=−1/2. The CDM number control is δc₂'=C₂'+D D'. junction_balance.py first integrates the individual unaveraged source terms, then applies the two endpoint projections; it does not silently commute averaging with time derivatives. Pressure, transport and geometric work are retained separately.

## Closing the oscillation-averaged stress

The KG equation gives 4L=(f²)''+(2H−C')(f²)'−Δγ(f²), with Δγ the spatial metric Laplacian. In the coherent low-gradient expansion the slow part of f² is E/m_a² at leading order. Write d₀,d₁,q₁ for projected homogeneous and first-order heavy energy and first-order momentum in W units. Then G≈(q₁²+k²d₁²/(4m_a²))/d₀: kinetic and gradient pieces of the same carrier, not an empirical sound-speed fit. Because 1/(W m_a²) scales as a⁻³, the slow Lagrangian ℒ=W⟨L₂⟩ has leading spatial term k²(Y+5ηd₁/2)/(4m_a²) and temporal term
```
[Y''−4H Y'+(3H²−3H')Y−D'(d₁'−3H d₁)−C₂'(d₀'−3H d₀)]/(4m_a²).
```
Use the energy and momentum equations to eliminate Y'', not a numerical second derivative of the unknown solution. Setting U=Y'+3HP+kQ and V=⟨D'Q₁⟩/2 introduces a −k²S term on the right, hence a 4m_a²+k² denominator before gravity feedback. Terms from differentiating H P and its contribution to −4H Y' are higher order and omitted here. P=ℒ−μG/3, S=ℒ−G/4. This is an asymptotic truncation tested on windows, not an exact identity for arbitrary states.

For the active metric replay, carry δc₂ and K=⟨C₂'⟩ as evolving variables:
```
δc₂'=K+⟨D D'⟩ ,
K'=−H K + (ρc δc₂)/2 + (Y+3P)/(2W) + F_ext .
```
ρc here includes the native 8πG a² prefactor. F_ext includes the measured-on-the-reference-history baryon and radiation active trace and the incoming squared metric terms. Its coefficients are not fitted. U=B₀K+⟨2W D'f₀'f₁'−(5/2)kη Q₁⟩ + cov, B₀=⟨W f₀'²⟩. K' includes P; its contribution to U' is solved algebraically with ℒ (see coupled_transport.py). The external second-order radiative/baryon histories remain prescribed in this reduced replay, while the original field reference evolves them. Restoring their joint dynamics after the match is a distinct test.

The leading fast-work correlation can also be calculated. Put f₀=A cosθ, f₁=A(u cosθ+v sinθ), f₂=A(U_c cosθ+V_c sinθ), θ'≈m_a. To leading order d₀=WA²m_a²/2, d₁=2d₀u, q₁=−kd₀v/m_a, Q=−kd₀V_c/m_a. The sin(2θ) coefficient in W L₂ is −2d₀(V_c+uv). Integrate its 3/(2W) contribution to the fast K', then contract with Wf₀'²=d₀(1−cos2θ). The resulting correction to the density work is
```
cov(C₂', W f₀'²) ≈ 3(d₀ Q + d₁ q₁/2)/(4W k).
```
Use evolving Q when advancing the state. Measured quadratic histories are used only to score this term and the transported variables, not to choose its sign or amplitude. The residual of the total transport includes other averaging and discretization errors; adding a correct work term need not improve every endpoint residual.

matching_restart.py extracts both the exact instantaneous state and the separately phase-filtered state from the complete reference, including angular distributions and massive shells. The filtered core entries for f₂,f₂' are not a substitute for projected stress/energy. The coefficients are still in CDM-synchronous coordinates. Using them at z=99 requires a consistent continued hierarchy and a second-order slicing/spatial-coordinate transformation.

