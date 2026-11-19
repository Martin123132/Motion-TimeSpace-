# Metric forcing from the retained action: frozen protocol

2026-11-10. This continues the sealed second-adiabatic state map, rather
than replacing the retained action or inventing a galaxy coupling.

1. Derive the Phi/Psi source and canonical momentum from the positive
   quadratic scalar action already owned by Stage49. Keep the potentials
   distinct. Prove the exact forced matter conservation identities, including
   the lapse contribution to stress. State the on-shell background assumption.
2. Extend the previous template-residual bound to the triangular forced
   background/perturbation system. Separate truncation, supplied-metric
   uncertainty and floating-point/integration error. Do not apply the frozen
   constant-conformal-H certificate to a general cosmological history.
3. Reuse all 399 saved modes at a=.01, in each of the heavy and cold models.
   Preserve each model's own H, Phi, Psi and initial density/current. The
   probe has constant H, constant supplied Phi/Psi, a=a0 exp(s), and
   0<=s<=.001. All original bank, mass, grids and tolerances are unchanged.
4. For the heavy field keep both carrier quadratures and the full forcing
   integral, including sum-frequency terms. Predeclare composite 16-point
   Gauss-Legendre with 128, 256, 512 panels, processed eight panels at a time.
   Compare fixed canonical initial states across these refinements.
5. Independently integrate the original physical field equation for modes
   nearest k=.03,.1,1,5 inverse Mpc, both carrier quadratures. DOP853 controls
   use rtol 2e-11 and 2e-12, atol 2e-13 and 2e-14 on normalized coordinates.
   These are numerical controls, not an analytic error certificate. Reproduce
   the saved cold probe with its own exact constant-H metric-held solution.
6. Prove the flat constant-potential solution and k->0 phase response. Check
   cancellation of a constant Phi at fixed physical initial field and field
   derivative; do not hold canonical momentum fixed while changing Phi.
7. Existing gates: algebra 1e-10, numerical comparison 2e-5. Normalizers
   include fixed initial and forcing scales, never a near-zero final value.
   Report failures rather than changing a gate or dropping modes.

The saved averaged late state does not supply a unique microscopic fast
phase. Two explicit quadratures supply controlled preparations; an ensemble
average over their initial phase is not silently called time averaging.
This tests the existing action-to-state interface, not a new galaxy fit.

One numerical worker, one numerical thread, CPU4, below-normal; each bounded
to 900 seconds with owner-hold checks. No other agent, browser, server,
GitHub action, observation download or existing checkpoint edit. New outputs
are exclusive-create. Source and artifact hashes plus process receipts are
required before closeout. Any failed attempt remains recorded.
