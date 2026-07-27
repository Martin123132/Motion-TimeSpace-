# 5100 — v11 continuous-subminimum-cycle carry-forward

v10 stopped at `E040__S507622_N0000__A10__coarse12` after `355` converged rows. Checkpoint 5100 carries only those converged rows into v11 and excludes A10 for a fresh replay under the exact 5099 contour certificate.

The schedule is unchanged. The only allowed config deltas are the run id, schema/config digests, source ledger, and the exact A10 continuous-subminimum policy.

Outputs:

- `scripts/Y5_R2FR_5100_v11_continuous_subminimum_cycle_carry_forward.py`
- `source-intake/functional_rg/5100/v11_continuous_subminimum_cycle_carry_forward_result.json`
- `source-intake/functional_rg/5100/v11_continuous_subminimum_cycle_carry_forward_manifest.json`
- `source-intake/mts_residuals/P8_Y5_BRR545_5100_VALIDATION.csv`
