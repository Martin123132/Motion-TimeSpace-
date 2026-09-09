# Shift-unfixed GR and a local-in-time quadratic clock action

Private continuation, 2026-09-09. All paths below are relative to
post-checkpoint-work. The previous completed evidence and preserved failures
were verified from their immutable hashes before this construction.

## 1. Concrete outcome

The shared gravity/matter action now retains all three areal-coordinate metric
components through arbitrary radial shift, not merely the old first-order beta
germ. Its shift variation supplies the mass-time equation and fixes the
normalization of the clock-current contribution without inserting that flux.

The finite time-link correction has an explicit quadratic reduction containing
only perturbation positions and FIRST time derivatives, plus a written time
boundary. There is no perturbation acceleration or unknown future-history
evaluation in that reduced quadratic functional. This is a real local-in-time
formulation at perturbative order, not yet a well-posed constrained evolution.

The scalar kinetic matrix is positive on all four tested reference-seeded
patches. The first-order metric pairing has the same rank as its matched GR
baseline. Nonzero affine Euler defects and patch boundary covectors are saved;
the backgrounds have NOT been declared solutions by discarding those terms.

No full Dirac/secondary-constraint closure, global characteristic boundary
problem, horizon regularity, coupling calibration or physical local-GR pass is
claimed. The complete MTS curvature/memory sectors are not newly derived by this
leading GR/P(X) discretization calculation. kappa is the existing normalized
input, not a newly derived Newton constant.

## 2. Full metric action rather than premature shift fixing

Use the spherical areal-coordinate metric

    ds^2=-N^2 d tau^2 + L^2(dR+V d tau)^2 + R^2 dOmega^2.

N, L and V are varied independently before taking the orthogonal background
V=0. This is a nonsingular parameterization of the three two-dimensional metric
components on the exterior patch. It retains the variation that earlier
premature metric gauge restrictions could lose. R remains the areal coordinate;
this is not an unfixed four-dimensional coordinate ansatz.

The starting convention is the ADM action. The spherical reduction agrees with
[Kuchar, equations 17-22](https://arxiv.org/pdf/gr-qc/9403003), using his radial
metric scale as our L, his radial shift as V, and R'=1, R_dot=0. The general
formalism is [Arnowitt, Deser and Misner](https://arxiv.org/abs/gr-qc/0405109).
The extra cosmological term and the retained P(X) sector below use our existing
normalization kappa=4 pi G, with the common angular factor divided out.

The extrinsic-curvature eigenvalues and spatial scalar curvature are

    k_R=(-L_t/L + V L_R/L + V_R)/N,
    k_Omega=V/(NR),
    3R=2(1-L^-2)/R^2 + 4L_R/(R L^3).

An independent Christoffel/Ricci calculation verifies the last expression.
Substitution in NL R^2[3R+KijKij-K^2-2Lambda]/(4 kappa) gives

    L_g = 1/kappa {
      R V L_t/N - R V^2 L_R/N - R L V V_R/N - L V^2/(2N)
      + N(L-L^-1)/2 + NR L_R/L^2 - Lambda N L R^2/2 }.

This is the full shift-unfixed bulk ADM density, not a truncation in V.
The usual gravitational variational boundary problem still has to be specified;
using an ADM bulk action does not magically select those conditions.

Define spatial mass mu by

    F_s=1-2mu/R-Lambda R^2/3=L^-2.

At V=0 the static density is exactly NL mu_R/kappa, matching the earlier
E mu_R/kappa block with E=NL. Away from V=0 the invariant mass is instead

    m_physical=mu + R V^2/(2N^2).

The shift-squared term is necessary at quadratic order. Spatial face mass mu
must not be relabelled as the invariant mass off the orthogonal background.

Integrating the V_R term by parts produces the spatial boundary

    B_R=-R L V^2/(2 kappa N),

and replaces its three quadratic shift terms by

    -R V^2[L_R+L N_R/N]/(2 kappa N).

Their equality INCLUDING partial_R B_R is verified symbolically. The numerical
action uses the unintegrated V_R form, so this boundary is not silently lost.

### Matter and the mass-time normalization

The same action contains

    L_m=R^2 N L K(X,chi),
    X=-(q-Vw)^2/N^2+w^2/L^2,
    K=-X/2-m_chi^2 chi^2/2+b2 X^2+b3 X^3,
    P=-2K_X, q=chi_t, w=chi_R.

At V=0, partial_V L_g=R L_t/(kappa N) and
partial_V L_m=-R^2 L P q w/N. Therefore the bare equation gives

    mu_t=kappa R^2 F_s P q w.

For the metric time connection

    A=L^2 V/(-N^2+L^2 V^2),  A_V|0=-L^2/N^2.

If a consistently paired connection edge contributes U_A=h J_cut, then the
shift variation of L_g-U gives

    Delta mu_t=-kappa J_cut/(NL).

The gravitational normalization is derived here from R L_t/(kappa N) and
mu_t=R L_t/L^3; it is not a source chosen to force conservation. Our mixed
finite-element assembly uses its actual variational quadrature/adjoints, not
an unproved assertion that every face covector is a collocated h times flux.

## 3. Explicit shared mixed discretization and owned background patch

Face mu and V use fixed continuous piecewise-linear bases; nodal N uses its
fixed piecewise-linear basis. The scalar uses a C1 cubic Hermite reconstruction
whose nodal derivatives are D chi+I. The actual defect I and its time derivative
are retained as a specified lifting, not projected to zero. All gravitational
and matter bulk terms share four-point Gauss quadrature on the merged knot
partition. Full nonlinear L(mu) and all basis adjoints are used.

This is a specified mixed finite-element action. It is NOT exactly the old
collocated/SBP action or the preceding mass-incidence action at finite mesh.
No stability/conservation pass of those other discretizations is inherited.
The Gram coefficient uses the same nodal Hermite derivative and metric fields:

    a=R^2 NL { P(F_s-V^2/N^2)
          +2P_X[F_s w+V(q-Vw)/N^2]^2 }.

The baseline orthogonal patch is derived by integrating the previous metric
connection, with anchor R=6 and old t=.15. The patch is [5.875,6.125], tested
with 16 and 32 intervals for both canonical and nonlinear references. Scalar,
metric and Jacobian jets come from the owned reference fields. The transformed
kinetic invariant X and time-derivative finite differences are checked.

Crucially, a common orthogonal slice across the WHOLE old annulus would generally
leave its short owned advanced-time interval [0,.5]. We do not extrapolate those
fields or pretend that local patches supply global Cauchy data.

For finite-variation validation, the patch jets define a DECLARED local time
path: scalar quadratic in tau, mass/lapse linear, physical nodal scalar gradient
linear, and V_background=0. The interval is [-.001,.001] about the patch slice.
These paths are seeded from actual reference jets but are not asserted to be
the exact parent solution at later times. Their nonzero Euler defects matter.

## 4. Derivation of the time-local quadratic correction

At the orthogonal background A_0=0, expand a one-parameter perturbation as

    chi_epsilon=chi+epsilon eta,
    a_epsilon=a+epsilon a1+epsilon^2 a2,
    A_epsilon=epsilon A1+epsilon^2 A2,
    phi_epsilon=tau+epsilon y+epsilon^2 z.

Here a1=Da[e] and a2=D2a[e,e]/2 include q, w, mu, N and V variations.
For each existing factor anchor the link ODE gives

    y_R=-A1,       z_R=-(A2+A1_t y),      y=z=0 at the anchor.

Both links depend on fields at the current tau. z involves first perturbation
time derivatives but no second ones. Spatial integrals are exact for the
specified piecewise-linear nodal A1/A2 reconstruction; the A1_t y product is
piecewise cubic and uses exact two-point Gauss integration.

The transported scalar and density coefficients are

    x1=eta+q y,
    x2=eta_t y+chi_tt y^2/2+q z,
    b1=a1+partial_t(a y),
    b2=a2+partial_t(a1 y+a z+a_t y^2/2).

The apparent accelerations occur inside the written total derivative in b2.
Let z0_l=sum_i T_li chi_i, z1_l=sum_i T_li x1_li, B_l=sum_i S_li a_i,
d_l=z0_l^2/(2h), and d_t,l=z0_l(Tq)_l/h. The unreduced second-order potential
coefficient is

    U2_raw=sum_l { B_l[z1_l^2+2z0_l(Tx2)_l]/(2h)
                  +(S b1)_l z0_l z1_l/h +(S b2)_l d_l }.

One time integration by parts gives U2_raw=U2_red+partial_t B_time, with

    B_time=sum_l d_l sum_i S_li(a1_i y_li+a_i z_li+a_t,i y_li^2/2).

In U2_red replace x2 by eta_t y+chi_tt y^2/2, replace b2 by a2, then add

    -sum_l d_t,l sum_i S_li(a1_i y_li+a_t,i y_li^2/2)
    -sum_li g_li z_li,
    g_li=a_i S_li d_t,l-q_i T_li B_l z0_l/h.

The full mixed quadratic action is the second variation of the explicit bulk
ADM+matter action minus U2_red, with -B_time at its time endpoints. It contains
only positions and first perturbation velocities. This avoids promoting the
full finite-history functional to an unproved causal evolution equation.

Checks compare this raw germ against INDEPENDENT finite link-ODE variations
and verify its reduction with nonzero boundary work. The combined-action
integral uses the same bulk second difference on both sides: it independently
checks the clock completion and endpoint term, not every bulk position Hessian.
Separate bulk position gradients, momenta and velocity Hessians are checked.

The smooth combined integral's endpoint term is around 1e-17, below some of
its finite-difference discrepancies. We do NOT claim those finite differences
resolved that tiny term. A separate rough-direction raw/reduced-germ control
resolves boundary derivatives 3.012e-11 and 3.220e-11, with identity errors
4.69e-23 and 7.13e-21; omitting that boundary is detectably wrong there.

## 5. What the kinetic and primary-rank tests actually establish

After reduction, the coefficient of perturbation velocity squared is confined
to the scalar block:

    M_chi = H_chi^T W_q H_chi - diag(rho_i a_qq,i),
    W_q = quadrature_weight R^2 L/N [P-2P_X(q/N)^2],
    rho=S^T(Tchi)^2/(2h).

There is no squared mass, lapse or radial-shift velocity. Shift velocities
can still enter linearly and change the first-order metric pairing; they are
not discarded merely because their velocity Hessian vanishes.

| Reference | Intervals | Minimum scalar kinetic eigenvalue | Relative Gram correction norm |
|---|---:|---:|---:|
| canonical | 16 | .18563645 | 0 exactly |
| canonical | 32 | .09274232 | 0 exactly |
| nonlinear | 16 | .18895112 | 3.187e-8 |
| nonlinear | 32 | .09439613 | 1.901e-9 |

Canonically a is independent of q, so a_qq=0 analytically. The nonlinear bound
is only a measured norm on these patches, not a uniform theorem for all fields.

For the position-velocity matrix C in L2=velocity^T C position+..., the metric
antisymmetric block, ordered (mu,V), has the form

    Omega_metric = [ 0    B ; -B^T    D ],
    B=Q_face^T diag(quadrature_weight/(kappa N F_s^(3/2))) Q_face.

B is positive definite for positive weights, kappa, N and F_s and a full-rank
face basis. D is the antisymmetric correction from the clock term. Consequently
this block is invertible for ANY finite D: its inverse is

    [ B^-T D B^-1    -B^-T ; B^-1    0 ].

The clock term has no mass/lapse velocity row and no lapse/mass column in its
shift-velocity row at this quadratic orthogonal background. Thus the lapse
directions stay null in the metric first-order block. Full N16 matrices verify
rank 36 in 53 metric variables, retaining 17 lapse null directions, for BOTH
baseline and candidate. The structurally forbidden clock blocks are exactly
zero in these evaluations, without a projection or changed rank threshold.

This is evidence against an immediate extra-primary-kinetic-mode problem in
this construction. It is NOT a complete degree-of-freedom count: secondary
constraints, their consistency and the spatial operator still determine whether
the constrained initial-boundary system is acceptable.

## 6. Actual affine defects and endpoint covectors are now explicit

The saved arrays include, separately for GR/P(X) baseline and candidate,

    E0=L_position-partial_t L_velocity,

for scalar, spatial mass, lapse and shift. These are computed from the declared
time path with the source lifting retained. They can supply the affine
right-hand side -E0 of a Newton correction. They are NOT newly calibrated
physical external sources or permission to call the background on shell.

The lapse and shift correction covectors are independently checked against
finite variations of the full time-link potential, including its linear time
boundary. Representative maximum weak lapse defects remain 5.90e-6 and
6.34e-6; shift defects remain about 3.16e-6 and 3.56e-6 for the candidate.
They are not zero and no constraint-propagation pass is claimed.

The raw mass covector has maxima near 10 because patch endpoint terms are
retained. That is not an instability score. At V=0 its signed boundary
coefficients are -NL/kappa and +NL/kappa, numerically approximately -9.9993
and +10.0003 here. Patch interfaces are not the old global physical boundaries.
More generally the unreduced bulk action has spatial boundary coefficients

    p_muR=(N F_s-V^2/N)/(kappa F_s^(3/2)),
    p_VR=-R L V/(kappa N),
    p_chiR=-R^2 N L P [F_s w+V(q-Vw)/N^2].

Their actual allowed variations or compensating boundary action must be fixed
before a constrained solve. Neither the large endpoint mass entries nor the
nonzero scalar lifting is silently removed to obtain a better result.

## 7. Reproducibility

- source-intake/navier-stokes/20260909/annular-adm-clock-quadratic-derived/status.json: complete 68/68.
- source-intake/navier-stokes/20260909/annular-adm-affine-and-boundary-derived/status.json: complete 33/33.
- scripts/annular_adm_mixed_action_20260909.py: mixed action, coefficient derivatives and owned orthogonal reference jets.
- scripts/annular_adm_clock_quadratic_20260909.py: explicit factor-local first/second links, reduced quadratic action and independent finite link functional.
- scripts/derive_annular_adm_clock_quadratic_20260909.py: action, kinetic, finite-link and complete first-order clock matrix controls.
- scripts/derive_annular_adm_affine_and_boundary_20260909.py: independent curvature, bulk variations, affine defects and boundary controls.

Previous context: DERIVATION-20260909-covariant-time-links-and-mixed-gravity-basis.md.
Final integrity: source-intake/navier-stokes/20260909/annular-adm-quadratic-final-integrity.json.
All work is local, single-core BelowNormal, with no subagents, public updates,
shared-process shutdowns or edits to the frozen workbench/galaxy projects.

## 8. Next calculation, not another current hunt

Complete the mixed quadratic spatial/constraint operator and stabilize the
lapse constraints. Derive admissible patch-interface/gauge conditions from
the characteristic and constraint count, then attempt one constrained Newton
correction using the SAVED -E0 vectors. Apply identical discretization, source
and boundary controls to the GR/P(X) baseline and Gram candidate.

The decisive question is now whether that constrained linear system is
solvable with controlled residual reduction and a compatible time evolution.
It is no longer whether an action/current or a local quadratic time formula
can be written: those constructions and their explicit limitations are here.
