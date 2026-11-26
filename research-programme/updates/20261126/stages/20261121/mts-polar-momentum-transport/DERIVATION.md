# Which angular momentum is being transported?

This is the polar momentum coefficient multiplying ∂θY₂₀ in a diagonal spherical background with a linear, even quadrupole. It is **not** an axial spin, a halo occupation or a new material coupling. Use the retained unit lapse, zero shift and 8πG=1 convention. Write A=exp(ℓ), B=r exp(b), V=AB², K=−∂t ln V for the background. Convert an orthonormal polar component to a coordinate covector by multiplying by **its own** B on each member of the signed host pair. Do that before differencing.

## Exact continuum relations in this sector

Write p for the isotropic stress, s for its radial trace-free coefficient (radial stress p+s), c for the orthonormal rθ stress, t for its trace-free angular tensor coefficient, and L₂ for the radial log-metric perturbation. The polar divergence is
```
D(S)θ = ∂r(B³ c)/(AB²) + p₂ − s₂/2 − 2 t₂ − (3/2) s₀ L₂ .
```
The first term is a **radial flux**, not spherical enclosed mass. The −2 is the divergence of the trace-free ℓ=2 Hessian on the unit sphere, 1−ℓ(ℓ+1)/2. The last term is the background radial/tangential stress difference contracted with the perturbed connection. It must not be dropped on an anisotropic background. Direct differentiation of the mixed-index divergence in the curved manufactured check gives the same coefficient at two nondegenerate polar angles.

At a smooth Cartesian origin, take the regular constant traceless tensor diag(−1/2,−1/2,1). Its orthonormal rr component is Y=P₂; its rθ component is (∂θY)/2 and its traceless tangent component is (∇θ∇θY+3Y)/2. Hence a regular extrinsic quadrupole may have **nonzero** s₂(0), with c(0)=t₂(0)=s₂(0)/2, rather than all three being zero. Let S=B/(rA), U=(S−1)/r², d_c=(c−s₂/2)/r² and d_t=(t₂−s₂/2)/r². For an elementary-flat even background, s₀=O(r²), K₂=O(r²), and the geometric covector can be written without a constant-term cancellation:

    τ/r² = S c′/r + 3[U+S b′/r]c + 3d_c − 2d_t − 2K₂/(3r²) − (3/2)(s₀/r²)L₂.

This is an algebraic change of variables for smooth data, not a boundary condition imposing τ=j. An even Taylor continuation has c′/r→2c₍₂₎. We checked the resulting centre coefficient on a curved manufactured tensor with nonzero leading shear. The independent 4-, 6- and widened 4-node origin extrapolations on the real snapshots are diagnostics, **not** boundary values to feed back into the model. Unstable estimates cannot certify a pointwise origin limit.

Apply this operator also to Kⁱⱼ−δⁱⱼ K: replace p₂ by −2K₂/3, s by extrinsic shear, c by extrinsic rθ and t by extrinsic angular tensor. Call the resulting covector τ. With material j, P=τ−j, H=R+K²−KⁱⱼKʲᵢ−2E and η=∂t j−K j+D(S)θ, the retained angular ADM transport gives
```
∂t τ = K τ − H₂/2 − D(S)θ ,
∂t P = K P − H₂/2 − η .
```
The factor ∂θY is factored out; there is no extra factor of 1/B in the covector equation. Neither H₂ nor η is set to zero. For a fixed compact taper w, the independently testable matter equation is
```
d/dt ∫ w V j dr = ∫ w′ B³ c dr − ∫ w V [p₂ − s₂/2 − 2 t₂ − (3/2) s₀ L₂] dr + ∫ w V η dr .
```
For the geometric equation add −∫ w V H₂/2 instead of the η term. This is a local weighted momentum balance, not conservation of each shell with no work through its boundary. Computations use the actual cold, ordinary, scalar and surrounding derivatives and stresses, not a flux defined from the measured shell change. The signed projection and the wave-minus-cold contrast are separate operations. The original proper-distance detectors are scored separately.

## Why two strong-form readouts disagree

Let V_f here denote the **face tilt velocity** (not the proper volume above), S=B/(rA), D₁₂ the evolution face-to-centre derivative, I₁₂ its interpolation and Dold the independent cell-to-cell derivative. The physical centre cross curvature is −S I₁₂ V_f/2 up to the fixed launch interpolation offset. The leading difference in polar covectors is therefore
```
−r S² [Dold I₁₂ V_f − D₁₂ V_f]/2 .
```
This predicts a field with a sign and a radial profile before subtracting any measured constraints. Terms from the derivative of S, non-exact finite-difference product rules and the launch offset are not assumed zero: the actual unexplained part is scored. Near the alternating grid mode face-to-centre averaging loses information, whereas a face derivative remains sensitive. This finding alone would *not* justify discarding an unfavourable readout. Independent conservative face-flux derivatives of orders 6–24, independent cell values, common-radius samples and weak fluxes are all retained.

## A change in arithmetic, not in the action

For angular chart increment y and launch y₀ the two curvature expressions have the form R=nL(y₀+y)+C(t), n=A⁻², L a linear derivative stencil, C the curved lower terms. The code adds the exact analytic reference and needs R−sR₀, where s=n/n₀. Computing both full, reference-sized derivatives before subtraction puts their floating-point errors through up to two spatial derivatives. Algebraically the required increment is **nL(y)+C(t)−sC(0)**. The same rearrangement applies to the radial curvature; the production time step and Hamiltonian, momentum, material, grid and detector definitions are untouched. In the synthetic tiny-increment test two full binary64 arrays are indistinguishable although the incremental curvature is nonzero. A separate 68-decimal calculation, not the new formula used as its own answer, provides the benchmark.

## Microscopic source of the polar force

For the retained scalar write a=ln|ψ| and φ=arg ψ in its factored carrier variables, μ the saved carrier scale, ζ its saved normal variable. The comoving number on the monopole is Nw=exp(ℓ+2b+2a₀)(1−Im ζ₀). The matter action gives the **density-weighted covector**
```
V jθ,w = r² ρ* Nw [ φ₂/μ − (Re ζ₀+K₀/(2μ)) a₂ / (μ (1−Im ζ₀)) ] .
V jθ,c = r² ρ* Nc u₂ .
```
Here u₂ is the cold velocity potential and ρ* is the same retained species normalization, not a new fit. The exact wave-minus-cold split is the sum of (Nw−Nc)u₂, Nw(φ₂/μ−u₂), and the normal-amplitude term, all multiplied by r²ρ*. It distinguishes movement of population, phase slip, and stress from amplitude without assigning a new occupation or discarding the common formation state. This does not fix galaxy-specific formation data.

Independently, the scalar rθ stress is ρ(a₀′a₂+φ₀′φ₂)/(μ²AB). It enters the boundary term with B³. Its remaining angular stress is (ρ[excess−gradient²]/2)₂ − (ρ gradient²)₀ L₂ in the retained normalization; the exact definitions of excess and gradient are evaluated using the saved canonical normal rate and spatial coframe. A cold irrotational species has no linear transverse pressure on this background, but has radial transport and the background radial-stress connection term. The independent force budget integrates these actual stresses from the five saved epochs and compares to the endpoint change, subtracting the launch rather than treating a pre-existing current as produced by the later history. Sparse quadrature is reported separately; five epochs do not constitute a certified integration bound for fast substep transients.
