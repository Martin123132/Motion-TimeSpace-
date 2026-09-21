# Cross-cut source action and the original driven initial boundaries

Date: 2026-09-13. Private candidate-action derivation and initial-data test.

## 1. Result and limits

The finite-width construction has been brought back to the ORIGINAL physical
cuts L=5.875, R=6.125. Six matched GR/MTS preparations now satisfy the inherited
inner mass value and mass drive, outer scalar velocity, outer clock value, and
P1=0 at both cuts. C0 and its full first time derivative C1 also pass tests that
do not vanish at either boundary, with all radial terms retained.

This is more than the preceding compact-interior test, but is NOT a completed
initial-boundary-value problem. Exterior source-region histories, their
variational matching to the interior, and higher boundary compatibility are
not yet closed. No point scalar reaction or unique regulator has been derived.
The old 79/177-pair evidence is not overwritten or relabelled as passing.

Predecessor:
`DERIVATION-20260913-shared-metric-bulk-current-and-compact-constraint-propagation.md`.
Starting seal:
`source-intake/navier-stokes/20260913/annular-finite-width-bulk-current-final-integrity.json`.

## 2. Keep the cut at the original radius, not at the end of the enlarged support

The scalar action averages complete translated stencils r_i(z)=r_i+delta z.
Its enlarged support reaches L-delta/2 and R+delta/2. At the outermost ends of
that complete support, the truncated-stencil current is zero: no links extend
farther out. Prescribing a nonzero original mass drive there, without adding an
exterior interaction, would be a different and inconsistent construction.

Instead retain the original physical cuts L and R, which pass through the two
edge bands. Some translated links cross those cuts. Their outside portions
form an explicit source region (a collar), and must remain in the action.
No new Gram coefficient, link scale, or physical coupling is added.

For every z classify each COMPLETE spatial factor by the radial hull of its
nonzero B and S entries:

    S_scalar = S_inside + S_outside + S_cross.

The kinetic terms split by their node location. Spatial factors are entirely
inside, entirely outside, or crossing a cut. Each original factor occurs ONCE.
In particular S_cross retains the complete A_f^2 D_f/(2h), not a truncated A,
truncated D, or a product of separately fitted endpoint energies.

Because this classification is independent of the fields and time, the
partition is an exact off-shell algebraic decomposition of the chosen action.
That statement is distinct from integrating out the exterior fields or
establishing a well-posed effective boundary action.

The formal interior functional with supplied exterior histories consists of
the interior gravity and kinetic terms, interior spatial factors and the full
crossing factors. Purely exterior terms have no direct interior variation when
those histories are held fixed. A complete physical open-system variational
problem must ALSO specify which boundary traces are shared, how their
variations match, and whether the exterior responds dynamically. We have not
assumed that fixing an exterior profile and freely varying its common trace
are automatically compatible.

## 3. Transport through a cut composes; it is not a new independent clock

For a link crossing a fixed cut b, the same horizontal flow satisfies

    T_ai(s) = T_bi(T_ab(s)),
    J_ai(s) = J_bi(T_ab(s)) J_ab(s).

This follows from the ODE T_R=c(T,R), uniqueness on the positive regular chart,
and differentiation with respect to s. On the P=0 initial slice,

    J_ai = exp(g_i-g_a)
         = exp(g_b-g_a) exp(g_i-g_b).

Neither segment is an independently selectable coupling. The proper-time
conversion remains J_proper=(ell_i/ell_a)J_ai and is not a declaration that
horizontal transport equals physical interface clock gluing.

The independent verifier splits nonzero-P manufactured time histories at the
cut, integrates the two transport segments, and compares them with the unsplit
parent flow. Those histories test the action and composition, not a coupled
spacetime evolution.

## 4. Gravity boundary action and source reaction

At P=0 the first-form initial gravity-plus-matter spatial action is

    int_L^R [N mu_R/(kappa U)-N U epsilon] dR,
    U=sqrt(1-2mu/R).

Its mass variation has the radial term [N delta_mu/(kappa U)]_L^R. Retain the
inherited outer action and represent the inner Dirichlet source by a multiplier:

    S_boundary = int dt [-C_out(t) mu_Rboundary/kappa
                         +lambda_L(t)(mu_L-m_L(t))].

Here mu_Rboundary means the value at the outer cut, not a radial derivative.
The resulting initial natural/reaction conditions are

    N_Rboundary/U_Rboundary = C_out,
    lambda_L = N_L/(kappa U_L),
    mu_L = m_L(t).

These are the already owned gravity boundary terms, now checked on the new
shared-metric/crossing-link preparation. They are not inferred by fitting C1.
The retained P-squared gravity radial term has zero first variation at P=0;
it must return for higher-order or nonzero-P work.

The initial oriented mass-work expression at either cut is

    power_b = n_b N_b mu1_b/(kappa U_b) = -n_b Kbar_b,
    n_L=-1, n_R=+1.

This equality uses the action-derived mu1=-kappa U Kbar/N. It does not prove
that the crossing-link reservoir can be collapsed to rho_b chi1_b. A changing
external clock and source have their additional explicit-time work; this
checkpoint matches the sourced initial clock value, not its full history.

## 5. Reprepare the actual initial boundary data

Retain the original scalar node values, h=1/64, kinetic seed, B and S matrices.
Use the SAME two earlier cubic auxiliary-momentum directions,

    p_i = p_seed,i + K_seed,i [a(1-3x_i^2+2x_i^3)
                              +b(3x_i^2-2x_i^3)].

The common kinetic seed is loaded from its existing owner, not reconstructed
from a new fitted lapse. The layer-linear extension and its slopes are rebuilt
from the trial node values; all layer modes remain admitted by the action.

Preparation is triangular:

1. For trial (a,b), form the live epsilon and solve the shared mass ODE.
2. Correct the enlarged-domain left seed by the exact linear integrating-factor
   response so mu(L), at the ORIGINAL cut, equals the inherited inner mass.
3. Choose two endpoint-derivative lapse lifts and the inherited normalization.
4. Recompute g, all J, scalar forces and crossing currents.
5. Solve ONLY the original inner mass-drive and outer scalar-velocity equations.

No C0/C1 residual, port force or current amplitude is a fitted equation in step 5.
The root has two unknown initial-data coefficients, not new theory parameters.
As before, the inner scalar velocity is derived rather than independently fixed.

For the explicit positive lapse, set x=(R-L)/(Rcut-L), span=Rcut-L and

    ln N = ln N_base + a_N span*x*(1-x)^2
                       +b_N span*x^2*(x-1) + ln(normalization).

The added shapes vanish at both cuts and have unit derivative at their own cut
and zero derivative at the other. With A=mu/(R^2 U^2), B=kappa epsilon/R,

    a_N=A_L+B_L-(ln N_base)_L',
    b_N=A_R+B_R-(ln N_base)_R'

enforces P1=0 at the cuts. Normalization imposes N(Rcut)/U(Rcut)=C_out. These
are explicit gauge/initial-compatibility choices, not a unique lapse theorem.
The same formula is extended into the narrow exterior collars and checked for
positivity. The common primitive g is changed consistently with ln N.

Sourced targets, in the existing fixture normalization rather than SI units:

    inner mass drive = 0.00033578281226508903,
    outer scalar velocity = 0.015344562303521506,
    outer clock value = 1.0000262973362133.

Source records:
- `source-intake/navier-stokes/20260912/annular-interface-layer-clock-attempt03/GR_source_snapshot.npz`
- `source-intake/navier-stokes/20260912/annular-interface-layer-clock-attempt03/metric_Gram_source_snapshot.npz`
- `source-intake/navier-stokes/20260912/annular-cubic-lapse-boundary-attempt07/GR_corrected_initial_data.npz`
- `source-intake/navier-stokes/20260912/annular-cubic-lapse-boundary-attempt07/metric_Gram_corrected_initial_data.npz`
- `scripts/annular_canonical_common_profile_aligned_20260912.py`

## 6. Boundary-inclusive constraint tests

For a test eta that need not vanish at the cuts, retain

    C0[eta] = int [eta(U+1/U-2Uref)/(2kappa)
                    +eta_R R(U-Uref)/kappa-eta U epsilon] dR
               -[eta R(U-Uref)/kappa]_L^R.

Its mass differential includes +[eta mu1/(kappa U)]_L^R. The full first-time
constraint also includes the scalar energy rate and -int eta Kbar g_R/N dR.
Using the previously derived current identity, these terms cancel on the
shared solution without discarding endpoint flux.

Tested six polynomials with nonzero boundary traces at two quadrature orders,
in three cases per branch: beta22 at delta=h/2 and h/4, and beta23 at h/2.
All six initial preparations and both quadrature levels pass 1e-10:

| Quantity | Maximum across the six cases |
|---|---:|
| Initial boundary-condition error | 4.45e-16 |
| Boundary-inclusive C0 | 9.44e-15 |
| Boundary-inclusive C1 | 3.42e-16 |
| C1 if its radial boundary term is omitted | 0.00269 to 0.00439 |
| C1 if the connection-time term is omitted | 6.36e-7 to 9.47e-7 |

Minimum F exceeds 0.6595. The two-coefficient solves use nine or ten residual
evaluations and report convergence. Momentum changes are NOT tiny: the maximum
node change ranges from about 0.246 to 0.493. These are re-prepared data, not
unchanged original fields or observational improvements over GR.

Further verification tests the full unrestricted metric variation with the
inner multiplier and outer clock action, off-shell whole-factor partition,
finite-history transport composition, source hashes, and untouched protected
files. The final integrity report records completion and numerical errors.

## 7. The exterior-profile dependence is real and cannot be hidden

A controlled perturbation changes only the momentum of node 0 for z<0, outside
the physical annulus. Its smooth polynomial bump and first three derivatives
vanish at the cut. The initial mass is re-prepared to retain mu(L); the drive
is deliberately NOT reimposed in this counterexample.

For GR/MTS the interior metric changes by at most 1.69e-14 and all original
node scalar/momentum/velocity traces by at most 3.41e-16, but the inner current
changes by approximately 1.64e-4 / 1.62e-4. Thus these endpoint and interior
initial data alone do not determine the exterior-dependent current. Supplying
a full collar response is not equivalent to picking a point reaction rho.

There is also significant shape dependence after matching the SAME drives:
changing beta22 to beta23 at delta=h/2 changes the unprescribed outer mass rate
by roughly 38%, and the derived inner scalar velocity by roughly 30%.
For example the GR outer rates are 0.000359582 and 0.000221935. Both cases pass
the mathematical consistency checks. Therefore numerical consistency has NOT
selected a unique physical boundary prediction or justified the regulator.

## 8. Next target and stop conditions

Derive the dynamical collar/source response and its variational trace matching,
then test second-order boundary compatibility with the sourced time histories.
One possible controlled route is to retain the exterior fields dynamically;
eliminating them would instead require a derived response operator. Neither is
completed by the exact algebraic factor partition above.

Do not insert two point forces, trim crossing links, set J=1, hold exterior
histories fixed while silently allowing their shared traces to vary, or claim
that passing these initial tests solves the old forced evolution problem.
Full first jet, full physical radial-port action, full GR limit and physics
claim flags remain false. No new trajectory, GitHub action or subagents.

Implementation and evidence:
- `scripts/annular_finite_width_boundary_cut_20260913.py`
- `scripts/derive_annular_finite_width_boundary_cut_20260913.py`
- `scripts/verify_annular_finite_width_boundary_cut_20260913.py`
- `source-intake/navier-stokes/20260913/annular-finite-width-boundary-cut-attempt01/status.json`
