# 5451: D4 event-endpoint x-t overlap geometry cover

## Decision

**FINITE_ENDPOINT_XT_OVERLAP_GEOMETRY_ATLAS_CERTIFIED__EVALUATE_INNER_Q_THEN_OUTER_PARENT**

## Construction

Every singular event-term cell, every one of the ten complex regulator boxes and all three straight contour segments were partitioned in `(x,t)`. A leaf is assigned to the inner Cauchy owner when `sup|E-p|<=7.5e-6`, and to the existing parent triangle owner when `inf|E-p|>=5e-6`. Only boxes crossing both thresholds are subdivided. The positive overlap makes this a finite covering problem rather than a demand to locate the artificial switching circle exactly.

| event | jobs | leaves | inner | outer | unresolved | max depth |
|---|---:|---:|---:|---:|---:|---:|
| `E01` | 184 | 33455 | 333 | 33122 | 0 | 9 |
| `E02` | 401 | 105565 | 8139 | 97426 | 0 | 7 |
| `E03` | 309 | 80751 | 6538 | 74213 | 0 | 9 |
| `E04` | 401 | 56814 | 4644 | 52170 | 0 | 2 |
| `E05` | 309 | 36672 | 4644 | 32028 | 0 | 2 |
| `E06` | 309 | 62411 | 4645 | 57766 | 0 | 2 |
| `E07` | 401 | 78483 | 4644 | 73839 | 0 | 2 |
| `E08` | 657 | 217571 | 31145 | 186426 | 0 | 16 |

The binary leaf areas reconstruct every source rectangle. Inner leaves now have an exact finite formula but still need their correlated `Q` circle evaluated on the full leaf `x` interval. Outer leaves have a strict positive pole gap but still need the unchanged parent amplitude enclosure run on those leaves.

## Primitive split

At `t=0`, outer connector leaves also give a finite candidate bound for the nonsingular logarithm using `|Log z|<=hypot(max(|log m|,|log M|),pi)`. Leaves touching the principal endpoint remain owned by the already-derived `H log + G` primitive. Candidate numbers are not promoted because the event-tube residue must first be enclosed on the same correlated `x` leaves.

## Claim boundary

This is a complete geometric atlas, not yet a complete amplitude atlas. Full event-cell finite cover, event-local `W3`, combined `W3`, the D4 regulator limit, all-operator local GR and full MTS remain false. The next runner evaluates the inner `Q` contours first, then the outer parent leaves, without changing this partition.
