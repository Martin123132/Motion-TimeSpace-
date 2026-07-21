# 5099 — E040/S507622/A10 continuous subminimum cycle

## Diagnosis

`E040__S507622_N0000__A10__coarse12` has stable residues but an adaptive residual of about `0.02568`. The old global-cycle selector changes numerical contour gauge when `0.2 min|z_j|` crosses `0.002`, then repeatedly changes which maximal annulus it selects. The exact residue-corrected contour is invariant, but its finite-node representation becomes discontinuous in the relative variable.

## Repair

Use the continuous pointwise contour

`r(q) = 0.2 min_j |z_j(q)|`.

It lies strictly inside every finite global pole. Adding the residues of exactly the causally owned poles reconstructs the same global cycle by Cauchy's theorem. No physical prescription, residue, tolerance, interval cap, or topology is changed; only the auxiliary base-circle gauge is made continuous.

The route is exact-job scoped until a broader regulated-path proof is supplied.

## Outputs

- `scripts/Y5_R2FR_5099_E040_S507622_A10_continuous_subminimum_cycle_certificate.py`
- `source-intake/functional_rg/5099/E040_S507622_A10_continuous_subminimum_cycle_certificate.json`
- `source-intake/mts_residuals/P8_Y5_BRR545_5099_VALIDATION.csv`
