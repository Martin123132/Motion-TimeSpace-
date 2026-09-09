# 5501 live parent-v58 high-x sibling run handoff

## Last certified state

- Checkpoint 5500 is complete at frontier `180/6/0`.
- Its state SHA-256 is `b916d268ac3c6466c46b53d9fa597feab86ae37d8d8584731c6c3fd248d05e8e`.
- The low-x child passes with collision-Jacobian lower `0.459458903598766`.
- All checkpoint-5500 validation and source-register rows pass.

## Live calculation

- Runner: `scripts/Y5_R2FR_5501_D4_parent_v58_high_x_sibling_gate.py`.
- Target: `R_E0S_E0S_E1S_X0S_X0S_T0S_X1S`.
- Started: `2026-09-02 12:43:25 Europe/London`.
- Unified execution session: `52784`.
- Numerical process observed: PID `25804`.
- Resource policy: one MTS numerical worker, one core, BelowNormal priority.
- At the four-hour check-in boundary the process remained active and the checkpoint-5501 record count remained zero.

The runner evaluates before committing. Therefore the authoritative frontier is
still checkpoint 5500 until checkpoint 5501 writes one record, validation,
result and status files. Do not launch a duplicate 5501 process while PID
`25804` or the matching command line remains active.

## Resume rule

On the next continuation, poll session `52784` first. If the process has ended,
inspect `source-intake/functional_rg/5501/status.json` and the checkpoint-5501
state before running anything. If no output record exists and the process is no
longer active, the atomic evaluation was not committed and can be restarted
from checkpoint 5500 without frontier corruption.

## Completed status

The process completed successfully after `16175.45627720002` seconds. The
high-x sibling is accepted, the exact low-t X2 parent union is certified, and
the frontier is `181/5/0`. This live note is superseded by
`5501-Y5-R2FR-D4-parent-v58-high-x-sibling-resume-handoff.md`; do not poll or
restart session `52784`.
