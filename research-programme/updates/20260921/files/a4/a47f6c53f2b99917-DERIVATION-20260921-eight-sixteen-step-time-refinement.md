# Eight- and sixteen-step coupled time refinement

## Target and experiment

The preceding experiment isolated four failed field time-refinement gates at the same fixed horizon T=1e-5, including the reference branch. This stage computes the missing eight- and sixteen-step trajectories rather than changing the model or its tolerances.

All three branches use the same physical initial data and all 16,425 state components (15 material nodes with 1,094 field components and one source coordinate each). The horizon is in inherited coordinate units, not assigned SI seconds. Each nonlinear trial re-solves the radial gravity problem. The saved full mass matrix is only a preconditioner; no physical modes are removed. The trial-history accelerator changes the nonlinear solution method, not the equations.

We hash-reuse the completed two- and four-step states and endpoint inverses. New work is 72 accepted forward steps and six full endpoint inverses if the experiment completes. Counting reused states gives 90 step records and 12 endpoint energies. Fresh trial counts and elapsed time refer to this new execution, not to the historical calculations being reused.

## What refinement measures

Write z_n for an endpoint calculated with n equal steps over T. For a smooth, consistently solved second-order method in its asymptotic regime,

    z_n = z_exact + C (T/n)^2 + O((T/n)^4).
    d_coarse = z_n - z_2n; d_fine = z_2n - z_4n.
    d_coarse = 4 d_fine + O((T/n)^4).

Hence the norm ratio approaches 1/4 and log2(||d_coarse||/||d_fine||) approaches 2. The remaining finest-grid error estimate ||d_fine||/3 is conditional on that expansion; it is not an independently proved error bound. We test both triplets (2,4,8) and (4,8,16), separately for field/source and position/momentum. A vector Richardson defect records how nearly the error vectors obey d_coarse=4*d_fine, rather than inferring alignment from their maximum norms alone.

The unchanged gates use signal = ||z_finest-z_initial||_infinity, scale = max(||z_initial||_infinity,1e-30), and floor=(2e-15 for position or 5e-12 for momentum)*scale:

    fine_difference < 0.002*signal + floor;
    fine_difference <= 0.4*coarse_difference + 2*floor.

Differences are tagged resolved only if both exceed four times the diagnostic floor. Passing these gates is a measured numerical acceptance result, not a theorem of continuum convergence. Floors retain the prior definition; they are not certified bounds on all roundoff or accumulated nonlinear-solver error.

The previous linear oscillator derivation supplies the motivation: implicit midpoint can preserve quadratic energy exactly while accumulating phase error, with omega_numerical=2*atan(omega*h/2)/h. Energy agreement therefore cannot replace the independent state comparison. No assumption that this mechanism completely explains our nonlinear error is needed to perform the test.

## Complete endpoint energy and independent checks

Each endpoint first inverts the full momentum map at fixed saved position and momentum. Midpoint rates are only seeds, never substituted as endpoint velocities. The numerical Hamiltonian is reconstructed from target momentum pairing, matter action, gravitational bulk and outer boundary contribution. The on-constraint boundary identity is checked, not substituted to manufacture a constant energy.

The independent seal reconstructs every discrete update and solver residual from saved arrays, recomputes each endpoint energy and both time-refinement triplets, verifies inherited hashes, and exports source-linked CSV tables. It preserves all earlier failures. Earlier single-step reversal controls remain evidence at their original resolution; this stage does not silently relabel them as new sixteen-step controls.

After all branches complete their time grids, a separate control recomputes sixteen steps at reference/material integration orders16/48, versus10/32. It preserves the physical initial coordinates/rates and uses the separately derived momentum for each integration rule. We compare increments, not unequal initial momenta. This adds48 new accepted steps and three new endpoint inverses; its48 coarse step records and three coarse energies are reused. Across the two runs there are138 distinct saved steps (120 new) and15 distinct endpoint energies (nine new), despite186 step and18 energy records being independently checked. Diagnostic comparisons of quadrature changes with the last time-grid difference are scale comparisons, not certified total-error bounds.

## Results

### Time refinement complete

The main run completes in5587.14seconds with184 implementation checks,318 fresh trial evaluations,72 new accepted steps and six new endpoint inverses. All12 finest4/8/16 gates pass, including all six resolved field comparisons. The table gives the finer-to-coarser maximum-error ratio:

| Branch | Position 2/4/8 | Momentum 2/4/8 | Position 4/8/16 | Momentum 4/8/16 |
| --- | ---: | ---: | ---: | ---: |
| Reference |0.290348|0.393288|0.260844|0.269139|
| MTS primary |0.281094|0.521403 (fail)|0.247432|0.299438|
| MTS alternative |0.280467|0.535521 (fail)|0.225860|0.339953|

Two coarser MTS momentum checks still fail the unchanged gate. The overall runner flag `trajectories_qualified=false` therefore stays false; the separate finest-grid acceptance must not overwrite those failures. The finest field differences are at most1.982e-7 of the corresponding measured block increment. Source acceptance bounds pass but their formal order measurements remain diagnostic-floor limited.

All12 recorded endpoint energies pass the original smoke gate; their maximum relative drift is4.054e-16. The energy order diagnostic remains below resolution. The result is evidence that the chosen smaller time steps resolve the earlier field-refinement failure on this tested interval, without modifying the action, field content or tolerances. The remaining departures from an exact quartering ratio and the vector Richardson diagnostics must be kept visible.

### Matched integration control and final integrity

The matched16-step integration run completes in3697.38seconds with241 implementation checks,176 fresh trial evaluations,48 new accepted steps and three new endpoint inverses. All12 increment comparisons pass. The maximum integration-induced change is3.258e-7 of the measured block increment. All six recorded endpoint energies pass their smoke gate, with maximum relative drift3.171e-16 against their matching initial integration rule.

| Branch | Integration change / last time difference: field position | Field momentum |
| --- | ---: | ---: |
| Reference |0.5367|3.1203|
| MTS primary |0.7298|1.9049|
| MTS alternative |0.8021|1.6434|

Thus field-momentum integration sensitivity now exceeds the eight-to-sixteen-step change in every branch. Finer time stepping alone would not remove that contribution. Position integration sensitivity is smaller but comparable. This is an observed error-scale budget, not an outward-rounded total-error estimate. It supports using the finer integration rule for the next physical calculation, keeping both time and integration sensitivities in its numerical budget.

Combined fresh work is120 accepted steps, nine endpoint inverses and494 trial evaluations; numerical execution takes about2hours35minutes on one restrained worker. The two execution logs have184 and241 implementation checks. The independent checker reconstructs186 step records and18 energy records, accounting explicitly for138 distinct saved steps and15 distinct saved energy states. Its final source manifest and CSV diagnostics are the authoritative record of completed validation, rather than these counts standing in for physical confirmations. Earlier coarse failed comparisons stay recorded; no threshold or original source is overwritten.

Final manifest: `source-intake/navier-stokes/20260914/annular-candidate-finer-time-final-integrity.json`. Resolved-order/vector diagnostics: `source-intake/navier-stokes/20260914/annular-candidate-finer-time-refinement-diagnostics.csv`. Integration/time budget: `source-intake/navier-stokes/20260914/annular-candidate-finer-time-quadrature-time-budget.csv`.

## Next physical calculation: from canonical evolution to source acceleration

The numerical work now enables a more physical comparison, rather than another automatic doubling of time resolution. For the autonomous reduced momentum map p=P(q,v), with the gravity solution included in P, differentiation along a trajectory gives

    p_dot = P_q v + P_v a = f,
    P_v a = f - P_q v.

Here f is the complete action-owned canonical force, not the metric factor F. This identity is a chain-rule derivation; evaluating and solving its full live-geometry Jacobian is the next calculation. Dividing a source momentum covector by a bare mass would drop field/source mixing and gravitational inertia response. All components must be retained.

For a fixed material label, let b be the physical source radius, V=db/dt, and s=d(tau)/dt=sqrt(N(b)^2-V^2/F(b)). The corresponding proper-time radial acceleration is

    d^2 b/d(tau)^2 = a_b/s^2 - V*s_dot/s^3,
    s_dot = [N*N_dot - V*a_b/F + V^2*F_dot/(2*F^2)]/s.

N_dot and F_dot are total derivatives along the moving source, including the evolving metric and its radial sampling. This is a radial-coordinate acceleration parametrized by proper time, not the invariant magnitude of four-acceleration. The next substantive target is to evaluate it on the qualified numerical branch, verify the same conversion in the reference/test-source limits, and then compare spatial resolutions and the GR/Newton limit using the same observable and normalization. The older frozen-force discrepancy percentages must not be transplanted onto a differently defined acceleration.

Sources for the already derived canonical map and covectors are `DERIVATION-20260920-candidate-canonical-momenta-and-live-response.md` and `DERIVATION-20260921-action-owned-coordinate-covectors.md`. Their conditional stationary-envelope scope remains in force. Numerical time and integration controls support this next calculation; they do not replace its missing Jacobian/clock evaluation.

## Sources and execution

- Previous immutable report: `DERIVATION-20260921-longer-coupled-evolution.md`.
- Previous authoritative seal: `source-intake/navier-stokes/20260914/annular-candidate-longer-evolution-v2-final-integrity.json`.
- Reused completed run: `source-intake/navier-stokes/20260914/annular-candidate-longer-1e-5-attempt04/status.json`.
- New runner: `scripts/run_annular_candidate_finer_time_20260921.py`.
- New run: `source-intake/navier-stokes/20260914/annular-candidate-finer-time-attempt01/status.json`.
- Matched integration runner: `scripts/run_annular_candidate_fine16_quadrature_20260921.py`.
- Matched integration run: `source-intake/navier-stokes/20260914/annular-candidate-fine16-quadrature-attempt01/status.json`.
- Independent checker: `scripts/seal_annular_candidate_finer_time_20260921.py`.

Private, local-only work. One single-core BelowNormal worker at a time with BLAS threads limited to one; no subagents or GitHub action. Numerical wall budgets were10,000seconds for the main run and6,600seconds for the subsequent control, started only after checking the remaining four-hour allowance. Both finish before their budgets. Protected workbench verification uses modification times since2026-09-21T11:06:27Z, not a pre-turn whole-tree hash baseline.
