# 5116 - 5111 external-timeout recovery

## Recovery audit

The capped 5111 continuation was interrupted by the outer shell timeout while
the runner was preparing schedule row 75. The runner processes were stopped,
then the run was audited from durable exact-digest job records rather than the
stale `RUNNING` status field.

The durable prefix is contiguous:

- converged: `74/180`;
- failed or unconverged: `0`;
- missing: `106`;
- last durable row: schedule 74,
  `E020__S507615_N0000__A13__primary24`;
- next row: schedule 75,
  `E020__S507615_N0000__A14__primary24`.

The interrupted next row left neither a job record nor a kernel record, so
there is no partial result to quarantine or accept. `status.json` is
reconciled to `PAUSED_EXTERNAL_TIMEOUT_RECOVERED`. Resume must recompute the
first missing row and may accept only exact-config-digest
`COMPLETED_CONVERGED` records.

## Status

- durable-prefix audit: passed;
- recovery validation: `9/9` passed;
- statistical analysis: blocked until `180/180` converge;
- independent efficiency and full MTS claims: not allowed.

## Outputs

- `scripts/Y5_R2FR_5116_5111_external_timeout_recovery.py`
- `source-intake/functional_rg/5116/5111_external_timeout_recovery.json`
- `source-intake/mts_residuals/P8_Y5_BRR545_5116_VALIDATION.csv`
