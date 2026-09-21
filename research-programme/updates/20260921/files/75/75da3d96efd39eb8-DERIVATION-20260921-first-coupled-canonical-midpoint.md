# First coupled canonical midpoint pilot

Private continuation of `DERIVATION-20260921-action-owned-coordinate-covectors.md`.

Status: COMPLETE for the tiny coupled midpoint pilot, equal-branch step refinement,40/64-digit arithmetic comparison, finer integration rule and independently perturbed-seed reversal. All declared numerical gates pass. This is a conditional evolved candidate calculation, not a full GR-limit or physical-force convergence result.

## 1. What changes from the previous checkpoint

The earlier stages qualified an initial self-consistent candidate metric, all 16,425 material-weighted momenta, their full local inverse, and matching coordinate covectors. They did not integrate their coupled dynamics. This stage implements the actual common-space, source/field/gravity midpoint step; the metric is re-solved at every nonlinear trial.

All 1,094 field coordinates at each of 15 material nodes, plus 15 source coordinates, remain active. There is no low-mode cutoff, native-subspace projection, fitted parameter or frozen-source substitution. Reference, primary MTS and alternative MTS receive the same time interval and numerical controls. The inherited polar, zero-shift, finite-width candidate is still conditional; this is not a claim to have derived the full GR limit or repaired the older physical-force/spatial discrepancies.

## 2. Same action, moving common state

The state is stored as Decimal position and momentum arrays. The original rational embedding is applied before rounding, and subsequent positions are updated directly in the full common space rather than being reconstructed from native coarse coordinates. At every trial the local P2 derivative polynomials and Gram factors are evaluated at high precision before converting their sampled values to binary64. Thus a small change in a field coefficient is not thrown away before a high-order difference is taken.

The new stable common-material adapter evaluates density gradients from those prepared local derivative polynomials. It rebuilds the moving material support, radial integration partitions, source density and Gram density. Candidate gravity is solved at radial degree22 with label order28; positive source/spatial map Jacobians, F>0 and a timelike source clock are retained. Geometry sampling and solves remain binary64; Decimal state handling does not turn the physical inputs or metric into 64-digit measurements.

Momentum and force are accumulated together on the SAME reference/material quadrature, initially orders (10,32). Inherited field and source terms, moving-radius metric gradients, Gram transpose and proper-clock terms are retained. The gravity solve and the reference/material action use different numerical integration organizations; the earlier independent on-shell tests support their agreement in tested directions, but this does not prove exact finite-dimensional variational stationarity.

Initial common-state forces are compared against the sealed preceding force vectors. The reference/material momentum is compared independently against the earlier radial/material momentum calculation. The old momentum array is not silently reused after changing quadrature.

## 3. Coupled implicit step and stopping rule

For a step h, the only nonlinear unknown is the midpoint velocity v. At each trial,

    q_m = q_0 + h v/2,
    R(v) = P(q_m,v) - p_0 - h F(q_m,v)/2.

After convergence,

    q_1 = q_0 + h v,
    p_1 = p_0 + h F(q_m,v).

P and F come from the current candidate action and current solved gravity, not the old prescribed metric. Position and momentum increments are accumulated in Decimal arithmetic. The formal Jacobian remains

    R_v = P_v + h(P_q-F_v)/2 - h^2 F_q/4.

The existing complete, positive fixed-metric mass matrix is used ONLY as a preconditioner for defect corrections. It does not replace the live momentum, force, source clock or gravity in the residual. All field/material bands and the full 15-component source Schur block are retained. This pilot tests convergence of that inexpensive preconditioner at a deliberately short interval, rather than asserting a global contraction theorem.

Both stopping conditions must hold: relative diagonally scaled residual below 5e-12 AND maximum mass-preconditioned velocity correction below 2e-12. The solver allows at most20 iterations and stops with a saved failure if a residual grows by more than25%; it never deletes modes or silently decreases the step. Radial residual must remain below2e-12. The old frozen scalar frequency estimate is not relabelled as a bound for this full coupled system.

## 4. Pilot and controls

The interval is the binary64 number 1e-7 in the inherited coordinate-time normalization; it is NOT assigned seconds. Three forward integrations use one, two and four equal steps to the same endpoint. A separate full-step backwards integration checks recovery of the initial state. This first backwards check reuses the forward midpoint velocity and is therefore primarily an algebraic/replay check, not an independent nonlinear root-finding challenge. The full-step calculation is repeated with40 rather than64 Decimal digits.

A separate postflight calculation makes the reverse test independent: all16,425 seed velocities are perturbed, with field perturbations of scale3e-5 and source perturbations of scale2e-4 from a recorded deterministic random generator. The reverse solve must recover the initial state under the unchanged nonlinear and recovery gates. It cannot simply start at the known forward midpoint solution.

The postflight also repeats a full forward step with finer reference/material orders(16,48). It preserves the same initial physical coordinates and velocities, computing their action-owned momenta on that finer rule. Position increments and momentum IMPULSES are compared with the base rule; comparing raw final momenta would otherwise mix a dynamics difference with a pre-existing quadrature difference in initial momenta. The radial gravity rule remains degree22/label28 in this control; it is not a new radial or spatial-convergence study.

Temporal endpoint comparisons are reported separately for field/source positions and field/source momenta. The two-versus-four-step difference must be below0.2% of the finest measured motion/impulse, plus a stated small numerical floor tied to the initial state scale. The observed error ratios are reported even when roundoff prevents a clean second-order ratio. Backward and arithmetic comparisons likewise have explicit per-block gates; these are controls for this tiny pilot, not long-time stability or physical accuracy bounds.

The endpoint coordinate update and momentum update are independently reconstructed from saved midpoint velocities and forces. A native-subspace diagnostic compares the common field with its native restriction and exact re-embedding WITHOUT altering the trajectory. This checks that the new common coordinates are actually allowed to leave the old embedded subspace. No total-energy conservation claim is made without solving endpoint velocities and evaluating the complete reduced Hamiltonian.

## 5. Results and next decision

### Main coupled pilot

The main run completes59 implementation/control checks and27 accepted midpoint steps across the three branches in1,392.32 seconds (23.2 minutes). Its75 nonlinear residual evaluations plus3 initial evaluations each solve live candidate gravity. Every forward/arithmetic step converges in3 residual evaluations; the known-midpoint-seeded reverse uses1, as expected from its construction. No modes are removed and no rejected step is secretly replaced by a smaller one.

The new common-state adapter reproduces the previously sealed initial force channels within3.316e-15 relative. Independently organized initial momentum quadratures differ by7.476e-11 in the preconditioner-scaled norm. Main-run final relative nonlinear residuals are at most5.297e-14; maximum preconditioned corrections are at most6.493e-15; radial integral residuals are at most5.638e-17. Sampled F stays above0.7302529 and the source speed ratio stays below0.039116. These numbers measure numerical consistency at the chosen initial annulus, not proximity to an observational or black-hole result.

| Branch | Field position error ratio, halving again | Field momentum error ratio, halving again | Finest field-position difference | Finest field-momentum difference |
|---|---:|---:|---:|---:|
| Reference | 0.24935 | 0.25007 | 7.102e-22 | 7.215e-20 |
| MTS primary | 0.24910 | 0.25020 | 1.257e-21 | 1.217e-19 |
| MTS alternative | 0.24910 | 0.25024 | 1.405e-21 | 1.367e-19 |

These approximately quarter-sized field errors are consistent with second-order time stepping on this pilot. The source-position difference is already around2.1e-22 and does NOT show that reduction ratio; it is treated as a numerical-floor-limited control, not advertised as a second-order demonstration. The largest finest-step difference relative to its measured motion/impulse is6.145e-10. For scale, the largest field-coordinate motion is about2.773e-11, source motion about3.0e-9, field impulse about2.224e-10 and source impulse about2.291e-11 in inherited units.

The40/64-digit endpoint comparison changes no component by more than3.626e-26. This is arithmetic reproducibility of the stored problem, not26-digit physical accuracy. The almost exact reverse recovery when seeded at the forward midpoint is algebraic replay; it is explicitly not used as the independent reverse-solver evidence.

### Independent postflight and interpretation

The postflight completes35 implementation/control checks and6 accepted steps in538.86 seconds (9.0 minutes). Each finer-quadrature forward solve takes3 residual evaluations. Each independent perturbed-seed reverse takes5: its starting relative residual is about0.0368 rather than an already solved midpoint, and all16,425 initial velocity components are perturbed. All12 reverse state-block comparisons pass. The largest recovered position/momentum component error is2.702e-21 in inherited units. That is an algorithmic recovery test at this tiny interval, not a physical precision claim.

All12 finer-quadrature increment comparisons pass. The largest change is7.254e-17 in a field impulse, or3.263e-7 of the measured impulse. Field position increments change by roughly7.523e-10 relative; source comparisons are near numerical noise. The quadrature sensitivity is therefore larger than the measured time-step sensitivity on this pilot. Claiming physical accuracy from time-step refinement alone would be unjustified.

Across the main and postflight,33 midpoint steps are accepted. All solves retain the full16,425 unknowns, solve the metric at each trial and use the unchanged strict residual gates. Nothing is inferred about a long-time attractor, global canonical invertibility, a black-hole crossing or stable evolution through F=0. The chart here is comfortably untrapped, with F around0.73 at its minimum.

The integrity output records the exact reconstruction of all discrete updates and the read-only native-subspace departure diagnostic. These are reproducibility and representation checks, not additional physical observations. The three branches receiving equal controls is important: this is not a test imposed only on MTS while leaving the reference unchecked.

**What is now genuinely new:** the implemented candidate can move its field and source together while consistently solving its own radial gravity, rather than only passing static inversions or a frozen scalar-block pilot. The tiny coupled run has reproducible step, precision, integration-rule and independent reversal controls.

**Next:** independently invert the endpoint momenta, evaluate the COMPLETE reduced Hamiltonian with the same gravity/boundary convention, and then increase the coupled interval in saved, bounded work blocks with equal branch/step controls. Longer evolution must monitor the quadrature sensitivity already measured here; the smaller time-step error is not the only numerical error. After those controls, revisit the sourced physical-force comparison and spatial refinement. No claim is made that the old12.5718% impulse,13.5770% fine/continuum or32.5535% coarse/fine discrepancies have disappeared.

## 6. Sources and scope

- `scripts/annular_candidate_midpoint_20260921.py`
- `scripts/derive_annular_candidate_midpoint_20260921.py`
- `scripts/check_annular_candidate_midpoint_quadrature_20260921.py`
- `scripts/seal_annular_candidate_midpoint_20260921.py`
- `scripts/annular_candidate_full_inverse_20260920.py`
- `scripts/annular_candidate_coordinate_covectors_20260921.py`
- `scripts/annular_candidate_radial_constraint_20260920.py`
- `DERIVATION-20260921-action-owned-coordinate-covectors.md`
- `source-intake/navier-stokes/20260914/annular-candidate-coordinate-covectors-final-integrity.json`
- `source-intake/navier-stokes/20260914/annular-candidate-coupled-midpoint-attempt01/status.json`
- `source-intake/navier-stokes/20260914/annular-candidate-midpoint-quadrature-attempt01/status.json`

No public-repository action, subagents or protected-workbench changes. One single-core BelowNormal numerical worker; no unrelated process is stopped. Old published and sealed calculations remain unchanged, including their failures. Numerical success here is not an empirical test, a spatial-convergence result, a general-shift/current derivation, a physical-force comparison or a full-GR theorem.
