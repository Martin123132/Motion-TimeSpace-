# Source variation between saved epochs — 2026-11-12

Authoritative result: `corner-safe-result.json`, per-case `cold-corner-safe-result.json` and `heavy-corner-safe-result.json`; the earlier `result.json` and `cell-result.json` deliberately retain failed diagnostic checks.

## Advance

Derived a piecewise integral remainder and a Bernstein enclosure for its numerical curvature reconstruction, then applied the saved absolute response gains. Acquired only read-only restart probes of the retained native histories. Original bank, 902 signed preparation nodes, physical grids, nine reporting epochs, masses/couplings, backgrounds and tolerances remain unchanged. The prior successful quadratic physical prediction is not replaced.

Baseline: 909 saved gaps split into 1,198 cells, with 289 background corners. MTS: 909 gaps, 1,623 cells, 714 corners. Across both cases, 29,217 diagnostic readouts were obtained in serial bounded workers, including initial/restart controls and fresh validation. No new observational fit or external dataset.

## Fresh frozen-prediction checks

At 2,396 baseline and 3,246 MTS fresh one-sixth/five-sixths times, maximum channel-scaled curvature errors are:

| Case | External density curvature | External current curvature | Gate |
|---|---:|---:|---:|
| Baseline | 3.70720e-14 | 1.25368e-13 | 2e-5 |
| MTS | 1.44572e-9 | 7.11963e-12 | 2e-5 |

The source integral also matches all nine saved boundary readouts: baseline D/Q relative errors 2.36560e-15 / 6.93325e-16; MTS 4.31756e-15 / 1.11752e-14. These tiny source-readout residuals are numerical consistency checks, not claimed accuracy of the full physical theory.

The earlier frozen-quadratic baseline D-source miss (3.220411e-5 versus 2e-5) remains in its original checkpoint. The missing between-epoch curvature variation explains it: adding the derived source integral passes the same source comparison without changing the gate or retrospectively rewriting the earlier prediction.

## Final-epoch working budget

| Case/output | Variation envelope | Observed interpolation/restart allowance | Fraction of available margin used |
|---|---:|---:|---:|
| Baseline density | 6.62210037e-12 | 7.64783e-24 | 3.54090e-9 |
| MTS density | 3.67948968e-12 | 1.47729e-19 | 3.91149e-6 |
| MTS current | 4.48618075e-14 | 1.79732e-21 | 6.49611e-8 |
| MTS pressure | 3.70058565e-12 | 1.46020e-19 | 0.000775045 |

Thus the most sensitive MTS pressure output spends about **0.0775% of its remaining margin** on this numerical source-variation estimate. Baseline dust current/pressure stay identically zero. The old frozen-curvature contribution (~2.13% of the old linear margin) is a different quantity and must not be confused with this additional variation.

The polynomial enclosure is derived; the true-minus-polynomial uniform error is not certified by finite probes. These are numerical working-budget passes. An explicit remaining continuous residual inequality is recorded in DERIVATION.md.

## Failure and repair trail

- The first scorer stopped at its first synthetic test because a legacy comparison helper requires arrays, not Python lists. `score_variation-attempt01.py` and failure receipts remain. No scientific output existed at that failure; the array conversion did not alter tolerances or formulas.
- The first piecewise-linear curvature diagnostic failed MTS D at 2.92237e-4 relative. A quartic diagnostic still failed at 1.67546e-4, concentrated in two cells.
- Investigation found two nominal left-side thermal samples rounded onto the right-hand branch. Only four targeted native readouts were needed to repair them. The wrong-side packets, failed checks and diagnosis remain intact.
- Correct native cell identities are now verified. Actual one-sided sample coordinates are used. New predictions were frozen and tested at fresh times for BOTH cases, with the original 2e-5 and 1e-10 gates.

## Ownership and scope

No physical source law was fitted or replaced. No fresh radiation/gas propagation was run in this stage; the budget reuses existing response gains. Private local work only, no GitHub or coordinator action. Earlier sealed checkpoints are checked unchanged. See `validation.json`, `closeout.json` and `CLEANUP-VERIFIED.json`; no task worker is intended to remain running. Goal remains paused for manual continuation.
