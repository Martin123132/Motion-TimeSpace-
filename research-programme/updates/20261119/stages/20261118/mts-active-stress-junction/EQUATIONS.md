# Active matching, continuation and the relative Newtonian state

Use the mode, input phases, field normalization, native 8πG a² densities and CDM-synchronous geometry of ../mts-polarized-counterflow-20261118/EQUATIONS.md. Equal magnitudes |p|=|q|=|K|=k=1.98095677855/Mpc, K=p+q, μ=p̂·q̂=−1/2, b=K̂·q̂=1/2. Incoming first-order amplitudes multiply cosines for densities and sines for longitudinal momenta. At K the crossed product of two cosine sums has coefficient 1, of gradient sine sums has coefficient −μ, and of a cosine times a longitudinal sine has coefficient b. No factorial is applied to the generated coefficient.

## Joint evolution

Variables are (C₂, K_e=C₂', Y, Q, β₂, P_b, F₀…F₁₂, G₀…G₁₂, η₂) plus massless and 36 massive momentum shells with 144 angular nodes. Y and Q are the heavy normal energy and **covariant** normal momentum in W=a/ρ_match units. β₂ is log Eulerian baryon number. The previous real-field reference and new averaged calculations have the same initial waves and same Thomson/streaming laws. Only the scalar (about K) of this particular triangle is evolved. Prior gravity and gas assumptions are kept. No separate gauge or coupling is chosen for photons.

The pressure, longitudinal stress, carrier work and direct field identities are derived in the preceding checkpoint. Here the generated external active trace is not input:
```
K_e' = −H K_e + ρc(C₂+D²/2)/2 + (Y+3P)/(2W)
       + D'²/3+(μ²−1/3)t² + ρb(β₂+β₁²/2−3μv_b²/2)/2 + ργ F₀₂ + Aν,
t₂ = −K_e + 3[Q/W+ρb P_b + ργ(F₁₂+l qγ) + Jν + Ggeom]/(2k),
3η₂' = K_e+t₂ .
```
D,η,t are incoming CDM density, scalar metric curvature and scalar shear, l=(Aμ+B)/4, A=−2D+6η, B=−2η. Both Aν (half the active energy plus spatial trace) and Jν (longitudinal covariant momentum) follow from the evolving thermal angular distributions. The same t₂ and K_e perturb the photon and neutrino skies at each integration stage. The photon return force simultaneously drives the gas. If Eν were added to K_e' *after* solving for pressure it would miss its occurrence in the derivative of the density work in the virial law. We instead solve the two-stage Gauss collocation equations with Aν and t₂ as simultaneous auxiliary unknowns at both stages. model.py builds the linear-affine rows; propagate.py eliminates free streaming at fixed thermal momentum before solving this small system. The held-out microscopic solver uses the independent three-stage Radau propagation and retains both scalar oscillator components.

Slow modes at two initial placements are independently projected from the x=120 angular restart. The reference replay reaches x=160 bit-identically before the new propagation. Incoming metric and optical histories remain prescribed *first order* waves, not evolving the first-order universe anew. No later **second-order** radiation state, trace or metric is a forcing input to the reduced solver.

## Crossing the native match without extrapolating the oscillating field

For a≥a_match on the retained branch the native background sets ρ_h proportional to a⁻³. Obtain d₁, q₁ and p₁ from the previously sealed matched linear table and native equations. Their pressure is p₁ = [r/(sqrt(1+r)+1)²](d₁+3H q₁/k), r=k²/(a m_h)². It is not a new fitted coefficient. Use B₀=1, d₀=1, and the leading transport work D'(d₁+p₁)−5kηq₁/2. The half-product ⟨D' Q₁⟩/2 needs one additional term if a rapidly oscillating metric acts on the same coherent current:
```
⟨D' Q₁⟩/2 ≈ D' q₁/2 + 3(q₁²+k²d₁²/(4m_a²))/(8 W k).
```
Indeed for f₀=A₀ cosθ and f₁=A₀(u cosθ+v sinθ), the fast scalar pressure drives D'_fast ≈ 3d₀(v cos2θ−u sin2θ)/(2W m_a) while Q₁_fast ≈ k d₀(v cos2θ−u sin2θ)/m_a. Their covariance gives the stated term. The leading self-correlation of D'_fast with first-order scalar pressure vanishes in quadrature. Higher-order carrier terms are approximations. The fast C₂' × kinetic-energy correction in the preceding equations is also retained and uses evolving Q. Native matched and exact background clocks are aligned at the *same* a_match, and all later comparisons use scale factor, not a phase-adjusted time. The He+ electron fraction differs from its plateau by less than 1.2e−8 in the new banks; this is not a hydrogen-recombination model. The inline photon hierarchy is continued from its existing first-order state.

## Bound on the rolling (slow) scalar

The retained native action has a quadratic rolling field as well as the heavy field. Its second-order response obeys exactly the same canonical KG forcing with its own background and first wave:
```
s₂''+2H s₂'+ω_s²s₂ = C₂' s₀' + D's₁' −(5/2)k²ηs₁,  ω_s²=k²+(a m_s)² .
```
For the retained regular radiation-era adiabatic state s₀'∝τ³, D∝k²τ²/4, C₂∝−3k²τ²/16. Consequently s₁ and s₂ start as τ⁶ with s₂/s₁→−3/4 and the same derivative ratio; no independent slow entropy mode is assumed. Start at x≈0.092 and repeat at x≈0.200. For R²=s₂'²+ω_s²s₂², R' ≤ |source| + (ω_s'/ω_s)R for monotonically increasing ω_s and positive H. This bounds R by (ω_max/ω_min)(R_initial+∫|source|dτ). slow.py upper-bounds the integral of the interpolated source by absolute cubic Bernstein coefficients on every cell. The active trace uses 2s₀'s₂'−(am_s)²s₀s₂+s₁'²−(am_s)²s₁²/2. This gives a conditional bound on the missing *direct* forcing in the saved pre-match history, not a bound on late-time dark energy, arbitrary slow initial data or full metric error.

## Converting the physically useful relative pair

The general second-order gauge transformation law is established physics ([Bruni et al.](https://arxiv.org/abs/gr-qc/9609040)); first-order synchronous/longitudinal conventions can be compared with [Ma & Bertschinger](https://arxiv.org/abs/astro-ph/9506072). Below is the application to this retained branch and mode convention. In the pullback from Newtonian coordinates to synchronous coordinates take τ_S=τ_N+T and x_S=x_N+∇L to first order. The spatial no-shear condition gives L=A/(2k²) and the vanishing shift gives T=L'=t/k². Thus δc₁,N=D−3HT, Φ=η−HT, Ψ=HT+T'. CDM and heavy homogeneous pressures vanish **on the averaged branch**, and their homogeneous density ratio is constant. The second-order coordinate generator therefore cancels from their relative density and current; this does not hold for the separate total density or the unaveraged field with nonzero oscillating background pressure.

Use δ=d₁−D, Δ_S=Y−(C₂+D²/2). The scalar log ratio of the two energies measured by the CDM observer has synchronous second-order coefficient Y−C₂−d₁²/2. Pulling it onto the Newtonian coordinates adds T(−kq₁−3Hp₁)−μk²Lδ. Changing to the Newtonian normal changes this ratio by −2μ kT q₁ (the common squared observer speed cancels). Finally convert log ratio back to a density-contrast difference by adding [(d₁−3HT)²−(D−3HT)²]/2. The q₁ terms proportional to (1+2μ) vanish for this triangle:
```
Δ_N = Δ_S − (3HT+μk²L)δ − 3HT p₁ .
```
This mixes coordinate slicing/threading and observer choice; a change in the value is not new gravity. gauge_pair.py checks via a finite coordinate pullback of both density fields and actual observer boosts, Fourier extracting the sum mode. Independent artificial second-order coordinate shifts cancel as required.

For momentum, Q is the **synchronous covariant** heavy current minus CDM (zero in that frame). Converting to the orthonormal synchronous triad subtracts l q₁. Displacement of the incoming flux contributes b[T(q₁'−3Hq₁)−μ k²L q₁]; the temporal −3H term is the physical background density in the transported current. Boosting into the Newtonian normal adds b kT(δ+p₁) to the relative current. In the Newtonian frame divide by the local enthalpy for each energy-frame velocity (linear intrinsic anisotropic stress vanishes). These give
```
Δj_N = Q + b{T(q₁'−3Hq₁)+kT(δ+p₁)+(η−2μk²L)q₁},
Δv_N = Q + b{Tq₁'+(η−2μk²L−d₁−p₁)q₁},   q₁'=−Hq₁+kp₁ .
```
For the native growing-mode convention the corresponding scaled velocity is −kΔv_N/H. gauge_current.py instead pulls back the fields on an independent angular grid, converts the spatial covector with the inverse metric triad, boosts both stress tensors using 4×4 Lorentz matrices, and recovers the velocities from their local energy and spatial stress (correct through the tested order). The cold null compares CDM with itself, not a logarithm of zero heavy density. These are relative variables, not all the individual Newtonian seeds. In particular Δv_N is not interchangeable with Q or Δj_N, and the released z=8 response row is normalized at z=99, not at z=3999.

