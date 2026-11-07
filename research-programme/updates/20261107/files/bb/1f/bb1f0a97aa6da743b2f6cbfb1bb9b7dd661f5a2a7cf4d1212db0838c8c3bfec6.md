# Exact metric-time primitive and cancellation-aware response

2026-11-07, turn starts13:18UTC. Previous goal turn progress: closed terminal
feedback identity,8 adjoint integrations,416 checks, source attribution.
Parent seal2843c90481aa70251f9f8caeedbba2e5cc9d8088619952afee1be56a55548d9a.

## Derive before evaluating

The previous source formulas have an exact primitive; no fitted Fourier
envelope or slow-adjoint assumption is needed. Define chi=1 for Poisson-spatial,
chi=0 for dust-force, Lchi=1+3chi Wq/(2k^2), P=-Dg/(2k^2), J=Phi_g-chi P.
Then T=3H J_N/(k Lchi), and J=-M for chi=1 by the retained GR constraint.
M=3H Qg/(2k^3). This uses the actual finite quadrature Wq.

With d=3H b_z/(k Lchi), C=lambda^T d, the metric-time integral is
[C J]_initial^final - integral C_N J dN, where
C_N=lambda^T(d_N-An d). Derive d_N including heavy carrier phase, velocity,
scale and Lchi derivatives. Keep both endpoint terms. No assumption that
lambda, d or C varies slowly; no fitted cancellation.

Evaluate both branches, both MTS/cold models, both saved step caps. Reuse
existing background/GR states, full coupled adjoint core traces and operator
coefficients. No new ODE solves, no new bank/grid/physical parameter/tolerance.
Check that An d has no hierarchy-tail component before using core traces alone.

## Fixed validation and reporting

Original-node quintic Wq derivative with independent direct finite-difference,
coarsening and non-midpoint d_N checks. Compare the contracted derivative
against the saved adjoint-curve derivative independently. Same algebra1e-10,
numerical2e-5 gates. Check primitive identities and endpoint reconstruction.

Use the qualified Bernstein absolute-integral algorithm; repeat integration
on every-second node and reuse both cap histories. Numerical enclosure of
an interpolant is not a rigorous native-continuum certificate.

Report both old and transformed bounds. A predeclared minimum of two valid
bounds is allowed, but never hides a worsening transformed bound or a failed
precision gate. Predict first, target readback only afterward. These reference
outputs were previously known; no statistical held-out claim.

One numerical worker/thread, below-normal CPU4. No subagents, compiler,
GitHub, galaxy, extra directions or unrelated process actions. Actual STOP
holds bind. Launch cutoff17:12, worker17:14; check-in<=17:18UTC.

