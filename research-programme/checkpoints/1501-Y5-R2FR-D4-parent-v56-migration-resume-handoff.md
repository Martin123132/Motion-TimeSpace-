# 5485: D4 parent-v56 migration resume handoff

Checkpoint 5483 promotes the checkpoint-5481 collision-Jacobian candidate to a complete parent-amplitude certificate. The unchanged parent-v55 evaluator reproduces the largest checkpoint-5480 failure. Parent v56 then applies the exact `16 x 128` x/t Jacobian leaf union only after the connector collision-Jacobian lower bound remains zero.

## Certified parent-v56 result

- Parent-v55 target failure reproduced: `true`.
- Complete parent-v56 target passed: `true`.
- V56 trigger rows: `3/3` positive.
- Minimum v56 Jacobian leaf-union lower: `218.56599306552303`.
- Minimum v56 chart-denominator lower: `6.353850106517455e-05`.
- Exact-cover error: `0.0`.
- Complete target amplitude-denominator lower: `3.1452925082799366e-08`.
- Complete target collision-Jacobian lower: `0.15648926122657356`.
- Untriggered parent-v55/v56 control: exactly unchanged.
- Checkpoint-5483 validations: `11/11` passed.

The action, contour, configurations, residues and numerical acceptance thresholds are unchanged. Parent v56 changes only interval-image composition under an exact finite cover.

## Migrated frontier

Checkpoint 5484 provides the resumable parent-v56 frontier and completes its status-only migration.

- State: `source-intake/functional_rg/5484/work-v1/E07__U051__RIGHT_CONNECTOR__CUBOID__6df3d70a73e4618b.json`.
- SHA-256: `6e30e31edaac0d93160df2bffe7864bae7f4f3677442d41a82c2556a906a8d73`.
- Accepted/pending/unresolved: `168/10/0`.
- Total inherited node evaluations: `219`.
- Refinement witnesses: `51`.
- Parent-v56 evaluations after migration: `0`.
- Checkpoint-5484 validations: `11/11` passed.

## Exact next calculation

Resume checkpoint 5484 with one atomic node only:

`./.venv-score/Scripts/python.exe -B ./scripts/Y5_R2FR_5484_D4_parent_v56_hash_locked_frontier_runner.py --max-node-evaluations 1 --max-runtime-seconds 900 --maximum-refinement-depth 33`

The runtime cap is checked between nodes, not inside an expensive complete-amplitude node. Keep the process BelowNormal and restricted to one core. If the node passes, preserve it and resume one node at a time; if it fails, derive the new local obstruction before adding another fallback or increasing depth.

Full active-cuboid, full outer, event-local/combined `W3`, regulator-limit, all-operator local-GR and full-MTS claims remain false. No GitHub action and no `formalization-workbench` edit belongs to this checkpoint.

**PARENT_V56_FULL_GATE_CERTIFIED__HASH_LOCKED_FRONTIER_READY**
