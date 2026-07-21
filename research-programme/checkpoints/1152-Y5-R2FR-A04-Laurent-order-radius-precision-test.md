# 5136: A04 Laurent-order radius/precision test

## Question

The locked default chart rejected `A04` because the small beam-spinor pole gave a
double-to-simple ratio above the fixed limit. Nested precision was not invoked as
a rescue because the existing policy allows it only after Laurent order already
passes. This checkpoint instead asks whether the apparent second-principal
coefficient behaves like a genuine double pole.

## Predeclared discriminator

The same pole is measured at boundary fractions `(0.12, 0.1, 0.08, 0.06)` with the
existing default and nested node profiles. A genuine coefficient `a_(-2)` must
be stable between quadratures and radii, while
`|a_(-2)|/(|a_(-1)| r)` must scale approximately as `r^-1`. Numerical
contamination is admitted only if refinement reduces the coefficient by at
least a factor of five, the original radius passes every locked threshold at
nested precision, and the coefficient is not radius-stable.

## Result

- Outcome: `INCONCLUSIVE_SIMPLE_CHART_REMAINS_BLOCKED`.
- Nested coefficient relative spread: `5.12806537286`.
- Nested ratio log-slope: `-0.969478742722`.
- Nested coefficient log-slope: `0.0308115393603`.
- Default-to-nested coefficient reduction at boundary fraction `0.12`: `1.6938823218`.
- Nested original-radius locked-threshold pass: `False`.
- Pilot counts remain `{'completed_converged': 50, 'completed_unconverged': 0, 'failed': 0, 'missing': 510}`; no coefficient job was executed.

## Discipline

This is a pole-order diagnostic, not a changed acceptance threshold. It cannot
establish a UV coefficient, local GR, galaxy phenomenology, or the full MTS
theory. The protected formalization tree remains `b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758` and no
GitHub action occurred.
