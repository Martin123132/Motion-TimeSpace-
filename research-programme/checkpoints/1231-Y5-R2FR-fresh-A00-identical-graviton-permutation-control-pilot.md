# 5215 - Fresh A00 identical-graviton permutation-control pilot

## Decision

`FROZEN_AWAITING_EXECUTION`

This checkpoint executes the fresh experiment authorized by checkpoint 5214.
It does not select a friendlier source family, refit the control coefficient,
or change the acceptance thresholds after observing outcomes.

## Frozen estimator

The exact identical-graviton identity is

`C_13 = Y[g1+,g3-] - (w1/w3)Y[g1-,g3+]`,

with

`w1/w3 = (E3/E1)^2`

inserted independently at each reciprocal root before winding-weighted
residue summation. The real control coefficient is exactly `1`; the
imaginary coefficient is exactly `0`.

The physical `A00` row uses the frozen extrapolation

`A00(0) = 2 A00(E020) - A00(E040)`

and the fixed `z=-0.6` weight `-0.008`.

## Locked experiment

The protocol is frozen before outcomes. It contains twelve fresh independent
topological events, two epsilon values and only the `A00` crossed argument:
`12 x 2 x 1 = 24` jobs. No checkpoint-5215 topology or residue value existed
when the lock was written.

Execution has not yet started.

## Frozen acceptance rule

Scaling is authorized only when all 24 jobs converge, every structural gate
passes, the absolute control mean is at most two standard errors, at least two
events carry a nonzero control under the frozen tolerance, and

`SD(controlled A00 real) / SD(raw A00 real) < 0.5`.

The bootstrap interval and exact sign-flip result are diagnostics only.

## Claim boundary

This pilot tests estimator bias and efficiency. It does not establish a
canonical two-loop coefficient. Numeric UV, all-operator local GR and full
MTS flags remain false. The exact checkpoint-5211 two-derivative
GR+Lambda+SM+Maxwell branch is unchanged.

## Machine-readable evidence

- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\functional_rg\5215\frozen_A00_control_pilot_manifest.json`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\functional_rg\5215\frozen_A00_control_pilot_lock.json`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\functional_rg\5215\fresh_A00_control_pilot_activation.json`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\functional_rg\5215\frozen_A00_control_pilot_config.json`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\functional_rg\5215\frozen_A00_control_pilot_schedule.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\functional_rg\5215\fresh_A00_control_pilot_event_rows.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\functional_rg\5215\fresh_A00_control_pilot_pair_rows.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\functional_rg\5215\fresh_A00_control_pilot_results.json`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_5215_VALIDATION.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\functional_rg\5215\PROVENANCE.md`
