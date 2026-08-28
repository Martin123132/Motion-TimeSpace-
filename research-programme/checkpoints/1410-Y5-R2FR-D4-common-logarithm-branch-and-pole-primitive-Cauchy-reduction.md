# 5394: D4 common logarithm branch and pole-primitive Cauchy reduction

## Result

The four material pole primitives now have one parent-compatible logarithm sheet on every parent-frozen away component and on every regulator-plane Cauchy disk required above the physical interval `epsilon in [0,0.02]`. This is a genuine closure of the logarithm ambiguity; it is not a numeric `W3` claim.

Writing the material pole as `p_b=1-R_b^2`, define

```text
a_b = E_U - p_b
b_b = p_b - E_L.
```

The interval certificate proves `Re(a_b)>0` and `Re(b_b)>0` throughout the full Cauchy stadium. Therefore both right-half-plane logarithms are analytic there and the causal parent primitive is

```text
L_b = Log(a_b) - Log(b_b) + i sigma_b pi,
P_b = rho_b L_b.
```

The constant `sigma_b` is fixed by the positive-regulator causal approach and cannot jump on an away component because neither gap reaches zero.

## Certified branches

| branch | surface | sheet | min Re(E_U-p) | min Re(p-E_L) | sup |L| |
|---|---|---:|---:|---:|---:|
| `B01` | `direct:L:s14` | `-1 i pi` | `4.2482726e-06` | `0.0011864313` | `17.876001` |
| `B02` | `direct:shared:s13` | `1 i pi` | `7.7623998e-05` | `0.082967523` | `15.057959` |
| `B03` | `direct:L:s01` | `1 i pi` | `1.1573559e-08` | `0.00010223562` | `25.950309` |
| `B04` | `direct:shared:s13` | `1 i pi` | `0.00010401454` | `0.006480864` | `15.370742` |

## Exact Cauchy reduction

For every real center `epsilon_0 in [0,0.02]`, the stored rectangles contain the complete disk `|z-epsilon_0| <= 5e-7`. Hence

```text
|d_epsilon^3 P_b(epsilon_0)|
  <= 3! / (5e-7)^3 * sup_stadium |rho_b| * sup_stadium |L_b|,
|d_epsilon^3 W_pole|
  <= sum_b integral_away dx |d_epsilon^3 P_b|.
```

The exact third-derivative multiplier is `4.8e+19`. The script emits branchwise integrated formulas with every factor fixed except the correlated parent-contour residue supremum `rho_b_sup`.

## What was rejected

A naive rectangular enclosure treats `R_b` and the soft coordinate as independent. Development probes showed that this destroys their exact material-polynomial correlation and creates false zero-containing channel quotients, despite the same contour evaluator reproducing the stored point residues and their factor-two winding normalization. That false box is not used as evidence.

## Decision

The next checkpoint must carry a correlated material-root representation into the parent contour coefficient. Once a certified finite `rho_b_sup` is inserted into the emitted formulas, the pole-primitive part of `W3` becomes numeric. Regular 2D away cells and event-local remainders remain separate owners.

No local-GR, UV, full phase-space, regulator-limit, or full-MTS claim is made here.
