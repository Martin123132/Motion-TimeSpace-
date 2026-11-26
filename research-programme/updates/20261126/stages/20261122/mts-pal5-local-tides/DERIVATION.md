# Differential gravity and what an escape indicator means

Let Φ(r,μ,t) be the saved external Newtonian potential in (km/s)², μ=z/r, n=x/r, m=e_z−μn, P=I−nnᵀ. For A=(1 km/s in kpc/Myr)² the gravitational acceleration gradient is

    T = −A [ Φ_rr nnᵀ + (Φ_r/r−μΦ_μ/r²)P
              + (Φ_rμ/r−Φ_μ/r²)(nmᵀ+mnᵀ) + Φ_μμ mmᵀ/r² ].

This follows from ∇r=n, ∇μ=m/r, ∇²r=P/r and Hess μ=−(nmᵀ+mnᵀ+μP)/r², with ∇²r here denoting the Hessian. T is symmetric, in Myr⁻²; positive eigenvalues stretch. It is evaluated from the saved radial value and slope, the radial Hermite curvature on each interval, and angular derivatives of the even Legendre multipoles through degree 68. Fine differences of accelerations check it independently. External force differences across a star and its cluster are evaluated directly in the nonlinear dynamics; the linear tensor is not substituted for them.

For a centre X obeying the same external force and a nonrotating translating frame,

    ξ̈ = a_ext(X+ξ,t)−a_ext(X,t) − GM ξ/(|ξ|²+a²)^(3/2).

The last term is a conditional Plummer model, not an inferred tidal prescription. In the frame whose radial axis tracks X with minimal rotation Ω=X×V/|X|², the additional terms are −2Ω×ξ̇−Ω̇×ξ−Ω×(Ω×ξ), where Ω̇=X×a/|X|²−2(X·V)Ω/|X|². The real symmetric stretching operator for frozen zero frame velocity excluding Euler force is T_eff=T+|Ω|²I−ΩΩᵀ. For λ=max eig(T_eff)>0, an isolated point mass would balance at (GM/λ)^(1/3). A Plummer cluster instead gives

    r_axis² = (GM/λ)^(2/3)−a².

A nonpositive squared radius means even the local linear tide dominates the model core along that axis, not a negative radius. A fully compressive nonrotating field need not give an inertial tidal radius. We also solve the finite external force balance on each sign of the eigenvector, including centrifugal and Euler forces, before assessing the leftover perpendicular acceleration. Neither axis roots nor instantaneous eigenvalues give a conserved Jacobi energy on an eccentric, time-dependent trajectory. The primary orbits never throw out or release a star just because it crosses such a radius.

The reported stellar energy is E_c=|ξ̇|²/2−GM/sqrt(|ξ|²+a²) in the translating nonrotating frame. For fixed mass and scale, exactly

    dE_c/dt = ξ̇ · [a_ext(X+ξ,t) − a_ext(X,t)].

Its sign can return negative after going positive, with ordinary tides alone or with a wave. A negative value need not imply permanent capture and a positive value is not proof of permanent escape. Shells with identical terminal sign counts may have quite different tidal work and phase-space trajectories.

For the original host, the representation before resampling is element-polynomial B_l(s)=r Φ_l. Native radial derivatives follow from (rΦ)'=B' and (rΦ)''=B'', so Φ'=(B'−Φ)/r and Φ''=(B''−2Φ')/r. At element faces, a continuous B can give distinct one-sided forces. The native implementation uses the same mean of side traces at an exact face as the original evaluator and does not define a unique classical Hessian across such a jump. The native stellar integrator uses the actual finite forces; central numerical derivative checks inside cells avoid faces. For a transverse radial crossing the variation caused by shifting crossing time is δv⁺−δv⁻=(a_after−a_before)(n·δx)/(n·v). This is a sensitivity of the represented field, not an extra physical impulse applied to stars. The saved face ledger evaluates this on bracketed crossings of the centres.
