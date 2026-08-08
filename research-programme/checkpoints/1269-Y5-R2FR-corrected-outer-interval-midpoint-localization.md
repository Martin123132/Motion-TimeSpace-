# 5253 - Corrected outer interval midpoint localization

## Derivation

Let `f_i=f(x_i)` be consecutive corrected order-9 endpoint values, `m_i=(x_i+x_(i+1))/2`, and `h_i=x_(i+1)-x_i`. The checkpoint evaluates the parent integrand at every arithmetic midpoint and forms

```text
T_i = J h_i [f(x_i)+f(x_(i+1))]/2;
S_i = J h_i [f(x_i)+4 f(m_i)+f(x_(i+1))]/6;
D_i = S_i-T_i
    = (2 J h_i/3) [f(m_i)-(f(x_i)+f(x_(i+1)))/2];
J   = 0.25.
```

`|D_i|` is used only to localize curvature and cancellation. It is not called a rigorous quadrature bound. That requires quarter-point refinement and comparison of one-panel with two-panel Simpson rules.

## Measured interval map

- `I01` [-0.919260134849, -0.703571247281]: midpoint `-0.811415691065`, |S-T| `74.1222522507`, rank `1`, refine `True`.
- `I06` [0.703571247281, 0.919260134849]: midpoint `0.811415691065`, |S-T| `67.6068129403`, rank `2`, refine `True`.
- `I03` [-0.380770015203, 6.09261782576e-17]: midpoint `-0.190385007602`, |S-T| `7.39462592644`, rank `3`, refine `False`.
- `I04` [6.09261782576e-17, 0.380770015203]: midpoint `0.190385007602`, |S-T| `7.21585740359`, rank `4`, refine `False`.
- `I02` [-0.703571247281, -0.380770015203]: midpoint `-0.542170631242`, |S-T| `3.55441902042`, rank `5`, refine `False`.
- `I07` [0.919260134849, 0.995]: midpoint `0.957130067424`, |S-T| `3.1151067819`, rank `6`, refine `False`.
- `I05` [0.380770015203, 0.703571247281]: midpoint `0.542170631242`, |S-T| `1.78081890353`, rank `7`, refine `False`.
- `I00` [-0.995, -0.919260134849]: midpoint `-0.957130067424`, |S-T| `0.531391540093`, rank `8`, refine `False`.

## Composite result

- Composite trapezoid (inner 512): `(14.272797333579959-0.5487182383577617j)`.
- Composite Simpson (inner 512): `(-16.413872711302368-0.9369904328582165j)`.
- Global embedded relative difference: `1.8666676027`.
- Cancellation-safe relative indicator: `10.0556751985`.
- Simpson inner 128/512 relative difference: `4.90516266815e-07`.
- Simpson versus parent global order-9 relative difference: `1.9130390545`.

## Decision

`ADOPT_INTERVAL_ERROR_MAP__BISECT_DOMINANT_INTERVALS`

Failed acceptance gates: `GLOBAL_FIRST_LEVEL_EMBEDDED_DIFFERENCE|CANCELLATION_SAFE_FIRST_LEVEL_EMBEDDED_BUDGET`.

## Claim boundary

- This is one fixed-soft-energy decay-angle slice.
- The first-level embedded indicator is not a proof of outer convergence.
- No numeric UV coefficient, all-operator local-GR result, or full-MTS claim is promoted.

## Next exact target

Evaluate both quarter points in the dominant intervals `I01, I06`. For each selected interval compare the one-panel Simpson value with the sum of its two half-panel Simpson values. Use `|S_two-S_one|/15` only where the measured topology is unchanged and the smoothness audit passes; otherwise split at the observed topology boundary.
