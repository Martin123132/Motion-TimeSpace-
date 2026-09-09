# Clock/coframe variation supplies the missing discrete energy-current coupling

Private continuation, 2026-09-09. Previous turn verified as progress from
immutable sources, actual face-transport arrays and terminal validation states.
This extends DERIVATION-20260909-joint-Gram-action-and-conservative-mass-transport.md.
All paths below are relative to post-checkpoint-work.

## 1. What changed

Previously, the Gram term gave a useful restoring force and an exact graph
energy current, but its coefficient-only metric variation did not supply
that current in the canonical mass-time equation. This turn constructs an
explicit relative-clock action germ whose coframe variation produces the
same current. The current is obtained by differentiating the action, not
by appending a source chosen to preserve a constraint.

The construction includes a changing metric coefficient, the complete clock
Hessian, field-clock cross variations and the nonlinear chain rule from clock
connection to metric variables. Eighteen actual reference backgrounds are
checked, including both canonical and nonlinear P(X) cases.

This is a discretization-level coupling construction, NOT a new physical
clock field, a full discrete Einstein action, a derived value of G or a local-GR
certificate. The common face/nodal geometry and physical boundary constraints
are still to be assembled. No full coupled evolution is claimed from this turn.

## 2. The principal coefficient is a time density

Use the same t=v-sigma(r-4) slicing, E=exp(delta),
F=1-2mu/r-Lambda r^2/3, q=chi_t, w=chi_R, p=q/E and s=w-sigma q.
Before setting beta=g_rr in the original (v,r) chart to zero, write

    d=1+F beta,
    X=(2ps+Fs^2-beta p^2)/d,
    P=1-4b2 X-6b3 X^2,
    a=r^2 E [FP/sqrt(d)+2P_X(p+Fs)^2/d^(3/2)].

This is r^2 sqrt(-g_2)[P g^{RR}+2P_X(grad^R chi)^2]. Under a local change of
time coordinate t -> t+epsilon(t,R), with R fixed, it transforms as a time
density: delta a=epsilon a_t+epsilon_t a. It must NOT be transported as an
ordinary scalar coefficient, which would count the metric work incorrectly.

At beta=0, the inhomogeneous primitive variations proportional to epsilon_t are

    delta q=q epsilon_t, delta w=0,
    delta mu=r sigma E F^2 epsilon_t,
    delta delta=(1+sigma EF)epsilon_t,
    delta beta=-2sigma E epsilon_t.

Those proportional to epsilon_R are

    delta q=0, delta w=q epsilon_R,
    delta mu=-rEF^2 epsilon_R,
    delta delta=-EF epsilon_R, delta beta=2E epsilon_R.

The common epsilon times the field's time derivative is additional in both
cases. Direct symbolic differentiation for the full retained polynomial P(X)
verifies the identities

    q a_q+r sigma EF^2 a_mu+(1+sigma EF)a_delta-2sigma E a_beta=a,
    q a_w-rEF^2 a_mu-EF a_delta+2E a_beta=0.

In particular, for G_metric=F partial_delta+rF^2 partial_mu-2 partial_beta,

    G_metric a=q a_w/E.

Thus the earlier coefficient-only mass-time correction is kappa q U_w/(HE).
It vanishes canonically because a_w=0; this does not imply zero energy transport.

## 3. A clock lift selected by the existing positive energy allocation

The already fixed Gram operator is

    R_a=T^T diag(Sa)T/h,
    U=sum_i a_i rho_i, rho=S^T(Tchi)^2/(2h)>=0.

There is no new damping or fitted coefficient. Let xi_i be relative clock
displacements used to represent a coframe variation, not independent physical
matter fields. Each Gram factor uses its existing positive energy allocation:

    omega_li=S_li a_i/(Sa)_l,   sum_i omega_li=1,
    xi_bar_l=sum_i omega_li xi_i,
    theta_li=xi_i-xi_bar_l.

The proposed clock lift is

    U_clock = sum_l (Sa)_l [sum_i T_li chi_i(t-theta_li)]^2/(2h).

Here a is the time-density at the common current time. Its local-clock
variation is the density law in section 2, not a second independent delay.
The factor weights follow the specified nodal energy allocation; this does
not claim uniqueness among every possible lattice/coframe construction.

At xi=0 this reduces exactly to U. A common clock displacement produces no
relative offsets. If J_ij is the previously derived antisymmetric energy
current, direct differentiation gives

    (U_clock)_xi,i = -q_i(R_a chi)_i+a_i rho_t,i = -sum_j J_ij.

For edge connection increments Delta xi_e=h_e Delta A_e,

    (U_clock)_A,e = h_e F_e,
    F_e=sum_{i left of e,j right of e} J_ij.

Every edge covector is verified against the old cut-flux construction. Existing
saved transport arrays at t=.1 agree with the independent parent-profile
evaluation. No flux was fitted or inserted into the action by hand.

### First local-clock Ward identity, including metric work

At xi=0 take delta chi_i=epsilon_i q_i,
delta a_i=epsilon_i a_t,i+epsilon_t,i a_i and delta xi_i=epsilon_i. Then

    delta U_clock
      =sum_i [epsilon_i(a_i rho_t,i+a_t,i rho_i)
               +epsilon_t,i a_i rho_i]
      =d/dt sum_i epsilon_i a_i rho_i.

The Lagrangian contribution -U therefore changes by the corresponding total
time derivative. The coefficient work rho_i a_t,i is retained explicitly.
This proves the first Ward identity in the specified local-clock variables;
it does not establish a full nonlinear spacetime gauge symmetry of the whole
metric discretization.

## 4. Connection to the metric source, with its exact limitation

In the present chart the temporal coframe connection is

    A=g_tR/g_tt=sigma-1/(EF),
    G_metric A=-1/E.

Consequently the isolated connection part of the metric variation gives

    G_metric U_clock = -h_e F_e/E_e,
    (kappa/h_e)G_metric U_clock = -kappa F_e/E_e.

The last expression is precisely the conservative face-mass source derived
in the previous canonical transport calculation. The kappa/h_e normalization
uses the corresponding face gravitational variation; its incorporation in
one common face/nodal gravity action remains to be verified. In the tests,
face geometry is sampled directly from the same parent, not inferred through
an unvalidated nodal interpolation. The old coefficient part and the nonlinear
momentum changes are separate retained contributions, not silently dropped.

There is a specific remaining covariance issue. The full coordinate law is

    delta A=epsilon A_t+epsilon_R-A epsilon_t.

A simple spatial primitive xi of Delta A correctly represents the compensated
spatial-gradient variation, but is NOT automatically the fully background-
covariant time-dependent link transport when A is nonzero. That transport and
the combined gravitational constraint algebra must still be derived. The
first Ward identity cannot be used to skip this step.

This connection chart also requires EF!=0. It does not establish a regular
extension through a horizon, nor claim a physical singularity when the chart
fails. No horizon or first-u promotion follows.

## 5. Linearized coupling is now explicit

The implementation uses a quadratic germ, not a live delayed-time evolution.
For theta induced by xi, let

    z0_l=(Tchi)_l,
    z1_l=-sum_i T_li theta_li q_i,
    z2_l=sum_i T_li theta_li^2 chi_tt,i/2.

Then

    U^(2)=sum_l (Sa)_l (z0_l^2+2z0_l z1_l+z1_l^2+2z0_l z2_l)/(2h).

Its complete clock Hessian for directions xi,zeta is

    D2_xi U[xi,zeta]
      =sum_l (Sa)_l/h [z1_l[xi] z1_l[zeta]
        +z0_l sum_i T_li theta_li[xi]theta_li[zeta] chi_tt,i].

Both terms are needed. The full matrices, constant-clock null direction,
independent bilinears and two-step mixed finite differences are checked.
Some clock-potential eigenvalues are negative; none are projected away.
These matrices are not the kinetic matrix of an evolved constrained theory,
so neither stability nor instability is inferred from these signs alone.

For a primitive field variation e, write da=Da[e], dq=e_q and dchi=e_chi.
The field-clock cross covector is explicitly

    d(U_xi) = -dq R_a chi-q R_a dchi-q R_da chi
              +da rho_t
              +a [B(dchi,q)+B(chi,dq)],
    B(u,v)=S^T[(Tu)(Tv)]/h.

This includes the derivative of the energy-weighted factor clocks; it does
not hold their allocation fixed under metric variation. All six primitive
directions are independently checked. At quadratic perturbative order the
mixed block involves dchi and dq, not a new perturbation chi_tt variable;
chi_tt in the clock-clock block is a known background coefficient. This is
not a license to promote the finite-delay functional to a fundamental causal
field theory or to ignore the metric constraint/degree-of-freedom analysis.

For physical face variables (mu,delta), the connection derivatives are

    A_mu=-2/(rEF^2), A_delta=1/(EF),
    A_mumu=-8/(r^2 EF^3), A_mudelta=2/(rEF^2),
    A_deltadelta=-1/(EF).

Thus the isolated geometry Hessian contains BOTH

    (P dA)^T U_xixi (P dA_other)
       +sum_e (h_e F_e) D2A_e,

where P integrates edge increments into relative clocks. Omitting the second
connection derivative loses a real term because the background current is
nonzero. These two terms are compared against direct metric variations.

The primitive representation P looks dense, but the action's dependence is
local: offsets in each factor cancel all edges outside that factor's support.
A production implementation should assemble factor-local edge maps rather
than use a dense cumulative matrix and rely on floating cancellation.

## 6. Remainder bound and high-precision qualification

For each owned scalar profile and time-shift interval, bound the third time
derivative by expanding its rational-in-r, polynomial-in-v harmonic amplitudes.
Leibniz's rule and |sin|,|cos|<=1 supply a finite explicit M3_i. All tested shifts
stay within the original reference's v domain. Let

    b_l=sum_i |T_li| |theta_li|^3 M3_i/6.

The exact delayed-profile potential minus its quadratic germ obeys

    |U_exact-U^(2)| <= sum_l (Sa)_l/(2h)
       [2|z1_l z2_l|+z2_l^2
        +2|z0_l+z1_l+z2_l| b_l+b_l^2].

This is a bound for the specified reference profiles and fixed-time coefficient,
not for the unknown full solution. Ordinary double-precision checks initially
included an arithmetic allowance larger than some tiny remainders. Four
extremal controls (worst observed error/bound and smallest bound for each
fixture) were therefore repeated at 60 and 90 digits WITHOUT that allowance:

| Control | Error / analytic bound |
|---|---:|
| canonical, worst observed ratio | .3436594 |
| canonical, smallest bound | .3100247 |
| nonlinear, worst observed ratio | .3527939 |
| nonlinear, smallest bound | .3058156 |

The two precisions agree to the tested relative 1e-35. Frozen Float64 spatial
coefficients are interpreted exactly, with the original rational time-profile
expressions. These are high-precision controls, not directed-rounding interval
certificates for every reference sample.

Under UNIFORM smooth spacetime and clock profiles, this remains a numerical
correction rather than a new finite continuum coupling. Third differences of
chi(t-xi(R)+constant,R) are O(h^3); bounded Gram factors give U_clock=O(h^4)
on a fixed interval. The needed third spatial derivative of the composition is

    chi_RRR-3xi' chi_tRR+3(xi')^2 chi_ttR-(xi')^3 chi_ttt
      -3xi'' chi_tR+3xi'xi'' chi_tt-xi''' chi_t.

The uniform bounds needed here have NOT been proved for the evolved branch.
Action-level O(h^4) does not imply an all-row fourth-order force or curvature
error, particularly at boundaries or on rough data.

## 7. Numerical control failure retained

The first linearization validator ended 231/232: one nonlinear w/clock
complex-step comparison failed. Promoting a real third-difference input to
complex selected a different matrix-multiplication rounding path, swamping a
tiny derivative. The control now applies the same real matrix to real and
imaginary parts separately. At unchanged tolerances the complete replay,
including the precision controls and failure-preservation check, passes 233/233.
The original failed owner, arrays and scripts remain unchanged. This is a
control-kernel correction, not a change of the mathematical derivative or a
relaxation of a physical gate.

## 8. Next bounded implementation

Assemble one mixed-grid matter/geometry action using these now-derived blocks:

1. Specify a fixed finite-element/volume placement for face mass and nodal
   lapse/scalar variables. Derive the interpolation and adjoint maps from that
   representation, not by choosing an interpolation that passes a test.
2. Include the coefficient, clock-current, field-clock and second-connection
   variations together with the ungauged gravitational variation.
3. Test the full time-dependent coframe law and constraint compatibility,
   retaining boundary covectors, actual mass-anchor data and parent forcing.
4. Only after that derive the response evolution and compare against the same
   baseline. Recover the continuum GR constraints; do not merely rename a
   conserved numerical quantity or replace the full objective by a flat limit.

The old failed coupled evolution, curvature/strong-norm issues and missing
physical calibration remain open. No new public, galaxy, local-GR, Maxwell,
horizon or first-u claim follows from this construction.

## 9. Saved evidence

Owners under source-intake/navier-stokes/20260909:
- annular-clock-coframe-current-derived/status.json: 308/308, 10:44:46 UTC;
  18 hashed coframe/current arrays.
- annular-clock-linearized-coupling-derived/status.json: FAILED 231/232,
  10:54:11 UTC, no COMPLETE; original control failure retained.
- annular-clock-linearized-coupling-qualified/status.json: 233/233,
  10:58:26 UTC; full block replay and four 60/90-digit controls.

Scripts:
- scripts/annular_clock_connection_20260909.py
- scripts/derive_annular_clock_coframe_current_20260909.py
- scripts/annular_clock_linearization_20260909.py
- scripts/derive_annular_clock_linearization_20260909.py
- scripts/annular_clock_complex_control_20260909.py
- scripts/derive_annular_clock_linearization_qualified_20260909.py

All jobs have exited. Work remains private, within post-checkpoint-work, with
single-core BelowNormal execution and no subagents, shared-process shutdown,
GitHub action, frozen-workbench edit or galaxy modification.
