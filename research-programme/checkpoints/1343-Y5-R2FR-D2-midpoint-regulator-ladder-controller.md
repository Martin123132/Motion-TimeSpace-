# 5327 - D2 midpoint regulator ladder controller

## Method

Each regulator value receives isolated event caches, shards, pole fits,
adaptive panels, and validation. The seven E0025 support events are used
only as candidate topology; every target epsilon must re-solve all event
coordinates and pass its own topology, inner, outer, and source gates.
Reciprocal algebraic candidates are repaired only when the inherited pair
residual is anomalous; both collision equations and the reciprocal-product
identity must then pass explicit residual gates, with every repair audited.
For every regulator, candidate detection extends to 32 imaginary-core widths
without relaxing any fit gate. Outside-support poles retain one-sided active-
support subtraction; inside-support poles use symmetric pole-centred Laurent samples
whose full stencil stays inside one support branch. Fit residual, residue-scale
stability, second-order suppression, and masked identity limits are unchanged.
If the common two-scale stencil crosses an internal selector orbit, its radius
is halved until a dense linear-plus-geometric guard is branch-pure; the radius
may not shrink below one imaginary pole core and no acceptance limit is relaxed.
The isolated E020 slow-energy nodes extend the inherited 64/128 partition
ladder to independently audited 256/512 subdivisions, retaining the same
Q4/Q8 and conservative error-budget gates. An outside-support pole whose
strict residue fit fails is never subtracted: because it remains off the real
contour, its failed fit is retained and direct real-contour refinement is used.

## State

- validated finite rows: `7/7`;
- missing rows: `none`;
- decision: **D2_SEVEN_POINT_FINITE_REGULATOR_LADDER_COMPLETE__FIT_ZERO_LIMIT**.
- maximum adjacent regulator change: `9.098333e-03`;
- maximum difference/error-envelope ratio: `1.962154e+00`;
- preliminary three-point trends: `5`; resolved above error: `1`;
- audited algebraic-selector repairs: `560`;
- synthetic regulator-inventory audit rows: `42`;
- maximum corrected collision residual: `2.647703e-73`;
- maximum corrected reciprocal-pair residual: `7.907045e-81`.

## Claim boundary

The E00125 and E000625 inventories extend the parent 5303 construction
only by the exact target `-9+i epsilon`; they retain the parent E020
component map byte-for-byte and do not assert a regulator-zero result.

No regulator-zero or decay-angle claim is made by the controller. A
zero-limit fit is allowed only after all seven finite rows validate.
