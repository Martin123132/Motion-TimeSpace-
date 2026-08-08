# 5079 — bounded central-anchor pilot status

Marker: `MTS_5079_BOUNDED_CENTRAL_ANCHOR_PILOT_RUNNER`.

## Authoritative state

The completed run is `bounded_central_anchor_pilot_v12`, with config digest
`bb930b0d2c11cd1bf4644b05db976f548e256d10add888144b98cfab95aa7a69` and unchanged schedule digest
`da19db9b4d7f5c1ca41babe2f1fcfafc2f9ed92a043cc4298f1fb5c4bee3f956`.

- All `360/360` jobs are `COMPLETED_CONVERGED`.
- Zero jobs are unconverged, failed, or missing.
- Checkpoint 5103 independently closes the complete job, kernel, topology, digest, certificate, and formalization provenance matrix.
- The predeclared aggregate statistical analysis is complete and does not pass its efficiency gate.
- No efficiency, epsilon-limit, production-`hhh`, local-GR, Newton, or full-MTS claim follows from matrix completion alone.

## Final repair

Checkpoint 5101 proves that the 5097 projective identity is independent of the external argument. For `p'=lambda p`, each of the four factor roots is a ratio of momentum-linear forms of equal degree, so `lambda` cancels exactly for every finite nonzero external factor.

The proof was checked at both reciprocal roots across all fifteen locked E040 arguments. The maximum factor-root mismatch is `2.1763879942877348e-13`; unrelated same-source roots remain separated by at least `0.00312717494022103`.

The runner applies this theorem only to `E040__S507622_N0000__A14__coarse12`. A fresh replay converges in `94.15743670001393 s`, retains the unchanged adaptive residual `0.0003562977572416951 < 0.0005`, and reports all residues stable.

## Locked statistical result

Checkpoints 5104-5107 preserve the unchanged 5080 code and original analysis semantics, bind them to v12, and repair one latent config-schema omission using the exact five margin rows already derived in 5040. The first attempt stopped before writing output; the repaired one-shot execution passes all provenance and validation checks.

The locked result is `LOCKED_FRESH_PILOT_DOES_NOT_PASS`: score ratio `1.3474894142500562` versus the predeclared `0.8`, while runtime passes at `8.938616622583346 h`.

Checkpoint 5108 proves the failure mechanism. The high-only bottleneck is `imag_z-0.3`, whose locked control is zero. Its variance is unchanged while the low bank adds cost, imposing the exact floor
`sqrt((C_correction+3 C_low)/C_high)=1.3474894142500562`.

This rejects the locked multifidelity estimator, not the v12 kernel matrix or MTS. Next: prove or reject an exact conjugation/reflection-symmetric control for the imaginary bottleneck before authorizing more kernels.

## Evidence

- v12 status: `source-intake/functional_rg/5079/runs/bounded_central_anchor_pilot_v12/status.json`
- v12 completion: `source-intake/functional_rg/5079/runs/bounded_central_anchor_pilot_v12/COMPLETED.json`
- 5101 theorem: `source-intake/functional_rg/5101/S507622_projective_cluster_argument_independence.json`
- 5102 carry-forward: `source-intake/functional_rg/5102/v12_argument_independent_projective_carry_forward_result.json`
- 5103 closure: `source-intake/functional_rg/5103/bounded_central_anchor_v12_matrix_closure.json`
- locked analysis: `source-intake/functional_rg/5080/fresh_pilot_analysis_v12.json`
- 5108 diagnosis: `source-intake/functional_rg/5108/locked_pilot_failure_mechanism.json`
- runner: `scripts/Y5_R2FR_5079_bounded_central_anchor_pilot_runner.py`
