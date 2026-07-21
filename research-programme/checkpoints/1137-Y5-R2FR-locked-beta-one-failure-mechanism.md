# 5121 - locked beta-one failure mechanism

## Why the design estimate failed

The design-stage score was `0.7462906810169911`; the independent-control
result is `1.5148246022524876`. The change is not a runtime overrun: actual
accepted runtime is slightly below the locked ten-hour cap.

The decisive difference is the independently observed control variance. At
the realized bottleneck `real_z-0.3`, it is `4.8092264142119125` times the
four-high design proxy. Other channels also move differently, changing the
bottleneck from the design-stage `imag_z-0.3` to `real_z-0.3`.

## Robustness diagnostics

Postdecision diagnostics do not change the locked decision:

- best score allowed by the original runtime cap: `1.5045429011673104` at
  ratio `3.084806310935511`;
- best score scanned through ratio 20: `1.1723088359800824`;
- best delete-one-low score: `1.1088196291370827`;
- no single low-row deletion passes `0.8`;
- largest delete-one estimator shift remains below one standard error.

Therefore this is not one corrupted event, one slow event, or an unfortunate
allocation within the original budget. Retuning beta or deleting rows after
seeing these controls would invalidate the lock.

## Decision

`LOCKED_BETA_ONE_CONTROL_VARIANCE_ROUTE_REJECTED_UNDER_ORIGINAL_BUDGET`.

Retain both completed matrices as numerical evidence. Return to the high-only
`hhh`-cut/UV-coefficient route unless a genuinely new control is first derived
and independently locked.

## Outputs

- `scripts/Y5_R2FR_5121_locked_beta_one_failure_mechanism.py`
- `source-intake/functional_rg/5121/locked_beta_one_failure_mechanism.json`
- `source-intake/functional_rg/5121/control_variance_inflation_by_channel.csv`
- `source-intake/functional_rg/5121/postdecision_allocation_diagnostic.csv`
- `source-intake/functional_rg/5121/delete_one_low_score_diagnostic.csv`
- `source-intake/mts_residuals/P8_Y5_BRR545_5121_VALIDATION.csv`
