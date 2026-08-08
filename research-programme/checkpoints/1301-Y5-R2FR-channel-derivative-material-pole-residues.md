# 5285 — Channel-derivative material-pole residues

## Derived residue law

For each material pole owner `X` with channel `D_X(E)`,

`F_X(E) = N_X(E) / D_X(E)`,

the complex channel zero `E_X` is Newton-refined and the residue is
computed from

`A_X = N_X(E_X) / D'_X(E_X)`.

The numerator samples use the already audited true local-limit
contributions from 5284:

`N_X(E_i) = D_X(E_i) F_X(E_i)`.

This removes the unstable direct fit of `F_X` to a Laurent ansatz.

## Result

- order 16: `-2.23328047953+2.13090588368i`
- order 4: `-2.23328042135+2.13090588304i`
- order 8: `-2.23328047061+2.13090587942i`

- maximum channel-root residual:
  `7.1470661499e-16`;
- maximum pole refinement shift:
  `1.37073580987e-08`;
- maximum derivative step change:
  `1.05422440569e-10`;
- maximum numerator-fit residual:
  `3.57970320966e-12`;
- maximum radius-refinement change:
  `1.57977440288e-12`;
- maximum degree change:
  `6.45714913785e-10`;
- maximum order-16 residue-ensemble shift:
  `3.80864252815e-08`;
- order 8 to 16 quadrature change:
  `3.20011450505e-09`;
- certificate:
  `True`.

Decision:
`CERTIFY_CHANNEL_DERIVATIVE_MC04_MC12_RESIDUES__BUILD_CHAMBER_ADAPTED_ANGULAR_RUNNER`.

Validation: **PASS**.

## Claim boundary

This certifies the fixed-angle pole subtraction only if every listed
gate passes. It does not yet supply the angular integral, a full
phase-space coefficient, a UV claim, local GR, or full MTS.
