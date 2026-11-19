# Final scope: usable population transport without a fictitious halo gap

Read this together with DERIVATION.md, RESULTS.md and ZERO-GAP-AND-SMOOTH-READOUT.md.

## The physical correction to the first formulation

A Newtonian finite-mass potential has weakly bound states accumulating at escape.
A finite-box eigenvalue spacing is not a physical gap between the whole halo
and the unbound continuum. The separated-projector bound is consequently a
deep-subspace result, not a uniform all-halo formation bound.

We do not patch this by choosing a new particle mass or an artificial wall.
The parent now supplies three distinct readouts:
- exact number-in-aperture transport through the physical boundary flux;
- bound-subspace occupation where the spectral definition and its derivative are valid;
- a smooth escape-energy-weighted count with a gap-free derivative bound.

## Gap-free derivative bound and its validation

For a fixed resolution sigma>0,

    W_sigma=1/2-arctan[(H-E_esc)/sigma]/pi,
    N_sigma=Tr(W_sigma Gamma),
    |N_sigma_dot| <= N ||H_dot-E_esc_dot I||/(pi sigma).

This assumes positive trace-class Gamma and a bounded operator variation, or
the stated finite regulator with a controlled continuum limit. It is an
observable with declared energy resolution, not a new particle distribution
or a sharp bound mass. If sigma varies, its derivative term must also be
included; current code and proof keep it fixed.

The threshold-crossing control gives N_sigma=.5 and derivative
-1.5915494309189535 at sigma=.2, saturating the predicted bound. It remains
regular where the sharp projector correctly refuses differentiation.
All222 additional checks pass, including noncommuting matrix variations,
complete degeneracy, unit changes and moving escape reference. Maximum
finite-difference derivative discrepancy is3.218390731088559e-8, below the
unchanged2e-5 gate. These222 supplement the333 unit-safe checks; the original
308 are already included in333 and are not added again.

## How the resolved count brackets a sharp count

Let P_B=1_(H<E_esc), and let P_near select |H-E_esc|<=epsilon for epsilon>0.
For each spectral energy outside this band,

    |w_sigma(E)-1_(E<E_esc)|
        = arctan(sigma/|E-E_esc|)/pi
        <= min(1/2, sigma/(pi epsilon)).

Inside the band the error is at most1/2, including the value exactly at
escape. Spectral calculus and positivity of Gamma therefore give

    N_near=Tr(P_near Gamma),
    |N_sigma-N_B|
       <= N_near/2
          + min(1/2,sigma/(pi epsilon)) (N-N_near).

No commutation of Gamma with H is required: positivity and the operator
inequality suffice under the trace. This connects the smooth readout to
the desired sharp count through a computed near-threshold population.
It does not assume that this population is small.

For finite total occupation, as sigma approaches zero, the readout approaches
N_B plus half the occupation exactly at threshold. If there is no threshold
atom, it approaches N_B. The derivative bound diverges as sigma shrinks, so
one cannot silently exchange this limit with a uniform formation-rate claim.

## Resulting next calculation

The remaining parent input is a source-complete physical initial state and
formation/environmental evolution, not a newly adjustable force coefficient.
The saved early real-field, correlated and gauge data should be mapped into
that input without deleting pairing, imposing thermal phases or extrapolating
an uncomputed k band. A declared global primordial preparation can be an
empirical input shared across galaxies; fitting local normalization to Vobs
is not part of this route.

The galaxy side can choose a physically meaningful aperture or a declared
escape-energy readout once its geometry/environment is specified. The
isolated stationary solver remains valuable for testing the resulting state,
but it cannot retrospectively select its population.

Use energy_units.py for dimensional projector calculations, smooth_escape.py
for the weighted readout, and the original covariance/stress owners for
physical evolution. No new galaxy fit, data selection, source bank, parent
action or published claim was made in this stage.
