# 5046 - restricted-scope primary24 benchmark

Marker: `MTS_5046_RESTRICTED_SCOPE_PRIMARY24_BENCHMARK`.

The restricted certificate was tested on six `E020/E040` primary24 jobs at
`A00`, `A07`, and `A14`. All six converge and reproduce the legacy numerical
values exactly; the maximum recorded relative difference is `0.0`, below the
locked `2e-6` exactness gate. The earlier broad-guard `A00` offset disappears.

This authorizes a scratch fourth-scramble recomputation only. It does not
authorize a physics claim or a live replacement by itself.

## Evidence

- Dry run: `source-intake/functional_rg/5046/dry_run.json`
- Benchmark: `source-intake/functional_rg/5046/restricted_primary24_benchmark.json`
- Generator: `scripts/Y5_R2FR_5046_restricted_scope_primary24_benchmark.py`
- Validation: `source-intake/mts_residuals/P8_Y5_BRR545_5046_VALIDATION.csv`
