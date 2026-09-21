# A covariant full scalar discretization, not another frozen enrichment

Private/local continuation, 12 September 2026. Read
`DERIVATION-20260912-history-Ward-identity-and-scalar-projection.md` for the
preceding identity and rejected frozen-space trial. No evolution, empirical
physics claim, GitHub action, or change to the protected workbench.

## 1. What was actually accomplished

1. Constructed a kinetic-compatible scalar pairing, removing its identified
   kinetic acceleration defect for the whole momentum-rate space. This does
   not remove the other Ward defect, and is not adopted as a coupled repair.
2. Derived an alternative first-order representation of the SAME continuum
   minimal scalar action. Discretized its complete spatial term using the
   existing covariant time-link construction, not just the Gram correction.
3. Checked actual action derivatives, finite time-coordinate transformations,
   temporal boundary work, a recovered scalar mass-flux law, and smooth-mesh
   consistency, with the same base construction in GR and MTS controls.
4. Evaluated a source-backed nodal scalar jet on prescribed old metric jets,
   including inherited boundary-force samples. Its scalar energy exchange
   obeys the derived identity at every node, without an off-space test family.
5. Derived the new initial lapse-constraint Jacobian and actually solved its
   19 rows by changing only the dependent mass profile, keeping the inner mass
   and sampled scalar/auxiliary inputs fixed. Higher quadrature checks these
   C0-only roots. They are NOT complete boundary-compatible initial data.

The earlier numerical working branch remains
annular-acceleration-trace-completion-attempt02. The new action and its
C0-only candidates are separate evidence, not a replacement certificate.

## 2. The kinetic mismatch can be removed algebraically

At P=0 set A0=N0 sqrt(F0)/R^2 and K0=1/A0. Choose a continuous scalar
configuration space Q and its momentum trial space P_s=K0 Q, with K0 frozen
at the initial geometry. With positive weights W,

    M_s=P_s^T W Q=Q^T W K0 Q,
    A0 P_s=Q,
    Pi_Q=Q M_s^(-1) P_s^T W.

Weighted normalization makes M_s the identity to roundoff. The old 74
configuration directions are retained in span; only one additional direction
is needed to represent all 22 requested continuous source directions. The
new dimension is 75 in both branches. The old momentum trial space is
deliberately replaced: it is not falsely claimed retained. This is a new
finite approximation, not a new physical kinetic constant or a K_seed refit.
The physical initial pi profile and initial mu_t,P_t,chi_t are retained to
the recorded numerical tolerances.

For the full scalar acceleration, independently verify

    chi_tt=Pi_Q[A0 pi_t+D],
    D=(N_t sqrtF/R^2-N mu_t/(R^3 sqrtF))pi
          +kappa N F^(3/2)P_t chi_R.

All continuous lapse/mass drift terms are included. The possibly broken
P_t chi_R term is NOT silently inserted into the continuous configuration
space. K0 remains a frozen basis weight, not an undeclared moving frame.

| Primary pointwise acceleration diagnostic | GR | MTS |
|---|---:|---:|
| Old kinetic-rate projection defect | .000354895903 | .044474073645 |
| New kinetic-rate projection defect | 1.67e-16 | 1.95e-16 |
| New continuous-drift defect | 2.38e-20 | 2.38e-20 |
| Remaining full acceleration defect | 1.425e-6 | 1.425e-6 |

The remaining acceleration defect is the shift drift. Its L2 norm is about
9.93e-8 at both quadratures. However the compact MTS Cddot residual only
changes from .0064413 to .00565237; E_chi[(v_chi)_t] still contributes about
.00564083. Full 19-row Cddot worsens to .01932658 MTS and .00020723 GR.
First-jet gates remain true, full second-jet gates remain false. This fixes
a specific mechanism, not the complete system. Simply enlarging Q again
would repeat the frozen-family feedback problem.

## 3. Rewrite the continuum scalar action before discretizing

Keep F=1-2mu/R, beta=kappa N F^(3/2)P, and d=1-beta^2/(N^2 F)>0.
Define

    c = beta/(N^2 F-beta^2),
    C = R^2 N sqrtF d,
    B = R^4/C = R^2/(N sqrtF d).

The exact identity is

    R^2/(2N sqrtF) (chi_t-beta chi_R)^2
          -R^2 N sqrtF chi_R^2/2
      = B chi_t^2/2 - C (chi_R+c chi_t)^2/2.                (1)

No new coefficient is fitted: B*C=R^4 follows from the metric. The
horizontal derivative chi_R+c chi_t is the derivative along T_R=c(T,R).
This is a rewriting of the existing minimal scalar sector, not a change
to Newton's constant or proof of the full MTS parent theory.

Introduce a different auxiliary scalar momentum p:

    L_scalar = p chi_t - C p^2/(2R^4)
                         -C(chi_R+c chi_t)^2/2.             (2)

Eliminating p gives p=B chi_t and recovers (1) exactly. It is essential that

    p != pi_old away from P=0,
    pi_old=R^2/(N sqrtF)(chi_t-beta chi_R).

They agree at P=0, so the initial sampled auxiliary values can be shared.
Their time derivatives need not agree even there: when P=0,
(p-pi_old)_t=R^2 beta_t chi_R/(N sqrtF). Do not reuse the old pi evolution
equation for p, or add the old beta*pi*chi_R term to (2). That double-counts
the spatial transport coupling.

## 4. The new finite scalar action

Use the inherited scalar nodes R_i and positive trapezoid weights omega_i.
For the GR base, take nearest-neighbour factors B_fi=(-1,+1), coefficient
sampling S_fi=(1/2,1/2), and anchor a_f=sum_i S_fi R_i. For the MTS
comparison concatenate precisely the old Gram factor/sampling matrices;
do not change their amplitudes or treat their h^4 remainder as a physical
screening scale.

Let T_f,R=c(T_f,R), T_f(s,a_f)=s and J_f=partial_s T_f. Define

    A_f(s)=sum_i B_fi chi_i(T_fi(s)),
    D_f(s)=sum_i S_fi J_fi(s) C_i(T_fi(s)).

The finite action is

    S_scalar,h = integral dt sum_i omega_i
                     [p_i chi_i,t-C_i p_i^2/(2R_i^4)]
                    -integral ds sum_f A_f(s)^2 D_f(s)/(2h). (3)

The scalar unknowns are independent nodal histories, not coefficients of
the old 75/125-function scalar space. This replaces the entire old finite
scalar block. The gravity action is still the sourced gravity action, but
the scalar contribution to its constraints and boundary work must now be
re-derived. Old prepared roots and finite certificates do not transfer.

### Time-coordinate covariance is built into the action

For H(t,R) with H_t>0, R fixed,

    chi'_i(t)=chi_i(H_i(t)),   p'_i(t)=p_i(H_i(t)),
    C'=H_t C(H),              B'=B(H)/H_t,
    c'=(c(H)-H_R)/H_t.

The nodal canonical kinetic term transforms as a time density OFF SHELL.
The spatial conjugacy is

    H(T'_fi(s),R_i)=T_fi(H(s,a_f)),
    H_t(T'_fi,R_i)J'_fi(s)=J_fi(H(s,a_f))H_t(s,a_f).

Thus each full spatial factor is a time density at its anchor. This
applies to the base factors as well as to the old Gram factors. It does
not require the time-coordinate generator to lie in an enlarged scalar
trial space. It is invariance under the stated time relabellings, not a
claim of arbitrary spatial-diffeomorphism invariance of a fixed lattice.

For a finite time interval, match the physical node/anchor endpoint events.
Identical coordinate-time bounds in two time charts are generally different
physical windows. Both canonical [sum omega_i p_i delta chi_i] work and the
existing transported-Y endpoint work remain. A nonlocal history action is
still not automatically a causal ordinary Hamiltonian initial-value problem.

## 5. Derive the scalar and metric exchange equations

Use the same inverse-time definitions of d_i,G_chi,i,K as the previous
history derivation, now summing over the ENTIRE spatial factor set. Set

    a_i=omega_i p_i^2/(2R_i^4),
    E_C,i=-a_i-d_i,
    G_y=K c_y-sum_i delta(R-R_i)(a_i+d_i)C_y,   y=mu,N,P.

Then, with external scalar force samples rho_i displayed explicitly,

    chi_i,t=C_i p_i/R_i^4,
    omega_i p_i,t=G_chi,i+rho_i,
    mu_t=(H_gravity)_P-G_P,
    P_t=-(H_gravity)_mu+G_mu,
    C_gravity+G_N=0.                                      (4)

The nodal scalar Euler equations have all their nodal variations, so there
is no missing Galerkin test-space residual in that scalar block. The full
coupled gravity constraints and metric projection can still fail; (4) is
not their numerical solution.

The exact algebraic identity behind the nodal Ward cancellation is

    -C_i (E_C,i)_t
      +(-omega_i p_i,t+G_chi,i)chi_i,t
      +omega_i(chi_i,t-C_i p_i/R_i^4)p_i,t
       = C_i d_i,t+G_chi,i chi_i,t.

The right-hand side is exactly the nodal source in the previously derived
connection-current Ward identity. With sources, the remaining term is
the prescribed power rho_i chi_i,t, not an unrecorded failure of conservation.

### The original scalar mass flux reappears, rather than being inserted

On an affine diagnostic chi=w R+q t, constant C, c=c_t=0, every base edge
has I_left=+C q w and I_right=-C q w. The oriented current is K=-C q w
on both halves of the edge. Therefore at P=0

    mu_t=-c_P K=kappa R^2 F q w,

which is the old local scalar mass flux expressed using q=chi_t. The base
transport now owns this coupling. Setting that transport to zero or also
retaining the old cross term would respectively lose or double-count it.
This diagnostic is exact for the stated affine fields; general finite-grid
solutions and their boundary traces still need checking.

## 6. What the new action tests actually establish

There are 33 validation checks in the action run, including both branches.
These are off-shell/manufactured histories, not measured data or solutions.

- The continuum decomposition, auxiliary elimination and nodal time-density
  law are checked symbolically.
- Ten actual action-variation tests cover each field and a mixed direction,
  at nonzero P. Maximum Richardson derivative error is 4.08e-12.
- The full adjoint equality including BOTH temporal boundary contributions
  agrees to at most 1.39e-17. The kinetic endpoint contribution is genuinely
  nonzero, about .0002084 in the scalar/mixed directions.
- Independent pulled-metric reconstruction and transport integration give
  matched-physical-window action errors of 1.83e-17 GR and 2.73e-17 MTS.
- Dropping J is detected at about 8.97e-7. Giving B the wrong time weight
  is detected at about 6.97e-5.
- Smooth N16/32/64 tests with nonzero c show decreasing base spatial and
  kinetic errors. The base spatial error falls 1.2411e-5 ->3.1157e-6
  ->7.7973e-7; the untransported-base error instead stays about 1.17e-4.
- The inherited Gram extra is positive and falls roughly as h^4 in this
  smooth test. This is numerical consistency, not a derived physical GR limit.

Floating-point agreement is not an interval bound or a universal stability,
hyperbolicity, causal-existence or black-hole regularity theorem.

## 7. Use the existing N16 source profile, with the assumptions explicit

Two separate calculations are stored; do not conflate them.

### A. Scalar jet on the prescribed OLD metric jet

Take the old sampled chi,p=pi_old and old metric's P=0 two-sided time jet.
J and L are reconstructed using the inherited global connection primitives.
The old endpoint scalar force and force-rate samples are carried explicitly;
this is NOT a derivation of a full new boundary history.

Compute p_t from (4), then chi_tt, G_chi,t and p_tt. The initial chi_t agrees
with the old sampled velocity. All 17 scalar equations and the differentiated
nodal energy identity close, including the source power. Maximum energy
identity errors are 5.21e-18 (initial) and 1.12e-15 (differentiated).
The endpoint source power itself is about .0088 and is NOT discarded.

This is a scalar solution jet on a prescribed geometry, not a coupled
MTS/GR solution. In particular, the metric jet cannot remain prescribed
when solving the new gravity equations.

### B. New C0-only mass preparation

At P=0 the new scalar lapse source is

    -sum_i eta_i sqrt(F_i) e_i,
    e_i=omega_i p_i^2/(2R_i^2)+R_i^2 d_i.

The e_i are independent of mu for fixed sampled scalar/auxiliary inputs.
Add 19 dependent mass directions X_j(R)=integral_Rin^R eta_j(r)dr; these
all preserve the inner mass. Use the existing integrated-gravity finite
functional, plus the new nodal scalar source. Its exact mass Jacobian is

    DC0[eta](delta mu)
      = Q[eta mu delta_mu/(kappa R^2 F^(3/2))]
          -Q[eta_R delta_mu/(kappa sqrtF)]
          +[eta delta_mu/(kappa sqrtF)]_in^out
          +sum_i eta_i e_i delta_mu_i/(R_i sqrtF_i).

The analytic Jacobian is independently checked by complex step. Newton
takes two updates, with condition number about 258, no source-amplitude fit
and no loss of the positive chart.

| New action's 19-row C0-only preparation | GR | MTS |
|---|---:|---:|
| New C0 on old mass profile | .01271333531 | .01276759009 |
| Reprepared C0, primary | 4.07e-14 | 6.90e-14 |
| Reprepared C0, higher quadrature | 1.51e-13 | 9.00e-14 |
| Maximum dependent mass change | 1.521e-5 | 1.525e-5 |

The inner mass and sampled scalar/auxiliary inputs stay fixed. First and
second jets have NOT been recomputed on these prepared mass profiles.
At the old lapse, the outer clock misses by about 8.90e-7 and the outer
scalar drive by about -1.37e-8. The C0 root is not full initial data.

## 8. Boundary coupling and the next actual solve

For the new full spatial action the endpoint connection current is

    K_b=n_b [C_b d_b,t+G_chi,b chi_b,t],  n_in=-1,n_out=+1,
    mu_b,t=-c_P,b K_b  at P=0.

The C_b d_b,t term is essential: base coefficient sampling includes the
endpoints, unlike the old Gram-only simplification. The source-backed old-
metric jet gives an inner mass-drive gap about 1.52e-4 in BOTH branches.
This is a real finite preparation/boundary mismatch, not a local-GR pass.
It is not evaluated on the new C0-only mass root and must not be reported
as that root's recomputed flux.

For prescribed outer clock C_out and scalar velocity v_out, the exact
P=0 compatibility formulas are

    N_out=C_out sqrt(F_out),
    p_out=R_out^2 v_out/(C_out F_out).

They require about a 1.78e-6 relative change of the outer auxiliary value
on these C0-only roots. The formulas are verified but NOT applied: changing
p_out also changes the constraint source and requires a joint solve.

NEXT: derive the complete metric/port first variation for action (3), and
jointly prepare the new 19 lapse rows, outer clock/scalar drive and inner
mass flux with the same sourced boundary protocol. Distinguish source-owned
free data from boundary-dependent momenta. Rebuild any required metric
trace spaces for the FULL coefficient/current family; do not copy the old
Gram-only endpoint cancellation or the old scalar equations. Then recompute
P_t, J, p_t, mu_t and all Cdot rows, with matched GR and independent
quadrature. Cddot and time evolution wait for that consistent first jet.

## 9. Evidence

- `scripts/annular_scalar_kinetic_pair_20260912.py`
- `scripts/derive_annular_scalar_kinetic_pair_20260912.py`
- `scripts/verify_annular_scalar_kinetic_ward_20260912.py`
- `scripts/annular_covariant_scalar_action_20260912.py`
- `scripts/derive_annular_covariant_scalar_action_20260912.py`
- `scripts/verify_annular_covariant_scalar_source_jet_20260912.py`
- `scripts/verify_annular_covariant_scalar_preparation_20260912.py`
- `source-intake/navier-stokes/20260912/annular-scalar-kinetic-pair-attempt01/status.json`
- `source-intake/navier-stokes/20260912/annular-scalar-kinetic-ward-control-attempt01/status.json`
- `source-intake/navier-stokes/20260912/annular-covariant-full-scalar-action-attempt01/status.json`
- `source-intake/navier-stokes/20260912/annular-covariant-scalar-source-jet-attempt01/status.json`
- `source-intake/navier-stokes/20260912/annular-covariant-scalar-preparation-control-attempt01/status.json`

All runs are private, bounded, one BelowNormal single-core worker at a time.
Old files and completed evidence are preserved. The final integrity seal
and resume snapshot keep this action candidate distinct from the old branch.
