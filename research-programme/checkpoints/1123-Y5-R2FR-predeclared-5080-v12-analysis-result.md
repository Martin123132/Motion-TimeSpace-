# 5107 — predeclared 5080 v12 analysis result

The unchanged, predeclared 5080 estimator executes successfully on the completed v12 matrix through the exact 5040 margin-schema adapter.

The locked result is `LOCKED_FRESH_PILOT_DOES_NOT_PASS`:

- realized cost-normalized score ratio: `1.3474894142500562`;
- predeclared threshold: `0.8`;
- recorded runtime: `8.938616622583346 h`, below the `10 h` cap;
- matrix: `360/360` converged;
- maximum delete-one shift: `0.9993198848647024` full-estimator standard errors.

This rejects the locked multifidelity estimator as an efficiency improvement. It does not reject the computed kernel, the local-GR programme, or MTS.

Outputs:

- `source-intake/functional_rg/5080/fresh_pilot_analysis_v12.json`
- `source-intake/functional_rg/5080/fresh_pilot_channels_v12.csv`
- `source-intake/functional_rg/5080/fresh_pilot_event_costs_v12.csv`
- `source-intake/functional_rg/5080/fresh_pilot_jackknife_v12.csv`
- `source-intake/functional_rg/5107/predeclared_5080_v12_margin_adapter_execution.json`
- `source-intake/mts_residuals/P8_Y5_BRR545_5080_V12_VALIDATION.csv`
- `source-intake/mts_residuals/P8_Y5_BRR545_5107_VALIDATION.csv`
