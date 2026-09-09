# 5446: S_X007 TOP additional-progress and priority gate

## Decision

**THE ADDITIONAL S_X007/TOP RUN IS HEALTHY, BUT FULL ENUMERATION IS NOT YET THE PROVEN PRIORITY.**

One source-identical parent-v49 run added certified leaves without reaching a terminal enclosure obstruction. The state remains exactly resumable.

## Production delta

- Accepted leaves: `167` -> `201` (`+34`).
- Live stack: `5` -> `5`.
- Maximum live depth: `9` of `18`.
- New accepted minimum amplitude denominator: `0.0007850556481955788`.
- New accepted minimum collision Jacobian: `0.04443994350177131`.

## New edge label

`IntervalSingularity:away_arc_right_K5:s1:c1:left0:edge_3_3_4:stable_edge` occurred `2` times. It did not halt the run, remained below depth 18, and generated accepted children; it is not promoted to a parent obstruction.

## Priority consequence

The full parent run reports `31/240` completed path jobs. Before committing many additional machine-hours, the next checkpoint must inspect whether full D4 regular-away enumeration is on the critical dependency path for local GR, Newtonian recovery, Maxwell stress, and calibrated source coupling.

## Claim boundary

S_X007/TOP remains incomplete with five live entries. No regular-away W3, UV, local-GR, or full-MTS claim is made.
