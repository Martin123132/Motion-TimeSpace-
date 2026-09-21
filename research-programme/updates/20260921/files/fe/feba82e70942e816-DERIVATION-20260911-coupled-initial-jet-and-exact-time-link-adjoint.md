# Coupled initial jets and the time-link action adjoint

Private continuation, 11 September 2026 (Europe/London).
No physical pass, continuum theorem, public update or numerical evolution.

## 1. Actual advance

The extra mass Euler equations now have an explicit repair: a nonzero
action-derived shift rate. We solve it together with scalar acceleration
and first lapse preservation, rather than repairing only the shift rows.

We also derive the nonunit-time-Jacobian Gram contributions from the FULL
time-integrated action. Direct mass/lapse Jacobians cancel under a change
to physical time; scalar and shift equations retain nontrivial factors.
This permits numerical coupled Gram initial jets without a plateau axiom
or new fitted coupling. It is not yet a Gram interval/evolution certificate.

Refinement exposes a specific remaining problem: one exceptionally small
lapse Schur eigenvalue in BOTH GR and Gram. Small residuals do not make
the resulting very large lapse rates reliable. That is the next target.

## 2. Scope and frozen enriched spaces

Use the canonical annular branch, kappa=1/10 and Lambda=m_chi=b2=b3=0:

    F=1-2 mu/R, rho=1/(kappa N F^(3/2)),
    m=R^2/(N sqrt(F)), p=R^2 N sqrt(F),
    q=chi_t, w=chi_R, s=kappa R^2 F q w.

Q is stored quadrature; V is the old mass reconstruction; H is the
previous bubble lift; A=[V,H]; S contains old and added broken shift tests.
The initial metric-seeded maps are FROZEN, not moving basis functions.
They are realized binary quadrature/derivative/trace maps, not a new
continuum or nonsmooth-spacetime construction certificate.

Free mass variations exclude the inner endpoint. Its mass covector is a
boundary reaction, not an equation set to zero. Added mass bubbles vanish
at original nodes/endpoints. Original scalar endpoint accelerations and
outer clock VALUE are retained. The clock RATE is needed at a later jet
order and is not replaced by a fitted input.

The weak bulk action retains its physical beta^2 boundary flux and the
inherited smooth/weak quadrature distinction. Their first variation and
first-time derivative of the lapse covector vanish at beta=0. They cannot
be discarded at higher orders on that account.

## 3. Coupled GR initial law

At beta=0 but unrestricted beta_t:

    Pi_mu[h]=Q[rho beta h],
    (Pi_mu[h])_t=Q[rho beta_t h].

Write beta_t=S z, mu_t=A u and P=Q[rho S^T A]. Then

    P u=Q[rho S^T s],
    P[:,free_mass]^T z=F_mu[free_mass].

F_mu includes the clock boundary term and all enlarged mass variations.
The second equation repairs the previously nonzero added mass Euler rows.
One shift-rate coefficient remains free. We solve the bordered FAMILY

    [P[:,free_mass]^T; inner_trace(S)] z=[F_mu[free_mass]; theta],
    theta=beta_t(R_inner).

Theta=0,+0.001,-0.001 are diagnostic members, not a parent-selected
boundary condition. The inner mass reaction is retained and reported.

Let V_s be free scalar velocity reconstruction and L the lapse hats:

    M=Q[m V_s^T V_s], D=Q[m(q/N) V_s^T L],
    E=Q[m(q/N)^2 L^T L], T=Q[m w V_s^T S],
    B=Q[(rho/N)(mu_t-s) L^T S].

After retaining prescribed endpoint accelerations, free scalar
acceleration a and lapse rate n satisfy

    [ M   -D  ] [a] = [ f_s+T z ],
    [-D^T  E  ] [n]   [ f_N+B z ].

The scalar source is its spatial force minus
Q[V_s^T m q mu_t/(R F)] and the prescribed endpoint kinetic columns.
The lapse source contains the negative of

    Q[L^T {mu_t,R/(kappa sqrt(F))
      +(mu_R/(kappa R F^(3/2))-R q^2/(2N^2 F^(3/2))
        +R w^2/(2 sqrt(F))) mu_t
      -R^2 sqrt(F) w q_R}],

plus the prescribed endpoint acceleration columns. B z is essential:
differentiating the lapse Euler equation contributes
-Q[L^T rho beta_t(mu_t-s)/N]. The old lapse tangent cannot be reused.

The Schur matrix has an exact finite projection representation:

    X=M^-1 D, U=(q/N)L, R_s=U-V_s X,
    E-D^T M^-1 D=Q[m R_s^T R_s].

It is a positive semidefinite projection Gram matrix, not a new physical
kinetic term. Small eigenvalues indicate lapse products almost represented
by the free scalar space. Calling them physical gauge freedom requires an
additional action/boundary argument, not just an eigenvalue calculation.

## 4. GR certificate: existence, not precision or evolution

The 16-interval inherited GR root box has verified inverses for P, the
bordered shift-rate matrix and the scalar/lapse matrix. Both affine
columns obey the free mass equations, scalar/lapse equations and trace
condition. Independent complex-step differentiation of the weak action's
momenta and lapse covector agrees at the tested midpoints.

The coupled midpoint condition number is about 1.324e11. The largest
enclosed lapse-rate width across affine columns is about 2810.82. These
are BROAD existence enclosures, not useful error bars or timestep bounds.
The projection-Gram Schur refinement improves its inverse contraction but
does not cure the wide source enclosures. Probe02 preserves that result.
First lapse preservation is not a proof of preservation at later times.

## 5. Vary the time-integrated Gram action

For each factor f and participating node i, let T_fi(t) be transported time
and J_fi=partial_t T_fi>0. Along each oriented radial path,

    partial_R T=c(T,R), c=beta/(N^2 F-beta^2).

Assume a regular positive chart and locally invertible time transport.
Use compactly supported time variations or retain their boundary terms.
Define

    A_f=sum_i B_fi chi_i(T_fi),
    D_f=sum_i S_fi J_fi C_i(T_fi),
    C_i=R_i^2 N_i sqrt(F_i) at beta=0,
    A'_f=sum_i B_fi q_i(T_fi) J_fi,
    S_G=-integral dt sum_f A_f^2 D_f/(2h).

Vary J C(T) as partial_t[C(T) delta T]. Integration by parts gives

    delta S_G|transport=integral dt sum_fi I_fi delta T_fi,
    I_fi=A_f [S_fi C_i(T_fi) A'_f-B_fi q_i(T_fi) D_f]/h.

The temporal boundary is
-[sum_fi A_f^2 S_fi C_i(T_fi) delta T_fi/(2h)]. The factor identity is

    sum_i J_fi I_fi=0,

not the old unweighted identity unless J=1. Direct variations of chi and C
are additional to this transport variation.

## 6. Physical-time pullback at beta(t0,R)=0

At a zero-shift slice, even with beta_t nonzero,

    T_fR(t0)=t0,
    J_fR(t0)=exp(integral_anchor^R beta_t/(N^2 F) dr).

For an arbitrary connection perturbation,

    delta T_fi(t)=J_fi(t) integral_anchor^Ri
                           delta c(T_fR(t),R)/J_fR(t) dR.

Changing the time integration variable to tau=T_fR(t) contributes another
factor 1/J_fR. Since partial_beta c=1/(N^2 F) on the slice, the Gram shift
covector is

    G_beta[b]=sum_fi I_fi J_fi integral_anchor^Ri
                                 b/(N^2 F J_fR^2) dR.

The square in J_fR^-2 is essential. Reverse path orientations are retained.
The mass-rate equation is P u=Q[rho S^T s]-G_beta[S].

For a DIRECT coefficient variation, J_fi in the density cancels the
physical-time change of measure. Therefore at this slice

    d_i=sum_f S_fi A_f^2/(2h),
    G_mu[h]=sum_i R_i N_i d_i h_i/sqrt(F_i),
    G_N[eta]=-sum_i R_i^2 sqrt(F_i) d_i eta_i.

The transport contribution to these metric covectors is zero there because
partial_mu c and partial_N c are proportional to beta. This is a full
time-integrated variational result, not a unit-J replacement of the raw
integrand. The direct scalar force instead retains

    G_chi,i=-sum_f B_fi A_f D_f/(h J_fi).

The mass equations first determine z, including ordinary Gram mass terms.
Then the nonunit-J shift source determines u. No new fitted coefficient
or beta_t=0 assumption is introduced.

## 7. First Gram lapse derivative

Each coefficient's amplitude is pulled back by t=T_fi^-1(tau), so define

    dot_dtilde_i=sum_f S_fi A_f A'_f/(h J_fi).

It generally differs from the unit-J density derivative. At beta=0,

    dot G_N[eta]
      =sum_i eta_i [R_i d_i mu_t,i/sqrt(F_i)
                   -R_i^2 sqrt(F_i) dot_dtilde_i]
        -2 sum_fi I_fi J_fi integral_anchor^Ri
                       eta beta_t/(N^3 F J_fR^2) dR.

The last term is necessary even though the transport part of G_N itself
vanishes on the slice. In fact

    (partial_N c)/(partial_beta c)
          =-2 N F beta/(N^2 F+beta^2),

whose time derivative at beta=0 is -2 beta_t/N.

On this canonical branch the scalar/lapse matrix in section 3 is unchanged.
Add G_chi to the scalar source and subtract dot G_N from the lapse source.
This constructs the Gram initial-jet diagnostic. Its dependence on theta
is nonlinear through the time Jacobians, unlike the affine GR family.

These formulas do not supply a full nonlinear time-discrete action,
global history or local residence theorem. The radial integrals and
nonlinear variational discretization still need error control.

## 8. Independent tests and negative control

The smallest GR and Gram cases solve the coupled midpoint equations at
theta=0,+/-0.001. The GR solutions lie inside the independently enclosed
GR families. Radial orders 8 and 16 differ by at most about 1.25e-8 in
the Gram lapse rate at 16 intervals. This is a CONTROL, not a quadrature
error certificate or a nonlinear discrete-action certificate.

An independent soluble connection c(t,R)=t g(R), hence T=J t, uses linear
time-dependent scalar/coefficient data and a Gaussian variation. Raw
delta-J variation, time integration by parts, and the physical-time adjoint
are evaluated separately. A boosted rate with max|log J|=0.2 gives
relative agreement about 1.63e-15 and 3.62e-16 on GR/Gram input data.
Omitting J_fR^-2 causes about 1.47e-9 absolute error against a correct
variation near -1.83e-8. The wrong formula is measurably rejected.

A separate nonlinear ADM coefficient/connection calculation differentiates
the full pulled-back lapse covector on a compatible soluble clock
background. It agrees with section 7 to about 3.18e-20 absolute. Its
nonzero transport derivative is about 5.45e-11. This checks a term omitted
by a unit-J substitution, not a full constructed spacetime solution.

Do not count the lapse-control script's constructed zero node-bubble array
as independent geometry validation. The seal evaluates the bubble
polynomials at actual knots instead.

## 9. Paired refinement: the new specific obstacle

Untuned theta=0, saved sample0, code-normalized midpoint quantities:

| Intervals | GR max reconstructed lapse rate | Gram max reconstructed lapse rate | Schur condition, approximately |
| --- | ---: | ---: | ---: |
| 16 | 17.7978 | 82.4980 | 3.19e6 |
| 32 | 7.13015 | 16.2371 | 5.01e7 |
| 64 | 20754.2 | 9359.65 | 7.60e13 |

The 64-interval scalar residuals remain order 1e-14 and lapse residuals
order 1e-16. This does NOT certify stability: the almost singular matrix
amplifies a tiny source component into a huge rate. Neither branch is
approved for evolution from this test.

At 64 intervals the smallest eigenvalue is about 6.85e-20; the next is
about 3.12e-12. As a READ-ONLY diagnostic, subtracting the first eigenvector
component leaves maximum lapse coefficients about 5.14 (GR) and 8.77
(Gram). No mode was removed from any saved solution, and no pseudoinverse,
regularization or damping was used to manufacture a pass. Floating
eigenvalues here are not certified signs or ranks.

This shared problem is not evidence against MTS alone. We also have NOT
proved it is harmless gauge freedom rather than broken discrete
compatibility. That distinction is now testable in a specific matrix and
source, not a generic missing-coupling discussion.

## 10. Next target and evidence

Resolve the near-null lapse direction through the existing boundary/clock
variational law or a compatible discrete identity, with GR and Gram
controls. Selecting theta merely to minimize a residual is not a
parent-derived boundary law. Then certify an initial jet and persistence.
Do not restart unspecified coupling searches: the time-link adjoint is
now explicit. The old initial data, clock and endpoint inputs remain intact.

Sources and reproducible outputs:

- `DERIVATION-20260910-joint-weak-action-and-compatible-mass-lift.md`
- `scripts/annular_initial_shift_jet_20260911.py`
- `scripts/derive_annular_initial_shift_jet_20260911.py`
- `scripts/annular_initial_shift_schur_20260911.py`
- `source-intake/navier-stokes/20260911/annular-initial-shift-jet-probe01/status.json`
- `source-intake/navier-stokes/20260911/annular-initial-shift-jet-probe02/status.json`
- `scripts/annular_time_link_adjoint_20260911.py`
- `scripts/derive_annular_time_link_adjoint_20260911.py`
- `source-intake/navier-stokes/20260911/annular-time-link-adjoint-attempt01/status.json`
- `scripts/verify_annular_time_link_lapse_20260911.py`
- `source-intake/navier-stokes/20260911/annular-time-link-lapse-control-attempt01/status.json`
- `scripts/verify_annular_initial_mesh_20260911.py`
- `source-intake/navier-stokes/20260911/annular-initial-mesh-control-attempt01/status.json`

Run primary scripts with the dedicated environment, -B, one BLAS thread,
and a fresh attempt name where supported. Probe02 explicitly substituted
refine_initial_gr_jet for initial_gr_jet via an import hook before invoking
the same GR runner. Its imported helper is hash-recorded; immutable sources
were not altered. The final seal records executed snapshots and this note.

All work is private, confined to post-checkpoint-work. No GitHub action,
simulation, delegation, frozen-workbench edit or remaining owned worker.
