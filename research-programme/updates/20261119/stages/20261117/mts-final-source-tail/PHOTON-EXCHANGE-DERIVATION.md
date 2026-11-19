# Photon/baryon momentum-exchange bridge from retained fields

Sources: previous_directory/native/fortran/mts_metric_hook.inc (opacity and species momentum terms), mts_response_hook.inc (represented RECFAST branch), and the previously verified native state/slip extraction. No physical evolution, tolerance or fit changes.

In the retained normalization B_gamma=kappa_grav a^2 rho_gamma has units Mpc^-2, opacity chi has units Mpc^-1, and s=v_b-3q_gamma/4 is dimensionless. The implemented Thomson drag is
    J=(4/3) B_gamma chi s.
It enters baryon/photon momentum balance with opposite signs. Cross section and gravitational normalization remain retained inputs, not newly derived MTS constants.

On the represented fixed-ionization RECFAST branch, B_gamma scales as a^-2 and chi=chi0(a0/a)^2. Therefore A=(4/3)B_gamma chi scales as a^-4. The native response hook restricts the branch to3500<zscale<5000; this is NOT a universal recombination law.

Let d=delta_a/a0 and lambda=(1+d)^-4. The exact finite coherent-minus-original exchange is
    delta_J=A0[lambda delta_s+(lambda-1)s0].
All delta_a*delta_s terms are retained. Evaluate
    lambda-1=-d(4+6d+4d^2+d^3)/(1+d)^4
without subtracting near-unity coefficients. Use the saved background and velocity increments rather than subtracting rounded histories.

Independently extract drag from actual saved native species derivatives:
    J_b=-Q_b'-(H+r)Q_b+k T_b,
    J_gamma=Q_gamma'+2r Q_gamma-k(T_gamma-2Pi_gamma/3).
Here r is the old scale interpolation rate and equals H in the coherent branch. These expressions remove explicit expansion contacts, not a fitted residual. Check both against J and against each other at the unchanged algebra tolerance on physical primitive scales. Check finite delta_J against the actual photon RHS difference, background reconstruction and a^-4 scaling.

Seven rational d values give14 exact Fraction algebra controls. Apply identical reconstruction and32/64 comparisons to baseline and MTS parent/approximation; report tiny baseline precision honestly. Conserved internal momentum exchange does NOT itself prove heating, Compton energy redistribution or final spectral distortion. Those require the retained energy collision kernels; this provides their sourced momentum input without an extra empirical coupling.
