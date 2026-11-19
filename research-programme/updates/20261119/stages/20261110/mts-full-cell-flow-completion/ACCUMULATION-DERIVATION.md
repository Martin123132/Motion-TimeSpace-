# Complete the retained source integral before changing physical models

This calculation uses the same saved physical path, source bank, branch equations, terminal adjoints and observable scales as the preceding stages. It changes neither the action nor a coupling. Its purpose is to finish and qualify the numerical representation of the previously derived source.

## Direct source versus component reconstruction

Let S be the full projected source and F its derived heavy-background-flow component. Let Q_old denote the saved whole-cell integration rule and Q_new the frozen segment-aligned rule. Linearity gives

```
Q_new(S) - [Q_old(S-F) + Q_new(F)]
    = Q_new(S-F) - Q_old(S-F).
```

The component comparison computes the old S-F difference with 90-digit arithmetic on the saved binary inputs, restores the complete F contribution, and checks this identity and the existing numerical threshold for both metric branches and both affected observables. It does not discard the flow defect or replace a stored background derivative by an equation-of-motion right-hand side. Agreement of two quadrature constructions is a numerical diagnostic, not a rigorous continuum error certificate.

## Accumulate once, from the two-cell result

With one common terminal adjoint, the first-order observable correction is additive over adjacent N intervals:

```
A_123 = A_12 + A_3,
B_123 = B_12 + B_3,
E_123,j = E_12,j + abs(delta A_3,j).
```

B is the retained conditional source-size/Cauchy budget. The E values carry absolute numerical-control changes, so cancellation between cells cannot turn a failed local check into a cumulative pass. The code also requires each individual cell's existing pass flag, common reference scales, exact shared physical endpoints and matching shared source/control packets. It uses the saved second-cell two-cell total, not any previously accumulated three-cell total. The older three-cell total is read only to report the effect of this numerical repair.

## Coordinate measure and physical clock controls

The inherited phase rule represents dN as dtheta/(dtheta/dN). The new source projection integrates the identical source directly in N, using weights tested against exact frozen interval moments. It therefore has no separately approximated phase-to-N Jacobian to vary. This is a coordinate-integration identity, already established in ../mts-segment-aware-flow-defect-20261109/DERIVATION.md, not a claim that physical time, phase evolution or background-flow defects vanish.

The prior two-cell clock-measure change and its absolute allowance remain in the cumulative result unchanged. The third-cell numerical clock-measure perturbation is marked not applicable rather than represented as a successful physical clock test. All third-cell phase-history, current-history, cross, combined, adjoint-interpolation and adjoint-step controls remain. Neither a physical source contribution nor the old cells' measure uncertainty is removed.

No additional coarser cumulative rule is invented where the direct projection has only a finest/coarse pair. All original algebra and numerical thresholds remain 1e-10 and 2e-5. Baseline failures remain visible alongside their absolute physical scales. Results apply to the saved balanced family and the first three specified cells; they do not certify the full physical history or supply a galaxy constitutive law.
