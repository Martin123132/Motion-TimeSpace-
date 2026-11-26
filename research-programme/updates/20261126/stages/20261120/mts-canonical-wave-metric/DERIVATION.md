> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# Finite canonical dynamics on the reconstructed metric

The previous action and current calculation (not bundled here) gives two canonical quadratures, not the identity P=b⁶z at all times. Here both are initial data. The common metric has lapse N=exp U and spatial scale a b², V=−2 log b. Let η be conformal time, ω=a m, d=3aH/2, T=N b². The physical mass m and background expansion are those used in the saved formation runs. In the rotating, dilution-removed variables let u=r z and v=r P. For a **frozen** slice:

    u′ = (iω+d)u − iω N b⁻⁶ v
    v′ = (iω−d)v − i[ω N b⁶ + S/ω]u
    S[u] = −∂r(T ∂r u)+(∂rT/r)u.

Primes on u,v here are conformal time derivatives. The last expression follows by writing −r div(T grad z) with z=u/r; in particular S[r]=0. In time-dependent geometry the canonical variables are still u,v; the change of variables used *within one frozen step* below is undone before passing to the next slice. It is not a new time-dependent canonical prescription. The inherited sign of the mass terms corresponds to removing the positive rest phase. For comparison, [Namjoo, Guth & Kaiser](https://arxiv.org/abs/1712.00445) explain why fast and slow components of a real scalar must be distinguished. Our shell calculations are not a result imported from that paper.

**How the mass oscillation is handled.** Introduce M=N½b⁻³ and x=u/M, y=Mv. Removing iωI leaves a two-component generator −iω J. Its square after division by −ω² is C·I, where

    J(x,y)=(i d x/ω+y, [C+(d/ω)²]x−i d y/ω)
    C=1+W,    W=(N²−1)−(d/ω)²+M S M / ω².

The two spectral factors over Δη are exp(−iωΔη·W/(1+√C)) and exp(2iωΔη) exp(+iωΔη·W/(1+√C)). Thus the second frequency sector rotates rapidly, but **the spatial operator inside these exponentials varies only by the small differential phase**, not by the large common mass phase. The full frozen map is the half sum of the factors times I plus their half difference times J/√C. No small-velocity truncation, identification of the two quadratures, or artificial damping of the fast component is needed. Evaluate the resulting matrix functions with a Chebyshev polynomial and a conservative interval for W, computing N²−1 with expm1. The polynomial and midpoint freezing are numerical approximations, not physical assumptions. A mixed-frequency analytic mode and a full variable-lapse matrix exponential provide independent frozen-step controls. The full matrix control tests the temporal calculus on the *same* spatial discretization, not continuum accuracy. Forward/backward and Wronskian tests use zero endpoint perturbations.

**Space and boundary.** The origin is a regular odd endpoint for u and v, not an extra density datum. At L=24 comoving Mpc the exterior is the *evolving homogeneous* two-quadrature state at the saved expansion and N=b=1; this is a specified matching condition, not an observation. It can exchange wave current with the interior. At each application subtract the affine continuation r u(L)/L, on which S is zero; represent the remainder on the sine grid. The gradient part of S is the cosine quadrature adjoint D* T D; the multiplicative term uses ∂rT obtained from the solved spatial and lapse gradients. Quintic radial interpolation for the stress recovers z(0) from the derivative of the represented sine field. No artificial reflecting inner shell is placed at a clock site.

**Closing the source.** For the general independent pair the dimensionless scalar sources are

    E/ρ̄=(|z|²+|P|²/b¹²+|∂r z|²/(ω² b⁴))/2,
    j_r/ρ̄=Im(P*∂r z)/(m b⁶),    (P_r−P_t)/ρ̄=|∂r z|²/(ω² b⁴).

Subtract the evolved *homogeneous* scalar energy when forming the excess; the catalogued H(a) supplies the smooth background. This is the paired or phase-averaged stress, not the oscillation-phase-resolved stress of a specified single real-field realization. For dust, each signed stream uses the same positive mass and canonical Hamiltonian as in the previous geodesic experiment. Evolve a midpoint prediction for both the wave and the mass-weighted projected streams, rebuild the constraints and lapse there, then step the full system from its old state with that midpoint generator. The scale-factor mean in the full-step mass phase uses Simpson integration of the independent expansion solution. The phase of an independent microscopic local cosmological clock is not measured. This scheme does not evolve the exterior cosmology or remove the original regularized central dust continuation.

**Independent diagnostics.** For a shell the coherent-pair bilinear is Q=∫r²Re(z*P)dr; its expected change is the time integral of J(inner)−J(outer), where J=r²T Im(z*∂r z)/ω. Units omit a common occupation factor. Compare the actual end-minus-start charge with face currents sampled from the wave and geometry. The other independent forecast is ∂ηV=a(H−Nh), from the normal expansion; measure it from the evolved spatial potential. The scale for each rate is unchanged. For null paths use the earlier two-emitter/single-receiver construction rather than interpreting potential values at one time as a frequency measurement. The pressure or charge-like Wronskian alone does not imply Maxwell charge for this matter field. The Einstein constraints used here are those of the [3+1 formulation](https://arxiv.org/abs/gr-qc/0703035), not inferred from a successful fit to force bands.
