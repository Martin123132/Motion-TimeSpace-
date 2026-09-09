# 5427: representative external01 square half-plane gate

## Decision

**PASS FOR THE REPRESENTATIVE-CHART `(0,1)` SQUARE EDGE ONLY.**

The v44 production failure is not the reciprocal external pole already treated by the path-integrated decomposition. It occurs only in the representative chart and chirality one. In the surviving external-minus / hard-plus rational charts, the exact edge is

`[01] = T p1_bar / ((1-target) p1_plus) - 1`.

After multiplying the hard lightcone terms by the parent representative coordinate, this becomes the explicit Laurent-free polynomial quotient implemented by the 5427 gate.

## Evidence

All `108` direct spinor checks agree within `1.1095104078178292e-16`. A closed adaptive cover of the recorded failure region uses `7424` leaves and places their common hull strictly in the negative-real half-plane with margin `0.078739978004953012`.

## Consequence

The representative branch does not require a pole integral on this recorded region. It requires an exact square-edge override, dual to the existing reciprocal angle-edge override. The next implementation may add that override and rerun the same historical failure boxes.

## Claim boundary

No connector, W3, regulator, UV, local-GR, or full-MTS claim follows from this chart-local edge proof.
