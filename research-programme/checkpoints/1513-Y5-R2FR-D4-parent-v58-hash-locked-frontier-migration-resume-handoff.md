# 5497: D4 parent-v58 hash-locked frontier migration resume handoff

## Certified migration

- Source frontier: checkpoint 5484, `178/8/0`, SHA-256 `3f485d18bb2a55d3fda317091e58c0330166a7b5ae7e2185a82ab46602e23faa`.
- Parent-v58 target certificate: checkpoint 5496, SHA-256 `27dc7fce1f83b424e9d9341778a392b83ed7c8659d12e05afd561338782fc708`.
- Target: `R_E0S_E0S_E0S_E1S` in `E07__U051__RIGHT_CONNECTOR__CUBOID__6df3d70a73e4618b`.
- Exact rational partition proof: five interior-disjoint pending descendants, zero accepted or unresolved descendants, volume error exactly `0`.
- Migration: remove the five pending descendants, add one accepted coarse target, retain four failures as superseded history.
- Migrated frontier: `179/3/0`; accepted volume `5.960853174050594e-07`; full partition error `0.0`.
- New node evaluations: `0`; parent-v58 certificate applications during migration: `0`.
- Validation: `15/15` gates pass; 13 registered sources are current.

The earlier decimal reference `5.96085317405059e-07` differs from the stored
binary-float sum by four units in the final displayed decimal place. The gate
requires exact rational equality of the serialized accepted-box volumes and an
eight-ulp bound against that reference; it does not rely on loose geometric
tolerance.

## Remaining frontier

The pending stack is, in stored order:

1. `R_E1S`, epsilon `[0.01,0.020001]`;
2. `R_E0S_E1S`, epsilon `[0.005,0.01]`;
3. `R_E0S_E0S_E1S`, epsilon `[0.0025,0.005]`.

`process_state` is LIFO, so checkpoint 5498 must evaluate only
`R_E0S_E0S_E1S` first.

## Exact checkpoint-5498 contract

1. Hash-lock the checkpoint-5497 script, state, result, validation, source register, collapse audit and supersession audit.
2. Verify the source state is `179/3/0`, has zero unresolved nodes and has exactly the pending paths listed above.
3. Reconstruct the unchanged `v52 -> v53 -> v54 -> v55 -> v56 -> v57` chain from its original sources.
4. Reconstruct parent v58 only from the checkpoint-5496 binding and aggregate certificate; its application remains restricted to that exact binding.
5. Run `process_state` with `--max-node-evaluations 1`, BelowNormal priority and one-core affinity.
6. Require node-evaluation count to increase by exactly one and require the consumed path to be `R_E0S_E0S_E1S`.
7. If the node passes, add exactly one accepted row. If it fails, preserve the exact failure witness and add only the source-aligned children chosen by the inherited splitter.
8. Preserve all pre-existing accepted, pending, unresolved, witness and audit values exactly; append only the one-node consequences.
9. Record parent-v58 application rows. The count should remain zero unless the exact checkpoint-5496 binding is encountered.
10. Stop after this single atomic node and validate the complete frontier partition before any second node.

## Immutable checkpoint-5497 evidence

- Runner: `scripts/Y5_R2FR_5497_D4_parent_v58_hash_locked_frontier_migration.py`
- Migrated state: `source-intake/functional_rg/5497/work-v1/E07__U051__RIGHT_CONNECTOR__CUBOID__6df3d70a73e4618b.json`
- Result: `source-intake/functional_rg/5497/D4_parent_v58_hash_locked_frontier_migration_result.json`
- Validation: `source-intake/functional_rg/5497/P8_Y5_BRR5496_5497_VALIDATION.csv`
- Source register: `source-intake/functional_rg/5497/source_register.csv`
- Collapse audit: `source-intake/functional_rg/5497/D4_parent_v58_frontier_collapse_audit.csv`
- Supersession audit: `source-intake/functional_rg/5497/D4_parent_v58_witness_supersession_audit.csv`
- Runner SHA-256: `288bea08b37f0a55512655549f214e0aae3364052ad8848ab06c960177bb9dda`
- State SHA-256: `0bb34051ffe2e603d6429fd2a6aab76b285633f2a81db0e63787f2c73024a69f`
- Result SHA-256: `dec831e177792de709bc7682fff29b5493a5b2455ffdc1e2cd265150c77efa50`
- Validation SHA-256: `86a473b6543f518170ca9a3e537f5edbce71e6fbca16f36b555f5e2bcef429bf`
- Source-register SHA-256: `a42d5fa53c71e17d58bc53a01c9aaaeb7880fce9582d89365c3c956160887189`
- Collapse-audit SHA-256: `9163b5d04a42dffefbde65514b305d28f27f88468428af256cdb911adf6579a4`
- Supersession-audit SHA-256: `46437fda565489290015561880c3dd8695f85dc06653884bcc7460182b3cdfa0`

## Claim boundary

Checkpoint 5497 certifies one status-only frontier migration. It does not
certify the complete active cuboid, full outer enclosure, event-local or
combined `W3`, the regulator limit, all-operator local GR or full MTS.
