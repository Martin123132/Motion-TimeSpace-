# Source-complete leading radiation: corrected forward evolution

Private checkpoint, 2026-11-10. This extends the retained action and native
species calculation; it is not a replacement theory, new galaxy law or fit.
The preceding seal is
`b637369aae96427cca2f2911fe152e97db3a2cac3619b78519bf64276d0e841b`.

## Physical advance

The previous stage identified omitted scalar stress in the native late
radiation-streaming approximation (RSA). This stage derives and implements
the leading correction from that same stress, rather than subtracting the
observed error. It enters native radiation, gravity, other species and baryon
Thomson drag consistently. The original library and all prior research remain
unchanged. No new fitted coefficient, altered tolerance or new dataset enters.

For synchronous missing scalar density DS and pressure PS, conformal H and
the native opacity, the increments are

    Delta q_gamma = Delta q_r = -2 DS/(3 k H)
    Delta delta_r = (4 DS + 6 PS)/k^2
    Delta delta_gamma = Delta delta_r - 2 opacity DS/(k^2 H).

DS/PS include both the slow and heavy scalar. The pressure clock sign and
resulting implicit metric feedback are solved in `DERIVATION.md`; canonical
heavy pressure is not set to zero. Four exact identities and 40 independent
native-port controls pass. The maximum native-port discrepancy is 1.09e-15.
Direct native RHS/readout and independent complex scalar equations also pass.
Turning the new port off reproduces the saved original capture.

## Forward test, not merely an endpoint substitution

The same short z=10, Delta ln a=0.001, k=5/Mpc window is retained. Native heavy
and cold comparisons use 64/128 steps; the unrestricted four-coordinate
canonical MTS uses 128/256. Nine trajectory probes are checked on each fine
run, with two row-derivative stencils. All norms/tolerances are unchanged.

Maximum independently differentiated metric error
`E_phi = Phi' + H Psi - Q/(2k)`, normalized by its largest equation term:

| Case | Original source | Corrected source | Corrected step refinement |
|---|---:|---:|---:|
| Native heavy | 5.450841e-4 | 5.638228e-8 | 5.328325e-7 |
| Cold control | 4.571045e-8 | 4.571045e-8 | 5.417824e-7 |
| Canonical MTS D0 | 5.450840e-4 | 5.638311e-8 | 4.339963e-7 |
| Canonical MTS D01 | 5.450840e-4 | 5.638311e-8 | 4.209578e-7 |

The unchanged gate is 2e-5. Thus the heavy/canonical metric failure is removed
on these sampled trajectories, with roughly a 9,700-fold smaller maximum
normalized error. Cold remains passing. This is a consistency improvement,
not a 9,700-fold improvement against observational data.

The canonical conditional preparations are recomputed from the new live
operator, not a supplied future metric. Their condition number is 1.0004094,
constraint residual 1.54e-16 and stencil-dependent initial-state difference
at most 8.93e-11. The D1/D0 response ratio is about 1.18453e-8. At each case,
source-off and source-on evolutions start from identical physical initial
states. This isolates the source change; it is not a separate reoptimization
of the source-off initial preparation.

Corrected canonical scalar energy/current errors are at most about
1.43e-10/3.66e-9 over the samples. Native-fluid controls do not have this
separate canonical scalar test; they must not be assigned fictitious zero
scalar errors. All sampled Hamiltonian and generalized budget identities
pass the separate 1e-10 algebra gate.

Source-on minus source-off state differences are about 4.521690e-4 in the
frozen component-normalized norm for all heavy cases, and zero at the saved
precision for cold. These are neither integration-error estimates nor
percent changes in an observable. No D01 superiority is inferred from
floating-point-scale differences from D0.

## Remaining errors, tested on both models

Individual photon and massless-radiation rate equations are stricter than
the total sampled metric gate. They are NOT all passing:

| Corrected case | Photon energy | Photon current, exchange removed | Massless energy | Massless current |
|---|---:|---:|---:|---:|
| Native heavy | 4.16438e-3 | 6.31218e-6 | 4.34844e-3 | 5.59285e-3 |
| Cold | 3.67667e-4 | 9.44535e-6 | 5.43950e-4 | 3.41317e-1 |
| Canonical D0 | 4.16437e-3 | 6.61251e-6 | 4.34843e-3 | 5.86053e-3 |
| Canonical D01 | 4.16438e-3 | 6.61251e-6 | 4.34843e-3 | 5.86053e-3 |

Entries are maxima normalized by the largest individual equation term, not
fractions of total cosmic energy. With the same 2e-5 threshold, the photon
current passes while the other three do not. Their absolute residuals and
16/32 derivative-stencil differences are retained in
`radiation-error-budget.csv`, alongside the original-source failures.

For corrected canonical D0, maximum photon/massless energy residuals are
7.775e-20/3.742e-20; corresponding current residuals are approximately
5.991e-24/2.761e-24. Current-stencil differences reach
2.731e-24/1.259e-24. The cold massless current's large relative error similarly
corresponds to an absolute residual about 6.635e-23. This demonstrates why
absolute budgets and conditioning must accompany these relative errors.
It does not convert a failed relative gate into a pass, or prove rounding is
their entire cause. Stencil differences alone are not certified error bounds.

Crucially, the corrected heavy total budget still reaches about 5.87e-15,
whereas the combined radiation contribution is bounded over the sampled
points by about 1.15e-19. The previous dominant-radiation explanation therefore
does not automatically explain the remaining total error. The next stage
must separate other species/background terms from derivative conditioning,
and separately derive the RSA remainder. See `NEXT.md`.

## Scope and reproducibility

- `evolution-summary.json` and `radiation-error-budget.csv` provide small
  summaries; `evolution-*-result.json` and paired NPZ files retain all probes,
  coarse/fine states, normalizations and original/corrected comparisons.
- `corrected-preparations.npz`, `correction-control-packets.npz`, source-code
  hashes, compiler receipts and the isolated copied build preserve the inputs.
- `validate_stage.py` checks source preservation, packet contents, refinements,
  process identities and honest pass/fail separation. `closeout.json` seals
  this stage; `CLEANUP-VERIFIED.json` is the subsequent exit/hash receipt.
- Nine probes and two step counts are not a uniform continuum certificate.
  Higher RSA time/opacity/feedback orders and the prior full-span historical
  archive discrepancy remain outside this short-window acceptance.
- This calculation does not select a galactic initial population or complete
  the Galaxy Lab's measured 3D geometry. GALAXY-07 is retained as an attributed
  external-agent report; no Galaxy fits, files, workers or releases are changed.
- No GitHub operation, automatic relay, timer or unrelated process action is
  part of this checkpoint. These numerical consistency tests are not evidence
  for an improved galaxy, expansion-history or CMB likelihood.
