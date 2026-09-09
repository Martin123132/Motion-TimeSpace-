# 5428: representative external01 ratio disk gate

## Decision

**PASS FOR THE RECORDED REPRESENTATIVE-CHART `(0,1)` EDGE REGION ONLY.**

Write the square edge as `[01] = R - 1`. At zero contour displacement, exact elimination of the representative coordinate gives the low-degree rational quotient `R0 = -A/(q B)`. For displacement `delta`, the only correction is `R = R0 z_sel/(z_sel + delta)`.

The symbolic numerator remainder modulo `S^2=1-x^2` and `U^2=1-d^2` is exactly zero. The pointwise implementation agrees with the independently spinor-checked 5427 expression to within `1.6413490917450851e-16`.

## Disk Certificate

A closed cover of the recorded failure union uses `1` leaves. Its common rectangular ratio hull obeys `|R| <= 0.78355814210605723 < 1`, so `[01]` has the rigorous reverse-triangle lower bound `0.21644185789394277`.

This removes the apparent zero without treating a chart artifact as a physical pole and is the candidate production fallback for representative-role, external-minus / hard-plus, chirality-one edges.

## Claim Boundary

No connector, W3, regulator, UV, local-GR, or full-MTS claim follows from this local chart certificate.
