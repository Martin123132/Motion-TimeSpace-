# Recovering the physical early state before any phase average

This stage continues the retained positive-quadratic real-scalar parent. It
does not replace the action, introduce a local population law, or identify
an averaged ensemble with a single coherent real history. Units and source
conventions follow `../mts-canonical-metric-closure-20261110/DERIVATION.md`:
c=hbar=1, fields in reduced-Planck units, conformal H=a'/a, mu=a*m,
and gravitational sources multiplied by 8*pi*G*a^2. Field perturbations
are dimensionless; their conformal velocities and p have units Mpc^-1.
D, P and Q have units Mpc^-2; alpha has units Mpc. k>0 throughout.

## 1. A derivative-free canonical gauge conversion

The saved native synchronous primitive state is (u_s,w_s=u_s'). Let the
background be (phi,v=phi'), with v'=-2Hv-mu^2 phi. The flat native output
conventions, read from equations.f90 rather than inferred from a column name,
are

    eta = saved_etak/k,
    alpha = sigma/k = -H*saved_v_newtonian_cdm/k^2,
    Phi = eta-H*alpha,
    Psi = 2*saved_Weyl/k^2-Phi.

Here saved_Weyl=k^2*(Phi+Psi)/2. The velocity output is NOT sigma or theta.
The gauge time shift satisfies alpha'=Psi-H*alpha, and u=u_s+v*alpha.
For the actual canonical momentum p=u'-(Psi+3Phi)*v, substitution gives

    u = u_s+v*alpha,
    p = w_s-mu^2*phi*alpha-3*eta*v.                         (1)

The physical canonical momentum is a^2*p. Equation (1) needs no numerical
metric derivative and divides by neither v nor phi, including at their
turning points. Its inverse is explicit. It is a real two-coordinate map
of the original real field, not a choice of the later affine response D0.

With D_s=v*w_s+mu^2*phi*u_s, P_s=v*w_s-mu^2*phi*u_s,
Q_s=k*v*u_s, and S=v^2, the independent source transformations are

    D = D_s-3H*S*alpha,
    P = P_s-(3H*S+2mu^2*phi*v)*alpha,
    Q = Q_s+k*S*alpha,
    Dstar = D_s-3eta*S.                                   (2)

They agree with D=v*p+mu^2*phi*u+3S*Phi,
P=v*p-mu^2*phi*u+3S*Phi, Q=k*v*u from the retained action.
The factor 8*pi*G*a^2 in a saved stress is evaluated on the background:
transform the underlying physical stress, not the already-scaled quantity
as though it were a new spacetime scalar.

For the synchronous-comoving cold control the corresponding normalized
coordinates are delta_N=delta_s-3H*alpha, Q/rho_g=k*alpha,
and Dstar/rho_g=delta_s-3eta, with rho_g=8*pi*G*a^2*rho_c.
No scalar phase is introduced for cold matter. The surviving slow scalar
uses (1)-(2) in both the cold and heavy models.

## 2. What the full complex carrier map actually requires

If TWO real quadratures u and p are independently specified, combine each
pair into a complex number. For B0=A0*exp(-i*theta), B0!=0,
lambda_k=Lk-i*Wk, q=a*u, define

    Z = a*u/B0,
    V = [a*p+(H-lambda_k)*a*u]/B0.                         (3)

The inverse is u=(B0/a)*Z and
p=(B0/a)*[V+(lambda_k-H)*Z]. Its four-real determinant is
|B0/a|^4>0. At fixed background and time the two-real-field canonical form
pulls back to

    a^2 sum_j du_j wedge dp_j
      = |B0|^2 [dx wedge dr+dy wedge ds+2Wk dx wedge dy],   (4)

where Z=x+i*y and V=r+i*s. This is a fixed-time statement; the earlier
action supplies the connection and boundary terms for time evolution.

Equation (3) is NOT an inverse from two averaged stress numbers. A saved
real field/velocity supplies the coherent real state in (1), not automatically
a second independent quadrature or a phase-invariant ensemble. Replacing
the latter by zero, D0, or an isotropic phase average is a state-preparation
choice and must not be called information recovered from (1).

## 3. Exact rank and a pressure-changing null direction

For the retained ensemble source map let aR=L0-H, ak=Lk-H, W0>0,
Db=aR^2+W0^2+mu^2, and S0=aR^2+W0^2. In coordinates (x,y,r,s),

    [dstar,current]^T = M (x,y,r,s)^T,
    M = (2/Db) [[aR*ak+W0*Wk+mu^2, aR*Wk-W0*ak, aR,-W0],
                [k*aR,                 -k*W0,    0,   0]].

Its (y,s) minor is -4k*W0^2/Db^2, so rank(M)=2 for this domain. Put
L=Wk*S0+mu^2*W0. An explicit basis of the nullspace is

    n1 = (W0,aR,-aR*L/S0,W0*L/S0),
    n2 = (0,0,W0,aR).

The pressure row is M_density-(4mu^2/Db,0,0,0). Its value on n1 is
-4mu^2*W0/Db, nonzero for the massive branch, while its value on n2 is zero.
Thus identical instantaneous density/current can hide different pressure;
even adding instantaneous pressure leaves another coordinate unresolved.
With the other species fixed the constraint sees the same metric initially,
so metric constraint satisfaction alone cannot select the missing state.
These are linear null directions, not an assertion that every finite
amplitude describes an admissible cosmological ensemble.

## 4. The retained data can supply more than the averaged table

The original exact k=1/Mpc packet saves BOTH primitive field perturbations
and their conformal velocities, for the slow and heavy fields, at 4253
epochs. Therefore the coherent physical early state in (1) is recoverable;
it is not necessary to reconstruct it from only two matching moments.

The existing a225-w6-d8 matching table deliberately compresses a phase
window: polynomial secular terms plus 2theta and 4theta harmonics, followed
by extraction of the constant secular coefficient. Density/current are
kept for the fluid handoff and pressure is retained as a diagnostic.
Reproducing that projection checks provenance, not invertibility.
Gauge conversion and temporal averaging must not be silently interchanged:
the products H*v^2*alpha and phi*v*alpha in (2) also have histories.

The coherent state still inherits the original adiabatic/native seed,
seed_scale=1, retained masses, homogeneous amplitude and heavy fraction.
It does not derive a primordial spectrum, select a galaxy's occupation,
or make a covariance assumption unnecessary. The concrete continuation is
to propagate (1) across a short matching window and compare an explicitly
defined phase projection, retaining its error and discarded phase response.
Do not evolve the late dust approximation backwards as the early history.

## 5. Frozen verification scope

Reconstruct backgrounds using the native natural cubic boundary convention,
actual saved a values, and the native pre-table extrapolation. Check saved
primitive stresses, (1)-(2), the inverse map, the cold density/current map,
the existing matching projection, and symbolic (3)-(4)/rank/nullspace.
Use both heavy and cold saved k=1 histories. No new native evolution, fit,
temperature-curve change, new phase window, or D0 preparation is performed.
The existing 2e-5 reconstruction and 1e-10 algebra gates are unchanged.
Component-sum/peak normalizations and absolute errors are recorded; zeros
must not be hidden by a unit floor. Stored transfer metric columns may have
single-precision origin: their algebraic consistency is not an independent
high-precision metric accuracy or integration test.
