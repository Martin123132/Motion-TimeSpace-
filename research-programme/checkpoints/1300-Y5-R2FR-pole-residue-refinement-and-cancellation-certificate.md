# 5284 — Pole-residue refinement and cancellation certificate

## Purpose

The 5283 energy sequence converged only after subtracting MC04 and MC12,
but the physical answer is a cancellation of much larger component
terms. This checkpoint therefore replaces a single direct Laurent fit
with a radius-refined numerator fit,

`N(E) = (E - E_p) F(E)`,

evaluates the fitted polynomial at the complex pole, and propagates the
last two radii and degrees 2–4 through the order-16 physical integral.

## Result

- order 16: `-2.23128837586+2.12593752908i`
- order 4: `-2.23236172099+2.13170269362i`
- order 8: `-2.23277361524+2.13090438313i`

- maximum selected fit residual:
  `3.82624561028e-05`;
- maximum radius-refinement change:
  `8.63129350351e-05`;
- maximum polynomial-degree change:
  `6.1174379102e-05`;
- order-16 cancellation condition number:
  `912.907477168`;
- maximum 1,296-member residue-ensemble shift:
  `0.00332052338173`;
- parent-to-refined order-16 shift:
  `0.00129491855715`;
- order 8 to 16 quadrature change:
  `0.00167966578823`;
- residue certificate:
  `False`.

Decision:
`REFINEMENT_COMPLETED_BUT_RESIDUE_CERTIFICATE_OPEN__DERIVE_CHANNEL_DERIVATIVE_RESIDUES`.

Validation: **PASS**.

## Claim boundary

Passing this checkpoint authorizes construction of the chamber-adapted
angular runner only. It is not a full phase-space coefficient, UV,
local-GR, or full-MTS claim.
