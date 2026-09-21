# Interface logarithmic trace and distinct clock maps

Private derivation, 2026-09-12. No GitHub action, subagents, new spacetime
evolution, full first-jet pass, physical fit, or completed GR limit.

## 1. What moved forward

The last note derived a jump condition but left its matter trace undefined.
Here we construct a specific smooth-layer regularization of the initial
metric/source action and derive, within that class:

1. An exponential geometry jump and a logarithmic-mean matter trace.
2. The metric-rate impulse needed to maintain a continuous coordinate lapse.
3. The distinct transformation that matches a stationary proper clock.
4. A conditional obstruction to identifying that clock map with the
   horizontal transport already used by the scalar action.
5. An explicit off-shell counterexample: endpoint values alone do not
   determine the regulated matter action, so the on-shell logarithmic mean
   cannot simply be inserted as a finished interface action.

These are derivations and controlled layer calculations, not a numerical
repair to the existing finite first-jet candidate. Its previous C1
residuals remain unchanged. The old working action branch and the 79/177
comparison data are untouched.

## 2. Starting point, and the additional regularization assumption

See:
`DERIVATION-20260912-local-gauge-error-law-and-trace-preserving-trial.md`,
`scripts/annular_covariant_joint_preparation_20260912.py`,
`scripts/annular_nonlinear_history_20260912.py`, and
`scripts/annular_covariant_scalar_action_20260912.py`.

At the P=0 initial slice, U=sqrt(1-2mu/R)>0. The existing nodal matter
Hamiltonian coefficient is N_i U_i e_i, where

    e_i = omega_i p_i^2/(2 R_i^2)
          + R_i^2 sum_f S_fi A_f^2/(2h),
    A_f = sum_j B_fj chi_j.

The base and MTS Gram factors remain exactly those of the parent. The
existing code differentiates e_i at fixed canonical matter variables:
its explicit metric dependence is in N_i U_i, not in e_i.

For THIS experiment replace one positive point-supported e_i by

    epsilon_delta(R) = e/delta * w(x),
    x=(R-R0)/delta+1/2,  0<=x<=1,
    w>=0, integral_0^1 w dx=1.                         (1)

The regulator shape and e are held fixed during metric variation.
This is a new regularization prescription; the full transported
scalar-history action has NOT yet selected it. On smooth backgrounds
its metric energy functional tends to the existing nodal one.

Keep the same local gravitational Hamiltonian density:

    H_delta = integral {
        -N (U+1/U-2Uref)/(2kappa)
        -R N_R (U-Uref)/kappa + N U epsilon_delta
    } dR,                                               (2)

with the inherited gravitational endpoint terms when a whole interval is
varied. Compact variations inside the test layer avoid any ambiguity
about those external terms. Kappa=.1 in the existing fixture.

We use the canonical metric one-form integral P dmu and derive the
initial metric equations. The full scalar symplectic reduction, moving
interface dynamics, source histories and all-time gauge algebra are not
replaced by (2). In particular, freezing e during a metric variation does
not mean that matter energy is constant during physical evolution.

## 3. Two equations from the same action

Variation of N and mu in (2) yields

    mu_R = kappa U^2 epsilon_delta,                      (3)
    P1 = -N_R/(kappa U)
         +N mu/(kappa R^2 U^3)
         +N epsilon_delta/(R U).                        (4)

Here P1 is the metric momentum time derivative, not scalar momentum p.
Define

    A=mu/(R^2 U^2),   B=kappa epsilon_delta/R,
    a=kappa U/N,     g_R=a P1.

Using (3), differentiation of U gives

    (ln U)_R = A-B,
    (ln N)_R = A+B-g_R.                                (5)

These identities are checked symbolically. The numerical action checks
differentiate the Hamiltonian itself, not just its rearranged ODE.

The original time connection is

    c=kappa U P / {N(1-kappa^2 U^4 P^2)}.

Since P=0 throughout this initial slice, c_t=a P1 there. For the existing
horizontal map T_R=c(T,R), its time Jacobian satisfies

    J_R=c_t J,    J(left)=1,    J_+=exp(G),
    G=integral_layer a P1 dR.                            (6)

## 4. Finite-width identities and the thin-layer limit

Write I_A=integral A dR and I_B=integral B dR. Equations (5)-(6) give

    U_+/U_- = exp(I_A-I_B),
    N_+/N_- = exp(I_A+I_B-G),
    J_+ (N_+ U_+)/(N_- U_-) = exp(2 I_A).               (7)

For C=R^2 N U at P=0, the last statement applies to J C/R^2. The ratio
of C itself has the additional finite R_+^2/R_-^2 factor. We do not drop
that factor at finite width.

Suppose R0>0, U and N stay uniformly positive and bounded, e is fixed,
and the layer width tends to zero. Then

    I_A -> 0,    I_B -> zeta=kappa e/R0.

Thus

    U_+ = U_- exp(-zeta),                               (8)
    sigma = lim integral U epsilon_delta dR
          = e U_log,
    U_log = (U_- - U_+)/ln(U_-/U_+).                     (9)

To prove shape independence, let W(x)=integral_0^x w. In the thin limit
U(x)=U_- exp(-zeta W(x)). Integrating U against dW gives (9), independently
of which of the three tested shapes, or any admissible normalized
nonnegative shape in this class, is used.

This derives the missing trace within the specified regularization; it
does NOT prove that all extensions of the point action select it.

For comparison, substituting the arithmetic mean directly into the jump
condition gives (1-zeta/2)/(1+zeta/2) rather than exp(-zeta). Those are
different finite-source extensions even though they agree at low order.
A manufactured zeta=.2 control makes the distinction easily measurable;
it is not fitted to MTS data.

An exact finite-width integral identity is also available:

    kappa sigma_delta
      = -[R U]_-^+ + (1/2) integral (U+1/U) dR.          (10)

It reduces to the earlier R0[U]+kappa sigma=0 in the thin limit.

## 5. What maintaining one coordinate lapse requires

If N_+=N_- in the same stationary coordinate description, (7) requires

    G=I_A+I_B -> zeta.                                  (11)

A constant N through the layer is one explicit representative satisfying
this endpoint condition, not a unique derived lapse profile. Equation
(4) then determines its P1. The opposite test choice P1=0 gives G=0 and

    N_+/N_- -> exp(zeta).

Therefore positive concentrated energy does not permit BOTH a continuous
coordinate lapse and uniformly bounded P1 in this regulator class.
For N>=Nmin, nonnegative mu and U<=1,

    |G| <= (kappa/Nmin) delta ||P1||_infinity.            (12)

If the endpoint lapse is continuous and e>0 is held fixed, (11)-(12)
force a rate growing at least as 1/delta. This is a conditional theorem,
not an inference from a finite scan.

For the constant-lapse representative there is additionally

    integral P1 dR
      = N/kappa [1/U]_-^+
        +2N/kappa integral A/U dR
      -> N/kappa (1/U_+ - 1/U_-).                       (13)

A distributional rate may require explicit interface degrees of freedom
or a different chart/function space. It cannot inherit the old smooth
finite-frame certificates. An unbounded initial derivative by itself is
NOT a proof of physical instability, nor a proof that every nonlinear
continuation fails.

If source energy decreases along with layer width, e=O(delta), the
singular lower-bound argument no longer forces divergence. That is why
joint matter/metric refinement differs from squeezing fixed positive
nodal energy into ever thinner smooth metric elements. Whether h is
numerical or owns a physical MTS kernel scale must still be respected.

## 6. Horizontal transport is not proper-clock identification

This is the crucial distinction exposed by the calculation.

On a stationary timelike line at P=0, proper time is d tau=N dt. If the
two sides are to describe that same stationary clock, their time-coordinate
gluing Jacobian L must satisfy

    L N_+ = N_-,
    L=N_-/N_+ = J exp(-I_A-I_B).                        (14)

In contrast the horizontal scalar-action map has J=exp(G). Their ratio
is derived, not adjustable:

    L/J -> exp(-zeta)=U_+/U_-.

Indeed

    J N_+/N_- = exp(I_A+I_B) -> exp(zeta) != 1.          (15)

So the near-continuity of transported J C is NOT proper-clock matching:
C contains the radial geometry factor U as well as the lapse.

Using the proper-clock gluing instead gives

    (L C_+/C_-) = (R_+^2/R_-^2) (U_+/U_-).

A radial density/coupling step remains. It should be accounted for by an
interface action, not erased by calling C a pure clock.

There is a further conditional check at zero shift. If J itself is used
to identify two sides at the same areal radius, let r=U_+/U_- and let
v=dR/dt_- be the common interface trajectory expressed on the left. In
the thin limit J N_+=N_-/r and dt_+=J dt_-. The pulled-back induced metric
on the right is r^-2 times that on the left. For r!=1 it cannot be the
same nondegenerate timelike induced metric; a null tangent is the
algebraic exception. Merely letting the interface move does not fix
this particular mistaken identification.

None of this proves that the parent intended horizontal transport to be
a chart-gluing map. It may instead remain an interaction transport
between distinct events, with a separate physical interface clock.
That distinction must be explicit in the next variational construction.
It is not evidence for reversed time dilation or a claim about photons.

## 7. Why an on-shell mean is not yet an off-shell interface action

It is tempting to write -N e U_log as a complete endpoint-only matter
action. That would promote (9), which used the constraint, into an
off-shell variational prescription without justification.

A counterexample makes the missing step concrete. In cumulative source
coordinate y in [0,1], compare

    U_0(y)=U_- exp(-zeta y),
    U_a(y)=U_0(y) [1+a y(1-y)].

They have exactly the same endpoints, positive geometry for the tested
a=.1, and the same e and N, but

    integral U_a dy - integral U_0 dy
       = a integral U_0 y(1-y) dy > 0.                  (16)

Their regulated matter Hamiltonians differ. The second path need not
obey the same constraint: that is the point of an OFF-SHELL variation.

Equation (16) does not forbid deriving an effective interface action by
properly eliminating fields. It shows that raw endpoint data alone do
not determine the uneliminated action, and that simply inserting the
on-shell mean can lose the variations, symplectic terms and clock terms
needed for that elimination.

## 8. Numerical evidence, source ownership and validator corrections

The center node (index8, R0=6) is taken read-only from the preferred small
original79 canonical-port comparison. All 17 nodal energies are first
recomputed from the saved p, chi and exact parent B/S factors.

| Quantity | GR plus scalar | MTS plus scalar |
|---|---:|---:|
| Actual nodal e | 2.213619644487088e-4 | 2.218189723095052e-4 |
| zeta=kappa e/R0 | 3.689366074145147e-6 | 3.696982871825088e-6 |
| Thin same-clock required G | zeta | zeta |
| Horizontal-as-clock mismatch | exp(zeta)-1 | exp(zeta)-1 |

These are the existing fixture's nondimensional values, not measured
clock anomalies, physical lengths, or limits on the MTS theory.

For each real source and one explicitly manufactured zeta=.2 source:
three normalized shapes (beta22, beta33, asymmetric beta23) and six widths
are tested. The width runs from h/2 to h/1048576, with h=1/64 unchanged.
That makes 54 layer solves. We copy the parent's center mass/lapse as the
layer's left input parameters; this is not a re-solved global annulus.

Each solve tests both constant-lapse and zero-P1 representatives with
four compact mass and lapse variations: 864 action variations in total.
Independent verification also uses a linear integrating-factor solution
for mu, rather than the original coupled ODE, plus (10) and (13).

At the thinnest width, actual-source logarithmic-mean errors are at most
about 5.08e-11 across the three shapes. G differs from its thin limit by
about 6.21e-10, accounted for by the finite background integral. The
constant-lapse peak P1 grows to approximately 3713-4640 GR and 3721-4649
MTS, depending on regulator shape. These large rates describe an
artificially narrow fixed-energy layer, not an observed instability.

Two failed validation runs are preserved, not overwritten:
- Attempt01 incorrectly required a 10,000-fold increase in the TOTAL
  peak P1; at the broadest width the regular background dominates.
  The corrected test checks the derived source-only inverse-width law.
- Attempt02 demanded a fixed reduction ratio even when a symmetric
  limit error was near floating-point resolution. Attempt03 checks
  derived analytic error envelopes, with a disclosed 1e-12 numerical
  allowance, rather than requiring rounding noise to scale.

No physical C1 tolerance was changed. These validation criteria concern
the conditional layer identities, not passage of the old first-jet gate.

The error envelopes use mu<=mu_left+kappa e and a positive analytic
lower bound on F throughout the layer to bound A, finite-radius source
corrections and the cumulative log-U error. They bound all five reported
thin-limit errors. They are not an interval enclosure of the numerical
solver or a certificate for full evolution.

## 9. Next constructive step

Do NOT adopt an endpoint logarithmic-mean action, identify J with L,
or add another frozen basis correction.

Construct an OFF-SHELL finite-width matter-and-clock action that retains
the scalar canonical variables and the parent's complete transported
kinetic/spatial factors. Keep horizontal interaction transport and
stationary proper-clock gluing distinct. Derive its nodal metric forces,
scalar forces, symplectic interface terms and boundary power together.
Only then attempt to eliminate the layer or take a controlled joint
limit without changing the physical MTS kernel scale.

The main new question is now precise: which radial measure and
interface variables carry the factor U_+/U_- in (14), while preserving
the canonical action? The calculation has supplied that factor and the
required rate impulse; it has not supplied the full interface action.

## 10. Files and reproducibility

Completed matrix:
`source-intake/navier-stokes/20260912/annular-interface-layer-clock-attempt03/status.json`.

Preserved failed validators:
`source-intake/navier-stokes/20260912/annular-interface-layer-clock-attempt01/status.json`,
`source-intake/navier-stokes/20260912/annular-interface-layer-clock-attempt02/status.json`.

Implementation:
`scripts/annular_interface_layer_clock_20260912.py`,
`scripts/annular_interface_layer_bounds_20260912.py`,
`scripts/derive_annular_interface_layer_clock_bounded_20260912.py`,
`scripts/verify_annular_interface_layer_clock_20260912.py`.

The final record is annular-interface-layer-clock-final-integrity.json
in the same intake directory, with the matching immutable resume
snapshot. It records source/output hashes, all retained failures,
independent solutions, clock identities, off-shell counterexamples and
compilation. The formalization-workbench check is an explicitly limited
mtime scan from this turn's start, not a content snapshot. All new work
stays private in post-checkpoint-work.
