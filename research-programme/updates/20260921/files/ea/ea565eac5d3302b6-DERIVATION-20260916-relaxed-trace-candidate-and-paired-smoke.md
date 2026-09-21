# Separate relaxed-trace candidate: implementation and paired smoke

Private continuation of `DERIVATION-20260916-boundary-memory-and-trace-domain-completion.md`.
Started2026-09-16T10:26:04Z; four-hour check-in deadline14:26:04Z.

## 1. What is implemented, and what is not

The earlier conditional bulk-L2 relaxation is now implemented as a separately named variational candidate. No previous action, trajectory, force gate, or result has been replaced. It is not asserted that the original moving-source dynamics converges to this candidate, or that the full parent theory selects it.

For field coordinates u, original sampled matrix G, reference hinge h, positive weights W(b), and D=h^T W h, set

    eta_star = h^T W G u/D,
    rho = G u-h eta_star,
    V_rel = V_bulk + rho^T W rho/2.

The full kinetic action, material action and source-field momentum are unchanged. In particular the source force still contains the time derivative of its full field momentum, rather than just boundary pressure. Every original sampling row contributes to the projected Gram energy. No fitted coefficient, damping, energy projection, or force correction is added.

The auxiliary eta_star is NOT imposed on the actual gradient jump j(u). Both are recorded separately. The original physical-jump Gram helper is explicitly rejected for this candidate; the source-position-dependent auxiliary data must be used instead.

## 2. Variational implementation

Envelope stationarity h^T W rho=0 gives

    partial_u V_rel,Gram = G^T W rho,
    partial_b V_rel,Gram = rho^T W_b rho/2.

The corresponding potential covectors enter with minus signs. The coefficient-weight dual uses rho squared, not the old lifted-gradient residual. The bulk coefficient dual remains unchanged. Both are retained for future coupling work, but live geometry is still rejected by this implementation's interface.

The independent shape-force diagnostic retains the physical source pressure, interior mesh pressure, and bulk Euler projection; only its direct Gram term is replaced by the derivative of the candidate's actual Gram energy. It is checked against the canonical force and the source's mechanical momentum derivative. The old diagnostic term is recorded as unused rather than silently interpreted as the new force.

The step-size guard uses the candidate stiffness

    K_rel = K_bulk+G^T W G-g g^T/D,  g=G^T W h,

not the old physical-trace stiffness. The conservative frozen-spectrum step cap is a numerical setting, not a nonlinear stability theorem.

Qualification covers base counts33,65,129, both reference/candidate branches, and prescribed background masses0 and0.7. All120 checks pass: action, field/source/velocity derivatives, coefficient duals, positive coupled inertia, Euler-Lagrange equations, energy identity, unchanged reference, zero-field motion, and the flat shape-force identity. Curved-background derivative checks are not live-gravity validation.

The coefficient probe initially used complex coefficients with real state dtypes, generating a warning about discarded imaginary parts in the returned kinetic bands. That probe used the action, not those bands. A separate explicit-complex control verifies both the action dual and the independent kinetic-matrix derivative with no complex-casting loss; the latter agrees within1.378e-16. The warning and its scope are recorded, not suppressed or hidden.

## 3. Prespecified paired smoke and bounded refinement

Both branches use the original flat spherical control, compact-quintic field amplitude0.01, source position6.03, speed0.06, material mass0.03, and final time0.4. The first matrix uses base65/129, with unrefined quadratic source-fitted meshes (130/258 scalar degrees of freedom). Each accepted0.05 interval is saved. A new paired257 run was declared after that coarse result, to check a resolution at which the earlier bulk field already passed; its original coarse failures remain part of the outcome.

All comparisons use the independently saved384/512/768 references. The unchanged limits are: field0.5%, source position5e-7, velocity2e-5, clock2e-7, and final force BOTH absolute2e-7 and relative2%. The stronger sampled force gate applies the absolute bound at all nine stored times, not at every continuous time.

| Base | Branch | Maximum field error | Final absolute force error against512 | Old unrelaxed force error | Force gate |
| --- | --- | ---: | ---: | ---: | --- |
| 65 | reference | 0.512784% | 3.40422e-6 | 3.40401e-6 | fail |
| 65 | relaxed MTS | 3.07181% | 5.35043e-4 | 5.28034e-4 | fail |
| 129 | reference | 0.143533% | 1.60684e-6 | 1.60685e-6 | fail |
| 129 | relaxed MTS | 0.770631% | 5.52600e-5 | 4.49107e-5 | fail |
| 257 | reference | 0.0365440% | 8.50152e-7 | 8.48963e-7 | fail |
| 257 | relaxed MTS | 0.194227% | 8.95964e-6 | 3.09945e-6 | fail |

The bounded refinement is complete. Both257 branches pass field and combined source/velocity/clock gates, but both fail the final and nine-sample force limits against all three oracle resolutions. The relaxed257 relative final-force error is0.522760%, below2%, while its absolute error is44.8 times the2e-7 limit. Both force requirements must hold. Its final absolute discrepancy is about2.89 times the old MTS257 discrepancy; the static relaxation is not adopted as a force cure.

Coarse MTS65 also fails the source-position and velocity gates: errors1.57887e-6 and4.90458e-5. Its clock error8.08730e-8 passes. MTS129 and both coarse references pass the combined source/velocity/clock gate. None of these four cases passes all nine force samples. All their final and sampled force classifications agree across the three oracle resolutions.

The candidate therefore does not qualify merely because its energy or Euler-Lagrange residual is small. On the coarse grids its final-force error is worse than the corresponding original MTS action, while the reference itself remains imperfect. Neither fact is used to change the acceptance limits.

## 4. Numerical controls

Both newly integrated reference trajectories reproduce the saved unrelaxed reference states within4.024e-10 at65 and3.269e-11 at129. This tests that the reference branch has not been changed while altering MTS.

The100-times tighter first-eighth temporal controls on129, with half the spectral step cap, differ from baseline by at most3.025e-14 in state and2.235e-14 in force. They are not full-duration temporal convergence proofs. Order16/24 field quadrature differs by at most1.125e-9 in the coarse smoke, below its unchanged2e-8 check. These controls make a short-time integration or quadrature artefact unlikely to explain the reported coarse discrepancy; they do not certify the whole time-continuum limit.

## 5. Derive the source-force change, not just label it

The unrelaxed and relaxed actions have the same velocity Hessian and momenta at the same state. Let delta=j(u)-eta_star and define the removed positive potential term

    DeltaV = D delta^2/2,
    L_rel = L_old+DeltaV.

At fixed field coordinates and source position,

    grad_u DeltaV = D delta [j_row-G^T W h/D],
    partial_b DeltaV = D_b delta^2/2-D delta (eta_star)_b,
    (eta_star)_b = [h^T W_b G u-eta_star D_b]/D.

With field mass M, kinetic cross-column c, full source inertia H_bb and material inertia mu_s, exact block elimination gives the same-state mechanical-force difference

    DeltaF_same = mu_s/(H_bb-c^T M^-1 c)
        * [partial_b DeltaV-c^T M^-1 grad_u DeltaV].

Small potential energy does not imply small force: spatial derivatives and the coupled inverse kinetic operator appear explicitly. This is a prediction of the two finite actions' difference, not a correction applied to either run.

The observed difference between independently evolved trajectories separates exactly into

    F_rel(q_rel)-F_old(q_old)
       = [F_rel(q_old)-F_old(q_old)]
         + [F_rel(q_rel)-F_rel(q_old)].

Here q abbreviates the complete field/source positions and rates. The first bracket is checked by the derived law above; the second measures changed-trajectory feedback. Neither component may be subtracted to force a pass.

All21 response checks pass over the three base grids and nine saved times. At257 and final time, the removed potential term is only1.06682e-12, but the derived same-state force change is-1.22416e-5. The changed-trajectory feedback is+1.81017e-5, giving a net+5.86019e-6 change. Thus the trajectory response even reverses the sign of the direct change. Agreement of the action-derived response law with direct acceleration differences is within6.05e-18 over the checked states. This is a verified mechanism in this finite comparison, not a proof of the full continuum error source.

### A useful sufficient instantaneous bound

Let ell=j_row-G^T W h/D, alpha=mu_s/(H_bb-c^T M^-1 c), and e=DeltaV. The exact law implies

    |DeltaF_same| <= A e + B sqrt(e),
    A = alpha |D_b|/D,
    B = alpha sqrt(2D) |(eta_star)_b+c^T M^-1 ell|.

For a chosen same-state force budget tau, a sufficient energy-gap condition is

    e <= [2 tau/(B+sqrt(B^2+4 A tau))]^2,

when A or B is nonzero. If both vanish, this same-state force difference is zero. This follows directly from the triangle inequality and the positive quadratic root; it is not a fitted condition. It is also NOT a sufficient evolved-force criterion by itself: the trajectory-feedback term still needs control. It makes precise why merely observing a small positive potential gap was inadequate.

## 6. Decision and next derivation

Implementation is qualified, but the tested relaxed candidate is not an accuracy improvement. Keep it as an explicit comparison, not as the new parent action or as the established GR limit. The old branch has not been discarded, and the imperfect reference is reported alongside both MTS versions.

The next derivation should retain the finite trace response and its initial-data term, then bound its force effect using the instantaneous law above AND the trajectory response through the previously derived retarded propagator. Establish a prepared-data/joint-refinement criterion before replacing the dynamics by a static auxiliary minimum. No new fitted damping or forced trace equality is justified by these results. The force data improve with base resolution, but three grids and a fixed final time are not a convergence theorem.

Successful current checks:120 qualification,27 coarse smoke,16 bounded refinement,19 precision/type controls,21 force-response checks; total203. These are implementation/algebra checks, not203 physics successes. No failed attempt was erased and no accuracy flag was promoted. The tighter temporal controls cover129 only and only its first eighth; they were not repeated across the entire fine257 trajectory.

## Scope and evidence

This is not a full GR limit or a replacement parent action. The earlier fixed-stencil static-relaxation theorem remains distinct from dynamic convergence, prepared initial data and simultaneous base-grid refinement. No GitHub action, no subagents, and no edits to formalization-workbench. All old executed sources and evidence remain immutable.

- Candidate: `scripts/annular_relaxed_trace_action_20260916.py`.
- Qualification: `scripts/verify_annular_relaxed_branch_20260916.py`.
- Paired smoke: `scripts/run_annular_relaxed_branch_smoke_20260916.py`.
- Bounded refinement: `scripts/run_annular_relaxed_branch_refinement257_20260916.py`.
- Precision/type controls: `scripts/verify_annular_relaxed_precision_20260916.py`.
- Derived force-change law: `scripts/derive_annular_relaxed_force_change_20260916.py`.
- Previous seal: `source-intake/navier-stokes/20260914/annular-boundary-response-final-integrity.json`.
- Coarse results: `source-intake/navier-stokes/20260914/annular-relaxed-branch-smoke-attempt01/status.json`.
- Fine results: `source-intake/navier-stokes/20260914/annular-relaxed-branch-refinement257-attempt01/status.json`.
- Force-response results: `source-intake/navier-stokes/20260914/annular-relaxed-force-change-attempt01/status.json`.
- Current integrity ledger, complete only when its state says so: `source-intake/navier-stokes/20260914/annular-relaxed-branch-final-integrity.json`.
