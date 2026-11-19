# Relative-phase perturbations on the retained cold background

Private continuation, 2026-11-07. This uses the same positive, constant-mass,
two-canonical-field branch and the accepted background; it does not replace
the MTS action, fit a mass or insert a dust perturbation law.

## 1. Owned equations and conventions

The starting point is the retained quadratic canonical scalar component,
with equation Box(phi)-m^2 phi=0 in the usual (-+++) convention. Its overall
gravitational normalization is unchanged. The normal-frame perturbation
equations, including both metric channels, were derived and checked against
the native equations in:

- ../mts-metric-channel-factorization-20261107/DERIVATION.md
- ../mts-metric-channel-factorization-20261107/metric_channels.py

The background and its error tube come from:

- ../mts-cold-background-extension-20261107/DERIVATION.md
- ../mts-cold-background-extension-20261107/extension/freeze.json
- ../mts-cold-background-extension-20261107/split-envelope/fine.npz
- ../mts-cold-background-extension-20261107/split-envelope/fine-dense.npz
- ../mts-cold-background-extension-20261107/extension/cold/fine.npz
- ../mts-cold-background-extension-20261107/extension/cold/fine-dense.npz

Here N=ln(a), prime means conformal time, H=a'/a is CONFORMAL Hubble rate,
omega=am, mu=omega/H, alpha=k^2/(omega H), eta=H_N/H. H, k, m and omega
have units Mpc^-1; alpha and mu are dimensionless. This alpha is NOT the
earlier gauge displacement. Scalar densities below have the retained
conformal gravitational normalization, in Mpc^-2, not physical kg/m^3.

For the heavy field put x=omega phi, v=phi', X=omega delta_phi_n, Y=pi_n.
The parent's full-frequency coordinate is X_full=Omega delta_phi_n,
Omega=sqrt(omega^2+k^2); thus X_full=sqrt(1+alpha/mu) X.

    x_N = x + mu v
    v_N = -2v - mu x
    X_N = X + mu Y + mu v Psi
    Y_N = -2Y -(mu+alpha)X -mu x Psi +3v Phi_N

Both injections are inherited, not fitted. The change from X to X_full,
including its derivative and injections, is checked in validate_relative.py.

## 2. Relative density and phase, without reconstructing a late carrier

For rho_h=(x^2+v^2)/2>0 define

    C = (X+iY)/(x+iv)
    delta = 2 Re(C)
    W = -alpha Im(C)
    theta = atan2(-v,x), c=cos(2theta), s=sin(2theta).

An infinitesimal phase displacement is delta_theta=-Im(C), so
W=alpha delta_theta. These are relative amplitude/phase variables, not
an additional field. They are undefined at rho_h=0. The baseline instead
uses its existing CDM density and velocity-divergence equations.

Direct differentiation and inversion give the exact equations:

    delta_N = (alpha s/2)delta -(1-c+6s/alpha)W +3(1-c)Phi_N
    W_N = alpha^2(1+c)delta/4
          -(1+eta+3c+alpha s/2)W
          +alpha mu Psi +(3alpha s/2)Phi_N.

The exact physical dictionary is

    D_h = rho_h delta
    P_h = rho_h[-c delta +(2s/alpha)W]
    Q_h = (H/k)rho_h[(1-c)W -(alpha s/2)delta]
    enthalpy_h = rho_h(1-c).

In particular D_h,N=-D_h-3P_h-(k/H)Q_h+3enthalpy_h Phi_N.
The pressure and current retain their oscillatory parts. Six symbolic
identities establish the rates, dictionary and density continuity.

For the same positive background let b=rho_h/(2H^2), so 0<=b<=3/2, and
eta=eta0+b c. The background equations imply

    theta_N = mu -(3/2)s
    alpha_N = -(1+eta)alpha
    mu_N = (1-eta)mu
    b_N = b[-1-2eta0+(3-2b)c].

These relations, not a guessed theta(N), drive the transformation.
The late cold background supplies bounds on all phases, not an owned
late microscopic phase trajectory.

## 3. Exact separation of the rapid oscillations

Write y=(delta,W)^T and y_N=A y+B u, where u=(Psi,Phi_N)^T:

    A=A0+Ac c+As s
    A0 = [[0,-1],[alpha^2/4,-1-eta0]]
    Ac = [[0,1],[alpha^2/4,-3-b]]
    As = [[alpha/2,-6/alpha],[0,-alpha/2]].

Define the small oscillatory coordinate correction

    P=(Ac s-As c)/(2mu), T=I+P.

Let partial_N differentiate its alpha, mu and b coefficients while holding
theta fixed. Then

    P_N = partial_N P +(Ac c+As s)theta_N/mu
    R = A P-P A0-partial_N P +(3s/(2mu))(Ac c+As s).

The homogeneous transformation y=T z is EXACT:

    z_N = [A0+T^-1 R]z.

No remainder is silently discarded. Symbolic expansion gives
R=(R0+Rc c+Rs s+Rc2 cos(4theta)+Rs2 sin(4theta))/(2mu):

    R0  = [[0,(alpha^2-6b)/(2alpha)],[-alpha^3/8,0]]
    Rc  = [[-5alpha/2,-(alpha^2+6eta0-6)/alpha],
           [-alpha^3/4,5alpha/2]]
    Rs  = [[-alpha^2/2,b+5],
           [alpha^2(b+5)/4,(alpha^2-2eta0 b+6eta0-4b-6)/2]]
    Rc2 = [[0,-9b/alpha],[0,-alpha b/2]]
    Rs2 = [[0,-b],[0,9b/2]].

The separate coefficient audit reconstructs this Fourier form and compares
it against the directly differentiated matrices at independent phases.

## 4. What the leading equation means physically

The zero-harmonic homogeneous block implies

    delta_NN +(1+eta0)delta_N
        +[k^4/(4a^2 m^2 H^2)]delta = 0.

Thus the leading restoring coefficient is obtained from the original
field equations, rather than fitted to a density curve. On the mean
background, with physical time t and H_phys=H/a, it becomes

    delta_tt +2H_phys delta_t +[k^4/(4a^4 m^2)]delta = 0.

This is the familiar quadratic-scalar wave-pressure structure, not a newly
unique MTS mechanism. The useful new work here is the retained-branch
coordinate dictionary, finite-interval error estimate and explicit coupling
bookkeeping. The saved mass is an inherited model input; this stage does
not derive that mass from more fundamental coefficients.

Dropping only the displayed restoring entry gives the free CDM block.
That is an operator limit, not a proof that arbitrary exact scalar initial
states converge uniformly to CDM: the relative coordinates and P contain
1/alpha, and 1/(alpha mu)=H^2/k^2 need not vanish as m increases at fixed k.
Physical initial-mode projection and the finite endpoints must be retained.

## 5. Uniform homogeneous bound and background replacement

Let L=N1-N0, alpha in [alpha_min,alpha_max], mu>=mu_min>0. Absolute
monomial bounds on the matrices above, using |eta0|<=2 and 0<=b<=3/2,
give p>=||P||_2 and r>=||R||_2. In code Frobenius bounds dominate the
operator norms. If p<1 then ||T^-1||<=1/(1-p) and
epsilon=r/(1-p) bounds the transformed remainder.

For the positive retained matter/scalar background -2<=eta0<=1. The
symmetric logarithmic norm of A0 is bounded by

    g = 1 + max(1,alpha_max^2/4)/2.

Variation of constants, including T(N1) AND T(N0)^-1, yields

    ||U_exact-U_A0||_2
      <= exp(g L)/(1-p) [2p+(1+p)expm1(epsilon L)].

This is an absolute induced Euclidean norm in (delta,W), for equal physical
initial y. It is not a percentage error in a spectrum, a density fraction,
or a guarantee for the metric-forced system.

The interval parameters are obtained from positive-energy inequalities,
not a maximum fitted to phase samples:

    mu_min = omega0/H_upper,0
    alpha_min = k^2/(omega0 H_upper,0) exp(-2L)
    alpha_max = k^2/(omega0 H_lower,0) exp(L).

Here eta in [-2,1] implies mu_N>=0 and bounds alpha_N/alpha. Numerical
phase samples only check the implementation of these uniform inequalities.

Replacing the exact background coefficients by the saved mean is a separate
error. Write E0 for the initial mean slow-field energy-coordinate norm,
e_max for the parent's terminal comparison radius, r0 for the initial mean
heavy density, u0 for its initial inverse-frequency upper bound, and d1
for the terminal invariant drift bound. Positivity gives

    E_max=E0 exp(L), E_min=E0 exp(-2L)
    w_max=1.5u0+2.8125u0^2+d1
    Delta_r=r0 expm1(w_max)
    Delta_R=Delta_r+E_max e_max+e_max^2/2
    Hlo^2=[Rext,0 exp(-2L)+r0 exp(-L-w_max)
           +max(E_min-e_max,0)^2/2]/3
    Hbarlo^2=[Rext,0 exp(-2L)+r0 exp(-L)+E_min^2/2]/3.

The slow comparison radius and drift are nondecreasing in the parent's
comparison problem. The original energy-coordinate equations bound E by
exp(-2N) and exp(N), and the positive thermal mixture bounds Rext by its
exp(-2N) floor. It follows that

    Delta_eta0 <= (4E_max e_max+2e_max^2+Delta_r)/(6Hlo^2)
                 +2Delta_R/(3Hlo^2)
    Delta_q <= k^4 Delta_R/(12 omega0^2 Hlo^2 Hbarlo^2)
    Delta_A <= sqrt(Delta_eta0^2+Delta_q^2).

The additional transfer error is exp(gL)L Delta_A. The reported combined
bound is the sum of this and the homogeneous micromotion bound.
The actual endpoints come from numerically qualified parent packets, with
the same algebra padding and refinement controls. These are analytic
inequalities evaluated on qualified numerical inputs, NOT a directed-rounding
interval-arithmetic proof of the entire computation.

## 6. Both metric forcings and their derivatives survive

The forcing matrices are

    B=B0+Bc c+Bs s
    B0=[[0,3],[alpha mu,0]]
    Bc=[[0,-3],[0,0]]
    Bs=[[0,0],[0,3alpha/2]].

Simply replacing B by B0 after y=Tz is wrong because T^-1 B0 itself
has an oscillatory part. Instead define

    Dc=Bc+As B0/(2mu), Ds=Bs-Ac B0/(2mu)
    V=(Dc s-Ds c)/(2mu), Dosc=Dc c+Ds s
    J=A V-partial_N V +(3s/(2mu))Dosc.

The exact affine change y=Tz+Vu gives

    z_N = [A0+T^-1R]z +[B0+T^-1J]u -T^-1 V u_N.

Here u_N=(Psi_N,Phi_NN). Neither derivative is declared small. The initial
condition is z0=T0^-1(y0-V0u0), and the final readout is y1=T1z1+V1u1.
Four additional symbolic identities and the resolved-history integrations
check the formula. Dropping the source-derivative term fails an algebraic
negative control. No uniform small bound for a general forcing is claimed
from the homogeneous table.

## 7. Exact relative-coordinate metric rows

Keep the parent's external density/current/shear rows, free rates ell_D and
ell_Q, quadrature enthalpy Wq and nonzero defect DeltaW=Wq-Wbackground.
Add the scalar dictionary of section 2 and its free rates

    ell_D,h = -D_h-3P_h-(k/H)Q_h
    ell_Q,h = -2Q_h+(k/H)P_h.

The differentiated total-source identities are

    D_N=ell_D+3DeltaW Psi+3Wq Phi_N
    Q_N=ell_Q+(k/H)(Wq-DeltaW)Psi.

For the retained GR constraints:

    Psi=-D/(2k^2)-3H Q/(2k^3)-shear/k^2
    Phi_N=-[ell_D+3H(eta Q+ell_Q)/k+3Wq Psi]/(2k^2+3Wq).

For the retained spatial-Poisson comparison:

    Psi=-D/(2k^2)
    Phi_N=-[ell_D+3DeltaW Psi]/(2k^2+3Wq).

The denominator is positive for positive quadrature enthalpy. The GR
Phi_N equation differentiates the Phi constraint; the anisotropic-stress
term belongs in Psi, not as an invented shear derivative in Phi_N.
The implementation checks both branches using explicit linear-row fixtures
on both saved backgrounds. These fixtures test algebra, not a substitute
for a full matter hierarchy or a late Einstein-Boltzmann evolution.

## 8. What was actually evolved

On the frozen cold interval, solve only the two-by-two homogeneous mean
transfer, beginning from the identity matrix. This tests an operator basis;
it does not select primordial cosmological initial data. With a dynamical
metric, a nonzero matter perturbation sources gravity, so this free block
must not be presented as a self-consistent standalone cosmology.

On the already resolved early history, compare the original normal canonical
equations to the EXACT affine equations with a known prescribed u and u_N.
Use two free basis columns plus a zero-initial forced response. The baseline
uses its own CDM equations and background, and is independently checked
against W(N)=W0 exp(N0-N)H0/H(N). No singular relative scalar division is
attempted at its zero heavy density. Zero error between duplicated baseline
coordinate paths is a control identity, not zero cosmological uncertainty.

Both use the inherited base DOP853 rtol=2e-10, fine DOP853 rtol=2e-12 and
independent RK45 rtol=2e-11, with atol=rtol/100. Cold output uses the exact
162 saved epochs; short diagnostics use existing early epochs plus their
explicit shared endpoints. No scattering grid, physical frequency, bank,
background packet or acceptance tolerance was changed.

## 9. Next construction: close the metric together with matter

Use the derived rows, not an independently prescribed metric, in the next
stage. If r denotes the remaining matter state and
u=L_h y+L_r r, then y=Tz+Vu requires

    (I-V L_h)y=Tz+V L_r r.

Test this inverse and form the resulting full block transformation S of
(y,r). For the original coupled generator G the exact transformed generator
is S^-1(G S-S_N). This product-rule route incorporates metric derivatives
through the actual coupled equations rather than assuming u_N is slow.
Its boundedness, joint averaging and physical initial-mode transport are
the next numerical/analytic target; they were not certified by today's
free-transfer or fixture tests.

## Context and provenance

The general scalar-wave setting is established in Hu, Barkana & Gruzinov,
[Cold and Fuzzy Dark Matter (2000)](https://arxiv.org/abs/astro-ph/0003365).
Multi-species scalar perturbation conventions are discussed by Ma &
Bertschinger, [Cosmological Perturbation Theory in the Synchronous and
Conformal Newtonian Gauges (1995)](https://arxiv.org/abs/astro-ph/9506072).
These are context references, not claims that their papers prove this
branch's error bounds. No external formula replaced the retained native
source derivation. All consumed local input hashes and source snapshots
are in the result JSON files and audit-01/result.json.
