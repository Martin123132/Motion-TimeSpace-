# Scalar pressure accounted for from the retained field equations

17 November2026. This stage reuses the complete3038..3039 histories; no new
coupled evolution, native binary, bank, parameter, report grid or fit.

## Owned heavy scalar: independent work identity closes

The derived endpoint/expansion/gradient/metric/contact decomposition agrees
with the separately saved integrated pressure-work variable. Across every
saved diagnostic time, residual plus conservative working quadrature,
sampling, paired32/64 and rounding allowances gives:

| Branch | Error / original heavy density norm | Gate |
|---|---:|---:|
| Original represented background | 2.02685e-10 | 2e-5 |
| Coherent coupled background | 5.93176e-10 | 2e-5 |

Direct pressure quadrature is a separate crosscheck:1.25839e-8 and2.76491e-8
of the same density norm, also passing. Stride1/2/4 interpolation differences
shrink. These are tested numerical estimates, not a rigorous uniform
trajectory enclosure.

Final coherent weighted-pressure integral:

| Contribution | Value in the saved source-work normalization |
|---|---:|
| Independent saved integral | +2.85148730e-5 |
| Endpoint term | +3.03744286e-5 |
| Expansion term | +9.16873508e-8 |
| Spatial gradient | -2.08224667e-6 |
| Metric forcing | +1.31003921e-7 |
| Original representation contacts | 0 on coherent branch |

The original branch retains its small+5.52872e-11 contact contribution.
The endpoint term is106.52% of the final coherent total; the other terms
partly cancel it. Omitting the endpoint OR gradient term is detected by the
unchanged gate. Omitting metric, expansion or old contacts individually is
not detected by that broad gate; do not describe all pieces as independently
required by this numerical test.

Deleting pressure from the density-exchange accounting produces a maximum
error1.05394e-2 of the original heavy density-source norm, about527 times
the2e-5 tolerance. Thus a zero-pressure substitution is not justified on
this finite, non-integer-cycle interval.

After retaining and separating the boundary contribution, the bulk integral
is approximately-0.005168 of the time-integrated absolute density-source
weight. This is a finite-window perturbation diagnostic, NOT an equation of
state, sound speed, observational result or universal dust limit.

## Baseline and slow-field controls: preserve the distinction

Native primitive stresses, actual background H derivatives and endpoint
field RHS checks pass for the slow scalar in BOTH baseline and MTS.
The owned cold-fluid pressure is structurally zero.

The slow scalar's integrated multi-term identity does NOT meet its own tiny
normalization. Gradient and metric integrals of order1e-12 cancel toward
pressure integrals of order1e-28. Saved double-precision states and finite
sampling cannot resolve that cancellation at2e-5 of a1e-26..1e-25 source.
All four old/coherent slow-only failures remain in science-score.json.

We addressed the separate system-impact question constructively rather than
renormalizing those failures. The exact inequality

|P_s| <= |V_s g_s| + a^2 m_s^2 |Phi_s f_s|

gives a positive bound on its pressure-work contribution without the large
gradient/metric subtraction. The authoritative outward-rounded implementation
encloses all declared32/64 and stride1/2/4 reconstructions.

Largest slow pressure contribution to density exchange, relative to a separately
frozen ORIGINAL934 L1 species-density norm:

| Case | Original | Coherent |
|---|---:|---:|
| Baseline | 3.04987e-29 | 3.04905e-29 |
| MTS | 7.99818e-29 | 1.46631e-28 |

These bounds are conditional on the represented/interpolated histories,
not rigorous enclosures of the unknown continuum ODE error. They show why
the failed slow self-scale cancellation does not by itself establish a
material error in this window's total stress. They neither turn the original
identity failures into passes nor authorize deleting the slow field at later
epochs.

## Verification and reuse

158 main technical checks and42 independent bound checks pass, including
exact score/bound replay, rational Bernstein-control tests, native stress
parity and unchanged inputs. The heavy independent identity passes; all
identity budgets together remain false because of the preserved slow checks.

1147 inherited/frozen input entries remain unchanged. Two preparation
implementation errors (boolean serialization and a missing parenthesis)
were fixed before pressure comparisons, with failed receipts retained.
The first bound implementation is superseded by slow_bound_outward.py:
rounding directions for subtraction and denominator minima were tightened;
both versions remain recorded.

No old research files were edited. No native worker, publication, browser,
scheduler, other-chat process or external download was needed.
See cleanup.json and closeout.json for final task-worker exits and hashes.
