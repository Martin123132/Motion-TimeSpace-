# What one can disentangle without an absorption calibration

Supplement to the prospectively frozen thermal forecasts, not a second blinded experiment. Use a **common total-wavenumber band** for all radial sightlines at fixed redshift, here [7.052308883999711,37] Mpc⁻¹ at z=4.2. Below the largest radial wavenumber this is only part of the ordinary one-dimensional survey power. Different lower limits would invalidate the following shared-coefficient identity.

Set x=(k_parallel/k_ref)², k_ref equal to the largest radial wavenumber. The model has thermal d=d_ref x, B0=2−0.7(γ−1), p=B0 D, v=(k_ref/k)² U, η=(γ−1)d_ref/B0, and q=v−ηp. Thus the signed response at fixed k is exactly p+xq. With inner product weighted by primordial dimensionless power divided by k and integrated in d ln k, the common-band power at **every** radial bin is

    P(x)=π ℋ c A² exp(−2 d_ref x) [ I0+2x I1+x² I2 ],
    I0=<p,p>, I1=<p,q>, I2=<q,q>.

The factorization is a consequence of the retained linear thermal readout and velocity projection. No coefficients are inferred from flux data. The Gram determinant is nonnegative and the normalized value

    J = I2/I0 − (I1/I0)² = <v−c p,v−c p>/I0,   c=<p,v>/I0,

is unchanged by adding any constant times p to v. In particular the readout shear −ηp cancels **exactly**, and an overall power normalization cancels. A change in J due to heating is dynamical (at fixed background and γ); setting the velocity to a constant times p gives J=0. Reconstructing J from raw damped measured powers would still require separating the broadening and unmeasured modes. J is a diagnostic of transfer shapes, not a new conserved charge.

A different statistic requires no assumed broadening width: take the three highest radial bins, with squared ratios x1<x2<x3, and form Q=ln P(x2)−[(x3−x2)ln P(x1)+(x2−x1)ln P(x3)]/(x3−x1). This removes any constant plus linear function of x from log power, cancelling both a common opacity normalization and a Gaussian damping prefactor exactly. Unlike J, Q retains the readout shear as well as the dynamical temperature response. Compare both diagnostics; do not identify a cancellation of a single three-dimensional mode with a null in observed line-of-sight power. Independent, arbitrary noise, temperature histories, or per-bin calibration are not projected out.

Numerical implementation: interpolate D and U separately on log k, integrate their products on the same positive Gauss rule on every knot interval, compare with evaluating the squared *signed sum* directly, repeat with fewer knots and a second interpolation rule. The zero residual of the polynomial identity tests algebra; the sampling differences test the actual numerical information.
