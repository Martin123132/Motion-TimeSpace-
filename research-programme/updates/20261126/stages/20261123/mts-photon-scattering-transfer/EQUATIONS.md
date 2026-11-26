# What was transported

The two launch coordinates are exactly the previous stage's complex normal-frame fractional photon energy D and normalized longitudinal covector current J, at equal scale factor a=5.792196445707299e-5. They include that parent's quadratic readout at launch. After this point we ask a linear response question: what part of these **two** coordinates reaches the recombination plasma, with no new metric or second-order source? This is not a new solution for the full cosmological perturbation. It does not identify all the other degrees of freedom at launch with zero.

In the phase and momentum convention of the retained regular_flow.py, put U=4 v_b/3, R=3 rho_b/(4 rho_gamma), Hc=aH, and let O be the positive Thomson scattering rate per conformal Mpc. Dropping new external drives gives

    D' = -k J
    J' = k(D-2 I2)/3 - O(J-U)
    U' = -Hc U + O(J-U)/R

A prime is a conformal-time derivative. Pressureless baryon momentum is the same approximation as in the retained parent short-window equations. For intensity and E-polarization moments X_l with l>=2,

    X_l' = k[l X_(l-1)/(2l+1) - c_l X_(l+1)] - O X_l
           + [l=2] O (I2/10 + 3 E2/5).

Here I1=J, E1=0; c_l=(l+1)/(2l+1) for intensity and (l+3)(l-1)/[(l+1)(2l+1)] for E. The first omitted moment is set to zero, then the truncation is tested by enlargement. Apply the transfer to the full complex pair, not to its magnitudes. Scattering alone conserves D and J+R U at fixed background and erases slip at rate O(1+1/R). Thus initially pure photon current shares momentum with baryons; it does **not** disappear exponentially with the single-photon optical depth. At zero optical depth and zero gravity, an isotropic monochromatic Fourier perturbation gives D=j0(k delta_eta), J=j1(k delta_eta); this independent analytic check also fixes the sign and scale of J. The solver verifies both analytic limits.

The tagged photon-only response has no initial velocity increment in the baryons (U=0), intensity or polarization multipoles l>=2. A separate control uses U=J at launch. Other preexisting baryon velocities, multipoles, potentials or later perturbations would have their own additive responses in the linear problem. They are not implicitly added; there is no late refit. Five original k values, both original launch amplitudes per probe and their branch assignments are inherited.

With T_H, T_C the two transfer matrices and X_H, X_C the launch vectors, the signed difference is exactly

    (T_H+T_C)(X_H-X_C)/2 + (T_H-T_C)(X_H+X_C)/2.

The first term transports the initial difference; the second isolates changes in transfer through the medium. Their **vectors** add, not their norms. The saved histories also separate the signal sourced by initial energy and initial current. Ratios quoted in the report are amplitudes: the root mean square of the joint complex energy/current difference, weighted by cold visibility d eta across 750<=z<=1500, divided by the corresponding joint launch norm. Point values are evaluated at the same scale for both branches. They are not sky C_l's or an inference about detectability.

Numerics: evaluate native conformal time, expansion, baryon loading, positive opacity and visibility at common scale factors. Integrate the rate matrix in scale factor with d eta/da from the native clock, two-stage implicit Radau IIA (order 3). Test angular depth, time resolution, background sampling and output interpolation separately, including the *difference* of the two models. See READOUT-CHECK.md for the early native visibility floor; it was not used to infer a surviving signal.
