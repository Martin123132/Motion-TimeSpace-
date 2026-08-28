# 5391 — D4 uniform full-H3 Cauchy bound

## Decision

`UNIFORM_FULL_H3_CAUCHY_BOUND_CERTIFIED__PROCEED_TO_G3_AND_W3`

## Bound

- regulator-plane Cauchy radius: `5e-07`;
- minimum soft-coordinate Cauchy radius: `5.632403328656322e-14`;
- minimum regulator-bin seam inclusion margin: `5.738271367602491e-16`;
- uniform full-H3 upper bound: `7.128414567646749e+31`;
- H-sector Taylor constant H3/6: `1.1880690946077915e+31`.

## Event bounds

| event | sup C0 | sup C1 | sup |z0/z1| | sup full H | sup full H''' |
|---|---:|---:|---:|---:|---:|
| E01 | 41849.9474458187 | 1.57413369523313e+16 | 6.476808095256517e-05 | 27280117.990858994 | 1.3094456635612327e+27 |
| E02 | 4078.1110457100735 | 1.032898358454382e+16 | 1.9779459756758646e-05 | 2020488.8570742265 | 9.698346513956295e+25 |
| E03 | 192.58073406695567 | 55237837528742.23 | 1.3801090881069789e-05 | 5260.581139354042 | 2.525078946889942e+23 |
| E04 | 22107400876.782364 | 2.516143433659645e+23 | 8.072928968937656e-07 | 81991296918.43433 | 3.935582252084851e+30 |
| E05 | 457347238562.54205 | 8.097219496391146e+24 | 6.580593755301841e-07 | 1403065352928.5657 | 6.734713694057121e+31 |
| E06 | 363.44868827474534 | 2528409893286690.0 | 5.65194666159832e-07 | 403.8441680705093 | 1.938452006738446e+22 |
| E07 | 199600.88318663812 | 7.79122509857118e+17 | 8.004059626483917e-07 | 249572.46282793765 | 1.1979478215741018e+25 |
| E08 | 3299.361550236294 | 330459176887129.94 | 3.136713268087748e-05 | 162569.00195752946 | 7.803312093961421e+24 |

## Derivation

The reserved-outer contour sweep bounds the physical direct double-pole coefficient `C0` on every state box. Checkpoint 5388 proves that the subtraction has no double-pole coefficient. Checkpoint 5389 places a complex soft-coordinate disk of radius `rho_x` around every event branch while keeping every dependent component `(u,v,H,S)` inside that same state box, and separately patches all regulator-bin seams. Cauchy's estimate therefore gives `|C1| <= sup|C0|/rho_x` without importing a fitted finite difference.

The exact parent affine endpoint coefficient is bounded boxwise by `|H| <= |C0||r| + |C1||r|^2/2`, with `r=z0/z1`. The 5380 strip and 5387 endpoint halos cover every regulator-plane disk of radius `rho_e` centered on `[0,0.02]`, so `sup|H'''| <= 3! sup|H|/rho_e^3`. The eight event bounds are then summed.

## Scope

This is deliberately an existence-grade enclosure and may be numerically loose. It closes only the H-sector derivative owner. G3 and mapped-away W3 remain required before the total uniform remainder and D4 outer limit can be claimed. Local GR and full MTS claims remain false.
