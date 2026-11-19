# Derived difference for the metric time-shift coordinate

The first saved-packet calculation identifies the native alpha coordinate as a large signed contributor to several weak-output integrals. This alpha is the metric time-shift state, not the fine-structure constant or a fitted MTS coupling.

The authoritative retained PoissonDriver.evaluate sets alpha_rate=Psi-H alpha, then divides by H to return d/dN. With the unchanged unit U_alpha and the SAME encoded native vector x on both backgrounds,

    r_alpha,b=Psi_b/(H_b U_alpha)-x_alpha.
    Delta r_alpha=[u_bar Delta Psi+Psi_bar Delta u]/U_alpha,
    u_b=1/H_b,
    Delta u=-(H_ref-H_ret)/(H_ref H_ret).

The common -x_alpha term cancels identically. This applies to both GR and spatial-Poisson branches because they both use the same alpha equation, with their own Psi. The calculation checks the individual native rates against that equation before using the difference. We do not assume H_ref=H_ret or Psi_ref=Psi_ret.

The test evaluates the identity as exact rational arithmetic on the SAVED binary64 potentials, H values and units. It therefore removes representation loss between those saved inputs and this one rate difference, but does not recover errors already present in Psi/H, certify the whole native operator, or alter the original bank. The resulting alpha-only correction is contracted with the saved-point dual covector and integrated through the same quadrature/terminal adjoint. All other native coordinates are kept unchanged. The original source and its flags remain immutable; this is a distinct diagnostic candidate.

The native source path is mts-independent-poisson-evolution-20261107/poisson_driver.py (relative to post-checkpoint-work); the wave-specific wrapper mts-cold-adapted-metric-gain-20261107/poisson_driver.py imports that class without replacing evaluate. Both sources are hashed into this test's evidence.
