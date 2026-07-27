# 3194 - Source-Owned Boundary Layer Action Or Modified Parent Profile Functional Under AX1090

Private checkpoint. This is not a local-GR claim, Newtonian-limit claim, PPN pass, solar-J2 pass, clock pass, orbital pass, or public-facing result.

## Result

3193 proved that the pure natural-interface route fails for the quadratic toy profile functional.

3194 tests whether the required interface counter-momenta can be represented by an actual variational mechanism rather than by hand-written closure coefficients.

Three routes were checked:

```text
1. linear boundary counterterm,
2. quadratic C1-mismatch penalty,
3. C1 gluing multiplier action.
```

## Candidate Actions

The arbitrary linear counterterm:

```text
S_bl = sum_i tau_i z_i,
z_i in {F,F'}
```

can always supply the required counter-momenta, but this is just the 3193 tau ledger repackaged as an action. It remains closure-only unless the `tau_i` are parent-derived.

The source-neutral quadratic penalty:

```text
S_bl = (1/2)k0[F]^2 + (1/2)k1[F']^2 + k01[F][F']
```

fails for the exact 3192 branch, because that branch is already C1 matched:

```text
[F] = 0,
[F'] = 0.
```

So the penalty gradient vanishes exactly where a nonzero counter-momentum is required.

## Best Current Route

The useful candidate is a C1 gluing multiplier action:

```text
S_glue = sum_interfaces(lambda_0[F] + lambda_1[F']).
```

Variation with respect to the multipliers gives:

```text
[F] = 0,
[F'] = 0.
```

Variation with respect to the boundary fields gives the interface force-balance equations:

```text
[Pi_0] + lambda_0 = 0,
[Pi_1] + lambda_1 = 0.
```

So:

```text
lambda_i = -[Pi_i].
```

This is better than an arbitrary counterterm because the multiplier values are solved by stationarity, not chosen as fixed coefficients.

## Numeric Closure

For the 3190/3192 same-width row:

```text
w = 0.435,
N4_D2 = 1.174307819436789,
lambda_norm = 4.712368709711363,
max cancellation residual = 0.
```

For the balanced-curvature row:

```text
w = 0.623,
N4_D2 = 1.093472635691388,
lambda_norm = 3.611505468707701,
max cancellation residual = 0.
```

For the smallest generated multiplier norm:

```text
w = 0.950,
N4_D2 = 0.9696291000650621,
lambda_norm = 2.512093788598432,
max cancellation residual = 0.
```

The last row inherits the 3193 scan-edge/large-curvature-jump issue, so it is not a clean selection.

## Interpretation

This checkpoint does not prove local GR.

It does show that the interface problem is no longer just:

```text
missing counter-momenta.
```

It is now:

```text
derive the parent origin of C1 gluing multipliers,
or derive a modified parent bulk functional whose natural momenta match without edge degrees.
```

That is a sharper and more physical target.

## Decision

The best current route is:

```text
C1 gluing multiplier mechanism,
parent signature still required.
```

The next target is:

```text
3195-Y5-R2FR-gluing-multiplier-parent-origin-or-finite-layer-limit-under-AX1090
```

## Generated Evidence

- `source-intake/mts_residuals/P8_Y5_R2FR_3194_INPUTS.csv`
- `source-intake/mts_residuals/P8_Y5_R2FR_3194_BOUNDARY_ACTION_CANDIDATE_REGISTER.csv`
- `source-intake/mts_residuals/P8_Y5_R2FR_3194_C1_GLUING_MULTIPLIER_DERIVATION.csv`
- `source-intake/mts_residuals/P8_Y5_R2FR_3194_MULTIPLIER_SOLUTIONS.csv`
- `source-intake/mts_residuals/P8_Y5_R2FR_3194_CLOSURE_CLASSIFICATION.csv`
- `source-intake/mts_residuals/P8_Y5_R2FR_3194_DECISION.csv`
- `source-intake/mts_residuals/P8_Y5_R2FR_3194_VALIDATION.csv`

Validation passed and all rows remain `valid_for_claim=false`.
