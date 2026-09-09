# 5504: D4 parent-v58 low-t child live resume handoff

**COMPLETED:** checkpoint 5504 committed one accepted leaf and passed all
`16/16` validation gates. The frozen continuation is
`5504-Y5-R2FR-D4-parent-v58-low-t-child-resume-handoff.md`; this file is
retained only as the audit trail of the live run.

## Run state

- Started: `2026-09-02`.
- Runner: `scripts/Y5_R2FR_5504_D4_parent_v58_low_t_child_gate.py`.
- Unified execution session: `86408`.
- Numerical worker at last audit: PID `24700`, BelowNormal, affinity mask `1` (one logical core), approximately `978 MB` RAM.
- Launcher shim at last audit: PID `26316`; it is not a second numerical worker.
- Evaluated target: `R_E0S_E0S_E1S_X0S_X1S_T0S`.
- Source state at launch: checkpoint 5503, frontier `182/5/0`, witnesses `64`.
- Source hashes, pending order, parent-v58 revision and exact partition all passed the dry-run.

At `2026-09-02T18:20:53Z` the calculation remained active. The output state's
`checkpoint_5504.records` list was still empty, so no numerical result had been
committed. This is expected evaluate-before-commit behavior: interruption
cannot partially alter the inherited frontier.

## Continuation audit

The next goal continuation recovered the same execution session rather than
starting a duplicate. At the latest audit the numerical worker had accumulated
approximately `4397` CPU-seconds, remained BelowNormal with affinity mask `1`,
used approximately `979 MB` RAM and still had zero committed checkpoint-5504
records. The adjacent checkpoint-5501 leaf had effectively identical x/t
widths and required about `16175` CPU-seconds, so a roughly four-and-a-half-hour
total runtime is a reasonable scheduling estimate rather than evidence of a
stall.

## Resume protocol

1. Poll unified execution session `86408` before launching anything else.
2. If that session is unavailable, inspect
   `source-intake/functional_rg/5504/status.json` and
   `source-intake/functional_rg/5504/work-v1/E07__U051__RIGHT_CONNECTOR__CUBOID__6df3d70a73e4618b.json`.
3. Do not launch a duplicate while a matching Python process is active.
4. If `checkpoint_5504.records` contains one row, rerun the same command only
   to regenerate and validate reports; the expensive node will replay rather
   than be recomputed.
5. If the process stopped with zero records, the source frontier is unchanged
   and the same atomic command is safe to restart.

## Command

`./.venv-score/Scripts/python.exe -B scripts/Y5_R2FR_5504_D4_parent_v58_low_t_child_gate.py`

## Parallel analytic progress

`D4-general-proof-carrying-adaptive-cover-theorem-draft.md` now derives the
finite-cover soundness theorem and strict no-smuggling contract for replacing
location-specific stable-edge repairs with a general proof-carrying recursive
evaluator. It is a draft integration target, not an active parent revision.
After checkpoint 5504 commits, use its actual child evidence to test the theorem
against the failed checkpoint-5503 broad sibling and an exact untriggered
control.

## Claim boundary

No checkpoint-5504 result exists yet. Checkpoint 5503 remains the latest frozen
certificate, and all active-cuboid, full-outer, event-local/combined `W3`,
regulator-limit, all-operator local-GR and full-MTS claims remain false.
