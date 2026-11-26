# Fixed occupation: from the signed stellar source to a force

## Stationary response

Work in the saved mass-weighted, real, even axisymmetric basis, so that an occupation is N = gᵀg. Two independent values of N are retained. Write the dimensionless constrained equation as (T + V₀ + aW + U[g²])g = μg; U is the attractive discrete Poisson potential. a=1 is the physical 0.4 stellar transfer, not the entire nominal S22 source. Products inside U are physical-space products with the original angular quadrature. W uses the signed new-minus-donor azimuthal mean and the vacuum Newton kernel, not a local force divided by a distance. Each cylindrical ring has zero added stellar mass; enclosed *spherical* mass, quadrupole and force need not vanish.

Let H = T + V₀ + U[g²] − μ, B map a potential to its product with g, and L be the positive discrete Poisson operator including the vacuum boundary. The density variation is 2gx. Eliminating its potential gives M = H − 2BL⁻¹Bᵀ. Differentiating at a=0, Mx − gμ′ = −Wg and gᵀx=0. With y=g″, the second derivative obeys My − gμ″ = −2[(W + U[2gx] − μ′)x + U[x²]g], with gᵀy=−xᵀx. Thus ρ′=2gx, ρ″=2(x²+gy), and the exact finite response is Δρ=2gΔg+(Δg)². The same signed Poisson readout is applied to all three. Symmetric perturbed equilibria and an independent residual equation in Δg check these formulas. In particular a spatially constant W changes μ, not the density. The equilibrium changes redistribute mass, not the occupation.

## Why one-way growth has a linear bound

Here H and M denote their restrictions/projections to g-perpendicular. Both are positive in the tested matrices; bordered symmetric factorizations check inertia and their reconstruction errors. For the initially unexcited response, ẋ=Hv, v̇=−Mx−a(t)F, F=P⊥Wg. A step in a has stationary shift xₛ=−M⁻¹F. In coordinates M¹ᐟ²x the homogeneous cosine propagator of the positive symmetric matrix M¹ᐟ²HM¹ᐟ² has norm ≤1. Integrating the step response against da therefore gives ‖x−xₛ‖_M ≤ TV(a)‖xₛ‖_M at final a=1. It holds for fast and slow turn-on, including jumps. The observable gradient columns A give G=AᵀM⁻¹A. Each linear force lies within its static value ±√(Gⱼⱼ FᵀM⁻¹F) for monotone growth. Minimize the energy over the four-component allowed force box to get a necessary total variation in the *linear* model. The saved box for that diagnostic is the previous frozen-force contract, not a claim that repeated pumping remains linear.

## A nonlinear check that does not choose a turn-on time

This step concerns the isolated finite-mesh wave with the same time-dependent ordinary source. It does not assume the field remains real. Fix the global phase while the overlap is nonzero, writing ψ=cg+u+iv, both deviations perpendicular to g, ξ²=‖u‖²+‖v‖², c=√(1−ξ²/N). Put b²=uᵀMu+vᵀHv. The constrained positivity checks yield ξ²≤b²/λ and ‖gu‖_D≤C_B b, where ‖d‖²_D=dᵀL⁻¹d for the density's Poisson right-hand side. The second inequality follows from testing M−BL⁻¹Bᵀ/C_B² on the tangent space.

Write Q=|u+iv|²−(ξ²/N)g². A nonnegative quadrature density of mass ξ² is a positive mixture of unit atoms of total weight ξ². The triangle inequality in the Poisson norm gives ‖Q‖_D≤C_Q ξ². C_Q is the largest unit-atom norm plus ‖g²‖_D/N. Each atom norm uses all retained Poisson multipoles and the corresponding diagonal entries of the inverse radial operators; no continuum point self-energy is used.

At equal N the isolated energy difference is ψ†Hψ−gᵀHg−½‖2cgu+Q‖²_D. Since c≤1, cancellation of the leading 2‖gu‖²_D term leaves the conservative lower bound at radius b:
 
L(b)=b²−2 C_B b C_Q r²−½(C_Q r²)²−2r‖Hg‖−r²|gᵀHg|/N, with r=b/√λ.

For a drive aW the exact work equals ∫〈W〉 da. Relative to the initial 〈W〉, the integrand is bounded by 2√S b+w r² as long as the tangent energy radius stays ≤b. Here S=FᵀM⁻¹F and w=‖W−(gᵀWg/N)I‖. Removing the final driven potential costs at most the same amount. Thus for 0≤a≤1 growing once from zero, the isolated excess energy cannot exceed U(b)=4√S b+2w r² up to first crossing. A radius with L(b)>U(b) and r²<N cannot be reached from g, even with jumps in the drive (the state remains continuous). The positive margin is tested on both meshes and occupations. For a force operator O its change is bounded by √Gⱼⱼ b+‖O−(gᵀOg/N)I‖r². This controls the actual nonlinear wave, not only the tangent calculation, under the stated forcing hypothesis.

The stored checks are floating-point matrix estimates with inertia, factorization and direct complex-energy controls, not an interval-arithmetic or continuum proof. This argument supplies no bound on simultaneous nonlinear satellite work, a rotating bar, sign-changing assembly, or an initially excited wave. No measured force band was used to set the source, N, energy radius, or the force operator.
