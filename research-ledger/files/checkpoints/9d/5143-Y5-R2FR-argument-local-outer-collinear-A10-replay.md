# 5143 - argument-local outer-collinear preflight and A10 replay

## Result

Checkpoint 5127's pole equations are event-level laws, while proximity to an
integration chamber is argument-local geometry. The locked
`A10` preflight therefore derives the roots first and activates
no chart unless the target contour enters its isolation disk. The resulting
selection is `chamber 0: 0, chamber 1: 4`. No numerical outcome was used to select it.

The exact locked job `E020__S512503_N0000__A10__primary24` ends as `COMPLETED_CONVERGED`. It uses
`4122` composite intervals and reaches maximum
adaptive relative error `0.00021516344483054253`
against the unchanged `5e-5` tolerance. The causally corrected value is
`(2.7040729725056765-0.9216267316896317j)`.

The chart was called `720` times
inside `294372` target-profile evaluations.
Its low/high boundary levels are
`96/128/192`
and
`128/192/256`;
the acceptance threshold was not changed.
The durable pilot count is
`52/560` converged,
`0` unconverged,
`0` failed and
`508` missing.

## Cog interpretation

This is the numerical analogue of the machine/cog requirement: one derived
pole law is retained, but the contour geometry decides whether it is active.
There is no hand-set argument switch and no tolerance retuning. This does not
yet establish the physical MTS transition between local GR and galaxies; it
does establish the required discipline in the coefficient pipeline.

## Discipline

- Validation failures: `['adaptive_error_below_unchanged_tolerance']`.
- Full-pilot continuation remains unauthorized.
- No principal value or half residue was inserted.
- The protected formalization tree remains `b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758`.
- No UV coefficient, local-GR, galaxy, or full-MTS claim follows.
- No GitHub action occurred.

## Next

Run the next untouched argument only after applying this preflight to its
transported contour. Do not infer that all later arguments share
`A10`'s active
chamber and do not bulk-resume the schedule.
