# 5395: D4 correlated material-residue supremum and numeric pole-primitive `W3`

## Result

The obstruction left by checkpoint 5394 is closed. The material root is no longer boxed independently of the soft coordinate and regulator. Each of the four parent-owned material branches now has a finite, source-traceable interval supremum for its correlated contour residue, and the pole-primitive contribution to the third regulator derivative has a finite numeric upper bound:

```text
sum_b |W3_pole,b| <= 3.3104357999901125e35.
```

This is a deliberately conservative enclosure, not an estimate of the physical coefficient and not a full `W3` result. The regular two-dimensional away-cell owner and the event-local remainders are still absent, so `valid_for_D4_numeric_W3_bound=false` remains mandatory.

## 1. Correlated material-root chart

For every material branch, let

```text
P_b(R;x,epsilon) = 0
```

be the exact branch polynomial inherited from the parent contour construction. The branch is simple on every certified box because the interval calculation proves

```text
0 notin partial_R P_b.
```

The implicit-function derivatives therefore exist and are enclosed by

```text
R_x       = -(partial_x P_b)/(partial_R P_b),
R_epsilon = -(partial_epsilon P_b)/(partial_R P_b).
```

With box centre `(x_0,epsilon_0)` and the point root `R_0`, the interval mean-value enclosure used in the calculation is

```text
R_b(x,epsilon)
  in R_0
     + R_x(B)       (x-x_0)
     + R_epsilon(B) (epsilon-epsilon_0).
```

The derivative intervals are evaluated over the complete raw parent root box, so the centred expression preserves the exact `R_b(x,epsilon)` correlation rather than treating `R_b`, `x`, and `epsilon` as independent coordinates. Adaptive bisection is invoked whenever a target box does not separate all required factors.

## 2. Correlated zero-factor quotients

At an energy-pole factor `s_E`, the regularized invariant quotient is evaluated directly from the channel jet,

```text
Q_E = -(partial_R s_E)/(2R).
```

Second-order interval automatic differentiation supplies the correlated derivatives

```text
partial_R Q_E
  = -1/2 [(partial_R^2 s_E)/R - (partial_R s_E)/R^2],

D_x Q_E
  = (partial_R Q_E) R_x - (partial_R partial_x s_E)/(2R),

D_epsilon Q_E
  = (partial_R Q_E) R_epsilon
    - (partial_R partial_epsilon s_E)/(2R).
```

These give a centred interval enclosure of `Q_E` on the same correlated material-root chart. The active opposite-chirality spinor bracket and the first rational spinors are treated by the same interval mean-value construction. The exact identity

```text
s_12 = 4 R^2
```

is inserted rather than re-enclosed from independently boxed momenta.

This matters for the endpoint-0 branch `B03`: an apparent two-denominator energy term is only simple after the KLT momentum-kernel zero is retained. The regularized kernel contains `Q_E` in place of the cancelled invariant. For the other active pairs, any surviving energy term must have exactly one cancelled denominator; unsupported higher pole orders are rejected.

## 3. Double regularization and chirality

The exhaustive KLT term reduction fixes complementary energy/global chiralities:

| branch | role | active pair | energy chirality | global chirality |
|---|---|---|---:|---:|
| `B01` | reciprocal | `1-4` | `0` | `1` |
| `B02` | reciprocal | `1-3` | `0` | `1` |
| `B03` | representative | `0-1` | `1` | `0` |
| `B04` | representative | `1-3` | `1` | `0` |

For each branch, the exactly double-regularized direct coefficient is assembled as

```text
H_b = (1/6) sum_(special=1)^3 K5_energy K5_global,

C_b = E_b M_b H_b / s^2,
```

where `M_b` is the stable parent energy multiplier. Every certified box retains at least one energy and one global KLT survivor. The material-residue enclosure in the parent winding normalization is

```text
|rho_b|
  <= 2 |C_b|
     / (|r_relative| |z_global| |J_collision|).
```

The factor `2` is the certified absolute winding bound. Every quotient and geometric denominator on the right-hand side is separated from zero on all 5,584 final boxes.

## 4. Certified residue suprema

| branch | boxes | max depth | min `|r_relative|` | min `|z_global|` | min `|J|` | min `|Q_E|` | `sup |rho_b|` |
|---|---:|---:|---:|---:|---:|---:|---:|
| `B01` | 2,032 | 7 | `1.0039707` | `2.4401745` | `0.83232994` | `2.6988736e-2` | `2.4628326451125874e12` |
| `B02` | 1,680 | 9 | `0.94669240` | `3.2262811` | `2.2697885e-2` | `2.7054719e-4` | `4.2206040217042424e16` |
| `B03` | 1,040 | 6 | `1.0034326` | `3.5205079` | `0.84343375` | `5.2991234e-2` | `3.9725314301878214e9` |
| `B04` | 832 | 6 | `0.96681267` | `3.9447805` | `1.8037464` | `4.5132379e-3` | `7.94589629510149e9` |

The 128 parent `(branch, atlas cell, regulator bin)` groups are covered exactly; the maximum reconstructed `x`-width error is `0.0`. The largest refinement depth is 9. The large `B02` bound is driven by a small but strictly positive energy quotient; it is retained as a conservative result rather than hidden or tuned away.

## 5. Numeric pole-primitive `W3`

Checkpoint 5394 proved one common logarithm branch and supplied

```text
|partial_epsilon^3 P_b|
  <= [3!/(5e-7)^3] sup|rho_b| sup|L_b|,

3!/(5e-7)^3 = 4.8e19.
```

Multiplication by each branch's complete away-interval width gives:

| branch | `sup |L_b|` | away width | integrated `|W3_pole,b|` upper |
|---|---:|---:|---:|
| `B01` | `17.87600082382626` | `0.07231322788636807` | `1.528143902124095e32` |
| `B02` | `15.057959406315048` | `0.010846819440988087` | `3.3089056102639507e35` |
| `B03` | `25.950309162141238` | `0.03592685948321006` | `1.7777487050329065e29` |
| `B04` | `15.370742108939154` | `0.004572754521296352` | `2.680753328069569e28` |

Thus

```text
sum_b integrated |W3_pole,b|
  <= 3.3104357999901125e35.
```

The number is finite and mechanically certified. Its size mainly measures interval/Cauchy conservatism and does not by itself establish phenomenological viability.

## 6. Validation and provenance

The full run used one thread, the complete parent regulator boxes, target `x` width `1e-3`, and adaptive depth at most 16:

```text
.venv-score\Scripts\python.exe \
  scripts\Y5_R2FR_5395_D4_correlated_material_residue_supremum_and_numeric_pole_W3.py \
  --epsilon-subdivisions 1 \
  --target-x-width 0.001 \
  --maximum-depth 16
```

It completed in `9078.8386 s`. All validation gates pass, all seven direct source paths exist with recorded SHA-256 hashes, the result marker is present, and the parent `formalization-workbench` modified-file count is zero.

Primary outputs:

```text
source-intake/functional_rg/5395/D4_correlated_material_residue_boxes.csv
source-intake/functional_rg/5395/D4_material_residue_supremum.csv
source-intake/functional_rg/5395/D4_numeric_pole_primitive_W3_bound.csv
source-intake/functional_rg/5395/D4_correlated_material_residue_validation.csv
source-intake/functional_rg/5395/D4_correlated_material_residue_result.json
source-intake/functional_rg/5395/source_register.csv
source-intake/mts_residuals/P8_Y5_BRR545_5395_VALIDATION.csv
```

## 7. Claim boundary and next target

Checkpoint 5395 certifies only:

```text
valid_for_D4_correlated_material_root_residue_enclosure = true
valid_for_D4_material_residue_supremum                 = true
valid_for_D4_numeric_pole_primitive_W3_bound           = true
```

It does not certify a full numeric `W3`, the uniform remainder, the outer-regulator zero limit, the decay-angle integral, full angular convergence, a full phase-space coefficient, a UV claim, local GR, or full MTS.

The next derivation target is the regular two-dimensional away-cell owner. The pole pieces must be subtracted analytically on each compatible cell, the third regulator derivative of the regular remainder must be interval-enclosed and integrated, and the event-local remainder owners must then be added. Only that combined result can promote `valid_for_D4_numeric_W3_bound` to true.
