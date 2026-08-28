# 5341 - D4 E00125 event-evidence migration

Date: `2026-08-10`

Marker: `MTS_5341_D4_E00125_EVENT_EVIDENCE_MIGRATION`.

## Executive result

Checkpoint 5341 transfers the already validated `E00125` support-event roots
from the seven-regulator scan in checkpoint 5337 into the D4 event-aligned
runner.  This avoids spending roughly two hours deriving the same roots a
second time.  The transfer is evidence-backed and does not claim an integral.

All `8/8` events pass the target event contract and the D4 dry-run accepts:

```text
epsilon                         = 0.00125,
event count                     = 8,
support entries/exits           = 4,
branch deaths                   = 4,
initial event-aligned segments  = 26,
event-coordinate error bound    = 1.0e-11,
coordinate tolerance            = 1.0e-8.
```

All `12/12` validation gates pass.  The next numerical operation is therefore
the generic support-entry/support-exit affine-log engine followed by the
bounded `E00125` fixed-decay run.

## 1. Source ownership

Checkpoint 5337 supplies the regulator-specific root coordinates, pole values,
contact residuals, transverse slopes and event-type contracts.  Checkpoint
5334 supplies the E0025 event/candidate schema and the current D4 reduced
contract.  The E00125 topology has the same ordered eight-event structure:

```text
E01-E03  support entries,
E04-E07  branch deaths,
E08      support exit.
```

For a support contact, the bracket midpoint is retained as the event
coordinate.  Its central signed support margin is zero by the definition of
the bracketed root, while `1.0e-11` is carried explicitly as the coordinate
error.  The boundary value is reconstructed from the source pole and signed
contact residual.  The non-contact support boundary is inherited from the
same D4 event schema.

No new root is inferred from a synthetic midpoint geometry.

## 2. Cache-identity repair

The first migration attempt exposed an implementation issue rather than a
physics issue: event hashes had been recorded before the D4 target was
configured, so they identified the old D2 parent files.  The script now
refreshes both hashes only after target configuration:

```text
contract = D4_outer_reduced_MC04_cubature_contract.csv,
poles    = D4_outer_E0025_geometric_poles.csv.
```

It then requires `event_cache_current()` before entering the dry-run.  During
that run, candidate and event access are temporarily restricted to the
migrated files; if the cache becomes stale, execution raises immediately
rather than falling back to a duplicate root scan.

## 3. Dry-run result

The target dry-run reports

```text
decision = DRY_RUN_ACCEPTED__RUN_D4_OUTER_EVENT_ALIGNED_REFINEMENT,
event candidates = 8,
refined events   = 8,
initial segments = 26,
plan SHA-256     = 4ce8c35c57b6539780c28fc6db73a99c59489bdfce6f9f4b549bfdaeac197540.
```

Panel containment, source-bracket containment, support-margin tolerance and
branch-death coordinate tolerance all have zero violation.

## 4. Claim boundary

The following narrow flag is true:

```text
valid_for_D4_outer_E00125_event_geometry = true.
```

The following remain false:

```text
valid_for_D4_outer_E00125_fixed_decay_integral;
valid_for_D4_outer_regulator_zero_limit;
valid_for_decay_angle_integral;
valid_for_full_angular_convergence;
valid_for_full_phase_space_coefficient;
valid_for_numeric_UV_claim;
valid_for_local_GR_claim;
valid_for_full_MTS_claim.
```

The event geometry is an input to the integral, not evidence that the integral
or regulator limit converges.

## 5. Artifacts and next action

The checkpoint artifacts are

```text
scripts/Y5_R2FR_5341_D4_E00125_event_evidence_migration.py
source-intake/functional_rg/5341/D4_E00125_event_evidence_migration.csv
source-intake/functional_rg/5341/D4_E00125_event_evidence_migration_result.json
source-intake/functional_rg/5341/source_register.csv
source-intake/functional_rg/5334/E00125/D4_outer_refined_support_events.csv
source-intake/functional_rg/5334/E00125/D4_outer_event_aligned_initial_plan.csv
source-intake/functional_rg/5334/E00125/D4_outer_event_aligned_E00125_dry_run.json
source-intake/mts_residuals/P8_Y5_BRR545_5341_VALIDATION.csv
```

Next, generalize the checkpoint-5339 endpoint normal form to every migrated
support entry or exit, require independent one-sided trace agreement at each
event, and launch one BelowNormal E00125 integral worker only after a strict
dry-run.  The local `0.005` and global `0.01` gates remain unchanged.

No GitHub action is taken.  The protected `formalization-workbench` digest is
unchanged.
