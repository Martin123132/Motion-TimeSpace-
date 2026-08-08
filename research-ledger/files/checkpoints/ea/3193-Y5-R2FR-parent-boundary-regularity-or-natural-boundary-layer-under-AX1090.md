# 3193 - Parent Boundary Regularity Or Natural Boundary Layer Under AX1090

Private checkpoint. This is not a local-GR claim, Newtonian-limit claim, PPN pass, solar-J2 pass, clock pass, orbital pass, or public-facing result.

## Result

3192 solved the exact interior profile equation for the toy quadratic projected-source functional.

3193 tests whether that interior solution can also pass the natural interface conditions at the core/transition and transition/exterior joins.

For:

```text
L = x^4 Q^2,
Q = D2[F],
u = x^4 Q,
```

the second-derivative variation gives boundary terms:

```text
delta J_boundary = [Pi_1 delta F' + Pi_0 delta F].
```

The two natural interface momenta are:

```text
Pi_1 = dL/dF'' = (4/5)u,
Pi_0 = dL/dF' - d(Pi_1)/dx = 4u/x - (4/5)u'.
```

So without a localized boundary/interface action, the joins require:

```text
[Pi_1] = 0,
[Pi_0] = 0.
```

## No-Go Result

The exact interior transition from 3192 is:

```text
F_tr = A + Bx^2 + C/x + D/x^3.
```

Only `A` and `B` contribute to `D2`, so:

```text
u_tr = 6B x^4 + (6/5)A x^2.
```

The exterior branch is:

```text
F_ext = x^-3,
u_ext = 0,
u_ext' = 0.
```

At the exterior join `x=b`, natural matching requires:

```text
u_tr(b)=0,
u_tr'(b)=0.
```

Those two equations force:

```text
A = 0,
B = 0.
```

Then the transition collapses to:

```text
F_tr = C/x + D/x^3.
```

Matching `F` and `F'` to the exterior at `b` then forces:

```text
C = 0,
D = 1,
F_tr = x^-3.
```

That cannot also match the core branch:

```text
F_core = x^2,
F_core' = 2x.
```

Therefore the pure natural-interface route is rejected for this toy functional.

## Numeric Interface Scan

The same-width exact EL row from 3192 has:

```text
w = 0.435,
N4_D2 = 1.174307819436789,
boundary momentum norm = 4.712368709711363.
```

The 3192 balanced-curvature row has:

```text
w = 0.623,
N4_D2 = 1.093472635691388,
boundary momentum norm = 3.611505468707701.
```

The smallest boundary-momentum norm in the scan is still nonzero and occurs at the scan edge:

```text
w = 0.950,
N4_D2 = 0.9696291000650621,
boundary momentum norm = 2.512093788598432.
```

So width tuning does not close the interface.

## Required Boundary Layer

If the exact interior EL branch is retained, a localized interface/boundary-layer action must vary to supply counter-momenta:

```text
tau = -jump(Pi).
```

This is now a concrete source target, not a vague closure gap.

For the same-width row:

```text
tau_left_Pi1  =  0.1799958699798417,
tau_left_Pi0  = -1.406232935887395,
tau_right_Pi1 = -4.268376530146791,
tau_right_Pi0 =  1.406232935887397.
```

These numbers are not claimed as physical until a parent-owned boundary-layer action derives them.

## Decision

This checkpoint is a real narrowing:

```text
interior profile equation solved,
pure natural interface matching rejected,
boundary/interface source action required.
```

The next target is:

```text
3194-Y5-R2FR-source-owned-boundary-layer-action-or-modified-parent-profile-functional-under-AX1090
```

## Generated Evidence

- `source-intake/mts_residuals/P8_Y5_R2FR_3193_INPUTS.csv`
- `source-intake/mts_residuals/P8_Y5_R2FR_3193_INTERFACE_CONDITION_DERIVATION.csv`
- `source-intake/mts_residuals/P8_Y5_R2FR_3193_EXTERIOR_NATURAL_MATCH_NO_GO.csv`
- `source-intake/mts_residuals/P8_Y5_R2FR_3193_BOUNDARY_MOMENTUM_RESIDUAL_SCAN.csv`
- `source-intake/mts_residuals/P8_Y5_R2FR_3193_BOUNDARY_MOMENTUM_SELECTION.csv`
- `source-intake/mts_residuals/P8_Y5_R2FR_3193_REQUIRED_BOUNDARY_LAYER_COUNTERMOMENTA.csv`
- `source-intake/mts_residuals/P8_Y5_R2FR_3193_DECISION.csv`
- `source-intake/mts_residuals/P8_Y5_R2FR_3193_VALIDATION.csv`

Validation passed and all rows remain `valid_for_claim=false`.
