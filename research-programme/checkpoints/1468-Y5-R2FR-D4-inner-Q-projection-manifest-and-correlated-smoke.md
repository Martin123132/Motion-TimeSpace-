# 5452: D4 inner-Q projection manifest and correlated smoke

## Decision

**INNER_Q_PROJECTION_COMPRESSION_CERTIFIED__EIGHT_EVENT_CORRELATED_SMOKE_PASSES__RUN_FULL_RESUME_SAFE_COVER**

## Exact reduction

The inner Cauchy bound depends on `(x,epsilon)` and the fixed `|delta|=1e-5` circle, not on the connector/top path parameter `t`. The 64,732 inner geometry leaves can therefore be projected and merged before the expensive parent amplitude call. The projection is lossless because every source leaf retains its full epsilon box and the union of its x interval.

The complete 5451 atlas reduces to `2074` inner `x×epsilon` jobs across `2074` epsilon groups. Maximum connected x components per group is `1`.

## Correlated smoke

One widest projection per event was sent through all 32 exact 5450 parent `Q` arcs. A node that failed an interval chart was bisected only in `x`; every accepted x leaf then had to pass all 32 arcs. Passed projections: `8/8` across `83` accepted x leaves.

## Claim boundary

This checkpoint validates the compression and a cross-event transplant of the exact parent contour. It does not yet evaluate all projection jobs. Full correlated inner-Q coverage, the outer parent amplitude atlas, event-local W3, combined W3, the D4 regulator limit, all-operator local GR and full MTS remain unclaimed.
