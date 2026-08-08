# 3979 - GR Baseline Residual Projector Contract Or Source Profile Runner

Timestamp: `2026-07-01T16:47:41+00:00`

## Result

3979 turns the fair-comparison rule into an operator:

```text
P_residual(Q_lm) =
  P_claim
  P_l>=1
  P_same_source
  P_same_frame_units
  P_GR_baseline
  P_total_source
  [Q_lm_total - Q_lm_GR_baseline]
```

If all gates pass:

```text
Q_lm_residual = Q_lm_total - Q_lm_GR_baseline
epsilon_extra_MTS_l_ge_1 = |Q_lm_residual| / |M_H_ref|
```

## Dry-Run

Toy smoke rows were generated to prove operator behavior only:

```text
pass rows: 2
blocked rows: 3
routed l=0 rows: 1
```

The runner blocks missing GR baselines, frame/coframe mismatches, and missing EM/Poynting inclusion. It also routes `l=0` to the Newton/source-calibration branch instead of angular hair.

## Claim Status

No claim is made. These are toy rows, not evidence.

Real promotion requires non-toy source rows with:

```text
Q_lm_total, Q_lm_GR_baseline, M_H_ref,
same source/worldtube/frame/units/r_eval,
total-source inclusion,
Poynting included or bounded,
source path and units.
```

Next target:

```text
3980-Y5-R2FR-first-real-local-source-profile-row-or-parent-zero-certificate.md
```

Source needles found: `19/19`.
