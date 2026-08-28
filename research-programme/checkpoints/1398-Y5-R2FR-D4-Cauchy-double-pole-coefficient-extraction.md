# 5382 — Y5/R2FR D4 Cauchy double-pole coefficient extraction

## Result

Decision: `D4_CAUCHY_DOUBLE_POLE_COEFFICIENT_AND_ENERGY_RESIDUE_CROSSCHECK_CERTIFIED__INTERVALIZE_COEFFICIENT`.

The parent finite-plus double-pole coefficient is extracted as the Laurent coefficient

`K=(2 pi i)^(-1) integral F(zeta)(zeta-z) d zeta`,

implemented as the circular average of `F(z+r exp(i theta)) r^2 exp(2 i theta)`. This replaces the earlier single tiny displacement by a phase-complete contour projection.

- maximum angular/radius contour relative spread: `3.661204280677494e-67`;
- maximum Cauchy-versus-displacement relative difference: `5.035396888994336e-28`;
- maximum Cauchy-C0 versus checkpoint-5359 relative difference: `8.574120225679775e-20`.

## Scope

This is a high-precision independent numerical Laurent extraction and parent-energy-residue crosscheck. It is not yet an interval enclosure over the 5380 complex strip, so endpoint C, H3, the uniform remainder, the D4 outer limit, and broader claims remain false.
