# Joining the affine wave response to the retained metric constraints

This is a continuation of the retained minimally coupled positive quadratic
subfamily, not a derivation of its assumed Einstein normalization from a new
substrate. Use c=hbar=1, conformal H=a'/a, mu=am, k>0, and fields divided by
the retained reduced Planck mass. Primes are conformal-time derivatives.

## 1. Unrestricted canonical momentum removes the apparent derivative loop

For each real background phi, v=phi', perturbation u, define

    C=Psi+3Phi, Dm=3Phi-Psi, p=u'-C v.

The canonical momentum is a^2 p, not p itself. The retained quadratic action
gives, on the background equation v'=-2Hv-mu^2 phi,

    u'=p+C v,
    p'=-2H p-(k^2+mu^2)u+mu^2 Dm phi.

No metric derivative is needed in these two equations. This change does not
delete a solution or set a fast component to zero. It is the unrestricted
parent reference for the previously derived two-real-coordinate plane.

The physical stress, in units 8piG a^2, is

    S_h=v^2,
    Dstar_h=v p+mu^2 phi u,
    Pstar_h=v p-mu^2 phi u,
    D_h=Dstar_h+3 S_h Phi,
    P_h=Pstar_h+3 S_h Phi,
    Q_h=k v u, Pi_h=0.

Here Dstar is compensated energy, not the affine response named D in the
earlier stage. The lapse cancels from the explicit source map because p
already includes it. It has not been ignored in the action.

Direct differentiation proves

    D_h'=-H(D_h+3P_h)-k Q_h+3 S_h Phi',
    Q_h'=-2H Q_h+k(P_h+S_h Psi).

These identities apply to exact real fields and their linear ensembles.
An approximate carrier adds its background equation residual; it is not
silently an exact homogeneous solution.

## 2. The explicit gravity feedback map

Retain ALL other species, their pressure and anisotropic stress. Let
S_total=8piG a^2(rho_total+p_total), Dstar_total=sum(Dstar), Q_total=sum(Q),
and Pi=k^2(Phi-Psi) in the existing observer convention. Then

    denominator=2k^2+3 S_total,
    Phi=-(Dstar_total+3H Q_total/k)/denominator,
    Psi=Phi-Pi/k^2,
    Phi'=-H Psi+Q_total/(2k).

For the retained positive-enthalpy matter/scalar background the denominator
is positive. It is the already derived constraint, not a new screening mass.
If Q or other species are themselves expressed in metric-dependent
coordinates, first transform them to their appropriate canonical/density
variables or solve the resulting joint linear system; do not hold them
fixed incorrectly during variation.

For one real scalar and independently supplied current rest state, set

    row=(mu^2 phi+3H v, v),
    rest=Dstar_rest+3H Q_rest/k,
    base=[[0,1],[-(k^2+mu^2),-2H]],
    coupling=(4v,2mu^2 phi)^T,
    slip=(-v,mu^2 phi)^T.

Its instantaneous closed equation is explicitly

    (u,p)'=[base-coupling row/denominator](u,p)
           -coupling rest/denominator+slip Pi/k^2.

The other species must evolve too for a self-consistent solution. This
formula supplies the scalar block and its exact metric ports without
inventing their evolution or omitting their initial state.

Writing E_constraint=2k^2Phi+D_total+3H Q_total/k, total conservation and
H'=H^2-S_total/2 imply E_constraint'=-H E_constraint. The momentum law
contains -2k Pi/3. Omitting that term breaks the result.

## 3. Explicit connection to the saved carrier-relative variables

Keep the earlier carrier B0=A0 exp(-i theta), lambda0=L0-iW0,
a0=lambda0-H, Omega_k^2=k^2+mu^2-H'-H^2. Let q=a u=B0 Z.
Introduce the independent canonical envelope

    U=(q'-C a0 B0)/B0.

U is a complex momentum coordinate, not the pressure. The four-real-state
parent equations obtained from the SAME canonical q action are

    Z'=U-lambda0 Z+C a0,
    U'=-lambda0 U-Omega_k^2 Z+H C a0+mu^2 Dm.

The earlier affine plane is exactly

    U=lambda_k Z+D-C a0.

Thus it fits into this closed reference without freezing D. Differentiating
the definition gives

    D'+(lambda0+lambda_k)D
      =C' a0-2mu^2 Psi+C R0-Rk Z,

where Rj=lambda_j'+lambda_j^2+Omega_j^2. This recovers the saved response
defect and explicitly retains its homogeneous initial component.

Let aR=L0-H, Db=|a0|^2+mu^2 and Rh be the carried homogeneous energy in
8piG a^2 units. The normalized ensemble sources are

    dstar=2 Re[a0* (U-H Z)+mu^2 Z]/Db,
    pstar=2 Re[a0* (U-H Z)-mu^2 Z]/Db,
    current=2k Re[a0* Z]/Db,
    enthalpy=2|a0|^2/Db,
    delta=dstar+3 enthalpy Phi,
    pressure=pstar+3 enthalpy Phi,
    phase_current=-mu current/k.

Multiply by Rh before adding to Einstein sources. Rh is the actual carried
ensemble normalization, not a locally adjustable halo mass. In the z=10
replay its retained matched-dust value is used as a reference weight only;
the small WKB pressure/background defect must accompany a dynamical test.

For w=(ReZ,ImZ,ReU,ImU), the compensated metric-source row is

    Dstar_h+3H Q_h/k = (2 Rh/Db)
        (mu^2+2H aR, -2H W0, aR, -W0) w.

The Phi forcing column of w' is

    (4aR,-4W0,4H aR+2mu^2,-4H W0)^T,

and the Pi/k^2 column is

    (-aR,W0,-H aR+mu^2,H W0)^T.

Together with the displayed equations, this is an explicit real matrix for
the joint constraint elimination, not a fitted fluid closure. In computation
the slow beat still needs the previous separate-rotation arithmetic; these
unrestricted equations retain the fast branch rather than providing a
numerically efficient adiabatic solver by themselves.

## 4. Canonical gravity and boundaries are not optional extras

For the real variables the Hamiltonian density before removing metric terms is

    a^2[(p+C v)^2/2+(k^2+mu^2)u^2/2-mu^2 Dm phi u]-L_metric.

The earlier ADM-shift variation gives Q. Retain L_metric and both earlier
coordinate boundaries, including -(H q^2/2)'. Metric source variation at
fixed unrestricted canonical momentum agrees with the original Lagrangian
variation at fixed u'. By contrast, varying a trajectory Hamiltonian with D
frozen does not. The joint gravity momentum shift already derived on
7 November remains its owner; this is its new scalar input map, not a new
choice of gravitational momentum or coupling.

The cold control uses dstar_c=delta_c-3Phi and its velocity current, with
zero pressure and S_c=Rc. No scalar carrier or arbitrary reference mass
enters its physical constraint sources.

## 5. Numerical scope and the next executable interface

Saved source replay and algebraic metric tests do not constitute a new
self-consistent late hierarchy evolution. The existing native adapter
explicitly rejects the averaged heavy selector and massive-neutrino memory.
Those are real state-ownership conditions, not guards to suppress. A late
adapter must retain the selector as discrete state and, when active, the
neutrino G11/G30 preparation constants as extra state with zero derivative.
It must check the late regime, observer and RHS against the unchanged native
solver before replacing the heavy block. Do not use 184/182 early dimensions.
