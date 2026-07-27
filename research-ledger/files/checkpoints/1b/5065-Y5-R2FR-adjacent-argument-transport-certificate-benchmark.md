# 5065 - adjacent-argument transport certificate benchmark

Marker: `MTS_5065_ADJACENT_ARGUMENT_TRANSPORT_CERTIFICATE_BENCHMARK`.

The epsilon continuation certificate was applied to all 112 adjacent edges of
the ordered `E040` argument ladder. It safely transports 42 edges, sends 70 to
full homotopy, produces no failed transports or false negatives, and reproduces
accepted target roots to `1.31e-16`.

The first retrospective projection reduces mean topology time from `1498.16 s`
to `1035.66 s` per event, a `30.9%` reduction. This is not yet a complete chain:
41 projective cases and seven unconverged certificates remain conservative
fallbacks.

## Evidence

- Result: `source-intake/functional_rg/5065/adjacent_argument_transport_certificate_benchmark.json`
- Rows: `source-intake/functional_rg/5065/adjacent_argument_certificate_rows.csv`
- Generator: `scripts/Y5_R2FR_5065_adjacent_argument_transport_certificate_benchmark.py`
- Validation: `source-intake/mts_residuals/P8_Y5_BRR545_5065_VALIDATION.csv`

This is a topology-cost result, not MTS physics evidence.
