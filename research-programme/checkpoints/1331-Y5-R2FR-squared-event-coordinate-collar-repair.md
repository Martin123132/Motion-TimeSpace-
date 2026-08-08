# 5315 - Squared-event-coordinate collar repair

## Derivation

At both failed 5314 leaves, the shared pole crosses a support edge with a
nonzero slope.  Locally,

`p(x)-E_edge(x) = kappa (x-x_event) + O((x-x_event)^2)`, with `kappa != 0`.

The exact energy-space pole primitive therefore contributes
`A log|x-x_event| + regular` to the outer integrand.  This is integrable but
converges slowly under ordinary Gauss-Legendre quadrature at an endpoint.
The exact coordinate change

`|x-x_event| = t^2`,  `|dx| = 2t dt`

maps it to `4 A t log(t) + O(t)`, which is integrable and vanishes at `t=0`.
No term, coefficient, or closure is added.  The Jacobian is included in every
quadrature weight and its constant-integrand identity is validated.

## Result

- parent passing leaves retained: `31`;
- failed parent leaves replaced: `2`;
- transformed segments: `4`;
- transformed nodes: `80` / `80`;
- failed transformed inner nodes: `0`;
- off-axis raw-contour nodes: `13`;
- maximum conservative repaired-leaf Q8/Q12 error:
  `2.06086995983e-05`;
- panel-nine conservative error:
  `0.0017541768142`;
- reassembled `E0025` fixed-decay integral:
  `104.534170859`
  `-20.0125498159 i`.

Decision: **E0025_SQUARED_EVENT_COORDINATE_REPAIR_CONVERGED__VALIDATE_THEN_EXTEND_REGULATOR_LADDER**.

Validation: **PASS**.

## Claim boundary

This closes only the `E0025` outer-soft integral at one fixed absolute decay
angle if validation passes.  It does not establish the regulator-zero limit,
decay-angle integral, full phase-space coefficient, UV prediction, local GR,
or the full MTS theory.
