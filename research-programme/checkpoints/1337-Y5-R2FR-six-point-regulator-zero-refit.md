# 5321 - Six-point regulator-zero refit

## Method

The validated E00125 value is appended to the five-point ladder.  The refit
retains every normal-form family derived in 5319, including both quadratic
and quadratic-logarithmic remainder stresses.  Conservative complex input
disks, leave-one-out shifts, small-epsilon windows, weighting changes, family
spread, and adjacent Richardson shifts remain in the error envelope.

## Result

- reference zero intercept: `104.543539399` `-19.847801864 i`;
- leading-family relative bound: `0.00615334286899`;
- complete-remainder relative bound: `0.0102967282605`;
- acceptance limit: `0.01`;
- decision: **SIX_POINT_LIMIT_STABLE__ADD_E000625_TO_CLOSE_REMAINDER_ENVELOPE**;
- validation: **PASS**.

## Claim boundary

No remainder family is removed to force acceptance.  If the complete envelope
still misses one percent, E000625 is computed directly.  Decay-angle and all
broader field-theory claims remain false here.
