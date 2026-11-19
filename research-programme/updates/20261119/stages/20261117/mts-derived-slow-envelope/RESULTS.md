# Derived slow response: second-order phase correction passes both saved windows

Completed 2026-11-17. The previous goal turn and this turn made verified
progress. The retained theory, couplings and initial physical states are
unchanged; no new physical parameter or observational fit was introduced.

## Derived, rather than assumed

DERIVATION.md gives an exact rotating-frame equation for the retained scalar
perturbation. Its free relative frequency is

    delta=sqrt((am)^2+k^2)-am=k^2/[sqrt((am)^2+k^2)+am],

not an imposed dust/sound-speed relation. Actual expansion, background phase,
representation contacts and metric forcing remain explicit. Physical density,
current and pressure are reconstructed from both field coordinates, preserving
the fast phase and finite pressure endpoints.

The integrated coefficient corrections K1 and K2 follow a recurrence derived
from that equation, with fixed zero initial coefficient corrections and the
exact physical initial state. They contain no fitted coefficients. Their
omitted term is exactly C K_p v_p. A logarithmic-norm equation bounds its effect;
an independent integrated-coefficient bound controls invertibility. This is a
finite, conditional approximation to the existing fields, not a new field law.

## Tests and results

The approximation and orders0/1/2 were frozen before comparison. Sixteen MTS
replays cover old/coherent branches, both saved3038..3039 and3039..3040 windows,
32/64 step caps and stride1/2/4 reconstruction. Each simultaneously evolves the
primitive field, exact envelope and all three frozen approximation orders.
Twenty-four baseline controls reuse the same supplied-metric convention.
All preserve the bank, native binary, original934 norms, source clocks and
1e-10 algebra /2e-5 numerical gates. There is no new full-hierarchy evolution.

The following are budgets divided by the ORIGINAL frozen density-source norm,
not fractional errors relative to instantaneous density or observed data:

| Coherent branch | Bare envelope | First correction | Second correction |
|---|---:|---:|---:|
| 3038..3039 density | 1.04296e-2 | 7.43000e-5 | 1.16489e-5 |
| 3039..3040 density | 8.87056e-3 | 1.01551e-4 | 1.23142e-5 |

Bare evolution fails density, current, pressure and integrated pressure on both
windows and both branches. First correction fails density everywhere and also
coherent pressure in the second window. These are preserved approximation
failures, not adjusted tolerances or discarded experiments.

Second correction passes all physical-source and integrated-pressure gates on
both branches/windows. The largest coherent pressure budgets are1.21730e-5
and1.28450e-5; integrated-pressure budgets are1.53069e-8 and1.56010e-8.
The exact primitive/envelope controls also pass. Their coherent reconstruction
budgets are already about1.2e-5: saved-forcing interpolation, rather than the
second-order truncation, dominates this working full-source allowance.

The derived second-order truncation-bound budget is at most5.35364e-7 in frozen
density units across these windows; first order reaches9.52679e-5 and fails.
Observed exact-envelope/truncation discrepancies remain within the evaluated
bounds up to the unchanged algebra allowance. As an additional conservative
check, combine the exact-replay budget AND the truncation-bound budget by the
triangle inequality. The largest combined second-order source ratio is
1.28979425e-5, still below2e-5. Only order2 is accepted by both score definitions.
See science-score.json and combined-budget.json; no threshold was changed.

Baseline density budgets are4.96149e-14 and7.47748e-14 for the two windows;
owned current and pressure stay structural zero. This does not resolve the
baseline's previously unresolved tiny coherent-minus-original correction.

## Physical scale separation and validity

At saved nodes, mu spans34.0484..34.7549 Mpc^-1, whereas the exact beat spans
0.357820..0.365167 Mpc^-1. The beat/mu ratio is at most0.010725, H/mu at most
0.00037457, and k/mu at most0.14685. These diagnose a real separation of carrier
and relative-phase timescales in this particular saved regime, not universally.

The integrated coefficient norm L reaches0.0204096 and0.0297281; the conservative
order2 inverse condition L+L^2/2<1 passes. Actual K1 norm is at most0.00108645,
K2 at most9.81518e-6. Their smallness is derived and tested, not fitted. The
coefficient matrices are not reset inside either window. Each window is a
separately matched replay, so this does NOT establish long-run accumulated
accuracy across many reset windows.

## Scope, verification and preserved limitations

These calculations use saved future background and metric histories. They are
conditional replays, not forecasts or new observed-universe tests. The error
inequality is mathematical for exact integration of the declared continuous
coefficients. Its numerical evaluation and history-error allowances here are
working estimates, not rigorous continuum enclosures. In a live evolution,
metric/source feedback also changes the forcing and needs its own test or
coupled error estimate; the conditional bound cannot simply be transplanted.

The full scalar phase/stress is reconstructed, so this is not a pressureless
closure. It is also not a demonstrated speed-up: the forcing and coefficient
corrections still contain fast variation. No occupation prescription, quantum
measure, new local-GR/sky likelihood or galaxy fit is supplied by this stage.
Earlier independent-native discrepancies, slow-sector self-normalized failures
and the87.5966% projected source uncertainty remain separate. The old slow-stress
bound has not been extended to3040 by these calculations.

125 algebra/analytic controls,727 technical verification checks and the
additional combined-budget/support checks pass. The initial NumPy Boolean
report-serialization failure was repaired BEFORE comparison; original source,
failure receipt and unchanged norms are preserved in PREPARATION-REPAIR.md.
The results are saved locally. cleanup.json/closeout.json record exact worker
exits, unchanged input hashes and sealed artifacts; no GitHub, native-owner
creation, browser/server or other-chat process action occurred.
