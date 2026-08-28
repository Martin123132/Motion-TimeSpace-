# 5386 — Y5/R2FR D4 nested-contour integrand enclosure

## Decision

`NESTED_CONTOUR_INTEGRAND_ENCLOSURE_CERTIFIED__PROCEED_TO_H3`

## Certified matrix

- contour cells: `2560`;
- complex regulator boxes: `80`;
- energy arcs per box: `32`;
- global enclosure arcs per energy arc: `1`;
- maximum numerator enclosure: `8.982482669999506e+17`;
- maximum event-integrand enclosure: `1271252622878497.8`;
- minimum recorded denominator clearance: `7.016408118911177e-10`;
- minimum collision-Jacobian clearance: `3.063529237166998`.

| event | rows | max integrand | min denominator | min Jacobian |
|---|---:|---:|---:|---:|
| E01 | 320 | 27295749.327946216 | 1.9192782971745513e-07 | 3.063529237166998 |
| E02 | 320 | 599306.5888342339 | 9.16096894377477e-06 | 16.297399494288086 |
| E03 | 320 | 27704.596915183232 | 1.1391056252334927e-06 | 20.669953575756097 |
| E04 | 320 | 19746246547822.324 | 2.068059898448133e-07 | 101.90243283009274 |
| E05 | 320 | 1271252622878497.8 | 7.016408118911177e-10 | 317.2579005068551 |
| E06 | 320 | 180644.326296988 | 9.41763251448768e-07 | 302.8935104597954 |
| E07 | 320 | 113291037.51625088 | 9.832275458701424e-07 | 82.35201718237047 |
| E08 | 320 | 468439.3706937941 | 1.6269191604001145e-07 | 6.199589212334397 |

## Exact chart repair

The branch-death hard leg uses its exact energy-channel diagonal p1(active) = -DeltaE Q/2. The soft leg is put in a rational light-cone chart. The right cut spinors are i times the left spinors, so their bispinors are exactly the negated cut momenta.

Edges that retain a default square-root spinor are transformed by the exact little-group factor. For the representative chart a1 = i p1_perp-minus/sqrt(-p1-plus); for the reciprocal chart a1 = i p1_perp-plus/sqrt(-p1-minus). The reciprocal first-soft square edge is desingularized by the algebraic identity -(1+q). No chart-only zero is treated as a physical pole.

The collision Jacobian is enclosed by a centered mixed-derivative mean-value formula along the recoil path. Every final row also contains the independently evaluated parent point inside the nested complex interval.

## Scope

This certificate establishes a finite enclosure of the H-sector nested-contour integrand on the stated complex regulator neighborhood. It does not by itself establish H3, G3, W3, the complete uniform remainder, the D4 outer limit, local GR, or full MTS.
