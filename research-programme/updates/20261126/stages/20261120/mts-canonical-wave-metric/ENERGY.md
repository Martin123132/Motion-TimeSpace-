# Does the wave transport stress-energy, not just its conserved norm?

For a shell with fixed comoving faces define B=b³z, C=P/b³, δ=C−B and ω=am. The scalar charge-like bilinear is Re(B*C), with the product conjugate-linear in the first argument. The proper normal-frame scalar energy includes rest energy. In units of the homogeneous comoving rest-density coefficient, the **rest-subtracted shell energy** is exactly

    K = ∫ r² [ |δ|² + b² |∂r z|²/ω² ] dr / 2  ≥ 0.

This identity uses ½(|B|²+|C|²)−Re(B*C)=½|C−B|². Computing K as the difference of the two large integrated numbers would destroy its precision. For the lapse N, normal expansion h, and comoving volume, the energy balance of the scalar on a given metric is

    ∂η K = F_K(inner)−F_K(outer) + W_pressure + W_lapse
    F_K = r² N Im(δ* ∂r z)/(ω b)
    F_E = r² N Im(P* ∂r z)/(ω b⁴)
    W_lapse = −∫ (∂r log N) F_E dr
    W_pressure = −∫ a N h r² [ (3/2) (2 Re(B*δ)+|δ|²) − b² |∂r z|²/(2ω²) ] dr.

Here * denotes complex conjugation when multiplying, not convolution. The relation follows by integrating the normal-observer projection of ∇T=0, including both the changing spatial volume and the gradient of the lapse, and subtracting the independently conserved bilinear flux. In particular the lapse work involves the **full** energy current, not its tiny rest-subtracted remainder. These equations test this one minimally coupled matter sector; the homogeneous smooth remainder of the cosmological background is not a dynamically modeled fluid. The use of h from the momentum constraint also tests kinematic consistency of the reconstructed slices.

Why not test only charge? Squared-field rest contributions to charge can be large while the moving energy *above* rest is small. A budget normalized to rest mass can hide an incorrect pressure or force. Here the budget is normalized to the largest of the actual energy change, individual signed contributions and their net sum. The absolute residual and each signed term are saved as well. Passing the ordinary mass-current gate does not imply passing this stricter test.

**Removing temporal aliasing without filtering the wave.** Direct Simpson integration samples the paired current and pressure at endpoints and the predicted midpoint. A fast negative-frequency quadrature can interfere with the slowly evolving component: a quadratic work integrand has a mean plus a sinusoid near 2am even though the metric and charge barely vary. Step-halving by itself may sample different phases rather than resolve that sinusoid. In the separate phase-resolved diagnostic, the same frozen midpoint generator is decomposed into its positive component and its *dephased* negative component everywhere on the wave grid. Compute a quadratic W on each separately. Then C=W(+ plus −)−mean, S=W(+ plus i·−)−mean isolate the cosine and sine coefficients. Slowly varying coefficients are sampled at four Gauss points on each actual evolution step. Integrate their cubic interpolant against exp(2iωη) analytically by the Legendre/spherical-Bessel identity; the underlying wave is not averaged or damped in the evolution. The result is a work diagnostic on the step's midpoint geometry. The difference from endpoint K still tests spatial error, quadrature, freezing the geometry, and its time evolution. It is not made zero algebraically.
