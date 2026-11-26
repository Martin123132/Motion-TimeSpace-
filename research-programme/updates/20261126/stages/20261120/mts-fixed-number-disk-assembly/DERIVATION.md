# Disk assembly on the retained weak-field equations

## What is prepared, and what is held fixed

Take one of the three original, census-supported Galactic ordinary potentials V_f. On every saved sphere let V_0 be its angular mean and D=V_f−V_0. Let V_s=V_0+sD. This keeps the radial ordinary potential monopole fixed (in Newtonian Poisson theory, the monopole mass profile is unchanged); it assembles angular structure, not all the mass of a galaxy. Each preparation starts in the real stationary coherent wave of V_0 with the same norm N as the retained final ground g. No tilt, external coupling, change in N, or speed renormalization. This pure-wave control is separate from the earlier mixed-state population test. Do not assume that it describes real Galactic initial data.

Use the saved mass-weighted finite-element variables, even vertical parity, m=0, and their isolated Newtonian Green operator G. Let ρ be the projected quadratic wave density and take positive sign for its Green quadratic form. The equations are iψ̇=(T+V_s+Φ[ρ])ψ; E_s=⟨T+V_s⟩−||ρ||²_G/2. Dimensionless time is physical time divided by L/v. All three preparations give L/v=81.951 Myr. The Hamiltonian has no new parameter; the protocol parameter s describes ordinary matter, not a force coupling.

For the slow benchmark follow stationary solutions, normalized separately at each s. Stationarity gives dE_eq/ds=⟨D⟩; the five-knot integral checks it. This is a branch continuation, not proof of tracking at a particular disk age. In a sudden switch the wave and its number do not jump. In the original stationary phase frame, d=(H_f[ψ_0]−μ_0)ψ_0, ψ̇(0)=−id, ρ̇(0)=0, and ψ̈(0)=−(H_f[ψ_0]−μ_0)d. Consequently ρ̈(0)=2(|d|²−ψ_0(H_f[ψ_0]−μ_0)d) before projection. The independent force double commutator checks the sign. Advancing the nonlinear equation uses a Cayley midpoint with the self-field evaluated on the mean of endpoint densities (not density of the mean wave). Reversibility, norm, instantaneous energy and supplied work are checked separately. For a finite ramp the ordinary midpoint field uses the mean endpoint coefficients: its work is Δs times the mean endpoint ⟨D⟩.

## Nonlinear bound: not extrapolation from seven output times

Let H=T+V_f+Φ[ρ_g]−μ_f, r=Hg, and e=E_f(ψ)−E_f(g). After a global phase choice write ψ=ag+x with g†x=0, a=√(1−l), ||x||²=Nl. Here l is squared overlap loss, not lost particles. Exactly,
    
    e = x†Hx − ½ ||ρ(ψ)−ρ_g||²_G + (a²−1)g†r + 2a Re(x†r).

On l≤S the last two terms are bounded in absolute value by ε=||r||(√N S+2√(NS)). Write the density difference as 2a J_g Re(x) + ρ(x)−lρ_g; J_g maps a wave displacement to the density product with g. Divide ρ(x) by ||x||². It is a convex average of the normalized point sources of the original quadrature, with positive weights proportional to |x|². Jensen's inequality in the positive Green norm therefore gives

    ||ρ(x)−lρ_g||²_G ≤ Nl ⟨x,Bx⟩,
    B_i = ||ρ_i−ρ_g/N||²_G.

This B is calculated, not parametrized: the point's harmonic components at a radial node are Y_j/(√w r_node); use the diagonal of the inverse radial Poisson block for each j, then subtract twice its Green product with ρ_g/N. For any η>0, the weighted square inequality now yields on the entire ball

    e ≥ x†Qx − ε,
    Q = H − 2(1+η) J_g† G J_g − (1+1/η) NS B/2 .

The real-part term was conservatively extended to the entire complex x. This argument uses the exact nonlinear density difference, not just a quadratic expansion of the action. No small-perturbation remainder is dropped.

To certify that a solution of energy at most E cannot leave this ball, test Q−(E+ε)/(NS) on the tangent g-perpendicular space with a strict positive margin. On the boundary l=S the energy would have to exceed E. For any signed observable A, set A′=A−⟨g,Ag⟩I/N and h=A′g. For t>0, check Q+tA′ positive on the tangent and h†(Q+tA′)_tangent⁻¹ h ≤ C. Completing the square with the exact observable difference 2a Re(x†h)+x†A′x gives

    ⟨A⟩ψ−⟨A⟩g ≥ −(E+ε)/t − t C.

Both positivity tests use the original Poisson auxiliary variables (Schur complement) and a single border for the norm constraint. The compliance upper bound is rechecked by adding an auxiliary scalar with diagonal C and column h. Exactly one negative eigenvalue of the full bordered pencil then includes the constraint border; the restricted stiffness is positive. Local block elimination checks inertia, retaining the dense border; different chunk widths/solvers and explicit final splitting provide checks. These are floating-point tests with margins, not interval-arithmetic or continuum proofs. In the preliminary overlap-only test the most permissive foreground did not close; the signed force operator in this stronger test is essential.

## Why any monotone turn-on is covered on this mesh

Use from the start the *final* Hamiltonian to define e(t), and write d(t)=⟨D⟩ψ−⟨D⟩g. From dE_s/dt=ṡ⟨D⟩ and s(0)=0,

    e(t) = c + [1−s(t)]d(t) + ∫₀ᵗ d(τ) ds(τ),    c=e(0)−d(0).

For monotone s between 0 and 1 the last two terms are a convex average of past and present d. A sudden jump is included with continuous state. Starting below an energy cap E and inside l<S, consider the first boundary hit. The overlap boundary is excluded by its stiffness test. For the energy boundary use the signed bound above with A=−D and demand c+sup d < E. This excludes the first energy hit, with no assumption about a ramp rate or adiabaticity. A second signed bound with A the mirrored vertical wave acceleration then applies at all later times, even after the source stops. Data enter only when comparing this cap on additional inward pull with the relaxed, signed eight-component constraints. They do not set the potential or the wave energy.

If there is an additional potential U acting on the wave, the same identity gains a term W_extra=−∫Tr(U dρ_onebody), with U and ρ_onebody in the common wave Hamiltonian. Equivalently, on a fixed basis W_extra equals the initial minus final expectation of U plus ∫⟨∂t U⟩dt. It is the cumulative work on the original wave energy above the specified angular-source term, not the instantaneous depth of a potential. For a second energy cap with c+sup d below it, the first-hit argument survives until W_extra reaches E−c−sup d. If the signed force remains excluded at that cap, any trajectory starting from the specified spherical state and achieving the band must have reached at least this much cumulative extra work at some time. This is a necessary threshold, not a proposed source or sufficient energy. Keeping U static but nonzero can still exchange energy with a changing state. The reported threshold assumes common norm, parity sector, final foreground/readout and the same prepared start; it does not cover open capture or dissipative matter by assertion.
