# 5118 - E020 control-extension second capped pass

## Durable result

After the 5117 repair, the locked 5111 matrix was resumed without changing
its config, estimator, tolerances, topology assignments or target list. The
clean wall-cap pause now has:

- `126/180` exact-digest jobs converged;
- `0` failed or unconverged jobs;
- `54` missing jobs;
- last durable row: schedule 126,
  `E020__S507619_N0000__A05__primary24`;
- next row: schedule 127,
  `E020__S507619_N0000__A06__primary24`;
- state: `PAUSED_WALL_CAP`.

The durable prefix is contiguous. The repaired A14 row contains 1472 guarded
cluster evaluations and is `COMPLETED_CONVERGED`. The protected
`formalization-workbench` hash remains
`b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758`.

## Decision

The matrix is 70 percent complete, but the predeclared complex-control
analysis requires all 180 rows. No partial estimator score is calculated.
Resume from the first missing row; once `180/180` converge, execute the locked
beta-one analysis with its existing ratio, threshold, margins and runtime
accounting.

## Outputs

- `scripts/Y5_R2FR_5118_5111_second_capped_pass_reconciliation.py`
- `source-intake/functional_rg/5118/5111_second_capped_pass_reconciliation.json`
- `source-intake/mts_residuals/P8_Y5_BRR545_5118_VALIDATION.csv`
