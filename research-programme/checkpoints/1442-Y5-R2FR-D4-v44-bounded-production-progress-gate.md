# 5426: v44 bounded production progress gate

## Decision

**PASS FOR COMMITTED V44 PRODUCTION PROGRESS ONLY.**

The first bounded resume after the exact `(1,3)` repair commits `10` additional interval boxes. Accepted coverage rises from `8.21151733398436%` to `8.23516845703123%`.

## Obstruction transfer

The repaired `(1,3)` failure count changes by `0`. The separate external `(0,1)` count changes by `10`. No new failure category appears. This is the production-level confirmation that v44 removes the intended obstruction rather than merely relabelling it.

## Saved frontier

The run is resume-safe with `354` accepted and `12` pending boxes. The next path is `LLDRDRDRDLDRDRDRD` at depth `17`.

## Claim boundary

The right connector remains incomplete. Regular-away W3, event-local W3, combined W3, regulator limit, UV, local-GR, and full-MTS claims remain false.
