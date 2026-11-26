# From a finite formation contrast to the Newtonian wave term

**Arithmetic, not a changed coupling.** Let Y denote the zero-host solution and h the full host minus zero-host difference *within one matter branch*. Propagate Y and h through every stage of both retained Einstein–matter evolutions. The secant of a product is hₐ b+(a+hₐ)hᵦ. For a ratio it is [hₐ−(a/b)hᵦ]/(b+hᵦ); for exp it is exp(a)expm1(hₐ). Spatial differentiation is linear. Apply the original stencils to the stored launch and the increment separately, retaining the analytic initial metric derivatives. No small-host Taylor expansion is imposed. The existing linear angular truncation, centred shear stencil and outer boundary are independent of this change of coordinates. Source and zero-host branches use their respective original incident banks. The number chart and its inverse are described in [its prospective protocol](NUMBER-CHART.md).

**Source ownership.** In the rotating wave frame define the velocity potential p=Im(w)/μ, so ṗ=Im z. For dust ṗ=−(γ−1). A compactly supported test of the field equations supplies the density response; p is a matter velocity potential, **not the Newtonian gravitational potential**. See the [monopole source derivation](MONOPOLE-SOURCE.md) for the signed wave/dust current comparison.

For a face value define L=exp(−Iℓ), U=D_f p, u=LU, B=(I N)L and V=u/γ. The cold mass flux without its geometric area is BV. For cloud minus cold, bars denote arithmetic means, not fitted backgrounds. The exact product identity gives
```
δ(BV) = V̄ L̄ δ(IN) + [V̄ (IN)̄ + B̄ d Ū] δL + B̄ d L̄ D_f δp,
d = [γ̄ − ū (u_w+u_c)/(γ_w+γ_c)]/(γ_w γ_c).
```
This is a symmetric finite-difference identity for the three prepared variables, not three extra adjustable sources. The implementation sums their radial divergences and compares the result with evaluating the two cold fluxes separately; it then takes host minus zero. Reported projections are onto the actual total. They can be negative or exceed one under cancellation and are not probabilities.

**Why the phase changes.** The continuously time-evolved discrete wave equation has
```
ż = 2iμz + (S−κ)/μ − μ z²,
κ = K̇/2 − K²/4,       S = L_g w + (e^(−ℓ) Dᵣw)²  (monopole).
```
This uses the actual K̇ for each of the two off-constraint formulations. Freeze the non-carrier source at launch but integrate the carrier exactly. The wave phase consists of an affine-in-time contribution and an oscillation:
```
p(t)−p₀ = t Im[z₀−ż₀/(2iμ)] + Im[ż₀ (exp(2iμt)−1)/(2iμ)²].
```
Only the frozen-source approximation is made here; the identities for its launch coefficients are algebraic. In particular,
```
Im[z₀−ż₀/(2iμ)] = (Re S₀−κ₀)/(2μ²) − Re(z₀²)/2.
```
Writing a=Re w and u_w=e^(−ℓ)Dᵣp_w, the nonoscillatory wave-minus-dust potential rate is therefore
```
[L_g a + (e^(−ℓ)Dᵣa)²]/(2μ²)                      amplitude pressure
− κ/(2μ²) − Re(z²)/2                               geometry and transformed velocity
+ (u_c−u_w)(u_c+u_w)/2 − (γ_c−1)²/2                kinetic and relativistic dust terms.
```
In addition, applying the two different spatial operators to the *same* dust phase rate contributes a calculable term to the current comparison. We retain that term and the oscillatory part. [The prediction protocol](PHASE-TEST.md) states which terms evolve and how the time integral is formed. The sign-flip and omission controls diagnose this approximation, not an alternative cosmological fit.

**Newton limit of the amplitude term alone.** On this mechanical contraction μ_q=√q M, M=a_FRW m, and the metric launch approaches flat space. The rest-density amplitude is a=(1/2)log n plus the normal-frequency and metric factors. Thus the *rescaled* amplitude term tends to [Δ_r log(√n)+|∇log(√n)|²]/(2M²), equal in the continuum to Δ_r√n/(2M²√n). The log formula and product rule are not exactly interchangeable on a finite mesh. In particular a mechanical wave pressure can survive in Newtonian units without modifying the gravitational force law.

There is a separate native mechanical calculation: its radial finite-element operator uses the reduced amplitude A=r(√n−1) and supplies −stiffness(A)/(2 M² lump × r√n). We evaluate the actual native wave-on minus wave-off phase-rate operation, as well as this explicit term. For a compact scalar weight W the corresponding continuum weak calculation on its finite-element reconstruction is −∫ A′[W/(r+A)]′ dr/(2M²); replacing W by −W′ measures the aperture mean of the radial potential gradient. Use the two named aperture widths at fixed launch coordinate, normalize by ∫W dr and split elements at support boundaries. This is a material-source check, not a tidal detector measurement. The three q values, two near-field mesh spacings, two independent integration orders and native lumped-versus-weak discrepancy are all reported. Nothing here equates the monopole source itself with a universal force or a galaxy occupation.
