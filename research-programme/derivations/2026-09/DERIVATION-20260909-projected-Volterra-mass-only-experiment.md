# Mass-only projected-Volterra experiment: derivation and qualification

Private continuation, 2026-09-09. Scope: a numerical source-completion repair
on the existing ordinary coupled annular correction, not a new physical
coupling, a local-GR proof, or a black-hole/horizon extension.

## Why this is a constructive next step

The preceding centered-mode diagnosis found almost perfectly alternating mass
traces. The interior centered first derivative annihilates the pure Nyquist
mode, while its boundary rows do not. Such traces can have a small discrete
constraint and a large unavoidable H4 reconstruction cost. That diagnosis did
not prove which term produced the mode. This experiment isolates the mass
source completion instead of increasing the mesh again or deleting j_h.

Preserve the old completed experiments and the failed N1024 field gate.
Use the SAME degree64 C3 initial-data payloads, parent background, independent
nonzero defects, cache, characteristic scalar and lapse boundaries, RK4/CFL,
no artificial dissipation, and the same scalar/lapse projection law. Change
only the mass completion below. Source values on different trajectories need
not be identical; equality is asserted at the SAME state.

## Actual replacement

Write g=(g_chi,g_q,g_mu,g_delta) in coordinate variables. Let S^P be the
original boundary-fixed scalar projection and centered mass completion.
Keep S_chi=S^P_chi=0, S_q=S^P_q and S_delta=S^P_delta. Set

    a = g_mu
    f = g_q S^P_q + g_delta S^P_delta
    u_R = a u + f,       u(R_outer)=0
    S_mu = u.

For cell length h define a_bar=(a_i+a_(i+1))/2, z=-h a_bar and
phi0(z)=integral_0^1 exp(z s) ds,
phi1(z)=integral_0^1 s exp(z s) ds. The declared piecewise-constant-a,
piecewise-linear-f boundary-value problem has the backward recurrence

    u_i = exp(z_i) u_(i+1)
          - h (phi0(z_i)-phi1(z_i)) f_i - h phi1(z_i) f_(i+1).

This is one-way integration, not inversion of the centered derivative. The
cell weights are positive for real z. This removes the centered solve from
the mass-completion channel, NOT from the scalar projection or bulk operator.

In current variables (chi,w,h_current,mu,delta), the source change is exactly

    Delta S = (0,0,h_mu Delta S_mu,Delta S_mu,0).

Thus the h-current source must change with mass; freezing it would change the
coordinate scalar equation. The direct source helper checks scalar/lapse
equality bit-for-bit against the same-state original projected completion.

## What can be proved about the isolated mass operator

On a finite annulus with bounded real a, the terminal-value ODE is unique:

    u(R)=-integral_R^Rout exp(-integral_R^s a(x) dx) f(s) ds.

Consequently ||u||infinity <= exp(A L) L ||f||infinity for zero outer value.
For two coefficient/forcing pairs (a,f) and (b,k), apply the same integrating
factor to (u-v)'=a(u-v)+(a-b)v+(f-k). With equal zero outer values,

    ||u-v||infinity <= exp(A L)L[
        ||a-b||infinity ||v||infinity + ||f-k||infinity].

This is a perturbation bound for the isolated completion, not a bound for the
whole coupled evolution. The discrete homogeneous recurrence is
u_i=exp(z_i)u_(i+1), so its zero outer condition also forces u=0, and a real
pure alternating mode cannot be a homogeneous cell solution because exp(z)>0.
For a=0 its forcing contribution is the trapezoidal cell integral; purely
alternating endpoint forcing has zero cell average. The scalar projection and
the bulk centered derivatives are still present, so these facts do not prove
that every alternating mode in the coupled system has been removed.

For differentiable coefficient and forcing functions the exact time equations
are (u_t)'=a u_t+a_t u+f_t and
(u_tt)'=a u_tt+2a_t u_t+a_tt u+f_tt, with zero outer time data.
These explain the differentiated cell recurrence. They do not supply missing
spatial regularity of mesh-dependent forcing or a horizon continuation.

## Conservation is bounded, not silently restored

Retain and report every row of

    rho_h = D_h S_mu - g_mu S_mu - f.

Use the already derived Volterra source bound with THIS projected f, including
endpoint rows. If A=max|a|, F=max|f| and L is the annulus length,

    U=exp(A L)(|u_outer|+L F),       V=A U+F,
    B_i=h[(A V+Lip(a) U+Lip(f)) m2_i + Lip(a) U m1_i],

where m1_i=sum_j |D_unit(i,j)| |j-i|/2 and
m2_i=sum_j |D_unit(i,j)| |j-i|^2/2. The analytic statement belongs to the
specified piecewise-source problem. Floating implementation tests are not
interval certificates. The previous owner also qualifies its small-moment
polynomial approximation. No exact source Noether identity is asserted.

Crucially, an explicit finite-grid bound is not a proof that B_i tends to zero:
boundary penalties and projected forcing can have mesh-dependent Lipschitz
constants. Field, boundary, curvature, and strong derivative controls remain
separate. Neither rho_h nor the evolved nonzero constraint j_h may be set to
zero when reconstructing curvature.

## Differentiate the operator actually used

Use normalized time coefficients through degree2. Differentiate every
product, the projected S_q, a, f, and the cell recurrence by Taylor convolution:

    u_i^[n] = sum_(k=0)^n [
        E_i^[k] u_(i+1)^[n-k]
        - wL_i^[k] f_i^[n-k] - wR_i^[k] f_(i+1)^[n-k] ].

Here E=exp(z); E^[0]=exp(z0), E^[1]=exp(z0)z1,
E^[2]=exp(z0)(z2+z1^2/2). The small-z implementation uses the SAME thirteen
terms sum_(k=0)^12 z^k/(k!(k+1)) and sum_(k=0)^12 z^k/(k!(k+2)) as the
scalar integrator, differentiated as polynomials. The time engine rejects
|z0|>=0.09; it does not silently differentiate the wrong large-z branch.
The unnormalized third time derivative follows from the actual RHS recurrence.

The preflight uses existing saved states as probes, not new solutions. It
compares with a separate scalar-arithmetic RHS and finite-time differences at
two step sizes. No projected-source time derivative is reused as the derivative
of the hybrid mass operator.

## Provenance and initial qualification

All paths here are relative to this post-checkpoint-work folder.

- Previous result: DERIVATION-20260909-normal-curvature-reconstruction-and-centered-mode-obstruction.md.
- Bound derivation: source-intake/navier-stokes/20260909/annular-volterra-source-completion-derived/status.json (33/33).
- Frozen C3 inputs: source-intake/navier-stokes/20260909/annular-analytic-third-corner-initial-data/status.json.
- Original comparison: source-intake/navier-stokes/20260909/annular-coupled-current-analytic-third-corner/status.json (129/129).
- Same-state preflight: source-intake/navier-stokes/20260909/annular-projected-volterra-time-jets-preflight/status.json (174/174, 08:38:41 UTC).
- Source implementation: scripts/annular_projected_volterra_source_20260909.py.
- Time derivative implementation: scripts/annular_projected_volterra_time_jets_20260909.py.
- Qualification/replay: scripts/derive_annular_projected_volterra_time_jets_20260909.py.
- Evolution: scripts/run_annular_projected_volterra_correction_20260909.py.
- Curvature reconstruction: scripts/derive_annular_projected_volterra_normal_reconstruction_20260909.py.

Input and execution hashes are recorded by each runner. Execution was
single-core BelowNormal, with numerical thread limits; no subagents or
unrelated process shutdowns. The completed outcomes follow.

## Completed experiment: do not adopt the hybrid as a repair

The new evolution completed FAILED147/149 at08:46:46 UTC. It preserves all
scalar/lapse source-law checks, source residual bounds, sampled boundary gates,
and all four field mesh/time refinements. Both full and half time steps fail
the late nonlinear mass-constraint gate: about3.14553e-12 against a background
scale4.86928e-11, or6.46%, above the unchanged5%+1e-16 absolute-floor gate.
There is no COMPLETE marker for that failed evolution.

Actual trajectory time jets pass187/187; reconstruction software passes526/526.
These validate diagnostic calculations on a FAILED field experiment, not its
acceptance. The diagnostic replay explicitly records the failed field checks.

At N512, same-state hybrid mass-source alternating RMS falls from approximately
2.34e-14,3.93e-14,9.33e-14,6.79e-14 to
1.64e-19,3.14e-19,6.74e-19,3.30e-19: suppression about125,000--206,000 times.
The isolated completion really removes that source channel's alternating
component. But the bulk mass RHS remains about1.72e-14,3.67e-14,7.82e-14,8.00e-14
in the same diagnostic. The source was not the only generator; some original
bulk/source cancellation also disappears. Do not identify these instantaneous
RMS diagnostics with a proof of complete causal history.

| Case/time | Original nodal Z stencil difference | Hybrid nodal Z difference | Hybrid/original mass H4 trace floor |
|---|---:|---:|---:|
| canonical .1 | 1.67% | 14.76% | .6474 |
| canonical .3 | 25.53% | 20.99% | 1.6706 |
| nonlinear .1 | 30.32% | 24.44% | .8592 |
| nonlinear .3 | 41.28% | 21.27% | 3.1674 |

All four hybrid nodal Z sensitivity gates fail. Nodal K1 stencil differences
are below.223%, but this does not rescue Z, the field constraint, or a
continuum derivative estimate. At poly7 the physical H3(chi)+H4(mu)+H4(delta)
coarse/fine difference ratios are .127,.312,.285,.431, all below1: strong
mesh differences INCREASE. These are sufficient regularity targets, not a
proof that the continuum theory is singular or impossible.

The matched comparison passes244/244 after correcting a Windows separator
bug in the input-path SELECTOR. All three actual frozen C3 hashes were already
identical; no data or numerical gate changed. The initial comparison's
240/241 failure, script and outputs are retained unchanged for provenance.

## Further isolation performed, not merely proposed

Resolve the actual bulk mass equation BEFORE applying the parity diagnostic:

    bulk_mu = C_chi e_chi + C_w e_w + C_h e_h
              + C_mu e_mu + C_delta e_delta - d_mu.

The 24-state decomposition passes77/77 and retains all terms. At N512 the
dominant alternating contributions are C_w e_w and C_h e_h, roughly1e-14 to
3e-13. The parent-defect contribution is only about0.9e-17 to2.4e-17 in these
four snapshots. The response products must be formed BEFORE extracting parity;
products of separate parity amplitudes would not represent this equation.
Cancellation means component RMS values cannot be interpreted as additive
positive causal percentages. Signed alignment fractions are saved as well.

This evidence points to the scalar/current sector feeding the mass flux,
not an isolated parent-defect arithmetic problem. It does NOT yet say whether
the projected q source, the bulk scalar discretization, initial traces, or
their interaction creates the w/h oscillation.

## Next bounded target

Keep the original projected C3 run as the accepted FIELD baseline, and keep
the hybrid as a failed diagnostic alternative. Resolve the actual w/h block's
near-Nyquist response at matched states: separately evaluate the boundary-fixed
q projection, interior current derivative terms, retained constraint force,
and nonzero parent forcing. Derive the corresponding coupled constraint/energy
effect BEFORE proposing a compatible scalar/current discretization repair.
The exact-source original and bounded-source hybrid must receive identical
diagnostics. Do not tune a blend merely to slip under5%, smooth output plots,
delete a constraint, or launch N2048 as a substitute for this derivation.

This checkpoint supplies an actual negative controlled experiment and a more
specific mechanism to attack. It supplies no first-u, horizon, local-GR,
calibrated physical-coupling, or broad unification promotion.

Additional reproducible outputs under source-intake/navier-stokes/20260909/:

- annular-projected-volterra-third-corner/status.json (FAILED147/149).
- annular-projected-volterra-time-jets-trajectory/status.json (187/187).
- annular-projected-volterra-normal-reconstruction/status.json (526/526; curvature flag false).
- annular-projected-volterra-matched-comparison/status.json (retained harness failure240/241).
- annular-projected-volterra-matched-comparison-portable/status.json (244/244; field/curvature/strong-refinement flags false).
- annular-mass-bulk-parity-channels/status.json (77/77).

The trajectory diagnostic uses scripts/replay_annular_projected_volterra_time_jets_20260909.py,
the corrected comparison uses scripts/compare_annular_projected_volterra_mass_repair_portable_20260909.py,
and the further decomposition uses scripts/diagnose_annular_mass_bulk_parity_channels_20260909.py.
No GitHub or frozen-workbench edits; all changes remain in post-checkpoint-work.

Final integrity check08:54:39 UTC: seven owners checked,190 unique input hashes
and80 output hashes verified; all nine new scripts compile without bytecode
cache. Both failed owners retain their failures and lack COMPLETE markers.
All calculation jobs from this continuation have exited; other tasks and
shared helpers were not stopped. Numbers in this note are normalized annular
fixture diagnostics, not observational error bars or calibrated SI predictions.
