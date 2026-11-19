# Longitudinal material response on the retained charged background

**Scope.** Use the previous order-reduced total-stress Hamiltonian H=e+γ₁Z₁+γ₂Z₂ and spherical Einstein equations in 4πG=c=1 units. The material number and radial electric displacement are conserved variables; the massive scalar is a separate field, not an invented gas pressure. We derive a local response at the symmetry centre rather than putting a uniform self-gravitating, net-charged universe in equilibrium. The initial launches are time symmetric. Signs below use positive ω² for restoring acceleration. Frozen-source matrix eigenvalues are not global normal-mode frequencies of a time-dependent body.

## Two-variable response with the constraints included

On the initial slice R=r, J=ar², proper material density n=b/a, scalar gradient s=h_r/a, displacement D=Q/r², w=Π=0. The actual constraints are Q'=ηr²b and m'=r²H, a=(1−2m/r)^−1/2. Thus at the regular centre, writing subscripts 0,2 for the coefficients of 1,r²,

    a₂=H₀/3,   n₂=b₂−n₀H₀/3,   D₁=ηn₀/3,   s₁=2h₂.

This uses the constrained mass, not an independently assigned Newton potential. Time symmetry sets the initial material and scalar velocities to zero but does not set their accelerations to zero. From the canonical equations the radial per-particle force is F_d=−∂r H_n/a+η H_D and the scalar momentum force is F_s=∂r(r² H_s)/J−H_h. At the centre define

    L = H_nn n₂ + H_nh h₂ + 2 H_nss h₂² + H_nDD D₁²/2,
    F = 6 H_ss h₂−H_h,      S=H₀+3(n₀H_n−H₀).
    (ln n)̈ = S + 6 H_ww L/n₀ − 3 H_ww η H_DD D₁/n₀
                   − 6 H_wΠs h₂ F/n₀,
    ḧ = H_ΠΠ F.

Dots denote central proper time. S is the gravitational focusing from Einstein's two spatial equations; the second term is the chemical-potential gradient, the third Gauss's electric force, the fourth the scalar contribution to acceleration of the number current. In particular n and h cannot be evolved by just inserting a sound speed into a one-component Jeans equation. The derivation uses the divergence of the **number current**, not the canonical impulse as velocity. All derivatives of H here are evaluated at n₀,h₀,D=s=w=Π=0 except that n₀,h₀ need not vanish.

For a material seed use δb=n₀[W j₀(kr)+W'j₁(kr)/k] and δQ=η n₀r² W j₁(kr)/k. W=1 through r=1.5 and zero beyond 3. At k=0 take j₁(kr)/k=r/3. The seed conserves total charge and number, not necessarily ADM mass. Its central coefficients are δb₀=n₀ and δb₂=−n₀k²/6. The independently selectable scalar seed has δh=√n₀ W j₀(kr). Use coordinates Y=(δln n, δh/√n₀), with the seed amplitude understood. Minus the derivative of the two accelerations gives Ω²(k)=A₀+k²A₂. The off-diagonal entries are calculated, not zeroed. The smallest eigenvalue is the instantaneous slow branch. Finite radial seeds and evolved fields are not assumed to remain eigenvectors.

**Independent direct computation.** The real ± initial profiles solve both nonlinear radial constraints before taking their difference. The earlier 10-component Einstein–matter right-hand side supplies rates and second proper-time derivatives. A second centre evaluation uses the regular identity lim[r⁻²∂r(r²U)]=3U'(0) for an odd flux U; a Cartesian differencing error divided by tiny r² had amplified the original null residuals. Waveform comparisons evolve the full fields rather than exponentiating A₀+k²A₂. The exact tests and the limits of freezing this matrix are listed in RESULTS.md.

## The same term in Newtonian and material variables

For ordinary matter at rest and no scalar, put g=γ₁+γ₂. The rest energy is n−gn²/4, the pressure −gn²/4, H_ww=n+gn²/2, H_nn=−g/2, H_DD=1−γ₁n/2, and H_nDD=−γ₁/2. Substitution gives, to first order in the contacts,

    (ln n)̈ = (1−η²)n −3g b₂ − η² n²(γ₁/6+γ₂/2).
    ω²_d = −(1−η²)n − g n k²/2 + η² n²(γ₁/3+γ₂).

These are distinct statements: the second differentiates the first along the compensated material seed. The cancellation of the curvature contribution in n₂ against the change in gravitational focusing is needed to obtain the intercept. At zero contact ordinary gravity gives −n and the plasma term gives +η²n.

**Matching, not adding forces.** Write ε=(m_h/M_R)². Checkpoints 4878 and 4964 give d₀=12a_R ε k², d₂=−4a_C ε k², γ₁=16a_C ε, γ₂=8(a_R−2a_C/3)ε. Therefore

    g k²/2 = (d₀−4d₂)/3 = δΦ/Φ_Newton,       γ₁/3+γ₂=8a_R ε.

The material gradient contribution is precisely the correction to the quasi-static Newtonian gravitational transfer in the untransformed variables. Including both would double count. The charged zero-wavenumber intercept singles out the scalar-curvature coefficient at this order. This reconciles a seemingly wrong-sign material gradient with the perturbative GR/Newton branch using the same normalization as the earlier parent action.

The inherited one-percent criterion applies **at the actual momentum**: |d₀|,|d₂|≤0.01. It implies |gk²/2|≤1/60, independent of the representative example pole. This bound controls the two retained operators, not missing higher operators or every possible material. At η=.8 the minimal attraction is 0.36 times the Newton contribution; the gradient cannot reverse it in this corridor. At η=1 the leading attraction vanishes and this argument no longer excludes a change of sign. To include the massive scalar at first order, its minimal matrix has diagonal entries −J,1+k², J=(1−η²)n, upper element B=2h₀√n, lower element zero. For each coefficient the correction to the slow eigenvalue is δΩ₁₁−B δΩ₂₁/(1+k²+J), not just δΩ₁₁. mixed-corridor.json evaluates and bounds the residual terms for the retained massive launch.

## An all-time first variation for ordinary matter

Here h=0; it remains exactly zero. In the covariant radial material rest frame let ν be proper rest number, E the radial electric field. For radial motion the time–radial electromagnetic stress is −(E²/2)g_ab. Before the Legendre transformation the new radial Lagrangian per proper volume is

    −ν+E²/2 + [g ν² + γ₁νE² + γ₁E⁴]/4.

The particle enthalpy is μ=1−gν/2−γ₁E²/4, and the electric displacement ℰ=(1+γ₁ν/2)E+γ₁E³. The material circulation equation is μa=ηE−Dμ in the radial rest direction, with D the material spatial derivative. Gauss gives div ℰ=ην. At the centre E=a=0, but their divergences are not zero. Local symmetry gives div(D E²)=2η²ν²/3 at leading order. Substituting into the material Raychaudhuri equation (shear and vorticity zero at the centre) gives the central proper-density law, with ℓ=ln ν,

    ℓ̈−ℓ̇²/3 = (1−η²)ν − g(D²ν/2+ν²) − η²ν²(γ₁/6+γ₂/2) + O(γ²).

D²ν is in the **material rest slice**, not the fixed synchronous observer slice. Induced changes of ℓ in the first term on the right and the expansion term on the left must also be propagated. At a time-symmetric launch this reduces to the previous constrained result. For η=1 the ordinary static charged family has Q=N, m=Q−Q²/(2r), a⁻¹=1−Q/r. The static lapse satisfies (ln α)'=aQ/r², exactly balancing the electric force. This holds for every compensated seed, not just a uniform ball. Thus the first variation of ℓ̈ from the explicit contacts is constant along the unperturbed central worldline, and the change in central density is **quadratic in proper time** at first order, for as long as the smooth expansion applies. This conclusion is not a harmonic fit.

For η≠1 the curvature of the profile changes. To compute its source without a new fluid prescription, use rest-mass shells of the *minimal* charged dust. Write N_x=νr² e^Λ, Q=ηN, M=m+Q²/(2r), Γ=D_l r=M_N−ηQ/r, U=D_τr. Einstein and Gauss give D_τ M=0 and

    U²=Γ²−1+2M/r−Q²/r²,    D_τ U=(−M+ηQΓ)/r²+Q²/r³,
    ∂x ln(lapse)=e^Λ ηQ/r².

Use the initial areal radius x as shell label and central proper time. Write r=A x+B x³, U=Vx+Wx³, N₃=n/3,N₅=b₂/5,Q_j=ηN_j, M₅=N₅+(η²−1)nN₃/5. Then

    Γ₂=(η²−1)N₃−ηQ₃/A,   φ₂=ηQ₃/(2A),    F₁=(η²−1)N₃/A²,
    A'=V, B'=W+φ₂V, V'=F₁,
    W'= (−M₅+ηQ₅+ηQ₃Γ₂)/A²−2BF₁/A+Q₃²/A³+φ₂F₁.
    ν₀=n/A³,   D²ν₀=6[b₂+n(Γ₂−5B/A)]/A⁵.

Launch at (A,B,V,W)=(1,0,0,0). For each contact evolve y=∂γ ln ν, y(0)=y'(0)=0:

    y''=−2(V/A)y'+(1−η²)ν₀ y − D²ν₀/2 − ν₀² − η²ν₀² c,
    c=1/6 (tensor) or 1/2 (trace).

Differentiate this solution along the same compensated seed to obtain a predicted waveform. No radial grid or empirical sound speed enters this reduction. It describes the centre, the ordinary subfamily and first-order contacts, before caustics; the massive scalar requires its own time-dependent sources. Mathematical extrapolations are distinguished from intervals independently tested in two coordinates.

## Which part is new gravity?

At fixed initial central number, changing the seed wavenumber changes its central curvature by −n k²/6, not its central value. A and V do not depend on this curvature, and the equations for B and W are linear with affine forcing in b₂. Only the term −D²ν/2 carries that dependence into either contact equation. Hence both differentiated contact responses have precisely the same slope in k²; their intercepts need not agree. The propagated correction is an intercept plus a known function of time multiplying (γ₁+γ₂)k². The latter is already fixed by the parent gravity insertions: (γ₁+γ₂)k²/2=(d₀−4d₂)/3. Counting the two as separate forces would double-count the same correction. The two 1% insertion bounds give 1/60 of the Newtonian term at the wavenumber being tested. This is a first-order, scale-dependent statement, not a claim about arbitrarily short wavelengths outside the retained expansion.

## A scalar pulse with no central shift at launch

In the minimal massive branch the exact central proper-time equations are ℓ̈=ℓ̇²/3+(1−η²)ν+2ḣ²−h² and ḧ=ℓ̇ ḣ−h+D²_rest h. In the synchronous evolution the material spatial Laplacian at the centre is 6h₂/a_c²+3(w₁/a_c)ḣ, with w₁ the central radial slope of the physical material velocity at this order. The second term matters when using spatial data to reconstruct the two histories. A reconstruction using h and ḣ from the full run is an identity check, not a forecast. For the initial-data-only forecast the ordinary charged geometry evolves independently; the scalar propagates on it, and its stress drives the central material density. The ignored effect is the scalar's change of its own propagation geometry.

The held packet W[j₀(9r)−j₀(15r)] has δh=δḣ=δℓ=δℓ̇=0 at the centre initially, but δḧ=144√n per unit seed. Thus the first nonzero material term is quartic, not quadratic (see EARLY-PACKET.md). The pulse combines two wavenumbers not used in the single-mode comparisons. This tests linear seed response on the same prepared family; it does not sample a different physical environment.

