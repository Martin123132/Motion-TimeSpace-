# From preparation energy to a finite clock signal

**What the input means.** Hold the ordinary baryon and charge distributions fixed. On the time-symmetric quiet slice let F=1−2m₀(r)/r. For the initial change v=εu+c(ε)w in the real scalar field (zero initial normal momentum) define the positive, rest-frame excitation norm

    E = (1/2) ∫ r² dr / √F [F(v')²+v²]  = (1/2) (ε,c) G (ε,c)ᵀ.

Here u is the previously held two-mode pulse and w the compact compensating shell; G is the two-profile Gram matrix in this expression. These are mass units of the simulation (4πG_N=c_light=m_scalar=1). The factor converting this integral to joules is c_light⁴ L/G_N; the sphere's 4π multiplies the proper volume and cancels the 4π in the source normalization. No factor of 4π multiplies it a second time. E is defined using the *same* quiet slice for both signs; it is not the difference in ADM mass, a luminosity, a binding energy, or an astronomical measurement.

**Mass matching.** For N, c=0. For M, set m(3;ε,c)−m₀(3)=0 with the regular full nonlinear radial mass constraint. The fields outside the pulse are unchanged initially and the exterior difference obeys a homogeneous equation, so the same boundary condition fixes the asymptotic mass change to zero. In particular M can have nonzero positive excitation norm at zero net mass change. At any finite event let F_e=1−2m_e/r, h_e=h₀+v. For an arbitrary profile g the directional launch derivative obeys

    δm_g' + r[b/√F_e+(h_e')²]δm_g = r²(F_e h_e' g'+h_e g),    δm_g(0)=0.
    c' = −δm_u(3)/δm_w(3),   ∂εm = δm_u+c'δm_w                  (M only).

This determines the *physical preparation derivative*, not a freely chosen correction to a clock after seeing its result. G is positive definite for the two saved profiles. The two roots E(ε)=E_* with opposite signs must be computed separately on the local branch. The Gram form and direct energy integration give independent numerical checks. Equal energy specifies neither sign nor profile.

**Finite stress, not just a tangent.** If B is the symmetric polarization of the scalar stress, T[h+v]−T[h]=B(h,v)+T[v], with B(f,f)=2T[f]. To first order in gravitational reaction to scalar stress, the metric/material response and the first clock variation about ordinary GR are linear operators on this source. Hence the complete finite leading clock curve is

    ε B_clock(h,u) + c B_clock(h,w) + ε² S_clock(u) + ε c B_clock(u,w) + c² S_clock(w).

The five shapes are calculated from propagating the indicated fields on the ordinary geometry, solving the linearized Einstein–Maxwell, matter and mass constraints and integrating the light and clock kernels. They do not use a measured clock curve or a waveform-dependent coefficient. Freezing c to its first variation loses terms of the same order as pulse self-energy. At higher stress order the geometry also affects all of these propagating fields and the clock path.

**Full feedback without differencing two nearly equal clocks in the prediction.** Let O(ε) be a one-way or echo observable on the prepared family. At each chosen amplitude solve the charge, material, scalar and metric equations and their linearized equations for ∂ε, initialized with the derivative above. A complex directional increment applies the chain rule to the independent ordinary-plus-scalar formulation at physical stress weight 1. The incoming scalar seed is not a perturbation in the coupling. Integrate the proper-time and frequency variations along the outgoing and returned photons, including perturbed reflection time. Then, before using any target signals,

    O(ε) − O(0) = ∫₀^ε [∂a O(a)] da.

Here the integration coordinate a is the *source parameter*, not cosmic scale factor. On a bounded interval, integrate the degree-six interpolant of seven computed derivatives exactly in a, and compare with a five-node subrule. No observed end value, measured clock curve or fitted dynamics enters the prediction. The quadrature refinement is an error diagnostic, not an absolute proof of absence of aliasing. The finite target uses the parent's different Einstein–Maxwell–scalar evolution with real initial fields, not this quadrature.

**Why the answer can depend on sign at fixed energy.** Write c=aε+bε²+… and p=u+aw. Set H=〈p,p〉, J=b〈p,w〉 in the quiet Gram metric. Then E=Hε²/2+Jε³+…, so with d=√(2E/H) the two roots are ε_±=±d−(J/H)d²+O(d³). For O(ε)−O(0)=Uε+Vε²+…, the half-difference of the two energy-matched waveforms is U d+O(d³), and the half-sum is (V−UJ/H)d²+O(d⁴) on a smooth branch. This is why an energy-calibrated odd waveform starts at √E, not E, and why sign-even stress and nonlinear preparation cannot be discarded. A fixed-energy source still needs its coherent phase relative to the quiet scalar background.
