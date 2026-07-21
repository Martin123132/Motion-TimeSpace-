# 5134 - argument-local outer-collinear preflight and A14 replay

## Result

Checkpoint 5127's pole equations are event-level laws, while proximity to an
integration chamber is argument-local geometry. The locked
`A14` preflight therefore derives the roots first and activates
no chart unless the target contour enters its isolation disk. The resulting
selection is `chamber 0: 0, chamber 1: 4`. No numerical outcome was used to select it.

The exact locked job `E040__S512503_N0000__A14__primary24` ends as `COMPLETED_CONVERGED`. It uses
`49` composite intervals and reaches maximum
adaptive relative error `2.5344072795132247e-05`
against the unchanged `5e-5` tolerance. The causally corrected value is
`(-1690.4795379392626+2447.6395440391343j)`.

The chart was called `864` times
inside `1836` target-profile evaluations.
Its low/high boundary levels are
`24/32/48`
and
`32/48/64`;
the acceptance threshold was not changed.
The durable pilot count is
`50/560` converged,
`0` unconverged,
`0` failed and
`510` missing.

## Cog interpretation

This is the numerical analogue of the machine/cog requirement: one derived
pole law is retained, but the contour geometry decides whether it is active.
There is no hand-set argument switch and no tolerance retuning. This does not
yet establish the physical MTS transition between local GR and galaxies; it
does establish the required discipline in the coefficient pipeline.

## Discipline

- Validation failures: `[]`.
- Full-pilot continuation remains unauthorized.
- No principal value or half residue was inserted.
- The protected formalization tree remains `b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758`.
- No UV coefficient, local-GR, galaxy, or full-MTS claim follows.
- No GitHub action occurred.

## Next

Run the next untouched argument only after applying this preflight to its
transported contour. Do not infer that all later arguments share
`A14`'s active
chamber and do not bulk-resume the schedule.
