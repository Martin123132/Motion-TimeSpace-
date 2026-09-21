# Local gauge-error law and trace-preserving trial

Private derivation, 2026-09-12. Extends the new finite scalar-action candidate,
not the old passing first-jet action branch. No publication, evolution,
physical fit, black-hole solution, or full GR/Newton limit is claimed.

## 1. Result in plain language

We derived the local constraint error as two explicit canonical
representation errors, not an unexplained residual. Adding ordinary
polynomial detail reduces the interior error but badly damages boundary
flow. A boundary-preserving construction avoids that problem and, at its
higher tested order, reduces the full local drift by about 45% in BOTH
GR-plus-scalar and MTS-plus-scalar.

That is a limited numerical improvement, not a passed consistency gate.
The better trial has 177 mass canonical pairs instead of 79. Its maximum
C1 is still about 1.8e-8 against the unchanged 1e-10 test tolerance.
The existing smaller reference and old working branch remain intact.

The derivation also supplies the explicit weak interface jump condition
needed if the fixed nodal source is retained. Its matter trace is not yet
specified by a discontinuous-metric parent action; we do not silently
choose one or claim that the interface route is implemented.

## 2. Setup and scope

Read the previous action and port derivation:
`DERIVATION-20260912-flux-moment-lifts-and-canonical-boundary-power.md`.

At the initial P=0 slice, write U=sqrt(1-2mu/R), kappa=.1 and
a=c_P=kappa U/N. Here p is the new scalar auxiliary momentum, P is the
metric canonical momentum, and P1 its time derivative. They are not
interchangeable. Write

    f=-a K,    v=Q M^-1 P^T W f,    delta=v-f,
    M=P^T W Q.

In the matrix expressions P denotes the momentum basis map, not the
scalar p or the values of metric P. Q is a continuous mass-coordinate
basis; metric momenta may be broken across elements.

All trials keep the physical scalar grid (17 nodes, 16 cells), the
transported base and MTS Gram factors, the annulus, coefficients, drives,
and the free source profile fixed. The total scalar momentum can change
through the same TWO previously owned boundary lifts. Both lapse
amplitudes and all 21 dependent initial-data coefficients are recomputed.
Thus this is not a comparison at artificially frozen P1 or raw current.

The comparator is GR WITH the common scalar sector, not vacuum GR.
Numbers are residuals in the existing nondimensional fixture conventions,
not observational bounds.

## 3. Exact simultaneous local gauge-error identity

Let eta be any of the 19 existing lapse tests, theta=eta/N, and

    b=-N_R/(kappa U)+N mu/(kappa R^2 U^3),
    s_i=N_i e_i/(R_i U_i),
    E(z)=integral z(b-P1) dR + sum_i z_i s_i.

The nodal e_i include endpoint quadrature weights where applicable.
This is the metric Euler residual after the signed inner reaction and
outer clock have cancelled their metric boundary loads. E(z)=0 for z
in the ACTUAL mass-coordinate trial span, up to numerical solve error.

Using canonical endpoint power rather than raw-current power, the
previous Ward identity reads

    C1[eta]=L0[eta](delta)+E(theta f).

The boundary-subtracted mass derivative is

    L0[eta](delta)
      = integral {eta mu/(kappa R^2 U^3)
                  -eta_R/(kappa U)} delta dR
        + sum_i eta_i e_i delta_i/(R_i U_i).

Substitute eta=N theta and eta_R=N_R theta+N theta_R:

    L0[eta](delta)
      = E(theta delta)
        + integral {theta P1-N theta_R/(kappa U)} delta dR.

Linearity of E gives the desired result:

    C1[eta] = E(z_q) + <z_p, delta>,
    z_q = theta v,
    z_p = theta P1 - N theta_R/(kappa U).                  (1)

This is an algebraic consequence of the action-derived Ward identity,
with the same interface conventions as that identity. In the actual
quadrature calculations a separately measured integration error remains.
We do not identify this floating-point check with an exact interval proof.

Both directions matter. Representing z_q in Q and z_p in the metric
momentum span is sufficient for instantaneous C1 cancellation, because

    E(Q c)=0,    <P d, delta>=0.

Dropping the spatial derivative term in z_p is wrong. An explicit negative
control omits it; it changes the result at order 1e-8, above the gate.

## 4. An honest error bound, including nodal forces

A plain radial L2 norm cannot bound arbitrary point evaluations. Use the
direct-sum graph norm

    ||z||_G^2 = integral z^2 dR + sum_i omega_i z_i^2,
    ||E||_*^2 = integral (b-P1)^2 dR + sum_i s_i^2/omega_i.

Let r_q be the graph-norm projection remainder of z_q against Q,
and r_p the radial L2 projection remainder of z_p against P. Then

    |C1[eta]| <= ||E||_* ||r_q||_G
                + ||delta||_L2 ||r_p||_L2.                (2)

Equation (2) assumes exact canonical equations and the underlying Ward
identity. The numerical verifier adds the measured Ward and both
projected-equation remainders explicitly, rather than omitting roundoff.

The estimates genuinely bound their two corresponding works. They are
loose: roughly 4.7e-6 for the original frame and 9.5-9.7e-7 for the
177-pair trace-preserving frame. They are NOT a 1e-10 certificate.

## 5. Source-independent constructions and numerical repairs

The unrestricted trial adds continuous piecewise polynomial coordinates
and a canonical dual momentum completion, keeping every old Q, Q_R and
P column exactly. Two and four bubble modes are tried on the unchanged
metric elements. This changes approximation space, not a physical
coupling or the scalar stencil.

For the trace-preserving trial require added coordinates H and momenta Z:

    P^T W H=0,  Z^T W Q=0,  Z^T W H=I,
    H_in=H_out=Z_in=Z_out=0.                              (3)

The pairing is diag(M,I). At fixed fields and quadrature,

    v_extended = v_old + H Z^T W f,

so BOTH endpoint mass-velocity operators are unchanged for every load.
Likewise the old momentum coefficients are unchanged for a fixed
regular-plus-nodal force; Z vanishes at the endpoints. This is an
operator statement, not a fit to one observed boundary velocity.
Recomputing P1 still changes g, K and f, so the actual raw/projected
endpoint error must be checked again.

We construct zero-endpoint candidates BEFORE solving the moment systems:
subtract the linear interpolant of their endpoint values. Physical
function values are reorthogonalized after nullspace normalization.
The new momentum dual is then solved against the represented functions.
The accepted block errors are below 7e-15; endpoint additions are exactly
zero in the stored node arrays. The 1e-10 physical tolerance is unchanged.

Two failed implementations are retained:
- The first nullspace/endpoint-constraint solve lost the protected traces
  at four modes and stopped before the matched MTS run.
- Factoring the traces fixed that problem, but coefficient-space
  cancellation left a 4.19e-8 canonical block error, above its 1e-8
  construction gate. Reorthogonalizing the represented functions fixed
  that numerical issue without relaxing the gate.

These were numerical construction failures, not evidence against either
physical theory. The final stable construction runs BOTH branches at
both selected orders. Its added space is a zero-endpoint interior
subspace, NOT a claim that every unrestricted polynomial mode is kept.
All singular values and discarded near-dependent counts are recorded.

## 6. Matched results

Higher quadrature values are shown; primary quadrature independently
agrees at the precision relevant to the reported C1 residuals.

| Frame | Pairs | GR C1 max | MTS C1 max | GR endpoint v-f max | MTS endpoint v-f max |
|---|---:|---:|---:|---:|---:|
| Original | 79 | 3.346e-8 | 3.267e-8 | 3.558e-9 | 4.371e-9 |
| Unrestricted, 2 modes | 142 | 1.704e-8 | 2.066e-8 | 6.851e-5 | 1.100e-5 |
| Unrestricted, 4 modes | 179 | 5.107e-9 | 5.304e-9 | 1.334e-5 | 2.698e-5 |
| Trace-preserving, 2 modes | 140 | 3.913e-8 | 3.962e-8 | 3.106e-9 | 2.187e-9 |
| Trace-preserving, 4 modes | 177 | 1.815e-8 | 1.837e-8 | 1.856e-9 | 1.849e-9 |

The unrestricted improvement is not acceptable because its boundary
error increases by several orders of magnitude. The 140-pair trial does
not improve C1. The 177-pair trial improves C1 and mass endpoint agreement
in both branches, but BOTH remain above tolerance.

For that final comparison, higher-quadrature P1 endpoint residuals are
3.827e-10 GR and 4.103e-10 MTS; the latter is worse than its smaller
reference's 9.29e-11. No all-gates promotion is justified. C0 remains below
1.8e-13 across the completed trace-preserving comparisons.

In the 177-pair trial the separate work maxima in (1) are:
- GR configuration 6.20e-9, momentum 1.68e-8;
- MTS configuration 7.90e-9, momentum 1.70e-8.

Their maxima need not occur on the same test, so they must not be added
as if they were one residual row. The momentum term is larger here; it
is not the sole remaining error.

## 7. Why not just keep padding a fixed smooth basis?

A limited algebraic lemma helps delimit that strategy. Suppose a finite
dimensional space Q contains a function nonzero throughout some interval,
and a continuous theta is nonconstant on that interval. If theta Q is
contained in Q, then q, theta q, theta^2 q, ... are linearly dependent.
Dividing the resulting relation by nonzero q makes a nonzero polynomial
vanish on the interval of values taken by theta, a contradiction.

Thus a fixed finite smooth trial space cannot be uniformly closed under
this ordinary multiplication for all its states on such an interval.
This is NOT a no-go for our instantaneous weak conditions, approximate
closure at fixed tolerance, a controlled refinement limit, adapted
gauge variables, or a differently derived discrete transformation law.
It is not a no-go for MTS or GR.

## 8. Constructive next route: derive the interface law before choosing a trace

The earlier fixed-node obstruction concerned smooth geometry coupled to
positive point-supported scalar energy. We can now state the required
weak interface condition explicitly, rather than only repeat that gap.

Temporarily allow piecewise smooth positive U with jumps at interior
scalar nodes. Keep the gravitational weak C0 expression itself unchanged.
Write the still-to-be-defined matter trace as mathcal_U_i, so its nodal
coefficient is sigma_i=mathcal_U_i e_i. Integration by parts element by
element gives

    C0[eta] = integral eta mu_R/(kappa U) dR
              - sum_interfaces eta_i R_i [U]_i/kappa
              - sum_nodes eta_i sigma_i,                 (4)

after the external radial boundary terms cancel as previously. Here
[U]=U_right-U_left, and the bulk derivative is one-sided on each open
element. With only nodal matter in this fixture, arbitrary compact tests
therefore require

    mu_R=0 between nodes,
    R_i [U]_i + kappa sigma_i = 0.                       (5)

The associated exact mass jump is

    [mu]_i = kappa (U_left+U_right) sigma_i/2.            (6)

Positive matter trace and energy give a positive mass jump and a downward
U jump, as expected from (5)-(6). A continuous U cannot satisfy a nonzero
positive nodal sigma under this stronger all-test requirement.

Equations (4)-(6) are CONDITIONAL weak-action identities, not permission
to insert arbitrary mass jumps into the current code. The smooth parent
does not yet specify mathcal_U_i when two metric traces exist. In
particular, choosing an arithmetic mean, a one-sided value, or an
independent node field would be a new assumption until its interface
matter, lapse, clock, coframe and symplectic terms are derived together.

The verifier tests (4)-(6) independently on manufactured two-cell
piecewise-constant mass data and five compact endpoint-zero polynomial
tests, including the wrong-sign negative control. The negative mass-jump
case checks algebra only, not positive-energy physics.

NEXT: derive that variational interface matter/clock prescription from
the existing transported action, preserving its scalar/Gram scale.
Start with one interface and both GR/MTS sectors, then test its canonical
flux and local constraint identities. If no unique compatible trace is
selected, state the remaining freedom explicitly and pursue a
scale-preserving joint scalar/metric reconstruction instead. Do not fit
the C1 rows, force a mean-trace convention, or launch more blind basis
enlargements. C2 and evolution wait.

## 9. Evidence and safeguards

Completed experiments:
- `source-intake/navier-stokes/20260912/annular-local-gauge-budget-attempt01/status.json`
- `source-intake/navier-stokes/20260912/annular-local-gauge-trace-stable-attempt01/status.json`

Preserved failed numerical constructions:
- `source-intake/navier-stokes/20260912/annular-local-gauge-trace-preserving-attempt01/status.json`
- `source-intake/navier-stokes/20260912/annular-local-gauge-trace-factored-attempt01/status.json`

Derivation and constructive implementation:
- `scripts/annular_local_gauge_commutator_20260912.py`
- `scripts/annular_local_gauge_trace_stable_20260912.py`
- `scripts/derive_annular_local_gauge_budget_20260912.py`
- `scripts/derive_annular_local_gauge_trace_stable_20260912.py`
- `scripts/seal_annular_local_gauge_budget_20260912.py`

The final integrity record is named annular-local-gauge-budget-final-integrity.json
in the same intake directory. It verifies saved hashes, all retained action
force directions and oriented history loads, the complete endpoint
operators rather than one chosen load, numerical bounds, source-profile
ownership, compilation and the cited paths. Validation completion is not
a physics pass.

The protected formalization-workbench scan is explicitly an mtime scan
since this turn started, not a pre-turn content-hash snapshot. No GitHub,
subagents or new evolution. Each calculation uses one BelowNormal
single-core Python worker. No other task's processes were stopped.
