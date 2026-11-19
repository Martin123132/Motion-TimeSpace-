# Regular phase-aware density variables

Retain the previous quadratic scalar and perturbation equations:

    Phi'=V+F, V'=-2HV-mu^2 Phi+G,
    f'=g, g'=-2Hg-(k^2+mu^2)f-kVz,
    beta=a/rho0, r=a'/a, mu=am>0, mu'=r mu.

D=Vg+mu^2 Phi f, P=Vg-mu^2 Phi f, Q=kVf and J=Vf+Phi g.
The preceding stage derived s=4mu^2/(4mu^2+k^2), c=1-s and
B=H beta s J/2. Set kappa=3Hs/2 and define two dimensionless weighted variables

    d_star=beta(D+kappa J)=d+3B,
    w=beta mu W, W=Vf-Phi g.

Using J itself as the second variable would fail when mu^2 Phi^2=V^2.
The DIFFERENCE W avoids that field-phase singularity. The transformation is

    [d_star] = beta [mu^2 Phi+kappa V, V+kappa Phi] [f],
    [w     ]       [mu V,             -mu Phi   ] [g].

Let E=V^2+mu^2 Phi^2 and Delta=E+2kappa Phi V. Its determinant is
-beta^2 mu Delta. For nonzero background amplitude and |kappa|/mu<1,

    Delta >= E(1-|kappa|/mu)>0,

because2mu|Phi V|<=E. Moreover kappa/mu=6Hmu/(4mu^2+k^2), whose
absolute value is at most3|H|/(2|k|) for k!=0. This is a sufficient condition,
not an assumption that every regime in the universe satisfies it. Test the
actual saved domain. Neither Phi=0 nor V=0 is singular.

Recover physical fields by

    Dstar=d_star/beta, W=w/(beta mu),
    f=[Phi Dstar+(V+kappa Phi)W]/Delta,
    g=[V Dstar-(mu^2 Phi+kappa V)W]/Delta.

No division by the physical density or pressure is needed. The ordinary stresses
are recovered from these f,g, not replaced by d_star or w.

## Closed equations conditional on the background and metric

Differentiate W directly:

    W'=-2H W+k^2 Phi f+k Phi V z+Gf-Fg,
    w'=2(r-H)w+beta mu[k^2 Phi f+k Phi V z+Gf-Fg].

The matched density equation follows from the previous exact pressure identity:

    s'=2r s c,
    E_exp=beta[s(2H^2-H'-Hr)-H s']J/2,
    M=beta H s k Phi V z/2,
    T=-beta H s(Gf+Fg)/2,
    d_star'=-3H c d-kq-k beta V^2 z-3(E_exp+M+T)
              +(r-H)(2d-p)+beta(Gg+mu^2 Ff).

Here d=beta D,p=beta P,q=beta Q. Together with the inverse transformation
these are TWO closed first-order equations when background and z are supplied.
They are an exact coordinate change of the two scalar perturbation equations,
not a reduction in their physical degrees of freedom or a proved coarse fluid.
For physical coherent evolution r=H,F=G=0. For a finite reconstruction of that
evolution, use actual spline derivatives and explicitly retain interpolation contacts.

For an independent algebra control, form the matrix T above. Its evolution must
equal (T'+T L)T^-1 U+T b, where L is the original KG2x2 operator and
b=(0,-kVz). T' must be obtained from actual background derivatives and
kappa'=3(H's+Hs')/2. This matrix calculation is NOT the implementation of the
explicit matched equation, so agreement tests the derived expressions.

The initial match is U0=T0(f0,g0), including3B0 once. Removing3B0 changes the
physical initial state and cannot be repaired by changing the output convention.

## Relation to the original objective

This targets the conservation/local-gravity bridge: use the same parent-field
stress without inventing a pressureless closure where the retained equations
retain phase pressure. A successful conditional replay establishes an equivalent
usable stress representation; a future self-consistent metric evolution is a
separate test. It does not derive galactic occupation or complete quantum matter.
