# 5078 - fresh central-anchor topology cost smoke

Marker: `MTS_5078_FRESH_CENTRAL_ANCHOR_TOPOLOGY_COST_SMOKE`.

One genuinely fresh seed, `507601`, is taken through all 30 required topology
artifacts: one `E040/A08` full anchor, 14 bidirectional argument constructions,
and 15 epsilon constructions. Every document passes its event, argument,
configuration, and kernel-contract metadata checks.

Measured construction time is `53.525 s`, or `56.425 s` after the declared
`2.9 s` write allowance. This is below the historical projected range
`59.198-174.860 s` and is `0.527` times its mean. A second invocation resumes
all 30 artifacts in `0.142 s`.

## Evidence

- Result: `source-intake/functional_rg/5078/fresh_central_anchor_topology_cost_smoke.json`
- Fresh rows: `source-intake/functional_rg/5078/fresh_topology_rows.csv`
- Resume rows: `source-intake/functional_rg/5078/resume_topology_rows.csv`
- Generator: `scripts/Y5_R2FR_5078_fresh_central_anchor_topology_cost_smoke.py`
- Validation: `source-intake/mts_residuals/P8_Y5_BRR545_5078_VALIDATION.csv`

One event supports the runtime envelope but cannot by itself authorize a
numerical or physical conclusion.
