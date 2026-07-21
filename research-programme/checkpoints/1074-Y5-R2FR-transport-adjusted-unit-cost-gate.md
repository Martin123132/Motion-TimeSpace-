# 5058 - transport-adjusted unit-cost gate

Marker: `MTS_5058_TRANSPORT_ADJUSTED_UNIT_COST_GATE`.

Charging the one required full-homotopy fallback and the measured transport
runtime saves a mean `1374.61 s` per high event. Mean high-primary cost falls
from `6492.92 s` to `5118.31 s`, and paired-correction cost falls from
`6861.22 s` to `5486.61 s`.

The shortcut does not by itself make the multifidelity estimator preferable
under 10 hours because it also makes the high-only comparator cheaper. The
conservative design's best sub-cap score is `0.980` at `9.73 h`, still not below
the locked `0.8` efficiency gate. Its first efficient integer allocation is
`18.02 h`; no fresh science run is authorized.

## Evidence

- Result: `source-intake/functional_rg/5058/transport_adjusted_unit_cost_gate.json`
- Event costs: `source-intake/functional_rg/5058/transport_adjusted_event_costs.csv`
- Designs: `source-intake/functional_rg/5058/transport_adjusted_designs.csv`
- Generator: `scripts/Y5_R2FR_5058_transport_adjusted_unit_cost_gate.py`
- Validation: `source-intake/mts_residuals/P8_Y5_BRR545_5058_VALIDATION.csv`

This is a retrospective operational projection, not a physics result.
