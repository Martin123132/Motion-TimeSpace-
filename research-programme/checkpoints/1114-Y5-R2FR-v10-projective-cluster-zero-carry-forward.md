# 5098 — v10 projective-cluster-zero carry-forward

The v9 matrix stopped correctly at `E040__S507622_N0000__A00__coarse12` with `345` converged rows, one residue-only obstruction, and fourteen unexecuted rows.

Checkpoint 5098 creates v10 under the new 5097 certificate contract. It carries only the `345` previously converged job, kernel, and topology records, rewrites their top-level config digest, and deliberately excludes the repaired A00 row.

The only permitted config changes are the run id, schema revision, config digest, source-file ledger, and exact projective cross-source cluster-zero policy. The schedule digest remains unchanged.

Outputs:

- `scripts/Y5_R2FR_5098_v10_projective_cluster_zero_carry_forward.py`
- `source-intake/functional_rg/5098/v10_projective_cluster_zero_carry_forward_result.json`
- `source-intake/functional_rg/5098/v10_projective_cluster_zero_carry_forward_manifest.json`
- `source-intake/mts_residuals/P8_Y5_BRR545_5098_VALIDATION.csv`
