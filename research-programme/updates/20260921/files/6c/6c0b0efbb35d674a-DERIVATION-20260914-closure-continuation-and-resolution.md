# Closed-system continuation, resolution and a conditional smooth-limit bound

Private continuation, local date2026-09-14. This extends the joint boundary–geometry solve; it does not claim the full physical MTS-to-GR limit.

## 1. The two questions addressed

First: does the closed source/exterior/geometry system survive a longer interval and a finer numerical representation without retuning its preparation?

Second: what does the ACTUAL extra Gram term in this annular candidate do when the physical lattice spacing shrinks? Resolution convergence at a fixed spacing cannot answer that second question by itself.

The first is tested by coupled evolution and independent numerical controls. For the second, a conditional action/weak-variation bound is derived from the actual third-difference factorization. The required uniform smoothness of solutions is NOT assumed proved.

Owners:

- `DERIVATION-20260914-joint-boundary-geometry-closure.md`
- `DERIVATION-20260913-live-exterior-response-and-energy-exchange.md`
- `scripts/annular_joint_boundary_geometry_20260914.py`

GR-control and MTS metric-Gram are the two existing branches of this apparatus/regulator candidate. Neither label makes these experiments a complete physical GR initial-boundary value problem.

## 2. What is held fixed and what is varied

The physical scalar lattice still has17 nodes, h=1/64 and collar width=h/2. The beta22 layer weight, source profile, fixed enlarged lower mass seed and saved exterior amplitudes are unchanged within each branch.

Layer polynomial degrees12,16,20 give851,1123,1395 dynamical components. Corresponding radial constraint degrees are32,40,48; current integration degrees48,60,72. Comparing those grids tests numerical RESOLUTION of the same finite-width model. It does not change h or remove the physical collar.

Common-coordinate scalar, momentum, clock and source-energy profiles are compared at65 layer offsets, rather than subtracting differently sized raw state vectors. The initial profiles, physical factor matrices, source amplitudes, spacing and width are explicitly checked for agreement across resolutions.

The previous maximum interval0.004 is extended to0.032 in PILOT units, not SI seconds. Readouts at0.004,0.008,0.016,0.032 expose the continuation. The unchanged apparatus family is

    D_eta(theta)=D0+V0 theta+aProper theta^2/2+eta theta^3/6,

with eta=-1,0,+1. These are declared source-history choices, not newly fitted fundamental couplings. Source displacement/velocity/acceleration at theta=0, initial state, initial geometry and initial source energy remain the saved ones.

The GR and MTS branches have their previously declared different microscopic exterior preparations. No claim of identical microscopic initial conditions across branches is made.

## 3. Continue the actual closure, not a supplied-metric surrogate

At degrees16 and20, an unperturbed long baseline is evolved to form the response operator. The retained/exterior Schur solve predicts the changed history for eta=-1,+1. It is then corrected against the full nonlinear time-node residual with geometry reconstructed from the trial state on every evaluation.

Temporal polynomial degrees16 and32 give17 and33 time nodes. BOTH linear and nonlinear temporal-resolution comparisons are made. The background Jacobian is reused only as a chord-Newton solver preconditioner; the nonlinear geometry is not frozen.

Each perturbed prediction is saved before its matching perturbed coupled reference is calculated. No changed metric or retained-field history is supplied to the predictor. Degree12 provides an additional coarse-resolution direct evolution, not a separate low-resolution Schur claim.

A fresh full variational solve checks the long-interval linear response. Independent verification adds:

- Full nonlinear RK4 at128 and256 steps on the highest spatial resolution.
- Separate integrations stopping at0.008 and0.016, compared with the corresponding prefix of the long evolution.
- The independently derived radial mass/lapse response at the final time.
- Reloaded common-coordinate spatial comparisons and feedback-resolution tests.

A prefix check tests consistency of the implemented initial-value evolution; it is not a relativistic causality theorem.

## 4. Budgets and diagnostics retain their meaning

The inherited laws remain

    M_L,tau=-kappa (U_L/N_L) K_L,
    E_tau=-rho D_eta'(theta),

with source kinetic density and reservoir energy included in the radial constraints. The mass-law derivative is checked along the LIVE RHS, not against a frozen field sample.

The experiment records radial constraint error, live mass-law error, integrated inner mass and source-energy balance, full-support mass drift, positive-chart margin, lapse, and source-energy reserve. Reported minima are sampled numerical diagnostics, not rigorous interval enclosures or global positivity theorems.

The old affine inner history is still only a diagnostic:

    Delta=M_L-M_L(0)-gamma theta_inner,
    gamma=M_L,tau(0)/N_L(0).

It is not imposed and must not be silently counted as satisfied. A larger affine-history defect is not by itself a conservation failure of the declared closed extension.

Deleting exterior feedback is a negative control. Its output effect is called resolved only when it exceeds both100 times the fresh tangent-comparison error and an absolute1e-13 floor. The same rule is used for each branch and for the inner-current component separately. Numerical resolution does not imply experimental detectability.

Authoritative run results, including any failed gates, are in the main status and final integrity file. The main runner retains failed scientific gates and continues the other cases; a failed gate is not made into a pass by completing the run.

### Main-run result

The full matrix completes all72 main checks with no failed gates:18 direct trajectories (three source protocols at three resolutions in each branch), eight nonlinear joint predictions, and four long-interval response/reference comparisons. Independent verification is recorded separately in the final authority file.

| Maximum error or minimum reserve across the main matrix | GR-control | MTS metric-Gram |
|---|---:|---:|
| Common-coordinate spatial profile difference | 7.986e-12 | 4.686e-12 |
| Spatial output difference | 1.155e-14 | 1.133e-14 |
| Nonlinear17-versus33-time-node difference | 3.997e-15 | 4.663e-15 |
| Nonlinear predicted-state versus fresh evolution error | 9.548e-15 | 1.435e-14 |
| Nonlinear predicted-output error | 4.441e-16 | 7.460e-17 |
| Full-support mass drift | 1.044e-14 | 1.177e-14 |
| Integrated inner-mass balance error | 1.792e-15 | 1.696e-15 |
| Integrated source-energy balance error | 1.193e-18 | 2.060e-18 |
| Sampled minimum F | 0.65934829 | 0.65934792 |
| Sampled minimum N | 0.81186844 | 0.81186843 |
| Sampled minimum source E | 0.00049757124 | 0.00050438965 |

At the highest resolution, removing exterior feedback changes the new source's predicted inner-current tangent by4.9353e-11 in GR and8.8814e-11 in MTS. Both now pass the declared numerical resolution gate. These are pilot-unit derivative differences, not observational detection claims.

The unperturbed affine-inner-history defects at tau=0.032 are -1.91887e-6 (GR) and -1.75427e-6 (MTS). The arbitrary affine history is therefore still not enforced in either branch. Its changing relative errors do not establish empirical preference for either model.

## 5. Derive the extra-term smooth-limit bound

This concerns the specific extra Gram correction of the CURRENT annular candidate. It is not a statement that every MTS sector or coupling has the same limit.

Actual owners:

- `scripts/annular_covariant_scalar_action_20260912.py`
- `scripts/annular_gram_joint_action_20260909.py`
- `scripts/sbp4_compatible_second_operator_20260909.py`

At a fixed time and translated lattice, let d=Delta_h^3 chi. The extra potential is

    V_G,h = (1/(2h)) d^T Q(C) d,
    C_i=R_i^2 N_i U_i > 0.

The Gram factors are third differences and weighted sums/differences of neighboring third differences. Their metric sampling weights are nonnegative and sum to one. Thus for 0<C_i<=C_max,

    0 <= Q(C) <= C_max Q(1)

in the quadratic-form sense. This uses the actual positive factor decomposition, not an assumed sign of an arbitrary truncation term.

### Exact matrix bound, including boundary closures

For node counts>=17 the left boundary patterns and their reflected right counterparts are disjoint. The four relevant diagonal entries are

    59097/573104, 1825/25284, 491/7056, 5/72.

Their sums of absolute incident off-diagonal weights are respectively

    253/50568+1/392,
    253/50568+3/392,
    3/392+1/144+1/392,
    1/144+1/144.

Each diagonal minus its incident sum is positive. Each diagonal plus its incident sum is at most1/8. Symmetry and the row-sum bound therefore imply

    ||Q(1)||_2 <= 1/8,
    0 <= V_G,h <= C_max ||Delta_h^3 chi||_2^2/(16h).

The helper checks these inequalities with exact rational arithmetic, not a fitted numerical eigenvalue. Count17 is the minimum supported disjoint-closure count in the source implementation.

### Smooth sampling bound

Suppose the nodal values are samples of chi in H^3 on the fixed physical interval. The integral identity for a third difference is

    Delta_h^3 chi(R_i)
      = integral_[0,h]^3 chi'''(R_i+s1+s2+s3) ds1 ds2 ds3.

Cauchy–Schwarz supplies a factor h^3. The density of the sum s1+s2+s3 is bounded by h^2, and the intervals [R_i,R_i+3h] overlap at most three times almost everywhere. Consequently

    sum_i |Delta_h^3 chi(R_i)|^2
      <= 3 h^5 ||chi'''||_(L2)^2,

and hence

    0 <= V_G,h
      <= (3 C_max/16) h^4 ||chi'''||_(L2)^2.

For a scalar variation v and an independent metric-coefficient variation delta C, the same factorization gives

    |delta_chi V_G,h[v]|
      <= (3 C_max/8) h^4 ||chi'''||_2 ||v'''||_2,

    |delta_C V_G,h|
      <= (3 ||delta C||_infinity/16) h^4 ||chi'''||_2^2.

These are energy and WEAK-VARIATION bounds, not pointwise strong-force bounds. They extend over the normalized nonnegative layer measure by integrating the right-hand sides for the translated profiles. Over time, an appropriate uniform time-integrated H^3 bound is needed.

The conclusion is conditional: this extra correction vanishes at least as O(h^4) for uniformly controlled smooth profile families and bounded regular metric coefficients. It does not follow merely because a fixed-grid calculation ran successfully.

### Why smoothness cannot be omitted

For the alternating sequence chi_i=(-1)^i, third differences do not become small as h decreases. The ratio of extra Gram energy to the base nearest-neighbor energy remains of order one. Both energies can grow rather than vanish.

The stronger finite-energy control is chi_i=h*(-1)^i on the unit interval with C=1. Its base nearest-neighbor energy is exactly2, while the extra Gram energy stays nonzero (approaching8/3 from the interior symbol; boundary corrections are O(h)). Thus bounded scalar energy ALONE cannot justify deleting the correction. Each nodal family can be sampled from a smooth oscillatory function, but its H^3 norm is not uniformly bounded. This is an algebraic counterexample to the proposed energy-only implication, not a newly constructed full coupled spacetime or an observed physical effect.

The checker uses four scalar lattices with17,33,65,129 nodes on a FIXED unit interval. Smooth analytic trial profiles test the energy and both weak-variation bounds; alternating profiles demonstrate the non-decoupling counterexample. These are manufactured spatial tests, not the evolved annular trajectories and not a full physical h-refinement of their source apparatus.

Accordingly:

- The conditional correction bound is derived.
- Uniform H^3 control of the actual evolving h-family is NOT derived.
- Convergence of solutions, boundary/source terms and the full GR limit is NOT proved.

This also distinguishes a finite-regulator artifact from a surviving physical prediction. We must not advertise a correction that vanishes under the required smooth continuum limit as established new continuum physics.

## 6. What the next GR-facing calculation should be

Do not equate another increase of layer polynomial degree with progress toward the physical continuum limit.

The next useful target is to propagate the conditional correction bound through the already derived radial geometry response, then construct a genuinely h-refined family on a fixed physical annulus with matched smooth scalar/source preparation. The mass seed, boundary protocol and source work must have explicit owners throughout that comparison.

The crucial unresolved issue is whether these sufficient regularity and metric bounds remain controlled for solutions, rather than being imposed as a new plateau/smoothness axiom. Uniform H^3 control is sufficient for this bound, not proved necessary for convergence; a weaker energy/compactness argument might replace it. The previous highly localized exterior preparation must not be copied onto a changing lattice without checking what it does to those norms and to its total energy.

A vanishing Gram action difference alone does not prove MTS reduces to vacuum GR: the candidate still has its scalar sector and apparatus, and the other parent-theory requirements remain. It is a concrete consistency step for the selected correction.

## 7. Evidence and limitations

- Continuation helper: `scripts/annular_closure_continuation_20260914.py`
- Main runner: `scripts/derive_annular_closure_continuation_20260914.py`
- Smooth-limit helper: `scripts/annular_gram_smooth_limit_20260914.py`
- Independent verifier: `scripts/verify_annular_closure_continuation_20260914.py`
- Main status: `source-intake/navier-stokes/20260914/annular-closure-continuation-attempt01/status.json`
- Final authority: `source-intake/navier-stokes/20260914/annular-closure-continuation-final-integrity.json`

The main output directory contains predictions, references, common-coordinate profiles and response operators. The independent directory contains RK4/radial controls and the exact-bound/manufactured-profile report.

No full GR/Newton limit, regulator removal, long-time stability theorem, physical apparatus completion, horizon crossing, or experimental preference is claimed. All calculations remain private. Only one below-normal single-core worker is used. The protected-workbench check is an mtime scan since2026-09-13T23:38:53Z, not a pre-turn content-hash snapshot. The final seal owns the note and a resume snapshot; any subsequent completion line in the mutable resume intentionally postdates that snapshot.
