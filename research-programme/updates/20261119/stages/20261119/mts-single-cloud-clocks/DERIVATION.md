# One initial state, not a transition between two prepared clouds

Use the inherited synchronous comoving radial metric −dτ²+A dr²+R² dΩ², C=(R/r)². The dust initially has zero radial velocity; its conserved number per coordinate radius is proportional to b(r)r², where b=f b_original. No mass, charge, energy or impulse is supplied at a later time. The scalar amplitude is √z H; z is a supplied occupation normalization, not obtained from the dust. Its initial normal derivative vanishes. The four states are (0,0), (b,0), (0,z), (b,z); every signal here uses common comoving clock labels, not four clocks at the same later areal radius.

## A sign that can be predicted before evolution

Write M_b, M_s and M_t for ordinary, scalar-only and combined enclosed mass on the initial R=r slice. Set F_i=1−2M_i/r. The retained constraint gives
```
M_b' = r² b √F_b
M_s' = z r² (H² + F_s H'²)/2
M_t' = r² b √F_t + z r² (H² + F_t H'²)/2.
```
Define h=M_t−M_b−M_s. Rationalize the square-root difference; then **exactly**, without assuming that z or b is small,
```
D = 2 r b/(√F_t + √F_b),   E = z r H'²
h' + (D+E)h = −D M_s − E M_b,    h(0)=0.
```
The integrating factor is positive. For nonnegative b,z and regular untrapped data, h≤0 at every radius. It is strictly negative after either positive overlap has accumulated. A constant-field mass term cancels explicitly from the difference but still gravitates through M_s. The two negative integrals with common factor separate the proper-volume change at fixed baryon count from the change in scalar gradient energy. This is a binding effect of the retained common metric, not a new attractive force parameter. The result concerns this initial slice and does **not** fix the sign of a clock signal or an evolved mass difference. An independent adaptive radial solver integrates the two terms separately and checks both the original launch constraint and source-mass scaling.

**A local physical consequence.** On this initially resting slice the areal acceleration of a freely falling shell obeys R̈/r=−M/r³−p_r, with R̈ the second derivative in its proper time. The statement also applies to a freely falling test shell in the no-dust corners. At fixed shell label the mixed radial pressure is −z(M_t−M_s)H'²/r. Moreover v=M_t−M_s obeys v'+Ev=r²b√F_t, v(0)=0, hence v≥0. These give the signed prediction

    mixed(R̈/r) = −h/r³ + z v H'²/r ≥ 0.

Both terms have the same sign. Relative to simply adding the two separately gravitating sources, the combined shell accelerates less inward (or more outward). This is an interaction difference, not net repulsion or a reversal of the ordinary inverse-square law. It uses areal radius and shell proper time; distant clock signs need not match it. A separate radial solve predicts both terms and is tested against the actual finite Einstein evolution's angular acceleration, at three baryon normalizations with no amplitude adjustment. Neither sign theorem is justified for a general moving, charged or nonspherical slice by this argument.

## Dust and scalar histories

In the scalar-free control the enclosed mass of a comoving shell is constant. With R(0,r)=r and Ṙ(0,r)=0 the dust equations have R̈=−M_b/R² and A=R'²/F_b. Write U=M_b/r³ and R/r=y(Uτ²). Substituting the power series in the acceleration law gives a₀=1 and aₙ₊₁=−[qⁿ]y⁻²/[(2n+2)(2n+1)]. At fixed τ the radial derivative is R'=y+τ² y'(b√F_b−3U). The predictor evaluates this ordinary metric and its extrinsic curvature at **each** Runge–Kutta stage, including its time dependence. Scalar and mixed metric responses are then computed to first order in z; b is finite. The target instead evolves all four finite states in conservative variables, including charge and impulse zeros. Baryon count is exactly constant. The initial scalar generally evolves even without dust: subtracting its entire separate clock signal, not just the Minkowski reference, matters.

For the normalized scalar field let L=√A and write K for the trace of extrinsic curvature. Its physical equation is Ḧ=Δ_g H−H+KḢ. For a mechanism diagnostic only, replace this operator on the normalized field by its flat or initial-dust-metric counterpart. Keep the first-order stress contraction, metric response, matter time dependence and clocks in all three runs. The flat-history piece includes the gravitational interaction of an independently evolving scalar with ordinary matter and the ray; it is not a static potential. Static minus flat isolates the initial dust curvature **in this operator**. Physical minus static isolates its subsequent time dependence. The pieces telescope but only the physical model is required to satisfy the full field equations. Their sum is not three independent measurements.

## Clocks and flux

For each readout Y, the mixed signal is Y(b,z)−Y(b,0)−Y(0,z)+Y(0,0). Subtract its value at the first emitted pulse to remove a constant offset; that first pulse already traverses the link. The frequency ratio is also tested independently against 1/(dτ_arr/dτ_emit), including the reflection. Compute the small mixed components directly, not by subtraction of four rounded large clocks.

On a comoving sphere, define j=−z Π H'/L, p_r=z(Π²+H'²/A−H²)/2. The Einstein mass balance and independent geometric mass are
```
Ṁ = −R² (p_r Ṙ + j R'/L)
M_geom = R/2 [1 + Ṙ² − (R'/L)²].
```
Positive j is outward; a decrease in M can be energy leaving the sphere, not a conservation failure. Pressure work and transport are integrated separately in proper time. The geometric check uses the spatial derivative of C and the time derivative of R, not the evolved mass. The checks at r=2,5,6.5 stay away from the numerical outer edge over the full duration. Exterior neutral dust is vacuum and its mass constant; for the scalar, do not call M(r=12) ADM or assume a zero boundary flux. The initial negative-binding result extends to the asymptotic mass if a regular asymptotically flat finite-mass extension is independently supplied.

## A receiver-calendar diagnostic, not a pulsar fit

For one-way light, delay at a common receiver time solves d_rec=D(t_arr−0.5−d_rec) on each corner. Reversion uses the mixed algebra including cross terms from the ordinary and scalar-only time shifts. This is different from comparing identical emission labels. Sample the resulting waveform on the retained J1713+0747 EPTA DR2full calendar in three placements wholly inside the simulation. Project out a quadratic spin trend, annual/semiannual sinusoids and instrument offsets with equal-day weights. No timing residuals, pulsar distances, noise likelihood or independently inferred source occupation enter; this is the response to actual sampling, not a pulsar constraint.
