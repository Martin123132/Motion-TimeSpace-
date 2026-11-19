# Derived regular momentum and source-complete slow background

Use the retained dimensionless canonical real field b=phi/Mpl, conformal
H=a'/a, mass m in Mpc^-1, and native energy units8*pi*G*a^2. The unchanged
scalar action gives v=b', v'=-2H*v-a^2*m^2*b. Therefore

    J=a^2*v,       J'=-a^4*m^2*b.

Let N=ln(a), j=J/a^5=v/a^3, and b=b_start+delta_b. Then exactly

    d(delta_b)/dN = a^3*j/H,
    dj/dN = -5j-m^2*b/(aH).                                (1)

The coefficient5 is derived from the scaling, not fitted. In the regular
radiation limit aH=A, j approaches -m^2*b/(5A); the tiny velocity v=a^3*j
is reconstructed rather than evolved under an order-one field tolerance.

## Friedmann includes the new slow source

From the retained table define at its original nodes

    R_rest=3H_old^2-[v_old^2+a^2*m^2*b_old^2]/2.

Keep this positive non-slow energy history fixed, using a positive log-cubic
interpolant whose sensitivity is tested. At EACH step in (1), use

    rho_s=[a^6*j^2+a^2*m^2*b^2]/2,
    P_s=[a^6*j^2-a^2*m^2*b^2]/2,
    H=sqrt[(R_rest+rho_s)/3].                               (2)

Thus the newly evolved field's kinetic and potential energy, not the old
velocity table, enter its expansion rate. Its energy identity is
d(rho_s)/dN=-(rho_s+3P_s). If an interpolation-consistent rest pressure is
needed it is -(dR_rest/dN+R_rest)/3; that numerical representation is not a
new microscopic equation of state or a replacement for the native species
stress. No full thermal/perturbation hierarchy is evolved in this stage.

The original late heavy-background averaging, neutrino history and fitted
parent parameters remain inherited. Initial b_start is retained, not shot
again to impose a=1 flatness. Verify the resulting present normalization.

## Finite-start regular seed: conditional bound, not an exact axiom

Let a_i=1e-9 and A_i=a_i H_i. Under the retained regular radiation/matter
branch, suppose for0<a<=a_i that A_min<=aH<=A_i and the positive slow field
has no decaying homogeneous momentum. The integral equation is

    J(a_i)=-m^2 integral_0^a_i [a^4*b(a)/A(a)] da.

If delta=m^2*a_i^4/(20*A_min^2)<1, its regular positive solution satisfies
b_i<=b(a)<=b_i/(1-delta). Hence the leading seed j_i=-m^2*b_i/(5*A_i)
has relative magnitude error at most

    A_i/[A_min*(1-delta)]-1.                                (3)

For a purely radiative background, the next term at FIXED finite-start b_i
is j_i=-m^2*b_i/(5A_i)-m^4*b_i*a_i^4/(225*A_i^3)+O(a_i^8).
This is not the coefficient for a fixed asymptotic b(0); those differ.

The numerical bound takes A_min^2=A_i^2(1-eta), where eta conservatively
includes unit^2*Omega_m*a_i/A_i^2 and twice the retained scalar-energy
fraction at that epoch. This relies on the retained standard radiation/
nonnegative matter and regular initially frozen scalar histories. The
mass/physical-H ratios are checked small so the scalar bootstrap is valid.
Massive-neutrino nonrelativistic excess is covered by the matter allowance.
These are explicit assumptions of (3), not a proof for arbitrary initial
universes, isocurvature or a decaying-mode admixture. The supplied initial
scalar amplitude and cosmic abundance remain external retained inputs.

Numerical evolution retains the actual original seed; (3) labels its
finite-start approximation. Convergence of this initial-value problem is
separate from a uniform theorem for the entire allowed primordial interval.

## Independent integral checks and precision

In addition to step refinement, check the integrated identities

    J(N)=J_i-m^2 integral_Ni^N exp(4s)*b(s)/H(s) ds,
    delta_b(N)=integral_Ni^N exp(3s)*j(s)/H(s) ds.

Use positive-weight quadrature and the stored offset, not the difference
of nearly equal rounded fields. Check early matching readouts separately
from their much larger late-time values. Retain j and delta_b in the
candidate output; a float64 b column alone cannot encode every tiny early
field increment. A later native interface should consume the stable state
or derive derivatives from its equations, not differentiate that column.
