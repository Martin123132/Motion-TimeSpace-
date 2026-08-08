# 5092 - v8 pilot certified carry-forward

Marker: `MTS_5092_V8_PILOT_CERTIFIED_CARRY_FORWARD`.

The v7 run remains preserved with its coarse-A11 failure. A new
`bounded_central_anchor_pilot_v8` run carries 131 converged jobs, 131 kernels,
and 90 distinct topologies under source and target hashes.

The only allowed top-level configuration changes are `run_id`,
`schema_revision`, `source_files`, the exact-double-zero policy, and the
derived `config_digest`. The corrected v8 digest is
`06df9ddc2bcfb27e4bfd8c302c069ddc4776165207cd11d9cce79449fda9a033`;
the schedule digest remains unchanged.

An initial integration invocation exposed a missing constructor argument and
failed before numerical evaluation. That file was not accepted: the wiring
was corrected, the carry-forward was rebuilt under the corrected source hash,
and coarse A11 was freshly executed. It converged in `278.48 s`, with six 5091
guard calls and zero numerical-removable calls.

The v8 matrix then advanced through coarse A12-A14 and the first two primary
rows of event `S507604_N0000`. Current state is `137/360` converged, zero
failed, 223 missing, and `PAUSED_JOB_CAP`.

## Evidence

- Carry result: `source-intake/functional_rg/5092/v8_certified_carry_forward_result.json`
- Hash manifest: `source-intake/functional_rg/5092/v8_certified_carry_forward_manifest.json`
- Validation: `source-intake/mts_residuals/P8_Y5_BRR545_5092_VALIDATION.csv`
- Live status: `source-intake/functional_rg/5079/runs/bounded_central_anchor_pilot_v8/status.json`
- Runner: `scripts/Y5_R2FR_5079_bounded_central_anchor_pilot_runner.py`

The exact next row is
`E040__S507604_N0000__A02__primary24`. Aggregate 5080 statistics remain
unauthorized until all 360 jobs converge.
