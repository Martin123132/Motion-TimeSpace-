# 5057 - direct target-root topology transport benchmark

Marker: `MTS_5057_DIRECT_TARGET_ROOT_TOPOLOGY_TRANSPORT_BENCHMARK`.

For every structurally seedable pair, each saved `E040` collision branch was
matched projectively to the roots obtained directly from the exact target
rationals at `E020`. The saved `E020` topology was used only as the validation
target.

All 119 permitted transports reproduce the full `E020` numerical signature
exactly. The maximum crossing-root error is `1.32e-16`, the maximum source-root
representation error is `1.33e-16`, and the mean direct transport time is
`0.00394 s` per argument. `S503402_N0000/A06` remains an explicit full-homotopy
fallback.

## Evidence

- Result: `source-intake/functional_rg/5057/direct_target_root_topology_transport_benchmark.json`
- Rows: `source-intake/functional_rg/5057/epsilon_transport_rows.csv`
- Generator: `scripts/Y5_R2FR_5057_direct_target_root_topology_transport_benchmark.py`
- Validation: `source-intake/mts_residuals/P8_Y5_BRR545_5057_VALIDATION.csv`

Transport is validated retrospectively here; this checkpoint alone does not
provide an a-priori transition detector.
