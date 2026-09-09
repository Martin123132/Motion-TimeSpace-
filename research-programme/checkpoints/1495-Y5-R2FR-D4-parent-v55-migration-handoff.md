# 5479: D4 parent-v55 migration handoff

Checkpoint 5478 certifies the parent-v55 repair required by the checkpoint-5477 frontier. The repair changes no action, contour, selector, residue, threshold, or acceptance inequality. It is invoked only after the precise parent-v54 stable-edge interval obstruction and evaluates the complete parent-v54 amplitude on an exact rectangular x/t leaf union rather than replacing disconnected leaf images by one interval hull.

## Certified parent-v55 result

- Target parent-v54 failure reproduced: `true`.
- Target parent-v55 result: passed on an exact `2 x 32` cover (`64` complete-amplitude leaves).
- Minimum selected parent amplitude-denominator lower bound: `2.3640791503504712e-07`.
- Minimum collision-Jacobian lower bound: `0.023597972930495505`.
- Centered-invariant diagnostic minimum: `0.0`; this weaker diagnostic is intentionally non-gating.
- Untriggered control: byte-for-byte equivalent result.
- Checkpoint-5478 validations: all passed.

The proof object is the complete parent-amplitude leaf certificate, including its denominator and collision-Jacobian bounds. The standalone centered invariant is only a diagnostic and must not be promoted back into an acceptance gate.

## Immutable migration source

- Source state: `source-intake/functional_rg/5477/work-v1/E07__U051__RIGHT_CONNECTOR__CUBOID__6df3d70a73e4618b.json`.
- SHA-256: `f268b8217afeb4f54c6d85a51755e216cc05b54e5eabfc91467d6cbba2829262`.
- Accepted nodes: `162`.
- Pending nodes: `13`.
- Unresolved nodes: `0`.
- Source decision: `PARENT_V54_FRONTIER_PARTIAL__RESUME`.

Checkpoint 5477 remains the source of truth. Checkpoint 5478 has not yet been installed into a resumable frontier, so the active cuboid is not complete.

## Exact next calculation

Create `scripts/Y5_R2FR_5480_D4_parent_v55_hash_locked_frontier_runner.py`. Copy the checkpoint-5477 state byte-for-byte, verify the source hash above before any evaluation, and install the evaluator chain `v52 -> v53 -> v54 -> v55`. Run status-only first, then at most one bounded `900 s` / `8`-node batch using one BelowNormal single-core worker. Commit each node atomically and stop on any unsigned exception.

The next runner must preserve every accepted and pending box, retain the original failure witnesses, and invoke v55 only for the demonstrated stable-edge class. It must not use the zero centered-invariant diagnostic as a rejection condition.

## Claim boundary

This closes a local parent-evaluator obstruction only. Full active-cuboid coverage, the complete outer enclosure, event-local or combined `W3`, the D4 regulator limit, all-operator local GR, and full MTS remain unproved. No GitHub action and no `formalization-workbench` edit belongs to this checkpoint.

**PARENT_V55_DERIVATION_SAVED__HASH_LOCKED_FRONTIER_MIGRATION_NEXT**
