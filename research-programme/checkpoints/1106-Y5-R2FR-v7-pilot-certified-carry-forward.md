# 5090 - v7 pilot certified carry-forward

Marker: `MTS_5090_V7_PILOT_CERTIFIED_CARRY_FORWARD`.

The failed v6 run is preserved unchanged. A new
`bounded_central_anchor_pilot_v7` run was built with a numerical-contract hash
of `ee4250c269f6fa70e7ff1c580edd15dc29345f340111d7282358f0f8dfd89257`.
The v6 and v7 numerical configurations are identical after removing only run
identity, source hashes, schema revision, and the new narrowly scoped 5088
policy.

All 112 previously converged v6 jobs and 83 causal topologies were copied with
source/output hashes and explicit carry-forward provenance. The repaired A07
job comes only from the accepted 5089 fresh integration run. The staged v7
matrix therefore began at `113/360` converged, zero failed.

The pilot was then resumed under the four-hour invocation cap with one new-job
limit. `E020__S507603_N0000__A08__primary24` converged in `76.35 s`, with
all residues stable and event residual `1.24255e-13`. The current matrix is
`114/360` converged, zero failed, 246 missing, and paused normally at the job
cap. The next missing row is `E020__S507603_N0000__A09__primary24`.

## Evidence

- Carry-forward result: `source-intake/functional_rg/5090/v7_certified_carry_forward_result.json`
- Hash manifest: `source-intake/functional_rg/5090/v7_certified_carry_forward_manifest.json`
- Generator: `scripts/Y5_R2FR_5090_v7_pilot_certified_carry_forward.py`
- Live v7 status: `source-intake/functional_rg/5079/runs/bounded_central_anchor_pilot_v7/status.json`
- Validation: `source-intake/mts_residuals/P8_Y5_BRR545_5090_VALIDATION.csv`

The matrix is incomplete, so statistical analysis and any physical claim remain
blocked.
