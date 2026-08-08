# 3195 - Gluing Multiplier Parent Origin Or Finite Layer Limit Under AX1090

Private checkpoint. This is not a local-GR claim, Newtonian-limit claim, PPN pass, solar-J2 pass, clock pass, orbital pass, or public-facing result.

## Result

3194 showed that C1 gluing multipliers close the interface equations exactly, but still need a parent origin.

3195 constructs the next-best mathematical origin: a finite positive boundary layer whose hard-constraint limit produces those multipliers as reaction forces.

Let the layer carry the C1 mismatch variables:

```text
z = (Delta F, Delta F').
```

For a layer of thickness `delta` with positive stiffness matrix `K`, the effective layer action is:

```text
S_layer = (1/(2 delta)) z^T K z.
```

The conjugate interface force is:

```text
lambda = dS_layer/dz = (K/delta)z.
```

Equivalently:

```text
z = delta K^-1 lambda.
```

So as:

```text
delta -> 0,
```

the mismatch goes to zero while the reaction force can stay finite:

```text
z -> 0,
lambda finite.
```

The layer energy also vanishes for finite `lambda`:

```text
S_layer = (1/2) lambda^T(delta K^-1)lambda -> 0.
```

## Meaning

This gives a clean interpretation of the 3194 multipliers:

```text
lambda_i = -[Pi_i]
```

can be understood as finite reaction forces of a vanishing-thickness C1 layer.

That is not the same as proving MTS derives the layer, but it removes the weaker objection that the multipliers are just arbitrary numbers written on the boundary.

## Scaling Smoke Test

For the 3190/3192 reference-width row:

```text
lambda_norm = 4.712368709711363.
```

At:

```text
epsilon = 1e-12,
```

the finite-layer scaling gives:

```text
mismatch_norm = 4.712368709711363e-12,
layer_energy_proxy = 1.110320942813337e-11,
force recovery residual = 0.
```

For the balanced-curvature row:

```text
lambda_norm = 3.611505468707701,
mismatch_norm = 3.611505468707701e-12,
layer_energy_proxy = 6.521485875252816e-12.
```

So the hard constraint limit behaves correctly:

```text
finite reaction force,
vanishing mismatch,
vanishing layer-energy proxy.
```

## Remaining Parent Gates

This still does not prove local GR.

The parent action must still derive:

```text
1. the layer or auxiliary edge degrees of freedom,
2. the positive stiffness/compliance matrix K,
3. the hard-constraint scaling delta K^-1 -> 0,
4. covariant localization of the layer,
5. width/profile selection,
6. suppression of PPN/clock/WEP/orbital/R10 residuals.
```

All six remain open blockers.

## Decision

3195 upgrades the route from:

```text
add multipliers by hand
```

to:

```text
derive multipliers as finite-layer reaction forces.
```

The best next target is:

```text
3196-Y5-R2FR-auxiliary-layer-field-elimination-or-parent-compliance-matrix-under-AX1090
```

That target should try to construct an auxiliary layer field whose elimination produces the compliance matrix, or else cleanly mark the finite-layer route as a closure assumption.

## Generated Evidence

- `source-intake/mts_residuals/P8_Y5_R2FR_3195_INPUTS.csv`
- `source-intake/mts_residuals/P8_Y5_R2FR_3195_FINITE_LAYER_DERIVATION.csv`
- `source-intake/mts_residuals/P8_Y5_R2FR_3195_COMPLIANCE_SCALING_RUNNER.csv`
- `source-intake/mts_residuals/P8_Y5_R2FR_3195_PARENT_SIGNATURE_GATE.csv`
- `source-intake/mts_residuals/P8_Y5_R2FR_3195_ROUTE_CLASSIFICATION.csv`
- `source-intake/mts_residuals/P8_Y5_R2FR_3195_DECISION.csv`
- `source-intake/mts_residuals/P8_Y5_R2FR_3195_VALIDATION.csv`

Validation passed and all rows remain `valid_for_claim=false`.
