# Bound matter and its common metric: which part oscillates?

We use the retained positive quadratic heavy field (pole energy 9.585761787277403e-25 eV), its existing metric coupling and the earlier spherical collisionless baryon count profile. No new gravity constant, coupling or halo force. The classical GR control with *identical* scalar and particles obeys the same equations. Scalar off and equilibrium-mean controls answer different questions.

## Matched equilibrium

In Compton units let F=1−2m/r and N=exp(ν); mass obeys m′=r²ρ with 4πG absorbed. For H=A(r) cos(ωt+θ), k=ω/N. Averaging its quadratic stress over θ gives ρ_s=z[(1+k²)A²+F A′²]/4 and p_s=z[(k²−1)A²+F A′²]/4. No extra particle species is introduced. For the resting circular counterstreams take λ=J/r²=rν′/(1−rν′), γ=√(1+λ), ρ_b=B√F γ. Solve
```
m′=r²(ρ_b+ρ_s),  ν′=(m/r²+r p_s)/F,
(r²N√F A′)′=r²N(1−k²)A/√F .
```
Regular origin, nodeless bound branch; set the scalar rest-density normalization at r=6 (40.03 pc), not at the Sun. Use vanishing field at two distant bounds, exterior lapse matched to Schwarzschild there. Each ordinary-content case has its own bound profile. Rescale time to unit central lapse for the short evolution. Within a case the same circular J of its mean is used in every real-field launch. Subtract the static mean; do not add a real wave on top of the same wave counted as matter. The short evolution is local; the global boundary problem fixes the initial mode, not a global time evolution proof.

## Driven material shell

Put σ=2ω. The real-minus-mean pressure coefficient multiplying cos(σt+2θ) is p*=z[−(1+k²)A²+F A′²]/4. The scalar flux coefficient multiplying sin(σt+2θ) is j*=zk√F A A′/2. Multiplying the radial wave equation by A turns its excess density into a weighted surface term. In particular η=z r²F A A′/4 satisfies η′+(ν′−F′/(2F))η=r² z[(1−k²)A²+F A′²]/4. This identity is exact for the stationary profile. It is not an exact nonlinear time-dependent mass formula.

At first order in the oscillating stress δm=η cos(σt+2θ)−m_b′ξ, m_b′=r²ρ_b. Conserving J along particle trajectories, δλ=−(J′/r²)ξ. Linearizing their canonical radial force and the lapse constraint gives
```
ξ̈ + κ² ξ = a cos(σt+2θ)
a = −N²[(1+2rν′)η/r² + r p*]
κ² = N²[F(1/r−ν′) (J′/r²)/(1+λ) − (1+2rν′)m_b′/r²].
```
This is a displacement of an orbit in the mean, not a fitted restoring force. Matter ends at r=5; outside it the trajectory is a tracer. The finite target separately evolves real field deviations, both matter conservation laws, gravitational mass flux and the lapse constraint (full equations in the predecessor DERIVATION.md). The four comparisons are isolated mean, supported mean, isolated oscillation, and the difference between the supported and isolated oscillations. The last includes the physical difference between their prepared profiles. It is not a partial derivative at fixed wave shape.

For extrema θ=0,π/2 and initially zero radial velocity, ξ=±a[cos(κt)−cos(σt)]/(σ²−κ²). These opposite phases are *not* a test of all initial phases. At θ=π/4 the particular periodic solution has ξ(0)=0, ξ̇(0)=V=aσ/(σ²−κ²). With arbitrary launch velocity v, the solution gains (v−V)sin(κt)/κ in addition to V sin(σt)/σ. After T=2π/σ its net displacement is (v−V)sin(κT)/κ; its net velocity change is (v−V)[cos(κT)−1]. Canonical P(0)=γv/(NF) at this order. These two quadrature initial states are frozen prospective tests, not outcomes of the finite run.

## From held clocks to a freely responding pair

In a separate, exploratory weak-field calculation take δν=U cos(σt), δg_rr/2=V_r cos(σt). At leading weak-field order V_r=z r A A′/4 and U′=z[A A′+r(−2A²+A′²)]/4, retaining the spatial gradients for the frozen envelope. With propagation direction n and μ=n·r̂ along an unperturbed ray, the linear electric tidal curvature amplitude is T_nn=μ²(U″+σ² V_r)+(1−μ²)U′/r. This follows from R_0i0j=∂i∂j U−(1/2)∂t²δg_ij at this order. With l measured back from the receiver, the free proper timing residual (up to phase/sign convention and fitted integration constants) has amplitude σ⁻² ∫T_nn exp(−iσl) dl. The independent one-way null-redshift computation includes both endpoint velocities −∇U sin(σt)/σ. Their difference cancels the large held-observer acceleration terms by integration by parts. A uniform-density core recovers the familiar potential amplitude πGρ/ω² in physical units (dimensionless metric potential for mass density and angular frequency); see [Khmelnitsky & Rubakov](https://arxiv.org/abs/1309.5888). Neither the fixed-radius cloud nor a timing calendar is a measured pulsar residual.

The line-of-sight exercise assumes a spherical, coherent, static mean halo assigned to the Galactic centre, negligible endpoint orbital evolution during observing, an unbent ray, no disk compression, and no propagation phase correction from the mean Galaxy. These physical approximations are separate from quadrature accuracy. The inferred pulsar distance spans multiple signal phases; a nominal prediction is not a robust limit. Galactic occupation and coherence were not derived from formation here.
