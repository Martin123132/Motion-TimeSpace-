# 5106 — predeclared margin schema-adapter lock

The missing `target_precision_budgets` rows are not new choices. Checkpoint 5040 derived them from the 5018 fixed-target source using `target=-known_nonlocal_residual/2` and `margin=known_master_error/2`; all later estimator-design checkpoints used the same five rows.

This checkpoint independently rederives those rows, requires exact equality to the historical 5040 config, records the failed 5105 attempt, and hash-locks a new one-shot wrapper. The adapter injects only the missing config field in memory. It does not change the unchanged 5080 analysis code, seeds, controls, covariance estimator, score, `0.8` threshold, ten-hour cap, or claim boundaries.

Outputs:

- `scripts/Y5_R2FR_5106_predeclared_margin_schema_adapter_lock.py`
- `scripts/Y5_R2FR_5107_execute_5080_v12_with_margin_adapter.py`
- `source-intake/functional_rg/5080/fresh_pilot_analysis_lock_v12_margin_adapter.json`
- `source-intake/functional_rg/5105/predeclared_5080_v12_schema_failure.json`
- `source-intake/functional_rg/5106/predeclared_margin_schema_adapter_lock.json`
- `source-intake/mts_residuals/P8_Y5_BRR545_5106_VALIDATION.csv`
