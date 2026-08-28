# 5343 - D4 E00125 log-corrected resumable runner

Date: `2026-08-10`

Marker: `MTS_5343_D4_E00125_LOG_CORRECTED_RESUMABLE_RUNNER`.

## Current result

Checkpoint 5343 integrates the four checkpoint-5342 support-endpoint normal
forms into the source-owned D4 adaptive evaluator. Its strict preflight and
bounded pause/resume chain pass. Final run `20260811-063701` has all `456/456`
manifest nodes at `COMPLETE_PASS`, zero failed or malformed shards, all planned
topology segments entered, `38` adaptive panels and `32` accepted leaves. The
coordinate-inclusive fixed-decay disk passes its frozen one-percent gate.

The active numerical contracts remain

```text
local Q4/Q8 relative-change limit = 0.005,
global conservative-error limit   = 0.01,
maximum adaptive depth            = 4,
one BelowNormal numerical worker.
```

No threshold is relaxed relative to the accepted E0025 rung.

## 1. Root-scan exclusion

The parent cache loader attempted to invalidate the migrated event plan
because its in-memory serialization hash did not reproduce the hash written
by checkpoint 5341.  That fallback would have repeated the expensive event
root scan and partially overwritten the eight-row event file.

Checkpoint 5343 now refuses that fallback.  It validates the saved dry-run
directly against

```text
the checkpoint-5341 plan hash,
the eight current event rows,
the current D4 contract and pole hashes,
the 26-row initial partition,
the accepted parent smoke validation.
```

If any of these fail, execution raises rather than deriving roots again.  The
eight-event file was deterministically restored by rerunning checkpoint 5341
after the interrupted fallback; no integral shard was lost.

That deterministic rerun changed the volatile runtime/timestamp fields in the
checkpoint-5341 result JSON. The stale checkpoint-5342 provenance hash was
repaired without altering any numerical value or claim flag and propagated
through the checkpoint-5343 parent ledger. The current wrapper now verifies
all ten recursive source hashes before accepting a resumable state.

## 2. Endpoint correction contract

For an event-adjacent panel, the runner first evaluates the unmodified parent
integral.  It constructs

```text
raw      = parent inner integral,
model    = s(C0+C1 delta) Log(z0+z1 delta),
regular  = raw-model,
corrected quadrature = quadrature(regular)+exact integral(model).
```

The correction is unavailable before depth four and is selected only if

```text
the raw panel fails the unchanged local gate;
the raw value is reproduced to <= 5e-13;
the affine gap path does not cross the principal-log cut;
the exact model improves its Q8 error;
the regular remainder passes 0.005;
the reconstructed panel passes 0.005;
the reconstructed disagreement is smaller than the raw disagreement.
```

Otherwise the raw parent result is retained.  The method is therefore an
audited exact add-and-subtract repair, not an unconditional replacement.

## 3. Cut-safety preflight

At maximum depth, each support contact has two event-adjacent sides.  All
eight are explicitly checked:

```text
E01: P08S01 and P08S02,
E02: P08S03 and P08S04,
E03: P10S01 and P10S02,
E08: P12S01 and P12S02.
```

All `8/8` affine gap paths avoid the principal-log cut and have finite exact
model primitives.  All `8/8` dry-run gates pass.

## 4. Coordinate error and claim boundary

The complete finite-rung budget is required to include the four-event linear
sum

```text
E_coordinate = 0.001319687531993736.
```

The final acceptance test is therefore

```text
(E_outer + E_inner + E_coordinate) / |I_E00125| <= 0.01.
```

The accepted finite-rung result is

```text
I_E00125 = 5.715762762970536 + 6.4917551451104485 i;
|I_E00125| = 8.649440954572068;
E_total = 0.02210570410532891;
E_total / |I_E00125| = 0.002555737905077426.
```

Therefore `valid_for_D4_outer_E00125_fixed_decay_integral` is true. All of the
following stronger claims remain false:

```text
valid_for_D4_outer_regulator_zero_limit;
valid_for_decay_angle_integral;
valid_for_full_angular_convergence;
valid_for_full_phase_space_coefficient;
valid_for_numeric_UV_claim;
valid_for_local_GR_claim;
valid_for_full_MTS_claim.
```

## 5. Bounded workflow

The launcher writes a separate run directory containing

```text
log.txt,
error.txt,
status.json,
completion.marker.
```

Each invocation runs at most one BelowNormal Python worker for its requested
bounded interval, finishes the current node before pausing, and preserves all
accepted shards. Final run `20260811-063701` ended with exit code zero, an
empty error log and decision
`D4_E00125_LOG_CORRECTED_FIXED_DECAY_RUNG_ACCEPTED`.

There is no pending frontier. The exact endpoint correction was selected once:

```text
panel P12S02LLLL;
adaptive depth 4;
event type SUPPORT_EXIT;
raw/reconstructed Q4-Q8 relative change = 1.7039431759946728e-05;
regular-remainder Q4-Q8 relative change = 2.3756322395446425e-06;
model Q8 relative error = 7.886913549952869e-05;
raw reproduction error = 0.
```

Depth four is the frozen maximum and the first depth at which the exact
endpoint correction may be selected. Its successful use closes the finite
`E00125` rung without relaxing any threshold.

## 6. Artifacts and next action

The checkpoint artifacts are

```text
scripts/Y5_R2FR_5343_D4_E00125_log_corrected_resumable_runner.py
scripts/run_5343_E00125_bounded.ps1
source-intake/functional_rg/5343/D4_E00125_endpoint_correction_preflight.csv
source-intake/functional_rg/5343/D4_E00125_log_corrected_resumable_runner_result.json
source-intake/functional_rg/5343/source_register.csv
source-intake/functional_rg/5343/runs/20260811-063701/status.json
source-intake/mts_residuals/P8_Y5_BRR545_5343_VALIDATION.csv
```

The finite `E00125` rung is closed. Checkpoints 5346--5349 now test its endpoint
coefficient against two additional finite regulators. Those coefficient tests
do not establish a regulator-zero limit for this full fixed-decay integral.

No GitHub action is taken.  The protected `formalization-workbench` digest is
unchanged.
