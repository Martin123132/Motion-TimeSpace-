# Duration-growth stage — 2026-11-15

## What was derived

Density/pressure corrections begin at fourth order in local elapsed conformal time, while the heavy current begins at fifth order. Coefficients follow from the retained coupled equations, source derivatives and signed preparation weights. The exact extension across source corners is a time-dependent integral response, not one fitted exponent.

Weighted local coefficients, ordered (density,current,pressure):
- Baseline fourth: (-1.2762947884660016e-4,0,0); fifth: (-1.7435882515875786e-7,0,0).
- MTS fourth: (-7.33879881544189e-5,0,-7.33879881544189e-5).
- MTS fifth: (-6.99007938727852e-4,-7.33879881544189e-5,-8.121066835270513e-4).

They multiply native elapsed-time powers; they are not new fitted parameters or SI measurements.

## Both saved windows checked

First window: original indices2892..2900, duration about0.009864.
Extended window: indices2892..2908, duration about0.019727. The scoring tables separately show the original eight nonzero reports and the eight added reports; together they check the entire17-report history.

A pure fourth-power extrapolation is insufficient for MTS. Adding the derived fifth coefficient still misses extended-block MTS pressure by14.1911% on the correction-amplitude scale, versus the unchanged0.002% gate. This failed approximation is retained rather than fitted or loosened. Baseline fourth-plus-fifth reaches6.16e-7 relative discrepancy in the extension.

The time-dependent response series through eight interactions passes both cases and both blocks. Maximum relative discrepancy INCLUDING the same-style absolute-weighted numerical working allowance:

| Case/channel | Original block | Added block |
|---|---:|---:|
| Baseline density | 2.6530e-15 | 1.9672e-15 |
| MTS density | 1.0318e-8 | 1.3602e-9 |
| MTS current | 2.6296e-8 | 3.3876e-9 |
| MTS pressure | 9.8488e-9 | 1.3501e-9 |

The gate is2e-5 relative to the correction's own amplitude, not the larger full observable. All original observable-scale checks also pass. Baseline current and pressure stay exactly zero. Node-state comparisons pass at both endpoints.

Hierarchy behavior is informative: at the later window, four interactions leave MTS current6.4241e-5 relative error and fail; six reduce it to2.5940e-7 raw, eight to7.3973e-10 raw. Thus retaining the evolving coupling/metric response, rather than changing a fitted exponent, resolves this discrepancy.

56 independent algebra/moment identities pass, including coefficient matching, the current's extra integration, and corner jump terms. These are algebraic/numerical checks, not56 new observations. The original90 recent-stage and49 preceding-stage artifacts are hash-preserved.

## Chosen next test

Target original index2924:16 additional intervals, in two manageable eight-interval acquisition blocks2909..2916 and2917..2924. It nearly doubles the present elapsed horizon:
- Baseline0.03945017660593919.
- MTS0.03944843281006172.

This is the largest predeclared candidate within doubling, chosen as a test design, not a theorem that it will pass. More elapsed time stresses the transfer expansion and source history meaningfully; a simple power extrapolation is not authorized.

The next-window-contract.json freezes original bank/grids/tolerances, all17 existing control reports, eight-interaction diagnostic, direct native reference requirements, and recomputation of endpoint gains. No new source has been extrapolated or acquired; no next-stage worker is running.

## Scope and files

DERIVATION.md contains the equations and assumptions. growth_math.py/run_growth.py calculate coefficients and the time-dependent expansion; score_growth.py checks saved histories; select_window.py records the next test. Machine-readable results retain low-order failures as well as the passing result.

This remains a retained-history conditional propagation result. It is not an independent observation, a universal time power, or a continuum-certified error estimate. Everything stays local; the persistent goal remains paused.
