# 5385 — Y5/R2FR D4 expanded energy contour and full pole-catalog clearance

## Result

Decision: `D4_EXPANDED_ENERGY_CONTOUR_FULL_POLE_CATALOG_CLEARANCE_CERTIFIED__ENCLOSE_FACTORIZED_FINITE_PLUS_NUMERATOR`.

The parent-energy Cauchy radius is expanded from `1e-6` to `1e-5`. The resulting double-Cauchy residues agree with checkpoint 5383, while the complete 20-root amplitude catalog is checked on the expanded contour: 12 direct roots (`g1,g2,g3`) and 8 subtraction roots (`soft,decay`). The selected collision owns three coincident catalog entries, leaving 17 nonactive roots to exclude.

- certified event/epsilon boxes: `64/64`;
- certified energy arcs: `2048/2048`;
- nonactive full-catalog checks: `34816`;
- minimum certified full-catalog separation: `6.84606889024063e-05`;
- maximum inner contour radius: `4.022309798781511e-07`;
- minimum full-catalog clearance margin: `6.813818051873083e-05`;
- maximum expanded-versus-5383 numerical C0 difference: `2.3969316412661483e-19`.

## Nearby g2 pole

At the four branch-death events, the nearest nonactive root is a `g2` root only about `8e-5` from the selected center. Direct rectangular subtraction loses that gap. The certificate therefore uses a centered complex mean-value bound at zero energy displacement and a 32-piece interval line integral in recoil space for the expanded energy contour. This treats the nearby pole as real geometry rather than numerical noise.

## Scope

This closes full pole-catalog isolation on a numerically crosschecked outer contour. It does not yet interval-enclose the finite-plus spinor numerator or prove that no separate energy-plane singularity lies inside the outer contour. Endpoint C, H3, the uniform remainder, the D4 outer limit, local GR, and the full MTS claim remain open.
