# Finite preparation on the retained Schrödinger–Poisson branch

Use the parent's length, velocity and time units (L, v, L/v), radial fields rψ, angular average normalized to one, and the unchanged extra source bank. The saved real ground g has chemical potential ε and norm N fixed at the inherited outer calibration. In a finite-element space we relax g at **fixed N** using only the Poisson potential of the difference from the saved density, iterating the orbital equation and normalization together. The stationary chemical shift and norm of the change are saved for every mesh. This is not a refit. The pulse changes the nonaxisymmetric bar only; the static bar monopole and its axisymmetric flattening remain throughout.

### Equations actually evolved

Remove the common ground-state phase. For one positive m, the first variation of rψ is a exp(iξ)+b* exp(−iξ), ξ=mφ−ωt, ω=mΩ in scaled units. Represent the second-order axisymmetric variation by q=x+iy. H_m is the mean Hamiltonian minus ε including centrifugal energy; B_m is multiplication by g/r projected between azimuthal harmonics; L_m=−∂ᵣ²+l(l+1)/r² is the positive Poisson operator. F is the projection of gV_m, where V_m is a **complex** Fourier coefficient, not a real cosine amplitude. In the rotating variables:

    i a′ = (H_m−ω)a + B_m w + A F
   −i b′ = (H_m+ω)b + B_m w + A F
    L_m w = −B_m†(a+b)
    i q′ = H₀ q + B₀ w₀ + projection[(A V_m+w/r)* a + (A V_m+w/r) b*]
    L₀ w₀ = −2 B₀† x − projection[(|a|²+|b|²)/r].

All variations start at zero. The density entering the second-order mean Newton force is the *sum* of the intensity and 2g x/r² in physical density notation (the intensity likewise divided by r²). The phase component along i g has no density and is separated by taking the real projection; the evolving real ground overlap is **not** discarded. Different m have no cross terms in this azimuthal mean. They do have cross terms in other azimuthal sectors, so these equations do not claim all second-order instantaneous forces.

Radial Gauss–Lobatto finite elements share endpoints; the discrete derivative energy is symmetric under the same mass quadrature that defines the dynamic norm. Regular radial variables vanish at the origin. The wave is initialized at rest relative to the ground, with no injected wave and a distant homogeneous Dirichlet numerical boundary; no stationary wave is artificially cut off at a chosen radius. The exterior for gravity is vacuum with w_l′+l w_l/R=0. Domain extension is a finite-time control, not a strict finite propagation theorem for Schrödinger waves. Fourth-order symmetric composition of implicit midpoint advances the first and second variations together. The diagnostic midpoint self-gravitational source is evaluated using the simultaneous sidebands. The second-order mean force is also integrated directly from its density using independent inner/outer Newton multipoles, including the signed contributions of outer material. No artificial mass-normalization step is applied to time-dependent states.

### Why there must be a compensating deformation

At second order total norm changes by |a|²+|b|²+2⟨g,x⟩ (norms integrated over the cloud). Its derivative vanishes for a closed finite domain; on an open subvolume there is boundary current. The angular momentum divided by mκ is |a|²−|b|². Its derivative is 2A Im⟨a+b,F⟩. With d=B_m†(a+b), the inertial energy relative to ε times the number variation is

    E₂ = ⟨a,H_m a⟩+⟨b,H_m b⟩+Re⟨d,w⟩+2A Re⟨a+b,F⟩.

The derivative of E₂−ω(|a|²−|b|²) is 2A′ Re⟨a+b,F⟩. Pattern work alone is insufficient during switch-on/off. These balances are measured independently from the stored endpoint states and integrated midpoint sources. phase_control.py independently reconstructs the nonlinear density and gravitational-potential-times-wave product on a nine-azimuth grid at two probe times. Extrapolation in the square of a test amplitude extracts the second-order coefficient without assuming the harmonic product formula used in the solver.

### Why closing the bar frequency is not the same as closing the spectrum

For a frozen one-body eigenstate with gap Δ=E−ε, the outgoing and conjugate sideband amplitudes involve the pulse transform K(Δ−ω) and K(−Δ−ω), not a monochromatic delta function. For A=sin⁴(πt/T) supported on [0,T], put ν=2π/T. Away from removable singularities,

    K(δ) = [(exp(iδT)−1)/i] × 3ν⁴/[2δ(δ²−ν²)(δ²−4ν²)].

The code uses five shifted sinc functions at the removable singularities. For |δ|≥d>2ν, |K|≤3ν⁴/[d(d²−ν²)(d²−4ν²)]; at all d>0 one can also use min(3T/8,2/d). The last inequality uses the total variation of the compact pulse, not a resonant-state assumption. At fixed positive detuning from the entire bound band the **squared** excitation envelope therefore decreases at least as T⁻⁸ asymptotically for this particular shape. Integrating the uniform bound against the spectral measure of F bounds occupation without enumerating highly extended box states.

### A prediction with self-gravity left on

Remove the known rotating phase: u=exp(−iωt)(a+b), v=exp(−iωt)(a−b). Then i u′=H v, i v′=M u+2F A exp(−iωt), with H=H_m and M=H−2B_m L_m⁻¹ B_m†. If H,M are positive, the equation for H⁻¹ᐟ²u is a self-adjoint forced oscillator with squared-frequency operator H¹ᐟ² M H¹ᐟ². For an eigenvector U satisfying M U=σ² H⁻¹ U, normalize ⟨U,H⁻¹U⟩=1 and define c=⟨H⁻¹U,u⟩. Its forcing is −2⟨U,F⟩A exp(−iωt). Hence at t≥T the two amplitudes (c±i c′/σ)/2 are predicted **before reading the evolved state**:

    A₊ = −i (⟨U,F⟩/σ) exp(−iσt) K(σ−ω)
    A₋ = +i (⟨U,F⟩/σ) exp(+iσt) K(−σ−ω).

The sum of the two actions σ(|A₊|²+|A₋|²) is constant once the drive ends. The action difference contributes to the conserved angular momentum in units mκ. Multiplying the sum by the saved mass unit allows comparison of scales; it is **not** a direct weighing of particles in a one-body orbital. In the frozen limit it reduces to the sum of the two ordinary eigenstate occupations. A single-particle projection can continue changing after switch-off even when the collective action is constant.

For the whole subthreshold collective band σ≤−ε, suppose H≥h and M≥d. Then σ≥s=√(hd). The spectral weight summed over a complete orthonormal oscillator basis is ||H¹ᐟ² F||²=⟨F,HF⟩. The total subthreshold action per ground number is at most

    [⟨F,HF⟩/(Ns)] [Kbound(ω+ε)² + Kbound(ω+s)²].

This adds over m. It gives the same asymptotic T⁻⁸ law for the specified smooth histories with *self-gravity included*, without assuming the one-body eigenstates solve the collective problem. It excludes neither embedded nonradiating modes above the threshold nor a time-varying background, incoming occupation, instability, or a different history. In this calculation h=d=0.5 is tested by symmetric, unpivoted-positive-diagonal sparse factorizations of H−h and the gravity-augmented Schur matrix for M−d on the actual retained meshes. A small factor residual is numerical evidence of discrete positivity, not a certified continuum lower bound or a Yang–Mills mass gap.
