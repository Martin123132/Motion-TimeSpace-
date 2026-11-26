> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# A real carrier on the previously tested LMC wave distribution

This is an optical follow-through on the fixed-number density/force calculation (not bundled here), not a change to that calculation. The two original grounds and six orbit alternatives are retained; the orbits are not independent data. At Galactocentric cylindrical radius 8.3 kpc we retain exactly the north axial ray and the three fixed-affine screens of the previous optical test (not bundled here). Its induced convergence is the difference relative to the same ground without the LMC-driven wave. We work at first order in that wave and first order in gravitational focusing, in the saved origin-subtracted potential convention. No fit or chosen phase.

## Reinstating the suppressed phase

Let g be the real stationary wave, N its squared mass-weighted norm, H g=0, B the gravitational coupling and L the positive radial Poisson operator. The driven perturbation is x+i(y+θg); x and y are the archived vectors orthogonal to g. The number perturbation 2〈g,x〉 vanishes; this condition does **not** imply θ=0. Project the unreduced imaginary-part evolution along g. Using Lw=−2B†x gives

    θ′ = [2〈B†g,L⁻¹B†x〉−〈g,Vg〉]/N.

Choose the same initial coherent phase for the driven and undriven preparations, θ(initial)=0. An absolute phase remains arbitrary. In each saved mode, c″+σ²c=−F with zero initial displacement and velocity, so ∫c=−(∫F+c′_end)/σ². The phase follows by one reciprocal Poisson solve per ground and time integration of the original radial drive. Five-point Boole weights integrate each degree-four force interpolant without replaying or sampling the orbit on a new grid. The present drive is independently compared to the archived modal forcing. The endpoint and retarded envelope share the same final polynomial panel; all event times used here are in the past.

## Contracting the real-field stress before averaging

Use native spatial length L₀, speed V₀, time τ in L₀/V₀, ε=V₀/c and the saved bound energy E in V₀². The native rest frequency is ε⁻² with this Schrödinger–Poisson scaling. Put ν=1+ε²E. In the stationary rotating frame let the envelope be u and the real scalar be proportional to Re[u exp(−i(ε⁻²+E)τ)]. On this north past cone τ=τₒ−εz. Squaring the null derivative gives, normalized to the earlier cycle-averaged mass source,

    A[u] = iνu + ε∂z u − ε²∂τ u
    Tkk = |A|² + Re{ A² exp[iφ −2i(ε⁻²+E)τₒ +2iνz/ε] }.

This uses the canonical real quadratic field: the trace term drops out when contracted twice with a null vector. A complex slow wave alone is not the entire instantaneous stress. The [real-scalar effective-envelope construction](https://arxiv.org/abs/1712.00445) provides context for the distinction. [Khmelnitsky & Rubakov](https://arxiv.org/abs/1309.5888) give an example of a double-frequency metric signal; their pulsar timing amplitude is **not** substituted for this screen-area observable.

With A₀=A[g], q=x+iy in physical spatial coordinates, the restored first variation is dA=A[q]+iθA₀−iε²θ′g. For the slow signal use 2 Re(A₀* dA); for the induced carrier use 2A₀ dA. The unperturbed carrier has coefficient A₀² and must be included for a measurement of total focusing. Omitting θ is provided only as a sensitivity control. Exponentiating just the uniform phase, while keeping the shape variation linear, is a second control, not a full nonlinear solution.

Each physical envelope is evaluated as Σ u_l(r) sqrt(2l+1) P_l(z/r)/r from the saved finite elements and the saved canonical displacement/momentum lifts. Differentiate the radial interpolant, 1/r and the angular harmonics at fixed τ before adding the known time derivative. The shell weight W=z min(z−20/L₀,50/L₀−z)/(15/L₀) is supported on 20/L₀ to 50/L₀; it cancels every common near-foreground slice at the same past event. It does not cancel the ground *inside the shell*. Multiply by ε². Use the pointwise field product here, not the old density/current product truncated again in angular order. The old versus new slow-drift column measures their net difference, including derivative-stress terms; it is not attributed solely to either.

## Numerical and observation windows

Split exactly at the tent kink and each crossed radial element. On each smooth interval of midpoint m and halfwidth h, expand the slow envelope times W in Legendre polynomials. Mode j has exact plane-wave moment 2h exp(ikm) i^j j_j(kh), k=2ν/ε. Endpoint terms are included. Check against the analytic transform of the entire piecewise-quadratic tent. Compare order 10 with order 14 on bisected panels, then use the latter on the independent enriched 64-mode basis versus the enriched 100 basis. Keep the 20-ppm threshold unchanged, including misses. The comparison is not an error theorem for untested wave modes.

Both exposures last one Julian year and their centers are 20 years apart. They lie entirely in the last 21 years. Evaluate the actual retarded envelope at five reception times. Use endpoints and midpoint for a quadratic and withhold the two quarter times; the interpolation check is empirical, not a supremum bound. Integrate over each exposure with 12-point Gauss quadrature including the carrier. For a frozen slowly varying stress coefficient C₀, the same one-year average multiplies it by sinc(Ω/2), **not zero**, where Ω=2(ε⁻²+E) in radians per Julian year after unit conversion. The stored matched-frozen control freezes the entire shell coefficient at today's value, leaving the carrier running.

Let D be the difference of these exposure averages divided by 20 years. With unknown but common absolute phase the induced slope lies exactly in [Dslow−|Dcarrier|, Dslow+|Dcarrier|] in the tested coherent model; no phase is selected. If phases of driven and control are independent the amplitude bound is |Dtotal|+|Dground| instead. An incoherent, number-diagonal *mean* has no double carrier; this does not establish its sample variance. A classical mixture with common coherence fraction f multiplies the coherent term by f. No value of f is inferred from the force bands.

As a control use four equally spaced one-year exposures spanning the same endpoints, with spacing d=20/3 years and c=cos(Ωd). The weights (−1,1+2c,−1−2c,1)/[2d(1−c)] annihilate a constant and a pure tone at Ω at any phase and reproduce the slope of a linear trend. Finite exposure common to the four times preserves this cancellation. Apply to evolving phasors as well; the residual need not be zero. The quoted noise penalty assumes independent equal-variance exposure errors. The notch is tuned to the **specified** pole and ground energy, not a claimed insensitivity to mass errors, broad frequency spectra, independent domain phases or unsynchronized sightlines.

All calculations use the same flat Born path in the weak field. Proper-clock calibration, source distances, motions, path-induced carrier-phase corrections, a Galactic phase/coherence preparation and other on-sky signals have not been inferred. A GR comparison with the very same real scalar and occupation gives the same metric term. The seven full-delay basis misses in the preceding stage are unchanged; this test concerns a different observable.
