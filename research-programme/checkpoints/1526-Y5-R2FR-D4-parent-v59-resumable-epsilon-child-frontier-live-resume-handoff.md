# 5510: D4 parent-v59 resumable epsilon-child frontier live resume handoff

**COMPLETED:** all eight atomic nodes are committed; the four accepted leaves
close three nested failed parents exactly and all `19/19` validation gates
pass. The frozen continuation is
`5510-Y5-R2FR-D4-parent-v59-resumable-epsilon-child-frontier-resume-handoff.md`;
this file is retained as the live-run audit trail.

## Run state

- Started: `2026-09-03T01:26:59Z` (`2026-09-03T02:26:59+01:00` local).
- Runner: `scripts/Y5_R2FR_5510_D4_parent_v59_resumable_epsilon_child_frontier.py`.
- Runner SHA-256: `078a00465877f7dd6c6de59faeb9706452eaee793939820cb7fbf1ba91a05e85`.
- Current command target: eight total atomic node evaluations with a `12600`-second between-node runtime budget.
- Current unified execution session: `51955`; session `79870` completed records five and six.
- Numerical worker at the latest check-in: PID `19164`, BelowNormal, affinity mask `1` (one logical core), approximately `981 MB` RAM.
- Launcher shim at the latest check-in: PID `28228`; it is not a second numerical worker.
- Source state: checkpoint 5509, frontier `185/3/0`, witnesses `65`.
- First target: `R_E0S_E1S_E0S`.

The strict dry-run passed all checkpoint-5509 hashes, exact pending order,
exact partition, parent-v59 revision, inherited 13-row v59 event ledger and two
scoped proof-cache bindings.

## Atomic progress

Five nodes are durably committed. The first four reproduce only the
collision-Jacobian interval zero and refine in the exact sequence x, x, t, x.
The fifth node,
`R_E0S_E1S_E0S_X0S_X0S_T0S_X0S`, is `ACCEPTED` after
`2937.27075460006` seconds. The committed frontier is now `186/6/0`, witnesses
remain `69`, and no node is unresolved.

At `2026-09-03T03:34:00Z`, the worker was evaluating matching high-x sibling
`R_E0S_E1S_E0S_X0S_X0S_T0S_X1S` as record six. The committed state SHA-256
was `44ed4a5bfda6b3c4232df36c76f97ca3436ccd4afe93a50a2e5932508e009ad5`.
The checkpoint-5510 result/validation reports still describe the four-record
safe point and must not be treated as final until the worker exits and
regenerates them.

## Continuation audit - record eight

Record six, matching high-x sibling
`R_E0S_E1S_E0S_X0S_X0S_T0S_X1S`, is also `ACCEPTED`. Record seven,
matching high-t node `R_E0S_E1S_E0S_X0S_X0S_T1S`, then passes directly.
These three leaves exactly replace the failed x/t parent in the frontier.

Seven nodes are now durably committed, the frontier is `188/4/0`, witnesses
remain `69`, and no node is unresolved. At `2026-09-03T07:39:33Z`, session
`51955` was evaluating record eight,
`R_E0S_E1S_E0S_X0S_X1S`. Its worker had accumulated approximately `5592`
CPU-seconds over `5795` wall-seconds and remained active on one BelowNormal
core. The seven-record state SHA-256 was
`96b335831ac4c3c45a9a25795b0c0ef028ad65c92e6e51470bb75aefe186c43a`.

## Resume protocol

1. Poll unified execution session `51955` before launching anything else.
2. If that session is unavailable, inspect the matching Python process and
   `source-intake/functional_rg/5510/work-v1/E07__U051__RIGHT_CONNECTOR__CUBOID__6df3d70a73e4618b.json`.
3. Do not launch a duplicate while a matching Python process is active.
4. If eight records exist, rerun the same command only to regenerate and
   validate reports; all eight expensive nodes replay from state.
5. If the process stopped with seven records, all seven remain atomic and the
   same command safely restarts only record eight.

## Command

`./.venv-score/Scripts/python.exe -B scripts/Y5_R2FR_5510_D4_parent_v59_resumable_epsilon_child_frontier.py --target-node-evaluations 8 --max-runtime-seconds 12600`

## Claim boundary

Checkpoint 5510 certifies the four-leaf low-x region and advances the frontier
to `189/3/0`. The complete low-epsilon parent, active cuboid, full outer cover,
event-local/combined `W3`, regulator limit, all-operator local GR and full MTS
remain unclaimed.
