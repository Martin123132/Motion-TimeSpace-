# 3196 - Auxiliary Layer Field Elimination Or Parent Compliance Matrix Under AX1090

Private checkpoint. This is not a local-GR claim, Newtonian-limit claim, PPN pass, solar-J2 pass, clock pass, orbital pass, or public-facing result.

## Result

3195 showed that the gluing multipliers can be interpreted as finite reaction forces of a hard C1 layer.

3196 tests whether a local auxiliary layer field can produce the layer compliance matrix by elimination.

Use the C1 mismatch slot vector:

```text
z = (Delta F_L, Delta F'_L, Delta F_R, Delta F'_R).
```

Introduce a nonpropagating auxiliary layer field `chi`:

```text
S_layer[z, chi]
  = (1/(2 delta))(z^T K0 z + 2 z^T B chi + chi^T M chi).
```

The auxiliary equation is algebraic:

```text
M chi + B^T z = 0,
chi* = -M^-1 B^T z.
```

Eliminating `chi` gives:

```text
S_eff[z] = (1/(2 delta)) z^T K_eff z,
K_eff = K0 - B M^-1 B^T.
```

This is the Schur-complement route to the 3195 compliance matrix:

```text
C_delta = delta K_eff^-1.
```

## Key Gate

The important no-go:

```text
if K0 = 0 and M > 0,
K_eff = -B M^-1 B^T <= 0.
```

So a healthy auxiliary field cannot create positive interface stiffness from nothing.

The parent must provide at least one of:

```text
1. direct positive layer stiffness K0,
2. a constrained/domain-geometry origin for the hard C1 layer,
3. a modified bulk functional whose natural interface momenta already match.
```

Without that, the auxiliary field route becomes a closure device.

## Model Scan

The canonical healthy model:

```text
K0 = 2I,
B = I,
M = I,
K_eff = I.
```

has positive full block eigenvalues:

```text
min eigenvalue = 0.3819660112501051,
max eigenvalue = 2.618033988749895.
```

The near-critical positive model:

```text
K0 = 1.1I,
B = I,
M = I,
K_eff = 0.1I.
```

is still healthy but much more compliant.

The pure auxiliary model:

```text
K0 = 0,
B = I,
M = I,
K_eff = -I.
```

is rejected as negative-stiffness/ghost-risk.

## Multiplier Recovery

For all generated positive models, the compliance rows recover the 3194 multipliers.

Validation maximum recovery residual:

```text
4.440892098500626e-16.
```

For the canonical model at the 3190/3192 reference width:

```text
K_eff = 1,
epsilon = 1e-12,
force recovery residual = 0.
```

So the chain is now:

```text
exact interior profile
-> interface no-go
-> gluing multipliers
-> finite-layer hard constraint
-> auxiliary-field Schur-complement compliance.
```

## Decision

This is a coherent effective route, but still not a parent-derived local-GR proof.

The next parent-owned target is:

```text
3197-Y5-R2FR-parent-owned-positive-layer-stiffness-or-domain-geometry-constraint-under-AX1090
```

That target should try to derive the positive direct layer stiffness/domain constraint from MTS parent structure. If it cannot, the finite-layer route must remain an explicit closure branch.

## Generated Evidence

- `source-intake/mts_residuals/P8_Y5_R2FR_3196_INPUTS.csv`
- `source-intake/mts_residuals/P8_Y5_R2FR_3196_AUXILIARY_ELIMINATION_DERIVATION.csv`
- `source-intake/mts_residuals/P8_Y5_R2FR_3196_POSITIVE_SCHUR_COMPLEMENT_MODELS.csv`
- `source-intake/mts_residuals/P8_Y5_R2FR_3196_PARENT_COMPLIANCE_MATRIX_ROWS.csv`
- `source-intake/mts_residuals/P8_Y5_R2FR_3196_ROUTE_CLASSIFICATION.csv`
- `source-intake/mts_residuals/P8_Y5_R2FR_3196_DECISION.csv`
- `source-intake/mts_residuals/P8_Y5_R2FR_3196_VALIDATION.csv`

Validation passed and all rows remain `valid_for_claim=false`.
