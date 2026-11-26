> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# Transport in a changing self-gravitating potential

**Preparation.** Use the [sealed spherical formation realization](../mts-collisionless-sheet-infall/RESULTS.md), not a static observed galaxy. Each model starts at a=0.65 on its own double-sheet snapshot. On the second mesh, prolong the complete heavy amplitude r(ψ−1) and both already-selected tag amplitudes by sine interpolation; keep the exact original positive dust mass elements, positions and momenta. No projection onto a newly selected fine-grid ground. The two tags are *alternative*, potentially overlapping initial negative subspaces, not two species. They evolve linearly in the full solution's live metric and are never added to the gravity source. A different mesh can put an identical initial state in a slightly different negative subspace. For the cold control use identical original particle labels even on the refined metric, not a different set selected on that mesh.

**Finite proper volume.** Let R=aχ, ℓ=ln(a), κ=ħ/m in Mpc km/s and H in km/s/Mpc. In physical radial measure the occupied complex wave is u(R)=exp[iHR²/(2κ)] χψ(χ)/√a. A tag uses the same conversion on its homogeneous-boundary radial wave. For a fixed *proper* outer radius B, N_B=∫₀ᴮ|u|²dR. The radial Schrödinger equation gives

    dN_B/dℓ = −J_B,      J_B = (κ/H) Im[u*(B) ∂R u(B)].

Using only the comoving peculiar current here would miss the motion of the comoving aperture boundary. Positive and negative integrals of J represent signed quantum current in opposite directions; they are not counts of distinct particles. Compute edge values and spatial derivatives directly from all sine coefficients; compare the integrated current to independently integrated stored endpoint densities. In the cold branch follow the actual initially negative particle labels in the same proper sphere. Intersections/differences of the occupied Lagrangian intervals give entered/left mass per time step. A particle passing through more than once counts more than once in gross flow; a crossing and return *within* a single step can be unresolved. Endpoints preserve particle identity. The cold tag is not a quantum measurement.

**Changing subspace.** In the Dirichlet radial sine basis b_n=√(2/B) sin(nπR/B), let q_n=〈b_n,u〉 on the aperture; q does *not* satisfy a closed evolution when u(B)≠0. The common metric gives the proper-coordinate Hamiltonian H_B=−κ²∂²_R/2+V, where V=Φ(R)−Φ(B)−(ä/2a)(R²−B²); Φ is in (km/s)². Integrating the kinetic term by parts gives the genuinely open equation

    iκ ∂t q = H_N q + κ² b′(B) u(B)/2 + [〈b,V u〉−V_N q] + scalar(t) q.

The last term is an irrelevant real phase; the bracket is measured finite-basis leakage. The sign of the surface term is positive. The negative spectral projector P gives W=q†Pq. In a smooth interval at fixed rank,

    dW/dℓ = (κ/H) Im[(Pq)† b′(B)u(B)]
           + 2/(κ H) Im[(Pq)† (〈b,Vu〉−V_N q)]
           + q†(dP/dℓ)q.

The first term is exchange with *negative modes* at an open surface, not the total current J_B. The last term describes evolution of the criterion for being negative: for eigenstates i below, j outside, 〈j|dP|i〉=〈j|dV|i〉/(E_i−E_j), plus the Hermitian transpose. This follows by differentiating the eigensystem; it is standard perturbation theory, not a new MTS coupling. [Greenbaum, Li & Overton](https://arxiv.org/abs/1903.00785) give the eigenprojector background. Where the cut gains or loses a mode, do **not** differentiate a step function as though smooth.

**Exact finite-interval cross-check.** Write ρ=q q†, use the lower of the two endpoint ranks for a persistent, energy-ordered subspace at both ends. Its exact change is tr(P_avg Δρ)+tr(ρ_avg ΔP), with arithmetic endpoint averages. Account separately for any additional state present at one end only, using its actual occupation *at that end*. No phase alignment or finite difference of arbitrary eigenvector signs is needed. This is algebraic bookkeeping, not by itself a proof of the dynamical equation: compare its two contributions with the independent surface/basis and dV terms above. Sign-changing excursions faster than the sampling interval may be missed. Potential matrix elements use V_|i−j|−V_i+j; each cosine coefficient is integrated analytically using the continuous piecewise quadratic metric and its one-sided derivative jumps. This avoids attributing changes at grid knots to new physics.

**What gravitates.** Only the complete wave enters the actual stress source. At leading Newtonian order, for C_h=8πG a³ρ̄_h (geometrized units), the heavy contribution in (km/s)²/Mpc at B and potential contribution between two shells are

    g_h(B) = −c² C_h [N_B−B³/(3a³)]/(2B²),
    [Φ_h(B₂)−Φ_h(B₁)]/c² = (C_h/2) [(1/B₁−1/B₂)N_B₁
      +∫_B₁^B₂ |u|²(1/R−1/B₂)dR − (B₂²−B₁²)/(6a³)].

The second equation follows by integrating the first and switching the order of integration. The additive potential gauge and exterior spherical shells drop out. It is the heavy density contribution to the weak-field lapse contrast, *not* an observed clock comparison; motion, other species and the cosmological background are separate. Net current enters the change in peculiar gravity via Δg_h=(c²C_h/2B²)[∫J_B dℓ+Δ(B³/3a³)]. Splitting a single wave into tag and complement requires keeping the signed 2 Re(tag* complement) density. Each term is propagated through exactly the same linear weak-field coupling; no adjustable species-dependent charge or second copy of the tagged mass is introduced. The Schrödinger–Poisson limit itself is established physics; see [Hui et al.](https://arxiv.org/abs/1610.08297). The conditional evolved state, its work and force compared on the saved MTS background are the project-specific quantities.
