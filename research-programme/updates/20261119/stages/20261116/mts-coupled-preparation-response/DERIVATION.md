# Live matter/preparation response on the tested common background

This stage uses one complete native perturbation state at the common
earliest preparation time, not the source projections alone. The existing
native species equations remain the owner. No new free coupling is added.

## Preparation and surrounding state

All active CDM, baryon, photon/polarization, neutrino and scalar variables
are captured with the unchanged native934-epoch reference. The disabled
new hook must reproduce the original934 diagnostic packets byte-for-byte.
The native state includes the metric variable eta_k. The same full state
and background are matched once at the earliest saved time. Corrected
states at the902 later preparation nodes follow by evolution; their
corrections are NOT independently reset to zero.

For native linear perturbation operator A on background B,
evolve U'=A(B)U and

    delta U'=A(B_star)delta U+[A(B_star)-A(B)]U.

This retains the surroundings and metric response rather than holding
their projected sources fixed. Native active-state/regime checks must pass.
The original quadrature preparation weights are unchanged.

The exact nonlinear background defect-response from the previous stage
is evolved simultaneously, in its tighter numerical coordinates. No new
background interpolating table is made. The original saved interpolation
boundaries split the calculation, with unchanged32/64 physical max steps,
original query grid,rtol1e-10 and normalized atol1e-12. Perturbation-difference
units are1e-5 of the native state units: this tightens absolute precision,
not acceptance. Original algebra1e-10/numerical2e-5 gates remain.

## Thermodynamics, not a zero-response assumption

The retained RECFAST branch at3500<z_scale<5000 explicitly sets
x_e=1+fHe and T_m=T_CMB/a. The native signatures and sampled temperatures
must confirm this branch throughout the small window. Thus the same-order
relative changes are cs2_star/cs2=a/a_star and
opacity_star/opacity=(a/a_star)^2. The existing baryon sound-speed
convention is retained; no new effective gamma is inserted. Exact
background reparameterization must reduce to the native operator when
the correction is zero. The thermo spline's existing approximation is
not silently reinterpreted as a recombination calculation outside this branch.

## Source and work identities

For a scalar, D=v w+M b u,Q=k v u,P=v w-M b u,Y=a(D,Q,P)/R0.
Use stable exact product differences in a,b,v,u,w, including all cross
terms, to resolve the small response without subtracting large sources.

For a coherent background,

    Y_D'=-3H Y_P-k Y_Q-k(a/R0)v^2 z,
    Y_Q'=-H Y_Q+k Y_P,
    z=[(D+D_o)/(2k)+eta_k]/H.

Split the last density-work term into own density, surroundings and
metric eta. For the represented old background include its explicit
Euler contacts

    C_D=(r-H)(2Y_D-Y_P)+(a/R0)[f_v w+M f_b u],
    C_Q=(r-H)Y_Q+(a/R0)k f_v u,

where f_b=b'-v and f_v=v'+2Hv+Mb. The corrected background removes these
contacts by its equations, not by deleting terms from the old balance.

For cold matter Y_D=C delta_c and Y_D'=-k C z, with current/pressure zero.
Its bare density, surroundings and metric still change.

Integrate old and difference work alongside the equations, then compare
with independently formed endpoint source increments on the original
signed preparation. Test the response on its own scale as well as the
saved physical source scale. Retain failed tiny baseline-relative tests.

The exchange certificate is for the selected subsystem with its live
surroundings and approximation contacts, not a new all-species quantum
stress theorem. Quantum measure remains separate. No publication or
goal resumption is part of this manual step.

