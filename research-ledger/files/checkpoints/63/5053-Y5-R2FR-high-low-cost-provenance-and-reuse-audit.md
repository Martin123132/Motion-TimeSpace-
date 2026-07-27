# 5053 - high/low cost provenance and reuse audit

Marker: `MTS_5053_HIGH_LOW_COST_PROVENANCE_AND_REUSE_AUDIT`.

All 120 event/argument rows were traced to their measured runtime source and
topology artifact. The mean one-event costs are:

- high primary `H`: `6492.92 s`;
- paired high correction, including its coarse `L` kernel: `6861.22 s`;
- low-only topology: `1498.16 s`;
- low-only kernel: `368.30 s`;
- complete low-only event: `1866.46 s`.

The coarse value in a high correction safely reuses that event's exact `E040`
topology. Fresh low-only events do not. No high topology charge is duplicated,
and none of the 120 `E020/E040` topology pairs is hash-identical. The previous
high cost also omitted the coarse kernel required by `H-L`; this audit restores
it.

The corrected full-vector score ratio is `0.6706`, but the runtime figures here
still inherit the paired-variance/single-event-cost mismatch later repaired in
5055. Use this checkpoint for provenance and 5055 for execution time.

## Evidence

- Result: `source-intake/functional_rg/5053/high_low_cost_provenance_and_reuse_audit.json`
- Rows: `source-intake/functional_rg/5053/high_low_cost_rows.csv`
- Events: `source-intake/functional_rg/5053/high_low_event_costs.csv`
- Generator: `scripts/Y5_R2FR_5053_high_low_cost_provenance_and_reuse_audit.py`
- Validation: `source-intake/mts_residuals/P8_Y5_BRR545_5053_VALIDATION.csv`
