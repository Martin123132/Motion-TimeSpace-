# Actual source reflection, boundary repair, and a derived source-loading law

Private working derivation, 2026-09-14. Numerical runs and independent checks are complete. This is a restricted spherical annular test, not a full-GR limit or an observational claim. No production parameters are retuned. The failed old-boundary control and first absolute radial audit are preserved rather than relabelled.

## 1. What changed

The old independent continuum solver was only checked while the compact pulse had not reached the boundary. Its one-sided endpoint derivative is not qualified for active reflection: an exact flat-space radial eigenmode develops *larger* errors as its grid is refined. This is a baseline numerical failure, not a discrepancy attributable to MTS. The old successful quiet-boundary evidence remains intact, but must not be extrapolated to arbitrary reflection.

The replacement changes the continuum boundary discretization, not the scalar field equation, gravitational constraints, initial pulse, source energy, or clock. Both regulator branches are compared with the same independent replacement. The original pulse is evolved to t=0.45, far enough to exert a substantial force on the source, rather than testing another quiet boundary.

## 2. Boundary energy cancellation, derived before comparison

Write u=chi_R, p=R^2 chi_t/L, L=NU>0. For a frozen positive metric,

    u_t = D(L p/R^2),     p_t = D(R^2 L u).

The endpoint constraints are u_left=0 and p_right=0; the right scalar value is fixed to zero. Use a positive diagonal quadrature H with endpoint weights

    H/h = (17/48, 59/48, 43/48, 49/48, 1, ..., 1,
           49/48, 43/48, 59/48, 17/48).

The boundary derivative in `scripts/annular_reflecting_boundary_20260914.py` obeys

    H D + D^T H = diag(-1, 0, ..., 0, +1).

This identity is verified using exact rational arithmetic, and separately against the implemented operator. The interior derivative is fourth order; the endpoint closure is second order. The positive energy is

    E_H = (1/2) sum_i H_i L_i (R_i^2 u_i^2 + p_i^2/R_i^2).

Set w=L p/R^2 and f=R^2 L u. With the constrained endpoint rates projected to zero,

    dE_H/dt = f^T H D w + w^T H D f = [w f]_left^right = 0.

The projections do not contribute because their energy multipliers are zero on the constrained components. This is an exact semidiscrete *frozen-metric* statement. When gravity evolves, L_t contributes and E_H is not the conserved gravitational mass; the coupled calculation must independently check total mass and radial constraints. No nonlinear arbitrary-boundary stability theorem is inferred from this calculation.

An exact flat radial solution is

    chi(R,t) = A sin(k(6-R)) cos(kt)/R,
    5 k cos(k) + sin(k) = 0,    pi/2 < k < pi.

It satisfies chi_R(5,t)=0 and chi(6,t)=0 and has nonzero source gradient. A=0.11. Through t=2 the new energy-norm errors at65/129/257 nodes are 8.12928e-7, 1.01069e-7, 1.25950e-8; its relative frozen-metric energy drift is below1.6e-15. These are observed approximately third-order solution errors on this mode, not a general rate theorem. The old operator gives 1.58033e-8, 2.42964e-7, 3.15435e-3: it fails refinement despite the initially smaller coarse-grid error.

Evidence: `source-intake/navier-stokes/20260914/annular-reflecting-boundary-attempt01/status.json`.

## 3. A stationary boundary can experience force without doing work

The common source remains at b=6 with angular-reduced proper reservoir S=0.003 and kappa=0.1. All these are the existing pilot-unit values, not SI measurements. Its scalar condition is chi(b,t)=0, hence p(b,t)=0. This imposes

    scalar energy flux = L p chi_R = 0,

but not chi_R=0. The canonical boundary reaction in the reduced scalar equation is

    f_b = b^2 L_b chi_R(b,t).

Here f_b is conjugate to the scalar value chi; it is not by itself the radial mechanical force on a moving material worldtube. Its scalar work rate is f_b chi_t(b,t)=0 while f_b can be large. The inward and outward characteristic amplitudes are w+L u and w-L u. At the fixed Dirichlet boundary they are opposite, rather than both zero. Energy conservation alone therefore cannot certify the source stress or its physical admissibility. Saved numeric fields named wall_force and holding_reaction_mean use this scalar-conjugate convention.

The initial pulse and both production regulators are unchanged. First interaction is examined through t=0.45, not an entire return trip. This is a two-boundary annulus: the inward-going part can also reach the inner reflecting boundary. Neither endpoint is identified with a regular centre or a black-hole horizon, and no material model for an inner apparatus is established. The long time is numerical evidence only: the existing uniform analytic interval t<0.00083457693 is not extended by these runs.

## 4. Exact surface stress from the junction, including the wave

Use the existing thin-shell identification, outward increasing-R normal on both sides, vacuum exterior, and continuous lapse. Define

    U_- = sqrt(1-2m_-/b),
    U_+ = U_- - kappa S/b > 0,
    N_b = (U_-+U_+)/2,
    Sigma = S/b^2,
    e_- = (b^2 u_-^2 + p_-^2/b^2)/2 = b^2 u_-^2/2.

The surface pressure derived from the curvature jump is

    P = Sigma/4 [1/(U_- U_+) - 1] - U_- e_-/(2b).

To check the sign and normalization independently, use

    Ktheta_+ = U_+/b,  Ktheta_- = U_-/b,
    Ktau_+ = m_+/(b^2 U_+),
    Ktau_- = m_-/(b^2 U_-) + kappa U_- e_-/b,
    P = ([Ktau]+[Ktheta])/(2 kappa).

Substituting m_+-m_- = kappa S U_--(kappa S)^2/(2b) gives the stated law. The source correction is not a vacuum pressure once the wave arrives. In terms of the canonical scalar-boundary reaction,

    P = P_vac - f_b^2/(4 b^3 N_b^2 U_-).

This explicitly links the previously measured source reaction to the missing supporting tension. It does not derive a source matter action.

## 5. Derived classical source-energy threshold

For isotropic timelike surface matter, a null vector tangent to the surface contracts its stress tensor to a positive normalization times Sigma+P. Thus the surface null energy condition requires Sigma+P>=0. With S>=0 and U_+>0,

    S [3 + 1/(U_- (U_--kappa S/b))] >= 2 b U_- e_-.

This is a condition on the chosen classical source interpretation, not an assumption that every possible quantum or effective source must satisfy it.

Let F=U_-^2, y=kappa S/(b U_-), C=2 kappa e_- F and B=3F+1+C. The inequality becomes

    -3F y^2 + B y - C >= 0,    0<=y<1.

The left-hand form y[3+1/(F(1-y))] is strictly increasing on this interval. The discriminant is positive:

    B^2-12F C = (C+1-3F)^2+12F > 0.

Consequently the unique lower threshold is

    y_min = 2C/(B+sqrt(B^2-12F C)),
    S_min = (b U_-/kappa) y_min.

This is a derived loading threshold, not a number assumed missing from the corpus. Its derivation holds at fixed instantaneous interior mass and scalar trace. The numerical maximum over sampled times is not a rigorous maximum over all continuous times.

Already on the2049-node trajectory the first sampled violation is t=0.31, the minimum Sigma+P is about-0.0234891, and the maximum sampled S_min is about0.773956, compared with the assigned S=0.003. This failure concerns the current low-energy rigid-shell interpretation. The mathematical externally constrained reflecting boundary remains usable, and the test must apply equally to the GR reference and MTS.

## 6. Why adding reservoir energy is not yet a parent-action derivation

In this continuum problem m_-(b) is constant because the boundary flux vanishes. Thus U_-(b) is constant. The bulk constraints are independent of S; changing S changes the boundary lapse

    N_b(S) = U_-(b)-kappa S/(2b)

and multiplies all bulk L values by a constant. The interior evolution has the form Y_t=N_b(S) V(Y). For two admissible constant reservoirs, the same orbit is therefore related by

    Y_new(t) = Y_old(c t),    c=N_b(S_new)/N_b(S_old).

This is a conditional clock-rescaling identity for the *continuum fixed-shell family*. It is not asserted as an exact identity of either finite-collar regulator. It explains why a counterfactual larger S can be tested on corresponding points of the existing interior orbit without pretending a production parameter has been derived. A numerical check of S=0.8 is explicitly counterfactual; the production source remains0.003.

Even if the energy condition is restored at the sampled points, a single autonomous barotropic surface with P=P(Sigma) cannot support this fixed-radius pulse history: Sigma is constant whereas the required P varies with e_-(t). Extra source degrees of freedom, a moving surface, or an acknowledged external constraint are required. This is a conditional obstruction to that simple source model, not a theorem excluding all matter models or MTS.

For an adiabatic spherical material surface at fixed particle number, the first law also fixes the pressure rather than allowing it to be prescribed independently. With physical energy4pi S(b) and area4pi b^2,

    d(4pi S) = -P d(4pi b^2),
    Sigma=S(b)/b^2,     P=-S'(b)/(2b).

Equivalently a local surface energy density rho(n) gives P=n rho_n-rho and n proportional to b^-2. The next derivation target is a covariant dynamical surface model with this stress relation, a comoving scalar boundary condition, and consistent energy exchange. Choosing rho(n) without deriving or otherwise justifying it would remain an explicit matter-model assumption.

## 7. Numerical status and limitations

The513/1025/2049-node coupled runs show mass drift decreasing from9.40e-8 to1.43e-9, and field/metric refinement during actual impact. Independent active RK4 versus DOP853 gives a maximum state difference1.29e-14 on the declared short segment; this is a time-integration cross-check, not a total error bar.

The first independent radial audit narrowly **failed** its unchanged absolute2e-9 gate at t=0.37: mass error2.039559743e-9, lapse error3.95736e-10. The failure and executed script are retained in `source-intake/navier-stokes/20260914/annular-collision-support-verification-attempt01/status.json`. A4097-node rerun passes the same gate without loosening it: mass error2.53985e-10 at.37 and4.14803e-11 at.45. Halving the independent radial integrator step changes these comparisons by less than5.3e-15. No successful label is substituted into the failed attempt.

At4097 nodes the total-mass drift is1.78239e-10. The2049-to4097 maximum differences over saved times are chi1.67771e-8, u2.86421e-6, p9.22924e-5, m2.37263e-9 and logN7.08955e-10. They are refinement differences, not certified error bounds. The refined maximum sampled source threshold is0.7739568153; the first sampled null-condition violation remains.31 and the minimum Sigma+P is-0.0234891674. Resolution did not remove the source-loading problem.

### Completed same-target comparison

Both regulators use the4097-node continuum target, with2049-to4097 refinement differences subjected to the same2% resolution gate. The largest actual target-noise/error ratio among the tested components is0.0224391%, well below that gate. This compares numerical resolution, not observational error or theoretical certainty.

At t=0.45:

| Branch | Nodes | Common-coordinate energy error | Physical-position energy error | Max mass error | Max log-lapse error |
| --- | ---: | ---: | ---: | ---: | ---: |
| Reference |33|4.42601e-3|4.23208e-3|2.67345e-4|2.08284e-4|
| Reference |65|1.26250e-3|1.28836e-3|1.70753e-4|7.34387e-5|
| Reference |129|2.36288e-4|2.45046e-4|5.23801e-5|2.65850e-5|
| MTS |33|1.50516e-3|1.61757e-3|1.65231e-4|1.33584e-4|
| MTS |65|3.56292e-4|3.90897e-4|1.17684e-4|6.01297e-5|
| MTS |129|9.83666e-5|1.08131e-4|4.27924e-5|2.50198e-5|

The common-coordinate diagnostic is half the squared joint-layer p/gradient norm with weights omega_i/R_i^2 and h R_mid^2. The physical-position cross-check evaluates the target at actual collar radii, using strictly interior momentum nodes and all interior edge midpoints; it does not extrapolate. These are different explicitly defined norms, not interchangeable measures. Metric errors use the same fixed physical probes5..5.95; exterior total mass is tested separately.

All five declared field/metric norms decrease on refinement for both branches at each collision sample.3,.4,.45. The physical-position energy error decreases about17.27-fold for the reference and14.96-fold for MTS from33 to129 nodes. MTS having smaller finite-grid errors here is not evidence that it physically outperforms GR: GR is the common target.

The maximum sampled canonical source-reaction errors over samples at and after.3 decrease reference1.14895 -> .591797 -> .218420 and MTS.572123 -> .308406 -> .0903252. At.45 both finest-grid source reactions are within.00462 of the continuum value-2.588212614. This sampled maximum is not a continuous-time uniform bound. Total-mass drift in every regulator run is below6e-15; that conservation diagnostic is not the field-solution error. Source scalar work is zero in both branches throughout the saved trajectory.

The S=0.8 counterfactual retains positive sampled dominant-energy margins, minimum0.00079743. Its interior clock ratio is0.992236322095, constant to about3.3e-13 on the tested states; direct vector-field rescaling residuals are below4.5e-12. This validates the conditional clock-rescaling calculation and shows how increased supporting energy affects this restricted family. It does **not** select S=0.8 as an MTS parameter, solve the source constitutive problem, or prove a continuous-time energy-condition bound.

Validation records: boundary20, original active continuum13, refined target18, regulator398 and final comparison136 checks pass. These are implementation checks, not585 independent physical experiments. The first absolute radial verification attempt remains failed and is explicitly accounted for by the higher-resolution rerun; the classical low-energy source remains physically inadmissible under the stated surface condition.

### What this advances, and what comes next

This moves the numerical GR comparison from a quiet source to actual wave/source interaction and removes a demonstrated baseline boundary error. It also converts an unspecified supporting-stress gap into an explicit pressure law, a minimum classical loading threshold, a clock-rescaling identity, and a conditional obstruction to a fixed-radius single-barotropic surface.

Next derive a covariant dynamical source with its own stress and motion, use the surface first law rather than prescribing P(t), and derive the comoving scalar condition and energy transfer. Keep the present rigid-source run as a preserved control. A successful future source model must face the same tests in the GR reference and MTS. No full-GR, horizon, black-hole regularity, unrestricted existence, or parent-action-completion claim follows from this checkpoint.

## Resource and preservation record

All work is private and confined to post-checkpoint-work. Original executed files and failed evidence are preserved. At most two numerical workers overlap, each BelowNormal and limited to one logical processor. During the final regulator run the identified worker alone was moved from saturated logical processor0 to lightly loaded processor10; the one-processor cap and priority were unchanged. No other task was stopped. The4097-node run saves selected states rather than retaining a multi-gigabyte dense interpolant. Each regulator time segment is saved separately for crash recovery.

## Source paths

- `DERIVATION-20260914-reference-continuum-and-source-shell.md`
- `DERIVATION-20260914-layer-locking-and-restricted-evolving-GR-limit.md`
- `DERIVATION-20260914-independent-continuum-GR-comparison.md`
- `scripts/annular_reflecting_boundary_20260914.py`
- `scripts/test_annular_reflecting_boundary_20260914.py`
- `scripts/run_annular_source_collision_continuum_20260914.py`
- `scripts/run_annular_source_collision_regulators_20260914.py`
- `scripts/verify_annular_collision_and_support_20260914.py`
- `scripts/refine_annular_collision_target_20260914.py`
- `scripts/finalize_annular_source_collision_20260914.py`
- `source-intake/navier-stokes/20260914/annular-source-collision-continuum-attempt01/status.json`
- `source-intake/navier-stokes/20260914/annular-collision-refined-target-attempt01/status.json`
- `source-intake/navier-stokes/20260914/annular-source-collision-regulators-attempt01/status.json`
- `source-intake/navier-stokes/20260914/annular-source-collision-final-comparison-attempt01/status.json`
- `source-intake/navier-stokes/20260914/annular-source-collision-final-comparison-attempt01/collision-comparison.csv`
