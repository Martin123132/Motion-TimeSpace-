# Spatial measure: retain both density and canonical number coordinates

The frozen late export's `heavy_relative_NR_real=delta_N/2` is a flat-measure
hydrodynamic amplitude coordinate, not the complete metric-correct canonical
number amplitude. This distinction matters when passing a state to a wave
solver with norm integral |A|^2 d^3x. The raw and derived packets remain unchanged.

For the leading positive-frequency, nonrelativistic interpretation, let n be
the proper number density. On a Newtonian-gauge slice, the invariant count is

    N = integral sqrt(gamma) n (-normal_mu u^mu) d^3x.

Here sqrt(gamma)=a^3(1-3Phi) at first order; the relative Lorentz factor is
1+O(v_pec^2). With rho=m n at leading NR order, this gives

    |A_coord|^2/nbar_com = 1 + delta_N - 3Phi,
    delta A_coord/Abar = (delta_N-3Phi)/2 + i S,
    S = -am theta_N/k^2.

The density-only coordinate therefore misses a term -3Phi in coordinate
number density. Apply the same spatial-volume map to the cold control:
delta_N,cold-3Phi_cold. No quantum phase is assigned to classical cold matter.
The lapse does not enter this instantaneous hypersurface measure; it enters
the evolution. Physical density is recovered by adding 3Phi, not by treating
coordinate density as an extra gravitating source.

This map is linear, conditional on the leading NR number interpretation, and
does not make the exact real scalar's number an exact relativistic conserved
charge. The retained slow field and all raw metric/stress outputs remain
necessary for more accurate matching. In particular a flat-space quantum
pressure formula applied to delta_N-3Phi alone would not reproduce the retained
stress: metric-gradient and relativistic terms must also be transformed.

`volume-state.npz` adds this explicitly labelled coordinate-number interface
without replacing any late source. Its canonical-amplitude covariance is the
same primordial power times outer(((delta_N-3Phi)/2,S),((delta_N-3Phi)/2,S)).
All inverse and covariance checks retain 1e-10. No random realization, local
population, nonlinear metric completion or new dynamics is manufactured.

The large full-band spatial-phase variance also forbids replacing exp(iS)
by 1+iS indiscriminately in a later wave realization. A large nearly uniform
phase is not itself a large velocity; that later construction must inspect
phase differences/gradients and preserve normalization and the metric measure.
