# 5450: D4 event-endpoint Cauchy subtraction and correlated probe

## Decision

**EXACT_ENDPOINT_SUBTRACTION_DERIVED__CORRELATED_PARENT_CONTOUR_PROBE_PASSES__BUILD_FINITE_XT_COVER**

## Exact endpoint identity

The 5386 parent interface is not the singular coefficient `F` itself. Its exact return value is `Q(delta)=delta F(delta)`, after the same global-pole regularization and the same three geometric divisions used by the 5395 centre residue. Consequently

```text
rho=Q(0),
F(delta)=rho/delta+G(delta),
G(delta)=[Q(delta)-Q(0)]/delta.
```

If `Q` is holomorphic on `|delta|<=R` and `sup_|delta|=R |Q|<=M_Q`, its Taylor coefficients obey `|q_n|<=M_Q/R^n`. Therefore, for every `a<R`,

```text
sup_|delta|<=a |G(delta)|
 <= sum_(n>=1) M_Q a^(n-1)/R^n
 = M_Q/(R-a).
```

This is the finite regular-part bound that replaces the divergent `rho/|delta|` triangle estimate at the connector endpoint. No plateau, fitted closure or zero-residue assumption is introduced.

## Overlap rule

The source contour has `R=1e-5`. The inner owner is valid through `0.75R`; the existing parent away evaluator is used only once `|delta|>=0.50R`. The positive `0.25R` overlap means adaptive boxes do not have to resolve the artificial switching circle exactly.

| event | branch | M_Q | sup inner | rho bound | overlap |
|---|---|---:|---:|---:|---:|
| `E01` | `B01` | 27295749.327946216 | 10918299731178.486 | 2462832645112.5874 | 2.5000000000000006e-06 |
| `E02` | `B03` | 599306.5888342339 | 239722635533.6936 | 3972531430.1878214 | 2.5000000000000006e-06 |
| `E03` | `B04` | 27704.596915183232 | 11081838766.073294 | 7945896295.10149 | 2.5000000000000006e-06 |
| `E04` | `B01` | 19746246547822.324 | 7.89849861912893e+18 | 2462832645112.5874 | 2.5000000000000006e-06 |
| `E05` | `B03` | 1271252622878497.8 | 5.0850104915139913e+20 | 3972531430.1878214 | 2.5000000000000006e-06 |
| `E06` | `B04` | 180644.326296988 | 72257730518.79521 | 7945896295.10149 | 2.5000000000000006e-06 |
| `E07` | `B02` | 113291037.51625088 | 45316415006500.35 | 4.2206040217042424e+16 | 2.5000000000000006e-06 |
| `E08` | `B02` | 468439.3706937941 | 187375748277.51767 | 4.2206040217042424e+16 | 2.5000000000000006e-06 |

## Correlated parent probe

The formula was also exercised through a different input route: each moving endpoint coordinate was replaced by a small independent correlated `x` interval, its material root was recomputed by the 5395 implicit-root machinery, and the exact 5386 `Q` contour was rerun on both regulator-edge boxes and all 32 energy arcs.

| event | probes | passed | max correlated M_Q | min denominator |
|---|---:|---:|---:|---:|
| `E01` | 64 | 64 | 7013636.234891888 | 3.767253716963976e-07 |
| `E02` | 64 | 64 | 72791.62956631657 | 9.254702338058739e-06 |
| `E03` | 64 | 64 | 9750.691452609177 | 1.3201070210680189e-06 |
| `E04` | 64 | 64 | 1977282315042.9736 | 2.542929562079242e-07 |
| `E05` | 64 | 64 | 1178127428758.0713 | 1.7609211828676152e-08 |
| `E06` | 64 | 64 | 57808.957949503056 | 9.7450192101674e-07 |
| `E07` | 64 | 64 | 23847245.4203846 | 1.0389180043728412e-06 |
| `E08` | 64 | 64 | 121959.72704616167 | 2.0584919238741004e-07 |

## Claim boundary

This proves the subtraction identity and a finite event-curve inner bound, and it verifies that the exact parent contour survives an independent correlated-x transplant. It does not yet cover the full 19 mapped cells: the next runner must tile connector `(x,t)` boxes with the overlapping inner/outer rule and bound the nonsingular upper/cutoff logarithm. Event-local `W3`, combined `W3`, the D4 regulator limit, all-operator local GR and full MTS remain false.
