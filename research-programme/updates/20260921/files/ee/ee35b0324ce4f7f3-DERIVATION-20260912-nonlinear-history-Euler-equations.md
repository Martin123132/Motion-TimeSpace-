# Beyond the zero-shift slice: nonlinear history Euler equations

Private/local continuation, 12 September 2026. This is an explicit action
derivation with manufactured-history checks, NOT an evolved MTS spacetime,
causal well-posedness theorem, black-hole solution or physical GR-limit claim.
The bounded N128 spatial experiment is documented separately.

## 1. What is new

We have written the nonlinear bulk equations and the complete metric/scalar
first variation of the inherited time-link action at NONZERO P. In particular,
the memory force is evaluated at inverse-transported anchor times, not by
reusing the zero-shift force at each instant. This is a constructive formula
for the history Euler covectors; it does not yet turn a history action into
an ordinary initial-value Hamiltonian system.

Seven manufactured histories/directions check the formula against direct
perturbations of the actual nonlinear action. Separate oriented physical-time
quadrature checks the inverse-time and double-Jacobian kernel. Incorrect
single-J and unpulled-time versions are numerically distinguishable.

The working sector remains kappa=1/10, Lambda=m_chi=b2=b3=0 on the existing
positive annulus. These are code-fixture conventions, not a determination of
Newton's constant or of physical MTS couplings. The comparator is GR with
the same canonical scalar, NOT vacuum GR.

## 2. Exact first-order bulk action, without freezing P

Let F=1-2mu/R, w=chi_R, and E=pi^2/(2R^2)+R^2 w^2/2. The action is

    S = integral dt dR [P mu_t + pi chi_t - H_bulk] + S_G + S_boundary,

    H_bulk = -N mu_R/(kappa sqrtF) + N sqrtF E
        + kappa N F^(3/2) P pi w
        + (kappa/2) R F^(5/2) N_R P^2
        + (kappa/2) N F^(3/2) (mu_R-mu/R) P^2.

Retain the previously specified radial boundary action

    S_boundary = integral dt {-[kappa R N F^(5/2) P^2/2]_in^out
                            -C_out(t) mu_out/kappa + existing port reactions}.

The change beta=kappa N F^(3/2)P is an algebraic reparameterization of the
weak bulk action; eliminating the auxiliary pi reproduces its scalar kinetic
term exactly. It does not assume that the FULL history action has an ordinary
local Legendre transform. The symbolic verifier checks this equality at
nonzero P, not just at the previously tested special slice.

The GR-plus-scalar bulk equations are

    mu_t = kappa N F^(3/2) pi w
           + kappa R F^(3/2)(F N_R-N F_R/2) P,

    chi_t = N sqrtF pi/R^2 + kappa N F^(3/2) P w,

    P_t = N E/(R sqrtF) - N_R/(kappa sqrtF)
          + N mu/(kappa R^2 F^(3/2))
          + 3 kappa N sqrtF P pi w/R
          + kappa F^(3/2)[(N/(2R)+3N_R)P^2 + N P P_R],

    pi_t = partial_R [N sqrtF R^2 w + kappa N F^(3/2) P pi].

The lapse equation is C_bulk=0, where

    C_bulk = mu_R/(kappa sqrtF) - sqrtF E - kappa F^(3/2) P pi w
       + kappa F^(3/2)[(F/2-3mu_R+3mu/R)P^2 + R F P P_R].

These interior expressions follow by spatial integration by parts. For
broken momentum functions they are interpreted cellwise/distributionally,
with interface terms retained; they are not permission to discard jump work.
The weak action is the safer implementation owner. Endpoint conditions also
remain part of the variational problem. We have not silently removed its
P-squared boundary term or inferred a full constraint algebra from these rows.

## 3. Nonlinear connection and coefficient

Define u=kappa^2 F^2 P^2 and d=1-u. The canonical ADM metric gives

    c = beta/(N^2 F-beta^2) = kappa sqrtF P/(N d),
    C = R^2 N sqrtF d.

The chart requires F>0, N>0 AND d>0. F>0 alone is insufficient at nonzero
shift. The Gram factor matrices B,S, radial nodes and geometric anchors
a_f=(S R)_f are the previously sourced numerical construction, unchanged.

For anchor time s, let T_f(s,R), J_f(s,R) satisfy

    T_R=c(T,R),                 T(s,a_f)=s,
    J_R=c_t(T,R)J,              J(s,a_f)=1,

and evaluate endpoint quantities at R_i. With J positive,

    A_f(s)=sum_i B_fi chi(T_fi(s),R_i),
    D_f(s)=sum_i S_fi J_fi(s) C(T_fi(s),R_i),
    A'_f(s)=sum_i B_fi J_fi(s) chi_t(T_fi(s),R_i),
    S_G=-integral ds sum_f A_f^2 D_f/(2h).

This is the existing full time-link action, not an instantaneous potential
invented from the initial jet. A positive D does not prove a positive
Hamiltonian or causal evolution for this nonlocal-in-time system.

## 4. Derive the transport variation and preserve the time boundary

At fixed anchor times, Y=delta T and Z=delta J obey

    Y_R=c_t Y+delta c,
    Z_R=c_t Z+(c_tt Y+partial_t delta c)J,
    Y(a_f)=Z(a_f)=0.

Here delta c is a DIRECT field variation at the transported physical time;
c_t Y has already accounted for the displaced evaluation time. The solution
of the first equation is

    Y_fi(s)=J_fi(s) integral_(a_f)^(R_i)
                         delta c(T_f(s,R),R)/J_f(s,R) dR.

Varying J C(T) gives partial_s[C(T)Y] plus J times the direct coefficient
variation. Thus the reduced transport current is

    I_fi=A_f [S_fi C(T_fi) A'_f - B_fi chi_t(T_fi) D_f]/h,
    sum_i J_fi I_fi=0,

    delta S_G = integral ds sum_fi {
        I_fi Y_fi - A_f D_f B_fi delta chi(T_fi)/h
        -A_f^2 S_fi J_fi delta C(T_fi)/(2h)}
        -[sum_fi A_f^2 S_fi C(T_fi)Y_fi/(2h)]_(s0)^(s1).

No temporal boundary term is dropped unless a stated variation/support
condition actually makes it zero. In the manufactured test it is retained.

## 5. The nonlinear physical-time kernel

The old zero-P formula is not generally evaluated at a single common s=t.
For each factor and each radial point, set

    s_f(t,R)=T_f(.,R)^(-1)(t).

Define the oriented indicator omega_fi(R): +1 between a_f and R_i when
R_i>a_f, -1 between R_i and a_f when R_i<a_f, and zero otherwise. Then

    K(t,R) = sum_fi omega_fi(R)
        [I_fi(s) J_fi(s)/J_f(s,R)^2]_(s=s_f(t,R)).

This follows by interchanging the radial and anchor-time integrals and using
dt=J_f(s,R) ds. One inverse J comes from the tangent solution, and the other
from this change of time measure. Both are required. On a finite anchor-time
window, each summand is supported only where s_f(t,R) lies in that window;
the physical-time limits generally differ with f and R.

For direct coefficient and scalar terms define nodal weights

    d_i(t)=sum_f [S_fi A_f(s)^2/(2h)]_(s=T_fi^(-1)(t)),
    g_chi,i(t)=-sum_f [B_fi A_f(s)D_f(s)/(h J_fi(s))]
                                            _(s=T_fi^(-1)(t)).

The coefficient's density Jacobian cancels the physical-time measure. The
scalar term instead retains 1/J_fi. The geometry Euler covectors, including
their nodal nature, are explicitly

    G_y(t,R)=K(t,R)c_y(t,R)
                -sum_i delta(R-R_i) d_i(t) C_y(t,R_i),   y in {mu,N,P},
    G_chi(t,R)=sum_i delta(R-R_i) g_chi,i(t),     G_pi=0.

The delta symbols denote the continuous functional representation of node
evaluation, not a proposal to smear these loads into a bulk density. Their
finite weak forms are obtained by contracting with the actual trial/test
maps, including every original and added direction.

All coefficients are now explicit:

    c_P  = kappa sqrtF (1+u)/(N d^2),
    c_mu = -kappa P(1+3u)/(R N sqrtF d^2),
    c_N  = -c/N,

    C_P  = -2 kappa^2 R^2 N F^(5/2) P,
    C_mu = -R N(1-5u)/sqrtF,
    C_N  = R^2 sqrtF d.

With G=delta S_G/delta field, the full interior history Euler equations are

    mu_t = (GR bulk mu rate) - G_P,
    P_t  = (GR bulk P rate)  + G_mu,
    chi_t = (GR bulk chi rate),
    pi_t = (GR bulk pi rate) + G_chi,
    C_bulk + G_N = 0.

This supplies the nonlinear covectors, not just a list of inputs to find.
It is conditional on the declared regular histories, chart, reconstruction,
interfaces and boundary treatment. It does not prove that the coupled
equations possess a solution for our saved annular initial data.

### Recovery of the earlier initial formula

When P(t0,R)=0, T(t0,R)=t0, but J can differ from one because

    partial_t c(t0,R)=kappa sqrtF P_t/N.

At that slice c_mu=c_N=C_P=0, c_P=kappa sqrtF/N,
C_mu=-RN/sqrtF and C_N=R^2 sqrtF. The formulas therefore reproduce the
earlier positive nodal mass source, negative lapse source, scalar D/J force
and the double-J P covector. This is not a beta_t=0 shortcut. The canonical
lapse derivative c_N=-c/N also avoids importing the fixed-beta factor -2.

## 6. A concrete boundary consequence, not another unspecified gap

The retained radial boundary Hamiltonian has derivative

    partial_P [kappa R N F^(5/2) P^2/2] = kappa R N F^(5/2) P.

For a CLASSICAL extension with independently free endpoint P variations,
no additional P-dependent boundary action and the present S_f,endpoint=0,
the natural endpoint equation is P_b(t)=0. Its first compatibility condition
is P_t,b=0 at the initial zero-P slice. Ordinary port reactions in mu and chi
do not cancel a P variation. If instead a shift trace is prescribed, its
allowed variations and compatibility must be declared explicitly.

This is not an extra row retroactively imposed on the completed finite
initial-jet test: finite endpoint covectors are coupled to bulk test functions.
It is a separate necessary boundary condition for that classical free-trace
interpretation. Interior nodal Gram forces and broken momentum traces also
require care when taking a continuum limit.

For the regular endpoint bulk trace at P=0, where the endpoint direct Gram
mass weight is zero, the resulting lapse-gradient law is

    (N_R/N)_b = kappa E_b/R_b + mu_b/(R_b^2 F_b).

A constructive trial satisfying this law while preserving both lapse VALUES
is available. Let L=R_out-R_in, x=(R-R_in)/L and
Delta_b=N_b*(required logarithmic derivative)_b-(N_R)_b. Set

    delta N = L [Delta_in (x^3-2x^2+x) + Delta_out (x^3-x^2)].

Both endpoint values vanish; its endpoint derivatives are the required
Delta_b. Also |delta N| <= 4L(|Delta_in|+|Delta_out|)/27, which supplies a
sufficient positive-lapse condition. The N128 control constructs this
UNAPPLIED candidate and tests the identities. It must be represented as
P1 plus this exact global cubic, not interpolated back to P1 and called the
same endpoint derivative law. It is a candidate boundary-compatible gauge
profile, not a fitted physical coupling or a new imposed stress tensor.

This does NOT close the full boundary problem: changed lapse shape changes
P_t, J and Gram fluxes. The original physical drives, complete weak equations,
time-boundary work and higher compatibility must all be replayed. No modified
lapse candidate or old failed state is silently used as an evolution seed.

## 7. Executed controls and numerical scale

The completed nonlinear run has 70 passing checks, including 18 exact
symbolic identities. It uses five independent directions (mu,N,P,chi,mixed)
on polynomial histories, and P/mixed on a soluble affine clock. These are
manufactured tests, not on-shell solutions. Full nonlinear geometry is
evaluated before differentiating; the tests do not freeze P back to zero.

- Raw tangent versus integrated-by-parts variation: maximum error 1.36e-20.
- Centered action differences at step 5e-4: maximum error 5.32e-14.
- Temporal Gauss orders 20 and 28 agree within the recorded gates.
- Soluble finite-shift transport is independently compared with its exact map.
- For the soluble P variation, the physical-time transport contribution is
  -1.665020964701123e-8. Using a single inverse J gives -1.7147264881661543e-8;
  using the unpulled anchor time gives -1.670430406521453e-8. Both are rejected.
- Mixed-case temporal boundary work is about -1.74e-12 and -1.57e-12; it is
  small but resolvable, and is not set to zero.

Attempt01 reached all seven comparisons but failed a poorly scaled diagnostic:
it required the boundary term to exceed an arbitrary absolute 1e-10. The
measured terms are about 1e-12, while the variation identity error is below
1.4e-20. Attempt02 changes ONLY that negative-control test to require a
100-fold separation from max(identity error,1e-15). Histories, perturbations,
equations, quadrature, physics gates and numerical results are unchanged.
Both executed versions and outcomes are retained, not overwritten.

## 8. What this enables next

We can now evaluate the action and its derivatives on genuine nonzero-shift
histories instead of extrapolating a P=0 jet formula. Next, use the small
owned annular construction to establish a boundary-consistent history
representation, including the derived endpoint gauge condition, interfaces
and physical time-window coverage. Freeze the completed trial maps or include
their transport terms if changed. Compare full weak rows and the GR control
before authorizing a short coupled evolution.

Whether this history problem admits a causal IVP, requires a history/terminal
boundary formulation, or needs a parent-selected auxiliary-field realization
is not settled here. Positivity, exact first variation and a finite initial
constraint pass do not settle that question. No N256 refinement or new
evolution is authorized by this calculation alone.

## 9. Reproducible evidence

Paths relative to post-checkpoint-work:

- `DERIVATION-20260911-canonical-action-and-boundary-consistent-initial-data.md`
- `DERIVATION-20260911-coupled-initial-jet-and-exact-time-link-adjoint.md`
- `DERIVATION-20260909-covariant-time-links-and-mixed-gravity-basis.md`
- `scripts/annular_nonlinear_history_20260912.py`
- `scripts/derive_annular_nonlinear_history_20260912.py`
- `scripts/derive_annular_nonlinear_history_control_20260912.py`
- `source-intake/navier-stokes/20260912/annular-nonlinear-history-attempt01/status.json`
- `source-intake/navier-stokes/20260912/annular-nonlinear-history-attempt02/status.json`

One BelowNormal, single-core Python at a time; no subagents, GitHub actions,
galaxy edits or frozen-workbench edits. The later combined seal owns final
provenance and the protected-workbench scan for this turn.
