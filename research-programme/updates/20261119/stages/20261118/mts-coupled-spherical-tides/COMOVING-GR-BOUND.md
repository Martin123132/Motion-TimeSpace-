# Eliminating the unknown ordinary rearrangement from a finite-time GR bound

There is a stronger result than adding an unspecified ordinary-force correction. In spherical Einstein gravity take geodesic dust as the ordinary material, with an optional positive canonical massive scalar. Release the observer comoving with the dust (or continue its geodesic congruence into the initial vacuum exterior). Match the initial areal radius R₀, rest initial velocity and conserved baryon rest mass in each initial areal shell. Write e,j,s for energies/flux/stress multiplied by 4πG in c=1 units. All quantities below are dimensional in these geometrical units, or scaled by the retained pole as in the simulation. The following inequalities are analytic, not regressions.

**Initial mass.** At rest the specified conserved profile is D=aρ. Write m₀(R₀) for the ordinary-only Misner–Sharp mass. For the same D plus a scalar, the initial enclosed mass difference obeys
    ΔM' + [2rD/(√(1−2M/r)+√(1−2m₀/r))] ΔM = M_h',    ΔM(0)=0.
This follows by rationalizing the difference of the two square roots in the dust mass constraint. Positivity and the integrating factor give 0≤ΔM(R₀)≤M_h(R₀). The ordinary part alone can decrease at fixed baryon rest mass; ignoring that distinction would give a spurious force. If both radial metric factors are ≤a_* on the initial shell, |Δρ₀|≤D(R₀)a_* M_h(R₀)/R₀.

**Evolving enclosed mass.** Along the dust geodesic dR/dτ=Wv/a, dt/dτ=W/α. The total mass equations reduce to
    dM/dτ=R² W/a (v e_h−j_h).
Ordinary dust cancels *exactly*, since its Eulerian flux is v e_d. The ordinary-only reference mass therefore stays m₀ on that shell. The same identity holds for an exterior geodesic while it remains outside ordinary matter. This is not conservation of wave particle number: it is the gravitating mass inside the moving sphere. It removes the need to guess an ordinary redistribution term.

**Observable equations.** In the dust frame the transverse ordinary pressure is zero in the radial boosted-stress term. The angular Jacobi field of a radially falling congruence is J_t=R/R₀, and
    R″=−M/R²−R s'_h .
For a radially neighboring comoving dust geodesic, number conservation gives ρ_d J_r (R/R₀)²=ρ_d0 until shell crossing (the density term vanishes in an empty exterior). The radial Jacobi equation becomes
    J_r″=[2M/R³−(P̂²−X̂²)] J_r −ρ_d0 (R₀/R)² .
Primes here are observer proper-time derivatives; P̂,X̂ are the Eulerian scalar time/radial derivatives in the stated rescaling. Their squared difference is invariant under a radial boost. These exact equations contain both Ricci and Weyl, and are directly testable from saved motion. No closure is needed for the ordinary density after specifying its initial profile.

**Sufficient bound.** For 0≤τ≤T assume regular solutions and matched geodesics with R_*≤R,R_b≤R^*, |v|≤v_*<1, and a≥1. Suppose the scalar Eulerian energy obeys 0≤e_h≤ε along this tube, and M_h(R₀,0)≤μ. The latter is ≤ε R₀³/3 if the same energy envelope holds throughout the initial enclosed region. No smallness of the carrier's gradients or its phase is assumed separately. Put W_*=(1−v_*²)^(-1/2), D_v=(1+v_*)/(1−v_*), and
    B_M=μ+T(R^*)² W_*(1+v_*) ε .
Then |M−m₀|≤B_M from the moving mass law and |j_h|≤e_h. The radius difference satisfies |ΔR″|≤K_R |ΔR|+F, with K_R=2m₀/R_*³ and F=B_M/R_*²+R^*D_v ε. Define C(K,T)=[cosh(√K T)−1]/K and S(K,T)=sinh(√K T)/√K, using their continuous zero limits. Twice integrating the acceleration inequality, or iterating its positive Volterra kernel, yields
    |ΔR| ≤ B_R=F C(K_R,T),      |ΔJ_t| ≤ B_R/R₀.

For radial separation use |P̂²−X̂²|≤2ε and a bound J_* on |J_r,b| from the ordinary-only solution. Let
    K_J=2(m₀+B_M)/R_*³+2ε,
    F_J=J_*[2 B_M/R_*³+6m₀ B_R/R_*⁴+2ε]
        +(R₀/R_*)² D(R₀)a_* μ/R₀ +2ρ_b0 R₀² B_R/R_*³.
Both initial radial separations are normalized to 1. Initially normal neighboring geodesics can have nonzero relative radial speed from the slice extrinsic curvature; the difference from the ordinary reference is bounded by V₀=R₀ a_* ε. Hence
    |ΔJ_r| ≤ V₀ S(K_J,T)+F_J C(K_J,T).
No lower bound on the mixed signal is implied. These bounds can be conservative and do not identify a particular occupied state. For bounded T, fixed regular geometry margins, and μ,ε→0, both *measured* separations recover the ordinary GR solution uniformly, regardless of scalar phase. This is stronger than just setting the scalar to zero: it specifies which stress and enclosed-mass budgets are sufficient, and no unknown ordinary-stress difference remains on the right-hand side.

**Scope.** The result assumes the retained common Einstein metric, spherical symmetry, positive canonical scalar stress, geodesic pressureless ordinary matter without multistreaming, aligned initial baryon labels, and a bounded time interval and energy envelope. No theorem here derives the envelope in an actual galaxy or the full Einstein action from deeper MTS variables. A pressure-supported or nonspherical ordinary system adds terms. The radii of a growing horizon, shell crossing or arbitrarily long evolution are not covered. An isolated synthetic cloud is not a calibration of a Solar System PPN parameter. The same comparison supplies an empirical interface: an independently established local stress and initial enclosed-energy limit can be inserted into the explicit bounds, with the geometry and duration of the intended test.

