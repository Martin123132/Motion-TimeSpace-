# 5390 — D4 reserved-outer C0 contour enclosure

## Decision

`RESERVED_OUTER_C0_CONTOUR_ENCLOSURE_CERTIFIED__APPLY_FULL_H_BRIDGE`

## Certified matrix

- contour cells: `2560`;
- complex regulator boxes: `80`;
- state-box contraction limit: `0`;
- maximum unscaled C0 integrand enclosure: `1325246748428576.5`;
- minimum denominator clearance: `6.982462293235754e-10`;
- minimum collision-Jacobian clearance: `3.063527605883027`.

| event | rows | max C0 integrand | min denominator | min Jacobian |
|---|---:|---:|---:|---:|
| E01 | 320 | 33516855.497868977 | 1.7492170100547076e-07 | 3.063527605883027 |
| E02 | 320 | 599384.2127796909 | 9.160955778503402e-06 | 16.297397109417552 |
| E03 | 320 | 27941.75323174513 | 1.1372904514317247e-06 | 20.669625034210497 |
| E04 | 320 | 19772135086809.094 | 2.0678083125030056e-07 | 101.89852227332071 |
| E05 | 320 | 1325246748428576.5 | 6.982462293235754e-10 | 317.25745745498307 |
| E06 | 320 | 181077.48945821123 | 9.416980073336606e-07 | 302.8674255212827 |
| E07 | 320 | 114196532.89391972 | 9.829570250810306e-07 | 82.30414465249034 |
| E08 | 320 | 490773.8583503669 | 1.6080421196561966e-07 | 6.1994096599815505 |

## Why this second enclosure exists

Checkpoint 5386 contracts each certified event box for a tight C0 bound. That is useful for C0 itself but consumes the strict Krawczyk margin needed for a soft-coordinate Cauchy disk. This run deliberately evaluates the identical contour formula on the uncontracted, already-certified 5380 image. Its first additional strict Krawczyk image is held in reserve by checkpoint 5389.

Every row records contraction limit zero and exactly one sentinel call that stops before the first additional contraction. The independent parent-code witness is evaluated at the physical event-center solution, not at the generally off-shell midpoint of the broad outer state box. Every such physical witness lies inside its input box and its parent value lies inside the nested interval enclosure; all contour denominators remain separated from zero.

This witness choice is substantive: a preliminary run rejected ten `E01` endpoint-halo arcs because the uncontracted box midpoint does not satisfy the event equations. Re-evaluating those same arcs at the enclosed physical center made all ten pass without changing any contour interval, denominator clearance, or C0 upper bound. The failed preliminary run is retained under `runs/` as an audit artifact and is not a claim source.

## Scope

This certifies the reserved-outer C0 enclosure required by the 5389 coordinate-Cauchy bridge. It does not alone claim full H, H3, the total uniform remainder, the D4 outer limit, local GR, or full MTS.
