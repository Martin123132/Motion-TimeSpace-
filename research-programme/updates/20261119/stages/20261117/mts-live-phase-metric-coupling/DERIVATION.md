# Stable old/change coordinates with live gravity

The previous regular transformation is U=T x, x=(f,g),

    T=beta [[mu^2 Phi+kappa V, V+kappa Phi],
            [mu V,          -mu Phi   ]],
    kappa=3Hs/2, s=4mu^2/(4mu^2+k^2).

It maps exactly to matched density and relative Wronskian. The inverse denominator
is E+2kappa Phi V; the previous positivity condition is enforced at every evaluation.
Here kappa is just this boundary coefficient, not Newton's gravitational constant.

Let branch0 be the retained original representation and branch1 the coherent
evolution. T1=T0+DeltaT and x1=x0+Deltax. Then EXACTLY

    U0=T0 x0,
    DeltaU=T1 Deltax+DeltaT x0,
    x0=T0^-1 U0,
    Deltax=T1^-1(DeltaU-DeltaT x0).

The differentiated pair is

    U0'=T0 x0'+T0' x0,
    DeltaU'=T1 Deltax'+DeltaT x0'+T1' Deltax+DeltaT' x0.

The retained full native old/change equations supply x0',Deltax' from the LIVE
metric and all species. The wrapper decodes both scalar coordinates before that
evaluation. Neither the pressure nor its derivative is supplied from future data.
These equations are the exact conjugation of the already derived phase-aware
generator; no auxiliary phase is frozen or averaged.

## Cancellation-preserving coefficient differences

Represent each coefficient by (old,change), not (old,new). For products,
Delta(ab)=a Delta b+Delta a b+Delta a Delta b; for reciprocals,
Delta(1/a)=-Delta a/[a(a+Delta a)]; for logarithms,
Delta(log a)=log1p(Delta a/a). Integer powers use these products.

The existing stable background correction supplies DeltaH. Compute actual T0'
from original spline jets and T1' from the coherent background ODE, retaining
the original contacts but NOT the previous replay's interpolation contacts.
H'=rho_total'/(6H) is differentiated from the retained Friedmann energy,
including the actual massive-neutrino background approximation. Its derivative
and difference are evaluated with the same factored arithmetic, not a silently
substituted perfect-fluid pressure expression. The chosen neutrino branch cannot
change unnoticed.

The logical input to DeltaT' is a pair of actual derivatives. At zero background
correction the matrices may coincide but their derivatives need not, because
the original representation can have nonzero interpolation contacts. It would
be wrong to force DeltaT'=0 in that case.

Native delta units and all remaining states are unchanged. Only the two old
heavy coordinates use the prior934 density-source unit, and their changes use
that unit times1e-5, mirroring the existing native old/change scaling. Full-source
tests keep their independently frozen original norms. The small observable
repair must pass its OWN precision check before any precision claim is extended
to it. Coordinate equivalence is not a new observational fit or new field law.
