# Pressure-work transport from the retained coupled histories

Private/local, 2026-11-17. No physical trajectory advanced beyond3044.
Previous stage remains the authoritative physical restart. This stage derives
and tests how its field approximation error accumulates into energy exchange.
Original bank, native binary, parameters, grids,934 norms and1e-10/2e-5 gates
remain fixed. No fitting, native rebuild, publication or other-chat action.

## Derived physical quantity

For the existing split e=h+f and pressure operator B_P,

    J_h'=-3 H B_P h, J_f'=-3 H B_P f,
    Delta Wp(t)-Delta Wp(3041)=J_h(t)+J_f(t).

Derived exact original/change forms include background-change cross terms.
The non-cancelling integrals retain inherited and newly generated errors
separately instead of relying on phase cancellation. DERIVATION.md specifies
the pressure normalization, conformal-time units and conditional scope.

The independent comparator is the pressure work already integrated with the
parent and approximate physical equations. It is NOT used to define J_h/J_f.
There is no new closure, fitted time-growth law, averaged pressure or changed
matter action in this calculation.

## Reused evidence and initial result

Reused both32/64 histories over3041..3044:1910 MTS nodes and727 baseline nodes.
Two fresh native owners evaluate actual RHS at saved states; no physical ODE
is reintegrated. The final full RHS and parent restore remain bitwise exact.
Extracted17 physical values/derivatives per node:5 background changes and
old/change heavy-field coordinates for inherited, generated and total error.
Reconstructed pressure differs from saved packets by at most1.89327e-29.

The frozen first diagnostic uses three-node Hermite fields, Gaussian orders
3/5/7 and diagnostic strides1/2/4. Physical work-scale comparisons and all
envelope coverage checks pass, but the branch-change interpolation estimate
is0.0229941 of its tiny error and fails2e-5. Its raw split identity also fails
at4.12196e-10 relative versus1e-10. science-score.json is preserved unchanged.
These failures are neither a new astrophysical exclusion nor hidden passes.

## Derived representation repair and separate test

The supplied reference fields are cubic splines and the clock is piecewise
cubic. A correction which cancels their representation defects need not be
as smooth across their knots as the complete physical field.

PAIRED-BACKGROUND.md derives deltaX_H=H[X0+deltaX]-X0(t), using the EXACT
known reference at each query. It is evaluated with centered, compensated
sums; alpha is reconstructed through deltaa before dividing by local a0.
No physical source curve, bank, tolerance or saved state is modified.

The separately frozen test compares three- and four-node physical-background
Hermite with the same strides and quadrature orders. Endpoint recovery error
is1.29247e-26 for both histories.14 manufactured full-background polynomial
controls pass (in addition to10 initial Hermite controls). Four-node was
selected before this test, not by fitting the saved pressure-work answer.

The remaining branch-change signed-prediction uncertainty falls to
1.5480514e-4 of the tiny error, about148.5 times smaller than the first test.
It STILL exceeds2e-5, and its successive stride differences do not contract.
The branch-change envelope's own precision estimate1.89325e-4 also fails.
These are unresolved diagnostic-resolution issues, recorded separately from
the physical-response error budget. No certified continuum bound is claimed.

## Physical work result

Approximation-minus-parent pressure-work error, accumulated from3041:

| Branch | Predicted final signed error | Working non-cancelling budget relative to parent work |
| --- | ---: | ---: |
| Original | -1.32766643465e-10 | 5.5734880e-7 |
| Coherent | -1.32766853463e-10 | 5.5734998e-7 |
| Coherent minus original | -2.09998390071e-16 | 8.2026932e-7 |

All three physical-response budgets are below the unchanged2e-5 gate; the
largest has about24.4-fold margin. They include interpolation/quadrature,
paired32/64 differences, primitive rounding and the separately computed split
defect. They cover the observed independent work errors at saved epoch ends.

For the branch change, inherited contribution=-4.50986338377e-18 and newly
generated contribution=-2.05488526688e-16. Its non-cancelling integral is
2.16559862613e-15; final working budget2.17638055512e-15. Independent observed
work error=-2.10079326109e-16. These are in retained weighted source/work units,
not observed energies in SI or a claim of improved cosmological fit.

Direct-comparison budgets relative to parent work are1.04479e-11,
1.04461e-11 and3.95190e-9. Relative to the much tinier approximation error
itself, the direct saved-work uncertainty still fails: about3.49e-5 for the
two full branches and0.04993 for their difference. The independent work
accumulators'32/64 difference dominates that last comparison. Do not report
the tiny error as measured to the accuracy of the main physical response.

## Split conservation and baseline

Derived J_e-J_h-J_f=integral -3 H B_P(e-h-f)dt for the actual saved numerical
state residual. The defect is evaluated from error-field coordinates, not
defined by subtracting integrated answers. Defect-accounted identity residuals
are4.56165e-15 /1.33867e-15 /4.55307e-15, below1e-10. The repaired raw split
test also passes; the first experiment's failed zero test remains preserved.
The branch-change defect contribution is only-1.15352e-26 at the final epoch
and is ADDED to, not subtracted from, the displayed working budget.

Baseline32/64 owned cold pressure and pressure work are exactly zero in their
saved source convention. This is structural, not an observed null, and says
nothing about baseline radiation pressure or its unresolved tiny velocity
response. All prior native, slow-sector and source/spectrum limitations remain.

## Verification, runtime issue and cleanup

50 technical checks pass:23 initial and27 paired. They cover input hashes,
cached score replay, exact values/clocks, same endpoints, numerical finiteness,
baseline checks, preserved initial failures, source freeze timing and cleanup
receipts. Fresh native owner count2; no native owner remains active.

One nonphysical runtime failure is retained: a wildcard import replaced the
module alias `original` with a string when scoring the paired integrations.
All36 paired integration trials and both endpoint checks had completed.
recover_paired_score.py restores only the module binding and scores those
cached files. It does NOT repeat quadrature, alter formulas or run new physics.
The original source, hashes and failure receipt remain; the recovery is explicit.

At closeout require10 exact worker identities exited (9 completed,1 inspected
scoring failure),2 native owners cleared, no bytecode or temporary apps/tools.
Independently verify artifact hashes and foreground closer exit. The sealed
physical3044 restart remains in the preceding stage, never overwritten here.

NEXT.md gives a route which avoids another round of increasingly high-order
offline interpolation: accumulate the derived work using accepted live-step
dense output, carrying this stage's finite3044 contributions and uncertainties.
