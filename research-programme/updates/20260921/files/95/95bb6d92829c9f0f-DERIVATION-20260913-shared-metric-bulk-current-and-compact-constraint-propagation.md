# Shared-metric finite-width current and compact constraint propagation

Date: 2026-09-13. Private working derivation and numerical pilot.

## 1. What is new, and what is not claimed

The candidate finite-width scalar action now supplies an explicit averaged scalar
force, a horizontal-current profile, and consistent bulk initial metric data.
The compact initial constraint C0 and its full first time derivative C1 pass the
same 1e-10 numerical threshold for the GR-comparator and MTS metric-Gram branches.
There is also a conditional analytic cancellation for arbitrary compact tests,
not merely a fit to the seven test functions used in the computation.

This does NOT complete the old forced annular boundary problem, prove the full
GR limit, derive a unique parent regulator, or establish a causal evolution.
It is a bulk first-order consistency result for the explicitly chosen action
extension. The old 79/177-pair results and their failures remain unchanged.
The GR comparator here is the existing GR-plus-scalar stencil branch with the
additional MTS Gram factors removed, not an assertion that finite-h transport
already equals all of continuum Einstein-scalar theory.

Starting action and scope:
`DERIVATION-20260913-off-shell-finite-width-action-and-clock-coframe.md`.
Starting seal:
`source-intake/navier-stokes/20260913/annular-finite-width-full-scalar-final-integrity.json`.

## 2. A zero initial shift does not make the time links trivial

Use the preceding notation, with U=sqrt(1-2mu/R), kappa=0.1 in the numerical
fixture, and the initial slice P=0. The lapse N is positive. Let

    g_R = c_t = kappa U P1 / N,
    c = kappa U P / [N(1-kappa^2 U^4 P^2)].

For every common translation z in [-1/2,1/2], keep the same spacing h and matrices
B_fi, S_fi, omega_i. Set r_i(z)=r_i+delta z and a_f(z)=sum_i S_fi r_i(z).
Here a_f denotes an anchor radius, not the radial coframe scale.
On the initial slice the horizontal map has T_fi(0)=0 but

    J_fi = exp(g(r_i(z))-g(a_f(z))).

In particular, P=0 does not imply P1=0, g_R=0, or J=1.
There is one shared metric and one g(R), not a separately solved metric for each
translated scalar copy. g is fixed up to an irrelevant additive constant.

For compact physical-time variations, the direct coefficient term in the
spatial action has J ds=dt_i. Thus the J factor cancels in that direct metric
covector, even though it does not cancel in the scalar force or its time rate.
This extends the preceding zero-shift-history energy formula to this initial
slice without assuming the entire history has P identically zero.

## 3. Live canonical energy and the shared initial metric

Define, separately at each z,

    A_f = sum_i B_fi chi_i,
    d_i = sum_f S_fi A_f^2/(2h),
    e_i = omega_i p_i^2/(2r_i^2) + r_i^2 d_i.

For delta<h the scalar bands do not overlap. The live density at R in band i is

    epsilon(R) = w(z_i) e_i(z_i)/delta,
    z_i = (R-r_i)/delta,

and is zero in the gaps. This is initial canonical data, not a prescribed energy
function frozen through the dynamics. e_i depends on the whole translated
stencil, including both scalar and momentum profiles. Only under a metric-only
variation at fixed canonical matter coordinates is this e_i held fixed.

The local initial equations from the unchanged gravity bulk and this scalar
action are

    C0 = mu_R/(kappa U) - U epsilon = 0,
    P1 = -N_R/(kappa U) + N mu/(kappa R^2 U^3) + N epsilon/(R U).

They give an actual shared-metric preparation:

    mu_R = kappa (1-2mu/R) epsilon,
    g_R = -N_R/N + mu/(R^2 U^2) + kappa epsilon/R.

Once initial chi_i(z), p_i(z), a positive lapse, and one initial mass are given,
these are radial ODEs, not fitted C1 forces. The mass ODE is linear in mu:

    mu_R + (2 kappa epsilon/R) mu = kappa epsilon.

An integrating factor therefore provides an independent check on the numerical
preparation. Writing A=mu/(R^2 U^2), B=kappa epsilon/R also gives

    (ln U)_R = A-B,
    g(R)-g(L) = -ln[N(R)/N(L)] -ln[U(R)/U(L)] + 2 int_L^R A dR.

Positive-chart existence here is local/conditional and checked in the pilot.
No all-data or black-hole regularity theorem follows from these ODEs.

## 4. Derive the force and current before averaging

For each translated stencil define

    C_i = r_i^2 N_i U_i,
    q_i = C_i p_i/r_i^4,
    D_f = sum_i S_fi J_fi C_i,
    A_s,f = sum_i B_fi J_fi q_i.

The spatial scalar covector, auxiliary canonical momentum rate and direct
coefficient rate in physical node time are

    Gchi_i = -sum_f B_fi A_f D_f/(h J_fi),
    p1_i = Gchi_i/omega_i,
    d1_i = sum_f S_fi A_f A_s,f/(h J_fi).

For the interior pilot there is no added external scalar port force. A physical
boundary-source term would have to be derived and added explicitly, not fitted
to the constraint residual.

Importantly d1_i is the derivative of the coefficient evaluated after pulling
each factor to node i's physical time. It is not obtained by differentiating a
same-coordinate-time bare A_f and discarding the time links. Hence

    e1_i = omega_i p_i p1_i/r_i^2 + r_i^2 d1_i,
    N_i U_i e1_i = q_i Gchi_i + C_i d1_i.

The oriented pair current from the full action is

    I_fi = A_f [S_fi C_i A_s,f - B_fi q_i D_f]/h.

Its anchor cancellation is algebraic:

    sum_i J_fi I_fi = A_f(D_f A_s,f-A_s,f D_f)/h = 0.

Set G_fi=exp(g_i+g_anchor) I_fi and let the oriented indicator be +1 on
(anchor,target) for target>anchor and -1 on (target,anchor) otherwise. Then

    K_z(R) = exp(-2g(R)) sum_fi G_fi oriented_indicator_fi(R),
    Kbar(R) = int w(z) K_z(R) dz.

This formula is implemented as an integral over the original translated links,
not inferred by integrating a desired conservation residual. Independent direct
oriented quadrature checks the spectral-antiderivative implementation.

## 5. The weak current identity and C1 cancellation

Differentiate the oriented indicators distributionally. Endpoint contributions
give minus G_fi delta(R-r_i). Anchor contributions cancel by sum_i J_fi I_fi=0.
Consequently

    (K_z)_R + 2 g_R K_z
      = -sum_i (q_i Gchi_i+C_i d1_i) delta_Dirac(R-r_i(z)).

Average with fixed w. Since every copy uses the same g(R),

    Kbar_R + 2 g_R Kbar + N U epsilon1 = 0,
    epsilon1(R) = w(z_i) e1_i(z_i)/delta.

For smooth data within the bands this is the corresponding pointwise identity
away from band endpoints; it remains a weak identity through the endpoints.
These statements assume sufficient integrability for differentiation and
averaging, positive N,U, and invertible time links. No physical radial boundary
term has been suppressed in the compact-test statement.

The initial metric velocity from the P variation is

    f = mu1 = -kappa U Kbar/N.

The lapse Euler equation contains the connection variation Kbar c_N. Although
c_N is zero at P=0, its time derivative there is -g_R/N. Therefore the full
first constraint derivative is

    C1 = d_t[mu_R/(kappa U)-U epsilon] - Kbar g_R/N.

Using C0, the derived P1, and f, direct algebra yields

    C1 = -[Kbar_R+2g_R Kbar+N U epsilon1]/N = 0.

This is the desired conditional bulk mechanism. It is not an extra plateau,
closure equation, or a tuned cancellation. In particular, omitting the last
lapse/connection term leaves Kbar g_R/N rather than zero. Setting all J to one
while retaining the same derived geometry also breaks the cancellation.

## 6. What was actually solved and tested

The scalar, momentum, matrices and mass seed are sourced from the immutable
original79 canonical-port snapshots already used in the preceding layer work:

- `source-intake/navier-stokes/20260912/annular-interface-layer-clock-attempt03/GR_source_snapshot.npz`
- `source-intake/navier-stokes/20260912/annular-interface-layer-clock-attempt03/metric_Gram_source_snapshot.npz`

Two explicit initial extensions were tested: layer-flat, and layer-linear using
the centered/one-sided gradients of those node values. Both recover the archived
values and energy at z=0. Neither extension is claimed uniquely parent-selected.
Layer profiles remain dynamical; the flat initial choice does not remove their
variations. The source data are not a new experimental dataset.

The interval extends from r_0-delta/2 to r_16+delta/2. The archived first-node mass
is assigned to that enlarged left endpoint as a new pilot initial condition.
The common positive lapse is 0.85 exp(slope*(R-r_0)). It is a gauge/test choice,
not the old forced clock history. No comparison has been made by silently
retuning physical coefficients, changing h, or relaxing the 1e-10 threshold.

Five cases per branch:

| Case | Width | Weight | Lapse slope | Initial extension |
|---|---:|---|---:|---|
| 0 | 1/128 | beta22 | 0.1 | linear |
| 1 | 1/256 | beta22 | 0.1 | linear |
| 2 | 1/128 | beta23 | 0.1 | linear |
| 3 | 1/128 | beta22 | 0 | linear |
| 4 | 1/128 | beta22 | 0.1 | flat |

Both branches retain h=1/64 and their exact inherited Gram/kinetic weights.
The common mass profile is solved over all bands and gaps with DOP853. A spectral
antiderivative integrates weighted link currents in z; this does not project
the metric velocity back into the old 79/177-pair spaces. Primary/higher tests
use degrees 28/40 and radial quadrature orders 24/36, split at band boundaries
and compact-test breakpoints. There are seven test functions per case and order,
140 C0 values and 140 C1 values in total.

Main run results, with all ten compact cases passing:

| Quantity | Maximum over the matched matrix |
|---|---:|
| Compact C0 residual | 7.40e-15 |
| Full compact C1 residual | 7.41e-16 |
| Pointwise current/power identity error | 1.83e-14 |
| Independent direct-link current integral error | 8.68e-18 |
| C1 with connection-time term omitted | 8.55e-6 to 1.20e-5 |
| C1 with J incorrectly set to one | 1.72e-5 to 2.41e-5 |

Minimum F exceeds 0.6593 and sampled minimum J exceeds 0.9976. These small
identity residuals are not observational error bars, full-theory accuracy,
interval certificates, or evidence that MTS outperforms the comparator.

The final independent verifier additionally checks:

- A linear integrating-factor mass solution, separately from the radial ODE.
- Direct metric variations of the initial action (14 per branch).
- The shared metric/clock identity without using the g ODE as its definition.
- Scalar-force extraction from the full spatial action using narrow normalized
  physical-time variations, retaining J and the exact positive coframe.
- Energy-rate extraction with factors resynchronized to each physical node time.
- Provenance, executed-source hashes, citations, finite arrays and protected files.

The physical-time force controls use an independent local manufactured history
c(R,t)=g_R(R)t, fixed initial mu,N, and chi=chi0+q t. They are action-variation
controls at this slice, NOT a coupled spacetime solution. Extrapolation of two
time-window widths removes the leading even-width error. The sealed report is
the authority for their completion and actual errors.

Implementation:
`scripts/annular_finite_width_bulk_current_20260913.py`.
Main runner:
`scripts/derive_annular_finite_width_bulk_current_20260913.py`.
Independent verifier:
`scripts/verify_annular_finite_width_bulk_current_20260913.py`.
Main evidence:
`source-intake/navier-stokes/20260913/annular-finite-width-bulk-current-attempt01/status.json`.

## 7. Next stage: boundary completion, not another bulk-fit loop

There is now a concrete bulk construction to carry forward. Its next test is to
derive the radial source/clock boundary action on the expanded scalar support,
reconcile it with the original forced annulus, and reprepare with those actual
boundary conditions. The present truncated-link current has no added external
current outside its full support; that does not reproduce the old driven ports.

Retain the complete layer scalar profiles and the kinetic plus transported
temporal boundary terms. Do not infer independent port forces from global
energy conservation alone or fit them to C1 rows. With boundary compatibility
established, attempt C2 and a short controlled evolution, checking both branches
and higher quadrature. Until then, full_first_jet_closed, full_GR_limit_proven,
full_physical_radial_port_action_signed and valid_for_physics_claim remain false.

The regulator, initial layer extension and full causal initial-value formulation
still need parent-level justification. A compact initial propagation identity
does not by itself remove those obligations.
