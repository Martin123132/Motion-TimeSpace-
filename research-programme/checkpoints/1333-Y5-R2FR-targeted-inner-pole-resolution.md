# 5317 - Targeted inner-pole resolution

## Derivation

For an approximate pole `p0` and exact simple pole `p*`,
`R/(E-p*) = R/(E-p0) + R(p*-p0)/(E-p0)^2 + ...`.
The normalized basis `r^2/(E-p)^2`, `r/(E-p)`, and powers of
`u=(E-E0)/r` therefore gives the pole correction `delta p=R2/R1`
without promoting a location error to a physical double pole. Independent
interlaced holdout points test the derived correction.

The sixteen small unresolved residues are not set to zero and are not
subtracted. Their poles remain separated from the real energy contour, so
the full raw integrand is retained and must pass the original Q4/Q8 gates.

## Result

- parent pass nodes reused unchanged: `198`;
- targeted repair nodes passed: `18` / `18`;
- combined inner nodes passed: `216` / 216;
- maximum material fit residual: `7.9035310037e-08`;
- maximum independent holdout residual: `8.7631011528e-08`;
- maximum residual pole-order ratio: `1.22489804901e-08`;
- decision: **FOUR_REGULATOR_INNER_NODES_CLOSED__BUILD_EVENT_ALIGNED_OUTER_REPAIRS**;
- validation: **PASS**.

| regulator | inner nodes | coarse failing panels | coarse value |
|---|---:|---|---:|
| E0025 | pass | - | 104.534171 -20.0125498 i |
| E005 | pass | 2|9 | 135.233547 +4.93090511 i |
| E010 | pass | 2|9 | 135.242577 +4.57829265 i |
| E020 | pass | 2|9 | 135.257776 +3.87305392 i |
| E040 | pass | 2|9 | 135.276741 +2.46265361 i |

## Claim boundary

No finite-regulator ladder, regulator-zero, decay-angle, phase-space,
UV, local-GR, or full-MTS claim follows until the named outer panels
are repaired under their unchanged convergence gates.
