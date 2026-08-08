# 5077 - central-anchor pilot runner

Marker: `MTS_5077_CENTRAL_ANCHOR_PILOT_RUNNER`.

The locked manifest expands to 360 jobs: 120 `primary24` and 240 `coarse12`.
Only 16 `A08` full homotopies are required; 284 topologies are produced by the
certified argument/epsilon constructors. The history-invariant breakpoint rule
is local to this opt-in runner.

Revision v7 removes all use of the quarantined broad 5041 theorem. It applies
the guarded 5084 recoil-source theorem, the fail-closed 5085 same-source
removable extension, and the 5086 outward-contour gate. A six-job v7 smoke
exercises a full anchor, forward argument composition, epsilon composition,
and both kernel profiles. All six converge fresh and all six resume from cache.
Failed or unconverged rows are never accepted as resumable completions.

## Evidence

- Gate: `source-intake/functional_rg/5077/central_anchor_pilot_runner_gate.json`
- Dry run: `source-intake/functional_rg/5077/central_anchor_pilot_dry_run.json`
- Smoke: `source-intake/functional_rg/5077/runs/central_anchor_integration_smoke_v7/smoke_result.json`
- Runner: `scripts/Y5_R2FR_5077_central_anchor_pilot_runner.py`
- Validation: `source-intake/mts_residuals/P8_Y5_BRR545_5077_VALIDATION.csv`

The runner remains default-off and cannot launch the full pilot by itself.
