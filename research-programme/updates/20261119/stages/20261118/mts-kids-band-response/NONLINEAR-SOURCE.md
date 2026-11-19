# The first nonlinear heavy source in the Newtonian limit

Start with the existing positive quadratic heavy normal mode, not a lensing fit. Local sources: ../MTS-HEAVY-BATH-COUNTERFLOW-AND-GALACTIC-STRESS.md and ../condensate-origin-20261003/motion-bath-matching-20261006/49-real-motion-envelope-and-existing-bath-matching.md. The nonrelativistic wave limit and coherent scalar stress are standard physics, not new MTS postulates; see [Namjoo, Guth & Kaiser](https://arxiv.org/abs/1712.00445) and [Hui et al.](https://arxiv.org/abs/1610.08297). What is fixed here is the coefficient and its role for the retained MTS pole, and a controlled comparison against the cold response.

Use comoving coordinates, cosmic time, comoving amplitudes with the background dilution removed, and λ=ℏ/m (or 1/m in c=1 Mpc units). In a common weak metric every occupied component obeys iλ ψ̇=−λ²∇²ψ/(2a²)+Φψ. Absorb constant nonnegative occupation weights into the components. Poisson's equation uses total gravitating density, not a new wave-only G. For n=Σ|ψ|² and J_i=λ Im Σψ*∂_iψ, differentiate the wave equation and its conjugate:

    ṅ = −∂_i J_i/a²
    J̇_i = −n ∂_i Φ − ∂_j T_ij/a²
    T_ij = λ²[Re Σ(∂_iψ)*∂_jψ − ¼∂_i∂_j n].

No division by density is required in this conservative form. For n>0 split T=JJ/n+P+S with P_ij=λ²[(∂_in)(∂_jn)/n−∂_i∂_jn]/4. The remainder S is λ² times the real Gram matrix of component gradients after projecting out their component-space direction along ψ. It is positive semidefinite (not its divergence), unchanged by constant unitary mixing of the ensemble representation, and zero for one coherent scalar amplitude. A genuine mixed state can have S≠0 even at uniform total density and vanishing net current. Collisionless cold matter can likewise acquire a velocity-dispersion tensor after shell crossing; the dust control is a single-stream control.

With δ=n/n̄−1, n̄ constant in this comoving convention, obtain

    δ̈+2Hδ̇ = ∂_i[(1+δ)∂_iΦ]/a² + ∂_i∂_j T_ij/(n̄ a⁴).

For the coherent pressure contribution alone, expand through second density order:

    −λ²∇⁴δ/(4a⁴) + λ²∂_i∂_j[(∂_iδ)(∂_jδ)]/(4a⁴) + O(δ³).

The coefficient of δ_p δ_q in the quadratic density source is λ²[(p+q)·p][(p+q)·q]/(4a⁴) under a full ordered convolution. It vanishes for a constant input or a zero output wavevector, as total mass conservation requires. This is the conservative density-acceleration kernel, **not** an Euler velocity vertex, the complete second-order growth kernel, or an instantaneous correction to a measured power spectrum. Advection and gravity also contribute. The conventional Hubble drag follows from differentiating a⁻² rather than assigning a phenomenological H term.

An independent 50-digit test starts from the Hamiltonian itself: for a real initial wave with zero current, n̈=2[(Hψ)²−ψ H²ψ]/λ² at fixed instantaneous scale. After subtracting the common dust gravitational acceleration, the standing-mode second harmonic has a useful extra cancellation. In sin²x/(1+ε cos x), the term ε² sin²x cos²x has **no** cos 2x component; the ε⁴ sin²x cos⁴x term has coefficient +1/32 against the leading −1/2. The first relative correction to the quadratic force prediction is therefore −ε⁴/16, not order ε². The generic crossed-mode test does retain order-ε² relative corrections. Both tests keep the original 2e-5 precision target.

**Exact finite-amplitude prediction for this preparation.** Write s=√(1−ε²), r=−ε/(1+s), with |ε|<1 so density is positive. For u=kx the one-dimensional pressure stress divided by its constant λ² n̄ k²/4 is particularly simple:

    ε cos u + ε² sin²u/(1+ε cos u) = 1 − (1−ε²)/(1+ε cos u).

The Fourier series of (1+ε cos u)⁻¹ is [1+2Σ_{j≥1}rʲ cos(ju)]/s. Taking the two spatial derivatives gives the instantaneous **wave contribution** to δ̈ at every harmonic j≥1:

    A_j = [λ²k⁴/(2a⁴)] j² s rʲ .

No mean mode. The exact second harmonic divided by its leading quadratic prediction is 4s/(1+s)². This resums a single specified wave; it is not a cosmological nonlinear power spectrum. finite_contrast.py compares the first six harmonics at four contrasts with independent direct wave Hamiltonian evolution derivatives, including common gravitational loading, without using the stress expression to produce the reference values. Do not extrapolate the density-divided form through zeros or average this single-mode formula over unrelated waves.

**Dimensional and physical probe.** Prepare one small coherent standing density mode δ=ε cos(kx), zero initial velocity, with baryons, cold dark matter and the heavy background mass given the same contrast; leave the other species unperturbed. The Newtonian quadratic acceleration into cos(2kx) is +4πGρ_cluster ε²; the leading heavy pressure term is +λ² ε² k⁴/(2a⁴). The linear heavy term has the *opposite* sign, −λ² ε k⁴/(4a⁴). Ratio of quadratic terms = 2(k/k_J)^4 with k_J⁴=16πGρ_cluster a⁴/λ². No parameter is fitted. The specified preparation is for a transfer-function-independent comparison, not the actual primordial realization. Use the saved density units 8πGa⁴ρ and m_h=149896.229/Mpc. This Jeans balance is instantaneous; it is **not** the half-power scale of a mode that evolved through radiation domination.

**Why a density-only extrapolation would fail.** As an explicit example take two equal incoherent amplitudes with phases ±A sin(x)/λ and unit total density, versus a constant pure wave. Both have n=1 and J=0. Only the pair has T_xx=A² cos²x. Initially both can have Φ=0, yet the pair has δ̈=−2A² cos(2x)/a⁴ and the constant wave does not. A cosmic average heavy fraction cannot select between them. Conversely, a fully specified coherent initial wave evolved by the field equation does not need a freely fitted dispersion. A useful next calculation is to evolve the derived forced second-order response from the *retained* linear density and velocity histories, checking the same gravitational and advective terms in the pressureless limit. For a mixed preparation propagate the extra state moments, not a guessed galaxy normalization.
