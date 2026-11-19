# Next eight saved epochs — 2026-11-15

Authoritative results: `result.json`, `cold-result.json`, `heavy-result.json`. Both cases pass all requested checks. The original nine rows remain byte-identical in both32/64 runs; eight new rows extend the total to17, through native index2908.

## Completed

- Same physical bank/grids,902 signed nodes, background, masses/couplings, normalization,2e-5/1e-10 gates and solver accuracy. Source-history, original quadratic control and independent difference states all continue from saved endpoints.
- Only11 baseline and13 MTS source cells added. All48 fresh frozen curvature predictions pass, with correct native one-sided branch checks. Old source cells and original910 main packets are byte-identical.
- New weighted-reference readouts at7,216 shifted node/epoch pairs per case, checked under two native probe schedules. Old reference uncertainty was NOT extrapolated; no new fitting or initial-offset adjustment.
- New endpoint gains computed and checked, rather than reusing the shorter-window allowance. All60 forward/adjoint, envelope and gain-refinement checks pass.

## New block: error plus numerical working allowance

These numbers use the original fixed reference scales and unchanged2e-5 gate:

| Case | Density | Current | Pressure |
|---|---:|---:|---:|
| Baseline | 2.54390765e-10 | identically zero | identically zero |
| MTS | 5.06595905e-11 | 7.06340825e-12 | 3.31779607e-10 |

All17 reports pass; the largest whole-window MTS pressure allowance remains1.19075113e-6 from the preserved earlier window. New-block residuals are against a direct native reference, while earlier rows retain their historical interpolated reference and uncertainty. The smaller new-block numbers are NOT evidence of a newly improved observational fit.

Native boundary-state and metric-force comparisons pass for both cases, as do both external source channels and per-node/weighted full-versus-difference superposition. Difference-equation pressure refinement is5.16843e-10 relative to the correction, inside2e-5.

## Actual response versus extended allowance

| Output | Actual final change from the original quadratic control | New endpoint envelope | Fraction used |
|---|---:|---:|---:|
| Baseline density | -1.9330400766e-11 | 1.0716115104e-10 | 18.04% |
| MTS density | -1.2212650328e-11 | 6.1941712045e-11 | 19.72% |
| MTS current | -2.3380956613e-13 | 1.4608186499e-12 | 16.01% |
| MTS pressure | -1.1856668450e-11 | 6.1247766132e-11 | 19.36% |

The pressure correction grew about16.18-fold on doubling the short duration, while remaining inside the recomputed envelope. This is consistent with a leading fourth-order time response, not proof of a universal scaling law. No coefficient was tuned to this factor.

## Reference and scope

The largest absolute-weighted native query-path discrepancies are5.06e-15 for baseline density and1.34e-14 for MTS pressure. Arithmetic and initial recapture are included separately. These are numerical working uncertainties, not certified continuum error bars or protection against common systematic error.

This remains a conditional propagation test of the retained model with a supplied native surrounding-source history. It is not a new observational result, a new galactic occupation prescription or closed evolution of every species under changed initial conditions.

Private local work only. No GitHub, browser relay, subagents, native rebuild or unrelated worker changes. Original checkpoints remain unchanged. See `validation.json`, `closeout.json` and `CLEANUP-VERIFIED.json`; the persistent goal stays paused for manual continuation.
