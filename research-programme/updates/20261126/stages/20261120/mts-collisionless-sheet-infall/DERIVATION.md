> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# One weak-field potential, even after streams cross

Work in the retained nonrelativistic, spherical branch, c=1 unless physical units are stated. The previous checkpoint supplies a, the complex heavy wave, and for each pressureless species s its ordered initial mass M_s(q), present oriented comoving position X_s(q) and canonical momentum p_s=a² dX_s/dt. The coordinate q labels initial comoving radius, not current position. A particle passing through the origin continues to negative X; its physical radius is a|X|. A positive-mass label is neither merged nor discarded.

Preserving the sheet through a caustic is an established collisionless method; see [Hahn & Angulo, phase-space elements](https://arxiv.org/abs/1501.01959). The calculation here is a radial reduction coupled to the retained heavy wave, not their 3D simulation. The collisionless source of the Newtonian metric is

    I_s(r)=∫ 1{|X_s(q)|≤r} dM_s(q),       I_h(r)=∫₀ʳ |ψ|² s² ds,
    ∂rΦ(r)=Σ_s C_s [I_s(r)−r³/3]/(2a r²),    C_s=8πG a³ ρ̄_s.

Each normalized species has homogeneous enclosed mass r³/3. The heavy wave evolves in the same Φ as all the dust. A field inferred from another branch or a phenomenological halo term is not inserted. In a cell of the Lagrangian sheet, X,p are linear in q and dM/dq is proportional to q²; this reproduces the supplied cell mass exactly. Intersect the oriented segment with each **signed** Eulerian bin and fold contributions onto |X|. At a regular positive radius, each root contributes density n_i=(dM/dq)/(r²|∂qX|) and velocity v_i=sign(X)p_i/a. Thus the cold radial stress relative to bulk flow is Σ n_i(v_i−v̄)²; no equation-of-state parameter was added. This classical radial family has no transverse dispersion. Relabeling streams by current radius and interpolating a single velocity would throw away this stress.

## Metric coupling from a discrete energy

Two force implementations are retained. One integrates Gauss's law for a uniform density in each radial shell, keeping both interior and exterior potentials. The independent action method uses continuous radial basis functions B_i, linear in r² per bin, and Φ(L)=0. In the normalized action the field equation and eliminated interaction energy are

    K Φ = −b/(2a),        K_ij=∫ r² ∂rB_i ∂rB_j dr,
    U=½ b·Φ=−a ΦᵀKΦ,     δU=Φ·δb.

Here b sums each species' **excess** density load multiplied by its own C_s. A link carries stiffness 4(r₂⁵−r₁⁵)/[5(r₂²−r₁²)²]. The continuum density integral of B_i over each intersected dust sheet is polynomial and performed exactly for that representation. Wave excess at the interior sine nodes uses the radial trapezoidal load h r_i²(|ψ_i|²−1); the multiplicative potential and that load are adjoints in the same radial kinetic inner product. The exact homogeneous state has no force. For sheet shape functions L_j(q) the impulse follows by variation, not a second force law:

    A_ij=∫L_iL_j dM,     A dp/dt=−∫L_i ∂_XΦ(|X|) dM.

C_s cancels against its inertial normalization. A is positive and unchanged through folding. For each occupied cell the force is linear in X, so the right side is another polynomial moment. Fixed origin and outer labels have prescribed endpoint reactions; the wave boundary is open as before. Commuting the mixed variations of U gives a testable symmetry: changing a fixed-number wave density must change the force on a dust displacement by the same bilinear amount that the dust displacement changes the wave potential energy. [Numerical variations on the folded state](evidence-001.zip) (archive member: `action-and-fold-checks.json`) test both directions. This derives the transpose couplings of the discretized retained Newtonian limit, not a new microscopic value of G.

## Time dependence and a stress check

For any smooth odd radial test function f(X), the sheet equation predicts

    d∫p f(X)dM/dt = ∫[(p/a)² f′(X)−f(X)∂_XΦ] dM.

We measure both the continuous force sampled on the sheet and the interpolation of the actual nodal impulses; their difference is a spatial discretization diagnostic, not an extra force. For a radial wave define P_f=∫r² f Im(ψ*∂rψ)/m dr. The integrated scalar momentum equation is

    dP_f/dt = ∫r²{ [|∂rψ|² f′−|ψ|²(f‴+4f″/r)/4]/(m²a²) − |ψ|² f ∂rΦ }dr.

Integrating the gradient correction to the quantum stress by parts leaves derivatives of the test function through third order. Radial and two transverse tensor components are both included. Use f=r exp(−r²/2b²), exponentially negligible at the outer boundary. Trapezoidal integration of signed work in time is compared with the change of the first moment; normalization is by the integral of absolute stress and gravitational work. An extra instantaneous sine-grid commutator diagnostic distinguishes this continuum stress from the exact spatially discretized kinetic/potential rates.

For u=r(ψ−1) with u(0)=u(L)=0, write u=Σ b_n sin(k_nr). During the free step b_n→b_n exp[−ik_n² Δt/(2ma²)]. The exactly integrated outward boundary current of the interpolant is 2L Re Σ(−1)^n(b_n,after−b_n,before)/k_n. We compare to the change of mass from positive midpoint quadrature of |rψ|² (the midpoints are evaluated by sine interpolation). A first trial that cubically interpolated the rapidly changing **complex amplitude** before squaring showed a spurious mass deficit. Both methods conserve the same spectral drift; that cubic readout is not the accepted density prescription. The absolute physical flux at the artificial wall need not vanish; subtracting it to check the budget does not establish independence from the exterior.
