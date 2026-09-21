# P2 primitive radial repair and tighter error budgets

Private local continuation of `DERIVATION-20260918-moving-P2-current-and-live-evolution.md`. The previous result was an actual short coupled evolution, but three numerical controls had limited margins: radial mass-equation residual1.34e-7, material-refinement velocity difference1.61e-8 and MTS time-refinement velocity difference1.32e-8. Those quantities, not exterior-mass conservation alone, set this checkpoint's target.

This work changes numerical representation/resolution, not the physical matter action, retained Gram factors, source parameters or Einstein/polar equations. All comparisons are normalized numerical controls, not observational tests or measurements of physical coupling constants.

## 1. Reproduce the error at a fixed canonical state

The original evolved reference/MTS principal arrays are loaded from the hash-checked outputs of `source-intake/navier-stokes/20260914/annular-live-P2-current-evolution-attempt01/status.json`. Coordinates and momenta are held unchanged while the canonical inverse and radial geometry are re-solved.

`scripts/diagnose_annular_P2_evolved_radial_budget_20260918.py` locates the radial residual instead of merely reporting its maximum. In both branches it is largest in the smallest physical interval, near R=6.028868. The interval width is about2.623e-7; this is a real interval, NOT the nearly coincident1.8e-15 endpoint defect repaired earlier. No additional physical interval is deleted or merged here.

At radial degree18 the old mass derivative residual is1.2493e-7 reference and1.3334e-7 MTS. Raising the degree to24 makes it WORSE:2.4954e-7 and3.0638e-7. These higher-order diagnostic values would fail the earlier2e-7 pilot gate; they are recorded, not called improved solutions. Meanwhile velocities change by less than3.5e-17 and forces by about2.03e-13. This distinguishes a radial derivative representation problem from a comparable change in the physical trajectory.

## 2. Why differentiation amplifies the background offset

On an interval of width Delta, let x=2(R-center)/Delta. The old dense output transforms the complete mass values, including background mass about0.7, to degree-n Chebyshev coefficients and differentiates them. If coefficient/nodal roundoff perturbs that polynomial by e_n, then

    ||partial_R e_n||_infinity <= (2 n^2/Delta) ||e_n||_infinity.

This is the polynomial derivative bound after rescaling the interval. Including interpolation amplification gives a scale proportional to n^2 Lambda_n epsilon_machine |m_background|/Delta, where Lambda_n is the interpolation operator norm. This is an error-amplification bound/scale, not an equality fitted to these data.

For these narrow intervals, the simple scale epsilon_machine n^2 |m|/Delta is about1.92e-7 at degree18 and3.42e-7 at degree24. It explains why spending more on polynomial order alone does not solve the problem. The lapse representation suffers the same mechanism at a smaller amplitude.

There is a second representation issue in exact arithmetic: integrating a degree-n right-hand-side polynomial gives degree n+1, whereas reinterpolating its values onto a degree-n state polynomial need not retain that highest primitive term. The repair retains the actual primitive rather than reinterpolating the large-offset solution values.

## 3. Construct a consistent primitive dense output

Keep the SAME radial collocation fixed-point equations and all the same integration splits. On each interval e, use its final collocation right-hand sides to form

    p_m,e(x) = I_n[ f_m(R_j, m_j, log N_j) ],
    p_n,e(x) = I_n[ f_n(R_j, m_j, log N_j) ].

Store the small, degree-(n+1) increments separately from the large left endpoint values:

    Q_m,e(x) = (Delta_e/2) integral_(-1)^x p_m,e(y) dy,
    Q_n,e(x) = (Delta_e/2) integral_(-1)^x p_n,e(y) dy,
    m_e(R) = m_left,e + Q_m,e(x),
    log N_e(R) = n_left,e + Q_n,e(x).

Obtain mass left endpoints by prefix sums of Q_m,e(1), beginning at the same fixed central mass. Obtain lapse left endpoints by prefix sums of Q_n,e(1), shifted by the same outer condition N_out=U_out. This supplies matching integral boundary data, rather than independent fits on either side of an interface.

The represented geometry has the exact polynomial derivative identity

    partial_R m_e = p_m,e(x),
    partial_R log N_e = p_n,e(x).

These are derivatives of the SAME reported primitive, not values of the nonlinear ODE substituted at the query point. The nonlinear equations are still tested independently off the collocation grid:

    residual_m(R) = p_m,e(x) - f_m(R,m_e(R),log N_e(R)),

with the analogous lapse residual. Consequently an interpolation error, an unconverged nonlinear solve or a changed physical density can still fail this check.

In floating point, the new derivative evaluates the right-hand-side polynomial directly. It no longer differentiates roundoff attached to the large background offset divided by Delta. The coefficient transform still has finite numerical conditioning, and the physical right-hand side can still be poorly resolved; this is not a claim that all radial errors vanish identically.

`scripts/annular_P2_primitive_geometry_20260918.py` implements this dense-output repair. It evaluates the final right-hand side once more after the existing fixed point and rebuilds the primitive/prefix sums. In the saved-state tests this changes collocation solution values by at most2.23e-16. All original executed geometry implementations and their evidence are retained unchanged.

## 4. Tests that prevent a cosmetic residual fix

The held-state diagnostic uses both branches and five configurations each: old degree18/24, primitive degree18/24, and primitive degree18 with independently increased action/label quadratures32/16 instead of20/12. The canonical state and physical problem are identical within each branch.

The following are checked separately:

- Radial derivatives agree with complex derivatives of the actual reported mass/lapse profiles, not merely with an ODE array.
- Off-grid nonlinear residuals use independently sampled continuous-label densities.
- The new primitive agrees with the preceding collocation integral solution at its nodes.
- Re-solving the coupled canonical inverse does not create a significant field, velocity or force change at the same input state.
- Original source arrays and completed prior evidence retain their hashes.

35 checks pass in `source-intake/navier-stokes/20260914/annular-P2-evolved-radial-budget-attempt01/status.json`.

| Held-state diagnostic | Reference | MTS |
| --- | --- | --- |
| Old degree18 mass residual | 1.2493e-7 | 1.3334e-7 |
| Old degree24 mass residual | 2.4954e-7 | 3.0638e-7 |
| Primitive degree18 mass residual | 3.9400e-14 | 3.4799e-14 |
| Primitive degree24 mass residual | 5.8977e-14 | 4.9441e-14 |
| Primitive degree18 velocity change, same quadratures | 1.05e-17 | 2.09e-17 |
| Primitive degree18 force change, same quadratures | 7.63e-14 | 1.30e-13 |

The largest derivative-versus-profile differentiation discrepancy is8.33e-17. Increasing action/label quadratures changes the force by about5.82e-10 and velocity by at most5.10e-13. Those are separate quadrature sensitivities, not failures of the primitive identity. This is a numerical conditioning repair, not a new physical term that improves agreement with desired data.

## 5. Separate time and material refinements in actual evolution

`scripts/run_annular_P2_tight_error_budget_20260918.py` runs each branch independently, with at most two owned single-core BelowNormal processes and no subagents. The matched configurations are:

- Primitive radial degree18, action quadrature32, density-label quadrature20 throughout.
- Principal material degree14, maximum time step0.0005.
- Time control: same material degree14, half maximum time step0.00025.
- Material control: degree18 with the principal maximum time step.
- Same smooth physical preparation, source mass, central mass, width, coupling and normalized horizon0.004.
- Identical solver tolerances rtol2e-12 and atol2e-14 throughout, compared with2e-10/2e-12 in the earlier pilot.

The new declared gates are2e-9 for radial equations, velocity/state refinement and current, and2e-11 for exterior-mass drift. These are tighter than the preceding pilot, not relaxed gates. The source stays ordered and timelike, and no mass/current/source/force projection is applied.

The comparison to the OLD degree6 pilot changes several numerical settings together and is explicitly reported as a combined change, not an isolated estimate of one error. Within the NEW matched controls, time step and material degree change separately. A degree14-to18 comparison is not falsely called the already-failed degree6-to10 reduction test; all earlier misses remain preserved.

The time-step control halves the maximum allowed step, not every adaptive accepted step. The principal and half-cap trajectories share the same tighter adaptive tolerances. Their difference is a sensitivity check, not an experimentally established eighth-order convergence rate or a certified global integration error.

### Check quantities needed for the next comparison

`scripts/qualify_annular_P2_readout_error_budget_20260918.py` reads the saved arrays without evolving or refitting them. It reconstructs geometry from the saved coordinates/velocities and checks those velocities against the saved canonical momenta. At all five saved times it compares:

- The canonical source covector L_b at common material labels.
- The complete scalar-coordinate covector, reported separately rather than assumed equally accurate.
- The total radial density m_R/(kappa R^2), evaluated from the actual matter right-hand side on241 fixed physical radii, not set by the repaired derivative.
- The proper-clock rate sqrt(N_b^2-V_b^2/U_b^2).

The source quantity is the CANONICAL source force, not the proper acceleration after eliminating field inertia. The density is an Eulerian physical readout within this model. These are finite-resolution comparisons, not agreement with an independent continuum solution. Their declared source-force/density/clock refinement gates are2e-8; the scalar covector is reported without promoting this to a full force-vector or continuum-force pass.

## 6. Evolved results

99 successful implementation checks:35 held-state radial diagnosis/repair checks,21 tighter reference-evolution checks,21 tighter MTS-evolution checks and22 saved-state force/density/clock checks. No new failed attempt is introduced; all33 inherited failed attempts and4 original flat-force failures remain unchanged. These are implementation/refinement checks, not99 independent physical validations.

All six new trajectories finish the same normalized horizon0.004. Source and spatial maps remain ordered, source motion remains timelike and no conservation correction is applied.

| Tighter evolution diagnostic | Reference | MTS |
| --- | --- | --- |
| Principal evolved radial mass-equation residual | 4.675e-14 | 5.730e-14 |
| Largest exterior-mass drift across the three controls | 3.331e-16 | 7.772e-16 |
| Evolved action-derived current residual | 6.800e-12 | 8.395e-12 |
| Evolved scalar-on-shell current residual | 6.800e-12 | 8.420e-12 |
| Half-cap whole-state difference | 5.33e-15 | 1.491e-12 |
| Half-cap maximum velocity difference | 3.683e-15 | 1.973e-11 |
| Degree14-to18 whole-state difference | 6.617e-11 | 7.145e-11 |
| Degree14-to18 maximum scalar velocity difference | 1.826e-9 | 1.831e-9 |
| Degree14-to18 source velocity difference | 1.782e-11 | 2.145e-11 |
| Degree14-to18 sampled metric-mass difference | 2.088e-14 | 2.210e-14 |

Compared with the preceding pilot, the radial derivative representation floor is removed rather than hidden by a higher gate. Measured MTS time-cap sensitivity falls from1.32e-8 to1.98e-11. Material-refinement velocity sensitivity falls from about1.61e-8 to1.84e-9. The latter passes the new2e-9 gate but remains close to it; it is now the leading tested refinement difference. Do not describe every component as accurate to machine precision just because the mass drift is small.

The adaptive right-hand-side counts are113/209 for reference principal/half-cap and221/209 for MTS. In particular, a smaller step cap need not double the MTS step count. No temporal convergence order is inferred from those counts.

The old-to-new comparison, which combines several changed numerical settings, has maximum velocity differences3.15e-9 reference and1.36e-8 MTS. It remains recorded as a combined change, not attributed entirely to the radial repair or treated as an isolated continuum error estimate.

### Force, density and clock budget

| Saved-state degree14-to18 readout difference | Reference | MTS |
| --- | --- | --- |
| Canonical source force | 2.502e-10 | 3.200e-10 |
| Total radial density on241 physical radii | 4.409e-12 | 3.714e-12 |
| Proper-clock rate | 7.931e-13 | 1.301e-12 |
| Scalar-coordinate force covector | 8.506e-8 | 8.506e-8 |

The source-force/density/clock budgets pass their separately declared2e-8 gates. The scalar-coordinate covector is noticeably more sensitive than those readouts and is NOT certified at2e-8 by this result. Its time-cap difference is1.51e-13 reference and3.30e-9 MTS. The source quantity above is still the canonical force, not the independently reduced proper acceleration or a continuum pressure-force prediction.

This distinction prevents a misleading conclusion: we have removed the roundoff-limited radial diagnostic and improved practical evolution controls without changing the model, but we have not proved full force-vector convergence or a continuum GR limit. The next comparison can use a much clearer numerical budget instead of interpreting solver artifacts as theoretical failure.

All owned numerical workers finished. Require `source-intake/navier-stokes/20260914/annular-P2-tight-error-budget-final-integrity.json` to have state complete before treating this note as sealed.

## 7. Scope and next physical comparison

The clock/current construction remains the explicitly chosen source-anchored horizontal extension from the preceding note, not a unique parent-covariance theorem. Material labels still use collocation rather than an exact finite-label Galerkin action. The Einstein/polar geometry is inherited; this checkpoint does not derive the full Einstein sector from microscopic MTS assumptions.

The error controls now pass. Next compare the waveform and source force with the independently implemented continuum spherical reference at fixed positive source width and the same boundary preparation, carrying the measured material/time/readout differences into the comparison. Start with a controlled short interval and spatial refinement rather than jumping to a long horizon. Keep canonical source force, reduced proper acceleration and full scalar-force residual distinct. Do not rerun the completed radial-conditioning diagnosis as a new scientific stage.

Tight conservation and local radial constraints do not answer that continuum question. The4 original flat full-horizon force failures remain failed, and no unrestricted GR/PPN, long-time stability or observational claim follows.

## Evidence

- `source-intake/navier-stokes/20260914/annular-P2-evolved-radial-budget-attempt01/status.json`
- `source-intake/navier-stokes/20260914/annular-P2-tight-budget-reference-attempt01/status.json`
- `source-intake/navier-stokes/20260914/annular-P2-tight-budget-MTS-attempt01/status.json`
- `source-intake/navier-stokes/20260914/annular-P2-readout-error-budget-attempt01/status.json`

Executed scripts/evidence are immutable. This note is not sealed until the final integrity ledger completes. All work remains local/private; no GitHub action.
