# 5407 — Sixth-right and next-supports completion gate

## Purpose

Checkpoint 5407 tests whether the shallow frontier left by checkpoint 5406 completes the sixth-support right connector and whether production can cross subsequent support boundaries without another analytic closure.

## Result

- The sixth-support right connector completes at `382` certified boxes. Its parameter-area sum is `0.01767396674516035`, its minimum amplitude-denominator lower bound is `0.0003970550036330211`, and all five previously audited depth-fourteen paths remain present.
- Production then completes all three `S_X004_MC04_SM_DM` paths at `1`, `4`, and `1` boxes.
- It completes all three `S_X005_MC04_SM_DM` paths at `1`, `11`, and `2` boxes.
- It completes the `S_X006_MC04_SM_DM` left connector at `4` boxes and enters that support's top path.
- Overall production advances `17/240 -> 25/240` completed path jobs in one bounded run.
- The active X006 top path has `25` accepted and `4` pending boxes at maximum depth `6`. Accepted area is `0.025808695634851872`, exactly `65.625%` of its complete parameter rectangle when combined with the preserved pending area.

## Decision

The sixth right connector and seven subsequent path jobs close under the unchanged v40 proof. No new denominator mechanism or closure is required on this interval. Continue from the shallow X006 top frontier. Global univalence, regular-away `W3`, regulator removal, local GR, and full MTS remain open.

Machine-readable validation is stored in `source-intake/functional_rg/5407/P8_Y5_BRR5396_5407_VALIDATION.csv` and `source-intake/functional_rg/5407/sixth_right_and_next_supports_completion_gate_result.json`.
